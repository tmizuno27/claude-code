"""ログ・ユーティリティ"""

import json
import logging
from datetime import datetime, timezone, timedelta
from pathlib import Path

PYT = timezone(timedelta(hours=-3))


def setup_logger(log_dir: Path) -> logging.Logger:
    """ロガー設定"""
    log_dir.mkdir(parents=True, exist_ok=True)
    logger = logging.getLogger("trading-bot")
    logger.setLevel(logging.INFO)

    if not logger.handlers:
        fh = logging.FileHandler(log_dir / "bot.log", encoding="utf-8")
        fh.setFormatter(logging.Formatter("%(asctime)s [%(levelname)s] %(message)s"))
        ch = logging.StreamHandler()
        ch.setFormatter(logging.Formatter("%(asctime)s [%(levelname)s] %(message)s"))
        logger.addHandler(fh)
        logger.addHandler(ch)

    return logger


def log_trade(log_file: Path, trade: dict):
    """取引をJSONログに追記"""
    trade["timestamp"] = datetime.now(PYT).isoformat()
    trades = []
    if log_file.exists():
        try:
            trades = json.loads(log_file.read_text("utf-8"))
        except (json.JSONDecodeError, FileNotFoundError):
            trades = []
    trades.append(trade)
    log_file.write_text(json.dumps(trades, indent=2, ensure_ascii=False), encoding="utf-8")
