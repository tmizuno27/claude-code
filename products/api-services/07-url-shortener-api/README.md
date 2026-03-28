# Free URL Shortener API - Short Links with Click Analytics

> **Free tier: 500 requests/month** | Create short URLs with built-in click tracking via Cloudflare KV

Create short URLs, track clicks with analytics (referrer, device, location), and manage your links. Powered by Cloudflare Workers + KV storage for instant redirects worldwide.

## Getting Started in 30 Seconds

1. Subscribe on [RapidAPI](https://rapidapi.com/miccho27-5OJaGGbBiO/api/url-shortener-api) (free plan available)
2. Copy your API key
3. Shorten your first URL:

```bash
curl -X POST "https://url-shortener-api.p.rapidapi.com/shorten" \
  -H "Content-Type: application/json" \
  -H "X-RapidAPI-Key: YOUR_KEY" \
  -H "X-RapidAPI-Host: url-shortener-api.p.rapidapi.com" \
  -d '{"url": "https://example.com/very/long/path"}'
```

## How It Compares

| Feature | This API | Bitly | TinyURL | Rebrandly |
|---------|----------|-------|---------|-----------|
| Free tier | 500 req/mo | 10 links/mo | Unlimited (no analytics) | 25 links/mo |
| Pro pricing | $5.99/50K req | $29/mo | $12.99/mo | $13/mo |
| Click analytics | Yes (referrer, device, geo) | Yes | No (free) | Yes |
| Custom aliases | Yes | Yes (paid) | No | Yes |
| Link expiration | Yes | No (free) | No | No |
| API-first | Yes | Yes | Limited | Yes |
| Edge latency | Sub-10ms (CF KV) | Variable | Variable | Variable |

## Why Choose This URL Shortener API?

- **Click analytics** -- track clicks, referrers, devices, and geographic data
- **Cloudflare KV storage** -- sub-10ms redirect latency globally
- **Custom aliases** -- create branded short links (e.g., /my-campaign)
- **Expiration support** -- auto-expire links after a set date
- **Free tier** -- 500 requests/month at $0

## Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/shorten` | POST | Create a short URL |
| `/r/{alias}` | GET | Redirect to original URL |
| `/stats/{alias}` | GET | Get click analytics |
| `/delete/{alias}` | DELETE | Delete a short URL |

## Use Cases

- **Marketing campaigns** -- track click-through rates on social media links
- **Email marketing** -- shorten and track links in newsletters
- **SaaS apps** -- generate shareable short links for user content
- **Affiliate marketing** -- create trackable short links for affiliate URLs
- **QR codes** -- pair with QR Code API for scannable short links

## Quick Start

```bash
curl -X POST "https://url-shortener-api.t-mizuno27.workers.dev/shorten" \
  -H "Content-Type: application/json" \
  -H "X-RapidAPI-Key: YOUR_KEY" \
  -d '{"url": "https://example.com/very/long/path", "alias": "my-link"}'
```

### Python Example

```python
import requests

url = "https://url-shortener-api.p.rapidapi.com/shorten"
headers = {"X-RapidAPI-Key": "YOUR_KEY", "X-RapidAPI-Host": "url-shortener-api.p.rapidapi.com"}
payload = {"url": "https://example.com/long-path"}

data = requests.post(url, headers=headers, json=payload).json()
print(f"Short URL: {data['short_url']}")
```

### Node.js Example

```javascript
const axios = require("axios");

const { data } = await axios.post(
  "https://url-shortener-api.p.rapidapi.com/shorten",
  { url: "https://example.com/very/long/path", alias: "my-link" },
  {
    headers: {
      "X-RapidAPI-Key": "YOUR_KEY",
      "X-RapidAPI-Host": "url-shortener-api.p.rapidapi.com",
    },
  }
);

console.log(`Short URL: ${data.short_url}`);
```

## FAQ

**Q: How long do short URLs last?**
A: Indefinitely by default. You can optionally set an expiration date when creating a link.

**Q: Can I use custom aliases?**
A: Yes. Pass an `alias` field when creating a link. If omitted, a random 6-character alias is generated.

**Q: What analytics data is tracked?**
A: Each click records timestamp, referrer URL, user agent (device/browser), and approximate geographic location.

**Q: Is there a limit on redirect speed?**
A: Redirects are served from Cloudflare KV edge storage with sub-10ms latency worldwide.

## Pricing

| Plan | Price | Requests/mo | Rate Limit |
|------|-------|-------------|------------|
| Basic (FREE) | $0 | 500 | 1 req/sec |
| Pro | $5.99 | 50,000 | 10 req/sec |

## Alternative To

A free alternative to Bitly API, TinyURL API, and Rebrandly. Get click analytics without per-link pricing.


## Also From This Publisher

Build powerful workflows by combining APIs:

| API | Why Combine? |
|-----|-------------|
| **QR Code API** | Generate QR codes for shortened URLs |
| **Link Preview API** | Extract metadata before shortening |
| **IP Geolocation API** | Geo-locate users who click short links |
| **Screenshot API** | Capture thumbnails for link previews |

> All APIs include a free tier. Subscribe to one, discover the full toolkit on [our RapidAPI profile](https://rapidapi.com/miccho27-5OJaGGbBiO).

## Keywords

`url shortener api`, `link shortener`, `short url api`, `click tracking api`, `link analytics`, `bitly alternative`, `free url shortener`, `custom short links`, `link management api`, `url redirect api`
