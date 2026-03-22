# Free Company Data API - Business Info from Public Sources

> **Free tier: 500 requests/month** | Company search and enrichment from free public databases

Look up company information including name, industry, size, location, website, and social profiles from free public sources. Useful for CRM enrichment, lead generation, and B2B data needs.

## Why Choose This Company Data API?

- **Public data sources** -- aggregates from free, publicly available business databases
- **Company search** -- find companies by name, domain, or industry
- **Data enrichment** -- enrich your CRM with company details
- **No upstream costs** -- uses only free public data sources
- **Free tier** -- 500 requests/month at $0

## Use Cases

- **CRM enrichment** -- auto-fill company profiles in Salesforce, HubSpot, etc.
- **Lead generation** -- find and qualify B2B leads by industry and size
- **Sales intelligence** -- research prospects before outreach
- **Due diligence** -- verify company details for partnerships or investments
- **Market research** -- analyze companies in specific industries or regions

## Quick Start

```bash
curl -X GET "https://company-data-api.t-mizuno27.workers.dev/search?name=Cloudflare" \
  -H "X-RapidAPI-Key: YOUR_KEY"
```

### Python Example

```python
import requests

url = "https://company-data-api.p.rapidapi.com/search"
params = {"name": "Stripe"}
headers = {"X-RapidAPI-Key": "YOUR_KEY", "X-RapidAPI-Host": "company-data-api.p.rapidapi.com"}

data = requests.get(url, headers=headers, params=params).json()
print(f"{data['name']} | {data['industry']} | {data['location']}")
```

## Pricing

| Plan | Price | Requests/mo | Rate Limit |
|------|-------|-------------|------------|
| Basic (FREE) | $0 | 500 | 1 req/sec |
| Pro | $9.99 | 50,000 | 10 req/sec |

## Alternative To

A free alternative to Clearbit, ZoomInfo, and FullContact company data APIs.

## Keywords

`company data api`, `business info api`, `company search api`, `b2b data api`, `crm enrichment`, `company lookup`, `free company api`, `lead generation api`, `business intelligence api`, `clearbit alternative`
