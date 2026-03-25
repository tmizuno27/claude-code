---
title: "Free QR Code Generator API — No Auth, Custom Colors, SVG & PNG Support"
published: false
tags: api, webdev, javascript, tutorial
---

Need to generate QR codes programmatically? Most QR code APIs either require complex authentication, charge per request, or limit you to basic black-and-white output.

I built a **free QR Code Generator API** running on Cloudflare Workers' edge network. Here's what makes it different:

- **No authentication** required for the free tier (500 requests/month)
- **Custom colors** — foreground, background, any hex code
- **Multiple formats** — PNG, SVG, or Base64
- **Error correction levels** — L, M, Q, H
- **Sub-50ms response** from 300+ global edge locations
- **Zero cold starts** — it's always warm

## Quick Start

### Generate a basic QR code

```bash
curl "https://qr-code-generator-api.p.rapidapi.com/generate?text=https://example.com&size=300&format=png"
```

### With custom colors (branded QR code)

```bash
curl "https://qr-code-generator-api.p.rapidapi.com/generate?text=https://mysite.com&size=400&format=svg&color=1DB954&bgcolor=191414"
```

This creates a Spotify-green-on-dark QR code — great for branded materials.

## JavaScript Example

```javascript
const response = await fetch(
  'https://qr-code-generator-api.p.rapidapi.com/generate?' +
  new URLSearchParams({
    text: 'https://example.com',
    size: '300',
    format: 'png',
    color: '000000',
    bgcolor: 'FFFFFF',
    errorCorrection: 'M'
  })
);

const blob = await response.blob();
const url = URL.createObjectURL(blob);
document.getElementById('qr').src = url;
```

## Python Example

```python
import requests

response = requests.get(
    "https://qr-code-generator-api.p.rapidapi.com/generate",
    params={
        "text": "https://example.com",
        "size": 300,
        "format": "svg",
        "color": "333333",
        "bgcolor": "FFFFFF"
    }
)

with open("qr.svg", "w") as f:
    f.write(response.text)
```

## Real-World Use Cases

### 1. Restaurant menus
Generate dynamic QR codes pointing to your menu page. Update the URL without reprinting.

### 2. Event tickets
Embed ticket IDs in QR codes with high error correction (level H) so they scan even when partially damaged.

### 3. Product packaging
Brand-colored QR codes that match your packaging design.

### 4. Business cards (vCards)

```bash
curl "https://qr-code-generator-api.p.rapidapi.com/generate?text=BEGIN:VCARD%0AVERSION:3.0%0AFN:John%20Doe%0AEMAIL:john@example.com%0AEND:VCARD&size=300&format=png"
```

## Parameters Reference

| Parameter | Default | Description |
|-----------|---------|-------------|
| `text` | (required) | Content to encode |
| `size` | 200 | Image size in pixels |
| `format` | png | `png`, `svg`, or `base64` |
| `color` | 000000 | Foreground hex color |
| `bgcolor` | FFFFFF | Background hex color |
| `errorCorrection` | M | `L`, `M`, `Q`, or `H` |

## Why Not Use a Library?

You absolutely can use `qrcode.js` or Python's `qrcode` library. But if you need QR generation in:

- **Serverless functions** (no native dependencies)
- **Mobile apps** (just an HTTP call)
- **No-code tools** (Zapier, Make, n8n)
- **Multiple languages** (one API, any client)

...then an API is simpler than managing dependencies across platforms.

## Performance

Built on Cloudflare Workers — no containers, no cold starts. Average response time is under 30ms globally. The free tier gives you 500 requests/month, which is plenty for development and small projects.

[**Try it free on RapidAPI →**](https://rapidapi.com/miccho27-5OJaGGbBiO/api/qr-code-generator-api)

---

*This API is part of a [collection of 24 developer tools](https://rapidapi.com/user/miccho27-5OJaGGbBiO) — all free tier, all on Cloudflare's edge.*
