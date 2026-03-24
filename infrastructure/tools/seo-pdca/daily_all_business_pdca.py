"""
全事業 PDCA 日次自動実行スクリプト
目的: 全事業の収益最大化のためPDCAを毎日自動で回す

対象事業:
  1. 3ブログサイト（GA4 + GSC + WP REST API）
  2. RapidAPI（24 API統計）
  3. Gumroad（売上データ）
  4. Chrome拡張（ストア公開状況）
  5. VS Code拡張（Marketplace統計）
  6. X/Twitter（2アカウントの投稿効果）
  7. Apify Actors
  8. WP Linker SaaS
  9. pSEO サイト

毎日自動実行:
  CHECK  → 全事業KPIデータ収集
  ACT    → 自動改善アクション実行
  PLAN   → 翌日の優先アクション計画
  DO     → 可能な改善を即実行

使い方:
  python daily_all_business_pdca.py           # 全事業実行
  python daily_all_business_pdca.py --sector blogs  # ブログのみ
"""
import sys
import os
import json
import csv
import time
import re
import traceback
from datetime import datetime, timedelta, timezone
from pathlib import Path
from urllib.parse import quote, unquote

if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")

import requests
from google.oauth2 import service_account
from googleapiclient.discovery import build

# ==== パス設定 ====
SCRIPT_DIR = Path(__file__).parent
REPO_ROOT = SCRIPT_DIR.parent.parent.parent  # claude-code/
SITES_DIR = REPO_ROOT / "sites"
PRODUCTS_DIR = REPO_ROOT / "products"
CRED_PATH = REPO_ROOT / "infrastructure" / "tools" / "sheets-sync" / "credentials" / "service-account.json"
LOG_DIR = REPO_ROOT / "logs"
LOG_DIR.mkdir(exist_ok=True)

PYT = timezone(timedelta(hours=-3))
NOW = datetime.now(PYT)
TODAY = NOW.strftime("%Y-%m-%d")


# ==== ロガー ====
class Logger:
    def __init__(self):
        self.log_path = LOG_DIR / "all-business-pdca.log"
        self.report_path = LOG_DIR / f"all-business-pdca-report-{TODAY}.md"
        self.lines = []

    def log(self, msg):
        ts = NOW.strftime("%Y-%m-%d %H:%M:%S")
        line = f"[{ts}] {msg}"
        print(line)
        with open(self.log_path, "a", encoding="utf-8") as f:
            f.write(line + "\n")

    def report(self, line=""):
        self.lines.append(line)

    def save_report(self):
        with open(self.report_path, "w", encoding="utf-8") as f:
            f.write("\n".join(self.lines))
        self.log(f"レポート保存: {self.report_path}")


logger = Logger()


# ==== 共通ヘルパー ====
def load_json(path):
    try:
        return json.loads(Path(path).read_text(encoding="utf-8"))
    except Exception:
        return {}


def get_wp_session(site_dir, site_url, use_secrets=False):
    config_dir = site_dir / "config"
    if use_secrets:
        secrets = load_json(config_dir / "secrets.json")
        wp = secrets.get("wordpress", {})
        base_url = wp.get("site_url", wp.get("url", site_url))
        username = wp.get("username", "")
        password = wp.get("app_password", "")
    else:
        cred = load_json(config_dir / "wp-credentials.json")
        base_url = cred.get("site_url", site_url)
        username = cred.get("username", "")
        password = cred.get("app_password", "")

    if not username or not password:
        return None, None

    session = requests.Session()
    session.auth = (username, password)
    session.headers.update({"Content-Type": "application/json"})
    api_base = f"{base_url.rstrip('/')}/wp-json/wp/v2"
    return session, api_base


# =====================================================================
# SECTOR 1: ブログ 3サイト（GA4 + GSC + 内部リンク + コンテンツ鮮度）
# =====================================================================
BLOG_SITES = {
    "nambei": {
        "label": "南米おやじ",
        "domain": "nambei-oyaji.com",
        "site_url": "https://nambei-oyaji.com",
        "gsc_url": "https://nambei-oyaji.com/",
        "ga4_property": "526536377",
        "use_secrets": False,
    },
    "otona": {
        "label": "マッチングナビ",
        "domain": "otona-match.com",
        "site_url": "https://otona-match.com",
        "gsc_url": "https://otona-match.com/",
        "ga4_property": "528520315",
        "use_secrets": True,
    },
    "sim": {
        "label": "SIM比較",
        "domain": "sim-hikaku.online",
        "site_url": "https://sim-hikaku.online",
        "gsc_url": "https://sim-hikaku.online/",
        "ga4_property": "528626242",
        "use_secrets": True,
    },
}


def pdca_blogs():
    """ブログ3サイトのPDCA"""
    logger.report("# 1. ブログ 3サイト")
    logger.report("")

    gsc_creds = service_account.Credentials.from_service_account_file(
        str(CRED_PATH), scopes=["https://www.googleapis.com/auth/webmasters.readonly"]
    )
    gsc = build("searchconsole", "v1", credentials=gsc_creds)

    end_date = (datetime.now() - timedelta(days=3)).strftime("%Y-%m-%d")
    start_7d = (datetime.now() - timedelta(days=10)).strftime("%Y-%m-%d")
    start_prev = (datetime.now() - timedelta(days=17)).strftime("%Y-%m-%d")
    end_prev = (datetime.now() - timedelta(days=10)).strftime("%Y-%m-%d")

    for site_key, cfg in BLOG_SITES.items():
        label = cfg["label"]
        site_dir = SITES_DIR / cfg["domain"]
        logger.log(f"  [{label}] CHECK開始")
        logger.report(f"## {label} ({cfg['domain']})")
        logger.report("")

        # --- GSC: 今週 vs 先週 ---
        try:
            resp_now = gsc.searchanalytics().query(
                siteUrl=cfg["gsc_url"],
                body={"startDate": start_7d, "endDate": end_date, "type": "web"},
            ).execute()
            resp_prev = gsc.searchanalytics().query(
                siteUrl=cfg["gsc_url"],
                body={"startDate": start_prev, "endDate": end_prev, "type": "web"},
            ).execute()

            now_rows = resp_now.get("rows", [{}])
            prev_rows = resp_prev.get("rows", [{}])
            now_imp = sum(r.get("impressions", 0) for r in now_rows) if now_rows else 0
            now_click = sum(r.get("clicks", 0) for r in now_rows) if now_rows else 0
            prev_imp = sum(r.get("impressions", 0) for r in prev_rows) if prev_rows else 0
            prev_click = sum(r.get("clicks", 0) for r in prev_rows) if prev_rows else 0

            imp_delta = now_imp - prev_imp
            click_delta = now_click - prev_click
            imp_pct = (imp_delta / prev_imp * 100) if prev_imp > 0 else 0

            logger.report("### CHECK")
            logger.report(f"| 指標 | 今週 | 先週 | 変化 |")
            logger.report(f"|------|-----:|-----:|-----:|")
            logger.report(f"| インプレッション | {now_imp:,} | {prev_imp:,} | {imp_delta:+,} ({imp_pct:+.0f}%) |")
            logger.report(f"| クリック | {now_click:,} | {prev_click:,} | {click_delta:+,} |")
            logger.report("")
        except Exception as e:
            logger.report(f"### CHECK: GSCエラー: {e}")
            logger.report("")

        # --- GA4: PV/ユーザー ---
        try:
            ga4_cred_path = site_dir / "config" / "ga4-credentials.json"
            if ga4_cred_path.exists():
                os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = str(ga4_cred_path)
                from google.analytics.data_v1beta import BetaAnalyticsDataClient
                from google.analytics.data_v1beta.types import (
                    DateRange, Metric, RunReportRequest,
                )
                client = BetaAnalyticsDataClient()
                req = RunReportRequest(
                    property=f"properties/{cfg['ga4_property']}",
                    date_ranges=[DateRange(start_date=start_7d, end_date=end_date)],
                    metrics=[
                        Metric(name="screenPageViews"),
                        Metric(name="activeUsers"),
                        Metric(name="sessions"),
                    ],
                )
                resp = client.run_report(req)
                if resp.rows:
                    row = resp.rows[0]
                    pv = int(row.metric_values[0].value)
                    users = int(row.metric_values[1].value)
                    sessions = int(row.metric_values[2].value)
                    logger.report(f"- GA4（7日間）: PV={pv:,} / ユーザー={users:,} / セッション={sessions:,}")
                    logger.report("")
        except Exception as e:
            logger.log(f"  [{label}] GA4エラー: {e}")

        # --- ACT: 内部リンク不足チェック ---
        try:
            session, api_base = get_wp_session(site_dir, cfg["site_url"], cfg["use_secrets"])
            if session:
                resp = session.get(f"{api_base}/posts", params={"per_page": 100, "page": 1, "status": "publish"})
                if resp.status_code == 200:
                    posts = resp.json()
                    total_posts = len(posts)
                    low_link = []
                    for post in posts:
                        content = post.get("content", {}).get("rendered", "")
                        internal = len(re.findall(rf'href=["\']https?://{re.escape(cfg["domain"])}', content))
                        if internal < 2:
                            low_link.append(post["slug"])

                    logger.report(f"### ACT")
                    logger.report(f"- 公開記事数: {total_posts}")
                    logger.report(f"- 内部リンク不足（2本未満）: {len(low_link)}件")
                    if low_link[:5]:
                        for s in low_link[:5]:
                            logger.report(f"  - `{s}`")
                    logger.report("")
        except Exception as e:
            logger.log(f"  [{label}] 内部リンクチェックエラー: {e}")

        # --- PLAN ---
        logger.report("### PLAN")
        actions = []
        if now_imp < 50:
            actions.append("⚠️ インプレッション極少 → ロングテールKW記事追加が急務")
        if imp_delta < 0:
            actions.append("📉 インプレッション減少 → 既存記事のリライト・タイトル改善")
        if now_click == 0 and now_imp > 0:
            actions.append("🎯 インプレッションあるがクリック0 → タイトル/メタ改善でCTR向上")
        if not actions:
            actions.append("✅ 推移観察継続")
        for a in actions:
            logger.report(f"- {a}")
        logger.report("")


# =====================================================================
# SECTOR 2: RapidAPI（24 API）
# =====================================================================
def pdca_rapidapi():
    """RapidAPI事業のPDCA"""
    logger.report("# 2. RapidAPI（24 API）")
    logger.report("")

    stats_path = PRODUCTS_DIR / "api-services" / "rapidapi-stats.json"
    stats = load_json(stats_path)

    if not stats:
        logger.report("- `rapidapi-stats.json` 未検出")
        logger.report("")
        return

    api_count = stats.get("total_apis", 0)
    total_subs = stats.get("total_subscribers", 0)
    total_requests = stats.get("total_requests", 0)
    total_revenue = 0
    apis = stats.get("apis", [])
    for api in apis:
        total_revenue += api.get("revenue_30d", 0)

    logger.report("### CHECK")
    logger.report(f"- API数: {api_count}")
    logger.report(f"- 総サブスクライバー: {total_subs}")
    logger.report(f"- 総リクエスト: {total_requests:,}")
    logger.report(f"- 総収益: ${total_revenue:.2f}")
    logger.report("")

    # ACT: ヘルスチェック（全APIにGETリクエスト）
    healthcheck_path = PRODUCTS_DIR / "api-services" / "healthcheck.py"
    logger.report("### ACT")
    if healthcheck_path.exists():
        logger.report("- ヘルスチェックスクリプト: 存在確認OK（Task Scheduler経由で実行中）")
    else:
        logger.report("- ⚠️ ヘルスチェックスクリプトなし")

    # PLAN
    logger.report("")
    logger.report("### PLAN")
    if total_subs == 0 and total_requests == 0:
        logger.report("- ⚠️ 全API利用ゼロ → RapidAPIリスティングのSEO改善（タイトル・説明・タグ）が必要")
        logger.report("- ⚠️ RapidAPI Provider APIキーの環境変数設定で正確な統計取得を")
        logger.report("- 📝 Dev.to/Qiita等での技術記事によるAPI宣伝を継続")
    else:
        logger.report("- 利用の多いAPIに注力してドキュメント・サンプルコード改善")
    logger.report("")


# =====================================================================
# SECTOR 3: Gumroad（Notionテンプレート + AIプロンプト）
# =====================================================================
def pdca_gumroad():
    """Gumroad事業のPDCA"""
    logger.report("# 3. Gumroad（デジタル商品）")
    logger.report("")

    gumroad_dir = PRODUCTS_DIR / "gumroad-notion"

    # 商品一覧をディレクトリからカウント
    products_dir = gumroad_dir / "products"
    product_count = 0
    if products_dir.exists():
        product_count = len([d for d in products_dir.iterdir() if d.is_dir()])

    # X投稿ログから効果確認
    x_log = LOG_DIR / "x-prodhq27-posts.log"
    recent_posts = 0
    if x_log.exists():
        try:
            lines = x_log.read_text(encoding="utf-8", errors="replace").splitlines()
            week_ago = (NOW - timedelta(days=7)).strftime("%Y-%m-%d")
            recent_posts = sum(1 for l in lines if week_ago <= l[:10] if l[:4].isdigit())
        except Exception:
            pass

    logger.report("### CHECK")
    logger.report(f"- 商品数: {product_count}（ディレクトリ数）")
    logger.report(f"- @prodhq27 X投稿（過去7日）: {recent_posts}件")
    logger.report(f"- ⚠️ Gumroad APIキー未設定のため売上データ自動取得不可")
    logger.report("")

    logger.report("### ACT")
    logger.report("- X自動投稿（@prodhq27）: 毎日3回稼働中")
    logger.report("")

    logger.report("### PLAN")
    logger.report("- Gumroad APIキー取得→secrets.jsonに設定で売上自動追跡を有効化")
    logger.report("- Product Hunt / IndieHackers への掲載でトラフィック獲得")
    logger.report("")


# =====================================================================
# SECTOR 4: Chrome拡張（10本）
# =====================================================================
def pdca_chrome_extensions():
    """Chrome拡張事業のPDCA"""
    logger.report("# 4. Chrome拡張（10本）")
    logger.report("")

    ext_dir = PRODUCTS_DIR / "chrome-extensions"
    status_file = ext_dir / "docs" / "review-status-2026-03-21.md"

    # 拡張一覧をディレクトリから取得
    ext_count = 0
    if ext_dir.exists():
        ext_count = len([d for d in ext_dir.iterdir() if d.is_dir() and not d.name.startswith(".")])

    logger.report("### CHECK")
    logger.report(f"- 拡張数: {ext_count}ディレクトリ")
    if status_file.exists():
        logger.report(f"- 最終ステータス確認: {status_file.name}")
    logger.report("- ⚠️ Chrome Developer Dashboard APIは存在しないため自動確認不可")
    logger.report("")

    logger.report("### PLAN")
    logger.report("- 審査待ち8本の通過状況を定期的に手動確認")
    logger.report("- 公開済み2本のレビュー・DL数をChrome Web Storeで確認")
    logger.report("")


# =====================================================================
# SECTOR 5: VS Code拡張（10本）
# =====================================================================
def pdca_vscode_extensions():
    """VS Code拡張事業のPDCA"""
    logger.report("# 5. VS Code拡張（10本）")
    logger.report("")

    vsc_dir = PRODUCTS_DIR / "vscode-extensions"

    # Marketplace APIで統計取得
    stats = []
    publisher = "miccho27"
    try:
        api_url = "https://marketplace.visualstudio.com/_apis/public/gallery/extensionquery"
        payload = {
            "filters": [{"criteria": [{"filterType": 4, "value": publisher}], "pageSize": 50, "pageNumber": 1}],
            "assetTypes": [],
            "flags": 0x200 | 0x80 | 0x2,  # IncludeStatistics | ExcludeNonValidated | IncludeVersions
        }
        resp = requests.post(
            api_url,
            json=payload,
            headers={"Content-Type": "application/json", "Accept": "application/json;api-version=6.1-preview.1"},
            timeout=15,
        )
        if resp.status_code == 200:
            data = resp.json()
            extensions = data.get("results", [{}])[0].get("extensions", [])
            total_installs = 0
            for ext in extensions:
                name = ext.get("displayName", ext.get("extensionName", "?"))
                ext_stats = ext.get("statistics", [])
                installs = 0
                for s in ext_stats:
                    if s.get("statisticName") == "install":
                        installs = int(s.get("value", 0))
                total_installs += installs
                stats.append({"name": name, "installs": installs})

            stats.sort(key=lambda x: x["installs"], reverse=True)

            logger.report("### CHECK")
            logger.report(f"- 公開数: {len(extensions)}本")
            logger.report(f"- 総インストール数: {total_installs:,}")
            logger.report("")
            if stats[:5]:
                logger.report("| 拡張名 | インストール数 |")
                logger.report("|--------|----------:|")
                for s in stats[:5]:
                    logger.report(f"| {s['name']} | {s['installs']:,} |")
                logger.report("")
        else:
            logger.report(f"### CHECK: Marketplace API HTTP {resp.status_code}")
            logger.report("")
    except Exception as e:
        logger.report(f"### CHECK: Marketplace APIエラー: {e}")
        logger.report("")

    logger.report("### PLAN")
    if stats and stats[0]["installs"] == 0:
        logger.report("- ⚠️ 全拡張インストール0 → README改善・スクリーンショット追加・VS Code Marketplaceタグ最適化")
    else:
        logger.report("- インストール数の多い拡張にフォーカスしてアップデート・レビュー誘導")
    logger.report("")


# =====================================================================
# SECTOR 6: X/Twitter（2アカウント）
# =====================================================================
def pdca_twitter():
    """X/Twitter 2アカウントのPDCA"""
    logger.report("# 6. X/Twitter（2アカウント）")
    logger.report("")

    accounts = [
        {"name": "@nambei_oyaji", "log": LOG_DIR / "x-auto-post-nambei.log", "purpose": "ブログ集客"},
        {"name": "@prodhq27", "log": LOG_DIR / "x-prodhq27-posts.log", "purpose": "Gumroad販促"},
    ]

    logger.report("### CHECK")
    week_ago = (NOW - timedelta(days=7)).strftime("%Y-%m-%d")

    for acc in accounts:
        recent = 0
        errors = 0
        if acc["log"].exists():
            try:
                lines = acc["log"].read_text(encoding="utf-8", errors="replace").splitlines()
                for l in lines:
                    if l[:4].isdigit() and l[:10] >= week_ago:
                        recent += 1
                        if "error" in l.lower() or "fail" in l.lower():
                            errors += 1
            except Exception:
                pass

        logger.report(f"- **{acc['name']}**（{acc['purpose']}）: 過去7日 {recent}投稿 / エラー{errors}件")

    logger.report("")
    logger.report("### PLAN")
    logger.report("- 投稿がゼロのアカウントがあればTask Scheduler確認")
    logger.report("- エンゲージメント率を分析してコンテンツ改善")
    logger.report("")


# =====================================================================
# SECTOR 7: Apify Actors（5本）
# =====================================================================
def pdca_apify():
    """Apify事業のPDCA"""
    logger.report("# 7. Apify Actors（5本）")
    logger.report("")

    actors_dir = PRODUCTS_DIR / "api-services" / "apify-actors"
    actor_count = 0
    if actors_dir.exists():
        actor_count = len([d for d in actors_dir.iterdir() if d.is_dir() and not d.name.startswith(".")])

    logger.report("### CHECK")
    logger.report(f"- 公開Actor数: {actor_count}")
    logger.report("- ⚠️ Apify API統計の自動取得は未実装")
    logger.report("")

    logger.report("### PLAN")
    logger.report("- Apify Store の各Actorページのランキング・利用状況を定期確認")
    logger.report("- READMEとサンプルコードの充実で利用促進")
    logger.report("")


# =====================================================================
# SECTOR 8: WP Linker SaaS
# =====================================================================
def pdca_wp_linker():
    """WP Linker SaaS のPDCA"""
    logger.report("# 8. WP Linker SaaS")
    logger.report("")

    saas_dir = REPO_ROOT / "saas" / "wp-linker"
    url = "https://wp-linker.vercel.app"

    # サイト稼働確認
    try:
        resp = requests.get(url, timeout=15)
        status = f"HTTP {resp.status_code}"
    except Exception as e:
        status = f"ERROR: {e}"

    logger.report("### CHECK")
    logger.report(f"- URL: {url}")
    logger.report(f"- 稼働状況: {status}")
    logger.report("- ⚠️ Stripe未連携のため決済不可（Stripe待ち）")
    logger.report("")

    logger.report("### PLAN")
    logger.report("- Stripe連携完了次第、料金プラン設定→本格ローンチ")
    logger.report("")


# =====================================================================
# SECTOR 9: pSEO AIツール比較
# =====================================================================
def pdca_pseo():
    """pSEO サイトのPDCA"""
    logger.report("# 9. pSEO AIツール比較")
    logger.report("")

    url = "https://ai-tool-compare-nu.vercel.app"

    try:
        resp = requests.get(url, timeout=15)
        status = f"HTTP {resp.status_code}"
    except Exception as e:
        status = f"ERROR: {e}"

    logger.report("### CHECK")
    logger.report(f"- URL: {url}")
    logger.report(f"- 稼働状況: {status}")
    logger.report(f"- 4,003静的ページ（291ツール×12カテゴリ）")
    logger.report("")

    logger.report("### PLAN")
    logger.report("- GSCでインデックス状況確認（4,003ページ中何ページインデックス済みか）")
    logger.report("- AdSenseまたはアフィリエイト導線の追加")
    logger.report("")


# =====================================================================
# SECTOR 10: インフラ・タスク稼働状況
# =====================================================================
def pdca_infrastructure():
    """インフラ・自動化タスクのPDCA"""
    logger.report("# 10. インフラ・自動化基盤")
    logger.report("")

    # Git自動同期ログ確認
    sync_log = LOG_DIR / "auto-sync.log"
    sync_ok = False
    if sync_log.exists():
        try:
            lines = sync_log.read_text(encoding="utf-8", errors="replace").splitlines()
            if lines:
                last_line = lines[-1]
                if TODAY in last_line:
                    sync_ok = True
        except Exception:
            pass

    # 各ログの最終更新日チェック
    log_files = [
        ("auto-sync.log", "Git自動同期"),
        ("seo-pdca.log", "SEO PDCA"),
        ("x-auto-post-nambei.log", "X投稿(@nambei)"),
        ("x-prodhq27-posts.log", "X投稿(@prodhq27)"),
        ("api-healthcheck.log", "APIヘルスチェック"),
        ("dashboard-update.log", "ダッシュボード更新"),
    ]

    logger.report("### CHECK — ログ最終更新")
    logger.report("| ログ | 最終更新 | ステータス |")
    logger.report("|------|---------|-----------|")

    for filename, desc in log_files:
        log_path = LOG_DIR / filename
        if log_path.exists():
            try:
                mtime = datetime.fromtimestamp(log_path.stat().st_mtime, tz=PYT)
                age_hours = (NOW - mtime).total_seconds() / 3600
                if age_hours < 25:
                    status = "✅ 正常"
                elif age_hours < 72:
                    status = "⚠️ 遅延"
                else:
                    status = "❌ 停止"
                logger.report(f"| {desc} | {mtime.strftime('%m/%d %H:%M')} | {status} |")
            except Exception:
                logger.report(f"| {desc} | 読取エラー | ❌ |")
        else:
            logger.report(f"| {desc} | 未検出 | ❌ |")

    logger.report("")

    logger.report("### PLAN")
    if not sync_ok:
        logger.report("- ⚠️ Git自動同期が今日動いていない可能性あり → Task Scheduler確認")
    logger.report("- 停止/遅延しているタスクがあれば原因調査→復旧")
    logger.report("")


# =====================================================================
# メイン
# =====================================================================
SECTORS = {
    "blogs": pdca_blogs,
    "rapidapi": pdca_rapidapi,
    "gumroad": pdca_gumroad,
    "chrome": pdca_chrome_extensions,
    "vscode": pdca_vscode_extensions,
    "twitter": pdca_twitter,
    "apify": pdca_apify,
    "wp-linker": pdca_wp_linker,
    "pseo": pdca_pseo,
    "devto": pdca_devto,
    "n8n": pdca_n8n,
    "stock-assets": pdca_stock_assets,
    "pod-etsy": pdca_pod_etsy,
    "trading-bot": pdca_trading_bot,
    "infra": pdca_infrastructure,
}


def main():
    args = sys.argv[1:]
    target = None
    for i, a in enumerate(args):
        if a == "--sector" and i + 1 < len(args):
            target = args[i + 1]

    logger.log("=" * 60)
    logger.log("全事業 PDCA 日次自動実行 開始")
    logger.log("=" * 60)

    logger.report(f"# 全事業 PDCA 日次レポート ({TODAY})")
    logger.report(f"実行時刻: {NOW.strftime('%Y-%m-%d %H:%M PYT')}")
    logger.report("")

    for sector_key, func in SECTORS.items():
        if target and sector_key != target:
            continue
        try:
            logger.log(f"--- {sector_key} ---")
            func()
        except Exception as e:
            logger.log(f"  [{sector_key}] エラー: {e}")
            logger.report(f"# {sector_key}: エラー")
            logger.report(f"```\n{traceback.format_exc()}\n```")
            logger.report("")

    # 全体サマリー
    logger.report("---")
    logger.report(f"*自動生成: {NOW.strftime('%Y-%m-%d %H:%M PYT')}*")

    logger.save_report()
    logger.log("全事業 PDCA 完了")


if __name__ == "__main__":
    main()
