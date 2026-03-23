#!/usr/bin/env python3
"""
アフィリエイトリンク挿入状況監査スクリプト
3サイトのWordPress全公開記事を取得し、各ASPのリンク挿入状況を集計する
"""
import json
import re
import base64
import time
from collections import defaultdict
from urllib.parse import urlparse, parse_qs

import requests
from bs4 import BeautifulSoup

# =====================
# サイト設定
# =====================
SITES = [
    {
        "name": "nambei-oyaji.com",
        "display": "南米おやじの海外生活ラボ",
        "config": "c:/Users/tmizu/マイドライブ/GitHub/claude-code/sites/nambei-oyaji.com/config/secrets.json",
        "api_url": "https://nambei-oyaji.com/wp-json/wp/v2",
        "auth_type": "base64",
    },
    {
        "name": "otona-match.com",
        "display": "大人のマッチングナビ",
        "config": "c:/Users/tmizu/マイドライブ/GitHub/claude-code/sites/otona-match.com/config/secrets.json",
        "api_url": "https://otona-match.com/?rest_route=/wp/v2",
        "posts_endpoint": "https://otona-match.com/?rest_route=/wp/v2/posts",
        "auth_type": "basic",
    },
    {
        "name": "sim-hikaku.online",
        "display": "SIM比較ナビ",
        "config": "c:/Users/tmizu/マイドライブ/GitHub/claude-code/sites/sim-hikaku.online/config/secrets.json",
        "api_url": None,  # secrets.jsonから取得
        "auth_type": "base64",
    },
]

# =====================
# ASP検出パターン
# =====================
ASP_PATTERNS = {
    "A8.net": [r"px\.a8\.net", r"a8mat="],
    "アクセストレード": [r"h\.accesstrade\.net", r"accesstrade\.net"],
    "もしもアフィリエイト": [r"af\.moshimo\.com", r"moshimo\.com"],
    "Value Commerce": [r"ck\.jp\.ap\.valuecommerce\.com", r"valuecommerce\.com"],
    "直接リンク": [
        r"wise\.com/invite",
        r"revolut\.com/referral",
        r"wise\.com",
        r"revolut\.com",
    ],
}


def load_credentials(config_path, default_api_url):
    with open(config_path, encoding="utf-8") as f:
        data = json.load(f)
    wp = data.get("wordpress", {})
    username = wp.get("username", "")
    app_password = wp.get("app_password", "")
    api_url = wp.get("api_url", default_api_url)
    return username, app_password, api_url


def make_headers_base64(username, app_password):
    token = base64.b64encode(f"{username}:{app_password}".encode()).decode()
    return {"Authorization": f"Basic {token}"}


def fetch_all_posts(posts_url, headers, auth=None):
    """全公開記事を取得（ページネーション対応）"""
    all_posts = []
    page = 1
    while True:
        params = {
            "status": "publish",
            "per_page": 100,
            "page": page,
            "context": "edit",
        }
        try:
            if auth:
                resp = requests.get(posts_url, params=params, auth=auth, timeout=30)
            else:
                resp = requests.get(posts_url, params=params, headers=headers, timeout=30)

            if resp.status_code == 400:
                # ページ超過
                break
            resp.raise_for_status()
            posts = resp.json()
            if not posts:
                break
            all_posts.extend(posts)
            total_pages = int(resp.headers.get("X-WP-TotalPages", 1))
            print(f"  ページ {page}/{total_pages} 取得: {len(posts)}件")
            if page >= total_pages:
                break
            page += 1
            time.sleep(0.5)
        except Exception as e:
            print(f"  エラー(page={page}): {e}")
            break
    return all_posts


def detect_asp(url):
    """URLからASPを判定"""
    for asp_name, patterns in ASP_PATTERNS.items():
        for pattern in patterns:
            if re.search(pattern, url, re.IGNORECASE):
                return asp_name
    return None


def extract_affiliate_links(content_raw):
    """
    記事コンテンツからアフィリエイトリンクを抽出
    戻り値: [(asp_name, href, anchor_text), ...]
    """
    soup = BeautifulSoup(content_raw, "html.parser")
    found = []
    seen = set()

    for a_tag in soup.find_all("a", href=True):
        href = a_tag.get("href", "").strip()
        if not href or href.startswith("#"):
            continue

        asp = detect_asp(href)
        if asp:
            anchor = a_tag.get_text(strip=True) or "(テキストなし)"
            key = (asp, href, anchor)
            if key not in seen:
                seen.add(key)
                found.append((asp, href, anchor))

    return found


def analyze_site(site_config):
    """1サイト分の解析を実行"""
    name = site_config["name"]
    display = site_config["display"]
    print(f"\n{'='*60}")
    print(f"解析開始: {display} ({name})")
    print(f"{'='*60}")

    # 認証情報の読み込み
    username, app_password, api_url = load_credentials(
        site_config["config"], site_config.get("api_url", "")
    )
    if not api_url:
        api_url = site_config.get("api_url", "")

    print(f"API URL: {api_url}")

    # 記事取得エンドポイントの決定
    posts_endpoint = site_config.get("posts_endpoint")
    if not posts_endpoint:
        posts_endpoint = f"{api_url}/posts"

    # 認証方式
    auth_type = site_config.get("auth_type", "base64")
    if auth_type == "basic":
        auth = (username, app_password)
        headers = {}
    else:
        auth = None
        headers = make_headers_base64(username, app_password)

    print(f"記事取得中...")
    posts = fetch_all_posts(posts_endpoint, headers, auth)
    total_posts = len(posts)
    print(f"取得完了: {total_posts}件")

    if total_posts == 0:
        print("記事が取得できませんでした。")
        return None

    # ASP別集計
    # asp_article_count[asp] = set(post_ids)
    asp_article_ids = defaultdict(set)

    # リンク別集計
    # link_data[(asp, href, anchor)] = set(post_ids)
    link_article_ids = defaultdict(set)

    for post in posts:
        post_id = post.get("id")
        content_raw = post.get("content", {})
        if isinstance(content_raw, dict):
            content_raw = content_raw.get("raw", content_raw.get("rendered", ""))
        if not content_raw:
            continue

        links = extract_affiliate_links(content_raw)
        for asp, href, anchor in links:
            asp_article_ids[asp].add(post_id)
            link_article_ids[(asp, href, anchor)].add(post_id)

    return {
        "name": name,
        "display": display,
        "total_posts": total_posts,
        "asp_article_ids": asp_article_ids,
        "link_article_ids": link_article_ids,
    }


def print_results(result):
    """結果を整形して出力"""
    if result is None:
        return

    name = result["name"]
    display = result["display"]
    total = result["total_posts"]
    asp_ids = result["asp_article_ids"]
    link_ids = result["link_article_ids"]

    print(f"\n{'='*70}")
    print(f"=== {display} ({name}) ===")
    print(f"{'='*70}")
    print(f"全公開記事数: {total}件")

    print(f"\n【ASP別サマリー】")
    print(f"{'ASP':<25} {'リンク挿入記事数':>15} {'ユニークリンク数':>15}")
    print("-" * 60)

    all_asps = list(ASP_PATTERNS.keys())
    for asp in all_asps:
        article_count = len(asp_ids.get(asp, set()))
        unique_links = sum(1 for (a, h, t) in link_ids.keys() if a == asp)
        if article_count > 0 or True:  # 0件でも表示
            print(f"{asp:<25} {article_count:>15}件 {unique_links:>14}本")

    # 未検出ASPチェック
    detected_asps = set(asp_ids.keys())
    print(f"\n※ リンク検出なし: {', '.join(a for a in all_asps if a not in detected_asps) or 'なし'}")

    print(f"\n【リンク別詳細】")
    print(f"{'ASP':<20} {'アンカーテキスト/URL':<50} {'記事数':>6} {'記事IDリスト'}")
    print("-" * 110)

    # ASP順に並べる
    sorted_links = sorted(
        link_ids.items(),
        key=lambda x: (all_asps.index(x[0][0]) if x[0][0] in all_asps else 99, -len(x[1]), x[0][2])
    )

    for (asp, href, anchor), post_ids in sorted_links:
        # URL短縮表示
        display_url = href[:60] + "..." if len(href) > 60 else href
        anchor_display = anchor[:30] + "..." if len(anchor) > 30 else anchor
        label = f"{anchor_display} | {display_url}"
        label = label[:75]
        ids_str = ", ".join(str(i) for i in sorted(post_ids))
        print(f"{asp:<20} {label:<75} {len(post_ids):>5}件  [{ids_str}]")


def main():
    print("=" * 70)
    print("アフィリエイトリンク挿入状況 監査レポート")
    print("=" * 70)

    all_results = []
    for site in SITES:
        try:
            result = analyze_site(site)
            all_results.append(result)
        except Exception as e:
            print(f"ERROR: {site['name']} の処理中にエラー: {e}")
            import traceback
            traceback.print_exc()

    print("\n\n" + "=" * 70)
    print("【最終レポート】")
    print("=" * 70)
    for result in all_results:
        print_results(result)

    # 全サイト横断サマリー
    print(f"\n\n{'='*70}")
    print("【3サイト横断 ASP別サマリー】")
    print(f"{'='*70}")
    print(f"{'ASP':<25} " + "  ".join(f"{r['display'][:15]:<15}" for r in all_results if r))
    print("-" * 80)
    for asp in ASP_PATTERNS.keys():
        row = f"{asp:<25} "
        for r in all_results:
            if r is None:
                row += f"{'N/A':>15}  "
            else:
                count = len(r['asp_article_ids'].get(asp, set()))
                total = r['total_posts']
                row += f"{count}/{total}件 ({count/total*100:.0f}%)  " if total else "N/A  "
        print(row)


if __name__ == "__main__":
    main()
