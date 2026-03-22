# Free Social Video Download API - Extract Video URLs from Social Platforms

> **Free tier: 500 requests/month** | Extract direct download URLs from social media videos

Extract video download URLs from YouTube, TikTok, Instagram, Twitter/X, and more by parsing public HTML pages. No scraping libraries or headless browsers -- pure HTTP parsing on Cloudflare Workers.

## Why Choose This Social Video API?

- **Multi-platform** -- YouTube, TikTok, Instagram, Twitter/X, Facebook, Reddit
- **Direct URLs** -- returns direct video file URLs for downloading
- **Multiple qualities** -- extracts all available video quality options
- **No browser automation** -- fast HTML parsing, no Puppeteer overhead
- **Free tier** -- 500 requests/month at $0

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

url = "https://social-video-api.p.rapidapi.com/extract"
params = {"url": "https://www.tiktok.com/@user/video/123"}
headers = {"X-RapidAPI-Key": "YOUR_KEY", "X-RapidAPI-Host": "social-video-api.p.rapidapi.com"}

data = requests.get(url, headers=headers, params=params).json()
print(f"Download URL: {data['video_url']}")
```

## Pricing

| Plan | Price | Requests/mo | Rate Limit |
|------|-------|-------------|------------|
| Basic (FREE) | $0 | 500 | 1 req/sec |
| Pro | $9.99 | 50,000 | 10 req/sec |

## Alternative To

A free alternative to RapidAPI video downloader APIs, SaveFrom, and yt-dlp API wrappers.

## Keywords

`video download api`, `social video api`, `tiktok download api`, `youtube video url`, `instagram video download`, `twitter video api`, `free video api`, `social media downloader`, `video extractor api`, `video url extractor`
