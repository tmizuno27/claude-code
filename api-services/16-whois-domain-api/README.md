# WHOIS Domain API

Domain WHOIS/RDAP lookup and DNS query API powered by Cloudflare Workers.

Uses the free **RDAP** (Registration Data Access Protocol) for domain registration data and **Cloudflare DoH** for DNS record queries. No API keys required.

## Endpoints

| Method | Path | Description |
|--------|------|-------------|
| GET | `/` | API info |
| GET | `/lookup?domain=example.com` | Full RDAP/WHOIS lookup (registrar, dates, nameservers, DNSSEC) |
| GET | `/dns?domain=example.com` | DNS records (A, AAAA, MX, NS, TXT, CNAME) |
| GET | `/availability?domain=example.com` | Check if domain is available |
| GET | `/tld-list` | List all RDAP-supported TLDs |

## How It Works

### RDAP Lookup Flow
1. Extract TLD from domain (e.g., `com` from `example.com`)
2. Fetch IANA RDAP bootstrap (`https://data.iana.org/rdap/dns.json`) to find the RDAP server for that TLD
3. Query `{rdap_server}/domain/{domain}`
4. Parse response for registration info, registrar, nameservers, DNSSEC

### DNS Lookup
Queries Cloudflare DoH (`https://cloudflare-dns.com/dns-query`) with `Accept: application/dns-json` for each record type.

## Rate Limiting

20 requests per minute per IP. Size-based cleanup (no timers).

## Caching

| Data | TTL |
|------|-----|
| RDAP responses | 3600s (1 hour) |
| DNS responses | 300s (5 minutes) |
| IANA bootstrap | 86400s (24 hours) |

## Setup

```bash
npm install
npm run dev      # local development
npm run deploy   # deploy to Cloudflare Workers
```

## Example Response

### GET /lookup?domain=example.com

```json
{
  "domain": "example.com",
  "status": ["client delete prohibited", "client transfer prohibited"],
  "registered": "1995-08-14T04:00:00Z",
  "expires": "2025-08-13T04:00:00Z",
  "lastUpdated": "2024-08-14T07:01:44Z",
  "registrar": {
    "name": "RESERVED-Internet Assigned Numbers Authority",
    "url": null,
    "ianaId": "376"
  },
  "nameservers": ["a.iana-servers.net", "b.iana-servers.net"],
  "dnssec": "signed"
}
```
