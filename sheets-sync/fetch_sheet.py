"""
Google Sheets 自動読み取りスクリプト
入金管理シートのデータをCSVとして保存する
"""

import csv
import json
import os
import sys
from datetime import datetime
from pathlib import Path

import gspread
from google.oauth2.service_account import Credentials

# --- 設定 ---
SCRIPT_DIR = Path(__file__).parent
CREDENTIALS_PATH = SCRIPT_DIR / "credentials" / "service-account.json"
OUTPUT_DIR = SCRIPT_DIR / "output"

# Google Sheets の設定
SPREADSHEET_ID = "1Q1W3Uf01-0Sp780M2lhjxO84D212dBZu7OvWoOsv9ws"

SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets.readonly",
    "https://www.googleapis.com/auth/drive.readonly",
]


def get_client():
    """認証済みのgspreadクライアントを返す"""
    if not CREDENTIALS_PATH.exists():
        print(f"エラー: 認証ファイルが見つかりません: {CREDENTIALS_PATH}")
        print("セットアップガイドを参照してください: setup-guide.md")
        sys.exit(1)

    creds = Credentials.from_service_account_file(str(CREDENTIALS_PATH), scopes=SCOPES)
    return gspread.authorize(creds)


def fetch_all_sheets(client):
    """全シートのデータを取得してCSVに保存する"""
    spreadsheet = client.open_by_key(SPREADSHEET_ID)
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    results = []

    for worksheet in spreadsheet.worksheets():
        sheet_name = worksheet.title
        safe_name = sheet_name.replace("/", "_").replace("\\", "_")
        data = worksheet.get_all_values()

        if not data:
            print(f"  [{sheet_name}] データなし - スキップ")
            continue

        # CSVファイルに保存
        csv_path = OUTPUT_DIR / f"{safe_name}.csv"
        with open(csv_path, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerows(data)

        print(f"  [{sheet_name}] {len(data)}行 → {csv_path.name}")
        results.append({"sheet": sheet_name, "file": str(csv_path), "rows": len(data)})

    # メタデータを保存
    meta = {
        "fetched_at": datetime.now().isoformat(),
        "spreadsheet_id": SPREADSHEET_ID,
        "sheets": results,
    }
    meta_path = OUTPUT_DIR / "metadata.json"
    with open(meta_path, "w", encoding="utf-8") as f:
        json.dump(meta, f, ensure_ascii=False, indent=2)

    return results


def main():
    print("=" * 50)
    print("入金管理シート データ取得")
    print("=" * 50)
    print()

    print("認証中...")
    client = get_client()

    print(f"スプレッドシートを取得中... (ID: {SPREADSHEET_ID[:20]}...)")
    results = fetch_all_sheets(client)

    print()
    print(f"完了! {len(results)}シートを取得しました。")
    print(f"出力先: {OUTPUT_DIR}")


if __name__ == "__main__":
    main()
