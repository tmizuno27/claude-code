# Free Placeholder Image API - Custom SVG/PNG with Text, Gradients, Presets

> **Free tier: 500 requests/month** | Generate placeholder images with text overlay, gradients, and category presets

Generate custom placeholder images in SVG or PNG format with configurable dimensions, colors, text overlay, gradients, and category presets (nature, tech, food, etc.). Perfect for prototyping and wireframes.

## Getting Started in 30 Seconds

1. Subscribe on [RapidAPI](https://rapidapi.com/miccho27-5OJaGGbBiO/api/placeholder-image-api) (free plan available)
2. Copy your API key
3. Generate your first placeholder:

```bash
curl -X GET "https://placeholder-image-api.p.rapidapi.com/image?width=400&height=300&text=Hello" \
  -H "X-RapidAPI-Key: YOUR_KEY" \
  -H "X-RapidAPI-Host: placeholder-image-api.p.rapidapi.com" \
  -o placeholder.png
```

## How It Compares

| Feature | This API | Placeholder.com | Lorem Picsum | PlaceIMG |
|---------|----------|----------------|-------------|----------|
| Free tier | 500 req/mo | Unlimited (no API) | Unlimited (no API key) | Shutdown |
| API key management | Yes (RapidAPI) | No | No | N/A |
| Custom text overlay | Yes | Yes | No | No |
| Gradient backgrounds | Yes | No | No | No |
| Category presets | Yes (nature, tech, food, etc.) | No | Random photos | Categories |
| SVG output | Yes | No | No | No |
| Custom colors | Yes (fg + bg) | Limited | No | No |
| Rate limiting headers | Yes (documented) | Undocumented | Undocumented | N/A |

## Why Choose This Placeholder Image API?

- **SVG and PNG** -- vector or raster output
- **Custom text** -- add text overlay with custom font size and color
- **Gradients** -- linear gradient backgrounds
- **Category presets** -- nature, tech, food, abstract, business, and more
- **Any dimension** -- from 1x1 to 4000x4000 pixels
- **Free tier** -- 500 requests/month at $0

## Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/image` | GET | Generate a placeholder image |
| `/gradients` | GET | List available gradient presets |
| `/categories` | GET | List available category presets |

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

### Node.js Example

```javascript
const axios = require("axios");
const fs = require("fs");

const response = await axios.get(
  "https://placeholder-image-api.p.rapidapi.com/image",
  {
    params: { width: 1200, height: 630, text: "OG Image", gradient: "sunset" },
    headers: {
      "X-RapidAPI-Key": "YOUR_KEY",
      "X-RapidAPI-Host": "placeholder-image-api.p.rapidapi.com",
    },
    responseType: "arraybuffer",
  }
);

fs.writeFileSync("og-image.png", response.data);
```

## FAQ

**Q: What image formats are supported?**
A: PNG (raster) and SVG (vector). Use the `format` parameter to choose. SVG is ideal for responsive designs.

**Q: What is the maximum image size?**
A: Up to 4000x4000 pixels. Larger sizes may increase response time.

**Q: Can I use gradient backgrounds?**
A: Yes. Use the `gradient` parameter with preset names (sunset, ocean, forest, etc.) or specify custom colors.

**Q: Are category preset images photos or illustrations?**
A: They are styled placeholder designs with category-specific color palettes and patterns, not actual photos.

## Pricing

| Plan | Price | Requests/mo | Rate Limit |
|------|-------|-------------|------------|
| Basic (FREE) | $0 | 500 | 1 req/sec |
| Pro | $5.99 | 50,000 | 10 req/sec |

## Alternative To

A free alternative to Placeholder.com, Lorem Picsum, and PlaceIMG. The only placeholder API with gradients, SVG output, and category presets.


## Also From This Publisher

Build powerful workflows by combining APIs:

| API | Why Combine? |
|-----|-------------|
| **QR Code API** | Generate QR codes for prototyping |
| **Screenshot API** | Capture real screenshots to replace placeholders |
| **PDF Generator API** | Include placeholder images in PDF mockups |
| **JSON Formatter API** | Mock API responses with placeholder data |

> All APIs include a free tier. Subscribe to one, discover the full toolkit on [our RapidAPI profile](https://rapidapi.com/miccho27-5OJaGGbBiO).

## Keywords

`placeholder image api`, `dummy image api`, `placeholder generator`, `svg placeholder`, `wireframe images`, `free placeholder api`, `custom image generator`, `development placeholder`, `mockup images`, `test image api`
