"""
X (Twitter) 自動投稿スクリプト（画像添付対応）
nambei_oyaji アカウント用

使い方:
  # 単発投稿
  python x_poster.py --text "投稿内容"

  # 画像付き投稿
  python x_poster.py --text "投稿内容" --image path/to/image.jpg

  # スケジュールファイルから投稿（現在時刻に合う投稿を実行）
  python x_poster.py --schedule outputs/social/x-schedule-2026-03-05.md

  # スレッド投稿（改行2つで区切り）
  python x_poster.py --thread "1つ目の投稿\n\n2つ目の投稿\n\n3つ目の投稿"

  # ドライラン（実際には投稿しない）
  python x_poster.py --text "テスト" --dry-run
"""

import argparse
import json
import re
import sys
from datetime import datetime
from pathlib import Path

try:
    import tweepy
except ImportError:
    print("ERROR: tweepy がインストールされていません")
    print("  pip install tweepy")
    sys.exit(1)


CONFIG_DIR = Path(__file__).parent.parent.parent / "config"
CREDENTIALS_FILE = CONFIG_DIR / "x-credentials.json"
LOG_DIR = Path(__file__).parent.parent.parent / "outputs" / "social"


def load_credentials() -> dict:
    """X API認証情報を読み込む"""
    if not CREDENTIALS_FILE.exists():
        print(f"ERROR: 認証ファイルが見つかりません: {CREDENTIALS_FILE}")
        print("blog/config/x-credentials.json を作成してください")
        sys.exit(1)

    with open(CREDENTIALS_FILE, "r", encoding="utf-8") as f:
        creds = json.load(f)

    required = ["api_key", "api_key_secret", "access_token", "access_token_secret"]
    missing = [k for k in required if not creds.get(k)]
    if missing:
        print(f"ERROR: 認証情報に不足があります: {', '.join(missing)}")
        sys.exit(1)

    return creds


def get_api(creds: dict) -> tweepy.API:
    """Tweepy v1.1 API を取得"""
    auth = tweepy.OAuth1UserHandler(
        creds["api_key"],
        creds["api_key_secret"],
        creds["access_token"],
        creds["access_token_secret"],
    )
    return tweepy.API(auth)


def post_tweet(api: tweepy.API, text: str, reply_to: str = None, image_path: str = None, dry_run: bool = False) -> str | None:
    """1つのツイートを投稿する。成功時はtweet IDを返す"""
    if len(text) > 280:
        print(f"WARNING: 文字数が280を超えています ({len(text)}文字)。投稿をスキップします")
        return None

    if dry_run:
        print(f"[DRY RUN] 投稿内容 ({len(text)}文字):")
        print(f"  {text}")
        if image_path:
            print(f"  (画像: {image_path})")
        if reply_to:
            print(f"  (リプライ先: {reply_to})")
        return "dry-run-id"

    try:
        kwargs = {"status": text}
        if reply_to:
            kwargs["in_reply_to_status_id"] = reply_to
        if image_path:
            media = api.media_upload(filename=image_path)
            kwargs["media_ids"] = [media.media_id]
            print(f"画像アップロード完了: {Path(image_path).name}")
        status = api.update_status(**kwargs)
        tweet_id = str(status.id)
        print(f"OK: 投稿成功 (ID: {tweet_id})")
        return tweet_id
    except tweepy.errors.TweepyException as e:
        print(f"ERROR: 投稿失敗 - {e}")
        return None


def post_thread(api: tweepy.API, texts: list[str], dry_run: bool = False) -> list[str]:
    """スレッド形式で連続投稿"""
    tweet_ids = []
    reply_to = None

    for i, text in enumerate(texts, 1):
        print(f"\n--- スレッド {i}/{len(texts)} ---")
        tweet_id = post_tweet(api, text, reply_to=reply_to, dry_run=dry_run)
        if tweet_id:
            tweet_ids.append(tweet_id)
            reply_to = tweet_id
        else:
            print(f"WARNING: スレッド {i} で中断")
            break

    return tweet_ids


def parse_schedule_file(filepath: str, target_hour: int = None) -> list[dict]:
    """
    スケジュールMDファイルから投稿を抽出する。
    target_hour が指定された場合、その時間帯の投稿のみを返す。
    """
    path = Path(filepath)
    if not path.exists():
        print(f"ERROR: スケジュールファイルが見つかりません: {filepath}")
        return []

    content = path.read_text(encoding="utf-8")
    posts = []

    # パターン: ### 投稿N（朝7:30）[カテゴリ] の後に本文
    pattern = r"### 投稿\d+（[^）]*?(\d{1,2}):\d{2}）\[([^\]]+)\]\s*\n(.*?)(?=\n###|\n## |\Z)"
    matches = re.finditer(pattern, content, re.DOTALL)

    for m in matches:
        hour = int(m.group(1))
        category = m.group(2)
        text = m.group(3).strip()

        # 【写真: ...】の行を除去（写真は別途対応が必要）
        text = re.sub(r"【写真:.*?】\s*", "", text).strip()

        if target_hour is not None and hour != target_hour:
            continue

        posts.append({
            "hour": hour,
            "category": category,
            "text": text,
        })

    return posts


def log_post(text: str, tweet_id: str, category: str = "manual"):
    """投稿ログを保存"""
    LOG_DIR.mkdir(parents=True, exist_ok=True)
    log_file = LOG_DIR / "x-post-log.jsonl"

    entry = {
        "timestamp": datetime.now().isoformat(),
        "tweet_id": tweet_id,
        "category": category,
        "text": text,
        "char_count": len(text),
    }

    with open(log_file, "a", encoding="utf-8") as f:
        f.write(json.dumps(entry, ensure_ascii=False) + "\n")


def main():
    parser = argparse.ArgumentParser(description="X (Twitter) 自動投稿 - nambei_oyaji")
    parser.add_argument("--text", type=str, help="投稿するテキスト")
    parser.add_argument("--thread", type=str, help="スレッド投稿（\\n\\nで区切り）")
    parser.add_argument("--schedule", type=str, help="スケジュールMDファイルのパス")
    parser.add_argument("--hour", type=int, help="スケジュールから特定の時間帯の投稿のみ実行")
    parser.add_argument("--image", type=str, help="添付する画像ファイルのパス")
    parser.add_argument("--dry-run", action="store_true", help="実際には投稿しない")
    args = parser.parse_args()

    if not any([args.text, args.thread, args.schedule]):
        parser.print_help()
        sys.exit(1)

    if args.image and not Path(args.image).exists():
        print(f"ERROR: 画像ファイルが見つかりません: {args.image}")
        sys.exit(1)

    creds = load_credentials()
    api = get_api(creds)

    if args.text:
        tweet_id = post_tweet(api, args.text, image_path=args.image, dry_run=args.dry_run)
        if tweet_id and not args.dry_run:
            log_post(args.text, tweet_id)

    elif args.thread:
        texts = [t.strip() for t in args.thread.split("\\n\\n") if t.strip()]
        tweet_ids = post_thread(api, texts, dry_run=args.dry_run)
        if tweet_ids and not args.dry_run:
            for text, tid in zip(texts, tweet_ids):
                log_post(text, tid, category="thread")

    elif args.schedule:
        posts = parse_schedule_file(args.schedule, target_hour=args.hour)
        if not posts:
            print("投稿対象が見つかりません")
            sys.exit(0)

        print(f"{len(posts)} 件の投稿が見つかりました")
        for post in posts:
            print(f"\n--- [{post['category']}] {post['hour']}時台 ---")
            tweet_id = post_tweet(api, post["text"], dry_run=args.dry_run)
            if tweet_id and not args.dry_run:
                log_post(post["text"], tweet_id, category=post["category"])


if __name__ == "__main__":
    main()
