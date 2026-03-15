# URL Shortener API

Cloudflare Worker that creates short URLs with click tracking, powered by KV storage.

## Endpoints

| Method | Path | Description |
|--------|------|-------------|
| POST | `/shorten` | Create a short URL |
| GET | `/r/:alias` | Redirect to original URL (301) |
| GET | `/stats/:alias` | Get click statistics |
| DELETE | `/delete/:alias` | Delete a short URL |

## Setup

```bash
npm install

# Create KV namespace
wrangler kv namespace create URL_STORE
wrangler kv namespace create URL_STORE --preview

# Update wrangler.toml with the returned namespace IDs

# Local development
npm run dev

# Deploy
npm run deploy
```

## Usage Examples

### Create short URL (auto-generated alias)
```bash
curl -X POST https://url-shortener-api.t-mizuno27.workers.dev/shorten \
  -H "Content-Type: application/json" \
  -d '{"url": "https://example.com/long/path"}'
```

### Create short URL (custom alias)
```bash
curl -X POST https://url-shortener-api.t-mizuno27.workers.dev/shorten \
  -H "Content-Type: application/json" \
  -d '{"url": "https://example.com", "custom_alias": "my-link"}'
```

### Get statistics
```bash
curl https://url-shortener-api.t-mizuno27.workers.dev/stats/abc123
```

### Delete short URL
```bash
curl -X DELETE https://url-shortener-api.t-mizuno27.workers.dev/delete/abc123
```
