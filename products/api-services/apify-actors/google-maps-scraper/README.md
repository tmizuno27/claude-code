# Google Maps Scraper - Free No-Code Local Business Data Extractor (Alternative to PhantomBuster, Outscraper)

Scrape Google Maps business listings at scale -- name, address, phone, website, ratings, reviews, opening hours, and GPS coordinates. No API keys, no Google Cloud billing, no monthly subscription. The best free alternative to PhantomBuster, Outscraper, SerpApi, and Google Places API.

## Who Is This For?

- **Sales teams & SDRs** -- Build hyper-local lead lists of businesses in any city, category, and radius
- **Real estate agents** -- Map competitor agencies, restaurants, amenities near properties
- **Local SEO agencies** -- Audit client Google Maps presence and benchmark against local competitors
- **Market researchers** -- Analyze business density, ratings, and review distribution in target markets
- **Franchise operators** -- Map competitor locations and identify expansion opportunities

## Features

- **Search Mode** -- Search by query (e.g., "restaurants in Tokyo") and get top results with full details
- **Direct URL Mode** -- Scrape specific Google Maps place URLs for targeted data extraction
- **Multi-Language** -- Supports any Google Maps language (en, ja, es, de, fr, pt, etc.)
- **Review Details** -- Optionally fetch detailed place information including opening hours
- **Geo Coordinates** -- Latitude/longitude for each listing, ready for mapping tools
- **Structured Output** -- Clean JSON output ready for CRM import, spreadsheets, or downstream pipelines

## Pricing -- Free to Start

| Tier | Cost | What You Get |
|------|------|-------------|
| **Free trial** | $0 | Apify free tier includes monthly compute credits |
| **Pay per listing** | ~$0.01-0.05/listing | Only pay for actual Apify compute used |
| **vs. PhantomBuster** | Saves $69-439/mo | Same data, no phantom credits |
| **vs. Outscraper** | Saves $22-100/mo | No per-record pricing |
| **vs. Google Places API** | Saves $17/1000 requests | No Google Cloud billing setup |

## Quick Start (3 Steps)

1. **Click "Try for free"** on this Actor's page in Apify Store
2. **Enter a search query** (e.g., "coffee shops in New York") or paste Google Maps URLs
3. **Click "Start"** and download results as JSON, CSV, or Excel

## How It Compares to Paid Alternatives

| Feature | This Actor (FREE) | PhantomBuster ($69/mo) | Outscraper ($22/mo) | Google Places API ($17/1K) | SerpApi ($75/mo) |
|---------|-------------------|----------------------|--------------------|--------------------------|--------------------|
| Business data scraping | Yes | Yes | Yes | Yes | Yes |
| Search by query | Yes | Yes | Yes | No (Place ID needed) | Yes |
| Ratings & reviews | Yes | Yes | Yes | Yes | Yes |
| Opening hours | Yes | Limited | Yes | Yes | Limited |
| GPS coordinates | Yes | No | Yes | Yes | Yes |
| Phone numbers | Yes | Yes | Yes | Yes | Yes |
| API/automation | Yes (Apify API) | Yes | Yes | Yes | Yes |
| Scheduling | Yes (Apify scheduler) | Yes | No | No | No |
| Bulk processing | Unlimited | Credit-limited | Per-record | Per-request | Plan-limited |
| Cloud-based | Yes | Yes | Yes | Yes | Yes |
| API keys required | None | None | None | Yes (Google Cloud) | Yes |
| Monthly cost | $0 (pay per run) | $69-439 | $22-100 | Usage-based ($17/1K) | $75-300 |

## Input

| Field | Type | Default | Description |
|-------|------|---------|-------------|
| `searchQuery` | string | -- | Search query (e.g., "dentists in Los Angeles") |
| `placeUrls` | string[] | -- | Direct Google Maps place URLs to scrape |
| `maxResults` | integer | `20` | Max results to return (search mode) |
| `includeReviews` | boolean | `true` | Include detailed place info |
| `language` | string | `"en"` | Google Maps language code |

### Example Input -- Search Mode

```json
{
  "searchQuery": "coffee shops in New York",
  "maxResults": 20,
  "includeReviews": true,
  "language": "en"
}
```

### Example Input -- Direct URL Mode

```json
{
  "placeUrls": [
    "https://www.google.com/maps/place/Starbucks/..."
  ]
}
```

### Example Input -- Japanese Market

```json
{
  "searchQuery": "ラーメン 渋谷",
  "maxResults": 30,
  "includeReviews": true,
  "language": "ja"
}
```

## Output Example

```json
{
  "name": "Blue Bottle Coffee",
  "address": "450 W 15th St, New York, NY 10011",
  "phone": "+1-510-653-3394",
  "website": "https://bluebottlecoffee.com",
  "rating": 4.5,
  "reviewCount": 2340,
  "category": "Coffee shop",
  "latitude": 40.7425,
  "longitude": -74.0053,
  "openingHours": [
    "Monday: 7:00 AM - 6:30 PM",
    "Tuesday: 7:00 AM - 6:30 PM"
  ]
}
```

## Output Fields

| Field | Description |
|-------|-------------|
| `name` | Business name |
| `address` | Street address |
| `phone` | Phone number |
| `website` | Business website URL |
| `rating` | Average star rating (1-5) |
| `reviewCount` | Total number of reviews |
| `category` | Business category |
| `latitude` | GPS latitude |
| `longitude` | GPS longitude |
| `openingHours` | Business hours (array of strings) |

## Real-World Use Cases

### 1. Local Lead Generation

Search "accountants in Miami" and get a ready-to-use prospect list with name, phone, website, and email (combine with Email Finder Actor for contact discovery).

### 2. Competitor Mapping

Map all competitors in a radius. Export GPS coordinates to Google My Maps or Tableau for visual competitive analysis.

### 3. Local SEO Audit

Scrape your client's category in their city. Compare their rating, review count, and category against top competitors for a data-driven SEO report.

### 4. Market Entry Analysis

Before opening a new location, scrape existing businesses in the target area. Analyze density, ratings, and review sentiment to assess market saturation.

### 5. Business Directory Building

Build niche directories (e.g., "vegan restaurants in London") with live data. Schedule weekly runs to keep listings current.

## FAQ

**Q: How does this compare to Google Places API?**

A: Google Places API requires a Google Cloud account, billing setup, and API key management. It charges ~$17 per 1,000 requests. This Actor requires zero setup and costs a fraction per listing through Apify's compute pricing.

**Q: How many listings can I scrape per run?**

A: No hard limit. Google Maps search typically returns 20-60 results per query. For larger datasets, use multiple search queries (e.g., by neighborhood or subcategory).

**Q: Can I scrape reviews text?**

A: Currently, the Actor extracts review count and average rating. Full review text extraction is planned for a future update.

**Q: Can I schedule this to run daily?**

A: Yes. Use Apify's built-in scheduler for automated lead generation or competitor monitoring. Combine with webhooks to push results to your CRM, Google Sheets, or Slack.

**Q: What languages are supported?**

A: Any language supported by Google Maps. Set the `language` parameter to the ISO language code (en, ja, es, de, fr, pt, zh, ko, etc.).

**Q: Can I export results to CSV or Google Sheets?**

A: Yes. Apify datasets can be exported as JSON, CSV, Excel, or pushed directly to Google Sheets, Slack, email, or any webhook endpoint.
