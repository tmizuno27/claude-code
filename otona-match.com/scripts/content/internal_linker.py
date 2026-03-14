"""otona-match.com Internal Linker
記事間の内部リンクを自動挿入するスクリプト。
Usage: python internal_linker.py [--dry-run]
"""
import urllib.request
import urllib.error
import json
import base64
import ssl
import re
import sys
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent.parent
CONFIG_DIR = BASE_DIR / "config"

BASE_URL = "https://otona-match.com/?rest_route="

# Internal link mapping: keyword -> slug
LINK_MAP = {
    "マッチングアプリ おすすめ": "matching-app-ranking-2026",
    "マッチングアプリおすすめ": "matching-app-ranking-2026",
    "ペアーズ": "pairs-review",
    "Pairs": "pairs-review",
    "ウィズ": "with-review",
    "with（ウィズ）": "with-review",
    "料金比較": "matching-app-price-comparison",
    "マッチングアプリの料金": "matching-app-price-comparison",
    "出会い系サイト": "deaikei-vs-matching-app",
    "ハッピーメール": "happy-mail-review",
    "PCMAX": "pcmax-review",
    "婚活アプリ": "konkatsu-app-osusume",
    "結婚相談所": "kekkon-soudan-vs-app",
    "30代 婚活": "konkatsu-30dai",
    "プロフィール写真": "profile-photo-tips",
    "返信が来ない": "matching-app-no-reply",
    "初デート": "first-date-manual",
    "サクラ": "sakura-gyosha-miwakekata",
    "業者の見分け方": "sakura-gyosha-miwakekata",
    "身バレ": "matching-app-mibare-taisaku",
    "安全チェック": "anzen-checklist",
    "結婚した人": "matching-app-kekkon-taikendan",
    "40代": "40dai-50dai-taikendan",
    "50代": "40dai-50dai-taikendan",
    "やめどき": "matching-app-yamedoki",
}

def load_credentials():
    secrets_path = CONFIG_DIR / "secrets.json"
    with open(secrets_path, "r", encoding="utf-8") as f:
        secrets = json.load(f)
    return secrets["wordpress"]["username"], secrets["wordpress"]["app_password"]

def get_auth():
    username, app_password = load_credentials()
    return base64.b64encode(f"{username}:{app_password}".encode()).decode()

def wp_get(endpoint, auth, ctx):
    req = urllib.request.Request(BASE_URL + endpoint)
    req.add_header("Authorization", f"Basic {auth}")
    with urllib.request.urlopen(req, context=ctx, timeout=30) as resp:
        return json.loads(resp.read())

def wp_update(post_id, data, auth, ctx):
    body = json.dumps(data).encode("utf-8")
    req = urllib.request.Request(BASE_URL + f"/wp/v2/posts/{post_id}", data=body, method="POST")
    req.add_header("Content-Type", "application/json; charset=utf-8")
    req.add_header("Authorization", f"Basic {auth}")
    with urllib.request.urlopen(req, context=ctx, timeout=30) as resp:
        return json.loads(resp.read())

def insert_internal_links(content, current_slug, max_links=3):
    """Insert internal links into content, avoiding self-links and duplicates."""
    inserted = 0
    used_slugs = set()

    for keyword, target_slug in LINK_MAP.items():
        if inserted >= max_links:
            break
        if target_slug == current_slug:
            continue
        if target_slug in used_slugs:
            continue
        # Check if keyword exists in text (not already linked)
        if keyword in content and f'href="https://otona-match.com/{target_slug}' not in content:
            link = f'<a href="https://otona-match.com/{target_slug}/">{keyword}</a>'
            # Replace first occurrence only
            content = content.replace(keyword, link, 1)
            used_slugs.add(target_slug)
            inserted += 1

    return content, inserted

if __name__ == "__main__":
    dry_run = "--dry-run" in sys.argv
    auth = get_auth()
    ctx = ssl.create_default_context()

    posts = wp_get("/wp/v2/posts&per_page=50&status=publish", auth, ctx)
    print(f"=== Internal Linker ({'DRY RUN' if dry_run else 'LIVE'}) ===")
    print(f"Found {len(posts)} published posts\n")

    for post in posts:
        slug = post["slug"]
        content = post["content"]["rendered"]
        new_content, count = insert_internal_links(content, slug)

        if count > 0:
            print(f"  {slug}: +{count} internal links")
            if not dry_run:
                wp_update(post["id"], {"content": new_content}, auth, ctx)
        else:
            print(f"  {slug}: no changes needed")

    print("\nDone!")
