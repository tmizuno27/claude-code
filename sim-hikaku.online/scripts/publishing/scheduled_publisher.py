"""
SIM比較ナビ — 予約投稿スケジューラ
Phase 2以降の記事を自動的にWordPressに予約投稿する。

使い方:
  python scheduled_publisher.py                  # スケジュール確認（dry-run）
  python scheduled_publisher.py --publish        # 実際に予約投稿を実行
  python scheduled_publisher.py --check          # 予約済み記事のステータス確認

スケジュール設定:
  config/publish-schedule.json に投稿スケジュールを定義。
  記事MDファイルが outputs/ に存在する記事のみ対象。
"""

import requests
import json
import base64
import sys
import os
from datetime import datetime, timezone, timedelta
from pathlib import Path

# Paths
BASE_DIR = Path(__file__).resolve().parent.parent.parent
CONFIG_DIR = BASE_DIR / "config"
OUTPUTS_DIR = BASE_DIR / "outputs"
THEME_CSS = BASE_DIR / "theme" / "css" / "sim-global.css"
SCHEDULE_FILE = CONFIG_DIR / "publish-schedule.json"
CSV_FILE = OUTPUTS_DIR / "article-management.csv"

JST = timezone(timedelta(hours=9))


def load_secrets():
    with open(CONFIG_DIR / "secrets.json", encoding="utf-8") as f:
        return json.load(f)


def get_wp_headers(secrets):
    wp = secrets["wordpress"]
    creds = base64.b64encode(
        f"{wp['username']}:{wp['app_password']}".encode()
    ).decode()
    return {
        "Authorization": f"Basic {creds}",
        "Content-Type": "application/json",
    }


def load_schedule():
    if not SCHEDULE_FILE.exists():
        print(f"スケジュールファイルが見つかりません: {SCHEDULE_FILE}")
        print("config/publish-schedule.json を作成してください。")
        sys.exit(1)
    with open(SCHEDULE_FILE, encoding="utf-8") as f:
        return json.load(f)


def load_css():
    if THEME_CSS.exists():
        with open(THEME_CSS, encoding="utf-8") as f:
            return f.read()
    return ""


def load_article_md(filename):
    md_path = OUTPUTS_DIR / f"{filename}.md"
    if not md_path.exists():
        return None
    with open(md_path, encoding="utf-8") as f:
        content = f.read()
    # Remove frontmatter
    if content.startswith("---"):
        end = content.index("---", 3)
        content = content[end + 3:].strip()
    return content


def inject_css(content, css):
    style_block = f"<style>{css}</style>"
    if "<style" in content:
        s1 = content.index("<style")
        s2 = content.index("</style>") + len("</style>")
        return content[:s1] + style_block + content[s2:]
    else:
        return f"<!-- wp:html -->\n{style_block}\n<!-- /wp:html -->\n\n{content}"


def schedule_post(api_url, headers, post_id, date_gmt, content=None):
    """Set a post to 'future' status with the given GMT datetime."""
    data = {
        "status": "future",
        "date_gmt": date_gmt,
    }
    if content:
        data["content"] = content
    r = requests.post(f"{api_url}/posts/{post_id}", headers=headers, json=data)
    return r.json()


def check_scheduled(api_url, headers):
    """Check all scheduled (future) posts."""
    r = requests.get(
        f"{api_url}/posts?status=future&per_page=50",
        headers=headers,
    )
    posts = r.json()
    if not posts:
        print("予約済み記事はありません。")
        return
    print(f"\n予約済み記事: {len(posts)}件")
    print("-" * 70)
    for p in sorted(posts, key=lambda x: x.get("date", "")):
        title = p["title"]["rendered"]
        date_jst = p.get("date", "")
        print(f"  ID:{p['id']}  {date_jst}  {title}")


def main():
    args = sys.argv[1:]
    secrets = load_secrets()
    wp = secrets["wordpress"]
    api_url = wp["api_url"]
    headers = get_wp_headers(secrets)

    if "--check" in args:
        check_scheduled(api_url, headers)
        return

    schedule = load_schedule()
    css = load_css()
    dry_run = "--publish" not in args

    if dry_run:
        print("=== DRY RUN（--publish で実行） ===\n")

    for entry in schedule["articles"]:
        filename = entry["filename"]
        date_jst = entry["publish_date_jst"]  # e.g. "2026-03-23T07:00:00"
        wp_id = entry.get("wp_id")
        category_slug = entry.get("category", "")

        # Parse JST date to GMT
        dt_jst = datetime.fromisoformat(date_jst).replace(tzinfo=JST)
        dt_gmt = dt_jst.astimezone(timezone.utc)
        date_gmt_str = dt_gmt.strftime("%Y-%m-%dT%H:%M:%S")

        # Check if MD exists
        md_content = load_article_md(filename)
        has_md = md_content is not None

        status_icon = "✓" if has_md else "✗"
        print(f"  {status_icon} {date_jst} | {filename}")
        if not has_md:
            print(f"    → MDファイルなし（outputs/{filename}.md）- スキップ")
            continue

        if wp_id and not dry_run:
            # Update existing draft with CSS and schedule
            content_with_css = inject_css(md_content, css)
            result = schedule_post(api_url, headers, wp_id, date_gmt_str, content_with_css)
            new_status = result.get("status", "error")
            print(f"    → 予約完了: status={new_status} date={result.get('date', '')}")
        elif not wp_id and not dry_run:
            print(f"    → WP IDなし - 先に下書きを作成してください")
        elif dry_run:
            print(f"    → 予約予定: {date_gmt_str} UTC (WP ID: {wp_id or '未作成'})")

    if dry_run:
        print("\n実行するには: python scheduled_publisher.py --publish")


if __name__ == "__main__":
    main()
