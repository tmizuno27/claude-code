#!/usr/bin/env python3
"""
3サイト週次アナリティクスレポート生成スクリプト
GA4 Data APIをrequests経由で直接呼び出す
"""

import json
import logging
import os
import sys
from datetime import datetime, timedelta
from pathlib import Path

import requests
from google.oauth2 import service_account

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

SITES = [
    {
        "name": "nambei-oyaji.com",
        "label": "南米おやじの海外生活ラボ",
        "base": Path("C:/Users/tmizu/マイドライブ/GitHub/claude-code/sites/nambei-oyaji.com"),
    },
    {
        "name": "otona-match.com",
        "label": "大人のマッチングナビ",
        "base": Path("C:/Users/tmizu/マイドライブ/GitHub/claude-code/sites/otona-match.com"),
    },
    {
        "name": "sim-hikaku.online",
        "label": "SIM比較オンライン",
        "base": Path("C:/Users/tmizu/マイドライブ/GitHub/claude-code/sites/sim-hikaku.online"),
    },
]

GA4_API_BASE = "https://analyticsdata.googleapis.com/v1beta"
SCOPES = ["https://www.googleapis.com/auth/analytics.readonly"]


def get_access_token(creds_path: Path) -> str:
    """サービスアカウントからアクセストークンを取得"""
    creds = service_account.Credentials.from_service_account_file(
        str(creds_path), scopes=SCOPES
    )
    import google.auth.transport.requests as google_requests
    req = google_requests.Request()
    creds.refresh(req)
    return creds.token


def run_report(token: str, property_id: str, start_date: str, end_date: str,
               dimensions: list, metrics: list, limit: int = 10) -> dict:
    """GA4 runReport APIを呼び出す"""
    url = f"{GA4_API_BASE}/properties/{property_id}:runReport"
    headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}
    body = {
        "dateRanges": [{"startDate": start_date, "endDate": end_date}],
        "dimensions": [{"name": d} for d in dimensions],
        "metrics": [{"name": m} for m in metrics],
        "limit": limit,
        "orderBys": [{"metric": {"metricName": metrics[0]}, "desc": True}],
    }
    resp = requests.post(url, headers=headers, json=body, timeout=30)
    resp.raise_for_status()
    return resp.json()


def fetch_site_data(site: dict) -> dict:
    """サイトのGA4データを取得"""
    config_path = site["base"] / "config" / "settings.json"
    creds_path = site["base"] / "config" / "ga4-credentials.json"

    with open(config_path, encoding="utf-8") as f:
        config = json.load(f)

    property_id = config.get("google_analytics", {}).get("property_id", "")
    if not property_id or "YOUR" in str(property_id):
        return {"error": "property_id未設定"}

    token = get_access_token(creds_path)

    today = datetime.now()
    end_date = today.strftime("%Y-%m-%d")
    start_date = (today - timedelta(days=7)).strftime("%Y-%m-%d")
    prev_start = (today - timedelta(days=14)).strftime("%Y-%m-%d")
    prev_end = (today - timedelta(days=8)).strftime("%Y-%m-%d")

    # 今週の集計値
    summary_resp = run_report(
        token, property_id, start_date, end_date,
        dimensions=[],
        metrics=["sessions", "screenPageViews", "activeUsers"],
        limit=1
    )
    # dimensionsなしのレスポンスはtotalsを使う
    # totalsが空の場合はrowsを使う
    rows = summary_resp.get("rows", [])
    totals = summary_resp.get("totals", [])
    if totals:
        mv = totals[0]["metricValues"]
    elif rows:
        mv = rows[0]["metricValues"]
    else:
        mv = [{"value": "0"}, {"value": "0"}, {"value": "0"}]

    sessions = int(mv[0]["value"])
    pageviews = int(mv[1]["value"])
    users = int(mv[2]["value"])

    # 前週比較
    prev_resp = run_report(
        token, property_id, prev_start, prev_end,
        dimensions=[],
        metrics=["sessions", "screenPageViews", "activeUsers"],
        limit=1
    )
    prev_rows = prev_resp.get("rows", [])
    prev_totals = prev_resp.get("totals", [])
    if prev_totals:
        pmv = prev_totals[0]["metricValues"]
    elif prev_rows:
        pmv = prev_rows[0]["metricValues"]
    else:
        pmv = [{"value": "0"}, {"value": "0"}, {"value": "0"}]

    prev_sessions = int(pmv[0]["value"])
    prev_pageviews = int(pmv[1]["value"])
    prev_users = int(pmv[2]["value"])

    # 人気ページ TOP10
    pages_resp = run_report(
        token, property_id, start_date, end_date,
        dimensions=["pagePath", "pageTitle"],
        metrics=["screenPageViews"],
        limit=10
    )
    top_pages = []
    for row in pages_resp.get("rows", []):
        path = row["dimensionValues"][0]["value"]
        title = row["dimensionValues"][1]["value"]
        pv = int(row["metricValues"][0]["value"])
        top_pages.append({"path": path, "title": title, "pageviews": pv})

    # 流入元内訳
    source_resp = run_report(
        token, property_id, start_date, end_date,
        dimensions=["sessionDefaultChannelGroup"],
        metrics=["sessions"],
        limit=10
    )
    traffic_sources = []
    for row in source_resp.get("rows", []):
        channel = row["dimensionValues"][0]["value"]
        sess = int(row["metricValues"][0]["value"])
        pct = round(sess / sessions * 100, 1) if sessions > 0 else 0
        traffic_sources.append({"channel": channel, "sessions": sess, "percentage": pct})

    return {
        "period": {"start": start_date, "end": end_date},
        "summary": {
            "sessions": sessions,
            "pageviews": pageviews,
            "users": users,
        },
        "prev_week": {
            "sessions": prev_sessions,
            "pageviews": prev_pageviews,
            "users": prev_users,
        },
        "changes": {
            "sessions_pct": round((sessions - prev_sessions) / prev_sessions * 100, 1) if prev_sessions > 0 else None,
            "pageviews_pct": round((pageviews - prev_pageviews) / prev_pageviews * 100, 1) if prev_pageviews > 0 else None,
            "users_pct": round((users - prev_users) / prev_users * 100, 1) if prev_users > 0 else None,
        },
        "top_pages": top_pages,
        "traffic_sources": traffic_sources,
    }


def format_change(pct) -> str:
    if pct is None:
        return "N/A"
    arrow = "▲" if pct >= 0 else "▼"
    return f"{arrow}{abs(pct):.1f}%"


def generate_report_md(site: dict, data: dict, generated_at: str) -> str:
    """マークダウン形式のレポートを生成"""
    label = site["label"]
    name = site["name"]

    if "error" in data:
        return f"# {label} 週次レポート\n\nエラー: {data['error']}\n"

    s = data["summary"]
    p = data["prev_week"]
    c = data["changes"]
    period = data["period"]

    lines = [
        f"# {label}（{name}）週次アナリティクスレポート",
        f"",
        f"**生成日時**: {generated_at}",
        f"**対象期間**: {period['start']} ～ {period['end']}（過去7日間）",
        f"",
        f"---",
        f"",
        f"## 📊 サマリー",
        f"",
        f"| 指標 | 今週 | 前週 | 増減 |",
        f"|------|-----:|-----:|-----:|",
        f"| セッション数 | {s['sessions']:,} | {p['sessions']:,} | {format_change(c['sessions_pct'])} |",
        f"| ページビュー | {s['pageviews']:,} | {p['pageviews']:,} | {format_change(c['pageviews_pct'])} |",
        f"| ユーザー数 | {s['users']:,} | {p['users']:,} | {format_change(c['users_pct'])} |",
        f"",
        f"---",
        f"",
        f"## 🏆 人気ページ TOP10",
        f"",
        f"| # | PV数 | ページタイトル | パス |",
        f"|---|-----:|----------------|------|",
    ]

    for i, page in enumerate(data["top_pages"], 1):
        title = page["title"][:40] + "..." if len(page["title"]) > 40 else page["title"]
        path = page["path"][:50] + "..." if len(page["path"]) > 50 else page["path"]
        lines.append(f"| {i} | {page['pageviews']:,} | {title} | `{path}` |")

    lines += [
        f"",
        f"---",
        f"",
        f"## 🚦 流入元内訳",
        f"",
        f"| チャネル | セッション数 | 割合 |",
        f"|----------|------------:|-----:|",
    ]

    for src in data["traffic_sources"]:
        lines.append(f"| {src['channel']} | {src['sessions']:,} | {src['percentage']:.1f}% |")

    lines += ["", "---", "", f"*このレポートは自動生成されました。*"]
    return "\n".join(lines)


def main():
    generated_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    all_results = {}

    for site in SITES:
        logger.info(f"データ取得中: {site['name']}")
        try:
            data = fetch_site_data(site)
            all_results[site["name"]] = data
            logger.info(f"  完了: sessions={data.get('summary', {}).get('sessions', 'N/A')}")
        except Exception as e:
            logger.error(f"  エラー: {e}")
            all_results[site["name"]] = {"error": str(e)}

    # 各サイトのoutputs/reports/に保存
    today_str = datetime.now().strftime("%Y-%m-%d")
    for site in SITES:
        data = all_results.get(site["name"], {"error": "データなし"})
        report_md = generate_report_md(site, data, generated_at)

        report_dir = site["base"] / "outputs" / "reports"
        report_dir.mkdir(parents=True, exist_ok=True)

        filename = f"weekly-analytics-{today_str}.md"
        report_path = report_dir / filename
        with open(report_path, "w", encoding="utf-8") as f:
            f.write(report_md)
        logger.info(f"レポート保存: {report_path}")

    # 全体サマリーをコンソール出力
    print("\n" + "=" * 60)
    print(f"  3サイト週次アナリティクスレポート（{today_str}）")
    print("=" * 60)
    for site in SITES:
        data = all_results.get(site["name"], {})
        print(f"\n【{site['label']}】")
        if "error" in data:
            print(f"  エラー: {data['error']}")
        else:
            s = data["summary"]
            c = data["changes"]
            print(f"  セッション: {s['sessions']:,} ({format_change(c['sessions_pct'])})")
            print(f"  PV:         {s['pageviews']:,} ({format_change(c['pageviews_pct'])})")
            print(f"  ユーザー:   {s['users']:,} ({format_change(c['users_pct'])})")
            if data["top_pages"]:
                print(f"  1位ページ:  {data['top_pages'][0]['path']} ({data['top_pages'][0]['pageviews']:,} PV)")
    print("\n" + "=" * 60)

    # 全サイト統合JSONも保存（任意）
    json_path = Path("C:/Users/tmizu/マイドライブ/GitHub/claude-code/logs/seo") / f"weekly-analytics-{today_str}.json"
    json_path.parent.mkdir(parents=True, exist_ok=True)
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump({"generated_at": generated_at, "data": all_results}, f, ensure_ascii=False, indent=2)
    logger.info(f"統合JSON保存: {json_path}")


if __name__ == "__main__":
    main()
