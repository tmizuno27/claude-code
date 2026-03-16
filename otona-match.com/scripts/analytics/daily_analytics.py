#!/usr/bin/env python3
"""
毎日のアクセス分析＆レポート生成スクリプト v1.0

GA4 Data API + Search Console API + WordPress REST API から
前日のアクセスデータを取得し、Claude API でインサイトレポートを生成。
レポートは outputs/daily-reports/ に保存され、auto-sync で GitHub に自動 push される。

データソース:
  1. GA4 Data API — PV、セッション、ユーザー数、人気記事、流入元
  2. Search Console API — 検索キーワード、表示回数、CTR、掲載順位
  3. WordPress REST API — 記事一覧、公開状況

実行方法:
  python daily_analytics.py              # 前日のレポート
  python daily_analytics.py --days 7     # 過去7日間のレポート
  python daily_analytics.py --compare    # 前日 vs 前週同曜日の比較
"""

import argparse
import io
import json
import logging
import os
import sys
from base64 import b64encode
from datetime import datetime, timedelta
from pathlib import Path

# Windows UTF-8 出力修正
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding="utf-8", errors="replace")

# プロジェクトルート
SCRIPT_DIR = Path(__file__).parent
PROJECT_ROOT = SCRIPT_DIR.parent.parent
CONFIG_DIR = PROJECT_ROOT / "config"
OUTPUTS_DIR = PROJECT_ROOT / "outputs"
REPORTS_DIR = OUTPUTS_DIR / "daily-reports"

# ログ設定
LOG_FILE = OUTPUTS_DIR / "daily-analytics.log"
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler(LOG_FILE, encoding="utf-8"),
    ],
)
logger = logging.getLogger(__name__)

# --- 依存ライブラリ ---
try:
    import anthropic
except ImportError:
    anthropic = None

try:
    import requests
except ImportError:
    requests = None
    logger.error("requests ライブラリが必要です: pip install requests")
    sys.exit(1)


def load_secrets():
    """secrets.json を読み込む"""
    path = CONFIG_DIR / "secrets.json"
    if not path.exists():
        logger.error(f"secrets.json が見つかりません: {path}")
        return {}
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def load_settings():
    """settings.json を読み込む"""
    path = CONFIG_DIR / "settings.json"
    if not path.exists():
        return {}
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


# =====================================================
# データソース 1: GA4 Data API
# =====================================================
def fetch_ga4_data(settings, start_date, end_date):
    """GA4 Data API からアクセスデータを取得"""
    ga_config = settings.get("google_analytics", {})
    property_id = ga_config.get("property_id", "")
    cred_path = ga_config.get("credentials_file", "ga4-credentials.json")
    cred_file = PROJECT_ROOT / cred_path if "/" in cred_path else CONFIG_DIR / cred_path

    if not property_id or "YOUR" in property_id:
        logger.info("GA4 property_id 未設定。スキップ")
        return None

    if not cred_file.exists():
        logger.info(f"GA4認証ファイル未作成: {cred_file}")
        return None

    try:
        os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = str(cred_file)
        from google.analytics.data_v1beta import BetaAnalyticsDataClient
        from google.analytics.data_v1beta.types import (
            DateRange, Dimension, Metric, RunReportRequest, OrderBy
        )

        client = BetaAnalyticsDataClient()

        # --- 基本指標 ---
        basic_req = RunReportRequest(
            property=f"properties/{property_id}",
            date_ranges=[DateRange(
                start_date=start_date.strftime("%Y-%m-%d"),
                end_date=end_date.strftime("%Y-%m-%d"),
            )],
            metrics=[
                Metric(name="sessions"),
                Metric(name="screenPageViews"),
                Metric(name="activeUsers"),
                Metric(name="averageSessionDuration"),
                Metric(name="bounceRate"),
                Metric(name="newUsers"),
            ],
        )
        basic_resp = client.run_report(basic_req)
        row = basic_resp.rows[0] if basic_resp.rows else None
        basics = {
            "sessions": int(row.metric_values[0].value) if row else 0,
            "pageviews": int(row.metric_values[1].value) if row else 0,
            "users": int(row.metric_values[2].value) if row else 0,
            "avg_session_duration": float(row.metric_values[3].value) if row else 0,
            "bounce_rate": float(row.metric_values[4].value) if row else 0,
            "new_users": int(row.metric_values[5].value) if row else 0,
        }

        # --- 人気ページ TOP 10 ---
        pages_req = RunReportRequest(
            property=f"properties/{property_id}",
            date_ranges=[DateRange(
                start_date=start_date.strftime("%Y-%m-%d"),
                end_date=end_date.strftime("%Y-%m-%d"),
            )],
            dimensions=[Dimension(name="pagePath"), Dimension(name="pageTitle")],
            metrics=[
                Metric(name="screenPageViews"),
                Metric(name="activeUsers"),
                Metric(name="averageSessionDuration"),
            ],
            order_bys=[OrderBy(metric=OrderBy.MetricOrderBy(metric_name="screenPageViews"), desc=True)],
            limit=10,
        )
        pages_resp = client.run_report(pages_req)
        top_pages = []
        for r in pages_resp.rows:
            top_pages.append({
                "path": r.dimension_values[0].value,
                "title": r.dimension_values[1].value,
                "pageviews": int(r.metric_values[0].value),
                "users": int(r.metric_values[1].value),
                "avg_duration": float(r.metric_values[2].value),
            })

        # --- 流入元 TOP 5 ---
        source_req = RunReportRequest(
            property=f"properties/{property_id}",
            date_ranges=[DateRange(
                start_date=start_date.strftime("%Y-%m-%d"),
                end_date=end_date.strftime("%Y-%m-%d"),
            )],
            dimensions=[Dimension(name="sessionSource"), Dimension(name="sessionMedium")],
            metrics=[Metric(name="sessions"), Metric(name="activeUsers")],
            order_bys=[OrderBy(metric=OrderBy.MetricOrderBy(metric_name="sessions"), desc=True)],
            limit=5,
        )
        source_resp = client.run_report(source_req)
        sources = []
        for r in source_resp.rows:
            sources.append({
                "source": r.dimension_values[0].value,
                "medium": r.dimension_values[1].value,
                "sessions": int(r.metric_values[0].value),
                "users": int(r.metric_values[1].value),
            })

        # --- デバイス別 ---
        device_req = RunReportRequest(
            property=f"properties/{property_id}",
            date_ranges=[DateRange(
                start_date=start_date.strftime("%Y-%m-%d"),
                end_date=end_date.strftime("%Y-%m-%d"),
            )],
            dimensions=[Dimension(name="deviceCategory")],
            metrics=[Metric(name="sessions")],
        )
        device_resp = client.run_report(device_req)
        devices = {}
        for r in device_resp.rows:
            devices[r.dimension_values[0].value] = int(r.metric_values[0].value)

        return {
            "status": "ok",
            **basics,
            "top_pages": top_pages,
            "sources": sources,
            "devices": devices,
        }

    except ImportError:
        logger.info("google-analytics-data ライブラリ未インストール")
        return None
    except Exception as e:
        logger.error(f"GA4 API エラー: {e}")
        return None


# =====================================================
# データソース 2: Search Console API
# =====================================================
def fetch_search_console_data(settings, start_date, end_date):
    """Search Console API から検索パフォーマンスデータを取得"""
    sc_config = settings.get("search_console", {})
    site_url = sc_config.get("site_url", "")
    cred_path = sc_config.get("credentials_file", "gsc-credentials.json")
    cred_file = PROJECT_ROOT / cred_path if "/" in cred_path else CONFIG_DIR / cred_path

    if not site_url or not cred_file.exists():
        logger.info("Search Console 未設定。スキップ")
        return None

    try:
        os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = str(cred_file)
        from google.oauth2 import service_account
        from googleapiclient.discovery import build

        credentials = service_account.Credentials.from_service_account_file(
            str(cred_file),
            scopes=["https://www.googleapis.com/auth/webmasters.readonly"],
        )
        service = build("searchconsole", "v1", credentials=credentials)

        # --- 検索クエリ TOP 20 ---
        response = service.searchanalytics().query(
            siteUrl=site_url,
            body={
                "startDate": start_date.strftime("%Y-%m-%d"),
                "endDate": end_date.strftime("%Y-%m-%d"),
                "dimensions": ["query"],
                "rowLimit": 20,
            },
        ).execute()

        queries = []
        for row in response.get("rows", []):
            queries.append({
                "query": row["keys"][0],
                "clicks": row.get("clicks", 0),
                "impressions": row.get("impressions", 0),
                "ctr": round(row.get("ctr", 0) * 100, 2),
                "position": round(row.get("position", 0), 1),
            })

        # --- ページ別 TOP 10 ---
        page_response = service.searchanalytics().query(
            siteUrl=site_url,
            body={
                "startDate": start_date.strftime("%Y-%m-%d"),
                "endDate": end_date.strftime("%Y-%m-%d"),
                "dimensions": ["page"],
                "rowLimit": 10,
            },
        ).execute()

        pages = []
        for row in page_response.get("rows", []):
            pages.append({
                "page": row["keys"][0],
                "clicks": row.get("clicks", 0),
                "impressions": row.get("impressions", 0),
                "ctr": round(row.get("ctr", 0) * 100, 2),
                "position": round(row.get("position", 0), 1),
            })

        return {
            "status": "ok",
            "total_clicks": sum(q["clicks"] for q in queries),
            "total_impressions": sum(q["impressions"] for q in queries),
            "queries": queries,
            "pages": pages,
        }

    except ImportError:
        logger.info("Google API ライブラリ未インストール")
        return None
    except Exception as e:
        logger.error(f"Search Console API エラー: {e}")
        return None


# =====================================================
# データソース 3: WordPress REST API
# =====================================================
def fetch_wordpress_stats(settings, secrets):
    """WordPress REST API から投稿情報を取得"""
    wp = settings.get("wordpress", {})
    rest_url = wp.get("rest_api_url", "")
    username = secrets.get("wordpress", {}).get("username", "")
    app_password = secrets.get("wordpress", {}).get("app_password", "")

    if not rest_url:
        return None

    credentials = f"{username}:{app_password}"
    token = b64encode(credentials.encode()).decode()
    headers = {"Authorization": f"Basic {token}"}

    try:
        # 公開済み記事の数
        resp = requests.get(
            f"{rest_url}/posts",
            params={"per_page": 1, "status": "publish"},
            headers=headers,
            timeout=15,
        )
        total_published = int(resp.headers.get("X-WP-Total", 0))

        # 最近の記事（直近5件）
        resp2 = requests.get(
            f"{rest_url}/posts",
            params={"per_page": 5, "status": "publish", "orderby": "date", "order": "desc"},
            headers=headers,
            timeout=15,
        )
        recent_posts = []
        if resp2.status_code == 200:
            for post in resp2.json():
                recent_posts.append({
                    "title": post["title"]["rendered"],
                    "slug": post["slug"],
                    "date": post["date"],
                    "url": post["link"],
                })

        # ドラフト記事数
        resp3 = requests.get(
            f"{rest_url}/posts",
            params={"per_page": 1, "status": "draft"},
            headers=headers,
            timeout=15,
        )
        total_drafts = int(resp3.headers.get("X-WP-Total", 0))

        return {
            "total_published": total_published,
            "total_drafts": total_drafts,
            "recent_posts": recent_posts,
        }

    except Exception as e:
        logger.error(f"WordPress API エラー: {e}")
        return None


# =====================================================
# レポート生成
# =====================================================
DAILY_REPORT_PROMPT = """あなたは「大人のマッチングナビ」(otona-match.com) のアクセス分析アドバイザーです。
以下のデータから、日本語で簡潔な日次レポートを生成してください。

## レポート要件
1. **サマリー**: 主要KPIを1-2行で要約
2. **トラフィック分析**: PV・ユーザー数の傾向、前日/前週比較（データがあれば）
3. **人気記事 TOP 5**: どの記事が読まれているか、なぜ読まれているかの分析
4. **検索パフォーマンス**: 上位キーワード、CTR改善の余地
5. **流入元分析**: オーガニック/SNS/ダイレクトの比率
6. **アクションアイテム**: 今日やるべきこと（具体的に2-3個）
7. **収益最大化の提案**: アフィリエイト記事の改善ポイント

## ブログの特徴
- 30代・40代向けマッチングアプリ比較サイト
- 収益源: アフィリエイト（結婚相談所、マッチングアプリ、出会い系）
- コンテンツ: マッチングアプリ比較、出会い系、婚活、恋愛テクニック
- ターゲット: 30-40代の出会いを求める日本人男女

## 出力形式
Markdownで出力。見出し・箇条書き・表を適切に使用。"""


def generate_daily_report(secrets, ga4_data, sc_data, wp_data, start_date, end_date, compare_data=None):
    """Claude API で分析レポートを生成"""
    api_key = secrets.get("claude_api", {}).get("api_key", "")
    if not api_key or "YOUR" in api_key:
        return generate_template_report(ga4_data, sc_data, wp_data, start_date, end_date)

    data_summary = f"""## 分析期間: {start_date.strftime('%Y/%m/%d')} 〜 {end_date.strftime('%Y/%m/%d')}

### GA4 アクセスデータ
{json.dumps(ga4_data, ensure_ascii=False, indent=2) if ga4_data else "GA4未設定（セットアップ待ち）"}

### Search Console 検索データ
{json.dumps(sc_data, ensure_ascii=False, indent=2) if sc_data else "Search Console未設定（セットアップ待ち）"}

### WordPress 投稿状況
{json.dumps(wp_data, ensure_ascii=False, indent=2) if wp_data else "WordPress接続エラー"}
"""

    if compare_data:
        data_summary += f"""
### 前週同曜日との比較データ
{json.dumps(compare_data, ensure_ascii=False, indent=2)}
"""

    if anthropic is None:
        logger.warning("anthropic ライブラリ未インストール。テンプレートレポートを生成")
        return generate_template_report(ga4_data, sc_data, wp_data, start_date, end_date)

    try:
        client = anthropic.Anthropic(api_key=api_key)
        response = client.messages.create(
            model="claude-sonnet-4-6",
            max_tokens=2048,
            system=DAILY_REPORT_PROMPT,
            messages=[{"role": "user", "content": data_summary}],
        )
        return response.content[0].text
    except Exception as e:
        logger.error(f"Claude API エラー: {e}")
        return generate_template_report(ga4_data, sc_data, wp_data, start_date, end_date)


def generate_template_report(ga4_data, sc_data, wp_data, start_date, end_date):
    """テンプレートレポート（API未設定時用）"""
    now = datetime.now().strftime("%Y/%m/%d %H:%M")
    period = f"{start_date.strftime('%Y/%m/%d')} 〜 {end_date.strftime('%Y/%m/%d')}"

    sections = [f"# 日次アクセスレポート ({period})\n"]
    sections.append(f"*生成: {now}*\n")

    if ga4_data and ga4_data.get("status") == "ok":
        sections.append("## トラフィック")
        sections.append(f"| 指標 | 値 |")
        sections.append(f"|---|---|")
        sections.append(f"| セッション | {ga4_data['sessions']:,} |")
        sections.append(f"| PV | {ga4_data['pageviews']:,} |")
        sections.append(f"| ユーザー | {ga4_data['users']:,} |")
        sections.append(f"| 新規ユーザー | {ga4_data['new_users']:,} |")
        sections.append(f"| 平均滞在時間 | {ga4_data['avg_session_duration']:.0f}秒 |")
        sections.append(f"| 直帰率 | {ga4_data['bounce_rate']:.1f}% |")
        sections.append("")

        if ga4_data.get("top_pages"):
            sections.append("## 人気ページ TOP 10")
            sections.append("| # | ページ | PV | ユーザー |")
            sections.append("|---|---|---|---|")
            for i, p in enumerate(ga4_data["top_pages"], 1):
                sections.append(f"| {i} | {p['path']} | {p['pageviews']:,} | {p['users']:,} |")
            sections.append("")

        if ga4_data.get("sources"):
            sections.append("## 流入元 TOP 5")
            sections.append("| ソース | メディア | セッション |")
            sections.append("|---|---|---|")
            for s in ga4_data["sources"]:
                sections.append(f"| {s['source']} | {s['medium']} | {s['sessions']:,} |")
            sections.append("")

        if ga4_data.get("devices"):
            sections.append("## デバイス別")
            for device, count in ga4_data["devices"].items():
                sections.append(f"- {device}: {count:,}")
            sections.append("")
    else:
        sections.append("## GA4データ")
        sections.append("GA4未設定。`config/settings.json` の `property_id` を設定してください。\n")

    if sc_data and sc_data.get("status") == "ok":
        sections.append("## 検索パフォーマンス")
        sections.append(f"- 合計クリック: {sc_data['total_clicks']:,}")
        sections.append(f"- 合計表示回数: {sc_data['total_impressions']:,}")
        sections.append("")
        if sc_data.get("queries"):
            sections.append("### 検索キーワード TOP 10")
            sections.append("| キーワード | クリック | 表示 | CTR | 順位 |")
            sections.append("|---|---|---|---|---|")
            for q in sc_data["queries"][:10]:
                sections.append(f"| {q['query']} | {q['clicks']} | {q['impressions']:,} | {q['ctr']}% | {q['position']} |")
            sections.append("")
    else:
        sections.append("## Search Console")
        sections.append("Search Console未設定。\n")

    if wp_data:
        sections.append("## WordPress")
        sections.append(f"- 公開済み: {wp_data['total_published']}記事")
        sections.append(f"- 下書き: {wp_data['total_drafts']}記事")
        if wp_data.get("recent_posts"):
            sections.append("\n### 最近の公開記事")
            for p in wp_data["recent_posts"]:
                sections.append(f"- [{p['title']}]({p['url']}) ({p['date'][:10]})")
        sections.append("")

    sections.append("---")
    sections.append("*このレポートは daily_analytics.py により自動生成されました*")

    return "\n".join(sections)


# =====================================================
# Discord 通知
# =====================================================
def notify_discord(settings, report_summary):
    """Discord Webhook でサマリーを通知"""
    webhook_url = settings.get("discord", {}).get("webhook_url", "")
    if not webhook_url or "YOUR" in webhook_url:
        return

    try:
        dashboard_url = "https://github.com/tmizuno27/claude-code/blob/main/nambei-oyaji.com/outputs/reports/daily-business-dashboard.html"
        content = report_summary[:1900] if len(report_summary) > 1900 else report_summary
        requests.post(
            webhook_url,
            json={"content": f"**日次アクセスレポート (otona-match.com)**\n```\n{content}\n```\n\n📊 [ダッシュボード]({dashboard_url})"},
            timeout=10,
        )
        logger.info("Discord 通知送信完了")
    except Exception as e:
        logger.warning(f"Discord 通知失敗: {e}")


def main():
    parser = argparse.ArgumentParser(description="日次アクセス分析レポート")
    parser.add_argument("--days", type=int, default=1, help="分析する日数（デフォルト: 1=前日）")
    parser.add_argument("--compare", action="store_true", help="前週同曜日と比較")
    parser.add_argument("--no-discord", action="store_true", help="Discord通知を送らない")
    args = parser.parse_args()

    logger.info(f"=== 日次アクセス分析開始 (days={args.days}) ===")

    secrets = load_secrets()
    settings = load_settings()

    # 分析期間
    end_date = datetime.now() - timedelta(days=1)
    start_date = end_date - timedelta(days=args.days - 1)

    # データ収集
    logger.info("GA4 データ取得中...")
    ga4_data = fetch_ga4_data(settings, start_date, end_date)

    logger.info("Search Console データ取得中...")
    sc_data = fetch_search_console_data(settings, start_date, end_date)

    logger.info("WordPress データ取得中...")
    wp_data = fetch_wordpress_stats(settings, secrets)

    # 前週比較データ
    compare_data = None
    if args.compare and ga4_data:
        prev_end = end_date - timedelta(days=7)
        prev_start = start_date - timedelta(days=7)
        compare_data = fetch_ga4_data(settings, prev_start, prev_end)

    # レポート生成
    logger.info("レポート生成中...")
    report = generate_daily_report(
        secrets, ga4_data, sc_data, wp_data, start_date, end_date, compare_data
    )

    # 保存
    REPORTS_DIR.mkdir(parents=True, exist_ok=True)
    date_str = end_date.strftime("%Y-%m-%d")
    report_path = REPORTS_DIR / f"daily-{date_str}.md"
    report_path.write_text(report, encoding="utf-8")
    logger.info(f"レポート保存: {report_path}")

    # Discord 通知
    if not args.no_discord:
        summary_lines = report.split("\n")[:15]
        notify_discord(settings, "\n".join(summary_lines))

    # コンソール出力（先頭20行）
    for line in report.split("\n")[:20]:
        print(line)

    logger.info("=== 日次アクセス分析完了 ===")


if __name__ == "__main__":
    main()
