# Gumroad Notion Templates 事業

## 概要
Notionテンプレート15本 + AIプロンプトパック4本をGumroadで販売するデジタルプロダクト事業。
英語圏グローバル市場をターゲットに、運用コスト$0で不労所得を構築する。

## 収益モデル
- **販売プラットフォーム**: Gumroad（手数料10%）
- **決済**: Gumroad経由（PayPal / Stripe）
- **運用コスト**: $0（Notion無料プラン + Gumroad無料プラン）

## テンプレート一覧・価格

| # | テンプレート名 | 価格 | ステータス |
|---|--------------|------|----------|
| 01 | Freelance Business OS | $19 | 出品済 |
| 02 | Content Creator Dashboard | $17 | 価格改定予定($15→$17) |
| 03 | Student Study Hub | $9 | 出品済 |
| 04 | Life OS / Second Brain | $19 | 出品済 |
| 05 | Small Business CRM | $19 | 価格改定予定($17→$19) |
| 06 | Side Hustle Tracker | $14 | 価格改定予定($12→$14) |
| 07 | Social Media Planner | $14 | 出品済 |
| 08 | Job Search Tracker | $9 | 出品済 |
| 09 | Book & Learning Tracker | $9 | 出品済 |
| 10 | Digital Products OS | $19 | 出品済 |
| 11 | Startup Launch Checklist | $12 | **NEW** 設計書+リスティング完了、Notion構築→出品待ち |
| 12 | Wedding Planning Hub | $17 | **NEW** 設計書+リスティング完了、Notion構築→出品待ち |
| 13 | Property Investment Tracker | $19 | **NEW** 設計書+リスティング完了、Notion構築→出品待ち |
| 14 | Travel Planner & Journal | $12 | **NEW** 設計書+リスティング完了、Notion構築→出品待ち |
| 15 | Habit Tracker & Goal System | $9 | **NEW** 設計書+リスティング完了、Notion構築→出品待ち |
| -- | Ultimate Bundle (全15本) | $49 (75% OFF) | リスティング更新済 |

**単品合計**: $204 / **バンドル**: $49 (75% OFF)

## ワークフロー

### テンプレート作成手順
1. `templates/` の設計書を見ながらNotionで構築
2. 全データベース・ビュー・リレーション・数式を設計書通りに作成
3. サンプルデータを入力（買い手が使い方を理解できるように）
4. Notionページ右上 → 「Share」→「Share to web」→ 「Allow duplicate as template」ON
5. テンプレートリンクを取得

### Gumroad出品手順
1. Gumroad → New Product → Digital Product
2. `listings/` のテキストをコピペ
3. Canvaでサムネイル作成（1600x900px）
4. テンプレートリンクをPDFに記載し、deliverableとして添付
5. 価格設定（Pay what you want: 最低価格 = 表示価格）
6. Publish

### マーケティング
1. **X (Twitter)**: `marketing/x-posts.md` の投稿を週2-3回
2. **Gumroad Discover**: タグ・カテゴリ最適化で自然流入
3. **Product Hunt**: バンドル出品
4. **Reddit**: r/Notion, r/productivity に価値提供型投稿
5. **SEO**: Gumroadページ自体のSEO最適化

## ファイル構成

```
gumroad-notion/
├── CLAUDE.md          ← このファイル
├── docs/
│   └── business-plan.md   ← 事業計画
├── templates/         ← 各テンプレートの完全設計書（15本）
├── listings/          ← Gumroad出品テキスト（英語、16本 + バンドル2種）
├── products/
│   └── ai-prompt-packs/  ← AIプロンプトパック4本
└── marketing/
    ├── x-posts.md            ← X投稿テキスト v1（10本）
    ├── x-posts-v2.md         ← X投稿テキスト v2（80本）
    ├── x-posts-new-products.md ← 新商品5本+バンドル用（30本）
    └── x-posts-batch2.md     ← 追加バッチ
```

## 注意事項
- 全出品テキスト・マーケティングは英語（グローバル市場向け）
- テンプレート内のサンプルデータも英語
- Notion APIは使わない（手動構築 → シェアリンク方式）
- 本名は使用しない（Gumroadプロフィールも匿名/ペンネーム）
