"""
バックテスト実行スクリプト
3戦略 × 複数通貨ペアで比較し、最適な組み合わせを特定
"""
import sys
import os
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
sys.path.insert(0, os.path.dirname(__file__))

import json
import pandas as pd
from datetime import datetime
from backtesting import Backtest
from backtesting.lib import FractionalBacktest

from data_fetcher import fetch_ohlcv
from strategies import RSIMeanReversion, BollingerMeanReversion, MACrossRSI

RESULTS_DIR = os.path.join(os.path.dirname(__file__), "results")
os.makedirs(RESULTS_DIR, exist_ok=True)

# ===== 設定 =====
PAIRS = ["BTC/USDT", "ETH/USDT", "SOL/USDT"]
TIMEFRAME = "1h"
DAYS = 180
INITIAL_CASH = 100000  # バックテスト用（USDT換算、結果は%で評価）
COMMISSION = 0.0006     # Bybit実効手数料（maker 0.02% + slippage）

STRATEGIES = {
    "RSI平均回帰": RSIMeanReversion,
    "ボリンジャーバンド": BollingerMeanReversion,
    "MAクロス+RSI": MACrossRSI,
}


def run_single_backtest(df, strategy_cls, pair_name, strategy_name):
    """単一のバックテストを実行"""
    # 価格が初期資金より高い場合、スケーリングして対応
    test_df = df.copy()
    max_price = test_df["Close"].max()
    scale = 1
    if max_price > INITIAL_CASH * 0.5:
        scale = max_price / (INITIAL_CASH * 0.01)
        for col in ["Open", "High", "Low", "Close"]:
            test_df[col] = test_df[col] / scale

    bt = Backtest(
        test_df,
        strategy_cls,
        cash=INITIAL_CASH,
        commission=COMMISSION,
        exclusive_orders=True,
        trade_on_close=True,
    )
    stats = bt.run()

    return {
        "通貨ペア": pair_name,
        "戦略": strategy_name,
        "リターン(%)": round(stats["Return [%]"], 2),
        "勝率(%)": round(stats["Win Rate [%]"], 2) if not pd.isna(stats["Win Rate [%]"]) else 0,
        "取引回数": stats["# Trades"],
        "最大DD(%)": round(stats["Max. Drawdown [%]"], 2),
        "シャープレシオ": round(stats["Sharpe Ratio"], 2) if not pd.isna(stats["Sharpe Ratio"]) else 0,
        "PF": round(stats["Profit Factor"], 2) if not pd.isna(stats["Profit Factor"]) else 0,
        "平均取引(%)": round(stats["Avg. Trade [%]"], 2) if not pd.isna(stats["Avg. Trade [%]"]) else 0,
    }, bt, stats


def run_all_backtests():
    """全組み合わせのバックテスト実行"""
    print("=" * 60)
    print("  自動売買バックテスト")
    print(f"  期間: {DAYS}日 | 時間足: {TIMEFRAME} | 手数料: {COMMISSION*100:.2f}%")
    print("=" * 60)

    # データ取得
    print("\n📊 データ取得中...")
    pair_data = {}
    for pair in PAIRS:
        pair_data[pair] = fetch_ohlcv(pair, TIMEFRAME, DAYS)

    # バックテスト実行
    print("\n🔄 バックテスト実行中...")
    results = []
    best_score = -999
    best_combo = None
    best_bt = None

    for pair in PAIRS:
        df = pair_data[pair]
        for name, cls in STRATEGIES.items():
            try:
                result, bt, stats = run_single_backtest(df, cls, pair, name)
                results.append(result)

                # スコア = シャープレシオ × 勝率重み
                win_rate = result["勝率(%)"]
                sharpe = result["シャープレシオ"]
                trades = result["取引回数"]

                # 取引回数が少なすぎる場合はペナルティ
                trade_penalty = 1.0 if trades >= 10 else trades / 10
                score = sharpe * (win_rate / 50) * trade_penalty

                if score > best_score:
                    best_score = score
                    best_combo = result
                    best_bt = bt

                status = "✅" if result["リターン(%)"] > 0 else "❌"
                print(f"  {status} {pair} × {name}: "
                      f"Return={result['リターン(%)']:+.1f}% "
                      f"WR={result['勝率(%)']:.0f}% "
                      f"Trades={result['取引回数']} "
                      f"Sharpe={result['シャープレシオ']:.2f}")
            except Exception as e:
                print(f"  ⚠️ {pair} × {name}: エラー - {e}")

    # 結果表示
    print("\n" + "=" * 60)
    print("  📋 全結果サマリー")
    print("=" * 60)

    df_results = pd.DataFrame(results)
    df_results = df_results.sort_values("シャープレシオ", ascending=False)
    print(df_results.to_string(index=False))

    # 最適戦略
    if best_combo:
        print("\n" + "=" * 60)
        print("  🏆 最適戦略")
        print("=" * 60)
        print(f"  通貨ペア: {best_combo['通貨ペア']}")
        print(f"  戦略:     {best_combo['戦略']}")
        print(f"  リターン: {best_combo['リターン(%)']:+.2f}%")
        print(f"  勝率:     {best_combo['勝率(%)']:.1f}%")
        print(f"  取引回数: {best_combo['取引回数']}")
        print(f"  最大DD:   {best_combo['最大DD(%)']:.1f}%")
        print(f"  シャープ: {best_combo['シャープレシオ']:.2f}")

    # 結果保存
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    results_file = os.path.join(RESULTS_DIR, f"backtest_{timestamp}.csv")
    df_results.to_csv(results_file, index=False, encoding="utf-8-sig")
    print(f"\n  結果保存: {results_file}")

    # 最適戦略のチャート保存
    if best_bt:
        try:
            chart_file = os.path.join(RESULTS_DIR, f"best_chart_{timestamp}.html")
            best_bt.plot(filename=chart_file, open_browser=False)
            print(f"  チャート: {chart_file}")
        except Exception as e:
            print(f"  チャート生成スキップ: {e}")

    # JSON保存（ライブ取引設定用）
    if best_combo:
        config = {
            "best_strategy": best_combo["戦略"],
            "best_pair": best_combo["通貨ペア"],
            "results": results,
            "timestamp": timestamp,
            "settings": {
                "timeframe": TIMEFRAME,
                "commission": COMMISSION,
                "days_tested": DAYS,
            }
        }
        config_file = os.path.join(RESULTS_DIR, f"backtest_config_{timestamp}.json")
        with open(config_file, "w", encoding="utf-8") as f:
            json.dump(config, f, ensure_ascii=False, indent=2)

    return df_results, best_combo


if __name__ == "__main__":
    run_all_backtests()
