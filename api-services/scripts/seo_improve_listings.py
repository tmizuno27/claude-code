#!/usr/bin/env python3
"""SEO improvement script for all 24 RapidAPI listing JSONs."""
import json
import os

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

improvements = {
    "01-qr-code-api": {
        "description": "Free QR Code Generator API - PNG, SVG, Base64, Custom Colors, No Auth Required",
        "tags_add": ["png", "svg"],
        "long_append": '\n\n## Alternative To\nLooking for a **QR code API alternative** to goqr.me, QR Server, or QRickit? This API offers faster response times via Cloudflare\'s edge network with a generous free tier.\n\n## Sample Response\nWith `format=base64`:\n```json\n{"qr_code": "data:image/png;base64,iVBOR..."}\n```\n\n## Need More Requests?\nThe **free plan** (500 req/mo) is perfect for prototyping. Upgrade to **Pro ($5.99/mo)** for production workloads with 50,000 requests and 10 req/sec rate limit.'
    },
    "02-email-validation-api": {
        "description": "Free Email Validation API - Disposable Detection, MX Lookup, Typo Fix, No Auth",
        "tags_add": [],
        "long_append": '\n\n## Alternative To\nA cost-effective **email verification API alternative** to ZeroBounce, Hunter.io, and NeverBounce. No signup friction with a free 500-request tier.\n\n## Sample Response\n```json\n{"email":"test@gmail.com","valid":true,"is_disposable":false,"has_mx":true,"score":95}\n```\n\n## Need More Requests?\nStart free with 500 validations/month. Scale to **Pro ($9.99/mo)** for bulk validation of 50,000 emails with 10 req/sec throughput.'
    },
    "03-link-preview-api": {
        "description": "Free Link Preview API - Open Graph, Twitter Card, Favicon, RSS Extraction",
        "tags_add": [],
        "long_append": '\n\n## Alternative To\nA lightweight **link unfurling API alternative** to Microlink, LinkPreview.net, and Open Graph.io. Edge-cached responses under 100ms.\n\n## Sample Response\n```json\n{"title":"GitHub","description":"Where the world builds software","image":"https://...","favicon":"https://..."}\n```\n\n## Need More Requests?\nFree plan covers 100 previews/month for development. **Pro ($9.99/mo)** unlocks 5,000 previews for production chat and social apps.'
    },
    "04-screenshot-api": {
        "description": "Free Website Screenshot API - Full Page Capture, PNG/JPEG, Custom Viewport",
        "tags_add": [],
        "long_append": '\n\n## Alternative To\nA zero-setup **screenshot API alternative** to Screenshotlayer, URL2PNG, and Apiflash. No browser farm needed.\n\n## Need More Requests?\nPrototype free (100 captures/month). **Pro ($9.99/mo)** delivers 5,000 screenshots with custom viewports and full-page capture.'
    },
    "05-text-analysis-api": {
        "description": "Free Text Analysis API - Sentiment, Keywords, Readability, Language Detection",
        "tags_add": [],
        "long_append": '\n\n## Alternative To\nA free **NLP API alternative** to MonkeyLearn, Aylien, and MeaningCloud. Pure JavaScript with no GPU or ML model hosting costs.\n\n## Sample Response\n```json\n{"sentiment":{"score":0.8,"label":"positive"},"keywords":[{"word":"API","tfidf":0.42}],"readability":{"grade_level":8.2}}\n```\n\n## Need More Requests?\nFree tier (500 analyses/month) covers testing. **Pro ($5.99/mo)** handles production NLP pipelines with 50,000 requests.'
    },
    "06-ip-geolocation-api": {
        "description": "Free IP Geolocation API - Country, City, VPN Detection, Bulk Lookup",
        "tags_add": [],
        "long_append": '\n\n## Alternative To\nA free **IP geolocation API alternative** to ipinfo.io, ipstack, and ip-api.com. Leverages Cloudflare native geo data for caller IP (zero latency).\n\n## Need More Requests?\nFree plan includes 500 lookups/month. **Pro ($5.99/mo)** scales to 50,000 lookups with bulk endpoint for fraud detection and analytics.'
    },
    "07-url-shortener-api": {
        "description": "Free URL Shortener API - Click Analytics, Custom Aliases, REST Interface",
        "tags_add": [],
        "long_append": '\n\n## Alternative To\nA developer-first **URL shortener API alternative** to Bitly, Rebrandly, and TinyURL. Built-in click analytics with zero third-party dependencies.\n\n## Need More Requests?\nFree plan (500 links/month) for personal projects. **Pro ($5.99/mo)** unlocks 50,000 links with detailed click stats.'
    },
    "08-json-formatter-api": {
        "description": "Free JSON Formatter API - Validate, Minify, Diff, CSV Convert, Transform",
        "tags_add": [],
        "long_append": '\n\n## Alternative To\nA programmatic **JSON tools API alternative** to JSONLint, JSON Formatter online, and JSONDiff. Automate JSON processing in your CI/CD pipeline.\n\n## Need More Requests?\nFree plan covers 500 operations/month. **Pro ($5.99/mo)** for 50,000 operations in build pipelines and ETL workflows.'
    },
    "09-hash-encoding-api": {
        "description": "Free Hash & Encoding API - SHA256, Bcrypt, Base64, HMAC, Web Crypto",
        "tags_add": [],
        "long_append": '\n\n## Alternative To\nA serverless **hashing API alternative** to hashapi.com and online hash generators. Uses Web Crypto API for security-grade hashing.\n\n## Need More Requests?\nFree tier (500 hashes/month) for testing. **Pro ($5.99/mo)** for production authentication and data integrity workflows.'
    },
    "10-currency-exchange-api": {
        "description": "Free Currency Exchange API - 30+ Currencies, ECB Rates, Historical Data",
        "tags_add": [],
        "long_append": '\n\n## Alternative To\nA free **exchange rate API alternative** to Fixer.io, ExchangeRate-API, and Open Exchange Rates. ECB-sourced data updated daily.\n\n## Need More Requests?\nFree plan (500 conversions/month) for personal finance apps. **Pro ($5.99/mo)** for e-commerce and fintech with 50,000 requests.'
    },
    "11-ai-text-api": {
        "description": "Free AI Text API - Generate, Summarize, Translate, Rewrite with Llama 3.1",
        "tags_add": [],
        "long_append": '\n\n## Alternative To\nA free **AI text API alternative** to OpenAI GPT, Cohere, and AI21 Labs. Powered by Meta Llama 3.1 8B on Cloudflare Workers AI (free tier).\n\n## Need More Requests?\nFree plan (500 generations/month) for experimentation. **Pro ($9.99/mo)** for production AI features with 50,000 requests.'
    },
    "12-social-video-api": {
        "description": "Free Social Video Download API - TikTok, YouTube, Instagram, Twitter/X",
        "tags_add": [],
        "long_append": '\n\n## Alternative To\nA developer-friendly **video download API alternative** to SaveFrom, SnapSave, and SSSTik. Supports 5 major platforms in one unified endpoint.\n\n## Need More Requests?\nFree plan (100 downloads/month) for personal use. **Pro ($9.99/mo)** for content tools and social media managers.'
    },
    "13-crypto-data-api": {
        "description": "Free Crypto Data API - Bitcoin, Ethereum, Real-time Prices, Market Data",
        "tags_add": [],
        "long_append": '\n\n## Alternative To\nA free **cryptocurrency API alternative** to CoinMarketCap, CoinGecko Pro, and CryptoCompare. Aggregates CoinGecko data with smart caching.\n\n## Need More Requests?\nFree plan (500 queries/month) for portfolio trackers. **Pro ($5.99/mo)** for trading bots and analytics dashboards.'
    },
    "14-seo-analyzer-api": {
        "description": "Free SEO Analyzer API - Meta Tags, Headings, Score, Structured Data Audit",
        "tags_add": [],
        "long_append": '\n\n## Alternative To\nA free **SEO audit API alternative** to Ahrefs, Moz, and Screaming Frog. Instant on-page SEO scoring via edge computing.\n\n## Need More Requests?\nFree plan (500 audits/month) for single-site checks. **Pro ($9.99/mo)** for SEO agencies and bulk site auditing.'
    },
    "15-weather-api": {
        "description": "Free Weather API - Current, Forecast, Hourly, Historical, Geocoding",
        "tags_add": [],
        "long_append": '\n\n## Alternative To\nA free **weather API alternative** to OpenWeatherMap, WeatherAPI, and AccuWeather. Powered by Open-Meteo with no API key required.\n\n## Need More Requests?\nFree plan (500 queries/month) for personal apps. **Pro ($5.99/mo)** for weather dashboards and IoT with 50,000 requests.'
    },
    "16-whois-domain-api": {
        "description": "Free WHOIS Domain API - RDAP Lookup, DNS Records, Availability Check",
        "tags_add": [],
        "long_append": '\n\n## Alternative To\nA free **WHOIS API alternative** to WhoisXML, DomainTools, and Namecheap API. Uses RDAP protocol for accurate, ICANN-compliant lookups.\n\n## Need More Requests?\nFree plan (500 lookups/month) for domain research. **Pro ($5.99/mo)** for domain registrars and security teams.'
    },
    "17-news-aggregator-api": {
        "description": "Free News API - BBC, Reuters, HN, Dev.to, Tech & Business Headlines",
        "tags_add": [],
        "long_append": '\n\n## Alternative To\nA free **news API alternative** to NewsAPI.org, GNews, and Currents API. Aggregates RSS feeds and public APIs from top sources.\n\n## Need More Requests?\nFree plan (500 queries/month) for news readers. **Pro ($5.99/mo)** for content aggregation platforms with 50,000 requests.'
    },
    "18-ai-translate-api": {
        "description": "Free AI Translation API - 40+ Languages, Detection, Batch, M2M100 Model",
        "tags_add": [],
        "long_append": '\n\n## Alternative To\nA free **translation API alternative** to DeepL, Google Translate API, and LibreTranslate. Powered by Meta M2M100 on Cloudflare Workers AI.\n\n## Need More Requests?\nFree plan (500 translations/month) for personal projects. **Pro ($9.99/mo)** for localization pipelines with 50,000 requests.'
    },
    "19-trends-api": {
        "description": "Free Trends API - Google, Reddit, HN, GitHub, Product Hunt Aggregator",
        "tags_add": [],
        "long_append": '\n\n## Alternative To\nA free **trends API alternative** to Google Trends API (unofficial), SerpAPI Trends, and social listening tools. 5 platforms in one API.\n\n## Need More Requests?\nFree plan (500 queries/month) for trend monitoring. **Pro ($5.99/mo)** for content marketing and social listening dashboards.'
    },
    "20-company-data-api": {
        "description": "Free Company Data API - Business Search, Domain Enrichment, Tech Stack",
        "tags_add": [],
        "long_append": '\n\n## Alternative To\nA free **company data API alternative** to Clearbit, ZoomInfo, and FullContact. Combines OpenCorporates, RDAP, and web scraping.\n\n## Need More Requests?\nFree plan (500 lookups/month) for lead research. **Pro ($9.99/mo)** for CRM integrations and sales prospecting.'
    },
    "21-wp-internal-link-api": {
        "description": "Free WordPress SEO API - Internal Link Suggestions, Anchor Text, Scoring",
        "tags_add": [],
        "long_append": '\n\n## Alternative To\nA free **WordPress internal linking API alternative** to Link Whisper, Yoast, and RankMath link suggestions. Automated keyword-to-URL matching.\n\n## Need More Requests?\nFree plan (100 analyses/month) for single-site use. **Pro ($9.99/mo)** for SEO agencies managing multiple WordPress sites.'
    },
    "22-pdf-generator-api": {
        "description": "Free PDF Generator API - HTML/Markdown/URL to PDF, Headers, Footers",
        "tags_add": ["free-api", "rest-api", "developer-tools"],
        "long_append": '\n\n## Alternative To\nA free **PDF generation API alternative** to PDFShift, HTML2PDF, and DocRaptor. Serverless on Cloudflare edge with no browser farm needed.\n\n## Need More Requests?\nFree plan (100 PDFs/month) for prototyping. **Pro ($5.99/mo)** for invoice generation and report automation with 5,000 PDFs.'
    },
    "23-placeholder-image-api": {
        "description": "Free Placeholder Image API - SVG/PNG, Gradients, Custom Text, Categories",
        "tags_add": ["free-api", "rest-api", "developer-tools"],
        "long_append": '\n\n## Alternative To\nA modern **placeholder image API alternative** to Placeholder.com, Lorem Picsum, and PlaceIMG. 10 gradient presets and category-based sizing.\n\n## Need More Requests?\nFree plan (100 images/month) for mockups. **Pro ($5.99/mo)** for design tools and prototyping platforms with 5,000 images.'
    },
    "24-markdown-converter-api": {
        "description": "Free Markdown Converter API - HTML to Markdown, TOC, GFM, Syntax Highlight",
        "tags_add": ["free-api", "rest-api", "developer-tools", "text-processing"],
        "long_append": '\n\n## Alternative To\nA free **Markdown API alternative** to Showdown, Turndown, and Marked.js hosted solutions. Full GFM support with auto-generated Table of Contents.\n\n## Sample Response\n```json\n{"html":"<h1>Hello</h1><p>This is <strong>bold</strong> text.</p>","toc":[{"level":1,"text":"Hello","id":"hello"}]}\n```\n\n## Need More Requests?\nFree plan (500 conversions/month) for personal blogs. **Pro ($5.99/mo)** for CMS platforms and documentation sites with 10,000 conversions.'
    }
}

updated = 0
for dirname, imp in improvements.items():
    listing_path = os.path.join(BASE, dirname, "rapidapi-listing.json")
    if not os.path.exists(listing_path):
        print(f"SKIP {dirname}: no listing file")
        continue

    with open(listing_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    data["description"] = imp["description"]

    existing_tags = data.get("tags", [])
    for tag in imp["tags_add"]:
        if tag not in existing_tags:
            existing_tags.append(tag)
    data["tags"] = existing_tags

    if imp["long_append"]:
        data["long_description"] = data.get("long_description", "") + imp["long_append"]

    with open(listing_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

    updated += 1
    print(f"OK {dirname}: desc={len(data['description'])}ch, long={len(data['long_description'])}ch, tags={len(data['tags'])}")

print(f"\nDone - {updated}/24 APIs updated")
