#!/usr/bin/env python3
"""
はてなブログ AtomPub API 自動投稿スクリプト

変換済みダイジェスト記事をはてなブログに自動投稿する。

使い方:
  python hatena_publisher.py                    # 未投稿の全記事を投稿
  python hatena_publisher.py --limit 3          # 3記事だけ投稿
  python hatena_publisher.py --draft            # 下書きとして投稿
  python hatena_publisher.py --dry-run          # 投稿せずにプレビュー
"""

import argparse
import json
import logging
import sys
import re
import time
from base64 import b64encode
from datetime import datetime
from pathlib import Path

import requests

# Log settings
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Paths
PROJECT_ROOT = Path(__file__).parent.parent.parent
SECRETS_PATH = PROJECT_ROOT / "config" / "secrets.json"
HATENA_OUTPUT_DIR = PROJECT_ROOT / "outputs" / "hatena"
HATENA_LOG_PATH = PROJECT_ROOT / "published" / "hatena-log.json"

# Default categories/tags for hatena
DEFAULT_CATEGORIES = ["パラグアイ", "海外移住", "海外生活"]


def load_secrets():
    """Load secrets from config."""
    with open(SECRETS_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


def load_hatena_log():
    """Load hatena publication log."""
    if HATENA_LOG_PATH.exists():
        with open(HATENA_LOG_PATH, "r", encoding="utf-8") as f:
            return json.load(f)
    return {"converted": [], "published": []}


def save_hatena_log(log_data):
    """Save hatena publication log."""
    HATENA_LOG_PATH.parent.mkdir(parents=True, exist_ok=True)
    with open(HATENA_LOG_PATH, "w", encoding="utf-8") as f:
        json.dump(log_data, f, ensure_ascii=False, indent=2)


def get_unpublished_articles(hatena_log):
    """Get converted articles that haven't been published to Hatena yet."""
    published_ids = {str(entry["article_id"]) for entry in hatena_log.get("published", [])}
    return [
        entry for entry in hatena_log.get("converted", [])
        if str(entry["article_id"]) not in published_ids
    ]


def read_hatena_article(filename):
    """Read converted hatena article and parse frontmatter."""
    filepath = HATENA_OUTPUT_DIR / filename
    if not filepath.exists():
        return None, None

    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()

    # Parse frontmatter
    frontmatter = {}
    body = content
    if content.startswith("---"):
        parts = content.split("---", 2)
        if len(parts) >= 3:
            for line in parts[1].strip().split("\n"):
                if ": " in line:
                    key, value = line.split(": ", 1)
                    frontmatter[key.strip()] = value.strip()
            body = parts[2].strip()

    return frontmatter, body


def build_atom_entry(title, body, categories, is_draft=False):
    """Build AtomPub XML entry."""
    draft_value = "yes" if is_draft else "no"

    escaped_title = escape_xml(title)

    category_xml = ""
    for cat in categories:
        category_xml += f'  <category term="{escape_xml(cat)}" />\n'

    entry_xml = f"""<?xml version="1.0" encoding="utf-8"?>
<entry xmlns="http://www.w3.org/2005/Atom"
       xmlns:app="http://www.w3.org/2007/app">
  <title>{escaped_title}</title>
  <author><name>miccho27</name></author>
  <content type="text/x-markdown"><![CDATA[{body}]]></content>
{category_xml}  <app:control>
    <app:draft>{draft_value}</app:draft>
  </app:control>
</entry>"""

    return entry_xml


def escape_xml(text):
    """Escape special XML characters."""
    text = text.replace("&", "&amp;")
    text = text.replace("<", "&lt;")
    text = text.replace(">", "&gt;")
    text = text.replace('"', "&quot;")
    text = text.replace("'", "&apos;")
    return text


def post_to_hatena(hatena_config, title, body, categories, is_draft=False):
    """Post article to Hatena Blog via AtomPub API."""
    hatena_id = hatena_config["hatena_id"]
    blog_id = hatena_config["blog_id"]
    api_key = hatena_config["api_key"]

    endpoint = f"https://blog.hatena.ne.jp/{hatena_id}/{blog_id}/atom/entry"

    # Escape XML content
    escaped_body = escape_xml(body)
    escaped_title = escape_xml(title)

    entry_xml = build_atom_entry(escaped_title, escaped_body, categories, is_draft)

    # WSSE authentication
    auth_string = b64encode(f"{hatena_id}:{api_key}".encode()).decode()

    headers = {
        "Content-Type": "application/xml; charset=utf-8",
        "Authorization": f"Basic {auth_string}"
    }

    response = requests.post(endpoint, data=entry_xml.encode("utf-8"), headers=headers)

    if response.status_code in (200, 201):
        # Extract entry URL from response
        entry_url = ""
        url_match = re.search(r'<link rel="alternate"[^>]*href="([^"]+)"', response.text)
        if url_match:
            entry_url = url_match.group(1)
        return True, entry_url
    else:
        return False, f"HTTP {response.status_code}: {response.text[:500]}"


def detect_categories(title, body):
    """Detect appropriate categories from content."""
    categories = list(DEFAULT_CATEGORIES)

    keyword_map = {
        "費用": "お金",
        "生活費": "お金",
        "物価": "お金",
        "食": "グルメ",
        "料理": "グルメ",
        "アサード": "グルメ",
        "ビザ": "移住準備",
        "永住権": "移住準備",
        "気候": "気候・天気",
        "天気": "気候・天気",
        "子育て": "子育て",
        "教育": "子育て",
        "副業": "副業",
        "稼ぐ": "副業",
        "VPN": "IT・ツール",
        "送金": "お金",
    }

    combined_text = f"{title} {body}"
    for keyword, category in keyword_map.items():
        if keyword in combined_text and category not in categories:
            categories.append(category)

    return categories[:5]  # Hatena recommends max 5 categories


def main():
    parser = argparse.ArgumentParser(description="はてなブログ自動投稿")
    parser.add_argument("--limit", type=int, default=0, help="投稿する記事数の上限")
    parser.add_argument("--draft", action="store_true", help="下書きとして投稿")
    parser.add_argument("--dry-run", action="store_true", help="投稿せずにプレビュー")
    args = parser.parse_args()

    secrets = load_secrets()
    hatena_config = secrets.get("hatena")
    if not hatena_config:
        logger.error("はてなブログの認証情報がsecrets.jsonにありません")
        sys.exit(1)

    # Load log and find unpublished
    hatena_log = load_hatena_log()
    targets = get_unpublished_articles(hatena_log)

    if args.limit > 0:
        targets = targets[:args.limit]

    if not targets:
        logger.info("投稿対象の記事がありません")
        return

    logger.info(f"投稿対象: {len(targets)}記事 (draft={args.draft})")

    success_count = 0
    for entry in targets:
        article_id = entry["article_id"]
        hatena_file = entry["hatena_file"]
        hatena_title = entry["hatena_title"]

        logger.info(f"[#{article_id}] {hatena_title}")

        frontmatter, body = read_hatena_article(hatena_file)
        if body is None:
            logger.warning(f"  → ファイルが見つかりません: {hatena_file}")
            continue

        categories = detect_categories(hatena_title, body)

        if args.dry_run:
            logger.info(f"  → DRY RUN: {len(body)}文字, カテゴリ: {categories}")
            continue

        # Post to Hatena
        success, result = post_to_hatena(
            hatena_config, hatena_title, body, categories, is_draft=args.draft
        )

        if success:
            hatena_log["published"].append({
                "article_id": article_id,
                "hatena_title": hatena_title,
                "hatena_url": result,
                "is_draft": args.draft,
                "published_at": datetime.now().isoformat()
            })
            save_hatena_log(hatena_log)
            success_count += 1
            logger.info(f"  → 投稿成功: {result}")
        else:
            logger.error(f"  → 投稿失敗: {result}")

    logger.info(f"投稿完了: {success_count}/{len(targets)}記事")


if __name__ == "__main__":
    main()
