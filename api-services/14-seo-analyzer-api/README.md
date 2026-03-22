# Free SEO Analyzer API - On-Page SEO Audit with Scoring

> **Free tier: 500 requests/month** | Analyze any URL's SEO elements and get a detailed score (0-100)

Analyze any web page's SEO elements including title, meta description, headings, images, links, Open Graph, Twitter Cards, JSON-LD structured data, and more. Returns a weighted SEO score (0-100) based on 19 checks. Built on Cloudflare Workers.

## Why Choose This SEO Analyzer API?

- **Comprehensive audit** -- 19 weighted SEO checks covering on-page elements, structure, and metadata
- **SEO score** -- 0-100 score with detailed breakdown per check
- **Structured data detection** -- parses JSON-LD, Open Graph, and Twitter Card tags
- **Granular endpoints** -- full analysis, headings only, links only, or score only
- **Fast** -- sub-500ms analysis powered by Cloudflare Workers edge network
- **Free tier** -- 500 requests/month at $0

## Use Cases

- **SEO auditing tools** -- build page-level SEO audits into your SaaS product
- **Content management** -- validate SEO elements before publishing articles
- **Competitor analysis** -- compare your pages against competitor SEO scores
- **CI/CD pipelines** -- automated SEO checks on every deploy
- **Agency dashboards** -- bulk audit client websites and track improvements
- **Chrome extensions** -- show real-time SEO scores for any page

## Quick Start

### Full SEO Analysis

```bash
curl -X GET "https://seo-analyzer-api.t-mizuno27.workers.dev/analyze?url=https://example.com" \
  -H "X-RapidAPI-Key: YOUR_KEY"
```

**Response (abbreviated):**
```json
{
  "url": "https://example.com",
  "seo_score": 72,
  "title": {
    "text": "Example Domain",
    "length": 14,
    "optimal": false
  },
  "meta_description": {
    "text": null,
    "length": 0,
    "optimal": false
  },
  "headings": {
    "h1": 1,
    "h2": 0,
    "h3": 0
  },
  "images": {
    "total": 0,
    "with_alt": 0,
    "without_alt": 0
  },
  "links": {
    "internal": 0,
    "external": 1,
    "nofollow": 0
  },
  "open_graph": { "title": null },
  "twitter_card": { "card": null },
  "structured_data": [],
  "word_count": 29,
  "page_size_bytes": 1256
}
```

### Get SEO Score Only

```bash
curl "https://seo-analyzer-api.t-mizuno27.workers.dev/score?url=https://example.com"
```

### Heading Structure Only

```bash
curl "https://seo-analyzer-api.t-mizuno27.workers.dev/headings?url=https://example.com"
```

### Link Analysis Only

```bash
curl "https://seo-analyzer-api.t-mizuno27.workers.dev/links?url=https://example.com"
```

### Python Example

```python
import requests

url = "https://seo-analyzer-api.p.rapidapi.com/analyze"
params = {"url": "https://example.com"}
headers = {
    "X-RapidAPI-Key": "YOUR_KEY",
    "X-RapidAPI-Host": "seo-analyzer-api.p.rapidapi.com"
}

response = requests.get(url, headers=headers, params=params)
data = response.json()
print(f"SEO Score: {data['seo_score']}/100")
print(f"Title: {data['title']['text']} ({data['title']['length']} chars)")
```

### Node.js Example

```javascript
const axios = require("axios");

const { data } = await axios.get(
  "https://seo-analyzer-api.p.rapidapi.com/analyze",
  {
    params: { url: "https://example.com" },
    headers: {
      "X-RapidAPI-Key": "YOUR_KEY",
      "X-RapidAPI-Host": "seo-analyzer-api.p.rapidapi.com",
    },
  }
);

console.log(`SEO Score: ${data.seo_score}/100`);
```

## Analysis Includes

| Element | Details |
|---------|---------|
| **Title** | Text, length, optimal range check (30-60 chars) |
| **Meta Description** | Text, length, optimal range check (120-160 chars) |
| **Headings** | H1-H6 counts and texts |
| **Images** | Total count, with/without alt text |
| **Links** | Internal, external, nofollow counts |
| **Canonical URL** | Present and correct |
| **Robots Meta** | Index/nofollow directives |
| **Open Graph** | Title, description, image |
| **Twitter Card** | Card type, title, description |
| **JSON-LD** | Structured data schemas |
| **Page Metrics** | Size (bytes), word count, language, viewport |
| **Favicon** | Present or missing |
| **Hreflang** | International targeting tags |

## Pricing

| Plan | Price | Requests/mo | Rate Limit |
|------|-------|-------------|------------|
| Basic (FREE) | $0 | 500 | 20 req/min |
| Pro | $9.99 | 50,000 | 100 req/min |
| Ultra | $24.99 | 500,000 | 500 req/min |

## Alternative To

A free alternative to Ahrefs Site Audit API, Moz API, and Screaming Frog. Get instant on-page SEO analysis without monthly subscriptions or complex setup.

## Keywords

`seo analyzer api`, `seo audit api`, `on-page seo`, `website seo score`, `seo check api`, `meta tag analyzer`, `heading analysis`, `structured data checker`, `free seo api`, `page audit api`

## Development

```bash
npm install
npm run dev      # Local development
npm run deploy   # Deploy to Cloudflare
```
