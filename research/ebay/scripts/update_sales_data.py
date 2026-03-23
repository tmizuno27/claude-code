#!/usr/bin/env python3
"""Column I（eBay販売実績・出品数）を定量的データに更新"""

import os
import time
import gspread
from google.oauth2.service_account import Credentials

CREDENTIALS_PATH = os.path.join(os.path.dirname(__file__), '..', '..', 'tools', 'sheets-sync', 'credentials', 'service-account.json')
SHEET_ID = "1xjdusAVbdyzRwC_JnG93s9J9tC5G11pYtBCrP7Vr_l4"

SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive",
]

# カテゴリ別の定量的販売実績データ
SALES_DATA = {
    "鉋・大工道具": "出品1,200+件 / 主要店舗累計販売61個(SUIZAN) / 日本製工具価格5年で2倍上昇",
    "鑿（のみ）": "出品4,600+件 / カテゴリ常時出品多数 / セラー単位で数十〜数百個販売実績",
    "盆栽鉢": "累計28,200個販売済(総売上$197万) / kaedebonsai-en: 18,000件販売 / kakinoya: 2,500件販売",
    "南部鉄瓶": "出品500+件 / eBay・Etsy両方で活発取引 / 1.2L〜1.4Lモデルが中心価格帯",
    "和包丁": "出品1,874件(中古1,759件/新品228件) / 肥後守: 1商品253個販売 / Charlie Japan: 累計10,000件販売",
    "帯付きレコード": "日本レコード市場$8,550万(2024年) / 年間生産314.9万枚(前年比+17%) / OBI有無で価格最大10倍差",
    "万年筆": "Sailor/Pilotカテゴリ常時出品 / 蒔絵万年筆は$500〜$2,000で取引 / コレクター市場安定",
    "ポケモンカード": "eBay検索14,000回/時間 / 2019→2020年販売+574% / 2021年上半期TCG売上$20億超 / 9四半期連続2桁成長",
    "トレーディングカード": "鑑定済カード前年比+98%成長 / 2021年上半期eBay TCG売上$20億超(前年比+175%) / 9四半期連続2桁成長",
    "レトロゲーム": "SFC出品6,618件 / FC収録1,115タイトル / SFC収録1,529タイトル(PriceCharting) / 3DS: メルカリ¥6,500→eBay$136",
    "アニメフィギュア": "eBayマンガ系100万件+出品 / Solo Leveling検索+520% / 世界市場2031年$185.6億(CAGR9%) / 日本シェア49%($52億)",
    "腕時計": "Seiko専門店: 累計8,900件販売 / Grand Seiko1商品37個販売 / ヴィンテージSeiko12年で価値+1,000% / Seiko売上¥1,759億(+11.7%)",
    "カメラ・レンズ": "出品12,070件(Canon363/Leica428/Nikon291) / 日本セラー151,919件出品 / plusbonbuono: 累計4,800件販売 / 成長率1位カテゴリ",
    "釣り具": "Shimanoスピニング5,142件出品 / ヴィンテージスピニング3,017件 / キャスティング1,649件 / DAIWA6,220件出品",
    "伝統工芸品": "江戸切子$100〜$600で取引 / 有田焼$200〜$1,700 / 九谷焼$50〜$200 / 日本工芸品カテゴリ安定需要",
    "サンリオ・キャラクター": "ハローキティ玩具5,181件出品(アクティブ) / 日本限定品はプレミアム価格 / 福袋・万博限定品が高値",
    "ミニ四駆・プラモデル": "特定モーター商品62個販売実績 / プレバン限定ガンプラ高需要 / タミヤミニ四駆専用カテゴリあり",
    "小型家電": "ソニーウォークマンWM-2: $100〜$250 / ナノケアドライヤー: メルカリ¥19,950→eBay$212 / レトロ家電需要増加中",
    "ブランド品": "Chanel平均$1,500 / Cartier平均$2,150 / Van Cleef平均$3,300 / 日本eBay売上2020→2024年で2倍",
    "スニーカー": "オニツカタイガー: eBayメンズアパレル1位 / Atmos別注・都市限定が高プレミアム / Japan Made限定モデル人気",
    "JDMパーツ": "DMV JDM Depot: 累計14,000件販売 / JDM-CAR-PARTS: 7,200件販売 / JDM CAR JAPAN: 5,300件販売 / 合計26,500件+",
    "仮面ライダー・戦隊": "全カテゴリ34,965件出品 / アクションフィギュア9,155件 / S.H.フィギュアーツ4,115件 / 2025年新作926件",
    "ミニカー": "トミカLV Neo$20〜$100 / ホットウィール日本コンベンション限定$30〜$200 / コレクター市場安定",
    "日本製文房具": "Pilot キャップレス$80〜$200 / 廃番シャーペン$20〜$100 / JetPens・Amazon経由の国際販売が主流",
    "電子辞書": "出品673件(Casio388件/Sharp160件) / 中古品$162〜 / 日本語学習ブームで需要増加中",
}

def main():
    creds = Credentials.from_service_account_file(CREDENTIALS_PATH, scopes=SCOPES)
    gc = gspread.authorize(creds)
    sh = gc.open_by_key(SHEET_ID)
    ws = sh.worksheet("商品リスト")

    # 全データ取得
    all_data = ws.get_all_values()
    print(f"全{len(all_data)}行を取得")

    # I列（9列目）のデータを構築
    updates = []
    for i, row in enumerate(all_data):
        if i == 0:
            updates.append(["eBay販売実績（定量データ）"])
            continue
        category = row[0] if row else ""
        sales_info = SALES_DATA.get(category, "")
        updates.append([sales_info])

    # I列を一括更新
    ws.update(range_name="I1", values=updates)
    print(f"I列を{len(updates)}行更新しました")

    # ヘッダーフォーマット
    time.sleep(1)
    ws.format("I1", {
        "backgroundColor": {"red": 0.2, "green": 0.4, "blue": 0.8},
        "textFormat": {"bold": True, "foregroundColor": {"red": 1, "green": 1, "blue": 1}},
        "horizontalAlignment": "CENTER",
    })

    # I列の幅を広げる
    time.sleep(1)
    body = {
        "requests": [{
            "updateDimensionProperties": {
                "range": {
                    "sheetId": ws.id,
                    "dimension": "COLUMNS",
                    "startIndex": 8,
                    "endIndex": 9,
                },
                "properties": {"pixelSize": 450},
                "fields": "pixelSize",
            }
        }]
    }
    sh.batch_update(body)

    print("完了!")
    print(f"URL: {sh.url}")

if __name__ == "__main__":
    main()
