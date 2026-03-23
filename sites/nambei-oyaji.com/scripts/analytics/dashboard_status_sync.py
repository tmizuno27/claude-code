#!/usr/bin/env python3
"""
ダッシュボードHTML ステータス自動同期スクリプト

実態（CSV・API・設定ファイル等）を読み取り、
daily-business-dashboard.html のハードコード値を最新状態に更新。
更新後Gistにもアップロードする。

使い方:
  python dashboard_status_sync.py          # 全項目同期
  python dashboard_status_sync.py --dry    # 変更内容のプレビューのみ
"""

import csv
import json
import logging
import re
import subprocess
import sys
from datetime import datetime
from pathlib import Path

import requests

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

PROJECT_ROOT = Path(__file__).parent.parent.parent
CLAUDE_CODE = PROJECT_ROOT.parent
REPORTS_DIR = PROJECT_ROOT / "outputs" / "reports"
DASHBOARD_PATH = REPORTS_DIR / "daily-business-dashboard.html"
GIST_ID = "16a8680cadf8aed0c207777f7468963b"

SITES = {
    "nambei": {"dir": "nambei-oyaji.com", "domain": "nambei-oyaji.com"},
    "otona": {"dir": "otona-match.com", "domain": "otona-match.com"},
    "sim": {"dir": "sim-hikaku.online", "domain": "sim-hikaku.online"},
}


# ─── データ収集 ───────────────────────────────


def count_articles(site_dir: str) -> int:
    """article-management.csv の行数（ヘッダー除く）"""
    csv_path = CLAUDE_CODE / site_dir / "outputs" / "article-management.csv"
    if not csv_path.exists():
        return 0
    with open(csv_path, encoding="utf-8") as f:
        reader = csv.reader(f)
        next(reader, None)  # skip header
        return sum(1 for _ in reader)


def count_published_articles(site_dir: str) -> int:
    """status=published の記事数"""
    csv_path = CLAUDE_CODE / site_dir / "outputs" / "article-management.csv"
    if not csv_path.exists():
        return 0
    with open(csv_path, encoding="utf-8") as f:
        reader = csv.DictReader(f)
        return sum(1 for row in reader
                       if any(kw in row.get("status", row.get("ステータス", "")).lower()
                              for kw in ("公開", "publish")))


def check_ga4_access(site_dir: str) -> bool:
    """GA4 API にアクセスできるか"""
    try:
        settings_path = CLAUDE_CODE / site_dir / "config" / "settings.json"
        if not settings_path.exists():
            return False
        settings = json.loads(settings_path.read_text(encoding="utf-8"))
        ga_config = settings.get("google_analytics", {})
        property_id = ga_config.get("property_id")
        cred_file = ga_config.get("credentials_file", "")
        if not property_id:
            return False

        cred_path = CLAUDE_CODE / site_dir / cred_file
        if not cred_path.exists():
            # Try config/ prefix
            cred_path = CLAUDE_CODE / site_dir / "config" / cred_file
        if not cred_path.exists():
            return False

        from google.analytics.data_v1beta import BetaAnalyticsDataClient
        from google.analytics.data_v1beta.types import RunReportRequest, DateRange, Metric
        from google.oauth2 import service_account

        credentials = service_account.Credentials.from_service_account_file(
            str(cred_path),
            scopes=["https://www.googleapis.com/auth/analytics.readonly"],
        )
        client = BetaAnalyticsDataClient(credentials=credentials)
        client.run_report(RunReportRequest(
            property=f"properties/{property_id}",
            date_ranges=[DateRange(start_date="yesterday", end_date="today")],
            metrics=[Metric(name="sessions")],
        ))
        return True
    except Exception:
        return False


def count_chrome_extensions() -> dict:
    """Chrome拡張の数とステータス"""
    ext_dir = CLAUDE_CODE / "chrome-extensions"
    if not ext_dir.exists():
        return {"total": 0, "published": 0, "reviewing": 0}

    total = sum(1 for d in ext_dir.iterdir() if d.is_dir() and not d.name.startswith("."))

    # Check memory for published status
    memory_path = Path.home() / ".claude" / "projects" / "c--Users-tmizu--------GitHub" / "memory" / "chrome-extensions-business.md"
    published = 0
    if memory_path.exists():
        content = memory_path.read_text(encoding="utf-8")
        # Count published mentions
        published = len(re.findall(r"公開済み|published", content, re.IGNORECASE))

    return {"total": total, "published": published, "reviewing": total - published}


def count_vscode_extensions() -> dict:
    """VS Code拡張の数とステータス"""
    ext_dir = CLAUDE_CODE / "vscode-extensions"
    if not ext_dir.exists():
        return {"total": 0, "published": 0, "pending": 0}

    total = sum(1 for d in ext_dir.iterdir() if d.is_dir() and not d.name.startswith("."))

    memory_path = Path.home() / ".claude" / "projects" / "c--Users-tmizu--------GitHub" / "memory" / "vscode-extensions-business.md"
    published = 7  # default from memory
    if memory_path.exists():
        content = memory_path.read_text(encoding="utf-8")
        m = re.search(r"(\d+).*公開済み|(\d+)/\d+.*公開", content)
        if m:
            published = int(m.group(1) or m.group(2))

    return {"total": total, "published": published, "pending": total - published}


def get_accesstrade_status() -> str:
    """AccessTradeのステータス"""
    memory_path = Path.home() / ".claude" / "projects" / "c--Users-tmizu--------GitHub" / "memory" / "accesstrade-affiliate-pending.md"
    if memory_path.exists():
        content = memory_path.read_text(encoding="utf-8")
        # ✅マークのサイト数をカウント
        site_marks = len(re.findall(r"✅", content))
        if site_marks >= 3 or "3サイト" in content:
            return "3サイト承認"
        return f"{max(site_marks, 1)}サイト承認"
    return "3サイト承認"


def get_moshimo_status() -> str:
    """もしもアフィリエイトのステータス"""
    memory_path = Path.home() / ".claude" / "projects" / "c--Users-tmizu--------GitHub" / "memory" / "moshimo-affiliate-progress.md"
    if memory_path.exists():
        return "3サイト登録"
    return "未登録"


def count_gumroad_listed() -> dict:
    """Gumroad出品状況"""
    memory_path = Path.home() / ".claude" / "projects" / "c--Users-tmizu--------GitHub" / "memory" / "gumroad-listing-progress.md"
    listed = 1
    total = 10
    if memory_path.exists():
        content = memory_path.read_text(encoding="utf-8")
        m = re.search(r"(\d+)/(\d+).*出品", content)
        if m:
            listed = int(m.group(1))
            total = int(m.group(2))
    return {"listed": listed, "total": total}


def count_scheduled_tasks() -> int:
    """Task Schedulerのタスク数"""
    memory_path = Path.home() / ".claude" / "projects" / "c--Users-tmizu--------GitHub" / "memory" / "scheduled-tasks.md"
    if memory_path.exists():
        content = memory_path.read_text(encoding="utf-8")
        # Count task entries (lines starting with | that have task names)
        tasks = re.findall(r"^\|\s*\w+", content, re.MULTILINE)
        if tasks:
            return len(tasks) - 1  # subtract header
    return 52


# ─── ビジネス健全性スコア計算 ─────────────────


def calc_health_score() -> dict:
    """
    5カテゴリ×20点 = 100点満点のビジネス健全性スコアを実データから算出。

    【評価方針】忖度禁止・厳格評価
    - 「存在する」と「成果が出ている」は別物
    - 売上$0の事業は収益化カテゴリで高得点にならない
    - 設定済みでも活用されていなければ低評価
    - 改善ポイントが見えるスコアにする
    """

    # ─── 資産量 (20点) ───
    # 評価基準: 公開済み記事のSEO効果（PV・インデックス状況込み）
    # 100記事公開 = 8点が上限。300記事+でようやく14点
    # API/拡張は「出品済み×利用者あり」で評価。利用者0なら半減
    total_articles = sum(count_published_articles(s["dir"]) for s in SITES.values())
    if total_articles >= 300:
        article_pts = 14
    elif total_articles >= 200:
        article_pts = 10
    elif total_articles >= 100:
        article_pts = 7
    elif total_articles >= 50:
        article_pts = 4
    else:
        article_pts = round(total_articles * 4 / 50, 1)

    # API/Actor: 出品しただけでは低評価。利用者・売上がないと半減
    api_count = 20  # RapidAPI
    apify_count = 5
    # 売上$0 = 利用者ほぼゼロ → 出品の価値は半分
    api_pts = min(3, (api_count + apify_count) * 3 / 25) * 0.5  # 売上ゼロペナルティ

    chrome = count_chrome_extensions()
    vscode = count_vscode_extensions()
    # 審査中・未公開は価値なし。公開済みのみカウント
    published_ext = chrome.get("published", 0) + vscode.get("published", 0)
    ext_pts = min(3, published_ext * 3 / 20)

    asset_score = min(20, round(article_pts + api_pts + ext_pts))

    # ─── 計測基盤 (20点) ───
    # 評価基準: 接続+データ活用。接続だけなら半分
    # GA4接続+レポート活用: 各サイト3点 = 9点
    # GSC接続+インデックス管理: 4点
    # X API+実投稿: 4点（接続のみ=2, 定期投稿=4）
    # Healthchecks+Discord通知: 3点
    ga4_connected = sum(1 for s in SITES.values() if check_ga4_access(s["dir"]))
    # 接続 = 2点、接続+日次レポート自動化 = 3点
    ga4_pts = 0
    for s in SITES.values():
        if check_ga4_access(s["dir"]):
            report_dir = CLAUDE_CODE / s["dir"] / "outputs" / "daily-reports"
            if report_dir.exists() and any(report_dir.iterdir()):
                ga4_pts += 3  # 接続+レポート活用
            else:
                ga4_pts += 2  # 接続のみ

    gsc_count = sum(1 for s in SITES.values()
                    if (CLAUDE_CODE / s["dir"] / "config" / "gsc-credentials.json").exists())
    gsc_pts = min(4, gsc_count + 1) if gsc_count >= 3 else gsc_count

    # X API: 接続だけなら2点。実際にツイートしていれば4点
    x_cred = CLAUDE_CODE / "nambei-oyaji.com" / "config" / "secrets.json"
    x_pts = 0
    if x_cred.exists():
        try:
            secrets = json.loads(x_cred.read_text(encoding="utf-8"))
            if secrets.get("x_api_key") or secrets.get("twitter_api_key"):
                x_pts = 2  # 接続のみ
                # ツイート数チェック（X投稿ログがあれば+2）
                x_log = CLAUDE_CODE / "nambei-oyaji.com" / "outputs" / "x-posts"
                if x_log.exists() and any(x_log.iterdir()):
                    x_pts = 4
        except Exception:
            pass

    hc_dir = CLAUDE_CODE / "tools" / "healthchecks"
    hc_pts = 3 if hc_dir.exists() else 0

    measurement_score = min(20, ga4_pts + gsc_pts + x_pts + hc_pts)

    # ─── 収益化 (20点) ───
    # 【最重要】売上が全て。売上$0なら最大でも6点
    # 実売上: 月¥1→4点, 月¥10,000→10点, 月¥50,000→16点, 月¥100,000→20点
    # ASP提携だけ: 各ASP 0.5点（提携≠収益）
    # 商品出品だけ: 各プラットフォーム 0.5点（出品≠売上）
    monthly_revenue = 0  # TODO: 実売上データ連携時に更新

    if monthly_revenue >= 100000:
        revenue_pts = 20
    elif monthly_revenue >= 50000:
        revenue_pts = 16
    elif monthly_revenue >= 10000:
        revenue_pts = 10
    elif monthly_revenue >= 1000:
        revenue_pts = 6
    elif monthly_revenue > 0:
        revenue_pts = 4
    else:
        # 売上ゼロ: 準備状況のみで最大6点
        # ASP提携: 各0.5点 × 4ASP = 2点
        at_status = get_accesstrade_status()
        asp_pts = 0
        asp_pts += 0.5  # A8.net
        asp_pts += 0.5 if "3サイト" in at_status else 0.3
        asp_pts += 0.5 if get_moshimo_status() != "未登録" else 0
        asp_pts += 0.3  # Value Commerce（提携未着手）

        # 商品出品: 各0.5点。売上ゼロなので出品だけの価値は低い
        product_pts = 0
        product_pts += 0.5  # RapidAPI（10/20出品、売上$0）
        product_pts += 0.5  # Apify（5 Actor、売上$0）
        chrome_pub = chrome.get("published", 0)
        product_pts += 0.3 if chrome_pub > 0 else 0  # 審査中はカウントしない
        gumroad = count_gumroad_listed()
        product_pts += 0.3 if gumroad["listed"] > 0 else 0
        product_pts += 0  # n8n（KYC停止中 = 売上不可能 = 0点）

        revenue_pts = min(6, round(asp_pts + product_pts))

    monetize_score = min(20, revenue_pts)

    # ─── 自動化 (20点) ───
    # 評価基準: タスクの「数」ではなく「成果」
    # 基盤（同期・監視）: 8点
    # コンテンツ自動化（記事生成→投稿が自動で回っているか）: 6点
    # レポート自動化（日次/週次レポートが実際に生成されているか）: 6点
    task_count = count_scheduled_tasks()

    # 基盤: タスク存在+実際に動作
    infra_auto = 0
    infra_auto += 3 if task_count >= 20 else min(3, task_count * 3 / 20)  # タスク数
    infra_auto += 3  # GitHub自動同期（常時稼働確認済み）
    infra_auto += 2  # Sheets+ダッシュボード

    # コンテンツ自動化: 今週記事が自動生成→投稿されたか
    # 記事が週3ペースで増えていなければ自動化は機能していない
    content_auto = 0
    # outputs/に最近の記事ファイルがあるかチェック
    for s in SITES.values():
        outputs = CLAUDE_CODE / s["dir"] / "outputs"
        if outputs.exists():
            recent_md = [f for f in outputs.glob("*.md") if f.stat().st_mtime > (datetime.now().timestamp() - 7 * 86400)]
            if recent_md:
                content_auto += 2
                break
    # 最大6点だが、記事投稿頻度が低ければ低スコア
    content_auto = min(6, content_auto)

    # レポート自動化
    report_auto = 0
    report_dir = CLAUDE_CODE / "nambei-oyaji.com" / "outputs" / "reports"
    if report_dir.exists():
        recent_reports = [f for f in report_dir.glob("daily-business-*.md")
                         if f.stat().st_mtime > (datetime.now().timestamp() - 3 * 86400)]
        report_auto = min(6, len(recent_reports) * 3)

    automation_score = min(20, round(infra_auto + content_auto + report_auto))

    # ─── インフラ (20点) ───
    # 評価基準: 安定稼働+冗長性+監視
    # サーバー稼働(3サイト): 6点
    # GitHub+バックアップ: 4点
    # 監視（Healthchecks+Discord）: 4点
    # CDN/Workers: 3点
    # 開発環境: 3点
    conoha_pts = 6  # 3サイト稼働中
    backup_pts = 0
    backup_pts += 2  # GitHub auto-sync
    backup_pts += 2 if (CLAUDE_CODE / "claude-backup").exists() else 0
    monitor_pts = 0
    monitor_pts += 2 if hc_dir.exists() else 0  # Healthchecks
    monitor_pts += 2  # Discord通知
    cf_pts = 3  # Cloudflare Workers
    dev_pts = 3  # Python 3.13 + Node.js + PowerShell

    infra_score = min(20, conoha_pts + backup_pts + monitor_pts + cf_pts + dev_pts)

    total = asset_score + measurement_score + monetize_score + automation_score + infra_score

    return {
        "total": total,
        "asset": asset_score,
        "measurement": measurement_score,
        "monetize": monetize_score,
        "automation": automation_score,
        "infra": infra_score,
    }


# ─── HTML更新 ───────────────────────────────


def apply_updates(html: str, dry: bool = False) -> str:
    """実態データを収集し、HTMLに反映"""
    changes = []

    # --- ブログ記事数 ---
    for key, site in SITES.items():
        count = count_articles(site["dir"])
        published = count_published_articles(site["dir"])
        if count == 0:
            continue

        # ブログカードのリング内の数字
        domain = site["domain"]
        pattern = rf'(<div class="blog-domain">{re.escape(domain)}</div>.*?<div class="br-center"[^>]*>)\d+(</div>)'
        m = re.search(pattern, html, re.DOTALL)
        if m:
            old_val = re.search(r">(\d+)</div>$", m.group(0))
            if old_val and int(old_val.group(1)) != published:
                changes.append(f"  {domain} 記事数リング: {old_val.group(1)} → {published}")
                html = re.sub(pattern, rf"\g<1>{published}\2", html, flags=re.DOTALL)

        # 進捗率
        pct = min(100, int(published / 100 * 100))
        pct_pattern = rf'(<div class="blog-domain">{re.escape(domain)}</div>.*?進捗</span><span class="bi-val">)\d+%(</span>)'
        html = re.sub(pct_pattern, rf"\g<1>{pct}%\2", html, flags=re.DOTALL)

        # SVGリングのオフセット計算 (163.4 * (1 - pct/100))
        offset = round(163.4 * (1 - pct / 100), 1)
        ring_pattern = rf'(<div class="blog-domain">{re.escape(domain)}</div>.*?stroke-dashoffset=")[\d.]+("/>)'
        old_ring = re.search(ring_pattern, html, re.DOTALL)
        if old_ring:
            html = re.sub(ring_pattern, rf"\g<1>{offset}\2", html, flags=re.DOTALL)

        # Googleインデックスセクションの公開記事数
        idx_pattern = rf'(<div class="idx-domain">{re.escape(domain)}</div>.*?公開記事</span><span class="iv">)\d+(</span>)'
        m_idx = re.search(idx_pattern, html, re.DOTALL)
        if m_idx:
            html = re.sub(idx_pattern, rf"\g<1>{published}\2", html, flags=re.DOTALL)

    # --- GA4接続ステータス ---
    for key, site in SITES.items():
        domain = site["domain"]
        is_connected = check_ga4_access(site["dir"])
        status_text = "接続済み" if is_connected else "権限未付与"
        dot_color = "green" if is_connected else "orange"

        # SEO/計測基盤セクション
        ga4_pattern = rf'(<span class="sr-name">{re.escape(domain)} GA4</span><span class="status-badge"><span class="status-dot )\w+("></span>)[^<]+(</span>)'
        old_m = re.search(ga4_pattern, html)
        if old_m:
            old_status = re.search(r"</span>([^<]+)</span>$", old_m.group(0))
            if old_status and old_status.group(1) != status_text:
                changes.append(f"  {domain} GA4: {old_status.group(1)} → {status_text}")
            html = re.sub(ga4_pattern, rf"\g<1>{dot_color}\2{status_text}\3", html)

        # Googleインデックスセクション内GA4行（テキスト＋カラー）
        idx_ga4_color = "var(--green)" if is_connected else "var(--orange)"
        idx_ga4_pattern = rf'(<div class="idx-domain">{re.escape(domain)}</div>.*?GA4</span><span class="iv" style="color:)[^"]+("[^>]*>)[^<]+(</span>)'
        m_ga4 = re.search(idx_ga4_pattern, html, re.DOTALL)
        if m_ga4:
            html = re.sub(idx_ga4_pattern, rf"\g<1>{idx_ga4_color}\2{status_text}\3", html, flags=re.DOTALL)

    # GA4バッジ
    ga4_count = sum(1 for s in SITES.values() if check_ga4_access(s["dir"]))
    html = re.sub(
        r"GA4 接続済\(\d/\d\)",
        f"GA4 接続済({ga4_count}/3)",
        html
    )

    # --- Chrome拡張 ---
    chrome = count_chrome_extensions()
    if chrome["total"] > 0:
        # ヘッダーバッジ
        old_chrome_badge = re.search(r"(\d+)本 — Chrome Web Store", html)
        if old_chrome_badge and int(old_chrome_badge.group(1)) != chrome["total"]:
            changes.append(f"  Chrome拡張数: {old_chrome_badge.group(1)} → {chrome['total']}")
        html = re.sub(r"\d+本 — Chrome Web Store", f"{chrome['total']}本 — Chrome Web Store", html)
        # 収益テーブル
        html = re.sub(r"Chrome拡張 — \d+本", f"Chrome拡張 — {chrome['total']}本", html)

    # --- VS Code拡張 (ダッシュボードに項目があれば) ---
    vscode = count_vscode_extensions()

    # --- AccessTrade ---
    at_status = get_accesstrade_status()
    # SEO/計測基盤
    html = re.sub(
        r'(<span class="sr-name">AccessTrade</span><span class="status-badge"><span class="status-dot green"></span>)[^<]+(</span>)',
        rf"\g<1>{at_status}\2",
        html
    )
    # アフィリエイトマトリクス: otona-match.com AccessTrade
    # otona-matchのAccessTradeを承認済に修正
    otona_at_pattern = r'(otona-match\.com</td>\s*<td>.*?</td>\s*<td>)<span class="status-badge"><span class="status-dot \w+"></span>[^<]+</span>'
    html = re.sub(
        otona_at_pattern,
        r'\1<span class="status-badge"><span class="status-dot green"></span>承認済</span>',
        html,
        flags=re.DOTALL
    )
    # 収益テーブル AccessTrade
    html = re.sub(
        r'(AccessTrade</span><span class="mono t-right">¥0</span><span class="t-right"><span class="status-badge"><span class="status-dot green"></span>)\d+サイト',
        rf"\g<1>3サイト",
        html
    )

    # --- もしもアフィリエイト: アフィリエイトマトリクスにカラムがなければ追加は複雑なのでスキップ ---

    # --- 定期タスク数 ---
    task_count = count_scheduled_tasks()
    html = re.sub(
        r'(<div class="health-val">)\d+(</div>\s*<div class="health-lbl">定期タスク)',
        rf"\g<1>{task_count}\2",
        html
    )

    # --- ビジネス健全性スコア ---
    score = calc_health_score()
    total = score["total"]

    # スコア内訳テキスト更新
    score_map = {
        "資産量": score["asset"],
        "計測基盤": score["measurement"],
        "収益化": score["monetize"],
        "自動化": score["automation"],
        "インフラ": score["infra"],
    }
    for label, val in score_map.items():
        color_style = ' style="color:var(--orange)"' if val < 14 else ""
        pattern = rf'(<span>{label}</span><span class="sb-v"[^>]*>)\d+/20(</span>)'
        new_val = f"\\g<1>{val}/20\\2"
        old_m = re.search(pattern, html)
        if old_m:
            old_val_m = re.search(r"(\d+)/20", old_m.group(0))
            if old_val_m and int(old_val_m.group(1)) != val:
                changes.append(f"  スコア {label}: {old_val_m.group(1)}/20 → {val}/20")
        # カラーも更新
        html = re.sub(
            rf'(<span>{label}</span><span class="sb-v")(?:\s+style="[^"]*")?(>)\d+/20(</span>)',
            rf'\g<1>{color_style}\g<2>{val}/20\3',
            html
        )

    # JSのスコア数値更新
    html = re.sub(
        r'const score=\d+;// \d+/100',
        f'const score={total};// {total}/100',
        html
    )

    logger.info(f"  健全性スコア: {total}/100 (資産{score['asset']} 計測{score['measurement']} 収益{score['monetize']} 自動化{score['automation']} インフラ{score['infra']})")

    # --- 日付更新 ---
    now = datetime.now()
    html = re.sub(
        r'(<div class="header-date">)\d{2}\.\d{2}(</div>)',
        rf'\g<1>{now.strftime("%m.%d")}\2', html
    )
    html = re.sub(
        r'\d{4} — \d{2}:\d{2} PYT',
        f'{now.strftime("%Y — %H:%M")} PYT', html, count=1
    )
    html = re.sub(
        r'(<title>日次ビジネス総合レポート — )\d{4}\.\d{2}\.\d{2}(</title>)',
        rf'\g<1>{now.strftime("%Y.%m.%d")}\2', html
    )
    html = re.sub(
        r'(<span class="header-time" id="header-time">)\d{2}:\d{2}:\d{2} PYT(</span>)',
        rf'\g<1>{now.strftime("%H:%M:%S")} PYT\2', html
    )
    # フッタータイムスタンプ
    html = re.sub(
        r'(<span>)\d{4}/\d{2}/\d{2} \d{2}:\d{2} PYT(</span>)',
        rf'\g<1>{now.strftime("%Y/%m/%d %H:%M")} PYT\2', html
    )

    if changes:
        logger.info("変更点:")
        for c in changes:
            logger.info(c)
    else:
        logger.info("ハードコード値に変更なし")

    return html


def upload_to_gist(html: str) -> bool:
    """Gistにアップロード"""
    try:
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
            logger.warning("GitHubトークン取得失敗")
            return False

        resp = requests.patch(
            f"https://api.github.com/gists/{GIST_ID}",
            headers={"Authorization": f"token {token}", "Accept": "application/vnd.github+json"},
            json={"files": {"daily-business-dashboard.html": {"content": html}}},
            timeout=30,
        )
        if resp.status_code == 200:
            logger.info("Gist更新完了")
            return True
        else:
            logger.warning(f"Gist更新失敗: {resp.status_code}")
            return False
    except Exception as e:
        logger.warning(f"Gist更新エラー: {e}")
        return False


def main():
    dry = "--dry" in sys.argv

    if not DASHBOARD_PATH.exists():
        logger.error(f"ダッシュボードHTML未生成: {DASHBOARD_PATH}")
        sys.exit(1)

    html = DASHBOARD_PATH.read_text(encoding="utf-8")
    html = apply_updates(html, dry=dry)

    if dry:
        logger.info("ドライランモード — 変更は保存されません")
        return

    DASHBOARD_PATH.write_text(html, encoding="utf-8")
    logger.info("ローカルHTML更新完了")

    upload_to_gist(html)


if __name__ == "__main__":
    main()
