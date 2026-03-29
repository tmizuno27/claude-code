# Price Monitor - Free Product Price Tracker & Drop Alert Tool

Monitor product prices on Amazon and any e-commerce website -- no API keys, no monthly subscription. Set target price thresholds to detect price drops, track stock availability, and extract review scores in bulk. Schedule daily runs to catch deals automatically. The best free alternative to Keepa, CamelCamelCamel, Honey, and PriceRunner.

## Who Is This For?

- **Amazon sellers & FBA entrepreneurs** -- Monitor competitor pricing to stay competitive without overpaying for Keepa
- **Deal hunters & bargain shoppers** -- Track wishlisted products and get alerted when prices drop to target levels
- **E-commerce managers** -- Monitor competitor prices across multiple products at scale
- **Affiliate marketers** -- Track Amazon product prices to update comparison tables with current pricing
- **Price comparison sites** -- Bulk-fetch current prices across product catalogs for comparison databases
- **Market researchers** -- Analyze pricing strategies and trends across product categories

## Features

- **Multi-Source Price Extraction** -- Works on Amazon, and any e-commerce site using JSON-LD, Open Graph meta tags, or HTML pattern matching
- **Price Drop Alerts** -- Set a `targetPrice` threshold; the Actor flags any product at or below your target
- **JSON-LD Structured Data Parsing** -- Most reliable price source -- reads schema.org Product/Offer data directly
- **Stock Availability Detection** -- Detects in-stock, out-of-stock, and sold-out status across multiple languages (EN/JP/ES/FR)
- **Review Score Extraction** -- Extracts average rating and review count alongside price data
- **Bulk Processing** -- Monitor hundreds of products in a single run
- **Smart Retry Logic** -- Automatic retry on network errors with configurable delays

## Pricing -- Free to Start

| Tier | Cost | What You Get |
|------|------|-------------|
| **Free trial** | $0 | Apify free tier includes monthly compute credits |
| **Pay per product** | ~$0.02-0.10/product | Full price check per URL |
| **vs. Keepa** | Saves $18/mo | Real-time price + availability, no subscription |
| **vs. Honey** | Saves $0 (but manual) | Automated bulk monitoring, not browser extension |
| **vs. PriceRunner** | Saves $0 (but limited) | Custom product lists, any URL |

## How It Compares to Price Tracking Tools

| Feature | This Actor (FREE) | Keepa ($18/mo) | CamelCamelCamel (free) | Honey (free) | PriceRunner (free) |
|---------|-------------------|----------------|------------------------|-------------|-------------------|
| Price extraction | Yes (any URL) | Amazon only | Amazon only | Browser only | Limited sites |
| Non-Amazon sites | Yes | No | No | Partial | Limited |
| Bulk monitoring | Unlimited | Plan-limited | Manual | Manual | Manual |
| Price drop alerts | Yes (threshold) | Yes | Yes (email) | Browser push | Email |
| Stock availability | Yes | Yes | Limited | No | Limited |
| Review extraction | Yes | No | No | No | Yes |
| API/automation | Yes (Apify API) | Yes ($18+) | No | No | No |
| Scheduling | Yes (Apify) | Yes | No | No | No |
| Historical prices | Via scheduled runs | Yes (years) | Yes | No | Limited |
| Monthly cost | $0 (pay per run) | $18 | Free | Free | Free |

## Quick Start (3 Steps)

1. **Click "Try for free"** on this Actor's page in Apify Store
2. **Add product URLs** with optional name and target price threshold
3. **Click "Start"** and get current prices, availability, and alerts as JSON, CSV, or Excel

## Input

| Field | Type | Default | Description |
|-------|------|---------|-------------|
| `products` | object[] | *required* | Array of products with `url`, optional `name`, optional `targetPrice` |
| `currency` | string | `"$"` | Currency symbol for price parsing (e.g., `$`, `¥`, `€`, `£`, `R$`) |
| `extractReviews` | boolean | `true` | Also extract average rating and review count |
| `checkAvailability` | boolean | `true` | Detect in-stock / out-of-stock status |
| `delayMs` | integer | `2000` | Delay between requests in ms |

### Example Input -- Amazon Price Tracking with Alerts

```json
{
  "products": [
    {
      "url": "https://www.amazon.com/dp/B08N5WRWNW",
      "name": "Echo Dot 4th Gen",
      "targetPrice": 25
    },
    {
      "url": "https://www.amazon.com/dp/B07VGRJDFY",
      "name": "Fire TV Stick 4K",
      "targetPrice": 20
    },
    {
      "url": "https://www.amazon.com/dp/B08L5TNJHG",
      "name": "Kindle Paperwhite"
    }
  ],
  "currency": "$",
  "extractReviews": true,
  "checkAvailability": true,
  "delayMs": 2000
}
```

### Example Input -- Multi-Currency E-commerce Monitoring

```json
{
  "products": [
    {
      "url": "https://www.amazon.co.jp/dp/B0BQZPNX21",
      "name": "PlayStation 5",
      "targetPrice": 50000
    }
  ],
  "currency": "¥",
  "extractReviews": true,
  "checkAvailability": true
}
```

## Output Example

```json
{
  "url": "https://www.amazon.com/dp/B08N5WRWNW",
  "finalUrl": "https://www.amazon.com/dp/B08N5WRWNW",
  "name": "Echo Dot (4th Gen) | Smart speaker with Alexa | Twilight Blue",
  "success": true,
  "timestamp": "2026-03-29T10:00:00.000Z",
  "price": 21.99,
  "currency": "$",
  "priceSource": "json-ld",
  "targetPrice": 25,
  "priceAlert": true,
  "availability": "in_stock",
  "rating": 4.7,
  "reviewCount": 456732
}
```

### Price Alert Field

When `priceAlert: true`, the product's current price is at or below the `targetPrice` you set. Use Apify webhook integrations to send Slack notifications, emails, or trigger Zapier/Make automations when a price alert fires.

## Real-World Use Cases

### 1. Daily Deal Alert System
Schedule this Actor to run every morning with your wishlist of products and target prices. Connect to a Slack webhook via Apify integrations -- get instant notifications when any product drops to your target price.

### 2. Amazon FBA Competitor Price Monitoring
Monitor 50+ competitor ASINs daily. Track price changes, detect Buy Box price movements, and adjust your own pricing strategy based on competitor behavior.

### 3. Affiliate Content Price Sync
Affiliate bloggers: schedule weekly runs to verify current prices for products in comparison tables. Export to Google Sheets to automatically update "current price" cells in your content database.

### 4. Holiday Deal Hunting
During Black Friday/Cyber Monday, run every hour on your target products. Catch price drops in real-time and get alerted before items sell out.

### 5. B2B Procurement Monitoring
Procurement teams: track prices for regularly purchased products across multiple suppliers to identify the lowest-cost vendor at any given time.

## FAQ

**Q: Which e-commerce sites are supported?**
A: Amazon is the primary optimized target. For other e-commerce sites, the Actor uses JSON-LD structured data (schema.org Product/Offer), Open Graph meta tags, and generic HTML pattern matching. Sites using standard structured data markup work best.

**Q: How reliable is price extraction?**
A: JSON-LD source (shown in `priceSource` field) is most reliable. Sites without structured data fall back to regex patterns. If `price: null` is returned, the site may require a browser-based scraper or has dynamic pricing loaded via JavaScript.

**Q: Can I monitor JavaScript-heavy sites (SPA)?**
A: This Actor fetches plain HTML without JavaScript execution. Sites that load prices via JavaScript after page load may not return accurate prices. For those, use Apify's Playwright-based Actors.

**Q: How do I set up price drop notifications?**
A: In your Apify run settings, go to "Integrations" and add a webhook. Configure it to trigger on run completion. Use the dataset results to check for `priceAlert: true` items and route to Slack, email, or Zapier.

**Q: Can I track historical prices?**
A: Schedule daily runs and store results in Apify Storage. Each run creates a timestamped dataset. Connect to Google Sheets for a free price history chart.

## Tags

`price tracker`, `price monitor`, `amazon price`, `ecommerce`, `price drop alert`, `product monitor`, `price comparison`, `deal finder`, `stock monitor`, `web scraping`
