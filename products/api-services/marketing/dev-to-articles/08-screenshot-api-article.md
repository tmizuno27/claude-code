---
title: "Free Website Screenshot API — Capture Any URL as PNG with One HTTP Request"
published: false
tags: api, webdev, automation, javascript
---

Taking website screenshots programmatically is surprisingly annoying. You need Puppeteer (or Playwright), a headless browser, enough RAM to run Chrome, and a way to deploy it all. For a single screenshot.

I built a **Screenshot API** on Cloudflare Workers that does one thing: you send a URL, you get back a PNG. No browser to manage, no dependencies, no cold starts.

## Quick Start

```bash
curl "https://screenshot-api.p.rapidapi.com/capture?url=https://github.com&width=1280&height=800" --output screenshot.png
```

That's it. One request, one PNG.

## JavaScript — Dynamic OG Images

A common use case: generate social preview images for pages that don't have them.

```javascript
async function getScreenshot(url, width = 1280, height = 800) {
  const params = new URLSearchParams({ url, width, height });
  const response = await fetch(
    `https://screenshot-api.p.rapidapi.com/capture?${params}`
  );

  if (!response.ok) {
    throw new Error(`Screenshot failed: ${response.status}`);
  }

  return await response.blob();
}

// Use as a fallback OG image
async function getOgImage(pageUrl) {
  // First try to get the page's own OG image
  const meta = await fetch(`https://link-preview-api.p.rapidapi.com/preview?url=${pageUrl}`);
  const data = await meta.json();

  if (data.image) return data.image;

  // Fallback: take a screenshot
  const blob = await getScreenshot(pageUrl);
  return URL.createObjectURL(blob);
}
```

## Python — Batch Screenshots for Monitoring

```python
import requests
from pathlib import Path

def capture_screenshot(url: str, filename: str, width: int = 1280, height: int = 800):
    response = requests.get(
        "https://screenshot-api.p.rapidapi.com/capture",
        params={"url": url, "width": width, "height": height},
        timeout=30
    )
    response.raise_for_status()

    Path(filename).write_bytes(response.content)
    print(f"Saved: {filename} ({len(response.content)} bytes)")

# Monitor competitor landing pages
sites = [
    ("https://stripe.com", "stripe.png"),
    ("https://vercel.com", "vercel.png"),
    ("https://supabase.com", "supabase.png"),
]

for url, name in sites:
    capture_screenshot(url, name)
```

## Use Cases

### Visual regression testing
Capture screenshots before and after deploys, diff them programmatically.

### Link previews in chat apps
Show a thumbnail of URLs shared in your app — no browser needed on the server.

### Portfolio / showcase tools
Let users paste a URL and instantly see a preview card.

### SEO auditing
Capture screenshots alongside SEO analysis to show clients both the data and the visual state of their site.

### Archival
Take periodic snapshots of pages for compliance or record-keeping.

## Parameters

| Parameter | Default | Description |
|-----------|---------|-------------|
| `url` | (required) | URL to capture |
| `width` | 1280 | Viewport width in pixels |
| `height` | 800 | Viewport height in pixels |
| `format` | png | Output format |

## Why Not Run Puppeteer?

| | Screenshot API | Self-hosted Puppeteer |
|---|---|---|
| Setup | One HTTP call | Install Chrome + Puppeteer + deploy |
| Memory | 0 MB (API handles it) | 200–500 MB per instance |
| Cold start | None (Cloudflare Workers) | 2–5 seconds (container spin-up) |
| Scaling | Automatic | Manual (more containers) |
| Cost | Free (500/mo) | $5–20/mo minimum for hosting |

For occasional screenshots, an API is dramatically simpler than managing browser infrastructure.

[**Try it free on RapidAPI →**](https://rapidapi.com/miccho27-5OJaGGbBiO/api/screenshot-api)

---

*Part of a [collection of 24 free developer APIs](https://rapidapi.com/user/miccho27-5OJaGGbBiO) on Cloudflare Workers' edge network.*
