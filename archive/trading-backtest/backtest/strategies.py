"""
バックテスト戦略定義（3種類）
backtesting.py フレームワーク用
"""
import numpy as np
from backtesting import Strategy
from backtesting.lib import crossover


# ===== ヘルパー関数 =====

def SMA(values, n):
    """単純移動平均"""
    return pd.Series(values).rolling(n).mean().values


def EMA(values, n):
    """指数移動平均"""
    return pd.Series(values).ewm(span=n, adjust=False).mean().values


def RSI(values, n=14):
    """RSI（Relative Strength Index）"""
    deltas = np.diff(values, prepend=values[0])
    gain = np.where(deltas > 0, deltas, 0)
    loss = np.where(deltas < 0, -deltas, 0)

    avg_gain = pd.Series(gain).rolling(n).mean().values
    avg_loss = pd.Series(loss).rolling(n).mean().values

    rs = np.where(avg_loss != 0, avg_gain / avg_loss, 100)
    rsi = 100 - (100 / (1 + rs))
    return rsi


def BollingerBands(values, n=20, k=2):
    """ボリンジャーバンド"""
    s = pd.Series(values)
    mid = s.rolling(n).mean().values
    std = s.rolling(n).std().values
    upper = mid + k * std
    lower = mid - k * std
    return upper, mid, lower


import pandas as pd


# ===== 戦略1: RSI平均回帰 =====

class RSIMeanReversion(Strategy):
    """
    RSI平均回帰戦略
    - RSI < oversold → 買い
    - RSI > overbought → 売り（ポジション決済）
    - 損切り・利確をATRベースで設定

    勝率重視: レンジ相場で特に有効
    """
    rsi_period = 14
    oversold = 30
    overbought = 70
    sl_atr_mult = 1.5   # 損切り = ATR × 倍率
    tp_atr_mult = 2.0   # 利確 = ATR × 倍率
    atr_period = 14

    def init(self):
        self.rsi = self.I(RSI, self.data.Close, self.rsi_period)
        # ATR計算
        self.atr = self.I(
            lambda: pd.Series(
                np.maximum(
                    self.data.High - self.data.Low,
                    np.maximum(
                        abs(self.data.High - np.roll(self.data.Close, 1)),
                        abs(self.data.Low - np.roll(self.data.Close, 1))
                    )
                )
            ).rolling(self.atr_period).mean().values
        )

    def next(self):
        price = self.data.Close[-1]
        atr = self.atr[-1]

        if np.isnan(atr) or atr <= 0:
            return

        if not self.position:
            # RSIが売られすぎ → 買いエントリー
            if self.rsi[-1] < self.oversold:
                sl = price - atr * self.sl_atr_mult
                tp = price + atr * self.tp_atr_mult
                self.buy(sl=sl, tp=tp)
        else:
            # RSIが買われすぎ → 決済
            if self.rsi[-1] > self.overbought:
                self.position.close()


# ===== 戦略2: ボリンジャーバンド平均回帰 =====

class BollingerMeanReversion(Strategy):
    """
    ボリンジャーバンド平均回帰戦略
    - 価格がLower Bandを下回り → 買い
    - 価格がUpper Bandを上回り → 売り決済
    - MidライBandを利確ターゲットにすることで勝率向上

    勝率最重視の保守的戦略
    """
    bb_period = 20
    bb_std = 2.0
    sl_atr_mult = 1.5
    atr_period = 14

    def init(self):
        self.bb_upper, self.bb_mid, self.bb_lower = self.I(
            lambda: BollingerBands(self.data.Close, self.bb_period, self.bb_std),
            overlay=True
        )
        self.atr = self.I(
            lambda: pd.Series(
                np.maximum(
                    self.data.High - self.data.Low,
                    np.maximum(
                        abs(self.data.High - np.roll(self.data.Close, 1)),
                        abs(self.data.Low - np.roll(self.data.Close, 1))
                    )
                )
            ).rolling(self.atr_period).mean().values
        )

    def next(self):
        price = self.data.Close[-1]
        atr = self.atr[-1]

        if np.isnan(atr) or atr <= 0 or np.isnan(self.bb_lower[-1]):
            return

        if not self.position:
            # Lower Band下回り → 買い
            if price < self.bb_lower[-1]:
                sl = price - atr * self.sl_atr_mult
                tp = self.bb_mid[-1]  # Mid Bandで利確（保守的）
                if tp > price:
                    self.buy(sl=sl, tp=tp)
        else:
            # Upper Band到達 → 決済
            if price > self.bb_upper[-1]:
                self.position.close()


# ===== 戦略3: MAクロス + RSIフィルター =====

class MACrossRSI(Strategy):
    """
    移動平均クロス + RSIフィルター
    - 短期MAが長期MAを上抜け（ゴールデンクロス）→ 買い
    - ただしRSIが買われすぎでないことを確認
    - 短期MAが長期MAを下抜け → 売り決済

    トレンドフォロー型: 勝率はやや低いが利益幅が大きい
    """
    fast_ma = 10
    slow_ma = 30
    rsi_period = 14
    rsi_filter = 65   # RSIがこの値以下の時のみエントリー
    sl_atr_mult = 2.0
    tp_atr_mult = 3.0
    atr_period = 14

    def init(self):
        self.fast = self.I(SMA, self.data.Close, self.fast_ma)
        self.slow = self.I(SMA, self.data.Close, self.slow_ma)
        self.rsi = self.I(RSI, self.data.Close, self.rsi_period)
        self.atr = self.I(
            lambda: pd.Series(
                np.maximum(
                    self.data.High - self.data.Low,
                    np.maximum(
                        abs(self.data.High - np.roll(self.data.Close, 1)),
                        abs(self.data.Low - np.roll(self.data.Close, 1))
                    )
                )
            ).rolling(self.atr_period).mean().values
        )

    def next(self):
        price = self.data.Close[-1]
        atr = self.atr[-1]

        if np.isnan(atr) or atr <= 0:
            return

        if not self.position:
            # ゴールデンクロス + RSIフィルター
            if (crossover(self.fast, self.slow) and
                    self.rsi[-1] < self.rsi_filter):
                sl = price - atr * self.sl_atr_mult
                tp = price + atr * self.tp_atr_mult
                self.buy(sl=sl, tp=tp)
        else:
            # デッドクロス → 決済
            if crossover(self.slow, self.fast):
                self.position.close()
