"""
X (Twitter) アナリティクス日次レポート生成スクリプト

X Analytics（https://analytics.x.com）からエクスポートしたCSVを読み込み、
日次レポートを生成する。

【使い方】
1. https://analytics.x.com → 「ツイート」→「データをエクスポート」でCSVダウンロード
2. CSVを blog/inputs/x-analytics/ に保存
3. このスクリプトを実行

  # 最新CSVから日次レポート生成
  python scripts/social/x_analytics.py

  # 特定CSVを指定
  python scripts/social/x_analytics.py --csv inputs/x-analytics/tweet_activity.csv

  # 特定日のレポート
  python scripts/social/x_analytics.py --date 2026-03-08

  # API取得モード（Freeプランでは likes/rt のみ。Basicプラン以上で全メトリクス）
  python scripts/social/x_analytics.py --api

【CSVがない場合】
  --api オプションで、Freeプランでも取得可能なデータ（いいね数・RT数）を
  x-post-log.jsonl の各ツイートに対して取得し、レポートを生成する。
  ※インプレッション数はFreeプランでは取得不可（0と表示）

【出力先】
  outputs/social/x-analytics-report-YYYY-MM-DD.md
"""

import argparse
import csv
import json
import sys
from collections import defaultdict
from datetime import datetime, timedelta
from pathlib import Path

try:
    import tweepy
except ImportError:
    tweepy = None

BASE_DIR = Path(__file__).parent.parent.parent
CONFIG_DIR = BASE_DIR / "config"
INPUT_DIR = BASE_DIR / "inputs" / "x-analytics"
OUTPUT_DIR = BASE_DIR / "outputs" / "social"
LOG_FILE = OUTPUT_DIR / "x-post-log.jsonl"


def load_post_log() -> list[dict]:
    """投稿ログを読み込む"""
    if not LOG_FILE.exists():
        return []
    posts = []
    with open(LOG_FILE, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line:
                posts.append(json.loads(line))
    return posts


def fetch_metrics_api(posts: list[dict]) -> list[dict]:
    """API経由でメトリクスを取得（Freeプラン: get_me のみ）"""
    if tweepy is None:
        print("ERROR: tweepy がインストールされていません")
        return posts

    creds_file = CONFIG_DIR / "x-credentials.json"
    if not creds_file.exists():
        print("ERROR: x-credentials.json が見つかりません")
        return posts

    with open(creds_file, "r", encoding="utf-8") as f:
        creds = json.load(f)

    client = tweepy.Client(
        consumer_key=creds["api_key"],
        consumer_secret=creds["api_key_secret"],
        access_token=creds["access_token"],
        access_token_secret=creds["access_token_secret"],
    )

    # アカウント全体のメトリクス
    try:
        me = client.get_me(user_fields=["public_metrics"])
        account_metrics = me.data.public_metrics
        print(f"アカウント: @{me.data.username}")
        print(f"  フォロワー: {account_metrics['followers_count']}")
        print(f"  ツイート数: {account_metrics['tweet_count']}")
        print(f"  いいね数: {account_metrics['like_count']}")
    except Exception as e:
        print(f"アカウント情報取得エラー: {e}")
        account_metrics = {}

    # 個別ツイートのメトリクス取得を試みる
    for post in posts:
        tweet_id = post.get("tweet_id")
        if not tweet_id or tweet_id == "dry-run-id":
            continue
        try:
            tweet = client.get_tweet(
                tweet_id,
                tweet_fields=["public_metrics", "created_at"],
            )
            if tweet.data and tweet.data.public_metrics:
                post["metrics"] = tweet.data.public_metrics
                m = post["metrics"]
                print(f"  ID:{tweet_id} | imp:{m.get('impression_count', 'N/A')} like:{m['like_count']} rt:{m['retweet_count']}")
        except Exception:
            # Freeプランでは取得不可 → スキップ
            post["metrics"] = {
                "impression_count": 0,
                "like_count": 0,
                "retweet_count": 0,
                "reply_count": 0,
            }

    # アカウントメトリクスを返す
    for post in posts:
        post["account_metrics"] = account_metrics

    return posts


def parse_analytics_csv(csv_path: str) -> list[dict]:
    """X Analytics CSVを解析"""
    rows = []
    with open(csv_path, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            rows.append(row)
    return rows


def generate_report(posts: list[dict], target_date: str = None, csv_data: list[dict] = None) -> str:
    """日次レポートを生成"""
    now = datetime.now()
    report_date = target_date or now.strftime("%Y-%m-%d")

    lines = []
    lines.append(f"# X アナリティクス日次レポート ({report_date})")
    lines.append("")
    lines.append(f"**生成日時**: {now.strftime('%Y-%m-%d %H:%M')} (PYT)")
    lines.append("")

    # アカウント概要
    account = posts[0].get("account_metrics", {}) if posts else {}
    if account:
        lines.append("## アカウント概要")
        lines.append("")
        lines.append(f"| 指標 | 値 |")
        lines.append(f"|------|-----|")
        lines.append(f"| フォロワー | {account.get('followers_count', 'N/A')} |")
        lines.append(f"| 総ツイート数 | {account.get('tweet_count', 'N/A')} |")
        lines.append(f"| 総いいね数 | {account.get('like_count', 'N/A')} |")
        lines.append("")

    # CSV データがある場合
    if csv_data:
        lines.append("## ツイート別パフォーマンス（CSV）")
        lines.append("")
        lines.append("| 日時 | インプレッション | エンゲージメント | いいね | RT | 投稿文（先頭40字） |")
        lines.append("|------|----------------|----------------|-------|-----|-------------------|")

        total_imp = 0
        total_eng = 0
        total_likes = 0
        total_rt = 0

        for row in csv_data:
            imp = int(row.get("impressions", row.get("インプレッション", 0)))
            eng = int(row.get("engagements", row.get("エンゲージメント", 0)))
            likes = int(row.get("likes", row.get("いいね", 0)))
            rt = int(row.get("retweets", row.get("リツイート", 0)))
            text = row.get("Tweet text", row.get("ツイート本文", ""))[:40]
            date = row.get("time", row.get("時間", ""))

            total_imp += imp
            total_eng += eng
            total_likes += likes
            total_rt += rt

            lines.append(f"| {date} | {imp:,} | {eng:,} | {likes} | {rt} | {text}… |")

        lines.append("")
        lines.append(f"**合計**: インプレッション {total_imp:,} / エンゲージメント {total_eng:,} / いいね {total_likes} / RT {total_rt}")
        if total_imp > 0:
            eng_rate = total_eng / total_imp * 100
            lines.append(f"**エンゲージメント率**: {eng_rate:.2f}%")
        lines.append("")

    # ログベースのデータ
    if posts:
        lines.append("## 投稿一覧（ログベース）")
        lines.append("")
        lines.append("| 日時 | カテゴリ | imp | like | RT | reply | 投稿文（先頭40字） |")
        lines.append("|------|---------|-----|------|-----|-------|-------------------|")

        for post in posts:
            ts = post.get("timestamp", "")[:16]
            cat = post.get("category", "-")
            m = post.get("metrics", {})
            imp = m.get("impression_count", "-")
            like = m.get("like_count", "-")
            rt = m.get("retweet_count", "-")
            reply = m.get("reply_count", "-")
            text = post.get("text", "")[:40]
            lines.append(f"| {ts} | {cat} | {imp} | {like} | {rt} | {reply} | {text}… |")

        lines.append("")

    # カテゴリ別集計
    cat_counts = defaultdict(int)
    for post in posts:
        cat = post.get("category", "other")
        cat_counts[cat] += 1

    if cat_counts:
        lines.append("## カテゴリ別投稿数")
        lines.append("")
        lines.append("| カテゴリ | 投稿数 |")
        lines.append("|---------|--------|")
        for cat, count in sorted(cat_counts.items(), key=lambda x: -x[1]):
            lines.append(f"| {cat} | {count} |")
        lines.append("")

    # 注記
    lines.append("---")
    lines.append("")
    lines.append("> **注意**: X API Freeプランではインプレッション数は取得できません。")
    lines.append("> 正確なインプレッション数を取得するには:")
    lines.append("> 1. https://analytics.x.com からCSVをエクスポートして `inputs/x-analytics/` に保存")
    lines.append("> 2. `python scripts/social/x_analytics.py --csv inputs/x-analytics/ファイル名.csv` で実行")
    lines.append("> 3. または X API Basicプラン ($100/月) にアップグレード")
    lines.append("")

    return "\n".join(lines)


def main():
    sys.stdout.reconfigure(encoding="utf-8")

    parser = argparse.ArgumentParser(description="X アナリティクス日次レポート")
    parser.add_argument("--csv", type=str, help="X Analytics CSVファイルのパス")
    parser.add_argument("--date", type=str, help="レポート対象日 (YYYY-MM-DD)")
    parser.add_argument("--api", action="store_true", help="API経由でメトリクス取得")
    args = parser.parse_args()

    # 投稿ログ読み込み
    posts = load_post_log()
    print(f"投稿ログ: {len(posts)} 件")

    # CSVデータ
    csv_data = None
    if args.csv:
        csv_path = Path(args.csv)
        if not csv_path.is_absolute():
            csv_path = BASE_DIR / csv_path
        if csv_path.exists():
            csv_data = parse_analytics_csv(str(csv_path))
            print(f"CSV: {len(csv_data)} 件")
        else:
            print(f"WARNING: CSVファイルが見つかりません: {csv_path}")
    else:
        # inputs/x-analytics/ から最新CSVを自動検出
        INPUT_DIR.mkdir(parents=True, exist_ok=True)
        csv_files = sorted(INPUT_DIR.glob("*.csv"), key=lambda p: p.stat().st_mtime, reverse=True)
        if csv_files:
            csv_data = parse_analytics_csv(str(csv_files[0]))
            print(f"CSV (自動検出): {csv_files[0].name} ({len(csv_data)} 件)")

    # API経由メトリクス取得
    if args.api:
        posts = fetch_metrics_api(posts)

    # レポート生成
    report = generate_report(posts, target_date=args.date, csv_data=csv_data)

    # 保存
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    report_date = args.date or datetime.now().strftime("%Y-%m-%d")
    output_file = OUTPUT_DIR / f"x-analytics-report-{report_date}.md"
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(report)

    print(f"\nレポート生成完了: {output_file}")


if __name__ == "__main__":
    main()
