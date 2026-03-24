#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""ファクトチェック結果をスプレッドシートに反映"""

import sys, io, re, time, os, pathlib
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
import gspread
from google.oauth2.service_account import Credentials

CREDS = str(pathlib.Path(os.path.expanduser("~")) / "\u30de\u30a4\u30c9\u30e9\u30a4\u30d6" / "GitHub" / "claude-code" / "tools" / "sheets-sync" / "credentials" / "service-account.json")
SHEET_ID = "1xjdusAVbdyzRwC_JnG93s9J9tC5G11pYtBCrP7Vr_l4"
SCOPES = ["https://www.googleapis.com/auth/spreadsheets", "https://www.googleapis.com/auth/drive"]

# ファクトチェック結果: 商品名 → (eBay USD中間値, メルカリJPY中間値)
# eBay=中間値(数値), メルカリ=中間値(数値)
CORRECTIONS = {
    # === 鉋・大工道具 (大幅修正) ===
    "Tsunesaburo 70mm Maboroshi Plane": (444, 25000),
    "Naga Dai Kanna Yamamoto Kensuke 60mm": (593, 55000),
    "Tsunesaburo Meigo Ryomo 55mm Kanna": (275, 17500),
    "Togyu 65mm Smoothing Hand Plane": (275, 10000),
    "Vintage Hand Plane Kanna Iron Part": (95, 2000),
    "Morikage 65mm Smoothing Plane": (170, 6500),
    "Nankin Kanna Smoothing Plane Mitsu-Yuki": (140, 5000),
    "Kosado 60mm Smoothing Plane": (200, 7500),
    "Yoshihiromaru 58mm Smoothing Plane": (200, 7500),
    "Senkichi 60mm Japanese KANNA": (40, 2250),
    "Ishibashi Toushi Kanna 70mm": (190, 7500),
    "Kakuri 42mm Hand Plane": (43, 1750),
    "52mm Japanese Smoothing Hand Plane": (100, 3500),
    # === 鑿 ===
    "Kikuhiro Maru Vintage Nomi Chisel Set of 10": (550, 50000),
    "NOMI Vintage Long Chisel Set Made by Japanese Craftsmen": (300, 17500),
    # === 盆栽鉢 ===
    "Vintage Japanese Signed Turquoise Glaze Bonsai Pot": (35, 3250),
    # === 南部鉄瓶 ===
    "Vintage Nambu Tetsubin Cast Iron Teapot": (138, 9000),
    "Ryubundo Vintage Tetsubin Iron Kettle": (768, 55000),
    "Japanese Cast Iron Tetsubin Ribbed Design": (103, 6500),
    # === 和包丁 ===
    "Masamoto Japanese Deba Knife": (190, 12500),
    # === 帯付きレコード ===
    "KISS Dynasty Japanese Import LP w/OBI 1979": (52, 5000),
    "Gundam OST Vinyl LP Japan Anime w/Obi": (40, 6000),
    "SATELLITE LOVERS Japan LTD Edition LP OBI": (80, 6500),
    "Billy Joel The Stranger First Japanese Pressing w/Obi": (32, 2250),
    "Brand X Livestock 1977 OBI Japanese": (50, 3250),
    "Journey Departure Rare Vintage w/OBI": (68, 5000),
    # === 万年筆 ===
    "Kaweco Collection Sport Pearl Limited Edition": (67, 7500),
    # === ポケモンカード ===
    "Pokemon e-Card Psyduck コダック": (165, 5780),
    # === トレーディングカード ===
    "ONE PIECE Card Game Japanese Booster": (244, 12000),
    "Weiss Schwarz Japanese Anime Collaboration": (55, 14000),
    # === レトロゲーム ===
    "Dragon Quest IV Famicom": (15, 2500),
    "PS Vita Console Japan": (180, 15500),
    "Super Famicom Japanese RPG Games": (50, 1750),
    # === アニメフィギュア ===
    "Sailor Moon Vintage Alarm Clock": (123, 6500),
    "Gundam MG/PG Model Kit Bandai Limited": (200, 16000),
    "Nendoroid Limited Edition Japan Exclusive": (100, 5750),
    # === 腕時計 ===
    "SEIKO Vintage 6139-6002 Pogue Chronograph": (950, 90000),
    "SEIKO 62MAS Vintage Diver 1965": (3850, 400000),
    # === カメラ ===
    "Nikon F3 Film Camera Body": (250, 30000),
    "Canon FD 50mm f/1.4 Vintage Lens": (100, 10000),
    "Pentax 67 Medium Format Camera": (950, 85000),
    "Olympus OM-1 Film Camera": (130, 14000),
    "FUJIFILM X100 Series Digital": (1050, 125000),
    "Sony Cyber-shot RX100 Series": (500, 40000),
    # === 釣り具 ===
    "SHIMANO Stella Vintage Spinning Reel": (450, 55000),
    "SHIMANO Calcutta Conquest Baitcast": (275, 35000),
    "DAIWA Certate Spinning Reel": (325, 22500),
    # === 伝統工芸品 ===
    "Nousaku Tin Sake Cup Set": (108, 9000),
    # === サンリオ ===
    # === 小型家電 ===
    "Panasonic Nanoe Hair Dryer": (150, 15000),
    "Sony Walkman Vintage WM-2": (175, 14000),
    # === スニーカー ===
    "Onitsuka Tiger Japan Made": (150, 10000),
    # === ダイキャストカー ===
    "Hot Wheels Japan Convention Exclusive": (150, 18000),
    # === 文房具 ===
    "Pilot Vanishing Point Capless Fountain Pen": (180, 13000),
    # === JDMパーツ ===
    "Toyota Supra JDM Headlight": (400, 20000),
    # === 電子辞書 ===
    "Casio Ex-word Japanese Learning": (80, 5000),
}


def main():
    creds = Credentials.from_service_account_file(CREDS, scopes=SCOPES)
    gc = gspread.authorize(creds)
    sh = gc.open_by_key(SHEET_ID)
    ws = sh.worksheet("商品リスト")

    rows = ws.get_all_values()
    total = len(rows)
    print(f"{total}行取得")

    # 商品名(B列)でマッチングして、E列(eBay USD)とC列(メルカリJPY)を更新
    e_updates = {}  # row_index -> new eBay USD value
    c_updates = {}  # row_index -> new Mercari JPY value

    matched = 0
    for i, row in enumerate(rows):
        if i == 0:
            continue
        product_name = row[1]  # B列（HYPERLINK数式の場合はテキスト表示名）

        # HYPERLINK数式から表示名を抽出
        display_name = product_name
        # gspreadのget_all_valuesは表示値を返すのでそのまま使える

        for key, (ebay_usd, mercari_jpy) in CORRECTIONS.items():
            if key in display_name or display_name in key:
                e_updates[i] = ebay_usd
                c_updates[i] = mercari_jpy
                matched += 1
                break

    print(f"マッチした商品: {matched}件")

    # E列(eBay USD)を更新
    if e_updates:
        e_values = []
        for i in range(1, total):
            if i in e_updates:
                e_values.append([e_updates[i]])
            else:
                # 既存値を維持（get_all_valuesの値を使う）
                try:
                    existing = rows[i][4]  # E列
                    # 数値に変換できるか試す
                    clean = existing.replace("$", "").replace(",", "").replace("¥", "").strip()
                    e_values.append([float(clean) if clean else existing])
                except (ValueError, IndexError):
                    e_values.append([existing if len(rows[i]) > 4 else ""])

        ws.update(range_name="E2", values=e_values, value_input_option="USER_ENTERED")
        print("E列(eBay USD)更新完了")
        time.sleep(2)

    # C列(メルカリJPY)を更新
    if c_updates:
        c_values = []
        for i in range(1, total):
            if i in c_updates:
                c_values.append([c_updates[i]])
            else:
                try:
                    existing = rows[i][2]  # C列
                    clean = existing.replace("¥", "").replace(",", "").strip()
                    c_values.append([float(clean) if clean else existing])
                except (ValueError, IndexError):
                    c_values.append([existing if len(rows[i]) > 2 else ""])

        ws.update(range_name="C2", values=c_values, value_input_option="USER_ENTERED")
        print("C列(メルカリJPY)更新完了")
        time.sleep(1)

    # 表示形式を再設定
    ws.format(f"E2:E{total}", {"numberFormat": {"type": "NUMBER", "pattern": "$#,##0"}})
    time.sleep(0.5)
    ws.format(f"C2:C{total}", {"numberFormat": {"type": "NUMBER", "pattern": "\u00a5#,##0"}})

    print(f"\nファクトチェック反映完了! {matched}件の商品を修正")
    print(f"URL: {sh.url}")


if __name__ == "__main__":
    main()
