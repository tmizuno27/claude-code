# PDF Generator API

Generate PDFs from HTML, Markdown, or URLs with custom page settings. Deployed on Cloudflare Workers.

## Endpoints

| Method | Path | Description |
|--------|------|-------------|
| GET | `/` | API info and available endpoints |
| POST | `/generate` | Convert HTML string to PDF |
| POST | `/from-markdown` | Convert Markdown string to PDF |
| POST | `/from-url` | Fetch a URL and convert its HTML to PDF |

## Parameters

All POST endpoints accept these optional parameters:

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `page_size` | string | A4 | A4, A3, Letter, Legal |
| `orientation` | string | portrait | portrait or landscape |
| `margin_top` | number | 72 | Top margin in points |
| `margin_bottom` | number | 72 | Bottom margin in points |
| `margin_left` | number | 72 | Left margin in points |
| `margin_right` | number | 72 | Right margin in points |
| `font_size` | number | 12 | Font size in points |
| `header` | string | — | Header text for each page |
| `footer` | string | — | Footer text (use `{{page}}` and `{{pages}}`) |
| `filename` | string | document.pdf | Output filename |

## Examples

```bash
# HTML to PDF
curl -X POST https://pdf-generator-api.t-mizuno27.workers.dev/generate \
  -H "Content-Type: application/json" \
  -d '{"html": "<h1>Invoice</h1><p>Total: $100</p>", "page_size": "A4"}'

# Markdown to PDF
curl -X POST https://pdf-generator-api.t-mizuno27.workers.dev/from-markdown \
  -H "Content-Type: application/json" \
  -d '{"markdown": "# Report\n\n## Summary\n\nThis is a test."}'

# URL to PDF
curl -X POST https://pdf-generator-api.t-mizuno27.workers.dev/from-url \
  -H "Content-Type: application/json" \
  -d '{"url": "https://example.com"}'
```

## Response

Returns `application/pdf` binary with `Content-Disposition: attachment; filename="document.pdf"`.

## Rate Limiting

20 requests per minute per IP.

## Development

```bash
npm install
npm run dev      # Local development
npm run deploy   # Deploy to Cloudflare
```
