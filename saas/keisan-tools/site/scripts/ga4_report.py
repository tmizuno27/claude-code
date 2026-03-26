#!/usr/bin/env python3
"""
keisan-tools.com GA4 データ取得スクリプト

GA4 Data API (REST) でPV・セッション・ユーザー数・人気ページを取得する。
認証: config/ga4-credentials.json（サービスアカウント）
プロパティID: 529807198 (Measurement ID: G-3R1LVHX9VJ)
"""

import json
import logging
import sys
from datetime import datetime, timedelta
from pathlib import Path

import requests
from google.oauth2 import service_account
import google.auth.transport.requests

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)

SCRIPT_DIR = Path(__file__).parent
PROJECT_ROOT = SCRIPT_DIR.parent
CONFIG_DIR = PROJECT_ROOT / "config"
CREDENTIALS_FILE = CONFIG_DIR / "ga4-credentials.json"

GA4_PROPERTY_ID = "529807198"
GA4_API_URL = f"https://analyticsdata.googleapis.com/v1beta/properties/{GA4_PROPERTY_ID}:runReport"

SCOPES = ["https://www.googleapis.com/auth/analytics.readonly"]


def get_access_token():
    """サービスアカウントからアクセストークンを取得"""
    creds = service_account.Credentials.from_service_account_file(
        str(CREDENTIALS_FILE), scopes=SCOPES
    )
    creds.refresh(google.auth.transport.requests.Request())
    return creds.token


def run_report(token, start_date, end_date, metrics, dimensions=None):
    """GA4 Data API でレポートを実行"""
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
    }
    body = {
        "dateRanges": [{"startDate": start_date, "endDate": end_date}],
        "metrics": [{"name": m} for m in metrics],
    }
    if dimensions:
        body["dimensions"] = [{"name": d} for d in dimensions]

    resp = requests.post(GA4_API_URL, headers=headers, json=body, timeout=15)
    resp.raise_for_status()
    return resp.json()


def fetch_overview(token, days=7):
    """直近N日間のサマリーを取得"""
    end = datetime.now().strftime("%Y-%m-%d")
    start = (datetime.now() - timedelta(days=days)).strftime("%Y-%m-%d")

    data = run_report(
        token, start, end,
        metrics=["sessions", "screenPageViews", "activeUsers"],
    )
    if "rows" not in data:
        return {"sessions": 0, "pageviews": 0, "users": 0}

    row = data["rows"][0]["metricValues"]
    return {
        "sessions": int(row[0]["value"]),
        "pageviews": int(row[1]["value"]),
        "users": int(row[2]["value"]),
    }


def fetch_top_pages(token, days=7, limit=10):
    """人気ページ上位を取得"""
    end = datetime.now().strftime("%Y-%m-%d")
    start = (datetime.now() - timedelta(days=days)).strftime("%Y-%m-%d")

    data = run_report(
        token, start, end,
        metrics=["screenPageViews"],
        dimensions=["pagePath"],
    )
    if "rows" not in data:
        return []

    pages = []
    for row in data["rows"][:limit]:
        pages.append({
            "path": row["dimensionValues"][0]["value"],
            "pageviews": int(row["metricValues"][0]["value"]),
        })
    return sorted(pages, key=lambda x: x["pageviews"], reverse=True)


def main():
    """メイン実行"""
    days = int(sys.argv[1]) if len(sys.argv) > 1 else 7

    logger.info("keisan-tools.com GA4レポート取得開始（過去%d日間）", days)

    if not CREDENTIALS_FILE.exists():
        logger.error("認証ファイルが見つかりません: %s", CREDENTIALS_FILE)
        sys.exit(1)

    token = get_access_token()
    logger.info("認証成功")

    overview = fetch_overview(token, days)
    top_pages = fetch_top_pages(token, days)

    print(f"\n=== keisan-tools.com GA4レポート（過去{days}日間） ===")
    print(f"セッション: {overview['sessions']}")
    print(f"ページビュー: {overview['pageviews']}")
    print(f"ユーザー: {overview['users']}")

    if top_pages:
        print(f"\n--- 人気ページ TOP {len(top_pages)} ---")
        for i, page in enumerate(top_pages, 1):
            print(f"  {i}. {page['path']} ({page['pageviews']} PV)")
    else:
        print("\nページ別データなし（まだアクセスが少ない可能性）")

    # JSON出力も保存
    report = {
        "generated_at": datetime.now().isoformat(),
        "period_days": days,
        "property_id": GA4_PROPERTY_ID,
        "overview": overview,
        "top_pages": top_pages,
    }
    report_path = PROJECT_ROOT / "scripts" / "ga4_report_latest.json"
    with open(report_path, "w", encoding="utf-8") as f:
        json.dump(report, f, ensure_ascii=False, indent=2)
    logger.info("レポートJSON保存: %s", report_path)


if __name__ == "__main__":
    main()
