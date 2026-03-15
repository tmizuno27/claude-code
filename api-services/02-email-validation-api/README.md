# Email Validation API

A production-ready email validation API built as a Cloudflare Worker. Validates email addresses without sending any emails using format checks, MX record lookups (via DNS over HTTPS), disposable domain detection, and more.

## Endpoints

### `GET /validate?email=user@example.com`

Validate a single email address.

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

### `POST /validate/bulk`

Validate up to 50 emails in a single request.

**Request body:**
```json
{
  "emails": [
    "user@example.com",
    "test@mailinator.com",
    "admin@gmial.com"
  ]
}
```

**Response:**
```json
{
  "count": 3,
  "results": [ ... ]
}
```

### `GET /` or `GET /health`

Health check / service info.

## Validation Checks

| Check | Description |
|-------|-------------|
| **Format** | RFC 5322 regex + length validation |
| **MX Records** | DNS over HTTPS lookup via Cloudflare's 1.1.1.1 |
| **Disposable** | 500+ known disposable/temporary email domains |
| **Free Provider** | Detects Gmail, Yahoo, Hotmail, Outlook, etc. |
| **Role-Based** | Detects admin@, info@, support@, etc. |
| **Typo Suggestion** | Suggests corrections for common domain typos |

## Scoring (0-100)

- Format valid: +30
- MX records found: +40
- Not disposable: +15 (disposable: -20)
- Not role-based: +10
- No typo detected: +5

## Deployment

```bash
npm install
npx wrangler deploy
```

## Local Development

```bash
npx wrangler dev
```

## Configuration

Environment variables in `wrangler.toml`:

| Variable | Default | Description |
|----------|---------|-------------|
| `RATE_LIMIT_PER_MINUTE` | 60 | Rate limit per minute |
| `BULK_MAX_EMAILS` | 50 | Max emails per bulk request |
