# Content Repurposer Prompt

## Objective
Take existing content (blog article, guide, report) and repurpose it into multiple formats: social media threads, email newsletters, video scripts, infographics outlines, and short-form posts.

## Required Context / Inputs
- Source content (article URL or file path)
- Target platforms
- Brand voice

## Prompt

```
Repurpose the following content into multiple formats.

**Source Content:**
- File: [PATH TO ARTICLE or URL]
- Original format: [blog post / guide / report / podcast transcript]

**Target Formats:**

1. **X/Twitter Thread** (8-12 tweets):
   - Hook tweet that stands alone (contrarian or surprising)
   - Key insights broken into tweet-sized chunks
   - Final tweet with CTA and link to full article

2. **LinkedIn Post** (1300 chars max):
   - Professional tone
   - Personal insight or story angle
   - End with question to drive engagement

3. **Email Newsletter Segment** (200-300 words):
   - Casual, personal tone
   - One key takeaway from the article
   - Link to full article for details

4. **YouTube/Video Script Outline** (3-5 min):
   - Hook (first 10 seconds)
   - Key points with timestamps
   - CTA at the end

5. **Infographic Outline**:
   - Title
   - 5-7 data points or steps
   - Visual layout suggestion

6. **Short-form Quote Cards** (5 cards):
   - Extract quotable lines from the content
   - Each under 100 characters
   - Suitable for Instagram/Pinterest graphics

**Output:**
- Save all formats to outputs/repurposed/[article-slug]/
- One file per format
- Include a summary.md listing all generated assets

Source: [YOUR CONTENT PATH]
Brand voice: [professional / casual / educational]
```

## Expected Output
- `outputs/repurposed/[article-slug]/` with all format files

## Tips
- One article can generate 15+ pieces of content across platforms
- Schedule repurposed content over 2-3 weeks (don't dump everything at once)
- The thread format often outperforms the original article on social media
