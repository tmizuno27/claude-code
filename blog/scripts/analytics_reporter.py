#!/usr/bin/env python3
"""
週次分析レポート生成スクリプト

GA4、Search Console、Gumroad等のデータを集約し、
Claude APIで日本語の週次レポートを自動生成する。
"""

import json
import logging
import sys
from datetime import datetime, timedelta
from pathlib import Path

import requests

# ログ設定
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# プロジェクトルート
PROJECT_ROOT = Path(__file__).parent.parent
CONFIG_PATH = PROJECT_ROOT / "config" / "settings.json"
REPORTS_DIR = PROJECT_ROOT / "outputs" / "reports"
MANUAL_INPUT = PROJECT_ROOT / "inputs" / "weekly-revenue.md"


def load_config():
    """設定ファイルを読み込む"""
    with open(CONFIG_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


def fetch_ga4_data(config):
    """GA4データを取得する（API設定済みの場合）"""
    ga_config = config.get("google_analytics", {})
    property_id = ga_config.get("property_id", "")

    if "YOUR" in property_id or not property_id:
        return {
            "status": "未設定",
            "message": "GA4が未設定です。docs/setup-guide.md を参照してセットアップしてください。",
            "sessions": 0,
            "pageviews": 0,
            "users": 0,
            "top_pages": [],
            "traffic_sources": []
        }

    try:
        from google.analytics.data_v1beta import BetaAnalyticsDataClient
        from google.analytics.data_v1beta.types import (
            DateRange, Dimension, Metric, RunReportRequest
        )

        client = BetaAnalyticsDataClient()
        today = datetime.now()
        week_ago = today - timedelta(days=7)
        two_weeks_ago = today - timedelta(days=14)

        # 今週のデータ
        request = RunReportRequest(
            property=f"properties/{property_id}",
            date_ranges=[DateRange(
                start_date=week_ago.strftime("%Y-%m-%d"),
                end_date=today.strftime("%Y-%m-%d")
            )],
            metrics=[
                Metric(name="sessions"),
                Metric(name="screenPageViews"),
                Metric(name="activeUsers")
            ]
        )
        response = client.run_report(request)

        sessions = int(response.rows[0].metric_values[0].value) if response.rows else 0
        pageviews = int(response.rows[0].metric_values[1].value) if response.rows else 0
        users = int(response.rows[0].metric_values[2].value) if response.rows else 0

        return {
            "status": "取得成功",
            "sessions": sessions,
            "pageviews": pageviews,
            "users": users,
            "top_pages": [],
            "traffic_sources": []
        }

    except ImportError:
        return {
            "status": "ライブラリ未インストール",
            "message": "pip install google-analytics-data を実行してください。",
            "sessions": 0, "pageviews": 0, "users": 0,
            "top_pages": [], "traffic_sources": []
        }
    except Exception as e:
        return {
            "status": "エラー",
            "message": str(e),
            "sessions": 0, "pageviews": 0, "users": 0,
            "top_pages": [], "traffic_sources": []
        }


def fetch_gumroad_data(config):
    """Gumroad売上データを取得する"""
    api_key = config.get("gumroad", {}).get("api_key", "")

    if "YOUR" in api_key or not api_key:
        return {
            "status": "未設定",
            "message": "Gumroad APIキーが未設定です。",
            "total_revenue": 0,
            "products": []
        }

    try:
        url = "https://api.gumroad.com/v2/sales"
        today = datetime.now()
        week_ago = today - timedelta(days=7)

        params = {
            "access_token": api_key,
            "after": week_ago.strftime("%Y-%m-%d"),
            "before": today.strftime("%Y-%m-%d")
        }

        response = requests.get(url, params=params, timeout=30)
        if response.status_code == 200:
            data = response.json()
            sales = data.get("sales", [])
            total = sum(float(s.get("price", 0)) for s in sales)
            return {
                "status": "取得成功",
                "total_revenue": total,
                "sales_count": len(sales),
                "products": sales
            }
        else:
            return {
                "status": "エラー",
                "message": f"API応答: {response.status_code}",
                "total_revenue": 0, "products": []
            }

    except Exception as e:
        return {
            "status": "エラー",
            "message": str(e),
            "total_revenue": 0, "products": []
        }


def read_manual_revenue():
    """手動入力の売上データを読み込む（note、ココナラ等）"""
    if MANUAL_INPUT.exists():
        return MANUAL_INPUT.read_text(encoding="utf-8")
    return "手動入力データなし"


def load_wp_log():
    """WordPress投稿履歴を読み込む"""
    wp_log_path = PROJECT_ROOT / "published" / "wordpress-log.json"
    if wp_log_path.exists():
        with open(wp_log_path, "r", encoding="utf-8") as f:
            return json.load(f)
    return {"posts": []}


def generate_report_with_claude(config, ga4_data, gumroad_data, manual_revenue, wp_log):
    """Claude APIでレポートを生成する"""
    api_key = config.get("claude_api", {}).get("api_key", "")

    if "YOUR" in api_key or not api_key:
        # APIキー未設定の場合はテンプレートレポートを生成
        return generate_template_report(ga4_data, gumroad_data, manual_revenue, wp_log)

    try:
        import anthropic

        client = anthropic.Anthropic(api_key=api_key)
        model = config.get("claude_api", {}).get("model", "claude-sonnet-4-6")

        # エージェント定義を読み込む
        agent_path = PROJECT_ROOT / "docs" / "analytics-agent.md"
        system_prompt = ""
        if agent_path.exists():
            system_prompt = agent_path.read_text(encoding="utf-8")

        today = datetime.now()
        week_ago = today - timedelta(days=7)

        data_summary = f"""
## 収集データ（{week_ago.strftime('%Y/%m/%d')}〜{today.strftime('%Y/%m/%d')}）

### GA4データ
{json.dumps(ga4_data, ensure_ascii=False, indent=2)}

### Gumroad売上データ
{json.dumps(gumroad_data, ensure_ascii=False, indent=2)}

### 手動入力データ（note/ココナラ等）
{manual_revenue}

### WordPress投稿状況
公開済み記事数: {len(wp_log.get('posts', []))}
"""

        message = client.messages.create(
            model=model,
            max_tokens=2000,
            system=system_prompt if system_prompt else "あなたはビジネス分析の専門家です。",
            messages=[{
                "role": "user",
                "content": f"以下のデータから週次レポートを生成してください。\n\n{data_summary}"
            }]
        )

        return message.content[0].text

    except ImportError:
        logger.warning("anthropicライブラリ未インストール。テンプレートレポートを生成します。")
        return generate_template_report(ga4_data, gumroad_data, manual_revenue, wp_log)
    except Exception as e:
        logger.error(f"Claude API呼び出しエラー: {e}")
        return generate_template_report(ga4_data, gumroad_data, manual_revenue, wp_log)


def generate_template_report(ga4_data, gumroad_data, manual_revenue, wp_log):
    """テンプレートベースのレポート生成（API未設定時）"""
    today = datetime.now()
    week_ago = today - timedelta(days=7)

    report = f"""# 週次レポート（{week_ago.strftime('%Y/%m/%d')}〜{today.strftime('%Y/%m/%d')}）

## サマリー
レポート自動生成。API設定完了後、Claude AIによる詳細分析が有効になります。

## トラフィック
| 指標 | 今週 | ステータス |
|------|------|------------|
| セッション | {ga4_data.get('sessions', 'N/A')} | {ga4_data.get('status', '未設定')} |
| PV | {ga4_data.get('pageviews', 'N/A')} | - |
| ユーザー | {ga4_data.get('users', 'N/A')} | - |

## 収益
| 収益源 | 今週 | ステータス |
|--------|------|------------|
| Gumroad | {gumroad_data.get('total_revenue', 0)}円 | {gumroad_data.get('status', '未設定')} |

### 手動入力データ
{manual_revenue}

## WordPress
- 公開済み記事数: {len(wp_log.get('posts', []))}

## 来週のアクション
1. 各API設定を完了させてデータ取得を自動化する
2. 週3記事の公開ペースを維持する
3. デジタル商品のアイデアを検討する

---
*このレポートは自動生成されました。（{today.strftime('%Y/%m/%d %H:%M')}）*
"""
    return report


def main():
    """メイン処理"""
    logger.info("=== 週次分析レポート生成開始 ===")

    try:
        config = load_config()
    except FileNotFoundError:
        logger.error(f"設定ファイルが見つかりません: {CONFIG_PATH}")
        sys.exit(1)

    # データ収集
    logger.info("GA4データ取得中...")
    ga4_data = fetch_ga4_data(config)

    logger.info("Gumroadデータ取得中...")
    gumroad_data = fetch_gumroad_data(config)

    logger.info("手動入力データ読み込み中...")
    manual_revenue = read_manual_revenue()

    logger.info("WordPress投稿履歴読み込み中...")
    wp_log = load_wp_log()

    # レポート生成
    logger.info("レポート生成中...")
    report = generate_report_with_claude(config, ga4_data, gumroad_data, manual_revenue, wp_log)

    # 保存
    REPORTS_DIR.mkdir(parents=True, exist_ok=True)
    today = datetime.now().strftime("%Y-%m-%d")
    report_path = REPORTS_DIR / f"weekly-{today}.md"
    report_path.write_text(report, encoding="utf-8")

    logger.info(f"\nレポート保存先: {report_path}")
    logger.info("=== レポート生成完了 ===")

    # レポートの先頭を表示
    lines = report.split('\n')[:10]
    for line in lines:
        print(line)


if __name__ == "__main__":
    main()
