"""
SIM比較ナビ — 内部リンク一括挿入スクリプト
全記事のFAQ直前に「あわせて読みたい」セクションを挿入する。

使い方:
  python insert_internal_links.py           # dry-run（変更プレビュー）
  python insert_internal_links.py --apply   # 実際にMDファイルを更新
"""

import sys
import os
import re
from pathlib import Path

if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")

BASE_DIR = Path(__file__).resolve().parent.parent.parent
OUTPUTS_DIR = BASE_DIR / "outputs"
SITE_URL = "https://sim-hikaku.online"

# ========== 内部リンクマップ定義 ==========
# key: ファイル名（拡張子なし）
# value: list of (slug, anchor_text) — 挿入する関連記事リンク

# --- 柱1: 用途別 ---
PILLAR1_SLUG = "yoto-betsu-kakuyasu-sim-erabikata"
PILLAR1_CLUSTERS = [
    "sub-kaisen-kakuyasu-sim-osusume",
    "dual-sim-saikyo-kumiawase",
    "kakuyasu-sim-kodomo-shougakusei",
    "kakuyasu-sim-senior-60sai",
    "kakuyasu-sim-hitorigurashi-setsuyaku",
    "kakuyasu-sim-telework",
    "youtube-museigen-sim",
]

# --- 柱2: 乗り換え ---
PILLAR2_SLUG = "kakuyasu-sim-norikae-tejun-pillar"
PILLAR2_CLUSTERS = [
    "docomo-kara-norikae",
    "au-kara-norikae",
    "softbank-kara-norikae",
    "mnp-tenshutu-tejun",
    "norikae-shoshinsha-shippai",
]

# --- 柱3: 料金比較 ---
PILLAR3_SLUG = "kakuyasu-sim-ryokin-hikaku-ichiran"
PILLAR3_CLUSTERS = [
    "kakuyasu-sim-1gb-hikaku",
    "kakuyasu-sim-3gb-saiyas",
    "kakuyasu-sim-10gb-hikaku",
    "kakuyasu-sim-20gb-hikaku",
    "kakuyasu-sim-data-museigen",
    "kakuyasu-sim-esim-taiou",
    "kakuyasu-sim-ipad-tablet",
    "kakuyasu-sim-kazoku-wari",
    "kakuyasu-sim-fuufu-couple",
    "kakuyasu-sim-tsuwaho-kakehoudai",
    "kakuyasu-sim-sokudo-ranking",
    "kakuyasu-sim-campaign-matome",
]

# --- 柱4: レビュー ---
PILLAR4_SLUG = "kakuyasu-sim-review-matome-pillar"
PILLAR4_CLUSTERS = [
    "ahamo-hyoban",
    "iijmio-hyoban",
    "ymobile-hyoban",
    "uq-mobile-hyoban-kuchikomi",
    "rakuten-mobile-hyoban",
    "linemo-hyoban",
    "mineo-hyoban",
    "povo-hyoban",
]

# --- 柱5: 海外SIM ---
PILLAR5_SLUG = "kaigai-sim-esim-hikaku-pillar"
PILLAR5_CLUSTERS = [
    "kaigai-ryokou-esim-osusume",
    "nanbei-sim-esim-guide",
    "kaigai-nihon-bango-iji",
    "ryugakusei-sim-senryaku",
    "airalo-trifa-ubigi-hikaku",
]

# 記事タイトルマップ（リンクテキスト用）
TITLE_MAP = {
    # ピラー記事
    "yoto-betsu-kakuyasu-sim-erabikata": "【用途別】格安SIMの選び方完全ガイド",
    "kakuyasu-sim-norikae-tejun-pillar": "格安SIMへの乗り換え完全ガイド",
    "kakuyasu-sim-ryokin-hikaku-ichiran": "格安SIM20社の料金比較一覧表",
    "kakuyasu-sim-review-matome-pillar": "格安SIM全社レビューまとめ",
    "kaigai-sim-esim-hikaku-pillar": "海外SIM・eSIM完全比較ガイド",
    # 柱1クラスター
    "sub-kaisen-kakuyasu-sim-osusume": "サブ回線におすすめの格安SIM7選",
    "dual-sim-saikyo-kumiawase": "デュアルSIM最強の組み合わせ5選",
    "kakuyasu-sim-kodomo-shougakusei": "子供・小学生におすすめの格安SIM7選",
    "kakuyasu-sim-senior-60sai": "60歳以上・シニアにおすすめの格安SIM",
    "kakuyasu-sim-hitorigurashi-setsuyaku": "一人暮らしの格安SIMで月5,000円節約",
    "kakuyasu-sim-telework": "テレワーク向け格安SIMおすすめ4選",
    "youtube-museigen-sim": "YouTube見放題の格安SIM4選",
    # 柱2クラスター
    "docomo-kara-norikae": "ドコモから格安SIMへの乗り換えガイド",
    "au-kara-norikae": "auから格安SIMへの乗り換えガイド",
    "softbank-kara-norikae": "ソフトバンクから格安SIMへの乗り換えガイド",
    "mnp-tenshutu-tejun": "MNP転出の手順完全ガイド",
    "norikae-shoshinsha-shippai": "格安SIM乗り換えで失敗しがちな10のポイント",
    # 柱3クラスター
    "kakuyasu-sim-1gb-hikaku": "1GB以下の格安SIM最安ランキング",
    "kakuyasu-sim-3gb-saiyas": "3GBの格安SIM最安ランキング",
    "kakuyasu-sim-10gb-hikaku": "10GBの格安SIM最安ランキング",
    "kakuyasu-sim-20gb-hikaku": "20GBの格安SIM最安ランキング",
    "kakuyasu-sim-data-museigen": "データ無制限の格安SIM比較",
    "kakuyasu-sim-esim-taiou": "eSIM対応の格安SIM比較",
    "kakuyasu-sim-ipad-tablet": "iPad・タブレットにおすすめの格安SIM",
    "kakuyasu-sim-kazoku-wari": "家族割がお得な格安SIM比較",
    "kakuyasu-sim-fuufu-couple": "夫婦・カップルにおすすめの格安SIM",
    "kakuyasu-sim-tsuwaho-kakehoudai": "かけ放題の格安SIM比較",
    "kakuyasu-sim-sokudo-ranking": "格安SIM速度ランキング",
    "kakuyasu-sim-campaign-matome": "格安SIMキャンペーンまとめ",
    # 柱4クラスター
    "ahamo-hyoban": "ahamoの評判・口コミ",
    "iijmio-hyoban": "IIJmioの評判・口コミ",
    "ymobile-hyoban": "ワイモバイルの評判・口コミ",
    "uq-mobile-hyoban-kuchikomi": "UQモバイルの評判・口コミ",
    "rakuten-mobile-hyoban": "楽天モバイルの評判・口コミ",
    "linemo-hyoban": "LINEMOの評判・口コミ",
    "mineo-hyoban": "mineoの評判・口コミ",
    "povo-hyoban": "povo2.0の評判・口コミ",
    # 柱5クラスター
    "kaigai-ryokou-esim-osusume": "海外旅行におすすめのeSIM比較7選",
    "nanbei-sim-esim-guide": "南米旅行・移住のSIM・eSIMガイド",
    "kaigai-nihon-bango-iji": "海外在住でも日本の電話番号を維持する方法",
    "ryugakusei-sim-senryaku": "留学生向けSIM・通信戦略ガイド",
    "airalo-trifa-ubigi-hikaku": "Airalo vs trifa vs Ubigi徹底比較",
}

# 横リンク（柱をまたぐ関連記事）
CROSS_LINKS = {
    # 用途別 → 料金比較の関連
    "kakuyasu-sim-kodomo-shougakusei": ["kakuyasu-sim-kazoku-wari"],
    "kakuyasu-sim-senior-60sai": ["kakuyasu-sim-tsuwaho-kakehoudai"],
    "kakuyasu-sim-hitorigurashi-setsuyaku": ["kakuyasu-sim-3gb-saiyas"],
    "kakuyasu-sim-telework": ["kakuyasu-sim-20gb-hikaku", "kakuyasu-sim-data-museigen"],
    "youtube-museigen-sim": ["kakuyasu-sim-data-museigen"],
    "sub-kaisen-kakuyasu-sim-osusume": ["kakuyasu-sim-1gb-hikaku", "dual-sim-saikyo-kumiawase"],
    "dual-sim-saikyo-kumiawase": ["sub-kaisen-kakuyasu-sim-osusume", "kakuyasu-sim-esim-taiou"],
    # 乗り換え → レビュー
    "docomo-kara-norikae": ["ahamo-hyoban", "iijmio-hyoban"],
    "au-kara-norikae": ["uq-mobile-hyoban-kuchikomi", "ymobile-hyoban"],
    "softbank-kara-norikae": ["linemo-hyoban", "ymobile-hyoban"],
    "mnp-tenshutu-tejun": ["norikae-shoshinsha-shippai"],
    "norikae-shoshinsha-shippai": ["mnp-tenshutu-tejun"],
    # 料金比較 → レビュー/用途別
    "kakuyasu-sim-kazoku-wari": ["kakuyasu-sim-kodomo-shougakusei", "ymobile-hyoban"],
    "kakuyasu-sim-esim-taiou": ["kaigai-ryokou-esim-osusume", "kakuyasu-sim-ipad-tablet"],
    "kakuyasu-sim-ipad-tablet": ["kakuyasu-sim-esim-taiou", "kakuyasu-sim-data-museigen"],
    "kakuyasu-sim-data-museigen": ["youtube-museigen-sim", "rakuten-mobile-hyoban"],
    "kakuyasu-sim-tsuwaho-kakehoudai": ["kakuyasu-sim-senior-60sai", "ahamo-hyoban"],
    "kakuyasu-sim-fuufu-couple": ["kakuyasu-sim-kazoku-wari", "dual-sim-saikyo-kumiawase"],
    # レビュー → 料金比較/乗り換え
    "ahamo-hyoban": ["docomo-kara-norikae", "kakuyasu-sim-20gb-hikaku"],
    "iijmio-hyoban": ["kakuyasu-sim-esim-taiou", "kakuyasu-sim-ipad-tablet"],
    "ymobile-hyoban": ["kakuyasu-sim-kazoku-wari", "softbank-kara-norikae"],
    "uq-mobile-hyoban-kuchikomi": ["au-kara-norikae", "kakuyasu-sim-kazoku-wari"],
    "rakuten-mobile-hyoban": ["kakuyasu-sim-data-museigen", "kaigai-nihon-bango-iji"],
    "linemo-hyoban": ["softbank-kara-norikae", "kakuyasu-sim-3gb-saiyas"],
    "mineo-hyoban": ["kakuyasu-sim-data-museigen", "kakuyasu-sim-fuufu-couple"],
    "povo-hyoban": ["sub-kaisen-kakuyasu-sim-osusume", "dual-sim-saikyo-kumiawase"],
    # 海外SIM → 関連
    "kaigai-ryokou-esim-osusume": ["kakuyasu-sim-esim-taiou"],
    "nanbei-sim-esim-guide": ["kaigai-nihon-bango-iji"],
    "kaigai-nihon-bango-iji": ["rakuten-mobile-hyoban", "povo-hyoban"],
    "ryugakusei-sim-senryaku": ["kaigai-ryokou-esim-osusume"],
    "airalo-trifa-ubigi-hikaku": ["kaigai-ryokou-esim-osusume"],
}


def get_pillar_for(slug):
    """記事が属するピラーのslugを返す"""
    if slug in PILLAR1_CLUSTERS or slug == PILLAR1_SLUG:
        return PILLAR1_SLUG
    if slug in PILLAR2_CLUSTERS or slug == PILLAR2_SLUG:
        return PILLAR2_SLUG
    if slug in PILLAR3_CLUSTERS or slug == PILLAR3_SLUG:
        return PILLAR3_SLUG
    if slug in PILLAR4_CLUSTERS or slug == PILLAR4_SLUG:
        return PILLAR4_SLUG
    if slug in PILLAR5_CLUSTERS or slug == PILLAR5_SLUG:
        return PILLAR5_SLUG
    return None


def get_sibling_clusters(slug):
    """同じピラー内の兄弟クラスター（自分を除く、最大3件）"""
    for pillar_slug, clusters in [
        (PILLAR1_SLUG, PILLAR1_CLUSTERS),
        (PILLAR2_SLUG, PILLAR2_CLUSTERS),
        (PILLAR3_SLUG, PILLAR3_CLUSTERS),
        (PILLAR4_SLUG, PILLAR4_CLUSTERS),
        (PILLAR5_SLUG, PILLAR5_CLUSTERS),
    ]:
        if slug in clusters:
            siblings = [c for c in clusters if c != slug]
            return siblings[:3]
    return []


def build_links_for(slug):
    """記事に挿入する関連リンクリストを構築"""
    links = []
    pillar = get_pillar_for(slug)

    # ピラー記事の場合: 全クラスターへのリンク
    if slug in [PILLAR1_SLUG, PILLAR2_SLUG, PILLAR3_SLUG, PILLAR4_SLUG, PILLAR5_SLUG]:
        for p_slug, clusters in [
            (PILLAR1_SLUG, PILLAR1_CLUSTERS),
            (PILLAR2_SLUG, PILLAR2_CLUSTERS),
            (PILLAR3_SLUG, PILLAR3_CLUSTERS),
            (PILLAR4_SLUG, PILLAR4_CLUSTERS),
            (PILLAR5_SLUG, PILLAR5_CLUSTERS),
        ]:
            if slug == p_slug:
                for c in clusters:
                    links.append(c)
                break
        # 他のピラーへのリンク（最大2件）
        other_pillars = [p for p in [PILLAR1_SLUG, PILLAR2_SLUG, PILLAR3_SLUG, PILLAR4_SLUG, PILLAR5_SLUG] if p != slug]
        links.extend(other_pillars[:2])
        return links

    # クラスター記事の場合
    # 1. 親ピラーへのリンク
    if pillar:
        links.append(pillar)

    # 2. 横リンク（異なる柱の関連記事）
    cross = CROSS_LINKS.get(slug, [])
    links.extend(cross)

    # 3. 同柱の兄弟クラスター（横リンクで不足の場合）
    siblings = get_sibling_clusters(slug)
    for s in siblings:
        if s not in links and len(links) < 5:
            links.append(s)

    return links[:6]  # 最大6件


def make_link_html(slug):
    """1件分のリンクHTMLを生成"""
    title = TITLE_MAP.get(slug, slug)
    url = f"{SITE_URL}/{slug}/"
    return f'<a href="{url}">{title}</a>'


def build_related_section(slug):
    """「あわせて読みたい」セクションのMarkdownを生成"""
    links = build_links_for(slug)
    if not links:
        return ""

    lines = [
        "",
        "---",
        "",
        "## あわせて読みたい",
        "",
        '<div style="background: #f8f9fa; border-radius: 12px; padding: 24px; margin: 20px 0;">',
        "",
    ]

    for link_slug in links:
        title = TITLE_MAP.get(link_slug, link_slug)
        url = f"{SITE_URL}/{link_slug}/"
        lines.append(f'<p style="margin: 8px 0; padding: 8px 0; border-bottom: 1px solid #e9ecef;">')
        lines.append(f'  <a href="{url}" style="color: #0066CC; text-decoration: none; font-weight: 500;">{title}</a>')
        lines.append(f'</p>')
        lines.append("")

    lines.append("</div>")
    lines.append("")
    return "\n".join(lines)


def insert_links(slug, content, dry_run=True):
    """記事に関連記事セクションを挿入（FAQ直前）"""
    section = build_related_section(slug)
    if not section:
        return content, False

    # 既に「あわせて読みたい」セクションがある場合は置換
    if "## あわせて読みたい" in content:
        # Remove old section
        pattern = r"\n---\n\n## あわせて読みたい\n.*?</div>\n"
        content = re.sub(pattern, "", content, flags=re.DOTALL)

    # FAQ直前に挿入
    faq_pattern = r"(\n## よくある質問)"
    if re.search(faq_pattern, content):
        content = re.sub(faq_pattern, section + r"\1", content, count=1)
        return content, True

    # FAQがない場合: 末尾に追加
    content = content.rstrip() + "\n" + section
    return content, True


def main():
    args = sys.argv[1:]
    dry_run = "--apply" not in args

    if dry_run:
        print("=== DRY RUN (--apply で実行) ===\n")

    all_slugs = (
        [PILLAR1_SLUG] + PILLAR1_CLUSTERS +
        [PILLAR2_SLUG] + PILLAR2_CLUSTERS +
        [PILLAR3_SLUG] + PILLAR3_CLUSTERS +
        [PILLAR4_SLUG] + PILLAR4_CLUSTERS +
        [PILLAR5_SLUG] + PILLAR5_CLUSTERS
    )

    updated = 0
    skipped = 0

    for slug in all_slugs:
        md_path = OUTPUTS_DIR / f"{slug}.md"
        if not md_path.exists():
            print(f"  [NG] {slug} - MDファイルなし")
            skipped += 1
            continue

        content = md_path.read_text(encoding="utf-8")
        links = build_links_for(slug)

        new_content, changed = insert_links(slug, content, dry_run)
        if changed:
            link_count = len(links)
            print(f"  [OK] {slug} - {link_count}件のリンクを挿入")
            if not dry_run:
                md_path.write_text(new_content, encoding="utf-8")
            updated += 1
        else:
            print(f"  [--] {slug} - 変更なし")
            skipped += 1

    print(f"\n合計: {updated}件更新 / {skipped}件スキップ")
    if dry_run:
        print("\n実行するには: python insert_internal_links.py --apply")


if __name__ == "__main__":
    main()
