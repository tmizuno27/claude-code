# Trends API

Cloudflare Workers API that aggregates trending topic data from multiple public sources.

## Endpoints

| Method | Path | Cache | Description |
|--------|------|-------|-------------|
| GET | `/` | — | API info |
| GET | `/google/daily?geo=US` | 600s | Google daily trending searches |
| GET | `/hackernews/trending` | 300s | Top 25 Hacker News stories |
| GET | `/reddit/trending` | 600s | Top 25 Reddit r/popular posts |
| GET | `/github/trending` | 1800s | Top 25 new GitHub repos (past 7 days) |
| GET | `/producthunt/today` | 600s | Today's top Product Hunt products |

### Google Trends geo parameter

Supported country codes: `US`, `JP`, `GB`, `DE`, `FR`, `BR`, `IN`, and any code supported by Google Trends.

## Rate Limiting

20 requests per minute per IP. Returns `429` when exceeded.

## Development

```bash
npm install
npm run dev
```

## Deploy

```bash
npm run deploy
```
