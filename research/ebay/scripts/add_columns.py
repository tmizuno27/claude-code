#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
スプレッドシートに6列追加:
L: eBay手数料(USD) = E * 0.1325
M: 送料目安(JPY) ← カテゴリ別データ
N: 実質利益(USD) = E - (C/為替) - L - (M/為替)
O: 実質利益(JPY) = N * 為替
P: ROI(%) = N / (C/為替) * 100
Q: 回転率 ← カテゴリ別データ
R: メルカリ検索キーワード ← カテゴリ別データ

+ 説明書シートを新規作成
"""

import sys, io, os, time
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
import gspread
from google.oauth2.service_account import Credentials

CREDS = os.path.join(os.path.dirname(__file__), '..', '..', 'tools', 'sheets-sync', 'credentials', 'service-account.json')
SHEET_ID = "1xjdusAVbdyzRwC_JnG93s9J9tC5G11pYtBCrP7Vr_l4"

SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive",
]

LAST_COL = "R"

# カテゴリ別: 送料目安(JPY), 回転率, メルカリ検索キーワード
CATEGORY_DATA = {
    "鉋・大工道具": (1800, "標準（1〜2ヶ月）", "鉋 かんな ジャンク / 大工道具 まとめ / 鉋 名工"),
    "鑿（のみ）": (2000, "標準（1〜2ヶ月）", "鑿 のみ セット / 鑿 まとめ売り / 追入鑿"),
    "盆栽鉢": (2500, "標準（1〜2ヶ月）", "盆栽鉢 常滑 / 盆栽鉢 作家 / 盆栽鉢 まとめ"),
    "南部鉄瓶": (3000, "長期（2〜3ヶ月）", "南部鉄瓶 ジャンク / 鉄瓶 龍文堂 / 鉄瓶 まとめ"),
    "和包丁": (1500, "即売れ（1〜2週間）", "包丁 堺 中古 / 出刃包丁 / 和包丁 まとめ"),
    "帯付きレコード": (800, "即売れ（1〜2週間）", "レコード 帯付き / LP 帯付 まとめ / レコード OBI"),
    "万年筆": (1000, "標準（1〜2ヶ月）", "万年筆 漆 / 万年筆 セーラー 限定 / 万年筆 パイロット"),
    "ポケモンカード": (500, "即売れ（数日）", "ポケモンカード 旧裏 / ポケカ 初版 / ポケカ まとめ"),
    "トレーディングカード": (500, "即売れ（1週間）", "遊戯王 大会 / ワンピカード / トレカ まとめ"),
    "レトロゲーム": (1200, "即売れ（1〜2週間）", "ファミコン ソフト まとめ / スーファミ 箱付き / ゲームボーイ"),
    "アニメフィギュア": (2000, "即売れ（1〜2週間）", "フィギュア 限定 / 一番くじ / ねんどろいど"),
    "腕時計": (1500, "標準（1〜2ヶ月）", "セイコー ヴィンテージ / SEIKO 5 / G-SHOCK 限定"),
    "カメラ・レンズ": (2000, "即売れ（1〜2週間）", "フィルムカメラ ジャンク / オールドレンズ / Nikon F"),
    "釣り具": (2500, "標準（1〜2ヶ月）", "シマノ リール ヴィンテージ / ダイワ リール / ルアー まとめ"),
    "伝統工芸品": (2500, "長期（2〜3ヶ月）", "江戸切子 / 九谷焼 / 有田焼 金彩"),
    "サンリオ・キャラクター": (1200, "標準（1〜2ヶ月）", "サンリオ 限定 / キティ 日本限定 / サンリオ 福袋"),
    "ミニ四駆・プラモデル": (1200, "標準（1〜2ヶ月）", "ミニ四駆 限定 / ガンプラ プレバン / タミヤ 限定"),
    "小型家電": (2500, "標準（1〜2ヶ月）", "ウォークマン ヴィンテージ / ナノケア / レトロ家電"),
    "ブランド品": (2000, "即売れ（1〜2週間）", "ヴィトン 中古 / シャネル バッグ / ブランド まとめ"),
    "スニーカー": (2000, "即売れ（1〜2週間）", "オニツカタイガー 日本製 / スニーカー 限定 / atmos"),
    "JDMパーツ": (4000, "標準（1〜2ヶ月）", "スカイライン 純正 / JDM パーツ / GT-R 部品"),
    "仮面ライダー・戦隊": (2000, "標準（1〜2ヶ月）", "仮面ライダー ベルト DX / 戦隊ロボ / ウルトラマン"),
    "ミニカー": (800, "標準（1〜2ヶ月）", "トミカ リミテッド / ホットウィール 日本 / ミニカー まとめ"),
    "日本製文房具": (800, "長期（2〜3ヶ月）", "万年筆 キャップレス / シャーペン 廃番 / 文房具 レア"),
    "電子辞書": (1500, "標準（1〜2ヶ月）", "電子辞書 カシオ / Ex-word / 電子辞書 日本語"),
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


def main():
    creds = Credentials.from_service_account_file(CREDS, scopes=SCOPES)
    gc = gspread.authorize(creds)
    sh = gc.open_by_key(SHEET_ID)
    ws = sh.worksheet("商品リスト")

    rows = ws.get_all_values()
    total = len(rows)
    print(f"{total}行取得")

    # シートの列数を拡張（11列→20列）
    ws.resize(rows=total, cols=20)
    print("列数を20に拡張")
    time.sleep(1)

    # === 新列のヘッダー (L〜R) ===
    new_headers = [
        ["eBay手数料(USD)", "送料目安(JPY)", "実質利益(USD)", "実質利益(JPY)", "ROI(%)", "回転率", "メルカリ検索キーワード"]
    ]
    ws.update(range_name="L1", values=new_headers)
    print("ヘッダー追加完了")
    time.sleep(1)

    # === 送料・回転率・メルカリKWのデータ (M, Q, R列) ===
    m_vals = []  # 送料
    q_vals = []  # 回転率
    r_vals = []  # メルカリKW

    for row in rows[1:]:
        cat = row[0]
        data = CATEGORY_DATA.get(cat, (2000, "不明", ""))
        m_vals.append([data[0]])
        q_vals.append([data[1]])
        r_vals.append([data[2]])

    ws.update(range_name="M2", values=m_vals, value_input_option="USER_ENTERED")
    print("M列(送料)書き込み完了")
    time.sleep(1)

    ws.update(range_name="Q2", values=q_vals)
    print("Q列(回転率)書き込み完了")
    time.sleep(1)

    ws.update(range_name="R2", values=r_vals)
    print("R列(メルカリKW)書き込み完了")
    time.sleep(1)

    # === 数式列 (L, N, O, P) ===
    # 為替レートの参照用（全数式で同じ関数を呼ぶと遅いので1セルに集約）
    # S1に為替レートを置く（非表示列として）
    ws.update(range_name="S1", values=[["為替レート"]], value_input_option="USER_ENTERED")
    ws.update(range_name="S2", values=[['=GOOGLEFINANCE("CURRENCY:USDJPY")']], value_input_option="USER_ENTERED")
    print("為替レート参照セル(S2)設定完了")
    time.sleep(2)

    formulas_l = []  # eBay手数料
    formulas_n = []  # 実質利益USD
    formulas_o = []  # 実質利益JPY
    formulas_p = []  # ROI

    for i in range(2, total + 1):
        # L: eBay手数料 = E * 0.1325
        formulas_l.append([f'=IF(E{i}="","",E{i}*0.1325)'])
        # N: 実質利益USD = E(売値USD) - C(仕入JPY)/為替 - L(手数料USD) - M(送料JPY)/為替
        formulas_n.append([f'=IF(E{i}="","",E{i}-(C{i}/$S$2)-L{i}-(M{i}/$S$2))'])
        # O: 実質利益JPY = N * 為替
        formulas_o.append([f'=IF(N{i}="","",N{i}*$S$2)'])
        # P: ROI = 実質利益USD / 仕入れUSD * 100
        formulas_p.append([f'=IF(OR(N{i}="",C{i}=0),"",N{i}/(C{i}/$S$2)*100)'])

    ws.update(range_name="L2", values=formulas_l, value_input_option="USER_ENTERED")
    print("L列(eBay手数料)数式設定完了")
    time.sleep(1)

    ws.update(range_name="N2", values=formulas_n, value_input_option="USER_ENTERED")
    print("N列(実質利益USD)数式設定完了")
    time.sleep(1)

    ws.update(range_name="O2", values=formulas_o, value_input_option="USER_ENTERED")
    print("O列(実質利益JPY)数式設定完了")
    time.sleep(1)

    ws.update(range_name="P2", values=formulas_p, value_input_option="USER_ENTERED")
    print("P列(ROI)数式設定完了")
    time.sleep(1)

    # === 表示形式 ===
    ws.format(f"L2:L{total}", {"numberFormat": {"type": "NUMBER", "pattern": "$#,##0"}})
    time.sleep(0.5)
    ws.format(f"M2:M{total}", {"numberFormat": {"type": "NUMBER", "pattern": "\u00a5#,##0"}})
    time.sleep(0.5)
    ws.format(f"N2:N{total}", {"numberFormat": {"type": "NUMBER", "pattern": "$#,##0"}})
    time.sleep(0.5)
    ws.format(f"O2:O{total}", {"numberFormat": {"type": "NUMBER", "pattern": "\u00a5#,##0"}})
    time.sleep(0.5)
    ws.format(f"P2:P{total}", {"numberFormat": {"type": "NUMBER", "pattern": "#,##0.0\"%\""}})
    time.sleep(1)

    # === ヘッダーフォーマット (L1:R1) ===
    ws.format(f"L1:{LAST_COL}1", {
        "backgroundColor": {"red": 0.2, "green": 0.4, "blue": 0.8},
        "textFormat": {"bold": True, "foregroundColor": {"red": 1, "green": 1, "blue": 1}, "fontSize": 10},
        "horizontalAlignment": "CENTER",
        "wrapStrategy": "WRAP",
    })
    time.sleep(1)

    # === 塗りつぶしをR列まで拡張 ===
    print("色分け拡張中...")
    batch_formats = []
    for i, row in enumerate(rows[1:], start=2):
        cat = row[0]
        if cat in CATEGORY_COLORS:
            batch_formats.append({
                "range": f"L{i}:{LAST_COL}{i}",
                "format": {"backgroundColor": CATEGORY_COLORS[cat]},
            })

    for chunk_start in range(0, len(batch_formats), 15):
        chunk = batch_formats[chunk_start:chunk_start + 15]
        ws.batch_format(chunk)
        time.sleep(1)
    print("色分け完了")

    # === 列幅調整 (L〜R) ===
    col_widths = [
        (11, 12, 130),  # L: eBay手数料
        (12, 13, 110),  # M: 送料
        (13, 14, 130),  # N: 実質利益USD
        (14, 15, 130),  # O: 実質利益JPY
        (15, 16, 90),   # P: ROI
        (16, 17, 140),  # Q: 回転率
        (17, 18, 300),  # R: メルカリKW
        (18, 19, 100),  # S: 為替レート（参照用）
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

    # フィルターをR列まで拡張（既存フィルタ削除→再設定）
    requests.append({"clearBasicFilter": {"sheetId": ws.id}})
    sh.batch_update({"requests": requests})
    time.sleep(1)

    sh.batch_update({"requests": [{
        "setBasicFilter": {
            "filter": {
                "range": {
                    "sheetId": ws.id,
                    "startRowIndex": 0,
                    "endRowIndex": total,
                    "startColumnIndex": 0,
                    "endColumnIndex": 18,  # A-R
                }
            }
        }
    }]})
    print("フィルター拡張完了")

    # =========================================
    # 説明書シートを作成
    # =========================================
    print("\n説明書シート作成中...")
    try:
        guide_ws = sh.worksheet("説明書")
        guide_ws.clear()
    except gspread.WorksheetNotFound:
        guide_ws = sh.add_worksheet(title="説明書", rows=60, cols=4)
    time.sleep(1)

    guide_data = [
        ["eBay輸出せどり - 商品リスト説明書", "", "", ""],
        ["", "", "", ""],
        ["列", "項目名", "内容", "備考"],
        ["A", "カテゴリ", "商品の分類カテゴリ", "25カテゴリに分類"],
        ["B", "商品名", "eBay上の商品名（英語）", "クリックでeBay販売済み検索へリンク"],
        ["C", "メルカリ仕入れ目安(JPY)", "メルカリでの想定仕入れ価格（日本円）", "レンジの中間値を表示"],
        ["D", "eBay販売価格(JPY)", "eBayでの販売価格を日本円に換算", "E列 × 為替レート（自動計算）"],
        ["E", "eBay販売価格(USD)", "eBayでの実際の販売価格（米ドル）", "過去の販売実績に基づく"],
        ["F", "推定利益(JPY)", "概算の利益（日本円換算）", "G列 × 為替レート（自動計算）"],
        ["G", "推定利益(USD)", "概算の利益（米ドル）", "手数料・送料含まない粗利"],
        ["H", "販売日", "eBayでの販売確認日", "「通年」= 常時販売実績あり"],
        ["I", "ニッチ度", "商品のニッチさを★で評価", "★5=超ニッチ高利益、★3=一般的"],
        ["J", "備考", "商品に関する補足情報", ""],
        ["K", "eBay販売実績", "eBay上の出品数・販売件数", "定量的なデータ"],
        ["L", "eBay手数料(USD)", "eBayの落札手数料", "= 販売価格 × 13.25%（FVF）"],
        ["M", "送料目安(JPY)", "日本→米国の国際送料目安", "eパケット・EMS基準の概算"],
        ["N", "実質利益(USD)", "全経費差引後の実際の利益", "= 販売価格 - 仕入れ - 手数料 - 送料"],
        ["O", "実質利益(JPY)", "実質利益の日本円換算", "= N列 × 為替レート（自動計算）"],
        ["P", "ROI(%)", "投資利益率", "= 実質利益 ÷ 仕入れ原価 × 100"],
        ["Q", "回転率", "出品から売れるまでの目安期間", "即売れ / 標準 / 長期 の3段階"],
        ["R", "メルカリ検索キーワード", "仕入れ時にメルカリで検索するキーワード", "コピペしてそのまま使える"],
        ["", "", "", ""],
        ["", "", "", ""],
        ["用語・計算式の解説", "", "", ""],
        ["", "", "", ""],
        ["用語", "解説", "", ""],
        ["ROI", "Return On Investment（投資利益率）。100%なら仕入れ額と同額の利益。高いほど効率が良い", "", ""],
        ["FVF", "Final Value Fee。eBayが売上から徴収する手数料。カテゴリにより12〜15%。本表では13.25%で計算", "", ""],
        ["回転率「即売れ」", "出品後1〜2週間以内に売れる傾向。在庫リスク低、キャッシュフロー良好", "", ""],
        ["回転率「標準」", "出品後1〜2ヶ月で売れる傾向。一般的なペース", "", ""],
        ["回転率「長期」", "出品後2〜3ヶ月以上かかる可能性。高利益だが在庫保管コストに注意", "", ""],
        ["為替レート", "S2セルにGOOGLEFINANCEでリアルタイム取得。D/F/O列の日本円換算に使用", "", ""],
        ["", "", "", ""],
        ["", "", "", ""],
        ["仕入れのコツ", "", "", ""],
        ["", "", "", ""],
        ["No.", "コツ", "詳細", ""],
        ["1", "ジャンク・まとめ買い", "メルカリで「ジャンク」「まとめ売り」検索。安く大量仕入れ→eBayで個別販売", ""],
        ["2", "キーワード活用", "「日本限定」「廃番」「レア」で検索。海外入手困難品ほど高値", ""],
        ["3", "写真が命", "海外バイヤーは実物を見れない。高品質な写真が売上に直結", ""],
        ["4", "ROI重視で選別", "ROI 100%以上の商品を優先。ROIでソートして効率の良い商品から攻める", ""],
        ["5", "送料を意識", "軽量・小型商品は送料が安く利益が残りやすい。レコード・カードが好例", ""],
        ["6", "回転率とのバランス", "ROIが高くても売れなければ意味なし。即売れ×高ROIが最強", ""],
        ["", "", "", ""],
        ["", "", "", ""],
        ["送料の目安（日本→米国）", "", "", ""],
        ["", "", "", ""],
        ["発送方法", "重量", "料金目安", "特徴"],
        ["eパケットライト", "〜2kg", "¥600〜¥1,500", "最安。追跡あり、補償なし。2〜3週間"],
        ["eパケット", "〜2kg", "¥1,000〜¥2,000", "追跡+補償あり。1〜2週間"],
        ["EMS", "〜30kg", "¥2,000〜¥10,000", "最速3〜5日。補償あり。高額品向け"],
        ["国際eパケット", "〜2kg", "¥1,500〜¥2,500", "書留付き。追跡+補償充実"],
        ["クーリエ(DHL/FedEx)", "制限なし", "¥3,000〜", "大型・高額品向け。最速2〜3日"],
    ]

    guide_ws.update(range_name="A1", values=guide_data)
    print("説明書データ書き込み完了")
    time.sleep(1)

    # 説明書フォーマット
    # タイトル
    guide_ws.format("A1:D1", {
        "textFormat": {"bold": True, "fontSize": 16},
        "horizontalAlignment": "CENTER",
    })
    time.sleep(0.5)

    # 列説明ヘッダー (A3:D3)
    guide_ws.format("A3:D3", {
        "backgroundColor": {"red": 0.2, "green": 0.4, "blue": 0.8},
        "textFormat": {"bold": True, "foregroundColor": {"red": 1, "green": 1, "blue": 1}},
        "horizontalAlignment": "CENTER",
    })
    time.sleep(0.5)

    # セクションヘッダー
    for row_num in [23, 35, 46]:
        guide_ws.format(f"A{row_num}:D{row_num}", {
            "textFormat": {"bold": True, "fontSize": 13},
            "backgroundColor": {"red": 0.93, "green": 0.93, "blue": 0.93},
        })
        time.sleep(0.3)

    # 用語ヘッダー (A25:D25)
    guide_ws.format("A25:D25", {
        "backgroundColor": {"red": 0.85, "green": 0.92, "blue": 1.0},
        "textFormat": {"bold": True},
    })
    time.sleep(0.3)

    # 仕入れコツヘッダー (A37:D37)
    guide_ws.format("A37:D37", {
        "backgroundColor": {"red": 0.85, "green": 0.92, "blue": 1.0},
        "textFormat": {"bold": True},
    })
    time.sleep(0.3)

    # 送料ヘッダー (A48:D48)
    guide_ws.format("A48:D48", {
        "backgroundColor": {"red": 0.85, "green": 0.92, "blue": 1.0},
        "textFormat": {"bold": True},
    })
    time.sleep(0.5)

    # 列幅
    guide_requests = [
        {"updateDimensionProperties": {"range": {"sheetId": guide_ws.id, "dimension": "COLUMNS", "startIndex": 0, "endIndex": 1}, "properties": {"pixelSize": 180}, "fields": "pixelSize"}},
        {"updateDimensionProperties": {"range": {"sheetId": guide_ws.id, "dimension": "COLUMNS", "startIndex": 1, "endIndex": 2}, "properties": {"pixelSize": 250}, "fields": "pixelSize"}},
        {"updateDimensionProperties": {"range": {"sheetId": guide_ws.id, "dimension": "COLUMNS", "startIndex": 2, "endIndex": 3}, "properties": {"pixelSize": 500}, "fields": "pixelSize"}},
        {"updateDimensionProperties": {"range": {"sheetId": guide_ws.id, "dimension": "COLUMNS", "startIndex": 3, "endIndex": 4}, "properties": {"pixelSize": 300}, "fields": "pixelSize"}},
    ]
    sh.batch_update({"requests": guide_requests})

    # セルA1:D1をマージ
    sh.batch_update({"requests": [{
        "mergeCells": {
            "range": {"sheetId": guide_ws.id, "startRowIndex": 0, "endRowIndex": 1, "startColumnIndex": 0, "endColumnIndex": 4},
            "mergeType": "MERGE_ALL",
        }
    }]})

    print("説明書シート作成完了!")
    print(f"\n全作業完了! URL: {sh.url}")


if __name__ == "__main__":
    main()
