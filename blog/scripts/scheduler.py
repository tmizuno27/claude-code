#!/usr/bin/env python3
"""
Windowsタスクスケジューラ登録スクリプト

全自動化スクリプトをWindowsタスクスケジューラに登録する。
"""

import argparse
import logging
import subprocess
import sys
from pathlib import Path

# ログ設定
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# プロジェクトルート
PROJECT_ROOT = Path(__file__).parent.parent
SCRIPTS_DIR = PROJECT_ROOT / "scripts"

# タスク名のプレフィックス
TASK_PREFIX = "JidouBiz"

# スケジュール定義
TASKS = [
    {
        "name": f"{TASK_PREFIX}_AnalyticsReport",
        "script": "analytics_reporter.py",
        "schedule": "WEEKLY",
        "day": "MON",
        "time": "08:00",
        "description": "週次分析レポート生成"
    },
    {
        "name": f"{TASK_PREFIX}_KeywordResearch",
        "script": "keyword_research.py",
        "schedule": "WEEKLY",
        "day": "MON",
        "time": "09:00",
        "description": "キーワード調査"
    },
    {
        "name": f"{TASK_PREFIX}_Article_Tue",
        "script": "article_generator.py",
        "schedule": "WEEKLY",
        "day": "TUE",
        "time": "09:00",
        "description": "記事生成（火曜）"
    },
    {
        "name": f"{TASK_PREFIX}_Article_Thu",
        "script": "article_generator.py",
        "schedule": "WEEKLY",
        "day": "THU",
        "time": "09:00",
        "description": "記事生成（木曜）"
    },
    {
        "name": f"{TASK_PREFIX}_Article_Sat",
        "script": "article_generator.py",
        "schedule": "WEEKLY",
        "day": "SAT",
        "time": "09:00",
        "description": "記事生成（土曜）"
    },
    {
        "name": f"{TASK_PREFIX}_InternalLinker",
        "script": "internal_linker.py",
        "schedule": "WEEKLY",
        "day": "FRI",
        "time": "09:00",
        "description": "内部リンク最適化"
    },
    {
        "name": f"{TASK_PREFIX}_ContentCalendar",
        "script": "content_calendar.py",
        "schedule": "WEEKLY",
        "day": "SUN",
        "time": "09:00",
        "description": "コンテンツカレンダー更新"
    },
]


def get_python_path():
    """Pythonの実行パスを取得する"""
    return sys.executable


def register_task(task):
    """Windowsタスクスケジューラにタスクを登録する"""
    python_path = get_python_path()
    script_path = SCRIPTS_DIR / task["script"]

    if not script_path.exists():
        logger.warning(f"スクリプトが見つかりません: {script_path}")
        return False

    # schtasks コマンド構築
    cmd = [
        "schtasks", "/create",
        "/tn", task["name"],
        "/tr", f'"{python_path}" "{script_path}"',
        "/sc", task["schedule"],
        "/d", task["day"],
        "/st", task["time"],
        "/f"  # 既存タスクを上書き
    ]

    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            shell=True
        )

        if result.returncode == 0:
            logger.info(f"  登録成功: {task['name']} ({task['description']})")
            logger.info(f"    スケジュール: 毎週{task['day']} {task['time']}")
            return True
        else:
            logger.error(f"  登録失敗: {task['name']}")
            logger.error(f"    エラー: {result.stderr.strip()}")
            return False

    except Exception as e:
        logger.error(f"  実行エラー: {e}")
        return False


def list_tasks():
    """登録済みのJidouBizタスクを一覧表示する"""
    try:
        result = subprocess.run(
            ["schtasks", "/query", "/fo", "TABLE"],
            capture_output=True,
            text=True,
            shell=True
        )

        print(f"\n=== {TASK_PREFIX} 登録済みタスク ===\n")
        found = False
        for line in result.stdout.split('\n'):
            if TASK_PREFIX in line:
                print(line.strip())
                found = True

        if not found:
            print("登録済みタスクはありません。")

    except Exception as e:
        logger.error(f"タスク一覧取得エラー: {e}")


def remove_tasks():
    """登録済みのJidouBizタスクを全削除する"""
    logger.info(f"=== {TASK_PREFIX} タスク削除 ===")

    for task in TASKS:
        try:
            result = subprocess.run(
                ["schtasks", "/delete", "/tn", task["name"], "/f"],
                capture_output=True,
                text=True,
                shell=True
            )

            if result.returncode == 0:
                logger.info(f"  削除成功: {task['name']}")
            else:
                logger.warning(f"  削除スキップ: {task['name']}（未登録の可能性）")

        except Exception as e:
            logger.error(f"  削除エラー: {e}")


def main():
    """メイン処理"""
    parser = argparse.ArgumentParser(description="自動化スクリプトのスケジュール管理")
    parser.add_argument("--list", action="store_true", help="登録済みタスクを一覧表示")
    parser.add_argument("--remove", action="store_true", help="全タスクを削除")
    parser.add_argument("--register", action="store_true", help="全タスクを登録（デフォルト）")
    args = parser.parse_args()

    if args.list:
        list_tasks()
        return

    if args.remove:
        remove_tasks()
        return

    # デフォルト: タスク登録
    logger.info("=== タスクスケジューラ登録開始 ===")
    logger.info(f"Python: {get_python_path()}")
    logger.info(f"スクリプト: {SCRIPTS_DIR}\n")

    success_count = 0
    for task in TASKS:
        if register_task(task):
            success_count += 1

    logger.info(f"\n=== 登録結果: {success_count}/{len(TASKS)} タスク ===")

    if success_count < len(TASKS):
        logger.warning("一部タスクの登録に失敗しました。管理者権限で再実行してください。")

    # 登録済みタスクを表示
    print()
    list_tasks()


if __name__ == "__main__":
    main()
