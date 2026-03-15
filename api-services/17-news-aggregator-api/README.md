# News Aggregator API

Cloudflare Workers API that aggregates news from free RSS/Atom feeds and public APIs.

## Sources

- **RSS/Atom**: BBC News, NYT, Reuters, TechCrunch, Bloomberg
- **APIs**: Hacker News (Firebase API), Dev.to, HN Algolia Search

## Endpoints

| Method | Path | Description | Cache |
|--------|------|-------------|-------|
| GET | `/` | API info | - |
| GET | `/top` | Top headlines (BBC, NYT, Reuters) | 300s |
| GET | `/tech` | Tech news (TechCrunch + HN + Dev.to) | 300s |
| GET | `/business` | Business news (Reuters, Bloomberg) | 300s |
| GET | `/search?q=<query>` | Search via HN Algolia | 60s |
| GET | `/hackernews/top` | Top 20 Hacker News stories | 300s |
| GET | `/devto/latest` | Latest 20 Dev.to articles | 300s |

## Rate Limiting

30 requests per minute per IP. Size-based cleanup (no timers).

## Development

```bash
npm install
npm run dev
```

## Deployment

```bash
npm run deploy
```
