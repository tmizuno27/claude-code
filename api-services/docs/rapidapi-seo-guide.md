# RapidAPI マーケットプレイス SEO・集客改善ガイド

作成日: 2026-03-19

## 現状サマリー

- 全21 API（10本出品済み、11本出品待ち）
- 全APIの subscribers: 0、requests: 0、revenue: $0
- Cloudflare Workers上で稼働（運用コスト$0）

---

## 1. RapidAPI内部SEOの仕組み

### ランキング要因（公式ドキュメントより）

RapidAPIの検索結果は以下の指標で順位付けされる:

| 指標 | 説明 |
|------|------|
| **Popularity Score** (1-10) | リクエスト数 × ユーザー数で算出 |
| **Average Latency** | 過去30日の平均レスポンス時間 |
| **Service Level** | 過去30日の成功率（2xx応答率） |
| **テキストマッチ** | description, tags, API名が検索クエリにマッチするか |

### Dashboard「検索ギャップ」機能

RapidAPI Dashboardでは「結果0件だった検索ワード Top 5」が表示される。これを活用して:
- そのキーワードを自APIのdescription/tagsに追加 → 検索ヒット率向上
- 定期的にチェックして未カバーのニーズを発見

---

## 2. Short Description 最適化

Short descriptionはAPIタイル（検索結果一覧）に表示される最重要テキスト。

### ベストプラクティス

1. **先頭20文字に主要機能キーワードを入れる** — 検索結果で切り詰められるため
2. **ユースケースを具体的に列挙** — 「for e-commerce, marketing, SaaS」など
3. **差別化ポイント** — 「no API key setup needed」「free tier available」「sub-100ms latency」
4. **競合APIで頻出するキーワードを含める** — RapidAPIで同カテゴリの人気APIのdescriptionを参考に

### 現状の問題点と改善案

| API | 現在のdescription冒頭 | 改善ポイント |
|-----|----------------------|-------------|
| QR Code | "Generate QR codes in PNG, SVG..." | OK。「Free tier」を先頭に移動するとCTR向上 |
| Email Validation | "Production-ready email validation..." | 「Disposable email detection」をもっと前に |
| Screenshot | "A fast, reliable API for..." | 冒頭の修飾語を削除し機能を先に |
| URL Shortener | "Create short URLs with..." | 「Click analytics」を強調 |

---

## 3. Long Description 最適化

Long descriptionはMarkdown対応。Endpoints タブの short description 直下に表示される。

### 構成テンプレート

```markdown
## Why [API Name]?
- [差別化ポイント1: 速度、精度、無料枠など]
- [差別化ポイント2]
- [差別化ポイント3]

## Use Cases
- **[ユースケース1]**: 具体的な説明
- **[ユースケース2]**: 具体的な説明
- **[ユースケース3]**: 具体的な説明

## Key Features
- ✅ [機能1]
- ✅ [機能2]
- ✅ [機能3]

## Quick Start
\`\`\`
curl -X GET "https://..." -H "X-RapidAPI-Key: YOUR_KEY"
\`\`\`

## Pricing
| Plan | Price | Requests/mo | Rate Limit |
|------|-------|-------------|------------|
| Basic (FREE) | $0 | 500 | 1/sec |
| Pro | $5.99 | 50,000 | 10/sec |
```

### 重要ポイント

- **画像を含める**: `![diagram](URL)` でアーキテクチャ図やスクリーンショットを追加
- **SEOキーワードを自然に散りばめる**: 「REST API」「JSON response」「free API」など汎用検索ワード
- **「FREE」を目立たせる**: 無料プランがあることは最大の集客ポイント

---

## 4. Tags 最適化

Tags（バッジ）はAPIタイルに表示され、検索フィルタリングにも使われる。

### タグ設計ルール

1. **5-10個が適切** — 多すぎると焦点がぼける
2. **一般的な検索ワード + 具体的な機能名** の組み合わせ
3. **競合APIのタグを調査して取り入れる**
4. **「free」「no-auth」「rest-api」等の汎用タグ** を追加

### 各APIのタグ改善提案

| API | 追加すべきタグ |
|-----|---------------|
| 01 QR Code | `free-api`, `rest-api`, `qr-generator`, `marketing-tools` |
| 02 Email Validation | `free-api`, `email-hygiene`, `bounce-detection`, `saas-tools` |
| 03 Link Preview | `unfurl`, `url-metadata`, `social-media`, `free-api` |
| 04 Screenshot | `web-capture`, `page-screenshot`, `pdf-generation`, `free-api` |
| 05 Text Analysis | `text-mining`, `content-analysis`, `ai`, `free-api` |
| 06 IP Geolocation | `ip-info`, `geo-lookup`, `fraud-detection`, `free-api` |
| 07 URL Shortener | `bitly-alternative`, `link-management`, `free-api` |
| 09 Hash & Encoding | `password-hash`, `data-encoding`, `jwt`, `free-api` |
| 10 Currency Exchange | `fx-rates`, `currency-converter`, `ecb`, `free-api` |
| 11 AI Text | `gpt`, `chatgpt-alternative`, `text-rewrite`, `free-api` |
| 13 Crypto Data | `defi`, `crypto-api`, `coin-prices`, `free-api` |
| 14 SEO Analyzer | `lighthouse`, `page-audit`, `on-page-seo`, `free-api` |
| 15 Weather | `weather-forecast`, `openweathermap-alternative`, `free-api` |
| 16 WHOIS Domain | `domain-info`, `ssl-check`, `nameserver`, `free-api` |
| 18 AI Translate | `deepl-alternative`, `free-translation`, `free-api` |
| 19 Trends | `trending-topics`, `social-trends`, `real-time`, `free-api` |
| 20 Company Data | `company-search`, `b2b-data`, `crm`, `free-api` |
| 21 WP Internal Link | `wordpress-seo`, `content-strategy`, `free-api` |

**全APIに共通で追加すべきタグ**: `free-api`, `rest-api`, `cloudflare-workers`（高速性のアピール）

---

## 5. カテゴリ選択の最適化

### 現状のカテゴリ配分

| カテゴリ | API数 | 問題点 |
|---------|-------|--------|
| Data | 7 | 過密。より具体的なカテゴリへ移動検討 |
| Tools | 4 | 妥当 |
| Finance | 2 | 妥当 |
| Text / Text Analysis | 2 | 統一が必要 |
| Weather | 1 | 妥当 |
| Translation | 1 | 妥当 |

### カテゴリ変更提案

| API | 現在 | 推奨 |
|-----|------|------|
| 03 Link Preview | Data | **Social** または **Tools** |
| 06 IP Geolocation | Data | **Location** |
| 14 SEO Analyzer | Data | **SEO** or **Tools** |
| 16 WHOIS Domain | Data | **Tools** |
| 19 Trends | Data | **Social** or **News** |
| 20 Company Data | Data | **Business** or **Data Enrichment** |

※ RapidAPI管理画面で利用可能なカテゴリ一覧を確認して最適なものを選択すること

---

## 6. 外部集客戦略（RapidAPI公式推奨）

### 6-1. チュートリアル・ブログ記事

RapidAPI公式ドキュメントが推奨する最も効果的な集客方法:

- **API Listing の Tutorials タブ** にコード例付きチュートリアルを追加
- **Dev.to / Hashnode / Medium** に「How to use [API名] in Python/Node.js」記事を投稿
- **RapidAPIゲストブログ**: 1000語以上の教育的な記事をRapidAPIブログに寄稿可能（宣伝色が強いと拒否される）

### 6-2. SEO（Google検索経由）

RapidAPIの各APIページはGoogleにインデックスされるため:

- API名に**検索されやすいキーワード**を含める（例: "Free QR Code Generator API"）
- Long descriptionに「alternative to [競合API名]」を自然に含める
- 外部ブログからRapidAPIリスティングページへリンクを張る

### 6-3. コミュニティマーケティング

- **Reddit**: r/webdev, r/programming, r/SideProject でAPIを紹介
- **Hacker News**: Show HN で無料APIコレクションとして投稿
- **Product Hunt**: 20 APIをバンドルして「Free Developer API Toolkit」としてローンチ
- **GitHub**: 各APIのサンプルコードをリポジトリとして公開し、README内にRapidAPIリンクを設置

### 6-4. Popularityスコアを上げるハック

Popularity = リクエスト数 × ユーザー数 なので:

1. **自分のプロジェクトで自APIを使う** — nambei-oyaji.com等のサイトから呼び出す
2. **無料プランの閾値を緩くする** — 試用ハードルを下げてsubscriber数を増やす
3. **コードスニペットを充実させる** — cURL, Python, Node.js, PHP, Ruby等を全部用意
4. **レスポンスタイムを最速に保つ** — Cloudflare Workers の利点を最大活用

---

## 7. 優先アクションリスト

### 即実行（リスティング最適化）

1. [ ] 全APIのtagsに `free-api`, `rest-api` を追加
2. [ ] 各APIのshort descriptionを見直し、先頭にキーワードを配置
3. [ ] 全APIのlong descriptionを上記テンプレートで書き直し
4. [ ] カテゴリの見直し（Data カテゴリが多すぎる問題を解消）
5. [ ] 未出品の11 API（#11-#21）を出品

### 短期（1-2週間）

6. [ ] 各APIにTutorialsタブのコンテンツを追加
7. [ ] Dev.to に「20 Free APIs Every Developer Needs」記事を投稿
8. [ ] GitHubにサンプルコードリポジトリを作成

### 中期（1ヶ月）

9. [ ] RapidAPI Dashboard の検索ギャップデータを確認しタグ/description調整
10. [ ] Product Hunt で "Free Developer API Toolkit" としてローンチ
11. [ ] Reddit r/webdev, r/programming で紹介

---

## 参考リンク

- [RapidAPI SEO Documentation](https://docs.rapidapi.com/docs/seo-search-engine-optimization)
- [Hub Listing - General Tab](https://docs.rapidapi.com/docs/hub-listing-general-tab)
- [Marketing Your API](https://docs.rapidapi.com/docs/ive-added-my-api-to-rapidapi-now-what)
- [Content Creation and Promotion](https://docs.rapidapi.com/docs/content-creation-promotion)
- [Tags Documentation](https://docs.rapidapi.com/docs/tags)
- [Advanced Searching & Filtering](https://docs.rapidapi.com/docs/advanced-searching-filtering)
- [Community: Best strategies to increase visibility](https://community.latenode.com/t/best-strategies-to-increase-visibility-for-apis-on-rapidapi-platform/26531)
