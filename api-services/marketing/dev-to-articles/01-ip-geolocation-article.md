# Free IP Geolocation API with VPN Detection -- ipinfo.io Alternative for Developers

> Published on: Dev.to
> Tags: api, webdev, javascript, python
> Canonical URL: (set after publishing)

---

Looking for a free IP geolocation API with VPN detection? Most popular options like ipinfo.io charge $99/month for VPN detection, and ipstack doesn't even offer HTTPS on their free plan.

I built a lightweight alternative that runs on Cloudflare Workers' edge network. Here's what it does and how to use it.

## What You Get (Free Tier: 500 requests/month)

- IP to country, city, region, lat/long, timezone, ISP
- VPN / proxy / datacenter detection
- Own-IP endpoint (`/me`) -- zero external API calls
- Bulk lookup (up to 20 IPs per request)
- HTTPS included on free tier
- Sub-100ms latency via Cloudflare edge (300+ cities)

## Quick Example: Detect VPN Users in Your App

### Python

```python
import requests

url = "https://ip-geolocation-api.p.rapidapi.com/lookup"
params = {"ip": "8.8.8.8"}
headers = {
    "X-RapidAPI-Key": "YOUR_KEY",
    "X-RapidAPI-Host": "ip-geolocation-api.p.rapidapi.com"
}

data = requests.get(url, headers=headers, params=params).json()

if data["is_vpn"] or data["is_datacenter"]:
    print(f"WARNING: {data['ip']} is using VPN/datacenter ({data['isp']})")
else:
    print(f"User location: {data['city']}, {data['country_name']}")
```

### JavaScript (Node.js)

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

if (data.is_vpn || data.is_datacenter) {
  console.log(`Suspicious IP: ${data.ip} (${data.isp})`);
} else {
  console.log(`${data.city}, ${data.country_name}`);
}
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

## Use Case: Geo-Fencing Middleware (Express.js)

```javascript
const axios = require("axios");

async function geoFence(req, res, next) {
  const ip = req.headers["x-forwarded-for"] || req.socket.remoteAddress;

  const { data } = await axios.get(
    "https://ip-geolocation-api.p.rapidapi.com/lookup",
    {
      params: { ip },
      headers: {
        "X-RapidAPI-Key": process.env.RAPIDAPI_KEY,
        "X-RapidAPI-Host": "ip-geolocation-api.p.rapidapi.com",
      },
    }
  );

  // Block VPN users from payment page
  if (data.is_vpn && req.path.startsWith("/checkout")) {
    return res.status(403).json({ error: "VPN detected. Please disable VPN for payment." });
  }

  // Add geo data to request
  req.geo = data;
  next();
}

app.use(geoFence);
```

## Pricing Comparison

| | This API | ipinfo.io | ipstack | ip-api.com |
|-|----------|-----------|---------|------------|
| Free tier | 500/mo | 50K/mo | 100/mo | 45/min (no HTTPS) |
| VPN detection | Free | $99/mo add-on | Paid add-on | Not available |
| Bulk lookup | 20 IPs/req | Paid only | No | 100/batch |
| HTTPS (free) | Yes | Yes | No | No |
| Paid plans | From $5.99/mo | From $99/mo | From $9.99/mo | From $13/mo |

## Try It Now

**[Subscribe on RapidAPI (free)](https://rapidapi.com/miccho27-5OJaGGbBiO/api/ip-geolocation-api)** -- no credit card required for the free tier.

The API runs on Cloudflare Workers with zero server costs. Responses are cached for 24 hours at the edge, so repeat lookups are nearly instant.

---

*Built with Cloudflare Workers. If you have questions or feature requests, leave a comment below or reach out on RapidAPI.*
