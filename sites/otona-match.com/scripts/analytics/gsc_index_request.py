"""
Google Search Console Indexing API - otona-match.com インデックス登録申請
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
SITE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
CREDENTIALS_FILE = os.path.join(SITE_DIR, "config", "gsc-credentials.json")
SCOPES = ["https://www.googleapis.com/auth/indexing"]
API_URL = "https://indexing.googleapis.com/v3/urlNotifications:publish"

# サイト設定
SITE_NAME = "otona-match.com"
SITE_URL = "https://otona-match.com"
CSV_PATH = os.path.join(SITE_DIR, "outputs", "article-management.csv")
LOG_DIR = os.path.join(
    os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(SITE_DIR)))),
    "logs",
)


def get_url(row):
    """CSVの行からURLを取得"""
    wp_url = row.get("wp_url", "").strip()
    if wp_url:
        return wp_url
    slug = row.get("slug", "").strip()
    if slug:
        return f"{SITE_URL}/{slug}/"
    return None


def is_published(row):
    """公開済みかどうかを判定"""
    return row.get("status", "").strip() == "publish"


def main():
    # 認証ファイル存在チェック
    if not os.path.exists(CREDENTIALS_FILE):
        print(f"ERROR: 認証ファイルが見つかりません: {CREDENTIALS_FILE}")
        print("gsc-credentials.json を config/ に配置してください。")
        return

    # 認証
    credentials = service_account.Credentials.from_service_account_file(
        CREDENTIALS_FILE, scopes=SCOPES
    )
    session = AuthorizedSession(credentials)

    print(f"=== GSC Indexing API - {SITE_NAME} ===")
    print(f"開始: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()

    if not os.path.exists(CSV_PATH):
        print(f"ERROR: CSV not found: {CSV_PATH}")
        return

    # 公開済み記事のURL一覧を取得
    urls = []
    with open(CSV_PATH, "r", encoding="utf-8-sig") as f:
        reader = csv.DictReader(f)
        for row in reader:
            if is_published(row):
                url = get_url(row)
                if url and url.startswith("http"):
                    urls.append(url)

    # トップページも追加
    urls.insert(0, SITE_URL + "/")

    print(f"対象URL: {len(urls)}件（トップページ含む）")
    print()

    success_count = 0
    error_count = 0

    for url in urls:
        payload = {"url": url, "type": "URL_UPDATED"}
        try:
            resp = session.post(API_URL, json=payload)
            if resp.status_code == 200:
                data = resp.json()
                notify_time = (
                    data.get("urlNotificationMetadata", {})
                    .get("latestUpdate", {})
                    .get("notifyTime", "N/A")
                )
                print(f"  OK: {url} -> notifyTime: {notify_time}")
                success_count += 1
            else:
                print(f"  ERROR [{resp.status_code}]: {url} -> {resp.text[:200]}")
                error_count += 1
        except Exception as e:
            print(f"  EXCEPTION: {url} -> {e}")
            error_count += 1

        time.sleep(1)  # rate limit対策

    print()
    print(f"=== 完了 ===")
    print(f"成功: {success_count}, エラー: {error_count}")
    print(f"終了: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")


if __name__ == "__main__":
    main()
