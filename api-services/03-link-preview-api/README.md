# Free Link Preview API - Open Graph, Twitter Cards, Metadata Extraction

> **Free tier: 500 requests/month** | Extract rich metadata from any URL in milliseconds

Extract Open Graph tags, Twitter Cards, favicons, RSS feeds, author info, and more from any URL. Supports bulk extraction (up to 10 URLs). Built on Cloudflare Workers with 1-hour caching.

## Why Choose This Link Preview API?

- **Rich metadata** -- title, description, image, favicon, author, published date, language, keywords
- **Social tags** -- Open Graph and Twitter Card extraction
- **RSS/Atom discovery** -- automatically finds feed URLs
- **Bulk extraction** -- process up to 10 URLs in a single request
- **1-hour cache** -- repeated URLs served instantly from edge cache
- **Free tier** -- 500 requests/month at $0

## Use Cases

- **Chat apps** -- generate rich link previews like Slack, Discord, or WhatsApp
- **Social media tools** -- preview how links will appear when shared
- **Content aggregators** -- extract metadata for news feeds and bookmarking apps
- **SEO tools** -- verify Open Graph and meta tags across pages
- **CMS plugins** -- auto-fill title, description, and image when embedding links
- **Bookmark managers** -- enrich saved URLs with metadata

## Quick Start

```bash
curl -X GET "https://link-preview-api.t-mizuno27.workers.dev/preview?url=https://github.com" \
  -H "X-RapidAPI-Key: YOUR_KEY"
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
  "language": "en",
  "twitter": { "card": "summary_large_image", "site": "@github" },
  "feeds": [],
  "responseTime": 234
}
```

### Bulk Preview (up to 10 URLs)

```bash
curl -X POST "https://link-preview-api.t-mizuno27.workers.dev/preview/bulk" \
  -H "Content-Type: application/json" \
  -d '{"urls": ["https://github.com", "https://example.com"]}'
```

### Python Example

```python
import requests

url = "https://link-preview-api.p.rapidapi.com/preview"
params = {"url": "https://github.com"}
headers = {"X-RapidAPI-Key": "YOUR_KEY", "X-RapidAPI-Host": "link-preview-api.p.rapidapi.com"}

data = requests.get(url, headers=headers, params=params).json()
print(f"{data['title']}: {data['description']}")
```

## Pricing

| Plan | Price | Requests/mo | Rate Limit |
|------|-------|-------------|------------|
| Basic (FREE) | $0 | 500 | 1 req/sec |
| Pro | $5.99 | 50,000 | 10 req/sec |

## Alternative To

A free alternative to LinkPreview.net, Microlink, and OpenGraph.io.

## Keywords

`link preview api`, `url metadata`, `open graph api`, `twitter card extractor`, `unfurl url`, `website metadata`, `free link preview`, `og tags api`, `url preview`, `social media preview`
