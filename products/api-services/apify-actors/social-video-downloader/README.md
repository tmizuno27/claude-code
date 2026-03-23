# Social Video Downloader - Extract Videos from YouTube, TikTok, Instagram, X

Extract video download URLs and metadata from major social media platforms -- no API keys required. A free alternative to yt-dlp wrappers and commercial video download APIs.

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

## Why Choose This Actor?

- **5 platforms** in one Actor -- YouTube, TikTok, Instagram, Twitter/X, Facebook
- **No API keys needed** -- uses public page parsing, no developer accounts required
- **Full metadata** -- title, author, thumbnail, duration alongside download URLs
- **Bulk processing** -- pass dozens of URLs and get all results in one dataset
- **Respectful scraping** -- built-in rate limiting between requests

## FAQ

**Q: Is YouTube Shorts supported?**
A: Yes. YouTube Shorts URLs are handled the same as regular YouTube videos.

**Q: Why might some URLs fail?**
A: Private videos, age-restricted content, and heavily protected pages may fail. The Actor returns `success: false` with an error message for failed items.

**Q: Can I schedule this to run regularly?**
A: Yes. Use Apify's built-in scheduler to run this Actor hourly, daily, or on any cron schedule for automated video monitoring.

## Pricing

Pay Per Event -- charged per URL processed.
