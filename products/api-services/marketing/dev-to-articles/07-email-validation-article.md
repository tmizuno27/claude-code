---
title: "How to Validate Emails in Your App — Detect Disposable Emails, Typos, and Invalid Domains"
published: false
tags: api, webdev, saas, javascript
---

Bad emails kill your SaaS metrics. Disposable signups inflate your user count, typos cause failed onboarding, and invalid addresses tank your email deliverability score.

Here's how to catch all three problems with a single API call — no regex hacks, no maintaining your own blocklist of 500+ disposable domains.

## The Problem with Regex-Only Validation

Most developers start with regex:

```javascript
const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
```

This catches the obvious errors, but misses:
- `user@gmial.com` (typo — should be gmail.com)
- `user@tempmail.ninja` (disposable email)
- `user@nonexistent-domain.xyz` (no MX records)
- `user@example.com` (role-based, unlikely to be a real person)

## Email Validation API

One endpoint that checks all of the above, plus DNS verification and typo suggestions.

### Quick Start

```bash
curl "https://email-validation-api.p.rapidapi.com/validate?email=user@gmial.com" \
  -H "X-RapidAPI-Key: YOUR_KEY"
```

Response:

```json
{
  "email": "user@gmial.com",
  "valid": false,
  "reason": "possible_typo",
  "suggestion": "user@gmail.com",
  "disposable": false,
  "mx_records": true,
  "domain": "gmial.com"
}
```

### JavaScript: Signup Form Validation

```javascript
async function validateEmail(email) {
  const response = await fetch(
    `https://email-validation-api.p.rapidapi.com/validate?email=${encodeURIComponent(email)}`,
    { headers: { 'X-RapidAPI-Key': process.env.RAPIDAPI_KEY } }
  );
  return response.json();
}

// Express middleware
async function emailValidationMiddleware(req, res, next) {
  const { email } = req.body;

  if (!email) {
    return res.status(400).json({ error: 'Email is required' });
  }

  const result = await validateEmail(email);

  if (result.disposable) {
    return res.status(400).json({
      error: 'Disposable emails are not allowed',
      suggestion: 'Please use a permanent email address'
    });
  }

  if (result.suggestion) {
    return res.status(400).json({
      error: `Did you mean ${result.suggestion}?`,
      suggestion: result.suggestion
    });
  }

  if (!result.valid) {
    return res.status(400).json({ error: 'Invalid email address' });
  }

  next();
}
```

### Python: Bulk Email Cleaning

```python
import requests
import csv
from time import sleep

def validate_email(email):
    response = requests.get(
        "https://email-validation-api.p.rapidapi.com/validate",
        params={"email": email},
        headers={"X-RapidAPI-Key": "YOUR_KEY"}
    )
    return response.json()

def clean_email_list(input_csv, output_csv):
    """Remove disposable and invalid emails from a mailing list."""
    results = {"valid": 0, "invalid": 0, "disposable": 0, "typo": 0}

    with open(input_csv) as fin, open(output_csv, "w", newline="") as fout:
        reader = csv.DictReader(fin)
        writer = csv.DictWriter(fout, fieldnames=["email", "status", "suggestion"])
        writer.writeheader()

        for row in reader:
            result = validate_email(row["email"])
            sleep(0.5)  # respect rate limits

            if result.get("disposable"):
                status = "disposable"
                results["disposable"] += 1
            elif result.get("suggestion"):
                status = "typo"
                results["typo"] += 1
            elif result.get("valid"):
                status = "valid"
                results["valid"] += 1
            else:
                status = "invalid"
                results["invalid"] += 1

            writer.writerow({
                "email": row["email"],
                "status": status,
                "suggestion": result.get("suggestion", "")
            })

    print(f"Results: {results}")

clean_email_list("subscribers.csv", "cleaned_subscribers.csv")
```

### What Gets Checked

| Check | Description |
|-------|-------------|
| **Syntax** | RFC 5322 compliance |
| **MX Records** | DNS lookup to verify the domain accepts email |
| **Disposable** | 500+ known temporary email providers |
| **Typo Detection** | Levenshtein distance against popular providers |
| **Role-Based** | Detects info@, admin@, support@ addresses |

## Pricing

- **Free**: 500 requests/month
- **Basic**: $5/month for 10,000 requests
- **Pro**: $15/month for 50,000 requests

[Try Email Validation API on RapidAPI](https://rapidapi.com/miccho27-5OJaGGbBiO/api/email-validation-api)

---

*Built by [@miccho27](https://rapidapi.com/miccho27-5OJaGGbBiO). Powered by Cloudflare Workers with zero cold starts.*
