# Free News Aggregator API - Headlines from RSS Feeds and Public Sources

> **Free tier: 500 requests/month** | Aggregated news from multiple free RSS/Atom feeds

Aggregate news headlines and articles from multiple free public sources. Filter by category, search by keyword, and get trending stories. No upstream API keys required.

## Why Choose This News API?

- **Multi-source** -- aggregates from dozens of free RSS/Atom feeds
- **Category filtering** -- tech, business, science, sports, health, and more
- **Keyword search** -- find articles matching specific topics
- **No upstream costs** -- uses only free public RSS feeds
- **Free tier** -- 500 requests/month at $0

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

## Pricing

| Plan | Price | Requests/mo | Rate Limit |
|------|-------|-------------|------------|
| Basic (FREE) | $0 | 500 | 1 req/sec |
| Pro | $5.99 | 50,000 | 10 req/sec |

## Alternative To

A free alternative to NewsAPI, Bing News Search API, and GNews.

## Keywords

`news api`, `news aggregator`, `headlines api`, `rss feed api`, `free news api`, `news search api`, `trending news`, `tech news api`, `news data`, `newsapi alternative`
