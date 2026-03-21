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
      long_description: "## Why QR Code Generator API?\n- ✅ Zero authentication required — start generating QR codes instantly\n- ✅ 3 output formats (PNG, SVG, Base64) with full color customization\n- ✅ Sub-50ms response via Cloudflare's global edge network (300+ locations)\n\n## Key Features\n- PNG, SVG, and Base64 output formats\n- Custom foreground & background colors (hex)\n- Adjustable error correction levels (L/M/Q/H)\n- Configurable size from 10px to 1000px\n- CORS enabled for browser-side usage\n\n## Use Cases\n- **E-commerce**: QR codes for product pages, payments, and receipts\n- **Marketing**: Flyers, business cards, and poster campaigns\n- **Event Management**: Ticket QR codes and check-in systems\n- **Mobile Apps**: Deep-link QR codes for app downloads\n\n## Quick Start\n``\\"
GET /generate?text=https://example.com&size=300&format=png&color=FF0000&bgcolor=FFFFFF
\"\\"\`

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
      long_description: "## Why Email Validation API?\n- ✅ Validates without sending any emails — instant, non-intrusive checks\n- ✅ 500+ disposable domain blacklist with typo correction (gmial→gmail)\n- ✅ MX record verification + RFC 5322 format validation in one call\n\n## Key Features\n- RFC 5322 format validation with detailed error messages\n- MX record verification for deliverability\n- Disposable/temporary email detection (500+ domains)\n- Typo correction suggestions\n- Bulk validation up to 50 emails per request (Pro+)\n\n## Use Cases\n- **SaaS Signups**: Block disposable emails at registration\n- **Email Marketing**: Clean mailing lists before campaigns\n- **E-commerce**: Reduce failed order confirmation emails\n- **Lead Generation**: Ensure collected emails are valid\n\n## Quick Start\n``\\"
GET /validate?email=user@example.com
\"\\"\`
Returns JSON with \"is_valid\\", \"is_disposable\\", \"has_mx\\", \"suggestion\\", and more.

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
      long_description: "## Why Link Preview API?\n- ✅ Extracts Open Graph, Twitter Card, favicon, RSS, and author in one call\n- ✅ 1-hour smart caching for blazing-fast repeat requests\n- ✅ CORS enabled — use directly from browser-based applications\n\n## Key Features\n- Open Graph and Twitter Card metadata extraction\n- Favicon, RSS feed, and author detection\n- Bulk preview for up to 10 URLs per request\n- 1-hour smart caching\n- CORS enabled for direct browser usage\n\n## Use Cases\n- **Chat Applications**: Rich link previews like Slack and Discord\n- **Social Media Tools**: Preview how URLs appear when shared\n- **SEO Auditing**: Check Open Graph and meta tag implementation\n- **Content Aggregators**: Extract titles, descriptions, and images\n\n## Quick Start\n``\\"
GET /preview?url=https://github.com
\"\\"\`
Returns JSON with \"title\\", \"description\\", \"image\\", \"favicon\\", \"og_tags\\", \"twitter_card\\".

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
      long_description: "## Why Website Screenshot API?\n- ✅ Capture any public URL as PNG or JPEG with custom viewport sizes\n- ✅ Full-page capture mode for long scrolling pages\n- ✅ Configurable delay for JavaScript-heavy sites\n\n## Key Features\n- PNG and JPEG output formats with quality control\n- Custom viewport width and height\n- Full-page screenshot support\n- Configurable render delay for dynamic content\n- 1-hour result caching\n- CORS enabled\n\n## Use Cases\n- **SEO Monitoring**: Visual regression testing for websites\n- **Social Sharing**: Generate thumbnails and OG images\n- **Archiving**: Capture webpage snapshots for records\n- **QA Testing**: Automated visual testing across viewports\n\n## Quick Start\n``\\"
GET /capture?url=https://example.com&width=1280&height=720&format=png
\"\\"\`

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
      long_description: "## Why Text Analysis API?\n- ✅ Pure JavaScript NLP — no external AI dependencies, no rate limits from third parties\n- ✅ 6-in-1: Sentiment, keywords, readability, language detection, summarization, metrics\n- ✅ AFINN lexicon with negation handling + TF-IDF keyword extraction\n\n## Key Features\n- Sentiment analysis with confidence score (AFINN-style, 200+ words)\n- TF-IDF keyword extraction (top 10 ranked)\n- Flesch-Kincaid readability scoring\n- Language detection (10 languages)\n- Extractive summarization (TextRank-inspired)\n- Word/character/sentence/paragraph counts + reading time\n\n## Use Cases\n- **Content Marketing**: Analyze sentiment and readability before publishing\n- **Social Listening**: Monitor brand sentiment across text data\n- **SEO Tools**: Extract keywords and optimize content\n- **Chatbots**: Detect language and sentiment in user messages\n\n## Quick Start\n``\\"
POST /analyze
{"text": "Your text here", "features": ["sentiment", "keywords", "readability"]}
\"\\"\`

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
      long_description: "## Why IP Geolocation API?\n- ✅ VPN/proxy/datacenter detection built-in for fraud prevention\n- ✅ Bulk lookup up to 20 IPs per request + auto-detect caller's IP\n- ✅ Country, city, region, timezone, ISP, and ASN in one call\n\n## Key Features\n- IPv4 and IPv6 support\n- Country, city, region, latitude/longitude\n- Timezone and ISP/ASN information\n- VPN, proxy, and datacenter detection\n- Bulk lookup (up to 20 IPs)\n- Caller's own IP auto-detection\n\n## Use Cases\n- **Fraud Prevention**: Detect VPN/proxy usage in transactions\n- **Content Localization**: Serve region-specific content\n- **Analytics**: Enrich user data with geographic info\n- **Access Control**: Geo-restrict content by country\n\n## Quick Start\n``\\"
GET /lookup?ip=8.8.8.8
\"\\"\`
Returns JSON with \"country\\", \"city\\", \"region\\", \"timezone\\", \"isp\\", \"is_vpn\\", \"is_proxy\\".

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
      long_description: "## Why URL Shortener API?\n- ✅ Custom aliases + click analytics with timestamps\n- ✅ Persistent storage via Cloudflare KV — links never expire\n- ✅ Zero external dependencies, ultra-fast redirects\n\n## Key Features\n- Create short URLs with custom aliases\n- Click tracking with timestamps and referrer data\n- Cloudflare KV storage for persistence\n- Instant redirects via edge network\n- CORS enabled for browser usage\n\n## Use Cases\n- **Marketing Campaigns**: Track link performance across channels\n- **Social Media**: Share clean, short URLs\n- **Email Marketing**: Trackable links in newsletters\n- **Analytics**: Measure click-through rates\n\n## Quick Start\n``\\"
POST /shorten
{"url": "https://example.com/very/long/path", "alias": "my-link"}
\"\\"\`

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
      long_description: "## Why JSON Formatter API?\n- ✅ 6-in-1 toolkit: format, minify, validate, diff, transform, CSV convert\n- ✅ JMESPath-like query support for data transformation\n- ✅ Zero dependencies, sub-10ms response times\n\n## Key Features\n- Pretty-print JSON with custom indentation\n- Minify JSON for production\n- Validate JSON with detailed error messages\n- Diff two JSON objects with change highlighting\n- Convert between CSV and JSON\n- JMESPath-like query/transform\n\n## Use Cases\n- **Developer Tools**: Format and validate JSON in CI/CD pipelines\n- **Data Engineering**: Convert CSV to JSON and back\n- **API Development**: Compare API responses with JSON diff\n- **Debugging**: Validate and pretty-print malformed JSON\n\n## Quick Start\n``\\"
POST /format
{"json": "{\\"key\\":\\"value\\"}", "indent": 2}
\"\\"\`

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
      long_description: "## Why Hash & Encoding API?\n- ✅ All-in-one: MD5, SHA-1/256/384/512, HMAC, bcrypt, Base64, URL, HTML encoding\n- ✅ Bcrypt with configurable rounds + constant-time comparison\n- ✅ Cryptographically secure random byte generation\n\n## Key Features\n- Hash: MD5, SHA-1, SHA-256, SHA-384, SHA-512 (hex/base64)\n- HMAC with any supported hash algorithm\n- Bcrypt password hashing with configurable rounds\n- Bcrypt constant-time password verification\n- Encode/decode: Base64, URL, HTML, Hex\n- Secure random byte generation\n\n## Use Cases\n- **Authentication**: Hash and verify passwords with bcrypt\n- **Data Integrity**: Generate checksums for file verification\n- **Security**: HMAC signatures for API authentication\n- **Development**: Quick encoding/decoding during development\n\n## Quick Start\n``\\"
GET /hash?algorithm=sha256&data=hello&format=hex
\"\\"\`

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
      long_description: "## Why Currency Exchange API?\n- ✅ Official ECB (European Central Bank) data — reliable and authoritative\n- ✅ Historical rates back to 1999 for trend analysis\n- ✅ 30+ currencies with 1-hour cache for real-time accuracy\n\n## Key Features\n- 30+ currencies from ECB official feed\n- Real-time exchange rates with 1-hour caching\n- Currency conversion with amount calculation\n- Historical rates back to 1999\n- Latest rates endpoint for dashboards\n\n## Use Cases\n- **E-commerce**: Display prices in local currencies\n- **Finance Apps**: Real-time currency conversion widgets\n- **Accounting**: Historical rate lookups for bookkeeping\n- **Travel Apps**: Multi-currency converters\n\n## Quick Start\n``\\"
GET /convert?from=USD&to=EUR&amount=100
\"\\"\`

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
      long_description: "## Why AI Text API?\n- ✅ Powered by Cloudflare Workers AI (Llama 3.1) — no external API keys needed\n- ✅ 5-in-1: Generate, summarize, translate, sentiment, rewrite\n- ✅ Serverless edge inference for low latency worldwide\n\n## Key Features\n- Text generation with customizable prompts\n- Summarization of long documents\n- Translation across multiple languages\n- Sentiment analysis with confidence scores\n- Text rewriting with tone control\n\n## Use Cases\n- **Content Creation**: Generate blog posts, product descriptions, social media\n- **Customer Support**: Summarize tickets and detect sentiment\n- **Localization**: Translate content for international markets\n- **SEO**: Rewrite content for freshness and uniqueness\n\n## Quick Start\n``\\"
POST /generate
{"prompt": "Write a product description for...", "max_tokens": 500}
\"\\"\`

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
      long_description: "## Why Social Video Downloader API?\n- ✅ Multi-platform: TikTok, YouTube, Instagram, Twitter/X, Facebook\n- ✅ Extracts direct download URLs without watermarks (where available)\n- ✅ No scraping libraries — parses public HTML for reliability\n\n## Key Features\n- TikTok video download (with/without watermark)\n- YouTube video URL extraction\n- Instagram Reels and posts\n- Twitter/X video extraction\n- Facebook video download\n\n## Use Cases\n- **Content Repurposing**: Download and re-edit social media content\n- **Archiving**: Save important social media videos\n- **Analytics Tools**: Extract video metadata for analysis\n- **Media Monitoring**: Track and archive brand mentions\n\n## Quick Start\n``\\"
GET /download?url=https://www.tiktok.com/@user/video/123456
\"\\"\`

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
      long_description: "## Why Crypto Data API?\n- ✅ Real-time prices for Bitcoin, Ethereum, and 100+ cryptocurrencies\n- ✅ Market data: market cap, volume, price change, circulating supply\n- ✅ Trending coins and historical price data included\n\n## Key Features\n- Real-time cryptocurrency prices (USD, EUR, JPY, etc.)\n- Market cap, 24h volume, price change percentages\n- Trending/top coins rankings\n- Historical price data\n- Multi-currency support\n\n## Use Cases\n- **Portfolio Trackers**: Display real-time crypto holdings value\n- **Trading Bots**: Feed price data into automated strategies\n- **News Sites**: Show live crypto tickers and market data\n- **DeFi Apps**: Price feeds for decentralized applications\n\n## Quick Start\n``\\"
GET /prices?coins=bitcoin,ethereum&currency=usd
\"\\"\`

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
      long_description: "## Why SEO Analyzer API?\n- ✅ Comprehensive on-page audit: meta tags, headings, links, structured data\n- ✅ SEO score 0-100 with actionable improvement recommendations\n- ✅ Checks Open Graph, Twitter Card, robots.txt, and canonical tags\n\n## Key Features\n- Meta title/description analysis with length validation\n- Heading structure analysis (H1-H6)\n- Internal/external link counting and analysis\n- Structured data (Schema.org) detection\n- Open Graph and Twitter Card validation\n- SEO score 0-100 with recommendations\n\n## Use Cases\n- **SEO Agencies**: Automated on-page audits for clients\n- **Content Teams**: Pre-publish SEO checklist validation\n- **Developers**: SEO monitoring in CI/CD pipelines\n- **Marketers**: Competitive analysis of competitor pages\n\n## Quick Start\n``\\"
GET /analyze?url=https://example.com
\"\\"\`
Returns JSON with \"score\\", \"meta\\", \"headings\\", \"links\\", \"structured_data\\", \"recommendations\\".

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
      long_description: "## Why Weather API?\n- ✅ Current weather + daily forecast (16 days) + hourly forecast\n- ✅ Geocoding included — search by city name, not just coordinates\n- ✅ Historical weather data for trend analysis\n\n## Key Features\n- Current weather conditions (temperature, humidity, wind, etc.)\n- Daily forecast up to 16 days\n- Hourly forecast\n- Geocoding (city name to coordinates)\n- Historical weather data\n- Multiple units (metric/imperial)\n\n## Use Cases\n- **Travel Apps**: Weather forecasts for trip planning\n- **Agriculture**: Historical weather data for crop planning\n- **Event Planning**: Weather predictions for outdoor events\n- **IoT Dashboards**: Real-time weather monitoring\n\n## Quick Start\n``\\"
GET /current?city=Tokyo&units=metric
\"\\"\`

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
      long_description: "## Why WHOIS Domain API?\n- ✅ WHOIS + RDAP + DNS records + availability check in one API\n- ✅ Structured JSON output (not raw WHOIS text)\n- ✅ Supports all major TLDs with registrar and expiry info\n\n## Key Features\n- WHOIS/RDAP domain lookup with structured output\n- DNS records query (A, AAAA, MX, NS, TXT, CNAME, SOA)\n- Domain availability check\n- Registrar, creation/expiry dates, nameservers\n- SSL certificate information\n\n## Use Cases\n- **Domain Tools**: Build domain lookup and monitoring tools\n- **Security**: Investigate suspicious domains and phishing\n- **Brand Protection**: Monitor domain registrations for your brand\n- **SEO Tools**: Check domain age and authority signals\n\n## Quick Start\n``\\"
GET /lookup?domain=example.com
\"\\"\`

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
      long_description: "## Why News Aggregator API?\n- ✅ Multi-source: BBC, NYT, Reuters, TechCrunch, Hacker News, Dev.to\n- ✅ Category and source filtering for targeted news feeds\n- ✅ RSS parsing with structured JSON output\n\n## Key Features\n- Aggregated headlines from 6+ major sources\n- Category filtering (tech, business, world, etc.)\n- Source-specific endpoints\n- Hacker News top/new/best stories\n- Dev.to trending articles\n- Structured JSON with title, URL, date, source\n\n## Use Cases\n- **News Apps**: Build custom news aggregator applications\n- **Dashboards**: Real-time news feeds for monitoring tools\n- **Chatbots**: Serve latest news in conversational interfaces\n- **Research**: Track industry news and trends\n\n## Quick Start\n``\\"
GET /headlines?source=bbc&category=technology
\"\\"\`

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
      long_description: "## Why AI Translation API?\n- ✅ 40+ languages powered by Cloudflare Workers AI (M2M100)\n- ✅ Auto language detection — no need to specify source language\n- ✅ Batch translation for multiple texts in one request\n\n## Key Features\n- 40+ language pairs\n- Automatic source language detection\n- Batch translation (multiple texts per request)\n- Preserves formatting and structure\n- Edge-based AI inference for low latency\n\n## Use Cases\n- **Localization**: Translate app content for international markets\n- **Customer Support**: Real-time message translation\n- **Content Marketing**: Multi-language blog posts and social media\n- **E-commerce**: Translate product descriptions and reviews\n\n## Quick Start\n``\\"
POST /translate
{"text": "Hello, world!", "target": "es"}
\"\\"\`
Returns \"{\"translated\": \"¡Hola, mundo!\", \"detected_language\": \"en\"}\\".

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
      long_description: "## Why Trends Aggregator API?\n- ✅ 5 platforms in 1: Google Trends, Hacker News, Reddit, GitHub, Product Hunt\n- ✅ Real-time trending topics across tech, business, and culture\n- ✅ Structured JSON with rankings, scores, and URLs\n\n## Key Features\n- Google Trends daily/real-time trending searches\n- Hacker News top stories and trending posts\n- Reddit trending subreddits and posts\n- GitHub trending repositories\n- Product Hunt daily top products\n\n## Use Cases\n- **Content Strategy**: Find trending topics for blog posts and social media\n- **Market Research**: Track emerging technologies and products\n- **News Dashboards**: Multi-platform trend monitoring\n- **SEO**: Capitalize on trending search queries\n\n## Quick Start\n``\\"
GET /trends?source=google&geo=US
\"\\"\`

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
      long_description: "## Why Company Data API?\n- ✅ Enrich company data from public sources (Wikidata, web scraping)\n- ✅ Domain-based lookup — just provide a website URL\n- ✅ Company search by name with fuzzy matching\n\n## Key Features\n- Company search by name\n- Domain-based company lookup\n- Industry, employee count, revenue data\n- Founded date, headquarters, description\n- Social media profiles and website\n- Wikidata integration for verified data\n\n## Use Cases\n- **Sales Teams**: Enrich CRM records with company data\n- **Lead Generation**: Research prospects before outreach\n- **Market Research**: Analyze companies in target industries\n- **Due Diligence**: Quick company background checks\n\n## Quick Start\n``\\"
GET /search?name=Anthropic
\"\\"\`

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
      long_description: "## Why WP Internal Link API?\n- ✅ AI-powered internal link suggestions for WordPress articles\n- ✅ Analyzes content relevance and anchor text optimization\n- ✅ Sitemap parsing for comprehensive link opportunity discovery\n\n## Key Features\n- Internal link opportunity detection\n- Anchor text suggestions based on content relevance\n- WordPress sitemap analysis\n- Link density and distribution scoring\n- Orphan page detection\n- SEO impact estimation\n\n## Use Cases\n- **WordPress Bloggers**: Optimize internal linking structure\n- **SEO Agencies**: Automated internal link audits for clients\n- **Content Teams**: Discover linking opportunities between articles\n- **Site Migration**: Map internal links during redesigns\n\n## Quick Start\n``\\"
POST /analyze
{"content": "<article HTML>", "sitemap_url": "https://example.com/sitemap.xml"}
\"\\"\`

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
      long_description: "## Why PDF Generator API?\n- ✅ 3 input formats: HTML, Markdown, and URL — convert anything to PDF\n- ✅ Custom page size, margins, headers, footers, and orientation\n- ✅ Serverless generation on Cloudflare edge — no queue, instant results\n\n## Key Features\n- HTML to PDF with CSS support\n- Markdown to PDF with styling\n- URL to PDF (capture webpage as PDF)\n- Custom page size (A4, Letter, etc.)\n- Configurable margins, headers, and footers\n- Landscape/portrait orientation\n\n## Use Cases\n- **Invoicing**: Generate PDF invoices from HTML templates\n- **Reports**: Convert dashboards and reports to PDF\n- **Documentation**: Markdown docs to printable PDFs\n- **Archiving**: Save webpages as PDF documents\n\n## Quick Start\n``\\"
POST /generate
{"html": "<h1>Invoice</h1><p>Total: $100</p>", "format": "A4"}
\"\\"\`

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
      long_description: "## Why Placeholder Image API?\n- ✅ SVG and PNG output with 10 stunning gradient presets\n- ✅ Custom text overlay, font size, and colors\n- ✅ 8 category presets (avatar, banner, thumbnail, hero, etc.)\n\n## Key Features\n- Custom width & height (up to 4000x4000)\n- Text overlay with configurable font and color\n- 10 gradient presets (blue, sunset, ocean, forest, fire, etc.)\n- Custom gradient colors (any hex pair)\n- 8 category presets for common sizes\n- SVG and PNG output formats\n\n## Use Cases\n- **Web Development**: Placeholder images during development\n- **UI/UX Design**: Mockups and wireframe images\n- **Social Media**: Template images for posts\n- **App Prototyping**: Dynamic placeholder images\n\n## Quick Start\n``\\"
GET /image?width=800&height=400&text=Hello&gradient=sunset&format=svg
\"\\"\`

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
      long_description: "## Why Markdown Converter API?\n- ✅ Bidirectional: Markdown→HTML and HTML→Markdown\n- ✅ Full GFM support: tables, task lists, strikethrough, code blocks\n- ✅ Auto-generated Table of Contents with anchor links\n\n## Key Features\n- Markdown to HTML conversion (full GFM support)\n- HTML to Markdown reverse conversion\n- Table of Contents auto-generation\n- Syntax highlighting CSS classes for code blocks\n- Tables, task lists, strikethrough support\n- Pure JavaScript — no external dependencies\n\n## Use Cases\n- **CMS Platforms**: Render Markdown content as HTML\n- **Documentation Sites**: Auto-generate navigation from headings\n- **Static Site Generators**: Markdown processing pipeline\n- **Editor Plugins**: Live Markdown preview\n\n## Quick Start\n``\\"
POST /convert
{"markdown": "# Hello\\n\\nThis is **bold** text.", "toc": true}
\"\\"\`

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
  console.log("更新対象: " + API_DATA.length + " API");

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
      console.log("  セレクタ \"" + selector + "\" で " + found.length + " 件発見");
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
    console.log("  Studio関連リンク: " + studioLinks.length + " 件");
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

  console.log("  収集完了: " + apiEntries.length + " API");

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
        console.error("\"" + nameFragment + "\" に一致するAPIが見つかりません");
        return;
      }
      console.log("更新: " + match.name);
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
    console.log("\\n[" + i + 1 + "/" + apiEntries.length + "] " + entry.name || entry.originalUrl);

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
      console.warn("  スキップ: マッチするAPIデータなし (best score: " + bestScore.toFixed(2) + ")");
      skipCount++;
      continue;
    }

    console.log("  マッチ: " + bestMatch.name + " (score: " + bestScore.toFixed(2) + ")");

    try {
      // Hub Listingページに遷移
      console.log("  遷移中: " + entry.url);
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
        console.warn("  フィールドが見つかりません。ページ構造が異なる可能性");
        errorCount++;
        await sleep(3000);
        continue;
      }

      await updatePageFields(bestMatch);
      successCount++;
      console.log("  完了!");

    } catch (err) {
      console.error("  エラー: " + err.message);
      errorCount++;
    }

    // 次のAPIに進む前に待機
    if (i < apiEntries.length - 1) {
      console.log('  3秒待機...');
      await sleep(3000);
    }
  }

  console.log('\n=== 更新完了 ===');
  console.log("成功: " + successCount + " / スキップ: " + skipCount + " / エラー: " + errorCount + " / 合計: " + apiEntries.length);

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
      console.log("  Short Description を更新中...");
      setReactTextareaValue(shortDescField, apiData.description);
      await sleep(500);
    } else {
      console.warn("  Short Description フィールドが見つかりません");
    }

    // Long Description 更新
    if (longDescField) {
      console.log("  Long Description を更新中...");
      setReactTextareaValue(longDescField, apiData.long_description);
      await sleep(500);
    } else {
      console.warn("  Long Description フィールドが見つかりません");
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
          console.log("  保存ボタンをクリック: \"" + btn.textContent.trim() + "\"");
          btn.click();
          await sleep(2000);
          return;
        }
      }
    }

    console.warn("  保存ボタンが見つかりません（手動で保存が必要な場合があります）");
  }

})();
