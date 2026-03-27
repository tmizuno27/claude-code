---
title: "Building a SEO Analyzer with Cloudflare Workers"
published: false
description: "A deep dive into building a full on-page SEO analysis API that runs on the edge — parsing HTML, scoring pages, and returning actionable insights in under 200ms."
tags: seo, cloudflare, javascript, webdev
cover_image:
---

Most SEO tools are SaaS products with monthly subscriptions. But what if you just need a programmable API that tells you "this page is missing alt text on 3 images and the title is too long"?

I built an SEO Analyzer API that runs entirely on Cloudflare Workers. No server, no database, no dependencies beyond what Workers provides natively. In this article, I'll walk through the architecture, the HTML parsing strategy, the scoring algorithm, and how you can use it in your own projects.

---

## Architecture Overview

```
Client Request
    ↓
Cloudflare Worker (edge, 300+ locations)
    ├── Rate limiter (in-memory Map)
    ├── URL validation
    ├── fetch() target page
    ├── HTML parser (regex-based, no DOM)
    ├── SEO scoring engine
    └── JSON response
```

The entire API is a single Cloudflare Worker with two files:
- `index.js` — Request routing, rate limiting, orchestration
- `parser.js` — All HTML extraction and scoring logic

No npm packages. No build step beyond what `wrangler` does. The Worker runs in V8 isolates, so there's no DOM API available — all HTML parsing uses regex patterns.

## The Challenge: Parsing HTML Without a DOM

In Node.js you'd reach for `cheerio` or `jsdom`. In a Worker, you don't have that luxury (and even if you bundled them, the 1MB size limit and CPU time limits would bite you).

Instead, every extraction function uses targeted regex patterns. Here's the approach:

### Extracting the Title Tag

```javascript
function extractTitle(html) {
  const match = html.match(/<title[^>]*>([\s\S]*?)<\/title>/i);
  const text = match ? match[1].trim() : null;

  const issues = [];
  if (!text) {
    issues.push("Missing title tag");
  } else {
    if (text.length < 30) issues.push("Title is too short (under 30 chars)");
    if (text.length > 60) issues.push("Title is too long (over 60 chars)");
  }

  return { text, length: text?.length || 0, issues };
}
```

Simple, but there's a subtlety: we use `[\s\S]*?` instead of `.*?` because title tags can contain newlines. This pattern is non-greedy to handle edge cases where someone (incorrectly) has multiple title tags.

### Extracting Meta Description

```javascript
function extractMetaDescription(html) {
  const match = html.match(
    /<meta[^>]+name=["']description["'][^>]+content=["']([\s\S]*?)["'][^>]*>/i
  ) || html.match(
    /<meta[^>]+content=["']([\s\S]*?)["'][^>]+name=["']description["'][^>]*>/i
  );

  const text = match ? match[1].trim() : null;
  const issues = [];

  if (!text) {
    issues.push("Missing meta description");
  } else {
    if (text.length < 120) issues.push("Meta description is too short (under 120 chars)");
    if (text.length > 160) issues.push("Meta description is too long (over 160 chars)");
  }

  return { text, length: text?.length || 0, issues };
}
```

Notice the two regex patterns — `name` and `content` attributes can appear in either order in HTML. This is the kind of real-world messiness you hit when parsing arbitrary web pages.

### Heading Hierarchy Validation

Good SEO requires a logical heading structure: one H1, H2s under it, H3s under H2s, etc. Here's how we check:

```javascript
function extractHeadings(html) {
  const headings = { h1: 0, h2: 0, h3: 0, h4: 0, h5: 0, h6: 0, items: [] };
  const regex = /<h([1-6])[^>]*>([\s\S]*?)<\/h\1>/gi;

  let match;
  while ((match = regex.exec(html)) !== null) {
    const level = parseInt(match[1]);
    const text = match[2].replace(/<[^>]+>/g, "").trim();
    headings[`h${level}`]++;
    headings.items.push({ level, text });
  }

  // Validate hierarchy
  headings.hierarchy_valid = true;
  let prevLevel = 0;
  for (const item of headings.items) {
    if (item.level > prevLevel + 1 && prevLevel > 0) {
      headings.hierarchy_valid = false; // Skipped a level (e.g., H1 → H3)
      break;
    }
    prevLevel = item.level;
  }

  return headings;
}
```

The hierarchy check catches a common SEO mistake: jumping from H1 directly to H3, skipping H2 entirely. Search engines use heading structure to understand content hierarchy.

### Image Analysis

```javascript
function extractImages(html) {
  const imgRegex = /<img[^>]+>/gi;
  const images = [];
  let missing_alt = 0;
  let match;

  while ((match = imgRegex.exec(html)) !== null) {
    const tag = match[0];
    const src = tag.match(/src=["']([^"']+)["']/i)?.[1] || null;
    const alt = tag.match(/alt=["']([^"']*?)["']/i);
    const hasAlt = alt !== null && alt[1].trim().length > 0;

    if (!hasAlt) missing_alt++;
    images.push({ src, has_alt: hasAlt });
  }

  return { total: images.length, missing_alt, images: images.slice(0, 20) };
}
```

We cap the returned images at 20 to keep response sizes reasonable. The `missing_alt` count covers all images, though.

## The Scoring Algorithm

The SEO score is a weighted sum across 8 categories, each worth up to a maximum number of points:

```javascript
function calculateSeoScore(data) {
  const breakdown = {};
  let total = 0;

  // Title (max 15 points)
  breakdown.title = 0;
  if (data.title.text) {
    breakdown.title += 5;
    if (data.title.length >= 30 && data.title.length <= 60) breakdown.title += 10;
    else if (data.title.length >= 20) breakdown.title += 5;
  }

  // Meta description (max 10 points)
  breakdown.description = 0;
  if (data.metaDescription.text) {
    breakdown.description += 4;
    if (data.metaDescription.length >= 120 && data.metaDescription.length <= 160)
      breakdown.description += 6;
    else if (data.metaDescription.length >= 50)
      breakdown.description += 3;
  }

  // Headings (max 15 points)
  breakdown.headings = 0;
  if (data.headings.h1 === 1) breakdown.headings += 5;
  if (data.headings.h2 > 0) breakdown.headings += 5;
  if (data.headings.hierarchy_valid) breakdown.headings += 5;

  // Images (max 10 points)
  breakdown.images = data.images.total > 0
    ? Math.round((1 - data.images.missing_alt / data.images.total) * 10)
    : 10; // No images = no penalty

  // Links (max 10 points)
  breakdown.links = 0;
  if (data.links.internal > 0) breakdown.links += 5;
  if (data.links.external > 0) breakdown.links += 5;

  // Mobile friendliness (max 10 points)
  breakdown.mobile = data.viewport ? 10 : 0;

  // Structured data (max 15 points)
  breakdown.structured_data = 0;
  if (data.openGraph && Object.keys(data.openGraph).length > 0) breakdown.structured_data += 5;
  if (data.twitterCard && Object.keys(data.twitterCard).length > 0) breakdown.structured_data += 5;
  if (data.jsonLd && data.jsonLd.length > 0) breakdown.structured_data += 5;

  // Performance proxy (max 15 points)
  breakdown.performance = 15;
  if (data.pageSize > 500000) breakdown.performance -= 5;  // Over 500KB
  if (data.pageSize > 1000000) breakdown.performance -= 5; // Over 1MB
  if (data.wordCount < 300) breakdown.performance -= 5;    // Thin content

  for (const val of Object.values(breakdown)) total += val;
  const score = Math.min(100, total);

  return { score, breakdown };
}
```

The weights reflect what actually matters for SEO in 2026:
- **Title + headings (30 points):** Still the strongest on-page signals
- **Structured data (15 points):** Increasingly important for rich results
- **Performance (15 points):** Core Web Vitals correlation
- **Meta description (10 points):** Affects CTR, not ranking directly
- **Images, links, mobile (30 points):** Foundational hygiene

## Rate Limiting on the Edge

Workers don't have persistent memory across requests (isolates can be recycled), but within a single isolate's lifetime, we use an in-memory `Map`:

```javascript
const rateMap = new Map();
const RATE_LIMIT = 20;        // requests per window
const RATE_WINDOW = 60_000;   // 1 minute
const MAX_MAP_SIZE = 5000;    // prevent unbounded growth

function checkRateLimit(ip) {
  const now = Date.now();

  // Size-based cleanup — no timers in Workers
  if (rateMap.size > MAX_MAP_SIZE) {
    for (const [key, entry] of rateMap) {
      if (now - entry.start > RATE_WINDOW) rateMap.delete(key);
      if (rateMap.size <= MAX_MAP_SIZE / 2) break;
    }
  }

  const entry = rateMap.get(ip);
  if (!entry || now - entry.start > RATE_WINDOW) {
    rateMap.set(ip, { start: now, count: 1 });
    return { allowed: true, remaining: RATE_LIMIT - 1 };
  }

  entry.count++;
  if (entry.count > RATE_LIMIT) {
    return {
      allowed: false,
      remaining: 0,
      retryAfter: Math.ceil((entry.start + RATE_WINDOW - now) / 1000),
    };
  }

  return { allowed: true, remaining: RATE_LIMIT - entry.count };
}
```

Key design decisions:
- **Size-based cleanup, not timer-based.** `setInterval` doesn't behave predictably in Workers.
- **MAX_MAP_SIZE prevents OOM.** Under heavy traffic, the map could grow indefinitely.
- **Cleanup halves the map,** not empties it — amortized cost stays low.

This is a "best-effort" rate limiter. If the isolate recycles, the map resets. For production rate limiting on RapidAPI, their infrastructure handles the hard limits — this is a courtesy layer.

## Putting It All Together: 4 Endpoints

The router is intentionally minimal:

```javascript
export default {
  async fetch(request) {
    // CORS, method checks, rate limiting...

    const { pathname, searchParams } = new URL(request.url);
    const url = searchParams.get("url");

    const { html, size, finalUrl } = await fetchPage(url);

    switch (pathname) {
      case "/analyze":  return json(fullAnalysis(html, finalUrl, size));
      case "/headings": return json({ url: finalUrl, headings: extractHeadings(html) });
      case "/links":    return json({ url: finalUrl, links: extractLinks(html, finalUrl) });
      case "/score":    return json({ url: finalUrl, seoScore: calculateSeoScore(...) });
      default:          return error("Not found", 404);
    }
  },
};
```

Four endpoints, each serving a different use case:
- `/analyze` — Full audit (content teams, SEO dashboards)
- `/headings` — Structure check (content writers, accessibility tools)
- `/links` — Link analysis (internal linking tools, broken link checkers)
- `/score` — Quick pass/fail (CI/CD gates, monitoring)

## Real-World Integration Examples

### CI/CD SEO Gate (GitHub Actions)

```yaml
name: SEO Quality Gate
on:
  push:
    branches: [main]
    paths: ["content/**", "pages/**"]

jobs:
  seo-check:
    runs-on: ubuntu-latest
    steps:
      - name: Wait for deploy
        run: sleep 60

      - name: Check critical pages
        run: |
          PAGES=("https://yoursite.com" "https://yoursite.com/blog" "https://yoursite.com/pricing")
          FAILED=0
          for PAGE in "${PAGES[@]}"; do
            RESULT=$(curl -s "https://seo-analyzer-api.miccho27.workers.dev/score?url=$PAGE")
            SCORE=$(echo $RESULT | jq '.seoScore.score')
            echo "$PAGE: $SCORE/100"
            if [ "$SCORE" -lt 60 ]; then
              echo "::warning::$PAGE scored $SCORE (below 60)"
              FAILED=1
            fi
          done
          if [ "$FAILED" -eq 1 ]; then
            echo "::error::One or more pages failed the SEO quality gate"
            exit 1
          fi
```

### Daily SEO Monitoring (Python)

```python
import requests
import json
from datetime import datetime

API = "https://seo-analyzer-api.miccho27.workers.dev"

PAGES = [
    "https://yoursite.com",
    "https://yoursite.com/blog",
    "https://yoursite.com/pricing",
    "https://yoursite.com/docs",
]

def daily_audit():
    report = {"date": datetime.now().isoformat(), "pages": []}

    for url in PAGES:
        data = requests.get(f"{API}/analyze", params={"url": url}).json()
        report["pages"].append({
            "url": url,
            "score": data["seoScore"]["score"],
            "title_length": data["title"]["length"],
            "meta_length": data["metaDescription"]["length"],
            "missing_alt": data["images"]["missing_alt"],
            "internal_links": data["links"]["internal"],
            "issues": data["title"]["issues"] + data["metaDescription"].get("issues", []),
        })

    # Save or send report
    with open(f"seo-report-{datetime.now().strftime('%Y-%m-%d')}.json", "w") as f:
        json.dump(report, f, indent=2)

    # Alert on regressions
    for page in report["pages"]:
        if page["score"] < 60:
            print(f"ALERT: {page['url']} scored {page['score']}")

if __name__ == "__main__":
    daily_audit()
```

### Next.js ISR with SEO Metadata

```javascript
// pages/tools/seo-checker.js
export async function getStaticProps() {
  return { props: {}, revalidate: 3600 };
}

// Client-side component
function SEOChecker() {
  const [url, setUrl] = useState("");
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);

  const analyze = async () => {
    setLoading(true);
    const res = await fetch(
      `https://seo-analyzer-api.miccho27.workers.dev/analyze?url=${encodeURIComponent(url)}`
    );
    setResult(await res.json());
    setLoading(false);
  };

  return (
    <div>
      <input value={url} onChange={e => setUrl(e.target.value)} placeholder="https://..." />
      <button onClick={analyze} disabled={loading}>
        {loading ? "Analyzing..." : "Analyze"}
      </button>
      {result && (
        <div>
          <h2>Score: {result.seoScore.score}/100</h2>
          <pre>{JSON.stringify(result.seoScore.breakdown, null, 2)}</pre>
        </div>
      )}
    </div>
  );
}
```

## Deployment

The entire thing deploys with one command:

```bash
npx wrangler deploy
```

The `wrangler.toml` is minimal:

```toml
name = "seo-analyzer-api"
main = "src/index.js"
compatibility_date = "2024-01-01"
```

No KV, no D1, no Durable Objects. Just compute.

## Performance Numbers

From real-world testing:
- **API response time:** 100-300ms (dominated by fetching the target page)
- **Worker CPU time:** 5-15ms (parsing + scoring)
- **Memory:** Well within Worker limits even for 1MB+ pages
- **Cold start:** 0ms (Workers don't have cold starts)

The bottleneck is always `fetch()` to the target URL. The actual analysis is near-instant.

## Try It

The API is live and free to use (500 requests/month):

```bash
# Full analysis
curl "https://seo-analyzer-api.miccho27.workers.dev/analyze?url=https://dev.to"

# Just the score
curl "https://seo-analyzer-api.miccho27.workers.dev/score?url=https://example.com"
```

For higher limits, it's available on RapidAPI with Pro ($5.99/mo), Ultra ($14.99/mo), and Mega ($49.99/mo) tiers.

[SEO Analyzer API on RapidAPI](https://rapidapi.com/miccho27-5OJaGGbBiO/api/seo-analyzer-api)

---

*Have questions about the implementation? Drop a comment — I'm happy to go deeper on any part of the architecture.*
