# AI Blog Content Pipeline

Pick a topic from your queue → AI researches and writes a full SEO-optimized article → generates a featured image → publishes to WordPress as a draft.

## What This Workflow Does

1. **Topic queue** — Pulls the next pending topic from Google Sheets
2. **AI research** — Creates SEO-optimized outline with headings, FAQs, and internal link suggestions
3. **AI writing** — Generates a full 2,000-word article in HTML format
4. **Image generation** — DALL-E creates a professional featured image
5. **WordPress publish** — Posts as a draft for human review
6. **Queue update** — Marks topic as published with WordPress post ID

## Prerequisites

- n8n v1.30+, OpenAI API key, Google Sheets, WordPress (self-hosted or .com with API), Slack (optional)

## Quick Start

1. Import → Configure credentials
2. Create "Topic Queue" sheet with headers: topic, target_keyword, status, published_at, wp_post_id
3. Add topics with status "pending"
4. Run manually to test the first article
5. Activate the schedule (default: Mon/Wed/Fri at 7 AM)

## Customization

- **Word count**: Change `word_count_target` in Blog Config
- **Schedule**: Edit the cron expression in "Weekly Schedule"
- **Writing style**: Edit the system message in "Write Full Article"
- **Skip images**: Remove or disable the "Generate Featured Image" node
- **Ghost/Medium**: Replace WordPress node with their respective APIs

## Cost: ~$5-15/month (OpenAI text + DALL-E images)

## License
Personal and commercial use. Redistribution prohibited.
