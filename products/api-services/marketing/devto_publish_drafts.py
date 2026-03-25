"""Dev.to 下書き記事の予約公開スクリプト

実行日に応じて該当記事を公開する。
Task Schedulerで毎日1回実行する想定。
"""

import json
import sys
from datetime import date
from pathlib import Path

import requests

# Configuration
CONFIG_PATH = Path(__file__).parent / "dev-to-config.json"

# Schedule: {公開日: 記事ID}
PUBLISH_SCHEDULE = {
    date(2026, 3, 25): 3397563,
    date(2026, 3, 26): 3397564,
}


def load_api_key() -> str:
    """dev-to-config.json から API キーを読み込む"""
    if not CONFIG_PATH.exists():
        print(f"[エラー] 設定ファイルが見つかりません: {CONFIG_PATH}")
        sys.exit(1)
    with open(CONFIG_PATH, encoding="utf-8") as f:
        config = json.load(f)
    api_key = config.get("api_key", "")
    if not api_key:
        print("[エラー] api_key が設定ファイルに含まれていません")
        sys.exit(1)
    return api_key


def publish_article(api_key: str, article_id: int) -> bool:
    """Dev.to API で記事を公開する"""
    url = f"https://dev.to/api/articles/{article_id}"
    headers = {
        "api-key": api_key,
        "Content-Type": "application/json",
    }
    payload = {"article": {"published": True}}

    try:
        resp = requests.put(url, headers=headers, json=payload, timeout=30)
        if resp.status_code == 200:
            data = resp.json()
            print(f"[成功] 記事ID {article_id} を公開しました: {data.get('url', '')}")
            return True
        else:
            print(f"[エラー] 記事ID {article_id} の公開に失敗 (HTTP {resp.status_code}): {resp.text}")
            return False
    except requests.RequestException as e:
        print(f"[エラー] 記事ID {article_id} のAPI呼び出しに失敗: {e}")
        return False


def main():
    today = date.today()
    print(f"[情報] 実行日: {today}")

    article_id = PUBLISH_SCHEDULE.get(today)
    if article_id is None:
        print("[情報] 本日公開予定の記事はありません")
        return

    api_key = load_api_key()
    publish_article(api_key, article_id)


if __name__ == "__main__":
    main()
