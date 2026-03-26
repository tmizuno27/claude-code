"""
X Auto-Poster V2 for @prodhq27
Runs via Task Scheduler at 10:00, 14:00, 19:00 PYT

Improvements over V1:
- 5 tweet categories: value, promo, thread, engagement, seasonal
- Auto-reset cycle when all tweets in a category are posted
- Thread posting support (multi-tweet threads)
- Day-of-week awareness (threads Tue/Thu, engagement Sat/Sun)
- Healthchecks.io ping on success
- Dry-run mode for testing
- Stats command to see posting progress

Usage:
  python x_auto_post_v2.py              # Normal auto-post
  python x_auto_post_v2.py --dry-run    # Preview without posting
  python x_auto_post_v2.py --stats      # Show posting stats
  python x_auto_post_v2.py --type promo # Force specific type
"""

import tweepy
import json
import os
import sys
import time
import re
import random
from datetime import datetime, timedelta
from copy import deepcopy

try:
    import anthropic
except ImportError:
    anthropic = None

BASE_DIR = os.path.dirname(os.path.dirname(__file__))
CRED_PATH = os.path.join(BASE_DIR, "config", "x-credentials.json")
SCHEDULE_PATH = os.path.join(BASE_DIR, "config", "x-schedule-v2.json")
LOG_DIR = os.path.join(os.path.dirname(os.path.dirname(BASE_DIR)), "logs")
os.makedirs(LOG_DIR, exist_ok=True)
LOG_PATH = os.path.join(LOG_DIR, "x-prodhq27-posts.log")

# Optional: Healthchecks.io ping URL (set in config or env)
HEALTHCHECK_URL = os.environ.get("HEALTHCHECK_X_POST", "")
SECRETS_PATH = os.path.join(BASE_DIR, "config", "secrets.json")

# Products for dynamic tweet generation
PRODUCTS = [
    {"name": "Freelance Business OS", "price": "$19", "benefit": "Track clients, projects, invoices, and income in one dashboard. Stop juggling 5 different apps."},
    {"name": "Content Creator Dashboard", "price": "$17", "benefit": "Plan, create, and schedule content across platforms. See what performs and what doesn't."},
    {"name": "Student Study Hub", "price": "$9", "benefit": "Track assignments, study hours, and grades. Know exactly where to focus before exams."},
    {"name": "Life OS / Second Brain", "price": "$19", "benefit": "Capture everything — tasks, notes, goals, habits — in one connected system."},
    {"name": "Small Business CRM", "price": "$19", "benefit": "Manage leads, deals, and follow-ups without paying $50+/mo for bloated CRM software."},
    {"name": "Side Hustle Tracker", "price": "$14", "benefit": "Track multiple income streams, expenses, and hourly rates. Know your REAL profit per project."},
    {"name": "Social Media Planner", "price": "$14", "benefit": "Batch-create a month of content in one sitting. Never stare at a blank screen again."},
    {"name": "Job Search Tracker", "price": "$9", "benefit": "Track applications, interviews, follow-ups, and offers. Stop losing opportunities in your inbox."},
    {"name": "Digital Products OS", "price": "$19", "benefit": "Manage your entire digital product business — from idea to launch to revenue tracking."},
    {"name": "Ultimate Bundle (15 templates)", "price": "$49 (75% OFF)", "benefit": "Every Notion template we make, for the price of two. One purchase, complete workspace."},
]

PRODHQ_SYSTEM_PROMPT = """You are a tweet writer for @prodhq27, a Notion template seller on Gumroad.

## Voice & Tone
- Direct, no-fluff, slightly opinionated
- Speak from experience (as a productivity nerd who builds systems)
- Use concrete numbers and specific examples
- Never sound salesy or desperate. Sound like someone sharing what works

## Tweet Types & Guidelines

### VALUE tweets (most common)
Give genuinely useful productivity/Notion tips. The goal is to make people think "this person knows their stuff" so they check your profile.
- Share a specific workflow, hack, or insight
- Include a concrete number or timeframe when possible
- End with a thought that makes people want to reply or save

### PROMO tweets (product promotion)
Highlight a specific PROBLEM the product solves, not features.
- Lead with the pain point ("Tracking clients in spreadsheets?")
- Show the transformation ("→ One dashboard. Every client, project, and invoice.")
- Include the Gumroad link naturally: tatsuya27.gumroad.com
- Price anchoring: compare to expensive alternatives

### ENGAGEMENT tweets
Designed to get replies and discussion.
- Ask a genuine question about productivity struggles
- Share a controversial take on popular tools/methods
- "Unpopular opinion:" or "Hot take:" format works well

## Rules
1. Max 280 characters
2. 1-2 hashtags maximum (or zero)
3. No emojis spam (0-2 max)
4. No generic motivational fluff
5. Sound like a real person, not a brand
6. Every tweet should make someone want to follow you OR visit your Gumroad

## Output
Return ONLY the tweet text. No explanations."""


def generate_dynamic_tweet(category: str) -> str | None:
    """Generate a tweet dynamically using Claude API when static tweets are exhausted."""
    if anthropic is None:
        return None
    if not os.path.exists(SECRETS_PATH):
        return None

    try:
        with open(SECRETS_PATH, "r", encoding="utf-8") as f:
            secrets = json.load(f)
        api_key = secrets.get("claude_api", {}).get("api_key")
        if not api_key:
            return None
    except Exception:
        return None

    product = random.choice(PRODUCTS)

    prompts_by_category = {
        "value": f"Write a VALUE tweet. Share a genuinely useful productivity or Notion tip. Make it specific and actionable. Today is {datetime.now().strftime('%B %d, %Y')}.",
        "promo": f"Write a PROMO tweet for: {product['name']} ({product['price']}). Benefit: {product['benefit']}. Link: tatsuya27.gumroad.com. Lead with the problem it solves.",
        "engagement": "Write an ENGAGEMENT tweet. Ask a question or share a hot take about productivity tools, workflows, or remote work that will get people replying.",
        "thread": f"Write a VALUE tweet (single tweet, not a thread). Share a framework or system for productivity. Today is {datetime.now().strftime('%B %d, %Y')}.",
        "seasonal": f"Write a VALUE tweet relevant to {datetime.now().strftime('%B %Y')}. Connect it to seasonal productivity themes (Q1 goals, new year, summer planning, etc.).",
    }

    user_prompt = prompts_by_category.get(category, prompts_by_category["value"])

    # Get recent posted tweets to avoid repetition
    try:
        data = load_schedule()
        recent = [t["text"][:80] for t in data["tweets"] if t.get("posted") and t.get("posted_at")]
        recent = sorted(recent, key=lambda x: x, reverse=True)[:5]
        if recent:
            user_prompt += "\n\nAvoid similar content to these recent posts:\n" + "\n".join(f"- {r}" for r in recent)
    except Exception:
        pass

    try:
        client = anthropic.Anthropic(api_key=api_key)
        response = client.messages.create(
            model="claude-sonnet-4-6",
            max_tokens=256,
            system=PRODHQ_SYSTEM_PROMPT,
            messages=[{"role": "user", "content": user_prompt}],
        )
        text = response.content[0].text.strip()
        if text.startswith('"') and text.endswith('"'):
            text = text[1:-1]
        return text
    except Exception as e:
        log(f"WARNING: Claude API generation failed: {e}")
        return None


def log(msg):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    line = f"[{timestamp}] {msg}"
    print(line)
    with open(LOG_PATH, "a", encoding="utf-8") as f:
        f.write(line + "\n")


def get_client():
    with open(CRED_PATH, "r") as f:
        creds = json.load(f)
    return tweepy.Client(
        consumer_key=creds["api_key"],
        consumer_secret=creds["api_key_secret"],
        access_token=creds["access_token"],
        access_token_secret=creds["access_token_secret"],
    )


def load_schedule():
    with open(SCHEDULE_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


def save_schedule(data):
    with open(SCHEDULE_PATH, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


def get_next_tweet(tweets, category):
    """Get next unposted tweet of given category."""
    for tweet in tweets:
        if tweet["category"] == category and not tweet.get("posted", False):
            return tweet
    return None


def count_tweets(tweets, category=None):
    """Count posted/total tweets, optionally filtered by category."""
    filtered = tweets if category is None else [t for t in tweets if t["category"] == category]
    posted = sum(1 for t in filtered if t.get("posted", False))
    return posted, len(filtered)


def reset_category(tweets, category):
    """Reset all tweets in a category to unposted for a new cycle."""
    reset_count = 0
    for tweet in tweets:
        if tweet["category"] == category and tweet.get("posted", False):
            tweet["posted"] = False
            tweet.pop("posted_at", None)
            tweet.pop("tweet_id", None)
            tweet["cycle"] = tweet.get("cycle", 0) + 1
            reset_count += 1
    return reset_count


def determine_category(now):
    """Determine tweet category based on time and day of week."""
    hour = now.hour
    weekday = now.weekday()  # 0=Mon, 6=Sun

    if hour < 12:
        # 10:00 slot
        if weekday in (5, 6):  # Sat/Sun
            return "engagement"
        return "value"
    elif hour < 16:
        # 14:00 slot
        if weekday in (1, 3):  # Tue/Thu
            return "thread"
        return "value"
    else:
        # 19:00 slot
        day_of_year = now.timetuple().tm_yday
        if day_of_year % 2 == 0:
            return "promo"
        return "value"


def post_thread(client, tweet):
    """Post a multi-tweet thread. Returns list of tweet IDs."""
    parts = tweet["text"].split("\n---\n")
    tweet_ids = []
    reply_to = None

    for i, part in enumerate(parts):
        text = part.strip()
        if not text:
            continue
        if reply_to:
            response = client.create_tweet(text=text, in_reply_to_tweet_id=reply_to)
        else:
            response = client.create_tweet(text=text)
        tid = response.data["id"]
        tweet_ids.append(str(tid))
        reply_to = tid
        if i < len(parts) - 1:
            time.sleep(5)  # Longer pause to avoid rate limits on Free plan

    return tweet_ids


def ping_healthcheck(success=True):
    """Ping Healthchecks.io if URL is configured."""
    if not HEALTHCHECK_URL:
        return
    try:
        import urllib.request
        url = HEALTHCHECK_URL if success else f"{HEALTHCHECK_URL}/fail"
        urllib.request.urlopen(url, timeout=10)
    except Exception:
        pass  # Non-critical


def show_stats(data):
    """Display posting statistics."""
    tweets = data["tweets"]
    categories = ["value", "promo", "thread", "engagement", "seasonal"]

    print("\n=== @prodhq27 Posting Stats ===\n")
    for cat in categories:
        posted, total = count_tweets(tweets, cat)
        remaining = total - posted
        bar = "#" * posted + "." * remaining
        print(f"  {cat:12s} [{bar}] {posted}/{total}")

    posted_all, total_all = count_tweets(tweets)
    print(f"\n  {'TOTAL':12s} {posted_all}/{total_all} posted")
    print(f"  Days of content remaining: ~{(total_all - posted_all) // 3}")

    # Last 5 posts
    posted_tweets = sorted(
        [t for t in tweets if t.get("posted_at")],
        key=lambda t: t["posted_at"],
        reverse=True,
    )
    if posted_tweets:
        print("\n  Last 5 posts:")
        for t in posted_tweets[:5]:
            label = t.get("product", t["category"])
            print(f"    {t['posted_at']} [{t['category']}] {label}")
    print()


COOLDOWN_MINUTES = 15
# X API Free plan: 17 tweets per 24 hours (official limit)
DAILY_TWEET_LIMIT = 15  # Conservative limit to avoid hitting 17


def get_last_post_time():
    """Read last successful post timestamp from log file."""
    if not os.path.exists(LOG_PATH):
        return None
    try:
        with open(LOG_PATH, "r", encoding="utf-8") as f:
            lines = f.readlines()
        for line in reversed(lines):
            if "OK:" in line or "OK THREAD:" in line:
                match = re.search(r"\[(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2})\]", line)
                if match:
                    return datetime.strptime(match.group(1), "%Y-%m-%d %H:%M:%S")
        return None
    except Exception:
        return None


def count_posts_last_24h():
    """Count successful posts in the last 24 hours from log file."""
    if not os.path.exists(LOG_PATH):
        return 0
    cutoff = datetime.now() - timedelta(hours=24)
    count = 0
    try:
        with open(LOG_PATH, "r", encoding="utf-8") as f:
            for line in f:
                if "OK:" in line or "OK THREAD:" in line or "POSTED id=" in line:
                    match = re.search(r"\[(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2})\]", line)
                    if match:
                        ts = datetime.strptime(match.group(1), "%Y-%m-%d %H:%M:%S")
                        if ts >= cutoff:
                            count += 1
    except Exception:
        pass
    return count


def main():
    args = sys.argv[1:]
    dry_run = "--dry-run" in args
    show_stats_flag = "--stats" in args
    force_type = None

    for i, arg in enumerate(args):
        if arg == "--type" and i + 1 < len(args):
            force_type = args[i + 1]

    data = load_schedule()

    if show_stats_flag:
        show_stats(data)
        return

    now = datetime.now()

    # Duplicate post prevention: skip if last post was within COOLDOWN_MINUTES
    if not dry_run:
        last_post = get_last_post_time()
        if last_post and (now - last_post) < timedelta(minutes=COOLDOWN_MINUTES):
            elapsed = int((now - last_post).total_seconds() / 60)
            log(f"SKIP: Last post was {elapsed}min ago (cooldown: {COOLDOWN_MINUTES}min). Aborting.")
            return

        # Daily rate limit check (Free plan: 17 tweets/24h, using conservative limit)
        posts_24h = count_posts_last_24h()
        if posts_24h >= DAILY_TWEET_LIMIT:
            log(f"SKIP: {posts_24h} posts in last 24h (limit: {DAILY_TWEET_LIMIT}). Rate limit protection.")
            return

    # Determine category
    category = force_type if force_type else determine_category(now)

    tweet = get_next_tweet(data["tweets"], category)

    # If category exhausted, auto-reset cycle
    if tweet is None:
        posted, total = count_tweets(data["tweets"], category)
        if total > 0 and posted == total:
            reset_count = reset_category(data["tweets"], category)
            log(f"CYCLE RESET: {category} ({reset_count} tweets reset for new cycle)")
            save_schedule(data)
            tweet = get_next_tweet(data["tweets"], category)

    # Fallback chain: value -> engagement -> promo
    if tweet is None:
        for fallback in ["value", "engagement", "promo", "seasonal"]:
            if fallback != category:
                tweet = get_next_tweet(data["tweets"], fallback)
                if tweet:
                    log(f"FALLBACK: No {category} tweets, using {fallback}")
                    break

    # Dynamic generation fallback: if no static tweets, generate with Claude API
    use_dynamic = False
    dynamic_text = None
    if tweet is None:
        log(f"No static tweets for {category}. Attempting Claude API dynamic generation...")
        dynamic_text = generate_dynamic_tweet(category)
        if dynamic_text:
            use_dynamic = True
            log(f"DYNAMIC [{category}]: {dynamic_text[:100]}...")
        else:
            log("No unposted tweets remaining and dynamic generation failed. Refill schedule.")
            ping_healthcheck(success=False)
            return

    if dry_run:
        if use_dynamic:
            log(f"DRY RUN (dynamic): [{category}] - {dynamic_text[:100]}...")
        else:
            preview = tweet["text"][:100].replace("\n", " ")
            product = tweet.get("product", "")
            log(f"DRY RUN: [{tweet['category']}] {product} - {preview}...")
        return

    try:
        client = get_client()

        if use_dynamic:
            response = client.create_tweet(text=dynamic_text)
            tweet_id = response.data["id"]
            log(f"OK (dynamic): [{category}] - Tweet ID: {tweet_id}")
        else:
            is_thread = tweet.get("is_thread", False)

            # On Free plan, threads consume multiple tweets from daily quota.
            # If a thread has >3 parts, post just the first part as a standalone tweet.
            if is_thread:
                parts = tweet["text"].split("\n---\n")
                if len(parts) > 3:
                    log(f"THREAD TRUNCATED: {len(parts)} parts → posting first part only (Free plan safety)")
                    is_thread = False
                    tweet["text"] = parts[0].strip()

            if is_thread:
                tweet_ids = post_thread(client, tweet)
                tweet["posted"] = True
                tweet["posted_at"] = now.strftime("%Y-%m-%d %H:%M:%S")
                tweet["tweet_id"] = tweet_ids[0]
                tweet["thread_ids"] = tweet_ids
                save_schedule(data)
                product = tweet.get("product", "")
                label = f"[{tweet['category']}] {product}" if product else f"[{tweet['category']}]"
                log(f"OK THREAD: {label} - {len(tweet_ids)} tweets - Root ID: {tweet_ids[0]}")
            else:
                response = client.create_tweet(text=tweet["text"])
                tweet_id = response.data["id"]
                tweet["posted"] = True
                tweet["posted_at"] = now.strftime("%Y-%m-%d %H:%M:%S")
                tweet["tweet_id"] = str(tweet_id)
                save_schedule(data)
                product = tweet.get("product", "")
                label = f"[{tweet['category']}] {product}" if product else f"[{tweet['category']}]"
                log(f"OK: {label} - Tweet ID: {tweet_id}")

        ping_healthcheck(success=True)

    except tweepy.errors.Forbidden as e:
        log(f"ERROR: 403 Forbidden\n{e}")
        log("HINT: X API Free plan rate limit likely hit. Will retry next scheduled slot.")
        ping_healthcheck(success=False)
        # Don't exit(1) — let Task Scheduler report success so it retries next slot
    except Exception as e:
        log(f"ERROR: {e}")
        ping_healthcheck(success=False)
        sys.exit(1)


if __name__ == "__main__":
    main()
