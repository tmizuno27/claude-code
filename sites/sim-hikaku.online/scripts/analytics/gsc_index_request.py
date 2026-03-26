"""
Google Search Console Indexing API - sim-hikaku.online インデックス登録申請
全公開記事のURLをURL_UPDATEDとして通知する

機能:
- 429エラー（クォータ超過）時に未送信URLをpending fileに保存して中断
- 再実行時にpending fileがあれば続きから送信
- URL重複除去
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
SITE_NAME = "sim-hikaku.online"
SITE_URL = "https://sim-hikaku.online"
CSV_PATH = os.path.join(SITE_DIR, "outputs", "article-management.csv")
PENDING_FILE = os.path.join(SITE_DIR, "outputs", "indexing-pending-urls.json")
LOG_DIR = os.path.join(
    os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(SITE_DIR)))),
    "logs",
)


def get_url(row):
    """CSVの行からURLを取得"""
    wp_url = row.get("WordPress URL", "").strip()
    if wp_url:
        return wp_url
    filename = row.get("ファイル名", "").strip()
    if filename:
        return f"{SITE_URL}/{filename}/"
    return None


def is_published(row):
    """公開済みかどうかを判定"""
    return row.get("ステータス", "").strip() == "公開済"


def load_urls_from_csv():
    """CSVから公開済み記事のURL一覧を取得（重複除去）"""
    if not os.path.exists(CSV_PATH):
        print(f"ERROR: CSV not found: {CSV_PATH}")
        return []

    seen = set()
    urls = []
    with open(CSV_PATH, "r", encoding="utf-8-sig") as f:
        reader = csv.DictReader(f)
        for row in reader:
            if is_published(row):
                url = get_url(row)
                if url and url.startswith("http") and url not in seen:
                    seen.add(url)
                    urls.append(url)

    # トップページを先頭に追加
    top = SITE_URL + "/"
    if top not in seen:
        urls.insert(0, top)

    return urls


def load_pending_urls():
    """前回中断分のURL一覧を読み込み"""
    if os.path.exists(PENDING_FILE):
        with open(PENDING_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
        print(f"前回中断分を検出: {len(data['urls'])}件 (中断日時: {data.get('saved_at', 'N/A')})")
        return data["urls"]
    return None


def save_pending_urls(remaining_urls):
    """未送信URLを保存"""
    data = {
        "saved_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "count": len(remaining_urls),
        "urls": remaining_urls,
    }
    with open(PENDING_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print(f"未送信{len(remaining_urls)}件を {PENDING_FILE} に保存しました")


def clear_pending():
    """pending fileを削除"""
    if os.path.exists(PENDING_FILE):
        os.remove(PENDING_FILE)


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

    # pending fileがあれば続きから、なければCSVから全取得
    pending = load_pending_urls()
    if pending:
        urls = pending
        print(f"前回の続きから送信します")
    else:
        urls = load_urls_from_csv()
        if not urls:
            return

    print(f"対象URL: {len(urls)}件")
    print()

    success_count = 0
    error_count = 0
    quota_hit = False

    for i, url in enumerate(urls):
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
                print(f"  OK [{i+1}/{len(urls)}]: {url}")
                success_count += 1
            elif resp.status_code == 429:
                print(f"  QUOTA EXCEEDED at URL #{i+1}: {url}")
                remaining = urls[i:]
                save_pending_urls(remaining)
                quota_hit = True
                break
            else:
                print(f"  ERROR [{resp.status_code}]: {url} -> {resp.text[:200]}")
                error_count += 1
        except Exception as e:
            print(f"  EXCEPTION: {url} -> {e}")
            error_count += 1

        time.sleep(1)  # rate limit対策

    if not quota_hit:
        clear_pending()

    print()
    print(f"=== 完了 ===")
    print(f"成功: {success_count}, エラー: {error_count}")
    if quota_hit:
        print(f"クォータ超過により中断。残り{len(urls) - i}件は次回実行時に再送信されます。")
        print("Indexing APIの日次クォータはPST 0:00（PYT 3:00）にリセットされます。")
    print(f"終了: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")


if __name__ == "__main__":
    main()
