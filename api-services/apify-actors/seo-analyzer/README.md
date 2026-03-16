# SEO Analyzer

Comprehensive SEO analysis for any webpage. Extracts 15+ SEO factors and calculates an overall score out of 100.

## Features

- **Title & Meta Description** — Length check, optimal range validation
- **Heading Structure** — H1-H6 hierarchy analysis
- **Image Audit** — Alt text coverage
- **Link Analysis** — Internal/external/nofollow breakdown
- **Open Graph & Twitter Cards** — Social sharing metadata
- **JSON-LD Structured Data** — Schema.org detection
- **Technical SEO** — Canonical, robots, viewport, favicon, hreflang, language
- **SEO Score** — Weighted scoring with individual check breakdown

## Input

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `urls` | string[] | Yes | URLs to analyze |
| `analysisType` | string | No | `full` (default), `score`, `headings`, or `links` |

## Output Example

```json
{
  "url": "https://example.com",
  "success": true,
  "pageSize": 12345,
  "title": { "text": "Example", "length": 7, "optimal": false },
  "seoScore": { "score": 72, "maxPoints": 100, "earnedPoints": 72 }
}
```

## Use Cases

- Bulk SEO auditing for large websites
- Competitor SEO analysis
- Content optimization monitoring
- SEO reporting automation

## Pricing

Pay Per Event — charged per URL analyzed.
