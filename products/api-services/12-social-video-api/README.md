# Free Social Video Download API - Extract Video URLs from Social Platforms

> **Free tier: 500 requests/month** | Extract direct download URLs from social media videos

Extract video download URLs from YouTube, TikTok, Instagram, Twitter/X, and more by parsing public HTML pages. No scraping libraries or headless browsers -- pure HTTP parsing on Cloudflare Workers.

## Getting Started in 30 Seconds

1. Subscribe on [RapidAPI](https://rapidapi.com/miccho27-5OJaGGbBiO/api/social-video-api) (free plan available)
2. Copy your API key
3. Extract your first video URL:

```bash
curl -X GET "https://social-video-api.p.rapidapi.com/download?url=https://www.youtube.com/watch?v=dQw4w9WgXcQ" \
  -H "X-RapidAPI-Key: YOUR_KEY" \
  -H "X-RapidAPI-Host: social-video-api.p.rapidapi.com"
```

## How It Compares

| Feature | This API | SaveFrom | yt-dlp wrappers | RapidAPI competitors |
|---------|----------|----------|-----------------|---------------------|
| Free tier | 500 req/mo | Web only | Self-hosted | 50-100 req/mo |
| Platforms | 6 (YT, TikTok, IG, X, FB, Reddit) | 3-4 | 1,000+ (local) | 1-3 typically |
| Multiple qualities | Yes | Limited | Yes | Varies |
| Video metadata | Yes (title, author, thumbnail, duration) | No | Yes | Varies |
| No browser automation | Yes (pure HTTP) | N/A | Yes | Often Puppeteer |
| Edge latency | Sub-500ms (CF Workers) | N/A | Self-hosted | Variable |
| API-first | Yes | No | No (CLI) | Yes |

## Why Choose This Social Video API?

- **Multi-platform** -- YouTube, TikTok, Instagram, Twitter/X, Facebook, Reddit
- **Direct URLs** -- returns direct video file URLs for downloading
- **Multiple qualities** -- extracts all available video quality options
- **No browser automation** -- fast HTML parsing, no Puppeteer overhead
- **Free tier** -- 500 requests/month at $0

## Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/download` | GET | Extract video download URL from a social media URL |
| `/info` | GET | Get video metadata without download URL |
| `/platforms` | GET | List supported platforms |

## Use Cases

- **Video downloaders** -- build video download tools and browser extensions
- **Social media managers** -- archive and repurpose social video content
- **Content aggregators** -- embed social videos in your platform
- **Data analysis** -- collect video metadata for research

## Quick Start

```bash
curl -X GET "https://social-video-api.t-mizuno27.workers.dev/extract?url=https://www.tiktok.com/@user/video/123" \
  -H "X-RapidAPI-Key: YOUR_KEY"
```

### Python Example

```python
import requests

url = "https://social-video-api.p.rapidapi.com/download"
params = {"url": "https://www.youtube.com/watch?v=dQw4w9WgXcQ"}
headers = {"X-RapidAPI-Key": "YOUR_KEY", "X-RapidAPI-Host": "social-video-api.p.rapidapi.com"}

data = requests.get(url, headers=headers, params=params).json()
print(f"Title: {data['title']}")
print(f"Download URL: {data['video_url']}")
```

### Node.js Example

```javascript
const axios = require("axios");

const { data } = await axios.get(
  "https://social-video-api.p.rapidapi.com/download",
  {
    params: { url: "https://www.tiktok.com/@user/video/123" },
    headers: {
      "X-RapidAPI-Key": "YOUR_KEY",
      "X-RapidAPI-Host": "social-video-api.p.rapidapi.com",
    },
  }
);

console.log(`Download: ${data.video_url}`);
```

## FAQ

**Q: Which platforms are supported?**
A: YouTube, TikTok, Instagram, Twitter/X, Facebook, and Reddit. Use the `/platforms` endpoint for the latest list.

**Q: Does it work with private/restricted videos?**
A: No. Only publicly accessible videos can be processed. Private or age-restricted content will return an error.

**Q: Are YouTube Shorts supported?**
A: Yes. YouTube Shorts URLs are fully supported and treated like regular YouTube videos.

**Q: What video qualities are available?**
A: All qualities available from the platform are returned. Typically includes 360p, 480p, 720p, and 1080p options.

## Pricing

| Plan | Price | Requests/mo | Rate Limit |
|------|-------|-------------|------------|
| Basic (FREE) | $0 | 500 | 1 req/sec |
| Pro | $9.99 | 50,000 | 10 req/sec |

## Alternative To

A free alternative to RapidAPI video downloader APIs, SaveFrom, and yt-dlp API wrappers. Multi-platform support with a simple REST API.


## Also From This Publisher

Build powerful workflows by combining APIs:

| API | Why Combine? |
|-----|-------------|
| **Screenshot API** | Capture video page thumbnails |
| **Link Preview API** | Extract video metadata and OG tags |
| **Trends API** | Find trending videos to download |
| **AI Text API** | Generate descriptions for downloaded videos |

> All APIs include a free tier. Subscribe to one, discover the full toolkit on [our RapidAPI profile](https://rapidapi.com/miccho27-5OJaGGbBiO).

## Keywords

`video download api`, `social video api`, `tiktok download api`, `youtube video url`, `instagram video download`, `twitter video api`, `free video api`, `social media downloader`, `video extractor api`, `video url extractor`
