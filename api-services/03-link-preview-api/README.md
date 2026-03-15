# Link Preview API

Website metadata extraction API built on Cloudflare Workers. Extracts Open Graph tags, Twitter Cards, favicons, RSS feeds, and more from any URL.

## Endpoints

### GET /preview?url={url}

Extract metadata from a single URL.

```bash
curl "https://link-preview-api.YOUR-SUBDOMAIN.workers.dev/preview?url=https://github.com"
```

**Response:**

```json
{
  "url": "https://github.com",
  "title": "GitHub",
  "description": "Where the world builds software",
  "image": "https://github.githubassets.com/images/modules/open_graph/github-octocat.png",
  "favicon": "https://github.githubassets.com/favicons/favicon.svg",
  "siteName": "GitHub",
  "type": "website",
  "author": null,
  "publishedDate": null,
  "language": "en",
  "keywords": [],
  "twitter": { "card": "summary_large_image", "site": "@github" },
  "themeColor": "#1e2327",
  "canonical": "https://github.com",
  "feeds": [],
  "responseTime": 234
}
```

### POST /preview/bulk

Extract metadata from up to 10 URLs in a single request.

```bash
curl -X POST "https://link-preview-api.YOUR-SUBDOMAIN.workers.dev/preview/bulk" \
  -H "Content-Type: application/json" \
  -d '{"urls": ["https://github.com", "https://example.com"]}'
```

**Response:**

```json
{
  "results": [
    { "url": "https://github.com", "title": "GitHub", "..." : "..." },
    { "url": "https://example.com", "title": "Example Domain", "..." : "..." }
  ]
}
```

## Extracted Metadata

| Field | Sources |
|-------|---------|
| title | og:title, twitter:title, `<title>` |
| description | og:description, meta description |
| image | og:image, twitter:image |
| favicon | link[rel=icon], link[rel=apple-touch-icon], /favicon.ico fallback |
| siteName | og:site_name |
| type | og:type (default: "website") |
| author | meta[name=author], article:author |
| publishedDate | article:published_time, meta[name=date], `<time>` |
| language | html[lang], og:locale |
| keywords | meta[name=keywords] |
| twitter | twitter:card, twitter:site |
| themeColor | meta[name=theme-color] |
| canonical | link[rel=canonical], og:url |
| feeds | link[type=application/rss+xml], link[type=application/atom+xml] |

## Features

- 1-hour response caching via Cloudflare Cache API
- 5-second fetch timeout
- Follows redirects automatically
- Resolves relative URLs for images and favicons
- CORS enabled for browser usage

## Deploy

```bash
npm install
npx wrangler deploy
```

## Configuration (wrangler.toml)

| Variable | Default | Description |
|----------|---------|-------------|
| CACHE_TTL | 3600 | Cache duration in seconds |
| FETCH_TIMEOUT | 5000 | Max fetch time in ms |
| MAX_BULK_URLS | 10 | Max URLs per bulk request |
