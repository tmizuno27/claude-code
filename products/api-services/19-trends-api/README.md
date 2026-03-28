# Trends Aggregator API - 5 Trending Sources in 1 API (The Only Multi-Source Trends API)

**The only API that aggregates trending topics from Google Trends, Hacker News, Reddit, GitHub, and Product Hunt in a single service.** No other API does this. Each source has its own endpoint with structured JSON responses.

> Free tier: 500 requests/month | 5 platforms | Updated every 15-30 min | No credit card required

## The Problem This Solves

You want trending data from multiple platforms for content strategy, market research, or a news dashboard. Today, you need:
- Google Trends: No official API (scraping or expensive SerpAPI at $50/mo)
- Hacker News: Free API, but raw and needs parsing
- Reddit: OAuth required, rate-limited, complex auth flow
- GitHub: REST API, but no "trending" endpoint (scraping required)
- Product Hunt: GraphQL API, requires application approval

**This API gives you all 5 in one RapidAPI subscription.** Structured JSON, documented endpoints, no auth complexity.

## What Makes This Unique

| Feature | **This API** | SerpAPI Trends | Google Trends | BuzzSumo | Exploding Topics |
|---------|---|---|---|---|---|
| **Sources** | **5 platforms** | Google only | Google only | Social only | Google + social |
| **Free tier** | 500 req/mo | None | Web only (no API) | None | 10 searches/mo |
| **Price** | $5.99/50K | $50/mo (5K) | N/A | $99/mo | $39/mo |
| **Google Trends** | Daily trending | Yes | Web UI only | No | Limited |
| **Hacker News** | Top 25 stories | No | No | No | No |
| **Reddit** | Top 25 r/popular | No | No | Yes | No |
| **GitHub repos** | Top 25 trending | No | No | No | No |
| **Product Hunt** | Today's top | No | No | No | No |
| **Multi-source in 1 API** | **Yes** | No | No | No | No |

## Quick Start - Python

```python
import requests
import concurrent.futures

headers = {
    "X-RapidAPI-Key": "YOUR_KEY",
    "X-RapidAPI-Host": "trends-api.p.rapidapi.com"
}
base = "https://trends-api.p.rapidapi.com"

# Fetch all 5 sources in parallel
def fetch(endpoint):
    return requests.get(f"{base}{endpoint}", headers=headers).json()

with concurrent.futures.ThreadPoolExecutor() as executor:
    futures = {
        "google": executor.submit(fetch, "/google/daily?geo=US"),
        "hackernews": executor.submit(fetch, "/hackernews/trending"),
        "reddit": executor.submit(fetch, "/reddit/trending"),
        "github": executor.submit(fetch, "/github/trending"),
        "producthunt": executor.submit(fetch, "/producthunt/today"),
    }

    for source, future in futures.items():
        data = future.result()
        print(f"\n--- {source.upper()} ---")
        for item in data.get("items", [])[:5]:
            print(f"  {item.get('title', item.get('name', 'N/A'))}")
```

## Quick Start - JavaScript / Node.js

```javascript
const axios = require("axios");

const headers = {
  "X-RapidAPI-Key": "YOUR_KEY",
  "X-RapidAPI-Host": "trends-api.p.rapidapi.com",
};
const base = "https://trends-api.p.rapidapi.com";

// Fetch all 5 sources in parallel
const [google, hn, reddit, github, ph] = await Promise.all([
  axios.get(`${base}/google/daily?geo=US`, { headers }),
  axios.get(`${base}/hackernews/trending`, { headers }),
  axios.get(`${base}/reddit/trending`, { headers }),
  axios.get(`${base}/github/trending`, { headers }),
  axios.get(`${base}/producthunt/today`, { headers }),
]);

console.log("Google Trends:", google.data.items.slice(0, 5).map(i => i.title));
console.log("Hacker News:", hn.data.items.slice(0, 5).map(i => i.title));
console.log("Reddit:", reddit.data.items.slice(0, 5).map(i => i.title));
console.log("GitHub:", github.data.items.slice(0, 5).map(i => i.name));
console.log("Product Hunt:", ph.data.items.slice(0, 5).map(i => i.name));
```

## Endpoints

| Endpoint | Method | Source | Update Frequency | Returns |
|----------|--------|--------|------------------|---------|
| `/google/daily` | GET | Google Trends | Daily | Trending search topics with traffic estimates |
| `/hackernews/trending` | GET | Hacker News | Every 15 min | Top 25 stories with scores and comments |
| `/reddit/trending` | GET | Reddit | Every 15 min | Top 25 posts from r/popular with upvotes |
| `/github/trending` | GET | GitHub | Every few hours | Top 25 fastest-growing repos with stars |
| `/producthunt/today` | GET | Product Hunt | Daily | Today's top products with descriptions |

### Parameters

| Endpoint | Parameter | Type | Default | Description |
|----------|-----------|------|---------|-------------|
| `/google/daily` | `geo` | string | `US` | Country code: US, JP, GB, DE, FR, BR, etc. |

## Real-World Use Cases

### Content Marketing Dashboard
Build a "What's trending now" widget for your content team. Writers pick trending topics from 5 sources, ensuring timely, relevant content that captures search demand.

### AI Newsletter Generator
Fetch trending topics from all 5 sources, feed them to an LLM, and auto-generate a daily newsletter. Each source covers a different angle: Google (search demand), HN (tech), Reddit (social), GitHub (developer tools), PH (new products).

### Social Media Scheduling Tool
Surface trending topics in your scheduling app. Help users create posts about what's trending right now, improving engagement and reach.

### Market Research / Competitive Intelligence
Track when competitor products trend on Product Hunt or GitHub. Monitor industry-related trending searches on Google. Get early signals from Hacker News discussions.

### SEO Content Strategy
Find trending search queries from Google Trends, validate demand via Reddit/HN discussion volume, and create content that captures rising search traffic.

### Developer Dashboard / CLI Tool
Build a `trends` CLI that shows the top 5 from each source every morning. Start your day knowing what's happening across tech, social, and business.

## Pricing

| Plan | Price | Requests/mo | Rate Limit | Cost per Request |
|------|-------|-------------|------------|------------------|
| **Basic (FREE)** | $0 | 500 | 1/sec | $0 |
| **Pro** | $5.99 | 50,000 | 10/sec | $0.00012 |
| **Ultra** | $14.99 | 500,000 | 50/sec | $0.00003 |

Compare: SerpAPI Trends = $50/mo for 5K searches (Google only). BuzzSumo = $99/mo. Exploding Topics = $39/mo.

## FAQ

**Q: How often is the data updated?**
A: Google Trends: daily. Hacker News and Reddit: every 15-30 minutes. GitHub: every few hours. Product Hunt: daily.

**Q: Can I filter by country?**
A: Google Trends supports the `geo` parameter (e.g., US, JP, GB). Other sources are global.

**Q: Can I get all 5 sources in one call?**
A: Each source has its own endpoint. Call all 5 in parallel (see Python/JS examples above) for the fastest aggregation. This design means you only pay for the sources you need.

**Q: What if Product Hunt data is unavailable?**
A: Product Hunt uses GraphQL which may require authentication. If unavailable, the response includes a note explaining the limitation.

**Q: How does this compare to building my own scrapers?**
A: You save the time of building and maintaining 5 separate scrapers, handling rate limits, auth flows (Reddit OAuth, PH GraphQL), and parsing different response formats. This API normalizes everything into consistent JSON.


## Also From This Publisher

Build powerful workflows by combining APIs:

| API | Why Combine? |
|-----|-------------|
| **News Aggregator API** | Get full articles for trending topics |
| **AI Text API** | Generate content about trending topics |
| **Social Video API** | Find trending videos on social platforms |
| **Crypto Data API** | Track trending cryptocurrencies |

> All APIs include a free tier. Subscribe to one, discover the full toolkit on [our RapidAPI profile](https://rapidapi.com/miccho27-5OJaGGbBiO).

## Keywords

`trends api`, `trending topics api`, `google trends api`, `multi-source trends`, `social listening api`, `hacker news api`, `reddit trending api`, `github trending api`, `product hunt api`, `content marketing api`, `serpapi alternative`, `trend monitoring`, `viral topics api`, `real-time trends`
