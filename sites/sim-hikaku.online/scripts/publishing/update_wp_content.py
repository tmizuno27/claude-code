"""
SIM比較オンライン — WordPress記事コンテンツ更新スクリプト
MDファイルの最新内容でWordPressの予約済み記事を更新する。

使い方:
  python update_wp_content.py                    # dry-run
  python update_wp_content.py --apply            # 全予約済み記事を更新
  python update_wp_content.py --apply --ids 124,126  # 指定IDのみ更新
"""

import sys
import os
import json
import re
import base64
from pathlib import Path
from datetime import datetime, timezone, timedelta

if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")

# Import shared functions from scheduled_publisher
BASE_DIR = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(Path(__file__).resolve().parent))
from scheduled_publisher import (
    load_secrets, get_wp_headers, load_schedule, load_css,
    load_article_md, md_to_html, inject_css, wp_request_with_retry
)

JST = timezone(timedelta(hours=9))


def main():
    args = sys.argv[1:]
    dry_run = "--apply" not in args

    # Parse --ids filter
    target_ids = None
    for i, arg in enumerate(args):
        if arg == "--ids" and i + 1 < len(args):
            target_ids = set(int(x) for x in args[i + 1].split(","))

    secrets = load_secrets()
    wp = secrets["wordpress"]
    api_url = wp["api_url"]
    headers = get_wp_headers(secrets)
    schedule = load_schedule()
    css = load_css()

    if dry_run:
        print("=== DRY RUN（--apply で実行） ===\n")

    updated = 0
    skipped = 0

    for entry in schedule["articles"]:
        wp_id = entry.get("wp_id")
        filename = entry["filename"]
        status = entry.get("status", "pending")

        if not wp_id:
            continue
        if status not in ("scheduled", "published"):
            continue
        if target_ids and wp_id not in target_ids:
            continue

        # Load MD
        fm, md_content = load_article_md(filename)
        if not md_content:
            continue

        # Convert
        html_content = md_to_html(md_content)
        html_with_css = inject_css(html_content, css)

        if dry_run:
            print(f"  [OK] WP ID={wp_id} | {filename} — 更新予定")
            updated += 1
            continue

        # Update WordPress
        try:
            r = wp_request_with_retry(
                "post",
                f"{api_url}/posts/{wp_id}",
                headers,
                {"content": html_with_css}
            )
            if r.status_code == 200:
                print(f"  [OK] WP ID={wp_id} | {filename} — 更新完了")
                updated += 1
            else:
                print(f"  [NG] WP ID={wp_id} | {filename} — {r.status_code}: {r.text[:100]}")
                skipped += 1
        except Exception as e:
            print(f"  [NG] WP ID={wp_id} | {filename} — ERROR: {e}")
            skipped += 1

    print(f"\n--- 結果 ---")
    print(f"  更新: {updated}件")
    print(f"  失敗: {skipped}件")

    if dry_run:
        print("\n実行するには: python update_wp_content.py --apply")


if __name__ == "__main__":
    main()
