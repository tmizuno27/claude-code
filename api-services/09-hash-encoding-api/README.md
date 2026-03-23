# Free Hash & Encoding API - SHA256, MD5, Bcrypt, Base64, HMAC

> **Free tier: 500 requests/month** | Hashing, encoding, and cryptographic operations via Web Crypto API

Hash text with SHA-256/384/512, MD5, bcrypt. Encode/decode Base64, URL encoding, hex. Generate HMAC signatures and cryptographic random strings. Zero external dependencies -- uses Web Crypto API.

## Getting Started in 30 Seconds

1. Subscribe on [RapidAPI](https://rapidapi.com/miccho27-5OJaGGbBiO/api/hash-encoding-api) (free plan available)
2. Copy your API key
3. Hash your first string:

```bash
curl -X POST "https://hash-encoding-api.p.rapidapi.com/hash" \
  -H "Content-Type: application/json" \
  -H "X-RapidAPI-Key: YOUR_KEY" \
  -H "X-RapidAPI-Host: hash-encoding-api.p.rapidapi.com" \
  -d '{"text": "hello world", "algorithm": "sha256"}'
```

## How It Compares

| Feature | This API | CryptoJS Online | HashAPI | bcrypt-generator.com |
|---------|----------|----------------|---------|---------------------|
| Free tier | 500 req/mo | Web only | Web only | Web only |
| API access | Yes (REST) | No | Limited | No |
| SHA-256/384/512 | Yes | Yes | Yes | No |
| MD5 | Yes | Yes | Yes | No |
| Bcrypt | Yes (configurable rounds) | No | No | Yes (web) |
| HMAC signatures | Yes (SHA-256/512) | No | No | No |
| Base64/URL/Hex encoding | Yes | No | No | No |
| Random string generation | Yes (crypto-secure) | No | No | No |
| Edge latency | Sub-50ms (CF) | N/A | N/A | N/A |

## Why Choose This Hash & Encoding API?

- **Multiple algorithms** -- SHA-256, SHA-384, SHA-512, MD5, bcrypt
- **HMAC support** -- generate HMAC signatures for webhook verification
- **Bcrypt** -- password hashing with configurable salt rounds
- **Encoding** -- Base64, URL encoding, hex encoding/decoding
- **Random generation** -- cryptographically secure random strings and UUIDs
- **Free tier** -- 500 requests/month at $0

## Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/hash` | POST | Hash text (SHA-256/384/512, MD5) |
| `/hash/file` | POST | Hash file content |
| `/hmac` | POST | Generate HMAC signature |
| `/encode` | POST | Encode text (Base64, URL, hex) |
| `/decode` | POST | Decode encoded text |
| `/bcrypt` | POST | Bcrypt hash with salt rounds |
| `/compare` | POST | Compare bcrypt hash with plain text |
| `/random` | GET | Generate cryptographic random string/UUID |

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

### Node.js Example

```javascript
const axios = require("axios");

const { data } = await axios.post(
  "https://hash-encoding-api.p.rapidapi.com/hmac",
  { text: "webhook-payload", key: "my-secret", algorithm: "sha256" },
  {
    headers: {
      "X-RapidAPI-Key": "YOUR_KEY",
      "X-RapidAPI-Host": "hash-encoding-api.p.rapidapi.com",
    },
  }
);

console.log(`HMAC: ${data.hmac}`);
```

## FAQ

**Q: Is bcrypt hashing slow?**
A: By design, yes. Bcrypt is intentionally slow to prevent brute-force attacks. Higher salt rounds = more secure but slower. 10-12 rounds is recommended for most use cases.

**Q: Can I verify a bcrypt password?**
A: Yes. Use the `/compare` endpoint with the plain text and the bcrypt hash to verify.

**Q: What HMAC algorithms are supported?**
A: SHA-256 and SHA-512. HMAC is commonly used for webhook signature verification (Stripe, GitHub, etc.).

**Q: Are the random strings cryptographically secure?**
A: Yes. They use the Web Crypto API's `getRandomValues()`, which is cryptographically secure.

## Pricing

| Plan | Price | Requests/mo | Rate Limit |
|------|-------|-------------|------------|
| Basic (FREE) | $0 | 500 | 1 req/sec |
| Pro | $5.99 | 50,000 | 10 req/sec |

## Alternative To

A free alternative to CryptoJS online tools, HashAPI, and bcrypt generators. The only REST API that combines hashing, encoding, HMAC, bcrypt, and random generation in one service.

## Keywords

`hash api`, `sha256 api`, `md5 hash`, `bcrypt api`, `base64 encode api`, `hmac api`, `encoding api`, `password hash`, `crypto api`, `free hash api`
