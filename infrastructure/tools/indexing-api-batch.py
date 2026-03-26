"""
Google Indexing API 一括送信スクリプト（3サイト統合版）

日次クォータ200リクエストを3サイトで効率分配。
pending fileがあるサイトを優先的に処理する。

Usage:
    python indexing-api-batch.py                  # 全サイト（pending優先）
    python indexing-api-batch.py sim-hikaku        # sim-hikakuのみ
    python indexing-api-batch.py --quota 200       # クォータ上限指定
"""

import csv
import json
import os
import sys
import time
from datetime import datetime
from google.oauth2 import service_account
from google.auth.transport.requests import AuthorizedSession

BASE_DIR = os.path.join(
    os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))),
)
# Should resolve to claude-code/

SITES = {
    "sim-hikaku": {
        "name": "sim-hikaku.online",
        "url": "https://sim-hikaku.online",
        "dir": os.path.join(BASE_DIR, "sites", "sim-hikaku.online"),
    },
    "nambei-oyaji": {
        "name": "nambei-oyaji.com",
        "url": "https://nambei-oyaji.com",
        "dir": os.path.join(BASE_DIR, "sites", "nambei-oyaji.com"),
    },
    "otona-match": {
        "name": "otona-match.com",
        "url": "https://otona-match.com",
        "dir": os.path.join(BASE_DIR, "sites", "otona-match.com"),
    },
}

SCOPES = ["https://www.googleapis.com/auth/indexing"]
API_URL = "https://indexing.googleapis.com/v3/urlNotifications:publish"
DAILY_QUOTA = 200


def load_urls(site_config):
    """サイトのURL一覧を取得（pending優先）"""
    site_dir = site_config["dir"]
    pending_file = os.path.join(site_dir, "outputs", "indexing-pending-urls.json")
    csv_path = os.path.join(site_dir, "outputs", "article-management.csv")

    # pending fileがあればそちらを使用
    if os.path.exists(pending_file):
        with open(pending_file, "r", encoding="utf-8") as f:
            data = json.load(f)
        return data["urls"], pending_file, True

    # CSVから取得
    if not os.path.exists(csv_path):
        return [], None, False

    seen = set()
    urls = []
    with open(csv_path, "r", encoding="utf-8-sig") as f:
        reader = csv.DictReader(f)
        for row in reader:
            if row.get("ステータス", "").strip() == "公開済":
                wp_url = row.get("WordPress URL", "").strip()
                filename = row.get("ファイル名", "").strip()
                url = wp_url if wp_url else (
                    f"{site_config['url']}/{filename}/" if filename else None
                )
                if url and url.startswith("http") and url not in seen:
                    seen.add(url)
                    urls.append(url)

    top = site_config["url"] + "/"
    if top not in seen:
        urls.insert(0, top)

    return urls, None, False


def save_pending(site_dir, remaining_urls):
    """未送信URLを保存"""
    pending_file = os.path.join(site_dir, "outputs", "indexing-pending-urls.json")
    data = {
        "saved_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "count": len(remaining_urls),
        "urls": remaining_urls,
    }
    with open(pending_file, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def clear_pending(site_dir):
    """pending file削除"""
    pending_file = os.path.join(site_dir, "outputs", "indexing-pending-urls.json")
    if os.path.exists(pending_file):
        os.remove(pending_file)


def main():
    # 引数解析
    target_site = None
    quota = DAILY_QUOTA

    args = sys.argv[1:]
    for i, arg in enumerate(args):
        if arg == "--quota" and i + 1 < len(args):
            quota = int(args[i + 1])
        elif arg in SITES:
            target_site = arg

    # 認証（全サイト共通のサービスアカウント）
    creds_file = os.path.join(
        SITES["sim-hikaku"]["dir"], "config", "gsc-credentials.json"
    )
    if not os.path.exists(creds_file):
        print(f"ERROR: 認証ファイルが見つかりません: {creds_file}")
        return

    credentials = service_account.Credentials.from_service_account_file(
        creds_file, scopes=SCOPES
    )
    session = AuthorizedSession(credentials)

    print(f"=== Indexing API Batch - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} ===")
    print(f"クォータ上限: {quota}")
    print()

    # 処理対象サイトを決定（pending優先でソート）
    site_keys = [target_site] if target_site else list(SITES.keys())
    site_queue = []
    for key in site_keys:
        config = SITES[key]
        urls, pending_file, is_pending = load_urls(config)
        if urls:
            site_queue.append({
                "key": key,
                "config": config,
                "urls": urls,
                "is_pending": is_pending,
            })

    # pending優先でソート
    site_queue.sort(key=lambda x: (not x["is_pending"], -len(x["urls"])))

    total_sent = 0
    total_success = 0
    total_error = 0

    for site_info in site_queue:
        if total_sent >= quota:
            break

        key = site_info["key"]
        config = site_info["config"]
        urls = site_info["urls"]
        remaining_quota = quota - total_sent

        print(f"--- {config['name']} ({len(urls)} URLs, pending={site_info['is_pending']}) ---")

        success = 0
        errors = 0
        quota_hit = False

        for i, url in enumerate(urls):
            if total_sent >= quota:
                remaining = urls[i:]
                save_pending(config["dir"], remaining)
                print(f"  クォータ上限到達。残り{len(remaining)}件を保存")
                quota_hit = True
                break

            payload = {"url": url, "type": "URL_UPDATED"}
            try:
                resp = session.post(API_URL, json=payload)
                if resp.status_code == 200:
                    print(f"  OK [{i+1}/{len(urls)}]: {url}")
                    success += 1
                elif resp.status_code == 429:
                    remaining = urls[i:]
                    save_pending(config["dir"], remaining)
                    print(f"  QUOTA EXCEEDED. 残り{len(remaining)}件を保存")
                    quota_hit = True
                    break
                else:
                    print(f"  ERROR [{resp.status_code}]: {url}")
                    errors += 1
            except Exception as e:
                print(f"  EXCEPTION: {url} -> {e}")
                errors += 1

            total_sent += 1
            time.sleep(1)

        if not quota_hit:
            clear_pending(config["dir"])

        total_success += success
        total_error += errors
        print(f"  結果: 成功={success}, エラー={errors}")
        print()

    print(f"=== 全体結果 ===")
    print(f"送信: {total_sent}, 成功: {total_success}, エラー: {total_error}")
    print(f"終了: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")


if __name__ == "__main__":
    main()
