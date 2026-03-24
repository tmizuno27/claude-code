---
title: "Free WHOIS & DNS Lookup API — Build Domain Tools Without Scraping"
published: false
tags: api, dns, webdev, security
cover_image:
---

Building a domain lookup tool? A competitor analysis dashboard? A phishing detection system? You need WHOIS and DNS data, but:

- WHOIS servers rate-limit aggressively
- Parsing WHOIS text responses is a nightmare (every TLD has different formats)
- Most WHOIS APIs charge $50+/month

I built a free API that returns structured JSON for WHOIS lookups, DNS records, and domain availability — all via Cloudflare's DoH (DNS over HTTPS) for reliability.

## Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/whois?domain=` | GET | WHOIS/RDAP lookup with structured JSON output |
| `/dns?domain=&type=` | GET | DNS records (A, AAAA, MX, TXT, NS, CNAME, SOA) |
| `/available?domain=` | GET | Domain availability check |
| `/bulk` | POST | Bulk lookup (up to 10 domains) |

## Quick Example — Domain Investigation

### Python

```python
import requests

headers = {
    "X-RapidAPI-Key": "YOUR_KEY",
    "X-RapidAPI-Host": "whois-domain-api.p.rapidapi.com"
}

# WHOIS lookup
whois = requests.get(
    "https://whois-domain-api.p.rapidapi.com/whois?domain=example.com",
    headers=headers
).json()

print(f"Registrar: {whois['registrar']}")
print(f"Created: {whois['creation_date']}")
print(f"Expires: {whois['expiration_date']}")
print(f"Name Servers: {whois['name_servers']}")

# DNS records
dns = requests.get(
    "https://whois-domain-api.p.rapidapi.com/dns?domain=example.com&type=MX",
    headers=headers
).json()

for record in dns["records"]:
    print(f"MX: {record['value']} (priority: {record['priority']})")
```

### JavaScript — Bulk Domain Check

```javascript
const response = await fetch(
  "https://whois-domain-api.p.rapidapi.com/bulk",
  {
    method: "POST",
    headers: {
      "X-RapidAPI-Key": "YOUR_KEY",
      "X-RapidAPI-Host": "whois-domain-api.p.rapidapi.com",
      "Content-Type": "application/json"
    },
    body: JSON.stringify({
      domains: ["startup.io", "myapp.dev", "coolproject.com"]
    })
  }
);
const results = await response.json();
results.forEach(d => console.log(`${d.domain}: ${d.available ? "Available!" : "Taken"}`));
```

## Real-World Use Cases

1. **Domain Flipping Tool** — Check expiration dates in bulk, find expiring domains
2. **Phishing Detection** — Flag recently registered domains impersonating your brand
3. **Competitor Analysis** — Monitor DNS changes (CDN switches, email provider changes)
4. **DevOps Monitoring** — Alert on SSL cert expiry, DNS propagation verification
5. **Sales Intelligence** — Identify a company's tech stack from DNS/MX records

## How It Compares

| Feature | WHOIS Domain API | WhoisXML API | DomainTools | Whoxy |
|---------|-----------------|--------------|-------------|-------|
| Free tier | 500 req/mo | 500 req/mo | None | 1000 credits |
| JSON output | Yes | Yes | Yes | Yes |
| DNS records | Included | Separate API | Included | No |
| Bulk lookup | 10/request | 1/request | Paid only | Paid |
| Domain availability | Included | Separate | Paid | No |
| Price (paid) | $5.99/mo | $19/mo | $99/mo | $2/1000 |

## Try It Free

1. [WHOIS Domain API on RapidAPI](https://rapidapi.com/miccho27-5OJaGGbBiO/api/whois-domain-api)
2. Subscribe free (500 req/month)
3. Test any domain instantly

---

**What domain analysis features would be most useful?** Let me know in the comments.
