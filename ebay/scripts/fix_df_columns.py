#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""D列(eBay価格USD)とF列(推定利益USD)を数値で修正"""

import sys, io, os, csv, re, time
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
import gspread
from google.oauth2.service_account import Credentials

CREDS = os.path.join(os.path.dirname(__file__), '..', '..', 'tools', 'sheets-sync', 'credentials', 'service-account.json')
CSV_PATH = os.path.join(os.path.dirname(__file__), '..', 'ebay-niche-products.csv')
SHEET_ID = "1xjdusAVbdyzRwC_JnG93s9J9tC5G11pYtBCrP7Vr_l4"

SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive",
]


def parse_usd(val):
    """USD文字列を数値に変換"""
    val = val.strip().replace(",", "")
    # $1536 形式
    m = re.match(r'^\$(\d+(?:\.\d+)?)$', val)
    if m:
        return float(m.group(1))
    # $150-400 形式
    m = re.match(r'^\$(\d+(?:\.\d+)?)\s*[-\u301c~]\s*\$?(\d+(?:\.\d+)?)$', val)
    if m:
        return round((float(m.group(1)) + float(m.group(2))) / 2)
    # $1400+ 形式
    m = re.match(r'^\$(\d+(?:\.\d+)?)\+$', val)
    if m:
        return float(m.group(1))
    # ¥25428利益 形式（円→ドル概算）
    m = re.search(r'[\u00a5\uffe5](\d+)', val)
    if m:
        return round(int(m.group(1)) / 150, 1)
    return None


def main():
    creds = Credentials.from_service_account_file(CREDS, scopes=SCOPES)
    gc = gspread.authorize(creds)
    sh = gc.open_by_key(SHEET_ID)
    ws = sh.worksheet("商品リスト")

    # CSVからeBay価格と推定利益を再取得
    with open(CSV_PATH, "r", encoding="utf-8") as f:
        reader = csv.reader(f)
        csv_rows = list(reader)

    d_vals = []  # D列: eBay価格 USD
    f_vals = []  # F列: 推定利益 USD

    for i, row in enumerate(csv_rows):
        if i == 0:
            continue
        ebay_raw = row[2] if len(row) > 2 else ""
        profit_raw = row[4] if len(row) > 4 else ""

        d = parse_usd(ebay_raw)
        f = parse_usd(profit_raw)

        d_vals.append([d if d is not None else 0])
        f_vals.append([f if f is not None else 0])

        if i <= 5:
            print(f"Row{i}: D=[{ebay_raw}] -> {d}, F=[{profit_raw}] -> {f}")

    print(f"Total: {len(d_vals)} rows")

    # D列を数値で上書き (value_input_option=RAW で数式として解釈されない)
    ws.update(range_name="D2", values=d_vals, value_input_option="RAW")
    print("D列書き込み完了")
    time.sleep(1)

    # F列を数値で上書き
    ws.update(range_name="F2", values=f_vals, value_input_option="RAW")
    print("F列書き込み完了")
    time.sleep(1)

    # 表示形式を設定
    total = len(d_vals) + 1
    ws.format(f"D2:D{total}", {"numberFormat": {"type": "NUMBER", "pattern": '[$\u0024]#,##0'}})
    time.sleep(0.5)
    ws.format(f"F2:F{total}", {"numberFormat": {"type": "NUMBER", "pattern": '[$\u0024]#,##0'}})
    print("表示形式設定完了")

    # 確認
    time.sleep(1)
    check = ws.get("D1:D6")
    for r in check:
        print(f"  D: {r}")
    check2 = ws.get("F1:F6")
    for r in check2:
        print(f"  F: {r}")

    print("修正完了!")


if __name__ == "__main__":
    main()
