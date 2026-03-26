# Social Video Downloader - Extract Videos from YouTube, TikTok, Instagram, X, Facebook

Extract video download URLs and metadata from 5 major social media platforms in one Actor run -- no API keys, no developer accounts required. The best free alternative to yt-dlp cloud wrappers, SaveFrom, SnapSave, and commercial video download APIs.

## Who Is This For?

- **Social media managers** -- Archive campaign videos and influencer content for reporting
- **Content creators** -- Save your own published videos across platforms for backup and repurposing
- **Market researchers** -- Collect video metadata (titles, authors, engagement) at scale for competitor analysis
- **Digital agencies** -- Monitor client brand mentions in video content across platforms
- **Data scientists** -- Build video metadata datasets for trend analysis and NLP research
- **Journalists** -- Archive newsworthy social media videos before they disappear

## Supported Platforms

| Platform | Content Types | Metadata Available |
|----------|--------------|-------------------|
| **YouTube** | Videos, Shorts, Live replays | Title, author, thumbnail, duration |
| **TikTok** | Videos (public) | Title, author, thumbnail, duration |
| **Twitter / X** | Video tweets, embedded videos | Title, author, thumbnail |
| **Instagram** | Reels, video posts | Title, author, thumbnail |
| **Facebook** | Video posts (public) | Title, author, thumbnail |

## Pricing -- Free to Start

| Tier | Cost | What You Get |
|------|------|-------------|
| **Free trial** | $0 | Apify free tier includes monthly compute credits |
| **Pay per URL** | ~$0.01-0.05/video | Only pay for actual Apify compute used |
| **vs. SaveFrom Pro** | Saves $9.99/mo | Bulk processing + API access included |
| **vs. Commercial APIs** | Saves $49-199/mo | No rate limits, no API key management |

## How It Compares to Alternatives

| Feature | This Actor (FREE) | yt-dlp (CLI) | SaveFrom ($9.99/mo) | RapidAPI Video APIs ($49+/mo) |
|---------|-------------------|-------------|---------------------|------------------------------|
| Platforms | 5 (YT, TikTok, IG, X, FB) | 1000+ | 5-10 | Usually 1-2 per API |
| Cloud-based | Yes (Apify) | No (local) | Web only | Yes |
| API/automation | Yes (Apify API) | CLI only | No | Yes |
| Bulk processing | Yes (unlimited URLs) | Yes | 1 at a time | Rate limited |
| Metadata extraction | Yes | Yes | Limited | Varies |
| Scheduling | Yes (Apify scheduler) | Cron (manual) | No | No |
| No install required | Yes | Python required | Browser extension | SDK required |
| Monthly cost | $0 (pay per run) | Free (self-hosted) | $9.99 | $49-199 |

## Quick Start (3 Steps)

1. **Click "Try for free"** on this Actor's page in Apify Store
2. **Paste video URLs** from YouTube, TikTok, Instagram, X, or Facebook
3. **Click "Start"** and get download URLs with metadata as JSON, CSV, or Excel

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
    "https://youtube.com/shorts/abc123",
    "https://x.com/elonmusk/status/1234567890",
    "https://www.tiktok.com/@user/video/1234567890",
    "https://www.instagram.com/reel/ABC123/"
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

Failed URLs return `success: false` with a descriptive error message -- no silent failures.

## Real-World Use Cases

### 1. Social Media Campaign Archiving
Schedule daily runs to archive all video content from tracked accounts. Export to cloud storage via Apify integrations for long-term preservation.

### 2. Influencer Content Monitoring
Track influencer deliverables by automatically extracting video metadata (title, views proxy, duration) from campaign URLs.

### 3. Competitive Video Intelligence
Bulk-extract competitor video metadata to analyze their content strategy -- video length, posting frequency, title patterns.

### 4. Content Repurposing Pipeline
Extract your own videos from multiple platforms, then feed into editing workflows. Combine with Apify scheduler for automated content backup.

### 5. Research Dataset Collection
Build datasets of video metadata (titles, authors, durations) across platforms for academic research, trend analysis, or training data.

## Limitations

- Private or age-restricted videos may fail (returns `success: false` with clear error)
- YouTube signature-protected streams may not resolve to direct download URLs
- Instagram and Facebook restrict scraping -- results depend on page availability
- Built-in rate limiting respects platform policies (configurable delay between requests)

## FAQ

**Q: Is YouTube Shorts supported?**
A: Yes. YouTube Shorts URLs (`youtube.com/shorts/...`) are handled identically to regular YouTube videos.

**Q: Why might some URLs fail?**
A: Private videos, age-restricted content, login-required pages, and heavily protected content may fail. The Actor always returns `success: false` with a specific error message so you know exactly what happened.

**Q: Can I schedule this to run regularly?**
A: Yes. Use Apify's built-in scheduler to run hourly, daily, or on any cron schedule. Perfect for automated video monitoring, content archiving, and competitive intelligence workflows.

**Q: Can I integrate this with my existing tools?**
A: Yes. Use Apify API or integrations (Zapier, Make, webhooks, Google Sheets) to feed results into any workflow. Available in Python, JavaScript, and Go SDKs.

**Q: Is this legal to use?**
A: This Actor extracts publicly available data. Ensure your usage complies with each platform's Terms of Service and applicable copyright laws. Common legitimate uses include archiving your own content, research, and journalistic purposes.

## Pricing

Pay Per Event -- charged per URL processed. Typical cost: $0.01-0.05 per video. Free Apify tier available for testing.
