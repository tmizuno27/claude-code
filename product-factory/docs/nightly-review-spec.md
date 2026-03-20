# Nightly Review — 自己改善ループ仕様

## 概要
Felixの「毎晩の自己改善ループ」を再現。毎晩23:00 PYTに実行し、全商品のパフォーマンスを分析→改善→新企画を自動生成する。

## 実行タイミング
- **Task Scheduler**: 毎日 23:00 PYT (UTC-3)
- **スクリプト**: `product-factory/scripts/nightly_review.py`
- **Healthchecks.io**: ping送信で稼働監視

## 処理フロー

### Step 1: 統計収集（collect_stats.py）
```
Gumroad API → 売上・ビュー・コンバージョン
RapidAPI    → API呼び出し数・サブスクリプション数
Chrome      → インストール数・評価
VSCode      → ダウンロード数・評価
```
出力: `product-factory/reports/stats/{date}-stats.json`

### Step 2: パフォーマンス分析
各商品をスコアリング:
- **Revenue Score**: 売上額（0-10）
- **Growth Score**: 前週比の伸び（0-10）
- **Engagement Score**: ビュー→購入のCVR（0-10）
- **Total Score**: 上記の加重平均

### Step 3: 改善アクション生成
- **Score < 3（低パフォーマンス）**: リスティング改善案を生成
  - タイトルのA/Bテスト案
  - 説明文の改善ポイント
  - 価格調整の提案
- **Score > 7（高パフォーマンス）**: 類似商品をpipeline.jsonに追加
  - 同カテゴリの派生商品
  - 同ターゲットの別カテゴリ商品

### Step 4: レポート出力
`product-factory/reports/{date}-review.md`:
```markdown
# Nightly Review — {date}

## サマリー
- 総商品数: XX
- 本日売上: $XX
- 累計売上: $XX
- pipeline残: XX件

## Top 5 商品
| 商品 | Score | 売上 | アクション |
|------|-------|------|-----------|

## 改善が必要な商品
| 商品 | Score | 問題 | 改善案 |
|------|-------|------|--------|

## 新規企画（自動追加）
| 企画名 | カテゴリ | 根拠 |
|--------|---------|------|
```

### Step 5: Healthchecks.io ping
- 成功時: ping
- 失敗時: /fail

## Phase 3で実装予定
Phase 1-2ではこの仕組みは稼働しない。Phase 3（1週間後）で実装開始。
