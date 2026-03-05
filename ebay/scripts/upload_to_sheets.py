#!/usr/bin/env python3
"""
eBayニッチ商品データをGoogle Sheetsにアップロードするスクリプト

サービスアカウントのDrive容量が0のため、以下の流れで動作:
1. ブラウザで新規Googleスプレッドシートを開く
2. ユーザーがURLからスプレッドシートIDをコピペ
3. サービスアカウントに共有して自動でデータ入力

使い方:
  python upload_to_sheets.py
  または
  python upload_to_sheets.py <スプレッドシートID>
"""

import csv
import os
import sys
import time
import webbrowser
import gspread
from google.oauth2.service_account import Credentials

# 設定
CREDENTIALS_PATH = os.path.join(os.path.dirname(__file__), '..', '..', 'tools', 'sheets-sync', 'credentials', 'service-account.json')
CSV_PATH = os.path.join(os.path.dirname(__file__), '..', 'ebay-niche-products.csv')
SERVICE_ACCOUNT_EMAIL = "sheets-reader@sheets-sync-489022.iam.gserviceaccount.com"

SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive",
]


def get_spreadsheet_id():
    """スプレッドシートIDを取得（引数 or 対話的に）"""
    if len(sys.argv) > 1:
        return sys.argv[1]

    print("=" * 60)
    print("eBay輸出リサーチ - Google Sheetsセットアップ")
    print("=" * 60)
    print()
    print("1. ブラウザで新しいGoogleスプレッドシートを開きます...")
    webbrowser.open("https://sheets.new")
    time.sleep(2)

    print()
    print("2. 開いたスプレッドシートの共有設定で、")
    print(f"   以下のメールアドレスを「編集者」として追加してください:")
    print(f"   → {SERVICE_ACCOUNT_EMAIL}")
    print()
    print("3. スプレッドシートのURLからIDをコピーしてください")
    print("   URL例: https://docs.google.com/spreadsheets/d/XXXXX/edit")
    print("   IDは「XXXXX」の部分です")
    print()

    sheet_id = input("スプレッドシートIDを入力: ").strip()
    if not sheet_id:
        print("IDが入力されませんでした。終了します。")
        sys.exit(1)

    # URLが貼られた場合、IDを抽出
    if "docs.google.com" in sheet_id:
        parts = sheet_id.split("/d/")
        if len(parts) > 1:
            sheet_id = parts[1].split("/")[0]

    return sheet_id


def populate_spreadsheet(gc, sheet_id):
    """スプレッドシートにデータを入力"""
    sh = gc.open_by_key(sheet_id)
    print(f"スプレッドシートを開きました: {sh.title}")

    # --- 商品リスト タブ ---
    try:
        ws = sh.worksheet("商品リスト")
        ws.clear()
    except gspread.WorksheetNotFound:
        ws = sh.add_worksheet(title="商品リスト", rows=100, cols=10)
    print("商品リストタブ準備完了")

    # CSV読み込み
    with open(CSV_PATH, "r", encoding="utf-8") as f:
        reader = csv.reader(f)
        rows = list(reader)

    ws.update(range_name="A1", values=rows)
    print(f"商品リスト: {len(rows)-1}件のデータを書き込みました")
    time.sleep(2)

    # ヘッダーフォーマット
    ws.format("A1:H1", {
        "backgroundColor": {"red": 0.2, "green": 0.4, "blue": 0.8},
        "textFormat": {"bold": True, "foregroundColor": {"red": 1, "green": 1, "blue": 1}},
        "horizontalAlignment": "CENTER",
    })
    time.sleep(1)

    # カテゴリごとに色分け
    category_colors = {
        "鉋・大工道具": {"red": 1.0, "green": 0.95, "blue": 0.8},
        "盆栽鉢": {"red": 0.85, "green": 1.0, "blue": 0.85},
        "南部鉄瓶": {"red": 0.9, "green": 0.9, "blue": 1.0},
        "和包丁": {"red": 1.0, "green": 0.85, "blue": 0.85},
        "帯付きレコード": {"red": 1.0, "green": 0.9, "blue": 1.0},
        "万年筆": {"red": 0.95, "green": 1.0, "blue": 1.0},
    }

    for i, row in enumerate(rows[1:], start=2):
        category = row[0] if row else ""
        if category in category_colors:
            ws.format(f"A{i}:H{i}", {"backgroundColor": category_colors[category]})
            time.sleep(0.3)

    print("色分け完了")
    time.sleep(1)

    # --- サマリー タブ ---
    try:
        summary_ws = sh.worksheet("サマリー")
        summary_ws.clear()
    except gspread.WorksheetNotFound:
        summary_ws = sh.add_worksheet(title="サマリー", rows=30, cols=6)
    print("サマリータブ準備完了")

    summary_data = [
        ["カテゴリ別サマリー", "", "", "", "", ""],
        ["カテゴリ", "商品数", "eBay平均価格(USD)", "メルカリ仕入れ目安", "おすすめ度", "コメント"],
        ["鉋・大工道具", "15", "$200〜$1,961", "¥1,000〜¥15,000", "★★★★★", "最も利益率が高い。名工ものは$1,000超え"],
        ["盆栽鉢", "5", "$25〜$68", "¥1,500〜¥8,000", "★★★★☆", "米国盆栽人口増。作家ものは更に高値"],
        ["南部鉄瓶", "4", "$11〜$59", "¥2,000〜¥10,000", "★★★★☆", "茶道+インテリア需要。高級品は$100〜$1,000"],
        ["和包丁", "4", "$18〜$28", "¥1,500〜¥5,000", "★★★☆☆", "堺打刃物が人気。高級品は$100超えも"],
        ["帯付きレコード", "6", "$34〜$74", "¥500〜¥3,000", "★★★★★", "軽量で送料安。ニッチジャンルほど高値"],
        ["万年筆", "4", "$50〜$178", "¥5,000〜¥30,000", "★★★★☆", "漆塗り・限定品はプレミアム"],
        ["", "", "", "", "", ""],
        ["リサーチ日", "2026-03-04", "", "", "", ""],
        ["データソース", "eBay Sold Listings + メルカリ相場検索", "", "", "", ""],
        ["", "", "", "", "", ""],
        ["仕入れのコツ", "", "", "", "", ""],
        ["1. メルカリで「ジャンク」「まとめ売り」検索 → 安く大量に仕入れてeBayで個別販売", "", "", "", "", ""],
        ["2. 「日本限定」「廃番」「レア」がキーワード → 海外で手に入らないものほど高値", "", "", "", "", ""],
        ["3. ROI目安: アニメ系コレクタブルは平均ROI 441%", "", "", "", "", ""],
        ["4. 状態の良い写真が命 → 海外バイヤーは実物を見れないので写真の質が売上に直結", "", "", "", "", ""],
        ["", "", "", "", "", ""],
        ["最優先カテゴリ", "", "", "", "", ""],
        ["1位: 鉋・大工道具 — メルカリ数千円 → eBay $200〜$1,900。利益率最高", "", "", "", "", ""],
        ["2位: 帯付きレコード — 軽量で送料安、回転率が良い", "", "", "", "", ""],
        ["3位: 万年筆 — 日本限定の漆塗りは海外で入手困難", "", "", "", "", ""],
        ["4位: 盆栽鉢 — 米国盆栽ブームで需要拡大中", "", "", "", "", ""],
    ]

    summary_ws.update(range_name="A1", values=summary_data)
    print("サマリーデータ書き込み完了")
    time.sleep(1)

    # サマリーヘッダーフォーマット
    summary_ws.format("A1:F1", {
        "textFormat": {"bold": True, "fontSize": 14},
        "horizontalAlignment": "CENTER",
    })
    time.sleep(0.5)
    summary_ws.format("A2:F2", {
        "backgroundColor": {"red": 0.2, "green": 0.4, "blue": 0.8},
        "textFormat": {"bold": True, "foregroundColor": {"red": 1, "green": 1, "blue": 1}},
        "horizontalAlignment": "CENTER",
    })

    # デフォルトのSheet1を削除（あれば）
    try:
        default_sheet = sh.worksheet("Sheet1")
        sh.del_worksheet(default_sheet)
    except gspread.WorksheetNotFound:
        pass

    # シート名を変更
    try:
        sh.update_title("eBay輸出リサーチ - 日本ニッチ商品")
    except Exception:
        pass

    print(f"\nスプレッドシートURL: {sh.url}")
    print("完了!")


def main():
    # 認証
    creds = Credentials.from_service_account_file(CREDENTIALS_PATH, scopes=SCOPES)
    gc = gspread.authorize(creds)

    sheet_id = get_spreadsheet_id()
    populate_spreadsheet(gc, sheet_id)


if __name__ == "__main__":
    main()
