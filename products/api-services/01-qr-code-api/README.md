# Free QR Code Generator API - PNG, SVG, Base64 | No Auth Required

> **Free tier: 500 requests/month** | PNG, SVG, Base64 with custom colors in sub-100ms

Generate production-ready QR codes in PNG, SVG, or Base64 format with custom colors, sizes, and error correction levels. No API key setup needed -- just subscribe on RapidAPI and start generating.

## Getting Started in 30 Seconds

1. Subscribe on [RapidAPI](https://rapidapi.com/miccho27-5OJaGGbBiO/api/qr-code-generator-api) (free plan available)
2. Copy your API key
3. Generate your first QR code:

```bash
curl "https://qr-code-generator-api.p.rapidapi.com/generate?text=https://example.com&size=400" \
  -H "X-RapidAPI-Key: YOUR_KEY" \
  -H "X-RapidAPI-Host: qr-code-generator-api.p.rapidapi.com" \
  -o qrcode.png
```

## How It Compares

| Feature | This API | goqr.me | QR Server | QRickit |
|---------|----------|---------|-----------|---------|
| Free tier | 500 req/mo | Unlimited (no SLA) | Unlimited (no SLA) | Limited |
| Output formats | PNG, SVG, Base64 | PNG, SVG, EPS | PNG | PNG, SVG |
| Custom colors | Yes (fg + bg) | Yes | Limited | Yes |
| Error correction | L/M/Q/H selectable | Fixed | Fixed | Limited |
| Base64 JSON | Yes | No | No | No |
| Edge latency | Sub-100ms (CF) | Variable | Variable | Variable |
| Rate limiting | Documented headers | Undocumented | Undocumented | Undocumented |
| SLA/Support | RapidAPI backed | None | None | None |

## Why Choose This QR Code API?

- **Instant response** -- sub-100ms latency from Cloudflare's global edge network (300+ cities)
- **Multiple output formats** -- PNG image, SVG vector, or Base64 JSON for embedding
- **Full customization** -- colors, size (10-1000px), error correction (L/M/Q/H)
- **No auth overhead** -- no separate API key registration, no OAuth flow
- **Free tier available** -- 500 requests/month at $0, perfect for prototyping and personal projects
- **Production-ready** -- rate limiting, CORS support, proper error handling

## Use Cases

- **E-commerce** -- generate QR codes for product pages, payment links, order tracking
- **Marketing campaigns** -- flyers, posters, business cards with branded QR codes
- **Restaurant menus** -- contactless digital menus via QR code
- **Event ticketing** -- unique QR codes for admission and check-in
- **Mobile apps** -- dynamic QR code generation for sharing, authentication, Wi-Fi config
- **SaaS dashboards** -- embed QR codes in invoices, reports, user profiles

## Quick Start

### Generate a PNG QR Code

```bash
curl -X GET "https://qr-code-api.t-mizuno27.workers.dev/generate?text=https://example.com" \
  -H "X-RapidAPI-Key: YOUR_KEY" \
  -H "X-RapidAPI-Host: qr-code-generator-api.p.rapidapi.com" \
  -o qrcode.png
```

### Generate an SVG QR Code

```bash
curl -X GET "https://qr-code-api.t-mizuno27.workers.dev/generate?text=hello&format=svg" \
  -H "X-RapidAPI-Key: YOUR_KEY" \
  -o qrcode.svg
```

### Get Base64 JSON Response

```bash
curl -X GET "https://qr-code-api.t-mizuno27.workers.dev/generate?text=hello&format=base64" \
  -H "X-RapidAPI-Key: YOUR_KEY"
```

**Response:**
```json
{
  "data": "<base64-string>",
  "data_uri": "data:image/png;base64,<base64-string>",
  "mime_type": "image/png",
  "size": 1234
}
```

### Python Example

```python
import requests

url = "https://qr-code-generator-api.p.rapidapi.com/generate"
params = {"text": "https://mysite.com", "size": 400, "format": "png", "color": "1a73e8"}
headers = {
    "X-RapidAPI-Key": "YOUR_KEY",
    "X-RapidAPI-Host": "qr-code-generator-api.p.rapidapi.com"
}

response = requests.get(url, headers=headers, params=params)
with open("qrcode.png", "wb") as f:
    f.write(response.content)
```

### Node.js Example

```javascript
const axios = require("axios");
const fs = require("fs");

const response = await axios.get(
  "https://qr-code-generator-api.p.rapidapi.com/generate",
  {
    params: { text: "https://mysite.com", size: 400, format: "png" },
    headers: {
      "X-RapidAPI-Key": "YOUR_KEY",
      "X-RapidAPI-Host": "qr-code-generator-api.p.rapidapi.com",
    },
    responseType: "arraybuffer",
  }
);
fs.writeFileSync("qrcode.png", response.data);
```

## API Reference

### `GET /generate`

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `text` | string | Yes | -- | Text or URL to encode (max 4296 chars) |
| `size` | integer | No | 300 | Image size in pixels (10-1000) |
| `format` | string | No | `png` | Output format: `png`, `svg`, `base64` |
| `color` | string | No | `000000` | Foreground color (6-digit hex, no `#`) |
| `bgcolor` | string | No | `ffffff` | Background color (6-digit hex, no `#`) |
| `error_correction` | string | No | `M` | Error correction: `L` (7%), `M` (15%), `Q` (25%), `H` (30%) |

### `GET /`

Returns API info and available parameters as JSON.

## Pricing

| Plan | Price | Requests/mo | Rate Limit |
|------|-------|-------------|------------|
| Basic (FREE) | $0 | 500 | 1 req/sec |
| Pro | $5.99 | 50,000 | 10 req/sec |
| Ultra | $14.99 | 500,000 | 50 req/sec |

## Rate Limiting

Default: 60 requests per minute per IP. Headers returned:

- `X-RateLimit-Limit` -- Max requests per window
- `X-RateLimit-Remaining` -- Remaining requests
- `X-RateLimit-Reset` -- Seconds until window resets

## FAQ

**Q: What's the maximum text/URL length?**
A: Up to 4,296 characters. For long URLs, consider a URL shortener first.

**Q: Can I use custom brand colors?**
A: Yes. Set `color` (foreground) and `bgcolor` (background) parameters with 6-digit hex values. Example: `color=1a73e8&bgcolor=f0f0f0`

**Q: What's the difference between PNG, SVG, and Base64?**
A: PNG is a raster image (good for most uses). SVG is vector (scales infinitely, ideal for print). Base64 returns JSON with an embeddable data URI (no file download needed).

**Q: What error correction level should I use?**
A: `M` (15%) is the default and works for most cases. Use `H` (30%) if the QR code will be printed on curved surfaces or partially obscured.

**Q: Is there a batch/bulk generation endpoint?**
A: Not currently. For bulk generation, loop through the /generate endpoint. At 60 req/min rate limit, you can generate 60 QR codes per minute.

## Alternative To

A free, SLA-backed alternative to goqr.me, QR Server, and QRickit. Same QR generation capabilities with custom colors, multiple output formats, documented rate limits, and RapidAPI support.

## Keywords

`qr code api`, `qr code generator`, `free qr api`, `generate qr code`, `qr code rest api`, `svg qr code`, `base64 qr code`, `custom qr code`, `qr code for marketing`, `cloudflare workers api`, `qr code generator free`, `qr code api rest`

## Development

```bash
npm install
npm run dev      # Local development
npm run deploy   # Deploy to Cloudflare
```
