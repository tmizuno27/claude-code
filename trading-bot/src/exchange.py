"""Binance API ラッパー（ccxt使用）"""

import ccxt
import json
from pathlib import Path


class Exchange:
    """取引所への接続・注文管理"""

    def __init__(self, config_dir: Path):
        settings = json.loads((config_dir / "settings.json").read_text("utf-8"))
        secrets = json.loads((config_dir / "secrets.json").read_text("utf-8"))

        is_testnet = settings["mode"] == "testnet"

        self.exchange = ccxt.binance({
            "apiKey": secrets["api_key"],
            "secret": secrets["api_secret"],
            "enableRateLimit": True,
        })

        if is_testnet:
            self.exchange.set_sandbox_mode(True)

        self.symbol = settings["symbol"]
        self.timeframe = settings["timeframe"]

    def fetch_ohlcv(self, limit: int = 100):
        """ローソク足データ取得（OHLCV）"""
        return self.exchange.fetch_ohlcv(self.symbol, self.timeframe, limit=limit)

    def fetch_balance(self):
        """残高取得"""
        return self.exchange.fetch_balance()

    def get_usdt_balance(self) -> float:
        """USDT残高を取得"""
        balance = self.fetch_balance()
        return float(balance.get("free", {}).get("USDT", 0))

    def get_position(self) -> float:
        """現在のBTC保有量を取得"""
        balance = self.fetch_balance()
        base = self.symbol.split("/")[0]
        return float(balance.get("free", {}).get(base, 0))

    def fetch_ticker(self):
        """現在価格取得"""
        return self.exchange.fetch_ticker(self.symbol)

    def buy(self, amount: float):
        """成行買い注文"""
        return self.exchange.create_market_buy_order(self.symbol, amount)

    def sell(self, amount: float):
        """成行売り注文"""
        return self.exchange.create_market_sell_order(self.symbol, amount)
