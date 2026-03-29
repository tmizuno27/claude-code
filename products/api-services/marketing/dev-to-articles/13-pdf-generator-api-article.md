---
title: Generate PDFs from HTML, Markdown, or URL via API — Free, No Puppeteer Setup Required
tags: api, webdev, javascript, python
published: false
---

Setting up Puppeteer or wkhtmltopdf in production is a pain. Lambda cold starts, binary layer size limits, font rendering issues, memory spikes — every time I needed "just generate a PDF," it turned into a half-day infrastructure project.

So I built a PDF Generator API on Cloudflare Workers that handles the heavy lifting. Send it HTML, Markdown, or a URL — get back a PDF. That's it.

## What You Get (Free Tier: 500 requests/month)

- HTML to PDF conversion (full CSS support)
- Markdown to PDF (code highlighting included)
- URL to PDF (render any public webpage)
- Custom page size: A4, Letter, Legal
- Configurable margins, headers, footers
- Landscape / portrait orientation
- Returns base64-encoded PDF or binary stream

## Quick Start

### Python — Invoice Generator

```python
import requests
import base64

API_KEY = "your-rapidapi-key"
headers = {
    "x-rapidapi-key": API_KEY,
    "x-rapidapi-host": "pdf-generator-api2.p.rapidapi.com",
    "Content-Type": "application/json"
}

# HTML to PDF
invoice_html = """
<!DOCTYPE html>
<html>
<head>
  <style>
    body { font-family: Arial, sans-serif; margin: 40px; }
    h1 { color: #2c3e50; }
    table { width: 100%; border-collapse: collapse; margin-top: 20px; }
    th, td { border: 1px solid #ddd; padding: 8px; text-align: left; }
    th { background-color: #3498db; color: white; }
    .total { font-weight: bold; font-size: 1.2em; }
  </style>
</head>
<body>
  <h1>Invoice #2026-001</h1>
  <p>Date: 2026-03-29 | Due: 2026-04-29</p>
  <table>
    <tr><th>Item</th><th>Qty</th><th>Price</th><th>Total</th></tr>
    <tr><td>API Development</td><td>10h</td><td>$150</td><td>$1,500</td></tr>
    <tr><td>Cloudflare Setup</td><td>2h</td><td>$150</td><td>$300</td></tr>
    <tr><td colspan="3" class="total">Total</td><td class="total">$1,800</td></tr>
  </table>
</body>
</html>
"""

response = requests.post(
    "https://pdf-generator-api2.p.rapidapi.com/html",
    headers=headers,
    json={
        "html": invoice_html,
        "options": {
            "format": "A4",
            "margin": {"top": "20mm", "bottom": "20mm", "left": "15mm", "right": "15mm"}
        }
    }
)

result = response.json()

# Decode and save PDF
pdf_bytes = base64.b64decode(result["pdf"])
with open("invoice.pdf", "wb") as f:
    f.write(pdf_bytes)

print(f"PDF saved: {result.get('size_bytes', 0) / 1024:.1f} KB")
```

### JavaScript — Markdown Report to PDF

```javascript
const fetch = require('node-fetch');
const fs = require('fs');

const headers = {
  'x-rapidapi-key': 'your-rapidapi-key',
  'x-rapidapi-host': 'pdf-generator-api2.p.rapidapi.com',
  'Content-Type': 'application/json'
};

const reportMarkdown = `
# Weekly Performance Report

## Summary

| Metric | This Week | Last Week | Change |
|--------|-----------|-----------|--------|
| API Calls | 12,450 | 10,200 | +22% |
| Errors | 23 | 41 | -44% |
| Avg Latency | 87ms | 112ms | -22% |

## Key Findings

- Response times improved after edge caching implementation
- Error rate dropped following input validation fix
- Traffic spike on Wednesday correlated with Dev.to article publish

\`\`\`bash
# Top endpoints by usage
/price        4,201 calls
/translate    3,890 calls
/screenshot   2,100 calls
\`\`\`
`;

async function generateReport() {
  const res = await fetch('https://pdf-generator-api2.p.rapidapi.com/markdown', {
    method: 'POST',
    headers,
    body: JSON.stringify({
      markdown: reportMarkdown,
      options: {
        format: 'A4',
        header: { text: 'Weekly Report — Confidential', fontSize: 10 },
        footer: { text: 'Page {page} of {pages}', fontSize: 9 }
      }
    })
  });

  const data = await res.json();
  const pdfBuffer = Buffer.from(data.pdf, 'base64');
  fs.writeFileSync('report.pdf', pdfBuffer);
  console.log(`Report saved (${(pdfBuffer.length / 1024).toFixed(1)} KB)`);
}

generateReport();
```

## All Endpoints

| Method | Path | Input | Description |
|--------|------|-------|-------------|
| `POST` | `/html` | `{ html, options }` | Convert HTML string to PDF |
| `POST` | `/markdown` | `{ markdown, options }` | Convert Markdown to styled PDF |
| `POST` | `/url` | `{ url, options }` | Render a public URL as PDF |

### Options Reference

```json
{
  "format": "A4",           // A4, Letter, Legal, A3, Tabloid
  "orientation": "portrait", // portrait, landscape
  "margin": {
    "top": "20mm",
    "bottom": "20mm",
    "left": "15mm",
    "right": "15mm"
  },
  "header": {
    "text": "My Company Report",
    "fontSize": 10
  },
  "footer": {
    "text": "Page {page} of {pages}",
    "fontSize": 9
  }
}
```

## Use Case: SaaS Receipt Generator

```python
from flask import Flask, send_file
import requests
import base64
import io

app = Flask(__name__)

RAPIDAPI_KEY = "your-rapidapi-key"

def generate_receipt_pdf(order_id: str, items: list, total: float) -> bytes:
    rows = "".join(
        f"<tr><td>{item['name']}</td><td>{item['qty']}</td>"
        f"<td>${item['price']:.2f}</td></tr>"
        for item in items
    )
    html = f"""
    <html><body style="font-family:sans-serif;padding:30px">
      <h2>Receipt #{order_id}</h2>
      <table border="1" cellpadding="8" style="border-collapse:collapse;width:100%">
        <tr style="background:#f0f0f0"><th>Item</th><th>Qty</th><th>Price</th></tr>
        {rows}
        <tr><td colspan="2"><b>Total</b></td><td><b>${total:.2f}</b></td></tr>
      </table>
    </body></html>
    """
    r = requests.post(
        "https://pdf-generator-api2.p.rapidapi.com/html",
        headers={"x-rapidapi-key": RAPIDAPI_KEY,
                 "x-rapidapi-host": "pdf-generator-api2.p.rapidapi.com",
                 "Content-Type": "application/json"},
        json={"html": html, "options": {"format": "A4"}}
    )
    return base64.b64decode(r.json()["pdf"])

@app.route("/receipt/<order_id>")
def receipt(order_id):
    items = [{"name": "Pro Plan", "qty": 1, "price": 9.99}]
    pdf_bytes = generate_receipt_pdf(order_id, items, 9.99)
    return send_file(
        io.BytesIO(pdf_bytes),
        mimetype="application/pdf",
        download_name=f"receipt-{order_id}.pdf"
    )
```

## Pricing

| Plan | Price | Requests/month | Rate Limit |
|------|-------|----------------|------------|
| Basic (FREE) | $0 | 500 | 1 req/sec |
| Pro | $5.99 | 50,000 | 10 req/sec |
| Ultra | $14.99 | 500,000 | 50 req/sec |

**Available on RapidAPI:** [PDF Generator API](https://rapidapi.com/miccho27-RNuiryMxge/api/pdf-generator-api2)

## How It Compares to DIY Solutions

| Approach | Setup Time | Cold Start | Memory | Cost |
|----------|-----------|------------|--------|------|
| This API | 5 min | ~80ms | 0 (offloaded) | $0–$5.99/mo |
| Puppeteer on Lambda | 2–4 hrs | 3–8 sec | 512MB–1GB | $5–$30/mo |
| wkhtmltopdf server | 4–8 hrs | N/A | 256MB+ | EC2 cost |
| PDFKit (Node) | 1 hr | 0ms | Low | Free but limited CSS |

No layer management, no binary installs, no headless browser cold starts.

## See All My Free APIs

[Browse all 24 APIs on RapidAPI →](https://rapidapi.com/user/miccho27-RNuiryMxge)

---

*Using this for something? Let me know in the comments — always curious to see what people build.*
