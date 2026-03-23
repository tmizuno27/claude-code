# Free Trends API - Trending Topics from Multiple Public Sources

> **Free tier: 500 requests/month** | Aggregated trending data from Google, Reddit, HN, GitHub, Product Hunt

Get trending topics, hashtags, and stories from multiple public sources. Track what's trending in real time across tech, social media, and news.

## Getting Started in 30 Seconds

1. Subscribe on [RapidAPI](https://rapidapi.com/miccho27-5OJaGGbBiO/api/trends-api) (free plan available)
2. Copy your API key
3. Get today's trending topics:

```bash
curl -X GET "https://trends-api.p.rapidapi.com/google/daily" \
  -H "X-RapidAPI-Key: YOUR_KEY" \
  -H "X-RapidAPI-Host: trends-api.p.rapidapi.com"
```

## How It Compares

| Feature | This API | Google Trends | Exploding Topics | BuzzSumo |
|---------|----------|--------------|-----------------|----------|
| Free tier | 500 req/mo | Web only | 10 searches/mo | None |
| Pro pricing | $5.99/50K | No API | $39/mo | $99/mo |
| Google Trends | Yes (daily) | Yes | Limited | No |
| Hacker News | Yes (top stories) | No | No | No |
| Reddit trending | Yes (r/popular) | No | No | Yes |
| GitHub trending | Yes (new repos) | No | No | No |
| Product Hunt | Yes (today's top) | No | No | No |
| API access | Yes (REST) | Unofficial only | Yes | Yes |
| Multi-source in 1 call | Yes (5 sources) | No | No | No |

## Why Choose This Trends API?

- **Multi-source** -- aggregates trends from 5 platforms in one API
- **Real-time** -- updated frequently to capture emerging trends
- **Developer-focused** -- includes GitHub trending repos and Hacker News
- **No upstream costs** -- uses only free public sources
- **Free tier** -- 500 requests/month at $0

## Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/google/daily` | GET | Google Trends daily trending searches |
| `/hackernews/trending` | GET | Top Hacker News stories |
| `/reddit/trending` | GET | Trending posts from r/popular |
| `/github/trending` | GET | Fastest-growing new GitHub repos |
| `/producthunt/today` | GET | Today's top Product Hunt products |

## Use Cases

- **Content marketing** -- discover trending topics for timely content creation
- **Social media tools** -- show users what's trending to inspire posts
- **News apps** -- surface trending stories alongside regular news
- **Market research** -- track trending topics in your industry
- **SEO** -- find trending keywords for content optimization

## Quick Start

```bash
curl -X GET "https://trends-api.t-mizuno27.workers.dev/trending" \
  -H "X-RapidAPI-Key: YOUR_KEY"
```

### Python Example

```python
import requests

url = "https://trends-api.p.rapidapi.com/github/trending"
headers = {"X-RapidAPI-Key": "YOUR_KEY", "X-RapidAPI-Host": "trends-api.p.rapidapi.com"}

data = requests.get(url, headers=headers).json()
for repo in data["items"][:10]:
    print(f"{repo['name']} - {repo['stars']} stars - {repo['language']}")
```

### Node.js Example

```javascript
const axios = require("axios");

const { data } = await axios.get(
  "https://trends-api.p.rapidapi.com/reddit/trending",
  {
    params: { limit: 10 },
    headers: {
      "X-RapidAPI-Key": "YOUR_KEY",
      "X-RapidAPI-Host": "trends-api.p.rapidapi.com",
    },
  }
);

data.items.forEach(post => {
  console.log(`${post.title} (${post.subreddit}, ${post.score} upvotes)`);
});
```

## FAQ

**Q: How often is the data updated?**
A: Google Trends updates daily. Hacker News and Reddit update every 15-30 minutes. GitHub trending updates every few hours. Product Hunt updates daily.

**Q: Can I filter by country/region?**
A: Google Trends supports a `geo` parameter (e.g., `US`, `JP`, `GB`). Other sources are global.

**Q: Can I get all 5 sources in one API call?**
A: Each source has its own endpoint. Call them in parallel for the fastest multi-source aggregation.

**Q: Is Product Hunt data always available?**
A: Product Hunt uses GraphQL which may require authentication. If unavailable, the response will include a note explaining the limitation.

## Pricing

| Plan | Price | Requests/mo | Rate Limit |
|------|-------|-------------|------------|
| Basic (FREE) | $0 | 500 | 1 req/sec |
| Pro | $5.99 | 50,000 | 10 req/sec |

## Alternative To

A free alternative to Google Trends API (unofficial), Exploding Topics, and BuzzSumo. The only API combining 5 trending sources in one service.

## Keywords

`trends api`, `trending topics api`, `social trends`, `real-time trends`, `free trends api`, `hashtag trends`, `trending news`, `viral topics`, `content trends`, `google trends alternative`
