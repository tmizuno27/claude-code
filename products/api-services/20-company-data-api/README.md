# Free Company Data API - Business Info from Public Sources

> **Free tier: 500 requests/month** | Company search and enrichment from free public databases

Look up company information including name, industry, size, location, website, and social profiles from free public sources. Useful for CRM enrichment, lead generation, and B2B data needs.

## Getting Started in 30 Seconds

1. Subscribe on [RapidAPI](https://rapidapi.com/miccho27-5OJaGGbBiO/api/company-data-api) (free plan available)
2. Copy your API key
3. Search your first company:

```bash
curl -X GET "https://company-data-api.p.rapidapi.com/search?name=Stripe" \
  -H "X-RapidAPI-Key: YOUR_KEY" \
  -H "X-RapidAPI-Host: company-data-api.p.rapidapi.com"
```

## How It Compares

| Feature | This API | Clearbit | ZoomInfo | FullContact |
|---------|----------|---------|----------|-------------|
| Free tier | 500 req/mo | 50 req/mo | None | 100 req/mo |
| Pro pricing | $9.99/50K | $99/mo | Custom ($10K+/yr) | $99/mo |
| Company search | Yes (name, domain) | Yes | Yes | Yes |
| Domain enrichment | Yes | Yes | Yes | Yes |
| Industry data | Yes | Yes | Yes | Limited |
| Social profiles | Yes | Yes | Yes | Yes |
| No upstream API key | Yes (public sources) | No | No | No |
| B2B data | Yes (basic) | Yes (extensive) | Yes (extensive) | Yes (moderate) |

## Why Choose This Company Data API?

- **Public data sources** -- aggregates from free, publicly available business databases
- **Company search** -- find companies by name, domain, or industry
- **Data enrichment** -- enrich your CRM with company details
- **No upstream costs** -- uses only free public data sources
- **Free tier** -- 500 requests/month at $0

## Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/search` | GET | Search companies by name |
| `/company` | GET | Get detailed company info |
| `/domain` | GET | Look up company by domain |
| `/enrich` | POST | Enrich multiple companies at once |

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

url = "https://company-data-api.p.rapidapi.com/domain"
params = {"domain": "stripe.com"}
headers = {"X-RapidAPI-Key": "YOUR_KEY", "X-RapidAPI-Host": "company-data-api.p.rapidapi.com"}

data = requests.get(url, headers=headers, params=params).json()
print(f"{data['name']} | {data['industry']} | {data['location']}")
```

### Node.js Example

```javascript
const axios = require("axios");

const { data } = await axios.get(
  "https://company-data-api.p.rapidapi.com/search",
  {
    params: { name: "Shopify" },
    headers: {
      "X-RapidAPI-Key": "YOUR_KEY",
      "X-RapidAPI-Host": "company-data-api.p.rapidapi.com",
    },
  }
);

console.log(`${data.name} - ${data.industry} - ${data.employees} employees`);
```

## FAQ

**Q: How does data quality compare to Clearbit or ZoomInfo?**
A: This API uses public sources, so coverage is good for well-known companies but may have gaps for small/private businesses. Clearbit and ZoomInfo have richer proprietary datasets but cost 10-100x more.

**Q: Can I enrich by domain name?**
A: Yes. Use the `/domain` endpoint with a company domain (e.g., `stripe.com`) to get company details.

**Q: What data fields are returned?**
A: Company name, industry, location, website, social profiles (LinkedIn, Twitter), employee count, founding year, and description.

**Q: Is the data real-time?**
A: Data is sourced from public databases and cached. Updates happen periodically. For time-critical data, verify against the company's website.

## Pricing

| Plan | Price | Requests/mo | Rate Limit |
|------|-------|-------------|------------|
| Basic (FREE) | $0 | 500 | 1 req/sec |
| Pro | $9.99 | 50,000 | 10 req/sec |

## Alternative To

A free alternative to Clearbit, ZoomInfo, and FullContact company data APIs. B2B company intelligence without enterprise pricing.


## Also From This Publisher

Build powerful workflows by combining APIs:

| API | Why Combine? |
|-----|-------------|
| **Email Validation API** | Validate company email addresses |
| **IP Geolocation API** | Geo-locate company headquarters |
| **WHOIS Domain API** | Look up company domain registration |
| **Screenshot API** | Capture company website screenshots |

> All APIs include a free tier. Subscribe to one, discover the full toolkit on [our RapidAPI profile](https://rapidapi.com/miccho27-5OJaGGbBiO).

## Keywords

`company data api`, `business info api`, `company search api`, `b2b data api`, `crm enrichment`, `company lookup`, `free company api`, `lead generation api`, `business intelligence api`, `clearbit alternative`
