# Trends Aggregator - Multi-Source Trending Topics (Google, Reddit, Hacker News, GitHub, Product Hunt)

Aggregate trending topics from 5 sources in a single Apify Actor run -- Google Trends, Reddit, Hacker News, GitHub, and Product Hunt. No API keys required. The best free alternative to Exploding Topics, BuzzSumo, SparkToro, Google Trends API wrappers, and Feedly.

## Who Is This For?

- **Content marketers** -- Discover trending topics before competitors and create timely content
- **SEO specialists** -- Identify trending keywords and topics for content calendar planning
- **Product managers** -- Track emerging tools, frameworks, and products in your industry
- **Startup founders** -- Monitor Product Hunt and Hacker News for competitor launches and market signals
- **Developers** -- Track trending GitHub repos and tech discussions on Hacker News
- **Journalists & media** -- Aggregate breaking topics across platforms for story ideas
- **Social media managers** -- Find trending topics to create timely posts that ride the wave

## Sources

| Source | What It Captures | Update Frequency |
|--------|-----------------|-----------------|
| **Google Trends** | Daily trending searches with traffic volume + related news articles | Updates multiple times/day |
| **Hacker News** | Top stories (tech, startups, science, culture) | Updates every few minutes |
| **Reddit** | Trending posts from r/popular (all topics) | Updates every few minutes |
| **GitHub** | Fastest-growing repositories created in the last 7 days | Updates daily |
| **Product Hunt** | Today's top-voted product launches | Updates daily |

## Pricing -- Free to Start

| Tier | Cost | What You Get |
|------|------|-------------|
| **Free trial** | $0 | Apify free tier includes monthly compute credits |
| **Pay per run** | ~$0.01-0.05/run | All 5 sources in one run |
| **vs. Exploding Topics** | Saves $39-249/mo | Real-time data from 5 sources |
| **vs. BuzzSumo** | Saves $199-499/mo | Trending topics + tech/product trends |
| **vs. Feedly AI** | Saves $18-99/mo | No curation needed, raw trending data |

## How It Compares to Paid Trend Tools

| Feature | This Actor (FREE) | Exploding Topics ($39/mo) | BuzzSumo ($199/mo) | SparkToro ($50/mo) | Feedly ($18/mo) |
|---------|-------------------|--------------------------|--------------------|--------------------|----------------|
| Google Trends data | Yes (with traffic volume) | Yes | No | No | No |
| Reddit trending | Yes | No | Limited | No | Yes |
| Hacker News | Yes | No | No | No | Yes |
| GitHub trending repos | Yes | No | No | No | No |
| Product Hunt | Yes | No | No | No | No |
| Region filtering | Yes (Google Trends) | Yes | No | No | No |
| API/automation | Yes (Apify API) | API ($249/mo) | API ($299/mo) | API ($150/mo) | API ($99/mo) |
| Scheduling | Yes (Apify scheduler) | Dashboard only | Dashboard only | Dashboard only | Dashboard only |
| Raw JSON output | Yes | No | CSV export | CSV export | No |
| Monthly cost | $0 (pay per run) | $39-249 | $199-499 | $50-150 | $18-99 |

## Quick Start (3 Steps)

1. **Click "Try for free"** on this Actor's page in Apify Store
2. **Select sources** (Google Trends, Reddit, Hacker News, GitHub, Product Hunt) and region
3. **Click "Start"** and get aggregated trending topics as JSON, CSV, or Excel

## Input

| Field | Type | Default | Description |
|-------|------|---------|-------------|
| `sources` | array | all 5 sources | Which sources to fetch: `google`, `hackernews`, `reddit`, `github`, `producthunt` |
| `googleGeo` | string | `"US"` | ISO country code for Google Trends region (e.g. `US`, `JP`, `GB`, `DE`, `BR`) |
| `limit` | integer | `25` | Max items per source (1-50) |

### Example Input -- All Sources, US Region

```json
{
  "sources": ["google", "hackernews", "reddit", "github", "producthunt"],
  "googleGeo": "US",
  "limit": 25
}
```

### Example Input -- Tech-Focused, Japan Region

```json
{
  "sources": ["google", "hackernews", "github"],
  "googleGeo": "JP",
  "limit": 10
}
```

### Example Input -- Product & Startup Monitoring

```json
{
  "sources": ["producthunt", "hackernews", "github"],
  "limit": 15
}
```

## Output

Each source produces one dataset record:

```json
{
  "source": "hackernews",
  "updated": "2026-03-16T10:00:00.000Z",
  "count": 25,
  "items": [ ... ]
}
```

If a source fails, the record includes an `"error"` field instead of items -- no silent failures.

### Google Trends Item

```json
{
  "title": "Topic name",
  "traffic": "500K+",
  "pubDate": "Mon, 16 Mar 2026 ...",
  "link": "https://trends.google.com/...",
  "relatedArticles": [
    { "title": "...", "url": "...", "source": "..." }
  ]
}
```

### Hacker News Item

```json
{
  "id": 12345678,
  "title": "Show HN: Something cool",
  "url": "https://example.com",
  "score": 342,
  "by": "username",
  "comments": 87,
  "time": 1710000000
}
```

### Reddit Item

```json
{
  "title": "Post title",
  "subreddit": "r/technology",
  "score": 12000,
  "comments": 450,
  "url": "https://www.reddit.com/r/technology/comments/...",
  "author": "username",
  "created_utc": 1710000000
}
```

### GitHub Item

```json
{
  "name": "owner/repo",
  "description": "Repo description",
  "url": "https://github.com/owner/repo",
  "stars": 1200,
  "forks": 80,
  "language": "TypeScript",
  "created_at": "2026-03-10T00:00:00Z"
}
```

### Product Hunt Item

```json
{
  "name": "Product Name",
  "tagline": "Short description",
  "votes": 540,
  "url": "https://www.producthunt.com/posts/...",
  "website": "https://product.com",
  "topics": ["AI", "Productivity"]
}
```

## Real-World Use Cases

### 1. Daily Content Inspiration Dashboard
Schedule this Actor to run every morning. Export to Google Sheets via Apify integrations for a free, auto-updating trend dashboard your content team can reference daily.

### 2. SEO Trend-Jacking
Monitor Google Trends + Reddit for emerging topics in your niche. When a topic spikes, publish content within hours to capture early search traffic.

### 3. Competitive Product Intelligence
Track Product Hunt and GitHub for new tools in your space. Get alerted via webhook when a competitor launches or a relevant open-source project gains traction.

### 4. Tech Stack Trend Monitoring
Filter GitHub trending repos by language to track which frameworks and tools are gaining momentum. Essential for CTOs and engineering managers making technology decisions.

### 5. Newsletter Content Curation
Run weekly across all 5 sources, filter the top items, and use the structured output to auto-generate a trend digest newsletter via n8n, Make, or Zapier.

### 6. Regional Trend Analysis
Compare Google Trends across US, JP, GB, DE, and BR to identify regional content opportunities and localization priorities.

## FAQ

**Q: How often should I run this?**
A: For daily trend monitoring, run once per day. For real-time trend tracking, run every 1-4 hours. Hacker News and Reddit update most frequently; GitHub and Product Hunt are best checked daily.

**Q: Can I filter by specific subreddits or GitHub languages?**
A: Currently, Reddit fetches from r/popular and GitHub fetches all languages. Filtering by specific subreddits or languages is planned for a future update.

**Q: What does the Google Trends "traffic" field mean?**
A: It's Google's estimated daily search volume for that trending topic (e.g., "500K+" means over 500,000 searches that day).

**Q: Can I send results to Slack or email?**
A: Yes. Use Apify's built-in integrations to push results to Slack, email, Google Sheets, webhooks, or any tool via Zapier/Make.

**Q: What if Product Hunt data is unavailable?**
A: Product Hunt's GraphQL API may occasionally require authentication. If unavailable, the record returns `count: 0` with a `note` field. The other 4 sources will still work normally.

**Q: Can I use the Apify API to call this programmatically?**
A: Yes. Full API access via REST or SDKs (Python, JavaScript, Go). Trigger runs, retrieve results, and build automated trend monitoring pipelines.

## Notes

- Product Hunt GraphQL may require authentication; if unavailable the record will have `count: 0` and a `note` field.
- All sources use public endpoints (RSS, JSON APIs, HTML parsing) -- no API keys needed.
