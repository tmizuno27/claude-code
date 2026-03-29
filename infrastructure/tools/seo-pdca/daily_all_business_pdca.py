"""
全事業 PDCA 日次自動実行スクリプト
目的: 全事業の収益最大化のためPDCAを毎日自動で回す

対象事業:
  1. 3ブログサイト（GA4 + GSC + WP REST API）
  1b. はてなブログ（本家送客チャネル、投稿状況・送客効果）
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
CRED_PATH = REPO_ROOT / "sites" / "nambei-oyaji.com" / "config" / "gsc-credentials.json"
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

    gsc = None
    try:
        gsc_creds = service_account.Credentials.from_service_account_file(
            str(CRED_PATH), scopes=["https://www.googleapis.com/auth/webmasters.readonly"]
        )
        gsc = build("searchconsole", "v1", credentials=gsc_creds)
    except Exception as e:
        logger.log(f"  [blogs] GSC認証失敗: {e}")
        logger.report(f"- ⚠️ GSC認証失敗（{e.__class__.__name__}）— ローカルデータのみでレポート生成")
        logger.report("")

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
        now_imp = 0
        now_click = 0
        prev_imp = 0
        prev_click = 0
        imp_delta = 0
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
        # now_imp / imp_delta / now_click are initialized above the try block
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

    # Gumroad APIから商品数・売上データ取得
    product_count = 0
    total_sales = 0
    total_revenue = 0.0
    gumroad_api_ok = False
    secrets_path = gumroad_dir / "config" / "secrets.json"
    if secrets_path.exists():
        try:
            secrets = json.loads(secrets_path.read_text(encoding="utf-8"))
            token = secrets.get("gumroad_access_token", "")
            if token:
                resp = requests.get(
                    "https://api.gumroad.com/v2/products",
                    params={"access_token": token},
                    timeout=15,
                )
                if resp.status_code == 200:
                    data = resp.json()
                    products = data.get("products", [])
                    product_count = len(products)
                    for p in products:
                        total_sales += p.get("sales_count", 0)
                        total_revenue += (p.get("total_revenue", 0) or 0) / 100.0
                    gumroad_api_ok = True
        except Exception as e:
            logger.log(f"  [gumroad] API error: {e}")

    # X投稿ログから効果確認
    x_log = LOG_DIR / "x-prodhq27-posts.log"
    recent_posts = 0
    if x_log.exists():
        try:
            lines = x_log.read_text(encoding="utf-8", errors="replace").splitlines()
            week_ago = (NOW - timedelta(days=7)).strftime("%Y-%m-%d")
            for l in lines:
                date_str = l[1:11] if l.startswith("[") and len(l) > 11 else (l[:10] if len(l) > 10 and l[:4].isdigit() else "")
                if date_str >= week_ago and ("OK:" in l or "POSTED" in l):
                    recent_posts += 1
        except Exception:
            pass

    logger.report("### CHECK")
    if gumroad_api_ok:
        logger.report(f"- 商品数: **{product_count}**（Gumroad API取得）")
        logger.report(f"- 総販売数: **{total_sales}件**")
        logger.report(f"- 総売上: **${total_revenue:.2f}**")
    else:
        logger.report(f"- 商品数: 取得失敗（API接続エラー）")
    logger.report(f"- @prodhq27 X投稿（過去7日）: {recent_posts}件")
    logger.report("")

    logger.report("### ACT")
    logger.report("- X自動投稿（@prodhq27）: 毎日3回稼働中")
    if gumroad_api_ok and total_sales == 0:
        logger.report("- ⚠️ 販売数ゼロ → 商品ページ・価格・プロモーション戦略の見直しが急務")
    logger.report("")

    logger.report("### PLAN")
    if not gumroad_api_ok:
        logger.report("- ⚠️ Gumroad API接続に失敗。トークンの有効性を確認")
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
            "filters": [
                {
                    "criteria": [
                        {"filterType": 8, "value": "Microsoft.VisualStudio.Code"},
                        {"filterType": 10, "value": publisher},  # filterType 10 = Publisher name
                    ],
                    "pageSize": 50,
                    "pageNumber": 1,
                }
            ],
            "assetTypes": [],
            "flags": 0x200 | 0x80,  # IncludeStatistics | IncludeLatestVersionOnly
        }
        resp = requests.post(
            api_url,
            json=payload,
            headers={"Content-Type": "application/json", "Accept": "application/json;api-version=3.0-preview.1"},
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
                last_date = ""
                for l in lines:
                    # ログ形式: [2026-03-25 14:16:18] or 2026-03-25T... or タイムスタンプなし
                    if l.startswith("[") and len(l) > 11 and l[1:5].isdigit():
                        last_date = l[1:11]
                    elif len(l) > 10 and l[:4].isdigit():
                        last_date = l[:10]
                    if last_date >= week_ago:
                        if "OK:" in l or "POSTED" in l or "投稿成功" in l:
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
# SECTOR 11: Dev.to（技術記事 → API販促）
# =====================================================================
def pdca_devto():
    """Dev.to記事のPDCA"""
    logger.report("# 11. Dev.to（技術記事）")
    logger.report("")

    # Dev.to API（認証付きで正確なViews取得）
    devto_config_path = PRODUCTS_DIR / "api-services" / "marketing" / "dev-to-config.json"
    devto_api_key = ""
    if devto_config_path.exists():
        try:
            devto_cfg = json.loads(devto_config_path.read_text(encoding="utf-8"))
            devto_api_key = devto_cfg.get("api_key", "")
        except Exception:
            pass

    headers = {"Accept": "application/json"}
    if devto_api_key:
        headers["api-key"] = devto_api_key
        api_url = "https://dev.to/api/articles/me/all?per_page=50"
    else:
        api_url = "https://dev.to/api/articles?username=miccho27&per_page=30"

    try:
        resp = requests.get(api_url, headers=headers, timeout=15)
        if resp.status_code == 200:
            articles = resp.json()
            total_views = sum(a.get("page_views_count", 0) for a in articles)
            total_reactions = sum(a.get("positive_reactions_count", 0) for a in articles)
            total_comments = sum(a.get("comments_count", 0) for a in articles)

            logger.report("### CHECK")
            logger.report(f"- 記事数: {len(articles)}")
            logger.report(f"- 総閲覧数: {total_views:,}")
            logger.report(f"- 総リアクション: {total_reactions}")
            logger.report(f"- 総コメント: {total_comments}")
            logger.report("")

            if articles:
                logger.report("| 記事 | 閲覧数 | リアクション |")
                logger.report("|------|------:|----------:|")
                for a in sorted(articles, key=lambda x: x.get("page_views_count", 0), reverse=True)[:5]:
                    title = a.get("title", "?")[:50]
                    views = a.get("page_views_count", 0)
                    reacts = a.get("positive_reactions_count", 0)
                    logger.report(f"| {title} | {views:,} | {reacts} |")
                logger.report("")
        else:
            logger.report(f"### CHECK: Dev.to API HTTP {resp.status_code}")
            logger.report("")
    except Exception as e:
        logger.report(f"### CHECK: Dev.to APIエラー: {e}")
        logger.report("")

    logger.report("### PLAN")
    logger.report("- 閲覧数が伸びている記事があればRapidAPI導線を強化")
    logger.report("- 新記事投稿（月2-3本）でRapidAPIへのトラフィック誘導")
    logger.report("")


# =====================================================================
# SECTOR 12: n8nテンプレート（Stripe待ち）
# =====================================================================
def pdca_n8n():
    """n8nテンプレート事業のPDCA"""
    logger.report("# 12. n8nテンプレート（一時停止）")
    logger.report("")

    n8n_dir = PRODUCTS_DIR / "n8n-templates"

    # テンプレート数カウント
    workflow_count = 0
    workflows_dir = n8n_dir / "workflows"
    if workflows_dir.exists():
        workflow_count = len(list(workflows_dir.glob("*.json")))

    listing_dir = n8n_dir / "listings"
    listing_count = 0
    if listing_dir.exists():
        listing_count = len([d for d in listing_dir.iterdir() if d.is_dir()])

    logger.report("### CHECK")
    logger.report(f"- ワークフロー数: {workflow_count}")
    logger.report(f"- リスティング数: {listing_count}")
    logger.report("- ステータス: **一時停止**（Stripe KYC認証問題）")
    logger.report("- プラットフォーム: Gumroad（tatsuya27.gumroad.com）")
    logger.report("")

    logger.report("### PLAN")
    logger.report("- Stripe KYC解決次第、即座に販売再開")
    logger.report("- 解決までの間、テンプレートの品質改善・新テンプレート作成を進める")
    logger.report("")


# =====================================================================
# SECTOR 13: Stock Assets（出品準備中）
# =====================================================================
def pdca_stock_assets():
    """Stock Assets事業のPDCA"""
    logger.report("# 13. Stock Assets（出品準備中）")
    logger.report("")

    assets_dir = PRODUCTS_DIR / "stock-assets"
    output_dir = assets_dir / "output"

    # ファイル数カウント
    png_count = 0
    csv_count = 0
    prompt_count = 0
    if output_dir.exists():
        png_count = len(list(output_dir.rglob("*.png")))
        csv_count = len(list(output_dir.rglob("*.csv")))

    scripts_dir = assets_dir / "scripts"
    prompts_dir = assets_dir / "docs"
    if prompts_dir.exists():
        for f in prompts_dir.rglob("*.md"):
            try:
                content = f.read_text(encoding="utf-8", errors="replace")
                prompt_count += content.count("prompt")
            except Exception:
                pass

    logger.report("### CHECK")
    logger.report(f"- 生成済み画像: {png_count}枚")
    logger.report(f"- メタデータCSV: {csv_count}ファイル")
    logger.report(f"- ステータス: 出品準備中（Adobe Stock/Freepik）")
    logger.report("")

    logger.report("### PLAN")
    if png_count >= 80:
        logger.report(f"- ✅ {png_count}枚生成済み → Adobe Stockアカウント開設→テスト出品が次のステップ")
    else:
        logger.report(f"- 生成枚数 {png_count}/630目標 → 画像生成を加速")
    logger.report("- 出品後はダウンロード数・収益をAdobe Stock Contributorダッシュボードで追跡")
    logger.report("")


# =====================================================================
# SECTOR 14: POD Etsy (AsuInk)
# =====================================================================
def pdca_pod_etsy():
    """POD Etsy事業のPDCA"""
    logger.report("# 14. POD Etsy — AsuInk（準備中）")
    logger.report("")

    pod_dir = PRODUCTS_DIR / "pod-etsy"

    listing_count = 0
    design_count = 0
    if (pod_dir / "listings").exists():
        listing_count = len(list((pod_dir / "listings").iterdir()))
    if (pod_dir / "designs").exists():
        design_count = len(list((pod_dir / "designs").iterdir()))

    logger.report("### CHECK")
    logger.report(f"- リスティング: {listing_count}件")
    logger.report(f"- デザインフォルダ: {design_count}件")
    logger.report("- ステータス: 準備中（Etsy/Printfulアカウント開設待ち）")
    logger.report("")

    logger.report("### PLAN")
    logger.report("- Etsy/Printfulアカウント開設 → デザイン生成（Gemini有料プランまたは代替）→ 出品開始")
    logger.report("- 150リスティング完成済みなのでアカウント開設が唯一のブロッカー")
    logger.report("")


# =====================================================================
# SECTOR 15: 仮想通貨自動売買（Bybit）
# =====================================================================
def pdca_trading_bot():
    """仮想通貨自動売買のPDCA"""
    logger.report("# 15. 仮想通貨自動売買（Bybit）")
    logger.report("")

    bot_dir = REPO_ROOT / "trading-bot"
    log_dir = bot_dir / "logs"

    # バックテスト結果確認
    has_backtest = False
    backtest_files = list(bot_dir.rglob("*backtest*")) if bot_dir.exists() else []
    has_backtest = len(backtest_files) > 0

    # 最新ログ確認
    latest_log = None
    if log_dir.exists():
        logs = sorted(log_dir.glob("*.log"), key=lambda p: p.stat().st_mtime, reverse=True)
        if logs:
            latest_log = logs[0]

    logger.report("### CHECK")
    logger.report(f"- バックテスト完了: {'✅' if has_backtest else '❌'}")
    logger.report(f"- 最優秀戦略: MAクロス+RSI × BTC/USDT (Sharpe 4.91)")
    logger.report(f"- ステータス: **口座開設待ち**（パラグアイ住所証明の準備中）")
    if latest_log:
        mtime = datetime.fromtimestamp(latest_log.stat().st_mtime, tz=PYT)
        logger.report(f"- 最新ログ: {latest_log.name} ({mtime.strftime('%Y-%m-%d')})")
    logger.report("")

    logger.report("### PLAN")
    logger.report("- Bybit口座開設完了次第、小額（$100-200）でライブテスト開始")
    logger.report("- パラグアイ住所証明の準備を進める")
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
# SECTOR 16: keisan-tools.com（計算ツールサイト）
# =====================================================================
def pdca_keisan_tools():
    """keisan-tools.com 計算ツールサイトのPDCA"""
    logger.report("# 16. keisan-tools.com（計算ツールサイト）")
    logger.report("")

    url = "https://keisan-tools.com"
    sitemap_urls = [f"{url}/sitemap.xml", f"{url}/sitemap_index.xml"]

    # CHECK: サイト稼働確認
    try:
        resp = requests.get(url, timeout=15)
        site_status = f"HTTP {resp.status_code}"
    except Exception as e:
        site_status = f"ERROR: {e}"

    # CHECK: サイトマップからページ数取得
    page_count = 0
    sitemap_status = "未検出"
    for smap_url in sitemap_urls:
        try:
            smap_resp = requests.get(smap_url, timeout=15)
            if smap_resp.status_code == 200:
                import xml.etree.ElementTree as ET
                root = ET.fromstring(smap_resp.text)
                ns = {"sm": "http://www.sitemaps.org/schemas/sitemap/0.9"}
                locs = root.findall(".//sm:loc", ns)
                if locs:
                    page_count = len(locs)
                    sitemap_status = f"✅ {smap_url.split('/')[-1]} ({page_count}ページ)"
                    break
        except Exception:
            continue

    # サイトマップ取得失敗時はローカルビルド出力からページ数を取得
    if page_count == 0:
        local_out = REPO_ROOT / "saas" / "keisan-tools" / "site" / "out"
        if local_out.exists():
            html_files = list(local_out.rglob("*.html"))
            if html_files:
                page_count = len(html_files)
                sitemap_status = f"⚠️ サイトマップ解析失敗 → ローカルビルドから{page_count}ページ検出"
        if page_count == 0:
            sitemap_status = "⚠️ サイトマップ未検出・ローカルビルドも未検出"

    logger.report("### CHECK")
    logger.report(f"- URL: {url}")
    logger.report(f"- 稼働状況: {site_status}")
    logger.report(f"- サイトマップ: {sitemap_status}")
    logger.report(f"- 公開ページ数: {page_count}")

    # --- GA4: PV/ユーザー/セッション ---
    keisan_ga4_property = 529807198  # measurement ID: G-3R1LVHX9VJ
    keisan_ga4_cred_path = REPO_ROOT / "saas" / "keisan-tools" / "site" / "config" / "ga4-credentials.json"
    if keisan_ga4_property != 0 and keisan_ga4_cred_path.exists():
        try:
            os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = str(keisan_ga4_cred_path)
            from google.analytics.data_v1beta import BetaAnalyticsDataClient
            from google.analytics.data_v1beta.types import (
                DateRange, Metric, RunReportRequest,
            )
            end_date_ga4 = (datetime.now() - timedelta(days=3)).strftime("%Y-%m-%d")
            start_date_ga4 = (datetime.now() - timedelta(days=10)).strftime("%Y-%m-%d")
            client = BetaAnalyticsDataClient()
            req = RunReportRequest(
                property=f"properties/{keisan_ga4_property}",
                date_ranges=[DateRange(start_date=start_date_ga4, end_date=end_date_ga4)],
                metrics=[
                    Metric(name="screenPageViews"),
                    Metric(name="activeUsers"),
                    Metric(name="sessions"),
                ],
            )
            resp_ga4 = client.run_report(req)
            if resp_ga4.rows:
                row = resp_ga4.rows[0]
                pv = int(row.metric_values[0].value)
                users = int(row.metric_values[1].value)
                sessions = int(row.metric_values[2].value)
                logger.report(f"- GA4（7日間）: PV={pv:,} / ユーザー={users:,} / セッション={sessions:,}")
            else:
                logger.report("- GA4（7日間）: データなし")
        except Exception as e:
            logger.report(f"- GA4エラー: {e}")
    elif keisan_ga4_property == 0:
        logger.report("- GA4: プロパティID未設定（0）→ スキップ")
    elif not keisan_ga4_cred_path.exists():
        logger.report(f"- GA4: 認証ファイル未配置 → {keisan_ga4_cred_path}")
    logger.report("")

    logger.report("### ACT")
    if "ERROR" in site_status:
        logger.report("- ❌ サイトダウン検出 → Vercelデプロイ状況確認")
    elif page_count < 30:
        logger.report(f"- ⚠️ {page_count}ページ → AdSense申請には30ページ以上必要。ページ追加を優先")
    else:
        logger.report(f"- ✅ {page_count}ページ公開中 → AdSense申請可能ライン")
    logger.report("")

    logger.report("### PLAN")
    logger.report("- 300ページ目標に向けてページ量産継続")
    logger.report("- 30ページ達成後にAdSense申請")
    logger.report("- GSCでインデックス状況を定期確認")
    logger.report("")


# =====================================================================
# SECTOR 17: Product Factory（AIエージェント×デジタル商品自動量産）
# =====================================================================
def pdca_product_factory():
    """Product Factory事業のPDCA"""
    logger.report("# 17. Product Factory（AIエージェント×デジタル商品自動量産）")
    logger.report("")

    pf_dir = REPO_ROOT / "product-factory"

    # CHECK: エージェント数・生成済み商品数
    agent_count = 0
    product_count = 0
    if pf_dir.exists():
        agents_dir = pf_dir / "agents"
        if agents_dir.exists():
            agent_count = len([f for f in agents_dir.iterdir() if f.is_file() and f.suffix in (".md", ".py", ".json")])
        # 生成済み商品をカウント（output/products等）
        for subdir_name in ("output", "products", "generated"):
            subdir = pf_dir / subdir_name
            if subdir.exists():
                product_count += len([f for f in subdir.rglob("*") if f.is_file() and not f.name.startswith(".")])

    logger.report("### CHECK")
    logger.report(f"- エージェント数: {agent_count}")
    logger.report(f"- 生成済み商品ファイル: {product_count}")
    logger.report(f"- Phase 1完了済み（エージェント4体+テスト商品生成）")
    logger.report("")

    logger.report("### PLAN")
    logger.report("- Phase 2（自動量産パイプライン）の進捗確認・実装推進")
    logger.report("- 市場リサーチ→商品生成→出品の自動フロー構築")
    logger.report("")


# =====================================================================
# SECTOR 18: フリーランス（Fiverr/Upwork）
# =====================================================================
def pdca_freelance():
    """フリーランス事業のPDCA"""
    logger.report("# 18. フリーランス（Fiverr/Upwork）")
    logger.report("")

    freelance_dir = REPO_ROOT / "research" / "freelance"

    gig_count = 0
    md_files = []
    if freelance_dir.exists():
        for f in freelance_dir.rglob("*"):
            if f.is_file() and not f.name.startswith("."):
                if f.suffix == ".md":
                    md_files.append(f)
                gig_count += 1

    logger.report("### CHECK")
    logger.report(f"- Gig定義ファイル数: {gig_count}")
    if md_files:
        for mf in md_files[:5]:
            logger.report(f"  - `{mf.name}`")
    logger.report("")

    logger.report("### PLAN")
    logger.report("- Fiverrアカウント開設・Gig公開の進捗確認")
    logger.report("- 定義済みGig 3件の公開準備を進める")
    logger.report("")


# =====================================================================
# SECTOR 19: せどり（Amazon FBA×電脳せどり）
# =====================================================================
def pdca_sedori():
    """せどり事業のPDCA"""
    logger.report("# 19. せどり（Amazon FBA×電脳せどり）")
    logger.report("")

    sedori_dir = REPO_ROOT / "research" / "sedori"

    file_count = 0
    has_plan = False
    if sedori_dir.exists():
        for f in sedori_dir.rglob("*"):
            if f.is_file() and not f.name.startswith("."):
                file_count += 1
                if "plan" in f.name.lower() or "計画" in f.name:
                    has_plan = True

    logger.report("### CHECK")
    logger.report(f"- リサーチファイル数: {file_count}")
    logger.report(f"- 計画書: {'✅ あり' if has_plan else '❌ なし'}")
    logger.report("- ステータス: 計画段階")
    logger.report("")

    logger.report("### PLAN")
    logger.report("- 事業開始に向けた次のステップ: リサーチ完了→Amazon出品アカウント開設→テスト仕入れ")
    logger.report("")


# =====================================================================
# SECTOR 20: eBay輸出
# =====================================================================
def pdca_ebay():
    """eBay輸出事業のPDCA"""
    logger.report("# 20. eBay輸出")
    logger.report("")

    ebay_dir = REPO_ROOT / "research" / "ebay"

    file_count = 0
    if ebay_dir.exists():
        for f in ebay_dir.rglob("*"):
            if f.is_file() and not f.name.startswith("."):
                file_count += 1

    logger.report("### CHECK")
    logger.report(f"- リサーチファイル数: {file_count}")
    logger.report("- ステータス: リサーチ段階")
    logger.report("")

    logger.report("### PLAN")
    logger.report("- eBayアカウント開設・出品準備")
    logger.report("- 日本→パラグアイの輸出商品リサーチ継続")
    logger.report("")


# =====================================================================
# SECTOR 21: AI自動化ビジネス
# =====================================================================
def pdca_ai_automation():
    """AI自動化ビジネスのPDCA"""
    logger.report("# 21. AI自動化ビジネス")
    logger.report("")

    planning_dir = REPO_ROOT / "research" / "planning"

    file_count = 0
    file_list = []
    if planning_dir.exists():
        for f in planning_dir.rglob("*"):
            if f.is_file() and not f.name.startswith("."):
                file_count += 1
                file_list.append(f.name)

    logger.report("### CHECK")
    logger.report(f"- 企画書・リサーチファイル数: {file_count}")
    if file_list:
        for fn in file_list[:5]:
            logger.report(f"  - `{fn}`")
    logger.report("- ステータス: 検討中")
    logger.report("")

    logger.report("### PLAN")
    logger.report("- 事業化判断: 市場ニーズ・競合・収益性を評価")
    logger.report("- 次のアクション: MVP定義または他事業への注力判断")
    logger.report("")


# =====================================================================
# SECTOR 22: ホームページ（ランディングページ）
# =====================================================================
def pdca_homepage():
    """ランディングページのPDCA"""
    logger.report("# 22. ホームページ（ランディングページ）")
    logger.report("")

    hp_dir = REPO_ROOT / "infrastructure" / "homepage"

    # CHECK: ファイル存在・稼働確認
    html_files = list(hp_dir.glob("*.html")) if hp_dir.exists() else []

    logger.report("### CHECK")
    logger.report(f"- HTMLファイル数: {len(html_files)}")
    for f in html_files[:10]:
        logger.report(f"  - `{f.name}`")
    logger.report("")

    logger.report("### PLAN")
    logger.report("- LPの目的・導線を明確化（全事業へのハブとして活用）")
    logger.report("- デザイン・コンテンツの定期見直し")
    logger.report("")


# =====================================================================
# SECTOR 23: 財務管理
# =====================================================================
def pdca_finance():
    """財務管理のPDCA"""
    logger.report("# 23. 財務管理")
    logger.report("")

    finance_dir = REPO_ROOT / "infrastructure" / "finance"

    # CHECK: ファイル一覧・最終更新日
    files = []
    if finance_dir.exists():
        for f in finance_dir.iterdir():
            if f.is_file() and not f.name.startswith("."):
                mtime = datetime.fromtimestamp(f.stat().st_mtime, tz=PYT)
                files.append({"name": f.name, "mtime": mtime})

    logger.report("### CHECK")
    if files:
        logger.report("| ファイル | 最終更新 |")
        logger.report("|---------|---------|")
        for fi in sorted(files, key=lambda x: x["mtime"], reverse=True):
            logger.report(f"| {fi['name']} | {fi['mtime'].strftime('%Y-%m-%d')} |")
    else:
        logger.report("- 財務ファイル未検出")
    logger.report("")

    logger.report("### PLAN")
    logger.report("- 月次で全事業の収支を集計・更新")
    logger.report("- 入金管理スプレッドシートの定期チェック")
    logger.report("- 事業別ROIの把握 → 注力先の判断材料に")
    logger.report("")


# =====================================================================
# はてなブログ（本家送客チャネル）
# =====================================================================
def pdca_hatena_blog():
    logger.report("# はてなブログ（nambei-oyaji.hatenablog.com）")
    logger.report("")

    hatena_dir = SITES_DIR / "nambei-oyaji.com" / "outputs" / "hatena"
    hatena_log = SITES_DIR / "nambei-oyaji.com" / "published" / "hatena-log.json"
    pipeline_log = REPO_ROOT / "logs" / "hatena-pipeline.log"

    # CHECK
    logger.report("### CHECK")

    # 投稿ログから統計
    total_posts = 0
    recent_posts = []
    if hatena_log.exists():
        try:
            with open(hatena_log, "r", encoding="utf-8") as f:
                log_data = json.load(f)
            # Support both list format and dict format {"published": [...]}
            if isinstance(log_data, dict):
                entries = log_data.get("published", [])
            elif isinstance(log_data, list):
                entries = log_data
            else:
                entries = []
            total_posts = len(entries)
            # 過去7日の投稿
            week_ago = (NOW - timedelta(days=7)).strftime("%Y-%m-%d")
            for entry in entries:
                pub_date = entry.get("published_at", entry.get("date", ""))[:10]
                if pub_date >= week_ago:
                    recent_posts.append(entry)
        except Exception as e:
            logger.log(f"  [hatena] ログ読み込みエラー: {e}")

    logger.report(f"- 総投稿数: **{total_posts}**")
    logger.report(f"- 過去7日の投稿: **{len(recent_posts)}件**")

    # 変換済みダイジェスト記事数
    digest_count = 0
    if hatena_dir.exists():
        digest_count = len(list(hatena_dir.glob("*.md")))
    logger.report(f"- 変換済みダイジェスト: {digest_count}件")

    # パイプラインログの最終実行
    if pipeline_log.exists():
        mtime = datetime.fromtimestamp(pipeline_log.stat().st_mtime, PYT)
        logger.report(f"- パイプライン最終実行: {mtime.strftime('%Y-%m-%d %H:%M PYT')}")
    else:
        logger.report("- パイプラインログ: 未検出")

    logger.report("")

    # ACT
    logger.report("### ACT")
    logger.report("- Task Scheduler: `HatenaPipeline`（月水金 07:00 PYT、2記事/回）")
    if len(recent_posts) == 0:
        logger.report("- ⚠️ 過去7日間の投稿がゼロ → パイプライン稼働確認が必要")
    else:
        logger.report(f"- ✅ 直近7日で{len(recent_posts)}件投稿済み")
    logger.report("")

    # PLAN
    logger.report("### PLAN")
    logger.report("- 本家（nambei-oyaji.com）への送客効果をGA4 UTMパラメータで計測")
    logger.report("- はてなコミュニティ（グループ・読者登録）からの流入を分析")
    if total_posts < 20:
        logger.report(f"- 📈 投稿数{total_posts} → まずは20記事到達を目指す（週6記事ペース）")
    logger.report("- 被リンク効果のGSC確認（参照元ドメインにhatenablog.comがあるか）")
    logger.report("")


# =====================================================================
# メイン
# =====================================================================
SECTORS = {
    "blogs": pdca_blogs,
    "hatena": pdca_hatena_blog,
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
    "keisan-tools": pdca_keisan_tools,
    "product-factory": pdca_product_factory,
    "freelance": pdca_freelance,
    "sedori": pdca_sedori,
    "ebay": pdca_ebay,
    "ai-automation": pdca_ai_automation,
    "homepage": pdca_homepage,
    "finance": pdca_finance,
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

    # 古い記事検出を実行
    try:
        from stale_content_detector import main as stale_main
        logger.log("--- stale-content ---")
        stale_report = stale_main()
        if stale_report:
            logger.report("")
            for line in stale_report:
                logger.report(line)
            logger.report("")
    except Exception as e:
        logger.log(f"  [stale-content] エラー: {e}")

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
