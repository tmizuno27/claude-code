#!/usr/bin/env python3
"""
記事管理CSVの累計PV列をGA4 Data APIから取得して更新するスクリプト。
毎朝5:00 PYTにTask Schedulerから自動実行される。

使い方:
  python update_pv.py          # PV更新 + Google Sheets同期
  python update_pv.py --no-sheets  # PV更新のみ（Sheets同期なし）
"""
import argparse
import csv
import json
import os
import sys
import time
from datetime import datetime
from pathlib import Path
from urllib.parse import unquote

# パス設定
SCRIPT_DIR = Path(__file__).parent
PROJECT_ROOT = SCRIPT_DIR.parent.parent
CSV_PATH = PROJECT_ROOT / "outputs" / "article-management.csv"
SECRETS_PATH = PROJECT_ROOT / "config" / "secrets.json"
GA4_CREDS_PATH = PROJECT_ROOT / "config" / "ga4-credentials.json"
LOG_PATH = PROJECT_ROOT / "outputs" / "update-pv.log"

def log(msg):
    ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    line = f"[{ts}] {msg}"
    print(line)
    for attempt in range(3):
        try:
            with open(LOG_PATH, "a", encoding="utf-8") as f:
                f.write(line + "\n")
            return
        except PermissionError:
            if attempt < 2:
                time.sleep(1)
    # ログ書き込み失敗は無視して処理を継続
    print(f"[WARNING] Could not write to log file: {LOG_PATH}")


def fetch_pv():
    """GA4から全期間の記事別PVを取得"""
    from google.analytics.data_v1beta import BetaAnalyticsDataClient
    from google.analytics.data_v1beta.types import RunReportRequest, DateRange, Dimension, Metric
    from google.oauth2.service_account import Credentials

    with open(SECRETS_PATH, encoding="utf-8") as f:
        secrets = json.load(f)

    property_id = secrets["ga4"]["property_id"]
    creds = Credentials.from_service_account_file(
        str(GA4_CREDS_PATH),
        scopes=["https://www.googleapis.com/auth/analytics.readonly"]
    )
    client = BetaAnalyticsDataClient(credentials=creds)

    response = client.run_report(RunReportRequest(
        property=f"properties/{property_id}",
        date_ranges=[DateRange(start_date="2020-01-01", end_date="today")],
        dimensions=[Dimension(name="pagePath")],
        metrics=[Metric(name="screenPageViews")],
        limit=200,
    ))

    # パスからスラッグ→PVマップ作成
    pv_map = {}
    for row in response.rows:
        path = unquote(row.dimension_values[0].value).strip("/")
        slug = path.split("/")[0] if "/" in path else path
        skip = ("category", "about", "contact", "privacy-policy", "sitemap", "")
        if slug not in skip:
            pv_map[slug] = pv_map.get(slug, 0) + int(row.metric_values[0].value)

    return pv_map


def build_slug_mapping(rows):
    """旧スラッグ（GA4記録）→ 現在のパーマリンクのマッピングを構築"""
    # 既知の旧→新マッピング
    old_to_new = {
        "paraguay-kikou": "paraguay-climate-weather",
        "paraguay-ijuu-hiyou": "paraguay-immigration-cost",
        "paraguay-seikatsuhi": "paraguay-living-cost",
        "paraguay-chian": "paraguay-safety-security",
        "kaigai-kosodate": "moving-abroad-with-kids",
        "kaigai-ijuu-hatarakikata": "working-after-moving-abroad",
        "kaigai-soukin-hikaku": "international-money-transfer-comparison",
    }
    # 現在のパーマリンクもそのまま自分自身にマッピング
    for row in rows[1:]:
        permalink = row[14] if len(row) > 14 else ""
        if permalink:
            old_to_new[permalink] = permalink
    return old_to_new


def update_csv(pv_map):
    """CSVの累計PV列（index 15）を更新"""
    with open(CSV_PATH, "r", encoding="utf-8") as f:
        rows = list(csv.reader(f))

    if not rows:
        log("ERROR: CSV is empty")
        return rows

    # ヘッダー確認
    header = rows[0]
    try:
        pv_col = header.index("累計PV")
    except ValueError:
        log("ERROR: 累計PV column not found in CSV header")
        return rows

    permalink_col = header.index("パーマリンク")
    slug_map = build_slug_mapping(rows)

    # 新パーマリンク→PV変換
    permalink_pv = {}
    for old_slug, pv in pv_map.items():
        new_slug = slug_map.get(old_slug, old_slug)
        permalink_pv[new_slug] = permalink_pv.get(new_slug, 0) + pv

    # 日本語スラッグ（食文化等）の特別処理
    for slug, pv in pv_map.items():
        if any(c > "\u007f" for c in slug):
            # 日本語を含むスラッグは食文化記事の可能性
            if "食文化" in slug or "アサード" in slug:
                permalink_pv["paraguay-food-culture"] = permalink_pv.get("paraguay-food-culture", 0) + pv

    updated = 0
    total_pv = 0
    for row in rows[1:]:
        permalink = row[permalink_col] if len(row) > permalink_col else ""
        pv = permalink_pv.get(permalink, 0)
        # 列数が足りない場合は拡張
        while len(row) <= pv_col:
            row.append("")
        row[pv_col] = str(pv) if pv > 0 else ""
        if pv > 0:
            updated += 1
            total_pv += pv

    with open(CSV_PATH, "w", encoding="utf-8", newline="") as f:
        writer = csv.writer(f)
        writer.writerows(rows)

    log(f"CSV updated: {updated} articles with PV, total {total_pv} PV")
    return rows


def sync_sheets():
    """Google Sheetsに同期（3サイト統合スクリプト経由）"""
    import subprocess
    unified_script = PROJECT_ROOT.parent / "tools" / "update_all_sheets.py"
    if unified_script.exists():
        result = subprocess.run(
            [sys.executable, str(unified_script), "--site", "nambei"],
            capture_output=True, text=True, encoding="utf-8", errors="replace"
        )
        log(f"Unified sheets sync (nambei): exit={result.returncode}")
        if result.stdout:
            for line in result.stdout.strip().split("\n")[-3:]:
                log(f"  {line}")
    else:
        # フォールバック: 旧スクリプト
        sys.path.insert(0, str(SCRIPT_DIR))
        from create_article_sheet import main as sheet_main
        sheet_main()
    log("Google Sheets synced")


def main():
    parser = argparse.ArgumentParser(description="Update article PV from GA4")
    parser.add_argument("--no-sheets", action="store_true", help="Skip Google Sheets sync")
    args = parser.parse_args()

    log("=== PV Update Start ===")

    try:
        pv_map = fetch_pv()
        log(f"GA4: {len(pv_map)} slugs fetched")
        update_csv(pv_map)
        if not args.no_sheets:
            sync_sheets()
    except Exception as e:
        log(f"ERROR: {e}")
        raise

    log("=== PV Update Complete ===")


if __name__ == "__main__":
    main()
