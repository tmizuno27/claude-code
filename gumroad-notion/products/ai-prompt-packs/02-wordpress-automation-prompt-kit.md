# WordPress Automation Prompt Kit
## API Calls + Prompts for Automated Publishing — $29

> A complete WordPress automation toolkit combining AI prompts with ready-to-use API code. Built from a production system that publishes 3+ articles per week on autopilot.

---

## SECTION 1: WordPress REST API Foundations (10 Prompts + Code)

### Prompt 1: WordPress Site Setup Audit
```
I want to automate my WordPress site using the REST API.

Site details:
- URL: [SITE_URL]
- Theme: [THEME_NAME]
- SEO plugin: [Rank Math / Yoast / None]
- Hosting: [HOSTING_PROVIDER]

Generate a complete setup checklist:
1. [ ] Enable REST API (verify with curl [SITE_URL]/wp-json/wp/v2/)
2. [ ] Create Application Password (Users → Profile → Application Passwords)
3. [ ] Test authentication
4. [ ] List available endpoints
5. [ ] Check rate limits
6. [ ] Verify CORS settings (if calling from external scripts)
7. [ ] Set up error logging

For each step, provide:
- The exact curl command to test
- Expected successful response
- Common error and fix
- Python requests equivalent code
```
**Usage**: Verify your WordPress site is ready for automation.
**Expected output**: Complete setup checklist with test commands.
**Tip**: Application Passwords are the recommended auth method since WordPress 5.6.

---

### Prompt 2: Authentication & Connection Manager
```
Generate a reusable Python class for WordPress REST API authentication and connection management.

Requirements:
- Support Basic Auth (Application Password)
- Configurable base URL, credentials from environment variables or config file
- Automatic retry with exponential backoff (3 retries)
- Request logging (timestamp, endpoint, status code)
- Rate limiting (configurable requests per second)
- Timeout handling (30 second default)
- Response validation helper
- Connection health check method

Config file format (JSON):
{
    "wordpress": {
        "rest_api_url": "[SITE_URL]/wp-json/wp/v2",
        "username": "[USERNAME]",
        "app_password": "[APP_PASSWORD]"
    }
}

Include:
- The complete Python class
- Usage examples for GET, POST, PUT, DELETE
- Error handling for common HTTP status codes (401, 403, 404, 429, 500)
- Unit test template
```
**Usage**: Foundation class for all WordPress automation scripts.
**Expected output**: Production-ready Python connection manager.
**Tip**: Store credentials in a separate secrets.json file excluded from version control.

---

### Prompt 3: Bulk Article Publisher
```
Generate a Python script that publishes articles to WordPress in bulk from Markdown files.

Input: A directory of .md files with YAML frontmatter:
---
title: "Article Title"
keyword: "target keyword"
category: "category-slug"
tags: ["tag1", "tag2"]
status: "draft"
---

# Article content in Markdown...

The script should:
1. Scan [DIRECTORY] for .md files
2. Parse YAML frontmatter + Markdown body
3. Convert Markdown to WordPress HTML (handling: headings, lists, tables, links, bold/italic, blockquotes, code blocks)
4. Create or update WordPress posts via REST API:
   - Map category slugs to category IDs (fetch once, cache)
   - Create tags if they don't exist
   - Set SEO meta fields (Rank Math or Yoast)
   - Set featured image if specified
5. Log results: success/failure per file
6. Move processed files to a "published" directory
7. Generate a JSON log: [{filename, post_id, url, status, timestamp}]

Include:
- Dry-run mode (--dry-run flag)
- Resume capability (skip already-published files)
- Rate limiting between API calls
- Complete error handling

Provide the full script with clear comments.
```
**Usage**: Publish multiple articles in one run.
**Expected output**: Complete bulk publishing script (~200 lines).
**Tip**: Always test with --dry-run first to verify content formatting.

---

### Prompt 4: Category & Tag Manager
```
Generate prompts and Python code for WordPress category/tag management:

## Category Structure Planner Prompt:
Given my blog niche "[NICHE]" with these content pillars:
- Pillar 1: [PILLAR_1]
- Pillar 2: [PILLAR_2]
- Pillar 3: [PILLAR_3]

Design the optimal category hierarchy:
- Parent categories (max 5-7)
- Child categories (max 3-5 per parent)
- Category descriptions (SEO-optimized, 150 words each)
- Category slugs (URL-friendly)

## Python Code:
```python
# WordPress Category & Tag Manager
# - List all categories with post counts
# - Create category hierarchy from JSON definition
# - Bulk assign categories to existing posts
# - Merge duplicate tags
# - Delete unused tags (0 posts)
# - Export category/tag structure to JSON

import requests
from base64 import b64encode

class WPTaxonomyManager:
    def __init__(self, api_url, username, app_password):
        self.api_url = api_url
        self.auth = b64encode(f"{username}:{app_password}".encode()).decode()
        self.headers = {"Authorization": f"Basic {self.auth}"}

    def list_categories(self):
        """Fetch all categories with post counts."""
        # [FULL IMPLEMENTATION]
        pass

    def create_category_tree(self, tree_json):
        """Create categories from a hierarchical JSON definition."""
        # [FULL IMPLEMENTATION]
        pass

    def assign_categories_bulk(self, assignments):
        """Bulk assign categories: [{post_id, category_ids}]"""
        # [FULL IMPLEMENTATION]
        pass

    def cleanup_tags(self, min_posts=1):
        """Delete tags with fewer than min_posts."""
        # [FULL IMPLEMENTATION]
        pass

    def export_structure(self, output_file):
        """Export full taxonomy structure to JSON."""
        # [FULL IMPLEMENTATION]
        pass
```

Provide complete implementation for all methods.
```
**Usage**: Set up and maintain your site's taxonomy.
**Expected output**: Category strategy + management code.
**Tip**: Flat category structures (2 levels max) perform better for SEO than deep hierarchies.

---

### Prompt 5: Featured Image Automation
```
Generate a Python script for WordPress featured image automation:

Features:
1. **Upload image to WordPress media library**
   - Accept local file path or URL
   - Set alt text, title, caption, description
   - Return media ID

2. **Generate placeholder images** (using Pillow)
   - Create [WIDTH]x[HEIGHT] images with:
     - Gradient background (customizable colors)
     - Title text overlay
     - Category badge
     - Site watermark
   - Save as WebP for optimal file size

3. **Bulk assign featured images**
   - Match images to posts by keyword/title
   - Update posts that lack featured images

4. **Image optimization before upload**
   - Resize to max dimensions
   - Convert to WebP
   - Compress to target file size
   - Strip EXIF data

Include:
- Complete Python script with CLI arguments
- Example usage for each feature
- Integration with the bulk publisher (Prompt 3)
```
**Usage**: Automate featured image generation and upload.
**Expected output**: Complete image automation script.
**Tip**: WebP images are 25-35% smaller than JPEG with the same quality.

---

### Prompt 6: WordPress Post Updater & Content Refresher
```
Generate a Python script that bulk-updates existing WordPress posts:

Use cases:
1. **Find and replace** across all posts:
   - Text replacement (e.g., old year → new year)
   - URL replacement (e.g., old affiliate links → new ones)
   - Pattern-based replacement (regex support)

2. **Append content** to posts matching criteria:
   - Add a section to all posts in category X
   - Add disclosure text to all posts with affiliate links
   - Add "last updated" date to all posts

3. **Update meta fields** in bulk:
   - Update SEO meta descriptions
   - Update focus keywords
   - Update custom fields

4. **Audit mode** (read-only):
   - Find posts missing meta descriptions
   - Find posts without featured images
   - Find posts with broken internal links
   - Find posts shorter than X words

Script requirements:
- --dry-run mode (show changes without applying)
- Backup original content before updating
- Progress bar for bulk operations
- JSON report of all changes made

Provide the complete script with examples.
```
**Usage**: Maintain and update your entire content library.
**Expected output**: Complete post updater script.
**Tip**: Always run --dry-run first and review the report before applying changes.

---

### Prompt 7: Internal Link Injection System
```
Generate a Python script that automatically adds internal links between WordPress posts:

Algorithm:
1. Fetch all published posts (title, URL, content, categories, tags)
2. Extract keywords from each post (title + content tokenization)
3. Calculate relevance scores between all post pairs:
   - Shared keywords (unigrams + bigrams)
   - Same category bonus
   - Shared tags bonus
4. For each post, identify top 3 most relevant unlinked posts
5. Generate a "Related Articles" section with links
6. Insert the section at the end of each post (before the conclusion)
7. Skip posts that already have the section (idempotent)

The related links HTML format:
```html
<!-- internal-links-section -->
<div class="related-articles">
  <h3>Related Articles</h3>
  <ul>
    <li><a href="[URL]">[Title]</a></li>
    ...
  </ul>
</div>
```

Include:
- Relevance scoring algorithm (no external NLP libraries needed)
- Japanese text support (stop words list, character handling)
- Dry-run mode
- JSON report with all links added
- Update existing sections (replace, don't duplicate)

Provide the complete script.
```
**Usage**: Build internal link structure automatically.
**Expected output**: Complete internal linking script (~300 lines).
**Tip**: Internal links are one of the strongest on-page SEO signals you control.

---

### Prompt 8: SEO Meta Fields Bulk Optimizer
```
Create a system that optimizes SEO meta fields for all WordPress posts:

## AI Prompt for generating meta fields:
For each article, generate:
- **SEO title** (max 60 chars, keyword-first)
- **Meta description** (max 155 chars, includes keyword, ends with CTA)
- **Focus keyword** (primary target keyword)
- **Open Graph title** (can differ from SEO title)
- **Open Graph description** (max 200 chars)

Article: "[TITLE]"
Content summary: "[FIRST_300_WORDS]"
Current keyword: "[KEYWORD]"

## Python Script:
1. Fetch all posts
2. For each post, check if meta fields are optimized:
   - Title length OK? Keyword included?
   - Meta description length OK? Keyword included?
   - Focus keyword set?
3. Generate optimization suggestions using the AI prompt above
4. Apply optimizations via REST API (Rank Math or Yoast fields)

Rank Math custom fields:
- rank_math_title
- rank_math_description
- rank_math_focus_keyword

Yoast custom fields:
- _yoast_wpseo_title
- _yoast_wpseo_metadesc
- _yoast_wpseo_focuskw

Include complete script with both Rank Math and Yoast support.
```
**Usage**: Optimize SEO meta across your entire site.
**Expected output**: Meta optimization script with AI integration.
**Tip**: Well-optimized meta descriptions can improve CTR by 5-15%.

---

### Prompt 9: WordPress Backup & Migration Helper
```
Generate scripts for WordPress content backup and migration:

## Backup Script:
1. Export all posts with full metadata to JSON:
   - Post content (HTML)
   - Title, slug, date, status
   - Categories, tags
   - Featured image URL
   - SEO meta fields
   - Custom fields
   - Author info
2. Download all media files to local directory
3. Export taxonomy structure
4. Create a manifest file with counts and checksums
5. Compress everything into a dated archive

## Migration Script:
1. Read backup archive
2. Create categories and tags on target site
3. Upload media files and map old IDs to new IDs
4. Create posts with all metadata
5. Update internal links to point to new URLs
6. Verify migration with checksums

Both scripts should:
- Handle pagination (100+ posts)
- Show progress
- Resume on failure
- Log everything

Provide complete scripts for both backup and migration.
```
**Usage**: Reliable content backup and site migration.
**Expected output**: Backup + migration scripts.
**Tip**: Run backups weekly via Task Scheduler for automated protection.

---

### Prompt 10: Publishing Schedule Automator
```
Generate a Python script for automated scheduled publishing:

Features:
1. **Content queue management**:
   - Read from a JSON queue file:
     [{article_path, scheduled_date, scheduled_time, category, status}]
   - Support for recurring schedules (e.g., "every Monday 9:00")

2. **Pre-publish checks**:
   - Word count minimum (configurable)
   - Required sections present (intro, conclusion, FAQ)
   - No [PLACEHOLDER] or [TODO] markers remaining
   - Featured image assigned
   - SEO meta fields filled
   - Internal links present (minimum 2)
   - Affiliate disclosure present (if affiliate links found)

3. **Publishing**:
   - Set post status to "publish" at scheduled time
   - Or create as "future" status with WordPress scheduler
   - Notify via webhook (Discord/Slack) on publish

4. **Post-publish**:
   - Update article management CSV
   - Ping search engines (Google, Bing)
   - Generate social media post draft
   - Update content calendar

Include the complete script and a sample queue JSON file.
```
**Usage**: Automate your entire publishing workflow.
**Expected output**: Complete publishing automation script.
**Tip**: "Future" status lets WordPress handle the scheduling natively.

---

## SECTION 2: Content Pipeline Automation (10 Prompts)

### Prompt 11: Article Generation Pipeline
```
Design a complete article generation pipeline that:

1. **Input**: keyword + article type from queue
2. **Research**: Generate article outline with SEO structure
3. **Write**: Generate full article with AI
4. **Optimize**: Add internal links, affiliate links, meta data
5. **Format**: Convert to WordPress-ready HTML
6. **Publish**: Upload as draft to WordPress
7. **Log**: Record everything to CSV/JSON

For each stage, provide:
- The AI prompt to use
- The Python code to execute it
- Input/output format
- Error handling
- How to chain to the next stage

Include a main orchestrator script that runs the full pipeline:

```python
# Usage: python pipeline.py --keyword "target keyword" --type "how-to"
```

Make each stage independently runnable and testable.
```
**Usage**: End-to-end content automation.
**Expected output**: Complete pipeline architecture + code.
**Tip**: Always keep human review as a step — AI-only publishing risks quality issues.

---

### Prompt 12: Keyword-to-Article Queue System
```
Build a keyword queue management system:

## Queue JSON format:
[
  {
    "keyword": "best seo tools 2026",
    "type": "listicle",
    "priority": 1,
    "status": "pending",
    "category": "seo",
    "assigned_date": null,
    "processed_date": null,
    "article_path": null
  }
]

## Python Script Features:
1. **Add keywords**: From CSV, manual input, or API
2. **Prioritize**: Score by type (longtail > question > main), value terms, word count
3. **Dedup**: Check against published articles and existing queue
4. **Next keyword**: Get the highest-priority unprocessed keyword
5. **Mark complete**: Update status with article path and date
6. **Report**: Show queue stats (pending, processed, by category)
7. **Integration**: Hook into article_generator.py

Scoring algorithm:
- Longtail (3+ words): +30 points
- Question pattern: +20 points
- Contains high-value terms (稼ぐ, best, review, compare): +5 points
- 8-25 characters: +10 points (sweet spot for search volume)
- Already in queue or published: SKIP

Provide the complete script.
```
**Usage**: Manage your content pipeline queue.
**Expected output**: Queue management system.
**Tip**: Process longtail keywords first — they rank faster and build domain authority.

---

### Prompt 13: Affiliate Link Manager
```
Build an affiliate link management system for WordPress content:

## Link Database (JSON):
{
  "categories": {
    "hosting": {
      "links": [
        {
          "name": "ConoHa WING",
          "url": "https://affiliate-link/conoha",
          "anchor_text": ["ConoHa WING", "ConoHa WING公式サイト", "ConoHaを見る"],
          "context": "server hosting wordpress blog",
          "commission": "5000 JPY",
          "priority": 1
        }
      ]
    }
  },
  "insertion_rules": {
    "max_affiliate_links_per_article": 5,
    "min_words_between_links": 300,
    "disclosure_text": "※This article contains affiliate links..."
  }
}

## Features:
1. **Link selection**: Match keywords to relevant affiliate links
   - Score by keyword overlap with link context
   - Respect max links per article
   - Prioritize high-commission links
2. **Link insertion**: Natural placement in article content
   - Use varied anchor text
   - Maintain minimum spacing
   - Add disclosure text automatically
3. **Link rotation**: Prevent same anchor text across articles
4. **Link auditor**: Check all published posts for:
   - Broken affiliate links
   - Missing disclosures
   - Over-optimization (too many links)
5. **Revenue tracking**: Log which links are in which posts

Provide the complete Python script with examples.
```
**Usage**: Manage affiliate monetization systematically.
**Expected output**: Affiliate link management system.
**Tip**: Varied anchor text looks more natural to both readers and search engines.

---

### Prompt 14: Content Analytics Reporter
```
Generate a script that creates weekly content performance reports:

## Data Sources:
- WordPress REST API (post dates, categories, word counts)
- Google Analytics 4 API (pageviews, sessions, bounce rate)
- Google Search Console API (impressions, clicks, positions, keywords)

## Report Contents:
1. **Overview dashboard**:
   - Total posts: X (Y this week)
   - Total pageviews this week vs last week
   - Top 5 posts by pageviews
   - Average position change

2. **Content performance**:
   - New articles published this week + their initial metrics
   - Top gainers (position improved)
   - Top losers (position dropped)
   - Posts with high impressions but low CTR (optimization opportunities)

3. **Keyword tracking**:
   - Keywords ranking in positions 1-3
   - Keywords ranking in positions 4-10 (push to page 1)
   - Keywords ranking in positions 11-20 (quick wins)
   - New keywords found

4. **Action items**:
   - Posts to refresh (declining traffic)
   - Posts to optimize (high impressions, low clicks)
   - Internal linking opportunities
   - New keyword opportunities

## Output:
- Markdown report saved to file
- Optional: send via email or Discord webhook

Provide the complete script with GA4 and Search Console API integration.
```
**Usage**: Track content performance and identify opportunities.
**Expected output**: Complete analytics reporting script.
**Tip**: Focus action items on "almost ranking" keywords (positions 4-20) for quick wins.

---

### Prompt 15: Google Sheets Content Tracker Integration
```
Build a bidirectional sync between WordPress and Google Sheets:

## Spreadsheet structure:
| Post ID | Title | URL | Keyword | Category | Status | Pub Date | Word Count | Pageviews | Position | Notes |

## Features:
1. **WordPress → Sheets** (pull):
   - Fetch all posts metadata from WordPress
   - Update spreadsheet rows (match by Post ID)
   - Add new posts as new rows
   - Highlight changes since last sync

2. **Sheets → WordPress** (push):
   - Read "Status" column changes (draft → publish)
   - Read "Notes" column for bulk actions
   - Apply category changes
   - Update SEO meta from spreadsheet columns

3. **Auto-populate**:
   - New row in Sheets → create draft in WordPress
   - Word count calculated automatically
   - Analytics data pulled weekly

4. **Notification**:
   - Log sync results
   - Report conflicts (changed in both places)

## Setup:
- Google Sheets API (service account)
- Spreadsheet ID: [SPREADSHEET_ID]

Provide:
- Complete Python script
- Service account setup instructions
- Google Sheets API authorization code
- Sample spreadsheet structure
```
**Usage**: Manage content from a spreadsheet with WordPress sync.
**Expected output**: Complete bidirectional sync script.
**Tip**: Google Sheets works as a free content management dashboard for small teams.

---

### Prompt 16: Automated SEO Checklist Validator
```
Create a pre-publish SEO validation script:

## Checks (with pass/fail/warning):
### Content Quality
- [ ] Word count >= [MIN_WORDS] (configurable)
- [ ] No placeholder text ([TODO], [PLACEHOLDER], [ADD], [VERIFY])
- [ ] No AI artifacts ("As an AI", "I cannot", "I don't have")
- [ ] Introduction contains keyword in first 100 words
- [ ] Conclusion section exists
- [ ] FAQ section exists with 3+ questions

### SEO Elements
- [ ] H1 exists (exactly one)
- [ ] H1 contains target keyword
- [ ] H2 headings contain keyword (at least 2)
- [ ] Meta description exists and is under 155 chars
- [ ] Meta description contains keyword
- [ ] URL slug is optimized (no stop words, under 60 chars)
- [ ] Image alt text includes keyword (at least one)

### Links
- [ ] Internal links: minimum 2
- [ ] External links: minimum 1
- [ ] No broken links
- [ ] Affiliate disclosure present (if affiliate links found)

### Technical
- [ ] All images have alt text
- [ ] All images have width/height attributes
- [ ] No oversized images (> 200KB)
- [ ] Mobile-friendly table formatting

Input: Markdown file or WordPress post ID
Output: JSON report with pass/fail per check + overall score

Provide the complete Python script.
```
**Usage**: Catch SEO issues before publishing.
**Expected output**: Complete validation script.
**Tip**: Run this automatically before every publish — it catches 80% of common mistakes.

---

### Prompt 17: Social Media Post Generator for Published Articles
```
Generate a prompt + script that creates social media posts for every published article:

## AI Prompt:
Given this article, create social media posts:
- Title: "[TITLE]"
- URL: [URL]
- Keyword: [KEYWORD]
- Summary: [FIRST_200_WORDS]

Generate:
1. **Twitter/X post** (280 chars max):
   - Hook + key insight + link
   - Include 2-3 relevant hashtags

2. **Thread version** (5 tweets):
   - Tweet 1: Hook question
   - Tweet 2-4: Key takeaways
   - Tweet 5: CTA + link

3. **LinkedIn post** (300 words):
   - Personal story angle
   - Key insight with data
   - CTA

## Python Script:
1. Listen for new published posts (poll WordPress API)
2. Generate social posts using AI prompt
3. Save to JSON queue for scheduled posting
4. Optional: post directly via X API

Include the complete prompt and automation script.
```
**Usage**: Automate social promotion of new content.
**Expected output**: Social post generator + automation script.
**Tip**: Post within 1 hour of publishing for maximum social signal impact.

---

### Prompt 18: WordPress Performance Monitor
```
Build a monitoring script for WordPress site health:

## Checks (run daily):
1. **Uptime**: HTTP status check on homepage + key pages
2. **Response time**: Average load time (flag if > 3 seconds)
3. **SSL certificate**: Days until expiration
4. **WordPress version**: Current vs latest, flag if outdated
5. **Plugin updates**: Count of plugins needing updates
6. **Disk usage**: Media library size
7. **Database size**: Post count, revision count
8. **Broken links**: Scan published content for 404 internal links
9. **Search Console errors**: Crawl errors from API
10. **Core Web Vitals**: PageSpeed Insights API scores

## Alerting:
- Save daily report to JSON
- Send Discord/Slack webhook on critical issues
- Weekly summary email

## Healthchecks.io integration:
- Ping on successful run
- Fail signal on critical errors

Provide the complete monitoring script.
```
**Usage**: Catch WordPress issues before they affect rankings.
**Expected output**: Complete site monitoring script.
**Tip**: Integrate with Healthchecks.io for reliable dead man's switch monitoring.

---

### Prompt 19: WordPress Revision Cleaner & Optimizer
```
Generate a WordPress optimization script:

## Database Cleanup:
1. Delete post revisions older than 30 days
2. Delete auto-drafts
3. Delete trashed posts
4. Delete orphaned meta data
5. Delete expired transients
6. Optimize database tables

## Content Optimization:
1. Find and fix double spaces in post content
2. Normalize smart quotes and em dashes
3. Fix broken shortcodes
4. Remove empty paragraphs
5. Clean up MS Word paste artifacts

## Media Cleanup:
1. Find unattached media items
2. Find media not used in any post
3. Report potential duplicates (same filename)
4. Calculate total media library size

## Safety:
- Full backup before any destructive operations
- Dry-run mode by default
- Detailed log of all changes
- Undo capability (for content changes)

Provide the complete script with --cleanup and --audit modes.
```
**Usage**: Keep your WordPress installation lean and fast.
**Expected output**: Complete optimization script.
**Tip**: Run cleanup monthly — revisions can bloat your database by 10x.

---

### Prompt 20: Multi-Site Content Syndicator
```
Build a system for managing content across multiple WordPress sites:

## Configuration:
```json
{
  "sites": [
    {"name": "Site A", "url": "https://site-a.com/wp-json/wp/v2", "auth": "..."},
    {"name": "Site B", "url": "https://site-b.com/wp-json/wp/v2", "auth": "..."},
    {"name": "Site C", "url": "https://site-c.com/wp-json/wp/v2", "auth": "..."}
  ]
}
```

## Features:
1. **Cross-publish**: Publish same article to multiple sites with customization
   - Different categories per site
   - Different affiliate links per site
   - Canonical URL pointing to primary site

2. **Template sync**: Apply the same article template across sites
   - Different author bios
   - Site-specific header/footer injections

3. **Bulk operations**: Run any command across all sites
   - Update affiliate links on all sites
   - Add disclosure text to all sites
   - Refresh year references on all sites

4. **Dashboard**: Show status of all sites
   - Post counts
   - Last published date
   - Pending drafts

Provide the complete multi-site management script.
```
**Usage**: Manage a portfolio of WordPress sites from one script.
**Expected output**: Multi-site content management system.
**Tip**: Always set canonical URLs to avoid duplicate content penalties.

---

## SECTION 3: Advanced Automation Recipes (10 Prompts)

### Prompt 21: Full Auto-Pilot Publishing Pipeline
```
Design a complete zero-touch article publishing system:

Pipeline steps (each as a separate Python function):
1. `get_next_keyword()` → Read from queue, return highest priority
2. `research_topic(keyword)` → Generate article outline using AI
3. `generate_article(keyword, outline)` → Write full article using AI
4. `optimize_seo(article)` → Add meta fields, optimize headings
5. `add_internal_links(article)` → Insert relevant internal links
6. `add_affiliate_links(article)` → Insert appropriate affiliate links
7. `validate(article)` → Run SEO checklist, return pass/fail
8. `generate_featured_image(keyword)` → Create placeholder image
9. `publish_to_wordpress(article, image)` → Upload as draft
10. `notify(result)` → Send Discord webhook with summary
11. `update_tracking(result)` → Update CSV + Google Sheet

Orchestrator:
```python
def run_pipeline():
    keyword = get_next_keyword()
    outline = research_topic(keyword)
    article = generate_article(keyword, outline)
    article = optimize_seo(article)
    article = add_internal_links(article)
    article = add_affiliate_links(article)

    validation = validate(article)
    if not validation.passed:
        notify(f"FAILED: {keyword} - {validation.errors}")
        return

    image_id = generate_featured_image(keyword)
    result = publish_to_wordpress(article, image_id)
    notify(result)
    update_tracking(result)
```

Provide complete code for each function.
```
**Usage**: Fully automated content pipeline (human review recommended).
**Expected output**: Complete auto-publishing system.
**Tip**: Even in autopilot mode, review drafts before setting to "publish" status.

---

### Prompt 22: WordPress Webhook Handler
```
Create a lightweight webhook server that responds to WordPress events:

## Triggers:
1. **Post published** → Generate social media posts + ping search engines
2. **Post updated** → Invalidate CDN cache + update Sheets
3. **Comment received** → Send Discord notification
4. **Plugin update available** → Send alert

## Implementation:
- Flask/FastAPI server (lightweight)
- Verify webhook signatures
- Queue processing (don't block the webhook response)
- Error handling and retry logic
- Health check endpoint

## WordPress side:
- Use WP Webhooks plugin or custom functions.php hook
- Payload format for each event type

Provide:
- Complete webhook server code
- WordPress hook configuration
- Deployment instructions (local + VPS)
- Testing with curl commands
```
**Usage**: React to WordPress events in real-time.
**Expected output**: Complete webhook handler.
**Tip**: Use ngrok for local testing before deploying to production.

---

### Prompt 23: Content A/B Testing System
```
Build a title and meta description A/B testing system:

## How it works:
1. For each post, store 2-3 title variants in custom fields
2. Rotate titles on a schedule (7 days per variant)
3. Track CTR from Search Console for each period
4. After all variants tested, set the winner permanently

## Components:
1. **Variant generator prompt**:
   Given article "[TITLE]" targeting "[KEYWORD]", generate 3 title variants:
   - Original: [ORIGINAL]
   - Variant A: [More emotional/curiosity-driven]
   - Variant B: [More specific/number-driven]

2. **Rotation script** (daily cron):
   - Check which posts are in A/B test
   - Rotate titles if current variant period expired
   - Log the rotation

3. **Results analyzer** (weekly):
   - Pull CTR data from Search Console API
   - Compare performance per variant per post
   - Recommend winners with statistical significance check

4. **Winner applier**:
   - Set the best-performing title as permanent
   - Update meta description to match
   - Archive test results

Provide complete scripts for all components.
```
**Usage**: Data-driven title optimization.
**Expected output**: Complete A/B testing system.
**Tip**: Minimum 1000 impressions per variant for statistical significance.

---

### Prompt 24: Automated Content Brief Generator
```
Create a system that generates content briefs from keywords:

Input: keyword + article type
Output: Complete content brief (Markdown file)

## Brief template:
```markdown
# Content Brief: [KEYWORD]
Generated: [DATE]

## Target
- Primary keyword: [KEYWORD]
- Secondary keywords: [AI-GENERATED LIST]
- Search intent: [AI-DETERMINED]
- Target word count: [BASED ON TOP-RANKING CONTENT]

## Audience
- Who: [AUDIENCE DESCRIPTION]
- Knowledge level: [BEGINNER/INTERMEDIATE/ADVANCED]
- Pain points: [3 BULLET POINTS]
- What they want to achieve: [OUTCOME]

## Article Structure
[AI-GENERATED H2/H3 OUTLINE WITH WORD COUNTS PER SECTION]

## Must-Cover Topics
[AI-GENERATED LIST BASED ON TOP-RANKING COMPETITORS]

## SEO Requirements
- Title tag: [SUGGESTION]
- Meta description: [SUGGESTION]
- URL slug: [SUGGESTION]
- Internal links to: [EXISTING ARTICLES]
- External sources: [AUTHORITY SITES TO REFERENCE]

## Monetization
- Affiliate links: [WHICH PRODUCTS TO MENTION]
- CTA: [WHAT ACTION TO DRIVE]

## Differentiation
- What competitors miss: [GAP ANALYSIS]
- Unique angle: [PERSONAL EXPERIENCE / DATA / PERSPECTIVE]
```

Python script that:
1. Takes keyword as input
2. Generates brief using AI
3. Saves to briefs/ directory
4. Adds to content queue

Provide the complete prompt + script.
```
**Usage**: Standardize content production with detailed briefs.
**Expected output**: Brief generation system.
**Tip**: Good briefs reduce article revision cycles by 50%.

---

### Prompt 25: WordPress Security Audit Script
```
Create a security audit script for WordPress sites:

## Checks:
1. **Authentication**:
   - Verify XML-RPC is disabled (or rate-limited)
   - Check for exposed user enumeration (wp-json/wp/v2/users)
   - Verify Application Passwords are not leaked in API responses

2. **Headers**:
   - X-Content-Type-Options
   - X-Frame-Options
   - Content-Security-Policy
   - Strict-Transport-Security
   - Permissions-Policy

3. **WordPress-specific**:
   - Debug mode disabled (WP_DEBUG)
   - File editing disabled (DISALLOW_FILE_EDIT)
   - WordPress version not exposed
   - readme.html not accessible
   - wp-config.php not accessible
   - Directory listing disabled

4. **Content security**:
   - Mixed content (HTTP resources on HTTPS pages)
   - External scripts loaded (potential security risk)
   - Forms without CSRF protection

## Output:
- Pass/Fail/Warning per check
- Fix instructions for each failure
- Overall security score (A-F)
- Priority-ranked fix list

Provide the complete audit script.
```
**Usage**: Regular security checks for your WordPress site.
**Expected output**: Complete security audit script.
**Tip**: Run monthly and after every WordPress/plugin update.

---

### Prompt 26: Content Repurposing Pipeline
```
Build a system that repurposes one article into multiple content formats:

Input: WordPress post ID or Markdown file
Output: Multiple content pieces

## Repurposing AI Prompts:

### Blog → Twitter Thread:
Given article content, create a 7-tweet thread:
- Tweet 1: Hook/question
- Tweets 2-6: Key points (1 per tweet, 280 chars max)
- Tweet 7: Summary + link

### Blog → Newsletter:
Given article content, create an email newsletter version:
- Subject line (under 50 chars)
- Preview text (under 90 chars)
- Body: Personal intro + 3 key takeaways + CTA

### Blog → YouTube Script:
Convert to a 5-minute video script:
- Hook (15 seconds)
- Intro (30 seconds)
- Main points (3 minutes)
- CTA (30 seconds)
- Outro (15 seconds)

### Blog → LinkedIn Post:
Create a 200-word LinkedIn post:
- Personal angle
- Key insight
- Call for discussion

### Blog → Infographic Outline:
Create a data layout for an infographic:
- Title
- 5-7 data points
- Flow/process visualization
- Key stat highlight

Provide the complete prompt for each format + orchestrator script.
```
**Usage**: Maximize the value of every article.
**Expected output**: Repurposing system with 5+ output formats.
**Tip**: Repurposing is the highest ROI content activity — one article becomes 5+ pieces.

---

### Prompt 27: Automated Link Building Outreach Tracker
```
Build a system to manage SEO outreach and link building:

## Database (JSON):
{
  "prospects": [
    {
      "site": "example.com",
      "contact_email": "...",
      "domain_authority": 45,
      "relevance": "high",
      "status": "not_contacted",
      "outreach_date": null,
      "follow_up_dates": [],
      "response": null,
      "link_acquired": false
    }
  ]
}

## AI Prompts:

### Prospect finder:
Given my blog about [NICHE], suggest 20 websites that might link to my article about "[KEYWORD]":
- Resource pages that list tools/guides
- Blogs that cover similar topics
- Industry directories
- Broken link opportunities
- Guest post opportunities

### Outreach email generator:
Write a personalized outreach email to [CONTACT_NAME] at [SITE]:
- Reference their specific article: [ARTICLE_URL]
- Explain why my article adds value
- Keep under 150 words
- Include specific value proposition
- No generic templates

## Tracker Script:
1. Add prospects from AI suggestions
2. Generate personalized emails
3. Track outreach status
4. Schedule follow-ups (7 days, 14 days)
5. Report: response rate, link acquisition rate

Provide the complete system.
```
**Usage**: Systematic link building for SEO.
**Expected output**: Outreach tracking system.
**Tip**: Personalized emails get 3x higher response rates than templates.

---

### Prompt 28: WordPress Comment Moderator
```
Build an AI-powered comment moderation system:

## Features:
1. **Fetch pending comments** via REST API
2. **Classify each comment** using AI:
   - Spam (auto-delete)
   - Low quality (auto-delete)
   - Question (approve + flag for reply)
   - Positive feedback (auto-approve)
   - Negative feedback (approve + flag for response)
   - Contains links (hold for review)
3. **Auto-reply** to questions using article content as context
4. **Report**: Daily digest of comment activity

## AI Classification Prompt:
Classify this blog comment and suggest an action:

Article title: "[TITLE]"
Comment author: "[AUTHOR]"
Comment text: "[COMMENT]"

Classify as: spam / low_quality / question / positive / negative / link_spam
Suggested action: approve / delete / hold / reply
If "reply", suggest a helpful response.

## Script:
- Run every hour via Task Scheduler
- Configurable auto-approve/auto-delete rules
- Discord notification for items needing manual review

Provide the complete script.
```
**Usage**: Automate comment moderation.
**Expected output**: AI comment moderation system.
**Tip**: Responding to comments improves engagement signals and builds community.

---

### Prompt 29: Structured Data Generator for All Content Types
```
Build a script that automatically generates and injects schema markup:

## Supported types:
1. **Article** (all posts)
2. **FAQ** (posts with FAQ section)
3. **HowTo** (posts with step-by-step instructions)
4. **Product Review** (review posts)
5. **Breadcrumb** (all pages)
6. **LocalBusiness** (about page)
7. **Person** (author pages)

## Script:
1. Fetch post content from WordPress
2. Detect content type from structure (H2 patterns, FAQ format, step lists)
3. Generate appropriate JSON-LD schema
4. Inject into post HTML (before </body>) via custom field or filter
5. Validate against schema.org standards
6. Report: which posts have schema, which need it

## Detection rules:
- FAQ: Contains "Q:" or "Q." patterns, or H3s starting with question words
- HowTo: Contains "Step 1", "Step 2" or numbered H3s with action verbs
- Review: Contains rating, pros/cons, or "verdict" section
- Default: Article schema

Provide the complete script with validation.
```
**Usage**: Automatic rich results for all content types.
**Expected output**: Schema generation and injection system.
**Tip**: FAQ schema alone can increase CTR by 20-30%.

---

### Prompt 30: Complete WordPress Automation Dashboard
```
Build a web-based dashboard to monitor and control all automations:

## Dashboard features (single HTML + JavaScript page):
1. **Site Status**:
   - All managed sites with uptime status
   - Last publish date
   - Post count / draft count

2. **Content Pipeline**:
   - Keyword queue: pending / processing / complete
   - Articles in draft
   - Scheduled publications

3. **SEO Health**:
   - Posts missing meta descriptions
   - Posts without featured images
   - Posts with SEO score below threshold

4. **Performance**:
   - Top 10 posts by traffic (last 7 days)
   - Position changes (up/down)
   - New keywords ranking

5. **Quick Actions**:
   - Generate article from keyword (one click)
   - Publish draft (one click)
   - Run SEO audit (one click)
   - Refresh content (one click)

## Tech:
- Single HTML file with embedded CSS/JS
- Fetches data from JSON files (generated by scripts above)
- Auto-refresh every 5 minutes
- Mobile-responsive

Provide the complete dashboard HTML file.
```
**Usage**: Visual control center for all WordPress automation.
**Expected output**: Complete single-page dashboard.
**Tip**: Host locally or on the same server as your scripts for fastest data access.

---

## Quick Reference: WordPress REST API Cheat Sheet

### Authentication
```bash
# Test authentication
curl -u "username:application_password" https://yoursite.com/wp-json/wp/v2/posts?per_page=1
```

### Common Endpoints
```
GET    /wp-json/wp/v2/posts          # List posts
POST   /wp-json/wp/v2/posts          # Create post
PUT    /wp-json/wp/v2/posts/{id}     # Update post
DELETE /wp-json/wp/v2/posts/{id}     # Delete post
GET    /wp-json/wp/v2/categories     # List categories
GET    /wp-json/wp/v2/tags           # List tags
POST   /wp-json/wp/v2/media          # Upload media
```

### Post Fields
```json
{
  "title": "Post Title",
  "content": "<p>HTML content</p>",
  "status": "draft|publish|future",
  "categories": [1, 2],
  "tags": [3, 4],
  "featured_media": 123,
  "slug": "url-slug",
  "date": "2026-03-19T09:00:00",
  "meta": {
    "rank_math_title": "SEO Title",
    "rank_math_description": "Meta description",
    "rank_math_focus_keyword": "focus keyword"
  }
}
```

### Python Quick Start
```python
import requests
from base64 import b64encode

api_url = "https://yoursite.com/wp-json/wp/v2"
auth = b64encode(b"username:app_password").decode()
headers = {"Authorization": f"Basic {auth}"}

# Create a post
post = requests.post(f"{api_url}/posts", json={
    "title": "My Article",
    "content": "<p>Content here</p>",
    "status": "draft",
}, headers=headers)

print(post.json()["id"], post.json()["link"])
```

---

*30 prompts + production code. Built from a real system publishing 3+ articles per week on autopilot.*
