"""
Bybit ライブ取引エンジン（ccxt経由）
ペーパートレード（テストネット）→ ライブの段階的移行対応
"""
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "backtest"))

import json
import time
import logging
from datetime import datetime, timedelta

import ccxt
import numpy as np
import pandas as pd

from strategies import RSI, BollingerBands, SMA

# ===== ログ設定 =====
LOG_DIR = os.path.join(os.path.dirname(__file__), "..", "..", "..", "logs")
os.makedirs(LOG_DIR, exist_ok=True)
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler(os.path.join(LOG_DIR, "trading.log"), encoding="utf-8"),
        logging.StreamHandler(),
    ]
)
logger = logging.getLogger(__name__)


class LiveTrader:
    def __init__(self, config_path=None):
        if config_path is None:
            config_path = os.path.join(os.path.dirname(__file__), "config.json")

        with open(config_path, "r") as f:
            self.config = json.load(f)

        self.mode = self.config["mode"]  # "paper" or "live"
        self.pair = self.config["trading"]["pair"]
        self.timeframe = self.config["trading"]["timeframe"]
        self.strategy_name = self.config["trading"]["strategy"]
        self.strategy_params = self.config["trading"].get("params", {})

        # リスク管理パラメータ
        self.max_daily_loss_pct = self.config["risk"]["max_daily_loss_pct"]
        self.max_drawdown_pct = self.config["risk"]["max_drawdown_pct"]
        self.max_trades_per_day = self.config["risk"]["max_trades_per_day"]
        self.cool_down_minutes = self.config["risk"]["cool_down_minutes"]

        # 取引状態
        self.daily_trades = 0
        self.daily_pnl = 0.0
        self.last_trade_time = None
        self.peak_balance = 0
        self.trade_log = []

        # 取引所接続
        self._init_exchange()
        logger.info(f"取引エンジン起動: mode={self.mode}, pair={self.pair}, strategy={self.strategy_name}")

    def _init_exchange(self):
        """取引所APIに接続"""
        exchange_config = {
            "apiKey": self.config["api_key"],
            "secret": self.config["api_secret"],
            "enableRateLimit": True,
        }

        if self.config.get("testnet", True):
            exchange_config["sandbox"] = True
            logger.info("テストネット（サンドボックス）モードで接続")

        self.exchange = ccxt.bybit(exchange_config)

    def fetch_recent_candles(self, limit=100):
        """直近のローソク足データを取得"""
        ohlcv = self.exchange.fetch_ohlcv(self.pair, self.timeframe, limit=limit)
        df = pd.DataFrame(ohlcv, columns=["timestamp", "open", "high", "low", "close", "volume"])
        df["timestamp"] = pd.to_datetime(df["timestamp"], unit="ms")
        return df

    def calculate_signal(self, df):
        """
        戦略に基づいて売買シグナルを算出

        Returns:
            "buy", "sell", or None
        """
        close = df["close"].values

        p = self.strategy_params

        if self.strategy_name == "RSIMeanReversion":
            period = p.get("rsi_period", 14)
            oversold = p.get("oversold", 30)
            overbought = p.get("overbought", 70)
            rsi = RSI(close, period)
            if rsi[-1] < oversold:
                return "buy"
            elif rsi[-1] > overbought:
                return "sell"

        elif self.strategy_name == "BollingerMeanReversion":
            bb_period = p.get("bb_period", 20)
            bb_std = p.get("bb_std", 2.0)
            upper, mid, lower = BollingerBands(close, bb_period, bb_std)
            price = close[-1]
            if price < lower[-1]:
                return "buy"
            elif price > upper[-1]:
                return "sell"

        elif self.strategy_name == "MACrossRSI":
            fast_n = p.get("fast_ma", 7)
            slow_n = p.get("slow_ma", 30)
            rsi_filter = p.get("rsi_filter", 60)
            fast = SMA(close, fast_n)
            slow = SMA(close, slow_n)
            rsi = RSI(close, 14)
            if fast[-1] > slow[-1] and fast[-2] <= slow[-2] and rsi[-1] < rsi_filter:
                return "buy"
            elif fast[-1] < slow[-1] and fast[-2] >= slow[-2]:
                return "sell"

        return None

    def check_risk_limits(self):
        """リスク制限チェック"""
        # 日次取引回数チェック
        if self.daily_trades >= self.max_trades_per_day:
            logger.warning(f"日次取引上限到達: {self.daily_trades}/{self.max_trades_per_day}")
            return False

        # クールダウンチェック
        if self.last_trade_time:
            elapsed = (datetime.now() - self.last_trade_time).total_seconds() / 60
            if elapsed < self.cool_down_minutes:
                return False

        # 日次損失チェック
        if self.daily_pnl < -self.max_daily_loss_pct:
            logger.warning(f"日次損失上限到達: {self.daily_pnl:.2f}%")
            return False

        # 最大DD チェック
        try:
            balance = self.get_balance()
            if self.peak_balance > 0:
                dd = (self.peak_balance - balance) / self.peak_balance * 100
                if dd > self.max_drawdown_pct:
                    logger.warning(f"最大DD到達: {dd:.2f}% > {self.max_drawdown_pct}%")
                    return False
        except Exception:
            pass

        return True

    def get_balance(self):
        """USDT残高取得"""
        balance = self.exchange.fetch_balance()
        return float(balance.get("USDT", {}).get("free", 0))

    def get_position(self):
        """現在のポジション取得"""
        try:
            positions = self.exchange.fetch_positions([self.pair])
            for pos in positions:
                if float(pos.get("contracts", 0)) > 0:
                    return pos
        except Exception:
            pass
        return None

    def execute_trade(self, signal):
        """取引実行"""
        if not self.check_risk_limits():
            return None

        balance = self.get_balance()
        position = self.get_position()
        max_pct = self.config["trading"]["max_position_pct"]

        if signal == "buy" and not position:
            # 買いエントリー
            ticker = self.exchange.fetch_ticker(self.pair)
            price = ticker["last"]
            amount_usdt = balance * max_pct
            amount = amount_usdt / price

            logger.info(f"買いエントリー: {self.pair} @ {price:.2f}, 数量={amount:.6f}")

            if self.mode == "live":
                order = self.exchange.create_market_buy_order(self.pair, amount)
                logger.info(f"注文約定: {order['id']}")
            else:
                order = {"id": "paper", "price": price, "amount": amount}
                logger.info(f"[ペーパー] 買い約定: {price:.2f}")

            self.daily_trades += 1
            self.last_trade_time = datetime.now()
            self.trade_log.append({
                "time": datetime.now().isoformat(),
                "signal": signal,
                "price": price,
                "amount": amount,
                "mode": self.mode,
            })
            return order

        elif signal == "sell" and position:
            # 決済
            contracts = float(position["contracts"])
            logger.info(f"決済: {self.pair}, 数量={contracts}")

            if self.mode == "live":
                order = self.exchange.create_market_sell_order(self.pair, contracts)
                logger.info(f"決済約定: {order['id']}")
            else:
                ticker = self.exchange.fetch_ticker(self.pair)
                order = {"id": "paper", "price": ticker["last"]}
                logger.info(f"[ペーパー] 決済: {ticker['last']:.2f}")

            self.daily_trades += 1
            self.last_trade_time = datetime.now()
            return order

        return None

    def run_once(self):
        """1サイクル実行（スケジューラから呼び出し用）"""
        try:
            df = self.fetch_recent_candles()
            signal = self.calculate_signal(df)

            if signal:
                logger.info(f"シグナル検出: {signal}")
                self.execute_trade(signal)
            else:
                logger.debug("シグナルなし")

        except Exception as e:
            logger.error(f"実行エラー: {e}", exc_info=True)

    def run_loop(self, interval_seconds=None):
        """
        連続実行ループ

        Args:
            interval_seconds: チェック間隔（秒）。Noneの場合、timeframeに応じて自動設定
        """
        if interval_seconds is None:
            tf_map = {"1m": 60, "5m": 300, "15m": 900, "1h": 3600, "4h": 14400}
            interval_seconds = tf_map.get(self.timeframe, 3600)

        logger.info(f"取引ループ開始: 間隔={interval_seconds}秒")
        logger.info(f"停止するには Ctrl+C")

        while True:
            self.run_once()

            # 日次リセット（UTC 0:00）
            now = datetime.utcnow()
            if now.hour == 0 and now.minute < (interval_seconds / 60):
                self.daily_trades = 0
                self.daily_pnl = 0.0
                logger.info("日次カウンターリセット")

            # 残高更新
            try:
                balance = self.get_balance()
                self.peak_balance = max(self.peak_balance, balance)
            except Exception:
                pass

            time.sleep(interval_seconds)


def main():
    import argparse
    parser = argparse.ArgumentParser(description="Bybit自動売買エンジン")
    parser.add_argument("--mode", choices=["paper", "live"], default="paper",
                        help="取引モード（default: paper）")
    parser.add_argument("--config", default=None, help="設定ファイルパス")
    parser.add_argument("--once", action="store_true", help="1回だけ実行")
    args = parser.parse_args()

    # 設定ファイル読み込み
    config_path = args.config or os.path.join(os.path.dirname(__file__), "config.json")

    if not os.path.exists(config_path):
        print(f"設定ファイルが見つかりません: {config_path}")
        print(f"config_template.json をコピーして config.json を作成し、APIキーを設定してください。")
        sys.exit(1)

    # モード上書き
    with open(config_path, "r") as f:
        config = json.load(f)
    config["mode"] = args.mode
    with open(config_path, "w") as f:
        json.dump(config, f, indent=2)

    trader = LiveTrader(config_path)

    if args.once:
        trader.run_once()
    else:
        trader.run_loop()


if __name__ == "__main__":
    main()
