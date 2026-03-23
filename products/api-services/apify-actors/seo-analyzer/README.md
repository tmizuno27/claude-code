# SEO Analyzer - Free Website SEO Audit & Scoring Tool

Run a comprehensive SEO audit on any webpage and get a weighted score out of 100. Checks 15+ on-page SEO factors including title tags, meta descriptions, heading structure, image alt text, internal/external links, Open Graph, Twitter Cards, JSON-LD structured data, and technical SEO. The best free alternative to Ahrefs Site Audit, Screaming Frog, Moz Pro, and Sitebulb.

## Who Is This For?

- **SEO specialists & agencies** -- Bulk audit client websites before and after optimization
- **Content marketers** -- Verify on-page SEO before publishing new pages
- **Web developers** -- SEO regression testing in CI/CD pipelines before deployments
- **E-commerce managers** -- Audit product pages for missing meta tags and structured data
- **Freelancers** -- Generate SEO audit reports for prospective clients in minutes
- **Site owners** -- Monitor SEO health across all pages with scheduled runs

## Features

- **Title & Meta Description** -- Length check, optimal range validation (50-60 chars title, 150-160 chars description)
- **Heading Structure** -- H1-H6 hierarchy analysis, missing H1 detection
- **Image Audit** -- Alt text coverage percentage across all images
- **Link Analysis** -- Internal/external/nofollow breakdown with counts
- **Open Graph & Twitter Cards** -- Social sharing metadata completeness check
- **JSON-LD Structured Data** -- Schema.org detection and validation
- **Technical SEO** -- Canonical URL, robots meta, viewport, favicon, hreflang, language attribute
- **SEO Score** -- Weighted 0-100 scoring with individual check breakdown

## Pricing -- Free to Start

| Tier | Cost | What You Get |
|------|------|-------------|
| **Free trial** | $0 | Apify free tier includes monthly compute credits |
| **Pay per URL** | ~$0.01-0.10/URL | Only pay for actual Apify compute used |
| **vs. Ahrefs** | Saves $99-999/mo | Same on-page checks, no subscription |
| **vs. Screaming Frog** | Saves $259/yr | Cloud-based, no desktop install needed |
| **vs. Moz Pro** | Saves $99-599/mo | More detailed on-page analysis |

## How It Compares to Paid SEO Audit Tools

| Feature | This Actor (FREE) | Ahrefs Site Audit ($99/mo) | Screaming Frog ($259/yr) | Moz Pro ($99/mo) | Sitebulb ($152/yr) |
|---------|-------------------|---------------------------|-------------------------|------------------|-------------------|
| SEO Score (0-100) | Yes (weighted) | Yes | No (raw data only) | Yes | Yes |
| Title/meta check | Yes | Yes | Yes | Yes | Yes |
| Heading structure | Yes | Yes | Yes | Yes | Yes |
| Image alt audit | Yes | Yes | Yes | Yes | Yes |
| JSON-LD detection | Yes | Yes | Yes | No | Yes |
| Open Graph check | Yes | No | No | No | Yes |
| Twitter Cards check | Yes | No | No | No | No |
| API/automation | Yes (Apify API) | Yes | Limited | Yes | No |
| CI/CD integration | Yes (webhook/API) | No | No | No | No |
| Bulk URLs | Unlimited | Site-based | 500 free | Site-based | Site-based |
| Cloud-based | Yes | Yes | Desktop only | Yes | Desktop only |
| Monthly cost | $0 (pay per run) | $99-999 | $259/yr | $99-599 | $152/yr |

## Input

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `urls` | string[] | Yes | URLs to analyze (no limit) |
| `analysisType` | string | No | `full` (default), `score` (score only), `headings` (heading structure), or `links` (link analysis) |

### Example Input

```json
{
  "urls": [
    "https://example.com",
    "https://example.com/about",
    "https://example.com/blog/seo-guide"
  ],
  "analysisType": "full"
}
```

## Output Example

```json
{
  "url": "https://example.com",
  "success": true,
  "pageSize": 12345,
  "title": { "text": "Example Domain", "length": 14, "optimal": false },
  "metaDescription": { "text": "...", "length": 155, "optimal": true },
  "headings": { "h1Count": 1, "h2Count": 5, "h3Count": 8, "hasH1": true },
  "images": { "total": 12, "withAlt": 10, "altCoverage": 83.3 },
  "links": { "internal": 24, "external": 8, "nofollow": 2 },
  "openGraph": { "hasOG": true, "title": "...", "description": "...", "image": "..." },
  "twitterCard": { "hasCard": true, "type": "summary_large_image" },
  "structuredData": { "hasJsonLd": true, "types": ["WebPage", "Organization"] },
  "technical": { "hasCanonical": true, "hasViewport": true, "hasFavicon": true },
  "seoScore": { "score": 72, "maxPoints": 100, "earnedPoints": 72, "checks": [...] }
}
```

## Real-World Use Cases

### 1. Pre-Publication SEO Checklist
Run this Actor on staging URLs before publishing to catch missing meta descriptions, broken heading hierarchy, and missing alt text before going live.

### 2. Bulk Website Migration Audit
Analyzing 500+ pages during a site migration? Run before and after to ensure SEO parity and catch regressions.

### 3. Competitor SEO Benchmarking
Audit competitors' top pages and compare their SEO scores to yours. Identify specific factors where they outperform you.

### 4. Client SEO Audit Report
Freelancers and agencies: run this on a prospect's website, export results as JSON/CSV, and present a professional SEO audit in your sales process.

### 5. CI/CD SEO Regression Testing
Trigger this Actor via API after every deployment. If SEO score drops below a threshold, fail the pipeline and alert the team.

### 6. Monthly SEO Health Monitoring
Schedule weekly/monthly runs across your entire sitemap and track SEO score trends over time in Google Sheets or a dashboard.

## FAQ

**Q: How many URLs can I analyze in one run?**
A: No hard limit. Processing time and cost scale linearly with URL count. Typical runs analyze 10-1,000 URLs. For very large sites (10K+ pages), split into multiple runs.

**Q: What is the SEO score based on?**
A: Weighted scoring across all checks: title optimization (15pts), meta description (10pts), heading structure (10pts), image alt coverage (10pts), link health (10pts), technical SEO (15pts), structured data (10pts), social meta (10pts), and more. Each check has a clear pass/fail with points breakdown.

**Q: Can I use this in CI/CD pipelines?**
A: Yes. Trigger the Actor via Apify API and check results programmatically. Perfect for automated SEO regression testing before deployments. Integrates with GitHub Actions, Jenkins, and any webhook-capable CI system.

**Q: Does this check page speed or Core Web Vitals?**
A: No. This Actor focuses on on-page SEO factors (content, metadata, structure). For performance metrics, use Google PageSpeed Insights or Lighthouse.

**Q: Can I export results to CSV or Google Sheets?**
A: Yes. Apify datasets can be exported as JSON, CSV, Excel, or pushed directly to Google Sheets, Slack, email, or any webhook endpoint.

## Pricing

Pay Per Event -- charged per URL analyzed. Typical cost: $0.01-0.10 per URL depending on page complexity. Free Apify tier available for testing.
