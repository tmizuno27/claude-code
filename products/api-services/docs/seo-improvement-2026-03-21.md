# RapidAPI SEO・導線改善レポート（2026-03-21）

## 実施サマリー

| 項目 | 対象数 | 内容 |
|------|--------|------|
| Short Description最適化 | 24本 | 競合キーワード追加、文字数70-78ch統一 |
| Long Description拡張 | 24本 | 「Alternative To」「Sample Response」「Need More Requests?」セクション追加 |
| Tags標準化 | 24本 | 全API 12-13タグに統一、API 22-24に`free-api`/`rest-api`追加 |
| README.md新規作成 | 3本 | API 22(PDF), 23(Placeholder Image), 24(Markdown Converter) |

---

## 改善内容の詳細

### 1. Short Description SEO最適化（全24本）

RapidAPI検索結果のタイルに表示される最重要テキスト。全APIで以下を統一:
- **先頭に「Free」を配置** → CTR向上（無料検索フィルターにも対応）
- **主要機能キーワードを70文字以内に凝縮**
- **差別化ワード追加**: "No Auth Required", "Custom", "Bulk" 等

| API | 変更前 | 変更後 |
|-----|--------|--------|
| 01 QR Code | Free QR Code Generator - PNG, SVG... | Free QR Code Generator API - PNG, SVG, Base64, Custom Colors, No Auth Required |
| 02 Email | Free Email Validation: Disposable... | Free Email Validation API - Disposable Detection, MX Lookup, Typo Fix, No Auth |
| 11 AI Text | Free AI Text Generation: Summarize... | Free AI Text API - Generate, Summarize, Translate, Rewrite with Llama 3.1 |
| 22 PDF | Free PDF Generator: HTML/Markdown... | Free PDF Generator API - HTML/Markdown/URL to PDF, Headers, Footers |
| 24 Markdown | Free Markdown Converter: HTML to... | Free Markdown Converter API - HTML to Markdown, TOC, GFM, Syntax Highlight |

（他19本も同様に最適化済み）

### 2. Long Description拡張（全24本）

各APIのlong_descriptionに以下3セクションを追加:

#### 「Alternative To」セクション
Google検索で「[ツール名] alternative API」を狙うキーワード戦略。各APIごとに競合3サービスを名指し:

| API | 記載した競合名 |
|-----|---------------|
| 01 QR Code | goqr.me, QR Server, QRickit |
| 02 Email | ZeroBounce, Hunter.io, NeverBounce |
| 05 Text Analysis | MonkeyLearn, Aylien, MeaningCloud |
| 06 IP Geolocation | ipinfo.io, ipstack, ip-api.com |
| 10 Currency | Fixer.io, ExchangeRate-API, Open Exchange Rates |
| 11 AI Text | OpenAI GPT, Cohere, AI21 Labs |
| 13 Crypto | CoinMarketCap, CoinGecko Pro, CryptoCompare |
| 14 SEO Analyzer | Ahrefs, Moz, Screaming Frog |
| 15 Weather | OpenWeatherMap, WeatherAPI, AccuWeather |
| 18 AI Translate | DeepL, Google Translate API, LibreTranslate |
| 20 Company Data | Clearbit, ZoomInfo, FullContact |
| 22 PDF | PDFShift, HTML2PDF, DocRaptor |

（他12本も同様に競合名を記載）

#### 「Sample Response」セクション（該当API）
JSON応答例をlong_descriptionに追加。ユーザーがテスト前に出力イメージを確認可能に。

#### 「Need More Requests?」セクション
無料プランから有料プランへの自然なアップセル導線:
- 無料プランの用途を明示（prototyping, testing, personal use）
- Pro プランの具体的メリットを記載（リクエスト数、レート制限）
- 価格を明示（$5.99/mo or $9.99/mo）

### 3. Tags標準化（全24本）

**変更前**: API 22-24は9-10タグのみ（`free-api`, `rest-api`が欠落）
**変更後**: 全24 APIが12-13タグに統一

追加したタグ:
| API | 追加タグ |
|-----|---------|
| 01 QR Code | `png`, `svg` |
| 22 PDF Generator | `free-api`, `rest-api`, `developer-tools` |
| 23 Placeholder Image | `free-api`, `rest-api`, `developer-tools` |
| 24 Markdown Converter | `free-api`, `rest-api`, `developer-tools`, `text-processing` |

### 4. README.md新規作成（3本）

API 22-24にREADME.mdがなかったため新規作成:
- `22-pdf-generator-api/README.md` — エンドポイント、パラメータ、使用例
- `23-placeholder-image-api/README.md` — グラデーション/カテゴリプリセット一覧
- `24-markdown-converter-api/README.md` — 双方向変換、TOC生成の使用例

---

## 変更ファイル一覧

```
api-services/
├── 01-qr-code-api/rapidapi-listing.json          ← 更新
├── 02-email-validation-api/rapidapi-listing.json  ← 更新
├── 03-link-preview-api/rapidapi-listing.json      ← 更新
├── 04-screenshot-api/rapidapi-listing.json        ← 更新
├── 05-text-analysis-api/rapidapi-listing.json     ← 更新
├── 06-ip-geolocation-api/rapidapi-listing.json    ← 更新
├── 07-url-shortener-api/rapidapi-listing.json     ← 更新
├── 08-json-formatter-api/rapidapi-listing.json    ← 更新
├── 09-hash-encoding-api/rapidapi-listing.json     ← 更新
├── 10-currency-exchange-api/rapidapi-listing.json ← 更新
├── 11-ai-text-api/rapidapi-listing.json           ← 更新
├── 12-social-video-api/rapidapi-listing.json      ← 更新
├── 13-crypto-data-api/rapidapi-listing.json       ← 更新
├── 14-seo-analyzer-api/rapidapi-listing.json      ← 更新
├── 15-weather-api/rapidapi-listing.json           ← 更新
├── 16-whois-domain-api/rapidapi-listing.json      ← 更新
├── 17-news-aggregator-api/rapidapi-listing.json   ← 更新
├── 18-ai-translate-api/rapidapi-listing.json      ← 更新
├── 19-trends-api/rapidapi-listing.json            ← 更新
├── 20-company-data-api/rapidapi-listing.json      ← 更新
├── 21-wp-internal-link-api/rapidapi-listing.json  ← 更新
├── 22-pdf-generator-api/rapidapi-listing.json     ← 更新
├── 22-pdf-generator-api/README.md                 ← 新規
├── 23-placeholder-image-api/rapidapi-listing.json ← 更新
├── 23-placeholder-image-api/README.md             ← 新規
├── 24-markdown-converter-api/rapidapi-listing.json← 更新
├── 24-markdown-converter-api/README.md            ← 新規
├── scripts/seo_improve_listings.py                ← 新規（改善スクリプト）
└── docs/seo-improvement-2026-03-21.md             ← 本レポート
```

---

## RapidAPIへの反映方法

更新した`rapidapi-listing.json`をRapidAPI Studioに反映するには:

```bash
# Chrome をデバッグモードで起動
"C:\Program Files\Google\Chrome\Application\chrome.exe" --remote-debugging-port=9222 --user-data-dir=C:\Users\tmizu\chrome-debug-profile https://rapidapi.com/studio/

# RapidAPI Studio にログインした状態で実行
cd c:\Users\tmizu\マイドライブ\GitHub\claude-code\api-services
python scripts/rapidapi_studio_updater.py
```

既存の`rapidapi_studio_updater.py`がshort description / long descriptionを自動入力する。

---

## 次のアクション（推奨）

1. **即実行**: `rapidapi_studio_updater.py`で24本分のlisting反映
2. **1週間後**: RapidAPI Dashboardの検索ギャップデータを確認し、タグ/descriptionを微調整
3. **外部集客**: Dev.toに「24 Free APIs Every Developer Needs in 2026」記事を投稿
4. **自己利用**: nambei-oyaji.com等から自APIを呼び出してPopularityスコアを上げる
5. **Product Hunt**: 24 APIをバンドルして「Free Developer API Toolkit」としてローンチ
