# Social Media Content Factory

AI generates a full week of social media posts (Twitter, LinkedIn, Instagram) with DALL-E images, informed by trending topics and industry news. Saves to your content calendar.

## What This Workflow Does

1. **Fetches trends** — Pulls trending topics from Twitter API and industry RSS feeds
2. **AI content plan** — Generates 7 platform-specific posts with varied content pillars
3. **Image generation** — Creates accompanying images via DALL-E 3
4. **Content calendar** — Saves everything to Google Sheets for review
5. **Slack notification** — Alerts your team when the weekly plan is ready

## Prerequisites

- n8n v1.30+, OpenAI API key, Twitter API (optional), Google Sheets, Slack (optional)

## Quick Start

1. Import `workflow.json` → Configure credentials
2. Edit "Content Config" node with your brand info
3. Add your industry RSS feed URL
4. Create a "Content Calendar" sheet with headers: week_of, day, platform, pillar, post_text, hashtags, best_time, cta, image_url, status, created_at
5. Run manually to test, then activate the weekly schedule

## Customization

- **Post frequency**: Change `posts_per_week` in config
- **Platforms**: Add/remove from the platforms array
- **Content pillars**: Modify to match your strategy
- **Image style**: Edit the DALL-E prompt in "Generate Image" node
- **Auto-posting**: Add Twitter/LinkedIn API nodes to post directly instead of saving to calendar

## Cost: ~$10-20/month (OpenAI + DALL-E images)

## License
Personal and commercial use. Redistribution prohibited.
