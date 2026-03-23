#!/usr/bin/env python3
"""
otona-match.com アフィリエイトCTA挿入スクリプト
カテゴリ・テーマベースで記事末尾にCTAブロックを挿入する
"""

import json
import re
import sys
import requests
from requests.auth import HTTPBasicAuth

# 設定
WP_API = "https://otona-match.com/?rest_route=/wp/v2"
SECRETS_PATH = "C:/Users/tmizu/マイドライブ/GitHub/claude-code/sites/otona-match.com/config/secrets.json"

# dry-runフラグ
DRY_RUN = "--dry-run" in sys.argv

with open(SECRETS_PATH, encoding="utf-8") as f:
    secrets = json.load(f)

AUTH = HTTPBasicAuth(secrets["wordpress"]["username"], secrets["wordpress"]["app_password"])

# カテゴリID
CAT_MATCHING = 2      # matching-apps
CAT_DEAIKEI = 3       # deaikei
CAT_KONKATSU = 4      # konkatsu
CAT_RENAI = 5         # renai-technique
CAT_SAFETY = 6        # safety
CAT_REVIEWS = 7       # reviews

# CTAブロック生成関数
def make_cta(service_name, url, anchor_text, description, tracking_img=None):
    tracking = f'\n<img border="0" width="1" height="1" src="{tracking_img}" alt="">' if tracking_img else ""
    return f"""
<div class="affiliate-cta" style="background:#f8f9fa;border:1px solid #e9ecef;border-radius:8px;padding:20px;margin:30px 0;text-align:center;">
<p style="font-weight:bold;font-size:1.1em;margin-bottom:10px;">＼ {service_name}を無料で試す ／</p>
<p><a href="{url}" rel="nofollow" target="_blank" style="display:inline-block;background:#e74c3c;color:#fff;padding:12px 30px;border-radius:5px;text-decoration:none;font-weight:bold;">{anchor_text}</a>{tracking}</p>
<p style="font-size:0.85em;color:#666;margin-top:8px;">{description}</p>
</div>"""

# アフィリエイトリンク定義（activeのみ）
LINKS = {
    "marrish": make_cta(
        "marrish（マリッシュ）",
        "https://px.a8.net/svt/ejp?a8mat=4AZGCF+DRY4GQ+3N2M+67JUA",
        "marrishで無料登録する",
        "再婚・シンママに人気のマッチングアプリ",
        "https://www10.a8.net/0.gif?a8mat=4AZGCF+DRY4GQ+3N2M+67JUA"
    ),
    "concoi": make_cta(
        "concoi（こんこい）",
        "https://h.accesstrade.net/sp/cc?rk=0100pvup00opif",
        "concoiで無料登録する",
        "AIマッチングのマッチングアプリ",
        "https://h.accesstrade.net/sp/rr?rk=0100pvup00opif"
    ),
    "pcmax": make_cta(
        "PCMAX",
        "https://px.a8.net/svt/ejp?a8mat=4AZGCF+EGCW9M+YQK+631SY",
        "PСMAXで無料登録する",
        "累計1,800万人が利用する出会い系サイト",
        "https://www16.a8.net/0.gif?a8mat=4AZGCF+EGCW9M+YQK+631SY"
    ),
    "wakuwaku": make_cta(
        "ワクワクメール",
        "https://px.a8.net/svt/ejp?a8mat=4AZGCF+F75EHM+1KZ4+601S2",
        "ワクワクメールで無料登録する",
        "会員数1,000万人超の老舗出会い系",
        "https://www14.a8.net/0.gif?a8mat=4AZGCF+F75EHM+1KZ4+601S2"
    ),
    "nacodo": make_cta(
        "naco-do（ナコード）",
        "https://h.accesstrade.net/sp/cc?rk=0100o94500opif",
        "naco-doで無料相談する",
        "オンライン完結の結婚相談所",
        "https://h.accesstrade.net/sp/rr?rk=0100o94500opif"
    ),
    "wellsuma": make_cta(
        "ウェルスマ",
        "//af.moshimo.com/af/c/click?a_id=5432440&p_id=3750&pc_id=9201&pl_id=52304",
        "ウェルスマで無料相談する",
        "月額9,800円からの結婚相談所",
        "//i.moshimo.com/af/i/impression?a_id=5432440&p_id=3750&pc_id=9201&pl_id=52304"
    ),
    "subsuku": make_cta(
        "サブスク婚活（スマリッジ）",
        "//af.moshimo.com/af/c/click?a_id=5432442&p_id=3509&pc_id=8461&pl_id=49639",
        "スマリッジで無料体験する",
        "月額9,900円のオンライン婚活",
        "//i.moshimo.com/af/i/impression?a_id=5432442&p_id=3509&pc_id=8461&pl_id=49639"
    ),
    "partner_agent": make_cta(
        "パートナーエージェント OTOCON",
        "https://h.accesstrade.net/sp/cc?rk=0100dq7e00opif",
        "パートナーエージェントで無料相談する",
        "成婚率No.1の結婚相談所",
        "https://h.accesstrade.net/sp/rr?rk=0100dq7e00opif"
    ),
    "renta": make_cta(
        "Renta!",
        "//ck.jp.ap.valuecommerce.com/servlet/referral?sid=3765527&pid=892567965",
        "Renta!で恋愛漫画を読む",
        "恋愛漫画が豊富な電子書籍サービス",
        "//ad.jp.ap.valuecommerce.com/servlet/gifbanner?sid=3765527&pid=892567965"
    ),
    "hanayume": make_cta(
        "ハナユメ",
        "//ck.jp.ap.valuecommerce.com/servlet/referral?sid=3765527&pid=892567969",
        "ハナユメで式場を探す",
        "結婚式場探しに人気のサービス",
        "//ad.jp.ap.valuecommerce.com/servlet/gifbanner?sid=3765527&pid=892567969"
    ),
}

# カテゴリ別CTAマッピング（最大2個）
CATEGORY_CTA_MAP = {
    CAT_MATCHING: ["marrish", "concoi"],
    CAT_DEAIKEI:  ["pcmax", "wakuwaku"],
    CAT_KONKATSU: ["nacodo", "wellsuma"],
    CAT_RENAI:    ["marrish", "renta"],
    CAT_SAFETY:   ["marrish", "concoi"],
    CAT_REVIEWS:  ["marrish", "concoi"],
}

def count_affiliate_links(content):
    """アフィリエイトリンク数をカウント（CTAブロック数のみ）"""
    # CTAブロック（視覚的ボタン型）の数のみをカウント
    return len(re.findall(r'affiliate-cta', content))

def find_insert_position(content):
    """挿入位置を決定: まとめセクションの直前、なければ末尾"""
    # まとめセクションを探す（h2タグ）
    matome_patterns = [
        r'(<h2[^>]*>(?:まとめ|最後に|おわりに|総まとめ)[^<]*</h2>)',
        r'(<h2[^>]*>[^<]*まとめ[^<]*</h2>)',
    ]
    for pat in matome_patterns:
        m = re.search(pat, content, re.IGNORECASE)
        if m:
            return m.start()
    # なければ末尾（最後の</div>や</p>の後ろ）
    return len(content)

def get_all_posts():
    """全記事を取得"""
    posts = []
    page = 1
    while True:
        resp = requests.get(
            f"{WP_API}/posts",
            params={"per_page": 100, "page": page, "status": "publish,draft"},
            auth=AUTH,
            timeout=30
        )
        if resp.status_code != 200:
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

def update_post_content(post_id, new_content):
    """記事コンテンツを更新"""
    resp = requests.post(
        f"{WP_API}/posts/{post_id}",
        json={"content": new_content},
        auth=AUTH,
        timeout=30
    )
    return resp.status_code == 200

def main():
    print(f"{'[DRY RUN] ' if DRY_RUN else ''}otona-match.com アフィリエイトCTA挿入スクリプト")
    print("=" * 60)

    posts = get_all_posts()
    print(f"取得記事数: {len(posts)}件\n")

    results = []
    skipped = []
    updated = []

    for post in posts:
        post_id = post["id"]
        title = post["title"]["rendered"]
        content = post["content"]["rendered"]
        categories = post.get("categories", [])

        link_count = count_affiliate_links(content)

        # 3個以上あればスキップ
        if link_count >= 3:
            skipped.append(f"ID:{post_id} [{link_count}個] {title[:40]}")
            continue

        # カテゴリに基づいてCTAを決定
        ctas_to_insert = []
        for cat_id, cta_keys in CATEGORY_CTA_MAP.items():
            if cat_id in categories:
                for key in cta_keys:
                    if key not in ctas_to_insert:
                        ctas_to_insert.append(key)
                break  # 最初にマッチしたカテゴリを使用

        # カテゴリが不明な場合はデフォルト
        if not ctas_to_insert:
            ctas_to_insert = ["marrish", "concoi"]

        # 既存リンク数に応じて挿入数を調整
        max_insert = 2 - max(0, link_count)
        if max_insert <= 0:
            max_insert = 1
        ctas_to_insert = ctas_to_insert[:max_insert]

        # 挿入位置を決定
        insert_pos = find_insert_position(content)

        # CTAブロックを生成
        cta_html = "\n".join(LINKS[key] for key in ctas_to_insert)

        # コンテンツに挿入
        new_content = content[:insert_pos] + cta_html + content[insert_pos:]

        cat_names = [str(c) for c in categories]
        result_line = f"ID:{post_id} → {', '.join(ctas_to_insert)} を挿入 | カテゴリ:{cat_names} | 既存リンク:{link_count}個 | 「{title[:35]}」"
        results.append(result_line)

        if not DRY_RUN:
            success = update_post_content(post_id, new_content)
            status = "[OK]" if success else "[NG]"
            updated.append(f"{status} {result_line}")
        else:
            updated.append(f"[DRY] {result_line}")

    print("=== 更新対象記事 ===")
    for line in updated:
        print(line)

    print(f"\n=== スキップ（リンク3個以上） ===")
    for line in skipped:
        print(line)

    print(f"\n=== 集計 ===")
    print(f"更新: {len(updated)}件 / スキップ: {len(skipped)}件 / 合計: {len(posts)}件")

if __name__ == "__main__":
    main()
