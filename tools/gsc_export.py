#!/usr/bin/env python3
"""
Google Search Console — 3サイト一括ページ別パフォーマンスCSVエクスポート

各サイトの inputs/gsc-performance.csv に以下を出力:
  page, clicks, impressions, ctr, position, query_top3, date_from, date_to

実行:
  python tools/gsc_export.py              # デフォルト: 過去28日
  python tools/gsc_export.py --days 7     # 過去7日
  python tools/gsc_export.py --days 90    # 過去90日
"""

import csv
import json
import sys
import os
from datetime import datetime, timedelta
from pathlib import Path

if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")

# ── 定数 ──────────────────────────────────────
BASE_DIR = Path(__file__).resolve().parent.parent.parent  # claude-code/

SITES = [
    {"key": "nambei", "dir": "sites/nambei-oyaji.com"},
    {"key": "otona", "dir": "sites/otona-match.com"},
    {"key": "sim", "dir": "sites/sim-hikaku.online"},
]

CSV_HEADERS = [
    "page",
    "clicks",
    "impressions",
    "ctr",
    "position",
    "query_top3",
    "date_from",
    "date_to",
]


def load_site_config(site_dir: Path):
    """settings.json から search_console 設定を読み込む"""
    settings_path = site_dir / "config" / "settings.json"
    if not settings_path.exists():
        return None, None

    with open(settings_path, encoding="utf-8") as f:
        settings = json.load(f)

    sc = settings.get("search_console", {})
    site_url = sc.get("site_url", "")
    cred_filename = sc.get("credentials_file", "gsc-credentials.json")

    # credentials_file がパス区切りを含む場合はプロジェクトルート相対
    if "/" in cred_filename or "\\" in cred_filename:
        cred_path = site_dir / cred_filename
    else:
        cred_path = site_dir / "config" / cred_filename

    if not site_url or not cred_path.exists():
        return None, None

    return site_url, cred_path


def fetch_page_data(site_url, cred_path, start_date, end_date):
    """GSC API からページ別パフォーマンスを取得（全ページ）"""
    from google.oauth2 import service_account
    from googleapiclient.discovery import build

    credentials = service_account.Credentials.from_service_account_file(
        str(cred_path),
        scopes=["https://www.googleapis.com/auth/webmasters.readonly"],
    )
    service = build("searchconsole", "v1", credentials=credentials)

    start_str = start_date.strftime("%Y-%m-%d")
    end_str = end_date.strftime("%Y-%m-%d")

    # ページ別データ（最大1000行）
    page_response = (
        service.searchanalytics()
        .query(
            siteUrl=site_url,
            body={
                "startDate": start_str,
                "endDate": end_str,
                "dimensions": ["page"],
                "rowLimit": 1000,
            },
        )
        .execute()
    )

    pages = {}
    for row in page_response.get("rows", []):
        url = row["keys"][0]
        pages[url] = {
            "clicks": row.get("clicks", 0),
            "impressions": row.get("impressions", 0),
            "ctr": round(row.get("ctr", 0) * 100, 2),
            "position": round(row.get("position", 0), 1),
        }

    # ページ×クエリ（上位クエリ紐付け用、最大5000行）
    pq_response = (
        service.searchanalytics()
        .query(
            siteUrl=site_url,
            body={
                "startDate": start_str,
                "endDate": end_str,
                "dimensions": ["page", "query"],
                "rowLimit": 5000,
            },
        )
        .execute()
    )

    # ページごとに上位3クエリを集約
    page_queries = {}
    for row in pq_response.get("rows", []):
        url = row["keys"][0]
        query = row["keys"][1]
        impressions = row.get("impressions", 0)
        if url not in page_queries:
            page_queries[url] = []
        page_queries[url].append((query, impressions))

    # 表示回数順でソートして上位3つ
    for url in page_queries:
        page_queries[url].sort(key=lambda x: x[1], reverse=True)
        page_queries[url] = [q for q, _ in page_queries[url][:3]]

    # 結合
    results = []
    for url, data in sorted(pages.items(), key=lambda x: x[1]["impressions"], reverse=True):
        results.append(
            {
                "page": url,
                "clicks": data["clicks"],
                "impressions": data["impressions"],
                "ctr": data["ctr"],
                "position": data["position"],
                "query_top3": " | ".join(page_queries.get(url, [])),
                "date_from": start_str,
                "date_to": end_str,
            }
        )

    return results


def export_site(site_dir: Path, start_date, end_date):
    """1サイト分のGSCデータをCSVエクスポート"""
    site_url, cred_path = load_site_config(site_dir)
    if not site_url:
        print(f"  [SKIP] {site_dir.name}: GSC設定なし or 認証ファイルなし")
        return False

    print(f"  [FETCH] {site_url} ...")
    try:
        rows = fetch_page_data(site_url, cred_path, start_date, end_date)
    except Exception as e:
        print(f"  [ERROR] {site_dir.name}: {e}")
        return False

    # 出力
    output_path = site_dir / "inputs" / "gsc-performance.csv"
    output_path.parent.mkdir(parents=True, exist_ok=True)

    with open(output_path, "w", newline="", encoding="utf-8-sig") as f:
        writer = csv.DictWriter(f, fieldnames=CSV_HEADERS)
        writer.writeheader()
        writer.writerows(rows)

    print(f"  [OK] {output_path} ({len(rows)} pages)")
    return True


def main():
    import argparse

    parser = argparse.ArgumentParser(description="GSC Performance CSV Export (3 sites)")
    parser.add_argument("--days", type=int, default=28, help="過去何日分 (default: 28)")
    args = parser.parse_args()

    end_date = datetime.now().date() - timedelta(days=3)  # GSCは3日前まで確定
    start_date = end_date - timedelta(days=args.days - 1)

    print(f"GSC Export: {start_date} ~ {end_date} ({args.days}日間)")
    print("=" * 60)

    success_count = 0
    for site in SITES:
        site_dir = BASE_DIR / site["dir"]
        print(f"\n[{site['key']}] {site['dir']}")
        if export_site(site_dir, start_date, end_date):
            success_count += 1

    print(f"\n{'=' * 60}")
    print(f"完了: {success_count}/{len(SITES)} サイト")


if __name__ == "__main__":
    main()
