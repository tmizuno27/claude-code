#!/usr/bin/env python3
"""
WordPress自動投稿スクリプト

Markdown記事をWordPressに投稿する。
デフォルトはドラフト投稿。--status publish で即時公開。

使い方:
  python wp_publisher.py                          # 全未投稿をドラフト投稿
  python wp_publisher.py --status publish          # 全未投稿を即時公開
  python wp_publisher.py --status publish --limit 1  # 1記事だけ即時公開
  python wp_publisher.py --dry-run                 # 投稿せずにプレビュー
"""

import argparse
import json
import logging
import re
import sys
import urllib.request
from base64 import b64encode
from datetime import datetime
from pathlib import Path

import markdown
import requests

# ログ設定
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# プロジェクトルート
PROJECT_ROOT = Path(__file__).parent.parent
CONFIG_PATH = PROJECT_ROOT / "config" / "settings.json"
ARTICLES_DIR = PROJECT_ROOT / "outputs" / "articles"
WP_LOG_PATH = PROJECT_ROOT / "published" / "wordpress-log.json"


def load_config():
    """設定ファイルを読み込む"""
    with open(CONFIG_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


def load_wp_log():
    """WordPress投稿履歴を読み込む"""
    if WP_LOG_PATH.exists():
        with open(WP_LOG_PATH, "r", encoding="utf-8") as f:
            return json.load(f)
    return {"posts": []}


def save_wp_log(log_data):
    """WordPress投稿履歴を保存する"""
    WP_LOG_PATH.parent.mkdir(parents=True, exist_ok=True)
    with open(WP_LOG_PATH, "w", encoding="utf-8") as f:
        json.dump(log_data, f, ensure_ascii=False, indent=2)


def parse_front_matter(content):
    """Markdownファイルからフロントマターとボディを分離する"""
    front_matter = {}
    body = content

    # --- で囲まれたフロントマターを解析
    fm_match = re.match(r'^---\s*\n(.*?)\n---\s*\n(.*)', content, re.DOTALL)
    if fm_match:
        fm_text = fm_match.group(1)
        body = fm_match.group(2)

        for line in fm_text.strip().split('\n'):
            if ':' in line:
                key, value = line.split(':', 1)
                front_matter[key.strip()] = value.strip().strip('"').strip("'")

    return front_matter, body


def find_unpublished_articles():
    """未投稿のMarkdown記事を検索する"""
    unpublished = []

    if not ARTICLES_DIR.exists():
        logger.warning(f"記事ディレクトリが存在しません: {ARTICLES_DIR}")
        return unpublished

    # 日付フォルダとルート直下の両方を検索
    md_files = list(ARTICLES_DIR.rglob("*.md"))

    # 既に投稿済みのファイルを除外
    wp_log = load_wp_log()
    published_files = {p.get("source_file") for p in wp_log.get("posts", [])}

    for md_file in md_files:
        relative_path = str(md_file.relative_to(PROJECT_ROOT))
        if relative_path in published_files:
            continue

        content = md_file.read_text(encoding="utf-8")
        front_matter, body = parse_front_matter(content)

        # status が "draft" または フロントマターなしの記事を対象
        status = front_matter.get("status", "draft")
        if status in ("draft", ""):
            unpublished.append({
                "path": md_file,
                "relative_path": relative_path,
                "front_matter": front_matter,
                "body": body
            })

    return unpublished


def markdown_to_html(md_text):
    """MarkdownをHTMLに変換する"""
    extensions = [
        'markdown.extensions.tables',
        'markdown.extensions.fenced_code',
        'markdown.extensions.toc',
        'markdown.extensions.nl2br'
    ]
    return markdown.markdown(md_text, extensions=extensions)


def publish_to_wordpress(config, article, status="draft"):
    """記事をWordPressに投稿する"""
    wp_config = config["wordpress"]
    url = f"{wp_config['rest_api_url']}/posts"

    # Basic認証ヘッダー
    credentials = f"{wp_config['username']}:{wp_config['app_password']}"
    token = b64encode(credentials.encode()).decode()
    headers = {
        "Authorization": f"Basic {token}",
        "Content-Type": "application/json"
    }

    # 記事データ
    title = article["front_matter"].get("title", "無題の記事")
    keyword = article["front_matter"].get("keyword", "")
    html_content = markdown_to_html(article["body"])

    post_data = {
        "title": title,
        "content": html_content,
        "status": status,
    }

    logger.info(f"投稿中 (status={status}): {title}")

    response = requests.post(url, headers=headers, json=post_data, timeout=30)

    if response.status_code in (200, 201):
        post = response.json()
        result = {
            "post_id": post["id"],
            "title": title,
            "keyword": keyword,
            "url": post["link"],
            "edit_url": f"{wp_config['url']}/wp-admin/post.php?post={post['id']}&action=edit",
            "status": status,
            "source_file": article["relative_path"],
            "published_at": datetime.now().isoformat()
        }
        logger.info(f"投稿成功! ID: {post['id']} (status: {status})")
        logger.info(f"  URL: {result['url']}")
        return result
    else:
        logger.error(f"投稿失敗: {response.status_code} - {response.text}")
        return None


def notify_discord(message):
    """Discord Webhookで通知を送信"""
    try:
        settings_file = CONFIG_PATH
        with open(settings_file, "r", encoding="utf-8") as f:
            settings = json.load(f)
        webhook_url = settings.get("discord", {}).get("webhook_url")
        if not webhook_url:
            return
        payload = json.dumps({"content": message}).encode("utf-8")
        req = urllib.request.Request(
            webhook_url,
            data=payload,
            headers={"Content-Type": "application/json", "User-Agent": "BlogPublisher/1.0"},
        )
        urllib.request.urlopen(req)
        logger.info("Discord通知を送信しました")
    except Exception as e:
        logger.warning(f"Discord通知の送信に失敗: {e}")


def main():
    """メイン処理"""
    parser = argparse.ArgumentParser(description="WordPress自動投稿スクリプト")
    parser.add_argument("--status", default="draft", choices=["draft", "publish"],
                        help="投稿ステータス: draft(下書き) / publish(即時公開)")
    parser.add_argument("--limit", type=int, default=0,
                        help="投稿する記事数の上限 (0=全件)")
    parser.add_argument("--dry-run", action="store_true",
                        help="投稿せずにプレビューのみ")
    args = parser.parse_args()

    logger.info("=== WordPress自動投稿スクリプト開始 ===")
    logger.info(f"  ステータス: {args.status} / 上限: {'全件' if args.limit == 0 else f'{args.limit}件'}")

    # 設定読み込み
    try:
        config = load_config()
    except FileNotFoundError:
        logger.error(f"設定ファイルが見つかりません: {CONFIG_PATH}")
        sys.exit(1)

    # WordPress設定チェック
    wp_url = config.get("wordpress", {}).get("url", "")
    if "YOUR" in wp_url or not wp_url:
        logger.error("WordPress URLが未設定です。config/settings.json を編集してください。")
        sys.exit(1)

    # 未投稿記事を検索
    articles = find_unpublished_articles()
    if not articles:
        logger.info("未投稿の記事はありません。")
        return

    # limit が指定されている場合は制限
    if args.limit > 0:
        articles = articles[:args.limit]

    logger.info(f"投稿対象の記事: {len(articles)}件")

    if args.dry_run:
        for article in articles:
            title = article["front_matter"].get("title", "無題")
            logger.info(f"  [DRY RUN] {title} → {args.status}")
        return

    # 投稿履歴の読み込み
    wp_log = load_wp_log()

    # 各記事を投稿
    success_count = 0
    published_posts = []
    for article in articles:
        try:
            result = publish_to_wordpress(config, article, status=args.status)
            if result:
                wp_log["posts"].append(result)
                published_posts.append(result)
                success_count += 1
        except requests.RequestException as e:
            logger.error(f"ネットワークエラー: {e}")
        except Exception as e:
            logger.error(f"予期しないエラー: {e}")

    # 履歴を保存
    save_wp_log(wp_log)

    # サマリー
    logger.info(f"\n=== 結果サマリー ===")
    logger.info(f"投稿成功: {success_count}/{len(articles)}件 (status: {args.status})")

    # Discord通知
    if success_count > 0 and args.status == "publish":
        for post in published_posts:
            notify_discord(
                f"📝 ブログ記事を公開しました\n\n"
                f"**{post['title']}**\n"
                f"{post['url']}"
            )
    elif success_count > 0:
        logger.info(f"\nWordPress管理画面でドラフトを確認し、「公開」ボタンを押してください。")
        for post in published_posts:
            logger.info(f"  → {post['title']}")
            logger.info(f"    編集: {post['edit_url']}")


if __name__ == "__main__":
    main()
