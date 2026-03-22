# Free URL Shortener API - Short Links with Click Analytics

> **Free tier: 500 requests/month** | Create short URLs with built-in click tracking via Cloudflare KV

Create short URLs, track clicks with analytics (referrer, device, location), and manage your links. Powered by Cloudflare Workers + KV storage for instant redirects worldwide.

## Why Choose This URL Shortener API?

- **Click analytics** -- track clicks, referrers, devices, and geographic data
- **Cloudflare KV storage** -- sub-10ms redirect latency globally
- **Custom aliases** -- create branded short links (e.g., /my-campaign)
- **Expiration support** -- auto-expire links after a set date
- **Free tier** -- 500 requests/month at $0

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

## Pricing

| Plan | Price | Requests/mo | Rate Limit |
|------|-------|-------------|------------|
| Basic (FREE) | $0 | 500 | 1 req/sec |
| Pro | $5.99 | 50,000 | 10 req/sec |

## Alternative To

A free alternative to Bitly API, TinyURL API, and Rebrandly. Get click analytics without per-link pricing.

## Keywords

`url shortener api`, `link shortener`, `short url api`, `click tracking api`, `link analytics`, `bitly alternative`, `free url shortener`, `custom short links`, `link management api`, `url redirect api`
