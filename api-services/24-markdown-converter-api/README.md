# Free Markdown Converter API - HTML to Markdown, GFM, TOC, Syntax Highlight

> **Free tier: 500 requests/month** | Bidirectional Markdown/HTML conversion with full GFM support

Convert Markdown to HTML and HTML back to Markdown. Supports GitHub Flavored Markdown (GFM), auto-generated Table of Contents, syntax highlighting for code blocks, and tables.

## Why Choose This Markdown Converter API?

- **Bidirectional** -- Markdown to HTML and HTML to Markdown
- **GFM support** -- tables, task lists, strikethrough, autolinks
- **Table of Contents** -- auto-generate TOC from headings
- **Syntax highlighting** -- code block highlighting for 100+ languages
- **Sanitized output** -- XSS-safe HTML output
- **Free tier** -- 500 requests/month at $0

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

url = "https://markdown-converter-api.p.rapidapi.com/to-html"
headers = {"X-RapidAPI-Key": "YOUR_KEY", "X-RapidAPI-Host": "markdown-converter-api.p.rapidapi.com"}
payload = {"markdown": "# My Document\n\n- Item 1\n- Item 2", "toc": True}

data = requests.post(url, headers=headers, json=payload).json()
print(data["html"])
```

## Pricing

| Plan | Price | Requests/mo | Rate Limit |
|------|-------|-------------|------------|
| Basic (FREE) | $0 | 500 | 1 req/sec |
| Pro | $5.99 | 50,000 | 10 req/sec |

## Alternative To

A free alternative to Showdown.js API, Marked API, and Pandoc API.

## Keywords

`markdown to html api`, `html to markdown`, `markdown converter`, `gfm api`, `markdown parser api`, `free markdown api`, `toc generator`, `syntax highlighting api`, `markdown render api`, `text conversion api`
