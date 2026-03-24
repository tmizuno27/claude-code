---
title: "How to Build a Trending Topics Dashboard with One API Call — Google, Reddit, HN, GitHub, Product Hunt"
published: false
tags: api, webdev, javascript, python
cover_image:
---

Every content creator, marketer, and indie hacker needs to know what's trending *right now*. But scraping Google Trends, Reddit, Hacker News, GitHub, and Product Hunt individually? That's 5 different APIs, 5 auth flows, and a maintenance nightmare.

I built a **single API** that aggregates trending topics from all five sources in one call. It runs on Cloudflare Workers (300+ edge locations, sub-50ms latency) and costs $0 to try.

## What You Get

One `GET /trends` request returns:

- **Google Trends** — top daily & real-time searches
- **Reddit** — r/all hot posts
- **Hacker News** — front page stories with scores
- **GitHub** — trending repos (daily/weekly)
- **Product Hunt** — daily top products

Each item includes: title, URL, source, score/votes, and timestamp.

## Quick Start

### Python — Get All Trending Topics

```python
import requests

url = "https://trends-api.p.rapidapi.com/trends"
headers = {
    "X-RapidAPI-Key": "YOUR_KEY",
    "X-RapidAPI-Host": "trends-api.p.rapidapi.com"
}

response = requests.get(url, headers=headers)
data = response.json()

for source, items in data["trends"].items():
    print(f"\n--- {source.upper()} ---")
    for item in items[:3]:
        print(f"  {item['title']} ({item.get('score', 'N/A')} pts)")
```

### JavaScript — Filter by Source

```javascript
const response = await fetch(
  "https://trends-api.p.rapidapi.com/trends?source=github",
  {
    headers: {
      "X-RapidAPI-Key": "YOUR_KEY",
      "X-RapidAPI-Host": "trends-api.p.rapidapi.com"
    }
  }
);
const { trends } = await response.json();
console.log("Trending GitHub repos:", trends.github);
```

## Real-World Use Cases

1. **Content Calendar Generator** — Fetch trending topics weekly, auto-generate blog post ideas based on overlap between Google Trends and Reddit
2. **Slack Bot** — Post a daily digest of what's hot in your niche to #general
3. **Competitor Monitoring** — Track when competitors appear on Product Hunt or HN
4. **SEO Content Brief** — Cross-reference Google Trends with HN/Reddit to find topics with both search demand and community interest

## How It Compares

| Feature | Trends API | Google Trends API | Social Mention | BuzzSumo |
|---------|-----------|-------------------|----------------|----------|
| Sources | 5 in 1 | Google only | Social only | Web + Social |
| Free tier | 500 req/mo | Unofficial only | Shut down | $0 free tier |
| Auth complexity | API key only | OAuth + scraping | N/A | OAuth |
| Latency | <50ms | Varies | N/A | 200ms+ |
| Price (paid) | $5.99/mo | N/A | N/A | $99/mo |

## Try It Now (Free)

1. Go to [Trends API on RapidAPI](https://rapidapi.com/miccho27-5OJaGGbBiO/api/trends-api)
2. Subscribe to free plan (500 requests/month)
3. Hit "Test Endpoint" — see results instantly

---

**What trending data source would you add?** Drop a comment — I'm actively building based on feedback.

*Built with Cloudflare Workers. Zero cold starts, zero external dependencies, zero excuses.*
