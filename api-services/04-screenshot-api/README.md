# Free Website Screenshot API - Capture Any Page as PNG or JPEG

> **Free tier: 500 requests/month** | Full-page and viewport screenshots with custom dimensions

Capture screenshots of any website as PNG or JPEG. Supports custom viewport sizes, full-page capture, JPEG quality control, and render delay for JavaScript-heavy pages. Powered by Cloudflare Workers with 1-hour caching.

## Getting Started in 30 Seconds

1. Subscribe on [RapidAPI](https://rapidapi.com/miccho27-5OJaGGbBiO/api/screenshot-api) (free plan available)
2. Copy your API key
3. Capture your first screenshot:

```bash
curl -X GET "https://screenshot-api.p.rapidapi.com/screenshot?url=https://github.com" \
  -H "X-RapidAPI-Key: YOUR_KEY" \
  -H "X-RapidAPI-Host: screenshot-api.p.rapidapi.com" \
  -o screenshot.png
```

## How It Compares

| Feature | This API | ScreenshotAPI | URLBox | Screenshotlayer |
|---------|----------|-------------|--------|----------------|
| Free tier | 500 req/mo | 100/mo | None | 100/mo |
| Pro pricing | $9.99/50K | $19/1K | $19/mo | $10/2K |
| Full-page capture | Yes | Yes | Yes | Yes |
| Custom viewports | Yes (320-3840px) | Yes | Yes | Limited |
| PNG + JPEG | Yes | Yes | Yes | Yes |
| JPEG quality control | Yes (1-100) | Yes | Yes | No |
| Render delay | Yes (up to 5s) | Yes | Yes | No |
| 1-hour edge cache | Yes (CF Workers) | No | No | No |
| Per-screenshot pricing | No (flat plan) | Yes ($0.019/each) | Yes | Yes ($0.005/each) |

## Why Choose This Screenshot API?

- **Multiple output formats** -- PNG for crisp screenshots, JPEG with quality control (1-100)
- **Full-page capture** -- scroll the entire page and capture everything
- **Custom viewports** -- desktop (1920x1080), tablet (768x1024), mobile (375x812)
- **Render delay** -- wait up to 5 seconds for JavaScript content to load
- **1-hour caching** -- repeat requests served instantly from Cloudflare edge cache
- **Free tier** -- 500 screenshots/month at $0

## Use Cases

- **SEO monitoring** -- capture competitor pages for visual comparison over time
- **Social media previews** -- generate Open Graph images from web pages
- **Testing and QA** -- automated visual regression testing across viewports
- **Portfolio builders** -- auto-generate thumbnails for website showcases
- **PDF reports** -- embed website screenshots in automated reports
- **Link preview services** -- show visual previews of shared URLs
- **Archiving** -- capture web pages for compliance or record-keeping

## Quick Start

### Basic Screenshot (PNG)

```bash
curl -X GET "https://screenshot-api.t-mizuno27.workers.dev/screenshot?url=https://example.com" \
  -H "X-RapidAPI-Key: YOUR_KEY" \
  -o screenshot.png
```

### Full Page JPEG

```bash
curl -X GET "https://screenshot-api.t-mizuno27.workers.dev/screenshot?url=https://example.com&full_page=true&format=jpeg&quality=90" \
  -H "X-RapidAPI-Key: YOUR_KEY" \
  -o fullpage.jpg
```

### Mobile Viewport

```bash
curl -X GET "https://screenshot-api.t-mizuno27.workers.dev/screenshot?url=https://example.com&width=375&height=812" \
  -H "X-RapidAPI-Key: YOUR_KEY" \
  -o mobile.png
```

### Python Example

```python
import requests

url = "https://screenshot-api.p.rapidapi.com/screenshot"
params = {
    "url": "https://github.com",
    "width": 1280,
    "height": 720,
    "format": "png"
}
headers = {
    "X-RapidAPI-Key": "YOUR_KEY",
    "X-RapidAPI-Host": "screenshot-api.p.rapidapi.com"
}

response = requests.get(url, headers=headers, params=params)
with open("screenshot.png", "wb") as f:
    f.write(response.content)
```

### Node.js Example

```javascript
const axios = require("axios");
const fs = require("fs");

const response = await axios.get(
  "https://screenshot-api.p.rapidapi.com/screenshot",
  {
    params: { url: "https://github.com", width: 1280, format: "png" },
    headers: {
      "X-RapidAPI-Key": "YOUR_KEY",
      "X-RapidAPI-Host": "screenshot-api.p.rapidapi.com",
    },
    responseType: "arraybuffer",
  }
);
fs.writeFileSync("screenshot.png", response.data);
```

## API Reference

### `GET /screenshot`

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `url` | string | Yes | -- | Target URL to capture |
| `width` | integer | No | 1280 | Viewport width (320-3840) |
| `height` | integer | No | 720 | Viewport height (0 = full page) |
| `format` | string | No | `png` | Output: `png` or `jpeg` |
| `quality` | integer | No | 80 | JPEG quality (1-100) |
| `delay` | integer | No | 0 | Wait ms before capture (max 5000) |
| `full_page` | boolean | No | false | Capture full scrollable page |

Returns the screenshot image directly with appropriate `Content-Type` header.

## Pricing

| Plan | Price | Requests/mo | Rate Limit |
|------|-------|-------------|------------|
| Basic (FREE) | $0 | 500 | 1 req/sec |
| Pro | $9.99 | 50,000 | 10 req/sec |
| Ultra | $24.99 | 500,000 | 50 req/sec |

## Alternative To

A free alternative to ScreenshotAPI, URLBox, and Screenshotlayer. Capture website screenshots without complex setup or per-screenshot billing.

## Keywords

`screenshot api`, `website screenshot`, `capture webpage`, `web screenshot api`, `page capture`, `full page screenshot`, `url to image`, `website thumbnail`, `free screenshot api`, `headless browser api`

## Development

```bash
npm install
npx wrangler deploy
```
