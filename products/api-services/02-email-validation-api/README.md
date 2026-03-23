# Free Email Validation API - Disposable Detection, MX Lookup, Typo Fix

> **Free tier: 500 requests/month** | Production-ready email verification without sending any emails

Validate email addresses in real time with format checks, MX record lookups, disposable domain detection (500+ domains), free provider detection, role-based address detection, and typo suggestions. Built on Cloudflare Workers for sub-100ms global latency.

## Getting Started in 30 Seconds

1. Subscribe on [RapidAPI](https://rapidapi.com/miccho27-5OJaGGbBiO/api/email-validation-api) (free plan available)
2. Copy your API key
3. Validate your first email:

```bash
curl -X GET "https://email-validation-api.p.rapidapi.com/validate?email=user@example.com" \
  -H "X-RapidAPI-Key: YOUR_KEY" \
  -H "X-RapidAPI-Host: email-validation-api.p.rapidapi.com"
```

## How It Compares

| Feature | This API | ZeroBounce | Hunter.io | NeverBounce |
|---------|----------|-----------|-----------|-------------|
| Free tier | 500 req/mo | 100/mo | 25 searches/mo | 1,000 free |
| Pro pricing | $5.99/50K | $16/2K | $49/500 | $8/1K |
| MX lookup | Yes | Yes | Yes | Yes |
| Disposable detection | Yes (500+ domains) | Yes | No | Yes |
| Typo correction | Yes | No | No | No |
| Bulk validation | Yes (50/request) | Yes | Yes | Yes |
| Confidence score | Yes (0-100) | Yes | Yes | Yes |
| Role-based detection | Yes | Yes | No | No |
| No per-email pricing | Yes (flat plan) | No ($0.008/email) | No ($0.098/email) | No ($0.008/email) |

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

## FAQ

**Q: Does this API actually send emails to verify addresses?**
A: No. Validation is done via DNS MX record lookups, format checks, and domain intelligence. No emails are ever sent, which means no bounce risk.

**Q: How many disposable email domains are detected?**
A: Over 500 known disposable/temporary email domains including Mailinator, Guerrilla Mail, 10MinuteMail, and more. The list is regularly updated.

**Q: Can I validate emails in bulk?**
A: Yes. The `/validate/bulk` endpoint accepts up to 50 emails per request. For larger lists, batch your requests.

**Q: What does the confidence score mean?**
A: A score of 0-100 reflecting email quality. 90-100 = high quality, 50-89 = moderate (free provider or role-based), below 50 = risky (disposable or invalid format).

**Q: Does it catch typos like "gmial.com"?**
A: Yes. Common domain typos are detected and the correct domain is suggested (e.g., gmial.com -> gmail.com, yaho.com -> yahoo.com).

## Development

```bash
npm install
npm run dev      # Local development
npm run deploy   # Deploy to Cloudflare
```
