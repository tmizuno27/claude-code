"""売買戦略: SMAクロスオーバー"""

import pandas as pd


class SMAStrategy:
    """短期SMAが長期SMAを上抜け→買い、下抜け→売り"""

    def __init__(self, short_period: int = 10, long_period: int = 50):
        self.short_period = short_period
        self.long_period = long_period

    def analyze(self, ohlcv: list) -> str:
        """
        OHLCVデータを分析してシグナルを返す。
        Returns: "buy", "sell", or "hold"
        """
        df = pd.DataFrame(ohlcv, columns=["timestamp", "open", "high", "low", "close", "volume"])
        df["sma_short"] = df["close"].rolling(window=self.short_period).mean()
        df["sma_long"] = df["close"].rolling(window=self.long_period).mean()

        # データ不足
        if df["sma_long"].isna().iloc[-1]:
            return "hold"

        current_short = df["sma_short"].iloc[-1]
        current_long = df["sma_long"].iloc[-1]
        prev_short = df["sma_short"].iloc[-2]
        prev_long = df["sma_long"].iloc[-2]

        # ゴールデンクロス（短期が長期を上抜け）→ 買い
        if prev_short <= prev_long and current_short > current_long:
            return "buy"

        # デッドクロス（短期が長期を下抜け）→ 売り
        if prev_short >= prev_long and current_short < current_long:
            return "sell"

        return "hold"

    def get_info(self, ohlcv: list) -> dict:
        """現在のSMA値とシグナルを返す（ダッシュボード用）"""
        df = pd.DataFrame(ohlcv, columns=["timestamp", "open", "high", "low", "close", "volume"])
        df["sma_short"] = df["close"].rolling(window=self.short_period).mean()
        df["sma_long"] = df["close"].rolling(window=self.long_period).mean()

        return {
            "price": float(df["close"].iloc[-1]),
            "sma_short": round(float(df["sma_short"].iloc[-1]), 2) if not pd.isna(df["sma_short"].iloc[-1]) else None,
            "sma_long": round(float(df["sma_long"].iloc[-1]), 2) if not pd.isna(df["sma_long"].iloc[-1]) else None,
            "signal": self.analyze(ohlcv),
        }
