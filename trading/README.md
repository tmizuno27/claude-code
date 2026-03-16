# 自動売買ツール（個人使用）

Bybit向け仮想通貨自動売買ツール。

## 構成

```
trading/
├── backtest/
│   ├── strategies.py      # 戦略定義（3種）
│   ├── data_fetcher.py    # 価格データ取得（ccxt経由）
│   ├── run_backtest.py    # バックテスト実行
│   └── results/           # バックテスト結果出力
├── live/
│   ├── trader.py          # ライブ取引エンジン
│   ├── risk_manager.py    # リスク管理
│   └── config.json        # API設定（gitignore対象）
├── requirements.txt
└── README.md
```

## 戦略

1. **RSI平均回帰** - RSI売られすぎ/買われすぎで逆張り（勝率重視）
2. **ボリンジャーバンド平均回帰** - バンドタッチで逆張り
3. **MAクロス + RSIフィルター** - トレンドフォロー＋フィルター

## 使い方

```bash
# バックテスト実行
python backtest/run_backtest.py

# ライブ取引（ペーパー → 本番）
python live/trader.py --mode paper
python live/trader.py --mode live
```
