"""
WordPress全記事からYAMLフロントマター（---で囲まれたメタデータ）を除去するスクリプト
3サイト対応: nambei-oyaji.com, otona-match.com, sim-hikaku.online
"""
import sys
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
import requests
import re
import json
import base64

SITES = [
    {
        "name": "nambei-oyaji.com",
        "api_url": "https://nambei-oyaji.com/wp-json/wp/v2",
        "username": "t.mizuno27@gmail.com",
        "app_password": "agNg 2624 4lL4 QoT9 EOOZ OEZr",
    },
    {
        "name": "otona-match.com",
        "api_url": "https://otona-match.com/?rest_route=/wp/v2",
        "username": "t.mizuno27@gmail.com",
        "app_password": "Yw4j OgFf wwzT o0mn wXQ9 TjYs",
    },
    {
        "name": "sim-hikaku.online",
        "api_url": "https://sim-hikaku.online/wp-json/wp/v2",
        "username": "t.mizuno27@gmail.com",
        "app_password": "P4A1 P4eh Nk0z 29An hS6H 9OHq",
    },
]

FRONTMATTER_PATTERNS = [
    # HTML内のフロントマター（<p>タグ等で囲まれている場合）
    re.compile(r'<p>---\s*</p>\s*(?:<p>.*?</p>\s*)*?<p>---\s*</p>', re.DOTALL),
    # プレーンテキストのフロントマター
    re.compile(r'^---\s*\n.*?\n---\s*\n', re.DOTALL),
    # preタグ内のフロントマター
    re.compile(r'<pre[^>]*>---\s*\n.*?\n---\s*</pre>', re.DOTALL),
    # divで囲まれたフロントマター
    re.compile(r'<div[^>]*>---\s*\n.*?\n---\s*</div>', re.DOTALL),
]

# フロントマターの特徴的なキー
FM_KEYS = ['title:', 'focus_keyword:', 'meta_description:', 'category:', 'tags:', 'article_type:', 'pillar:', 'affiliate_disclosure:']


def has_frontmatter(content):
    """コンテンツにフロントマターが含まれているか判定"""
    if not content:
        return False
    # --- で始まるパターン
    if re.search(r'---\s*\n', content):
        # フロントマターのキーが含まれているかチェック
        for key in FM_KEYS:
            if key in content:
                return True
    return False


def remove_frontmatter(content):
    """コンテンツからフロントマターを除去"""
    original = content

    for pattern in FRONTMATTER_PATTERNS:
        content = pattern.sub('', content, count=1)

    # もしパターンで除去できなかった場合、行単位で処理
    if has_frontmatter(content):
        lines = content.split('\n')
        in_fm = False
        fm_start = -1
        fm_end = -1
        for i, line in enumerate(lines):
            stripped = re.sub(r'<[^>]+>', '', line).strip()
            if stripped == '---':
                if not in_fm:
                    in_fm = True
                    fm_start = i
                else:
                    fm_end = i
                    break

        if fm_start >= 0 and fm_end > fm_start:
            # フロントマター部分にFM_KEYSが含まれるか確認
            fm_block = '\n'.join(lines[fm_start:fm_end+1])
            if any(key in fm_block for key in FM_KEYS):
                lines = lines[:fm_start] + lines[fm_end+1:]
                content = '\n'.join(lines)

    # 先頭の空白行を除去
    content = content.lstrip('\n')

    return content


def get_auth_header(username, app_password):
    token = base64.b64encode(f"{username}:{app_password}".encode()).decode()
    return {"Authorization": f"Basic {token}"}


def process_site(site):
    print(f"\n{'='*60}")
    print(f"サイト: {site['name']}")
    print(f"{'='*60}")

    headers = get_auth_header(site["username"], site["app_password"])

    # 全記事を取得（公開+下書き+予約）
    all_posts = []
    for status in ["publish", "draft", "pending", "future", "private"]:
        page = 1
        while True:
            params = {"status": status, "per_page": 100, "page": page}
            try:
                resp = requests.get(f"{site['api_url']}/posts", headers=headers, params=params, timeout=30)
                if resp.status_code != 200:
                    break
                posts = resp.json()
                if not posts:
                    break
                all_posts.extend(posts)
                page += 1
                if len(posts) < 100:
                    break
            except Exception as e:
                print(f"  エラー ({status}, page {page}): {e}")
                break

    # 固定ページも取得
    for status in ["publish", "draft"]:
        page = 1
        while True:
            params = {"status": status, "per_page": 100, "page": page}
            try:
                resp = requests.get(f"{site['api_url']}/pages", headers=headers, params=params, timeout=30)
                if resp.status_code != 200:
                    break
                pages = resp.json()
                if not pages:
                    break
                for p in pages:
                    p["_type"] = "page"
                all_posts.extend(pages)
                page += 1
                if len(pages) < 100:
                    break
            except Exception as e:
                break

    print(f"  取得記事数: {len(all_posts)}")

    fixed_count = 0
    for post in all_posts:
        post_id = post["id"]
        title = post["title"]["rendered"]
        content = post["content"]["rendered"]
        post_type = post.get("_type", "post")

        if has_frontmatter(content):
            cleaned = remove_frontmatter(content)
            if cleaned != content:
                print(f"  [修正] ID:{post_id} ({post_type}) - {title[:50]}")

                # 更新
                endpoint = f"{site['api_url']}/{'pages' if post_type == 'page' else 'posts'}/{post_id}"
                update_resp = requests.post(
                    endpoint,
                    headers=headers,
                    json={"content": cleaned},
                    timeout=30
                )
                if update_resp.status_code == 200:
                    print(f"    OK 修正完了")
                    fixed_count += 1
                else:
                    print(f"    NG 修正失敗: {update_resp.status_code} - {update_resp.text[:200]}")
            else:
                print(f"  [検出・除去不能] ID:{post_id} - {title[:50]}")
        else:
            pass  # フロントマターなし（正常）

    print(f"\n  修正完了: {fixed_count}件")
    return fixed_count


if __name__ == "__main__":
    total = 0
    for site in SITES:
        total += process_site(site)
    print(f"\n{'='*60}")
    print(f"全サイト合計修正: {total}件")
