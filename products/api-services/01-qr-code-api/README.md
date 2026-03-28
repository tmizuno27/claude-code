# QR Code Generator API - The Fastest Free QR Code API on RapidAPI

**Generate QR codes in under 50ms from 300+ edge locations worldwide.** PNG, SVG, or Base64 with full color customization. No auth setup, no SDK, no overhead.

> Free tier: 500 requests/month | Production-ready | Zero configuration

## Why Developers Choose This Over Alternatives

Most QR code APIs are slow, undocumented, or charge per-image. This API runs on Cloudflare's edge network, returns in under 50ms, and costs nothing for prototyping.

| | **This API** | goqr.me | QR Server | QRickit | QR Code Monkey |
|---|---|---|---|---|---|
| **Free tier** | 500 req/mo (SLA-backed) | Unlimited (no SLA, no support) | Unlimited (no SLA) | Limited | Limited |
| **Latency** | <50ms (Cloudflare edge) | 200-500ms | 300-800ms | Variable | Variable |
| **Output formats** | PNG + SVG + Base64 JSON | PNG, SVG | PNG only | PNG, SVG | PNG |
| **Custom colors** | Foreground + background | Yes | Limited | Yes | Yes (web UI) |
| **Error correction** | L/M/Q/H selectable | Fixed | Fixed | Limited | Yes (web UI) |
| **Base64 JSON embed** | Yes (no file download) | No | No | No | No |
| **Rate limit headers** | Documented | Undocumented | Undocumented | Undocumented | N/A |
| **RapidAPI support** | Yes | No | No | No | No |
| **Pro plan (50K/mo)** | **$5.99** | N/A | N/A | N/A | $14/mo |

## Quick Start - Python

```python
import requests

url = "https://qr-code-generator-api.p.rapidapi.com/generate"
params = {
    "text": "https://your-product.com/checkout?ref=qr123",
    "size": 400,
    "format": "png",
    "color": "1a73e8",
    "bgcolor": "ffffff"
}
headers = {
    "X-RapidAPI-Key": "YOUR_KEY",
    "X-RapidAPI-Host": "qr-code-generator-api.p.rapidapi.com"
}

response = requests.get(url, headers=headers, params=params)
with open("branded-qr.png", "wb") as f:
    f.write(response.content)
print(f"QR code saved ({len(response.content)} bytes)")
```

## Quick Start - JavaScript / Node.js

```javascript
const axios = require("axios");
const fs = require("fs");

const response = await axios.get(
  "https://qr-code-generator-api.p.rapidapi.com/generate",
  {
    params: { text: "https://your-product.com", size: 400, format: "base64" },
    headers: {
      "X-RapidAPI-Key": "YOUR_KEY",
      "X-RapidAPI-Host": "qr-code-generator-api.p.rapidapi.com",
    },
  }
);

// Base64 format returns JSON - embed directly in HTML
const { data_uri } = response.data;
console.log(`<img src="${data_uri}" alt="QR Code" />`);
```

## Quick Start - cURL

```bash
# Download as PNG file
curl "https://qr-code-generator-api.p.rapidapi.com/generate?text=https://example.com&size=400&color=FF5722" \
  -H "X-RapidAPI-Key: YOUR_KEY" \
  -H "X-RapidAPI-Host: qr-code-generator-api.p.rapidapi.com" \
  -o branded-qr.png

# Get as Base64 JSON (no file download needed)
curl "https://qr-code-generator-api.p.rapidapi.com/generate?text=https://example.com&format=base64" \
  -H "X-RapidAPI-Key: YOUR_KEY" \
  -H "X-RapidAPI-Host: qr-code-generator-api.p.rapidapi.com"
```

## Real-World Use Cases

### E-Commerce: Dynamic Checkout QR Codes
Generate unique QR codes for each order that link to payment pages. Sub-50ms response means no checkout delay.

### Restaurant Menus: Contactless Digital Menus
Generate a QR code per table linking to your digital menu. Use custom colors to match your brand. SVG format for print-quality output.

### SaaS Invoices: Embedded QR Codes
Use Base64 format to embed QR codes directly in HTML invoices and PDFs without file I/O. The `data_uri` field is ready for `<img src="">`.

### Marketing: Branded Campaign QR Codes
Custom foreground/background colors for brand consistency on flyers, posters, and business cards. Error correction level H (30%) for QR codes that work even when partially covered.

### Mobile Apps: Deep Link QR Codes
Generate QR codes pointing to app deep links (`myapp://screen/123`). Works with iOS Universal Links and Android App Links.

### CI/CD: Automated QR Code Generation
Generate QR codes as part of your build pipeline for deployment URLs, staging previews, or release notes.

## API Reference

### `GET /generate`

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `text` | string | Yes | -- | Text or URL to encode (max 4,296 chars) |
| `size` | integer | No | 300 | Image size in pixels (10-1000) |
| `format` | string | No | `png` | `png`, `svg`, or `base64` |
| `color` | string | No | `000000` | Foreground color (hex, no `#`) |
| `bgcolor` | string | No | `ffffff` | Background color (hex, no `#`) |
| `error_correction` | string | No | `M` | `L` (7%), `M` (15%), `Q` (25%), `H` (30%) |

### Response Formats

**PNG/SVG**: Binary image data (set `responseType: "arraybuffer"` in axios)

**Base64 JSON**:
```json
{
  "data": "<base64-string>",
  "data_uri": "data:image/png;base64,<base64-string>",
  "mime_type": "image/png",
  "size": 1234
}
```

## Pricing Recommendation

| Plan | Price | Requests/mo | Rate Limit | Best For |
|------|-------|-------------|------------|----------|
| **Basic (FREE)** | $0 | 500 | 1 req/sec | Prototyping, personal projects |
| **Pro** | $5.99 | 50,000 | 10 req/sec | Production apps, SaaS products |
| **Ultra** | $14.99 | 500,000 | 50 req/sec | High-traffic e-commerce, agencies |
| **Mega** | $49.99 | 5,000,000 | 100 req/sec | Enterprise, white-label solutions |

Start free. No credit card required. Upgrade when you need more capacity.

## FAQ

**Q: What's the maximum text/URL length?**
A: Up to 4,296 characters. For long URLs, use a URL shortener first.

**Q: Can I use custom brand colors?**
A: Yes. Set `color` (foreground) and `bgcolor` (background) with 6-digit hex values. Example: `color=1a73e8&bgcolor=f0f0f0`.

**Q: What's the difference between PNG, SVG, and Base64?**
A: PNG is raster (good for web/mobile). SVG is vector (scales perfectly for print). Base64 returns JSON with an embeddable `data_uri` -- no file download needed, perfect for email templates and dynamic HTML.

**Q: What error correction level should I use?**
A: `M` (15%) works for most cases. Use `H` (30%) if the QR code will be printed on curved surfaces, partially covered by a logo, or used in harsh environments.

**Q: Is there a batch generation endpoint?**
A: Not currently. For bulk generation, loop through `/generate`. At Pro tier (10 req/sec), you can generate 600 QR codes per minute.

**Q: Can I add a logo to the center of the QR code?**
A: Not natively. Generate with `error_correction=H` (30% redundancy), then overlay your logo on the center 20% of the image client-side. The high error correction ensures scannability.


## Also From This Publisher

Build powerful workflows by combining APIs:

| API | Why Combine? |
|-----|-------------|
| **PDF Generator API** | Generate PDFs with embedded QR codes |
| **Screenshot API** | Capture QR code landing pages for previews |
| **URL Shortener API** | Shorten URLs before encoding in QR codes |
| **Placeholder Image API** | Generate placeholder images for prototypes |

> All APIs include a free tier. Subscribe to one, discover the full toolkit on [our RapidAPI profile](https://rapidapi.com/miccho27-5OJaGGbBiO).

## Keywords

`qr code api`, `qr code generator api`, `free qr api`, `qr code rest api`, `generate qr code programmatically`, `svg qr code api`, `base64 qr code`, `custom color qr code`, `qr code for e-commerce`, `cloudflare workers api`, `rapidapi qr code`, `qr code alternative to goqr`
