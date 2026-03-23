# Trends Aggregator - Multi-Source Trending Topics (Google, Reddit, HN, GitHub, PH)

Aggregate trending topics from 5 sources in a single Apify Actor run. No API keys required. A free alternative to Exploding Topics, BuzzSumo, and Google Trends API wrappers.

## Sources

| Source | Description |
|--------|-------------|
| `google` | Google Trends daily trending searches (with related news articles) |
| `hackernews` | Top stories from Hacker News |
| `reddit` | Trending posts from r/popular |
| `github` | Fastest-growing GitHub repositories created in the last 7 days |
| `producthunt` | Today's top products on Product Hunt |

## Input

| Field | Type | Default | Description |
|-------|------|---------|-------------|
| `sources` | array | all 5 sources | Which sources to fetch: `google`, `hackernews`, `reddit`, `github`, `producthunt` |
| `googleGeo` | string | `"US"` | ISO country code for Google Trends region (e.g. `US`, `JP`, `GB`) |
| `limit` | integer | `25` | Max items per source (1–50) |

### Example input

```json
{
  "sources": ["google", "hackernews", "github"],
  "googleGeo": "JP",
  "limit": 10
}
```

## Output

Each source produces one dataset record with the structure:

```json
{
  "source": "hackernews",
  "updated": "2026-03-16T10:00:00.000Z",
  "count": 25,
  "items": [ ... ]
}
```

If a source fails, the record will include an `"error"` field instead of items.

### Google item shape

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

### Hacker News item shape

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

### Reddit item shape

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

### GitHub item shape

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

### Product Hunt item shape

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

## Why Choose This Actor?

- **5 sources in 1 run** -- Google Trends, Hacker News, Reddit, GitHub, Product Hunt
- **No API keys** -- all sources are public (RSS, JSON APIs, HTML parsing)
- **Region support** -- Google Trends supports country-specific trending topics
- **Configurable limits** -- control how many items per source (1-50)
- **Structured output** -- clean JSON with timestamps, scores, and source attribution

## FAQ

**Q: How often should I run this?**
A: For daily trend monitoring, run once per day. For real-time trend tracking, run every 1-4 hours. Hacker News and Reddit update most frequently.

**Q: Can I filter by specific subreddits or GitHub languages?**
A: Currently, Reddit fetches from r/popular and GitHub fetches all languages. Filtering by specific subreddits or languages is planned for a future update.

**Q: What does the Google Trends "traffic" field mean?**
A: It's Google's estimated daily search volume for that trending topic (e.g., "500K+" means over 500,000 searches).

## Notes

- Product Hunt GraphQL may require authentication; if unavailable the record will have `count: 0` and a `note` field.
- This Actor is a port of the [19-trends-api](../../19-trends-api/) Cloudflare Worker, adapted for the Apify platform.
