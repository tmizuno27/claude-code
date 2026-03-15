# Hash & Encoding API

Cloudflare Worker for hashing, HMAC, encoding/decoding, bcrypt, and cryptographic random generation. Zero external dependencies — uses Web Crypto API and pure JS implementations for MD5 and bcrypt.

## Base URL

```
https://hash-encoding-api.t-mizuno27.workers.dev
```

## Endpoints

### POST /hash
Generate a hash from text.

```json
{"text": "hello", "algorithm": "sha256"}
```
Algorithms: `md5`, `sha1`, `sha256`, `sha384`, `sha512`

### POST /hash/file
Hash a file (base64-encoded).

```json
{"data": "SGVsbG8gV29ybGQ=", "algorithm": "sha256"}
```

### POST /hmac
Generate HMAC signature.

```json
{"text": "hello", "key": "secret", "algorithm": "sha256"}
```

### POST /encode
Encode text.

```json
{"text": "hello world", "format": "base64"}
```
Formats: `base64`, `url`, `html`, `hex`

### POST /decode
Decode text.

```json
{"text": "aGVsbG8gd29ybGQ=", "format": "base64"}
```

### POST /bcrypt
Bcrypt hash a password.

```json
{"text": "password", "rounds": 10}
```

### POST /compare
Compare text against bcrypt hash.

```json
{"text": "password", "hash": "$2b$10$..."}
```

### GET /random
Generate cryptographically secure random bytes.

```
GET /random?length=32&format=hex
```
Formats: `hex`, `base64`. Max length: 1024.

## Deploy

```bash
npm install
npx wrangler deploy
```

## Development

```bash
npx wrangler dev
```
