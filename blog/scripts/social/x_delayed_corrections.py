#!/usr/bin/env python3
"""
修正投稿スクリプト（1回実行で1件投稿、投稿番号を引数で指定）

使い方:
  python x_delayed_corrections.py 1   # 1件目を投稿
  python x_delayed_corrections.py 2   # 2件目を投稿
  python x_delayed_corrections.py 3   # 3件目を投稿
"""

import json
import sys
from datetime import datetime
from pathlib import Path

import tweepy

CONFIG_DIR = Path(__file__).parent.parent.parent / "config"
LOG_FILE = Path(__file__).parent.parent.parent / "outputs" / "social" / "x-post-log.jsonl"

CORRECTIONS = {
    1: "パラグアイから日本の仕事をリモートでやって約9ヶ月。時差12時間のせいで「日本の朝イチ対応」がこっちの夜になる。最初は不便だと思ってたけど、今は昼間が完全に自分の時間になってる。移住前より集中できてる気がする。 #海外移住 #リモートワーク #海外生活",
    2: "パラグアイから日本の仕事をリモートでやると、時差12時間のおかげで「日本の午前中＝こちらの深夜〜早朝」になる。つまり日中は自分の時間。子どもを学校に送って、アサードの準備して、夕方から仕事。これが今の日常。 #海外移住 #リモートワーク",
    3: "パラグアイ移住の初期費用、よく聞かれるので整理すると——航空券+ビザ関連書類・翻訳・公証で約30万円、銀行預金証明用に約75万円、家賃初月+敷金で10万円前後。トータル約80万円。意外とかかるけど、日本での生活コストを考えたら1年で回収できる。 #パラグアイ移住 #海外移住準備",
}


def main():
    if len(sys.argv) < 2 or sys.argv[1] not in ("1", "2", "3"):
        print("Usage: python x_delayed_corrections.py [1|2|3]")
        sys.exit(1)

    num = int(sys.argv[1])
    text = CORRECTIONS[num]

    creds = json.load(open(CONFIG_DIR / "x-credentials.json", "r", encoding="utf-8"))
    client = tweepy.Client(
        consumer_key=creds["api_key"],
        consumer_secret=creds["api_key_secret"],
        access_token=creds["access_token"],
        access_token_secret=creds["access_token_secret"],
    )

    try:
        response = client.create_tweet(text=text)
        tweet_id = str(response.data["id"])
        print(f"OK: correction #{num} posted (ID: {tweet_id})")

        entry = {
            "timestamp": datetime.now().isoformat(),
            "tweet_id": tweet_id,
            "category": "correction",
            "text": text,
            "char_count": len(text),
        }
        with open(LOG_FILE, "a", encoding="utf-8") as f:
            f.write(json.dumps(entry, ensure_ascii=False) + "\n")

        print("Logged to x-post-log.jsonl")
    except Exception as e:
        print(f"ERROR: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
