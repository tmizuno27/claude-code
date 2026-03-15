"""otona-match.com Affiliate Link Inserter
既存の公開済み記事にアフィリエイトリンクを挿入するスクリプト。
Usage: python insert_affiliate_links.py [--dry-run]
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

DISCLOSURE_TEXT = '<p style="font-size:0.85em;color:#666;margin-top:2em;padding:1em;background:#f9f9f9;border-radius:8px;">※この記事にはアフィリエイトリンクが含まれています。リンクを経由してご登録いただいた場合、当サイトに紹介料が発生しますが、読者の皆様への費用負担は一切ありません。</p>'

# マリッシュを挿入する記事 (WP ID -> 挿入位置の説明)
MARRISH_TARGETS = {
    138: "marrish-review",           # マリッシュレビュー（メイン記事）
    143: "matching-app-40dai-osusume",# 40代おすすめ
    151: "matching-app-batuichi-saikon",# バツイチ・再婚向け
    139: "konkatsu-40dai",           # 40代の婚活
    9:   "matching-app-ranking-2026",# ランキングTOP10
    155: "matching-app-nentai-betsu", # 年代別の選び方
    159: "matching-app-sotsukon-saikon",# 50代の活用術
    27:  "40dai-50dai-taikendan",    # 40代・50代の体験談
}

# ワクワクメールを挿入する記事
WAKUWAKU_TARGETS = {
    142: "wakuwaku-mail-review",     # ワクワクメールレビュー（メイン記事）
    14:  "deaikei-vs-matching-app",  # 出会い系vs.マッチングアプリ
    149: "deaikei-anzen-tsukaikata", # 安全な使い方
    9:   "matching-app-ranking-2026",# ランキングTOP10
}

MARRISH_CTA = '''<div style="margin:2em 0;padding:1.5em;background:linear-gradient(135deg,#fff5f5,#fff0f6);border:1px solid #ffccd5;border-radius:12px;text-align:center;">
<p style="font-size:1.1em;font-weight:bold;color:#e63946;margin-bottom:0.8em;">再婚・バツイチの方にはマリッシュがおすすめ</p>
<p style="margin-bottom:1em;color:#555;">真剣な出会いを求める方に特化したマッチングアプリ。再婚活・シンママ・シンパパを応援する優遇プログラムあり。</p>
<a href="https://px.a8.net/svt/ejp?a8mat=4AZGCF+DRY4GQ+3N2M+67JUA" rel="nofollow" style="display:inline-block;padding:12px 32px;background:#e63946;color:#fff;border-radius:8px;text-decoration:none;font-weight:bold;">マリッシュを無料で試す</a>
<img border="0" width="1" height="1" src="https://www10.a8.net/0.gif?a8mat=4AZGCF+DRY4GQ+3N2M+67JUA" alt="">
</div>'''

WAKUWAKU_CTA = '''<div style="margin:2em 0;padding:1.5em;background:linear-gradient(135deg,#f0f7ff,#e8f4fd);border:1px solid #b3d4fc;border-radius:12px;text-align:center;">
<p style="font-size:1.1em;font-weight:bold;color:#0066CC;margin-bottom:0.8em;">運営20年の安心感！ワクワクメール</p>
<p style="margin-bottom:1em;color:#555;">累計会員数1,000万人超の老舗出会い系サービス。安心・安全なマッチングを提供。</p>
<a href="https://px.a8.net/svt/ejp?a8mat=4AZGCF+F75EHM+1KZ4+601S2" rel="nofollow" style="display:inline-block;padding:12px 32px;background:#0066CC;color:#fff;border-radius:8px;text-decoration:none;font-weight:bold;">ワクワクメールを無料で試す</a>
<img border="0" width="1" height="1" src="https://www14.a8.net/0.gif?a8mat=4AZGCF+F75EHM+1KZ4+601S2" alt="">
</div>'''


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


def has_affiliate_link(content, a8mat_id):
    """Check if the affiliate link is already in the content."""
    return a8mat_id in content


def find_last_h2_position(content):
    """Find the position before the last H2 heading (good place for CTA)."""
    matches = list(re.finditer(r'<h2[^>]*>', content))
    if len(matches) >= 2:
        return matches[-1].start()
    return None


def find_first_h2_after_intro(content):
    """Find position after the first H2 section (after intro)."""
    matches = list(re.finditer(r'</h2>', content))
    if matches:
        # Find the end of the next paragraph after first h2
        first_h2_end = matches[0].end()
        next_p = content.find('</p>', first_h2_end)
        if next_p > 0:
            return next_p + 4
    return None


def insert_cta(content, cta_html, a8mat_id, is_main_article=False):
    """Insert CTA block into article content."""
    if has_affiliate_link(content, a8mat_id):
        return content, False

    if is_main_article:
        # Main review article: insert after intro + before last H2
        pos_after_intro = find_first_h2_after_intro(content)
        pos_before_last_h2 = find_last_h2_position(content)

        if pos_after_intro and pos_before_last_h2 and pos_after_intro < pos_before_last_h2:
            # Insert at both positions (reverse order to preserve positions)
            content = content[:pos_before_last_h2] + "\n" + cta_html + "\n" + content[pos_before_last_h2:]
            content = content[:pos_after_intro] + "\n" + cta_html + "\n" + content[pos_after_intro:]
        elif pos_before_last_h2:
            content = content[:pos_before_last_h2] + "\n" + cta_html + "\n" + content[pos_before_last_h2:]
        else:
            content += "\n" + cta_html
    else:
        # Related article: insert before last H2 only
        pos = find_last_h2_position(content)
        if pos:
            content = content[:pos] + "\n" + cta_html + "\n" + content[pos:]
        else:
            content += "\n" + cta_html

    return content, True


def add_disclosure(content):
    """Add affiliate disclosure if not present."""
    if "アフィリエイトリンクが含まれています" in content:
        return content, False
    content += "\n" + DISCLOSURE_TEXT
    return content, True


def fetch_all_posts(auth, ctx):
    """Fetch all published posts (paginated)."""
    all_posts = []
    page = 1
    while True:
        posts = wp_get(f"/wp/v2/posts&per_page=50&page={page}&status=publish", auth, ctx)
        if not posts:
            break
        all_posts.extend(posts)
        if len(posts) < 50:
            break
        page += 1
    return all_posts


if __name__ == "__main__":
    dry_run = "--dry-run" in sys.argv
    auth = get_auth()
    ctx = ssl.create_default_context()

    print(f"=== Affiliate Link Inserter ({'DRY RUN' if dry_run else 'LIVE'}) ===\n")

    # Fetch all posts
    print("Fetching all published posts...")
    posts = fetch_all_posts(auth, ctx)
    print(f"Found {len(posts)} published posts\n")

    # Build ID -> post lookup
    post_map = {post["id"]: post for post in posts}

    updated_count = 0

    # Process マリッシュ targets
    print("--- マリッシュ ---")
    marrish_a8mat = "4AZGCF+DRY4GQ+3N2M"
    for wp_id, slug in MARRISH_TARGETS.items():
        if wp_id not in post_map:
            print(f"  [SKIP] ID:{wp_id} ({slug}) - not found")
            continue

        post = post_map[wp_id]
        content = post["content"]["rendered"]
        is_main = (wp_id == 138)  # marrish-review is the main article

        new_content, inserted = insert_cta(content, MARRISH_CTA, marrish_a8mat, is_main)
        if inserted:
            new_content, _ = add_disclosure(new_content)
            print(f"  [INSERT] ID:{wp_id} ({slug}) {'(main: 2 CTAs)' if is_main else '(1 CTA)'}")
            if not dry_run:
                wp_update(wp_id, {"content": new_content}, auth, ctx)
            updated_count += 1
        else:
            print(f"  [SKIP] ID:{wp_id} ({slug}) - already has link")

    # Process ワクワクメール targets
    print("\n--- ワクワクメール ---")
    wakuwaku_a8mat = "4AZGCF+F75EHM+1KZ4"
    for wp_id, slug in WAKUWAKU_TARGETS.items():
        if wp_id not in post_map:
            print(f"  [SKIP] ID:{wp_id} ({slug}) - not found")
            continue

        post = post_map[wp_id]
        # Re-fetch if already modified by marrish insertion
        if wp_id in MARRISH_TARGETS and not dry_run and wp_id in [p["id"] for p in posts if p["id"] in MARRISH_TARGETS]:
            refreshed = wp_get(f"/wp/v2/posts/{wp_id}", auth, ctx)
            content = refreshed["content"]["rendered"]
        else:
            content = post["content"]["rendered"]

        is_main = (wp_id == 142)  # wakuwaku-mail-review is the main article

        new_content, inserted = insert_cta(content, WAKUWAKU_CTA, wakuwaku_a8mat, is_main)
        if inserted:
            new_content, _ = add_disclosure(new_content)
            print(f"  [INSERT] ID:{wp_id} ({slug}) {'(main: 2 CTAs)' if is_main else '(1 CTA)'}")
            if not dry_run:
                wp_update(wp_id, {"content": new_content}, auth, ctx)
            updated_count += 1
        else:
            print(f"  [SKIP] ID:{wp_id} ({slug}) - already has link")

    print(f"\n=== Complete: {updated_count} articles {'would be' if dry_run else ''} updated ===")
