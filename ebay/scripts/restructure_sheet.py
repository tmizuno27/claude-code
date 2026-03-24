#!/usr/bin/env python3
"""
スプレッドシートの列構成を変更:
A: カテゴリ
B: 商品名
C: メルカリ仕入れ目安(JPY)
D: eBay販売価格(USD) ← 数値
E: eBay販売価格(JPY) ← =D*GOOGLEFINANCE為替レート
F: 推定利益(USD) ← 数値
G: 推定利益(JPY) ← =F*GOOGLEFINANCE為替レート
H: 販売日
I: ニッチ度
J: 備考
K: eBay販売実績（定量データ）
+ 塗りつぶしをA〜K全列に拡張
"""

import csv
import os
import re
import time
import gspread
from google.oauth2.service_account import Credentials

CREDENTIALS_PATH = os.path.join(os.path.dirname(__file__), '..', '..', 'tools', 'sheets-sync', 'credentials', 'service-account.json')
SHEET_ID = "1xjdusAVbdyzRwC_JnG93s9J9tC5G11pYtBCrP7Vr_l4"
CSV_PATH = os.path.join(os.path.dirname(__file__), '..', 'ebay-niche-products.csv')

SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive",
]

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

# パステルカラー（カテゴリ別）
CATEGORY_COLORS = {
    "鉋・大工道具": {"red": 1.0, "green": 0.95, "blue": 0.85},
    "鑿（のみ）": {"red": 0.98, "green": 0.93, "blue": 0.82},
    "盆栽鉢": {"red": 0.88, "green": 1.0, "blue": 0.88},
    "南部鉄瓶": {"red": 0.9, "green": 0.9, "blue": 1.0},
    "和包丁": {"red": 1.0, "green": 0.88, "blue": 0.88},
    "帯付きレコード": {"red": 1.0, "green": 0.92, "blue": 1.0},
    "万年筆": {"red": 0.92, "green": 1.0, "blue": 1.0},
    "ポケモンカード": {"red": 1.0, "green": 1.0, "blue": 0.85},
    "トレーディングカード": {"red": 1.0, "green": 0.98, "blue": 0.88},
    "レトロゲーム": {"red": 0.93, "green": 0.93, "blue": 1.0},
    "アニメフィギュア": {"red": 1.0, "green": 0.9, "blue": 0.93},
    "腕時計": {"red": 0.9, "green": 0.95, "blue": 1.0},
    "カメラ・レンズ": {"red": 0.95, "green": 0.95, "blue": 0.95},
    "釣り具": {"red": 0.88, "green": 0.98, "blue": 0.93},
    "伝統工芸品": {"red": 1.0, "green": 0.93, "blue": 0.88},
    "サンリオ・キャラクター": {"red": 1.0, "green": 0.9, "blue": 0.95},
    "ミニ四駆・プラモデル": {"red": 0.93, "green": 0.98, "blue": 0.88},
    "小型家電": {"red": 0.95, "green": 0.93, "blue": 0.98},
    "ブランド品": {"red": 0.98, "green": 0.95, "blue": 0.9},
    "スニーカー": {"red": 0.9, "green": 1.0, "blue": 0.95},
    "JDMパーツ": {"red": 0.93, "green": 0.9, "blue": 0.98},
    "仮面ライダー・戦隊": {"red": 1.0, "green": 0.93, "blue": 0.93},
    "ミニカー": {"red": 0.95, "green": 1.0, "blue": 0.9},
    "日本製文房具": {"red": 0.9, "green": 0.95, "blue": 0.98},
    "電子辞書": {"red": 0.95, "green": 0.98, "blue": 0.95},
}

LAST_COL = "K"  # 最終列


def parse_usd(val):
    """USD文字列を数値に変換。レンジは中間値を返す。"""
    val = val.strip().replace(",", "")
    # $1536 形式
    m = re.match(r'^\$(\d+(?:\.\d+)?)$', val)
    if m:
        return float(m.group(1))
    # $150-400 形式
    m = re.match(r'^\$(\d+(?:\.\d+)?)\s*[-〜~]\s*\$?(\d+(?:\.\d+)?)$', val)
    if m:
        return (float(m.group(1)) + float(m.group(2))) / 2
    # $1400+ 形式
    m = re.match(r'^\$(\d+(?:\.\d+)?)\+?$', val)
    if m:
        return float(m.group(1))
    return None


def parse_profit(val):
    """推定利益を数値に。¥表記や$表記に対応。"""
    val = val.strip().replace(",", "")
    # ¥25428利益 形式（円表記 → ドル換算しない、あとで為替で計算）
    m = re.match(r'[¥￥](\d+)', val)
    if m:
        # 円表記の場合、概算でドルに変換（150円/ドル想定）
        return round(float(m.group(1)) / 150, 1)
    # $1400+ 形式
    m = re.match(r'^\$(\d+(?:\.\d+)?)\+?$', val)
    if m:
        return float(m.group(1))
    # $100-300 形式
    m = re.match(r'^\$(\d+(?:\.\d+)?)\s*[-〜~]\s*\$?(\d+(?:\.\d+)?)$', val)
    if m:
        return (float(m.group(1)) + float(m.group(2))) / 2
    return None


def make_ebay_link(product_name):
    """eBay検索リンクのHYPERLINK数式を生成"""
    query = product_name.replace('"', '').replace("'", "")
    url = f"https://www.ebay.com/sch/i.html?_nkw={query.replace(' ', '+')}&LH_Complete=1&LH_Sold=1"
    return f'=HYPERLINK("{url}","{query}")'


def main():
    creds = Credentials.from_service_account_file(CREDENTIALS_PATH, scopes=SCOPES)
    gc = gspread.authorize(creds)
    sh = gc.open_by_key(SHEET_ID)
    ws = sh.worksheet("商品リスト")

    # CSV読み込み
    with open(CSV_PATH, "r", encoding="utf-8") as f:
        reader = csv.reader(f)
        csv_rows = list(reader)

    print(f"CSV: {len(csv_rows)-1}件の商品データ")

    # シートをクリア
    ws.clear()
    time.sleep(1)

    # ヘッダー行
    headers = [
        "カテゴリ",
        "商品名",
        "メルカリ仕入れ目安(JPY)",
        "eBay販売価格(USD)",
        "eBay販売価格(JPY)※リアルタイム為替",
        "推定利益(USD)",
        "推定利益(JPY)※リアルタイム為替",
        "販売日",
        "ニッチ度",
        "備考",
        "eBay販売実績（定量データ）",
    ]

    # データ行を構築
    all_rows = [headers]
    formulas_e = []  # E列の数式
    formulas_g = []  # G列の数式

    for i, csv_row in enumerate(csv_rows[1:], start=2):
        # CSV列: カテゴリ,商品名,eBay販売価格(USD),メルカリ仕入れ目安(JPY),推定利益(USD),販売日,ニッチ度,備考
        category = csv_row[0] if len(csv_row) > 0 else ""
        product = csv_row[1] if len(csv_row) > 1 else ""
        ebay_usd_raw = csv_row[2] if len(csv_row) > 2 else ""
        mercari_jpy = csv_row[3] if len(csv_row) > 3 else ""
        profit_usd_raw = csv_row[4] if len(csv_row) > 4 else ""
        sale_date = csv_row[5] if len(csv_row) > 5 else ""
        niche = csv_row[6] if len(csv_row) > 6 else ""
        note = csv_row[7] if len(csv_row) > 7 else ""

        # USD価格を数値に
        ebay_usd = parse_usd(ebay_usd_raw)
        profit_usd = parse_profit(profit_usd_raw)

        # 販売実績データ
        sales_info = SALES_DATA.get(category, "")

        row = [
            category,                                   # A: カテゴリ
            product,                                    # B: 商品名（あとでHYPERLINK数式に）
            mercari_jpy,                                # C: メルカリ仕入れ目安(JPY)
            ebay_usd if ebay_usd else ebay_usd_raw,    # D: eBay販売価格(USD) 数値
            "",                                         # E: placeholder（数式で埋める）
            profit_usd if profit_usd else profit_usd_raw, # F: 推定利益(USD) 数値
            "",                                         # G: placeholder（数式で埋める）
            sale_date,                                  # H: 販売日
            niche,                                      # I: ニッチ度
            note,                                       # J: 備考
            sales_info,                                 # K: eBay販売実績
        ]
        all_rows.append(row)

        # E列: =D{i}*GOOGLEFINANCE("CURRENCY:USDJPY")
        formulas_e.append([f'=IF(D{i}="","",D{i}*GOOGLEFINANCE("CURRENCY:USDJPY"))'])
        # G列: =F{i}*GOOGLEFINANCE("CURRENCY:USDJPY")
        formulas_g.append([f'=IF(F{i}="","",F{i}*GOOGLEFINANCE("CURRENCY:USDJPY"))'])

    # 一括書き込み（値データ）
    ws.update(range_name="A1", values=all_rows)
    print("値データ書き込み完了")
    time.sleep(2)

    # B列にHYPERLINK数式を設定
    hyperlinks = []
    for csv_row in csv_rows[1:]:
        product = csv_row[1] if len(csv_row) > 1 else ""
        hyperlinks.append([make_ebay_link(product)])

    ws.update(range_name=f"B2", values=hyperlinks, value_input_option="USER_ENTERED")
    print("HYPERLINK数式を設定完了")
    time.sleep(2)

    # E列に為替連動数式を設定
    ws.update(range_name=f"E2", values=formulas_e, value_input_option="USER_ENTERED")
    print("E列（eBay価格JPY）の為替数式を設定完了")
    time.sleep(2)

    # G列に為替連動数式を設定
    ws.update(range_name=f"G2", values=formulas_g, value_input_option="USER_ENTERED")
    print("G列（推定利益JPY）の為替数式を設定完了")
    time.sleep(2)

    total_rows = len(all_rows)

    # --- フォーマット設定 ---

    # ヘッダー行（A1:K1）を青背景・白太字
    ws.format(f"A1:{LAST_COL}1", {
        "backgroundColor": {"red": 0.2, "green": 0.4, "blue": 0.8},
        "textFormat": {"bold": True, "foregroundColor": {"red": 1, "green": 1, "blue": 1}, "fontSize": 10},
        "horizontalAlignment": "CENTER",
        "wrapStrategy": "WRAP",
    })
    time.sleep(1)

    # D列・F列を通貨フォーマット（USD）
    ws.format(f"D2:D{total_rows}", {"numberFormat": {"type": "CURRENCY", "pattern": "$#,##0.00"}})
    time.sleep(0.5)
    ws.format(f"F2:F{total_rows}", {"numberFormat": {"type": "CURRENCY", "pattern": "$#,##0.00"}})
    time.sleep(0.5)

    # E列・G列を通貨フォーマット（JPY）
    ws.format(f"E2:E{total_rows}", {"numberFormat": {"type": "NUMBER", "pattern": "¥#,##0"}})
    time.sleep(0.5)
    ws.format(f"G2:G{total_rows}", {"numberFormat": {"type": "NUMBER", "pattern": "¥#,##0"}})
    time.sleep(1)

    # カテゴリ別色分け（A〜K全列）
    print("カテゴリ別色分け開始...")
    batch_formats = []
    for i, row in enumerate(all_rows[1:], start=2):
        category = row[0]
        if category in CATEGORY_COLORS:
            batch_formats.append({
                "range": f"A{i}:{LAST_COL}{i}",
                "format": {"backgroundColor": CATEGORY_COLORS[category]},
            })

    # バッチで色分け（10行ずつ）
    for chunk_start in range(0, len(batch_formats), 10):
        chunk = batch_formats[chunk_start:chunk_start + 10]
        ws.batch_format(chunk)
        time.sleep(1)
        print(f"  色分け: {chunk_start + len(chunk)}/{len(batch_formats)}行")

    print("色分け完了")
    time.sleep(1)

    # 列幅調整
    col_widths = [
        (0, 1, 140),   # A: カテゴリ
        (1, 2, 300),   # B: 商品名
        (2, 3, 160),   # C: メルカリ仕入れ
        (3, 4, 140),   # D: eBay USD
        (4, 5, 180),   # E: eBay JPY
        (5, 6, 130),   # F: 推定利益USD
        (6, 7, 170),   # G: 推定利益JPY
        (7, 8, 90),    # H: 販売日
        (8, 9, 90),    # I: ニッチ度
        (9, 10, 200),  # J: 備考
        (10, 11, 450), # K: 販売実績
    ]

    requests = []
    for start, end, width in col_widths:
        requests.append({
            "updateDimensionProperties": {
                "range": {
                    "sheetId": ws.id,
                    "dimension": "COLUMNS",
                    "startIndex": start,
                    "endIndex": end,
                },
                "properties": {"pixelSize": width},
                "fields": "pixelSize",
            }
        })

    # ヘッダー行を固定
    requests.append({
        "updateSheetProperties": {
            "properties": {
                "sheetId": ws.id,
                "gridProperties": {"frozenRowCount": 1},
            },
            "fields": "gridProperties.frozenRowCount",
        }
    })

    sh.batch_update({"requests": requests})
    print("列幅調整・ヘッダー固定完了")

    print(f"\n完了! 全{total_rows-1}件の商品データを{len(headers)}列で構成")
    print(f"URL: {sh.url}")


if __name__ == "__main__":
    main()
