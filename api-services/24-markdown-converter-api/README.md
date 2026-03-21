# Markdown Converter API

Bidirectional Markdown/HTML conversion with full GFM support, syntax highlighting, and auto-generated Table of Contents. Deployed on Cloudflare Workers.

## Endpoints

| Method | Path | Description |
|--------|------|-------------|
| GET | `/` | API info |
| POST | `/convert` | Markdown to HTML (with optional TOC) |
| POST | `/reverse` | HTML to Markdown |
| POST | `/toc` | Extract Table of Contents from Markdown |

## Usage

### Markdown to HTML

```bash
curl -X POST https://markdown-converter-api.t-mizuno27.workers.dev/convert \
  -H "Content-Type: application/json" \
  -d '{"markdown": "# Hello\n\nThis is **bold** text.", "toc": true}'
```

**Response:**
```json
{
  "html": "<h1 id=\"hello\">Hello</h1>\n<p>This is <strong>bold</strong> text.</p>",
  "toc": [{"level": 1, "text": "Hello", "id": "hello"}]
}
```

### HTML to Markdown

```bash
curl -X POST https://markdown-converter-api.t-mizuno27.workers.dev/reverse \
  -H "Content-Type: application/json" \
  -d '{"html": "<h1>Hello</h1><p>This is <strong>bold</strong> text.</p>"}'
```

### Extract TOC

```bash
curl -X POST https://markdown-converter-api.t-mizuno27.workers.dev/toc \
  -H "Content-Type: application/json" \
  -d '{"markdown": "# Chapter 1\n## Section 1.1\n# Chapter 2"}'
```

## Features

- Full GFM support (tables, task lists, strikethrough)
- Syntax highlighting CSS classes for code blocks
- Auto-generated Table of Contents with anchor links
- Bidirectional conversion (MD to HTML and HTML to MD)
- Pure JavaScript, no external dependencies

## Rate Limiting

20 requests per minute per IP.

## Development

```bash
npm install
npm run dev      # Local development
npm run deploy   # Deploy to Cloudflare
```
