# QR Code Generator API

A high-performance QR Code Generator running on Cloudflare Workers. Pure JavaScript implementation with zero Node.js dependencies.

## Quick Start

```bash
npm install
npm run dev      # Local development
npm run deploy   # Deploy to Cloudflare
```

## API Reference

### `GET /generate`

Generate a QR code image from text or URL.

#### Parameters

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `text` | string | Yes | — | Text or URL to encode (max 4296 chars) |
| `size` | integer | No | 300 | Image size in pixels (10–1000) |
| `format` | string | No | `png` | Output format: `png`, `svg`, `base64` |
| `color` | string | No | `000000` | Foreground color (6-digit hex, no `#`) |
| `bgcolor` | string | No | `ffffff` | Background color (6-digit hex, no `#`) |
| `error_correction` | string | No | `M` | Error correction: `L` (7%), `M` (15%), `Q` (25%), `H` (30%) |

#### Examples

```
# PNG image (default)
GET /generate?text=https://example.com

# SVG format
GET /generate?text=hello&format=svg

# Base64 JSON response
GET /generate?text=hello&format=base64

# Custom colors and size
GET /generate?text=hello&size=500&color=1a73e8&bgcolor=f0f0f0

# High error correction
GET /generate?text=hello&error_correction=H
```

#### Response Formats

**PNG** (`format=png`): Returns `image/png` binary.

**SVG** (`format=svg`): Returns `image/svg+xml` text.

**Base64** (`format=base64`): Returns JSON:
```json
{
  "data": "<base64-string>",
  "data_uri": "data:image/png;base64,<base64-string>",
  "mime_type": "image/png",
  "size": 1234
}
```

### `GET /`

Returns API info and available parameters as JSON.

## Rate Limiting

Default: 60 requests per minute per IP. Response headers:

- `X-RateLimit-Limit` — Max requests per window
- `X-RateLimit-Remaining` — Remaining requests
- `X-RateLimit-Reset` — Seconds until window resets

Exceeding the limit returns `429 Too Many Requests` with a `Retry-After` header.

## Error Handling

All errors return JSON with appropriate HTTP status codes:

| Status | Meaning |
|--------|---------|
| 400 | Bad request (missing/invalid parameters) |
| 404 | Endpoint not found |
| 405 | Method not allowed |
| 429 | Rate limit exceeded |

```json
{
  "error": "Missing required parameter: text",
  "status": 400
}
```

## CORS

All responses include CORS headers. The API can be called directly from browser JavaScript.

## Configuration

Environment variables in `wrangler.toml`:

| Variable | Default | Description |
|----------|---------|-------------|
| `RATE_LIMIT_PER_MINUTE` | 60 | Rate limit per IP |
| `MAX_QR_SIZE` | 1000 | Maximum image size |
| `DEFAULT_QR_SIZE` | 300 | Default image size |

## Architecture

- Pure JavaScript QR code encoder (supports versions 1–40, all EC levels)
- Reed-Solomon error correction over GF(256)
- Minimal PNG encoder (uncompressed deflate, no zlib dependency)
- SVG output as direct XML text
- In-memory per-instance rate limiting
- Zero external dependencies at runtime
