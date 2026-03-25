---
title: "Build Automated SEO Audits with a Free API — No Ahrefs Subscription Needed"
published: false
description: "A free SEO Analyzer API with 19 on-page checks and a weighted 0-100 score. Add SEO quality gates to CI/CD pipelines or build custom audit tools. Python & JS examples."
tags: seo, api, webdev, javascript
---

Want to add SEO auditing to your app, CI/CD pipeline, or internal tool? Ahrefs charges $99+/month. Moz API requires a similar subscription. Screaming Frog is desktop-only.

I built a **free SEO Analyzer API** that returns a weighted SEO score (0-100) with 19 on-page checks — and it runs on Cloudflare Workers, so it's fast from anywhere.

## What It Checks (19 Factors)

The API audits a URL and returns structured data on:

- **Title tag** — length, presence, optimal range (30-60 chars)
- **Meta description** — length, optimal range (120-160 chars)
- **Heading structure** — H1 through H6 counts
- **Image alt text** — total images vs. images with alt attributes
- **Links** — internal and external link counts
- **Canonical URL** — present or missing
- **Robots meta** — index/noindex directives
- **Open Graph tags** — og:title, og:description, og:image
- **Twitter Card tags** — card type, title, description
- **JSON-LD structured data** — detected schemas
- **Word count, page size, language, viewport, favicon, hreflang**

All checks are weighted and combined into a single **0-100 SEO score**.

## Quick Start

```bash
curl "https://seo-analyzer-api.p.rapidapi.com/analyze?url=https://dev.to" \
  -H "X-RapidAPI-Key: YOUR_KEY" \
  -H "X-RapidAPI-Host: seo-analyzer-api.p.rapidapi.com"
```

## JavaScript — SEO Quality Gate in CI/CD

Block deployments when SEO score drops below your threshold. Add this to your GitHub Actions or CI pipeline:

```javascript
// ci-seo-check.js
const PAGES = ["/", "/about", "/pricing", "/blog"];
const MIN_SCORE = 70;
const BASE_URL = process.env.STAGING_URL || "https://staging.yoursite.com";
const API_KEY = process.env.RAPIDAPI_KEY;

async function checkSEO() {
  let allPassed = true;

  for (const page of PAGES) {
    const url = `https://seo-analyzer-api.p.rapidapi.com/score?url=${encodeURIComponent(BASE_URL + page)}`;
    const res = await fetch(url, {
      headers: {
        "X-RapidAPI-Key": API_KEY,
        "X-RapidAPI-Host": "seo-analyzer-api.p.rapidapi.com",
      },
    });
    const data = await res.json();

    const status = data.seo_score >= MIN_SCORE ? "PASS" : "FAIL";
    console.log(`${status}: ${page} -> Score: ${data.seo_score}/100`);

    if (data.seo_score < MIN_SCORE) allPassed = false;
  }

  if (!allPassed) {
    console.error("SEO check failed. Fix issues before deploying.");
    process.exit(1);
  }

  console.log("All pages passed SEO check.");
}

checkSEO();
```

**GitHub Actions integration:**

```yaml
- name: SEO Quality Gate
  run: node ci-seo-check.js
  env:
    STAGING_URL: ${{ env.STAGING_URL }}
    RAPIDAPI_KEY: ${{ secrets.RAPIDAPI_KEY }}
```

This catches SEO regressions — missing meta descriptions, broken OG tags, removed H1s — before they reach production.

## Python — Competitor Analysis

Compare your pages against competitors on the same keywords:

```python
import requests

urls = [
    "https://your-site.com/blog/react-performance",
    "https://competitor-a.com/react-performance-guide",
    "https://competitor-b.com/optimize-react-apps",
]

headers = {
    "X-RapidAPI-Key": "YOUR_KEY",
    "X-RapidAPI-Host": "seo-analyzer-api.p.rapidapi.com",
}

results = []
for target_url in urls:
    resp = requests.get(
        "https://seo-analyzer-api.p.rapidapi.com/analyze",
        params={"url": target_url},
        headers=headers,
    ).json()

    results.append({
        "url": target_url,
        "score": resp["seo_score"],
        "title_len": resp["title"]["length"],
        "meta": "Yes" if resp["meta_description"]["text"] else "Missing",
        "h1_count": resp["headings"]["h1"],
        "images": resp["images"]["total"],
        "alt_coverage": (
            f"{resp['images']['with_alt']}/{resp['images']['total']}"
            if resp["images"]["total"] > 0
            else "N/A"
        ),
    })

# Print comparison table
print(f"{'URL':<50} {'Score':>5} {'Title':>6} {'Meta':>5} {'H1':>3} {'Images':>8}")
print("-" * 85)
for r in results:
    print(
        f"{r['url']:<50} {r['score']:>5} {r['title_len']:>6} "
        f"{r['meta']:>5} {r['h1_count']:>3} {r['alt_coverage']:>8}"
    )
```

This tells you exactly where your pages fall short compared to competitors — and what to fix first.

## Endpoints

| Endpoint | Returns |
|----------|---------|
| `GET /analyze?url=...` | Full 19-check audit with weighted score |
| `GET /score?url=...` | Score only (lighter, faster response) |
| `GET /headings?url=...` | Heading structure (H1-H6 breakdown) |
| `GET /links?url=...` | Internal and external link analysis |

## Use Cases

- **CI/CD quality gates** — Prevent SEO regressions in every deploy
- **Content team dashboards** — Show writers their SEO score before publishing
- **Agency tools** — Build white-label SEO audits for clients
- **Chrome extensions** — Show SEO score for any page in one click
- **Monitoring** — Weekly cron job to audit your top 50 pages, alert on score drops

## Free Tier: 500 Requests/Month

That's 16 pages per day — enough for continuous monitoring of a small-to-medium site. Paid plans start at $5.99/month for 50,000 requests.

**[Try it free on RapidAPI](https://rapidapi.com/miccho27-5OJaGGbBiO/api/seo-analyzer-api)** — no credit card required.

---

*Questions or feature requests? Drop a comment below.*

*Part of a [collection of 24 free developer APIs](https://rapidapi.com/user/miccho27-5OJaGGbBiO) on Cloudflare Workers.*
