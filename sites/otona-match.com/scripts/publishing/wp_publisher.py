"""otona-match.com WordPress Publisher
Usage:
  python wp_publisher.py                     # outputs/内の未公開MDを投稿
  python wp_publisher.py --status draft      # ドラフトとして投稿
  python wp_publisher.py --file article.md   # 特定ファイルを投稿
"""
import urllib.request
import urllib.error
import json
import base64
import ssl
import os
import sys
import csv
import re
from pathlib import Path
from datetime import datetime

# Paths
BASE_DIR = Path(__file__).resolve().parent.parent.parent  # otona-match.com/
CONFIG_DIR = BASE_DIR / "config"
OUTPUTS_DIR = BASE_DIR / "outputs"
PUBLISHED_DIR = BASE_DIR / "published"
CSV_PATH = OUTPUTS_DIR / "article-management.csv"

# Load credentials
def load_credentials():
    secrets_path = CONFIG_DIR / "secrets.json"
    if not secrets_path.exists():
        print(f"ERROR: {secrets_path} not found")
        sys.exit(1)
    with open(secrets_path, "r", encoding="utf-8") as f:
        secrets = json.load(f)
    return secrets["wordpress"]["username"], secrets["wordpress"]["app_password"]

# WordPress API
def get_wp_client():
    username, app_password = load_credentials()
    auth = base64.b64encode(f"{username}:{app_password}".encode()).decode()
    ctx = ssl.create_default_context()
    return auth, ctx

BASE_URL = "https://otona-match.com/?rest_route="

# List style fix CSS (Cocoon theme override)
LIST_CSS = '<style>.entry-content ul{list-style:none!important;padding-left:0!important}.entry-content ul li{position:relative!important;padding-left:1.5em!important;margin-bottom:.5em!important}.entry-content ul li::before{content:"•"!important;position:absolute!important;left:.3em!important;color:#0066CC!important;font-weight:bold!important}.entry-content ol{list-style:decimal!important;padding-left:1.5em!important}.entry-content ol li{margin-bottom:.5em!important}.entry-content ol li::before{content:none!important}</style>\n'

def wp_post(endpoint, data, auth, ctx):
    body = json.dumps(data).encode("utf-8")
    req = urllib.request.Request(BASE_URL + endpoint, data=body, method="POST")
    req.add_header("Content-Type", "application/json; charset=utf-8")
    req.add_header("Authorization", f"Basic {auth}")
    try:
        with urllib.request.urlopen(req, context=ctx, timeout=60) as resp:
            return json.loads(resp.read())
    except urllib.error.HTTPError as e:
        print(f"  HTTP Error {e.code}: {e.read().decode()[:300]}")
        return None

def strip_frontmatter(text):
    """テキスト/HTMLからYAMLフロントマターを除去する安全装置"""
    fm_keys = ['title:', 'focus_keyword:', 'meta_description:', 'category:', 'tags:', 'article_type:', 'pillar:', 'affiliate_disclosure:', 'keyword:', 'status:']
    # Markdownフロントマター
    cleaned = re.sub(r'^---\s*\n.*?\n---\s*\n', '', text, count=1, flags=re.DOTALL)
    if cleaned != text:
        removed = text[:len(text) - len(cleaned)]
        if any(k in removed for k in fm_keys):
            print("  [安全装置] フロントマターを除去しました")
            return cleaned.lstrip('\n')
    # HTML内フロントマター（<p>---</p>パターン）
    pattern = re.compile(r'<p>---\s*</p>\s*(?:<p>.*?</p>\s*)*?<p>---\s*</p>', re.DOTALL)
    match = pattern.search(text)
    if match and any(k in match.group() for k in fm_keys):
        text = pattern.sub('', text, count=1)
        print("  [安全装置] HTML内のフロントマターを除去しました")
    return text.lstrip('\n')


def publish_article(title, slug, content, categories, excerpt, status="publish"):
    content = strip_frontmatter(content)
    auth, ctx = get_wp_client()
    data = {
        "title": title,
        "slug": slug,
        "content": LIST_CSS + content,
        "categories": categories,
        "excerpt": excerpt,
        "status": status,
    }
    result = wp_post("/wp/v2/posts", data, auth, ctx)
    if result and "id" in result:
        print(f"  Published: ID:{result['id']} - {title}")
        # Save to published log
        log = {
            "id": result["id"],
            "title": title,
            "slug": slug,
            "url": result.get("link", ""),
            "status": status,
            "published_at": datetime.now().isoformat(),
        }
        log_path = PUBLISHED_DIR / f"{slug}.json"
        with open(log_path, "w", encoding="utf-8") as f:
            json.dump(log, f, ensure_ascii=False, indent=2)
        return result
    return None

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Publish articles to otona-match.com")
    parser.add_argument("--status", default="publish", choices=["publish", "draft"])
    parser.add_argument("--file", help="Specific markdown file to publish")
    args = parser.parse_args()

    print(f"=== otona-match.com Publisher (status: {args.status}) ===")
    print("Publisher ready. Use publish_article() to post articles.")
