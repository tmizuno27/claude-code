# Sitemap Crawler - Free XML Sitemap Extractor & URL Auditor

Extract all URLs from any XML sitemap in seconds -- including nested sitemap index files. Auto-discovers sitemaps via /sitemap.xml and robots.txt. Optionally checks HTTP status codes for each URL to find broken pages and redirects. The best free alternative to Screaming Frog's sitemap mode, Sitebulb, and paid XML sitemap parsers.

## Who Is This For?

- **SEO specialists** -- Extract full URL lists for bulk on-page audits, redirect mapping, and content inventories
- **Web developers** -- Find 404s and broken links before or after site migrations
- **Content strategists** -- Get a complete content inventory of any website instantly
- **Digital agencies** -- Audit client sitemaps as part of technical SEO onboarding
- **Indexing specialists** -- Verify sitemap coverage and submit extracted URLs to Google Indexing API
- **Data analysts** -- Build URL datasets from competitor websites for pattern analysis
- **Site migration teams** -- Map all existing URLs before platform migrations to plan redirects

## Features

- **Sitemap Index Support** -- Automatically processes nested sitemap indexes and fetches all child sitemaps recursively (up to 5 levels deep)
- **Auto-Discovery** -- No sitemap URL? Provide the website root and the Actor finds sitemaps via /sitemap.xml and robots.txt
- **HTTP Status Checking** -- Optional HEAD request per URL to check 200/301/404/500 status without downloading full pages
- **URL Filtering** -- Regex pattern filter to extract only matching URLs (e.g., only `/blog/` or `/product/` paths)
- **All Sitemap Fields** -- Extracts `url`, `lastmod`, `changefreq`, and `priority` from sitemap XML
- **Max URL Limit** -- Cap extraction at a specific count for large sitemaps
- **Error Resilient** -- Failed child sitemaps are logged and skipped; processing continues for remaining sitemaps

## Pricing -- Free to Start

| Tier | Cost | What You Get |
|------|------|-------------|
| **Free trial** | $0 | Apify free tier includes monthly compute credits |
| **Pay per run** | ~$0.01-0.10/run | Full sitemap extraction |
| **vs. Screaming Frog** | Saves $259/yr | Cloud-based, no desktop install needed |
| **vs. Sitebulb** | Saves $152/yr | URL extraction without full crawl cost |
| **vs. ContentKing** | Saves $99-999/mo | Lightweight sitemap extraction only |

## Quick Start (3 Steps)

1. **Click "Try for free"** on this Actor's page in Apify Store
2. **Enter your sitemap URL(s)** or just the website root for auto-discovery
3. **Click "Start"** and download your complete URL list as JSON, CSV, or Excel

## Input

| Field | Type | Default | Description |
|-------|------|---------|-------------|
| `sitemapUrls` | string[] | `[]` | One or more sitemap XML URLs to process |
| `websiteUrl` | string | null | Website root for auto-discovery (used if `sitemapUrls` is empty) |
| `checkHttpStatus` | boolean | `false` | HEAD-check each URL for HTTP status codes |
| `filterPattern` | string | null | Regex filter -- only include matching URLs |
| `maxUrls` | integer | `0` | Max URLs to extract (0 = unlimited) |
| `outputFormat` | string | `"full"` | `"full"` (all fields) or `"urls-only"` (just URL strings) |

### Example Input -- Simple Sitemap Extraction

```json
{
  "sitemapUrls": ["https://example.com/sitemap.xml"],
  "outputFormat": "full"
}
```

### Example Input -- Auto-Discovery

```json
{
  "websiteUrl": "https://example.com",
  "outputFormat": "full"
}
```

### Example Input -- Blog URLs Only with Status Check

```json
{
  "sitemapUrls": ["https://example.com/sitemap.xml"],
  "filterPattern": "/blog/",
  "checkHttpStatus": true,
  "outputFormat": "full"
}
```

### Example Input -- Large Site (Limited Extraction)

```json
{
  "sitemapUrls": [
    "https://bigsite.com/sitemap_index.xml"
  ],
  "maxUrls": 500,
  "outputFormat": "full"
}
```

## Output Example

### Full Format

```json
{
  "url": "https://example.com/blog/how-to-learn-seo/",
  "lastmod": "2026-02-15",
  "changefreq": "monthly",
  "priority": 0.8,
  "sitemapSource": "https://example.com/sitemap-posts.xml",
  "httpStatus": 200
}
```

### URLs Only Format

```json
{
  "url": "https://example.com/blog/how-to-learn-seo/"
}
```

### Error Record (when a child sitemap fails)

```json
{
  "type": "error",
  "sitemapUrl": "https://example.com/broken-sitemap.xml",
  "error": "HTTP 404"
}
```

## Real-World Use Cases

### 1. Pre-Migration URL Inventory
Before migrating from WordPress to a new platform, extract all URLs from your sitemap to create a complete redirect mapping plan. Ensures no page is left without a 301 redirect.

### 2. Bulk SEO Audit with SEO Analyzer
Extract all URLs with this Actor, then pipe them into the **SEO Analyzer** Actor to audit every page in your sitemap. Get a scored SEO report for your entire site in one workflow.

### 3. Broken Link Detection
Run with `checkHttpStatus: true` to find all URLs returning 404, 500, or redirect chains (301/302) in your sitemap. Fix broken links before Google crawls them.

### 4. Content Inventory Building
Export the complete URL list to a spreadsheet. Add metadata like page type, content category, and word count manually or via SEO Analyzer integration.

### 5. Competitor Content Analysis
Extract a competitor's complete sitemap to understand their content structure, publishing frequency (from `lastmod` dates), content priorities, and URL taxonomy.

### 6. Google Indexing API Submission
Extract URLs from your sitemap, filter for recently published or updated pages (using `lastmod`), and submit them to Google Indexing API via a downstream automation to accelerate indexing.

### 7. Automated Sitemap Monitoring
Schedule daily runs to track when new URLs appear in your sitemap. Connect to Slack to get notifications when competitors publish new content.

## FAQ

**Q: What if the site has a sitemap index with many child sitemaps?**
A: The Actor recursively processes all child sitemaps automatically, up to 5 levels of nesting. All URLs from all child sitemaps are combined into a single dataset.

**Q: How does auto-discovery work?**
A: When `websiteUrl` is set, the Actor tries `/sitemap.xml` and `/sitemap_index.xml` directly, then parses `robots.txt` for `Sitemap:` directives. All discovered sitemaps are processed.

**Q: What happens if a child sitemap returns 404?**
A: Failed sitemaps are logged as an error record in the dataset and processing continues with the remaining sitemaps. You won't lose data from successful sitemaps.

**Q: Is `checkHttpStatus` slow?**
A: Yes, for large sitemaps. It sends a HEAD request per URL -- for a 10,000 URL sitemap at 100ms per request, expect ~17 minutes. Use it selectively with `filterPattern` to check specific URL subsets.

**Q: Can I extract compressed sitemaps (.xml.gz)?**
A: Compressed sitemaps are not yet supported. Most modern servers serve decompressed XML -- if your sitemap is gzip-compressed, the Actor may not parse it correctly.

**Q: Can I use this with multiple sitemaps at once?**
A: Yes. Provide multiple URLs in `sitemapUrls`. All are processed sequentially and results are combined into one dataset.

## Tags

`sitemap`, `xml sitemap`, `url extractor`, `seo audit`, `technical seo`, `broken links`, `url crawler`, `site migration`, `content inventory`, `seo tools`
