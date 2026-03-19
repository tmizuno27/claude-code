"""
SIM比較オンライン — WordPress記事投稿スクリプト
指定ディレクトリのMarkdown記事をWordPressに下書き投稿する。

使い方:
  python wp_publisher.py                           # outputs/articles/今日の日付/ を投稿
  python wp_publisher.py --date 2026-03-18         # 日付指定
  python wp_publisher.py --dir outputs/articles/X  # ディレクトリ直接指定
"""

import sys
import os

if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")

import json
import re
import requests
from pathlib import Path
from datetime import datetime, timezone, timedelta

BASE_DIR = Path(__file__).resolve().parent.parent.parent
CONFIG_DIR = BASE_DIR / "config"
OUTPUTS_DIR = BASE_DIR / "outputs"
THEME_CSS = BASE_DIR / "theme" / "css" / "sim-global.css"
SETUP_RESULT = CONFIG_DIR / "setup-result.json"

JST = timezone(timedelta(hours=9))


def load_secrets():
    with open(CONFIG_DIR / "secrets.json", encoding="utf-8") as f:
        return json.load(f)


def get_auth(secrets):
    wp = secrets["wordpress"]
    return (wp["username"], wp["app_password"])


def get_api_url(secrets):
    return secrets["wordpress"]["api_url"]


def load_category_ids():
    if SETUP_RESULT.exists():
        with open(SETUP_RESULT, encoding="utf-8") as f:
            data = json.load(f)
        return data.get("category_ids", {})
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
    """HTML変換後に残ったフロントマターを除去する安全装置"""
    fm_keys = ['title:', 'focus_keyword:', 'meta_description:', 'category:', 'tags:', 'article_type:', 'pillar:', 'affiliate_disclosure:', 'keyword:', 'status:']
    pattern = re.compile(r'<p>---\s*</p>\s*(?:<p>.*?</p>\s*)*?<p>---\s*</p>', re.DOTALL)
    match = pattern.search(html)
    if match and any(k in match.group() for k in fm_keys):
        html = pattern.sub('', html, count=1)
        print("  [安全装置] HTML内のフロントマターを除去しました")
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


def publish_as_draft(api_url, auth, title, slug, html_content, category_id=None, excerpt=""):
    data = {
        "title": title,
        "slug": slug,
        "content": html_content,
        "status": "draft",
        "excerpt": excerpt,
    }
    if category_id:
        data["categories"] = [category_id]

    # Check if already exists
    r = requests.get(f"{api_url}/posts?slug={slug}&status=draft,publish,future", auth=auth, timeout=30)
    if r.status_code == 200 and r.json():
        existing = r.json()[0]
        post_id = existing["id"]
        print(f"  Already exists (ID={post_id}), updating...")
        r2 = requests.post(f"{api_url}/posts/{post_id}", auth=auth, json=data, timeout=120)
        if r2.status_code == 200:
            print(f"  Updated: ID={post_id}")
            return post_id
        else:
            print(f"  Update failed: {r2.status_code} {r2.text[:200]}")
            return None

    r = requests.post(f"{api_url}/posts", auth=auth, json=data, timeout=120)
    if r.status_code == 201:
        post_id = r.json()["id"]
        print(f"  Created draft: ID={post_id}")
        return post_id
    else:
        print(f"  Failed: {r.status_code} {r.text[:200]}")
        return None


def main():
    args = sys.argv[1:]
    secrets = load_secrets()
    api_url = get_api_url(secrets)
    auth = get_auth(secrets)
    category_ids = load_category_ids()

    # Determine article directory
    if "--dir" in args:
        idx = args.index("--dir")
        article_dir = Path(args[idx + 1])
        if not article_dir.is_absolute():
            article_dir = BASE_DIR / article_dir
    elif "--date" in args:
        idx = args.index("--date")
        date_str = args[idx + 1]
        article_dir = OUTPUTS_DIR / "articles" / date_str
    else:
        today = datetime.now(JST).strftime("%Y-%m-%d")
        article_dir = OUTPUTS_DIR / "articles" / today

    if not article_dir.exists():
        print(f"ディレクトリが見つかりません: {article_dir}")
        sys.exit(1)

    md_files = sorted(article_dir.glob("*.md"))
    if not md_files:
        print(f"MDファイルが見つかりません: {article_dir}")
        sys.exit(1)

    print(f"=== sim-hikaku.online WordPress Draft Publisher ===")
    print(f"Directory: {article_dir}")
    print(f"Articles: {len(md_files)}件\n")

    results = []
    for md_file in md_files:
        print(f"Processing: {md_file.name}")
        md_content = md_file.read_text(encoding="utf-8")
        fm = extract_frontmatter(md_content)
        title = fm.get("title", md_file.stem)
        slug = fm.get("slug", md_file.stem)
        cat_slug = fm.get("category", "")
        cat_id = category_ids.get(cat_slug)
        excerpt = fm.get("description", "")

        html = md_to_html(md_content)
        html = inject_css(html)

        post_id = publish_as_draft(api_url, auth, title, slug, html, cat_id, excerpt)
        results.append({"file": md_file.name, "title": title, "wp_id": post_id})

    print(f"\n=== 完了 ===")
    print(f"投稿結果:")
    success_count = 0
    for r in results:
        status = f"ID={r['wp_id']}" if r["wp_id"] else "FAILED"
        print(f"  {r['file']}: {r['title']} → {status}")
        if r["wp_id"]:
            success_count += 1

    # 投稿成功した記事にアフィリエイトリンクを自動挿入
    if success_count > 0:
        import subprocess
        affiliate_script = Path(__file__).parent / "insert_affiliate_all.py"
        if affiliate_script.exists():
            try:
                result_aff = subprocess.run(
                    [sys.executable, str(affiliate_script), "--apply"],
                    capture_output=True, text=True, timeout=120
                )
                if result_aff.returncode == 0:
                    print("アフィリエイトリンク自動挿入完了")
                else:
                    print(f"アフィリエイトリンク挿入失敗: {result_aff.stderr[:200]}")
            except Exception as e:
                print(f"アフィリエイトリンク挿入エラー: {e}")


if __name__ == "__main__":
    main()
