"""Post a single RapidAPI promotion tweet via X API v2."""

import json
import sys
from pathlib import Path
from requests_oauthlib import OAuth1Session

CREDS_FILE = Path(r"C:\Users\tmizu\マイドライブ\GitHub\claude-code\sites\nambei-oyaji.com\config\x-credentials.json")

TWEET_TEXT = (
    "SEO Analyzer API - instant technical audit for any URL.\n\n"
    "Check meta tags, headings, links, mobile & performance. JSON response, free tier included.\n\n"
    "https://rapidapi.com/t-mizuno27/api/seo-analyzer-api\n\n"
    "#API #SEO #WebDev"
)


def main():
    if not CREDS_FILE.exists():
        print(f"ERROR: {CREDS_FILE} not found")
        sys.exit(1)

    creds = json.loads(CREDS_FILE.read_text(encoding="utf-8"))

    oauth = OAuth1Session(
        client_key=creds["api_key"],
        client_secret=creds["api_key_secret"],
        resource_owner_key=creds["access_token"],
        resource_owner_secret=creds["access_token_secret"],
    )

    url = "https://api.twitter.com/2/tweets"
    payload = {"text": TWEET_TEXT}

    print(f"Posting tweet ({len(TWEET_TEXT)} chars)...")
    resp = oauth.post(url, json=payload)

    if resp.status_code in (200, 201):
        data = resp.json()
        tweet_id = data.get("data", {}).get("id", "unknown")
        print(f"SUCCESS: Tweet posted! ID={tweet_id}")
        print(f"URL: https://x.com/nambei_oyaji/status/{tweet_id}")
    else:
        print(f"ERROR: {resp.status_code}")
        print(resp.text)
        sys.exit(1)


if __name__ == "__main__":
    main()
