---
title: "Build an Email Validation System with a Free API — Disposable Detection, MX Checks, Typo Suggestions"
published: false
tags: api, webdev, python, email
---

Bad email addresses cost money. Every bounced email hurts your sender reputation, and disposable emails pollute your user database. Most email validation services charge $0.005–$0.01 per check — that's $50 for 10,000 validations.

I built a **free Email Validation API** that handles the heavy lifting: syntax validation, MX record verification, disposable domain detection (500+ domains), and even typo suggestions (catches `gmial.com` → `gmail.com`).

## What It Checks

1. **Syntax validation** — RFC-compliant format check
2. **MX record lookup** — Does the domain actually accept email?
3. **Disposable detection** — 500+ throwaway email providers flagged
4. **Typo correction** — Suggests fixes for common domain typos
5. **Role-based detection** — Flags `info@`, `admin@`, `support@` addresses

## Quick Start

```bash
curl "https://email-validation-api.p.rapidapi.com/validate?email=user@gmial.com"
```

Response:
```json
{
  "email": "user@gmial.com",
  "valid_syntax": true,
  "mx_records": false,
  "is_disposable": false,
  "is_role_based": false,
  "suggestion": "user@gmail.com",
  "score": 30,
  "verdict": "risky"
}
```

Notice it caught the `gmial.com` typo and suggested `gmail.com`.

## JavaScript — Form Validation

```javascript
async function validateEmail(email) {
  const response = await fetch(
    `https://email-validation-api.p.rapidapi.com/validate?email=${encodeURIComponent(email)}`
  );
  const result = await response.json();

  if (result.is_disposable) {
    return { valid: false, reason: 'Disposable emails are not allowed' };
  }

  if (result.suggestion) {
    return { valid: false, reason: `Did you mean ${result.suggestion}?` };
  }

  if (result.score < 50) {
    return { valid: false, reason: 'This email address appears invalid' };
  }

  return { valid: true };
}

// Usage in a signup form
const { valid, reason } = await validateEmail('user@gmial.com');
if (!valid) {
  showError(reason); // "Did you mean user@gmail.com?"
}
```

## Python — Bulk Validation

```python
import requests
import csv

def validate_email(email: str) -> dict:
    response = requests.get(
        "https://email-validation-api.p.rapidapi.com/validate",
        params={"email": email},
        timeout=10
    )
    return response.json()

# Validate a CSV of emails
with open("emails.csv") as f:
    reader = csv.DictReader(f)
    for row in reader:
        result = validate_email(row["email"])
        if result["is_disposable"]:
            print(f"DISPOSABLE: {row['email']}")
        elif result["score"] < 50:
            print(f"INVALID: {row['email']} (score: {result['score']})")
        elif result.get("suggestion"):
            print(f"TYPO: {row['email']} → {result['suggestion']}")
        else:
            print(f"OK: {row['email']}")
```

## When to Use This

| Scenario | Without validation | With validation |
|----------|-------------------|-----------------|
| Signup form | 15% fake emails → bounce | Catch typos + disposables at entry |
| Newsletter | High bounce rate → domain blacklisted | Only valid addresses get through |
| Lead gen | Sales wastes time on bad leads | Only real emails in CRM |
| Waitlist | Inflated numbers, useless data | Accurate user count |

## API Response Fields

| Field | Type | Description |
|-------|------|-------------|
| `valid_syntax` | boolean | RFC email format check |
| `mx_records` | boolean | Domain has MX records |
| `is_disposable` | boolean | Known throwaway provider |
| `is_role_based` | boolean | Generic address (info@, admin@) |
| `suggestion` | string | Typo correction (null if none) |
| `score` | number | 0–100 deliverability score |
| `verdict` | string | `valid`, `risky`, or `invalid` |

## Free Tier

500 requests/month — no API key required. That's enough for a small SaaS signup flow or cleaning a contact list.

[**Try it free on RapidAPI →**](https://rapidapi.com/miccho27-5OJaGGbBiO/api/email-validation-api)

---

*Part of a [collection of 24 free developer APIs](https://rapidapi.com/user/miccho27-5OJaGGbBiO) running on Cloudflare Workers.*
