---
name: Apify DaaS事業
description: Apify 6 Actor（既存5本改善済み+新規Website Tech Stack Detector）。全Actorにタイムアウト/リトライ追加、Store SEO最適化済み。apify pushでデプロイ待ち
type: project
---

## 2026-03-28更新（2回目）
- 全9 Actor: タイムアウト30秒+リトライ2回追加完了（amazon, email-finder, google-mapsに新規追加）
- 致命的バグ修正: trends-aggregator/sources.js の fetchWithRetry が自分自身を再帰呼び出し → fetch に修正
- 3 Actor（amazon, email-finder, google-maps）に .actor/actor.json + input_schema.json 新規作成
- keyword-research: dockerfile パス修正（./Dockerfile → ../Dockerfile）、version 0.1 → 1.0
- 全Actor input_schema にprefill値追加、SEO最適化済みdescription設定
- deploy-all.sh 一括デプロイスクリプト作成（--dry-run対応）
- deploy-guide.md 更新（価格設定最適化提案含む）
- 次アクション: `bash deploy-all.sh` で9 Actorデプロイ

## Apify DaaS事業（2026-03-16 立ち上げ完了）

Apify Store上に5つのActorを公開・収益化設定済み。

**Why:** RapidAPI 20本と合わせた二重収益チャネル。課金・管理はApify側が全自動処理。

**How to apply:** Actorの改善・追加API展開時はこの構成を前提とする。

### アカウント情報
- ユーザー名: miccho27
- プラン: Creator plan（$7.26/半年、次回請求: 2026-09）
- プロジェクトパス: `claude-code/products/api-services/apify-actors/`

### 公開Actor一覧

| # | Actor | Pricing | ソースAPI |
|---|-------|---------|----------|
| 1 | Social Video Downloader | $2.00 / 1,000 results | API 12 |
| 2 | Keyword Research (Google Suggest) | $3.00 / 1,000 results | Python script |
| 3 | Trends Aggregator | $2.00 / 1,000 results | API 19 |
| 4 | Company Data Enricher | $5.00 / 1,000 results | API 20 |
| 5 | SEO Analyzer | $3.00 / 1,000 results | API 14 |
| 6 | Website Tech Detector | $3.00 / 1,000 results | 新規 |
| 7 | Amazon Product Scraper | $3.00 / 1,000 results | 新規 |
| 8 | Email Finder | $4.00 / 1,000 results | 新規 |
| 9 | Google Maps Scraper | $3.00 / 1,000 results | 新規 |

### README更新（2026-03-27）
全5 ActorのREADMEをApify API経由で自動更新完了。

### 注意事項
- Apifyは毎日自動テストを実行。3日連続失敗で「under maintenance」マーク
- Redditソース（Trends Aggregator）は403エラーが出る場合あり（他ソースは正常）
- PayPal payout: t.mizuno27@gmail.com で設定済み（2026-03-20）、本人確認レビュー中（1-2営業日）
- Payout設定ページ: Apify Console → Insights → Payouts タブ（左メニュー Development → Insights）
