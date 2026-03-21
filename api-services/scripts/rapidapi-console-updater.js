// ============================================================
// RapidAPI Studio リスティング一括更新スクリプト
// ============================================================
// 使い方:
//   1. https://rapidapi.com/studio/ にログインする
//   2. Studioトップページ（APIカード一覧が見えるページ）を開く
//   3. DevTools (F12) → Console タブを開く
//   4. このスクリプト全体をコピーしてConsoleに貼り付け、Enter
//   5. 自動で各APIのHub Listingページに遷移し、Short/Long Descriptionを更新する
//   6. 進捗はConsoleに表示される（エラーが出ても次のAPIに進む）
// ============================================================

(async () => {
  'use strict';

  // === 24本分のAPI更新データ ===
  const API_DATA = [
    {
      name: "QR Code Generator API",
      description: "Free QR Code Generator - PNG, SVG, Base64, Custom Colors, No Auth",
      long_description: `## Why QR Code Generator API?
- ✅ Zero authentication required — start generating QR codes instantly
- ✅ 3 output formats (PNG, SVG, Base64) with full color customization
- ✅ Sub-50ms response via Cloudflare's global edge network (300+ locations)

## Key Features
- PNG, SVG, and Base64 output formats
- Custom foreground & background colors (hex)
- Adjustable error correction levels (L/M/Q/H)
- Configurable size from 10px to 1000px
- CORS enabled for browser-side usage

## Use Cases
- **E-commerce**: QR codes for product pages, payments, and receipts
- **Marketing**: Flyers, business cards, and poster campaigns
- **Event Management**: Ticket QR codes and check-in systems
- **Mobile Apps**: Deep-link QR codes for app downloads

## Quick Start
\`\`\`
GET /generate?text=https://example.com&size=300&format=png&color=FF0000&bgcolor=FFFFFF
\`\`\`

## Pricing
| Plan | Price | Requests/mo | Rate Limit |
|------|-------|-------------|------------|
| **Basic (FREE)** | $0 | 500 | 1/sec |
| Pro | $5.99 | 50,000 | 10/sec |
| Ultra | $14.99 | 500,000 | 50/sec |
| Mega | $49.99 | 5,000,000 | 100/sec |

Free tier includes all formats and colors. No credit card required.`
    },
    {
      name: "Email Validation API",
      description: "Free Email Validation: Disposable Detection, MX Lookup, Bounce Check",
      long_description: `## Why Email Validation API?
- ✅ Validates without sending any emails — instant, non-intrusive checks
- ✅ 500+ disposable domain blacklist with typo correction (gmial→gmail)
- ✅ MX record verification + RFC 5322 format validation in one call

## Key Features
- RFC 5322 format validation with detailed error messages
- MX record verification for deliverability
- Disposable/temporary email detection (500+ domains)
- Typo correction suggestions
- Bulk validation up to 50 emails per request (Pro+)

## Use Cases
- **SaaS Signups**: Block disposable emails at registration
- **Email Marketing**: Clean mailing lists before campaigns
- **E-commerce**: Reduce failed order confirmation emails
- **Lead Generation**: Ensure collected emails are valid

## Quick Start
\`\`\`
GET /validate?email=user@example.com
\`\`\`
Returns JSON with \`is_valid\`, \`is_disposable\`, \`has_mx\`, \`suggestion\`, and more.

## Pricing
| Plan | Price | Requests/mo | Rate Limit |
|------|-------|-------------|------------|
| **Basic (FREE)** | $0 | 500 | 1/sec |
| Pro | $9.99 | 50,000 | 10/sec |
| Ultra | $29.99 | 500,000 | 50/sec |

Free tier includes all validation checks. No credit card required.`
    },
    {
      name: "Link Preview - Website Metadata API",
      description: "Free Link Preview: Open Graph, Twitter Card, Favicon, RSS Metadata",
      long_description: `## Why Link Preview API?
- ✅ Extracts Open Graph, Twitter Card, favicon, RSS, and author in one call
- ✅ 1-hour smart caching for blazing-fast repeat requests
- ✅ CORS enabled — use directly from browser-based applications

## Key Features
- Open Graph and Twitter Card metadata extraction
- Favicon, RSS feed, and author detection
- Bulk preview for up to 10 URLs per request
- 1-hour smart caching
- CORS enabled for direct browser usage

## Use Cases
- **Chat Applications**: Rich link previews like Slack and Discord
- **Social Media Tools**: Preview how URLs appear when shared
- **SEO Auditing**: Check Open Graph and meta tag implementation
- **Content Aggregators**: Extract titles, descriptions, and images

## Quick Start
\`\`\`
GET /preview?url=https://github.com
\`\`\`
Returns JSON with \`title\`, \`description\`, \`image\`, \`favicon\`, \`og_tags\`, \`twitter_card\`.

## Pricing
| Plan | Price | Requests/mo | Rate Limit |
|------|-------|-------------|------------|
| **Basic (FREE)** | $0 | 100 | 1/sec |
| Pro | $9.99 | 5,000 | 10/sec |
| Ultra | $29.99 | 25,000 | 50/sec |

Free tier includes all metadata extraction. No credit card required.`
    },
    {
      name: "Website Screenshot API",
      description: "Free Website Screenshot: PNG/JPEG, Custom Viewport, Full Page Capture",
      long_description: `## Why Website Screenshot API?
- ✅ Capture any public URL as PNG or JPEG with custom viewport sizes
- ✅ Full-page capture mode for long scrolling pages
- ✅ Configurable delay for JavaScript-heavy sites

## Key Features
- PNG and JPEG output formats with quality control
- Custom viewport width and height
- Full-page screenshot support
- Configurable render delay for dynamic content
- 1-hour result caching
- CORS enabled

## Use Cases
- **SEO Monitoring**: Visual regression testing for websites
- **Social Sharing**: Generate thumbnails and OG images
- **Archiving**: Capture webpage snapshots for records
- **QA Testing**: Automated visual testing across viewports

## Quick Start
\`\`\`
GET /capture?url=https://example.com&width=1280&height=720&format=png
\`\`\`

## Pricing
| Plan | Price | Requests/mo | Rate Limit |
|------|-------|-------------|------------|
| **Basic (FREE)** | $0 | 100 | 1/sec |
| Pro | $9.99 | 5,000 | 10/sec |
| Ultra | $29.99 | 25,000 | 50/sec |

Free tier includes PNG output and default viewport. No credit card required.`
    },
    {
      name: "Text Analysis / NLP API",
      description: "Free Text Analysis: Sentiment, Keywords, Readability Score",
      long_description: `## Why Text Analysis API?
- ✅ Pure JavaScript NLP — no external AI dependencies, no rate limits from third parties
- ✅ 6-in-1: Sentiment, keywords, readability, language detection, summarization, metrics
- ✅ AFINN lexicon with negation handling + TF-IDF keyword extraction

## Key Features
- Sentiment analysis with confidence score (AFINN-style, 200+ words)
- TF-IDF keyword extraction (top 10 ranked)
- Flesch-Kincaid readability scoring
- Language detection (10 languages)
- Extractive summarization (TextRank-inspired)
- Word/character/sentence/paragraph counts + reading time

## Use Cases
- **Content Marketing**: Analyze sentiment and readability before publishing
- **Social Listening**: Monitor brand sentiment across text data
- **SEO Tools**: Extract keywords and optimize content
- **Chatbots**: Detect language and sentiment in user messages

## Quick Start
\`\`\`
POST /analyze
{"text": "Your text here", "features": ["sentiment", "keywords", "readability"]}
\`\`\`

## Pricing
| Plan | Price | Requests/mo | Rate Limit |
|------|-------|-------------|------------|
| **Basic (FREE)** | $0 | 500 | 1/sec |
| Pro | $9.99 | 50,000 | 10/sec |
| Ultra | $29.99 | 500,000 | 50/sec |

Free tier includes all analysis features. No credit card required.`
    },
    {
      name: "IP Geolocation API",
      description: "Free IP Geolocation: VPN Detection, Fraud Prevention, Bulk Lookup",
      long_description: `## Why IP Geolocation API?
- ✅ VPN/proxy/datacenter detection built-in for fraud prevention
- ✅ Bulk lookup up to 20 IPs per request + auto-detect caller's IP
- ✅ Country, city, region, timezone, ISP, and ASN in one call

## Key Features
- IPv4 and IPv6 support
- Country, city, region, latitude/longitude
- Timezone and ISP/ASN information
- VPN, proxy, and datacenter detection
- Bulk lookup (up to 20 IPs)
- Caller's own IP auto-detection

## Use Cases
- **Fraud Prevention**: Detect VPN/proxy usage in transactions
- **Content Localization**: Serve region-specific content
- **Analytics**: Enrich user data with geographic info
- **Access Control**: Geo-restrict content by country

## Quick Start
\`\`\`
GET /lookup?ip=8.8.8.8
\`\`\`
Returns JSON with \`country\`, \`city\`, \`region\`, \`timezone\`, \`isp\`, \`is_vpn\`, \`is_proxy\`.

## Pricing
| Plan | Price | Requests/mo | Rate Limit |
|------|-------|-------------|------------|
| **Basic (FREE)** | $0 | 500 | 1/sec |
| Pro | $9.99 | 50,000 | 10/sec |
| Ultra | $29.99 | 500,000 | 50/sec |

Free tier includes all lookup features. No credit card required.`
    },
    {
      name: "URL Shortener API",
      description: "Free URL Shortener: Click Analytics, Custom Aliases, KV Storage",
      long_description: `## Why URL Shortener API?
- ✅ Custom aliases + click analytics with timestamps
- ✅ Persistent storage via Cloudflare KV — links never expire
- ✅ Zero external dependencies, ultra-fast redirects

## Key Features
- Create short URLs with custom aliases
- Click tracking with timestamps and referrer data
- Cloudflare KV storage for persistence
- Instant redirects via edge network
- CORS enabled for browser usage

## Use Cases
- **Marketing Campaigns**: Track link performance across channels
- **Social Media**: Share clean, short URLs
- **Email Marketing**: Trackable links in newsletters
- **Analytics**: Measure click-through rates

## Quick Start
\`\`\`
POST /shorten
{"url": "https://example.com/very/long/path", "alias": "my-link"}
\`\`\`

## Pricing
| Plan | Price | Requests/mo | Rate Limit |
|------|-------|-------------|------------|
| **Basic (FREE)** | $0 | 100 | 1/sec |
| Pro | $9.99 | 5,000 | 10/sec |
| Ultra | $29.99 | 25,000 | 50/sec |

Free tier includes link creation and click stats. No credit card required.`
    },
    {
      name: "JSON Formatter & Validator API",
      description: "Free JSON Formatter: Validate, Minify, Diff, CSV Convert",
      long_description: `## Why JSON Formatter API?
- ✅ 6-in-1 toolkit: format, minify, validate, diff, transform, CSV convert
- ✅ JMESPath-like query support for data transformation
- ✅ Zero dependencies, sub-10ms response times

## Key Features
- Pretty-print JSON with custom indentation
- Minify JSON for production
- Validate JSON with detailed error messages
- Diff two JSON objects with change highlighting
- Convert between CSV and JSON
- JMESPath-like query/transform

## Use Cases
- **Developer Tools**: Format and validate JSON in CI/CD pipelines
- **Data Engineering**: Convert CSV to JSON and back
- **API Development**: Compare API responses with JSON diff
- **Debugging**: Validate and pretty-print malformed JSON

## Quick Start
\`\`\`
POST /format
{"json": "{\\"key\\":\\"value\\"}", "indent": 2}
\`\`\`

## Pricing
| Plan | Price | Requests/mo | Rate Limit |
|------|-------|-------------|------------|
| **Basic (FREE)** | $0 | 500 | 1/sec |
| Pro | $9.99 | 50,000 | 10/sec |
| Ultra | $29.99 | 500,000 | 50/sec |

Free tier includes all operations. No credit card required.`
    },
    {
      name: "Hash & Encoding API",
      description: "Free Hash & Encoding: SHA256, Bcrypt, Base64, HMAC",
      long_description: `## Why Hash & Encoding API?
- ✅ All-in-one: MD5, SHA-1/256/384/512, HMAC, bcrypt, Base64, URL, HTML encoding
- ✅ Bcrypt with configurable rounds + constant-time comparison
- ✅ Cryptographically secure random byte generation

## Key Features
- Hash: MD5, SHA-1, SHA-256, SHA-384, SHA-512 (hex/base64)
- HMAC with any supported hash algorithm
- Bcrypt password hashing with configurable rounds
- Bcrypt constant-time password verification
- Encode/decode: Base64, URL, HTML, Hex
- Secure random byte generation

## Use Cases
- **Authentication**: Hash and verify passwords with bcrypt
- **Data Integrity**: Generate checksums for file verification
- **Security**: HMAC signatures for API authentication
- **Development**: Quick encoding/decoding during development

## Quick Start
\`\`\`
GET /hash?algorithm=sha256&data=hello&format=hex
\`\`\`

## Pricing
| Plan | Price | Requests/mo | Rate Limit |
|------|-------|-------------|------------|
| **Basic (FREE)** | $0 | 500 | 1/sec |
| Pro | $9.99 | 50,000 | 10/sec |
| Ultra | $29.99 | 500,000 | 50/sec |

Free tier includes all hash and encoding operations. No credit card required.`
    },
    {
      name: "Currency Exchange Rate API",
      description: "Free Currency Exchange: 30+ Currencies, ECB Data, Historical Rates",
      long_description: `## Why Currency Exchange API?
- ✅ Official ECB (European Central Bank) data — reliable and authoritative
- ✅ Historical rates back to 1999 for trend analysis
- ✅ 30+ currencies with 1-hour cache for real-time accuracy

## Key Features
- 30+ currencies from ECB official feed
- Real-time exchange rates with 1-hour caching
- Currency conversion with amount calculation
- Historical rates back to 1999
- Latest rates endpoint for dashboards

## Use Cases
- **E-commerce**: Display prices in local currencies
- **Finance Apps**: Real-time currency conversion widgets
- **Accounting**: Historical rate lookups for bookkeeping
- **Travel Apps**: Multi-currency converters

## Quick Start
\`\`\`
GET /convert?from=USD&to=EUR&amount=100
\`\`\`

## Pricing
| Plan | Price | Requests/mo | Rate Limit |
|------|-------|-------------|------------|
| **Basic (FREE)** | $0 | 500 | 1/sec |
| Pro | $9.99 | 50,000 | 10/sec |
| Ultra | $29.99 | 500,000 | 50/sec |

Free tier includes all conversion features. No credit card required.`
    },
    {
      name: "AI Text API",
      description: "Free AI Text Generation: Summarize, Translate, Sentiment Analysis",
      long_description: `## Why AI Text API?
- ✅ Powered by Cloudflare Workers AI (Llama 3.1) — no external API keys needed
- ✅ 5-in-1: Generate, summarize, translate, sentiment, rewrite
- ✅ Serverless edge inference for low latency worldwide

## Key Features
- Text generation with customizable prompts
- Summarization of long documents
- Translation across multiple languages
- Sentiment analysis with confidence scores
- Text rewriting with tone control

## Use Cases
- **Content Creation**: Generate blog posts, product descriptions, social media
- **Customer Support**: Summarize tickets and detect sentiment
- **Localization**: Translate content for international markets
- **SEO**: Rewrite content for freshness and uniqueness

## Quick Start
\`\`\`
POST /generate
{"prompt": "Write a product description for...", "max_tokens": 500}
\`\`\`

## Pricing
| Plan | Price | Requests/mo | Rate Limit |
|------|-------|-------------|------------|
| **Basic (FREE)** | $0 | 100 | 1/sec |
| Pro | $9.99 | 5,000 | 10/sec |
| Ultra | $29.99 | 25,000 | 50/sec |

Free tier includes all AI features. No credit card required.`
    },
    {
      name: "Social Video Downloader API",
      description: "Free Social Video Downloader: TikTok, YouTube, Instagram",
      long_description: `## Why Social Video Downloader API?
- ✅ Multi-platform: TikTok, YouTube, Instagram, Twitter/X, Facebook
- ✅ Extracts direct download URLs without watermarks (where available)
- ✅ No scraping libraries — parses public HTML for reliability

## Key Features
- TikTok video download (with/without watermark)
- YouTube video URL extraction
- Instagram Reels and posts
- Twitter/X video extraction
- Facebook video download

## Use Cases
- **Content Repurposing**: Download and re-edit social media content
- **Archiving**: Save important social media videos
- **Analytics Tools**: Extract video metadata for analysis
- **Media Monitoring**: Track and archive brand mentions

## Quick Start
\`\`\`
GET /download?url=https://www.tiktok.com/@user/video/123456
\`\`\`

## Pricing
| Plan | Price | Requests/mo | Rate Limit |
|------|-------|-------------|------------|
| **Basic (FREE)** | $0 | 100 | 1/sec |
| Pro | $9.99 | 5,000 | 10/sec |
| Ultra | $29.99 | 25,000 | 50/sec |

Free tier includes all platforms. No credit card required.`
    },
    {
      name: "Crypto Data API",
      description: "Free Crypto Data: Bitcoin, Ethereum, Real-time Prices, Market Data",
      long_description: `## Why Crypto Data API?
- ✅ Real-time prices for Bitcoin, Ethereum, and 100+ cryptocurrencies
- ✅ Market data: market cap, volume, price change, circulating supply
- ✅ Trending coins and historical price data included

## Key Features
- Real-time cryptocurrency prices (USD, EUR, JPY, etc.)
- Market cap, 24h volume, price change percentages
- Trending/top coins rankings
- Historical price data
- Multi-currency support

## Use Cases
- **Portfolio Trackers**: Display real-time crypto holdings value
- **Trading Bots**: Feed price data into automated strategies
- **News Sites**: Show live crypto tickers and market data
- **DeFi Apps**: Price feeds for decentralized applications

## Quick Start
\`\`\`
GET /prices?coins=bitcoin,ethereum&currency=usd
\`\`\`

## Pricing
| Plan | Price | Requests/mo | Rate Limit |
|------|-------|-------------|------------|
| **Basic (FREE)** | $0 | 500 | 1/sec |
| Pro | $9.99 | 50,000 | 10/sec |
| Ultra | $29.99 | 500,000 | 50/sec |

Free tier includes all price and market data. No credit card required.`
    },
    {
      name: "SEO Analyzer API",
      description: "Free SEO Analyzer: Meta Tags, Headings, Structured Data, Score 0-100",
      long_description: `## Why SEO Analyzer API?
- ✅ Comprehensive on-page audit: meta tags, headings, links, structured data
- ✅ SEO score 0-100 with actionable improvement recommendations
- ✅ Checks Open Graph, Twitter Card, robots.txt, and canonical tags

## Key Features
- Meta title/description analysis with length validation
- Heading structure analysis (H1-H6)
- Internal/external link counting and analysis
- Structured data (Schema.org) detection
- Open Graph and Twitter Card validation
- SEO score 0-100 with recommendations

## Use Cases
- **SEO Agencies**: Automated on-page audits for clients
- **Content Teams**: Pre-publish SEO checklist validation
- **Developers**: SEO monitoring in CI/CD pipelines
- **Marketers**: Competitive analysis of competitor pages

## Quick Start
\`\`\`
GET /analyze?url=https://example.com
\`\`\`
Returns JSON with \`score\`, \`meta\`, \`headings\`, \`links\`, \`structured_data\`, \`recommendations\`.

## Pricing
| Plan | Price | Requests/mo | Rate Limit |
|------|-------|-------------|------------|
| **Basic (FREE)** | $0 | 100 | 1/sec |
| Pro | $9.99 | 5,000 | 10/sec |
| Ultra | $29.99 | 25,000 | 50/sec |

Free tier includes full SEO analysis. No credit card required.`
    },
    {
      name: "Weather API",
      description: "Free Weather API: Forecast, Hourly, Historical, Geocoding",
      long_description: `## Why Weather API?
- ✅ Current weather + daily forecast (16 days) + hourly forecast
- ✅ Geocoding included — search by city name, not just coordinates
- ✅ Historical weather data for trend analysis

## Key Features
- Current weather conditions (temperature, humidity, wind, etc.)
- Daily forecast up to 16 days
- Hourly forecast
- Geocoding (city name to coordinates)
- Historical weather data
- Multiple units (metric/imperial)

## Use Cases
- **Travel Apps**: Weather forecasts for trip planning
- **Agriculture**: Historical weather data for crop planning
- **Event Planning**: Weather predictions for outdoor events
- **IoT Dashboards**: Real-time weather monitoring

## Quick Start
\`\`\`
GET /current?city=Tokyo&units=metric
\`\`\`

## Pricing
| Plan | Price | Requests/mo | Rate Limit |
|------|-------|-------------|------------|
| **Basic (FREE)** | $0 | 500 | 1/sec |
| Pro | $9.99 | 50,000 | 10/sec |
| Ultra | $29.99 | 500,000 | 50/sec |

Free tier includes current weather and 3-day forecast. No credit card required.`
    },
    {
      name: "WHOIS Domain API",
      description: "Free WHOIS Domain: RDAP, DNS Records, Availability Check",
      long_description: `## Why WHOIS Domain API?
- ✅ WHOIS + RDAP + DNS records + availability check in one API
- ✅ Structured JSON output (not raw WHOIS text)
- ✅ Supports all major TLDs with registrar and expiry info

## Key Features
- WHOIS/RDAP domain lookup with structured output
- DNS records query (A, AAAA, MX, NS, TXT, CNAME, SOA)
- Domain availability check
- Registrar, creation/expiry dates, nameservers
- SSL certificate information

## Use Cases
- **Domain Tools**: Build domain lookup and monitoring tools
- **Security**: Investigate suspicious domains and phishing
- **Brand Protection**: Monitor domain registrations for your brand
- **SEO Tools**: Check domain age and authority signals

## Quick Start
\`\`\`
GET /lookup?domain=example.com
\`\`\`

## Pricing
| Plan | Price | Requests/mo | Rate Limit |
|------|-------|-------------|------------|
| **Basic (FREE)** | $0 | 100 | 1/sec |
| Pro | $9.99 | 5,000 | 10/sec |
| Ultra | $29.99 | 25,000 | 50/sec |

Free tier includes all lookup features. No credit card required.`
    },
    {
      name: "News Aggregator API",
      description: "Free News Aggregator: BBC, HN, Dev.to, Tech News, RSS Feed",
      long_description: `## Why News Aggregator API?
- ✅ Multi-source: BBC, NYT, Reuters, TechCrunch, Hacker News, Dev.to
- ✅ Category and source filtering for targeted news feeds
- ✅ RSS parsing with structured JSON output

## Key Features
- Aggregated headlines from 6+ major sources
- Category filtering (tech, business, world, etc.)
- Source-specific endpoints
- Hacker News top/new/best stories
- Dev.to trending articles
- Structured JSON with title, URL, date, source

## Use Cases
- **News Apps**: Build custom news aggregator applications
- **Dashboards**: Real-time news feeds for monitoring tools
- **Chatbots**: Serve latest news in conversational interfaces
- **Research**: Track industry news and trends

## Quick Start
\`\`\`
GET /headlines?source=bbc&category=technology
\`\`\`

## Pricing
| Plan | Price | Requests/mo | Rate Limit |
|------|-------|-------------|------------|
| **Basic (FREE)** | $0 | 500 | 1/sec |
| Pro | $9.99 | 50,000 | 10/sec |
| Ultra | $29.99 | 500,000 | 50/sec |

Free tier includes all sources and categories. No credit card required.`
    },
    {
      name: "AI Translate API",
      description: "Free AI Translation: 40+ Languages, Detection, Batch Support",
      long_description: `## Why AI Translation API?
- ✅ 40+ languages powered by Cloudflare Workers AI (M2M100)
- ✅ Auto language detection — no need to specify source language
- ✅ Batch translation for multiple texts in one request

## Key Features
- 40+ language pairs
- Automatic source language detection
- Batch translation (multiple texts per request)
- Preserves formatting and structure
- Edge-based AI inference for low latency

## Use Cases
- **Localization**: Translate app content for international markets
- **Customer Support**: Real-time message translation
- **Content Marketing**: Multi-language blog posts and social media
- **E-commerce**: Translate product descriptions and reviews

## Quick Start
\`\`\`
POST /translate
{"text": "Hello, world!", "target": "es"}
\`\`\`
Returns \`{"translated": "¡Hola, mundo!", "detected_language": "en"}\`.

## Pricing
| Plan | Price | Requests/mo | Rate Limit |
|------|-------|-------------|------------|
| **Basic (FREE)** | $0 | 100 | 1/sec |
| Pro | $9.99 | 5,000 | 10/sec |
| Ultra | $29.99 | 25,000 | 50/sec |

Free tier includes all languages and detection. No credit card required.`
    },
    {
      name: "Trends Aggregator API",
      description: "Free Trends Aggregator: Google, HN, Reddit, GitHub, Product Hunt",
      long_description: `## Why Trends Aggregator API?
- ✅ 5 platforms in 1: Google Trends, Hacker News, Reddit, GitHub, Product Hunt
- ✅ Real-time trending topics across tech, business, and culture
- ✅ Structured JSON with rankings, scores, and URLs

## Key Features
- Google Trends daily/real-time trending searches
- Hacker News top stories and trending posts
- Reddit trending subreddits and posts
- GitHub trending repositories
- Product Hunt daily top products

## Use Cases
- **Content Strategy**: Find trending topics for blog posts and social media
- **Market Research**: Track emerging technologies and products
- **News Dashboards**: Multi-platform trend monitoring
- **SEO**: Capitalize on trending search queries

## Quick Start
\`\`\`
GET /trends?source=google&geo=US
\`\`\`

## Pricing
| Plan | Price | Requests/mo | Rate Limit |
|------|-------|-------------|------------|
| **Basic (FREE)** | $0 | 500 | 1/sec |
| Pro | $9.99 | 50,000 | 10/sec |
| Ultra | $29.99 | 500,000 | 50/sec |

Free tier includes all sources. No credit card required.`
    },
    {
      name: "Company Data API",
      description: "Free Company Data: Enrichment, Domain Lookup, Business Search",
      long_description: `## Why Company Data API?
- ✅ Enrich company data from public sources (Wikidata, web scraping)
- ✅ Domain-based lookup — just provide a website URL
- ✅ Company search by name with fuzzy matching

## Key Features
- Company search by name
- Domain-based company lookup
- Industry, employee count, revenue data
- Founded date, headquarters, description
- Social media profiles and website
- Wikidata integration for verified data

## Use Cases
- **Sales Teams**: Enrich CRM records with company data
- **Lead Generation**: Research prospects before outreach
- **Market Research**: Analyze companies in target industries
- **Due Diligence**: Quick company background checks

## Quick Start
\`\`\`
GET /search?name=Anthropic
\`\`\`

## Pricing
| Plan | Price | Requests/mo | Rate Limit |
|------|-------|-------------|------------|
| **Basic (FREE)** | $0 | 100 | 1/sec |
| Pro | $9.99 | 5,000 | 10/sec |
| Ultra | $29.99 | 25,000 | 50/sec |

Free tier includes all search and enrichment features. No credit card required.`
    },
    {
      name: "WP Internal Link Optimization API",
      description: "Free WP SEO: Internal Link Optimizer, Sitemap Analysis",
      long_description: `## Why WP Internal Link API?
- ✅ AI-powered internal link suggestions for WordPress articles
- ✅ Analyzes content relevance and anchor text optimization
- ✅ Sitemap parsing for comprehensive link opportunity discovery

## Key Features
- Internal link opportunity detection
- Anchor text suggestions based on content relevance
- WordPress sitemap analysis
- Link density and distribution scoring
- Orphan page detection
- SEO impact estimation

## Use Cases
- **WordPress Bloggers**: Optimize internal linking structure
- **SEO Agencies**: Automated internal link audits for clients
- **Content Teams**: Discover linking opportunities between articles
- **Site Migration**: Map internal links during redesigns

## Quick Start
\`\`\`
POST /analyze
{"content": "<article HTML>", "sitemap_url": "https://example.com/sitemap.xml"}
\`\`\`

## Pricing
| Plan | Price | Requests/mo | Rate Limit |
|------|-------|-------------|------------|
| **Basic (FREE)** | $0 | 100 | 1/sec |
| Pro | $9.99 | 5,000 | 10/sec |
| Ultra | $29.99 | 25,000 | 50/sec |

Free tier includes full analysis. No credit card required.`
    },
    {
      name: "PDF Generator API",
      description: "Free PDF Generator: HTML/Markdown/URL to PDF, Custom Layout",
      long_description: `## Why PDF Generator API?
- ✅ 3 input formats: HTML, Markdown, and URL — convert anything to PDF
- ✅ Custom page size, margins, headers, footers, and orientation
- ✅ Serverless generation on Cloudflare edge — no queue, instant results

## Key Features
- HTML to PDF with CSS support
- Markdown to PDF with styling
- URL to PDF (capture webpage as PDF)
- Custom page size (A4, Letter, etc.)
- Configurable margins, headers, and footers
- Landscape/portrait orientation

## Use Cases
- **Invoicing**: Generate PDF invoices from HTML templates
- **Reports**: Convert dashboards and reports to PDF
- **Documentation**: Markdown docs to printable PDFs
- **Archiving**: Save webpages as PDF documents

## Quick Start
\`\`\`
POST /generate
{"html": "<h1>Invoice</h1><p>Total: $100</p>", "format": "A4"}
\`\`\`

## Pricing
| Plan | Price | Requests/mo | Rate Limit |
|------|-------|-------------|------------|
| **Basic (FREE)** | $0 | 100 | 1/sec |
| Pro | $9.99 | 5,000 | 10/sec |
| Ultra | $29.99 | 25,000 | 50/sec |

Free tier includes all input formats. No credit card required.`
    },
    {
      name: "Placeholder Image API",
      description: "Free Placeholder Image: SVG/PNG, Gradients, Custom Text",
      long_description: `## Why Placeholder Image API?
- ✅ SVG and PNG output with 10 stunning gradient presets
- ✅ Custom text overlay, font size, and colors
- ✅ 8 category presets (avatar, banner, thumbnail, hero, etc.)

## Key Features
- Custom width & height (up to 4000x4000)
- Text overlay with configurable font and color
- 10 gradient presets (blue, sunset, ocean, forest, fire, etc.)
- Custom gradient colors (any hex pair)
- 8 category presets for common sizes
- SVG and PNG output formats

## Use Cases
- **Web Development**: Placeholder images during development
- **UI/UX Design**: Mockups and wireframe images
- **Social Media**: Template images for posts
- **App Prototyping**: Dynamic placeholder images

## Quick Start
\`\`\`
GET /image?width=800&height=400&text=Hello&gradient=sunset&format=svg
\`\`\`

## Pricing
| Plan | Price | Requests/mo | Rate Limit |
|------|-------|-------------|------------|
| **Basic (FREE)** | $0 | 100 | 1/sec |
| Pro | $9.99 | 5,000 | 10/sec |
| Ultra | $29.99 | 25,000 | 50/sec |

Free tier includes all formats and presets. No credit card required.`
    },
    {
      name: "Markdown Converter API",
      description: "Free Markdown Converter: HTML to Markdown, TOC, GFM Support",
      long_description: `## Why Markdown Converter API?
- ✅ Bidirectional: Markdown→HTML and HTML→Markdown
- ✅ Full GFM support: tables, task lists, strikethrough, code blocks
- ✅ Auto-generated Table of Contents with anchor links

## Key Features
- Markdown to HTML conversion (full GFM support)
- HTML to Markdown reverse conversion
- Table of Contents auto-generation
- Syntax highlighting CSS classes for code blocks
- Tables, task lists, strikethrough support
- Pure JavaScript — no external dependencies

## Use Cases
- **CMS Platforms**: Render Markdown content as HTML
- **Documentation Sites**: Auto-generate navigation from headings
- **Static Site Generators**: Markdown processing pipeline
- **Editor Plugins**: Live Markdown preview

## Quick Start
\`\`\`
POST /convert
{"markdown": "# Hello\\n\\nThis is **bold** text.", "toc": true}
\`\`\`

## Pricing
| Plan | Price | Requests/mo | Rate Limit |
|------|-------|-------------|------------|
| **Basic (FREE)** | $0 | 500 | 1/sec |
| Pro | $9.99 | 50,000 | 10/sec |
| Ultra | $29.99 | 500,000 | 50/sec |

Free tier includes all conversion features. No credit card required.`
    }
  ];

  // === ユーティリティ関数 ===
  const sleep = (ms) => new Promise(resolve => setTimeout(resolve, ms));

  // Reactのtextareaに値をセットする関数
  function setReactTextareaValue(textarea, value) {
    const nativeInputValueSetter = Object.getOwnPropertyDescriptor(
      window.HTMLTextAreaElement.prototype, 'value'
    ).set;
    nativeInputValueSetter.call(textarea, value);
    textarea.dispatchEvent(new Event('input', { bubbles: true }));
    textarea.dispatchEvent(new Event('change', { bubbles: true }));
    textarea.dispatchEvent(new Event('blur', { bubbles: true }));
  }

  // Reactのinputに値をセットする関数
  function setReactInputValue(input, value) {
    const nativeInputValueSetter = Object.getOwnPropertyDescriptor(
      window.HTMLInputElement.prototype, 'value'
    ).set;
    nativeInputValueSetter.call(input, value);
    input.dispatchEvent(new Event('input', { bubbles: true }));
    input.dispatchEvent(new Event('change', { bubbles: true }));
    input.dispatchEvent(new Event('blur', { bubbles: true }));
  }

  // 名前の部分一致マッチング（単語レベル）
  function matchApiName(studioName, jsonName) {
    const normalize = (s) => s.toLowerCase().replace(/[^a-z0-9\s]/g, '').trim();
    const a = normalize(studioName);
    const b = normalize(jsonName);
    // 完全一致
    if (a === b) return 1.0;
    // 片方が片方を含む
    if (a.includes(b) || b.includes(a)) return 0.9;
    // 単語の重複率
    const wordsA = new Set(a.split(/\s+/));
    const wordsB = new Set(b.split(/\s+/));
    const intersection = [...wordsA].filter(w => wordsB.has(w));
    const score = intersection.length / Math.max(wordsA.size, wordsB.size);
    return score;
  }

  // === メイン処理 ===
  console.log('=== RapidAPI Studio リスティング一括更新 開始 ===');
  console.log(`更新対象: ${API_DATA.length} API`);

  // Step 1: Studioトップページから全APIカードのリンクを収集
  console.log('\n[Step 1] APIカードのリンクを収集中...');

  // APIカードのリンクを探す（複数のセレクタを試行）
  const cardSelectors = [
    'a[href*="/studio/"][href*="/hub-listing"]',
    'a[href*="/studio/"][href*="/general"]',
    'a[href*="/studio/"]',
    '[data-testid] a',
    '.api-card a',
    'a[href*="/api/"]'
  ];

  let apiCards = [];
  for (const selector of cardSelectors) {
    const found = document.querySelectorAll(selector);
    if (found.length > 0) {
      apiCards = [...found];
      console.log(`  セレクタ "${selector}" で ${found.length} 件発見`);
      break;
    }
  }

  // カードが見つからない場合、ページ内の全リンクからStudio系URLを抽出
  if (apiCards.length === 0) {
    console.log('  カードセレクタでは見つからず。全リンクからStudio URLを検索...');
    const allLinks = document.querySelectorAll('a[href]');
    const studioLinks = [...allLinks].filter(a => {
      const href = a.getAttribute('href') || '';
      return href.includes('/studio/') && href !== '/studio/' && !href.endsWith('/studio/');
    });
    apiCards = studioLinks;
    console.log(`  Studio関連リンク: ${studioLinks.length} 件`);
  }

  // APIカードからURLとAPI名を抽出
  const apiEntries = [];
  const seenUrls = new Set();

  for (const card of apiCards) {
    let href = card.getAttribute('href') || '';
    if (!href.startsWith('http')) {
      href = window.location.origin + href;
    }
    // 重複除外
    const baseUrl = href.split('?')[0].replace(/\/$/, '');
    if (seenUrls.has(baseUrl)) continue;
    seenUrls.add(baseUrl);

    // API名を取得（カード内のテキスト or リンクテキスト）
    const name = card.textContent.trim() ||
                 card.querySelector('h3, h4, [class*="name"], [class*="title"]')?.textContent?.trim() ||
                 '';

    // Hub Listing URLを構築
    let hubListingUrl = baseUrl;
    if (!hubListingUrl.includes('/hub-listing')) {
      hubListingUrl = hubListingUrl.replace(/\/[^/]*$/, '') + '/hub-listing/general';
      // もしくはそのまま /hub-listing/general を付ける
      if (!hubListingUrl.includes('/hub-listing')) {
        hubListingUrl = baseUrl + '/hub-listing/general';
      }
    }

    apiEntries.push({ name, url: hubListingUrl, originalUrl: baseUrl });
  }

  console.log(`  収集完了: ${apiEntries.length} API`);

  if (apiEntries.length === 0) {
    console.error('APIカードが見つかりません。https://rapidapi.com/studio/ のトップページで実行してください。');
    console.log('代替方式: 手動でHub Listing URLリストを使用します...');

    // フォールバック: ページ遷移なしで現在のページがHub Listingなら直接更新
    console.log('\n=== 代替方式: 個別URL遷移モード ===');
    console.log('各APIのHub Listing > General ページを手動で開いて、以下を実行してください:');
    console.log('updateCurrentPage("API名の一部")');

    window.updateCurrentPage = function(nameFragment) {
      const match = API_DATA.find(api =>
        api.name.toLowerCase().includes(nameFragment.toLowerCase()) ||
        nameFragment.toLowerCase().includes(api.name.toLowerCase().split(' ')[0])
      );
      if (!match) {
        console.error(`"${nameFragment}" に一致するAPIが見つかりません`);
        return;
      }
      console.log(`更新: ${match.name}`);
      updatePageFields(match);
    };
    return;
  }

  // Step 2: 各APIのHub Listingページに遷移して更新
  let successCount = 0;
  let errorCount = 0;
  let skipCount = 0;

  for (let i = 0; i < apiEntries.length; i++) {
    const entry = apiEntries[i];
    console.log(`\n[${i + 1}/${apiEntries.length}] ${entry.name || entry.originalUrl}`);

    // API_DATAとマッチング
    let bestMatch = null;
    let bestScore = 0;

    for (const apiData of API_DATA) {
      const score = matchApiName(entry.name, apiData.name);
      if (score > bestScore) {
        bestScore = score;
        bestMatch = apiData;
      }
    }

    if (bestScore < 0.3 || !bestMatch) {
      console.warn(`  スキップ: マッチするAPIデータなし (best score: ${bestScore.toFixed(2)})`);
      skipCount++;
      continue;
    }

    console.log(`  マッチ: ${bestMatch.name} (score: ${bestScore.toFixed(2)})`);

    try {
      // Hub Listingページに遷移
      console.log(`  遷移中: ${entry.url}`);
      window.location.href = entry.url;

      // ページ読み込み待機（最大15秒）
      await sleep(5000);

      // textareaが見つかるまで待機
      let retries = 0;
      let textareas = [];
      while (retries < 10) {
        textareas = document.querySelectorAll('textarea');
        if (textareas.length >= 2) break;
        // inputも含めて探す
        const inputs = document.querySelectorAll('input[type="text"], textarea');
        if (inputs.length >= 2) {
          textareas = inputs;
          break;
        }
        retries++;
        await sleep(1000);
      }

      if (textareas.length < 1) {
        console.warn(`  フィールドが見つかりません。ページ構造が異なる可能性`);
        errorCount++;
        await sleep(3000);
        continue;
      }

      await updatePageFields(bestMatch);
      successCount++;
      console.log(`  完了!`);

    } catch (err) {
      console.error(`  エラー: ${err.message}`);
      errorCount++;
    }

    // 次のAPIに進む前に待機
    if (i < apiEntries.length - 1) {
      console.log('  3秒待機...');
      await sleep(3000);
    }
  }

  console.log('\n=== 更新完了 ===');
  console.log(`成功: ${successCount} / スキップ: ${skipCount} / エラー: ${errorCount} / 合計: ${apiEntries.length}`);

  // === ページ内フィールド更新関数 ===
  async function updatePageFields(apiData) {
    // Short Description: 最初のtextareaまたはdescription関連のフィールド
    const allTextareas = document.querySelectorAll('textarea');
    const allInputs = document.querySelectorAll('input[type="text"]');

    // ラベルやplaceholderからフィールドを特定
    let shortDescField = null;
    let longDescField = null;

    // textareaを走査してShort/Long Descriptionを特定
    for (const ta of allTextareas) {
      const label = ta.closest('label')?.textContent?.toLowerCase() ||
                    ta.getAttribute('placeholder')?.toLowerCase() ||
                    ta.getAttribute('name')?.toLowerCase() ||
                    ta.getAttribute('aria-label')?.toLowerCase() || '';

      // 親要素のラベルテキストも確認
      const parent = ta.parentElement;
      const parentText = parent?.querySelector('label, span, div')?.textContent?.toLowerCase() || '';
      const combinedLabel = label + ' ' + parentText;

      if (combinedLabel.includes('short') || combinedLabel.includes('summary')) {
        shortDescField = ta;
      } else if (combinedLabel.includes('long') || combinedLabel.includes('description') || combinedLabel.includes('about')) {
        longDescField = ta;
      }
    }

    // ラベルで特定できなかった場合、順番で判断（1番目=Short, 2番目=Long）
    if (!shortDescField && allTextareas.length >= 1) {
      shortDescField = allTextareas[0];
    }
    if (!longDescField && allTextareas.length >= 2) {
      longDescField = allTextareas[1];
    }

    // Short Description 更新
    if (shortDescField) {
      console.log(`  Short Description を更新中...`);
      setReactTextareaValue(shortDescField, apiData.description);
      await sleep(500);
    } else {
      console.warn(`  Short Description フィールドが見つかりません`);
    }

    // Long Description 更新
    if (longDescField) {
      console.log(`  Long Description を更新中...`);
      setReactTextareaValue(longDescField, apiData.long_description);
      await sleep(500);
    } else {
      console.warn(`  Long Description フィールドが見つかりません`);
    }

    // 保存ボタンを探してクリック
    const saveSelectors = [
      'button[type="submit"]',
      'button:not([disabled])',
      '[data-testid*="save"]',
      'button'
    ];

    for (const selector of saveSelectors) {
      const buttons = document.querySelectorAll(selector);
      for (const btn of buttons) {
        const text = btn.textContent.trim().toLowerCase();
        if (text === 'save' || text === 'save changes' || text === 'update' || text === 'submit') {
          console.log(`  保存ボタンをクリック: "${btn.textContent.trim()}"`);
          btn.click();
          await sleep(2000);
          return;
        }
      }
    }

    console.warn(`  保存ボタンが見つかりません（手動で保存が必要な場合があります）`);
  }

})();
