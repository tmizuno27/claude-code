# WP Internal Link Optimization API

Cloudflare Workers API that analyzes WordPress article content and suggests internal links based on keyword matching and relevance scoring.

## Endpoints

### POST /analyze
Analyze article HTML against a sitemap or list of existing pages. Returns ranked internal link suggestions with anchor text, confidence scores, and insert positions.

**Request body:**
```json
{
  "article_html": "<h1>My Article</h1><p>Content about WordPress SEO...</p>",
  "article_title": "My Article Title",
  "sitemap_url": "https://example.com/sitemap.xml",
  "pages": [
    { "url": "https://example.com/page1", "title": "Page One", "content": "optional content" }
  ]
}
```
Provide either `sitemap_url` OR `pages`, not both required.

### POST /suggest
Lightweight keyword-to-URL matching. Returns keyword matches found in article text that correspond to existing page titles.

**Request body:**
```json
{
  "article_text": "Plain text content about WordPress SEO optimization...",
  "pages": [
    { "url": "https://example.com/seo-guide", "title": "SEO Optimization Guide" }
  ]
}
```

### GET /health
Returns `{ "status": "ok" }`.

## Development

```bash
npm install
npm run dev      # Local dev server
npm run deploy   # Deploy to Cloudflare
```

## Pricing (RapidAPI)

| Plan | Price | Requests/month |
|------|-------|---------------|
| Free | $0 | 100 |
| Pro | $9.99 | 1,000 |
| Ultra | $29.99 | 10,000 |
