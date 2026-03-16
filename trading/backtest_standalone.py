"""
自動売買バックテストエンジン（スタンドアロン版）
外部ライブラリ: pandas, numpy のみ（yfinanceなし、CSVデータ使用）

3つの戦略を比較して最適なものを選定する:
1. ボリンジャーバンド平均回帰
2. RSI逆張り
3. 移動平均クロス + RSIフィルター
"""

import csv
import json
import math
import os
import urllib.request
import urllib.error
from datetime import datetime, timedelta
from pathlib import Path
from dataclasses import dataclass, field


# ============================================================
# データ取得（urllib のみ、外部ライブラリ不要）
# ============================================================

def fetch_forex_data(symbol: str = "USDJPY=X", period_days: int = 730) -> list[dict]:
    """
    Yahoo Finance から CSV をダウンロード（urllib のみ使用）
    戻り値: [{"date": str, "open": float, "high": float, "low": float, "close": float, "volume": int}, ...]
    """
    end = int(datetime.now().timestamp())
    start = int((datetime.now() - timedelta(days=period_days)).timestamp())

    url = (f"https://query1.finance.yahoo.com/v7/finance/download/{symbol}"
           f"?period1={start}&period2={end}&interval=1d&events=history")

    headers = {"User-Agent": "Mozilla/5.0"}
    req = urllib.request.Request(url, headers=headers)

    print(f"データ取得中: {symbol}...")
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            text = resp.read().decode("utf-8")
    except urllib.error.HTTPError:
        # フォールバック: v8 API
        url2 = (f"https://query2.finance.yahoo.com/v8/finance/chart/{symbol}"
                f"?period1={start}&period2={end}&interval=1d")
        req2 = urllib.request.Request(url2, headers=headers)
        with urllib.request.urlopen(req2, timeout=30) as resp:
            data = json.loads(resp.read().decode("utf-8"))
            result = data["chart"]["result"][0]
            timestamps = result["timestamp"]
            quotes = result["indicators"]["quote"][0]
            rows = []
            for i in range(len(timestamps)):
                o = quotes["open"][i]
                h = quotes["high"][i]
                l = quotes["low"][i]
                c = quotes["close"][i]
                v = quotes["volume"][i] if quotes["volume"][i] else 0
                if o and h and l and c:
                    rows.append({
                        "date": datetime.fromtimestamp(timestamps[i]).strftime("%Y-%m-%d"),
                        "open": float(o), "high": float(h),
                        "low": float(l), "close": float(c),
                        "volume": int(v),
                    })
            print(f"  取得完了: {len(rows)}行")
            return rows

    reader = csv.DictReader(text.strip().split("\n"))
    rows = []
    for row in reader:
        try:
            rows.append({
                "date": row["Date"],
                "open": float(row["Open"]),
                "high": float(row["High"]),
                "low": float(row["Low"]),
                "close": float(row["Close"]),
                "volume": int(float(row.get("Volume", 0))),
            })
        except (ValueError, KeyError):
            continue

    print(f"  取得完了: {len(rows)}行 ({rows[0]['date']} ~ {rows[-1]['date']})")
    return rows


def generate_sample_data(base_price: float = 150.0, days: int = 500, seed: int = 42) -> list[dict]:
    """
    Yahoo Finance にアクセスできない場合のサンプルデータ生成
    ランダムウォーク + 平均回帰成分でリアルなFXデータを模擬
    """
    import random
    random.seed(seed)

    rows = []
    price = base_price
    start_date = datetime.now() - timedelta(days=days)

    for i in range(days):
        # 平均回帰 + ランダムウォーク
        mean_revert = (base_price - price) * 0.02
        change = mean_revert + random.gauss(0, 0.5)
        price += change

        o = price + random.gauss(0, 0.1)
        h = max(o, price) + abs(random.gauss(0, 0.3))
        l = min(o, price) - abs(random.gauss(0, 0.3))
        c = price

        date = start_date + timedelta(days=i)
        if date.weekday() < 5:  # 平日のみ
            rows.append({
                "date": date.strftime("%Y-%m-%d"),
                "open": round(o, 3),
                "high": round(h, 3),
                "low": round(l, 3),
                "close": round(c, 3),
                "volume": random.randint(10000, 100000),
            })

    print(f"  サンプルデータ生成: {len(rows)}行")
    return rows


# ============================================================
# インジケーター計算
# ============================================================

def sma(values: list[float], period: int) -> list[float]:
    result = [None] * len(values)
    for i in range(period - 1, len(values)):
        result[i] = sum(values[i - period + 1: i + 1]) / period
    return result


def ema(values: list[float], period: int) -> list[float]:
    result = [None] * len(values)
    k = 2 / (period + 1)
    result[period - 1] = sum(values[:period]) / period
    for i in range(period, len(values)):
        result[i] = values[i] * k + result[i - 1] * (1 - k)
    return result


def stdev(values: list[float], period: int) -> list[float]:
    result = [None] * len(values)
    for i in range(period - 1, len(values)):
        window = values[i - period + 1: i + 1]
        avg = sum(window) / period
        variance = sum((x - avg) ** 2 for x in window) / period
        result[i] = math.sqrt(variance)
    return result


def bollinger_bands(closes: list[float], period: int = 20, num_std: float = 2.0):
    mid = sma(closes, period)
    sd = stdev(closes, period)
    upper = [None] * len(closes)
    lower = [None] * len(closes)
    for i in range(len(closes)):
        if mid[i] is not None and sd[i] is not None:
            upper[i] = mid[i] + num_std * sd[i]
            lower[i] = mid[i] - num_std * sd[i]
    return upper, mid, lower


def rsi(closes: list[float], period: int = 14) -> list[float]:
    result = [None] * len(closes)
    if len(closes) < period + 1:
        return result

    gains = []
    losses = []
    for i in range(1, len(closes)):
        diff = closes[i] - closes[i - 1]
        gains.append(max(0, diff))
        losses.append(max(0, -diff))

    avg_gain = sum(gains[:period]) / period
    avg_loss = sum(losses[:period]) / period

    if avg_loss == 0:
        result[period] = 100
    else:
        result[period] = 100 - (100 / (1 + avg_gain / avg_loss))

    for i in range(period, len(gains)):
        avg_gain = (avg_gain * (period - 1) + gains[i]) / period
        avg_loss = (avg_loss * (period - 1) + losses[i]) / period
        if avg_loss == 0:
            result[i + 1] = 100
        else:
            result[i + 1] = 100 - (100 / (1 + avg_gain / avg_loss))

    return result


def atr(highs: list[float], lows: list[float], closes: list[float], period: int = 14) -> list[float]:
    tr_list = [None]
    for i in range(1, len(closes)):
        h_l = highs[i] - lows[i]
        h_c = abs(highs[i] - closes[i - 1])
        l_c = abs(lows[i] - closes[i - 1])
        tr_list.append(max(h_l, h_c, l_c))

    result = [None] * len(closes)
    valid_trs = [x for x in tr_list[1:period + 1] if x is not None]
    if len(valid_trs) == period:
        result[period] = sum(valid_trs) / period
        for i in range(period + 1, len(closes)):
            if tr_list[i] is not None and result[i - 1] is not None:
                result[i] = (result[i - 1] * (period - 1) + tr_list[i]) / period
    return result


# ============================================================
# トレード管理
# ============================================================

@dataclass
class Trade:
    entry_date: str
    entry_price: float
    direction: str  # "long" or "short"
    sl: float  # ストップロス
    tp: float  # テイクプロフィット
    exit_date: str = ""
    exit_price: float = 0.0
    pnl: float = 0.0
    exit_reason: str = ""


@dataclass
class BacktestResult:
    strategy_name: str
    trades: list = field(default_factory=list)
    equity_curve: list = field(default_factory=list)
    initial_cash: float = 100000
    final_equity: float = 0
    total_return_pct: float = 0
    win_rate: float = 0
    num_trades: int = 0
    max_drawdown_pct: float = 0
    sharpe_ratio: float = 0
    profit_factor: float = 0
    avg_trade_pct: float = 0

    def calculate_stats(self):
        if not self.trades:
            self.final_equity = self.initial_cash
            return

        self.num_trades = len(self.trades)
        wins = [t for t in self.trades if t.pnl > 0]
        losses = [t for t in self.trades if t.pnl <= 0]
        self.win_rate = len(wins) / self.num_trades * 100 if self.num_trades > 0 else 0

        # 最終資産
        self.final_equity = self.equity_curve[-1] if self.equity_curve else self.initial_cash
        self.total_return_pct = (self.final_equity - self.initial_cash) / self.initial_cash * 100

        # 最大ドローダウン
        peak = self.initial_cash
        max_dd = 0
        for eq in self.equity_curve:
            if eq > peak:
                peak = eq
            dd = (peak - eq) / peak * 100
            if dd > max_dd:
                max_dd = dd
        self.max_drawdown_pct = -max_dd

        # プロフィットファクター
        gross_profit = sum(t.pnl for t in wins)
        gross_loss = abs(sum(t.pnl for t in losses))
        self.profit_factor = gross_profit / gross_loss if gross_loss > 0 else float('inf')

        # 平均リターン
        trade_returns = [t.pnl / self.initial_cash * 100 for t in self.trades]
        self.avg_trade_pct = sum(trade_returns) / len(trade_returns) if trade_returns else 0

        # シャープレシオ（簡易版: 日次リターンから年率換算）
        if len(self.equity_curve) > 1:
            daily_returns = []
            for i in range(1, len(self.equity_curve)):
                r = (self.equity_curve[i] - self.equity_curve[i-1]) / self.equity_curve[i-1]
                daily_returns.append(r)
            if daily_returns:
                avg_r = sum(daily_returns) / len(daily_returns)
                std_r = math.sqrt(sum((r - avg_r)**2 for r in daily_returns) / len(daily_returns))
                self.sharpe_ratio = (avg_r / std_r * math.sqrt(252)) if std_r > 0 else 0


# ============================================================
# バックテストエンジン
# ============================================================

def run_backtest(data: list[dict], strategy_func, cash: float = 100000,
                 leverage: float = 25, commission: float = 0.0002,
                 strategy_name: str = "") -> BacktestResult:
    """
    バックテスト実行
    - leverage: レバレッジ倍率（FXは最大25倍）
    - commission: 片道手数料率
    """
    closes = [d["close"] for d in data]
    highs = [d["high"] for d in data]
    lows = [d["low"] for d in data]
    dates = [d["date"] for d in data]

    # インジケーター事前計算
    indicators = strategy_func("init", closes, highs, lows)

    equity = cash
    position = None  # Tradeオブジェクト
    trades = []
    equity_curve = []
    position_size = 0

    for i in range(50, len(data)):  # 最初の50本はインジケーター安定化用
        price = closes[i]
        high = highs[i]
        low = lows[i]

        # ポジションチェック（SL/TP判定）
        if position is not None:
            hit_sl = False
            hit_tp = False

            if position.direction == "long":
                if low <= position.sl:
                    hit_sl = True
                    exit_price = position.sl
                elif high >= position.tp:
                    hit_tp = True
                    exit_price = position.tp
            else:  # short
                if high >= position.sl:
                    hit_sl = True
                    exit_price = position.sl
                elif low <= position.tp:
                    hit_tp = True
                    exit_price = position.tp

            # 戦略独自のエグジット判定
            custom_exit = strategy_func("exit", closes, highs, lows, indicators, i, position)

            if hit_sl or hit_tp or custom_exit:
                if custom_exit and not (hit_sl or hit_tp):
                    exit_price = price

                if position.direction == "long":
                    pnl = (exit_price - position.entry_price) * position_size
                else:
                    pnl = (position.entry_price - exit_price) * position_size

                pnl -= abs(exit_price * position_size * commission)  # 手数料

                position.exit_date = dates[i]
                position.exit_price = exit_price
                position.pnl = pnl
                position.exit_reason = "SL" if hit_sl else ("TP" if hit_tp else "Signal")

                equity += pnl
                trades.append(position)
                position = None
                position_size = 0

        # エントリー判定
        if position is None:
            signal = strategy_func("signal", closes, highs, lows, indicators, i)
            if signal:
                direction, sl, tp = signal
                # ポジションサイズ: 資金の2%リスク
                risk_amount = equity * 0.02
                risk_per_unit = abs(price - sl)
                if risk_per_unit > 0:
                    position_size = min(risk_amount / risk_per_unit, equity * leverage / price)
                else:
                    position_size = equity * 0.1 / price

                cost = price * position_size * commission
                equity -= cost

                position = Trade(
                    entry_date=dates[i],
                    entry_price=price,
                    direction=direction,
                    sl=sl, tp=tp,
                )

        equity_curve.append(equity + (
            (price - position.entry_price) * position_size if position and position.direction == "long"
            else (position.entry_price - price) * position_size if position
            else 0
        ))

    # 未決済ポジションを最終価格で強制決済
    if position is not None:
        final_price = closes[-1]
        if position.direction == "long":
            pnl = (final_price - position.entry_price) * position_size
        else:
            pnl = (position.entry_price - final_price) * position_size
        position.exit_date = dates[-1]
        position.exit_price = final_price
        position.pnl = pnl
        position.exit_reason = "End"
        equity += pnl
        trades.append(position)

    result = BacktestResult(
        strategy_name=strategy_name,
        trades=trades,
        equity_curve=equity_curve,
        initial_cash=cash,
    )
    result.calculate_stats()
    return result


# ============================================================
# 戦略定義
# ============================================================

def bollinger_strategy(action, closes, highs, lows, indicators=None, i=None, position=None):
    """ボリンジャーバンド平均回帰"""
    if action == "init":
        bb_upper, bb_mid, bb_lower = bollinger_bands(closes, 20, 2.0)
        rsi_vals = rsi(closes, 14)
        atr_vals = atr(highs, lows, closes, 14)
        return {"bb_upper": bb_upper, "bb_mid": bb_mid, "bb_lower": bb_lower,
                "rsi": rsi_vals, "atr": atr_vals}

    if action == "signal":
        price = closes[i]
        bb_lower = indicators["bb_lower"][i]
        bb_upper = indicators["bb_upper"][i]
        bb_mid = indicators["bb_mid"][i]
        rsi_val = indicators["rsi"][i]
        atr_val = indicators["atr"][i]

        if any(v is None for v in [bb_lower, bb_upper, bb_mid, rsi_val, atr_val]):
            return None

        if price <= bb_lower and rsi_val < 35:
            sl = price - atr_val * 1.5
            tp = bb_mid
            return ("long", sl, tp)
        elif price >= bb_upper and rsi_val > 65:
            sl = price + atr_val * 1.5
            tp = bb_mid
            return ("short", sl, tp)
        return None

    if action == "exit":
        return False


def rsi_strategy(action, closes, highs, lows, indicators=None, i=None, position=None):
    """RSI逆張り"""
    if action == "init":
        rsi_vals = rsi(closes, 14)
        atr_vals = atr(highs, lows, closes, 14)
        sma_vals = sma(closes, 50)
        return {"rsi": rsi_vals, "atr": atr_vals, "sma": sma_vals}

    if action == "signal":
        price = closes[i]
        rsi_val = indicators["rsi"][i]
        atr_val = indicators["atr"][i]

        if rsi_val is None or atr_val is None:
            return None

        if rsi_val < 30:
            sl = price - atr_val * 2.0
            tp = price + atr_val * 2.0
            return ("long", sl, tp)
        elif rsi_val > 70:
            sl = price + atr_val * 2.0
            tp = price - atr_val * 2.0
            return ("short", sl, tp)
        return None

    if action == "exit":
        rsi_val = indicators["rsi"][i]
        if rsi_val is None:
            return False
        if position.direction == "long" and rsi_val > 55:
            return True
        if position.direction == "short" and rsi_val < 45:
            return True
        return False


def ma_cross_strategy(action, closes, highs, lows, indicators=None, i=None, position=None):
    """移動平均クロス + RSIフィルター"""
    if action == "init":
        fast = ema(closes, 10)
        slow = ema(closes, 30)
        rsi_vals = rsi(closes, 14)
        atr_vals = atr(highs, lows, closes, 14)
        return {"fast_ema": fast, "slow_ema": slow, "rsi": rsi_vals, "atr": atr_vals}

    if action == "signal":
        price = closes[i]
        fast_now = indicators["fast_ema"][i]
        fast_prev = indicators["fast_ema"][i - 1]
        slow_now = indicators["slow_ema"][i]
        slow_prev = indicators["slow_ema"][i - 1]
        rsi_val = indicators["rsi"][i]
        atr_val = indicators["atr"][i]

        if any(v is None for v in [fast_now, fast_prev, slow_now, slow_prev, rsi_val, atr_val]):
            return None

        # ゴールデンクロス
        if fast_prev <= slow_prev and fast_now > slow_now and rsi_val < 70:
            sl = price - atr_val * 2.0
            tp = price + atr_val * 3.0
            return ("long", sl, tp)
        # デッドクロス
        elif fast_prev >= slow_prev and fast_now < slow_now and rsi_val > 30:
            sl = price + atr_val * 2.0
            tp = price - atr_val * 3.0
            return ("short", sl, tp)
        return None

    if action == "exit":
        return False


# ============================================================
# メイン
# ============================================================

def print_result(r: BacktestResult):
    print(f"  最終資産: ¥{r.final_equity:,.0f}")
    print(f"  リターン: {r.total_return_pct:+.2f}%")
    print(f"  勝率: {r.win_rate:.1f}%")
    print(f"  取引回数: {r.num_trades}")
    print(f"  最大ドローダウン: {r.max_drawdown_pct:.2f}%")
    print(f"  シャープレシオ: {r.sharpe_ratio:.3f}")
    print(f"  プロフィットファクター: {r.profit_factor:.3f}")
    print(f"  平均トレード: {r.avg_trade_pct:.4f}%")


def main():
    output_dir = Path(__file__).parent / "results"
    output_dir.mkdir(exist_ok=True)

    symbols = {
        "USD/JPY": "USDJPY=X",
        "EUR/USD": "EURUSD=X",
        "GBP/USD": "GBPUSD=X",
    }

    strategies = [
        ("ボリンジャーバンド平均回帰", bollinger_strategy),
        ("RSI逆張り", rsi_strategy),
        ("移動平均クロス+RSI", ma_cross_strategy),
    ]

    all_results = {}

    for pair_name, symbol in symbols.items():
        print(f"\n{'#'*60}")
        print(f"# 通貨ペア: {pair_name}")
        print(f"{'#'*60}")

        try:
            data = fetch_forex_data(symbol, period_days=730)
        except Exception as e:
            print(f"  Yahoo Finance取得失敗 ({e}), サンプルデータ使用")
            base = {"USD/JPY": 150.0, "EUR/USD": 1.08, "GBP/USD": 1.26}
            data = generate_sample_data(base_price=base.get(pair_name, 150.0), days=500)

        if len(data) < 100:
            print(f"  データ不足 ({len(data)}行), スキップ")
            continue

        pair_results = []
        for name, strategy_func in strategies:
            print(f"\n{'='*50}")
            print(f"戦略: {name}")
            print(f"{'='*50}")

            result = run_backtest(data, strategy_func, cash=100000, strategy_name=name)
            print_result(result)
            pair_results.append(result)

        # 最適戦略選定
        best = None
        best_score = -float('inf')
        for r in pair_results:
            score = (
                r.win_rate * 0.30 +
                r.sharpe_ratio * 25.0 +
                r.profit_factor * 20.0 +
                r.total_return_pct * 0.15 +
                r.max_drawdown_pct * 0.10
            )
            if score > best_score:
                best_score = score
                best = r

        all_results[pair_name] = {
            "results": [{
                "戦略名": r.strategy_name,
                "最終資産": r.final_equity,
                "リターン(%)": r.total_return_pct,
                "勝率(%)": r.win_rate,
                "取引回数": r.num_trades,
                "最大DD(%)": r.max_drawdown_pct,
                "シャープレシオ": r.sharpe_ratio,
                "プロフィットファクター": r.profit_factor,
            } for r in pair_results],
            "best": best.strategy_name if best else "N/A",
        }

        if best:
            print(f"\n★ {pair_name} 最適戦略: {best.strategy_name}")

    # JSON保存
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    result_file = output_dir / f"backtest_{timestamp}.json"
    with open(result_file, "w", encoding="utf-8") as f:
        json.dump(all_results, f, ensure_ascii=False, indent=2)
    print(f"\n結果保存先: {result_file}")

    # 総合サマリー
    print(f"\n{'='*60}")
    print("【総合サマリー】")
    print(f"{'='*60}")
    for pair, d in all_results.items():
        print(f"\n  {pair}: 最適 → {d['best']}")
        for r in d["results"]:
            marker = " ★" if r["戦略名"] == d["best"] else ""
            print(f"    {r['戦略名']}: 勝率{r['勝率(%)']:.0f}% / "
                  f"リターン{r['リターン(%)']:+.1f}% / "
                  f"DD{r['最大DD(%)']:.1f}%{marker}")

    # トレード詳細ログ（最適戦略のみ）
    print(f"\n{'='*60}")
    print("【直近トレード例（最適戦略）】")
    print(f"{'='*60}")
    # 最初のペアの最適戦略のトレードを表示
    for pair_name, symbol in symbols.items():
        try:
            data = fetch_forex_data(symbol, period_days=730)
        except Exception:
            base = {"USD/JPY": 150.0, "EUR/USD": 1.08, "GBP/USD": 1.26}
            data = generate_sample_data(base_price=base.get(pair_name, 150.0), days=500)

        best_name = all_results.get(pair_name, {}).get("best", "")
        for name, func in strategies:
            if name == best_name:
                r = run_backtest(data, func, cash=100000, strategy_name=name)
                print(f"\n  {pair_name} - {name} (直近10トレード):")
                for t in r.trades[-10:]:
                    emoji = "✅" if t.pnl > 0 else "❌"
                    print(f"    {emoji} {t.entry_date} → {t.exit_date} | "
                          f"{t.direction:5s} | {t.entry_price:.3f} → {t.exit_price:.3f} | "
                          f"P&L: ¥{t.pnl:+,.0f} | {t.exit_reason}")
                break
        break  # 最初のペアだけ表示


if __name__ == "__main__":
    main()
