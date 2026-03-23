"""
X (Twitter) posting script for @prodhq27
Usage: python x_post.py "Tweet text here"
"""

import tweepy
import json
import os
import sys

CRED_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "config", "x-credentials.json")

with open(CRED_PATH, "r") as f:
    creds = json.load(f)

client = tweepy.Client(
    consumer_key=creds["api_key"],
    consumer_secret=creds["api_key_secret"],
    access_token=creds["access_token"],
    access_token_secret=creds["access_token_secret"],
)

if __name__ == "__main__":
    text = sys.argv[1] if len(sys.argv) > 1 else "test"
    response = client.create_tweet(text=text)
    print(f"OK: Tweet posted! ID: {response.data['id']}")
