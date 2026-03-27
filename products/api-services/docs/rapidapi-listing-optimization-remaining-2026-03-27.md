# RapidAPI リスティング最適化 — 残り19本（2026-03-27）

> 上位5本（SEO Analyzer, Email Validation, Screenshot, QR Code, WHOIS）は `rapidapi-listing-optimization-2026-03-26.md` で最適化済み。
> 本ドキュメントは残り全APIのリスティングを網羅する。

---

## 3. Link Preview API

### API Name

```
Link Preview API - URL Metadata & OG Tags Extractor (Unfurl Alternative)
```

### Short Description

```
Extract title, description, OG image, favicon & social tags from any URL. Bulk support (10 URLs/request). 1-hour edge cache. Free 500/mo. Unfurl/LinkPreview alternative at 1/10th cost.
```

### Tags

```
link-preview, og-tags, open-graph, url-metadata, unfurl, social-share, meta-tags, favicon, web-scraping, embed
```

### Long Description

```
## Extract Rich Link Previews from Any URL — Like Slack, Discord & Twitter

One API call returns title, description, OG image, favicon, Twitter Card tags, and more. Build link previews for chat apps, CMS, social dashboards, or email builders without maintaining your own scraping infrastructure.

### What Every Response Includes

- Page title & description
- Open Graph tags (og:title, og:image, og:description, og:type, og:site_name)
- Twitter Card tags (twitter:card, twitter:image, twitter:title)
- Favicon URL
- Canonical URL
- Response time (ms)

### Why Developers Choose This API

| | This API | LinkPreview.net | Microlink | Iframely |
|---|---|---|---|---|
| Free tier | **500/mo** | 60/mo | 50/day | None |
| Bulk preview | **10 URLs/request** | 1 | 1 | 1 |
| Edge cache | **1-hour** | None | None | Varies |
| Latency | <200ms (cached) | 500ms+ | 300ms+ | 500ms+ |

### 2 Endpoints

- `GET /preview?url=<url>` — Single URL metadata extraction
- `POST /preview/bulk` — Batch up to 10 URLs in one request

### Use Cases

- **Chat apps**: Rich link unfurling (Slack-style previews)
- **CMS/Blog platforms**: Auto-generate social share cards
- **SEO tools**: Audit OG tags across multiple pages
- **Email builders**: Preview links before sending campaigns
- **Social media dashboards**: Display link metadata in feeds
- **Bookmark managers**: Auto-populate link details

### Quick Start

```
GET /preview?url=https://github.com
→ {"title": "GitHub", "description": "...", "image": "https://...", "favicon": "..."}
```

### Bulk Preview

```
POST /preview/bulk
{"urls": ["https://github.com", "https://dev.to"]}
→ {"results": [...], "total": 2}
```

Free tier: 500 previews/month. No credit card required.
```

### Pricing

```
Basic (Free):    500 req/mo,   1 req/sec  — $0
Pro:           50,000 req/mo,  10 req/sec — $5.99/mo
Ultra:        500,000 req/mo,  50 req/sec — $14.99/mo
Mega:       2,000,000 req/mo, 100 req/sec — $49.99/mo
```

---

## 5. Text Analysis API

### API Name

```
Text Analysis API - Sentiment, Keywords, Readability & Summary (NLP Toolkit)
```

### Short Description

```
All-in-one NLP: sentiment analysis, keyword extraction, readability scoring (Flesch-Kincaid), language detection (40+), text summarization. Free 500/mo. No ML model costs — runs on Cloudflare Edge.
```

### Tags

```
text-analysis, sentiment-analysis, keyword-extraction, readability, nlp, language-detection, text-summarization, content-analysis, flesch-kincaid, developer-tools
```

### Long Description

```
## Complete NLP Toolkit in One API — Sentiment, Keywords, Readability & More

Analyze any text with 7 NLP features in a single API call. No ML model hosting costs — all algorithms run natively on Cloudflare Workers for sub-100ms latency.

### 7 Endpoints

1. **`POST /analyze`** — Full analysis: word count, readability, sentiment, language, keywords, summary
2. **`POST /sentiment`** — Sentiment score (-1 to +1) with label (positive/negative/neutral)
3. **`POST /keywords`** — TF-IDF keyword extraction (top N configurable)
4. **`POST /readability`** — Flesch-Kincaid, Gunning Fog, Coleman-Liau, ARI scores
5. **`POST /language`** — Language detection (40+ languages supported)
6. **`POST /summarize`** — TextRank extractive summarization (configurable sentence count)
7. **`POST /stats`** — Word/character/sentence/paragraph counts, reading & speaking time

### Cost Comparison

| | This API | MonkeyLearn | IBM Watson NLU | Google NLP |
|---|---|---|---|---|
| 500 analyses/mo | **FREE** | $299+/mo | Pay-per-use | Pay-per-use |
| 50K analyses/mo | **$9.99** | $299+/mo | ~$50+ | ~$25+ |
| No ML model costs | **Yes** | No | No | No |
| Latency | <100ms | 200-500ms | 300-600ms | 200-400ms |

### Use Cases

- **Content teams**: Pre-publish readability & SEO keyword check
- **SaaS products**: Add text analytics features without ML infrastructure
- **Customer support**: Sentiment analysis on tickets & reviews
- **Education**: Readability scoring for learning materials
- **Research**: Bulk text analysis for academic papers
- **Marketing**: Campaign copy optimization

### Quick Start

```
POST /analyze
{"text": "This API is incredibly fast and affordable for developers building NLP features."}
→ {"word_count": 12, "sentiment": {"score": 0.8, "label": "positive"}, "readability": {"flesch_kincaid_grade": 8.2}, ...}
```

Free tier: 500 analyses/month. No credit card required.
```

### Pricing

```
Basic (Free):    500 req/mo,   1 req/sec  — $0
Pro:           50,000 req/mo,  10 req/sec — $9.99/mo
Ultra:        500,000 req/mo,  50 req/sec — $24.99/mo
Mega:       2,000,000 req/mo, 100 req/sec — $49.99/mo
```

---

## 6. IP Geolocation API

### API Name

```
IP Geolocation API - IP to Location, ISP & Proxy Detection (Free)
```

### Short Description

```
Look up any IP: country, city, lat/lon, timezone, ISP, proxy/VPN/datacenter detection. Bulk support (20 IPs). Auto-detect with /me endpoint. Free 500/mo. IPinfo alternative at 1/20th cost.
```

### Tags

```
ip-geolocation, ip-lookup, geolocation, ip-address, proxy-detection, vpn-detection, ipinfo-alternative, ip-to-location, fraud-detection, geoip
```

### Long Description

```
## IP Geolocation & Threat Detection — IPinfo Alternative at 1/20th the Cost

Get country, city, coordinates, timezone, ISP, and proxy/VPN/datacenter flags for any IP address. 24-hour edge cache for instant repeat lookups.

### 3 Endpoints

1. **`GET /lookup?ip=<ip>`** — Full geolocation for any IPv4/IPv6 address
2. **`GET /me`** — Auto-detect caller's IP and return geolocation (zero config)
3. **`POST /bulk`** — Batch lookup up to 20 IPs in one request

### Every Response Includes

- Country (code + name), region, city
- Latitude & longitude
- Timezone
- ISP / organization
- Proxy, VPN, datacenter flags
- ASN & Cloudflare colo (for /me)

### Cost Comparison

| | This API | IPinfo | IPGeolocation.io | ip-api.com |
|---|---|---|---|---|
| Free tier | **500/mo** | 50K/mo (limited) | 1K/day | 45/min (no API key) |
| Full lookup | **$5.99/50K** | $99+/mo | $15+/mo | No bulk tier |
| Proxy detection | **Included** | $99+/mo extra | Extra tier | Included (limited) |
| Bulk endpoint | **20 IPs/req** | 1 | Batch API extra | N/A |

### Use Cases

- **Fraud prevention**: Detect proxies, VPNs, and datacenter IPs at signup
- **Geo-targeting**: Customize content, currency, and language by visitor location
- **Analytics**: Enrich server logs with geographic data
- **Compliance**: Geo-restriction enforcement (GDPR, sanctions)
- **Security**: Identify suspicious traffic origins
- **Ad tech**: Location-based ad targeting

### Quick Start

```
GET /lookup?ip=8.8.8.8
→ {"ip": "8.8.8.8", "country": "US", "city": "Mountain View", "isp": "Google LLC", "is_proxy": false, ...}
```

```
GET /me
→ {"ip": "your.ip.here", "country": "JP", "city": "Tokyo", ...}
```

Free tier: 500 lookups/month. No credit card required.
```

### Pricing

```
Basic (Free):    500 req/mo,   1 req/sec  — $0
Pro:           50,000 req/mo,  10 req/sec — $5.99/mo
Ultra:        500,000 req/mo,  50 req/sec — $14.99/mo
Mega:       2,000,000 req/mo, 100 req/sec — $49.99/mo
```

---

## 7. URL Shortener API

### API Name

```
URL Shortener API - Shorten, Track Clicks & Custom Aliases (Free)
```

### Short Description

```
Shorten URLs with custom aliases, track clicks, and manage links via API. Click analytics with timestamps. KV-powered persistence. Free 500/mo. Bitly API alternative at 1/10th cost.
```

### Tags

```
url-shortener, short-url, link-shortener, bitly-alternative, click-tracking, custom-alias, link-analytics, redirect, link-management, marketing-tools
```

### Long Description

```
## Programmable URL Shortener with Click Tracking — Bitly API Alternative

Create short URLs, use custom aliases, and track click analytics — all via a simple REST API. Powered by Cloudflare KV for persistent storage and global edge delivery.

### 4 Endpoints

1. **`POST /shorten`** — Create a short URL (auto-generated or custom alias)
2. **`GET /r/:alias`** — Redirect to original URL (302)
3. **`GET /stats/:alias`** — Get click count, creation date, last clicked timestamp
4. **`DELETE /delete/:alias`** — Remove a short URL

### Features

- **Custom aliases**: Choose your own slug (1-64 chars, alphanumeric + hyphens)
- **Click tracking**: Total clicks + last clicked timestamp
- **Persistent storage**: Cloudflare KV — links don't expire
- **Fast redirects**: Global edge network, <50ms redirect latency
- **Conflict detection**: 409 error if alias already taken

### Cost Comparison

| | This API | Bitly API | TinyURL API | Rebrandly |
|---|---|---|---|---|
| Free tier | **500/mo** | 50 links | None | 500 links (no API) |
| 50K links/mo | **$5.99** | $29+/mo | N/A | $69+/mo |
| Click analytics | **Included** | $29+/mo | None | $69+/mo |
| Custom aliases | **Included** | $29+/mo | Premium only | $69+/mo |

### Use Cases

- **Marketing**: Branded short links for campaigns and social posts
- **SaaS products**: Shareable links within your app
- **Affiliate marketing**: Track click-through rates
- **Email marketing**: Short URLs that fit in SMS/email
- **QR codes**: Short URLs pair well with QR code generation
- **Analytics dashboards**: Monitor link performance

### Quick Start

```
POST /shorten
{"url": "https://example.com/very/long/path?param=value", "custom_alias": "my-link"}
→ {"short_url": "https://url-shortener-api.../r/my-link", "alias": "my-link", "clicks": 0}
```

```
GET /stats/my-link
→ {"alias": "my-link", "original_url": "https://...", "clicks": 42, "last_clicked": "2026-03-27T..."}
```

Free tier: 500 requests/month. No credit card required.
```

### Pricing

```
Basic (Free):    500 req/mo,   1 req/sec  — $0
Pro:           50,000 req/mo,  10 req/sec — $5.99/mo
Ultra:        500,000 req/mo,  50 req/sec — $14.99/mo
Mega:       2,000,000 req/mo, 100 req/sec — $49.99/mo
```

---

## 8. JSON Formatter API

### API Name

```
JSON Formatter API - Validate, Format, Diff, CSV Convert & Transform
```

### Short Description

```
Format, minify, validate, diff, flatten/unflatten & convert JSON↔CSV. Stats (depth, key count, size). Free 500/mo. The Swiss Army Knife for JSON — one API, 8 operations.
```

### Tags

```
json-formatter, json-validator, json-diff, json-to-csv, csv-to-json, json-minify, json-transform, json-flatten, developer-tools, data-conversion
```

### Long Description

```
## The Swiss Army Knife for JSON — 8 Operations in One API

Format, minify, validate, diff, transform, flatten/unflatten, and convert between JSON and CSV. Perfect for data pipelines, developer tools, and SaaS products.

### 8 Endpoints

1. **`POST /format`** — Pretty-print with configurable indent
2. **`POST /minify`** — Remove all whitespace
3. **`POST /validate`** — Validate JSON with error position + stats (depth, keys, size)
4. **`POST /diff`** — Deep diff between two JSON objects (added/removed/changed paths)
5. **`POST /transform`** — Flatten, unflatten, sort keys, pick/omit fields, rename keys
6. **`POST /csv-to-json`** — Convert CSV string to JSON array
7. **`POST /json-to-csv`** — Convert JSON array to CSV string
8. **`POST /stats`** — Key count, max depth, size in bytes

### Why Use an API Instead of npm Packages?

- **No dependencies**: Zero `node_modules` bloat
- **Language-agnostic**: Works from Python, Ruby, Go, PHP — not just JavaScript
- **CI/CD pipelines**: Validate JSON configs in GitHub Actions without installing tools
- **Serverless functions**: Keep cold start times low

### Use Cases

- **CI/CD**: Validate `package.json`, `tsconfig.json`, Terraform configs pre-deploy
- **Data pipelines**: JSON↔CSV conversion for ETL workflows
- **Developer tools**: Build online JSON formatters/validators
- **API testing**: Diff expected vs actual JSON responses
- **Database migration**: Transform/flatten nested JSON before import
- **Content management**: Bulk transform CMS data exports

### Quick Start

```
POST /validate
{"data": "{\"name\": \"test\", \"value\": 42}"}
→ {"valid": true, "stats": {"keys": 2, "depth": 1, "size_bytes": 28}}
```

```
POST /diff
{"a": {"name": "v1"}, "b": {"name": "v2", "added": true}}
→ {"equal": false, "total_differences": 2, "differences": [...]}
```

Free tier: 500 operations/month. No credit card required.
```

### Pricing

```
Basic (Free):    500 req/mo,   1 req/sec  — $0
Pro:           50,000 req/mo,  10 req/sec — $5.99/mo
Ultra:        500,000 req/mo,  50 req/sec — $14.99/mo
Mega:       2,000,000 req/mo, 100 req/sec — $49.99/mo
```

---

## 9. Hash & Encoding API

### API Name

```
Hash & Encoding API - SHA256, MD5, HMAC, Bcrypt, Base64 & UUID Generator
```

### Short Description

```
Hash (SHA-1/256/384/512, MD5), HMAC, bcrypt, Base64/hex/URL encode-decode, UUID v4 generation. File hashing via Base64 upload. Free 500/mo. One API for all cryptographic utilities.
```

### Tags

```
hash, sha256, md5, hmac, bcrypt, base64, encoding, uuid-generator, cryptography, developer-tools
```

### Long Description

```
## All Cryptographic Utilities in One API — Hash, Encode, Sign & Generate

Stop installing 5 different npm packages for hashing, encoding, and token generation. One API covers SHA-256, MD5, HMAC, bcrypt, Base64, URL encoding, and UUID generation.

### 8 Endpoints

1. **`POST /hash`** — Hash text with SHA-1, SHA-256, SHA-384, SHA-512, or MD5
2. **`POST /hash/file`** — Hash file content (Base64 encoded)
3. **`POST /hmac`** — HMAC signature (SHA-1/256/384/512 + secret key)
4. **`POST /bcrypt/hash`** — Bcrypt password hashing (configurable rounds)
5. **`POST /bcrypt/verify`** — Verify password against bcrypt hash
6. **`POST /encode`** — Encode/decode: Base64, hex, URL encoding
7. **`GET /uuid`** — Generate UUID v4
8. **`POST /uuid/batch`** — Generate multiple UUIDs (up to 100)

### Output Format

Every hash/encode endpoint returns both `hex` and `base64` representations — no need for separate conversion calls.

### Use Cases

- **Authentication**: Bcrypt password hashing & verification
- **Webhooks**: HMAC signature verification (Stripe, GitHub, Shopify)
- **File integrity**: SHA-256 checksums for uploads/downloads
- **API development**: Generate UUIDs for database IDs
- **Data pipelines**: Base64/URL encode payloads
- **Security auditing**: Verify password hash strength

### Quick Start

```
POST /hash
{"text": "Hello World", "algorithm": "sha256"}
→ {"algorithm": "sha256", "hex": "a591a6d40...", "base64": "pZGm1A..."}
```

```
POST /bcrypt/hash
{"password": "my-secret-password", "rounds": 12}
→ {"hash": "$2b$12$...", "rounds": 12}
```

Free tier: 500 operations/month. No credit card required.
```

### Pricing

```
Basic (Free):    500 req/mo,   1 req/sec  — $0
Pro:           50,000 req/mo,  10 req/sec — $5.99/mo
Ultra:        500,000 req/mo,  50 req/sec — $14.99/mo
Mega:       2,000,000 req/mo, 100 req/sec — $49.99/mo
```

---

## 10. Currency Exchange API

### API Name

```
Currency Exchange API - Real-Time Rates & Converter (ECB Data, Free)
```

### Short Description

```
Real-time exchange rates from ECB (Frankfurter). Convert between 30+ currencies. Historical rates by date. 1-hour edge cache. Free 500/mo. Fixer.io alternative — no upstream API key costs.
```

### Tags

```
currency-exchange, exchange-rates, currency-converter, forex, ecb-rates, fixer-alternative, real-time-rates, financial-data, currency-api, money-conversion
```

### Long Description

```
## Real-Time Currency Exchange Rates — Powered by ECB, Zero Upstream Costs

Get live exchange rates for 30+ currencies sourced from the European Central Bank via Frankfurter API. Convert amounts, fetch historical rates, and list all supported currencies.

### 4 Endpoints

1. **`GET /rates?base=USD`** — Latest rates for all currencies (base configurable)
2. **`GET /convert?from=USD&to=EUR&amount=100`** — Convert amount between currencies
3. **`GET /historical?base=USD&date=2026-01-15`** — Historical rates for a specific date
4. **`GET /currencies`** — List all supported currency codes

### Cost Comparison

| | This API | Fixer.io | ExchangeRate-API | CurrencyLayer |
|---|---|---|---|---|
| Free tier | **500/mo** | 100/mo | 1,500/mo | 100/mo |
| 50K calls/mo | **$5.99** | $9.99+ | $9.99+ | $9.99+ |
| No API key costs | **Yes** | No | No | No |
| ECB source | **Yes** | Yes | Mixed | Mixed |

### Use Cases

- **E-commerce**: Display prices in visitor's local currency
- **Fintech apps**: Currency conversion in banking/payment apps
- **Accounting software**: Multi-currency invoicing
- **Travel apps**: Real-time exchange rates for travelers
- **SaaS pricing**: Dynamic pricing by region
- **Data analysis**: Historical exchange rate trends

### Quick Start

```
GET /convert?from=USD&to=JPY&amount=100
→ {"from": "USD", "to": "JPY", "amount": 100, "rate": 149.52, "result": 14952, "date": "2026-03-27"}
```

```
GET /rates?base=EUR
→ {"base": "EUR", "date": "2026-03-27", "rates": {"USD": 1.08, "JPY": 161.5, ...}}
```

Free tier: 500 requests/month. No credit card required.
```

### Pricing

```
Basic (Free):    500 req/mo,   1 req/sec  — $0
Pro:           50,000 req/mo,  10 req/sec — $5.99/mo
Ultra:        500,000 req/mo,  50 req/sec — $14.99/mo
Mega:       2,000,000 req/mo, 100 req/sec — $49.99/mo
```

---

## 11. AI Text API

### API Name

```
AI Text API - Generate, Summarize, Translate & Analyze with Llama 3.1 (Free)
```

### Short Description

```
AI-powered text generation, summarization, translation, sentiment analysis & grammar check. Llama 3.1 8B on Cloudflare Workers AI. Free 500/mo. No OpenAI API key needed — zero infrastructure cost.
```

### Tags

```
ai-text, text-generation, summarization, translation, sentiment-analysis, llama, workers-ai, openai-alternative, nlp, content-generation
```

### Long Description

```
## AI Text Processing Powered by Llama 3.1 — No API Key Costs

Generate, summarize, translate, and analyze text using Meta's Llama 3.1 8B model running natively on Cloudflare Workers AI. No OpenAI API key, no per-token billing surprises.

### 5 Endpoints

1. **`POST /generate`** — Generate text from a prompt (configurable max_tokens & temperature)
2. **`POST /summarize`** — Summarize long text into a concise version
3. **`POST /translate`** — Translate text between languages (auto-detect source)
4. **`POST /sentiment`** — Sentiment analysis with score & label
5. **`POST /grammar`** — Grammar correction with explanations

### Why This API Over OpenAI/Claude?

| | This API | OpenAI GPT-4 | Claude API | Cohere |
|---|---|---|---|---|
| Free tier | **500/mo** | None (pay-per-token) | None | 5/min |
| 50K calls/mo | **$9.99 flat** | ~$50-500+ | ~$50-500+ | $35+ |
| Pricing model | **Flat rate** | Per token | Per token | Per token |
| Model hosting | **Included** | Included | Included | Included |
| Use case | Utility text tasks | Complex reasoning | Complex reasoning | Text tasks |

> Best for: Bulk utility tasks (summarization, translation, sentiment) where Llama 3.1 8B quality is sufficient. Not a replacement for GPT-4 on complex reasoning tasks.

### Use Cases

- **Content marketing**: Generate blog outlines, social captions, ad copy
- **SaaS products**: Add AI text features without managing models
- **Customer support**: Auto-summarize ticket threads
- **Localization**: Quick draft translations for 40+ languages
- **E-commerce**: Generate product descriptions from specs
- **Education**: Summarize articles for students

### Quick Start

```
POST /generate
{"prompt": "Write 3 taglines for a coffee shop", "max_tokens": 200}
→ {"result": "1. Wake up to perfection...", "model": "@cf/meta/llama-3.1-8b-instruct"}
```

```
POST /summarize
{"text": "Long article text here...", "max_length": 100}
→ {"result": "Concise summary...", "original_length": 2500}
```

Free tier: 500 requests/month. No credit card required.
```

### Pricing

```
Basic (Free):    500 req/mo,   1 req/sec  — $0
Pro:           50,000 req/mo,  10 req/sec — $9.99/mo
Ultra:        500,000 req/mo,  50 req/sec — $24.99/mo
Mega:       2,000,000 req/mo, 100 req/sec — $49.99/mo
```

---

## 12. Social Video API

### API Name

```
Social Video API - Download Videos from TikTok, Twitter, Instagram & More
```

### Short Description

```
Extract video download URLs from TikTok, Twitter/X, Instagram, Reddit, YouTube & more. Metadata included (title, author, duration). Free 500/mo. No auth tokens needed — works via public page parsing.
```

### Tags

```
social-video, video-downloader, tiktok-downloader, twitter-video, instagram-video, youtube-download, video-metadata, social-media, content-scraping, video-extraction
```

### Long Description

```
## Download Social Media Videos via API — TikTok, Twitter/X, Instagram & More

Extract direct video download URLs and metadata from social media platforms. No OAuth tokens, no API keys for upstream services — works by parsing public HTML pages.

### 3 Endpoints

1. **`GET /download?url=<video_url>`** — Extract video download URL + metadata
2. **`GET /info?url=<video_url>`** — Get video metadata only (title, author, duration) — no download URL
3. **`GET /platforms`** — List all supported platforms

### Supported Platforms

- TikTok
- Twitter / X
- Instagram (public posts)
- Reddit (v.redd.it)
- YouTube (public videos)
- And more — check `/platforms` for the full list

### Use Cases

- **Content aggregators**: Build cross-platform video feeds
- **Social media tools**: Video archiving and backup
- **Analytics platforms**: Track video metadata across platforms
- **Content creators**: Download your own videos for repurposing
- **Research**: Collect video metadata for analysis
- **Digital marketing**: Monitor competitor video content

### Quick Start

```
GET /download?url=https://twitter.com/user/status/123456
→ {"success": true, "platform": "twitter", "video_url": "https://...", "title": "...", "author": "..."}
```

```
GET /info?url=https://www.tiktok.com/@user/video/123
→ {"success": true, "platform": "tiktok", "title": "...", "author": "...", "duration": 30}
```

Free tier: 500 requests/month. No credit card required.
```

### Pricing

```
Basic (Free):    500 req/mo,   1 req/sec  — $0
Pro:           50,000 req/mo,  10 req/sec — $9.99/mo
Ultra:        500,000 req/mo,  50 req/sec — $24.99/mo
Mega:       2,000,000 req/mo, 100 req/sec — $49.99/mo
```

---

## 13. Crypto Data API

### API Name

```
Crypto Data API - Live Prices, Market Data, Trending & History (CoinGecko Alternative)
```

### Short Description

```
Live crypto prices, market cap rankings, trending coins, historical data & exchange info. 10K+ coins supported. Free 500/mo. CoinGecko/CoinMarketCap alternative — no upstream API key costs.
```

### Tags

```
crypto, cryptocurrency, bitcoin, ethereum, crypto-prices, market-data, coingecko-alternative, trading, defi, blockchain
```

### Long Description

```
## Cryptocurrency Market Data API — CoinGecko Alternative at Zero Upstream Cost

Access live prices, market rankings, trending coins, historical data, exchange information, and global market stats for 10,000+ cryptocurrencies. Powered by CoinCap API — no upstream API key required.

### 8 Endpoints

1. **`GET /price?ids=bitcoin,ethereum&vs=usd`** — Current prices for multiple coins
2. **`GET /coin/:id`** — Detailed coin info (price, market cap, volume, supply, rank)
3. **`GET /search?q=<query>`** — Search coins by name or symbol
4. **`GET /trending`** — Top trending coins right now
5. **`GET /markets?per_page=100&page=1`** — Market listings with pagination
6. **`GET /history?id=bitcoin&date=2026-01-01`** — Historical price on a specific date
7. **`GET /exchanges`** — List top exchanges
8. **`GET /global`** — Global market stats (total market cap, BTC dominance, etc.)

### Cost Comparison

| | This API | CoinGecko API | CoinMarketCap | CryptoCompare |
|---|---|---|---|---|
| Free tier | **500/mo** | 10K/mo (limited) | 10K/mo | 100K/mo |
| Pro tier | **$5.99/50K** | $129+/mo | $29+/mo | $19+/mo |
| No API key costs | **Yes** | No | No | No |
| Rate limit | 30/min | 10-30/min | 30/min | 100K/mo |

### Use Cases

- **Trading bots**: Real-time price feeds for automated trading
- **Portfolio trackers**: Display holdings value in real time
- **Fintech apps**: Crypto market data in banking/investment apps
- **Analytics dashboards**: Market cap rankings and trends
- **Price alerts**: Monitor price changes with periodic polling
- **Research**: Historical price analysis

### Quick Start

```
GET /price?ids=bitcoin,ethereum&vs=usd
→ {"bitcoin": {"usd": 67234.50}, "ethereum": {"usd": 3456.78}}
```

```
GET /trending
→ {"coins": [{"id": "bitcoin", "name": "Bitcoin", "symbol": "BTC", "rank": 1}, ...]}
```

Free tier: 500 requests/month. No credit card required.
```

### Pricing

```
Basic (Free):    500 req/mo,   1 req/sec  — $0
Pro:           50,000 req/mo,  10 req/sec — $5.99/mo
Ultra:        500,000 req/mo,  50 req/sec — $14.99/mo
Mega:       2,000,000 req/mo, 100 req/sec — $49.99/mo
```

---

## 15. Weather API

### API Name

```
Weather API - Current, Forecast, Hourly & Historical Weather Data (Free)
```

### Short Description

```
Current weather, 7-day forecast, hourly forecast & historical data by coordinates. Open-Meteo powered — no API key costs. WMO weather codes decoded. Free 500/mo. OpenWeatherMap alternative.
```

### Tags

```
weather, weather-api, forecast, current-weather, historical-weather, open-meteo, openweathermap-alternative, temperature, hourly-forecast, geocoding
```

### Long Description

```
## Weather Data API — Current, Forecast & Historical (OpenWeatherMap Alternative)

Get current conditions, 7-day daily forecast, 48-hour hourly forecast, and historical weather data for any location by latitude/longitude. Powered by Open-Meteo — zero upstream API costs.

### 5 Endpoints

1. **`GET /current?lat=35.68&lon=139.76`** — Current temperature, humidity, wind, weather code
2. **`GET /forecast?lat=35.68&lon=139.76`** — 7-day daily forecast (high/low, precipitation, wind)
3. **`GET /hourly?lat=35.68&lon=139.76`** — 48-hour hourly forecast
4. **`GET /history?lat=35.68&lon=139.76&date=2026-01-15`** — Historical weather for a specific date
5. **`GET /geocode?city=Tokyo`** — City name to coordinates lookup

### Every Response Includes

- Temperature (celsius)
- Humidity, wind speed
- WMO weather code with human-readable description (e.g., "Partly cloudy")
- is_day flag for day/night distinction
- Timezone-aware timestamps

### Cost Comparison

| | This API | OpenWeatherMap | WeatherAPI | Visual Crossing |
|---|---|---|---|---|
| Free tier | **500/mo** | 1K/day | 1M/mo | 1K/day |
| 50K calls/mo | **$5.99** | $0 (limited) | $4+/mo | $0 (limited) |
| No API key costs | **Yes** | No | No | No |
| Historical data | **Included** | $0 (30 day limit) | Paid only | Included |

### Use Cases

- **Travel apps**: Weather at destination
- **Agriculture**: Crop planning with forecast data
- **Event planning**: Weather outlook for outdoor events
- **IoT dashboards**: Display current conditions
- **Logistics**: Weather-based route planning
- **Content personalization**: Weather-aware UI/UX

### Quick Start

```
GET /current?lat=35.68&lon=139.76
→ {"temperature": 22.5, "humidity": 65, "wind_speed": 12.3, "weather": "Partly cloudy", "is_day": true}
```

```
GET /forecast?lat=35.68&lon=139.76
→ {"daily": [{"date": "2026-03-27", "temp_max": 25, "temp_min": 18, "weather": "Clear sky"}, ...]}
```

Free tier: 500 requests/month. No credit card required.
```

### Pricing

```
Basic (Free):    500 req/mo,   1 req/sec  — $0
Pro:           50,000 req/mo,  10 req/sec — $5.99/mo
Ultra:        500,000 req/mo,  50 req/sec — $14.99/mo
Mega:       2,000,000 req/mo, 100 req/sec — $49.99/mo
```

---

## 17. News Aggregator API

### API Name

```
News Aggregator API - RSS, Hacker News & Dev.to Feed in One Endpoint
```

### Short Description

```
Aggregated tech & business news from RSS feeds, Hacker News & Dev.to. Search, filter by category (tech/business/top). Free 500/mo. No NewsAPI key needed — multi-source aggregation built in.
```

### Tags

```
news, news-aggregator, rss, hacker-news, devto, tech-news, business-news, news-feed, content-aggregation, newsapi-alternative
```

### Long Description

```
## Multi-Source News Aggregator — RSS + Hacker News + Dev.to in One API

Get curated news from multiple free sources in a single, normalized JSON format. No upstream API keys, no NewsAPI subscription — everything aggregated from public RSS feeds, Hacker News Firebase API, and Dev.to API.

### 6 Endpoints

1. **`GET /top`** — Top headlines from curated RSS feeds
2. **`GET /tech`** — Technology news (TechCrunch, Ars Technica, The Verge, etc.)
3. **`GET /business`** — Business & finance news
4. **`GET /search?q=<query>`** — Search across all sources
5. **`GET /hackernews/top`** — Hacker News top stories (25 stories with scores & comments)
6. **`GET /devto/latest`** — Latest Dev.to articles with reactions & tags

### Why This Over NewsAPI?

| | This API | NewsAPI | GNews | Bing News |
|---|---|---|---|---|
| Free tier | **500/mo** | 100/day (dev only) | 100/day | 1K/mo |
| Production use | **$5.99/50K** | $449+/mo | $84+/mo | $3/1K txn |
| No API key costs | **Yes** | No | No | No |
| Hacker News | **Built in** | No | No | No |
| Dev.to | **Built in** | No | No | No |

### Use Cases

- **Developer dashboards**: Curated tech news feeds
- **Slack/Discord bots**: Daily news digest
- **Content curation**: Auto-populate news sections in apps
- **Research**: Monitor industry trends
- **Newsletter automation**: Source articles for email newsletters
- **Portfolio sites**: Display latest tech news in sidebar

### Quick Start

```
GET /tech
→ {"source": "tech", "items": [{"title": "...", "url": "...", "description": "...", "publishedAt": "..."}, ...]}
```

```
GET /hackernews/top
→ {"items": [{"title": "...", "url": "...", "score": 342, "comments": 128, "by": "..."}, ...]}
```

Free tier: 500 requests/month. No credit card required.
```

### Pricing

```
Basic (Free):    500 req/mo,   1 req/sec  — $0
Pro:           50,000 req/mo,  10 req/sec — $5.99/mo
Ultra:        500,000 req/mo,  50 req/sec — $14.99/mo
Mega:       2,000,000 req/mo, 100 req/sec — $49.99/mo
```

---

## 18. AI Translate API

### API Name

```
AI Translate API - 40+ Languages with AI Detection (M2M-100, Free)
```

### Short Description

```
Translate text between 40+ languages using Meta's M2M-100 1.2B model on Cloudflare Workers AI. Language detection, batch translation (10/request). Free 500/mo. Google Translate API alternative.
```

### Tags

```
translation, ai-translate, language-detection, m2m100, multilingual, google-translate-alternative, batch-translation, workers-ai, localization, i18n
```

### Long Description

```
## AI-Powered Translation for 40+ Languages — Google Translate API Alternative

Translate text between 40+ language pairs using Meta's M2M-100 1.2B model running on Cloudflare Workers AI. No Google Cloud billing, no per-character charges.

### 4 Endpoints

1. **`POST /translate`** — Translate text (source_lang + target_lang required)
2. **`POST /detect`** — Detect language with confidence score (powered by Llama 3.1)
3. **`POST /batch`** — Batch translate up to 10 texts in one request
4. **`GET /languages`** — List all 40+ supported language codes

### Supported Languages

English, Spanish, French, German, Italian, Portuguese, Dutch, Polish, Russian, Chinese, Japanese, Korean, Arabic, Hindi, Turkish, Vietnamese, Thai, Indonesian, Czech, Romanian, Danish, Finnish, Hungarian, Norwegian, Swedish, Ukrainian, Bulgarian, Greek, Croatian, Slovak, Slovenian, Serbian, Lithuanian, Latvian, Estonian, Maltese, Irish, Welsh, Afrikaans, Swahili, Hausa, Igbo, Yoruba, Zulu

### Cost Comparison

| | This API | Google Translate | DeepL API | Azure Translator |
|---|---|---|---|---|
| Free tier | **500/mo** | 500K chars/mo | 500K chars/mo | 2M chars/mo |
| Pricing model | **Flat rate** | Per character | Per character | Per character |
| 50K translations | **$9.99** | ~$10-50 | ~$25+ | ~$10-50 |
| Batch support | **10/request** | 128 | 50 | 25 |

### Use Cases

- **SaaS localization**: Translate UI strings for international users
- **Content platforms**: Auto-translate user-generated content
- **E-commerce**: Translate product descriptions for global markets
- **Customer support**: Translate incoming tickets from any language
- **Social media tools**: Translate posts for cross-language analytics
- **Education**: Language learning apps

### Quick Start

```
POST /translate
{"text": "Hello, how are you?", "source_lang": "en", "target_lang": "ja"}
→ {"translated_text": "こんにちは、お元気ですか？", "source_lang": "en", "target_lang": "ja"}
```

```
POST /detect
{"text": "Bonjour le monde"}
→ {"detected_language": "fr", "confidence": 0.95}
```

Free tier: 500 translations/month. No credit card required.
```

### Pricing

```
Basic (Free):    500 req/mo,   1 req/sec  — $0
Pro:           50,000 req/mo,  10 req/sec — $9.99/mo
Ultra:        500,000 req/mo,  50 req/sec — $24.99/mo
Mega:       2,000,000 req/mo, 100 req/sec — $49.99/mo
```

---

## 19. Trends API

### API Name

```
Trends API - Google Trends, Hacker News & Dev.to Trending Topics (Free)
```

### Short Description

```
Trending topics from Google Trends (daily, by country), Hacker News, Dev.to & Product Hunt. Related news articles included. Free 500/mo. Google Trends API alternative — no scraping needed.
```

### Tags

```
trends, google-trends, trending-topics, hacker-news, devto, product-hunt, market-research, social-trends, content-ideas, trend-analysis
```

### Long Description

```
## Trending Topics Aggregator — Google Trends + Hacker News + Dev.to + Product Hunt

Get today's trending topics from multiple sources in one unified API. Google Trends daily trends with traffic estimates and related news, Hacker News top stories, Dev.to trending articles, and Product Hunt launches.

### 5 Endpoints

1. **`GET /google?geo=US`** — Google Trends daily trending topics (configurable country)
2. **`GET /hackernews`** — Hacker News top 25 stories with scores & comments
3. **`GET /devto`** — Dev.to trending articles with reactions
4. **`GET /producthunt`** — Product Hunt today's launches
5. **`GET /all`** — Combined feed from all sources

### Google Trends Response Includes

- Trend title
- Approximate traffic volume (e.g., "200K+")
- Publication date
- Related news articles (title, URL, source)

### Use Cases

- **Content marketing**: Find trending topics for blog posts & social media
- **Market research**: Monitor industry trends in real time
- **SEO**: Discover rising keywords before competition
- **Product development**: Spot emerging needs and opportunities
- **Journalism**: Track breaking stories across platforms
- **Slack/Discord bots**: Daily trending topics digest

### Quick Start

```
GET /google?geo=US
→ {"geo": "US", "count": 20, "items": [{"title": "...", "traffic": "500K+", "relatedArticles": [...]}, ...]}
```

```
GET /hackernews
→ {"items": [{"title": "...", "url": "...", "score": 456, "comments": 123}, ...]}
```

Free tier: 500 requests/month. No credit card required.
```

### Pricing

```
Basic (Free):    500 req/mo,   1 req/sec  — $0
Pro:           50,000 req/mo,  10 req/sec — $5.99/mo
Ultra:        500,000 req/mo,  50 req/sec — $14.99/mo
Mega:       2,000,000 req/mo, 100 req/sec — $49.99/mo
```

---

## 20. Company Data API

### API Name

```
Company Data API - Business Search, Domain Enrichment & Tech Stack Detection
```

### Short Description

```
Search companies via Wikidata, enrich by domain (website metadata, tech stack, social links, RDAP). Free 500/mo. Clearbit/ZoomInfo alternative for basic company intelligence at zero cost.
```

### Tags

```
company-data, business-search, domain-enrichment, tech-stack, company-lookup, clearbit-alternative, lead-enrichment, wikidata, business-intelligence, sales-tools
```

### Long Description

```
## Company Intelligence API — Clearbit Alternative for Domain Enrichment

Search for company information, enrich domains with website metadata, detect technology stacks, and extract social links — all from free public sources. No Clearbit subscription needed.

### 4 Endpoints

1. **`GET /search?q=<company_name>`** — Search companies via Wikidata
2. **`GET /company?jurisdiction=<code>&number=<number>`** — Specific company details
3. **`GET /domain?domain=<domain>`** — Company info by domain (RDAP + website metadata)
4. **`GET /enrich?domain=<domain>`** — Full enrichment: metadata, tech stack, social links, contacts

### Enrichment Data Points

- **Website metadata**: Title, description, OG tags, favicon
- **Technology detection**: Frameworks, analytics, CMS, CDN, hosting
- **RDAP/WHOIS**: Domain registrar, creation/expiry dates, nameservers
- **Social links**: Twitter, LinkedIn, GitHub, Facebook (from website meta)

### Cost Comparison

| | This API | Clearbit | ZoomInfo | Hunter.io |
|---|---|---|---|---|
| Free tier | **500/mo** | 25/mo | None | 25/mo |
| 50K enrichments | **$9.99** | Custom ($) | Custom ($$) | $399+/mo |
| Tech stack | **Included** | Included | No | No |
| WHOIS data | **Included** | No | No | No |

### Use Cases

- **Sales teams**: Qualify leads by domain — tech stack, company size signals
- **Marketing**: Enrich CRM contacts with company data
- **Competitive intelligence**: Monitor competitor technology changes
- **Due diligence**: Domain age, registrar, WHOIS data for investigations
- **SaaS products**: "Powered by" badges and competitor analysis features
- **Security**: Verify business legitimacy by domain

### Quick Start

```
GET /search?q=Stripe
→ {"results": [{"name": "Stripe", "description": "Financial technology company", ...}]}
```

```
GET /enrich?domain=github.com
→ {"domain": "github.com", "title": "GitHub", "technologies": ["React", "Ruby on Rails"], "social": {"twitter": "@github"}, ...}
```

Free tier: 500 enrichments/month. No credit card required.
```

### Pricing

```
Basic (Free):    500 req/mo,   1 req/sec  — $0
Pro:           50,000 req/mo,  10 req/sec — $9.99/mo
Ultra:        500,000 req/mo,  50 req/sec — $24.99/mo
Mega:       2,000,000 req/mo, 100 req/sec — $49.99/mo
```

---

## 21. WP Internal Link API

### API Name

```
WP Internal Link API - WordPress Internal Linking Suggestions & Optimization
```

### Short Description

```
Analyze WordPress articles and get intelligent internal link suggestions. Keyword overlap scoring, n-gram matching (Japanese & English). Free 500/mo. SEO internal linking automation for WordPress sites.
```

### Tags

```
wordpress, internal-links, seo, internal-linking, wp-api, link-building, content-optimization, keyword-matching, seo-tool, wordpress-seo
```

### Long Description

```
## Automate WordPress Internal Linking — SEO Optimization API

Analyze your WordPress articles and get intelligent internal link suggestions based on keyword overlap, n-gram matching, and relevance scoring. Supports both English and Japanese content.

### Key Features

- **Keyword overlap scoring**: Matches unigrams, bigrams, and trigrams between articles
- **Japanese language support**: Full Unicode tokenization for Japanese content
- **Stop word filtering**: English + Japanese stop words removed for accurate matching
- **HTML-safe processing**: Strips HTML tags before analysis
- **Configurable thresholds**: Control minimum relevance score for suggestions

### How It Works

1. Submit your articles (title + content + URL)
2. API analyzes keyword overlap between all article pairs
3. Returns ranked internal link suggestions with relevance scores
4. Implement the suggestions in your WordPress posts

### Use Cases

- **WordPress bloggers**: Automate internal linking for better SEO
- **Content agencies**: Scale internal link building across client sites
- **SEO tools**: Add internal linking analysis to your product
- **Content audits**: Identify linking opportunities across large sites
- **Multilingual sites**: Japanese + English content analysis

### Quick Start

```
POST /analyze
{"articles": [
  {"id": 1, "title": "Best SIM Cards", "content": "...", "url": "/best-sim-cards/"},
  {"id": 2, "title": "Budget Mobile Plans", "content": "...", "url": "/budget-mobile/"}
]}
→ {"suggestions": [{"from": 1, "to": 2, "relevance": 0.85, "anchor_text": "budget mobile plans"}]}
```

Free tier: 500 analyses/month. No credit card required.
```

### Pricing

```
Basic (Free):    500 req/mo,   1 req/sec  — $0
Pro:           50,000 req/mo,  10 req/sec — $9.99/mo
Ultra:        500,000 req/mo,  50 req/sec — $24.99/mo
Mega:       2,000,000 req/mo, 100 req/sec — $49.99/mo
```

---

## 22. PDF Generator API

### API Name

```
PDF Generator API - HTML/Markdown/Text to PDF Conversion (Free, No Puppeteer)
```

### Short Description

```
Generate PDFs from HTML, Markdown, or plain text. Custom margins, headers, footers, page numbers. Pure JS — no Puppeteer, no Chrome dependency. Free 500/mo. Lightweight PDF generation via API.
```

### Tags

```
pdf-generator, html-to-pdf, markdown-to-pdf, pdf-api, document-generation, pdf-conversion, invoice-generator, report-generator, developer-tools, serverless
```

### Long Description

```
## Generate PDFs via API — No Puppeteer, No Chrome, No Heavy Dependencies

Convert HTML, Markdown, or plain text to PDF documents with custom margins, headers, footers, and page numbers. Built with pure JavaScript PDF binary construction — runs on Cloudflare Workers with zero cold start.

### 3 Input Formats

1. **Plain Text** — Direct text-to-PDF with automatic word wrapping and pagination
2. **Markdown** — Parsed to structured PDF with heading hierarchy
3. **HTML** — Converted to clean text layout in PDF

### Customization Options

- **Page size**: A4 (default), Letter, Legal, or custom dimensions
- **Margins**: Top, bottom, left, right (in points)
- **Font size**: Configurable (default 12pt)
- **Line height**: Configurable spacing
- **Headers**: Custom text on every page
- **Footers**: Custom text with `{{page}}`/`{{pages}}` placeholders

### Use Cases

- **Invoice generation**: Create PDF invoices from structured data
- **Report automation**: Generate PDF reports from API data
- **Document management**: Convert content to archival PDF format
- **Email attachments**: Generate PDF attachments dynamically
- **E-commerce**: Order confirmation PDFs
- **Education**: Generate certificates and course materials

### Quick Start

```
POST /generate
{"content": "Hello World\nThis is page 1", "format": "text", "options": {"header": "My Report", "footer": "Page {{page}} of {{pages}}"}}
→ Returns binary PDF file
```

```
POST /generate
{"content": "# Report Title\n\n## Section 1\n\nContent here...", "format": "markdown"}
→ Returns binary PDF file
```

Free tier: 500 PDFs/month. No credit card required.
```

### Pricing

```
Basic (Free):    500 req/mo,   1 req/sec  — $0
Pro:           50,000 req/mo,  10 req/sec — $9.99/mo
Ultra:        500,000 req/mo,  50 req/sec — $24.99/mo
Mega:       2,000,000 req/mo, 100 req/sec — $49.99/mo
```

---

## 23. Placeholder Image API

### API Name

```
Placeholder Image API - SVG Placeholders with Gradients, Categories & Custom Text
```

### Short Description

```
Generate beautiful SVG placeholder images instantly. 10 gradient presets, 8 categories (avatar, banner, hero, etc.), custom text, colors & sizes. Free 500/mo. Placeholder.com alternative with gradients.
```

### Tags

```
placeholder-image, svg-generator, image-placeholder, gradient, avatar-placeholder, banner-placeholder, mockup, design-tools, prototyping, ui-development
```

### Long Description

```
## Beautiful SVG Placeholder Images — Not Just Gray Boxes

Generate visually appealing SVG placeholders with gradient backgrounds, custom text, and category presets. Perfect for prototyping, mockups, and development environments.

### Features

- **10 gradient presets**: blue, sunset, ocean, forest, fire, purple, dark, sky, peach, mint
- **8 category presets**: avatar, banner, thumbnail, product, hero, card, icon, cover
- **Custom dimensions**: Any width × height combination
- **Custom text**: Override default dimension label with your text
- **Custom colors**: Foreground & background hex colors, text color
- **SVG output**: Vector format — scales perfectly at any size
- **Zero dependencies**: Pure SVG generation, no image processing libraries

### Endpoint

```
GET /image?width=400&height=300&bg=sunset&text=My+Image
```

### Parameters

| Param | Default | Description |
|-------|---------|-------------|
| width | 300 | Image width in pixels |
| height | 200 | Image height in pixels |
| text | `{width}x{height}` | Custom label text |
| bg | blue | Gradient preset name |
| category | — | Category preset (overrides bg + text) |
| color1 | — | Custom gradient start color (hex) |
| color2 | — | Custom gradient end color (hex) |
| textColor | #ffffff | Text color (hex) |
| fontSize | auto | Font size in pixels |

### Use Cases

- **UI prototyping**: Beautiful placeholders during development
- **Design mockups**: Category-specific placeholders (avatar, product, banner)
- **Documentation**: Illustrative images in API docs and READMEs
- **Testing**: Consistent placeholder images in automated tests
- **Email templates**: Fallback images for broken links
- **CMS development**: Default images for empty content slots

### Quick Start

```
GET /image?width=800&height=400&bg=ocean&text=Hero+Banner
→ Returns SVG image with ocean gradient and "Hero Banner" text
```

```
GET /image?category=avatar&width=128&height=128
→ Returns SVG avatar placeholder with purple gradient
```

Free tier: 500 images/month. No credit card required.
```

### Pricing

```
Basic (Free):    500 req/mo,   1 req/sec  — $0
Pro:           50,000 req/mo,  10 req/sec — $3.99/mo
Ultra:        500,000 req/mo,  50 req/sec — $9.99/mo
Mega:       5,000,000 req/mo, 100 req/sec — $29.99/mo
```

---

## 24. Markdown Converter API

### API Name

```
Markdown Converter API - MD to HTML with GFM Tables, TOC & Syntax Highlighting
```

### Short Description

```
Convert Markdown to HTML with GFM support: tables, task lists, strikethrough, code blocks with syntax classes, auto TOC generation. Free 500/mo. Pure JS — no dependencies, <10ms latency.
```

### Tags

```
markdown, markdown-to-html, gfm, github-flavored-markdown, html-converter, toc-generator, syntax-highlighting, content-rendering, developer-tools, static-site
```

### Long Description

```
## Markdown to HTML Converter — Full GFM Support with TOC Generation

Convert GitHub Flavored Markdown to clean, semantic HTML. Supports tables, task lists, strikethrough, fenced code blocks with language classes, and automatic Table of Contents generation. Pure JavaScript — no external dependencies.

### Features

- **GFM tables**: Full table rendering with alignment support
- **Task lists**: `- [x]` checkbox rendering
- **Strikethrough**: `~~text~~` support
- **Fenced code blocks**: Language-specific CSS classes for syntax highlighting
- **Auto TOC**: Generate Table of Contents from headings
- **Smart typography**: Smart quotes, dashes, ellipses
- **XSS-safe**: HTML entities escaped by default

### Endpoints

1. **`POST /convert`** — Convert Markdown to HTML
2. **`POST /toc`** — Extract Table of Contents from Markdown
3. **`POST /convert-with-toc`** — HTML output + TOC in single response

### Use Cases

- **CMS/Blog platforms**: Render Markdown content as HTML
- **Documentation sites**: Convert .md files to HTML pages
- **API documentation**: Render endpoint descriptions from Markdown
- **Email generators**: Convert Markdown drafts to HTML email
- **Static site generators**: Server-side Markdown rendering
- **Note-taking apps**: Live Markdown preview

### Quick Start

```
POST /convert
{"markdown": "# Hello\n\nThis is **bold** and ~~struck~~.\n\n| Col 1 | Col 2 |\n|-------|-------|\n| A | B |"}
→ {"html": "<h1>Hello</h1><p>This is <strong>bold</strong> and <del>struck</del>.</p><table>...</table>"}
```

```
POST /toc
{"markdown": "# Introduction\n## Getting Started\n## API Reference\n### Endpoints"}
→ {"toc": [{"level": 1, "text": "Introduction"}, {"level": 2, "text": "Getting Started"}, ...]}
```

Free tier: 500 conversions/month. No credit card required.
```

### Pricing

```
Basic (Free):    500 req/mo,   1 req/sec  — $0
Pro:           50,000 req/mo,  10 req/sec — $5.99/mo
Ultra:        500,000 req/mo,  50 req/sec — $14.99/mo
Mega:       2,000,000 req/mo, 100 req/sec — $49.99/mo
```

---

## RapidAPI Studio での更新手順（全API共通）

各APIについて以下の順序で更新する:

1. [RapidAPI Studio](https://rapidapi.com/studio) にログイン
2. 対象APIを選択 → **Settings** タブ
3. **API Name**: 上記の改善後API名をコピペ
4. **Short Description**: 上記をコピペ
5. **Tags**: 既存タグを全削除 → 上記タグをカンマ区切りで入力
6. **Documentation** タブ → **Long Description**: 上記Markdown全文をコピペ
7. **Pricing** タブ → 上記のプラン設定に合わせる（既存プランがある場合は価格・リミットを確認）
8. **Save** して公開

### 更新後の確認チェックリスト

- [ ] 03 - Link Preview API
- [ ] 05 - Text Analysis API
- [ ] 06 - IP Geolocation API
- [ ] 07 - URL Shortener API
- [ ] 08 - JSON Formatter API
- [ ] 09 - Hash & Encoding API
- [ ] 10 - Currency Exchange API
- [ ] 11 - AI Text API
- [ ] 12 - Social Video API
- [ ] 13 - Crypto Data API
- [ ] 15 - Weather API
- [ ] 17 - News Aggregator API
- [ ] 18 - AI Translate API
- [ ] 19 - Trends API
- [ ] 20 - Company Data API
- [ ] 21 - WP Internal Link API
- [ ] 22 - PDF Generator API
- [ ] 23 - Placeholder Image API
- [ ] 24 - Markdown Converter API
