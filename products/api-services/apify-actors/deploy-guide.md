# Apify Actor デプロイガイド（9 Actor）

## Actor一覧と価格設定

| # | Actor | 推奨価格 | 競合比較 | ターゲット |
|---|-------|---------|---------|-----------|
| 1 | Amazon Product Scraper | $3.00 / 1,000 results | Jungle Scout $49/mo | ECセラー、リサーチャー |
| 2 | Company Data Enricher | $5.00 / 1,000 results | Clearbit $99/mo | B2Bセールス、マーケター |
| 3 | Email Finder | $4.00 / 1,000 results | Hunter.io $49/mo | リード獲得、営業 |
| 4 | Google Maps Scraper | $3.00 / 1,000 results | Outscraper $0.002/rec | ローカルSEO、営業 |
| 5 | Keyword Research | $3.00 / 1,000 results | Ahrefs $99/mo | SEO担当、ブロガー |
| 6 | SEO Analyzer | $3.00 / 1,000 results | Screaming Frog $259/yr | Web開発者、SEO担当 |
| 7 | Social Video Downloader | $2.00 / 1,000 results | yt-dlp(無料) | コンテンツクリエイター |
| 8 | Trends Aggregator | $2.00 / 1,000 results | BuzzSumo $99/mo | マーケター、ライター |
| 9 | Website Tech Detector | $3.00 / 1,000 results | BuiltWith $295/mo | セールス、競合分析 |

### 価格設定の根拠
- **高付加価値（$5.00）**: Company Data Enricher — B2Bデータは商用価値が高い
- **中付加価値（$3-4.00）**: Amazon, Email, Maps, Keyword, SEO, Tech — 明確な競合代替
- **低価格（$2.00）**: Social Video, Trends — 無料代替が多い分野、低価格で回転率狙い

## デプロイ手順

### 1. 前提条件

```bash
# Apify CLI インストール
npm install -g apify-cli

# ログイン（APIトークン: Apify Console → Settings → Integrations）
apify login
```

### 2. 一括デプロイ

```bash
cd "C:/Users/tmizu/マイドライブ/GitHub/claude-code/products/api-services/apify-actors"

# ドライラン（実際にはデプロイしない）
bash deploy-all.sh --dry-run

# 本番デプロイ
bash deploy-all.sh
```

### 3. 個別デプロイ

```bash
cd "C:/Users/tmizu/マイドライブ/GitHub/claude-code/products/api-services/apify-actors/[actor-name]"
apify push
```

### 4. デプロイ後の確認

1. https://console.apify.com/actors で各Actorを確認
2. 各ActorのPublicationタブでREADMEが反映されているか確認
3. テスト実行（各ActorのInput画面からprefillデータで実行）
4. Pricing設定を上記表の価格に合わせる

## 公開設定チェックリスト

各Actorについて以下をApify Consoleで確認:
- [ ] Actor名とタイトルが正しい
- [ ] READMEが表示されている
- [ ] Input Schemaのprefill値でテスト実行成功
- [ ] Pricing設定済み
- [ ] カテゴリ/タグ設定済み
- [ ] SEO: title/descriptionに競合名（代替ツール名）が含まれている

## 中断中の作業

- **Actor ID**: jmtLVhG6qPqjc0b34
- **URL**: https://console.apify.com/actors/jmtLVhG6qPqjc0b34/publication
- **状態**: Publication設定が途中で中断中（2026-03-16）
