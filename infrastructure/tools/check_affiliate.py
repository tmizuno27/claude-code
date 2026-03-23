import sys
sys.stdout.reconfigure(encoding='utf-8')
import requests
import json
import re
from requests.auth import HTTPBasicAuth
from collections import defaultdict

BASE_URL = "https://nambei-oyaji.com/wp-json/wp/v2"
USERNAME = "t.mizuno27@gmail.com"
APP_PASSWORD = "agNg 2624 4lL4 QoT9 EOOZ OEZr"
auth = HTTPBasicAuth(USERNAME, APP_PASSWORD)

affiliate_cases = [
    {"id": 1,  "name": "Wise",          "keywords": ["Wise", "ワイズ"],           "affiliate_url_patterns": ["wise.com/invite"]},
    {"id": 2,  "name": "Revolut",       "keywords": ["Revolut", "レボリュート"],   "affiliate_url_patterns": ["revolut.com/referral"]},
    {"id": 3,  "name": "NordVPN",       "keywords": ["NordVPN", "ノードVPN"],     "affiliate_url_patterns": ["px.a8.net"]},
    {"id": 4,  "name": "ExpressVPN",    "keywords": ["ExpressVPN"],               "affiliate_url_patterns": ["px.a8.net"]},
    {"id": 5,  "name": "Surfshark",     "keywords": ["Surfshark", "サーフシャーク"], "affiliate_url_patterns": ["px.a8.net"]},
    {"id": 6,  "name": "ConoHa WING",   "keywords": ["ConoHa WING", "コノハウィング", "ConoHa"], "affiliate_url_patterns": ["px.a8.net"]},
    {"id": 7,  "name": "Xserver",       "keywords": ["エックスサーバー", "Xserver"], "affiliate_url_patterns": ["px.a8.net"]},
    {"id": 8,  "name": "NativeCamp",    "keywords": ["ネイティブキャンプ", "NativeCamp"], "affiliate_url_patterns": ["px.a8.net"]},
    {"id": 9,  "name": "エポスカード",   "keywords": ["エポスカード", "EPOS", "エポス"], "affiliate_url_patterns": ["px.a8.net"]},
    {"id": 10, "name": "DMM WEBCAMP",   "keywords": ["DMM WEBCAMP", "DMMウェブキャンプ"], "affiliate_url_patterns": ["af.moshimo.com", "dmm-webcamp"]},
    {"id": 11, "name": "クラウドワークス", "keywords": ["クラウドワークス", "CrowdWorks"], "affiliate_url_patterns": ["px.a8.net"]},
    {"id": 12, "name": "ココナラ",       "keywords": ["ココナラ", "coconala"],      "affiliate_url_patterns": ["px.a8.net"]},
    {"id": 13, "name": "trifa",         "keywords": ["trifa", "トリファ"],         "affiliate_url_patterns": ["px.a8.net"]},
    {"id": 14, "name": "TRAVeSIM",      "keywords": ["TRAVeSIM", "トラベシム"],     "affiliate_url_patterns": ["px.a8.net"]},
    {"id": 15, "name": "Voye Global",   "keywords": ["Voye", "ボイエ", "Voye Global"], "affiliate_url_patterns": ["px.a8.net"]},
]

def get_all_posts():
    posts = []
    page = 1
    while True:
        resp = requests.get(
            f"{BASE_URL}/posts",
            params={"per_page": 100, "page": page, "status": "publish,draft,private"},
            auth=auth
        )
        if resp.status_code != 200:
            print(f"Error: {resp.status_code} {resp.text[:200]}")
            break
        data = resp.json()
        if not data:
            break
        posts.extend(data)
        total_pages = int(resp.headers.get("X-WP-TotalPages", 1))
        if page >= total_pages:
            break
        page += 1
    return posts

def find_keyword_contexts(content, keywords, affiliate_url_patterns):
    results = []
    for kw in keywords:
        for m in re.finditer(re.escape(kw), content, re.IGNORECASE):
            start = m.start()
            # Find nearest <a href> before this keyword
            all_a = list(re.finditer(r'<a\s[^>]*href=["\']([^"\']+)["\'][^>]*>', content[:start], re.IGNORECASE))
            all_close = list(re.finditer(r'</a>', content[:start], re.IGNORECASE))
            href = None
            if all_a:
                last_a = all_a[-1]
                last_close = all_close[-1] if all_close else None
                if last_close is None or last_a.start() > last_close.start():
                    href = last_a.group(1)

            is_affiliate = False
            if href:
                is_affiliate = any(pat in href for pat in affiliate_url_patterns)
                link_type = "アフィリエイトリンク済み" if is_affiliate else f"別URLリンク: {href[:80]}"
            else:
                link_type = "素テキスト（リンクなし）"

            results.append({
                "keyword": kw,
                "href": href,
                "link_type": link_type,
                "is_affiliate": is_affiliate
            })
    return results

print("WordPress記事取得中...")
posts = get_all_posts()
print(f"取得記事数: {len(posts)}")
print()

all_results = []
unlinked_items = []

for post in posts:
    post_id = post["id"]
    title = re.sub(r'<[^>]+>', '', post.get("title", {}).get("rendered", "(no title)"))
    content = post.get("content", {}).get("rendered", "")
    status = post.get("status", "unknown")

    post_findings = []

    for case in affiliate_cases:
        # Check if any keyword exists in content
        has_keyword = any(re.search(re.escape(kw), content, re.IGNORECASE) for kw in case["keywords"])
        if not has_keyword:
            continue

        contexts = find_keyword_contexts(content, case["keywords"], case["affiliate_url_patterns"])

        seen_types = set()
        for ctx in contexts:
            key = (case["name"], ctx["link_type"])
            if key in seen_types:
                continue
            seen_types.add(key)

            post_findings.append({
                "case_name": case["name"],
                "keyword": ctx["keyword"],
                "link_type": ctx["link_type"],
                "is_affiliate": ctx["is_affiliate"]
            })

            if not ctx["is_affiliate"]:
                unlinked_items.append({
                    "post_id": post_id,
                    "title": title,
                    "status": status,
                    "case_name": case["name"],
                    "keyword": ctx["keyword"],
                    "link_type": ctx["link_type"]
                })

    if post_findings:
        all_results.append({
            "post_id": post_id,
            "title": title,
            "status": status,
            "findings": post_findings
        })

print("=" * 80)
print("【全記事・全キーワード検出結果】")
print("=" * 80)

for r in sorted(all_results, key=lambda x: x["post_id"]):
    print(f"\n■ ID:{r['post_id']} [{r['status']}] {r['title']}")
    for f in r["findings"]:
        mark = "OK" if f["is_affiliate"] else "NG"
        print(f"  [{mark}] {f['case_name']} ({f['keyword']}) → {f['link_type']}")

print()
print("=" * 80)
print("【要対応リスト：アフィリエイトリンク未設定箇所】")
print("=" * 80)

if unlinked_items:
    by_case = defaultdict(list)
    for item in unlinked_items:
        by_case[item["case_name"]].append(item)

    for case_name in sorted(by_case.keys()):
        items = by_case[case_name]
        print(f"\n▼ {case_name}")
        seen = set()
        for item in items:
            key = (item["post_id"], item["link_type"])
            if key in seen:
                continue
            seen.add(key)
            print(f"  - ID:{item['post_id']} [{item['status']}] {item['title']}")
            print(f"    キーワード: {item['keyword']}")
            print(f"    状態: {item['link_type']}")
else:
    print("全てアフィリエイトリンク設定済みです。")

print()
print("=" * 80)
total_unlinked = len(set((i["post_id"], i["case_name"]) for i in unlinked_items))
print(f"総計: {len(posts)}記事取得 / {len(all_results)}記事でキーワード検出 / 要対応: {total_unlinked}件")
print("=" * 80)
