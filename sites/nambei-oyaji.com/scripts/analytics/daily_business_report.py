#!/usr/bin/env python3
"""
日次ビジネス総合レポート生成スクリプト

全事業（3ブログサイト、RapidAPI、Apify、pSEO、n8nテンプレート）のデータを集約し、
日次レポートをMarkdown形式で自動生成する。
"""

import json
import logging
import re
import sys
import threading
from datetime import datetime, timedelta
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, TimeoutError as FuturesTimeoutError

import requests

# ログ設定
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# プロジェクトルート（sites/nambei-oyaji.com/scripts/analytics/ から3つ上）
PROJECT_ROOT = Path(__file__).parent.parent.parent
WORKSPACE_ROOT = PROJECT_ROOT.parent.parent  # claude-code/ (sites/ の1つ上)
REPORTS_DIR = PROJECT_ROOT / "outputs" / "reports"

# 各サイトの設定ファイルパス
SITE_CONFIGS = {
    "nambei-oyaji.com": {
        "config_path": WORKSPACE_ROOT / "sites" / "nambei-oyaji.com" / "config" / "settings.json",
        "secrets_path": WORKSPACE_ROOT / "sites" / "nambei-oyaji.com" / "config" / "secrets.json",
        "published_dir": WORKSPACE_ROOT / "sites" / "nambei-oyaji.com" / "published",
        "display_name": "南米おやじの海外生活ラボ",
    },
    "otona-match.com": {
        "config_path": WORKSPACE_ROOT / "sites" / "otona-match.com" / "config" / "settings.json",
        "secrets_path": WORKSPACE_ROOT / "sites" / "otona-match.com" / "config" / "secrets.json",
        "published_dir": WORKSPACE_ROOT / "sites" / "otona-match.com" / "published",
        "display_name": "大人のマッチングナビ",
    },
    "sim-hikaku.online": {
        "config_path": WORKSPACE_ROOT / "sites" / "sim-hikaku.online" / "config" / "settings.json",
        "secrets_path": WORKSPACE_ROOT / "sites" / "sim-hikaku.online" / "config" / "secrets.json",
        "published_dir": WORKSPACE_ROOT / "sites" / "sim-hikaku.online" / "published",
        "display_name": "SIM比較ナビ",
    },
}

# その他パス
RAPIDAPI_STATS_PATH = WORKSPACE_ROOT / "products" / "api-services" / "rapidapi-stats.json"
PSEO_DIR = WORKSPACE_ROOT / "saas" / "pseo-saas"
N8N_DIR = WORKSPACE_ROOT / "products" / "n8n-templates"
AUTO_SYNC_LOG = WORKSPACE_ROOT / "logs" / "auto-sync.log"
APIFY_AUTH_PATH = Path.home() / ".apify" / "auth.json"


def load_config(config_path: Path) -> dict:
    """設定ファイルを読み込む"""
    if not config_path.exists():
        logger.warning(f"設定ファイルが見つかりません: {config_path}")
        return {}
    with open(config_path, "r", encoding="utf-8") as f:
        return json.load(f)


def load_secrets(secrets_path: Path) -> dict:
    """シークレットファイルを読み込む"""
    if not secrets_path.exists():
        return {}
    try:
        with open(secrets_path, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return {}


# ─────────────────────────────────────────────
# 1. ブログ3サイト データ取得
# ─────────────────────────────────────────────

def _fetch_ga4_data_inner(property_id: str, credentials_file: Path) -> dict:
    """GA4データを取得する内部関数（タイムアウトラッパーから呼ばれる）"""
    from google.analytics.data_v1beta import BetaAnalyticsDataClient
    from google.analytics.data_v1beta.types import DateRange, Metric, RunReportRequest
    import os

    if credentials_file.exists():
        os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = str(credentials_file)

    client = BetaAnalyticsDataClient()
    today = datetime.now()
    yesterday = today - timedelta(days=1)

    request = RunReportRequest(
        property=f"properties/{property_id}",
        date_ranges=[DateRange(
            start_date=yesterday.strftime("%Y-%m-%d"),
            end_date=today.strftime("%Y-%m-%d")
        )],
        metrics=[
            Metric(name="screenPageViews"),
            Metric(name="activeUsers"),
        ]
    )
    response = client.run_report(request, timeout=30)
    if response.rows:
        return {
            "status": "取得成功",
            "pageviews": int(response.rows[0].metric_values[0].value),
            "users": int(response.rows[0].metric_values[1].value),
        }
    return {"status": "取得成功", "pageviews": 0, "users": 0}


def fetch_ga4_data_for_site(property_id: str, credentials_file: Path) -> dict:
    """GA4データを取得する（1日分）。10秒でタイムアウト"""
    if not property_id or "YOUR" in str(property_id):
        return {"status": "未設定", "pageviews": 0, "users": 0}

    try:
        with ThreadPoolExecutor(max_workers=1) as executor:
            future = executor.submit(_fetch_ga4_data_inner, property_id, credentials_file)
            return future.result(timeout=10)
    except FuturesTimeoutError:
        logger.warning(f"GA4データ取得タイムアウト: property={property_id}")
        return {"status": "タイムアウト", "pageviews": 0, "users": 0}
    except ImportError:
        return {"status": "ライブラリ未インストール", "pageviews": 0, "users": 0}
    except Exception as e:
        return {"status": f"エラー: {e}", "pageviews": 0, "users": 0}


def fetch_search_console_data(site_url: str, credentials_file: Path) -> dict:
    """Search Consoleデータを取得する（昨日分）"""
    if not site_url:
        return {"status": "未設定", "impressions": 0, "clicks": 0}

    try:
        from google.oauth2 import service_account
        from googleapiclient.discovery import build

        if not credentials_file.exists():
            return {"status": "認証ファイルなし", "impressions": 0, "clicks": 0}

        scopes = ["https://www.googleapis.com/auth/webmasters.readonly"]
        credentials = service_account.Credentials.from_service_account_file(
            str(credentials_file), scopes=scopes
        )
        service = build("webmasters", "v3", credentials=credentials, cache_discovery=False)

        today = datetime.now()
        yesterday = (today - timedelta(days=1)).strftime("%Y-%m-%d")
        three_days_ago = (today - timedelta(days=3)).strftime("%Y-%m-%d")

        response = service.searchanalytics().query(
            siteUrl=site_url,
            body={
                "startDate": three_days_ago,
                "endDate": yesterday,
                "rowLimit": 1,
            }
        ).execute()

        rows = response.get("rows", [])
        if rows:
            return {
                "status": "取得成功",
                "impressions": int(rows[0].get("impressions", 0)),
                "clicks": int(rows[0].get("clicks", 0)),
            }
        return {"status": "取得成功", "impressions": 0, "clicks": 0}

    except ImportError:
        return {"status": "ライブラリ未インストール", "impressions": 0, "clicks": 0}
    except Exception as e:
        return {"status": f"エラー: {e}", "impressions": 0, "clicks": 0}


def fetch_wp_post_count(rest_api_url: str, secrets: dict) -> dict:
    """WordPress REST APIで公開済み記事数を取得する"""
    if not rest_api_url or "SEE" in str(rest_api_url):
        return {"status": "未設定", "post_count": 0}

    try:
        username = secrets.get("wordpress", {}).get("username", "")
        app_password = secrets.get("wordpress", {}).get("app_password", "")

        if not username or not app_password:
            return {"status": "認証情報なし", "post_count": 0}

        url = f"{rest_api_url}/posts"
        params = {"status": "publish", "per_page": 1, "_fields": "id"}
        resp = requests.get(
            url, params=params,
            auth=(username, app_password),
            timeout=15
        )
        if resp.status_code == 200:
            total = int(resp.headers.get("X-WP-Total", 0))
            return {"status": "取得成功", "post_count": total}
        else:
            return {"status": f"HTTP {resp.status_code}", "post_count": 0}

    except Exception as e:
        return {"status": f"エラー: {e}", "post_count": 0}


def collect_blog_data() -> list:
    """3サイト分のブログデータをまとめて収集する"""
    results = []
    for site_key, site_meta in SITE_CONFIGS.items():
        logger.info(f"  {site_key} データ取得中...")
        config = load_config(site_meta["config_path"])
        secrets = load_secrets(site_meta["secrets_path"])

        # 共通credentials（nambei-oyaji.com配下のga4-credentials.jsonを全サイトで共用）
        shared_creds = WORKSPACE_ROOT / "sites" / "nambei-oyaji.com" / "config" / "ga4-credentials.json"

        ga4_cfg = config.get("google_analytics", {})
        property_id = ga4_cfg.get("property_id", "")
        ga4_creds = site_meta["config_path"].parent / ga4_cfg.get("credentials_file", "ga4-credentials.json")
        if not ga4_creds.exists():
            ga4_creds = shared_creds

        gsc_cfg = config.get("search_console", {})
        gsc_site_url = gsc_cfg.get("site_url", "")
        gsc_creds = site_meta["config_path"].parent / gsc_cfg.get("credentials_file", "gsc-credentials.json")

        wp_cfg = config.get("wordpress", {})
        rest_api_url = wp_cfg.get("rest_api_url", "")

        # GA4データ取得（タイムアウト付き）
        ga4_data = {"status": "未設定", "pageviews": 0, "users": 0}
        if property_id and ga4_creds.exists():
            try:
                with ThreadPoolExecutor(max_workers=1) as ex:
                    future = ex.submit(fetch_ga4_data_for_site, property_id, ga4_creds)
                    ga4_data = future.result(timeout=20)
            except Exception as e:
                ga4_data = {"status": f"タイムアウト: {e}", "pageviews": 0, "users": 0}
                logger.warning(f"  GA4 timeout for {site_key}: {e}")

        # GSCデータ取得（タイムアウト付き）
        gsc_site = gsc_site_url or f"https://{site_key}/"
        gsc_creds_file = ga4_creds if ga4_creds.exists() else gsc_creds
        gsc_data = {"status": "未設定", "impressions": 0, "clicks": 0}
        if gsc_creds_file.exists():
            try:
                with ThreadPoolExecutor(max_workers=1) as ex:
                    future = ex.submit(fetch_search_console_data, gsc_site, gsc_creds_file)
                    gsc_data = future.result(timeout=20)
            except Exception as e:
                gsc_data = {"status": f"タイムアウト: {e}", "impressions": 0, "clicks": 0}
                logger.warning(f"  GSC timeout for {site_key}: {e}")

        wp_data = fetch_wp_post_count(rest_api_url, secrets)

        results.append({
            "site": site_key,
            "display_name": site_meta["display_name"],
            "url": wp_cfg.get("url", site_key),
            "ga4": ga4_data,
            "gsc": gsc_data,
            "wp": wp_data,
        })
    return results


# ─────────────────────────────────────────────
# 2. RapidAPI データ
# ─────────────────────────────────────────────

def collect_rapidapi_data() -> dict:
    """RapidAPIの統計データを収集する"""
    api_count = 0
    try:
        api_dirs = [
            d for d in (WORKSPACE_ROOT / "products" / "api-services").iterdir()
            if d.is_dir() and d.name[0].isdigit()
        ]
        api_count = len(api_dirs)
    except Exception:
        pass

    if RAPIDAPI_STATS_PATH.exists():
        try:
            with open(RAPIDAPI_STATS_PATH, "r", encoding="utf-8") as f:
                stats = json.load(f)
            return {
                "status": "データあり",
                "api_count": api_count,
                "stats": stats,
            }
        except Exception as e:
            return {
                "status": f"読み込みエラー: {e}",
                "api_count": api_count,
                "stats": {},
            }

    return {
        "status": "stats未設定（rapidapi-stats.json なし）",
        "api_count": api_count,
        "stats": {},
    }


# ─────────────────────────────────────────────
# 3. Apify データ
# ─────────────────────────────────────────────

def collect_apify_data() -> dict:
    """Apify APIでActorの実行統計を取得する"""
    if not APIFY_AUTH_PATH.exists():
        return {"status": "認証ファイルなし", "actors": []}

    try:
        with open(APIFY_AUTH_PATH, "r", encoding="utf-8") as f:
            auth = json.load(f)
        token = auth.get("token", "")
        if not token:
            return {"status": "トークンなし", "actors": []}

        url = "https://api.apify.com/v2/acts"
        params = {"token": token, "my": "true", "limit": 100}
        resp = requests.get(url, params=params, timeout=30)

        if resp.status_code != 200:
            return {"status": f"APIエラー: HTTP {resp.status_code}", "actors": []}

        data = resp.json()
        items = data.get("data", {}).get("items", [])

        actors = []
        for actor in items:
            actor_id = actor.get("id", "")
            name = actor.get("name", "不明")
            stats = actor.get("stats", {})

            # 最新の実行情報を取得
            last_run_info = {"status": "N/A", "date": "N/A"}
            try:
                runs_url = f"https://api.apify.com/v2/acts/{actor_id}/runs"
                runs_params = {"token": token, "limit": 1, "desc": "true"}
                runs_resp = requests.get(runs_url, params=runs_params, timeout=15)
                if runs_resp.status_code == 200:
                    runs_data = runs_resp.json()
                    runs_items = runs_data.get("data", {}).get("items", [])
                    if runs_items:
                        last_run = runs_items[0]
                        last_run_info = {
                            "status": last_run.get("status", "N/A"),
                            "date": last_run.get("finishedAt", last_run.get("startedAt", "N/A"))[:10]
                            if last_run.get("finishedAt") or last_run.get("startedAt")
                            else "N/A",
                        }
            except Exception:
                pass

            actors.append({
                "name": name,
                "total_runs": stats.get("totalRuns", 0),
                "last_run_status": last_run_info["status"],
                "last_run_date": last_run_info["date"],
            })

        return {"status": "取得成功", "actors": actors}

    except Exception as e:
        return {"status": f"エラー: {e}", "actors": []}


# ─────────────────────────────────────────────
# 4. pSEO サイト
# ─────────────────────────────────────────────

def collect_pseo_data() -> dict:
    """pSEOサイトのステータスを確認する"""
    if not PSEO_DIR.exists():
        return {"status": "ディレクトリなし", "page_count": 0, "deployed": False}

    # 静的ページ数をカウント（site/out を優先。0件なら次のディレクトリへ）
    page_count = 0
    for subdir in ["site/out", "out", "site", "public"]:
        target = PSEO_DIR / subdir
        if target.exists():
            try:
                html_files = list(target.rglob("*.html"))
                if html_files:
                    page_count = len(html_files)
                    break
            except Exception:
                pass

    # デプロイ確認（既知URLへのHTTPリクエスト）
    deployed = False
    deploy_url = ""
    try:
        # pseo-saas/CLAUDE.md や config から URL を探す
        config_candidates = [
            PSEO_DIR / "config" / "settings.json",
            PSEO_DIR / "docs" / "deploy-info.json",
        ]
        for cp in config_candidates:
            if cp.exists():
                with open(cp, "r", encoding="utf-8") as f:
                    cfg = json.load(f)
                deploy_url = cfg.get("deploy_url", cfg.get("url", ""))
                if deploy_url:
                    break

        # フォールバック: 既知のVercel URL
        if not deploy_url:
            deploy_url = "https://ai-tool-compare-nu.vercel.app"

        if deploy_url:
            resp = requests.head(deploy_url, timeout=10, allow_redirects=True)
            deployed = resp.status_code < 400
    except Exception:
        pass

    return {
        "status": "デプロイ未完" if not deployed else "稼働中",
        "page_count": page_count,
        "deployed": deployed,
        "deploy_url": deploy_url or "未設定",
    }


# ─────────────────────────────────────────────
# 5. n8nテンプレート
# ─────────────────────────────────────────────

def collect_n8n_data() -> dict:
    """n8nテンプレートのステータスを確認する"""
    template_count = 0
    if N8N_DIR.exists():
        try:
            json_files = list(N8N_DIR.rglob("*.json"))
            # ワークフローファイルのみカウント（設定ファイル除外）
            template_count = sum(
                1 for f in json_files
                if "workflow" in f.name.lower() or f.parent.name.startswith(("0", "1", "2", "3"))
            )
        except Exception:
            pass

    return {
        "status": "Stripe KYC認証問題により停止中",
        "template_count": template_count,
        "platform": "Gumroad（9/10本出品済み）",
        "note": "Stripe KYC認証が解決次第、販売再開予定",
    }


# ─────────────────────────────────────────────
# 5.5 X (Twitter) API データ取得
# ─────────────────────────────────────────────

def collect_x_data() -> dict:
    """X APIからフォロワー数・ツイート数を取得する"""
    x_creds_path = WORKSPACE_ROOT / "sites" / "nambei-oyaji.com" / "config" / "x-credentials.json"
    if not x_creds_path.exists():
        return {"status": "認証ファイルなし", "followers": 0, "tweets": 0}

    try:
        import hmac, hashlib, base64, time, urllib.parse

        with open(x_creds_path, encoding="utf-8") as f:
            creds = json.load(f)

        def make_oauth_header(method, url, params={}):
            oauth = {
                'oauth_consumer_key': creds['api_key'],
                'oauth_nonce': str(int(time.time() * 1000)),
                'oauth_signature_method': 'HMAC-SHA1',
                'oauth_timestamp': str(int(time.time())),
                'oauth_token': creds['access_token'],
                'oauth_version': '1.0'
            }
            all_params = {**oauth, **params}
            sorted_params = '&'.join(
                f'{urllib.parse.quote(k, safe="")}'
                f'={urllib.parse.quote(str(v), safe="")}'
                for k, v in sorted(all_params.items())
            )
            base_string = (
                f'{method}'
                f'&{urllib.parse.quote(url, safe="")}'
                f'&{urllib.parse.quote(sorted_params, safe="")}'
            )
            signing_key = (
                f'{urllib.parse.quote(creds["api_key_secret"], safe="")}'
                f'&{urllib.parse.quote(creds["access_token_secret"], safe="")}'
            )
            sig = base64.b64encode(
                hmac.new(signing_key.encode(), base_string.encode(), hashlib.sha1).digest()
            ).decode()
            oauth['oauth_signature'] = sig
            return 'OAuth ' + ', '.join(
                f'{k}="{urllib.parse.quote(v, safe="")}"'
                for k, v in sorted(oauth.items())
            )

        url = 'https://api.twitter.com/2/users/me'
        params = {'user.fields': 'public_metrics'}
        auth = make_oauth_header('GET', url, params)
        r = requests.get(url, headers={'Authorization': auth}, params=params, timeout=15)

        if r.status_code == 200:
            data = r.json()['data']
            m = data['public_metrics']
            return {
                "status": "接続済み",
                "followers": m['followers_count'],
                "following": m['following_count'],
                "tweets": m['tweet_count'],
                "username": data.get('username', 'nambei_oyaji'),
            }
        return {"status": f"HTTPエラー {r.status_code}", "followers": 0, "tweets": 0}

    except Exception as e:
        logger.warning(f"  X API error: {e}")
        return {"status": f"エラー: {e}", "followers": 0, "tweets": 0}


# ─────────────────────────────────────────────
# 6. 定期タスク健全性チェック
# ─────────────────────────────────────────────

def collect_task_health() -> dict:
    """定期タスクの健全性をログから確認する"""
    if not AUTO_SYNC_LOG.exists():
        return {"status": "ログファイルなし", "recent_entries": 0, "last_sync": "N/A"}

    try:
        content = AUTO_SYNC_LOG.read_text(encoding="utf-8", errors="replace")
        lines = [l for l in content.strip().splitlines() if l.strip()]
        recent = lines[-20:] if len(lines) >= 20 else lines

        # 最後の同期日時を探す
        last_sync = "N/A"
        for line in reversed(recent):
            if "push" in line.lower() or "sync" in line.lower() or "commit" in line.lower():
                # 行頭のタイムスタンプを取得
                parts = line.split()
                if len(parts) >= 2:
                    last_sync = f"{parts[0]} {parts[1]}" if len(parts[1]) >= 5 else parts[0]
                break

        # 直近1時間のエントリー数
        now = datetime.now()
        one_hour_ago = now - timedelta(hours=1)
        recent_count = 0
        for line in lines[-60:]:
            try:
                # 典型的なログ形式: "2026-03-16 10:30:xx ..."
                parts = line.split()
                if len(parts) >= 2:
                    ts_str = f"{parts[0]} {parts[1][:8]}"
                    ts = datetime.strptime(ts_str, "%Y-%m-%d %H:%M:%S")
                    if ts >= one_hour_ago:
                        recent_count += 1
            except Exception:
                pass

        return {
            "status": "正常" if len(lines) > 0 else "エントリーなし",
            "total_entries": len(lines),
            "recent_entries_1h": recent_count,
            "last_sync": last_sync,
            "last_lines": recent[-3:],
        }

    except Exception as e:
        return {"status": f"読み込みエラー: {e}", "recent_entries": 0, "last_sync": "N/A"}


# ─────────────────────────────────────────────
# レポート生成
# ─────────────────────────────────────────────

def generate_executive_summary(blog_data: list, rapidapi_data: dict,
                                apify_data: dict, config: dict) -> str:
    """Claude APIで経営サマリーを生成する（APIキー未設定時はテンプレート）"""
    api_key = config.get("claude_api", {}).get("api_key", "")

    if not api_key or "SEE" in api_key or "YOUR" in api_key:
        # secrets.json から読む
        secrets = load_secrets(PROJECT_ROOT / "config" / "secrets.json")
        api_key = secrets.get("claude_api", {}).get("api_key", "")

    if not api_key or "YOUR" in api_key:
        return _template_summary(blog_data)

    try:
        import anthropic

        client = anthropic.Anthropic(api_key=api_key)
        model = config.get("claude_api", {}).get("model", "claude-sonnet-4-6")

        blog_summary = "\n".join([
            f"- {d['display_name']}({d['site']}): "
            f"PV={d['ga4'].get('pageviews', 'N/A')}, "
            f"ユーザー={d['ga4'].get('users', 'N/A')}, "
            f"記事数={d['wp'].get('post_count', 'N/A')}"
            for d in blog_data
        ])
        apify_summary = f"Actorx{len(apify_data.get('actors', []))}件"
        rapidapi_summary = f"API x{rapidapi_data.get('api_count', 0)}本"

        prompt = f"""以下のデータから3行の経営エグゼクティブサマリーを日本語で生成してください。
箇条書き3点（強み・懸念・今日のアクション）でまとめてください。

データ:
ブログ3サイト:
{blog_summary}

RapidAPI: {rapidapi_summary}（{rapidapi_data.get('status')}）
Apify: {apify_summary}（{apify_data.get('status')}）
"""

        message = client.messages.create(
            model=model,
            max_tokens=500,
            timeout=30.0,
            system="あなたはマルチ事業運営のビジネスアナリストです。簡潔に要点をまとめてください。",
            messages=[{"role": "user", "content": prompt}]
        )
        return message.content[0].text

    except ImportError:
        logger.warning("anthropicライブラリ未インストール。テンプレートサマリーを使用します。")
        return _template_summary(blog_data)
    except Exception as e:
        logger.error(f"Claude API呼び出しエラー: {e}")
        return _template_summary(blog_data)


def _template_summary(blog_data: list) -> str:
    total_posts = sum(d["wp"].get("post_count", 0) for d in blog_data)
    total_pv = sum(d["ga4"].get("pageviews", 0) for d in blog_data)
    return (
        f"- **強み**: 3サイト合計{total_posts}記事公開済み、本日PV合計{total_pv}PV\n"
        f"- **懸念**: GA4/GSC未設定サイトあり（データ取得を要設定）\n"
        f"- **今日のアクション**: 各サイトの認証設定を確認し、データ収集を自動化する"
    )


def generate_priority_actions(blog_data: list, rapidapi_data: dict,
                              apify_data: dict, pseo_data: dict,
                              n8n_data: dict, x_data: dict,
                              config: dict) -> list:
    """Claude APIで収益最大化の優先アクションを生成する"""
    api_key = config.get("claude_api", {}).get("api_key", "")
    if not api_key or "SEE" in api_key or "YOUR" in api_key:
        secrets = load_secrets(PROJECT_ROOT / "config" / "secrets.json")
        api_key = secrets.get("claude_api", {}).get("api_key", "")
    if not api_key or "YOUR" in api_key:
        logger.warning("Claude APIキー未設定。優先アクション生成スキップ")
        return []

    try:
        import anthropic
        client = anthropic.Anthropic(api_key=api_key)
        model = config.get("claude_api", {}).get("model", "claude-sonnet-4-6")

        # 全事業データをまとめる
        blog_summary = ""
        for d in blog_data:
            blog_summary += (
                f"- {d['display_name']}({d['site']}): "
                f"記事数={d['wp'].get('post_count', 0)}, "
                f"PV(30d)={d['ga4'].get('pageviews', 0)}, "
                f"ユーザー={d['ga4'].get('users', 0)}, "
                f"GSC表示={d['gsc'].get('impressions', 0)}, "
                f"GSCクリック={d['gsc'].get('clicks', 0)}, "
                f"GA4状態={d['ga4'].get('status', 'N/A')}, "
                f"GSC状態={d['gsc'].get('status', 'N/A')}\n"
            )

        rapidapi_info = (
            f"RapidAPI: API数={rapidapi_data.get('api_count', 0)}, "
            f"状態={rapidapi_data.get('status')}, "
            f"出品済み=20/20, 月売上=$0, "
            f"料金プラン=統一済み（Basic$0/500req, Pro$5.99, Ultra$14.99, Mega$49.99/2M req）"
        )

        actors = apify_data.get("actors", [])
        apify_info = (
            f"Apify Store: Actor数={len(actors)}, "
            f"状態={apify_data.get('status')}, "
            f"PayPal payout=未設定, 月売上=$0"
        )

        pseo_info = (
            f"pSEO AIツール比較: ページ数={pseo_data.get('page_count', 0)}, "
            f"デプロイ={'済' if pseo_data.get('deployed') else '未（Vercel未設定）'}"
        )

        n8n_info = (
            f"n8nテンプレート: {n8n_data.get('template_count', 0)}本, "
            f"状態={n8n_data.get('status')}, 備考={n8n_data.get('note', '')}"
        )

        x_info = (
            f"X(Twitter): フォロワー={x_data.get('followers', 0)}, "
            f"ツイート数={x_data.get('tweets', 0)}"
        )

        prompt = f"""あなたは収益最大化の専門コンサルタントです。
以下の全事業データを分析し、今日やるべき優先アクションを
「収益インパクト÷必要な労力」が高い順に提案してください。

件数制限なし。その日のデータから本当に重要なものだけを厳選してください。
些細なことや効果の薄いアクションは含めないこと。

■ 判断基準（重要度順）:
1. 即座に収益に繋がるアクション（出品・設定するだけで課金が始まるもの）
2. 収益のボトルネック解消（データが取れない→改善できない→稼げない）
3. 低労力で高リターン（1時間以内で完了し、月1万円以上の可能性があるもの）
4. 中長期の収益基盤構築（SEO、コンテンツ拡充）

■ 現在の事業データ:
【ブログ3サイト】（収益源: アフィリエイト+AdSense）
{blog_summary}
【RapidAPI】（収益源: API課金）
{rapidapi_info}

【Apify Store】（収益源: Actor課金）
{apify_info}

【pSEOサイト】（収益源: アフィリエイト+AdSense）
{pseo_info}

【n8nテンプレート】（収益源: Gumroad販売）
{n8n_info}

【X SNS】（集客チャネル）
{x_info}

■ 月次コスト: 約¥3,700/月（ConoHa WING ¥1,452 + Claude API ~$5 + Apify $1.21 + ドメイン3件 ~¥300）
■ 現在の月間総売上: $0
■ 目標: Phase1 = ¥50,000/月（3ヶ月以内）

■ 出力フォーマット（厳密に守ること）:
各アクションを以下のJSON配列で返してください。説明文やマークダウンは不要です。JSONのみ返してください。

[
  {{"id": "英数字ハイフンのID", "title": "アクション名（20文字以内）", "reason": "なぜ収益に繋がるか（30文字以内）", "priority": "P1", "effort": "15分/1時間/半日/1日", "revenue_potential": "月○○円の可能性"}},
  ...
]

P1=今日必ずやる、P2=今日できればやる、P3=今週中
件数は自由。重要度の高いものだけを厳選し、JSON配列のみ出力してください。"""

        message = client.messages.create(
            model=model,
            max_tokens=2000,
            timeout=45.0,
            system="収益最大化に特化したビジネスコンサルタント。JSON形式で簡潔に回答する。",
            messages=[{"role": "user", "content": prompt}]
        )

        response_text = message.content[0].text.strip()
        # Extract JSON from response (handle markdown code blocks)
        json_match = re.search(r'\[.*\]', response_text, re.DOTALL)
        if json_match:
            actions = json.loads(json_match.group())
        else:
            actions = json.loads(response_text)

        logger.info(f"優先アクション {len(actions)}件 生成完了")
        return actions

    except ImportError:
        logger.warning("anthropicライブラリ未インストール。優先アクション生成スキップ")
        return []
    except Exception as e:
        logger.error(f"優先アクション生成エラー: {e}")
        return []


def update_action_status_file(actions: list):
    """action-status.json と ダッシュボードHTMLの優先アクション欄を更新"""
    today_str = datetime.now().strftime("%Y-%m-%d")
    status_path = REPORTS_DIR / "action-status.json"
    dashboard_path = REPORTS_DIR / "daily-business-dashboard.html"

    # 1. action-status.json を更新（既存の完了状態を保持）
    existing_done = {}
    if status_path.exists():
        try:
            old_data = json.loads(status_path.read_text(encoding="utf-8"))
            if old_data.get("date") == today_str:
                for old_a in old_data.get("actions", []):
                    if old_a.get("done"):
                        existing_done[old_a["id"]] = old_a.get("done_at")
        except Exception:
            pass

    status_data = {
        "date": today_str,
        "actions": [
            {
                "id": a["id"],
                "title": a["title"],
                "priority": a["priority"],
                "done": a["id"] in existing_done,
                "done_at": existing_done.get(a["id"]),
            }
            for a in actions
        ]
    }
    status_path.write_text(
        json.dumps(status_data, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8"
    )
    logger.info(f"action-status.json 更新完了 ({len(actions)}件, {len(existing_done)}件完了済み保持)")

    # 2. ダッシュボードHTMLの優先アクション欄を書き換え
    if not dashboard_path.exists():
        return

    html = dashboard_path.read_text(encoding="utf-8")

    # Build new action items HTML
    action_items = []
    for a in actions:
        pri_class = {"P1": "p1", "P2": "p2", "P3": "p3"}.get(a["priority"], "p3")
        effort = a.get("effort", "")
        revenue = a.get("revenue_potential", "")
        reason = a.get("reason", "")
        sub_parts = []
        if reason:
            sub_parts.append(reason)
        if effort and revenue:
            sub_parts.append(f"⏱{effort} → {revenue}")
        elif revenue:
            sub_parts.append(revenue)
        sub_text = "　".join(sub_parts)

        is_done = a["id"] in existing_done
        done_class = ' done' if is_done else ''
        check_mark = '✅' if is_done else '☐'
        done_time_html = f'<span class="done-time">✓ {existing_done[a["id"]]}</span>' if is_done and existing_done.get(a["id"]) else ''

        item = (
            f'    <div class="action-item{done_class}" data-action-id="{a["id"]}">'
            f'<span class="a-check">{check_mark}</span>'
            f'<span class="a-pri {pri_class}">{a["priority"]}</span>'
            f'<div class="a-text"><strong>{a["title"]}</strong>'
            f'<span class="a-reason">{sub_text}</span>'
            f'</div></div>'
        )
        action_items.append(item)

    new_action_html = "\n".join(action_items)

    # Replace action list content
    pattern = r'(<div class="action-list anim" id="action-list">)\s*.*?\s*(</div>\s*\n\s*<footer>)'
    replacement = rf'\1\n{new_action_html}\n  \2'
    html = re.sub(pattern, replacement, html, flags=re.DOTALL)

    # Update badge
    html = re.sub(
        r'(id="actions".*?<span class="badge">).*?(</span>)',
        rf'\g<1>{len(actions)} items\2',
        html
    )

    dashboard_path.write_text(html, encoding="utf-8")
    logger.info("ダッシュボードHTML 優先アクション欄 更新完了")


def build_report(blog_data: list, rapidapi_data: dict, apify_data: dict,
                 pseo_data: dict, n8n_data: dict, task_health: dict,
                 summary: str) -> str:
    """Markdownレポートを組み立てる"""
    today = datetime.now()
    date_str = today.strftime("%Y年%m月%d日")
    time_str = today.strftime("%H:%M")

    lines = []
    lines.append(f"# 日次ビジネス総合レポート — {date_str}")
    lines.append(f"*生成日時: {date_str} {time_str} (PYT)*")
    lines.append("")

    # エグゼクティブサマリー
    lines.append("## エグゼクティブサマリー")
    lines.append("")
    lines.append(summary)
    lines.append("")

    # ─── 1. ブログ3サイト ───
    lines.append("---")
    lines.append("")
    lines.append("## 1. ブログ3サイト（WordPress）")
    lines.append("")
    lines.append("| サイト | PV | ユーザー | 検索表示 | クリック | 記事数 |")
    lines.append("|--------|-----|---------|---------|---------|--------|")
    for d in blog_data:
        pv = d["ga4"].get("pageviews", "–")
        users = d["ga4"].get("users", "–")
        impressions = d["gsc"].get("impressions", "–")
        clicks = d["gsc"].get("clicks", "–")
        posts = d["wp"].get("post_count", "–")
        lines.append(
            f"| [{d['display_name']}]({d['url']}) "
            f"| {pv} | {users} | {impressions} | {clicks} | {posts} |"
        )
    lines.append("")

    # 各サイトのステータス詳細
    for d in blog_data:
        ga4_status = d["ga4"].get("status", "–")
        gsc_status = d["gsc"].get("status", "–")
        wp_status = d["wp"].get("status", "–")
        if ga4_status != "取得成功" or gsc_status != "取得成功" or wp_status != "取得成功":
            lines.append(f"**{d['display_name']} ステータス備考:**")
            if ga4_status != "取得成功":
                lines.append(f"- GA4: {ga4_status}")
            if gsc_status != "取得成功":
                lines.append(f"- Search Console: {gsc_status}")
            if wp_status != "取得成功":
                lines.append(f"- WordPress API: {wp_status}")
            lines.append("")

    # ─── 2. RapidAPI ───
    lines.append("---")
    lines.append("")
    lines.append("## 2. RapidAPI（20 APIs）")
    lines.append("")
    lines.append(f"- **ステータス**: {rapidapi_data.get('status')}")
    lines.append(f"- **出品API数**: {rapidapi_data.get('api_count', 0)} 本")

    if rapidapi_data.get("stats"):
        stats = rapidapi_data["stats"]
        lines.append(f"- **総呼び出し数**: {stats.get('total_requests', 'N/A')}")
        lines.append(f"- **今月売上**: ${stats.get('monthly_revenue_usd', 'N/A')}")
        if stats.get("apis"):
            lines.append("")
            lines.append("| API名 | 呼び出し数 | ステータス |")
            lines.append("|-------|----------|-----------|")
            for api in stats["apis"][:10]:
                lines.append(
                    f"| {api.get('name', '–')} | {api.get('requests', 0)} | {api.get('status', '–')} |"
                )
    else:
        lines.append("- **利用統計**: `api-services/rapidapi-stats.json` を作成して統計収集を設定してください")
    lines.append("")

    # ─── 3. Apify ───
    lines.append("---")
    lines.append("")
    lines.append("## 3. Apify Store")
    lines.append("")
    lines.append(f"- **ステータス**: {apify_data.get('status')}")

    actors = apify_data.get("actors", [])
    if actors:
        lines.append(f"- **Actor数**: {len(actors)} 件")
        lines.append("")
        lines.append("| Actor名 | 総実行数 | 最終ステータス | 最終実行日 |")
        lines.append("|---------|---------|--------------|----------|")
        for actor in actors:
            lines.append(
                f"| {actor['name']} | {actor['total_runs']} "
                f"| {actor['last_run_status']} | {actor['last_run_date']} |"
            )
    else:
        lines.append("- Actor情報を取得できませんでした")
    lines.append("")

    # ─── 4. pSEO ───
    lines.append("---")
    lines.append("")
    lines.append("## 4. pSEO AIツール比較サイト")
    lines.append("")
    lines.append(f"- **ステータス**: {pseo_data.get('status')}")
    lines.append(f"- **静的ページ数**: {pseo_data.get('page_count', 0):,} ページ")
    lines.append(f"- **デプロイURL**: {pseo_data.get('deploy_url', '未設定')}")
    if not pseo_data.get("deployed"):
        lines.append("- **TODO**: Vercel デプロイ + ドメイン取得が必要")
    lines.append("")

    # ─── 5. n8nテンプレート ───
    lines.append("---")
    lines.append("")
    lines.append("## 5. n8nテンプレート販売")
    lines.append("")
    lines.append(f"- **ステータス**: {n8n_data.get('status')}")
    lines.append(f"- **プラットフォーム**: {n8n_data.get('platform')}")
    lines.append(f"- **テンプレート数**: {n8n_data.get('template_count', 0)} 本（概算）")
    lines.append(f"- **備考**: {n8n_data.get('note')}")
    lines.append("")

    # ─── 6. 定期タスク健全性 ───
    lines.append("---")
    lines.append("")
    lines.append("## 6. 定期タスク健全性")
    lines.append("")
    lines.append(f"- **GitHub自動同期**: {task_health.get('status')}")
    lines.append(f"- **最終同期**: {task_health.get('last_sync', 'N/A')}")
    lines.append(f"- **総ログエントリー数**: {task_health.get('total_entries', 0):,} 件")
    lines.append(f"- **直近1時間のエントリー**: {task_health.get('recent_entries_1h', 0)} 件")

    last_lines = task_health.get("last_lines", [])
    if last_lines:
        lines.append("")
        lines.append("**最新ログ（直近3行）:**")
        lines.append("```")
        for l in last_lines:
            lines.append(l)
        lines.append("```")
    lines.append("")

    # ─── 7. 財務サマリー ───
    lines.append("---")
    lines.append("")
    lines.append("## 7. 財務サマリー（概算）")
    lines.append("")
    lines.append("### 月次コスト")
    lines.append("")
    lines.append("| 項目 | 月次コスト |")
    lines.append("|------|----------|")
    lines.append("| Apify（Freeプラン） | $0（月$5クレジット内） |")
    lines.append("| Claude API | $5以内（予算設定済み） |")
    lines.append("| サーバー/ドメイン | 別途管理 |")
    lines.append("| **合計（推定）** | **$1.21〜$6.21/月** |")
    lines.append("")
    lines.append("### 収益源（手動更新）")
    lines.append("")
    lines.append("| 収益源 | 今月 | 累計 | ステータス |")
    lines.append("|--------|------|------|----------|")
    lines.append("| RapidAPI | – | – | 稼働中 |")
    lines.append("| Apify Store | – | – | 稼働中 |")
    lines.append("| Google Adsense | – | – | 承認待ち/運用中 |")
    lines.append("| アフィリエイト（A8/アクセストレード） | – | – | 運用中 |")
    lines.append("| n8nテンプレート（Gumroad） | – | – | Stripe KYC停止中 |")
    lines.append("")
    lines.append("> ※ 収益数値は手動で更新してください")
    lines.append("")

    # フッター
    lines.append("---")
    lines.append("")
    lines.append(f"*このレポートは自動生成されました。（{today.strftime('%Y/%m/%d %H:%M')} PYT）*")

    return "\n".join(lines)


# ─────────────────────────────────────────────
# Discord通知
# ─────────────────────────────────────────────

def send_discord_notification(blog_data, rapidapi_data, apify_data, x_data, task_health, today_str, report_path):
    """Discord Webhookで日次レポートサマリーを通知"""
    try:
        # Webhook URL取得
        settings_path = PROJECT_ROOT / "config" / "settings.json"
        with open(settings_path, encoding="utf-8") as f:
            settings = json.load(f)
        webhook_url = settings.get("discord", {}).get("webhook_url", "")
        if not webhook_url:
            logger.warning("Discord webhook URL が未設定です")
            return

        # ブログデータ集計
        total_articles = sum(d["wp"].get("post_count", 0) for d in blog_data)
        blog_lines = []
        for d in blog_data:
            name = d["display_name"]
            posts = d["wp"].get("post_count", "–")
            pv = d["ga4"].get("pageviews", 0)
            clicks = d["gsc"].get("clicks", 0)
            blog_lines.append(f"  {name}: {posts}記事 / PV:{pv} / GSCクリック:{clicks}")

        # API集計
        api_count = rapidapi_data.get("api_count", 0)
        actor_count = len(apify_data.get("actors", []))

        # X集計
        followers = x_data.get("followers", "–")
        tweets = x_data.get("tweets", "–")

        # Embed構築
        # ダッシュボードURL（GitHub上のHTMLファイル）
        dashboard_url = "https://htmlpreview.github.io/?https://gist.githubusercontent.com/tmizuno27/16a8680cadf8aed0c207777f7468963b/raw/daily-business-dashboard.html"

        embed = {
            "title": f"📊 日次ビジネスレポート — {today_str}",
            "url": dashboard_url,
            "color": 0xD4A017,  # gold
            "fields": [
                {
                    "name": "📝 ブログ 3サイト",
                    "value": "\n".join(blog_lines) if blog_lines else "データなし",
                    "inline": False
                },
                {
                    "name": "🔌 API / Actor",
                    "value": f"RapidAPI: {api_count}本\nApify: {actor_count} Actors",
                    "inline": True
                },
                {
                    "name": "🐦 X (@nambei_oyaji)",
                    "value": f"フォロワー: {followers}\nツイート: {tweets}",
                    "inline": True
                },
                {
                    "name": "🔧 システム",
                    "value": f"定期タスク: {task_health.get('status', 'N/A')}\nGitSync: {task_health.get('total_entries', 0):,} entries",
                    "inline": True
                },
                {
                    "name": "📄 レポート",
                    "value": f"`{report_path.name}`\nダッシュボード: `daily-business-dashboard.html`",
                    "inline": False
                }
            ],
            "footer": {
                "text": "daily_business_report.py v3.0 — 自動生成"
            },
            "timestamp": datetime.now().isoformat()
        }

        payload = {
            "embeds": [embed]
        }

        resp = requests.post(webhook_url, json=payload, timeout=10)
        if resp.status_code in (200, 204):
            logger.info("Discord通知送信完了")
        else:
            logger.warning(f"Discord通知失敗: {resp.status_code} {resp.text}")

    except Exception as e:
        logger.warning(f"Discord通知エラー: {e}")


# ─────────────────────────────────────────────
# Gist自動更新
# ─────────────────────────────────────────────

GIST_ID = "16a8680cadf8aed0c207777f7468963b"


def update_gist_dashboard():
    """ダッシュボードHTMLをGitHub Gistに自動アップロード"""
    try:
        dashboard_path = REPORTS_DIR / "daily-business-dashboard.html"
        if not dashboard_path.exists():
            logger.warning("ダッシュボードHTML未生成。Gist更新スキップ")
            return

        # GitのCredential Managerからトークン取得
        import subprocess
        result = subprocess.run(
            ["git", "credential", "fill"],
            input="protocol=https\nhost=github.com\n",
            capture_output=True, text=True, timeout=10
        )
        token = None
        for line in result.stdout.splitlines():
            if line.startswith("password="):
                token = line.split("=", 1)[1]
                break
        if not token:
            logger.warning("GitHubトークン取得失敗。Gist更新スキップ")
            return

        html_content = dashboard_path.read_text(encoding="utf-8")
        # HTMLの日付・時刻を現在に更新
        now = datetime.now()
        html_content = re.sub(
            r'(<div class="header-date">)\d{2}\.\d{2}(</div>)',
            rf'\g<1>{now.strftime("%m.%d")}\2', html_content
        )
        html_content = re.sub(
            r'\d{4} — \d{2}:\d{2} PYT',
            f'{now.strftime("%Y — %H:%M")} PYT', html_content, count=1
        )
        html_content = re.sub(
            r'(<title>日次ビジネス総合レポート — )\d{4}\.\d{2}\.\d{2}(</title>)',
            rf'\g<1>{now.strftime("%Y.%m.%d")}\2', html_content
        )
        html_content = re.sub(
            r'(<span class="header-time" id="header-time">)\d{2}:\d{2}:\d{2} PYT(</span>)',
            rf'\g<1>{now.strftime("%H:%M:%S")} PYT\2', html_content
        )
        # ローカルHTMLも更新
        dashboard_path.write_text(html_content, encoding="utf-8")
        resp = requests.patch(
            f"https://api.github.com/gists/{GIST_ID}",
            headers={"Authorization": f"token {token}", "Accept": "application/vnd.github+json"},
            json={"files": {"daily-business-dashboard.html": {"content": html_content}}},
            timeout=30,
        )
        if resp.status_code == 200:
            logger.info("Gistダッシュボード更新完了")
        else:
            logger.warning(f"Gist更新失敗: {resp.status_code}")
    except Exception as e:
        logger.warning(f"Gist更新エラー: {e}")


# ─────────────────────────────────────────────
# メイン処理
# ─────────────────────────────────────────────

def main():
    """メイン処理"""
    logger.info("=== 日次ビジネス総合レポート生成開始 ===")

    # nambei-oyaji.com の設定を読み込む（Claude APIキー取得のため）
    try:
        config = load_config(PROJECT_ROOT / "config" / "settings.json")
    except Exception as e:
        logger.warning(f"設定ファイル読み込みエラー: {e}")
        config = {}

    # ─── データ収集 ───
    logger.info("1. ブログ3サイトのデータ収集中...")
    blog_data = collect_blog_data()

    logger.info("2. RapidAPIデータ収集中...")
    rapidapi_data = collect_rapidapi_data()

    logger.info("3. Apifyデータ収集中...")
    apify_data = collect_apify_data()

    logger.info("4. pSEOサイトステータス確認中...")
    pseo_data = collect_pseo_data()

    logger.info("5. n8nテンプレートステータス確認中...")
    n8n_data = collect_n8n_data()

    logger.info("5.5 X (Twitter) データ収集中...")
    x_data = collect_x_data()
    logger.info(f"  X API: {x_data.get('status', 'N/A')} — followers:{x_data.get('followers', 0)}")

    logger.info("6. 定期タスク健全性チェック中...")
    task_health = collect_task_health()

    # ─── エグゼクティブサマリー生成 ───
    logger.info("エグゼクティブサマリー生成中...")
    with ThreadPoolExecutor(max_workers=1) as executor:
        future = executor.submit(generate_executive_summary, blog_data, rapidapi_data, apify_data, config)
        try:
            summary = future.result(timeout=45)
        except Exception as e:
            logger.warning(f"サマリー生成タイムアウト: {e}")
            summary = _template_summary(blog_data)

    # ─── レポート組み立て ───
    logger.info("レポート組み立て中...")
    report = build_report(
        blog_data, rapidapi_data, apify_data,
        pseo_data, n8n_data, task_health, summary
    )

    # ─── 保存 ───
    REPORTS_DIR.mkdir(parents=True, exist_ok=True)
    today_str = datetime.now().strftime("%Y-%m-%d")
    report_path = REPORTS_DIR / f"daily-business-{today_str}.md"
    report_path.write_text(report, encoding="utf-8")

    logger.info(f"レポート保存先: {report_path}")
    logger.info("=== 日次ビジネス総合レポート生成完了 ===")

    # stdout にサマリーを出力（PS1ログキャプチャ用）
    print(f"\n{'='*60}")
    print(f"日次ビジネスレポート生成完了: {today_str}")
    print(f"{'='*60}")
    for d in blog_data:
        pv = d["ga4"].get("pageviews", "–")
        posts = d["wp"].get("post_count", "–")
        print(f"  {d['display_name']}: PV={pv}, 記事数={posts}")
    print(f"  RapidAPI: {rapidapi_data.get('api_count', 0)}本 ({rapidapi_data.get('status')})")
    print(f"  Apify: {len(apify_data.get('actors', []))}Actor ({apify_data.get('status')})")
    print(f"  定期タスク: {task_health.get('status')}")
    print(f"保存先: {report_path}")
    print(f"{'='*60}\n")

    # ─── 優先アクション生成（収益最大化AI分析） ───
    logger.info("優先アクション生成中（Claude API）...")
    with ThreadPoolExecutor(max_workers=1) as executor:
        future = executor.submit(
            generate_priority_actions,
            blog_data, rapidapi_data, apify_data,
            pseo_data, n8n_data, x_data, config
        )
        try:
            actions = future.result(timeout=60)
            if actions:
                update_action_status_file(actions)
                logger.info(f"優先アクション {len(actions)}件 → action-status.json + HTML更新完了")
        except Exception as e:
            logger.warning(f"優先アクション生成タイムアウト: {e}")

    # ─── ダッシュボードステータス同期 ───
    logger.info("ダッシュボードステータス同期中...")
    try:
        from dashboard_status_sync import apply_updates
        dashboard_path = REPORTS_DIR / "daily-business-dashboard.html"
        if dashboard_path.exists():
            dash_html = dashboard_path.read_text(encoding="utf-8")
            dash_html = apply_updates(dash_html)
            dashboard_path.write_text(dash_html, encoding="utf-8")
            logger.info("ステータス同期完了")
    except Exception as e:
        logger.warning(f"ステータス同期エラー: {e}")

    # ─── Gistダッシュボード更新 ───
    logger.info("Gistダッシュボード更新中...")
    update_gist_dashboard()

    # ─── Discord通知 ───
    send_discord_notification(blog_data, rapidapi_data, apify_data, x_data, task_health, today_str, report_path)

    sys.exit(0)


if __name__ == "__main__":
    main()
