# SERP Checker - Free Google Rank Tracker & SERP Scraper (No API Key Required)

Track keyword rankings in Google search results and extract full SERP data -- no API keys, no monthly subscription. Check your website's position for target keywords, analyze top 10/20/50/100 results, and detect SERP features like featured snippets and People Also Ask boxes. The best free alternative to SEMrush Position Tracking, Ahrefs Rank Tracker, SERPWatcher, and AccuRanker.

## Who Is This For?

- **SEO specialists** -- Track keyword rankings across target pages and monitor position changes over time
- **Content marketers** -- Identify which of your pages rank for key terms before publishing new content
- **Agencies & freelancers** -- Bulk-check client keyword positions and generate ranking reports
- **Affiliate marketers** -- Monitor which competitor pages rank #1-3 and analyze their content patterns
- **E-commerce managers** -- Track product category keyword positions against competitors
- **Bloggers** -- Find out where your articles rank and identify optimization opportunities

## Features

- **Rank Tracking** -- Check your domain's position for any keyword in top 10/20/50/100 results
- **Full SERP Extraction** -- Get title, URL, domain, and snippet for each organic result
- **SERP Feature Detection** -- Detect featured snippets, People Also Ask, local packs, knowledge panels, and shopping ads
- **Multi-Region Support** -- Check rankings in any Google country (US, JP, GB, DE, FR, AU, BR, and 100+ more)
- **Multi-Language** -- Google search in any language (en, ja, es, de, fr, pt, zh, etc.)
- **Bulk Processing** -- Check dozens of keywords in a single run
- **Configurable Delay** -- Built-in rate limiting to avoid Google blocks

## Pricing -- Free to Start

| Tier | Cost | What You Get |
|------|------|-------------|
| **Free trial** | $0 | Apify free tier includes monthly compute credits |
| **Pay per keyword** | ~$0.01-0.05/keyword | Full SERP data per keyword |
| **vs. SEMrush** | Saves $129-499/mo | Same rank data, no subscription |
| **vs. Ahrefs** | Saves $99-999/mo | On-demand rank checks, no limits |
| **vs. AccuRanker** | Saves $99-499/mo | Cloud-based, no install needed |

## How It Compares to Paid Rank Trackers

| Feature | This Actor (FREE) | SEMrush ($129/mo) | Ahrefs ($99/mo) | AccuRanker ($99/mo) | SERPWatcher ($49/mo) |
|---------|-------------------|-------------------|-----------------|---------------------|---------------------|
| SERP rank check | Yes | Yes | Yes | Yes | Yes |
| Full SERP extraction | Yes (all 100) | Top 10 | Top 10 | Top 10 | Top 10 |
| SERP features detection | Yes | Yes | Limited | Limited | No |
| Multi-country | Yes (100+) | Yes | Yes | Yes | Yes |
| Multi-language | Yes | Yes | Yes | Limited | Limited |
| API automation | Yes (Apify API) | Yes | Yes | Yes | No |
| Scheduling | Yes (Apify) | Yes | Yes | Yes | Yes |
| Historical tracking | Via scheduled runs | Yes | Yes | Yes | Yes |
| Monthly cost | $0 (pay per run) | $129-499 | $99-999 | $99-499 | $49-199 |

## Quick Start (3 Steps)

1. **Click "Try for free"** on this Actor's page in Apify Store
2. **Enter keywords** and optionally your domain for rank tracking
3. **Click "Start"** and get full SERP data as JSON, CSV, or Excel

## Input

| Field | Type | Default | Description |
|-------|------|---------|-------------|
| `keywords` | string[] | *required* | Keywords to check rankings for |
| `targetUrl` | string | null | Your domain/URL to track position (e.g., `example.com`) |
| `countryCode` | string | `"us"` | Google country code (`us`, `jp`, `gb`, `de`, `fr`, `au`, etc.) |
| `languageCode` | string | `"en"` | Google language code (`en`, `ja`, `es`, `de`, `fr`, etc.) |
| `numResults` | integer | `10` | SERP results per keyword (10, 20, 50, or 100) |
| `includeFeatures` | boolean | `true` | Detect SERP features (snippets, PAA, etc.) |
| `delayMs` | integer | `3000` | Delay between searches in ms (min 1000) |

### Example Input -- Rank Tracking

```json
{
  "keywords": ["best coffee maker", "drip coffee maker review", "coffee maker under 100"],
  "targetUrl": "mycoffeeblog.com",
  "countryCode": "us",
  "languageCode": "en",
  "numResults": 20,
  "includeFeatures": true,
  "delayMs": 3000
}
```

### Example Input -- Japanese SERP Research

```json
{
  "keywords": ["パラグアイ 移住", "格安SIM 比較 2025", "副業 おすすめ"],
  "targetUrl": "nambei-oyaji.com",
  "countryCode": "jp",
  "languageCode": "ja",
  "numResults": 10,
  "delayMs": 3000
}
```

### Example Input -- Competitor Analysis (No Rank Tracking)

```json
{
  "keywords": ["project management software", "crm for small business", "time tracking app"],
  "countryCode": "us",
  "languageCode": "en",
  "numResults": 50,
  "includeFeatures": true
}
```

## Output Example

```json
{
  "keyword": "best coffee maker",
  "success": true,
  "timestamp": "2026-03-29T10:00:00.000Z",
  "countryCode": "us",
  "languageCode": "en",
  "targetUrl": "mycoffeeblog.com",
  "targetRank": 7,
  "totalResults": 10,
  "serpFeatures": ["featured_snippet", "people_also_ask", "shopping_ads"],
  "organicResults": [
    {
      "position": 1,
      "url": "https://www.nytimes.com/wirecutter/reviews/best-drip-coffee-maker/",
      "title": "The Best Drip Coffee Maker (2025) - Wirecutter",
      "snippet": "After over 100 hours of testing 22 drip coffee makers...",
      "domain": "nytimes.com"
    },
    {
      "position": 7,
      "url": "https://mycoffeeblog.com/best-coffee-maker-reviews/",
      "title": "Best Coffee Makers Reviewed and Ranked (2025)",
      "snippet": "We tested 15 coffee makers over 6 months...",
      "domain": "mycoffeeblog.com"
    }
  ]
}
```

## Real-World Use Cases

### 1. Daily Rank Monitoring
Schedule this Actor to run daily. Track your site's position for 20-50 target keywords. Export to Google Sheets via Apify integrations for a free rank tracking dashboard with trend history.

### 2. Competitor SERP Analysis
For each target keyword, extract all top 10 results. Analyze what domains, content types, and word counts dominate the first page to inform your content strategy.

### 3. Content Gap Identification
Check rankings for 100+ keywords in your niche. Identify keywords where you rank 11-20 ("page 2 keywords") -- these are your best optimization opportunities for quick wins.

### 4. SERP Feature Audit
Detect which keywords trigger featured snippets and People Also Ask in your niche. Prioritize these for structured content (Q&A format, tables, lists) that earns position zero.

### 5. Pre-Launch Competitive Research
Before creating a new blog post or product page, check the current top 10 rankings for your target keyword to understand the competition level and content format requirements.

### 6. Client Rank Reporting
Agencies: run weekly rank checks for client keywords, export as CSV, and generate automated ranking reports showing position changes over time.

## FAQ

**Q: How accurate are the ranking positions?**
A: Results reflect Google's search results at the time of the run. Positions can vary slightly by IP, personalization, and time of day. For most SEO purposes, positions within ±1-2 ranks are normal variation.

**Q: Can I track rankings in countries other than the US?**
A: Yes. Set `countryCode` to any two-letter country code (e.g., `jp`, `gb`, `de`, `fr`, `au`, `br`, `in`). Combine with the matching `languageCode` for best results.

**Q: Will Google block the scraper?**
A: The Actor uses browser-like headers and configurable delays. Set `delayMs` to at least 3000ms for reliable operation. For heavy usage (100+ keywords), consider using Apify Proxy.

**Q: Can I detect if my site has a featured snippet?**
A: Yes. The `serpFeatures` field detects `featured_snippet`, `people_also_ask`, `local_pack`, `knowledge_panel`, and `shopping_ads`. Position 0 data requires additional parsing -- currently detected as a feature flag.

**Q: How many keywords can I check in one run?**
A: No hard limit. Processing time = (number of keywords × delayMs). For 50 keywords at 3000ms delay, expect ~3 minutes runtime.

**Q: Can I use a proxy for more reliable results?**
A: Yes. Configure Apify Proxy in Actor settings for higher reliability on large batches or in regions with stricter rate limits.

## Tags

`seo`, `serp`, `rank tracker`, `google search`, `keyword ranking`, `search engine`, `google scraper`, `seo tools`, `rank checking`, `competitor analysis`
