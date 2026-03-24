#!/usr/bin/env python3
"""
はてなブログ統合パイプライン

WordPress記事の変換→はてなブログ投稿を一括実行する。
Task Schedulerから週次で自動実行される想定。

使い方:
  python hatena_pipeline.py                     # 未処理の全記事を変換+投稿
  python hatena_pipeline.py --limit 3           # 3記事だけ処理
  python hatena_pipeline.py --convert-only      # 変換のみ（投稿しない）
  python hatena_pipeline.py --publish-only      # 投稿のみ（変換済みを投稿）
  python hatena_pipeline.py --draft             # 下書きとして投稿
  python hatena_pipeline.py --dry-run           # 何もせずプレビュー
"""

import argparse
import logging
import subprocess
import sys
from datetime import datetime
from pathlib import Path

# Log settings
LOG_DIR = Path(__file__).parent.parent.parent.parent.parent / "logs"
LOG_FILE = LOG_DIR / "hatena-pipeline.log"

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler(LOG_FILE, encoding="utf-8")
    ]
)
logger = logging.getLogger(__name__)

SCRIPTS_DIR = Path(__file__).parent


def run_script(script_name, extra_args=None):
    """Run a Python script and return success status."""
    cmd = [sys.executable, str(SCRIPTS_DIR / script_name)]
    if extra_args:
        cmd.extend(extra_args)

    logger.info(f"実行: {' '.join(cmd)}")

    result = subprocess.run(
        cmd,
        capture_output=True,
        text=True,
        encoding="cp932",
        errors="replace"
    )

    if result.stdout:
        for line in result.stdout.strip().split("\n"):
            logger.info(f"  {line}")
    if result.stderr:
        for line in result.stderr.strip().split("\n"):
            if "ERROR" in line or "error" in line:
                logger.error(f"  {line}")
            else:
                logger.info(f"  {line}")

    return result.returncode == 0


def main():
    parser = argparse.ArgumentParser(description="はてなブログ統合パイプライン")
    parser.add_argument("--limit", type=int, default=3, help="処理する記事数の上限（デフォルト3）")
    parser.add_argument("--convert-only", action="store_true", help="変換のみ実行")
    parser.add_argument("--publish-only", action="store_true", help="投稿のみ実行")
    parser.add_argument("--draft", action="store_true", help="下書きとして投稿")
    parser.add_argument("--dry-run", action="store_true", help="何もせずプレビュー")
    args = parser.parse_args()

    logger.info("=" * 60)
    logger.info(f"はてなブログパイプライン開始: {datetime.now().isoformat()}")
    logger.info(f"設定: limit={args.limit}, draft={args.draft}, dry_run={args.dry_run}")
    logger.info("=" * 60)

    # Ensure log directory exists
    LOG_DIR.mkdir(parents=True, exist_ok=True)

    # Step 1: Convert
    if not args.publish_only:
        logger.info("[Step 1/2] WordPress記事 → はてなダイジェスト変換")
        converter_args = []
        if args.limit > 0:
            converter_args.extend(["--limit", str(args.limit)])
        if args.dry_run:
            converter_args.append("--dry-run")

        success = run_script("hatena_converter.py", converter_args)
        if not success:
            logger.error("変換処理でエラーが発生しました")
            if not args.dry_run:
                sys.exit(1)
    else:
        logger.info("[Step 1/2] スキップ（--publish-only）")

    # Step 2: Publish
    if not args.convert_only:
        logger.info("[Step 2/2] はてなブログへ投稿")
        publisher_args = []
        if args.limit > 0:
            publisher_args.extend(["--limit", str(args.limit)])
        if args.draft:
            publisher_args.append("--draft")
        if args.dry_run:
            publisher_args.append("--dry-run")

        success = run_script("hatena_publisher.py", publisher_args)
        if not success:
            logger.error("投稿処理でエラーが発生しました")
            if not args.dry_run:
                sys.exit(1)
    else:
        logger.info("[Step 2/2] スキップ（--convert-only）")

    logger.info("=" * 60)
    logger.info("パイプライン完了")
    logger.info("=" * 60)


if __name__ == "__main__":
    main()
