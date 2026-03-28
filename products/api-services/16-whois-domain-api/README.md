# Free WHOIS Domain API - Domain Lookup, DNS Records, RDAP

> **Free tier: 500 requests/month** | WHOIS/RDAP domain lookup and DNS queries via Cloudflare DoH

Look up domain registration data (registrar, creation date, expiration, nameservers) via RDAP protocol and query DNS records (A, AAAA, MX, TXT, CNAME, NS) via Cloudflare DNS over HTTPS. No external API keys required.

## Getting Started in 30 Seconds

1. Subscribe on [RapidAPI](https://rapidapi.com/miccho27-5OJaGGbBiO/api/whois-domain-api) (free plan available)
2. Copy your API key
3. Look up your first domain:

```bash
curl -X GET "https://whois-domain-api.p.rapidapi.com/lookup?domain=github.com" \
  -H "X-RapidAPI-Key: YOUR_KEY" \
  -H "X-RapidAPI-Host: whois-domain-api.p.rapidapi.com"
```

## How It Compares

| Feature | This API | WhoisXML API | DomainTools | SecurityTrails |
|---------|----------|-------------|-------------|----------------|
| Free tier | 500 req/mo | 500 req/mo | None | 50 req/mo |
| Pro pricing | $5.99/50K | $19/mo | $99/mo | $50/mo |
| WHOIS/RDAP lookup | Yes (RDAP) | Yes | Yes | Yes |
| DNS records | Yes (A, AAAA, MX, TXT, CNAME, NS) | Yes | Yes | Yes |
| Domain availability | Yes | Yes | Yes | No |
| TLD list | Yes | No | No | No |
| No upstream API key | Yes (free RDAP + CF DoH) | No | No | No |
| Edge latency | Sub-100ms (CF Workers) | 200-500ms | 300-800ms | 200-500ms |

## Why Choose This WHOIS API?

- **RDAP protocol** -- modern replacement for WHOIS with structured JSON responses
- **DNS queries** -- A, AAAA, MX, TXT, CNAME, NS records via Cloudflare DoH
- **No upstream keys** -- uses free RDAP and Cloudflare DNS, zero external costs
- **Domain availability** -- check if a domain is registered
- **SSL info** -- certificate expiration and issuer details
- **Free tier** -- 500 requests/month at $0

## Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/lookup` | GET | RDAP domain registration lookup |
| `/dns` | GET | DNS record query (A, AAAA, MX, TXT, etc.) |
| `/availability` | GET | Check if domain is available |
| `/tld-list` | GET | List supported TLDs |

## Use Cases

- **Domain research** -- check registration details, expiration dates, registrar info
- **Cybersecurity** -- investigate suspicious domains, check DNS configurations
- **SEO tools** -- verify domain age and authority signals
- **Brand protection** -- monitor domain registrations for trademark infringement
- **DevOps** -- verify DNS propagation and record configuration
- **Domain investing** -- research domain history and expiration dates

## Quick Start

```bash
curl -X GET "https://whois-domain-api.t-mizuno27.workers.dev/lookup?domain=example.com" \
  -H "X-RapidAPI-Key: YOUR_KEY"
```

### Python Example

```python
import requests

url = "https://whois-domain-api.p.rapidapi.com/lookup"
params = {"domain": "github.com"}
headers = {"X-RapidAPI-Key": "YOUR_KEY", "X-RapidAPI-Host": "whois-domain-api.p.rapidapi.com"}

data = requests.get(url, headers=headers, params=params).json()
print(f"Registrar: {data['registrar']} | Expires: {data['expiration_date']}")
```

### Node.js Example

```javascript
const axios = require("axios");

const { data } = await axios.get(
  "https://whois-domain-api.p.rapidapi.com/dns",
  {
    params: { domain: "github.com", type: "MX" },
    headers: {
      "X-RapidAPI-Key": "YOUR_KEY",
      "X-RapidAPI-Host": "whois-domain-api.p.rapidapi.com",
    },
  }
);

console.log(`MX Records: ${JSON.stringify(data.records)}`);
```

## FAQ

**Q: What is RDAP?**
A: Registration Data Access Protocol is the modern successor to WHOIS. It returns structured JSON instead of free-text, making it easier to parse programmatically.

**Q: Can I check if a domain is available for purchase?**
A: Yes. Use the `/availability` endpoint. It checks RDAP and returns whether the domain is registered or available.

**Q: What DNS record types are supported?**
A: A, AAAA, MX, TXT, CNAME, NS, and SOA records via Cloudflare's DNS over HTTPS service.

**Q: Is WHOIS data always available?**
A: Most gTLDs (.com, .net, .org) have full RDAP coverage. Some ccTLDs may have limited data due to registry policies or privacy regulations (GDPR).

## Pricing

| Plan | Price | Requests/mo | Rate Limit |
|------|-------|-------------|------------|
| Basic (FREE) | $0 | 500 | 1 req/sec |
| Pro | $5.99 | 50,000 | 10 req/sec |

## Alternative To

A free alternative to WhoisXML API, DomainTools, and SecurityTrails. Modern RDAP protocol with DNS queries, no upstream API costs.


## Also From This Publisher

Build powerful workflows by combining APIs:

| API | Why Combine? |
|-----|-------------|
| **SEO Analyzer API** | Full SEO audit after domain lookup |
| **Link Preview API** | Extract metadata for discovered domains |
| **Screenshot API** | Capture screenshots of looked-up domains |
| **Email Validation API** | Validate emails on discovered domains |

> All APIs include a free tier. Subscribe to one, discover the full toolkit on [our RapidAPI profile](https://rapidapi.com/miccho27-5OJaGGbBiO).

## Keywords

`whois api`, `domain lookup api`, `rdap api`, `dns records api`, `domain info`, `domain availability`, `free whois api`, `nameserver lookup`, `ssl check api`, `domain registration api`
