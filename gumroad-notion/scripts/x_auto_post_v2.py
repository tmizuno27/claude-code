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
from datetime import datetime
from copy import deepcopy

BASE_DIR = os.path.dirname(os.path.dirname(__file__))
CRED_PATH = os.path.join(BASE_DIR, "config", "x-credentials.json")
SCHEDULE_PATH = os.path.join(BASE_DIR, "config", "x-schedule-v2.json")
LOG_DIR = os.path.join(os.path.dirname(BASE_DIR), "logs")
os.makedirs(LOG_DIR, exist_ok=True)
LOG_PATH = os.path.join(LOG_DIR, "x-prodhq27-posts.log")

# Optional: Healthchecks.io ping URL (set in config or env)
HEALTHCHECK_URL = os.environ.get("HEALTHCHECK_X_POST", "")


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
            time.sleep(2)  # Brief pause between thread tweets

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

    if tweet is None:
        log("No unposted tweets remaining in any category. Refill schedule.")
        ping_healthcheck(success=False)
        return

    if dry_run:
        preview = tweet["text"][:100].replace("\n", " ")
        product = tweet.get("product", "")
        log(f"DRY RUN: [{tweet['category']}] {product} — {preview}...")
        return

    try:
        client = get_client()

        is_thread = tweet.get("is_thread", False)

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

    except Exception as e:
        log(f"ERROR: {e}")
        ping_healthcheck(success=False)
        sys.exit(1)


if __name__ == "__main__":
    main()
