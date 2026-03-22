# Build Automated SEO Audits with a Free API -- No Ahrefs Subscription Needed

> Published on: Dev.to
> Tags: seo, api, webdev, javascript
> Canonical URL: (set after publishing)

---

Want to add SEO auditing to your app, CI/CD pipeline, or Chrome extension? Ahrefs charges $99+/month and Moz API requires a similar subscription. Here's a free alternative that returns a weighted SEO score (0-100) with 19 on-page checks.

## What It Analyzes (19 Checks)

- Title tag (length, presence, optimal range 30-60 chars)
- Meta description (length, optimal range 120-160 chars)
- Heading structure (H1-H6 counts)
- Image alt text coverage
- Internal and external links
- Canonical URL
- Robots meta directives
- Open Graph tags
- Twitter Card tags
- JSON-LD structured data
- Word count, page size, language, viewport, favicon, hreflang

All checks are weighted and combined into a 0-100 SEO score.

## Quick Start

```bash
curl "https://seo-analyzer-api.p.rapidapi.com/analyze?url=https://dev.to" \
  -H "X-RapidAPI-Key: YOUR_KEY" \
  -H "X-RapidAPI-Host: seo-analyzer-api.p.rapidapi.com"
```

## Use Case 1: SEO Check in CI/CD

Add an SEO quality gate to your deployment pipeline. Fail the build if the score drops below 70.

```javascript
// ci-seo-check.js
const axios = require("axios");

const PAGES = ["/", "/about", "/pricing", "/blog"];
const MIN_SCORE = 70;
const BASE_URL = "https://your-staging-site.com";

async function checkSEO() {
  let failed = false;

  for (const page of PAGES) {
    const { data } = await axios.get(
      "https://seo-analyzer-api.p.rapidapi.com/score",
      {
        params: { url: `${BASE_URL}${page}` },
        headers: {
          "X-RapidAPI-Key": process.env.RAPIDAPI_KEY,
          "X-RapidAPI-Host": "seo-analyzer-api.p.rapidapi.com",
        },
      }
    );

    const status = data.seo_score >= MIN_SCORE ? "PASS" : "FAIL";
    console.log(`${status}: ${page} -> Score: ${data.seo_score}/100`);

    if (data.seo_score < MIN_SCORE) failed = true;
  }

  if (failed) {
    console.error("SEO check failed. Fix issues before deploying.");
    process.exit(1);
  }
}

checkSEO();
```

## Use Case 2: Competitor Comparison (Python)

```python
import requests

urls = [
    "https://your-site.com/blog/post-1",
    "https://competitor-a.com/similar-post",
    "https://competitor-b.com/similar-post",
]

headers = {
    "X-RapidAPI-Key": "YOUR_KEY",
    "X-RapidAPI-Host": "seo-analyzer-api.p.rapidapi.com"
}

for url in urls:
    resp = requests.get(
        "https://seo-analyzer-api.p.rapidapi.com/analyze",
        params={"url": url},
        headers=headers
    ).json()

    print(f"\n{url}")
    print(f"  Score: {resp['seo_score']}/100")
    print(f"  Title: {resp['title']['text']} ({resp['title']['length']} chars)")
    print(f"  Meta: {'Yes' if resp['meta_description']['text'] else 'Missing'}")
    print(f"  H1: {resp['headings']['h1']} | Images: {resp['images']['total']} (alt: {resp['images']['with_alt']})")
```

## Endpoints

| Endpoint | What it returns |
|----------|----------------|
| `GET /analyze?url=...` | Full 19-check audit with score |
| `GET /score?url=...` | Score only (lighter response) |
| `GET /headings?url=...` | Heading structure only |
| `GET /links?url=...` | Link analysis only |

## Free Tier: 500 requests/month

Enough to audit 500 pages per month -- that's 16 pages/day. For most blogs and small sites, that's more than enough for continuous monitoring.

**[Try it on RapidAPI (free)](https://rapidapi.com/miccho27-5OJaGGbBiO/api/seo-analyzer-api)** -- no credit card required.

---

*Questions or feature requests? Drop a comment below.*
