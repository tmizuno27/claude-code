---
title: Build a Multi-Source News Feed in 10 Lines — Free News Aggregator API (NewsAPI Alternative)
tags: api, webdev, javascript, python
published: false
---

NewsAPI.org is great — until you try to use it in production. The free tier blocks commercial use, restricts responses to 100 articles, and enforces a 100-request-per-day limit. By the time you need it for something real, you're looking at $449/month for their business plan.

I built a lightweight alternative that aggregates headlines from Hacker News, Dev.to, and major RSS feeds through a single endpoint. Free tier, commercial use OK, and it runs on Cloudflare's edge so response times are fast.

## What You Get (Free Tier: 500 requests/month)

- Top news from BBC, NYT, Reuters
- Tech news from TechCrunch, Hacker News, Dev.to
- Business news feed
- Full-text search via Hacker News Algolia
- Dev.to trending articles
- Structured JSON: title, URL, published date, source

## Quick Start

### Python — Fetch Tech News

```python
import requests

API_KEY = "your-rapidapi-key"
headers = {
    "x-rapidapi-key": API_KEY,
    "x-rapidapi-host": "news-aggregator-api1.p.rapidapi.com"
}

# Get tech headlines
response = requests.get(
    "https://news-aggregator-api1.p.rapidapi.com/tech",
    headers=headers
)

news = response.json()
for article in news.get("articles", [])[:5]:
    print(f"[{article['source']}] {article['title']}")
    print(f"  {article['url']}\n")
```

### JavaScript — Build a News Dashboard

```javascript
const BASE = 'https://news-aggregator-api1.p.rapidapi.com';
const headers = {
  'x-rapidapi-key': 'your-rapidapi-key',
  'x-rapidapi-host': 'news-aggregator-api1.p.rapidapi.com'
};

async function buildNewsDashboard() {
  // Fetch multiple categories in parallel
  const [top, tech, hn] = await Promise.all([
    fetch(`${BASE}/top`, { headers }).then(r => r.json()),
    fetch(`${BASE}/tech`, { headers }).then(r => r.json()),
    fetch(`${BASE}/hackernews/top`, { headers }).then(r => r.json()),
  ]);

  return {
    topNews: top.articles?.slice(0, 3) || [],
    techNews: tech.articles?.slice(0, 3) || [],
    hackerNews: hn.items?.slice(0, 3) || [],
  };
}

buildNewsDashboard().then(dashboard => {
  console.log('=== Top News ===');
  dashboard.topNews.forEach(a => console.log(`• ${a.title}`));

  console.log('\n=== Tech News ===');
  dashboard.techNews.forEach(a => console.log(`• ${a.title}`));

  console.log('\n=== Hacker News ===');
  dashboard.hackerNews.forEach(a => console.log(`• ${a.title}`));
});
```

## All Endpoints

| Method | Path | Description |
|--------|------|-------------|
| `GET` | `/top` | Headlines from BBC, NYT, Reuters |
| `GET` | `/tech` | Tech news from TechCrunch, HN, Dev.to |
| `GET` | `/business` | Business news from Reuters, Bloomberg |
| `GET` | `/search?q=query` | Full-text search via Hacker News Algolia |
| `GET` | `/hackernews/top` | Top Hacker News stories with scores |
| `GET` | `/devto/latest` | Latest articles from Dev.to |

## Use Case: Slack News Bot

```python
import requests
import json

RAPIDAPI_KEY = "your-rapidapi-key"
SLACK_WEBHOOK = "https://hooks.slack.com/services/YOUR/WEBHOOK/URL"

def post_daily_digest():
    headers = {
        "x-rapidapi-key": RAPIDAPI_KEY,
        "x-rapidapi-host": "news-aggregator-api1.p.rapidapi.com"
    }

    # Get top tech stories
    r = requests.get(
        "https://news-aggregator-api1.p.rapidapi.com/tech",
        headers=headers
    )
    articles = r.json().get("articles", [])[:5]

    # Format for Slack
    blocks = [{"type": "header", "text": {"type": "plain_text", "text": "📰 Daily Tech Digest"}}]
    for article in articles:
        blocks.append({
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": f"*<{article['url']}|{article['title']}>*\n_{article.get('source', 'Unknown')}_"
            }
        })

    requests.post(SLACK_WEBHOOK, json={"blocks": blocks})
    print(f"Posted {len(articles)} articles to Slack")

post_daily_digest()
```

## Use Case: Monitor a Keyword in HN

```python
import requests

def monitor_keyword(keyword: str, min_score: int = 50):
    """Find HN stories mentioning a keyword with significant traction."""
    r = requests.get(
        "https://news-aggregator-api1.p.rapidapi.com/search",
        headers={
            "x-rapidapi-key": "your-rapidapi-key",
            "x-rapidapi-host": "news-aggregator-api1.p.rapidapi.com"
        },
        params={"q": keyword}
    )
    results = r.json().get("hits", [])

    print(f"Top HN results for '{keyword}':")
    for item in results[:5]:
        score = item.get("points", 0)
        if score >= min_score:
            print(f"  [{score} pts] {item['title']}")
            print(f"  {item.get('url', 'N/A')}")

monitor_keyword("Cloudflare Workers")
monitor_keyword("AI API")
```

## Pricing

| Plan | Price | Requests/month | Rate Limit |
|------|-------|----------------|------------|
| Basic (FREE) | $0 | 500 | 1 req/sec |
| Pro | $5.99 | 50,000 | 10 req/sec |
| Ultra | $14.99 | 500,000 | 50 req/sec |

**Available on RapidAPI:** [News Aggregator API](https://rapidapi.com/miccho27-RNuiryMxge/api/news-aggregator-api1)

## How It Compares

| Feature | This API | NewsAPI.org Free | Currents API Free |
|---------|----------|-----------------|-------------------|
| Commercial use | ✅ | ❌ | ✅ |
| Hacker News | ✅ | ❌ | ❌ |
| Dev.to articles | ✅ | ❌ | ❌ |
| Free req/month | 500 | 100/day | 600/day |
| Price for 50K req | $5.99 | $49 | $39 |

## See All My Free APIs

This is one of 24 free APIs I've built on Cloudflare Workers. Others include crypto prices, screenshot capture, SEO analysis, AI translation, and more.

[Browse all 24 APIs on RapidAPI →](https://rapidapi.com/user/miccho27-RNuiryMxge)

---

*Building something with this? I'd love to see it — drop a comment below.*
