# Placeholder Image API

Generate custom placeholder images with text overlay, gradients, and category presets. SVG and PNG output. Deployed on Cloudflare Workers.

## Endpoints

| Method | Path | Description |
|--------|------|-------------|
| GET | `/` | API info |
| GET | `/image` | Generate a placeholder image |
| GET | `/presets` | List available gradient and category presets |
| GET | `/categories` | List category presets with dimensions |

## Parameters

### GET /image

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `width` | integer | 300 | Image width (1-4000) |
| `height` | integer | 200 | Image height (1-4000) |
| `text` | string | WxH | Text overlay |
| `font_size` | integer | auto | Font size in px |
| `color` | string | ffffff | Text color (hex) |
| `bg` | string | cccccc | Background color (hex) |
| `gradient` | string | — | Gradient preset name |
| `category` | string | — | Category preset (avatar, banner, thumbnail, hero, etc.) |
| `format` | string | svg | Output format: svg or png |

## Gradient Presets

blue, sunset, ocean, forest, fire, purple, emerald, rose, midnight, gold

## Category Presets

| Category | Dimensions |
|----------|-----------|
| avatar | 150x150 |
| thumbnail | 320x180 |
| banner | 1200x300 |
| hero | 1920x600 |
| card | 400x300 |
| icon | 64x64 |
| social | 1200x630 |
| square | 500x500 |

## Examples

```bash
# Basic placeholder
curl "https://placeholder-image-api.miccho27.workers.dev/image?width=800&height=400&text=Hello"

# Gradient placeholder
curl "https://placeholder-image-api.miccho27.workers.dev/image?width=600&height=300&gradient=sunset&text=Preview"

# Category preset
curl "https://placeholder-image-api.miccho27.workers.dev/image?category=banner&text=My+Banner"
```

## Rate Limiting

20 requests per minute per IP.

## Development

```bash
npm install
npm run dev      # Local development
npm run deploy   # Deploy to Cloudflare
```
