"""
自動売買バックテストエンジン
3つの戦略を比較して最適なものを選定する

戦略:
1. ボリンジャーバンド平均回帰 (Bollinger Band Mean Reversion)
2. RSI逆張り (RSI Mean Reversion)
3. 移動平均クロス + RSIフィルター (MA Cross + RSI Filter)
"""

import json
import sys
from datetime import datetime
from pathlib import Path

import numpy as np
import pandas as pd
import yfinance as yf
from backtesting import Backtest, Strategy
from backtesting.lib import crossover


# ============================================================
# データ取得
# ============================================================

def fetch_data(symbol: str = "USDJPY=X", period: str = "2y", interval: str = "1d") -> pd.DataFrame:
    """yfinanceでFXデータを取得"""
    print(f"データ取得中: {symbol} ({period}, {interval})...")
    df = yf.download(symbol, period=period, interval=interval, progress=False)
    # backtesting.pyが要求するカラム名に変換
    if isinstance(df.columns, pd.MultiIndex):
        df.columns = df.columns.get_level_values(0)
    df = df.rename(columns={
        "Open": "Open", "High": "High", "Low": "Low",
        "Close": "Close", "Volume": "Volume"
    })
    df = df[["Open", "High", "Low", "Close", "Volume"]].dropna()
    print(f"  取得完了: {len(df)}行 ({df.index[0].strftime('%Y-%m-%d')} ~ {df.index[-1].strftime('%Y-%m-%d')})")
    return df


# ============================================================
# インジケーター関数
# ============================================================

def SMA(values, n):
    return pd.Series(values).rolling(n).mean()

def EMA(values, n):
    return pd.Series(values).ewm(span=n, adjust=False).mean()

def BBANDS(values, n=20, n_std=2.0):
    sma = SMA(values, n)
    std = pd.Series(values).rolling(n).std()
    upper = sma + n_std * std
    lower = sma - n_std * std
    return upper, sma, lower

def RSI(values, n=14):
    deltas = pd.Series(values).diff()
    gain = deltas.clip(lower=0)
    loss = -deltas.clip(upper=0)
    avg_gain = gain.rolling(n).mean()
    avg_loss = loss.rolling(n).mean()
    rs = avg_gain / avg_loss
    return 100 - (100 / (1 + rs))

def ATR(high, low, close, n=14):
    h_l = pd.Series(high) - pd.Series(low)
    h_c = (pd.Series(high) - pd.Series(close).shift()).abs()
    l_c = (pd.Series(low) - pd.Series(close).shift()).abs()
    tr = pd.concat([h_l, h_c, l_c], axis=1).max(axis=1)
    return tr.rolling(n).mean()


# ============================================================
# 戦略1: ボリンジャーバンド平均回帰
# ============================================================

class BollingerMeanReversion(Strategy):
    """
    ボリンジャーバンド平均回帰戦略
    - 価格が下限バンドを下回ったら買い
    - 価格が上限バンドを上回ったら売り（利確）
    - 中央バンド到達でも利確
    - ATRベースのストップロス
    """
    bb_period = 20
    bb_std = 2.0
    atr_period = 14
    atr_sl_multiplier = 1.5
    risk_per_trade = 0.02  # 1トレードあたりリスク2%

    def init(self):
        close = self.data.Close
        self.bb_upper, self.bb_mid, self.bb_lower = self.I(
            BBANDS, close, self.bb_period, self.bb_std,
            overlay=True
        )
        self.rsi = self.I(RSI, close, 14)
        self.atr = self.I(ATR, self.data.High, self.data.Low, close, self.atr_period)

    def next(self):
        price = self.data.Close[-1]

        if not self.position:
            # エントリー: 価格が下限バンド以下 & RSI < 35
            if price <= self.bb_lower[-1] and self.rsi[-1] < 35:
                sl = price - self.atr[-1] * self.atr_sl_multiplier
                self.buy(sl=sl, tp=self.bb_mid[-1])
            # ショート: 価格が上限バンド以上 & RSI > 65
            elif price >= self.bb_upper[-1] and self.rsi[-1] > 65:
                sl = price + self.atr[-1] * self.atr_sl_multiplier
                self.sell(sl=sl, tp=self.bb_mid[-1])


# ============================================================
# 戦略2: RSI逆張り
# ============================================================

class RSIMeanReversion(Strategy):
    """
    RSI逆張り戦略
    - RSI < 30 で買い（売られすぎ）
    - RSI > 70 で売り（買われすぎ）
    - RSI 50付近で利確
    """
    rsi_period = 14
    rsi_oversold = 30
    rsi_overbought = 70
    atr_period = 14
    atr_sl_multiplier = 2.0

    def init(self):
        self.rsi = self.I(RSI, self.data.Close, self.rsi_period)
        self.atr = self.I(ATR, self.data.High, self.data.Low, self.data.Close, self.atr_period)
        self.sma = self.I(SMA, self.data.Close, 50)

    def next(self):
        price = self.data.Close[-1]

        if not self.position:
            if self.rsi[-1] < self.rsi_oversold:
                sl = price - self.atr[-1] * self.atr_sl_multiplier
                tp = price + self.atr[-1] * 2.0
                self.buy(sl=sl, tp=tp)
            elif self.rsi[-1] > self.rsi_overbought:
                sl = price + self.atr[-1] * self.atr_sl_multiplier
                tp = price - self.atr[-1] * 2.0
                self.sell(sl=sl, tp=tp)
        else:
            # RSIが中立ゾーンに戻ったら利確
            if self.position.is_long and self.rsi[-1] > 55:
                self.position.close()
            elif self.position.is_short and self.rsi[-1] < 45:
                self.position.close()


# ============================================================
# 戦略3: 移動平均クロス + RSIフィルター
# ============================================================

class MACrossRSI(Strategy):
    """
    移動平均クロス + RSIフィルター
    - 短期EMAが長期EMAを上抜け & RSI < 70 → 買い
    - 短期EMAが長期EMAを下抜け & RSI > 30 → 売り
    """
    fast_period = 10
    slow_period = 30
    rsi_period = 14
    atr_period = 14
    atr_sl_multiplier = 2.0
    atr_tp_multiplier = 3.0

    def init(self):
        self.fast_ema = self.I(EMA, self.data.Close, self.fast_period, overlay=True)
        self.slow_ema = self.I(EMA, self.data.Close, self.slow_period, overlay=True)
        self.rsi = self.I(RSI, self.data.Close, self.rsi_period)
        self.atr = self.I(ATR, self.data.High, self.data.Low, self.data.Close, self.atr_period)

    def next(self):
        price = self.data.Close[-1]

        if not self.position:
            if crossover(self.fast_ema, self.slow_ema) and self.rsi[-1] < 70:
                sl = price - self.atr[-1] * self.atr_sl_multiplier
                tp = price + self.atr[-1] * self.atr_tp_multiplier
                self.buy(sl=sl, tp=tp)
            elif crossover(self.slow_ema, self.fast_ema) and self.rsi[-1] > 30:
                sl = price + self.atr[-1] * self.atr_sl_multiplier
                tp = price - self.atr[-1] * self.atr_tp_multiplier
                self.sell(sl=sl, tp=tp)


# ============================================================
# バックテスト実行
# ============================================================

def run_backtest(data: pd.DataFrame, strategy_class, cash: float = 100000,
                 commission: float = 0.0002, margin: float = 1/25) -> dict:
    """単一戦略のバックテストを実行"""
    bt = Backtest(
        data, strategy_class,
        cash=cash,
        commission=commission,  # FXスプレッド相当
        margin=margin,          # レバレッジ25倍
        exclusive_orders=True,
        trade_on_close=True,
    )
    stats = bt.run()
    return stats, bt


def compare_strategies(data: pd.DataFrame, cash: float = 100000):
    """3戦略を比較"""
    strategies = [
        ("ボリンジャーバンド平均回帰", BollingerMeanReversion),
        ("RSI逆張り", RSIMeanReversion),
        ("移動平均クロス+RSI", MACrossRSI),
    ]

    results = []
    for name, strategy_class in strategies:
        print(f"\n{'='*50}")
        print(f"戦略: {name}")
        print(f"{'='*50}")

        stats, bt = run_backtest(data, strategy_class, cash=cash)

        result = {
            "戦略名": name,
            "最終資産": float(stats["Equity Final [$]"]),
            "リターン(%)": float(stats["Return [%]"]),
            "勝率(%)": float(stats["Win Rate [%]"]) if not pd.isna(stats["Win Rate [%]"]) else 0,
            "取引回数": int(stats["# Trades"]),
            "最大DD(%)": float(stats["Max. Drawdown [%]"]),
            "シャープレシオ": float(stats["Sharpe Ratio"]) if not pd.isna(stats["Sharpe Ratio"]) else 0,
            "プロフィットファクター": float(stats["Profit Factor"]) if not pd.isna(stats["Profit Factor"]) else 0,
            "平均トレード(%)": float(stats["Avg. Trade [%]"]) if not pd.isna(stats["Avg. Trade [%]"]) else 0,
        }
        results.append(result)

        print(f"  最終資産: ¥{result['最終資産']:,.0f}")
        print(f"  リターン: {result['リターン(%)']:.2f}%")
        print(f"  勝率: {result['勝率(%)']:.1f}%")
        print(f"  取引回数: {result['取引回数']}")
        print(f"  最大ドローダウン: {result['最大DD(%)']:.2f}%")
        print(f"  シャープレシオ: {result['シャープレシオ']:.3f}")
        print(f"  プロフィットファクター: {result['プロフィットファクター']:.3f}")

    return results


def find_best_strategy(results: list) -> dict:
    """総合スコアで最適戦略を選定"""
    for r in results:
        # 総合スコア = 勝率×0.3 + シャープ×0.25 + PF×0.2 + リターン×0.15 - DD×0.1
        score = (
            r["勝率(%)"] * 0.30 +
            r["シャープレシオ"] * 25.0 +  # スケール調整
            r["プロフィットファクター"] * 20.0 +
            r["リターン(%)"] * 0.15 +
            r["最大DD(%)"] * 0.10  # DDは負の値なので加算でペナルティ
        )
        r["総合スコア"] = score

    best = max(results, key=lambda x: x["総合スコア"])
    return best


# ============================================================
# メイン実行
# ============================================================

def main():
    output_dir = Path(__file__).parent / "results"
    output_dir.mkdir(exist_ok=True)

    # 複数通貨ペアでテスト
    symbols = {
        "USD/JPY": "USDJPY=X",
        "EUR/USD": "EURUSD=X",
        "GBP/USD": "GBPUSD=X",
    }

    all_results = {}

    for pair_name, symbol in symbols.items():
        print(f"\n{'#'*60}")
        print(f"# 通貨ペア: {pair_name}")
        print(f"{'#'*60}")

        try:
            data = fetch_data(symbol, period="2y", interval="1d")
            if len(data) < 100:
                print(f"  データ不足 ({len(data)}行), スキップ")
                continue

            results = compare_strategies(data, cash=100000)
            best = find_best_strategy(results)
            all_results[pair_name] = {
                "results": results,
                "best": best["戦略名"],
            }

            print(f"\n★ {pair_name} 最適戦略: {best['戦略名']} (スコア: {best['総合スコア']:.1f})")

        except Exception as e:
            print(f"  エラー: {e}")
            continue

    # 結果をJSON保存
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    result_file = output_dir / f"backtest_{timestamp}.json"

    # numpy/pandasの型をJSON対応に変換
    def convert(obj):
        if isinstance(obj, (np.integer,)):
            return int(obj)
        if isinstance(obj, (np.floating,)):
            return float(obj)
        if isinstance(obj, np.ndarray):
            return obj.tolist()
        raise TypeError(f"Type {type(obj)} not serializable")

    with open(result_file, "w", encoding="utf-8") as f:
        json.dump(all_results, f, ensure_ascii=False, indent=2, default=convert)

    print(f"\n結果保存先: {result_file}")

    # 総合サマリー
    print(f"\n{'='*60}")
    print("【総合サマリー】")
    print(f"{'='*60}")
    for pair, data in all_results.items():
        print(f"  {pair}: 最適 → {data['best']}")
        for r in data["results"]:
            marker = " ★" if r["戦略名"] == data["best"] else ""
            print(f"    {r['戦略名']}: 勝率{r['勝率(%)']:.0f}% / "
                  f"リターン{r['リターン(%)']:+.1f}% / "
                  f"DD{r['最大DD(%)']:.1f}%{marker}")


if __name__ == "__main__":
    main()
