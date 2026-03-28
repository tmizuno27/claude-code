# Free News Aggregator API - Headlines from RSS Feeds and Public Sources

> **Free tier: 500 requests/month** | Aggregated news from multiple free RSS/Atom feeds

Aggregate news headlines and articles from multiple free public sources. Filter by category, search by keyword, and get trending stories. No upstream API keys required.

## Getting Started in 30 Seconds

1. Subscribe on [RapidAPI](https://rapidapi.com/miccho27-5OJaGGbBiO/api/news-aggregator-api) (free plan available)
2. Copy your API key
3. Get your first headlines:

```bash
curl -X GET "https://news-aggregator-api.p.rapidapi.com/top?category=tech" \
  -H "X-RapidAPI-Key: YOUR_KEY" \
  -H "X-RapidAPI-Host: news-aggregator-api.p.rapidapi.com"
```

## How It Compares

| Feature | This API | NewsAPI | Bing News Search | GNews |
|---------|----------|--------|-----------------|-------|
| Free tier | 500 req/mo | 100 req/day (dev only) | 1,000 req/mo | 100 req/day |
| Pro pricing | $5.99/50K | $449/mo | $7/1K txn | $84/mo |
| Categories | Tech, Business, Science, Sports, Health | Yes | Yes | Yes |
| Keyword search | Yes | Yes | Yes | Yes |
| Hacker News integration | Yes | No | No | No |
| Dev.to integration | Yes | No | No | No |
| No upstream API key | Yes (free RSS) | No | No | No |
| Commercial use (free) | Yes | No (dev only) | Yes | No |

## Why Choose This News API?

- **Multi-source** -- aggregates from dozens of free RSS/Atom feeds
- **Category filtering** -- tech, business, science, sports, health, and more
- **Keyword search** -- find articles matching specific topics
- **Developer-focused feeds** -- Hacker News and Dev.to integration
- **No upstream costs** -- uses only free public RSS feeds
- **Free tier** -- 500 requests/month at $0, commercial use allowed

## Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/top` | GET | Top headlines by category |
| `/tech` | GET | Technology news |
| `/business` | GET | Business and finance news |
| `/search` | GET | Search articles by keyword |
| `/hackernews/top` | GET | Top Hacker News stories |
| `/devto/latest` | GET | Latest Dev.to articles |

## Use Cases

- **News apps** -- build custom news feeds for your audience
- **Content curation** -- aggregate industry news for newsletters
- **Market research** -- monitor news mentions of companies or topics
- **Chatbots** -- serve relevant news in conversational interfaces
- **Dashboards** -- display latest headlines in internal tools

## Quick Start

```bash
curl -X GET "https://news-aggregator-api.t-mizuno27.workers.dev/headlines?category=tech" \
  -H "X-RapidAPI-Key: YOUR_KEY"
```

### Python Example

```python
import requests

url = "https://news-aggregator-api.p.rapidapi.com/search"
params = {"q": "artificial intelligence", "limit": 10}
headers = {"X-RapidAPI-Key": "YOUR_KEY", "X-RapidAPI-Host": "news-aggregator-api.p.rapidapi.com"}

data = requests.get(url, headers=headers, params=params).json()
for article in data["articles"]:
    print(f"{article['title']} - {article['source']}")
```

### Node.js Example

```javascript
const axios = require("axios");

const { data } = await axios.get(
  "https://news-aggregator-api.p.rapidapi.com/hackernews/top",
  {
    params: { limit: 10 },
    headers: {
      "X-RapidAPI-Key": "YOUR_KEY",
      "X-RapidAPI-Host": "news-aggregator-api.p.rapidapi.com",
    },
  }
);

data.articles.forEach(a => console.log(`${a.title} (${a.score} points)`));
```

## FAQ

**Q: Can I use this for commercial applications?**
A: Yes. Unlike NewsAPI (which restricts free tier to development only), this API allows commercial use on all plans.

**Q: How frequently is the data updated?**
A: RSS feeds are polled and cached. Most sources update every 15-60 minutes.

**Q: What news sources are included?**
A: Multiple major RSS feeds per category, plus Hacker News and Dev.to. Use the root endpoint to see all available sources.

**Q: Can I get full article content?**
A: The API returns headlines, descriptions, and links. Full article content must be fetched from the source URL.

## Pricing

| Plan | Price | Requests/mo | Rate Limit |
|------|-------|-------------|------------|
| Basic (FREE) | $0 | 500 | 1 req/sec |
| Pro | $5.99 | 50,000 | 10 req/sec |

## Alternative To

A free alternative to NewsAPI, Bing News Search API, and GNews. No upstream API costs, commercial use allowed on free tier.


## Also From This Publisher

Build powerful workflows by combining APIs:

| API | Why Combine? |
|-----|-------------|
| **AI Text API** | Summarize or rewrite news articles |
| **AI Translation API** | Translate news to multiple languages |
| **Text Analysis API** | Sentiment analysis on news headlines |
| **Trends API** | Cross-reference news with trending topics |

> All APIs include a free tier. Subscribe to one, discover the full toolkit on [our RapidAPI profile](https://rapidapi.com/miccho27-5OJaGGbBiO).

## Keywords

`news api`, `news aggregator`, `headlines api`, `rss feed api`, `free news api`, `news search api`, `trending news`, `tech news api`, `news data`, `newsapi alternative`
