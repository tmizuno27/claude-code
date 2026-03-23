# Free Markdown Converter API - HTML to Markdown, GFM, TOC, Syntax Highlight

> **Free tier: 500 requests/month** | Bidirectional Markdown/HTML conversion with full GFM support

Convert Markdown to HTML and HTML back to Markdown. Supports GitHub Flavored Markdown (GFM), auto-generated Table of Contents, syntax highlighting for code blocks, and tables.

## Getting Started in 30 Seconds

1. Subscribe on [RapidAPI](https://rapidapi.com/miccho27-5OJaGGbBiO/api/markdown-converter-api) (free plan available)
2. Copy your API key
3. Convert your first Markdown:

```bash
curl -X POST "https://markdown-converter-api.p.rapidapi.com/md-to-html" \
  -H "Content-Type: application/json" \
  -H "X-RapidAPI-Key: YOUR_KEY" \
  -H "X-RapidAPI-Host: markdown-converter-api.p.rapidapi.com" \
  -d '{"markdown": "# Hello World\n\nThis is **bold** text.", "toc": true}'
```

## How It Compares

| Feature | This API | Showdown.js | Marked.js | Pandoc |
|---------|----------|------------|-----------|--------|
| Free tier | 500 req/mo | Library (no API) | Library (no API) | CLI (no API) |
| API access | Yes (REST) | No (JS library) | No (JS library) | No (CLI) |
| Markdown to HTML | Yes | Yes | Yes | Yes |
| HTML to Markdown | Yes | No | No | Yes |
| GFM tables | Yes | Yes | Yes | Yes |
| Auto TOC | Yes | No | No | Yes |
| Syntax highlighting | Yes (100+ langs) | No | No | Yes |
| XSS sanitization | Yes | No | No | N/A |
| No installation | Yes | npm install | npm install | System install |

## Why Choose This Markdown Converter API?

- **Bidirectional** -- Markdown to HTML and HTML to Markdown
- **GFM support** -- tables, task lists, strikethrough, autolinks
- **Table of Contents** -- auto-generate TOC from headings
- **Syntax highlighting** -- code block highlighting for 100+ languages
- **Sanitized output** -- XSS-safe HTML output
- **Free tier** -- 500 requests/month at $0

## Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/md-to-html` | POST | Convert Markdown to HTML |
| `/html-to-md` | POST | Convert HTML to Markdown |
| `/toc` | POST | Generate Table of Contents from Markdown |

## Use Cases

- **CMS platforms** -- render Markdown content as HTML for web display
- **Documentation tools** -- convert between Markdown and HTML formats
- **Blog engines** -- process Markdown blog posts into styled HTML
- **Email templates** -- convert Markdown drafts to HTML emails
- **Developer tools** -- format README files and documentation
- **Migration tools** -- convert HTML content to Markdown for Git-based CMS

## Quick Start

```bash
curl -X POST "https://markdown-converter-api.t-mizuno27.workers.dev/to-html" \
  -H "Content-Type: application/json" \
  -H "X-RapidAPI-Key: YOUR_KEY" \
  -d '{"markdown": "# Hello World\n\nThis is **bold** text.", "toc": true}'
```

### Python Example

```python
import requests

url = "https://markdown-converter-api.p.rapidapi.com/md-to-html"
headers = {"X-RapidAPI-Key": "YOUR_KEY", "X-RapidAPI-Host": "markdown-converter-api.p.rapidapi.com"}
payload = {"markdown": "# My Document\n\n- Item 1\n- Item 2", "toc": True}

data = requests.post(url, headers=headers, json=payload).json()
print(data["html"])
```

### Node.js Example

```javascript
const axios = require("axios");

const { data } = await axios.post(
  "https://markdown-converter-api.p.rapidapi.com/html-to-md",
  { html: "<h1>Title</h1><p>Paragraph with <strong>bold</strong></p>" },
  {
    headers: {
      "X-RapidAPI-Key": "YOUR_KEY",
      "X-RapidAPI-Host": "markdown-converter-api.p.rapidapi.com",
    },
  }
);

console.log(data.markdown);
```

## FAQ

**Q: Is the HTML output safe from XSS attacks?**
A: Yes. All HTML output is sanitized to remove potentially dangerous scripts, event handlers, and other XSS vectors.

**Q: What Markdown flavor is supported?**
A: GitHub Flavored Markdown (GFM), including tables, task lists, strikethrough, and autolinks.

**Q: How does the TOC generator work?**
A: Set `toc: true` and the API extracts all headings (H1-H6) to generate a nested table of contents with anchor links.

**Q: Can I use this for real-time preview?**
A: Yes. With sub-100ms response times, it works well for live Markdown preview in editors and CMS platforms.

## Pricing

| Plan | Price | Requests/mo | Rate Limit |
|------|-------|-------------|------------|
| Basic (FREE) | $0 | 500 | 1 req/sec |
| Pro | $5.99 | 50,000 | 10 req/sec |

## Alternative To

A free alternative to Showdown.js API, Marked API, and Pandoc API. The only REST API with bidirectional conversion, auto TOC, and syntax highlighting built in.

## Keywords

`markdown to html api`, `html to markdown`, `markdown converter`, `gfm api`, `markdown parser api`, `free markdown api`, `toc generator`, `syntax highlighting api`, `markdown render api`, `text conversion api`
