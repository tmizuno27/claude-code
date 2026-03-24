#!/usr/bin/env python3
"""
アフィリエイトリンク挿入状況監査スクリプト（統合版）
3サイトのWordPress全公開記事を取得し、各ASPのリンク挿入状況を集計する

統合元:
- check_affiliate.py (nambei専用) — キーワード文脈チェック機能
- check_affiliates.py (sim専用) — A8固有IDパターン検出
- affiliate_link_audit.py — 3サイト横断監査（ベース）
"""
import sys
import json
import os
import re
import base64
import time
from datetime import datetime
from collections import defaultdict

import requests
from bs4 import BeautifulSoup

sys.stdout.reconfigure(encoding="utf-8")

# =====================
# ログ出力設定
# =====================
LOG_DIR = "c:/Users/tmizu/マイドライブ/GitHub/claude-code/logs"
LOG_FILE = os.path.join(LOG_DIR, "affiliate-audit.log")

_log_file_handle = None


def init_log():
    """ログファイルを初期化（追記モード）"""
    global _log_file_handle
    os.makedirs(LOG_DIR, exist_ok=True)
    _log_file_handle = open(LOG_FILE, "a", encoding="utf-8")
    log(f"\n{'#'*70}")
    log(f"# 監査実行: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    log(f"{'#'*70}")


def close_log():
    """ログファイルを閉じる"""
    global _log_file_handle
    if _log_file_handle:
        _log_file_handle.close()
        _log_file_handle = None


def log(message=""):
    """print + ログファイル書き出し"""
    print(message)
    if _log_file_handle:
        _log_file_handle.write(message + "\n")
        _log_file_handle.flush()


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
        "api_url": None,
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

# =====================
# キーワード別アフィリエイト案件定義
# キーワードが記事中に出現した場合、対応するアフィリエイトリンクが
# 貼られているかをチェックする
# =====================
AFFILIATE_CASES = [
    # --- nambei-oyaji.com 由来 ---
    {"name": "Wise", "keywords": ["Wise", "ワイズ"], "url_patterns": ["wise.com/invite"]},
    {"name": "Revolut", "keywords": ["Revolut", "レボリュート"], "url_patterns": ["revolut.com/referral"]},
    {"name": "NordVPN", "keywords": ["NordVPN", "ノードVPN"], "url_patterns": ["px.a8.net"]},
    {"name": "ExpressVPN", "keywords": ["ExpressVPN"], "url_patterns": ["px.a8.net"]},
    {"name": "Surfshark", "keywords": ["Surfshark", "サーフシャーク"], "url_patterns": ["px.a8.net"]},
    {"name": "ConoHa WING", "keywords": ["ConoHa WING", "コノハウィング", "ConoHa"], "url_patterns": ["px.a8.net"]},
    {"name": "Xserver", "keywords": ["エックスサーバー", "Xserver"], "url_patterns": ["px.a8.net"]},
    {"name": "NativeCamp", "keywords": ["ネイティブキャンプ", "NativeCamp"], "url_patterns": ["px.a8.net"]},
    {"name": "エポスカード", "keywords": ["エポスカード", "EPOS", "エポス"], "url_patterns": ["px.a8.net"]},
    {"name": "DMM WEBCAMP", "keywords": ["DMM WEBCAMP", "DMMウェブキャンプ"], "url_patterns": ["af.moshimo.com", "dmm-webcamp"]},
    {"name": "クラウドワークス", "keywords": ["クラウドワークス", "CrowdWorks"], "url_patterns": ["px.a8.net"]},
    {"name": "ココナラ", "keywords": ["ココナラ", "coconala"], "url_patterns": ["px.a8.net"]},
    {"name": "trifa", "keywords": ["trifa", "トリファ"], "url_patterns": ["px.a8.net"], "a8_id_pattern": r"4AZH4C\.CWZK8I"},
    {"name": "TRAVeSIM", "keywords": ["TRAVeSIM", "トラベシム"], "url_patterns": ["px.a8.net"], "a8_id_pattern": r"4AZH48\.2M2JWI"},
    {"name": "Voye Global", "keywords": ["Voye", "ボイエ", "Voye Global"], "url_patterns": ["px.a8.net"], "a8_id_pattern": r"4AZH48\.2G47UQ"},
    # --- sim-hikaku.online 由来 ---
    {"name": "ワイモバイル", "keywords": ["ワイモバイル", "Y!mobile", "ymobile", "Ymobile"], "url_patterns": ["px.a8.net"], "a8_id_pattern": r"4AZH48\.1XNS3M"},
]


def load_credentials(config_path, default_api_url):
    """secrets.jsonから認証情報を読み込む"""
    with open(config_path, encoding="utf-8") as f:
        data = json.load(f)
    wp = data.get("wordpress", {})
    username = wp.get("username", "")
    app_password = wp.get("app_password", "")
    api_url = wp.get("api_url", default_api_url)
    return username, app_password, api_url


def make_headers_base64(username, app_password):
    """Base64認証ヘッダーを生成"""
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
                break
            resp.raise_for_status()
            posts = resp.json()
            if not posts:
                break
            all_posts.extend(posts)
            total_pages = int(resp.headers.get("X-WP-TotalPages", 1))
            log(f"  ページ {page}/{total_pages} 取得: {len(posts)}件")
            if page >= total_pages:
                break
            page += 1
            time.sleep(0.5)
        except Exception as e:
            log(f"  エラー(page={page}): {e}")
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


def check_keyword_contexts(content, cases):
    """
    キーワード文脈チェック（check_affiliate.py由来）
    記事コンテンツ中のキーワード出現箇所を調べ、
    アフィリエイトリンクが貼られているかを判定する。

    戻り値: [
        {
            "case_name": str,
            "keyword": str,
            "link_type": "affiliate" | "other_link" | "plain_text",
            "href": str or None,
            "has_specific_a8_id": bool,
        }, ...
    ]
    """
    results = []
    for case in cases:
        has_keyword = any(
            re.search(re.escape(kw), content, re.IGNORECASE)
            for kw in case["keywords"]
        )
        if not has_keyword:
            continue

        for kw in case["keywords"]:
            for m in re.finditer(re.escape(kw), content, re.IGNORECASE):
                start = m.start()
                # Find nearest <a href> before this keyword (if keyword is inside a link)
                all_a = list(re.finditer(
                    r'<a\s[^>]*href=["\']([^"\']+)["\'][^>]*>',
                    content[:start], re.IGNORECASE
                ))
                all_close = list(re.finditer(r'</a>', content[:start], re.IGNORECASE))

                href = None
                if all_a:
                    last_a = all_a[-1]
                    last_close = all_close[-1] if all_close else None
                    if last_close is None or last_a.start() > last_close.start():
                        href = last_a.group(1)

                is_affiliate = False
                has_specific_a8 = False
                if href:
                    is_affiliate = any(pat in href for pat in case["url_patterns"])
                    # A8固有IDチェック
                    if case.get("a8_id_pattern") and is_affiliate:
                        has_specific_a8 = bool(
                            re.search(case["a8_id_pattern"], href, re.IGNORECASE)
                        )

                if is_affiliate:
                    link_type = "affiliate"
                elif href:
                    link_type = "other_link"
                else:
                    link_type = "plain_text"

                results.append({
                    "case_name": case["name"],
                    "keyword": kw,
                    "link_type": link_type,
                    "href": href,
                    "has_specific_a8_id": has_specific_a8,
                })
                # One match per keyword is enough
                break

    # Deduplicate by (case_name, link_type)
    seen = set()
    deduped = []
    for r in results:
        key = (r["case_name"], r["link_type"])
        if key not in seen:
            seen.add(key)
            deduped.append(r)
    return deduped


def analyze_site(site_config):
    """1サイト分の解析を実行"""
    name = site_config["name"]
    display = site_config["display"]
    log(f"\n{'='*60}")
    log(f"解析開始: {display} ({name})")
    log(f"{'='*60}")

    username, app_password, api_url = load_credentials(
        site_config["config"], site_config.get("api_url", "")
    )
    if not api_url:
        api_url = site_config.get("api_url", "")

    log(f"API URL: {api_url}")

    posts_endpoint = site_config.get("posts_endpoint")
    if not posts_endpoint:
        posts_endpoint = f"{api_url}/posts"

    auth_type = site_config.get("auth_type", "base64")
    if auth_type == "basic":
        auth = (username, app_password)
        headers = {}
    else:
        auth = None
        headers = make_headers_base64(username, app_password)

    log("記事取得中...")
    posts = fetch_all_posts(posts_endpoint, headers, auth)
    total_posts = len(posts)
    log(f"取得完了: {total_posts}件")

    if total_posts == 0:
        log("記事が取得できませんでした。")
        return None

    # ASP別集計
    asp_article_ids = defaultdict(set)
    link_article_ids = defaultdict(set)

    # キーワード文脈チェック結果
    keyword_findings = []  # (post_id, title, finding_dict)

    for post in posts:
        post_id = post.get("id")
        title_data = post.get("title", {})
        if isinstance(title_data, dict):
            title = re.sub(r"<[^>]+>", "", title_data.get("rendered", title_data.get("raw", "(no title)")))
        else:
            title = str(title_data)

        content_raw = post.get("content", {})
        if isinstance(content_raw, dict):
            content_raw = content_raw.get("raw", content_raw.get("rendered", ""))
        if not content_raw:
            continue

        # ASPリンク抽出
        links = extract_affiliate_links(content_raw)
        for asp, href, anchor in links:
            asp_article_ids[asp].add(post_id)
            link_article_ids[(asp, href, anchor)].add(post_id)

        # キーワード文脈チェック
        findings = check_keyword_contexts(content_raw, AFFILIATE_CASES)
        for f in findings:
            keyword_findings.append((post_id, title, f))

    return {
        "name": name,
        "display": display,
        "total_posts": total_posts,
        "asp_article_ids": asp_article_ids,
        "link_article_ids": link_article_ids,
        "keyword_findings": keyword_findings,
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
    keyword_findings = result["keyword_findings"]

    log(f"\n{'='*70}")
    log(f"=== {display} ({name}) ===")
    log(f"{'='*70}")
    log(f"全公開記事数: {total}件")

    # --- ASP別サマリー ---
    log(f"\n【ASP別サマリー】")
    log(f"{'ASP':<25} {'リンク挿入記事数':>15} {'ユニークリンク数':>15}")
    log("-" * 60)

    all_asps = list(ASP_PATTERNS.keys())
    for asp in all_asps:
        article_count = len(asp_ids.get(asp, set()))
        unique_links = sum(1 for (a, h, t) in link_ids.keys() if a == asp)
        log(f"{asp:<25} {article_count:>15}件 {unique_links:>14}本")

    detected_asps = set(asp_ids.keys())
    log(f"\n※ リンク検出なし: {', '.join(a for a in all_asps if a not in detected_asps) or 'なし'}")

    # --- リンク別詳細 ---
    log(f"\n【リンク別詳細】")
    log(f"{'ASP':<20} {'アンカーテキスト/URL':<50} {'記事数':>6} {'記事IDリスト'}")
    log("-" * 110)

    sorted_links = sorted(
        link_ids.items(),
        key=lambda x: (all_asps.index(x[0][0]) if x[0][0] in all_asps else 99, -len(x[1]), x[0][2]),
    )

    for (asp, href, anchor), post_ids in sorted_links:
        display_url = href[:60] + "..." if len(href) > 60 else href
        anchor_display = anchor[:30] + "..." if len(anchor) > 30 else anchor
        label = f"{anchor_display} | {display_url}"
        label = label[:75]
        ids_str = ", ".join(str(i) for i in sorted(post_ids))
        log(f"{asp:<20} {label:<75} {len(post_ids):>5}件  [{ids_str}]")

    # --- キーワード文脈チェック結果 ---
    if keyword_findings:
        unlinked = [
            (pid, title, f) for pid, title, f in keyword_findings
            if f["link_type"] != "affiliate"
        ]
        linked = [
            (pid, title, f) for pid, title, f in keyword_findings
            if f["link_type"] == "affiliate"
        ]

        log(f"\n【キーワード文脈チェック】")
        log(f"検出数: {len(keyword_findings)}件 (OK: {len(linked)}, 要対応: {len(unlinked)})")

        if unlinked:
            log(f"\n▼ 要対応（キーワードにアフィリエイトリンク未設定）")
            by_case = defaultdict(list)
            for pid, title, f in unlinked:
                by_case[f["case_name"]].append((pid, title, f))
            for case_name in sorted(by_case.keys()):
                log(f"  [{case_name}]")
                for pid, title, f in by_case[case_name]:
                    status = "素テキスト" if f["link_type"] == "plain_text" else f"別リンク: {(f['href'] or '')[:60]}"
                    log(f"    ID:{pid} {title[:40]} → {status}")

    # --- 全記事でキーワード未検出の案件 ---
    detected_cases = {f["case_name"] for _, _, f in keyword_findings}
    undetected = [c["name"] for c in AFFILIATE_CASES if c["name"] not in detected_cases]
    if undetected:
        log(f"\n【全記事でキーワード未検出の案件】")
        for name in undetected:
            log(f"  {name}")


def main():
    init_log()
    try:
        log("=" * 70)
        log("アフィリエイトリンク挿入状況 監査レポート（統合版）")
        log(f"実行日時: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        log("=" * 70)

        all_results = []
        for site in SITES:
            try:
                result = analyze_site(site)
                all_results.append(result)
            except Exception as e:
                log(f"ERROR: {site['name']} の処理中にエラー: {e}")
                import traceback
                traceback.print_exc()

        log("\n\n" + "=" * 70)
        log("【最終レポート】")
        log("=" * 70)
        for result in all_results:
            print_results(result)

        # 全サイト横断サマリー
        valid_results = [r for r in all_results if r]
        log(f"\n\n{'='*70}")
        log("【3サイト横断 ASP別サマリー】")
        log(f"{'='*70}")
        log(f"{'ASP':<25} " + "  ".join(f"{r['display'][:15]:<15}" for r in valid_results))
        log("-" * 80)
        for asp in ASP_PATTERNS.keys():
            row = f"{asp:<25} "
            for r in valid_results:
                count = len(r["asp_article_ids"].get(asp, set()))
                total = r["total_posts"]
                if total:
                    row += f"{count}/{total}件 ({count/total*100:.0f}%)  "
                else:
                    row += "N/A  "
            log(row)

        # 全サイト横断キーワード要対応サマリー
        all_unlinked = []
        for r in valid_results:
            if r and r.get("keyword_findings"):
                for pid, title, f in r["keyword_findings"]:
                    if f["link_type"] != "affiliate":
                        all_unlinked.append((r["name"], pid, title, f))

        if all_unlinked:
            log(f"\n\n{'='*70}")
            log(f"【3サイト横断 キーワード未リンク要対応一覧】({len(all_unlinked)}件)")
            log(f"{'='*70}")
            for site_name, pid, title, f in all_unlinked:
                status = "素テキスト" if f["link_type"] == "plain_text" else "別リンク"
                log(f"  [{site_name}] ID:{pid} [{f['case_name']}] {title[:40]} → {status}")

        log(f"\nログ保存先: {LOG_FILE}")
    finally:
        close_log()


if __name__ == "__main__":
    main()
