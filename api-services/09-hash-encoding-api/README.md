# Free Hash & Encoding API - SHA256, MD5, Bcrypt, Base64, HMAC

> **Free tier: 500 requests/month** | Hashing, encoding, and cryptographic operations via Web Crypto API

Hash text with SHA-256/384/512, MD5, bcrypt. Encode/decode Base64, URL encoding, hex. Generate HMAC signatures and cryptographic random strings. Zero external dependencies -- uses Web Crypto API.

## Why Choose This Hash & Encoding API?

- **Multiple algorithms** -- SHA-256, SHA-384, SHA-512, MD5, bcrypt
- **HMAC support** -- generate HMAC signatures for webhook verification
- **Bcrypt** -- password hashing with configurable salt rounds
- **Encoding** -- Base64, URL encoding, hex encoding/decoding
- **Random generation** -- cryptographically secure random strings and UUIDs
- **Free tier** -- 500 requests/month at $0

## Use Cases

- **Webhook verification** -- generate and verify HMAC signatures
- **Password hashing** -- bcrypt for secure password storage
- **Data integrity** -- SHA-256 checksums for file/data verification
- **API development** -- Base64 encode/decode payloads
- **Security tools** -- hash comparison, encoding conversion

## Quick Start

```bash
curl -X POST "https://hash-encoding-api.t-mizuno27.workers.dev/hash" \
  -H "Content-Type: application/json" \
  -H "X-RapidAPI-Key: YOUR_KEY" \
  -d '{"text": "hello world", "algorithm": "sha256"}'
```

### Python Example

```python
import requests

url = "https://hash-encoding-api.p.rapidapi.com/hash"
headers = {"X-RapidAPI-Key": "YOUR_KEY", "X-RapidAPI-Host": "hash-encoding-api.p.rapidapi.com"}
payload = {"text": "my-password", "algorithm": "bcrypt", "rounds": 12}

data = requests.post(url, headers=headers, json=payload).json()
print(f"Hash: {data['hash']}")
```

## Pricing

| Plan | Price | Requests/mo | Rate Limit |
|------|-------|-------------|------------|
| Basic (FREE) | $0 | 500 | 1 req/sec |
| Pro | $5.99 | 50,000 | 10 req/sec |

## Alternative To

A free alternative to CryptoJS online tools, HashAPI, and bcrypt generators.

## Keywords

`hash api`, `sha256 api`, `md5 hash`, `bcrypt api`, `base64 encode api`, `hmac api`, `encoding api`, `password hash`, `crypto api`, `free hash api`
