import json, os

BASE = r"C:\Users\tmizu\マイドライブ\GitHub\claude-code\products\api-services"

listings = {
    "01-qr-code-api": {
        "name": "Free QR Code Generator API - PNG, SVG, Base64 | <50ms Edge Response",
        "slug": "qr-code-generator-api",
        "short_description": "Free QR Code API - Generate PNG/SVG/Base64 in <50ms. Custom colors, error correction. 500 req/mo free.",
        "category": "Tools",
        "tags": ["qr-code", "qr-code-generator", "barcode", "png-to-base64", "svg-generator", "free-api", "image-generation", "edge-computing", "marketing-tools", "cloudflare-workers"],
        "pricing": [
            {"name": "Basic", "price": 0, "requests_per_month": 500, "rate_limit": "1/sec"},
            {"name": "Pro", "price": 5.99, "requests_per_month": 50000, "rate_limit": "10/sec"},
            {"name": "Ultra", "price": 14.99, "requests_per_month": 500000, "rate_limit": "50/sec"},
            {"name": "Mega", "price": 49.99, "requests_per_month": 5000000, "rate_limit": "100/sec"},
        ],
    },
    "02-email-validation-api": {
        "name": "Free Email Validation API - MX Lookup, Disposable Detection, Bulk Verify",
        "slug": "email-validation-api",
        "short_description": "Free Email Validator - MX check, disposable detection (500+ domains), typo fix, bulk. Save $390/mo vs ZeroBounce.",
        "category": "Email",
        "tags": ["email-validation", "email-verification", "disposable-email", "mx-lookup", "bulk-email-check", "free-api", "bounce-detection", "email-hygiene", "lead-validation", "zerobounce-alternative"],
        "pricing": [
            {"name": "Basic", "price": 0, "requests_per_month": 500, "rate_limit": "1/sec"},
            {"name": "Pro", "price": 9.99, "requests_per_month": 50000, "rate_limit": "10/sec"},
            {"name": "Ultra", "price": 29.99, "requests_per_month": 500000, "rate_limit": "50/sec"},
        ],
    },
    "03-link-preview-api": {
        "name": "Free Link Preview API - Open Graph, Twitter Cards, Favicon, Bulk URLs",
        "slug": "link-preview-api",
        "short_description": "Free URL metadata extractor - Open Graph, Twitter Cards, RSS discovery, bulk (10 URLs). Cached on edge.",
        "category": "Data",
        "tags": ["link-preview", "open-graph", "twitter-cards", "url-metadata", "web-scraping", "favicon", "rss-feed", "social-media-preview", "og-tags", "url-parser"],
        "pricing": [
            {"name": "Basic", "price": 0, "requests_per_month": 500, "rate_limit": "1/sec"},
            {"name": "Pro", "price": 5.99, "requests_per_month": 50000, "rate_limit": "10/sec"},
            {"name": "Ultra", "price": 14.99, "requests_per_month": 500000, "rate_limit": "50/sec"},
            {"name": "Mega", "price": 49.99, "requests_per_month": 5000000, "rate_limit": "100/sec"},
        ],
    },
    "04-screenshot-api": {
        "name": "Free Website Screenshot API - Capture Any Page as PNG/JPEG | Custom Viewport",
        "slug": "screenshot-api",
        "short_description": "Free Screenshot API - Capture any URL as PNG/JPEG. Full-page, custom viewport (320-3840px), render delay. 500 req/mo free.",
        "category": "Visual Recognition",
        "tags": ["screenshot-api", "website-screenshot", "webpage-capture", "url-to-image", "full-page-capture", "free-api", "website-thumbnail", "headless-browser", "website-preview", "cloudflare-workers"],
        "pricing": [
            {"name": "Basic", "price": 0, "requests_per_month": 500, "rate_limit": "1/sec"},
            {"name": "Pro", "price": 5.99, "requests_per_month": 50000, "rate_limit": "10/sec"},
            {"name": "Ultra", "price": 14.99, "requests_per_month": 500000, "rate_limit": "50/sec"},
            {"name": "Mega", "price": 49.99, "requests_per_month": 5000000, "rate_limit": "100/sec"},
        ],
    },
    "05-text-analysis-api": {
        "name": "Free Text Analysis API - Sentiment, Keywords, Readability | NLP No AI Key",
        "slug": "text-analysis-api",
        "short_description": "Free NLP API - Sentiment analysis, keyword extraction, readability score, language detection. No AI key needed.",
        "category": "Text Analysis",
        "tags": ["text-analysis", "sentiment-analysis", "keyword-extraction", "nlp-api", "readability-score", "language-detection", "free-api", "natural-language-processing", "text-mining", "content-analysis"],
        "pricing": [
            {"name": "Basic", "price": 0, "requests_per_month": 500, "rate_limit": "1/sec"},
            {"name": "Pro", "price": 5.99, "requests_per_month": 50000, "rate_limit": "10/sec"},
            {"name": "Ultra", "price": 14.99, "requests_per_month": 500000, "rate_limit": "50/sec"},
            {"name": "Mega", "price": 49.99, "requests_per_month": 5000000, "rate_limit": "100/sec"},
        ],
    },
    "06-ip-geolocation-api": {
        "name": "Free IP Geolocation API - VPN Detection, City Lookup, Bulk | HTTPS Free",
        "slug": "ip-geolocation-api",
        "short_description": "Free IP Lookup - Country, city, ISP, VPN/proxy detection, bulk (20 IPs). HTTPS on free tier. $5.99 vs $99 ipinfo.",
        "category": "Location",
        "tags": ["ip-geolocation", "ip-lookup", "vpn-detection", "proxy-detection", "ip-address-api", "geoip", "free-api", "ip-to-country", "bulk-ip-lookup", "ipinfo-alternative"],
        "pricing": [
            {"name": "Basic", "price": 0, "requests_per_month": 500, "rate_limit": "1/sec"},
            {"name": "Pro", "price": 5.99, "requests_per_month": 50000, "rate_limit": "10/sec"},
            {"name": "Ultra", "price": 14.99, "requests_per_month": 500000, "rate_limit": "50/sec"},
            {"name": "Mega", "price": 49.99, "requests_per_month": 5000000, "rate_limit": "100/sec"},
        ],
    },
    "07-url-shortener-api": {
        "name": "Free URL Shortener API - Short Links with Click Analytics & Expiration",
        "slug": "url-shortener-api",
        "short_description": "Free URL Shortener - Create short links with click analytics (referrer, device, geo), custom aliases, expiration.",
        "category": "Tools",
        "tags": ["url-shortener", "link-shortener", "short-url", "click-analytics", "link-tracking", "free-api", "custom-short-link", "bitly-alternative", "link-management", "url-redirect"],
        "pricing": [
            {"name": "Basic", "price": 0, "requests_per_month": 500, "rate_limit": "1/sec"},
            {"name": "Pro", "price": 5.99, "requests_per_month": 50000, "rate_limit": "10/sec"},
            {"name": "Ultra", "price": 14.99, "requests_per_month": 500000, "rate_limit": "50/sec"},
            {"name": "Mega", "price": 49.99, "requests_per_month": 5000000, "rate_limit": "100/sec"},
        ],
    },
    "08-json-formatter-api": {
        "name": "Free JSON Formatter API - Validate, Minify, Diff, CSV Convert | All-in-One",
        "slug": "json-formatter-api",
        "short_description": "Free JSON toolkit API - Format, minify, validate, diff, JSON-to-CSV, CSV-to-JSON. The only all-in-one JSON API.",
        "category": "Tools",
        "tags": ["json-formatter", "json-validator", "json-minify", "json-to-csv", "csv-to-json", "json-diff", "free-api", "json-parser", "data-conversion", "developer-tools"],
        "pricing": [
            {"name": "Basic", "price": 0, "requests_per_month": 500, "rate_limit": "1/sec"},
            {"name": "Pro", "price": 5.99, "requests_per_month": 50000, "rate_limit": "10/sec"},
            {"name": "Ultra", "price": 14.99, "requests_per_month": 500000, "rate_limit": "50/sec"},
            {"name": "Mega", "price": 49.99, "requests_per_month": 5000000, "rate_limit": "100/sec"},
        ],
    },
    "09-hash-encoding-api": {
        "name": "Free Hash & Encoding API - SHA256, MD5, Bcrypt, Base64, HMAC | Web Crypto",
        "slug": "hash-encoding-api",
        "short_description": "Free Hash API - SHA256/384/512, MD5, bcrypt, Base64, HMAC, random string. Web Crypto, zero dependencies.",
        "category": "Tools",
        "tags": ["hash-api", "sha256", "md5", "bcrypt", "base64-encode", "hmac", "free-api", "encryption", "hash-generator", "cryptography", "password-hash"],
        "pricing": [
            {"name": "Basic", "price": 0, "requests_per_month": 500, "rate_limit": "1/sec"},
            {"name": "Pro", "price": 5.99, "requests_per_month": 50000, "rate_limit": "10/sec"},
            {"name": "Ultra", "price": 14.99, "requests_per_month": 500000, "rate_limit": "50/sec"},
            {"name": "Mega", "price": 49.99, "requests_per_month": 5000000, "rate_limit": "100/sec"},
        ],
    },
    "10-currency-exchange-api": {
        "name": "Free Currency Exchange API - Real-Time FX Rates, Conversion, Historical | ECB Data",
        "slug": "currency-exchange-api",
        "short_description": "Free FX Rates API - 30+ currencies, real-time conversion, historical (1999~). ECB official data. Any base free.",
        "category": "Finance",
        "tags": ["currency-exchange", "exchange-rate-api", "forex-api", "currency-converter", "fx-rates", "ecb-exchange-rate", "free-api", "historical-exchange-rate", "money-conversion", "fintech"],
        "pricing": [
            {"name": "Basic", "price": 0, "requests_per_month": 500, "rate_limit": "1/sec"},
            {"name": "Pro", "price": 5.99, "requests_per_month": 50000, "rate_limit": "10/sec"},
            {"name": "Ultra", "price": 14.99, "requests_per_month": 500000, "rate_limit": "50/sec"},
            {"name": "Mega", "price": 49.99, "requests_per_month": 5000000, "rate_limit": "100/sec"},
        ],
    },
    "21-wp-internal-link-api": {
        "name": "Free WordPress Internal Link API - SEO Link Suggestions | Only REST API",
        "slug": "wp-internal-link-api",
        "short_description": "The ONLY REST API for internal link optimization. Keyword matching, relevance scoring. Works with any CMS, not just WP.",
        "category": "SEO",
        "tags": ["internal-link", "wordpress-api", "seo-links", "link-optimization", "content-linking", "free-api", "link-whisper-alternative", "internal-linking", "cms-api", "seo-automation"],
        "pricing": [
            {"name": "Basic", "price": 0, "requests_per_month": 100, "rate_limit": "1/sec"},
            {"name": "Pro", "price": 9.99, "requests_per_month": 10000, "rate_limit": "10/sec"},
            {"name": "Ultra", "price": 29.99, "requests_per_month": 100000, "rate_limit": "50/sec"},
        ],
    },
    "22-pdf-generator-api": {
        "name": "Free PDF Generator API - HTML/Markdown/URL to PDF | Custom Headers & Footers",
        "slug": "pdf-generator-api",
        "short_description": "Free PDF API - Convert HTML, Markdown, or URL to PDF. Custom page size, margins, headers/footers. 500 req/mo free.",
        "category": "Tools",
        "tags": ["pdf-generator", "html-to-pdf", "pdf-api", "markdown-to-pdf", "url-to-pdf", "free-api", "document-generation", "invoice-generator", "report-generation", "pdf-converter"],
        "pricing": [
            {"name": "Basic", "price": 0, "requests_per_month": 500, "rate_limit": "1/sec"},
            {"name": "Pro", "price": 5.99, "requests_per_month": 50000, "rate_limit": "10/sec"},
            {"name": "Ultra", "price": 14.99, "requests_per_month": 500000, "rate_limit": "50/sec"},
            {"name": "Mega", "price": 49.99, "requests_per_month": 5000000, "rate_limit": "100/sec"},
        ],
    },
    "23-placeholder-image-api": {
        "name": "Free Placeholder Image API - SVG/PNG with Text, Gradients, Presets",
        "slug": "placeholder-image-api",
        "short_description": "Free Placeholder API - Custom SVG/PNG with text overlay, gradients, category presets. For prototyping & wireframes.",
        "category": "Visual Recognition",
        "tags": ["placeholder-image", "placeholder-api", "dummy-image", "svg-generator", "wireframe-image", "free-api", "prototype-images", "test-images", "mock-images", "developer-tools"],
        "pricing": [
            {"name": "Basic", "price": 0, "requests_per_month": 500, "rate_limit": "1/sec"},
            {"name": "Pro", "price": 5.99, "requests_per_month": 50000, "rate_limit": "10/sec"},
            {"name": "Ultra", "price": 14.99, "requests_per_month": 500000, "rate_limit": "50/sec"},
            {"name": "Mega", "price": 49.99, "requests_per_month": 5000000, "rate_limit": "100/sec"},
        ],
    },
    "24-markdown-converter-api": {
        "name": "Free Markdown Converter API - HTML to MD, MD to HTML, GFM, TOC, Syntax Highlight",
        "slug": "markdown-converter-api",
        "short_description": "Free Markdown API - Bidirectional MD/HTML conversion, GFM tables, auto TOC, syntax highlighting. The only MD REST API.",
        "category": "Tools",
        "tags": ["markdown-converter", "markdown-to-html", "html-to-markdown", "gfm", "markdown-api", "free-api", "table-of-contents", "syntax-highlighting", "markdown-parser", "text-converter"],
        "pricing": [
            {"name": "Basic", "price": 0, "requests_per_month": 500, "rate_limit": "1/sec"},
            {"name": "Pro", "price": 5.99, "requests_per_month": 50000, "rate_limit": "10/sec"},
            {"name": "Ultra", "price": 14.99, "requests_per_month": 500000, "rate_limit": "50/sec"},
            {"name": "Mega", "price": 49.99, "requests_per_month": 5000000, "rate_limit": "100/sec"},
        ],
    },
}

for api_dir, data in listings.items():
    path = os.path.join(BASE, api_dir, "rapidapi-listing.json")
    if os.path.exists(path):
        print(f"SKIP: {api_dir} already exists")
        continue

    listing = {
        "name": data["name"],
        "slug": data["slug"],
        "description": data["short_description"],
        "long_description": f"See README.md for full long description content to paste into RapidAPI Studio.",
        "category": data["category"],
        "tags": data["tags"],
        "website": f"https://{data['slug']}.t-mizuno27.workers.dev",
        "pricing": {
            "plans": [
                {
                    "name": p["name"],
                    "price": p["price"],
                    "rate_limit": {
                        "requests_per_month": p["requests_per_month"],
                        "requests_per_second": int(p["rate_limit"].split("/")[0]),
                    },
                }
                for p in data["pricing"]
            ]
        },
    }

    with open(path, "w", encoding="utf-8") as f:
        json.dump(listing, f, indent=2, ensure_ascii=False)

    print(f"OK: {api_dir}")

print("\nDone!")
