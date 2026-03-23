# SEO Analyzer - Free Website SEO Audit Tool

Comprehensive SEO analysis for any webpage. Extracts 15+ SEO factors and calculates an overall score out of 100. A free alternative to Ahrefs Site Audit, Screaming Frog, and Moz Pro.

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

## Why Choose This Actor?

- **15+ SEO checks** in a single run -- title, meta, headings, images, links, OG, Twitter Cards, JSON-LD, canonical, robots, viewport, favicon, hreflang
- **Weighted scoring** -- not just pass/fail, but a meaningful 0-100 score
- **Bulk processing** -- analyze hundreds of URLs in one Actor run
- **No API keys** -- runs entirely on Apify, no external service dependencies
- **Free to try** -- pay only for Apify compute usage

## How It Compares

| Feature | This Actor | Ahrefs Site Audit | Screaming Frog | Moz Pro |
|---------|-----------|------------------|----------------|---------|
| Price | Pay per run ($0.01-0.10) | $99/mo | $259/yr | $99/mo |
| SEO Score | Yes (0-100) | Yes | No (raw data) | Yes |
| Heading structure | Yes | Yes | Yes | Yes |
| Image alt audit | Yes | Yes | Yes | Yes |
| JSON-LD detection | Yes | Yes | Yes | No |
| Open Graph check | Yes | No | No | No |
| API/automation | Yes (Apify API) | Yes | Limited | Yes |
| Bulk URLs | Yes (unlimited) | Site-based | 500 free | Site-based |

## FAQ

**Q: How many URLs can I analyze in one run?**
A: No hard limit. Processing time and cost scale linearly with URL count. Typical runs analyze 10-1,000 URLs.

**Q: What is the SEO score based on?**
A: Weighted scoring across all checks: title optimization (15pts), meta description (10pts), heading structure (10pts), image alt coverage (10pts), link health (10pts), technical SEO (15pts), structured data (10pts), social meta (10pts), and more.

**Q: Can I use this in CI/CD pipelines?**
A: Yes. Trigger the Actor via Apify API and check results programmatically. Perfect for automated SEO regression testing before deployments.

## Pricing

Pay Per Event -- charged per URL analyzed.
