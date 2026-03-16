"""
Bybitから価格データを取得（ccxt経由）
認証不要 - 公開OHLCVデータのみ使用
"""
import ccxt
import pandas as pd
from datetime import datetime, timedelta
import time
import os

CACHE_DIR = os.path.join(os.path.dirname(__file__), "results", "cache")


def fetch_ohlcv(symbol="BTC/USDT", timeframe="1h", days=180, use_cache=True):
    """
    BybitからOHLCVデータを取得

    Args:
        symbol: 通貨ペア (例: "BTC/USDT", "ETH/USDT")
        timeframe: 時間足 (例: "1h", "4h", "1d")
        days: 取得日数
        use_cache: キャッシュ利用するか

    Returns:
        pandas DataFrame (Open, High, Low, Close, Volume)
    """
    os.makedirs(CACHE_DIR, exist_ok=True)
    cache_file = os.path.join(
        CACHE_DIR,
        f"{symbol.replace('/', '_')}_{timeframe}_{days}d.csv"
    )

    # キャッシュ確認（24時間以内なら再利用）
    if use_cache and os.path.exists(cache_file):
        mtime = os.path.getmtime(cache_file)
        if time.time() - mtime < 86400:
            df = pd.read_csv(cache_file, index_col=0, parse_dates=True)
            print(f"  キャッシュ使用: {cache_file}")
            return df

    print(f"  Bybitからデータ取得中: {symbol} {timeframe} ({days}日分)...")
    exchange = ccxt.bybit({"enableRateLimit": True})

    since = exchange.parse8601(
        (datetime.utcnow() - timedelta(days=days)).isoformat()
    )

    all_ohlcv = []
    while True:
        ohlcv = exchange.fetch_ohlcv(symbol, timeframe, since=since, limit=1000)
        if not ohlcv:
            break
        all_ohlcv.extend(ohlcv)
        since = ohlcv[-1][0] + 1
        if len(ohlcv) < 1000:
            break
        time.sleep(0.1)

    df = pd.DataFrame(all_ohlcv, columns=["timestamp", "Open", "High", "Low", "Close", "Volume"])
    df["timestamp"] = pd.to_datetime(df["timestamp"], unit="ms")
    df.set_index("timestamp", inplace=True)
    df = df[~df.index.duplicated(keep="last")]

    # キャッシュ保存
    df.to_csv(cache_file)
    print(f"  取得完了: {len(df)}本のローソク足")
    return df


def fetch_multiple_pairs(pairs=None, timeframe="1h", days=180):
    """複数ペアのデータを一括取得"""
    if pairs is None:
        pairs = ["BTC/USDT", "ETH/USDT", "SOL/USDT"]

    data = {}
    for pair in pairs:
        data[pair] = fetch_ohlcv(pair, timeframe, days)
    return data


if __name__ == "__main__":
    df = fetch_ohlcv("BTC/USDT", "1h", 90)
    print(f"\n取得データ:")
    print(f"  期間: {df.index[0]} ~ {df.index[-1]}")
    print(f"  件数: {len(df)}")
    print(f"\n直近5件:")
    print(df.tail())
