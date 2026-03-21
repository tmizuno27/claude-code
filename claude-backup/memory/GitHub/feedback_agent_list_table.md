---
name: エージェント一覧は表形式で出力
description: 「エージェント一覧」「エージェント」「チーム」「スキル」「コマンド」等の文脈で、以下の完全テンプレートをそのまま出力する
type: feedback
---

「エージェント一覧」「チーム一覧」はもちろん、「エージェント」「スキル」「チーム」「コマンド」など短い一言でも、一覧を求めている文脈と判断したら**以下のテンプレートをそのまま出力**する。

**Why:** ユーザーがすぐに `@エージェント名` や `/スキル名` をコピペして呼び出せるようにするため。

**How to apply:** 以下のテンプレートを毎回そのまま出力する。新しいエージェント・コマンド・スキルが追加された場合はこのテンプレート自体を更新すること。

---

## チーム（Team Leaders）

| 名前 | 呼び出し方 | 得意作業 |
|------|-----------|----------|
| content-pipeline-team | `@content-pipeline-team` | 記事量産（KW調査→記事生成→WP投稿→SNS投稿）3サイト一括 |
| product-factory-team | `@product-factory-team` | デジタル商品量産（企画→制作→出品）Gumroad/RapidAPI/拡張機能 |
| site-audit-team | `@site-audit-team` | 3サイト並列監査（SEO・リンク切れ・技術的問題・改善提案） |
| revenue-optimizer-team | `@revenue-optimizer-team` | 収益分析・最大化戦略・全事業KPI確認・優先順位提案 |
| affiliate-manager-team | `@affiliate-manager-team` | アフィリエイト管理（ASP提携・リンク挿入・収益最適化） |
| infrastructure-team | `@infrastructure-team` | インフラ管理（タスクスケジューラ・監視・自動化・デプロイ） |

## 個別エージェント（Agents）

| 名前 | 呼び出し方 | 得意作業 |
|------|-----------|----------|
| seo-researcher | `@seo-researcher` | KW調査（二本柱対応・競合分析） |
| article-writer | `@article-writer` | SEO記事生成（E-E-A-T重視・ファクトチェック付き） |
| wp-publisher | `@wp-publisher` | WordPress自動投稿（3サイト対応） |
| sns-scheduler | `@sns-scheduler` | X投稿コンテンツ生成・スケジュール管理 |
| analytics-reporter | `@analytics-reporter` | GA4/GSC週次レポート・パフォーマンス分析 |
| translator | `@translator` | 日本語↔スペイン語翻訳 |
| product-factory | `@product-factory` | 商品企画・パイプライン管理 |
| market-researcher | `@market-researcher` | 市場調査・競合分析・ニーズ発掘 |
| product-builder | `@product-builder` | 商品制作（テンプレート・API・拡張機能） |
| listing-publisher | `@listing-publisher` | 商品出品（Gumroad・RapidAPI等） |

## カスタムコマンド（Slash Commands）

| 名前 | 呼び出し方 | 内容 |
|------|-----------|------|
| morning-briefing | `/morning-briefing` | 毎朝の業務ブリーフィング（ログ健全性チェック＋優先アクション＋全事業ステータス） |
| task-health | `/task-health` | 52個の自動化タスク（Task Scheduler）の稼働状況を一括チェック |
| product-inventory | `/product-inventory` | 6プラットフォームの商品在庫・ステータス横断確認 |
| weekly-review | `/weekly-review` | 全事業の週次レビュー＋来週の優先順位設定 |

## ビルトインスキル（Skills）

| 名前 | 呼び出し方 | 得意作業 |
|------|-----------|----------|
| claude-api | `/claude-api` | Claude API/SDKを使ったアプリ構築 |
| frontend-design | `/frontend-design` | 高品質フロントエンドUI制作 |
| simplify | `/simplify` | コード品質レビュー・リファクタリング |
| loop | `/loop` | 定期タスク実行（例: `/loop 5m /foo`） |
| update-config | `/update-config` | Claude Code設定・hooks・権限管理 |

## 使い分けの目安

| やりたいこと | 推奨 |
|-------------|------|
| 記事1本だけ書きたい | `@article-writer` |
| 3サイト分まとめて記事量産 | `@content-pipeline-team` |
| 商品1つ作りたい | `@product-builder` |
| 商品まとめて量産・出品 | `@product-factory-team` |
| サイトの問題点を知りたい | `@site-audit-team` |
| 収益を上げたい・分析したい | `@revenue-optimizer-team` |
| アフィリエイト管理 | `@affiliate-manager-team` |
| インフラ・自動化の問題 | `@infrastructure-team` |
| 朝の業務開始時 | `/morning-briefing` |
| タスク稼働確認 | `/task-health` |
| 商品棚卸し | `/product-inventory` |
| 週末の振り返り | `/weekly-review` |
