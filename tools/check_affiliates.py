import sys
sys.stdout.reconfigure(encoding='utf-8')
import requests
import re
from base64 import b64encode

# 認証設定
url_base = "https://sim-hikaku.online/wp-json/wp/v2"
username = "t.mizuno27@gmail.com"
app_password = "P4A1 P4eh Nk0z 29An hS6H 9OHq"
credentials = b64encode(f"{username}:{app_password}".encode()).decode()
headers = {
    "Authorization": f"Basic {credentials}",
    "Content-Type": "application/json"
}

# 全記事取得
all_posts = []
page = 1
while True:
    resp = requests.get(f"{url_base}/posts", headers=headers, params={"page": page, "per_page": 100, "status": "any"})
    if resp.status_code != 200:
        print(f"Error: {resp.status_code} - {resp.text[:200]}")
        break
    posts = resp.json()
    if not posts:
        break
    all_posts.extend(posts)
    total_pages = int(resp.headers.get("X-WP-TotalPages", 1))
    print(f"  page {page}/{total_pages} 取得: {len(posts)}件")
    if page >= total_pages:
        break
    page += 1

print(f"取得記事数合計: {len(all_posts)}")
print()

# キーワード定義
affiliates = [
    {
        "name": "ワイモバイル",
        "keywords": ["ワイモバイル", "Y!mobile", "ymobile", "Ymobile"],
        "affiliate_pattern": r'px\.a8\.net[^"\'<\s]*4AZH48.1XNS3M',
    },
    {
        "name": "TRAVeSIM",
        "keywords": ["TRAVeSIM", "トラベシム", "travesim", "TRAVESIM"],
        "affiliate_pattern": r'px\.a8\.net[^"\'<\s]*4AZH48.2M2JWI',
    },
    {
        "name": "Voye Global / ボイエ",
        "keywords": ["Voye", "ボイエ", "voye"],
        "affiliate_pattern": r'px\.a8\.net[^"\'<\s]*4AZH48.2G47UQ',
    },
    {
        "name": "trifa / トリファ",
        "keywords": ["trifa", "トリファ"],
        "affiliate_pattern": r'px\.a8\.net[^"\'<\s]*4AZH4C.CWZK8I',
    },
]

# 各記事を調査
results = []
for post in all_posts:
    post_id = post["id"]
    title = post["title"]["rendered"]
    content = post["content"]["rendered"]
    status = post["status"]

    found = []
    for aff in affiliates:
        # キーワード検索（大文字小文字無視）
        keyword_found = False
        matched_kw = None
        for kw in aff["keywords"]:
            if re.search(kw, content, re.IGNORECASE):
                keyword_found = True
                matched_kw = kw
                break

        if keyword_found:
            # アフィリエイトリンク（特定パターン）があるか
            aff_link_found = bool(re.search(aff["affiliate_pattern"], content, re.IGNORECASE))
            # px.a8.netのリンク全般があるか
            any_a8_link = bool(re.search(r'px\.a8\.net', content))

            found.append({
                "affiliate": aff["name"],
                "matched_keyword": matched_kw,
                "has_affiliate_link": aff_link_found,
                "has_any_a8_link": any_a8_link,
            })

    if found:
        results.append({
            "id": post_id,
            "title": title,
            "status": status,
            "matches": found,
        })

print("=" * 80)
print("【アフィリエイトキーワード検出結果】")
print("=" * 80)

no_link_posts = []
for r in results:
    print(f"\n■ ID:{r['id']} 「{r['title']}」 ({r['status']})")
    for m in r["matches"]:
        if m["has_affiliate_link"]:
            status_str = "OK: A8リンク貼付済み（対象リンク）"
        elif m["has_any_a8_link"]:
            status_str = "注意: 他のA8リンクあり（この案件の対象リンクはなし）"
        else:
            status_str = "NG: リンクなし（テキストのみ or 公式リンク）"
        print(f"   [{m['affiliate']}] キーワード={m['matched_keyword']} / {status_str}")
        if not m["has_affiliate_link"]:
            no_link_posts.append({
                "id": r["id"],
                "title": r["title"],
                "affiliate": m["affiliate"],
                "has_any_a8": m["has_any_a8_link"],
                "status": r["status"]
            })

print("\n" + "=" * 80)
print("【リンク未設置の記事一覧（要対応）】")
print("=" * 80)
for p in no_link_posts:
    link_status = "他A8リンクあり" if p["has_any_a8"] else "素テキストのみ"
    print(f"  ID:{p['id']} ({p['status']}) [{p['affiliate']}] 「{p['title']}」 -> {link_status}")

print(f"\n合計 {len(no_link_posts)} 件のリンク未設置を検出")

# キーワードが1件も見つからなかった案件を報告
found_affiliates = set()
for r in results:
    for m in r["matches"]:
        found_affiliates.add(m["affiliate"])

print("\n" + "=" * 80)
print("【全記事でキーワード未検出の案件】")
print("=" * 80)
for aff in affiliates:
    if aff["name"] not in found_affiliates:
        print(f"  [{aff['name']}] → 全記事でキーワード未検出")
