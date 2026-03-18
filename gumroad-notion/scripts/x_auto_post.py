"""
X Auto-Poster for @prodhq27
Runs via Task Scheduler at 10:00, 14:00, 19:00 PYT

Strategy:
- 10:00 PYT (8AM EST): Value tweet
- 14:00 PYT (12PM EST): Value tweet
- 19:00 PYT (5PM EST): Promo tweet (every other day) or Value tweet

Posts the next unposted tweet of the appropriate type,
marks it as posted, and logs the result.
"""

import tweepy
import json
import os
import sys
from datetime import datetime

BASE_DIR = os.path.dirname(os.path.dirname(__file__))
CRED_PATH = os.path.join(BASE_DIR, "config", "x-credentials.json")
SCHEDULE_PATH = os.path.join(BASE_DIR, "config", "x-schedule.json")
LOG_DIR = os.path.join(os.path.dirname(BASE_DIR), "logs")
os.makedirs(LOG_DIR, exist_ok=True)
LOG_PATH = os.path.join(LOG_DIR, "x-prodhq27-posts.log")


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


def get_next_tweet(tweets, tweet_type):
    """Get next unposted tweet of given type."""
    for tweet in tweets:
        if tweet["type"] == tweet_type and not tweet.get("posted", False):
            return tweet
    return None


def should_post_promo():
    """Post promo every other day based on day of year."""
    return datetime.now().timetuple().tm_yday % 2 == 0


def main():
    now = datetime.now()
    hour = now.hour

    # Determine tweet type based on time
    if hour < 12:
        # 10:00 slot - always value
        tweet_type = "value"
    elif hour < 16:
        # 14:00 slot - always value
        tweet_type = "value"
    else:
        # 19:00 slot - promo every other day, value otherwise
        if should_post_promo():
            tweet_type = "promo"
        else:
            tweet_type = "value"

    # Allow override via command line
    if len(sys.argv) > 1:
        tweet_type = sys.argv[1]

    data = load_schedule()
    tweet = get_next_tweet(data["tweets"], tweet_type)

    if tweet is None:
        # Fallback: if no promo left, post value (and vice versa)
        fallback = "value" if tweet_type == "promo" else "promo"
        tweet = get_next_tweet(data["tweets"], fallback)

    if tweet is None:
        log("No unposted tweets remaining. Refill x-schedule.json.")
        return

    try:
        client = get_client()
        response = client.create_tweet(text=tweet["text"])
        tweet_id = response.data["id"]

        # Mark as posted
        tweet["posted"] = True
        tweet["posted_at"] = now.strftime("%Y-%m-%d %H:%M:%S")
        tweet["tweet_id"] = str(tweet_id)
        save_schedule(data)

        product = tweet.get("product", "")
        label = f"[{tweet['type']}] {product}" if product else f"[{tweet['type']}]"
        log(f"OK: {label} - Tweet ID: {tweet_id}")

    except Exception as e:
        log(f"ERROR: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
