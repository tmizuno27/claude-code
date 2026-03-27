#!/usr/bin/env python3
"""
ダッシュボード更新スクリプト（1時間おき実行）

action-status.json の完了状態をHTMLに反映し、
タイムスタンプを更新してGistにアップロードする。

使い方:
  python dashboard_updater.py                    # 通常更新
  python dashboard_updater.py done <action-id>   # アクションを完了にする
  python dashboard_updater.py undo <action-id>   # アクションを未完了に戻す
  python dashboard_updater.py list               # アクション一覧表示
"""

import json
import logging
import re
import subprocess
import sys
from datetime import datetime
from pathlib import Path

import requests

import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

PROJECT_ROOT = Path(__file__).parent.parent.parent
REPORTS_DIR = PROJECT_ROOT / "outputs" / "reports"
DASHBOARD_PATH = REPORTS_DIR / "daily-business-dashboard.html"
ACTION_STATUS_PATH = REPORTS_DIR / "action-status.json"
GIST_ID = "16a8680cadf8aed0c207777f7468963b"


def load_action_status():
    if not ACTION_STATUS_PATH.exists():
        return {"date": datetime.now().strftime("%Y-%m-%d"), "actions": []}
    return json.loads(ACTION_STATUS_PATH.read_text(encoding="utf-8"))


def save_action_status(data):
    ACTION_STATUS_PATH.write_text(
        json.dumps(data, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8"
    )


def mark_action(action_id, done=True):
    """アクションの完了/未完了を切り替え"""
    data = load_action_status()
    found = False
    for action in data["actions"]:
        if action["id"] == action_id:
            action["done"] = done
            action["done_at"] = datetime.now().strftime("%H:%M") if done else None
            if done:
                action["completed_date"] = datetime.now().strftime("%Y-%m-%d")
            else:
                action.pop("completed_date", None)
            found = True
            status = "✅ 完了" if done else "☐ 未完了に戻し"
            print(f"{status}: {action['title']}")
            break
    if not found:
        print(f"エラー: アクションID '{action_id}' が見つかりません")
        print("利用可能なID:")
        for a in data["actions"]:
            print(f"  {a['id']}")
        return False
    save_action_status(data)
    return True


def list_actions():
    """アクション一覧を表示"""
    data = load_action_status()
    print(f"\n📋 今日の優先タスク ({data.get('date', '?')})")
    print("=" * 50)
    done_count = 0
    for a in data["actions"]:
        check = "✅" if a["done"] else "☐"
        time_str = f" ({a['done_at']})" if a.get("done_at") else ""
        print(f"  {check} [{a['priority']}] {a['title']}{time_str}")
        if a["done"]:
            done_count += 1
    total = len(data["actions"])
    print(f"\n  進捗: {done_count}/{total} 完了")
    if done_count == total:
        print("  🎉 全タスク完了！")


def apply_action_status_to_html(html, actions):
    """HTMLのアクションアイテムに完了状態を反映"""
    done_count = sum(1 for a in actions if a["done"])
    total = len(actions)

    for action in actions:
        aid = action["id"]
        if action["done"]:
            # Add 'done' class and change checkbox
            pattern = rf'class="action-item"(\s+data-action-id="{re.escape(aid)}")'
            replacement = rf'class="action-item done"\1'
            html = re.sub(pattern, replacement, html)

            # Change ☐ to ✅
            pattern = rf'(data-action-id="{re.escape(aid)}"><span class="a-check")>☐</span>'
            replacement = rf'\1>✅</span>'
            html = re.sub(pattern, replacement, html)

            # Remove existing done-time spans, then add current one
            html = re.sub(
                rf'(data-action-id="{re.escape(aid)}".*?</strong>)(?:<span class="done-time">.*?</span>)*',
                r'\1',
                html
            )
            if action.get("done_at"):
                pattern = rf'(data-action-id="{re.escape(aid)}".*?</strong>)'
                time_tag = f'<span class="done-time">✓ {action["done_at"]}</span>'
                html = re.sub(pattern, rf'\1{time_tag}', html)
        else:
            # Ensure not marked done (idempotent)
            pattern = rf'class="action-item done"(\s+data-action-id="{re.escape(aid)}")'
            replacement = rf'class="action-item"\1'
            html = re.sub(pattern, replacement, html)

            pattern = rf'(data-action-id="{re.escape(aid)}"><span class="a-check")>✅</span>'
            replacement = rf'\1>☐</span>'
            html = re.sub(pattern, replacement, html)

    # Update badge count
    html = re.sub(
        r'(id="actions".*?<span class="badge">)(?:\d+/\d+ 完了|\d+ items)(</span>)',
        rf'\g<1>{done_count}/{total} 完了\2' if done_count > 0 else rf'\g<1>{total} items\2',
        html
    )

    return html


def update_timestamp(html):
    """フッターのタイムスタンプ・ヘッダー日付・時刻を現在時刻に更新"""
    now = datetime.now()
    new_ts = now.strftime("%Y/%m/%d %H:%M") + " PYT"
    html = re.sub(
        r'(<span>)\d{4}/\d{2}/\d{2} \d{2}:\d{2} PYT(</span>)',
        rf'\g<1>{new_ts}\2',
        html
    )
    # Update header date (e.g. 03.16 → 03.17)
    new_header_date = now.strftime("%m.%d")
    html = re.sub(
        r'(<div class="header-date">)\d{2}\.\d{2}(</div>)',
        rf'\g<1>{new_header_date}\2',
        html
    )
    # Update header subtitle date (2026 — 09:00 PYT)
    new_subtitle = now.strftime("%Y — %H:%M") + " PYT"
    html = re.sub(
        r'\d{4} — \d{2}:\d{2} PYT',
        new_subtitle,
        html,
        count=1
    )
    # Update title tag
    new_title_date = now.strftime("%Y.%m.%d")
    html = re.sub(
        r'(<title>日次ビジネス総合レポート — )\d{4}\.\d{2}\.\d{2}(</title>)',
        rf'\g<1>{new_title_date}\2',
        html
    )
    # Update header time
    new_header_time = now.strftime("%H:%M:%S") + " PYT"
    html = re.sub(
        r'(<span class="header-time" id="header-time">)\d{2}:\d{2}:\d{2} PYT(</span>)',
        rf'\g<1>{new_header_time}\2',
        html
    )
    return html


def upload_to_gist(html):
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


def update_dashboard():
    """メイン: ダッシュボードHTML更新 → Gistアップロード"""
    if not DASHBOARD_PATH.exists():
        logger.error(f"ダッシュボードHTML未生成: {DASHBOARD_PATH}")
        return False

    html = DASHBOARD_PATH.read_text(encoding="utf-8")
    status = load_action_status()

    # Reset date if it's a new day
    today = datetime.now().strftime("%Y-%m-%d")
    if status.get("date") != today:
        logger.info(f"日付変更検知: {status.get('date')} → {today}")
        # completed_date が設定されている(=過去に完了済み)タスクは除外
        fresh_actions = [
            a for a in status["actions"]
            if not a.get("completed_date")
        ]
        removed = len(status["actions"]) - len(fresh_actions)
        if removed > 0:
            logger.info(f"完了済みタスク {removed}件 を除外")
        for action in fresh_actions:
            action["done"] = False
            action["done_at"] = None
        status["actions"] = fresh_actions
        status["date"] = today
        save_action_status(status)

    # 鮮度チェック: 2日以上前に生成されたタスクリストには警告
    status_date = status.get("date", today)
    try:
        days_old = (datetime.strptime(today, "%Y-%m-%d") - datetime.strptime(status_date, "%Y-%m-%d")).days
        if days_old >= 2:
            logger.warning(f"優先タスクが{days_old}日間更新されていません。daily_business_report.py の実行を確認してください。")
    except ValueError:
        pass

    # Apply action status
    html = apply_action_status_to_html(html, status["actions"])

    # ステータス自動同期（記事数・GA4・拡張数等）
    try:
        from dashboard_status_sync import apply_updates
        html = apply_updates(html)
        logger.info("ステータス同期完了")
    except Exception as e:
        logger.warning(f"ステータス同期スキップ: {e}")

    # Update timestamp
    html = update_timestamp(html)

    # Save locally
    DASHBOARD_PATH.write_text(html, encoding="utf-8")
    logger.info("ローカルHTML更新完了")

    # Upload to Gist
    return upload_to_gist(html)


def main():
    args = sys.argv[1:]

    if not args:
        # Default: update dashboard
        success = update_dashboard()
        sys.exit(0 if success else 1)

    cmd = args[0]

    if cmd == "done" and len(args) >= 2:
        if mark_action(args[1], done=True):
            update_dashboard()
    elif cmd == "undo" and len(args) >= 2:
        if mark_action(args[1], done=False):
            update_dashboard()
    elif cmd == "list":
        list_actions()
    else:
        print(__doc__)
        sys.exit(1)


if __name__ == "__main__":
    main()
