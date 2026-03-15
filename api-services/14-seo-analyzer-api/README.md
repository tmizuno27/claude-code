# SEO Analyzer API

Cloudflare Workers API that analyzes any URL's SEO elements and returns a detailed report with scoring.

## Endpoints

| Method | Path | Description |
|--------|------|-------------|
| GET | `/` | API info |
| GET | `/analyze?url=<url>` | Full SEO analysis |
| GET | `/headings?url=<url>` | Heading structure only |
| GET | `/links?url=<url>` | Link analysis only |
| GET | `/score?url=<url>` | SEO score with breakdown |

## Analysis Includes

- **Title** — text, length, optimal range check (30-60 chars)
- **Meta description** — text, length, optimal range check (120-160 chars)
- **Headings** — H1-H6 counts and texts
- **Images** — total count, with/without alt text
- **Links** — internal, external, nofollow counts
- **Canonical URL**
- **Robots meta** — index/nofollow directives
- **Open Graph tags**
- **Twitter Card tags**
- **JSON-LD structured data**
- **Page size** (bytes)
- **Word count**
- **Language attribute**
- **Viewport meta tag**
- **Favicon**
- **Hreflang tags**
- **SEO Score** — 0-100 based on 19 weighted checks

## Rate Limiting

20 requests per minute per IP. Returns `429` with `Retry-After` header when exceeded.

## Development

```bash
npm install
npm run dev
```

## Deployment

```bash
npm run deploy
```
