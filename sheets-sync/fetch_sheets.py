# -*- coding: utf-8 -*-
"""
Google Sheets → CSV 自動取得スクリプト
config.json に登録されたスプレッドシートをCSVとして保存する
"""

import csv
import json
import os
import sys
from datetime import datetime
from pathlib import Path

from google.oauth2 import service_account
from googleapiclient.discovery import build

SCRIPT_DIR = Path(__file__).parent
CONFIG_FILE = SCRIPT_DIR / "config.json"
LOG_FILE = SCRIPT_DIR / "sheets-sync.log"


def log(message):
    ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    entry = f"[{ts}] {message}"
    print(entry)
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(entry + "\n")


def load_config():
    with open(CONFIG_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def get_sheets_service(credentials_file):
    creds_path = SCRIPT_DIR / credentials_file
    if not creds_path.exists():
        log(f"[ERROR] credentials not found: {creds_path}")
        log("[ERROR] See SETUP.md for instructions")
        sys.exit(1)

    scopes = ["https://www.googleapis.com/auth/spreadsheets.readonly"]
    creds = service_account.Credentials.from_service_account_file(
        str(creds_path), scopes=scopes
    )
    return build("sheets", "v4", credentials=creds)


def fetch_and_save(service, sheet_config, output_dir):
    name = sheet_config["name"]
    spreadsheet_id = sheet_config["spreadsheet_id"]
    ranges = sheet_config.get("ranges", ["シート1"])

    output_path = SCRIPT_DIR / output_dir
    output_path.mkdir(parents=True, exist_ok=True)

    for range_name in ranges:
        try:
            result = (
                service.spreadsheets()
                .values()
                .get(spreadsheetId=spreadsheet_id, range=range_name)
                .execute()
            )
            values = result.get("values", [])

            if not values:
                log(f"[WARN] {name}/{range_name}: no data")
                continue

            safe_range = range_name.replace("!", "_").replace(":", "-")
            csv_file = output_path / f"{name}_{safe_range}.csv"

            with open(csv_file, "w", encoding="utf-8-sig", newline="") as f:
                writer = csv.writer(f)
                writer.writerows(values)

            log(f"OK: {name}/{range_name} → {csv_file.name} ({len(values)} rows)")

        except Exception as e:
            log(f"[ERROR] {name}/{range_name}: {e}")


def save_metadata(config, output_dir):
    output_path = SCRIPT_DIR / output_dir
    metadata = {
        "last_sync": datetime.now().isoformat(),
        "sheets": [s["name"] for s in config["sheets"]],
    }
    with open(output_path / "metadata.json", "w", encoding="utf-8") as f:
        json.dump(metadata, f, ensure_ascii=False, indent=2)


def main():
    log("=== Google Sheets sync start ===")

    config = load_config()
    service = get_sheets_service(config["credentials_file"])
    output_dir = config.get("output_dir", "output")

    for sheet_config in config["sheets"]:
        if sheet_config["spreadsheet_id"].startswith("ここに"):
            log(f"[SKIP] {sheet_config['name']}: not configured yet")
            continue
        fetch_and_save(service, sheet_config, output_dir)

    save_metadata(config, output_dir)
    log("=== Google Sheets sync complete ===")


if __name__ == "__main__":
    main()
