---
title: "Generate QR Codes and Website Screenshots with a Single API — No Puppeteer, No Headless Chrome"
published: false
tags: api, webdev, javascript, tutorial
---

You want to generate a QR code or capture a website screenshot in your app. The typical advice? Spin up Puppeteer, install headless Chrome, deal with memory leaks and cold starts.

There's a simpler way. Two lightweight APIs running on Cloudflare Workers that handle both — with sub-50ms response times and zero infrastructure on your end.

## QR Code Generator API

Generate QR codes in PNG, SVG, or Base64 format with customizable colors, size, and error correction levels.

### Quick Start

```bash
# Generate a PNG QR code
curl "https://qr-code-generator-api.p.rapidapi.com/generate?text=https://example.com&size=300&format=png" \
  -H "X-RapidAPI-Key: YOUR_KEY" \
  --output qr.png
```

### JavaScript Example

```javascript
const axios = require('axios');
const fs = require('fs');

async function generateQR(text, options = {}) {
  const { size = 300, format = 'png', color = '000000', bgcolor = 'FFFFFF' } = options;

  const response = await axios.get(
    'https://qr-code-generator-api.p.rapidapi.com/generate',
    {
      params: { text, size, format, color, bgcolor },
      headers: { 'X-RapidAPI-Key': process.env.RAPIDAPI_KEY },
      responseType: format === 'svg' ? 'text' : 'arraybuffer'
    }
  );

  if (format === 'svg') {
    fs.writeFileSync('qr.svg', response.data);
  } else {
    fs.writeFileSync('qr.png', Buffer.from(response.data));
  }
  console.log(`QR code saved as qr.${format}`);
}

// Usage
generateQR('https://myapp.com/download', { size: 500, color: '1a73e8' });
```

### Python Example

```python
import requests

def generate_qr(text, size=300, fmt="png", color="000000", bgcolor="FFFFFF"):
    response = requests.get(
        "https://qr-code-generator-api.p.rapidapi.com/generate",
        params={"text": text, "size": size, "format": fmt, "color": color, "bgcolor": bgcolor},
        headers={"X-RapidAPI-Key": "YOUR_KEY"}
    )

    filename = f"qr.{fmt}"
    if fmt == "svg":
        with open(filename, "w") as f:
            f.write(response.text)
    else:
        with open(filename, "wb") as f:
            f.write(response.content)
    print(f"Saved {filename}")

generate_qr("https://example.com", size=400, color="e91e63")
```

### Use Cases

- **Event tickets**: Encode ticket IDs into QR codes for scanning
- **Restaurant menus**: Generate dynamic menu QR codes
- **App download links**: Create branded QR codes for marketing materials
- **Two-factor authentication**: Generate TOTP setup QR codes

[Try QR Code Generator API on RapidAPI](https://rapidapi.com/miccho27-5OJaGGbBiO/api/qr-code-generator-api)

---

## Screenshot Capture API

Capture full-page or viewport screenshots of any website as PNG images — without running a browser.

### Quick Start

```bash
curl "https://screenshot-capture-api.p.rapidapi.com/capture?url=https://github.com&width=1280&height=800" \
  -H "X-RapidAPI-Key: YOUR_KEY" \
  --output screenshot.png
```

### Building a Link Preview Service

Here's a practical example — building a link preview service that generates thumbnails for shared URLs:

```javascript
const express = require('express');
const axios = require('axios');

const app = express();
const CACHE = new Map();

app.get('/preview/:url', async (req, res) => {
  const targetUrl = decodeURIComponent(req.params.url);
  const cacheKey = targetUrl;

  if (CACHE.has(cacheKey)) {
    res.setHeader('Content-Type', 'image/png');
    return res.send(CACHE.get(cacheKey));
  }

  try {
    const response = await axios.get(
      'https://screenshot-capture-api.p.rapidapi.com/capture',
      {
        params: { url: targetUrl, width: 1280, height: 800 },
        headers: { 'X-RapidAPI-Key': process.env.RAPIDAPI_KEY },
        responseType: 'arraybuffer'
      }
    );

    CACHE.set(cacheKey, Buffer.from(response.data));
    res.setHeader('Content-Type', 'image/png');
    res.send(response.data);
  } catch (err) {
    res.status(500).json({ error: 'Screenshot capture failed' });
  }
});

app.listen(3000);
```

### Python: Batch Screenshot Tool

```python
import requests
from pathlib import Path

def capture_screenshots(urls, output_dir="screenshots"):
    Path(output_dir).mkdir(exist_ok=True)

    for url in urls:
        slug = url.replace("https://", "").replace("/", "_")[:50]
        response = requests.get(
            "https://screenshot-capture-api.p.rapidapi.com/capture",
            params={"url": url, "width": 1280, "height": 800},
            headers={"X-RapidAPI-Key": "YOUR_KEY"}
        )

        if response.status_code == 200:
            filepath = f"{output_dir}/{slug}.png"
            with open(filepath, "wb") as f:
                f.write(response.content)
            print(f"Captured: {filepath}")
        else:
            print(f"Failed: {url} (HTTP {response.status_code})")

# Monitor competitor websites
capture_screenshots([
    "https://github.com",
    "https://dev.to",
    "https://stackoverflow.com"
])
```

[Try Screenshot Capture API on RapidAPI](https://rapidapi.com/miccho27-5OJaGGbBiO/api/screenshot-capture-api)

---

## Why Cloudflare Workers?

Both APIs run on Cloudflare's edge network (300+ locations worldwide), which means:

- **No cold starts** — Workers are always warm
- **Sub-50ms latency** — served from the nearest edge location
- **Automatic scaling** — handles traffic spikes without configuration
- **99.99% uptime** — Cloudflare's global infrastructure

## Free Tier

Both APIs offer **500 requests/month** on the free tier via RapidAPI. No credit card required to get started.

---

*Built and maintained by [@miccho27](https://rapidapi.com/miccho27-5OJaGGbBiO). Found a bug or have a feature request? Open an issue on [GitHub](https://github.com/tmizuno27).*
