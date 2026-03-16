#!/usr/bin/env python3
"""
全事業統合 週次KPIレポート生成スクリプト v1.0

全事業（ブログ・X・eBay・フリーランス・財務）のKPIを1つのレポートに集約し、
Claude APIでインサイト付きの週次サマリーを生成する。

実行方法:
  python all_business_kpi.py              # 通常実行（過去7日間）
  python all_business_kpi.py --weeks 2    # 過去2週間
  python all_business_kpi.py --no-discord # Discord通知なし

出力先:
  outputs/kpi-reports/all-business-kpi-YYYY-MM-DD.md
"""

import argparse
import csv
import json
import logging
import os
import sys
from base64 import b64encode
from datetime import datetime, timedelta
from pathlib import Path

# プロジェクトルート
SCRIPT_DIR = Path(__file__).parent
PROJECT_ROOT = SCRIPT_DIR.parent.parent  # blog/
REPO_ROOT = PROJECT_ROOT.parent  # claude-code/
CONFIG_DIR = PROJECT_ROOT / "config"
OUTPUTS_DIR = PROJECT_ROOT / "outputs"
KPI_DIR = OUTPUTS_DIR / "kpi-reports"

# ログ設定
LOG_FILE = OUTPUTS_DIR / "all-business-kpi.log"
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
    path = CONFIG_DIR / "secrets.json"
    if not path.exists():
        logger.error(f"secrets.json が見つかりません: {path}")
        return {}
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def load_settings():
    path = CONFIG_DIR / "settings.json"
    if not path.exists():
        return {}
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


# =====================================================
# データソース 1: ブログ（GA4 + Search Console + WP）
# =====================================================
def fetch_blog_kpi(settings, secrets, start_date, end_date):
    """ブログ関連KPIを取得"""
    kpi = {
        "ga4": None,
        "search_console": None,
        "wordpress": None,
        "articles": None,
    }

    # --- GA4 ---
    ga_config = settings.get("google_analytics", {})
    property_id = ga_config.get("property_id", "")
    cred_path = ga_config.get("credentials_file", "config/ga4-credentials.json")
    cred_file = PROJECT_ROOT / cred_path if "/" in cred_path else CONFIG_DIR / cred_path

    if property_id and "YOUR" not in property_id and cred_file.exists():
        try:
            os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = str(cred_file)
            from google.analytics.data_v1beta import BetaAnalyticsDataClient
            from google.analytics.data_v1beta.types import (
                DateRange, Metric, RunReportRequest,
            )

            client = BetaAnalyticsDataClient()
            req = RunReportRequest(
                property=f"properties/{property_id}",
                date_ranges=[DateRange(
                    start_date=start_date.strftime("%Y-%m-%d"),
                    end_date=end_date.strftime("%Y-%m-%d"),
                )],
                metrics=[
                    Metric(name="sessions"),
                    Metric(name="screenPageViews"),
                    Metric(name="activeUsers"),
                    Metric(name="newUsers"),
                    Metric(name="averageSessionDuration"),
                    Metric(name="bounceRate"),
                ],
            )
            resp = client.run_report(req)
            row = resp.rows[0] if resp.rows else None
            if row:
                kpi["ga4"] = {
                    "sessions": int(row.metric_values[0].value),
                    "pageviews": int(row.metric_values[1].value),
                    "users": int(row.metric_values[2].value),
                    "new_users": int(row.metric_values[3].value),
                    "avg_session_duration": round(float(row.metric_values[4].value), 1),
                    "bounce_rate": round(float(row.metric_values[5].value), 1),
                }
                logger.info(f"GA4: PV={kpi['ga4']['pageviews']}, Users={kpi['ga4']['users']}")

            # 前週データ（比較用）
            prev_start = start_date - timedelta(days=7)
            prev_end = end_date - timedelta(days=7)
            prev_req = RunReportRequest(
                property=f"properties/{property_id}",
                date_ranges=[DateRange(
                    start_date=prev_start.strftime("%Y-%m-%d"),
                    end_date=prev_end.strftime("%Y-%m-%d"),
                )],
                metrics=[
                    Metric(name="sessions"),
                    Metric(name="screenPageViews"),
                    Metric(name="activeUsers"),
                ],
            )
            prev_resp = client.run_report(prev_req)
            prev_row = prev_resp.rows[0] if prev_resp.rows else None
            if prev_row and kpi["ga4"]:
                kpi["ga4"]["prev_sessions"] = int(prev_row.metric_values[0].value)
                kpi["ga4"]["prev_pageviews"] = int(prev_row.metric_values[1].value)
                kpi["ga4"]["prev_users"] = int(prev_row.metric_values[2].value)

        except ImportError:
            logger.info("google-analytics-data ライブラリ未インストール")
        except Exception as e:
            logger.error(f"GA4 API エラー: {e}")

    # --- Search Console ---
    sc_config = settings.get("search_console", {})
    site_url = sc_config.get("site_url", "")
    sc_cred_path = sc_config.get("credentials_file", "config/gsc-credentials.json")
    sc_cred_file = PROJECT_ROOT / sc_cred_path if "/" in sc_cred_path else CONFIG_DIR / sc_cred_path

    if site_url and sc_cred_file.exists():
        try:
            os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = str(sc_cred_file)
            from google.oauth2 import service_account
            from googleapiclient.discovery import build

            credentials = service_account.Credentials.from_service_account_file(
                str(sc_cred_file),
                scopes=["https://www.googleapis.com/auth/webmasters.readonly"],
            )
            service = build("searchconsole", "v1", credentials=credentials)

            response = service.searchanalytics().query(
                siteUrl=site_url,
                body={
                    "startDate": start_date.strftime("%Y-%m-%d"),
                    "endDate": end_date.strftime("%Y-%m-%d"),
                    "dimensions": [],
                },
            ).execute()

            rows = response.get("rows", [])
            if rows:
                r = rows[0]
                kpi["search_console"] = {
                    "clicks": r.get("clicks", 0),
                    "impressions": r.get("impressions", 0),
                    "ctr": round(r.get("ctr", 0) * 100, 2),
                    "position": round(r.get("position", 0), 1),
                }
                logger.info(f"GSC: clicks={kpi['search_console']['clicks']}, impressions={kpi['search_console']['impressions']}")
        except ImportError:
            logger.info("Google API ライブラリ未インストール")
        except Exception as e:
            logger.error(f"Search Console API エラー: {e}")

    # --- WordPress ---
    wp = settings.get("wordpress", {})
    rest_url = wp.get("rest_api_url", "")
    username = secrets.get("wordpress", {}).get("username", "")
    app_password = secrets.get("wordpress", {}).get("app_password", "")

    if rest_url and username:
        try:
            token = b64encode(f"{username}:{app_password}".encode()).decode()
            headers = {"Authorization": f"Basic {token}"}

            resp = requests.get(f"{rest_url}/posts", params={"per_page": 1, "status": "publish"}, headers=headers, timeout=15)
            total_published = int(resp.headers.get("X-WP-Total", 0))

            resp2 = requests.get(f"{rest_url}/posts", params={"per_page": 1, "status": "draft"}, headers=headers, timeout=15)
            total_drafts = int(resp2.headers.get("X-WP-Total", 0))

            # 今週公開された記事
            resp3 = requests.get(
                f"{rest_url}/posts",
                params={
                    "per_page": 10, "status": "publish",
                    "after": start_date.strftime("%Y-%m-%dT00:00:00"),
                    "before": (end_date + timedelta(days=1)).strftime("%Y-%m-%dT00:00:00"),
                },
                headers=headers, timeout=15,
            )
            new_posts = []
            if resp3.status_code == 200:
                for p in resp3.json():
                    new_posts.append({"title": p["title"]["rendered"], "url": p["link"]})

            kpi["wordpress"] = {
                "total_published": total_published,
                "total_drafts": total_drafts,
                "new_posts_this_week": len(new_posts),
                "new_posts": new_posts,
            }
            logger.info(f"WP: 公開={total_published}, 下書き={total_drafts}, 今週新規={len(new_posts)}")
        except Exception as e:
            logger.error(f"WordPress API エラー: {e}")

    # --- 記事管理CSV ---
    csv_path = OUTPUTS_DIR / "article-management.csv"
    if csv_path.exists():
        try:
            with open(csv_path, "r", encoding="utf-8") as f:
                reader = csv.DictReader(f)
                rows = list(reader)

            total = len(rows)
            published = sum(1 for r in rows if r.get("ステータス") == "公開済")
            drafts = sum(1 for r in rows if r.get("ステータス") in ("下書き", "ドラフト"))
            pillar1 = sum(1 for r in rows if "パラグアイ" in r.get("柱", ""))
            pillar2 = sum(1 for r in rows if "仕事" in r.get("柱", "") or "副業" in r.get("柱", ""))

            kpi["articles"] = {
                "total": total,
                "published": published,
                "drafts": drafts,
                "pillar1_paraguay": pillar1,
                "pillar2_work": pillar2,
            }
        except Exception as e:
            logger.warning(f"記事管理CSV読込エラー: {e}")

    return kpi


# =====================================================
# データソース 2: X (Twitter)
# =====================================================
def fetch_x_kpi(start_date, end_date):
    """X関連KPIをx-post-log.jsonlから取得"""
    log_file = OUTPUTS_DIR / "social" / "x-post-log.jsonl"
    if not log_file.exists():
        logger.info("x-post-log.jsonl が見つかりません")
        return None

    try:
        posts = []
        with open(log_file, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                post = json.loads(line)
                ts = post.get("timestamp", "")
                if ts:
                    post_date = datetime.fromisoformat(ts.replace("Z", "+00:00")).replace(tzinfo=None)
                    if start_date <= post_date <= end_date + timedelta(days=1):
                        posts.append(post)

        total_posts = len(posts)
        total_likes = sum(post.get("metrics", {}).get("like_count", 0) for post in posts)
        total_rts = sum(post.get("metrics", {}).get("retweet_count", 0) for post in posts)
        total_replies = sum(post.get("metrics", {}).get("reply_count", 0) for post in posts)
        total_impressions = sum(post.get("metrics", {}).get("impression_count", 0) for post in posts)

        kpi = {
            "posts_count": total_posts,
            "likes": total_likes,
            "retweets": total_rts,
            "replies": total_replies,
            "impressions": total_impressions,
            "engagement_rate": round((total_likes + total_rts + total_replies) / max(total_impressions, 1) * 100, 2) if total_impressions > 0 else 0,
        }
        logger.info(f"X: 投稿={total_posts}, いいね={total_likes}, RT={total_rts}")
        return kpi
    except Exception as e:
        logger.error(f"X投稿ログ読込エラー: {e}")
        return None


# =====================================================
# データソース 3: eBay
# =====================================================
def fetch_ebay_kpi():
    """eBay関連KPIをCSVから取得"""
    csv_path = REPO_ROOT / "ebay" / "ebay-niche-products.csv"
    if not csv_path.exists():
        logger.info("ebay-niche-products.csv が見つかりません")
        return None

    try:
        with open(csv_path, "r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            rows = list(reader)

        total_products = len(rows)
        categories = set()
        for r in rows:
            cat = r.get("カテゴリ", "").strip()
            if cat:
                categories.add(cat)

        kpi = {
            "total_products_tracked": total_products,
            "categories": len(categories),
            "category_list": sorted(categories),
        }
        logger.info(f"eBay: リサーチ商品={total_products}, カテゴリ={len(categories)}")
        return kpi
    except Exception as e:
        logger.error(f"eBay CSV読込エラー: {e}")
        return None


# =====================================================
# データソース 4: フリーランス
# =====================================================
def fetch_freelance_kpi():
    """フリーランス関連KPIを取得"""
    freelance_dir = REPO_ROOT / "freelance"
    if not freelance_dir.exists():
        return None

    research_count = len(list((freelance_dir / "research").glob("*.md"))) if (freelance_dir / "research").exists() else 0
    gigs_count = len(list((freelance_dir / "gigs").glob("*"))) if (freelance_dir / "gigs").exists() else 0

    kpi = {
        "research_docs": research_count,
        "gigs_defined": gigs_count,
    }
    logger.info(f"Freelance: リサーチ={research_count}, Gig={gigs_count}")
    return kpi


# =====================================================
# データソース 5: 財務（invoices）
# =====================================================
def fetch_finance_kpi():
    """財務関連KPIを取得"""
    invoice_dir = REPO_ROOT / "finance" / "invoices"
    if not invoice_dir.exists():
        return None

    invoices = list(invoice_dir.glob("*.pdf"))
    months = set()
    for inv in invoices:
        # ファイル名パターン: 水野達也＿YYYY-MM_category.pdf
        parts = inv.stem.split("＿")
        if len(parts) >= 2:
            months.add(parts[1][:7])  # YYYY-MM

    kpi = {
        "total_invoices": len(invoices),
        "months_covered": sorted(months),
    }
    logger.info(f"Finance: 請求書={len(invoices)}")
    return kpi


# =====================================================
# レポート生成
# =====================================================
KPI_REPORT_PROMPT = """あなたは「南米おやじ」（パラグアイ在住の日本人フリーランサー）の経営アドバイザーです。
以下の全事業KPIデータから、日本語で簡潔な統合週次レポートを生成してください。

## レポート要件
1. **全体サマリー**: 全事業を横断した1週間の総括（3-4行）
2. **事業別KPI**: 各事業のKPIをテーブルで表示（前週比があれば増減率も）
3. **成長トレンド**: 伸びている指標と停滞している指標
4. **クロスセル機会**: 事業間でシナジーが生まれそうなポイント
5. **今週のアクションアイテム**: 優先度付きで3-5個

## 事業概要
- **ブログ** (nambei-oyaji.com): パラグアイ移住・海外生活メディア。アフィリエイト収益化
- **X (Twitter)**: @nambei_oyaji。ブログへの集客チャネル
- **eBay**: 日本の大工道具・伝統工具の海外輸出
- **フリーランス**: Upwork/Fiverr でAI翻訳・テック系ギグ
- **財務**: 全事業の請求・入金管理

## 出力形式
Markdownで出力。見出し・テーブル・箇条書きを適切に使用。"""


def generate_kpi_report(secrets, settings, all_kpi, start_date, end_date):
    """Claude APIでKPIレポートを生成"""
    api_key = secrets.get("claude_api", {}).get("api_key", "")

    data_summary = f"""## 分析期間: {start_date.strftime('%Y/%m/%d')} 〜 {end_date.strftime('%Y/%m/%d')}

### ブログKPI
{json.dumps(all_kpi.get('blog', {}), ensure_ascii=False, indent=2)}

### X (Twitter) KPI
{json.dumps(all_kpi.get('x', {}), ensure_ascii=False, indent=2)}

### eBay KPI
{json.dumps(all_kpi.get('ebay', {}), ensure_ascii=False, indent=2)}

### フリーランス KPI
{json.dumps(all_kpi.get('freelance', {}), ensure_ascii=False, indent=2)}

### 財務 KPI
{json.dumps(all_kpi.get('finance', {}), ensure_ascii=False, indent=2)}
"""

    if not api_key or "YOUR" in api_key or anthropic is None:
        logger.info("Claude API未設定。テンプレートレポートを生成")
        return generate_template_report(all_kpi, start_date, end_date)

    try:
        client = anthropic.Anthropic(api_key=api_key)
        model = settings.get("claude_api", {}).get("model", "claude-sonnet-4-6")
        response = client.messages.create(
            model=model,
            max_tokens=2048,
            system=KPI_REPORT_PROMPT,
            messages=[{"role": "user", "content": data_summary}],
        )
        return response.content[0].text
    except Exception as e:
        logger.error(f"Claude API エラー: {e}")
        return generate_template_report(all_kpi, start_date, end_date)


def generate_template_report(all_kpi, start_date, end_date):
    """テンプレートレポート（API未設定時用）"""
    now = datetime.now().strftime("%Y/%m/%d %H:%M")
    period = f"{start_date.strftime('%Y/%m/%d')} 〜 {end_date.strftime('%Y/%m/%d')}"

    sections = [f"# 全事業 週次KPIレポート ({period})\n"]
    sections.append(f"*生成: {now}*\n")

    # --- ブログ ---
    sections.append("## 1. ブログ (nambei-oyaji.com)")
    blog = all_kpi.get("blog", {})
    ga4 = blog.get("ga4")
    if ga4:
        sections.append("| 指標 | 今週 | 前週 | 増減 |")
        sections.append("|---|---|---|---|")
        for key, label in [("pageviews", "PV"), ("sessions", "セッション"), ("users", "ユーザー")]:
            curr = ga4.get(key, 0)
            prev = ga4.get(f"prev_{key}", 0)
            diff = curr - prev
            pct = f"{diff/max(prev,1)*100:+.1f}%" if prev else "-"
            sections.append(f"| {label} | {curr:,} | {prev:,} | {pct} |")
        sections.append(f"| 平均滞在時間 | {ga4.get('avg_session_duration', 0):.0f}秒 | - | - |")
        sections.append(f"| 直帰率 | {ga4.get('bounce_rate', 0):.1f}% | - | - |")
    else:
        sections.append("GA4データ未取得")
    sections.append("")

    sc = blog.get("search_console")
    if sc:
        sections.append("### Search Console")
        sections.append(f"- クリック: {sc['clicks']:,}")
        sections.append(f"- 表示回数: {sc['impressions']:,}")
        sections.append(f"- CTR: {sc['ctr']}%")
        sections.append(f"- 平均順位: {sc['position']}")
    sections.append("")

    wp = blog.get("wordpress")
    if wp:
        sections.append("### WordPress")
        sections.append(f"- 公開済み: {wp['total_published']}記事")
        sections.append(f"- 下書き: {wp['total_drafts']}記事")
        sections.append(f"- 今週新規公開: {wp['new_posts_this_week']}記事")
        for p in wp.get("new_posts", []):
            sections.append(f"  - [{p['title']}]({p['url']})")
    sections.append("")

    articles = blog.get("articles")
    if articles:
        sections.append("### 記事構成")
        sections.append(f"- 総記事数: {articles['total']}")
        sections.append(f"- 柱1（パラグアイ）: {articles['pillar1_paraguay']}記事")
        sections.append(f"- 柱2（仕事・副業）: {articles['pillar2_work']}記事")
    sections.append("")

    # --- X ---
    sections.append("## 2. X (Twitter) @nambei_oyaji")
    x = all_kpi.get("x")
    if x:
        sections.append(f"| 指標 | 値 |")
        sections.append(f"|---|---|")
        sections.append(f"| 投稿数 | {x['posts_count']} |")
        sections.append(f"| いいね | {x['likes']} |")
        sections.append(f"| RT | {x['retweets']} |")
        sections.append(f"| リプライ | {x['replies']} |")
        if x['impressions'] > 0:
            sections.append(f"| インプレッション | {x['impressions']:,} |")
            sections.append(f"| エンゲージメント率 | {x['engagement_rate']}% |")
    else:
        sections.append("X投稿ログなし")
    sections.append("")

    # --- eBay ---
    sections.append("## 3. eBay輸出")
    ebay = all_kpi.get("ebay")
    if ebay:
        sections.append(f"- リサーチ商品数: {ebay['total_products_tracked']}")
        sections.append(f"- カテゴリ数: {ebay['categories']}")
        sections.append(f"- カテゴリ: {', '.join(ebay['category_list'])}")
    else:
        sections.append("データなし")
    sections.append("")

    # --- Freelance ---
    sections.append("## 4. フリーランス (Upwork/Fiverr)")
    fl = all_kpi.get("freelance")
    if fl:
        sections.append(f"- リサーチ文書: {fl['research_docs']}本")
        sections.append(f"- Gig定義: {fl['gigs_defined']}件")
    else:
        sections.append("データなし")
    sections.append("")

    # --- Finance ---
    sections.append("## 5. 財務")
    fin = all_kpi.get("finance")
    if fin:
        sections.append(f"- 請求書: {fin['total_invoices']}件")
        sections.append(f"- 対象月: {', '.join(fin['months_covered'])}")
    else:
        sections.append("データなし")
    sections.append("")

    sections.append("---")
    sections.append("*このレポートは all_business_kpi.py により自動生成されました*")

    return "\n".join(sections)


# =====================================================
# Discord 通知
# =====================================================
def notify_discord(settings, report_summary):
    """Discord Webhook でKPIサマリーを通知"""
    webhook_url = settings.get("discord", {}).get("webhook_url", "")
    if not webhook_url or "YOUR" in webhook_url:
        return

    try:
        # エンベッド形式で送信
        # レポートから主要数値を抽出してサマリー作成
        content = report_summary[:1800] if len(report_summary) > 1800 else report_summary
        kpi_url = "https://github.com/tmizuno27/claude-code/blob/main/nambei-oyaji.com/outputs/reports/daily-business-dashboard.html"
        payload = {
            "embeds": [{
                "title": "📊 全事業 週次KPIレポート",
                "url": kpi_url,
                "description": f"```\n{content}\n```",
                "color": 0x3498DB,
                "timestamp": datetime.now().isoformat(),
            }]
        }
        requests.post(webhook_url, json=payload, timeout=10)
        logger.info("Discord 通知送信完了")
    except Exception as e:
        logger.warning(f"Discord 通知失敗: {e}")


def main():
    parser = argparse.ArgumentParser(description="全事業統合 週次KPIレポート")
    parser.add_argument("--weeks", type=int, default=1, help="分析する週数（デフォルト: 1）")
    parser.add_argument("--no-discord", action="store_true", help="Discord通知を送らない")
    args = parser.parse_args()

    logger.info("=== 全事業KPIレポート生成開始 ===")

    secrets = load_secrets()
    settings = load_settings()

    # 分析期間
    end_date = datetime.now() - timedelta(days=1)
    start_date = end_date - timedelta(days=7 * args.weeks - 1)

    # データ収集
    logger.info("--- ブログKPI取得中 ---")
    blog_kpi = fetch_blog_kpi(settings, secrets, start_date, end_date)

    logger.info("--- X KPI取得中 ---")
    x_kpi = fetch_x_kpi(start_date, end_date)

    logger.info("--- eBay KPI取得中 ---")
    ebay_kpi = fetch_ebay_kpi()

    logger.info("--- フリーランスKPI取得中 ---")
    freelance_kpi = fetch_freelance_kpi()

    logger.info("--- 財務KPI取得中 ---")
    finance_kpi = fetch_finance_kpi()

    all_kpi = {
        "blog": blog_kpi,
        "x": x_kpi,
        "ebay": ebay_kpi,
        "freelance": freelance_kpi,
        "finance": finance_kpi,
    }

    # レポート生成
    logger.info("--- レポート生成中 ---")
    report = generate_kpi_report(secrets, settings, all_kpi, start_date, end_date)

    # 保存
    KPI_DIR.mkdir(parents=True, exist_ok=True)
    date_str = datetime.now().strftime("%Y-%m-%d")
    report_path = KPI_DIR / f"all-business-kpi-{date_str}.md"
    report_path.write_text(report, encoding="utf-8")
    logger.info(f"レポート保存: {report_path}")

    # KPIデータも保存（JSON）
    json_path = KPI_DIR / f"all-business-kpi-{date_str}.json"
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump({
            "period": {"start": start_date.strftime("%Y-%m-%d"), "end": end_date.strftime("%Y-%m-%d")},
            "generated": datetime.now().isoformat(),
            "kpi": {k: v for k, v in all_kpi.items() if v is not None},
        }, f, ensure_ascii=False, indent=2)

    # Discord 通知
    if not args.no_discord:
        summary_lines = report.split("\n")[:25]
        notify_discord(settings, "\n".join(summary_lines))

    # コンソール出力（先頭20行）
    for line in report.split("\n")[:20]:
        print(line)

    logger.info("=== 全事業KPIレポート生成完了 ===")


if __name__ == "__main__":
    main()
