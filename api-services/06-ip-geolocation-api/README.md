# IP Geolocation API

IP geolocation lookup API powered by Cloudflare Workers.

## Endpoints

### GET /me
Returns geolocation for the caller's IP using Cloudflare's built-in `request.cf` data (free, no external API).

### GET /lookup?ip=8.8.8.8
Lookup geolocation for a specific IP address. Uses ip-api.com as the data source with 24-hour caching.

### POST /lookup/bulk
Batch lookup up to 20 IPs at once.

**Request body:**
```json
{ "ips": ["8.8.8.8", "1.1.1.1"] }
```

## Response Format

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

## Architecture

- **/me** uses Cloudflare's free `request.cf` object (zero external calls)
- **/lookup** and **/lookup/bulk** use ip-api.com free tier (45 req/min)
- All results cached 24 hours via CF Cache API to minimize upstream calls

## Deploy

```bash
npm install
npx wrangler deploy
```

## Base URL

https://ip-geolocation-api.t-mizuno27.workers.dev
