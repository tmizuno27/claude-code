# Free Email Validation API - Disposable Detection, MX Lookup, Typo Fix

> **Free tier: 500 requests/month** | Production-ready email verification without sending any emails

Validate email addresses in real time with format checks, MX record lookups, disposable domain detection (500+ domains), free provider detection, role-based address detection, and typo suggestions. Built on Cloudflare Workers for sub-100ms global latency.

## Why Choose This Email Validation API?

- **No emails sent** -- validates via DNS/MX lookup, format checks, and domain intelligence
- **Disposable email detection** -- blocks 500+ temporary/throwaway email domains (Mailinator, Guerrilla, etc.)
- **Typo correction** -- suggests fixes for common domain typos (gmial.com -> gmail.com)
- **Bulk validation** -- validate up to 50 emails in a single API call
- **Confidence score** -- 0-100 scoring system for easy filtering
- **Free tier** -- 500 requests/month at $0, perfect for form validation and sign-up flows

## Use Cases

- **SaaS sign-up forms** -- reject disposable emails and catch typos before account creation
- **Email marketing** -- clean your mailing list to reduce bounce rates and protect sender reputation
- **E-commerce checkout** -- validate customer emails to ensure order confirmations are delivered
- **Lead generation** -- score and filter inbound leads by email quality
- **CRM data hygiene** -- bulk validate existing contacts to remove invalid addresses
- **Fraud prevention** -- flag disposable and role-based emails in high-risk transactions

## Quick Start

### Validate a Single Email

```bash
curl -X GET "https://email-validation-api.t-mizuno27.workers.dev/validate?email=user@example.com" \
  -H "X-RapidAPI-Key: YOUR_KEY" \
  -H "X-RapidAPI-Host: email-validation-api.p.rapidapi.com"
```

**Response:**
```json
{
  "email": "user@example.com",
  "valid": true,
  "format_valid": true,
  "mx_found": true,
  "is_disposable": false,
  "is_free_provider": false,
  "is_role_based": false,
  "suggestion": null,
  "score": 100,
  "checks": {
    "format_valid": true,
    "mx_found": true,
    "mx_records": [
      { "priority": 1, "exchange": "aspmx.l.google.com" }
    ],
    "is_disposable": false,
    "is_free_provider": false,
    "is_role_based": false,
    "suggestion": null
  }
}
```

### Detect a Disposable Email

```bash
curl "https://email-validation-api.t-mizuno27.workers.dev/validate?email=test@mailinator.com"
```

```json
{
  "email": "test@mailinator.com",
  "valid": false,
  "is_disposable": true,
  "score": 10
}
```

### Bulk Validation (up to 50 emails)

```bash
curl -X POST "https://email-validation-api.t-mizuno27.workers.dev/validate/bulk" \
  -H "Content-Type: application/json" \
  -H "X-RapidAPI-Key: YOUR_KEY" \
  -d '{"emails": ["user@example.com", "test@mailinator.com", "admin@gmial.com"]}'
```

### Python Example

```python
import requests

url = "https://email-validation-api.p.rapidapi.com/validate"
params = {"email": "user@example.com"}
headers = {
    "X-RapidAPI-Key": "YOUR_KEY",
    "X-RapidAPI-Host": "email-validation-api.p.rapidapi.com"
}

response = requests.get(url, headers=headers, params=params)
data = response.json()

if data["valid"] and data["score"] >= 80:
    print("Email is valid and high quality")
elif data["suggestion"]:
    print(f"Did you mean {data['suggestion']}?")
```

### Node.js Example

```javascript
const axios = require("axios");

const { data } = await axios.get(
  "https://email-validation-api.p.rapidapi.com/validate",
  {
    params: { email: "user@example.com" },
    headers: {
      "X-RapidAPI-Key": "YOUR_KEY",
      "X-RapidAPI-Host": "email-validation-api.p.rapidapi.com",
    },
  }
);

console.log(`Valid: ${data.valid}, Score: ${data.score}`);
```

## Validation Checks

| Check | Points | Description |
|-------|--------|-------------|
| **Format** | +30 | RFC 5322 regex + length validation |
| **MX Records** | +40 | DNS over HTTPS lookup via Cloudflare 1.1.1.1 |
| **Not Disposable** | +15 | 500+ known disposable/temporary domains |
| **Not Role-Based** | +10 | Detects admin@, info@, support@, etc. |
| **Disposable Penalty** | -20 | Detected as throwaway email domain |

## Pricing

| Plan | Price | Requests/mo | Rate Limit |
|------|-------|-------------|------------|
| Basic (FREE) | $0 | 500 | 1 req/sec |
| Pro | $5.99 | 50,000 | 10 req/sec |
| Ultra | $14.99 | 500,000 | 50 req/sec |

## Alternative To

A free alternative to ZeroBounce, Hunter.io, and NeverBounce. Get the same core validation features -- MX lookup, disposable detection, typo correction -- without per-email pricing or expensive monthly minimums.

## Keywords

`email validation api`, `email verification`, `disposable email detection`, `mx lookup api`, `email hygiene`, `bounce detection`, `email typo fix`, `bulk email validation`, `free email api`, `saas email validation`

## Development

```bash
npm install
npm run dev      # Local development
npm run deploy   # Deploy to Cloudflare
```
