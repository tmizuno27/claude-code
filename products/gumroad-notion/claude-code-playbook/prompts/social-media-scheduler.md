# Social Media Scheduler Prompt

## Objective
Generate a batch of social media posts (X/Twitter, LinkedIn, etc.) promoting your content and products, scheduled across optimal time slots.

## Required Context / Inputs
- `outputs/article-management.csv` — published articles to promote
- Product listings or landing page URLs
- Brand voice guidelines (optional)
- Posting schedule (times and frequency)

## Prompt

```
Create a week of social media content for my [PLATFORM] account.

**Account Details:**
- Platform: [X/Twitter / LinkedIn / both]
- Handle: @[YOUR_HANDLE]
- Brand voice: [professional / casual / educational / witty]
- Niche: [YOUR NICHE]
- Posting frequency: [X posts per day]
- Posting times: [e.g., 10:00, 14:00, 19:00 local time]

**Content Sources:**
- Read my published articles from outputs/article-management.csv
- Products to promote: [LIST PRODUCT URLS OR READ FROM listings/]
- Evergreen topics I want to be known for: [LIST 3-5 TOPICS]

**Generate:**

1. **Content Mix** (per week):
   - 40% Value posts (tips, insights, how-tos — no links)
   - 30% Content promotion (link to articles with compelling hook)
   - 20% Product promotion (soft sell with problem-solution framing)
   - 10% Engagement (questions, polls, hot takes)

2. **For each post:**
   - Post text (within platform character limits)
   - Post type: value / promotion / product / engagement
   - Scheduled time
   - Hashtags (3-5 relevant ones)
   - Link (if applicable)
   - Thread indicator (if it's a thread, include all parts)

3. **Thread content** (2-3 threads per week):
   - Take a complex topic from an article and break it into 5-8 tweet-sized insights
   - First tweet must hook attention (contrarian take, surprising stat, or question)
   - Last tweet links to the full article

4. **Output:**
   - Save as outputs/social/[platform]-week-[date].csv
   - Columns: date, time, post_text, type, hashtags, link, thread_part
   - Also output a human-readable preview version

Week starting: [DATE]
```

## Expected Output
- `outputs/social/[platform]-week-[date].csv` — scheduled posts
- Console preview of the week's content

## Example Usage

```
Platform: X/Twitter
Handle: @mybusinesshandle
Brand voice: educational but approachable
Niche: digital business automation
Posting frequency: 3 posts per day
Posting times: 10:00, 14:00, 19:00 PYT
Week starting: 2026-03-31
```

## Tips
- Generate 2-4 weeks ahead so you always have a buffer
- Value posts build audience; product posts monetize it. Never skip value posts.
- Repurpose article sections as standalone insights — you already wrote the content
- Track engagement per post type and adjust the mix based on data
