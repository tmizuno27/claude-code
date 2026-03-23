# Company Data Enricher - Free B2B Data from Public Sources

An Apify Actor that enriches company data from domains and company names using only free public sources -- no API keys required. A free alternative to Clearbit Enrichment, ZoomInfo, and FullContact.

## Features

- **Domain Enrichment** — Website metadata, OG tags, social profile links, email/phone contacts, technology stack detection, and RDAP domain registration info
- **Company Search** — Search companies by name via Wikidata
- **Wikidata Lookup** — Retrieve structured company data (founded, HQ, CEO, industry, employees) by Wikidata entity ID

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

- **Website HTML** — Fetched directly from the target domain
- **RDAP** — IANA RDAP bootstrap + registry RDAP servers (domain registration data)
- **Wikidata** — Free public knowledge graph API

## Technology Detection

Detects 28 technologies including: Google Analytics, Google Tag Manager, Facebook Pixel, Shopify, WordPress, React, Next.js, Vue.js, Nuxt.js, Angular, jQuery, Bootstrap, Tailwind CSS, Cloudflare, Stripe, Intercom, HubSpot, Segment, Hotjar, Zendesk, Wix, Squarespace, Webflow, Vercel, Gatsby, Svelte, Drift.

## Why Choose This Actor?

- **Zero API keys** -- uses only RDAP, Wikidata, and public HTML parsing
- **3 enrichment modes** -- domain enrichment, company search, Wikidata lookup
- **Tech stack detection** -- identifies 28 technologies from website HTML
- **Social profiles** -- extracts LinkedIn, Twitter, and other social links
- **Bulk processing** -- enrich dozens of companies in one Actor run

## FAQ

**Q: How does this compare to Clearbit?**
A: Clearbit has richer proprietary data but costs $99+/mo. This Actor uses free public sources, making it ideal for startups and small-scale enrichment needs.

**Q: What data sources are used?**
A: Website HTML (direct fetch), IANA RDAP (domain registration), and Wikidata (company metadata). No paid APIs are called.

**Q: Can I run this on a schedule?**
A: Yes. Use Apify's scheduler to enrich new leads automatically on a daily or weekly basis.

## Notes

- Domains in the `domains` array are automatically normalized (strips `https://` and paths)
- Tech detection only runs in `enrich` mode
- Failed items are still pushed to the dataset with `success: false` and an `error` field
