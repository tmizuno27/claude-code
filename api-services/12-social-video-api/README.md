# Social Video API

Cloudflare Workers API that extracts video download URLs from social media platforms by parsing their public HTML pages.

## Supported Platforms

| Platform | Method |
|----------|--------|
| TikTok | oembed + page HTML (`__UNIVERSAL_DATA_FOR_REHYDRATION__`, `SIGI_STATE`) |
| Twitter/X | Syndication API + embed page |
| Instagram | Embed page (`/p/{shortcode}/embed/`) |
| YouTube | oembed + watch page (`ytInitialPlayerResponse`) |
| Facebook | Page HTML (og tags, `playable_url`, `sd_src`/`hd_src`) |

## Endpoints

| Method | Path | Description |
|--------|------|-------------|
| GET | `/` | API info |
| GET | `/download?url=<video_url>` | Extract video download URL |
| GET | `/info?url=<video_url>` | Get metadata only (no download URL) |
| GET | `/platforms` | List supported platforms |

## Rate Limits

20 requests per minute per IP (configurable via `wrangler.toml` vars).

## Development

```bash
npm install
npm run dev      # Local dev server
npm run deploy   # Deploy to Cloudflare Workers
```

## Limitations

- Platforms frequently change their HTML structure, which may break extractors
- Some platforms (especially Instagram and Facebook) heavily restrict scraping and may require authentication
- YouTube video URLs are often signature-protected and may not be directly downloadable
- No external paid APIs are used; all extraction is from publicly accessible pages
- Rate limiting is per-isolate (in-memory), not globally distributed

## OpenAPI Spec

See `openapi.json` for the full OpenAPI 3.0.3 specification (RapidAPI compatible).
