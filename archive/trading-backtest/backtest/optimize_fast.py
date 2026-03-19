"""
高速パラメータ最適化（軽量版）
パラメータ範囲を絞り、1ペアずつ高速に最適化
"""
import sys
import os
import warnings
warnings.filterwarnings("ignore")
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
sys.path.insert(0, os.path.dirname(__file__))

import json
import pandas as pd
from datetime import datetime
from backtesting import Backtest

from data_fetcher import fetch_ohlcv
from strategies import RSIMeanReversion, BollingerMeanReversion, MACrossRSI

RESULTS_DIR = os.path.join(os.path.dirname(__file__), "results")
os.makedirs(RESULTS_DIR, exist_ok=True)
INITIAL_CASH = 100000
COMMISSION = 0.0006


def prepare_df(df):
    test_df = df.copy()
    max_price = test_df["Close"].max()
    if max_price > INITIAL_CASH * 0.5:
        scale = max_price / (INITIAL_CASH * 0.01)
        for col in ["Open", "High", "Low", "Close"]:
            test_df[col] = test_df[col] / scale
    return test_df


def optimize_one(pair, strategy_cls, strategy_name, params, timeframe="1h", days=180):
    print(f"  {pair} x {strategy_name}...", end=" ", flush=True)
    df = fetch_ohlcv(pair, timeframe, days)
    test_df = prepare_df(df)

    bt = Backtest(
        test_df, strategy_cls,
        cash=INITIAL_CASH, commission=COMMISSION,
        exclusive_orders=True, trade_on_close=True,
    )
    try:
        stats = bt.optimize(**params, maximize="Sharpe Ratio")
        ret = stats["Return [%]"]
        wr = stats["Win Rate [%]"] if not pd.isna(stats["Win Rate [%]"]) else 0
        trades = stats["# Trades"]
        dd = stats["Max. Drawdown [%]"]
        sharpe = stats["Sharpe Ratio"] if not pd.isna(stats["Sharpe Ratio"]) else 0
        pf = stats["Profit Factor"] if not pd.isna(stats["Profit Factor"]) else 0

        # 最適パラメータ取得
        opt_params = {}
        for k in params:
            if k in ("maximize", "constraint", "return_heatmap"):
                continue
            opt_params[k] = getattr(stats._strategy, k)

        status = "OK" if ret > 0 else "NG"
        print(f"{status} Return={ret:+.1f}% WR={wr:.0f}% Trades={trades} Sharpe={sharpe:.2f}")

        return {
            "pair": pair, "strategy": strategy_name,
            "return": round(ret, 2), "win_rate": round(wr, 1),
            "trades": trades, "max_dd": round(dd, 1),
            "sharpe": round(sharpe, 2), "pf": round(pf, 2),
            "params": opt_params,
        }
    except Exception as e:
        print(f"ERROR: {e}")
        return None


def main():
    print("=" * 60)
    print("  高速パラメータ最適化")
    print("=" * 60)

    pairs = ["BTC/USDT", "ETH/USDT", "SOL/USDT"]
    results = []

    # 1. RSI平均回帰（パラメータ絞り込み済み）
    print("\n[1/3] RSI平均回帰")
    for pair in pairs:
        r = optimize_one(pair, RSIMeanReversion, "RSI平均回帰", {
            "rsi_period": [7, 14, 21],
            "oversold": [25, 30, 35],
            "overbought": [65, 70, 75],
            "sl_atr_mult": [1.5, 2.0],
            "tp_atr_mult": [2.0, 3.0],
            "constraint": lambda p: p.oversold < p.overbought - 25,
        })
        if r:
            results.append(r)

    # 2. ボリンジャーバンド
    print("\n[2/3] ボリンジャーバンド")
    for pair in pairs:
        r = optimize_one(pair, BollingerMeanReversion, "ボリンジャー", {
            "bb_period": [15, 20, 25],
            "bb_std": [1.5, 2.0, 2.5],
            "sl_atr_mult": [1.5, 2.0],
        })
        if r:
            results.append(r)

    # 3. MAクロス+RSI
    print("\n[3/3] MAクロス+RSI")
    for pair in pairs:
        r = optimize_one(pair, MACrossRSI, "MAクロス+RSI", {
            "fast_ma": [7, 10, 15],
            "slow_ma": [25, 30, 40],
            "rsi_filter": [60, 65, 70],
            "sl_atr_mult": [1.5, 2.0, 2.5],
            "tp_atr_mult": [2.0, 3.0, 4.0],
            "constraint": lambda p: p.fast_ma < p.slow_ma,
        })
        if r:
            results.append(r)

    # 結果ランキング
    print(f"\n{'='*60}")
    print("  最適化後 総合ランキング")
    print(f"{'='*60}\n")

    results.sort(key=lambda x: x["sharpe"], reverse=True)
    print(f"{'順位':>4} {'ペア':<10} {'戦略':<14} {'Return%':>8} {'勝率%':>6} {'取引数':>5} {'MaxDD%':>7} {'Sharpe':>7} {'PF':>5}")
    print("-" * 70)
    for i, r in enumerate(results):
        mark = " *" if i == 0 else ""
        print(f"{i+1:>4} {r['pair']:<10} {r['strategy']:<14} {r['return']:>+7.1f}% {r['win_rate']:>5.0f}% {r['trades']:>5} {r['max_dd']:>6.1f}% {r['sharpe']:>7.2f} {r['pf']:>5.2f}{mark}")

    # 最優秀の詳細
    if results:
        best = results[0]
        print(f"\n{'='*60}")
        print(f"  最優秀: {best['strategy']} x {best['pair']}")
        print(f"{'='*60}")
        print(f"  リターン:    {best['return']:+.2f}%")
        print(f"  勝率:        {best['win_rate']:.1f}%")
        print(f"  取引回数:    {best['trades']}")
        print(f"  最大DD:      {best['max_dd']:.1f}%")
        print(f"  シャープ:    {best['sharpe']:.2f}")
        print(f"  PF:          {best['pf']:.2f}")
        print(f"  最適パラメータ:")
        for k, v in best["params"].items():
            print(f"    {k}: {v}")

        # JSON保存
        # numpy int64をPython intに変換
        def convert(obj):
            if isinstance(obj, dict):
                return {k: convert(v) for k, v in obj.items()}
            if isinstance(obj, list):
                return [convert(v) for v in obj]
            if hasattr(obj, "item"):
                return obj.item()
            return obj

        config_file = os.path.join(RESULTS_DIR, "optimized_config.json")
        with open(config_file, "w", encoding="utf-8") as f:
            json.dump(convert({
                "best": best,
                "all_results": results,
                "optimized_at": datetime.now().isoformat(),
            }), f, ensure_ascii=False, indent=2)
        print(f"\n  設定保存: {config_file}")


if __name__ == "__main__":
    main()
