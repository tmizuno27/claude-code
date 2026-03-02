# -*- coding: utf-8 -*-
"""全シートデータをCSVに保存"""
import csv
import json
from pathlib import Path

from google.oauth2 import service_account
from googleapiclient.discovery import build

CREDS_FILE = "c:/Users/tmizu/マイドライブ/GitHub/data/sheets-sync/credentials/service-account.json"
SHEET_ID = "1ZNOFUPwDu64Oyp47tdvsOdgRO5_l9YxmQE3FkIttGxE"
OUTPUT = Path("c:/Users/tmizu/マイドライブ/GitHub/data/sheets-sync/output")

creds = service_account.Credentials.from_service_account_file(
    CREDS_FILE,
    scopes=[
        "https://www.googleapis.com/auth/spreadsheets.readonly",
        "https://www.googleapis.com/auth/drive.readonly",
    ],
)
service = build("sheets", "v4", credentials=creds)
OUTPUT.mkdir(parents=True, exist_ok=True)

spreadsheet = service.spreadsheets().get(spreadsheetId=SHEET_ID).execute()
title = spreadsheet["properties"]["title"]
sheets_info = []

for sheet in spreadsheet["sheets"]:
    name = sheet["properties"]["title"]
    safe = name.replace("/", "_").replace(" ", "_")
    try:
        result = (
            service.spreadsheets()
            .values()
            .get(spreadsheetId=SHEET_ID, range=name)
            .execute()
        )
        values = result.get("values", [])
        if values:
            csv_path = OUTPUT / f"{safe}.csv"
            with open(csv_path, "w", encoding="utf-8-sig", newline="") as f:
                writer = csv.writer(f)
                writer.writerows(values)
            sheets_info.append({"name": name, "file": csv_path.name, "rows": len(values)})
    except Exception as e:
        sheets_info.append({"name": name, "error": str(e)})

meta = {"spreadsheet_id": SHEET_ID, "title": title, "sheets": sheets_info}
with open(OUTPUT / "metadata.json", "w", encoding="utf-8") as f:
    json.dump(meta, f, ensure_ascii=False, indent=2)

with open(OUTPUT / "summary.txt", "w", encoding="utf-8") as f:
    f.write(f"Title: {title}\n")
    for s in sheets_info:
        if "error" in s:
            f.write(f"  {s['name']}: ERROR - {s['error']}\n")
        else:
            f.write(f"  {s['name']}: {s['rows']} rows -> {s['file']}\n")
