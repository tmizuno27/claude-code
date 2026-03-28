# RapidAPI Studio コピペ用テキスト（2026-03-28更新・SEO最適化版）

RapidAPI Studioの各APIページで手動更新するためのテキスト集。
**Title → Short Description → Tags → Long Description** の順にコピペして Save。

> **重要**: タイトルに「Free」を前方配置。Short Descriptionに競合比較・差別化ポイントを含める。

---

## 更新手順

1. https://studio.rapidapi.com/ にログイン
2. 対象APIを選択 → "Details" タブ
3. **API Name** に Title をペースト
4. **Short Description** をペースト
5. **Tags** をカンマ区切りで入力
6. **Long Description** をペースト → Save
7. 次のAPIへ

## 共通タグ（全APIに追加）
```
free api, no auth required, cloudflare workers, rest api, fast api
```

---

## API #01: QR Code Generator API

### Title
```
Free QR Code Generator API - PNG, SVG, Base64 | <50ms Edge Response
```

### Short Description
```
Free QR Code API - Generate PNG/SVG/Base64 in <50ms. Custom colors, error correction. 500 req/mo free.
```

### Tags
```
qr code, qr code generator, qr code api, barcode, png to base64, svg generator, free qr api, image generation, edge computing, marketing tools
```

### Long Description
```
## The Fastest QR Code API on RapidAPI
Generate production-ready QR codes in under 50ms from Cloudflare's 300+ edge locations. PNG, SVG, or Base64 JSON output with full color customization.

## Why This API?
- **Sub-50ms latency** from Cloudflare's global edge network
- **3 output formats**: PNG (raster), SVG (vector/print), Base64 JSON (embed in HTML without file I/O)
- **Brand colors**: Custom foreground + background hex colors
- **Error correction**: L/M/Q/H levels — H allows logo overlay on center 20%

## Real-World Use Cases
- **E-commerce**: Dynamic checkout/payment QR codes per order
- **Restaurants**: Contactless digital menu QR codes per table
- **SaaS invoices**: Embed QR codes in HTML/PDF via Base64 data_uri
- **Marketing**: Branded QR codes for flyers, posters, business cards

## Quick Start
GET /generate?text=https://example.com&size=400&format=png&color=FF5722

## Pricing — 97% Cheaper Than Alternatives
| Plan | Price | Requests/mo |
|------|-------|-------------|
| Basic (FREE) | $0 | 500 |
| Pro | $5.99 | 50,000 |
| Ultra | $14.99 | 500,000 |
| Mega | $49.99 | 5,000,000 |

## Alternative To
Faster and cheaper than goqr.me, QR Server, QRickit, and QR Code Monkey.
```

---

## API #02: Email Validation API

### Title
```
Free Email Validation API - MX Lookup, Disposable Detection, Bulk Verify
```

### Short Description
```
Free Email Validator - MX check, disposable detection (500+ domains), typo fix, bulk. Save $390/mo vs ZeroBounce.
```

### Tags
```
email validation, email verification, disposable email, mx lookup, bulk email check, email api, bounce detection, email hygiene, lead validation, free email validator
```

### Long Description (Markdown)
```
Validate email addresses in real time with format checks, MX record lookups, disposable domain detection (500+ domains), free provider detection, role-based address detection, and typo suggestions.

## Getting Started
1. Subscribe (free plan available)
2. Call `/validate?email=user@example.com`
3. Check `valid`, `score`, and `suggestion` fields

## Key Features
- **MX Record Lookup** — DNS verification without sending emails
- **Disposable Detection** — 500+ temporary email domains blocked
- **Typo Correction** — Suggests fixes for gmial.com → gmail.com
- **Bulk Validation** — Up to 50 emails per request
- **Confidence Score** — 0-100 quality scoring

## Alternative To
ZeroBounce ($16/2K emails), Hunter.io ($49/500 searches), NeverBounce ($8/1K). This API offers flat-rate pricing starting at $0/month.

## Sample Response
{"email":"user@example.com","valid":true,"score":100,"is_disposable":false,"suggestion":null}

## Need More Requests?
Upgrade to Pro (50,000 req/mo) or Ultra (500,000 req/mo) for high-volume email validation.
```

---

## API #03: Link Preview API

### Title
```
Link Preview API - Open Graph, Twitter Cards, Metadata Extraction
```

### Short Description
```
Free Link Preview API - Open Graph, Twitter Cards, RSS Discovery, Bulk URLs, No Auth
```

### Long Description
```
Extract Open Graph tags, Twitter Cards, favicons, RSS feeds, author info, and more from any URL. Supports bulk extraction (up to 10 URLs).

## Getting Started
1. Subscribe (free plan available)
2. Call `/preview?url=https://github.com`
3. Get title, description, image, favicon, and social tags

## Key Features
- **Open Graph & Twitter Cards** — Full social metadata extraction
- **RSS/Atom Discovery** — Automatically finds feed URLs
- **Bulk Extraction** — Process up to 10 URLs in one request
- **1-Hour Edge Cache** — Repeated URLs served instantly
- **Rich Metadata** — Title, description, image, favicon, author, published date, language

## Alternative To
LinkPreview.net (60 req/hr), Microlink ($15.9/mo), OpenGraph.io ($12/mo). This API starts at $0/month with 500 requests.

## Need More Requests?
Upgrade to Pro for 50,000 requests/month at $5.99.
```

---

## API #04: Screenshot API

### Title
```
Screenshot API - Capture Any Page as PNG or JPEG
```

### Short Description
```
Free Screenshot API - Full-Page, Custom Viewport, PNG/JPEG, Render Delay, No Auth
```

### Long Description
```
Capture screenshots of any website as PNG or JPEG. Supports custom viewport sizes (mobile/tablet/desktop), full-page capture, JPEG quality control, and render delay for JavaScript-heavy pages.

## Getting Started
1. Subscribe (free plan available)
2. Call `/screenshot?url=https://example.com`
3. Receive PNG image directly

## Key Features
- **Full-Page Capture** — Scroll and capture entire page
- **Custom Viewports** — 320px to 3840px width
- **PNG + JPEG** — Quality control for JPEG (1-100)
- **Render Delay** — Wait up to 5s for JavaScript
- **1-Hour Cache** — Repeated requests served from edge

## Alternative To
ScreenshotAPI ($19/1K), URLBox ($19/mo), Screenshotlayer ($10/2K). Flat-rate pricing, no per-screenshot billing.

## Need More Requests?
Upgrade to Pro (50,000/mo) or Ultra (500,000/mo).
```

---

## API #05: Text Analysis API

### Title
```
Text Analysis API - Sentiment, Keywords, Readability, NLP
```

### Short Description
```
Free Text Analysis API - Sentiment, Keywords, Readability, Language Detection, Pure JS NLP
```

### Long Description
```
Analyze text for sentiment, extract keywords, calculate readability scores, and detect language. Pure JavaScript NLP — no external AI APIs, no per-token costs.

## Getting Started
1. Subscribe (free plan available)
2. POST to `/analyze` with `{"text": "Your text here"}`
3. Get sentiment, keywords, readability score, and language

## Key Features
- **Sentiment Analysis** — Positive/negative/neutral scoring
- **Keyword Extraction** — Top keywords with relevance scores
- **Readability Score** — Flesch-Kincaid grade level
- **Language Detection** — 50+ languages
- **Privacy** — Text never sent to third-party AI services

## Alternative To
MonkeyLearn ($299/mo), Aylien (custom), MeaningCloud ($79/mo). Pure NLP at $0/month, no AI API costs.

## Need More Requests?
Upgrade to Pro for 50,000 requests/month at $5.99.
```

---

## API #07: URL Shortener API

### Title
```
URL Shortener API - Short Links with Click Analytics
```

### Short Description
```
Free URL Shortener API - Click Analytics, Custom Aliases, Expiration, CF KV Storage
```

### Long Description
```
Create short URLs with built-in click tracking. Analytics include referrer, device, and geographic data. Powered by Cloudflare KV for sub-10ms redirects worldwide.

## Getting Started
1. Subscribe (free plan available)
2. POST to `/shorten` with `{"url": "https://example.com/long"}`
3. Get short URL with analytics tracking

## Key Features
- **Click Analytics** — Referrer, device, geographic data
- **Custom Aliases** — /my-campaign style branded links
- **Link Expiration** — Auto-expire after set date
- **Sub-10ms Redirects** — Cloudflare KV edge storage

## Alternative To
Bitly ($29/mo), TinyURL ($12.99/mo), Rebrandly ($13/mo). Full analytics at $0/month.

## Need More Requests?
Upgrade to Pro for 50,000 requests/month at $5.99.
```

---

## API #08: JSON Formatter API

### Title
```
JSON Formatter & Validator API - Format, Minify, Diff, CSV Convert
```

### Short Description
```
Free JSON API - Format, Minify, Validate, Diff, JMESPath, CSV Convert, Schema Validation
```

### Long Description
```
All-in-one JSON toolkit: format, minify, validate, diff, JMESPath transform, and JSON/CSV conversion. 7 endpoints in one API.

## Getting Started
1. Subscribe (free plan available)
2. POST to `/format` with `{"json": "..."}`
3. Get formatted JSON with proper indentation

## Key Features
- **7 Endpoints** — Format, minify, validate, diff, transform, CSV↔JSON
- **JSON Diff** — Compare two JSON objects with detailed changes
- **JMESPath** — Query and reshape JSON with expressions
- **Schema Validation** — Validate against JSON Schema
- **CSV Conversion** — Bidirectional JSON ↔ CSV

## Alternative To
JSONLint (web only), JSON Formatter Online (web only), ConvertCSV (web only). The only REST API combining all JSON operations.

## Need More Requests?
Upgrade to Pro for 50,000 requests/month at $5.99.
```

---

## API #09: Hash & Encoding API

### Title
```
Hash & Encoding API - SHA256, MD5, Bcrypt, Base64, HMAC
```

### Short Description
```
Free Hash API - SHA256, MD5, Bcrypt, HMAC, Base64, URL Encode, Random String, UUID
```

### Long Description
```
Hash, encode, and perform cryptographic operations via REST API. SHA-256/384/512, MD5, bcrypt, HMAC, Base64, URL encoding, and secure random generation.

## Getting Started
1. Subscribe (free plan available)
2. POST to `/hash` with `{"text": "hello", "algorithm": "sha256"}`
3. Get hash result

## Key Features
- **8 Endpoints** — Hash, HMAC, bcrypt, encode, decode, compare, random, file hash
- **Bcrypt** — Password hashing with configurable salt rounds
- **HMAC** — Webhook signature verification (Stripe, GitHub, etc.)
- **Random** — Cryptographically secure strings and UUIDs

## Alternative To
CryptoJS online (web only), HashAPI (web only), bcrypt generators (web only). The only REST API combining hashing, encoding, HMAC, and random generation.

## Need More Requests?
Upgrade to Pro for 50,000 requests/month at $5.99.
```

---

## API #12: Social Video API

### Title
```
Social Video Download API - YouTube, TikTok, Instagram, X
```

### Short Description
```
Free Social Video API - Download URLs from YouTube, TikTok, Instagram, X, Facebook, Reddit
```

### Long Description
```
Extract video download URLs from 6 social platforms. Returns direct video file URLs with metadata (title, author, thumbnail, duration). No headless browser — pure HTTP parsing.

## Getting Started
1. Subscribe (free plan available)
2. GET `/download?url=https://youtube.com/watch?v=...`
3. Get direct download URL and metadata

## Key Features
- **6 Platforms** — YouTube, TikTok, Instagram, Twitter/X, Facebook, Reddit
- **Multiple Qualities** — All available resolutions returned
- **Full Metadata** — Title, author, thumbnail, duration
- **No Browser Automation** — Fast HTTP parsing

## Alternative To
SaveFrom (web only), yt-dlp (CLI only), other RapidAPI video APIs (1-3 platforms). 6-platform support with simple REST API.

## Need More Requests?
Upgrade to Pro for 50,000 requests/month at $9.99.
```

---

## API #15: Weather API

### Title
```
Weather API - Forecast, Current Conditions, Historical Data
```

### Short Description
```
Free Weather API - Current, Hourly, Daily Forecast, Historical Data, Open-Meteo Powered
```

### Long Description
```
Current weather, hourly/daily forecasts, and historical data for any location. Powered by Open-Meteo (ECMWF, NOAA). No upstream API key costs.

## Getting Started
1. Subscribe (free plan available)
2. GET `/current?city=Tokyo`
3. Get temperature, humidity, wind, and conditions

## Key Features
- **5 Endpoints** — Current, forecast, hourly, geocode, historical
- **Historical Data** — Back to 1940 via ERA5 reanalysis
- **Open-Meteo Source** — ECMWF, NOAA, DWD accuracy
- **Geocoding** — City name or coordinates

## Alternative To
OpenWeatherMap ($40/mo), WeatherAPI ($8/mo), AccuWeather (custom). Open-source data at $0/month.

## Need More Requests?
Upgrade to Pro for 50,000 requests/month at $5.99.
```

---

## API #16: WHOIS Domain API

### Title
```
WHOIS Domain API - Domain Lookup, DNS Records, RDAP
```

### Short Description
```
Free WHOIS API - RDAP Lookup, DNS Records, Domain Availability, TLD List, No Auth
```

### Long Description
```
Domain registration lookup via modern RDAP protocol and DNS record queries via Cloudflare DoH. Check domain availability and list supported TLDs.

## Getting Started
1. Subscribe (free plan available)
2. GET `/lookup?domain=github.com`
3. Get registrar, creation date, expiration, nameservers

## Key Features
- **RDAP Protocol** — Modern WHOIS with structured JSON
- **DNS Queries** — A, AAAA, MX, TXT, CNAME, NS records
- **Domain Availability** — Check if domain is registered
- **No Upstream Keys** — Free RDAP + Cloudflare DoH

## Alternative To
WhoisXML API ($19/mo), DomainTools ($99/mo), SecurityTrails ($50/mo). RDAP + DNS at $0/month.

## Need More Requests?
Upgrade to Pro for 50,000 requests/month at $5.99.
```

---

## API #17: News Aggregator API

### Title
```
News Aggregator API - Headlines from RSS, Hacker News, Dev.to
```

### Short Description
```
Free News API - Headlines, Categories, Search, Hacker News, Dev.to, Commercial Use OK
```

### Long Description
```
Aggregated news from multiple free RSS feeds plus Hacker News and Dev.to. Search by keyword, filter by category. Commercial use allowed on all plans.

## Getting Started
1. Subscribe (free plan available)
2. GET `/top?category=tech`
3. Get headlines with title, source, description, and link

## Key Features
- **6 Endpoints** — Top, tech, business, search, Hacker News, Dev.to
- **Keyword Search** — Find articles on any topic
- **Developer Feeds** — Hacker News top stories + Dev.to latest
- **Commercial Use** — Allowed on free tier (unlike NewsAPI)

## Alternative To
NewsAPI ($449/mo, dev-only free tier), Bing News ($7/1K), GNews ($84/mo). Commercial use at $0/month.

## Need More Requests?
Upgrade to Pro for 50,000 requests/month at $5.99.
```

---

## API #18: AI Translate API

### Title
```
AI Translation API - 100+ Languages via Meta M2M-100
```

### Short Description
```
Free AI Translate API - 100+ Languages, Neural MT, Batch, Language Detection, M2M-100
```

### Long Description
```
Neural machine translation between 100+ languages using Meta's M2M-100 model on Cloudflare Workers AI. Direct translation between any language pair without English pivot.

## Getting Started
1. Subscribe (free plan available)
2. POST to `/translate` with `{"text": "Hello", "source": "en", "target": "es"}`
3. Get translated text

## Key Features
- **100+ Languages** — Meta M2M-100 1.2B model
- **Direct Translation** — Any pair without English pivot
- **Batch Support** — Translate multiple texts in one call
- **Language Detection** — Auto-detect source language
- **No Per-Character Pricing** — Flat rate plans

## Alternative To
DeepL API ($5.49/1M chars), Google Translate ($20/1M chars), LibreTranslate (self-hosted). Neural translation at $0/month.

## Need More Requests?
Upgrade to Pro for 50,000 requests/month at $9.99.
```

---

## API #19: Trends API

### Title
```
Trends API - Google, Reddit, Hacker News, GitHub, Product Hunt
```

### Short Description
```
Free Trends API - 5 Sources (Google, Reddit, HN, GitHub, PH), Real-Time Trending Topics
```

### Long Description
```
Aggregated trending topics from 5 sources: Google Trends daily, Hacker News top stories, Reddit r/popular, GitHub trending repos, and Product Hunt today.

## Getting Started
1. Subscribe (free plan available)
2. GET `/google/daily`
3. Get today's trending topics with traffic volume

## Key Features
- **5 Sources** — Google, Hacker News, Reddit, GitHub, Product Hunt
- **Developer-Focused** — GitHub repos + HN stories
- **Region Support** — Google Trends by country (US, JP, GB, etc.)
- **No Upstream Costs** — All public sources

## Alternative To
Google Trends (no official API), Exploding Topics ($39/mo), BuzzSumo ($99/mo). 5-source aggregation at $0/month.

## Need More Requests?
Upgrade to Pro for 50,000 requests/month at $5.99.
```

---

## API #20: Company Data API

### Title
```
Company Data API - Business Info, CRM Enrichment, Domain Lookup
```

### Short Description
```
Free Company Data API - Search, Domain Lookup, CRM Enrichment, B2B Data, Public Sources
```

### Long Description
```
Company search and enrichment from free public databases. Look up by name, domain, or industry. Enrich CRM with company details.

## Getting Started
1. Subscribe (free plan available)
2. GET `/search?name=Stripe`
3. Get company name, industry, location, social profiles

## Key Features
- **4 Endpoints** — Search, company, domain, enrich
- **Domain Enrichment** — Look up company by domain name
- **Social Profiles** — LinkedIn, Twitter links
- **Public Sources** — No paid upstream APIs

## Alternative To
Clearbit ($99/mo), ZoomInfo ($10K+/yr), FullContact ($99/mo). B2B data at $0/month.

## Need More Requests?
Upgrade to Pro for 50,000 requests/month at $9.99.
```

---

## API #21: WP Internal Link API

### Title
```
WordPress Internal Link API - SEO Link Suggestions
```

### Short Description
```
Free WP Internal Link API - Keyword Matching, Relevance Scoring, Bulk Analysis, Any CMS
```

### Long Description
```
Analyze article content and get intelligent internal link suggestions based on keyword matching and relevance scoring. Works with any CMS, not just WordPress.

## Getting Started
1. Subscribe (free plan available)
2. POST to `/analyze` with article content and article list
3. Get link suggestions with anchor text and relevance scores

## Key Features
- **Keyword Matching** — Content-based link opportunities
- **Relevance Scoring** — 0-100 contextual relevance
- **Bulk Analysis** — Multiple articles per request
- **Platform-Agnostic** — REST API, works with any CMS
- **CI/CD Ready** — Automate internal linking checks

## Alternative To
Link Whisper ($77/yr, WP only), Yoast ($99/yr, WP only), Internal Link Juicer ($69.99/yr, WP only). The only REST API for internal link optimization.

## Need More Requests?
Upgrade to Pro for 50,000 requests/month at $9.99.
```

---

## API #22: PDF Generator API

### Title
```
PDF Generator API - HTML/Markdown/URL to PDF
```

### Short Description
```
Free PDF API - HTML/Markdown/URL to PDF, Custom Sizes, Headers, Footers, Landscape
```

### Long Description
```
Generate PDFs from HTML, Markdown, or web URLs. Custom page sizes (A4/Letter/Legal), margins, headers/footers, and landscape orientation.

## Getting Started
1. Subscribe (free plan available)
2. POST to `/generate` with `{"html": "<h1>Invoice</h1>", "format": "A4"}`
3. Receive PDF binary

## Key Features
- **3 Input Types** — HTML, Markdown, URL
- **Custom Layout** — A4, Letter, Legal, margins, landscape
- **Headers/Footers** — Custom HTML header/footer on every page
- **Markdown Direct** — No HTML conversion step needed

## Alternative To
PDFShift ($9/mo), HTML2PDF ($14.99/mo), DocRaptor ($15/mo). PDF generation with Markdown support at $0/month.

## Need More Requests?
Upgrade to Pro for 50,000 requests/month at $9.99.
```

---

## API #23: Placeholder Image API

### Title
```
Placeholder Image API - Custom SVG/PNG with Text & Gradients
```

### Short Description
```
Free Placeholder Image API - SVG/PNG, Text Overlay, Gradients, Category Presets, Any Size
```

### Long Description
```
Generate custom placeholder images with text overlay, gradients, and category presets. SVG or PNG, any dimension up to 4000x4000px.

## Getting Started
1. Subscribe (free plan available)
2. GET `/image?width=400&height=300&text=Hello`
3. Receive placeholder image

## Key Features
- **SVG + PNG** — Vector or raster output
- **Text Overlay** — Custom text, font size, color
- **Gradients** — Linear gradient backgrounds with presets
- **Category Presets** — Nature, tech, food, abstract, business
- **Any Size** — 1x1 to 4000x4000 pixels

## Alternative To
Placeholder.com (no API), Lorem Picsum (no customization), PlaceIMG (shutdown). API with gradients and categories at $0/month.

## Need More Requests?
Upgrade to Pro for 50,000 requests/month at $5.99.
```

---

## API #24: Markdown Converter API

### Title
```
Markdown Converter API - HTML, GFM, TOC, Syntax Highlighting
```

### Short Description
```
Free Markdown API - Bidirectional HTML/MD, GFM Tables, Auto TOC, Syntax Highlight, XSS Safe
```

### Long Description
```
Bidirectional Markdown/HTML conversion with GFM support, auto-generated Table of Contents, syntax highlighting for 100+ languages, and XSS-safe output.

## Getting Started
1. Subscribe (free plan available)
2. POST to `/md-to-html` with `{"markdown": "# Hello", "toc": true}`
3. Get HTML with TOC

## Key Features
- **Bidirectional** — Markdown → HTML and HTML → Markdown
- **GFM** — Tables, task lists, strikethrough, autolinks
- **Auto TOC** — Table of Contents from headings
- **Syntax Highlighting** — 100+ programming languages
- **XSS Safe** — Sanitized HTML output

## Alternative To
Showdown.js (no API), Marked.js (no API), Pandoc (CLI only). The only REST API with bidirectional conversion and auto TOC.

## Need More Requests?
Upgrade to Pro for 50,000 requests/month at $5.99.
```
