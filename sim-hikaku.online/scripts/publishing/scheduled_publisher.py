"""
SIM比較オンライン — 予約投稿スケジューラ
Phase 2以降の記事を自動的にWordPressに予約投稿する。

使い方:
  python scheduled_publisher.py                  # スケジュール確認（dry-run）
  python scheduled_publisher.py --publish        # 実際に予約投稿を実行
  python scheduled_publisher.py --check          # 予約済み記事のステータス確認

スケジュール設定:
  config/publish-schedule.json に投稿スケジュールを定義。
  記事MDファイルが outputs/ に存在する記事のみ対象。

自動処理フロー（--publish時）:
  1. wp_id が null の記事 → WP下書きを自動作成して wp_id を取得
  2. publish-schedule.json を wp_id で更新・保存
  3. 公開日時が未来の記事 → WordPress予約投稿（status: future）に設定
  4. article-management.csv を同期更新
"""

import sys
import os
# Force UTF-8 output on Windows
if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")

import requests
import json
import base64
import re
from datetime import datetime, timezone, timedelta
from pathlib import Path

# Paths
BASE_DIR = Path(__file__).resolve().parent.parent.parent
CONFIG_DIR = BASE_DIR / "config"
OUTPUTS_DIR = BASE_DIR / "outputs"
THEME_CSS = BASE_DIR / "theme" / "css" / "sim-global.css"
SCHEDULE_FILE = CONFIG_DIR / "publish-schedule.json"
CSV_FILE = OUTPUTS_DIR / "article-management.csv"
SETUP_RESULT = CONFIG_DIR / "setup-result.json"

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


def save_schedule(schedule):
    with open(SCHEDULE_FILE, "w", encoding="utf-8") as f:
        json.dump(schedule, f, ensure_ascii=False, indent=2)
    print(f"  → publish-schedule.json を更新しました")


def load_category_ids():
    if SETUP_RESULT.exists():
        with open(SETUP_RESULT, encoding="utf-8") as f:
            data = json.load(f)
        return data.get("category_ids", {})
    return {}


def load_css():
    if THEME_CSS.exists():
        with open(THEME_CSS, encoding="utf-8") as f:
            return f.read()
    return ""


def load_article_md(filename):
    md_path = OUTPUTS_DIR / f"{filename}.md"
    if not md_path.exists():
        return None, None
    with open(md_path, encoding="utf-8") as f:
        raw = f.read()
    # Extract frontmatter
    fm = {}
    content = raw
    if raw.startswith("---"):
        end = raw.index("---", 3)
        fm_text = raw[3:end].strip()
        for line in fm_text.split("\n"):
            if ":" in line:
                key, value = line.split(":", 1)
                fm[key.strip()] = value.strip().strip('"').strip("'")
        content = raw[end + 3:].strip()
    return fm, content


def md_to_html(md_content):
    """基本的なMarkdown→HTML変換"""
    lines = md_content.split("\n")
    html_lines = []
    in_table = False

    for line in lines:
        stripped = line.strip()

        if not stripped:
            if in_table:
                html_lines.append("</tbody></table>")
                in_table = False
            html_lines.append("")
            continue

        # Headers
        if stripped.startswith("## "):
            if in_table:
                html_lines.append("</tbody></table>")
                in_table = False
            html_lines.append(f"<h2>{stripped[3:]}</h2>")
            continue
        if stripped.startswith("### "):
            html_lines.append(f"<h3>{stripped[4:]}</h3>")
            continue
        if stripped.startswith("#### "):
            html_lines.append(f"<h4>{stripped[5:]}</h4>")
            continue

        if stripped == "---":
            html_lines.append("<hr>")
            continue

        # Table
        if "|" in stripped and stripped.startswith("|"):
            cells = [c.strip() for c in stripped.split("|")[1:-1]]
            if all(set(c) <= set("-: ") for c in cells):
                continue
            if not in_table:
                html_lines.append('<table style="width: 100%; border-collapse: collapse;">')
                html_lines.append("<thead><tr>")
                for cell in cells:
                    html_lines.append(f"<th>{cell}</th>")
                html_lines.append("</tr></thead><tbody>")
                in_table = True
                continue
            html_lines.append("<tr>")
            for cell in cells:
                html_lines.append(f"<td>{cell}</td>")
            html_lines.append("</tr>")
            continue

        if stripped.startswith("- "):
            html_lines.append(f"<li>{stripped[2:]}</li>")
            continue
        if stripped.startswith("> "):
            html_lines.append(f"<blockquote>{stripped[2:]}</blockquote>")
            continue
        if stripped.startswith("<"):
            html_lines.append(stripped)
            continue

        html_lines.append(f"<p>{stripped}</p>")

    if in_table:
        html_lines.append("</tbody></table>")

    html = "\n".join(html_lines)
    html = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", html)
    html = re.sub(r"\[(.+?)\]\((.+?)\)", r'<a href="\2">\1</a>', html)
    html = re.sub(r"`(.+?)`", r"<code>\1</code>", html)
    return html


def inject_css(content, css):
    # Cocoonリスト丸数字対策CSS
    list_fix = """
.entry-content ul, .entry-content ol { list-style-type: disc !important; }
.entry-content ol { list-style-type: decimal !important; }
.entry-content ul li::before, .entry-content ol li::before { content: none !important; display: none !important; }
"""
    full_css = css + "\n" + list_fix
    style_block = f"<style>{full_css}</style>"
    if "<style" in content:
        s1 = content.index("<style")
        s2 = content.index("</style>") + len("</style>")
        return content[:s1] + style_block + content[s2:]
    else:
        return f"<!-- wp:html -->\n{style_block}\n<!-- /wp:html -->\n\n{content}"""


def wp_request_with_retry(method, url, headers, json_data, max_retries=3):
    """WordPress API request with retry on timeout."""
    import time
    for attempt in range(max_retries):
        try:
            r = requests.request(method, url, headers=headers, json=json_data, timeout=120)
            return r
        except (requests.exceptions.Timeout, requests.exceptions.ConnectionError) as e:
            if attempt < max_retries - 1:
                wait = 10 * (attempt + 1)
                print(f"    → Timeout, retrying in {wait}s... (attempt {attempt + 2}/{max_retries})")
                time.sleep(wait)
            else:
                raise


def create_draft(api_url, headers, title, slug, html_content, category_id=None):
    """Create a new draft post on WordPress and return the post ID."""
    data = {
        "title": title,
        "slug": slug,
        "content": html_content,
        "status": "draft",
    }
    if category_id:
        data["categories"] = [category_id]
    try:
        r = wp_request_with_retry("post", f"{api_url}/posts", headers, data)
        if r.status_code == 201:
            return r.json()["id"]
        else:
            print(f"    → ERROR creating draft: {r.status_code} {r.text[:200]}")
            return None
    except Exception as e:
        print(f"    → ERROR: {e}")
        return None


def schedule_post(api_url, headers, post_id, date_gmt, content=None):
    """Set a post to 'future' status with the given GMT datetime."""
    data = {
        "status": "future",
        "date_gmt": date_gmt,
    }
    if content:
        data["content"] = content
    r = wp_request_with_retry("post", f"{api_url}/posts/{post_id}", headers, data)
    return r.json()


def update_csv(schedule):
    """Update article-management.csv with wp_ids and statuses from schedule."""
    if not CSV_FILE.exists():
        return
    with open(CSV_FILE, encoding="utf-8") as f:
        lines = f.readlines()
    if not lines:
        return

    # Build lookup: filename -> entry
    lookup = {}
    for entry in schedule["articles"]:
        lookup[entry["filename"]] = entry

    header = lines[0]
    new_lines = [header]
    for line in lines[1:]:
        cols = line.strip().split(",")
        if len(cols) >= 12:
            filename = cols[11]  # ファイル名列
            if filename in lookup:
                entry = lookup[filename]
                # Update WordPress ID (col 12)
                if entry.get("wp_id"):
                    while len(cols) < 13:
                        cols.append("")
                    cols[12] = str(entry["wp_id"])
                # Update status (col 2)
                status_map = {
                    "published": "公開済",
                    "scheduled": "予約済",
                    "pending": "予約済",
                }
                if entry.get("status") in status_map:
                    cols[2] = status_map[entry["status"]]
                # Update publish date (col 3)
                if entry.get("publish_date_jst"):
                    date_str = entry["publish_date_jst"][:10]
                    cols[3] = date_str
                # Update WordPress URL (col 13)
                if entry.get("wp_id") and len(cols) >= 14:
                    cols[13] = f"https://sim-hikaku.online/{filename}/"
        new_lines.append(",".join(cols) + "\n")

    with open(CSV_FILE, "w", encoding="utf-8") as f:
        f.writelines(new_lines)
    print("  → article-management.csv を更新しました")


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
    category_ids = load_category_ids()
    dry_run = "--publish" not in args
    schedule_modified = False
    now_jst = datetime.now(JST)

    if dry_run:
        print("=== DRY RUN（--publish で実行） ===\n")

    for entry in schedule["articles"]:
        filename = entry["filename"]
        date_jst = entry["publish_date_jst"]  # e.g. "2026-03-23T07:00:00"
        wp_id = entry.get("wp_id")
        category_slug = entry.get("category", "")
        status = entry.get("status", "pending")

        # Skip already published/scheduled
        if status in ("published", "scheduled"):
            print(f"  [OK] {date_jst} | {filename} ({status})")
            continue

        # Parse JST date to GMT
        dt_jst = datetime.fromisoformat(date_jst).replace(tzinfo=JST)
        dt_gmt = dt_jst.astimezone(timezone.utc)
        date_gmt_str = dt_gmt.strftime("%Y-%m-%dT%H:%M:%S")

        # Check if MD exists
        fm, md_content = load_article_md(filename)
        has_md = md_content is not None

        status_icon = "[OK]" if has_md else "[NG]"
        print(f"  {status_icon} {date_jst} | {filename}")
        if not has_md:
            print(f"    → MDファイルなし（outputs/{filename}.md）- スキップ")
            continue

        if dry_run:
            print(f"    → 予約予定: {date_gmt_str} UTC (WP ID: {wp_id or '未作成'})")
            continue

        # Convert MD to HTML with CSS
        html_content = md_to_html(md_content)
        html_with_css = inject_css(html_content, css)

        # Step 1: Create draft if no wp_id
        if not wp_id:
            title = fm.get("title", filename) if fm else filename
            cat_id = category_ids.get(category_slug)
            wp_id = create_draft(api_url, headers, title, filename, html_with_css, cat_id)
            if wp_id:
                entry["wp_id"] = wp_id
                schedule_modified = True
                print(f"    → 下書き作成: WP ID={wp_id}")
            else:
                print(f"    → 下書き作成失敗 - スキップ")
                continue

        # Step 2: Schedule the post
        result = schedule_post(api_url, headers, wp_id, date_gmt_str, html_with_css)
        new_status = result.get("status", "error")
        if new_status == "future":
            entry["status"] = "scheduled"
            schedule_modified = True
            print(f"    → 予約完了: status={new_status} date={result.get('date', '')}")
        else:
            print(f"    → 予約結果: status={new_status} {result.get('message', '')}")

    # Save updated schedule
    if schedule_modified:
        save_schedule(schedule)
        update_csv(schedule)

    if dry_run:
        print("\n実行するには: python scheduled_publisher.py --publish")
    else:
        print(f"\n処理完了 ({datetime.now(JST).strftime('%Y-%m-%d %H:%M JST')})")


if __name__ == "__main__":
    main()
