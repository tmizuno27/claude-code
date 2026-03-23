#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
もしもアフィリエイト・Value Commerce CTAブロック一括挿入スクリプト
nambei-oyaji.com 全25記事対象
"""

import requests
import base64
import json
import re
import sys
import time
from pathlib import Path

# ===== 設定 =====
CONFIG_DIR = Path(__file__).parent.parent.parent / "config"
SECRETS_PATH = CONFIG_DIR / "secrets.json"
AFFILIATE_PATH = CONFIG_DIR / "affiliate-links.json"
API_URL = "https://nambei-oyaji.com/wp-json/wp/v2"

DRY_RUN = "--live" not in sys.argv  # デフォルトはdry-run

# ===== 記事テーマ → CTAマッピング =====
# (headline, url, anchor, description, tracking_img, asp)
LINK_DEFS = {
    "global_wifi_moshimo": {
        "headline": "📶 パラグアイ渡航・旅行のWiFiはグローバルWiFiが便利",
        "url": "//af.moshimo.com/af/c/click?a_id=5432419&p_id=2627&pc_id=5877&pl_id=33477",
        "anchor": "グローバルWiFiで海外WiFiをレンタルする",
        "desc": "パラグアイ含む200カ国以上に対応。出発前日まで申込OK",
        "tracking_img": '<img loading="lazy" src="//i.moshimo.com/af/i/impression?a_id=5432419&p_id=2627&pc_id=5877&pl_id=33477" width="1" height="1" style="border:none;" />',
        "asp": "もしも",
    },
    "his_tour_vc": {
        "headline": "✈️ 南米・パラグアイへのツアーはHISで検索",
        "url": "//ck.jp.ap.valuecommerce.com/servlet/referral?sid=3765528&pid=892567778",
        "anchor": "HISで南米・パラグアイのツアーを探す",
        "desc": "海外ツアー・航空券の比較予約ならHIS。南米方面も充実",
        "tracking_img": '<img loading="lazy" src="//ad.jp.ap.valuecommerce.com/servlet/gifbanner?sid=3765528&pid=892567778" width="1" height="1" style="border:none;" />',
        "asp": "VC",
    },
    "his_air_vc": {
        "headline": "✈️ パラグアイ行き航空券はHISで比較",
        "url": "//ck.jp.ap.valuecommerce.com/servlet/referral?sid=3765528&pid=892567779",
        "anchor": "HIS航空券でパラグアイへの航空券を探す",
        "desc": "格安航空券の比較・予約。早期割引を活用してお得に渡航",
        "tracking_img": '<img loading="lazy" src="//ad.jp.ap.valuecommerce.com/servlet/gifbanner?sid=3765528&pid=892567779" width="1" height="1" style="border:none;" />',
        "asp": "VC",
    },
    "expedia_vc": {
        "headline": "🏨 海外ホテル・フライト予約はエクスペディア",
        "url": "//ck.jp.ap.valuecommerce.com/servlet/referral?sid=3765528&pid=892567809",
        "anchor": "エクスペディアで海外ホテル・航空券を予約する",
        "desc": "世界最大級の旅行予約サイト。南米のホテルも豊富に掲載",
        "tracking_img": '<img loading="lazy" src="//ad.jp.ap.valuecommerce.com/servlet/gifbanner?sid=3765528&pid=892567809" width="1" height="1" style="border:none;" />',
        "asp": "VC",
    },
    "jalpack_vc": {
        "headline": "✈️ JALパックで南米・パラグアイへ",
        "url": "//ck.jp.ap.valuecommerce.com/servlet/referral?sid=3765528&pid=892567785",
        "anchor": "JALパックで海外ツアーを探す",
        "desc": "JALの安心感と現地サポートで南米旅行をもっと快適に",
        "tracking_img": '<img loading="lazy" src="//ad.jp.ap.valuecommerce.com/servlet/gifbanner?sid=3765528&pid=892567785" width="1" height="1" style="border:none;" />',
        "asp": "VC",
    },
    "jalan_vc": {
        "headline": "🏨 一時帰国の宿泊はじゃらんで予約",
        "url": "//ck.jp.ap.valuecommerce.com/servlet/referral?sid=3765528&pid=892567783",
        "anchor": "じゃらんnetで一時帰国の宿を探す",
        "desc": "国内最大級の宿泊予約サイト。ポイントも貯まってお得",
        "tracking_img": '<img loading="lazy" src="//ad.jp.ap.valuecommerce.com/servlet/gifbanner?sid=3765528&pid=892567783" width="1" height="1" style="border:none;" />',
        "asp": "VC",
    },
    "jtb_vc": {
        "headline": "🏨 一時帰国の旅行・宿泊はJTBで",
        "url": "//ck.jp.ap.valuecommerce.com/servlet/referral?sid=3765528&pid=892567790",
        "anchor": "JTBで国内旅行・宿泊を予約する",
        "desc": "大手旅行会社JTBの安心サービス。一時帰国の旅行をサポート",
        "tracking_img": '<img loading="lazy" src="//ad.jp.ap.valuecommerce.com/servlet/gifbanner?sid=3765528&pid=892567790" width="1" height="1" style="border:none;" />',
        "asp": "VC",
    },
    "yahoo_travel_vc": {
        "headline": "🏨 一時帰国の宿泊はYahoo!トラベルで比較",
        "url": "//ck.jp.ap.valuecommerce.com/servlet/referral?sid=3765528&pid=892567791",
        "anchor": "Yahoo!トラベルで宿泊先を探す",
        "desc": "Tポイントが使える・貯まる宿泊予約サイト",
        "tracking_img": '<img loading="lazy" src="//ad.jp.ap.valuecommerce.com/servlet/gifbanner?sid=3765528&pid=892567791" width="1" height="1" style="border:none;" />',
        "asp": "VC",
    },
    "nihon_ryoko_vc": {
        "headline": "🚅 一時帰国の国内移動は日本旅行で",
        "url": "//ck.jp.ap.valuecommerce.com/servlet/referral?sid=3765528&pid=892567792",
        "anchor": "日本旅行で新幹線+宿泊セットを予約する",
        "desc": "JR+宿泊セットプランでお得に国内移動。新幹線の割引も",
        "tracking_img": '<img loading="lazy" src="//ad.jp.ap.valuecommerce.com/servlet/gifbanner?sid=3765528&pid=892567792" width="1" height="1" style="border:none;" />',
        "asp": "VC",
    },
    "beyond_border_moshimo": {
        "headline": "🌍 海外経験を活かして転職したいなら The Beyond Border",
        "url": "//af.moshimo.com/af/c/click?a_id=5432430&p_id=1678&pc_id=3136&pl_id=24078",
        "anchor": "The Beyond Borderで海外経験者向け求人を見る",
        "desc": "海外経験者・留学経験者専門の転職エージェント。パラグアイ在住でも相談可能",
        "tracking_img": '<img loading="lazy" src="//i.moshimo.com/af/i/impression?a_id=5432430&p_id=1678&pc_id=3136&pl_id=24078" width="1" height="1" style="border:none;" />',
        "asp": "もしも",
    },
    "lolipop_moshimo": {
        "headline": "💻 海外ブログを月220円〜始めるならロリポップ",
        "url": "//af.moshimo.com/af/c/click?a_id=5432415&p_id=16&pc_id=16&pl_id=14954",
        "anchor": "ロリポップ!レンタルサーバーを確認する",
        "desc": "月額220円〜の格安レンタルサーバー。海外からでも申し込みOK",
        "tracking_img": '<img loading="lazy" src="//i.moshimo.com/af/i/impression?a_id=5432415&p_id=16&pc_id=16&pl_id=14954" width="1" height="1" style="border:none;" />',
        "asp": "もしも",
    },
    "conoha_moshimo": {
        "headline": "💻 海外生活ブログを始めるならConoHa WING",
        "url": "//af.moshimo.com/af/c/click?a_id=5432414&p_id=2312&pc_id=4967&pl_id=30490",
        "anchor": "ConoHa WINGでWordPressブログを始める",
        "desc": "高速・安定のレンタルサーバー。WordPressの自動インストールで簡単開設",
        "tracking_img": '<img loading="lazy" src="//i.moshimo.com/af/i/impression?a_id=5432414&p_id=2312&pc_id=4967&pl_id=30490" width="1" height="1" style="border:none;" />',
        "asp": "もしも",
    },
    "visionwimax_moshimo": {
        "headline": "📶 一時帰国中のWiFiはVisionWiMAXが便利",
        "url": "//af.moshimo.com/af/c/click?a_id=5432420&p_id=3359&pc_id=7984&pl_id=47733",
        "anchor": "VisionWiMAXで一時帰国のWiFiを契約する",
        "desc": "月額3,000円台〜。一時帰国中の自宅・外出でもWiFi使い放題",
        "tracking_img": '<img loading="lazy" src="//i.moshimo.com/af/i/impression?a_id=5432420&p_id=3359&pc_id=7984&pl_id=47733" width="1" height="1" style="border:none;" />',
        "asp": "もしも",
    },
    "dinomo_moshimo": {
        "headline": "📶 海外旅行・移住のWiFiはdinomoWiFi",
        "url": "//af.moshimo.com/af/c/click?a_id=5432421&p_id=5538&pc_id=15178&pl_id=71447",
        "anchor": "dinomoWiFiで海外WiFiをレンタルする",
        "desc": "eSIM・SIM・WiFiルーターで海外の通信環境をカバー",
        "tracking_img": '<img loading="lazy" src="//i.moshimo.com/af/i/impression?a_id=5432421&p_id=5538&pc_id=15178&pl_id=71447" width="1" height="1" style="border:none;" />',
        "asp": "もしも",
    },
    "furunabi_vc": {
        "headline": "🏯 海外在住でもできるふるさと納税はふるなびで",
        "url": "//ck.jp.ap.valuecommerce.com/servlet/referral?sid=3765528&pid=892567810",
        "anchor": "ふるなびでふるさと納税をする",
        "desc": "海外在住者も住民税を払っていればふるさと納税が可能。一時帰国前に活用しよう",
        "tracking_img": '<img loading="lazy" src="//ad.jp.ap.valuecommerce.com/servlet/gifbanner?sid=3765528&pid=892567810" width="1" height="1" style="border:none;" />',
        "asp": "VC",
    },
}

# ===== 記事ID → 挿入するリンクキーのリスト（最大2個）=====
# 記事タイトルから分類（APIで確認したIDベース）
ARTICLE_MAPPING = {
    # パラグアイ移住・渡航系
    1735: ["his_tour_vc", "global_wifi_moshimo"],           # パラグアイ移住のメリット・デメリット
    2076: ["his_tour_vc", "global_wifi_moshimo"],           # 海外移住の持ち物完全ガイド
    2078: ["his_tour_vc", "expedia_vc"],                    # パラグアイ移住で失敗しない注意点
    2096: ["his_tour_vc", "expedia_vc"],                    # パラグアイの生活費
    2097: ["his_tour_vc", "global_wifi_moshimo"],           # パラグアイのビザの種類と取得方法
    2099: ["his_tour_vc", "global_wifi_moshimo"],           # パラグアイの言語事情
    2100: ["expedia_vc", "his_tour_vc"],                    # パラグアイの学校・インターナショナルスクール
    2098: ["dinomo_moshimo", "global_wifi_moshimo"],        # パラグアイのインターネット・通信環境
    1214: ["his_tour_vc", "expedia_vc"],                    # パラグアイの食べ物
    1008: ["his_tour_vc", "global_wifi_moshimo"],           # パラグアイの気候・天気
    1065: ["his_tour_vc", "expedia_vc"],                    # パラグアイ移住の費用・家探しの全手順
    1066: ["his_tour_vc", "expedia_vc"],                    # パラグアイの生活費月10万〜
    1067: ["his_tour_vc", "global_wifi_moshimo"],           # パラグアイの食文化
    1068: ["expedia_vc", "his_tour_vc"],                    # 子連れでパラグアイ・インターナショナルスクール
    1069: ["beyond_border_moshimo", "his_tour_vc"],         # 海外在住の副業5選
    1070: ["his_tour_vc", "expedia_vc"],                    # 海外送金サービス比較
    # 副業・ブログ・仕事系
    2058: ["conoha_moshimo", "beyond_border_moshimo"],      # AIで稼ぐためのサイト7選
    2057: ["conoha_moshimo", "beyond_border_moshimo"],      # AI副業ツール7選
    2056: ["conoha_moshimo", "lolipop_moshimo"],            # 海外在住のAIアプリで副業
    2055: ["beyond_border_moshimo", "conoha_moshimo"],      # データ分析の副業のはじめ方
    2016: ["beyond_border_moshimo", "conoha_moshimo"],      # オンラインスペイン語学習サービス比較
    2015: ["conoha_moshimo", "lolipop_moshimo"],            # 海外生活ブログの始め方
    2014: ["conoha_moshimo", "lolipop_moshimo"],            # 海外移住前に受けるべきオンラインスクール
    2013: ["his_tour_vc", "expedia_vc"],                    # 海外移住者向けクレジットカード比較
    2012: ["visionwimax_moshimo", "dinomo_moshimo"],        # 海外で必須のVPN
}

# 一時帰国関連記事をVC旅行系でカバー（追加マッピング）
ICHIJI_ARTICLE_IDS = []  # 現状一時帰国特化記事なし


def make_cta_html(link_key: str) -> str:
    d = LINK_DEFS[link_key]
    return f"""<div class="affiliate-cta" style="background:#f0f7ff;border:1px solid #d0e3f7;border-radius:8px;padding:20px;margin:30px 0;text-align:center;">
<p style="font-weight:bold;font-size:1.1em;margin-bottom:10px;">{d['headline']}</p>
<p><a href="{d['url']}" rel="nofollow" target="_blank" style="display:inline-block;background:#2980b9;color:#fff;padding:12px 30px;border-radius:5px;text-decoration:none;font-weight:bold;">{d['anchor']}</a></p>
<p style="font-size:0.85em;color:#666;margin-top:8px;">{d['desc']}</p>
</div>
{d['tracking_img']}"""


def get_auth_headers():
    secrets = json.loads(SECRETS_PATH.read_text(encoding="utf-8"))
    username = secrets["wordpress"]["username"]
    app_password = secrets["wordpress"]["app_password"]
    creds = base64.b64encode(f"{username}:{app_password}".encode()).decode()
    return {"Authorization": f"Basic {creds}"}


def get_post(post_id: int, headers: dict) -> dict:
    r = requests.get(f"{API_URL}/posts/{post_id}", headers=headers)
    r.raise_for_status()
    return r.json()


def insert_ctas(content: str, cta_blocks: list[str]) -> tuple[str, bool]:
    """CTAブロックを挿入。まとめセクション直前または末尾に追加。変更有無も返す"""
    existing_cta_count = content.count("affiliate-cta")
    if existing_cta_count >= 3:
        return content, False

    combined = "\n".join(cta_blocks)

    # まとめ系見出しを探す
    summary_patterns = [
        r'(<h[23][^>]*>(?:まとめ|総まとめ|おわりに|最後に|まとめ：)[^<]*</h[23]>)',
        r'(<h[23][^>]*>[^<]*まとめ[^<]*</h[23]>)',
    ]
    for pat in summary_patterns:
        m = re.search(pat, content, re.IGNORECASE)
        if m:
            insert_pos = m.start()
            new_content = content[:insert_pos] + combined + "\n" + content[insert_pos:]
            return new_content, True

    # まとめがなければ末尾に追加
    new_content = content.rstrip() + "\n" + combined
    return new_content, True


def update_post(post_id: int, new_content: str, headers: dict):
    r = requests.post(
        f"{API_URL}/posts/{post_id}",
        headers={**headers, "Content-Type": "application/json"},
        json={"content": new_content},
    )
    r.raise_for_status()
    return r.json()


def main():
    headers = get_auth_headers()
    mode_label = "DRY-RUN" if DRY_RUN else "LIVE"
    print(f"\n{'='*60}")
    print(f"  もしも/VC CTAブロック挿入スクリプト [{mode_label}]")
    print(f"{'='*60}\n")

    updated = 0
    skipped = 0
    errors = 0

    for post_id, link_keys in ARTICLE_MAPPING.items():
        try:
            post = get_post(post_id, headers)
            title = post["title"]["rendered"]
            content = post["content"]["rendered"]
            existing_cta = content.count("affiliate-cta")

            print(f"[ID:{post_id}] {title[:55]}")
            print(f"  現在のCTA数: {existing_cta}")

            if existing_cta >= 3:
                print(f"  → スキップ (CTA既に{existing_cta}個)\n")
                skipped += 1
                continue

            # 追加するCTAを既存数を考慮して絞る
            slots = max(0, 2 - existing_cta)
            keys_to_add = link_keys[:slots]
            if not keys_to_add:
                print(f"  → スキップ (追加スロットなし)\n")
                skipped += 1
                continue

            cta_blocks = [make_cta_html(k) for k in keys_to_add]
            new_content, changed = insert_ctas(content, cta_blocks)

            if not changed:
                print(f"  → 変更なし\n")
                skipped += 1
                continue

            added_links = [LINK_DEFS[k]["anchor"] for k in keys_to_add]
            print(f"  追加予定CTA: {', '.join(added_links)}")

            if DRY_RUN:
                print(f"  -> [DRY-RUN] 更新しません\n")
            else:
                update_post(post_id, new_content, headers)
                print(f"  -> 更新完了\n")
                time.sleep(1)

            updated += 1

        except Exception as e:
            print(f"  -> ERROR: {e}\n")
            errors += 1

    print(f"{'='*60}")
    print(f"  結果: 更新対象={updated} / スキップ={skipped} / エラー={errors}")
    if DRY_RUN:
        print(f"  ※ dry-runです。本番実行は --live オプションを付けてください")
    print(f"{'='*60}\n")


if __name__ == "__main__":
    main()
