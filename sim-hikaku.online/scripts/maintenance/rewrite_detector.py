#!/usr/bin/env python3
"""記事リライト候補抽出 — PV低下+公開30日超の記事を自動検出
SIM比較オンライン (sim-hikaku.online) 版。

Usage:
    python rewrite_detector.py              # デフォルト（30日超+PV下位）
    python rewrite_detector.py --days 60    # 60日超の記事
    python rewrite_detector.py --top 10     # 上位10件表示
"""
import argparse
import csv
import io
import json
import logging
import sys
from datetime import datetime, timedelta
from pathlib import Path

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding="utf-8", errors="replace")

# --- Paths ---
SCRIPT_DIR = Path(__file__).parent
PROJECT_ROOT = SCRIPT_DIR.parent.parent
CONFIG_DIR = PROJECT_ROOT / "config"
OUTPUTS_DIR = PROJECT_ROOT / "outputs"
CSV_PATH = OUTPUTS_DIR / "article-management.csv"
REPORTS_DIR = OUTPUTS_DIR / "maintenance-reports"
LOG_FILE = OUTPUTS_DIR / "rewrite-detector.log"

REPORTS_DIR.mkdir(parents=True, exist_ok=True)
OUTPUTS_DIR.mkdir(parents=True, exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler(LOG_FILE, encoding="utf-8"),
    ],
)
logger = logging.getLogger(__name__)

try:
    import requests
except ImportError:
    requests = None


def load_secrets():
    path = CONFIG_DIR / "secrets.json"
    if not path.exists():
        return {}
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def load_csv_articles():
    """article-management.csv から記事データを読み込み"""
    if not CSV_PATH.exists():
        logger.error(f"CSVが見つかりません: {CSV_PATH}")
        return []
    articles = []
    with open(CSV_PATH, "r", encoding="utf-8-sig") as f:
        reader = csv.DictReader(f)
        for row in reader:
            articles.append(row)
    return articles


def fetch_ga4_page_data(secrets, days=30):
    """GA4から過去N日間の記事別PVを取得"""
    try:
        from google.analytics.data_v1beta import BetaAnalyticsDataClient
        from google.analytics.data_v1beta.types import (
            DateRange, Dimension, Metric, RunReportRequest,
        )
        from google.oauth2.service_account import Credentials
    except ImportError:
        logger.warning("google-analytics-data 未インストール。CSV PVデータのみ使用。")
        return {}

    ga4_creds_path = CONFIG_DIR / "ga4-credentials.json"
    if not ga4_creds_path.exists():
        logger.warning("ga4-credentials.json が見つかりません。CSV PVデータのみ使用。")
        return {}

    property_id = secrets.get("ga4", {}).get("property_id", "")
    if not property_id:
        return {}

    creds = Credentials.from_service_account_file(
        str(ga4_creds_path),
        scopes=["https://www.googleapis.com/auth/analytics.readonly"],
    )
    client = BetaAnalyticsDataClient(credentials=creds)

    end_date = datetime.now()
    start_date = end_date - timedelta(days=days)

    request = RunReportRequest(
        property=f"properties/{property_id}",
        date_ranges=[DateRange(
            start_date=start_date.strftime("%Y-%m-%d"),
            end_date=end_date.strftime("%Y-%m-%d"),
        )],
        dimensions=[Dimension(name="pagePath")],
        metrics=[Metric(name="screenPageViews")],
    )

    response = client.run_report(request)
    page_views = {}
    for row in response.rows:
        path = row.dimension_values[0].value
        pv = int(row.metric_values[0].value)
        page_views[path] = pv

    return page_views


def calculate_rewrite_score(article, recent_pv, days_since_publish):
    """リライト優先度スコア算出（高い=リライトすべき）"""
    score = 0

    if days_since_publish > 90:
        score += 30
    elif days_since_publish > 60:
        score += 20
    elif days_since_publish > 30:
        score += 10

    if recent_pv == 0:
        score += 40
    elif recent_pv < 10:
        score += 30
    elif recent_pv < 50:
        score += 20
    elif recent_pv < 100:
        score += 10

    word_count = int(article.get("文字数", "0") or "0")
    if word_count < 2000:
        score += 15
    elif word_count < 2500:
        score += 5

    internal_links = int(article.get("内部リンク数", "0") or "0")
    if internal_links == 0:
        score += 10
    elif internal_links < 3:
        score += 5

    return score


def send_discord_notification(secrets, summary):
    if not requests:
        return
    webhook_url = secrets.get("discord", {}).get("webhook_url", "")
    if not webhook_url or webhook_url.startswith("YOUR"):
        return
    payload = {
        "embeds": [{
            "title": "リライト候補レポート (sim-hikaku)",
            "description": summary,
            "color": 0xFFA500,
            "timestamp": datetime.utcnow().isoformat(),
        }]
    }
    try:
        requests.post(webhook_url, json=payload, timeout=10)
    except Exception as e:
        logger.warning(f"Discord通知失敗: {e}")


def main():
    parser = argparse.ArgumentParser(description="リライト候補抽出 (sim-hikaku.online)")
    parser.add_argument("--days", type=int, default=30, help="公開後N日超の記事を対象")
    parser.add_argument("--top", type=int, default=10, help="上位N件を表示")
    parser.add_argument("--no-discord", action="store_true")
    args = parser.parse_args()

    logger.info("========== リライト候補抽出 開始 (sim-hikaku.online) ==========")

    secrets = load_secrets()
    articles = load_csv_articles()

    if not articles:
        logger.error("記事データなし。終了。")
        return

    recent_pv_data = fetch_ga4_page_data(secrets, days=30)

    today = datetime.now()
    candidates = []

    for article in articles:
        status = article.get("ステータス", "")
        if status not in ("公開済み", "published"):
            continue

        pub_date_str = article.get("公開日", "")
        if not pub_date_str:
            continue

        try:
            pub_date = datetime.strptime(pub_date_str.strip(), "%Y-%m-%d")
        except ValueError:
            continue

        days_since = (today - pub_date).days
        if days_since < args.days:
            continue

        slug = article.get("ファイル名", "").replace(".md", "")
        recent_pv = recent_pv_data.get(f"/{slug}/", 0)
        if recent_pv == 0:
            recent_pv = int(article.get("累計PV", "0") or "0")

        score = calculate_rewrite_score(article, recent_pv, days_since)

        candidates.append({
            "title": article.get("タイトル", ""),
            "slug": slug,
            "published": pub_date_str,
            "days_since": days_since,
            "recent_pv": recent_pv,
            "word_count": article.get("文字数", "0"),
            "internal_links": article.get("内部リンク数", "0"),
            "score": score,
            "wp_url": article.get("WordPress URL", ""),
        })

    candidates.sort(key=lambda x: x["score"], reverse=True)
    top = candidates[: args.top]

    report_date = today.strftime("%Y-%m-%d")
    report_path = REPORTS_DIR / f"rewrite-candidates-{report_date}.json"
    report = {
        "date": report_date,
        "total_published": len([a for a in articles if a.get("ステータス") in ("公開済み", "published")]),
        "candidates_found": len(candidates),
        "top_candidates": top,
    }
    with open(report_path, "w", encoding="utf-8") as f:
        json.dump(report, f, ensure_ascii=False, indent=2)

    logger.info(f"リライト候補: {len(candidates)}件中 上位{len(top)}件")
    for i, c in enumerate(top, 1):
        logger.info(
            f"  {i}. [{c['score']}pt] {c['title'][:40]} "
            f"(PV:{c['recent_pv']}, {c['days_since']}日前, {c['word_count']}字)"
        )

    if not args.no_discord and top:
        summary = f"**{len(candidates)}件のリライト候補を検出**\n\n"
        for i, c in enumerate(top[:5], 1):
            summary += (
                f"{i}. **{c['title'][:35]}** "
                f"(スコア:{c['score']}, PV:{c['recent_pv']}, {c['days_since']}日前)\n"
            )
        send_discord_notification(secrets, summary)

    logger.info(f"レポート: {report_path}")
    logger.info("========== リライト候補抽出 終了 ==========")


if __name__ == "__main__":
    main()
