"""
SIM比較オンライン — 全下書き記事の一括公開スクリプト
outputs/articles/2026-03-19/ の全MDファイルと既存WP下書きを公開する。
"""

import sys
import os

if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")

import json
import re
import csv
import time
import requests
from pathlib import Path
from datetime import datetime, timezone, timedelta

BASE_DIR = Path(__file__).resolve().parent.parent.parent
CONFIG_DIR = BASE_DIR / "config"
OUTPUTS_DIR = BASE_DIR / "outputs"
ARTICLES_DIR = OUTPUTS_DIR / "articles" / "2026-03-19"
THEME_CSS = BASE_DIR / "theme" / "css" / "sim-global.css"
SETUP_RESULT = CONFIG_DIR / "setup-result.json"
CSV_FILE = OUTPUTS_DIR / "article-management.csv"

JST = timezone(timedelta(hours=9))


def load_secrets():
    with open(CONFIG_DIR / "secrets.json", encoding="utf-8") as f:
        return json.load(f)


def load_category_ids():
    if SETUP_RESULT.exists():
        with open(SETUP_RESULT, encoding="utf-8") as f:
            return json.load(f).get("category_ids", {})
    return {}


def extract_frontmatter(md_content):
    match = re.match(r"^---\s*\n(.*?)\n---", md_content, re.DOTALL)
    if not match:
        return {}
    fm = {}
    for line in match.group(1).split("\n"):
        if ":" in line:
            key, value = line.split(":", 1)
            fm[key.strip()] = value.strip().strip('"').strip("'")
    return fm


def strip_frontmatter_html(html):
    fm_keys = ['title:', 'focus_keyword:', 'meta_description:', 'category:', 'tags:', 'article_type:', 'pillar:', 'affiliate_disclosure:', 'keyword:', 'status:', 'slug:']
    pattern = re.compile(r'<p>---\s*</p>\s*(?:<p>.*?</p>\s*)*?<p>---\s*</p>', re.DOTALL)
    match = pattern.search(html)
    if match and any(k in match.group() for k in fm_keys):
        html = pattern.sub('', html, count=1)
    return html.lstrip('\n')


def md_to_html(md_content):
    content = re.sub(r"^---.*?---\s*", "", md_content, flags=re.DOTALL)
    lines = content.split("\n")
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
    html = strip_frontmatter_html(html)
    return html


def inject_css(html_content):
    list_fix = """<style>
.entry-content ul, .entry-content ol { list-style-type: disc !important; }
.entry-content ol { list-style-type: decimal !important; }
.entry-content ul li::before, .entry-content ol li::before { content: none !important; display: none !important; }
</style>
"""
    css = ""
    if THEME_CSS.exists():
        css = THEME_CSS.read_text(encoding="utf-8")
    if css:
        return f"<!-- wp:html -->\n<style>{css}</style>\n<!-- /wp:html -->\n\n{list_fix}{html_content}"
    return f"{list_fix}{html_content}"


def wp_request(method, url, auth, json_data=None, max_retries=3):
    for attempt in range(max_retries):
        try:
            r = requests.request(method, url, auth=auth, json=json_data, timeout=120)
            return r
        except (requests.exceptions.Timeout, requests.exceptions.ConnectionError) as e:
            if attempt < max_retries - 1:
                wait = 10 * (attempt + 1)
                print(f"    Timeout, retrying in {wait}s... (attempt {attempt+2}/{max_retries})")
                time.sleep(wait)
            else:
                raise


def publish_article(api_url, auth, title, slug, html_content, category_id=None, existing_id=None):
    """Create or update a post and set status to publish."""
    data = {
        "title": title,
        "slug": slug,
        "content": html_content,
        "status": "publish",
    }
    if category_id:
        data["categories"] = [category_id]

    if existing_id:
        r = wp_request("post", f"{api_url}/posts/{existing_id}", auth, data)
        if r.status_code == 200:
            return r.json()["id"], r.json().get("link", "")
        else:
            print(f"    Update failed: {r.status_code} {r.text[:200]}")
            return None, ""

    # Check if slug already exists
    r = wp_request("get", f"{api_url}/posts?slug={slug}&status=draft,publish,future", auth)
    if r.status_code == 200 and r.json():
        existing = r.json()[0]
        post_id = existing["id"]
        print(f"    Existing post found (ID={post_id}), updating & publishing...")
        r2 = wp_request("post", f"{api_url}/posts/{post_id}", auth, data)
        if r2.status_code == 200:
            return r2.json()["id"], r2.json().get("link", "")
        else:
            print(f"    Update failed: {r2.status_code} {r2.text[:200]}")
            return None, ""

    # Create new
    r = wp_request("post", f"{api_url}/posts", auth, data)
    if r.status_code == 201:
        return r.json()["id"], r.json().get("link", "")
    else:
        print(f"    Create failed: {r.status_code} {r.text[:200]}")
        return None, ""


def main():
    secrets = load_secrets()
    wp = secrets["wordpress"]
    api_url = wp["api_url"]
    auth = (wp["username"], wp["app_password"])
    category_ids = load_category_ids()

    # Category mapping from CSV column names to setup-result keys
    cat_map = {
        "yoto-betsu": "yoto-betsu",
        "review": "review",
        "ryokin-hikaku": "ryokin-hikaku",
        "carrier-review": "review",
        "kaigai-sim": "kaigai-sim",
        "norikae-guide": "norikae",
        "sokudo-hikaku": "ryokin-hikaku",
        "norikae": "norikae",
    }

    # Collect all MD files from articles/2026-03-19/
    md_files = sorted(ARTICLES_DIR.glob("*.md"))

    # Also check outputs/ for kakuyasu-sim-hikaku-povo.md
    povo_hikaku = OUTPUTS_DIR / "kakuyasu-sim-hikaku-povo.md"
    if povo_hikaku.exists():
        md_files.append(povo_hikaku)

    # Also check for sim.md in articles/2026-03-18/ (existing WP ID 395)
    sim_2018 = OUTPUTS_DIR / "articles" / "2026-03-18" / "sim.md"
    if sim_2018.exists():
        md_files.append(sim_2018)
    sim_2019 = OUTPUTS_DIR / "articles" / "2026-03-19" / "sim.md"
    # sim.md already included from glob

    print(f"=== sim-hikaku.online 全下書き一括公開 ===")
    print(f"対象記事: {len(md_files)}件")
    print(f"開始: {datetime.now(JST).strftime('%Y-%m-%d %H:%M JST')}\n")

    # Read CSV to get existing WP IDs
    csv_wp_ids = {}  # filename -> wp_id
    if CSV_FILE.exists():
        with open(CSV_FILE, encoding="utf-8") as f:
            reader = csv.reader(f)
            header = next(reader)
            for row in reader:
                if len(row) >= 13 and row[12].strip():
                    try:
                        csv_wp_ids[row[12].strip()] = int(row[13].strip()) if len(row) > 13 and row[13].strip() else None
                    except (ValueError, IndexError):
                        pass
                if len(row) >= 14:
                    filename = row[12].strip()  # column index 12 = filename
                    wp_id_str = row[13].strip() if len(row) > 13 else ""
                    if filename and wp_id_str:
                        try:
                            csv_wp_ids[filename] = int(wp_id_str)
                        except ValueError:
                            pass

    results = []
    success = 0
    failed = 0

    for md_file in md_files:
        md_content = md_file.read_text(encoding="utf-8")
        fm = extract_frontmatter(md_content)
        title = fm.get("title", md_file.stem)
        slug = fm.get("slug", md_file.stem)
        category_slug = fm.get("category", "")

        # Map category
        cat_key = cat_map.get(category_slug, category_slug)
        cat_id = category_ids.get(cat_key)

        # Check for existing WP ID
        existing_id = csv_wp_ids.get(md_file.stem) or csv_wp_ids.get(slug)

        print(f"[{success + failed + 1}/{len(md_files)}] {slug}")
        print(f"  Title: {title}")

        html = md_to_html(md_content)
        html = inject_css(html)

        try:
            wp_id, wp_url = publish_article(api_url, auth, title, slug, html, cat_id, existing_id)
            if wp_id:
                print(f"  -> Published: ID={wp_id} URL={wp_url}")
                results.append({
                    "filename": md_file.stem,
                    "slug": slug,
                    "title": title,
                    "wp_id": wp_id,
                    "url": wp_url,
                    "status": "success",
                })
                success += 1
            else:
                print(f"  -> FAILED")
                results.append({"filename": md_file.stem, "slug": slug, "title": title, "status": "failed"})
                failed += 1
        except Exception as e:
            print(f"  -> ERROR: {e}")
            results.append({"filename": md_file.stem, "slug": slug, "title": title, "status": "error", "error": str(e)})
            failed += 1

        # Small delay to avoid rate limiting
        time.sleep(1)

    print(f"\n=== 完了 ===")
    print(f"成功: {success}件 / 失敗: {failed}件")

    # Update CSV
    if CSV_FILE.exists() and results:
        update_csv(results)

    # Save results
    results_file = OUTPUTS_DIR / "publish-results.json"
    with open(results_file, "w", encoding="utf-8") as f:
        json.dump(results, f, ensure_ascii=False, indent=2)
    print(f"\n結果保存: {results_file}")


def update_csv(results):
    """Update article-management.csv: set status to 公開済, add WP ID and URL."""
    result_map = {}
    for r in results:
        if r["status"] == "success":
            result_map[r["filename"]] = r
            result_map[r["slug"]] = r

    with open(CSV_FILE, encoding="utf-8") as f:
        lines = f.readlines()

    new_lines = [lines[0]]  # header
    updated = 0
    for line in lines[1:]:
        if not line.strip():
            new_lines.append(line)
            continue
        cols = line.rstrip("\n").split(",")
        if len(cols) >= 13:
            filename = cols[12].strip()
            r = result_map.get(filename)
            if r:
                cols[2] = "公開済"  # status
                cols[3] = "2026-03-20"  # publish date
                # Ensure enough columns for WP ID (col 13) and URL (col 14)
                while len(cols) < 15:
                    cols.append("")
                cols[13] = str(r["wp_id"])
                cols[14] = r.get("url", f"https://sim-hikaku.online/{r['slug']}/")
                updated += 1
        new_lines.append(",".join(cols) + "\n")

    with open(CSV_FILE, "w", encoding="utf-8") as f:
        f.writelines(new_lines)
    print(f"  CSV更新: {updated}件のステータスを「公開済」に変更")


if __name__ == "__main__":
    main()
