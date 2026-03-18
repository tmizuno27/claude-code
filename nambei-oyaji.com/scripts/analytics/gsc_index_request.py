"""
Google Search Console Indexing API - 3サイト一括インデックス登録申請
全公開記事のURLをURL_UPDATEDとして通知する
"""

import csv
import json
import time
import os
from datetime import datetime
from google.oauth2 import service_account
from google.auth.transport.requests import AuthorizedSession

# 認証設定
CREDENTIALS_FILE = r"C:\Users\tmizu\マイドライブ\GitHub\claude-code\nambei-oyaji.com\config\ga4-credentials.json"
SCOPES = ["https://www.googleapis.com/auth/indexing"]
API_URL = "https://indexing.googleapis.com/v3/urlNotifications:publish"

BASE = r"C:\Users\tmizu\マイドライブ\GitHub\claude-code"

# サイト定義: (dir, csv_path, site_url, url_extractor)
SITES = [
    {
        "name": "nambei-oyaji.com",
        "csv": os.path.join(BASE, "nambei-oyaji.com", "outputs", "article-management.csv"),
        "site_url": "https://nambei-oyaji.com",
        "get_url": lambda row: f"https://nambei-oyaji.com/{row['パーマリンク']}/" if row.get("パーマリンク") else None,
        "is_published": lambda row: row.get("ステータス", "").strip() == "公開済",
    },
    {
        "name": "otona-match.com",
        "csv": os.path.join(BASE, "otona-match.com", "outputs", "article-management.csv"),
        "site_url": "https://otona-match.com",
        "get_url": lambda row: row.get("wp_url", "").strip() or (f"https://otona-match.com/{row['slug']}/" if row.get("slug") else None),
        "is_published": lambda row: row.get("status", "").strip() == "publish",
    },
    {
        "name": "sim-hikaku.online",
        "csv": os.path.join(BASE, "sim-hikaku.online", "outputs", "article-management.csv"),
        "site_url": "https://sim-hikaku.online",
        "get_url": lambda row: row.get("WordPress URL", "").strip() or (f"https://sim-hikaku.online/{row.get('ファイル名', '')}/" if row.get("ファイル名") else None),
        "is_published": lambda row: row.get("ステータス", "").strip() == "公開済",
    },
]


def main():
    # 認証
    credentials = service_account.Credentials.from_service_account_file(
        CREDENTIALS_FILE, scopes=SCOPES
    )
    session = AuthorizedSession(credentials)

    print(f"=== GSC Indexing API 一括申請 ===")
    print(f"開始: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()

    total_success = 0
    total_error = 0

    for site in SITES:
        print(f"--- {site['name']} ---")

        if not os.path.exists(site["csv"]):
            print(f"  CSV not found: {site['csv']}")
            continue

        urls = []
        with open(site["csv"], "r", encoding="utf-8-sig") as f:
            reader = csv.DictReader(f)
            for row in reader:
                if site["is_published"](row):
                    url = site["get_url"](row)
                    if url and url.startswith("http"):
                        urls.append(url)

        print(f"  公開済み記事: {len(urls)}件")

        for url in urls:
            payload = {
                "url": url,
                "type": "URL_UPDATED"
            }
            try:
                resp = session.post(API_URL, json=payload)
                if resp.status_code == 200:
                    data = resp.json()
                    print(f"  OK: {url} -> notifyTime: {data.get('urlNotificationMetadata', {}).get('latestUpdate', {}).get('notifyTime', 'N/A')}")
                    total_success += 1
                else:
                    print(f"  ERROR [{resp.status_code}]: {url} -> {resp.text[:200]}")
                    total_error += 1
            except Exception as e:
                print(f"  EXCEPTION: {url} -> {e}")
                total_error += 1

            time.sleep(1)  # rate limit対策

        print()

    print(f"=== 完了 ===")
    print(f"成功: {total_success}, エラー: {total_error}")
    print(f"終了: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")


if __name__ == "__main__":
    main()
