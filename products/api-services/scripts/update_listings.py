import json, os

BASE = r"C:\Users\tmizu\マイドライブ\GitHub\claude-code\products\api-services"

# Updated SEO-optimized names and descriptions from rapidapi-seo-improvements.md
updates = {
    "01-qr-code-api": {
        "name": "Free QR Code Generator API - PNG, SVG, Base64 | <50ms Edge Response",
        "description": "Free QR Code API - Generate PNG/SVG/Base64 in <50ms. Custom colors, error correction. 500 req/mo free.",
    },
    "02-email-validation-api": {
        "name": "Free Email Validation API - MX Lookup, Disposable Detection, Bulk Verify",
        "description": "Free Email Validator - MX check, disposable detection (500+ domains), typo fix, bulk. Save $390/mo vs ZeroBounce.",
    },
    "03-link-preview-api": {
        "name": "Free Link Preview API - Open Graph, Twitter Cards, Favicon, Bulk URLs",
        "description": "Free URL metadata extractor - Open Graph, Twitter Cards, RSS discovery, bulk (10 URLs). Cached on edge.",
    },
    "04-screenshot-api": {
        "name": "Free Website Screenshot API - Capture Any Page as PNG/JPEG | Custom Viewport",
        "description": "Free Screenshot API - Capture any URL as PNG/JPEG. Full-page, custom viewport (320-3840px), render delay. 500 req/mo free.",
    },
    "05-text-analysis-api": {
        "name": "Free Text Analysis API - Sentiment, Keywords, Readability | NLP No AI Key",
        "description": "Free NLP API - Sentiment analysis, keyword extraction, readability score, language detection. No AI key needed.",
    },
    "06-ip-geolocation-api": {
        "name": "Free IP Geolocation API - VPN Detection, City Lookup, Bulk | HTTPS Free",
        "description": "Free IP Lookup - Country, city, ISP, VPN/proxy detection, bulk (20 IPs). HTTPS on free tier. $5.99 vs $99 ipinfo.",
    },
    "07-url-shortener-api": {
        "name": "Free URL Shortener API - Short Links with Click Analytics & Expiration",
        "description": "Free URL Shortener - Create short links with click analytics (referrer, device, geo), custom aliases, expiration.",
    },
    "08-json-formatter-api": {
        "name": "Free JSON Formatter API - Validate, Minify, Diff, CSV Convert | All-in-One",
        "description": "Free JSON toolkit API - Format, minify, validate, diff, JSON-to-CSV, CSV-to-JSON. The only all-in-one JSON API.",
    },
    "09-hash-encoding-api": {
        "name": "Free Hash & Encoding API - SHA256, MD5, Bcrypt, Base64, HMAC | Web Crypto",
        "description": "Free Hash API - SHA256/384/512, MD5, bcrypt, Base64, HMAC, random string. Web Crypto, zero dependencies.",
    },
    "10-currency-exchange-api": {
        "name": "Free Currency Exchange API - Real-Time FX Rates, Conversion, Historical | ECB Data",
        "description": "Free FX Rates API - 30+ currencies, real-time conversion, historical (1999~). ECB official data. Any base free.",
    },
    "11-ai-text-api": {
        "name": "Free AI Text API - Generate, Summarize, Translate, Rewrite | Llama 3.1 No Key",
        "description": "Free AI Text API - Generate, summarize, translate, rewrite with Llama 3.1. No OpenAI key, flat-rate pricing.",
    },
    "12-social-video-api": {
        "name": "Free Social Video Download API - YouTube, TikTok, Instagram, X | Extract URLs",
        "description": "Free Video Download API - Extract direct URLs from YouTube, TikTok, Instagram, X, Facebook, Reddit. Multiple qualities.",
    },
    "13-crypto-data-api": {
        "name": "Free Crypto API - Real-Time Prices, Market Cap, Charts | 10,000+ Coins",
        "description": "Free Crypto API - Real-time prices, market cap, volume, charts for 10,000+ coins. Sub-100ms edge cached.",
    },
    "14-seo-analyzer-api": {
        "name": "Free SEO Analyzer API - 19-Point Audit, Score 0-100 | Ahrefs Alternative",
        "description": "Free SEO Audit API - 19 weighted checks, 0-100 score, structured data, CI/CD ready. $9.99 vs Ahrefs $99/mo.",
    },
    "15-weather-api": {
        "name": "Free Weather API - Forecast, Current, Historical | Open-Meteo Powered",
        "description": "Free Weather API - Current conditions, 48h hourly + 7d daily forecast, historical data. Open-Meteo (ECMWF/NOAA).",
    },
    "16-whois-domain-api": {
        "name": "Free WHOIS Domain API - Registrar Lookup, DNS Records, Domain Availability",
        "description": "Free WHOIS API - Domain registration data (RDAP), DNS records (A/MX/TXT/CNAME), availability check. Sub-100ms.",
    },
    "17-news-aggregator-api": {
        "name": "Free News API - Headlines, Hacker News, Dev.to | Commercial Use OK",
        "description": "Free News API - Aggregate headlines from RSS, Hacker News, Dev.to. Category filter, keyword search. Commercial use OK.",
    },
    "18-ai-translate-api": {
        "name": "Free AI Translation API - 100+ Languages | Meta M2M-100 No Google Key",
        "description": "Free AI Translation - 100+ languages via Meta M2M-100. Any-to-any direct, batch, auto-detect. No Google/DeepL key.",
    },
    "19-trends-api": {
        "name": "Free Trends API - Google Trends + Reddit + GitHub + HN + Product Hunt in 1 API",
        "description": "The ONLY multi-source trends API. Google Trends, Reddit, GitHub, Hacker News, Product Hunt. 5 platforms, 1 subscription.",
    },
    "20-company-data-api": {
        "name": "Free Company Data API - Business Lookup, CRM Enrichment | Clearbit Alternative",
        "description": "Free Company API - Search by name/domain, get industry, size, location, social profiles. Clearbit alternative at $0.",
    },
    "21-wp-internal-link-api": {
        "name": "Free WordPress Internal Link API - SEO Link Suggestions | Only REST API",
        "description": "The ONLY REST API for internal link optimization. Keyword matching, relevance scoring. Works with any CMS, not just WP.",
    },
    "22-pdf-generator-api": {
        "name": "Free PDF Generator API - HTML/Markdown/URL to PDF | Custom Headers & Footers",
        "description": "Free PDF API - Convert HTML, Markdown, or URL to PDF. Custom page size, margins, headers/footers. 500 req/mo free.",
    },
    "23-placeholder-image-api": {
        "name": "Free Placeholder Image API - SVG/PNG with Text, Gradients, Presets",
        "description": "Free Placeholder API - Custom SVG/PNG with text overlay, gradients, category presets. For prototyping & wireframes.",
    },
    "24-markdown-converter-api": {
        "name": "Free Markdown Converter API - HTML to MD, MD to HTML, GFM, TOC, Syntax Highlight",
        "description": "Free Markdown API - Bidirectional MD/HTML conversion, GFM tables, auto TOC, syntax highlighting. The only MD REST API.",
    },
}

updated = 0
for api_dir, new_data in updates.items():
    path = os.path.join(BASE, api_dir, "rapidapi-listing.json")
    if not os.path.exists(path):
        print(f"SKIP: {api_dir} no listing.json")
        continue

    with open(path, "r", encoding="utf-8") as f:
        listing = json.load(f)

    changed = False
    if listing.get("name") != new_data["name"]:
        listing["name"] = new_data["name"]
        changed = True
    if listing.get("description") != new_data["description"]:
        listing["description"] = new_data["description"]
        changed = True

    if changed:
        with open(path, "w", encoding="utf-8") as f:
            json.dump(listing, f, indent=2, ensure_ascii=False)
        print(f"UPDATED: {api_dir}")
        updated += 1
    else:
        print(f"OK (no change): {api_dir}")

print(f"\n{updated} files updated.")
