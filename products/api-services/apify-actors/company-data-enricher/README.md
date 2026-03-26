# Company Data Enricher - Free B2B Lead Enrichment from Public Sources

Enrich company data by domain name, company name, or Wikidata ID using only free public sources -- zero API keys, zero monthly fees. The best free alternative to Clearbit Enrichment, ZoomInfo, Apollo.io, and FullContact for startups, sales teams, and growth hackers.

## Who Is This For?

- **Sales & SDR teams** -- Enrich inbound leads with company info before outreach
- **Growth hackers** -- Build prospect lists with tech stack and social data
- **Market researchers** -- Analyze competitor technology choices at scale
- **Recruiters** -- Identify company size, industry, and HQ location instantly
- **Data analysts** -- Bulk company data collection for market intelligence

## Features

- **Domain Enrichment** -- Website metadata, OG tags, social profile links (LinkedIn, Twitter, GitHub), email/phone contacts, technology stack detection (28 technologies), and RDAP domain registration info
- **Company Search** -- Search companies by name via Wikidata (founded date, HQ, CEO, industry, employee count)
- **Wikidata Lookup** -- Retrieve structured company data by Wikidata entity ID
- **Bulk Processing** -- Enrich hundreds of companies in a single Actor run
- **Zero Configuration** -- No API keys, no developer accounts, no signup required

## Pricing -- Free to Start

| Tier | Cost | What You Get |
|------|------|-------------|
| **Free trial** | $0 | Apify free tier includes monthly compute credits |
| **Pay per run** | ~$0.01-0.05/company | Only pay for actual Apify compute used |
| **vs. Clearbit** | Saves $99-999/mo | Same core data from public sources |
| **vs. ZoomInfo** | Saves $15,000+/yr | No enterprise contract needed |

## Quick Start (3 Steps)

1. **Click "Try for free"** on this Actor's page in Apify Store
2. **Enter company domains** (e.g., `stripe.com`, `shopify.com`) or company names to search
3. **Click "Start"** and download enriched company data as JSON, CSV, or Excel

## Input

| Field | Type | Description |
|-------|------|-------------|
| `domains` | string[] | Company domains to enrich (e.g. `stripe.com`) |
| `queries` | string[] | Company name search queries (e.g. `Google`) |
| `wikidataIds` | string[] | Wikidata entity IDs (e.g. `Q95` for Google) |
| `mode` | string | `enrich` (default) for full enrichment or `domain` for basic metadata + RDAP |
| `delayMs` | integer | Delay between requests in ms (default: `1000`) |

At least one of `domains`, `queries`, or `wikidataIds` must be provided.

### Example Input

```json
{
  "domains": ["stripe.com", "shopify.com"],
  "queries": ["Cloudflare"],
  "wikidataIds": ["Q95"],
  "mode": "enrich",
  "delayMs": 1000
}
```

## Output

Results are pushed to the default dataset. Each record includes a `type` field (`enrich`, `domain`, `search`, or `wikidata`) and a `success` boolean.

### Domain Enrichment (`mode: "enrich"`) Output Example

```json
{
  "success": true,
  "type": "enrich",
  "domain": "stripe.com",
  "metadata": {
    "title": "Stripe | Financial Infrastructure to Grow Your Revenue",
    "description": "...",
    "ogTags": { "title": "...", "description": "...", "image": "...", "type": "website", "siteName": "Stripe" }
  },
  "domainInfo": {
    "registrar": "MarkMonitor Inc.",
    "registrationDate": "2009-09-22T00:00:00Z",
    "expirationDate": "2026-09-22T00:00:00Z",
    "domainAge": "15 years",
    "nameservers": ["ns1.p07.dynect.net", "..."]
  },
  "socialLinks": {
    "linkedin": "https://www.linkedin.com/company/stripe",
    "twitter": "https://twitter.com/stripe"
  },
  "technologies": ["React", "Next.js", "Google Tag Manager", "Stripe"],
  "contact": {
    "emails": null,
    "phones": null
  }
}
```

### Search Output Example

```json
{
  "success": true,
  "type": "search",
  "query": "Cloudflare",
  "count": 10,
  "companies": [
    {
      "name": "Cloudflare",
      "description": "American web infrastructure company",
      "wikidataId": "Q61117",
      "wikidataUrl": "https://www.wikidata.org/wiki/Q61117"
    }
  ]
}
```

## Data Sources

| Source | Data Provided |
|--------|-------------|
| **Website HTML** | Title, description, OG tags, social links, contact info, tech stack |
| **RDAP** | Registrar, registration/expiration dates, domain age, nameservers |
| **Wikidata** | Founded date, HQ location, CEO, industry, employee count, revenue |

## Technology Stack Detection

Detects 28 technologies from website HTML: Google Analytics, Google Tag Manager, Facebook Pixel, Shopify, WordPress, React, Next.js, Vue.js, Nuxt.js, Angular, jQuery, Bootstrap, Tailwind CSS, Cloudflare, Stripe, Intercom, HubSpot, Segment, Hotjar, Zendesk, Wix, Squarespace, Webflow, Vercel, Gatsby, Svelte, Drift, and more.

## How It Compares to Paid Alternatives

| Feature | This Actor (FREE) | Clearbit ($99/mo) | ZoomInfo ($15K/yr) | Apollo.io ($49/mo) |
|---------|-------------------|-------------------|-------------------|-------------------|
| Domain enrichment | Yes | Yes | Yes | Yes |
| Tech stack detection | 28 technologies | 100+ | Limited | No |
| Social profiles | Yes | Yes | Yes | Yes |
| Domain WHOIS/RDAP | Yes | No | No | No |
| Company search | Yes (Wikidata) | Yes | Yes | Yes |
| API keys required | None | Yes | Yes | Yes |
| Bulk processing | Unlimited | Rate limited | Rate limited | Rate limited |
| Monthly cost | $0 (pay per run) | $99-999 | $15,000+ | $49-99 |

## Real-World Use Cases

### 1. Sales Lead Enrichment Pipeline
Upload a CSV of prospect domains, run this Actor on a schedule, and get enriched company data pushed to your CRM via Apify integrations (Zapier, Make, webhook).

### 2. Competitive Tech Stack Analysis
Input your competitors' domains to discover what frameworks, analytics tools, and marketing tech they use. Track changes over time with scheduled runs.

### 3. Domain Due Diligence
Before acquiring a domain or partnering with a company, check domain age, registration history, and technology footprint in seconds.

### 4. Market Research at Scale
Enrich hundreds of companies in a vertical to identify technology trends, common social platforms, and company characteristics for market reports.

## FAQ

**Q: How does this compare to Clearbit?**
A: Clearbit has richer proprietary data (employee count, revenue estimates) but costs $99+/mo. This Actor uses free public sources (RDAP, Wikidata, HTML parsing), making it ideal for startups, bootstrapped businesses, and small-scale enrichment needs. For most lead qualification tasks, the data quality is comparable.

**Q: What data sources are used?**
A: Website HTML (direct fetch), IANA RDAP (domain registration), and Wikidata (company metadata). No paid APIs are called, so you never get surprise bills.

**Q: Can I run this on a schedule?**
A: Yes. Use Apify's built-in scheduler to enrich new leads automatically on a daily or weekly basis. Combine with webhooks to push results to your CRM, Google Sheets, or Slack.

**Q: How accurate is the technology detection?**
A: Very accurate for client-side technologies (React, Vue, jQuery, analytics scripts). Server-side technologies are detected via response headers and meta tags when available.

**Q: Can I use the Apify API to call this programmatically?**
A: Yes. Use the Apify API or any of the official SDKs (Python, JavaScript, Go) to trigger runs and retrieve results. Perfect for building automated enrichment pipelines.

## Notes

- Domains in the `domains` array are automatically normalized (strips `https://` and paths)
- Tech detection only runs in `enrich` mode
- Failed items are still pushed to the dataset with `success: false` and an `error` field
