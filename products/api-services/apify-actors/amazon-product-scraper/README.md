# Amazon Product Scraper - Free No-Code Amazon Data Extractor (Alternative to Jungle Scout, Helium 10)

Scrape Amazon product details or search results at scale -- no API keys, no browser extension, no monthly subscription. Extract price, ratings, reviews, features, BSR, images, and more from any Amazon marketplace. The best free alternative to Jungle Scout, Helium 10, Keepa, and AMZScout.

## Who Is This For?

- **Amazon sellers & FBA entrepreneurs** -- Monitor competitor prices, BSR rankings, and review counts to optimize your listings
- **E-commerce analysts** -- Track pricing trends and product availability across marketplaces
- **Market researchers** -- Analyze product categories, identify gaps, and validate product ideas before launch
- **Affiliate marketers** -- Build product comparison databases with live pricing for content sites
- **Data scientists** -- Collect structured Amazon product data for ML models and trend analysis

## Features

- **Product Mode** -- Scrape full details from one or many Amazon product URLs (ASIN pages)
- **Search Mode** -- Search by keyword and get top results with all metadata
- **Multi-Marketplace** -- Supports amazon.com, .co.uk, .de, .co.jp, .fr, .it, .es, .ca, .com.au, and more
- **Anti-Detection** -- Random delays and browser-like headers to avoid blocking
- **Structured Output** -- Clean JSON output ready for spreadsheets, databases, or downstream pipelines

## Pricing -- Free to Start

| Tier | Cost | What You Get |
|------|------|-------------|
| **Free trial** | $0 | Apify free tier includes monthly compute credits |
| **Pay per product** | ~$0.01-0.05/product | Only pay for actual Apify compute used |
| **vs. Jungle Scout** | Saves $49-129/mo | Same product data, no subscription |
| **vs. Helium 10** | Saves $39-249/mo | No Chrome extension or desktop app needed |
| **vs. Keepa** | Saves $19-89/mo | Bulk processing + API access included |

## Quick Start (3 Steps)

1. **Click "Try for free"** on this Actor's page in Apify Store
2. **Paste your input** -- either Amazon product URLs or a search keyword (see examples below)
3. **Click "Start"** and download results as JSON, CSV, or Excel

## How It Compares to Paid Amazon Tools

| Feature | This Actor (FREE) | Jungle Scout ($49/mo) | Helium 10 ($39/mo) | Keepa ($19/mo) | AMZScout ($45/mo) |
|---------|-------------------|----------------------|--------------------|-----------------|--------------------|
| Product data scraping | Yes | Yes | Yes | Yes | Yes |
| Search results | Yes | Yes | Yes | No | Yes |
| Multi-marketplace | 10+ marketplaces | Limited | Limited | Yes | Limited |
| BSR tracking | Yes | Yes | Yes | Yes | Yes |
| API/automation | Yes (Apify API) | No | No | API ($) | No |
| Scheduling | Yes (Apify scheduler) | No | No | No | No |
| Bulk processing | Unlimited | Plan-limited | Plan-limited | Rate limited | Plan-limited |
| Cloud-based | Yes | Browser extension | Browser extension | Browser extension | Browser extension |
| Monthly cost | $0 (pay per run) | $49-129 | $39-249 | $19-89 | $45-100 |

## Input

| Field | Type | Default | Description |
|-------|------|---------|-------------|
| `mode` | string | `"product"` | `"product"` (scrape URLs) or `"search"` (keyword search) |
| `urls` | string[] | -- | Amazon product URLs to scrape (product mode) |
| `keywords` | string | -- | Search query (search mode) |
| `marketplace` | string | `"com"` | Amazon domain suffix: `com`, `co.uk`, `de`, `co.jp`, `fr`, `it`, `es`, `ca`, `com.au` |
| `maxResults` | integer | `20` | Max results to return (search mode) |

### Example Input -- Product Mode

```json
{
  "mode": "product",
  "urls": [
    "https://www.amazon.com/dp/B0XXXXXXXXX",
    "https://www.amazon.com/dp/B0YYYYYYYYY"
  ]
}
```

### Example Input -- Search Mode

```json
{
  "mode": "search",
  "keywords": "wireless bluetooth headphones",
  "marketplace": "com",
  "maxResults": 20
}
```

### Example Input -- Japan Marketplace

```json
{
  "mode": "search",
  "keywords": "ワイヤレスイヤホン",
  "marketplace": "co.jp",
  "maxResults": 10
}
```

## Output Example

```json
{
  "asin": "B0XXXXXXXXX",
  "title": "Sony WH-1000XM5 Wireless Noise Canceling Headphones",
  "brand": "Sony",
  "price": 348.00,
  "currency": "$",
  "rating": 4.6,
  "reviewCount": 12450,
  "availability": "In Stock",
  "features": [
    "Industry Leading Noise Cancellation",
    "30-hour battery life",
    "Multipoint connection"
  ],
  "bestSellersRank": [
    { "rank": 5, "category": "Over-Ear Headphones" }
  ],
  "mainImage": "https://m.media-amazon.com/images/I/..."
}
```

## Output Fields

| Field | Description |
|-------|-------------|
| `asin` | Amazon Standard Identification Number |
| `title` | Product title |
| `brand` | Brand name |
| `price` | Current price (numeric) |
| `currency` | Price currency symbol |
| `rating` | Average star rating (1-5) |
| `reviewCount` | Total number of reviews |
| `availability` | Stock status |
| `features` | Bullet point features (array) |
| `bestSellersRank` | BSR rank and category |
| `mainImage` | Main product image URL |

## Real-World Use Cases

### 1. Competitor Price Monitoring
Track competitor ASINs daily with Apify scheduler. Export to Google Sheets and set up alerts when prices drop below your threshold.

### 2. Product Research for Amazon FBA
Search high-volume keywords, analyze BSR, review counts, and pricing to validate product ideas before investing in inventory.

### 3. Affiliate Content Database
Build a product comparison database with live pricing. Feed into your WordPress or static site generator for auto-updating affiliate pages.

### 4. Multi-Marketplace Price Comparison
Run the same ASINs across `.com`, `.co.uk`, `.de`, and `.co.jp` to identify arbitrage opportunities or regional pricing differences.

### 5. Review & Rating Tracker
Monitor review counts and ratings over time for your products and competitors. Detect review bombing or sudden quality issues.

## FAQ

**Q: How does this compare to Jungle Scout or Helium 10?**
A: Those tools provide sales estimates and keyword search volume which this Actor does not. However, for raw product data (price, BSR, ratings, reviews, features), this Actor delivers the same data at a fraction of the cost -- pay per run instead of $49+/month.

**Q: Which Amazon marketplaces are supported?**
A: amazon.com, .co.uk, .de, .co.jp, .fr, .it, .es, .ca, .com.au, and any other Amazon domain. Set the `marketplace` parameter to the domain suffix.

**Q: How many products can I scrape per run?**
A: No hard limit. Processing time and cost scale linearly. Typical runs handle 10-500 products. For very large batches (10K+), split into multiple runs.

**Q: Can I schedule this to run daily?**
A: Yes. Use Apify's built-in scheduler for automated price monitoring, BSR tracking, or daily product research. Combine with webhooks to push results to Google Sheets, Slack, or your database.

**Q: Will my requests get blocked by Amazon?**
A: The Actor uses random delays and browser-like headers for anti-detection. For high-volume scraping, increase the delay between requests. Failed items return `success: false` with an error message.

**Q: Can I export results to CSV or Google Sheets?**
A: Yes. Apify datasets can be exported as JSON, CSV, Excel, or pushed directly to Google Sheets, Slack, email, or any webhook endpoint.
