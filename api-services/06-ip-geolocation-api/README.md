# Free IP Geolocation API - Country, City, VPN Detection, Bulk Lookup

> **Free tier: 500 requests/month** | VPN detection + bulk lookups + 15 data fields per IP

Look up any IP address to get country, city, region, timezone, ISP, and VPN/proxy/datacenter detection. Supports single IP lookup, own-IP detection, and bulk lookups (up to 20 IPs). Powered by Cloudflare Workers with 24-hour caching.

## Getting Started in 30 Seconds

1. Subscribe on [RapidAPI](https://rapidapi.com/miccho27-5OJaGGbBiO/api/ip-geolocation-api) (free plan available)
2. Copy your API key
3. Look up any IP:

```bash
curl "https://ip-geolocation-api.p.rapidapi.com/lookup?ip=8.8.8.8" \
  -H "X-RapidAPI-Key: YOUR_KEY" \
  -H "X-RapidAPI-Host: ip-geolocation-api.p.rapidapi.com"
```

## How It Compares

| Feature | This API | ipinfo.io | ipstack | ip-api.com |
|---------|----------|-----------|---------|------------|
| Free tier | 500 req/mo | 50K req/mo | 100 req/mo | 45 req/min (no HTTPS) |
| HTTPS on free | Yes | Yes | No | No |
| VPN detection | Yes | Paid add-on ($99/mo) | Paid add-on | No |
| Bulk lookup | 20 IPs/request | 1,000 (paid) | 1 per request | 100/batch |
| Price (paid) | $5.99/mo | $99/mo | $9.99/mo | $13/mo |
| Own-IP endpoint | /me (zero-cost) | Yes | Yes | Yes |
| Edge caching | 24h (CF Workers) | No | No | No |

## Why Choose This IP Geolocation API?

- **VPN and proxy detection** -- identify VPN, proxy, and datacenter IPs for fraud prevention
- **Rich data** -- country, city, region, lat/long, timezone, ISP, currency, languages
- **Own-IP endpoint** -- `/me` returns caller's geolocation using Cloudflare's free `request.cf` (zero external calls)
- **Bulk lookups** -- query up to 20 IPs in a single request
- **24-hour caching** -- repeat lookups served from Cloudflare edge cache, minimizing latency
- **Free tier** -- 500 requests/month at $0

## Use Cases

- **Fraud detection** -- flag VPN/proxy/datacenter IPs in payment flows
- **Content localization** -- serve region-specific content, currency, and language
- **Ad targeting** -- geo-target ads based on visitor location
- **Analytics enrichment** -- add geographic data to your event logs and dashboards
- **Access control** -- restrict content by country or region (geo-fencing)
- **Compliance** -- verify user location for GDPR, gambling, or financial regulations
- **Cybersecurity** -- monitor login locations and detect suspicious access patterns

## Quick Start

### Look Up Your Own IP

```bash
curl -X GET "https://ip-geolocation-api.t-mizuno27.workers.dev/me" \
  -H "X-RapidAPI-Key: YOUR_KEY"
```

### Look Up a Specific IP

```bash
curl -X GET "https://ip-geolocation-api.t-mizuno27.workers.dev/lookup?ip=8.8.8.8" \
  -H "X-RapidAPI-Key: YOUR_KEY"
```

**Response:**
```json
{
  "ip": "8.8.8.8",
  "country": "US",
  "country_name": "United States",
  "region": "California",
  "city": "Mountain View",
  "latitude": 37.386,
  "longitude": -122.0838,
  "timezone": "America/Los_Angeles",
  "isp": "Google LLC",
  "is_vpn": false,
  "is_proxy": false,
  "is_datacenter": true,
  "currency": "USD",
  "languages": "en"
}
```

### Bulk Lookup (up to 20 IPs)

```bash
curl -X POST "https://ip-geolocation-api.t-mizuno27.workers.dev/lookup/bulk" \
  -H "Content-Type: application/json" \
  -H "X-RapidAPI-Key: YOUR_KEY" \
  -d '{"ips": ["8.8.8.8", "1.1.1.1", "104.16.0.1"]}'
```

### Python Example

```python
import requests

url = "https://ip-geolocation-api.p.rapidapi.com/lookup"
params = {"ip": "8.8.8.8"}
headers = {
    "X-RapidAPI-Key": "YOUR_KEY",
    "X-RapidAPI-Host": "ip-geolocation-api.p.rapidapi.com"
}

response = requests.get(url, headers=headers, params=params)
data = response.json()
print(f"{data['city']}, {data['country_name']} | VPN: {data['is_vpn']}")
```

### Node.js Example

```javascript
const axios = require("axios");

const { data } = await axios.get(
  "https://ip-geolocation-api.p.rapidapi.com/lookup",
  {
    params: { ip: "8.8.8.8" },
    headers: {
      "X-RapidAPI-Key": "YOUR_KEY",
      "X-RapidAPI-Host": "ip-geolocation-api.p.rapidapi.com",
    },
  }
);

console.log(`${data.city}, ${data.country_name}`);
```

## API Reference

### `GET /me`
Returns geolocation for the caller's IP. Uses Cloudflare's built-in `request.cf` data (zero external API calls).

### `GET /lookup?ip={ip}`
Look up geolocation for any IPv4 address. Uses ip-api.com with 24-hour caching.

### `POST /lookup/bulk`
Batch lookup up to 20 IPs. Body: `{"ips": ["8.8.8.8", "1.1.1.1"]}`

## Response Fields

| Field | Description |
|-------|-------------|
| `ip` | Queried IP address |
| `country` | ISO 3166-1 alpha-2 country code |
| `country_name` | Full country name |
| `region` | State/province |
| `city` | City name |
| `latitude` / `longitude` | Geographic coordinates |
| `timezone` | IANA timezone (e.g., America/Los_Angeles) |
| `isp` | Internet Service Provider |
| `is_vpn` | VPN connection detected |
| `is_proxy` | Proxy detected |
| `is_datacenter` | Datacenter IP (not residential) |
| `currency` | Local currency code |
| `languages` | Spoken languages |

## Pricing

| Plan | Price | Requests/mo | Rate Limit |
|------|-------|-------------|------------|
| Basic (FREE) | $0 | 500 | 1 req/sec |
| Pro | $5.99 | 50,000 | 10 req/sec |
| Ultra | $14.99 | 500,000 | 50 req/sec |

## FAQ

**Q: How accurate is the geolocation data?**
A: City-level accuracy is typically 80-90% for fixed-line IPs. Mobile and VPN IPs may resolve to ISP headquarters. Country-level accuracy is 99%+.

**Q: How does VPN/proxy detection work?**
A: The `is_datacenter` field uses ISP name pattern matching against known cloud/hosting providers. The `is_vpn` and `is_proxy` fields use the upstream data source's classification.

**Q: What happens when I hit the rate limit?**
A: You receive a 429 status code with a retry-after header. Upgrade to Pro for 10x the rate limit.

**Q: Can I look up IPv6 addresses?**
A: Yes. Both IPv4 and IPv6 are supported on the /lookup endpoint.

**Q: What's the /me endpoint for?**
A: It returns the geolocation of the caller's IP using Cloudflare's built-in request.cf data -- zero external API calls, making it the fastest endpoint.

## Alternative To

A free alternative to ipinfo.io ($99/mo for VPN detection), ipstack, and ip-api.com Pro. Get VPN detection, bulk lookups, and rich geolocation data at a fraction of the cost.

## Keywords

`ip geolocation api`, `ip lookup`, `geoip`, `ip to location`, `vpn detection api`, `proxy detection`, `ip address api`, `geolocation rest api`, `free ip api`, `bulk ip lookup`, `ipinfo alternative`, `ip geolocation free`, `ip to country api`

## Development

```bash
npm install
npm run dev      # Local development
npm run deploy   # Deploy to Cloudflare
```
