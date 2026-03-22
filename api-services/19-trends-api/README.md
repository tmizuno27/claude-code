# Free Trends API - Trending Topics from Multiple Public Sources

> **Free tier: 500 requests/month** | Aggregated trending data from social media and news

Get trending topics, hashtags, and stories from multiple public sources. Track what's trending in real time across tech, social media, and news.

## Why Choose This Trends API?

- **Multi-source** -- aggregates trends from multiple public data sources
- **Real-time** -- updated frequently to capture emerging trends
- **Category filtering** -- filter by topic area (tech, entertainment, business, etc.)
- **No upstream costs** -- uses only free public sources
- **Free tier** -- 500 requests/month at $0

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

url = "https://trends-api.p.rapidapi.com/trending"
headers = {"X-RapidAPI-Key": "YOUR_KEY", "X-RapidAPI-Host": "trends-api.p.rapidapi.com"}

data = requests.get(url, headers=headers).json()
for trend in data["trends"][:10]:
    print(f"#{trend['rank']}: {trend['topic']}")
```

## Pricing

| Plan | Price | Requests/mo | Rate Limit |
|------|-------|-------------|------------|
| Basic (FREE) | $0 | 500 | 1 req/sec |
| Pro | $5.99 | 50,000 | 10 req/sec |

## Alternative To

A free alternative to Google Trends API, Exploding Topics, and BuzzSumo.

## Keywords

`trends api`, `trending topics api`, `social trends`, `real-time trends`, `free trends api`, `hashtag trends`, `trending news`, `viral topics`, `content trends`, `google trends alternative`
