"""
パラメータ最適化スクリプト
有望な戦略×通貨ペアの組み合わせに対してグリッドサーチ
"""
import sys
import os
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
sys.path.insert(0, os.path.dirname(__file__))

import json
import pandas as pd
from datetime import datetime
from backtesting import Backtest

from data_fetcher import fetch_ohlcv
from strategies import RSIMeanReversion, BollingerMeanReversion, MACrossRSI

RESULTS_DIR = os.path.join(os.path.dirname(__file__), "results")
INITIAL_CASH = 100000
COMMISSION = 0.0006


def prepare_df(df):
    """価格スケーリング"""
    test_df = df.copy()
    max_price = test_df["Close"].max()
    if max_price > INITIAL_CASH * 0.5:
        scale = max_price / (INITIAL_CASH * 0.01)
        for col in ["Open", "High", "Low", "Close"]:
            test_df[col] = test_df[col] / scale
    return test_df


def optimize_macross_rsi(pair="SOL/USDT"):
    """MAクロス+RSI戦略の最適化"""
    print(f"\n{'='*60}")
    print(f"  MAクロス+RSI 最適化: {pair}")
    print(f"{'='*60}")

    df = fetch_ohlcv(pair, "1h", 180)
    test_df = prepare_df(df)

    bt = Backtest(
        test_df, MACrossRSI,
        cash=INITIAL_CASH, commission=COMMISSION,
        exclusive_orders=True, trade_on_close=True,
    )

    stats, heatmap = bt.optimize(
        fast_ma=range(5, 20, 2),
        slow_ma=range(20, 60, 5),
        rsi_period=[10, 14, 21],
        rsi_filter=range(55, 80, 5),
        sl_atr_mult=[1.0, 1.5, 2.0, 2.5],
        tp_atr_mult=[2.0, 3.0, 4.0, 5.0],
        maximize="Sharpe Ratio",
        constraint=lambda p: p.fast_ma < p.slow_ma,
        return_heatmap=True,
    )

    print(f"\n  最適パラメータ:")
    print(f"    fast_ma:      {stats._strategy.fast_ma}")
    print(f"    slow_ma:      {stats._strategy.slow_ma}")
    print(f"    rsi_period:   {stats._strategy.rsi_period}")
    print(f"    rsi_filter:   {stats._strategy.rsi_filter}")
    print(f"    sl_atr_mult:  {stats._strategy.sl_atr_mult}")
    print(f"    tp_atr_mult:  {stats._strategy.tp_atr_mult}")
    print(f"\n  結果:")
    print(f"    リターン:  {stats['Return [%]']:+.2f}%")
    print(f"    勝率:      {stats['Win Rate [%]']:.1f}%")
    print(f"    取引回数:  {stats['# Trades']}")
    print(f"    最大DD:    {stats['Max. Drawdown [%]']:.1f}%")
    print(f"    シャープ:  {stats['Sharpe Ratio']:.2f}")
    print(f"    PF:        {stats['Profit Factor']:.2f}" if not pd.isna(stats['Profit Factor']) else "    PF:        N/A")

    return stats


def optimize_rsi_mean_reversion(pair="BTC/USDT"):
    """RSI平均回帰の最適化"""
    print(f"\n{'='*60}")
    print(f"  RSI平均回帰 最適化: {pair}")
    print(f"{'='*60}")

    df = fetch_ohlcv(pair, "1h", 180)
    test_df = prepare_df(df)

    bt = Backtest(
        test_df, RSIMeanReversion,
        cash=INITIAL_CASH, commission=COMMISSION,
        exclusive_orders=True, trade_on_close=True,
    )

    stats = bt.optimize(
        rsi_period=[7, 10, 14, 21],
        oversold=range(20, 40, 5),
        overbought=range(65, 85, 5),
        sl_atr_mult=[1.0, 1.5, 2.0, 3.0],
        tp_atr_mult=[1.5, 2.0, 3.0, 4.0],
        maximize="Sharpe Ratio",
        constraint=lambda p: p.oversold < p.overbought - 20,
    )

    print(f"\n  最適パラメータ:")
    print(f"    rsi_period:   {stats._strategy.rsi_period}")
    print(f"    oversold:     {stats._strategy.oversold}")
    print(f"    overbought:   {stats._strategy.overbought}")
    print(f"    sl_atr_mult:  {stats._strategy.sl_atr_mult}")
    print(f"    tp_atr_mult:  {stats._strategy.tp_atr_mult}")
    print(f"\n  結果:")
    print(f"    リターン:  {stats['Return [%]']:+.2f}%")
    print(f"    勝率:      {stats['Win Rate [%]']:.1f}%")
    print(f"    取引回数:  {stats['# Trades']}")
    print(f"    最大DD:    {stats['Max. Drawdown [%]']:.1f}%")
    print(f"    シャープ:  {stats['Sharpe Ratio']:.2f}")
    print(f"    PF:        {stats['Profit Factor']:.2f}" if not pd.isna(stats['Profit Factor']) else "    PF:        N/A")

    return stats


def optimize_bollinger(pair="SOL/USDT"):
    """ボリンジャーバンドの最適化"""
    print(f"\n{'='*60}")
    print(f"  ボリンジャーバンド 最適化: {pair}")
    print(f"{'='*60}")

    df = fetch_ohlcv(pair, "1h", 180)
    test_df = prepare_df(df)

    bt = Backtest(
        test_df, BollingerMeanReversion,
        cash=INITIAL_CASH, commission=COMMISSION,
        exclusive_orders=True, trade_on_close=True,
    )

    stats = bt.optimize(
        bb_period=range(10, 35, 5),
        bb_std=[1.5, 2.0, 2.5, 3.0],
        sl_atr_mult=[1.0, 1.5, 2.0, 3.0],
        maximize="Sharpe Ratio",
    )

    print(f"\n  最適パラメータ:")
    print(f"    bb_period:    {stats._strategy.bb_period}")
    print(f"    bb_std:       {stats._strategy.bb_std}")
    print(f"    sl_atr_mult:  {stats._strategy.sl_atr_mult}")
    print(f"\n  結果:")
    print(f"    リターン:  {stats['Return [%]']:+.2f}%")
    print(f"    勝率:      {stats['Win Rate [%]']:.1f}%")
    print(f"    取引回数:  {stats['# Trades']}")
    print(f"    最大DD:    {stats['Max. Drawdown [%]']:.1f}%")
    print(f"    シャープ:  {stats['Sharpe Ratio']:.2f}")
    print(f"    PF:        {stats['Profit Factor']:.2f}" if not pd.isna(stats['Profit Factor']) else "    PF:        N/A")

    return stats


if __name__ == "__main__":
    print("=" * 60)
    print("  パラメータ最適化（全戦略 × 全ペア）")
    print("=" * 60)

    all_results = []

    # 全ペア × 全戦略で最適化
    for pair in ["BTC/USDT", "ETH/USDT", "SOL/USDT"]:
        try:
            s1 = optimize_rsi_mean_reversion(pair)
            all_results.append(("RSI平均回帰", pair, s1))
        except Exception as e:
            print(f"  エラー: RSI × {pair}: {e}")

        try:
            s2 = optimize_bollinger(pair)
            all_results.append(("ボリンジャー", pair, s2))
        except Exception as e:
            print(f"  エラー: BB × {pair}: {e}")

        try:
            s3 = optimize_macross_rsi(pair)
            all_results.append(("MAクロス+RSI", pair, s3))
        except Exception as e:
            print(f"  エラー: MA × {pair}: {e}")

    # 総合ランキング
    print(f"\n{'='*60}")
    print("  総合ランキング（最適化後）")
    print(f"{'='*60}")

    ranked = []
    for name, pair, stats in all_results:
        sharpe = stats['Sharpe Ratio'] if not pd.isna(stats['Sharpe Ratio']) else 0
        ret = stats['Return [%]']
        wr = stats['Win Rate [%]'] if not pd.isna(stats['Win Rate [%]']) else 0
        trades = stats['# Trades']
        dd = stats['Max. Drawdown [%]']
        pf = stats['Profit Factor'] if not pd.isna(stats['Profit Factor']) else 0
        ranked.append({
            "戦略": name, "ペア": pair,
            "Return%": round(ret, 2), "勝率%": round(wr, 1),
            "取引数": trades, "MaxDD%": round(dd, 1),
            "Sharpe": round(sharpe, 2), "PF": round(pf, 2),
        })

    df_ranked = pd.DataFrame(ranked).sort_values("Sharpe", ascending=False)
    print(df_ranked.to_string(index=False))

    # 最適設定をJSON保存
    if all_results:
        best = max(all_results, key=lambda x: x[2]['Sharpe Ratio'] if not pd.isna(x[2]['Sharpe Ratio']) else -999)
        best_name, best_pair, best_stats = best
        best_config = {
            "strategy": best_name,
            "pair": best_pair,
            "params": {k: getattr(best_stats._strategy, k)
                       for k in dir(best_stats._strategy)
                       if not k.startswith('_') and isinstance(getattr(best_stats._strategy, k), (int, float))},
            "performance": {
                "return_pct": round(best_stats['Return [%]'], 2),
                "win_rate": round(best_stats['Win Rate [%]'], 1) if not pd.isna(best_stats['Win Rate [%]']) else 0,
                "trades": best_stats['# Trades'],
                "max_dd": round(best_stats['Max. Drawdown [%]'], 1),
                "sharpe": round(best_stats['Sharpe Ratio'], 2),
            },
            "optimized_at": datetime.now().isoformat(),
        }
        config_file = os.path.join(RESULTS_DIR, "optimized_config.json")
        with open(config_file, "w", encoding="utf-8") as f:
            json.dump(best_config, f, ensure_ascii=False, indent=2)
        print(f"\n  最適設定保存: {config_file}")
        print(f"\n  🏆 最優秀: {best_name} × {best_pair} (Sharpe={best_stats['Sharpe Ratio']:.2f})")
