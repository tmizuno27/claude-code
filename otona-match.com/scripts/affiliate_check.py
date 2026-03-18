#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
otona-match.com アフィリエイトリンク最終チェックスクリプト
"""

import json
import re
import sys
from collections import defaultdict
from urllib.parse import urlparse

import requests
from requests.auth import HTTPBasicAuth

# ── 設定 ──────────────────────────────────────────────
CONFIG_DIR = r"C:\Users\tmizu\マイドライブ\GitHub\claude-code\otona-match.com\config"
SECRETS_FILE = f"{CONFIG_DIR}/secrets.json"
AFFILIATE_FILE = f"{CONFIG_DIR}/affiliate-links.json"
WP_BASE = "https://otona-match.com/?rest_route=/wp/v2"

# ── 認証読み込み ──────────────────────────────────────
with open(SECRETS_FILE, encoding="utf-8") as f:
    secrets = json.load(f)

wp_user = secrets["wordpress"]["username"]
wp_pass = secrets["wordpress"]["app_password"]
auth = HTTPBasicAuth(wp_user, wp_pass)

# ── アフィリエイトリンク読み込み ──────────────────────
with open(AFFILIATE_FILE, encoding="utf-8") as f:
    aff_data = json.load(f)

# active リンクを抽出
active_links = []
for cat_key, cat in aff_data["categories"].items():
    for link in cat["links"]:
        if link.get("status") == "active":
            link["category"] = cat_key
            active_links.append(link)

print(f"Active リンク数: {len(active_links)}")
print()

# ── WordPress 全公開記事取得 ──────────────────────────
def fetch_all_posts():
    posts = []
    page = 1
    while True:
        resp = requests.get(
            f"{WP_BASE}/posts",
            params={"status": "publish", "per_page": 100, "page": page},
            auth=auth,
            timeout=30,
        )
        if resp.status_code != 200:
            print(f"[ERROR] 記事取得失敗: {resp.status_code}", file=sys.stderr)
            break
        batch = resp.json()
        if not batch:
            break
        posts.extend(batch)
        total_pages = int(resp.headers.get("X-WP-TotalPages", 1))
        if page >= total_pages:
            break
        page += 1
    return posts

print("WordPress 記事取得中...")
posts = fetch_all_posts()
print(f"公開記事数: {len(posts)}")
print()

# ── 各記事からアフィリエイトリンク抽出 ──────────────
PLACEHOLDER_RE = re.compile(r"YOUR[-_]AFFILIATE[-_]LINK|YOUR[-_]LINK|placeholder", re.I)
HREF_RE = re.compile(r'<a\s[^>]*href=["\']([^"\']+)["\']', re.I)
IMG_1X1_RE = re.compile(
    r'<img\s[^>]*(width=["\']1["\'][^>]*height=["\']1["\']|height=["\']1["\'][^>]*width=["\']1["\'])[^>]*>',
    re.I,
)

# 問題点リスト
problems = []

# 記事別リンク数
article_link_counts = []

# active リンクのカバレッジ追跡
# key: link name, value: list of article titles where found
link_coverage = {lnk["name"]: [] for lnk in active_links}

# ASP 別カウント
asp_found = defaultdict(set)  # asp -> set of link names found
asp_total = defaultdict(set)  # asp -> set of all active link names
for lnk in active_links:
    asp_total[lnk["asp"]].add(lnk["name"])

for post in posts:
    content = post.get("content", {}).get("rendered", "")
    title = post.get("title", {}).get("rendered", "（タイトル不明）")
    post_id = post.get("id")
    url = post.get("link", "")

    # href 抽出
    hrefs = HREF_RE.findall(content)
    aff_hrefs = [h for h in hrefs if any(
        domain in h for domain in [
            "px.a8.net", "www.a8.net", "a8.net",
            "accesstrade.net",
            "af.moshimo.com", "i.moshimo.com",
            "valuecommerce.com",
            "ck.jp.ap.valuecommerce.com",
        ]
    )]
    article_link_counts.append({
        "id": post_id,
        "title": title,
        "url": url,
        "aff_link_count": len(aff_hrefs),
    })

    # プレースホルダー残り確認
    if PLACEHOLDER_RE.search(content):
        problems.append({
            "type": "PLACEHOLDER残り",
            "post_id": post_id,
            "title": title,
            "url": url,
            "detail": "YOUR-AFFILIATE-LINK 等のプレースホルダーが残っています",
        })

    # 壊れた URL チェック（href が空や # のみ）
    for href in hrefs:
        if href.strip() in ("", "#", "javascript:void(0)"):
            problems.append({
                "type": "壊れたリンク",
                "post_id": post_id,
                "title": title,
                "url": url,
                "detail": f"空または無効な href: '{href}'",
            })

    # 1x1 トラッキングピクセルの存在確認
    # A8/アクセストレード/もしも/VC のリンクがある記事でピクセルがあるか
    if aff_hrefs:
        if not IMG_1X1_RE.search(content):
            # ピクセル画像 URL を直接検索
            pixel_domains = [
                "a8.net/0.gif", "www.a8.net", "accesstrade.net/sp/rr",
                "i.moshimo.com", "valuecommerce.com/servlet/gifbanner",
                "ad.jp.ap.valuecommerce.com",
            ]
            has_pixel = any(d in content for d in pixel_domains)
            if not has_pixel:
                problems.append({
                    "type": "トラッキングピクセル欠落疑い",
                    "post_id": post_id,
                    "title": title,
                    "url": url,
                    "detail": f"アフィリエイトリンク {len(aff_hrefs)}件あるがピクセル画像が見当たらない",
                })

    # active リンクのカバレッジ判定
    for lnk in active_links:
        found = False
        # html フィールドあり → href で照合
        if lnk.get("html"):
            # html 内の href を抽出して照合
            html_hrefs = HREF_RE.findall(lnk["html"])
            for hhref in html_hrefs:
                if hhref and hhref in content:
                    found = True
                    break
        # url フィールドあり
        if not found and lnk.get("url") and lnk["url"] in content:
            found = True
        if not found and lnk.get("url_moshimo") and lnk["url_moshimo"] in content:
            found = True
        if found:
            link_coverage[lnk["name"]].append(title)
            asp_found[lnk["asp"]].add(lnk["name"])

# ── 出力 ──────────────────────────────────────────────
SEP = "=" * 70

print(SEP)
print("【1】 ASP別 アフィリエイトリンク挿入カバレッジ")
print(SEP)
for asp in sorted(asp_total.keys()):
    total = asp_total[asp]
    found = asp_found[asp]
    not_found = total - found
    print(f"\n▼ {asp}")
    print(f"  Active リンク数: {len(total)}  挿入済: {len(found)}  未挿入: {len(not_found)}")
    print(f"  [挿入済]")
    for name in sorted(found):
        n_articles = len(link_coverage[name])
        print(f"    OK {name} ({n_articles}記事)")
    print(f"  [未挿入]")
    if not_found:
        for name in sorted(not_found):
            print(f"    NG {name}")
    else:
        print("    (なし)")

print()
print(SEP)
print("【2】 記事別 アフィリエイトリンク数")
print(SEP)
article_link_counts.sort(key=lambda x: -x["aff_link_count"])
for art in article_link_counts:
    mark = "  " if art["aff_link_count"] > 0 else "!!"
    print(f"  {mark} [{art['aff_link_count']:2d}件] (ID:{art['id']}) {art['title'][:50]}")

zero_count = sum(1 for a in article_link_counts if a["aff_link_count"] == 0)
print(f"\n  ※ アフィリエイトリンク0件の記事: {zero_count}件 / 全{len(article_link_counts)}件")

print()
print(SEP)
print("【3】 問題点リスト")
print(SEP)
if not problems:
    print("  問題なし（プレースホルダー残り・壊れたリンク・ピクセル欠落は検出されませんでした）")
else:
    for i, p in enumerate(problems, 1):
        print(f"\n  [{i}] {p['type']}")
        print(f"      記事ID: {p['post_id']} / {p['title'][:50]}")
        print(f"      URL: {p['url']}")
        print(f"      詳細: {p['detail']}")

print()
print(SEP)
print("【4】 全 Active リンク カバレッジ一覧")
print(SEP)
covered = [(n, arts) for n, arts in link_coverage.items() if arts]
uncovered = [(n, arts) for n, arts in link_coverage.items() if not arts]
print(f"\n  挿入済み: {len(covered)} / {len(active_links)} リンク")
print(f"  未挿入  : {len(uncovered)} / {len(active_links)} リンク")
print()
print("  [未挿入リンク一覧]")
if uncovered:
    for name, _ in uncovered:
        lnk = next(l for l in active_links if l["name"] == name)
        print(f"    NG {name} (ASP: {lnk['asp']})")
else:
    print("    (全リンク挿入済み)")

print()
print("完了")
