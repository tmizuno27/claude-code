---
title: "Generate Custom QR Codes via API — Free, No Auth, SVG & PNG with Branded Colors"
published: false
description: "A free QR Code Generator API on Cloudflare Workers. Custom colors, SVG/PNG/Base64 output, sub-30ms latency, 500 free requests/month. Code examples in Python and JavaScript."
tags: api, webdev, javascript, tutorial
---

Need to generate QR codes programmatically? Most QR code APIs either require complex authentication, charge per request, or limit you to basic black-and-white output.

I built a **free QR Code Generator API** running on Cloudflare Workers' edge network. Here's what makes it different and how to integrate it in under 5 minutes.

## Why Another QR Code API?

Libraries like `qrcode.js` or Python's `qrcode` work fine locally — but they break down when you need QR generation in:

- **Serverless functions** where native dependencies are a pain
- **Mobile apps** where a simple HTTP call beats bundling a library
- **No-code tools** like Zapier, Make, or n8n
- **Multiple languages** — one API, any client

This API gives you a single HTTP endpoint that works everywhere, with **zero cold starts** and **sub-30ms response times** from 300+ Cloudflare edge locations.

## Features at a Glance

- **Custom colors** — any hex code for foreground and background
- **Multiple formats** — PNG, SVG, or Base64 (embed directly in HTML)
- **Error correction levels** — L, M, Q, H (H survives up to 30% damage)
- **No authentication** on the free tier (500 requests/month)
- **No rate limiting surprises** — clear 500/month quota

## Quick Start

### Basic QR Code (cURL)

```bash
curl "https://qr-code-generator-api.p.rapidapi.com/generate?text=https://example.com&size=300&format=png" \
  -H "X-RapidAPI-Key: YOUR_KEY" \
  -H "X-RapidAPI-Host: qr-code-generator-api.p.rapidapi.com" \
  --output qr.png
```

### Branded QR Code (Spotify Green on Dark)

```bash
curl "https://qr-code-generator-api.p.rapidapi.com/generate?text=https://mysite.com&size=400&format=svg&color=1DB954&bgcolor=191414" \
  -H "X-RapidAPI-Key: YOUR_KEY" \
  -H "X-RapidAPI-Host: qr-code-generator-api.p.rapidapi.com"
```

## JavaScript — Display QR Code in the Browser

```javascript
const url = "https://qr-code-generator-api.p.rapidapi.com/generate";
const params = new URLSearchParams({
  text: "https://example.com",
  size: "300",
  format: "png",
  color: "000000",
  bgcolor: "FFFFFF",
  errorCorrection: "M",
});

const response = await fetch(`${url}?${params}`, {
  headers: {
    "X-RapidAPI-Key": "YOUR_KEY",
    "X-RapidAPI-Host": "qr-code-generator-api.p.rapidapi.com",
  },
});

const blob = await response.blob();
const imageUrl = URL.createObjectURL(blob);
document.getElementById("qr").src = imageUrl;
```

**Tip:** Use `format=base64` to get a data URI string you can embed directly in an `<img>` tag without blob handling.

## Python — Generate and Save QR Codes

```python
import requests

url = "https://qr-code-generator-api.p.rapidapi.com/generate"
headers = {
    "X-RapidAPI-Key": "YOUR_KEY",
    "X-RapidAPI-Host": "qr-code-generator-api.p.rapidapi.com",
}

# SVG output
response = requests.get(
    url,
    params={
        "text": "https://example.com",
        "size": 300,
        "format": "svg",
        "color": "333333",
        "bgcolor": "FFFFFF",
    },
    headers=headers,
)

with open("qr.svg", "w") as f:
    f.write(response.text)
print(f"Saved QR code ({len(response.text)} bytes)")
```

### Batch Generation

```python
products = [
    {"name": "Product A", "url": "https://shop.example.com/a"},
    {"name": "Product B", "url": "https://shop.example.com/b"},
    {"name": "Product C", "url": "https://shop.example.com/c"},
]

for product in products:
    resp = requests.get(
        url,
        params={"text": product["url"], "size": 400, "format": "png"},
        headers=headers,
    )
    filename = f"qr_{product['name'].lower().replace(' ', '_')}.png"
    with open(filename, "wb") as f:
        f.write(resp.content)
    print(f"Generated: {filename}")
```

## Parameters Reference

| Parameter | Default | Description |
|-----------|---------|-------------|
| `text` | *(required)* | Content to encode (URL, text, vCard, etc.) |
| `size` | 200 | Image size in pixels (50-1000) |
| `format` | png | `png`, `svg`, or `base64` |
| `color` | 000000 | Foreground hex color (no `#`) |
| `bgcolor` | FFFFFF | Background hex color (no `#`) |
| `errorCorrection` | M | `L` (7%), `M` (15%), `Q` (25%), `H` (30%) |

## Real-World Use Cases

**Restaurant menus** — Generate dynamic QR codes pointing to your menu page. Update the URL without reprinting physical menus.

**Event tickets** — Embed ticket IDs with high error correction (level H) so they scan even when crumpled or partially obscured.

**Product packaging** — Brand-colored QR codes that match your design system.

**vCards on business cards:**

```bash
curl "https://qr-code-generator-api.p.rapidapi.com/generate?text=BEGIN:VCARD%0AVERSION:3.0%0AFN:Jane%20Doe%0AEMAIL:jane@example.com%0AEND:VCARD&size=300&format=png&errorCorrection=H" \
  -H "X-RapidAPI-Key: YOUR_KEY" \
  -H "X-RapidAPI-Host: qr-code-generator-api.p.rapidapi.com"
```

## Performance

Built on Cloudflare Workers — no containers, no cold starts, no scaling concerns. Average response time is under 30ms globally. The free tier gives you 500 requests/month, which covers development and small production apps.

For higher volume, paid plans start at $5.99/month for 50,000 requests.

---

**[Try it free on RapidAPI](https://rapidapi.com/miccho27-5OJaGGbBiO/api/qr-code-generator-api)** — no credit card required.

*This API is part of a [collection of 24 developer tools](https://rapidapi.com/user/miccho27-5OJaGGbBiO) running on Cloudflare's edge network.*
