# Social Video Downloader

Extract video download URLs and metadata from major social media platforms — no API keys required.

## Supported Platforms

- **TikTok** — Videos and metadata via oembed + page parsing
- **Twitter / X** — Videos via syndication API and embed fallback
- **Instagram** — Reels and video posts via embed page parsing
- **YouTube** — Videos and Shorts with streaming URL extraction
- **Facebook** — Videos via page HTML parsing

## Input

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `urls` | string[] | Yes | List of social media video URLs to process |
| `includeMetadata` | boolean | No | Include title, author, thumbnail, duration (default: true) |

### Example Input

```json
{
  "urls": [
    "https://www.youtube.com/watch?v=dQw4w9WgXcQ",
    "https://x.com/elonmusk/status/1234567890"
  ],
  "includeMetadata": true
}
```

## Output

Each URL produces one result in the dataset:

```json
{
  "url": "https://www.youtube.com/watch?v=dQw4w9WgXcQ",
  "success": true,
  "platform": "youtube",
  "title": "Rick Astley - Never Gonna Give You Up",
  "author": "Rick Astley",
  "thumbnail": "https://img.youtube.com/vi/dQw4w9WgXcQ/maxresdefault.jpg",
  "video_url": "https://...",
  "quality": "highest_available",
  "duration": 212
}
```

## Use Cases

- Social media monitoring and archiving
- Content aggregation and curation
- Video metadata collection for research
- Bulk video URL extraction

## Limitations

- Some platforms may require authentication for certain content
- YouTube video URLs may be signature-protected
- Instagram and Facebook heavily restrict scraping; results may vary
- Rate limiting is applied between requests to respect platform policies

## Pricing

Pay Per Event — charged per URL processed.
