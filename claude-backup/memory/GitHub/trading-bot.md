---
name: 自動売買ツール（Bybit）
description: Bybit向け仮想通貨自動売買ツール。バックテスト完了、口座開設待ち。
type: project
---

Bybit向け仮想通貨自動売買ツールを構築済み。

**Why:** 個人使用の自動売買で安定収入を目指す。小資金（数万〜数十万円）運用。

**現状:** Bybit口座開設待ち（パラグアイの住所証明が未完了）

**バックテスト最適結果:**
- 最優秀: MAクロス+RSI × BTC/USDT（Sharpe 4.91, 勝率64%, MaxDD -1.1%, Return +4.7%）
- 最適パラメータ: fast_ma=7, slow_ma=30, rsi_filter=60, sl_atr=2.0, tp_atr=2.0
- 全3ペア（BTC/ETH/SOL）でMAクロス+RSI戦略がプラス

**プロジェクトパス:** `claude-code/trading-bot/`（ライブ取引用）
- `src/bot.py` — ライブ取引エンジン（ccxt経由）
- `src/exchange.py` — 取引所接続
- `src/strategy.py` — 売買戦略
- `config/` — APIキー設定

**バックテストコード:** `claude-code/archive/trading-backtest/`（アーカイブ済み）

**How to apply:** Bybit口座開設完了の連絡があったら、テストネットAPIキー設定→ペーパートレード→少額リアル稼働の順で進める。
