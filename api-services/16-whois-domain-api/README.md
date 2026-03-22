# Free WHOIS Domain API - Domain Lookup, DNS Records, RDAP

> **Free tier: 500 requests/month** | WHOIS/RDAP domain lookup and DNS queries via Cloudflare DoH

Look up domain registration data (registrar, creation date, expiration, nameservers) via RDAP protocol and query DNS records (A, AAAA, MX, TXT, CNAME, NS) via Cloudflare DNS over HTTPS. No external API keys required.

## Why Choose This WHOIS API?

- **RDAP protocol** -- modern replacement for WHOIS with structured JSON responses
- **DNS queries** -- A, AAAA, MX, TXT, CNAME, NS records via Cloudflare DoH
- **No upstream keys** -- uses free RDAP and Cloudflare DNS, zero external costs
- **Domain availability** -- check if a domain is registered
- **SSL info** -- certificate expiration and issuer details
- **Free tier** -- 500 requests/month at $0

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

## Pricing

| Plan | Price | Requests/mo | Rate Limit |
|------|-------|-------------|------------|
| Basic (FREE) | $0 | 500 | 1 req/sec |
| Pro | $5.99 | 50,000 | 10 req/sec |

## Alternative To

A free alternative to WhoisXML API, DomainTools, and SecurityTrails.

## Keywords

`whois api`, `domain lookup api`, `rdap api`, `dns records api`, `domain info`, `domain availability`, `free whois api`, `nameserver lookup`, `ssl check api`, `domain registration api`
