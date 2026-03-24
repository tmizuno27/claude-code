#!/usr/bin/env python3
"""
Healthchecks.io セットアップスクリプト

全タスクのチェックを Healthchecks.io API で一括作成し、
各PS1ランチャーに追加するping URLを config.json に出力する。

【使い方】
1. https://healthchecks.io でアカウント作成（GitHub認証OK）
2. プロジェクト作成 → Settings → API Access → API key (read-write) をコピー
3. secrets.json に追加:
   "healthchecks": { "api_key": "YOUR_API_KEY_HERE" }
4. このスクリプトを実行:
   python setup_healthchecks.py
5. config.json が生成される → integrate_ps1.py で全PS1に自動反映
"""

import json
import sys
from pathlib import Path

try:
    import requests
except ImportError:
    print("ERROR: pip install requests")
    sys.exit(1)

SCRIPT_DIR = Path(__file__).parent
CONFIG_FILE = SCRIPT_DIR / "config.json"
BLOG_CONFIG = Path(__file__).parent.parent.parent / "sites" / "nambei-oyaji.com" / "config"

# Healthchecks.io API
HC_API = "https://healthchecks.io/api/v3/checks/"

# 全タスク定義（名前、タグ、期待周期、猶予時間）
TASKS = [
    # インフラ系
    {"name": "GitAutoSync-Data", "tags": "infra", "timeout": 120, "grace": 300,
     "desc": "Git自動同期 (1分おき)"},
    {"name": "GoogleSheetsSync", "tags": "infra", "timeout": 600, "grace": 600,
     "desc": "Google Sheets→CSV取得 (5分おき)"},

    # ブログ・分析系（日次）
    {"name": "BlogUpdatePV", "tags": "blog daily", "schedule": "0 5 * * *", "tz": "America/Asuncion", "grace": 3600,
     "desc": "GA4→記事別PV→CSV→Sheets (毎日05:00 PYT)"},
    {"name": "BlogDailyAnalytics", "tags": "blog daily", "schedule": "0 7 * * *", "tz": "America/Asuncion", "grace": 3600,
     "desc": "GA4+SC+WP日次レポート (毎日07:00 PYT)"},
    {"name": "BlogSheetSync", "tags": "blog daily", "schedule": "0 19 * * *", "tz": "America/Asuncion", "grace": 3600,
     "desc": "記事管理スプレッドシート更新 (毎日19:00 PYT)"},
    {"name": "NotionSync", "tags": "blog daily", "schedule": "30 18 * * *", "tz": "America/Asuncion", "grace": 3600,
     "desc": "CSV→Notion DB+WPステータス同期 (毎日18:30 PYT)"},

    # ブログ・コンテンツ系（週次）
    {"name": "BlogAutoPublish", "tags": "blog weekly", "schedule": "0 18 * * 1,4", "tz": "America/Asuncion", "grace": 7200,
     "desc": "記事自動生成→WP投稿 (月木18:00 PYT)"},
    {"name": "BlogWeeklyReport", "tags": "blog weekly", "schedule": "0 19 * * 0", "tz": "America/Asuncion", "grace": 3600,
     "desc": "週次Analyticsレポート (日曜19:00 PYT)"},
    {"name": "BlogKeywordResearch", "tags": "blog weekly", "schedule": "0 20 * * 0", "tz": "America/Asuncion", "grace": 3600,
     "desc": "KW調査→キューに追加 (日曜20:00 PYT)"},
    {"name": "BlogContentCalendar", "tags": "blog weekly", "schedule": "0 20 * * 6", "tz": "America/Asuncion", "grace": 3600,
     "desc": "コンテンツカレンダー更新 (土曜20:00 PYT)"},
    {"name": "BlogInternalLinker", "tags": "blog weekly", "schedule": "0 20 * * 4", "tz": "America/Asuncion", "grace": 3600,
     "desc": "内部リンク最適化 (木曜20:00 PYT)"},
    {"name": "BlogFactCheck", "tags": "blog weekly", "schedule": "0 10 * * 3", "tz": "America/Asuncion", "grace": 7200,
     "desc": "ファクトチェック (水曜10:00 PYT)"},

    # メンテナンス系
    {"name": "BlogUptimeMonitor", "tags": "maintenance", "timeout": 2400, "grace": 1800,
     "desc": "サイト死活監視 (30分おき)"},
    {"name": "BlogBrokenLinks", "tags": "maintenance weekly", "schedule": "0 21 * * 0", "tz": "America/Asuncion", "grace": 3600,
     "desc": "リンク切れチェック (日曜21:00 PYT)"},
    {"name": "BlogNewKeywords", "tags": "maintenance weekly", "schedule": "30 20 * * 1", "tz": "America/Asuncion", "grace": 3600,
     "desc": "GSC新規KW検出 (月曜20:30 PYT)"},
    {"name": "BlogRewriteDetector", "tags": "maintenance weekly", "schedule": "30 21 * * 1", "tz": "America/Asuncion", "grace": 3600,
     "desc": "リライト候補抽出 (月曜21:30 PYT)"},
    {"name": "BlogWpBackup", "tags": "maintenance weekly", "schedule": "0 22 * * 6", "tz": "America/Asuncion", "grace": 3600,
     "desc": "WP全記事バックアップ (土曜22:00 PYT)"},

    # X系
    {"name": "XAutoPost-Morning", "tags": "x daily", "schedule": "30 18 * * *", "tz": "America/Asuncion", "grace": 7200,
     "desc": "X朝投稿 (毎日18:30 PYT)"},
    {"name": "XAutoPost-Noon", "tags": "x daily", "schedule": "30 23 * * *", "tz": "America/Asuncion", "grace": 7200,
     "desc": "X昼投稿 (毎日23:30 PYT)"},
    {"name": "XAutoPost-Evening", "tags": "x daily", "schedule": "0 8 * * *", "tz": "America/Asuncion", "grace": 7200,
     "desc": "X夜投稿 (毎日08:00 PYT)"},
    {"name": "XAnalyticsDaily", "tags": "x daily", "schedule": "0 10 * * *", "tz": "America/Asuncion", "grace": 3600,
     "desc": "Xアカウント指標レポート (毎日10:00 PYT)"},

    # 統合レポート
    {"name": "AllBusinessWeeklyKPI", "tags": "report weekly", "schedule": "30 19 * * 0", "tz": "America/Asuncion", "grace": 3600,
     "desc": "全事業統合KPIレポート (日曜19:30 PYT)"},
]

# PS1ファイルとタスク名のマッピング
PS1_MAPPING = {
    "GitAutoSync-Data": "auto-sync.ps1",
    "GoogleSheetsSync": None,  # Python直接実行（Task Scheduler）
    "BlogUpdatePV": "blog-update-pv.ps1",
    "BlogDailyAnalytics": "blog-daily-analytics.ps1",
    "BlogSheetSync": "blog-support-tasks.ps1:sheet",
    "NotionSync": "notion-sync.ps1",
    "BlogAutoPublish": "blog-auto-publish.ps1",
    "BlogWeeklyReport": "blog-support-tasks.ps1:analytics",
    "BlogKeywordResearch": "blog-support-tasks.ps1:keyword",
    "BlogContentCalendar": "blog-support-tasks.ps1:calendar",
    "BlogInternalLinker": "blog-support-tasks.ps1:internal",
    "BlogFactCheck": "blog-fact-check.ps1",
    "BlogUptimeMonitor": "blog-uptime-monitor.ps1",
    "BlogBrokenLinks": "blog-broken-links.ps1",
    "BlogNewKeywords": "blog-new-keywords.ps1",
    "BlogRewriteDetector": "blog-rewrite-detector.ps1",
    "BlogWpBackup": "blog-wp-backup.ps1",
    "XAutoPost-Morning": "x-auto-post.ps1:morning",
    "XAutoPost-Noon": "x-auto-post.ps1:noon",
    "XAutoPost-Evening": "x-auto-post.ps1:evening",
    "XAnalyticsDaily": "x-analytics-daily.ps1",
    "AllBusinessWeeklyKPI": "all-business-kpi.ps1",
}


def load_api_key():
    """secrets.json から Healthchecks.io API キーを取得"""
    # blog/config/secrets.json
    secrets_path = BLOG_CONFIG / "secrets.json"
    if not secrets_path.exists():
        # 直接パス
        secrets_path = Path(r"C:\Users\tmizu") / "マイドライブ" / "GitHub" / "claude-code" / "sites" / "nambei-oyaji.com" / "config" / "secrets.json"

    if not secrets_path.exists():
        print(f"ERROR: secrets.json が見つかりません: {secrets_path}")
        print("secrets.json に以下を追加してください:")
        print('  "healthchecks": { "api_key": "YOUR_API_KEY_HERE" }')
        sys.exit(1)

    with open(secrets_path, "r", encoding="utf-8") as f:
        secrets = json.load(f)

    api_key = secrets.get("healthchecks", {}).get("api_key", "")
    if not api_key or "YOUR" in api_key:
        print("ERROR: healthchecks.api_key が未設定です")
        print("secrets.json に以下を追加してください:")
        print('  "healthchecks": { "api_key": "YOUR_READ_WRITE_API_KEY" }')
        sys.exit(1)

    return api_key


def create_check(api_key, task):
    """Healthchecks.io にチェックを作成"""
    headers = {"X-Api-Key": api_key, "Content-Type": "application/json"}

    payload = {
        "name": task["name"],
        "tags": task.get("tags", ""),
        "desc": task.get("desc", ""),
        "channels": "*",  # 全通知チャネル
    }

    # cron式スケジュール or simple timeout
    if "schedule" in task:
        payload["schedule"] = task["schedule"]
        payload["tz"] = task.get("tz", "America/Asuncion")
        payload["grace"] = task.get("grace", 3600)
    else:
        payload["timeout"] = task.get("timeout", 86400)
        payload["grace"] = task.get("grace", 3600)

    resp = requests.post(HC_API, headers=headers, json=payload, timeout=30)

    if resp.status_code in (200, 201):
        data = resp.json()
        return {
            "name": task["name"],
            "ping_url": data["ping_url"],
            "uuid": data["ping_url"].split("/")[-1],
            "status": "created",
        }
    elif resp.status_code == 409:
        # 既存のチェックがある場合はリストから取得
        print(f"  {task['name']}: 既に存在。スキップ")
        return None
    else:
        print(f"  ERROR creating {task['name']}: {resp.status_code} {resp.text}")
        return None


def get_existing_checks(api_key):
    """既存チェック一覧を取得"""
    headers = {"X-Api-Key": api_key}
    resp = requests.get(HC_API, headers=headers, timeout=30)
    if resp.status_code == 200:
        return {c["name"]: c for c in resp.json()["checks"]}
    return {}


def setup_discord_integration(api_key):
    """Discord連携の手順を表示"""
    print("\n" + "=" * 60)
    print("Discord連携の設定手順")
    print("=" * 60)
    print("1. https://healthchecks.io にログイン")
    print("2. プロジェクト → Integrations → Discord")
    print("3. 既存のDiscord Webhookを登録:")
    print("   （settings.json の discord.webhook_url を使用）")
    print("4. 'Save' をクリック")
    print("=" * 60)


def main():
    print("=== Healthchecks.io セットアップ ===\n")

    api_key = load_api_key()
    print(f"API キー取得OK (末尾: ...{api_key[-4:]})\n")

    # 既存チェック確認
    existing = get_existing_checks(api_key)
    print(f"既存チェック: {len(existing)}件\n")

    # チェック作成
    results = {}
    created = 0
    skipped = 0

    for task in TASKS:
        name = task["name"]
        if name in existing:
            print(f"  [SKIP] {name} (既に存在)")
            results[name] = {
                "name": name,
                "ping_url": existing[name]["ping_url"],
                "uuid": existing[name]["ping_url"].split("/")[-1],
                "ps1": PS1_MAPPING.get(name),
            }
            skipped += 1
            continue

        result = create_check(api_key, task)
        if result:
            result["ps1"] = PS1_MAPPING.get(name)
            results[name] = result
            print(f"  [OK] {name} → {result['ping_url']}")
            created += 1

    print(f"\n作成: {created}, スキップ: {skipped}, 合計: {len(results)}")

    # config.json に保存
    config = {
        "generated": str(Path(__file__).name),
        "total_checks": len(results),
        "checks": results,
    }
    with open(CONFIG_FILE, "w", encoding="utf-8") as f:
        json.dump(config, f, ensure_ascii=False, indent=2)
    print(f"\n設定保存: {CONFIG_FILE}")

    # Discord連携の案内
    setup_discord_integration(api_key)

    print(f"\n次のステップ:")
    print(f"  python {SCRIPT_DIR / 'integrate_ps1.py'}")
    print(f"  → 全PS1ファイルにpingを自動追加します")


if __name__ == "__main__":
    main()
