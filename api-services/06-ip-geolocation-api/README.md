# Free IP Geolocation API - Country, City, VPN Detection, Bulk Lookup

> **Free tier: 500 requests/month** | Your only subscriber-proven API -- already generating $9.99/mo revenue

Look up any IP address to get country, city, region, timezone, ISP, and VPN/proxy/datacenter detection. Supports single IP lookup, own-IP detection, and bulk lookups (up to 20 IPs). Powered by Cloudflare Workers with 24-hour caching.

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

## Alternative To

A free alternative to ipinfo.io, ipstack, and ip-api.com Pro. Get VPN detection, bulk lookups, and rich geolocation data without per-lookup pricing.

## Keywords

`ip geolocation api`, `ip lookup`, `geoip`, `ip to location`, `vpn detection api`, `proxy detection`, `ip address api`, `geolocation rest api`, `free ip api`, `bulk ip lookup`

## Development

```bash
npm install
npm run dev      # Local development
npm run deploy   # Deploy to Cloudflare
```
