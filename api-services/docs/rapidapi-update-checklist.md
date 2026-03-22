# RapidAPI リスティング更新チェックリスト

作成日: 2026-03-22 | 全24 API対象 | 参考: [rapidapi-marketing-plan.md](./rapidapi-marketing-plan.md)

## 所要時間

- 1 API あたり約5分 × 24本 = 約2時間
- 優先6本を先にやれば30分で最大インパクト

---

## 更新の優先順位

**Phase 1（最優先・高需要6本）** — まずこの6本を完了させる:

| 順番 | Dir | API名 | 理由 |
|------|-----|--------|------|
| 1 | 06 | IP Geolocation | 唯一の有料サブスク（$9.99）。最優先で強化 |
| 2 | 04 | Screenshot | 開発者需要が非常に高い |
| 3 | 01 | QR Code | 検索ボリューム大、競合多い→差別化必須 |
| 4 | 02 | Email Validation | SaaS開発者の必須ツール |
| 5 | 10 | Currency Exchange | Fintech需要 |
| 6 | 14 | SEO Analyzer | SEO業界からの流入期待 |

**Phase 2（中需要7本）**:
07-URL Shortener, 22-PDF Generator, 12-Social Video, 13-Crypto Data, 11-AI Text, 18-AI Translate, 16-WHOIS Domain

**Phase 3（残り11本）**:
03, 05, 08, 09, 15, 17, 19, 20, 21, 23, 24

---

## 各APIの更新手順（1本あたり約5分）

### ステップ1: Rapid Studio を開く

```
https://rapidapi.com/studio
```

左メニューから対象APIを選択。

### ステップ2: Listing タブ → 説明文を更新

READMEから以下をコピペ:

| RapidAPI Studio のフィールド | READMEのどこからコピーするか |
|---|---|
| **API Name** | READMEの `# タイトル`（`Free` は外してもOK） |
| **Short Description** | READMEの `>` 引用部分（1行目） |
| **Long Description** | README全体から以下を結合: `## Why Choose...` + `## Use Cases` + `## Quick Start` のcURLサンプル1つ |
| **Category** | 下記のカテゴリ表を参照 |
| **Tags / Keywords** | 下記のタグ表を参照（最大10個） |

**Long Description のコピペテンプレ**:

```
[Why Choose... セクションの箇条書きをそのまま貼る]

Use Cases:
[Use Cases セクションの箇条書きをそのまま貼る]

Quick Start:
[cURLサンプル1つだけ貼る]
```

> RapidAPI の Description は Markdown 対応。READMEからそのままコピペでOK。

### ステップ3: Pricing タブ → 無料枠を増量

**全24 API共通の変更**:
- Basic (FREE) プランの `Requests per Month` を **500 → 1000** に変更
- Rate Limit はそのまま（2 req/sec）

**Tier 1（高需要6本）のみ追加**:
- Megaプラン追加: $99.99/mo, Unlimited, 500 req/sec

### ステップ4: Save & Publish

- 「Save」を押す
- Listing が「Published」になっていることを確認

---

## API別タグ・カテゴリ一覧

| # | API | Category | Tags（最大10個、カンマ区切り） |
|---|-----|----------|------|
| 01 | QR Code | Tools | qr code, qr generator, qr code api, png, svg, base64, barcode, cloudflare workers, free api, developer tools |
| 02 | Email Validation | Email | email validation, email verification, email checker, mx lookup, disposable email, typo detection, spam filter, deliverability, free api, saas |
| 03 | Link Preview | Data | link preview, open graph, og tags, url metadata, website preview, social media, unfurl, embed, free api, web scraping |
| 04 | Screenshot | Tools | website screenshot, screenshot api, webpage capture, png, jpeg, full page screenshot, thumbnail, cloudflare workers, free api, headless browser |
| 05 | Text Analysis | Text | text analysis, word count, readability, sentiment, keyword extraction, nlp, content analysis, flesch score, free api, writing tools |
| 06 | IP Geolocation | Data | ip geolocation, ip lookup, ip address, vpn detection, proxy detection, geoip, country lookup, fraud detection, cybersecurity, free api |
| 07 | URL Shortener | Tools | url shortener, short link, link shortener, tiny url, url redirect, link management, free api, cloudflare workers, developer tools, bitly alternative |
| 08 | JSON Formatter | Tools | json formatter, json validator, json beautifier, json minifier, json parser, json diff, developer tools, free api, data processing, cloudflare workers |
| 09 | Hash Encoding | Tools | hash, md5, sha256, sha512, encoding, base64, hex, hmac, encryption, free api |
| 10 | Currency Exchange | Finance | currency exchange, exchange rate, forex, currency converter, fiat, multi-currency, pricing, fintech, free api, real-time rates |
| 11 | AI Text | Artificial Intelligence/ML | ai text generation, chatgpt alternative, text rewriting, summarization, ai writing, content generation, nlp, free api, cloudflare workers ai, llm |
| 12 | Social Video | Media | social video download, video downloader, tiktok, instagram, youtube, twitter video, social media, video api, free api, content creator |
| 13 | Crypto Data | Finance | cryptocurrency, crypto price, bitcoin, ethereum, market data, crypto api, portfolio tracker, defi, free api, real-time data |
| 14 | SEO Analyzer | Tools | seo analyzer, seo audit, seo score, on-page seo, meta tags, structured data, lighthouse alternative, website analysis, free api, seo tools |
| 15 | Weather | Weather | weather api, weather forecast, current weather, temperature, humidity, weather data, free api, location weather, cloudflare workers, meteorology |
| 16 | WHOIS Domain | Data | whois, domain lookup, domain info, registrar, dns, domain expiry, domain availability, cybersecurity, free api, domain tools |
| 17 | News Aggregator | Media | news api, news aggregator, rss, headlines, news feed, current events, media, content aggregation, free api, real-time news |
| 18 | AI Translate | Translation | ai translation, language translation, translate api, multilingual, localization, i18n, cloudflare workers ai, free api, machine translation, deepl alternative |
| 19 | Trends | Data | trends, trending topics, google trends, social trends, trend analysis, market research, content ideas, free api, real-time trends, data analytics |
| 20 | Company Data | Business | company data, business info, company lookup, firmographic, enrichment, lead generation, b2b, crm, free api, business intelligence |
| 21 | WP Internal Link | Tools | wordpress, internal linking, seo, wp api, content optimization, anchor text, link building, wordpress seo, free api, blogging tools |
| 22 | PDF Generator | Tools | pdf generator, html to pdf, pdf api, document generation, invoice pdf, report generator, free api, cloudflare workers, developer tools, pdf converter |
| 23 | Placeholder Image | Tools | placeholder image, dummy image, image generator, placeholder api, mockup, wireframe, design tools, free api, developer tools, lorem picsum |
| 24 | Markdown Converter | Tools | markdown converter, markdown to html, html to markdown, md parser, documentation, free api, developer tools, cloudflare workers, text processing, static site |

---

## 進捗トラッキング

更新したらチェックを入れる:

### Phase 1（高需要）
- [ ] 06 - IP Geolocation API
- [ ] 04 - Screenshot API
- [ ] 01 - QR Code API
- [ ] 02 - Email Validation API
- [ ] 10 - Currency Exchange API
- [ ] 14 - SEO Analyzer API

### Phase 2（中需要）
- [ ] 07 - URL Shortener API
- [ ] 22 - PDF Generator API
- [ ] 12 - Social Video API
- [ ] 13 - Crypto Data API
- [ ] 11 - AI Text API
- [ ] 18 - AI Translate API
- [ ] 16 - WHOIS Domain API

### Phase 3（ユーティリティ）
- [ ] 03 - Link Preview API
- [ ] 05 - Text Analysis API
- [ ] 08 - JSON Formatter API
- [ ] 09 - Hash Encoding API
- [ ] 15 - Weather API
- [ ] 17 - News Aggregator API
- [ ] 19 - Trends API
- [ ] 20 - Company Data API
- [ ] 21 - WP Internal Link API
- [ ] 23 - Placeholder Image API
- [ ] 24 - Markdown Converter API

---

## 注意事項

- READMEの `Free tier: 500 requests/month` の表記は **1000に書き換え不要**（RapidAPI Studio側で制御されるため）
- Long Description に競合サービス名（Ahrefs, ZeroBounce等）を入れると審査で弾かれる可能性あり。入れない方が安全
- Tags は検索順位に直結する。汎用的なタグ（`free api`, `developer tools`）は全APIに入れること
- 更新後、各APIの検索順位変動を1週間モニタリングする
