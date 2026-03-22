# Free Placeholder Image API - Custom SVG/PNG with Text, Gradients, Presets

> **Free tier: 500 requests/month** | Generate placeholder images with text overlay, gradients, and category presets

Generate custom placeholder images in SVG or PNG format with configurable dimensions, colors, text overlay, gradients, and category presets (nature, tech, food, etc.). Perfect for prototyping and wireframes.

## Why Choose This Placeholder Image API?

- **SVG and PNG** -- vector or raster output
- **Custom text** -- add text overlay with custom font size and color
- **Gradients** -- linear gradient backgrounds
- **Category presets** -- nature, tech, food, abstract, business, and more
- **Any dimension** -- from 1x1 to 4000x4000 pixels
- **Free tier** -- 500 requests/month at $0

## Use Cases

- **Prototyping** -- fill wireframes and mockups with realistic placeholder images
- **Development** -- use as temporary images during frontend development
- **Design systems** -- generate consistent placeholder images across components
- **Documentation** -- create example images for API docs and tutorials
- **Testing** -- generate images of specific dimensions for responsive design tests

## Quick Start

```bash
curl -X GET "https://placeholder-image-api.t-mizuno27.workers.dev/image?width=400&height=300&text=Hello" \
  -H "X-RapidAPI-Key: YOUR_KEY" \
  -o placeholder.png
```

### Python Example

```python
import requests

url = "https://placeholder-image-api.p.rapidapi.com/image"
params = {"width": 800, "height": 600, "text": "Product Image", "category": "tech"}
headers = {"X-RapidAPI-Key": "YOUR_KEY", "X-RapidAPI-Host": "placeholder-image-api.p.rapidapi.com"}

response = requests.get(url, headers=headers, params=params)
with open("placeholder.png", "wb") as f:
    f.write(response.content)
```

## Pricing

| Plan | Price | Requests/mo | Rate Limit |
|------|-------|-------------|------------|
| Basic (FREE) | $0 | 500 | 1 req/sec |
| Pro | $5.99 | 50,000 | 10 req/sec |

## Alternative To

A free alternative to Placeholder.com, Lorem Picsum, and PlaceIMG.

## Keywords

`placeholder image api`, `dummy image api`, `placeholder generator`, `svg placeholder`, `wireframe images`, `free placeholder api`, `custom image generator`, `development placeholder`, `mockup images`, `test image api`
