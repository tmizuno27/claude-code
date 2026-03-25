---
title: "Free Screenshot API — Capture Any Webpage as PNG with One HTTP Request"
published: true
tags: api, webdev, javascript, screenshot
cover_image:
---

Need website thumbnails for your link aggregator? Social media preview images? Visual regression testing? Automated report generation?

Most screenshot APIs charge per capture — Screenshotlayer at $10/mo for 100 captures, URLBox at $19/mo. For side projects and MVPs, that's overkill.

I built a **free Screenshot API** on Cloudflare Workers that captures any URL as a PNG image with a single GET request.

---

## Quick Start

```bash
curl "https://screenshot-api.t-mizuno27.workers.dev/capture?url=https://github.com&width=1280&height=720&format=png" -o screenshot.png
```

Parameters:

| Param | Default | Description |
|-------|---------|-------------|
| `url` | (required) | Target URL to capture |
| `width` | 1280 | Viewport width in pixels |
| `height` | 720 | Viewport height in pixels |
| `format` | png | Output format (png, jpeg, webp) |
| `full_page` | false | Capture entire scrollable page |
| `delay` | 0 | Wait N ms after page load before capture |

## Use Cases

### 1. Link Preview Generator (Node.js)

```javascript
const fetch = require("node-fetch");
const fs = require("fs");

async function generatePreview(url, outputPath) {
  const apiUrl = new URL(
    "https://screenshot-api.t-mizuno27.workers.dev/capture"
  );
  apiUrl.searchParams.set("url", url);
  apiUrl.searchParams.set("width", "1200");
  apiUrl.searchParams.set("height", "630"); // OG image ratio

  const res = await fetch(apiUrl);
  const buffer = await res.buffer();
  fs.writeFileSync(outputPath, buffer);
  console.log(`Preview saved: ${outputPath}`);
}

generatePreview("https://example.com", "preview.png");
```

### 2. Visual Regression Testing (Python)

```python
import requests
from PIL import Image
from io import BytesIO

def capture_page(url, viewport_width=1280):
    r = requests.get(
        "https://screenshot-api.t-mizuno27.workers.dev/capture",
        params={"url": url, "width": viewport_width, "full_page": "true"}
    )
    return Image.open(BytesIO(r.content))

# Compare staging vs production
staging = capture_page("https://staging.myapp.com")
production = capture_page("https://myapp.com")

# Simple pixel diff
import numpy as np
diff = np.array(staging) - np.array(production)
changed_pixels = np.count_nonzero(diff)
print(f"Changed pixels: {changed_pixels}")
```

### 3. Automated Report with Screenshots

```python
import requests

pages = [
    "https://analytics.google.com/analytics/web/",
    "https://search.google.com/search-console",
    "https://dashboard.stripe.com",
]

for i, url in enumerate(pages):
    r = requests.get(
        "https://screenshot-api.t-mizuno27.workers.dev/capture",
        params={"url": url, "width": 1920, "height": 1080}
    )
    with open(f"report-{i}.png", "wb") as f:
        f.write(r.content)
```

## Comparison with Alternatives

| Feature | This API | Screenshotlayer | URLBox | Puppeteer (self-hosted) |
|---------|----------|-----------------|--------|------------------------|
| Free tier | 500/mo | 100/mo | None | Unlimited (your server) |
| Setup time | 0 min | 5 min | 5 min | 30+ min |
| Full page capture | Yes | Pro only | Yes | Yes |
| Custom viewport | Yes | Pro only | Yes | Yes |
| Server cost | $0 | $10/mo+ | $19/mo+ | $5-20/mo |
| Global edge | 300+ PoPs | Single region | Single region | Single region |

## Available on RapidAPI

👉 [Screenshot API on RapidAPI](https://rapidapi.com/miccho27/api/screenshot-api)

**Free plan**: 500 requests/month, zero setup, no credit card.

---

## More Free APIs

This is one of **24 developer APIs** I maintain on Cloudflare Workers — all free tier, all edge-deployed:

- [20+ Free APIs Every Developer Needs in 2026](https://dev.to/miccho27/20-free-apis-every-developer-needs-in-2026-no-auth-required-18hj)
- [Free WHOIS & DNS Lookup API](https://dev.to/miccho27/free-whois-dns-lookup-api-build-domain-tools-without-scraping-3k1j)
- [Trending Topics Dashboard API](https://dev.to/miccho27/how-to-build-a-trending-topics-dashboard-with-one-api-call-google-reddit-hn-github-product-hunt-2fhm)

Questions or feature requests? Comment below!
