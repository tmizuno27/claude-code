#!/usr/bin/env python3
"""WordPressコンテンツバックアップ — 全記事+固定ページのHTMLをローカルに保存
SIM比較オンライン (sim-hikaku.online) 版。

Usage:
    python wp_backup.py              # 全記事バックアップ
    python wp_backup.py --pages      # 固定ページも含む
"""
import argparse
import io
import json
import logging
import sys
from base64 import b64encode
from datetime import datetime
from pathlib import Path

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding="utf-8", errors="replace")

try:
    import requests
except ImportError:
    print("ERROR: requests が必要です: pip install requests")
    sys.exit(1)

# --- Paths ---
SCRIPT_DIR = Path(__file__).parent
PROJECT_ROOT = SCRIPT_DIR.parent.parent
CONFIG_DIR = PROJECT_ROOT / "config"
OUTPUTS_DIR = PROJECT_ROOT / "outputs"
BACKUP_DIR = OUTPUTS_DIR / "wp-backups"
LOG_FILE = OUTPUTS_DIR / "wp-backup.log"

OUTPUTS_DIR.mkdir(parents=True, exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler(LOG_FILE, encoding="utf-8"),
    ],
)
logger = logging.getLogger(__name__)


def load_secrets():
    path = CONFIG_DIR / "secrets.json"
    if not path.exists():
        logger.error(f"secrets.json が見つかりません: {path}")
        return {}
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def get_wp_session(secrets):
    wp = secrets.get("wordpress", {})
    username = wp.get("username", "")
    app_password = wp.get("app_password", "")
    token = b64encode(f"{username}:{app_password}".encode()).decode()

    session = requests.Session()
    session.headers.update({
        "Authorization": f"Basic {token}",
        "Content-Type": "application/json",
    })
    return session


def fetch_all_items(session, endpoint):
    """WP REST APIから全アイテムを取得（ページネーション対応）"""
    items = []
    page = 1
    per_page = 50
    while True:
        url = f"https://sim-hikaku.online/wp-json/wp/v2/{endpoint}?per_page={per_page}&page={page}&status=publish,draft,private"
        resp = session.get(url, timeout=30)
        if resp.status_code != 200:
            break
        batch = resp.json()
        if not batch:
            break
        items.extend(batch)
        if len(batch) < per_page:
            break
        page += 1
    return items


def backup_items(items, item_type, backup_dir):
    """記事/ページをJSONとHTMLで保存"""
    type_dir = backup_dir / item_type
    type_dir.mkdir(parents=True, exist_ok=True)

    for item in items:
        item_id = item.get("id")
        slug = item.get("slug", f"id-{item_id}")
        title = item.get("title", {}).get("rendered", "No Title")
        content = item.get("content", {}).get("rendered", "")
        status = item.get("status", "unknown")

        # JSON（メタデータ含む完全バックアップ）
        meta = {
            "id": item_id,
            "slug": slug,
            "title": title,
            "status": status,
            "date": item.get("date", ""),
            "modified": item.get("modified", ""),
            "link": item.get("link", ""),
            "categories": item.get("categories", []),
            "tags": item.get("tags", []),
            "featured_media": item.get("featured_media", 0),
            "excerpt": item.get("excerpt", {}).get("rendered", ""),
        }
        json_path = type_dir / f"{slug}.json"
        with open(json_path, "w", encoding="utf-8") as f:
            json.dump({"meta": meta, "content": content}, f, ensure_ascii=False, indent=2)

        # HTML（コンテンツのみ、復旧用）
        html_path = type_dir / f"{slug}.html"
        html = f"""<!DOCTYPE html>
<html lang="ja">
<head>
<meta charset="UTF-8">
<title>{title}</title>
<meta name="wp-id" content="{item_id}">
<meta name="wp-status" content="{status}">
<meta name="wp-date" content="{item.get('date', '')}">
</head>
<body>
<h1>{title}</h1>
{content}
</body>
</html>"""
        with open(html_path, "w", encoding="utf-8") as f:
            f.write(html)

    return len(items)


def main():
    parser = argparse.ArgumentParser(description="WPコンテンツバックアップ (sim-hikaku.online)")
    parser.add_argument("--pages", action="store_true", help="固定ページも含む")
    args = parser.parse_args()

    logger.info("========== WPバックアップ 開始 (sim-hikaku.online) ==========")

    secrets = load_secrets()
    session = get_wp_session(secrets)

    today = datetime.now().strftime("%Y-%m-%d")
    backup_dir = BACKUP_DIR / today
    backup_dir.mkdir(parents=True, exist_ok=True)

    # 記事バックアップ
    logger.info("記事を取得中...")
    posts = fetch_all_items(session, "posts")
    post_count = backup_items(posts, "posts", backup_dir)
    logger.info(f"記事: {post_count}件バックアップ完了")

    # 固定ページ
    page_count = 0
    if args.pages:
        logger.info("固定ページを取得中...")
        pages = fetch_all_items(session, "pages")
        page_count = backup_items(pages, "pages", backup_dir)
        logger.info(f"固定ページ: {page_count}件バックアップ完了")

    # マニフェスト
    manifest = {
        "date": today,
        "posts": post_count,
        "pages": page_count,
        "backup_dir": str(backup_dir),
        "timestamp": datetime.now().isoformat(),
    }
    manifest_path = backup_dir / "manifest.json"
    with open(manifest_path, "w", encoding="utf-8") as f:
        json.dump(manifest, f, ensure_ascii=False, indent=2)

    # 古いバックアップを4世代まで保持
    if BACKUP_DIR.exists():
        all_backups = sorted(BACKUP_DIR.iterdir(), reverse=True)
        for old_backup in all_backups[4:]:
            if old_backup.is_dir() and old_backup.name != today:
                import shutil
                shutil.rmtree(old_backup)
                logger.info(f"古いバックアップ削除: {old_backup.name}")

    logger.info(f"バックアップ先: {backup_dir}")
    logger.info("========== WPバックアップ 終了 ==========")


if __name__ == "__main__":
    main()
