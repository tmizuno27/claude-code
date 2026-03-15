# Crypto Data API

Cloudflare Workers API that aggregates cryptocurrency data from CoinGecko's free API.

## Endpoints

| Method | Path | Description |
|--------|------|-------------|
| GET | `/` | API info and endpoint list |
| GET | `/price?ids=bitcoin,ethereum&vs=usd` | Current prices (multiple coins/currencies) |
| GET | `/coin/:id` | Detailed coin info (market cap, volume, ATH, etc.) |
| GET | `/search?q=bitcoin` | Search coins by name/symbol |
| GET | `/trending` | Top trending coins |
| GET | `/markets?vs=usd&per_page=100&page=1` | Market listings with pagination |
| GET | `/history?id=bitcoin&date=2025-01-15` | Historical price on specific date |
| GET | `/exchanges` | List top exchanges |
| GET | `/global` | Global crypto market stats |

## Cache TTLs

- Price data: 60s
- Coin details: 300s
- Markets: 60s
- Search: 300s
- Trending: 600s
- History: 3600s
- Exchanges: 600s
- Global: 600s

## Rate Limits

- API: 30 requests/min per IP
- CoinGecko free tier: ~30 calls/min (handled with caching)

## Development

```bash
npm install
npm run dev      # Local dev server
npm run deploy   # Deploy to Cloudflare
```

## Response Format

All responses use a consistent wrapper:

```json
{
  "success": true,
  "data": { ... }
}
```

Error responses:

```json
{
  "success": false,
  "error": "Error message"
}
```

## Data Source

[CoinGecko API v3](https://www.coingecko.com/en/api) (free tier, no API key required).
