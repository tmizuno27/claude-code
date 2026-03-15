# Company Data API

Cloudflare Workers API for company/business information from free public sources.

## Data Sources

- **OpenCorporates** (free, no API key) — Company registry search and details
- **RDAP** — Domain registration info (registrar, dates, nameservers)
- **Web scraping** — Website metadata, social links, technology detection, contact info

## Endpoints

| Method | Path | Description |
|--------|------|-------------|
| GET | `/` | API info |
| GET | `/search?q=<name>` | Search companies by name |
| GET | `/company?jurisdiction=<code>&number=<num>` | Get specific company details |
| GET | `/domain?domain=<domain>` | Domain + website info |
| GET | `/enrich?domain=<domain>` | Full enrichment (metadata, tech stack, social, contacts) |

## Examples

```bash
# Search companies
curl "https://company-data-api.YOUR.workers.dev/search?q=Stripe"

# Get company details
curl "https://company-data-api.YOUR.workers.dev/company?jurisdiction=us_de&number=5765218"

# Domain lookup
curl "https://company-data-api.YOUR.workers.dev/domain?domain=stripe.com"

# Full enrichment
curl "https://company-data-api.YOUR.workers.dev/enrich?domain=stripe.com"
```

## Enrichment Output

The `/enrich` endpoint returns:
- Website metadata (title, description, OG tags)
- Domain age and registrar (via RDAP)
- Social media links (LinkedIn, Twitter, Facebook, GitHub, Instagram, YouTube)
- Technology detection (27+ signatures: analytics, frameworks, CMS, payments, etc.)
- Contact info (emails and phone numbers extracted from page)

## Rate Limits

20 requests per minute per IP. Caching: search/company 1 hour, domain/enrich 30 minutes.

## Setup

```bash
npm install
npx wrangler dev    # local development
npx wrangler deploy # deploy to Cloudflare
```
