"""
Google Indexing API - otona-match.com 未インデックスURL送信
indexing-pending-urls.json から読み込んで送信する
"""

import json
import os
import sys
import time
from datetime import datetime

from google.auth.transport.requests import AuthorizedSession
from google.oauth2 import service_account

SITE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
CREDENTIALS_FILE = os.path.join(SITE_DIR, "config", "gsc-credentials.json")
PENDING_FILE = os.path.join(SITE_DIR, "outputs", "indexing-pending-urls.json")
SCOPES = ["https://www.googleapis.com/auth/indexing"]
API_URL = "https://indexing.googleapis.com/v3/urlNotifications:publish"

LOG_DIR = os.path.join(
    os.path.dirname(os.path.dirname(os.path.dirname(SITE_DIR))),
    "logs",
    "seo",
)


def main() -> None:
    if not os.path.exists(CREDENTIALS_FILE):
        print(f"ERROR: 認証ファイルが見つかりません: {CREDENTIALS_FILE}")
        sys.exit(1)

    if not os.path.exists(PENDING_FILE):
        print(f"ERROR: ペンディングURLファイルが見つかりません: {PENDING_FILE}")
        sys.exit(1)

    with open(PENDING_FILE, "r", encoding="utf-8") as f:
        data = json.load(f)

    urls: list[str] = data.get("urls", [])
    print(f"=== GSC Indexing API - otona-match.com (pending) ===")
    print(f"開始: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"対象URL: {len(urls)}件")
    print()

    credentials = service_account.Credentials.from_service_account_file(
        CREDENTIALS_FILE, scopes=SCOPES
    )
    session = AuthorizedSession(credentials)

    success_count = 0
    error_count = 0
    quota_hit = False
    failed_urls: list[str] = []

    for i, url in enumerate(urls, 1):
        payload = {"url": url, "type": "URL_UPDATED"}
        try:
            resp = session.post(API_URL, json=payload)
            if resp.status_code == 200:
                notify_time = (
                    resp.json()
                    .get("urlNotificationMetadata", {})
                    .get("latestUpdate", {})
                    .get("notifyTime", "N/A")
                )
                print(f"  [{i}/{len(urls)}] OK: {url}")
                success_count += 1
            elif resp.status_code == 429:
                print(f"  [{i}/{len(urls)}] QUOTA EXCEEDED: {url}")
                quota_hit = True
                failed_urls.append(url)
                # Add remaining URLs to failed list
                failed_urls.extend(urls[i:])
                error_count += len(urls) - i + 1
                break
            else:
                print(f"  [{i}/{len(urls)}] ERROR [{resp.status_code}]: {url} -> {resp.text[:200]}")
                error_count += 1
                failed_urls.append(url)
        except Exception as e:
            print(f"  [{i}/{len(urls)}] EXCEPTION: {url} -> {e}")
            error_count += 1
            failed_urls.append(url)

        time.sleep(1)

    print()
    print(f"=== 完了 ===")
    print(f"成功: {success_count}, エラー: {error_count}")
    if quota_hit:
        print(f"クォータ到達 - 残り{len(failed_urls)}件は明日送信が必要")
    print(f"終了: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

    # ログ保存
    os.makedirs(LOG_DIR, exist_ok=True)
    today = datetime.now().strftime("%Y-%m-%d")
    log_path = os.path.join(LOG_DIR, f"indexing-api-otona-{today}.md")
    with open(log_path, "w", encoding="utf-8") as f:
        f.write(f"# Indexing API - otona-match.com ({today})\n\n")
        f.write(f"- 対象: {len(urls)}件\n")
        f.write(f"- 成功: {success_count}件\n")
        f.write(f"- エラー: {error_count}件\n")
        f.write(f"- クォータ到達: {'はい' if quota_hit else 'いいえ'}\n")
        if failed_urls:
            f.write(f"\n## 未送信URL ({len(failed_urls)}件)\n\n")
            for u in failed_urls:
                f.write(f"- {u}\n")
    print(f"\nログ保存: {log_path}")

    # 未送信URLがあれば別ファイルに保存
    if failed_urls:
        retry_path = os.path.join(SITE_DIR, "outputs", "indexing-retry-urls.json")
        with open(retry_path, "w", encoding="utf-8") as f:
            json.dump(
                {
                    "saved_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    "count": len(failed_urls),
                    "domain": "otona-match.com",
                    "urls": failed_urls,
                },
                f,
                ensure_ascii=False,
                indent=2,
            )
        print(f"リトライ用ファイル保存: {retry_path}")


if __name__ == "__main__":
    main()
