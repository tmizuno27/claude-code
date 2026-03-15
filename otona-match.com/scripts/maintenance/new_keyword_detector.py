#!/usr/bin/env python3
"""Search Console 新規KW検出 — 意図せず拾ったKWを発見->新記事ネタに活用

Usage:
    python new_keyword_detector.py              # 直近7日間
    python new_keyword_detector.py --days 14    # 14日間
    python new_keyword_detector.py --min-clicks 2  # 2クリック以上
"""
import argparse
import io
import json
import logging
import sys
from datetime import datetime, timedelta
from pathlib import Path

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding="utf-8", errors="replace")

try:
    import requests
except ImportError:
    requests = None

# --- Paths ---
SCRIPT_DIR = Path(__file__).parent
PROJECT_ROOT = SCRIPT_DIR.parent.parent
CONFIG_DIR = PROJECT_ROOT / "config"
OUTPUTS_DIR = PROJECT_ROOT / "outputs"
REPORTS_DIR = OUTPUTS_DIR / "maintenance-reports"
LOG_FILE = OUTPUTS_DIR / "new-keyword-detector.log"
KNOWN_KW_FILE = OUTPUTS_DIR / "known-keywords.json"

REPORTS_DIR.mkdir(parents=True, exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler(LOG_FILE, encoding="utf-8"),
    ],
)
logger = logging.getLogger(__name__)


def load_secrets():
    path = CONFIG_DIR / "secrets.json"
    if not path.exists():
        return {}
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def load_known_keywords():
    """過去に検出済みのKWリスト"""
    if KNOWN_KW_FILE.exists():
        with open(KNOWN_KW_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {"keywords": [], "last_updated": None}


def save_known_keywords(data):
    with open(KNOWN_KW_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def fetch_search_console_data(secrets, days=7):
    """Google Search Console API からクエリデータ取得"""
    try:
        from google.oauth2.service_account import Credentials
        from googleapiclient.discovery import build
    except ImportError:
        logger.error("google-api-python-client 未インストール: pip install google-api-python-client google-auth")
        return []

    gsc_creds_path = CONFIG_DIR / "gsc-credentials.json"
    if not gsc_creds_path.exists():
        gsc_creds_path = CONFIG_DIR / "ga4-credentials.json"
    if not gsc_creds_path.exists():
        logger.error("GSC認証ファイルが見つかりません")
        return []

    creds = Credentials.from_service_account_file(
        str(gsc_creds_path),
        scopes=["https://www.googleapis.com/auth/webmasters.readonly"],
    )
    service = build("searchconsole", "v1", credentials=creds)

    end_date = datetime.now() - timedelta(days=3)  # GSCは3日遅延
    start_date = end_date - timedelta(days=days)

    body = {
        "startDate": start_date.strftime("%Y-%m-%d"),
        "endDate": end_date.strftime("%Y-%m-%d"),
        "dimensions": ["query", "page"],
        "rowLimit": 500,
        "dimensionFilterGroups": [],
    }

    try:
        response = service.searchanalytics().query(
            siteUrl="https://otona-match.com/",
            body=body,
        ).execute()
        return response.get("rows", [])
    except Exception as e:
        logger.error(f"GSC API エラー: {e}")
        return []


def analyze_keywords(rows, known_kw_set, min_clicks=1):
    """新規KWを検出"""
    new_keywords = []
    for row in rows:
        query = row["keys"][0]
        page = row["keys"][1]
        clicks = row.get("clicks", 0)
        impressions = row.get("impressions", 0)
        position = row.get("position", 0)

        if clicks < min_clicks:
            continue

        if query in known_kw_set:
            continue

        new_keywords.append({
            "query": query,
            "page": page,
            "clicks": clicks,
            "impressions": impressions,
            "ctr": round(row.get("ctr", 0) * 100, 1),
            "position": round(position, 1),
            "potential": "high" if position <= 20 and impressions >= 50 else "medium" if position <= 30 else "low",
        })

    new_keywords.sort(key=lambda x: (-x["clicks"], -x["impressions"]))
    return new_keywords


def send_discord_notification(secrets, summary):
    if not requests:
        return
    webhook_url = secrets.get("discord", {}).get("webhook_url", "")
    if not webhook_url or webhook_url.startswith("YOUR"):
        return
    payload = {
        "embeds": [{
            "title": "新規KW検出レポート (otona-match)",
            "description": summary,
            "color": 0x4488FF,
            "timestamp": datetime.utcnow().isoformat(),
        }]
    }
    try:
        requests.post(webhook_url, json=payload, timeout=10)
    except Exception as e:
        logger.warning(f"Discord通知失敗: {e}")


def main():
    parser = argparse.ArgumentParser(description="Search Console 新規KW検出")
    parser.add_argument("--days", type=int, default=7, help="分析期間（日数）")
    parser.add_argument("--min-clicks", type=int, default=1, help="最小クリック数")
    parser.add_argument("--no-discord", action="store_true")
    args = parser.parse_args()

    logger.info("========== 新規KW検出 開始 ==========")

    secrets = load_secrets()
    known_data = load_known_keywords()
    known_kw_set = set(known_data.get("keywords", []))

    # GSCデータ取得
    rows = fetch_search_console_data(secrets, days=args.days)
    if not rows:
        logger.warning("GSCデータが取得できませんでした。")
        logger.info("========== 新規KW検出 終了 ==========")
        return

    logger.info(f"GSCから{len(rows)}行取得")

    # 新規KW分析
    new_keywords = analyze_keywords(rows, known_kw_set, min_clicks=args.min_clicks)

    # レポート
    today = datetime.now().strftime("%Y-%m-%d")
    report_path = REPORTS_DIR / f"new-keywords-{today}.json"
    report = {
        "date": today,
        "period_days": args.days,
        "total_queries": len(rows),
        "new_keywords_found": len(new_keywords),
        "high_potential": len([k for k in new_keywords if k["potential"] == "high"]),
        "keywords": new_keywords,
    }
    with open(report_path, "w", encoding="utf-8") as f:
        json.dump(report, f, ensure_ascii=False, indent=2)

    # 既知KWリスト更新
    for kw in new_keywords:
        known_kw_set.add(kw["query"])
    known_data["keywords"] = sorted(known_kw_set)
    known_data["last_updated"] = today
    save_known_keywords(known_data)

    # ログ出力
    logger.info(f"新規KW: {len(new_keywords)}件検出 (High: {report['high_potential']}件)")
    for i, kw in enumerate(new_keywords[:10], 1):
        logger.info(
            f"  {i}. [{kw['potential']}] \"{kw['query']}\" "
            f"(clicks:{kw['clicks']}, imp:{kw['impressions']}, pos:{kw['position']})"
        )

    # Discord通知
    if not args.no_discord and new_keywords:
        high = [k for k in new_keywords if k["potential"] == "high"]
        summary = f"**{len(new_keywords)}件の新規KW検出** (High: {len(high)}件)\n\n"
        for kw in new_keywords[:7]:
            marker = "[HIGH]" if kw["potential"] == "high" else "[MED]" if kw["potential"] == "medium" else "[LOW]"
            summary += f"{marker} **{kw['query']}** -- {kw['clicks']}click, pos:{kw['position']}\n"
        send_discord_notification(secrets, summary)

    logger.info(f"レポート: {report_path}")
    logger.info("========== 新規KW検出 終了 ==========")


if __name__ == "__main__":
    main()
