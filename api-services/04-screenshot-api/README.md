# Website Screenshot API

Cloudflare Worker that captures website screenshots via [thum.io](https://www.thum.io/) with caching, rate limiting, and CORS support.

## Endpoint

```
GET /screenshot?url=https://example.com
```

### Parameters

| Parameter   | Type    | Default | Description                          |
|-------------|---------|---------|--------------------------------------|
| `url`       | string  | —       | **Required.** Target URL to capture  |
| `width`     | integer | 1280    | Viewport width (320–3840)            |
| `height`    | integer | 720     | Viewport height (0 = full page)      |
| `format`    | string  | png     | `png` or `jpeg`                      |
| `quality`   | integer | 80      | JPEG quality (1–100)                 |
| `delay`     | integer | 0       | Wait ms before capture (max 5000)    |
| `full_page` | boolean | false   | Capture full scrollable page         |

### Response

Returns the screenshot image directly (`image/png` or `image/jpeg`).

### Examples

```bash
# Basic screenshot
curl "https://screenshot-api.t-mizuno27.workers.dev/screenshot?url=https://example.com" -o screenshot.png

# Full page JPEG
curl "https://screenshot-api.t-mizuno27.workers.dev/screenshot?url=https://example.com&full_page=true&format=jpeg&quality=90" -o full.jpg

# Custom viewport
curl "https://screenshot-api.t-mizuno27.workers.dev/screenshot?url=https://example.com&width=375&height=812" -o mobile.png
```

## Deploy

```bash
npm install
npx wrangler deploy
```

## Configuration

Environment variables in `wrangler.toml`:

- `CACHE_TTL` — Cache duration in seconds (default: 3600)
- `RATE_LIMIT_MAX` — Max requests per window (default: 60)
- `RATE_LIMIT_WINDOW` — Window in seconds (default: 60)
