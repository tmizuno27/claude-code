"""自動売買Bot メインループ"""

import json
import time
import sys
from pathlib import Path

# プロジェクトルート
ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "src"))

from exchange import Exchange
from strategy import SMAStrategy
from utils import setup_logger, log_trade


def run():
    config_dir = ROOT / "config"
    settings = json.loads((config_dir / "settings.json").read_text("utf-8"))
    log_dir = ROOT / "logs"
    log_file = ROOT / settings["dashboard"]["log_file"]

    logger = setup_logger(log_dir)
    exchange = Exchange(config_dir)
    strategy_cfg = settings["strategy"]
    strategy = SMAStrategy(strategy_cfg["short_period"], strategy_cfg["long_period"])
    risk = settings["risk"]
    interval = settings["check_interval_seconds"]

    logger.info(f"=== 自動売買Bot起動 ===")
    logger.info(f"モード: {settings['mode']} | 通貨ペア: {settings['symbol']} | 間隔: {interval}秒")
    logger.info(f"戦略: SMA({strategy_cfg['short_period']}/{strategy_cfg['long_period']}) | 損切り: {risk['stop_loss_percent']}%")

    daily_pnl = 0.0
    entry_price = None

    while True:
        try:
            # ローソク足データ取得
            ohlcv = exchange.fetch_ohlcv(limit=strategy_cfg["long_period"] + 10)
            info = strategy.get_info(ohlcv)
            signal = info["signal"]
            price = info["price"]

            logger.info(f"価格: {price:.2f} | SMA短期: {info['sma_short']} | SMA長期: {info['sma_long']} | シグナル: {signal}")

            # 日次損失制限チェック
            if daily_pnl <= -(risk["max_daily_loss_percent"]):
                logger.warning(f"日次損失制限到達 ({daily_pnl:.2f}%)。Bot停止。")
                break

            usdt_balance = exchange.get_usdt_balance()
            btc_position = exchange.get_position()

            if signal == "buy" and usdt_balance > 10:
                # 残高の一定割合で買い
                trade_amount_usdt = usdt_balance * (risk["trade_size_percent"] / 100)
                amount = trade_amount_usdt / price
                order = exchange.buy(amount)
                entry_price = price
                trade = {"action": "buy", "price": price, "amount": amount, "order_id": order.get("id")}
                log_trade(log_file, trade)
                logger.info(f"★ 買い注文: {amount:.6f} BTC @ {price:.2f}")

            elif signal == "sell" and btc_position > 0.00001:
                order = exchange.sell(btc_position)
                # 損益計算
                if entry_price:
                    pnl_pct = ((price - entry_price) / entry_price) * 100
                    daily_pnl += pnl_pct
                    logger.info(f"損益: {pnl_pct:+.2f}% | 日次累計: {daily_pnl:+.2f}%")
                trade = {"action": "sell", "price": price, "amount": btc_position, "order_id": order.get("id"), "pnl_pct": pnl_pct if entry_price else None}
                log_trade(log_file, trade)
                entry_price = None
                logger.info(f"★ 売り注文: {btc_position:.6f} BTC @ {price:.2f}")

            # ストップロス
            elif entry_price and btc_position > 0.00001:
                loss_pct = ((price - entry_price) / entry_price) * 100
                if loss_pct <= -(risk["stop_loss_percent"]):
                    order = exchange.sell(btc_position)
                    daily_pnl += loss_pct
                    trade = {"action": "stop_loss", "price": price, "amount": btc_position, "order_id": order.get("id"), "pnl_pct": loss_pct}
                    log_trade(log_file, trade)
                    entry_price = None
                    logger.warning(f"★ 損切り: {btc_position:.6f} BTC @ {price:.2f} ({loss_pct:+.2f}%)")

        except Exception as e:
            logger.error(f"エラー: {e}")

        time.sleep(interval)


if __name__ == "__main__":
    run()
