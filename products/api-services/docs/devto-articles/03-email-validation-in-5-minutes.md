---
title: "How to Add Email Validation to Your App in 5 Minutes"
published: false
description: "Stop fake signups and typo-riddled emails from ruining your user data. A practical guide to integrating real-time email validation with MX lookups, disposable email detection, and typo correction."
tags: email, api, tutorial, webdev
cover_image:
---

You ship a signup form. Users start registering. Within a week, your database is full of:

- `test@test.com` (no MX record, will never receive email)
- `user@mailinator.com` (disposable, gone in 10 minutes)
- `john@gmial.com` (typo — meant gmail.com)
- `admin@yourcompany.com` (role-based, not a real person)

Your welcome emails bounce. Your sender reputation tanks. Your "1,000 users" metric is actually 600 real people and 400 garbage entries.

This tutorial shows you how to fix it in 5 minutes with a free API that does RFC validation, live MX record lookups, disposable domain detection, and typo suggestions — all in a single HTTP call.

---

## What Good Email Validation Actually Checks

Most developers stop at regex. That catches `not-an-email`, but it doesn't catch:

| Check | What it catches | Regex alone? |
|-------|----------------|:---:|
| RFC 5322 format | `user@@double.com`, `spaces in@email.com` | Yes |
| MX record exists | `user@nonexistent-domain-xyz.com` | No |
| Disposable domain | `user@mailinator.com`, `user@guerrillamail.com` | No |
| Role-based address | `admin@`, `support@`, `noreply@` | No |
| Free provider detection | `user@gmail.com` vs `user@company.com` | No |
| Typo suggestion | `user@gmial.com` → `user@gmail.com` | No |

A proper validation API handles all six in one request.

---

## The API

We'll use the [Email Validation API](https://rapidapi.com/miccho27-5OJaGGbBiO/api/email-validation-api) — a Cloudflare Workers-based service with a free tier of 500 requests/month. No API key needed for the direct endpoint.

### Single Email Validation

```bash
curl "https://email-validation-api.miccho27.workers.dev/validate?email=john@gmial.com"
```

```json
{
  "email": "john@gmial.com",
  "valid": false,
  "format_valid": true,
  "mx_found": false,
  "is_disposable": false,
  "is_free_provider": false,
  "is_role_based": false,
  "suggestion": "john@gmail.com",
  "score": 30
}
```

The response tells you:
- **valid: false** — Don't accept this email
- **format_valid: true** — The format is technically correct (regex would pass it)
- **mx_found: false** — `gmial.com` has no mail server
- **suggestion: "john@gmail.com"** — The API detected the typo and suggests a fix

### Bulk Validation (up to 50 emails)

```bash
curl -X POST "https://email-validation-api.miccho27.workers.dev/validate/bulk" \
  -H "Content-Type: application/json" \
  -d '{"emails": ["user@gmail.com", "test@mailinator.com", "admin@company.com"]}'
```

```json
{
  "count": 3,
  "results": [
    {
      "email": "user@gmail.com",
      "valid": true,
      "score": 85,
      "is_free_provider": true,
      "is_disposable": false,
      "is_role_based": false
    },
    {
      "email": "test@mailinator.com",
      "valid": false,
      "score": 25,
      "is_disposable": true
    },
    {
      "email": "admin@company.com",
      "valid": true,
      "score": 75,
      "is_role_based": true
    }
  ]
}
```

---

## Integration 1: React Signup Form (3 minutes)

Here's a complete React hook that validates emails on blur:

```javascript
import { useState, useCallback } from "react";

const API = "https://email-validation-api.miccho27.workers.dev/validate";

function useEmailValidation() {
  const [status, setStatus] = useState({ state: "idle" });

  const validate = useCallback(async (email) => {
    if (!email || !email.includes("@")) {
      setStatus({ state: "idle" });
      return;
    }

    setStatus({ state: "checking" });

    try {
      const res = await fetch(`${API}?email=${encodeURIComponent(email)}`);
      const data = await res.json();

      if (data.valid) {
        setStatus({ state: "valid", data });
      } else if (data.suggestion) {
        setStatus({
          state: "suggestion",
          message: `Did you mean ${data.suggestion}?`,
          suggested: data.suggestion,
          data,
        });
      } else if (data.is_disposable) {
        setStatus({
          state: "error",
          message: "Please use a permanent email address.",
          data,
        });
      } else if (!data.mx_found) {
        setStatus({
          state: "error",
          message: "This email domain doesn't appear to exist.",
          data,
        });
      } else {
        setStatus({
          state: "error",
          message: "Please enter a valid email address.",
          data,
        });
      }
    } catch {
      // API failure = don't block the user
      setStatus({ state: "valid", data: null });
    }
  }, []);

  return { status, validate };
}
```

Use it in a form component:

```jsx
function SignupForm() {
  const [email, setEmail] = useState("");
  const { status, validate } = useEmailValidation();

  return (
    <form>
      <label htmlFor="email">Email</label>
      <input
        id="email"
        type="email"
        value={email}
        onChange={(e) => setEmail(e.target.value)}
        onBlur={() => validate(email)}
        className={status.state === "error" ? "input-error" : ""}
      />

      {status.state === "checking" && (
        <span className="hint">Checking...</span>
      )}

      {status.state === "error" && (
        <span className="error">{status.message}</span>
      )}

      {status.state === "suggestion" && (
        <span className="warning">
          {status.message}{" "}
          <button
            type="button"
            onClick={() => {
              setEmail(status.suggested);
              validate(status.suggested);
            }}
          >
            Use suggestion
          </button>
        </span>
      )}

      {status.state === "valid" && (
        <span className="success">Looks good</span>
      )}

      <button type="submit" disabled={status.state === "error"}>
        Sign Up
      </button>
    </form>
  );
}
```

Key UX decisions:
- **Validate on blur, not on every keystroke** — avoids hammering the API and annoying users mid-typing
- **Show typo suggestions with a "Use suggestion" button** — don't auto-correct, let the user decide
- **If the API fails, let the user through** — never block signups due to a validation API outage

---

## Integration 2: Python Backend Validation (2 minutes)

For server-side validation (which you should always do in addition to client-side):

```python
import requests
from functools import lru_cache

API = "https://email-validation-api.miccho27.workers.dev"

def validate_email(email: str) -> dict:
    """
    Validate an email address. Returns a dict with:
    - valid (bool): Whether to accept this email
    - reason (str): Human-readable explanation if invalid
    - suggestion (str|None): Suggested correction if typo detected
    - score (int): 0-100 confidence score
    """
    try:
        resp = requests.get(
            f"{API}/validate",
            params={"email": email},
            timeout=5,
        )
        resp.raise_for_status()
        data = resp.json()
    except requests.RequestException:
        # Fail open — don't block registration if API is down
        return {"valid": True, "reason": "Validation service unavailable", "score": 0}

    if data["valid"]:
        return {
            "valid": True,
            "reason": "Valid email",
            "suggestion": data.get("suggestion"),
            "score": data["score"],
            "is_free_provider": data.get("is_free_provider", False),
        }

    # Build specific rejection reason
    reasons = []
    if not data["format_valid"]:
        reasons.append("Invalid email format")
    if not data["mx_found"]:
        reasons.append("Domain has no mail server")
    if data["is_disposable"]:
        reasons.append("Disposable email not allowed")

    return {
        "valid": False,
        "reason": "; ".join(reasons) if reasons else "Invalid email",
        "suggestion": data.get("suggestion"),
        "score": data["score"],
    }
```

### Flask Example

```python
from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route("/api/register", methods=["POST"])
def register():
    data = request.json
    email = data.get("email", "").strip().lower()

    # Validate email
    check = validate_email(email)
    if not check["valid"]:
        response = {"error": check["reason"]}
        if check.get("suggestion"):
            response["suggestion"] = check["suggestion"]
        return jsonify(response), 400

    # Warn about free providers (optional, for B2B)
    if check.get("is_free_provider"):
        # Log it, but don't block
        app.logger.info(f"Free provider signup: {email}")

    # Proceed with registration...
    return jsonify({"message": "Registration successful"}), 201
```

### Django Example

```python
# validators.py
from django.core.exceptions import ValidationError

def validate_email_real(email):
    result = validate_email(email)  # Using the function defined above
    if not result["valid"]:
        msg = result["reason"]
        if result.get("suggestion"):
            msg += f" Did you mean {result['suggestion']}?"
        raise ValidationError(msg)

# models.py
from django.db import models

class User(models.Model):
    email = models.EmailField(validators=[validate_email_real])
```

---

## Integration 3: Bulk Cleanup of Existing Data

Already have a database full of unvalidated emails? Clean it up:

```python
import requests
import csv
import time

API = "https://email-validation-api.miccho27.workers.dev"

def cleanup_email_list(input_csv, output_csv):
    with open(input_csv) as f:
        emails = [row[0] for row in csv.reader(f) if row]

    valid_emails = []
    invalid_emails = []
    suggestions = []

    # Process in batches of 50
    for i in range(0, len(emails), 50):
        batch = emails[i : i + 50]
        resp = requests.post(
            f"{API}/validate/bulk",
            json={"emails": batch},
            timeout=30,
        )
        results = resp.json()["results"]

        for r in results:
            if r["valid"]:
                valid_emails.append(r["email"])
            else:
                invalid_emails.append(r)
                if r.get("suggestion"):
                    suggestions.append((r["email"], r["suggestion"]))

        # Respect rate limits
        time.sleep(1)

    # Write results
    with open(output_csv, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["email", "status", "score", "issue", "suggestion"])
        for email in valid_emails:
            writer.writerow([email, "valid", "", "", ""])
        for r in invalid_emails:
            issue = "disposable" if r.get("is_disposable") else "invalid"
            writer.writerow([r["email"], "invalid", r.get("score", 0), issue, r.get("suggestion", "")])

    print(f"Results: {len(valid_emails)} valid, {len(invalid_emails)} invalid")
    if suggestions:
        print(f"\nTypo suggestions ({len(suggestions)}):")
        for original, suggested in suggestions:
            print(f"  {original} → {suggested}")

if __name__ == "__main__":
    cleanup_email_list("emails.csv", "validated_emails.csv")
```

---

## How It Works Under the Hood

A quick look at what happens when you call `/validate?email=user@example.com`:

### 1. Format Check (RFC 5322)

```javascript
const EMAIL_REGEX =
  /^[a-zA-Z0-9.!#$%&'*+/=?^_`{|}~-]+@[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?(?:\.[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?)*$/;
```

This catches obvious format errors. It's strict enough to reject garbage but permissive enough to allow valid edge cases (like `+` tags in Gmail addresses).

### 2. MX Record Lookup (Live DNS Query)

```javascript
async function lookupMX(domain) {
  const url = `https://cloudflare-dns.com/dns-query?name=${encodeURIComponent(domain)}&type=MX`;
  const res = await fetch(url, {
    headers: { Accept: "application/dns-json" },
  });
  const data = await res.json();
  const records = (data.Answer || [])
    .filter((r) => r.type === 15)
    .map((r) => ({
      priority: parseInt(r.data.split(" ")[0], 10),
      exchange: r.data.split(" ")[1]?.replace(/\.$/, ""),
    }))
    .sort((a, b) => a.priority - b.priority);

  return { found: records.length > 0, records };
}
```

This uses Cloudflare's DNS-over-HTTPS service to check if the domain actually has mail servers. It's the single most important check beyond format validation — if there's no MX record, the email can never receive messages.

### 3. Disposable Domain Detection

The API checks against a list of 10,000+ known disposable email providers (Mailinator, Guerrillamail, Tempmail, etc.). The list is embedded directly in the Worker for zero-latency lookups.

### 4. Typo Suggestion

Common domain typos are caught with a Levenshtein distance-based matcher:

- `gmial.com` → `gmail.com`
- `yaho.com` → `yahoo.com`
- `hotmal.com` → `hotmail.com`
- `outlok.com` → `outlook.com`

### 5. Score Calculation

The final score (0-100) is a weighted composite:

| Factor | Points | Logic |
|--------|--------|-------|
| Valid format | 30 | Basic requirement |
| MX record found | 40 | Strongest signal |
| Not disposable | 15 | Penalty if disposable |
| Not role-based | 10 | Soft signal |
| No typo detected | 5 | Minor factor |

A score of 70+ generally means "safe to accept." Below 50 is suspicious.

---

## Best Practices

### 1. Always Validate Server-Side

Client-side validation improves UX. Server-side validation is your actual defense. Never trust the client.

```python
# WRONG: Only client-side validation
# The user can bypass your JavaScript and POST directly

# RIGHT: Validate on both sides
# Client: Immediate feedback, UX improvement
# Server: Actual security gate
```

### 2. Fail Open

If the validation API is down, let the user register. A user you might need to verify later is better than a user you lost.

```javascript
try {
  const result = await validateEmail(email);
  if (!result.valid) return reject(result.reason);
} catch (error) {
  // API down — log it, but don't block the user
  console.error("Email validation API unavailable:", error);
}
```

### 3. Present Suggestions, Don't Auto-Correct

`john@gmial.com` is probably a typo. But `john@gm-ial.com` at a company called "GM-IAL" is not. Always show the suggestion and let the user confirm.

### 4. Don't Over-Validate

- **Blocking disposable emails is reasonable** for SaaS products.
- **Blocking free providers (Gmail, Yahoo)** is usually wrong unless you're specifically targeting B2B.
- **Blocking role-based addresses** depends on context — `support@company.com` might be a legitimate user.

Use the `score` field to make nuanced decisions rather than hard pass/fail.

---

## Pricing Comparison

| Service | Free Tier | Pro Price | What You Get |
|---------|-----------|-----------|-------------|
| ZeroBounce | 100/mo | $39/mo (2,500) | Bulk validation |
| NeverBounce | 1,000 one-time | $8/1,000 | Pay per use |
| Hunter.io | 25/mo | $49/mo | Email finder + validation |
| **This API** | **500/mo** | **$5.99/mo (50K)** | Real-time + bulk validation |

For most indie projects and startups, 500 free requests per month covers development and early production. The Pro tier at $5.99/mo for 50,000 requests is roughly 100x cheaper than ZeroBounce.

---

## Summary

In 5 minutes you can:

1. **Add client-side validation** — Better UX, fewer garbage signups
2. **Add server-side validation** — Actual security
3. **Clean existing data** — Bulk endpoint handles 50 emails per request

The API is live and free to use:

```bash
# Test it now
curl "https://email-validation-api.miccho27.workers.dev/validate?email=your@email.com"
```

[Email Validation API on RapidAPI](https://rapidapi.com/miccho27-5OJaGGbBiO/api/email-validation-api) | [Full API Collection](https://rapidapi.com/user/miccho27-5OJaGGbBiO)

Questions? Drop a comment or find me on [X @prodhq27](https://x.com/prodhq27).
