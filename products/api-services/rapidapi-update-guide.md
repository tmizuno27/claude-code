# RapidAPI リスティング手動更新ガイド（全24本）

> 作成日: 2026-03-25
> 参照: `rapidapi-seo-improvements.md` に全APIの改善タイトル・説明・タグを記載済み

## API更新が手動な理由

RapidAPI Platform API（REST / GraphQL）は **Enterprise Hub専用** であり、公開マーケットプレイス（rapidapi.com）のリスティングをプログラムで更新するAPIは存在しない。GitHub Action（`RapidAPI/create_or_update_rapidapi_listing`）もEnterprise向け。そのため、RapidAPI Studio での手動更新が唯一の方法。

---

## 事前準備

1. `rapidapi-seo-improvements.md` を別タブで開いておく（コピペ元）
2. 24本を一気にやると約60-90分。優先順位順に10本ずつ分けるのも可

---

## 更新手順（1APIあたり約3分）

### Step 1: RapidAPI Studioにログイン

```
https://studio.rapidapi.com/
```

右上のアカウントアイコンからログイン済みであることを確認。

### Step 2: 対象APIを選択

左サイドバーの **My APIs** から対象APIをクリック。

### Step 3: Detailsタブを開く

上部タブから **Details** を選択。

### Step 4: タイトルを更新

**API Name** フィールドに、`rapidapi-seo-improvements.md` の「改善タイトル」をペースト。

> **注意**: RapidAPIの仕様で、タイトルに「API」という単語を含めると自動的に末尾の「API」が重複表示される場合がある。プレビューで確認すること。

### Step 5: Short Descriptionを更新

**Short Description** フィールドに、`rapidapi-seo-improvements.md` の「Short Description」をペースト。

### Step 6: Long Descriptionを更新

**Long Description** フィールドは、既存の `docs/rapidapi-studio-copypaste.md` の内容を使用。未作成分はShort Descriptionを拡張して記入。

### Step 7: タグを更新

**Tags** フィールドで：
1. 既存タグがあれば全て削除（×ボタン）
2. `rapidapi-seo-improvements.md` のタグをカンマ区切りでペースト
3. 各タグがチップとして表示されることを確認

### Step 8: 保存

**Save** ボタンをクリック。

### Step 9: 次のAPIへ

左サイドバーから次のAPIを選択し、Step 3-8を繰り返す。

---

## 優先順位（推奨更新順）

`rapidapi-seo-improvements.md` の優先順位表に従い、以下の順序で更新：

| 順番 | API# | 名前 | 理由 |
|------|------|------|------|
| 1 | #12 | Social Video Download | 動画DL系は検索需要が極めて高い |
| 2 | #02 | Email Validation | B2B需要大、有料転換率が高い |
| 3 | #13 | Crypto Data | 仮想通貨データは常時需要あり |
| 4 | #01 | QR Code Generator | 汎用性が高い |
| 5 | #06 | IP Geolocation | セキュリティ・アナリティクス用途 |
| 6 | #10 | Currency Exchange | Fintech・EC系 |
| 7 | #14 | SEO Analyzer | SEO需要高い |
| 8 | #11 | AI Text | AI系は検索爆増中 |
| 9 | #18 | AI Translation | 同上 |
| 10 | #19 | Trends Aggregator | ユニーク性が高い |
| 11 | #03 | Link Preview | - |
| 12 | #04 | Screenshot | - |
| 13 | #05 | Text Analysis | - |
| 14 | #07 | URL Shortener | - |
| 15 | #08 | JSON Formatter | - |
| 16 | #09 | Hash & Encoding | - |
| 17 | #15 | Weather | - |
| 18 | #16 | WHOIS Domain | - |
| 19 | #17 | News Aggregator | - |
| 20 | #20 | Company Data | - |
| 21 | #21 | WP Internal Link | - |
| 22 | #22 | PDF Generator | - |
| 23 | #23 | Placeholder Image | - |
| 24 | #24 | Markdown Converter | - |

---

## クイックコピペ用リファレンス

以下は全24本のタイトル・Short Description・タグの一覧。RapidAPI Studioで順番にペーストしていく用。

---

### #01 QR Code Generator

**タイトル:**
```
Free QR Code Generator API - PNG, SVG, Base64 | <50ms Edge Response
```

**Short Description:**
```
Free QR Code API - Generate PNG/SVG/Base64 in <50ms. Custom colors, error correction. 500 req/mo free.
```

**タグ:**
```
qr code, qr code generator, qr code api, barcode, png to base64, svg generator, free qr api, image generation, edge computing, marketing tools
```

---

### #02 Email Validation

**タイトル:**
```
Free Email Validation API - MX Lookup, Disposable Detection, Bulk Verify
```

**Short Description:**
```
Free Email Validator - MX check, disposable detection (500+ domains), typo fix, bulk. Save $390/mo vs ZeroBounce.
```

**タグ:**
```
email validation, email verification, disposable email, mx lookup, bulk email check, email api, bounce detection, email hygiene, lead validation, free email validator
```

---

### #03 Link Preview

**タイトル:**
```
Free Link Preview API - Open Graph, Twitter Cards, Favicon, Bulk URLs
```

**Short Description:**
```
Free URL metadata extractor - Open Graph, Twitter Cards, RSS discovery, bulk (10 URLs). Cached on edge.
```

**タグ:**
```
link preview, open graph, twitter cards, url metadata, web scraping, favicon, rss feed, social media preview, og tags, url parser
```

---

### #04 Screenshot

**タイトル:**
```
Free Website Screenshot API - Capture Any Page as PNG/JPEG | Custom Viewport
```

**Short Description:**
```
Free Screenshot API - Capture any URL as PNG/JPEG. Full-page, custom viewport (320-3840px), render delay. 500 req/mo free.
```

**タグ:**
```
screenshot api, website screenshot, webpage capture, url to image, png screenshot, full page capture, website thumbnail, web capture api, headless browser, website preview
```

---

### #05 Text Analysis

**タイトル:**
```
Free Text Analysis API - Sentiment, Keywords, Readability | NLP No AI Key
```

**Short Description:**
```
Free NLP API - Sentiment analysis, keyword extraction, readability score, language detection. No AI key needed.
```

**タグ:**
```
text analysis, sentiment analysis, keyword extraction, nlp api, readability score, language detection, natural language processing, text mining, content analysis, free nlp
```

---

### #06 IP Geolocation

**タイトル:**
```
Free IP Geolocation API - VPN Detection, City Lookup, Bulk | HTTPS Free
```

**Short Description:**
```
Free IP Lookup - Country, city, ISP, VPN/proxy detection, bulk (20 IPs). HTTPS on free tier. $5.99 vs $99 ipinfo.
```

**タグ:**
```
ip geolocation, ip lookup, vpn detection, proxy detection, ip address api, geoip, ip location, ip to country, bulk ip lookup, free ip api
```

---

### #07 URL Shortener

**タイトル:**
```
Free URL Shortener API - Short Links with Click Analytics & Expiration
```

**Short Description:**
```
Free URL Shortener - Create short links with click analytics (referrer, device, geo), custom aliases, expiration.
```

**タグ:**
```
url shortener, link shortener, short url, click analytics, link tracking, url redirect, custom short link, bitly alternative, link management, free url shortener
```

---

### #08 JSON Formatter

**タイトル:**
```
Free JSON Formatter API - Validate, Minify, Diff, CSV Convert | All-in-One
```

**Short Description:**
```
Free JSON toolkit API - Format, minify, validate, diff, JSON-to-CSV, CSV-to-JSON. The only all-in-one JSON API.
```

**タグ:**
```
json formatter, json validator, json minify, json to csv, csv to json, json diff, json parser, json api, data conversion, free json tool
```

---

### #09 Hash & Encoding

**タイトル:**
```
Free Hash & Encoding API - SHA256, MD5, Bcrypt, Base64, HMAC | Web Crypto
```

**Short Description:**
```
Free Hash API - SHA256/384/512, MD5, bcrypt, Base64, HMAC, random string. Web Crypto, zero dependencies.
```

**タグ:**
```
hash api, sha256, md5, bcrypt, base64 encode, hmac, encryption api, hash generator, encoding api, cryptography, password hash
```

---

### #10 Currency Exchange

**タイトル:**
```
Free Currency Exchange API - Real-Time FX Rates, Conversion, Historical | ECB Data
```

**Short Description:**
```
Free FX Rates API - 30+ currencies, real-time conversion, historical (1999~). ECB official data. Any base free.
```

**タグ:**
```
currency exchange, exchange rate api, forex api, currency converter, fx rates, ecb exchange rate, historical exchange rate, currency api, money conversion, free forex api
```

---

### #11 AI Text

**タイトル:**
```
Free AI Text API - Generate, Summarize, Translate, Rewrite | Llama 3.1 No Key
```

**Short Description:**
```
Free AI Text API - Generate, summarize, translate, rewrite with Llama 3.1. No OpenAI key, flat-rate pricing.
```

**タグ:**
```
ai text generation, llama api, text summarization, ai rewrite, text generation api, openai alternative, free ai api, content generation, ai summarizer, natural language generation
```

---

### #12 Social Video Download

**タイトル:**
```
Free Social Video Download API - YouTube, TikTok, Instagram, X | Extract URLs
```

**Short Description:**
```
Free Video Download API - Extract direct URLs from YouTube, TikTok, Instagram, X, Facebook, Reddit. Multiple qualities.
```

**タグ:**
```
video download api, youtube download, tiktok download, instagram video, social media downloader, video extractor, twitter video download, facebook video, video url api, free video api
```

---

### #13 Crypto Data

**タイトル:**
```
Free Crypto API - Real-Time Prices, Market Cap, Charts | 10,000+ Coins
```

**Short Description:**
```
Free Crypto API - Real-time prices, market cap, volume, charts for 10,000+ coins. Sub-100ms edge cached.
```

**タグ:**
```
crypto api, cryptocurrency prices, bitcoin api, market cap, crypto charts, coin data, ethereum api, crypto market data, defi api, free crypto api
```

---

### #14 SEO Analyzer

**タイトル:**
```
Free SEO Analyzer API - 19-Point Audit, Score 0-100 | Ahrefs Alternative
```

**Short Description:**
```
Free SEO Audit API - 19 weighted checks, 0-100 score, structured data, CI/CD ready. $9.99 vs Ahrefs $99/mo.
```

**タグ:**
```
seo analyzer, seo audit api, on-page seo, website audit, seo score, meta tags checker, structured data, seo tool api, ahrefs alternative, free seo api
```

---

### #15 Weather

**タイトル:**
```
Free Weather API - Forecast, Current, Historical | Open-Meteo Powered
```

**Short Description:**
```
Free Weather API - Current conditions, 48h hourly + 7d daily forecast, historical data. Open-Meteo (ECMWF/NOAA).
```

**タグ:**
```
weather api, weather forecast, current weather, historical weather, temperature api, open meteo, weather data, free weather api, hourly forecast, climate data
```

---

### #16 WHOIS Domain

**タイトル:**
```
Free WHOIS Domain API - Registrar Lookup, DNS Records, Domain Availability
```

**Short Description:**
```
Free WHOIS API - Domain registration data (RDAP), DNS records (A/MX/TXT/CNAME), availability check. Sub-100ms.
```

**タグ:**
```
whois api, domain lookup, dns records, domain availability, rdap, domain registration, mx record, domain info, nameserver lookup, free whois api
```

---

### #17 News Aggregator

**タイトル:**
```
Free News API - Headlines, Hacker News, Dev.to | Commercial Use OK
```

**Short Description:**
```
Free News API - Aggregate headlines from RSS, Hacker News, Dev.to. Category filter, keyword search. Commercial use OK.
```

**タグ:**
```
news api, news aggregator, headlines api, hacker news api, rss feed, tech news, news search, free news api, breaking news, content aggregation
```

---

### #18 AI Translation

**タイトル:**
```
Free AI Translation API - 100+ Languages | Meta M2M-100 No Google Key
```

**Short Description:**
```
Free AI Translation - 100+ languages via Meta M2M-100. Any-to-any direct, batch, auto-detect. No Google/DeepL key.
```

**タグ:**
```
translation api, ai translation, language translation, machine translation, multilingual api, deepl alternative, google translate alternative, free translation api, text translation, language detection
```

---

### #19 Trends Aggregator

**タイトル:**
```
Free Trends API - Google Trends + Reddit + GitHub + HN + Product Hunt in 1 API
```

**Short Description:**
```
The ONLY multi-source trends API. Google Trends, Reddit, GitHub, Hacker News, Product Hunt. 5 platforms, 1 subscription.
```

**タグ:**
```
trends api, google trends api, reddit trending, github trending, hacker news, product hunt, trending topics, market research, content strategy, social trends
```

---

### #20 Company Data

**タイトル:**
```
Free Company Data API - Business Lookup, CRM Enrichment | Clearbit Alternative
```

**Short Description:**
```
Free Company API - Search by name/domain, get industry, size, location, social profiles. Clearbit alternative at $0.
```

**タグ:**
```
company data api, business lookup, crm enrichment, lead generation, company search, clearbit alternative, b2b data, company information, domain enrichment, free company api
```

---

### #21 WP Internal Link

**タイトル:**
```
Free WordPress Internal Link API - SEO Link Suggestions | Only REST API
```

**Short Description:**
```
The ONLY REST API for internal link optimization. Keyword matching, relevance scoring. Works with any CMS, not just WP.
```

**タグ:**
```
internal link, wordpress api, seo links, link optimization, content linking, wordpress seo, link whisper alternative, internal linking, cms api, seo automation
```

---

### #22 PDF Generator

**タイトル:**
```
Free PDF Generator API - HTML/Markdown/URL to PDF | Custom Headers & Footers
```

**Short Description:**
```
Free PDF API - Convert HTML, Markdown, or URL to PDF. Custom page size, margins, headers/footers. 500 req/mo free.
```

**タグ:**
```
pdf generator, html to pdf, pdf api, markdown to pdf, url to pdf, document generation, invoice generator, pdf converter, report generation, free pdf api
```

---

### #23 Placeholder Image

**タイトル:**
```
Free Placeholder Image API - SVG/PNG with Text, Gradients, Presets
```

**Short Description:**
```
Free Placeholder API - Custom SVG/PNG with text overlay, gradients, category presets. For prototyping & wireframes.
```

**タグ:**
```
placeholder image, placeholder api, dummy image, svg generator, wireframe image, prototype images, image placeholder, test images, mock images, free placeholder
```

---

### #24 Markdown Converter

**タイトル:**
```
Free Markdown Converter API - HTML to MD, MD to HTML, GFM, TOC, Syntax Highlight
```

**Short Description:**
```
Free Markdown API - Bidirectional MD/HTML conversion, GFM tables, auto TOC, syntax highlighting. The only MD REST API.
```

**タグ:**
```
markdown converter, markdown to html, html to markdown, gfm, markdown api, table of contents, syntax highlighting, markdown parser, text converter, free markdown api
```

---

## チェックリスト

更新完了後、各APIで以下を確認：

- [ ] タイトルがRapidAPI検索結果で正しく表示されるか
- [ ] Short Descriptionが切れずに表示されるか
- [ ] タグが全て反映されているか
- [ ] 保存エラーが出ていないか

## 所要時間の目安

- 1APIあたり: 約2-3分（コピペのみ）
- 全24本: 約60-90分
- 推奨: 優先度1-10を先にやり（30分）、残り14本は翌日

## 更新後の効果測定

- 更新後1-2週間でRapidAPI内検索順位の変化を確認
- `rapidapi-stats.json` のsubscribers/requestsの変化を追跡
- 効果が薄い場合はタイトルのA/Bテストを検討
