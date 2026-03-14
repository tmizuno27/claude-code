"""
sim-hikaku.online WordPress自動セットアップスクリプト
- カテゴリ作成
- 固定ページ作成（about, privacy-policy, disclaimer）
- トップページ作成・表示設定
- カスタムCSS適用
- ピラー記事投稿
"""

import json
import requests
import os
import re
from pathlib import Path

# パス設定
BASE_DIR = Path(__file__).resolve().parent.parent.parent
CONFIG_DIR = BASE_DIR / "config"
TEMPLATES_DIR = BASE_DIR / "templates"
THEME_DIR = BASE_DIR / "theme"
OUTPUTS_DIR = BASE_DIR / "outputs"


def load_secrets():
    with open(CONFIG_DIR / "secrets.json", "r", encoding="utf-8") as f:
        return json.load(f)


def get_auth(secrets):
    wp = secrets["wordpress"]
    return (wp["username"], wp["app_password"])


def get_api_url(secrets):
    return secrets["wordpress"]["api_url"]


def api_request(method, endpoint, secrets, **kwargs):
    url = f"{get_api_url(secrets)}/{endpoint}"
    auth = get_auth(secrets)
    kwargs.setdefault("timeout", 30)
    resp = getattr(requests, method)(url, auth=auth, **kwargs)
    if resp.status_code >= 400:
        print(f"  ERROR {resp.status_code}: {resp.text[:200]}")
    return resp


# ========== カテゴリ作成 ==========
def create_categories(secrets):
    categories = [
        {"name": "用途別おすすめ", "slug": "yoto-betsu", "description": "ターゲット別・用途別の格安SIM比較"},
        {"name": "乗り換えガイド", "slug": "norikae", "description": "MNP・乗り換え手順の解説"},
        {"name": "料金比較", "slug": "ryokin-hikaku", "description": "プラン別・容量別の料金比較"},
        {"name": "キャリアレビュー", "slug": "review", "description": "各格安SIMの詳細レビュー"},
        {"name": "海外SIM・eSIM", "slug": "kaigai-sim", "description": "海外旅行・留学・在住者向けSIM情報"},
    ]

    created = {}
    for cat in categories:
        print(f"Creating category: {cat['name']}...")
        resp = api_request("post", "categories", secrets, json=cat)
        if resp.status_code == 201:
            data = resp.json()
            created[cat["slug"]] = data["id"]
            print(f"  OK: ID={data['id']}")
        elif resp.status_code == 400 and "term_exists" in resp.text:
            # Already exists - get existing
            resp2 = api_request("get", f"categories?slug={cat['slug']}", secrets)
            if resp2.status_code == 200 and resp2.json():
                existing = resp2.json()[0]
                created[cat["slug"]] = existing["id"]
                print(f"  Already exists: ID={existing['id']}")
        else:
            print(f"  Failed: {resp.status_code}")

    return created


# ========== 固定ページ作成 ==========
def create_pages(secrets):
    pages = [
        {
            "title": "運営者情報",
            "slug": "about",
            "template_file": "about.html",
        },
        {
            "title": "プライバシーポリシー",
            "slug": "privacy-policy",
            "template_file": "privacy-policy.html",
        },
        {
            "title": "免責事項",
            "slug": "disclaimer",
            "template_file": "disclaimer.html",
        },
    ]

    created_pages = {}
    for page in pages:
        print(f"Creating page: {page['title']}...")

        # Check if page already exists
        resp = api_request("get", f"pages?slug={page['slug']}", secrets)
        if resp.status_code == 200 and resp.json():
            existing = resp.json()[0]
            created_pages[page["slug"]] = existing["id"]
            print(f"  Already exists: ID={existing['id']}")
            continue

        # Read template
        template_path = TEMPLATES_DIR / page["template_file"]
        if template_path.exists():
            content = template_path.read_text(encoding="utf-8")
        else:
            content = f"<p>{page['title']}ページ（準備中）</p>"
            print(f"  Template not found: {template_path}")

        data = {
            "title": page["title"],
            "slug": page["slug"],
            "content": content,
            "status": "publish",
        }

        resp = api_request("post", "pages", secrets, json=data)
        if resp.status_code == 201:
            result = resp.json()
            created_pages[page["slug"]] = result["id"]
            print(f"  OK: ID={result['id']}")
        else:
            print(f"  Failed: {resp.status_code}")

    return created_pages


# ========== トップページ作成 ==========
def create_front_page(secrets):
    print("Creating front page...")

    # Check if already exists
    resp = api_request("get", "pages?slug=home", secrets)
    if resp.status_code == 200 and resp.json():
        page_id = resp.json()[0]["id"]
        print(f"  Already exists: ID={page_id}")
        return page_id

    # Read front-page template
    fp_path = THEME_DIR / "front-page.html"
    if fp_path.exists():
        content = fp_path.read_text(encoding="utf-8")
    else:
        content = "<p>トップページ（準備中）</p>"
        print("  front-page.html not found!")

    data = {
        "title": "ホーム",
        "slug": "home",
        "content": content,
        "status": "publish",
    }

    resp = api_request("post", "pages", secrets, json=data)
    if resp.status_code == 201:
        page_id = resp.json()["id"]
        print(f"  OK: ID={page_id}")

        # Set as front page
        print("  Setting as static front page...")
        site_url = secrets["wordpress"]["site_url"]
        settings_resp = requests.put(
            f"{site_url}/wp-json/wp/v2/settings",
            auth=get_auth(secrets),
            json={
                "show_on_front": "page",
                "page_on_front": page_id,
            },
            timeout=30,
        )
        if settings_resp.status_code == 200:
            print("  Front page set successfully!")
        else:
            print(f"  Could not set front page: {settings_resp.status_code}")

        return page_id
    else:
        print(f"  Failed: {resp.status_code}")
        return None


# ========== 記事投稿 ==========
def md_to_html(md_content):
    """Markdown記事からフロントマター除去＋基本的なHTML変換"""
    # Remove frontmatter
    content = re.sub(r"^---.*?---\s*", "", md_content, flags=re.DOTALL)

    # Convert markdown to HTML (basic conversion)
    lines = content.split("\n")
    html_lines = []
    in_table = False
    table_header_done = False

    for line in lines:
        stripped = line.strip()

        # Skip empty lines
        if not stripped:
            if in_table:
                html_lines.append("</tbody></table>")
                in_table = False
                table_header_done = False
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

        # Horizontal rule
        if stripped == "---":
            html_lines.append("<hr>")
            continue

        # Table
        if "|" in stripped and stripped.startswith("|"):
            cells = [c.strip() for c in stripped.split("|")[1:-1]]

            # Skip separator rows
            if all(set(c) <= set("-: ") for c in cells):
                continue

            if not in_table:
                html_lines.append('<table style="width: 100%; border-collapse: collapse;">')
                html_lines.append("<thead><tr>")
                for cell in cells:
                    html_lines.append(f"<th>{cell}</th>")
                html_lines.append("</tr></thead><tbody>")
                in_table = True
                table_header_done = True
                continue

            html_lines.append("<tr>")
            for cell in cells:
                html_lines.append(f"<td>{cell}</td>")
            html_lines.append("</tr>")
            continue

        # Lists
        if stripped.startswith("- "):
            html_lines.append(f"<li>{stripped[2:]}</li>")
            continue

        # Blockquote
        if stripped.startswith("> "):
            html_lines.append(f"<blockquote>{stripped[2:]}</blockquote>")
            continue

        # Details/summary (keep as-is since they're HTML)
        if stripped.startswith("<"):
            html_lines.append(stripped)
            continue

        # Regular paragraph
        html_lines.append(f"<p>{stripped}</p>")

    if in_table:
        html_lines.append("</tbody></table>")

    html = "\n".join(html_lines)

    # Convert inline markdown
    # Bold
    html = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", html)
    # Links
    html = re.sub(r"\[(.+?)\]\((.+?)\)", r'<a href="\2">\1</a>', html)
    # Inline code
    html = re.sub(r"`(.+?)`", r"<code>\1</code>", html)

    return html


def extract_frontmatter(md_content):
    """Extract frontmatter from markdown"""
    match = re.match(r"^---\s*\n(.*?)\n---", md_content, re.DOTALL)
    if not match:
        return {}
    fm = {}
    for line in match.group(1).split("\n"):
        if ":" in line:
            key, value = line.split(":", 1)
            fm[key.strip()] = value.strip().strip('"').strip("'")
    return fm


def publish_article(secrets, md_file, category_ids):
    """Publish a markdown article to WordPress"""
    print(f"Publishing: {md_file.name}...")

    md_content = md_file.read_text(encoding="utf-8")
    fm = extract_frontmatter(md_content)
    html_content = md_to_html(md_content)

    # Cocoonリスト丸数字対策CSS
    list_fix_css = """<style>
.entry-content ul, .entry-content ol {
    list-style-type: disc !important;
}
.entry-content ol {
    list-style-type: decimal !important;
}
.entry-content ul li::before, .entry-content ol li::before {
    content: none !important;
    display: none !important;
}
</style>
"""
    html_content = list_fix_css + html_content

    # Get category ID
    cat_slug = fm.get("category", "yoto-betsu")
    cat_id = category_ids.get(cat_slug, None)

    data = {
        "title": fm.get("title", md_file.stem),
        "slug": fm.get("slug", md_file.stem),
        "content": html_content,
        "status": "publish",
        "excerpt": fm.get("description", ""),
    }
    if cat_id:
        data["categories"] = [cat_id]

    # Check if already exists
    resp = api_request("get", f"posts?slug={data['slug']}", secrets)
    if resp.status_code == 200 and resp.json():
        existing = resp.json()[0]
        print(f"  Already exists: ID={existing['id']}, updating...")
        resp = api_request("post", f"posts/{existing['id']}", secrets, json=data)
        if resp.status_code == 200:
            print(f"  Updated: ID={existing['id']}")
            return existing["id"]
    else:
        resp = api_request("post", "posts", secrets, json=data)
        if resp.status_code == 201:
            result = resp.json()
            print(f"  Published: ID={result['id']}, URL={result['link']}")
            return result["id"]
        else:
            print(f"  Failed: {resp.status_code}")
            return None


# ========== カスタムCSS適用 ==========
def apply_custom_css(secrets):
    """Apply custom CSS via WordPress Customizer API"""
    print("Applying custom CSS...")
    css_path = THEME_DIR / "css" / "sim-global.css"
    if not css_path.exists():
        print("  CSS file not found!")
        return

    css_content = css_path.read_text(encoding="utf-8")

    # WordPress custom CSS endpoint
    site_url = secrets["wordpress"]["site_url"]

    # Try to set via wp/v2/settings (custom_css)
    # This requires the customizer, so we'll use a different approach
    # Create a custom_html widget or use the wp_update_custom_css_post approach

    # Check for existing custom CSS post
    resp = api_request("get", "posts?slug=wp-custom-css&post_type=custom_css&status=publish", secrets)

    # Alternative: just print instructions
    print("  CSS file ready. Apply via:")
    print("  1. WordPress管理画面 → 外観 → カスタマイズ → 追加CSS")
    print(f"  2. CSS file: {css_path}")
    print(f"  3. Size: {len(css_content)} bytes")


# ========== メニュー作成 ==========
def create_menus(secrets, category_ids, page_ids):
    """Create navigation menus"""
    print("Creating menus...")

    # WordPress REST API doesn't natively support menu creation well
    # Print instructions instead
    print("  メニューはWordPress管理画面から手動設定してください:")
    print("  外観 → メニュー → ヘッダーメニュー:")
    for slug, cat_id in category_ids.items():
        print(f"    - カテゴリ: {slug} (ID: {cat_id})")
    print("  フッターメニュー:")
    for slug, page_id in page_ids.items():
        print(f"    - 固定ページ: {slug} (ID: {page_id})")


# ========== メイン ==========
def main():
    print("=" * 60)
    print("SIM比較ナビ WordPress自動セットアップ")
    print("=" * 60)

    secrets = load_secrets()

    # Check connection
    print("\n[1/6] Checking WordPress connection...")
    resp = api_request("get", "users/me", secrets)
    if resp.status_code != 200:
        print("ERROR: Cannot connect to WordPress REST API!")
        print("Please check:")
        print("1. secrets.json の app_password を設定してください")
        print("2. WordPress管理画面 → ユーザー → プロフィール → Application Passwords")
        print("3. 新しいパスワードを生成して secrets.json に貼り付け")
        return
    user = resp.json()
    print(f"  Connected as: {user.get('name', 'unknown')} (ID: {user['id']})")

    # Create categories
    print("\n[2/6] Creating categories...")
    category_ids = create_categories(secrets)
    print(f"  Categories: {category_ids}")

    # Create pages
    print("\n[3/6] Creating fixed pages...")
    page_ids = create_pages(secrets)
    print(f"  Pages: {page_ids}")

    # Create front page
    print("\n[4/6] Creating front page...")
    front_page_id = create_front_page(secrets)

    # Publish articles
    print("\n[5/6] Publishing articles...")
    article_files = list(OUTPUTS_DIR.glob("*.md"))
    article_files = [f for f in article_files if f.name != "article-management.csv"]
    for article_file in article_files:
        if article_file.suffix == ".md":
            publish_article(secrets, article_file, category_ids)

    # Apply CSS
    print("\n[6/6] Custom CSS...")
    apply_custom_css(secrets)

    # Menu instructions
    print("\n" + "=" * 60)
    print("セットアップ完了!")
    print("=" * 60)
    print("\n残りの手動作業:")
    print("1. 外観 → カスタマイズ → 追加CSS にCSSを貼り付け")
    print("2. 外観 → メニュー でヘッダー/フッターメニューを設定")
    print("3. Cocoon設定 → スキン → なし に設定")
    print("4. Rank Math SEO の初期設定")
    create_menus(secrets, category_ids, page_ids)

    # Save setup results
    setup_result = {
        "category_ids": category_ids,
        "page_ids": page_ids,
        "front_page_id": front_page_id,
    }
    result_path = CONFIG_DIR / "setup-result.json"
    with open(result_path, "w", encoding="utf-8") as f:
        json.dump(setup_result, f, ensure_ascii=False, indent=2)
    print(f"\nSetup results saved to: {result_path}")


if __name__ == "__main__":
    main()
