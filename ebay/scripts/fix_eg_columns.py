#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys, io, os, csv, re, time
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
import gspread
from google.oauth2.service_account import Credentials

CREDS = os.path.join(os.path.dirname(__file__), '..', '..', 'tools', 'sheets-sync', 'credentials', 'service-account.json')
CSV_PATH = os.path.join(os.path.dirname(__file__), '..', 'ebay-niche-products.csv')
SHEET_ID = "1xjdusAVbdyzRwC_JnG93s9J9tC5G11pYtBCrP7Vr_l4"

SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive",
]


def to_num(val):
    """USD価格文字列を数値に変換"""
    val = val.strip().replace(",", "")

    # $1536
    if re.match(r"^\$\d+$", val):
        return float(val.replace("$", ""))

    # $1400+
    if re.match(r"^\$\d+\+$", val):
        return float(val.replace("$", "").replace("+", ""))

    # $150-400 or $150-$400
    m = re.match(r"^\$(\d+)\s*-\s*\$?(\d+)$", val)
    if m:
        return round((float(m.group(1)) + float(m.group(2))) / 2)

    # ¥25428利益 (yen profit -> convert to USD at ~150)
    m = re.search(r"\xa5(\d+)", val)
    if m:
        return round(int(m.group(1)) / 150, 1)

    # plain number
    if re.match(r"^\d+(\.\d+)?$", val):
        return float(val)

    return 0


def main():
    creds = Credentials.from_service_account_file(CREDS, scopes=SCOPES)
    gc = gspread.authorize(creds)
    sh = gc.open_by_key(SHEET_ID)
    ws = sh.worksheet("商品リスト")

    with open(CSV_PATH, "r", encoding="utf-8") as f:
        csv_rows = list(csv.reader(f))

    e_vals = []  # E列: eBay販売価格(USD)
    g_vals = []  # G列: 推定利益(USD)

    for i, row in enumerate(csv_rows):
        if i == 0:
            continue
        ebay_raw = row[2] if len(row) > 2 else ""
        profit_raw = row[4] if len(row) > 4 else ""
        e = to_num(ebay_raw)
        g = to_num(profit_raw)
        e_vals.append([e])
        g_vals.append([g])
        if i <= 5:
            print(f"Row{i}: [{ebay_raw}] -> E={e}, [{profit_raw}] -> G={g}")

    print(f"Total: {len(e_vals)} rows")

    # E列に数値を書き込み
    ws.update(range_name="E2", values=e_vals, value_input_option="USER_ENTERED")
    print("E列書き込み完了")
    time.sleep(1)

    # G列に数値を書き込み
    ws.update(range_name="G2", values=g_vals, value_input_option="USER_ENTERED")
    print("G列書き込み完了")
    time.sleep(1)

    # 表示形式
    total = len(e_vals) + 1
    ws.format(f"E2:E{total}", {"numberFormat": {"type": "NUMBER", "pattern": "[$¥]#,##0"}})
    time.sleep(0.5)
    ws.format(f"G2:G{total}", {"numberFormat": {"type": "NUMBER", "pattern": "[$¥]#,##0"}})
    time.sleep(0.5)

    # Wait, E and G are USD columns! Fix format
    ws.format(f"E2:E{total}", {"numberFormat": {"type": "NUMBER", "pattern": "[$\\$]#,##0"}})
    time.sleep(0.5)
    ws.format(f"G2:G{total}", {"numberFormat": {"type": "NUMBER", "pattern": "[$\\$]#,##0"}})
    print("表示形式設定完了")
    time.sleep(1)

    # D列・F列の確認
    time.sleep(2)
    d_check = ws.get("D2:D6")
    e_check = ws.get("E2:E6")
    f_check = ws.get("F2:F6")
    g_check = ws.get("G2:G6")
    for i in range(5):
        print(f"Row{i+2}: D={d_check[i]} E={e_check[i]} F={f_check[i]} G={g_check[i]}")

    print("修正完了!")


if __name__ == "__main__":
    main()
