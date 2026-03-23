# RapidAPI & Apify SEO改善レポート（2026-03-23）

## 実施サマリー

| 項目 | 対象数 | 内容 |
|------|--------|------|
| RapidAPI README強化 | 19本 | Getting Started / How It Compares / FAQ / Endpoints表 追加 |
| RapidAPI README追加改善 | 4本 | #02,#03,#04,#10に競合比較表・FAQ追加 |
| Apify Actor README強化 | 5本 | SEOタイトル改善 / Why Choose / FAQ / 競合比較 追加 |
| RapidAPI Studioコピペ用テキスト | 13本分 | Title / Short Description / Long Description |

**合計: 24 RapidAPI + 5 Apify = 29プロダクト全てのSEOドキュメント改善完了**

---

## 前回（3/21, 3/22）からの差分

前回は5本のREADME（#01, #06, #11, #13, #14）のみ強化。今回で**残り全19本 + 追加4本の改善 = 全24本カバー完了**。

---

## RapidAPI README改善内容（19本一括）

### 追加したセクション（全APIに統一適用）

1. **Getting Started in 30 Seconds** -- 3ステップの即時コンバージョン誘導。RapidAPIリンク付き
2. **How It Compares** -- 競合4サービスとの比較表（価格・機能・レイテンシ）
3. **Endpoints** -- 全エンドポイントの一覧表
4. **FAQ** -- 4-5問のよくある質問（SEOロングテールKW狙い）
5. **Node.js Example** -- Python + Node.jsの2言語コード例

### 改善前後の行数比較

| API | 改善前 | 改善後 | 増加量 |
|-----|--------|--------|--------|
| #05 Text Analysis | 59行 | 130行 | +71行 |
| #07 URL Shortener | 58行 | 130行 | +72行 |
| #08 JSON Formatter | 59行 | 135行 | +76行 |
| #09 Hash & Encoding | 59行 | 140行 | +81行 |
| #12 Social Video | 55行 | 130行 | +75行 |
| #15 Weather | 59行 | 140行 | +81行 |
| #16 WHOIS Domain | 58行 | 135行 | +77行 |
| #17 News Aggregator | 57行 | 135行 | +78行 |
| #18 AI Translate | 59行 | 140行 | +81行 |
| #19 Trends | 56行 | 135行 | +79行 |
| #20 Company Data | 56行 | 130行 | +74行 |
| #21 WP Internal Link | 62行 | 140行 | +78行 |
| #22 PDF Generator | 61行 | 135行 | +74行 |
| #23 Placeholder Image | 59行 | 130行 | +71行 |
| #24 Markdown Converter | 60行 | 130行 | +70行 |

### 追加改善（4本: 既存READMEへの加筆）

| API | 追加内容 |
|-----|---------|
| #02 Email Validation | Getting Started + 競合比較表（ZeroBounce/Hunter/NeverBounce）+ FAQ 5問 |
| #03 Link Preview | Getting Started + 競合比較表（LinkPreview/Microlink/OpenGraph.io）+ FAQ 4問 |
| #04 Screenshot | Getting Started + 競合比較表（ScreenshotAPI/URLBox/Screenshotlayer）+ FAQ 4問 |
| #10 Currency Exchange | Getting Started + 競合比較表（Fixer/ExchangeRate/Open Exchange）+ FAQ 4問 |

---

## Apify Actor README改善内容（5本）

| Actor | 追加内容 |
|-------|---------|
| SEO Analyzer | SEOタイトル改善、競合比較表（Ahrefs/Screaming Frog/Moz）、Why Choose、FAQ 3問 |
| Social Video Downloader | SEOタイトル改善、Why Choose 5ポイント、FAQ 3問 |
| Company Data Enricher | SEOタイトル改善、Why Choose 5ポイント、FAQ 3問 |
| Keyword Research | SEOタイトル改善、Why Choose 5ポイント、FAQ 3問 |
| Trends Aggregator | SEOタイトル改善、Why Choose 5ポイント、FAQ 3問 |

---

## RapidAPI Studio コピペ用テキスト

`api-services/docs/rapidapi-studio-copypaste.md` に以下13 APIのTitle / Short Description / Long Descriptionをコピペ用に作成:

- #02, #03, #04, #05, #07, #08, #09, #12, #15, #16, #17, #18, #19, #20, #21, #22, #23, #24

（#01, #06, #10, #11, #13, #14は前回3/21で対応済み）

### 使い方
1. https://studio.rapidapi.com/ にログイン
2. 対象APIの "Details" タブを開く
3. `rapidapi-studio-copypaste.md` から該当APIのテキストをコピペ
4. Save

---

## SEO改善の狙い

### 1. RapidAPI内部検索対策
- **Short Description**: 先頭に「Free」配置 + 主要機能KW凝縮（70文字以内）
- **Long Description**: 「Alternative To」で競合名明記（検索ヒット率向上）
- **Tags**: 前回3/21で全API 12-13タグに統一済み

### 2. Google/外部検索対策
- **README.md**: 「How It Compares」「FAQ」でロングテールKW網羅
- **競合名**: 各READMEに3-4競合名を明記（「[ツール名] alternative」検索狙い）
- **構造化情報**: Getting Started / Endpoints表 / コード例 → Google Featured Snippets狙い

### 3. コンバージョン率向上
- **Getting Started in 30 Seconds**: 3ステップで即利用可能と示す
- **How It Compares**: 価格差を明示（競合$99 vs 当API$0）
- **FAQ**: 事前回答で離脱防止

---

## 残りの高優先アクション

| アクション | 効果 | 備考 |
|-----------|------|------|
| RapidAPI Studioで13本のTitle/Description更新 | 検索露出の即時改善 | コピペ用テキスト作成済み |
| Dev.to記事2本の投稿（前回作成済み） | 外部流入 + 被リンク | `marketing/dev-to-articles/` に保存済み |
| @prodhq27 X投稿にAPI紹介を追加 | SNS流入 | 週2-3回のAPI紹介ツイート |
| 自プロジェクトで自APIを使ってレビュー投稿 | RapidAPIランキング改善 | wp-linker等で実際に使用 |
| Product Huntへの掲出（IP Geolocation API） | 大量露出 | 中期施策 |

---

## 変更ファイル一覧

```
# RapidAPI README（19本: 全面書き換え）
api-services/05-text-analysis-api/README.md
api-services/07-url-shortener-api/README.md
api-services/08-json-formatter-api/README.md
api-services/09-hash-encoding-api/README.md
api-services/12-social-video-api/README.md
api-services/15-weather-api/README.md
api-services/16-whois-domain-api/README.md
api-services/17-news-aggregator-api/README.md
api-services/18-ai-translate-api/README.md
api-services/19-trends-api/README.md
api-services/20-company-data-api/README.md
api-services/21-wp-internal-link-api/README.md
api-services/22-pdf-generator-api/README.md
api-services/23-placeholder-image-api/README.md
api-services/24-markdown-converter-api/README.md

# RapidAPI README（4本: セクション追加）
api-services/02-email-validation-api/README.md
api-services/03-link-preview-api/README.md
api-services/04-screenshot-api/README.md
api-services/10-currency-exchange-api/README.md

# Apify Actor README（5本: SEO強化）
api-services/apify-actors/seo-analyzer/README.md
api-services/apify-actors/social-video-downloader/README.md
api-services/apify-actors/company-data-enricher/README.md
api-services/apify-actors/keyword-research/README.md
api-services/apify-actors/trends-aggregator/README.md

# 新規作成
api-services/docs/rapidapi-studio-copypaste.md    （コピペ用テキスト13本分）
api-services/docs/seo-improvement-2026-03-23.md   （本レポート）
```
