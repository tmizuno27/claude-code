# Claude Code Automation Playbook

## The Complete Guide to Automating Your Business with Claude Code

---

## Table of Contents

1. [What Is Claude Code and Why It Changes Everything](#chapter-1)
2. [Setting Up Claude Code for Business Automation](#chapter-2)
3. [Automating SEO — From Research to Publication](#chapter-3)
4. [Automating Digital Product Creation](#chapter-4)
5. [WordPress Integration via REST API](#chapter-5)
6. [Multi-Site Management at Scale](#chapter-6)
7. [Task Scheduling and Monitoring](#chapter-7)
8. [Real-World Automation Case Studies](#chapter-8)
9. [Advanced Patterns — Agents, Teams, and Pipelines](#chapter-9)
10. [Tips, Best Practices, and Pitfalls](#chapter-10)

---

## Chapter 1: What Is Claude Code and Why It Changes Everything {#chapter-1}

Claude Code is Anthropic's official CLI tool that gives you a conversational AI assistant with direct access to your filesystem, terminal, and development environment. Unlike ChatGPT or the Claude web interface, Claude Code operates *inside your project directory*. It can read files, write code, execute scripts, search your codebase, and chain complex multi-step operations — all from a single conversation.

**Why this matters for business automation:**

Most AI-assisted automation breaks down at the integration layer. You prompt an AI, copy the output, paste it into your system, tweak it, debug it, repeat. Claude Code eliminates that entire loop. You describe what you want, and it reads your config files, generates the code, runs it, checks the output, and fixes errors — all in one session.

Here is what becomes possible:

- **Content pipeline automation**: Research keywords, generate articles, format for WordPress, publish via REST API, and schedule social media posts — in a single command.
- **Multi-site management**: Run the same optimization across 3, 5, or 10 websites simultaneously.
- **Digital product creation**: Generate product assets, thumbnails, descriptions, and listing metadata without touching a design tool.
- **Data-driven decisions**: Pull analytics from Google Search Console, GA4, and affiliate dashboards, then generate actionable reports.

The key insight is that Claude Code is not just a coding assistant. It is a *business automation runtime*. Once you set up the right project structure, configuration files, and prompt templates, you can automate almost any digital business operation.

---

## Chapter 2: Setting Up Claude Code for Business Automation {#chapter-2}

### Installation

```bash
# Install Claude Code globally
npm install -g @anthropic-ai/claude-code

# Start a session in your project directory
cd ~/my-business-project
claude
```

### Project Structure That Enables Automation

The single most important thing you can do is organize your project so Claude Code can find what it needs. Here is a battle-tested structure:

```
my-business/
├── CLAUDE.md              # Project instructions (Claude reads this automatically)
├── config/
│   ├── secrets.json       # API keys, credentials (gitignored)
│   ├── affiliate-links.json
│   └── site-config.json
├── scripts/
│   ├── content/           # Article generation, keyword research
│   ├── publishing/        # WordPress publishing, social media
│   └── analytics/         # GA4, GSC, reporting
├── templates/             # Article templates, email templates
├── inputs/                # Keyword queues, content briefs
├── outputs/               # Generated articles, reports
└── logs/                  # Execution logs
```

### The CLAUDE.md File — Your Automation Blueprint

The `CLAUDE.md` file is the most powerful feature most people overlook. Claude Code reads this file automatically at the start of every session. It becomes the persistent memory and instruction set for your automation.

**What to put in CLAUDE.md:**

```markdown
# My Business Automation Hub

## Project Overview
[Describe your business, sites, products]

## Directory Structure
[Map out where everything lives]

## API Credentials
- WordPress: config/secrets.json
- Google APIs: config/service-account.json
- Social media: config/x-api.json

## Common Operations
- Article generation: python scripts/content/article_generator.py
- Publishing: python scripts/publishing/wp_publisher.py
- Analytics: python scripts/analytics/reporter.py

## Business Rules
- Always fact-check statistics before publishing
- Include affiliate links from config/affiliate-links.json
- Target 2000+ words per article
```

This file turns Claude Code from a generic assistant into *your* business-specific automation engine.

### Managing Secrets Safely

Never hardcode API keys. Use a `config/secrets.json` file:

```json
{
  "wordpress": {
    "url": "https://yoursite.com",
    "username": "admin",
    "app_password": "xxxx xxxx xxxx xxxx"
  },
  "claude_api_key": "sk-ant-...",
  "google_service_account": "./config/service-account.json"
}
```

Add `config/secrets.json` to `.gitignore`. Claude Code can read this file during automation but it never leaves your machine.

---

## Chapter 3: Automating SEO — From Research to Publication {#chapter-3}

### Keyword Research Automation

The traditional keyword research workflow is: open a tool, export CSV, analyze in a spreadsheet, pick winners, create a content brief. With Claude Code, this becomes:

1. **Feed Claude Code your niche and existing content** — it reads your published articles and identifies gaps.
2. **Generate keyword clusters** — grouped by search intent, difficulty, and revenue potential.
3. **Output a prioritized content queue** — saved as CSV or JSON, ready for article generation.

The key prompt pattern:

```
Read my published articles in outputs/article-management.csv.
Analyze the keyword gaps for [your niche].
Generate 20 keyword clusters I haven't covered.
Prioritize by: search volume estimate, competition, affiliate revenue potential.
Save to inputs/keyword-queue.csv.
```

### Article Generation That Actually Ranks

Generating SEO content with AI is easy. Generating content that *ranks* requires structure:

**The template approach:**

Create a `templates/article-template.md` with your required structure:

```markdown
# {TITLE}

## Introduction (Hook + Promise + Preview)
[150-200 words, include primary keyword naturally]

## {H2_1}
[300-400 words, answer a specific search intent]

## {H2_2}
[300-400 words, include comparison table if applicable]

...

## FAQ
[5-8 questions from "People Also Ask"]

## Conclusion
[Call-to-action + affiliate link placement]
```

Then prompt Claude Code to generate articles *using* this template, with real data from web search. The difference between a $0 AI article and a ranking article is:

- **Fact-checked statistics** (Claude Code can web search during generation)
- **Original analysis** (not just rephrased competitor content)
- **Proper internal linking** (Claude Code reads your existing articles and links them)
- **Strategic affiliate placement** (reads your affiliate-links.json and inserts contextually)

### Internal Link Optimization

This is one of the highest-ROI automations. Most sites lose significant ranking potential from poor internal linking.

The automation pattern:

1. Claude Code reads all your published articles.
2. It maps the topic relationships between them.
3. It identifies articles that should link to each other but don't.
4. It generates the updated HTML with contextual anchor text.
5. It pushes the changes via WordPress REST API.

One script run can add dozens of relevant internal links across your entire site in minutes.

---

## Chapter 4: Automating Digital Product Creation {#chapter-4}

### The Product Factory Pattern

If you sell digital products (templates, guides, prompt packs, tools), Claude Code can automate the entire creation pipeline:

1. **Market Research**: Analyze competitors on Gumroad, Etsy, or marketplaces to find gaps.
2. **Product Generation**: Create the actual product content — templates, guides, code.
3. **Asset Creation**: Generate thumbnails, preview images, and mockups using Python (Pillow).
4. **Listing Optimization**: Write titles, descriptions, and tags optimized for marketplace search.
5. **Packaging**: Bundle into ZIP files ready for upload.

**Example — Notion Template Product:**

```
Research the top 20 Notion templates on Gumroad in the [productivity] category.
Identify an underserved niche.
Create a complete Notion template with:
- 5+ interconnected databases
- Pre-built views (Board, Calendar, Gallery)
- Starter data
Generate a product listing with title, description, and 10 tags.
Create a thumbnail (1280x720) using Pillow.
Package everything into a ZIP.
```

### Thumbnail Generation with Python

Every Gumroad product needs a professional thumbnail. Instead of opening Canva every time:

```python
from PIL import Image, ImageDraw, ImageFont

def create_thumbnail(title, subtitle, output_path,
                     bg_color="#1a1a2e", accent_color="#e94560"):
    img = Image.new('RGB', (1280, 720), bg_color)
    draw = ImageDraw.Draw(img)
    # Add gradient, text, decorative elements
    # ... (see included generate_thumbnail.py for full implementation)
    img.save(output_path, quality=95)
```

This runs in seconds and produces consistent, professional thumbnails across your entire product catalog.

---

## Chapter 5: WordPress Integration via REST API {#chapter-5}

### Publishing Articles Programmatically

The WordPress REST API lets you do everything the admin dashboard does — and more — from scripts:

```python
import requests
import json

def publish_article(title, content, category_ids, featured_image_id=None):
    config = json.load(open('config/secrets.json'))
    wp = config['wordpress']

    response = requests.post(
        f"{wp['url']}/wp-json/wp/v2/posts",
        auth=(wp['username'], wp['app_password']),
        json={
            'title': title,
            'content': content,
            'status': 'publish',
            'categories': category_ids,
            'featured_media': featured_image_id
        }
    )
    return response.json()
```

### Image Upload and Management

Upload images before publishing, then reference them by media ID:

```python
def upload_image(image_path, alt_text=""):
    with open(image_path, 'rb') as f:
        response = requests.post(
            f"{wp_url}/wp-json/wp/v2/media",
            auth=(username, app_password),
            headers={'Content-Disposition': f'attachment; filename="{filename}"'},
            files={'file': f},
            data={'alt_text': alt_text}
        )
    return response.json()['id']
```

### Bulk Operations

The real power is bulk operations — updating meta descriptions across 50 articles, inserting affiliate links into every post, or reformatting all articles to match a new template. Claude Code can:

1. Fetch all posts via REST API.
2. Analyze each one for the required changes.
3. Apply changes and push updates.
4. Log every change for review.

This turns a week of manual work into a 10-minute script execution.

---

## Chapter 6: Multi-Site Management at Scale {#chapter-6}

### The Shared-Script Architecture

When you run multiple sites, code duplication is the enemy. The pattern that works:

```
sites/
├── site-a.com/
│   ├── CLAUDE.md          # Site-specific rules
│   ├── config/            # Site-specific credentials
│   └── inputs/            # Site-specific keyword queues
├── site-b.com/
│   └── (same structure)
└── shared/
    ├── scripts/           # Shared automation scripts
    └── templates/         # Shared article templates
```

Each site has its own config and content, but the automation scripts are shared. A single script can iterate across all sites:

```python
SITES = ['site-a.com', 'site-b.com', 'site-c.com']

for site in SITES:
    config = load_config(f'sites/{site}/config/secrets.json')
    articles = fetch_all_posts(config)
    optimized = optimize_internal_links(articles)
    push_updates(config, optimized)
    log_results(site, optimized)
```

### Parallel Site Audits

Claude Code's agent system can audit multiple sites in parallel:

- Agent 1: SEO audit on Site A
- Agent 2: Broken link check on Site B
- Agent 3: Performance analysis on Site C

Results are aggregated into a single report. What would take a full day manually completes in minutes.

---

## Chapter 7: Task Scheduling and Monitoring {#chapter-7}

### Automating Recurring Tasks

Once you have scripts that work, schedule them:

**On Windows (Task Scheduler):**

```powershell
# Create a scheduled task
$action = New-ScheduledTaskAction -Execute "python" -Argument "C:\path\scripts\daily_seo.py"
$trigger = New-ScheduledTaskTrigger -Daily -At "6:00AM"
Register-ScheduledTask -TaskName "DailySEO" -Action $action -Trigger $trigger
```

**On Mac/Linux (cron):**

```bash
# Run daily at 6 AM
0 6 * * * cd /path/to/project && python scripts/daily_seo.py >> logs/seo.log 2>&1
```

### Monitoring with Healthchecks

Every automated task should report its status. Healthchecks.io (free tier: 20 checks) provides dead-simple monitoring:

```python
import requests

def ping_healthcheck(check_id, status="success"):
    url = f"https://hc-ping.com/{check_id}"
    if status == "fail":
        url += "/fail"
    requests.get(url, timeout=10)
```

If a task fails to ping within its expected schedule, you get an alert via email, Slack, or Discord.

### The Daily Automation Stack

A production business automation setup runs these daily:

| Time | Task | Purpose |
|------|------|---------|
| 06:00 | GSC data pull | Fresh search performance data |
| 06:15 | SEO analysis | Identify declining pages, new opportunities |
| 06:30 | Meta tag optimization | Auto-improve underperforming titles |
| 07:00 | Article generation | Create next queued article |
| 08:00 | Internal link update | Add links to new content |
| 10:00 | Social media post | Promote content on X/Twitter |
| 14:00 | Social media post | Second daily post |
| 18:00 | Analytics report | Daily performance summary |
| 19:00 | Social media post | Third daily post |

All of this runs without human intervention. You review the daily report and adjust strategy as needed.

---

## Chapter 8: Real-World Automation Case Studies {#chapter-8}

### Case Study 1: Blog Network SEO Pipeline

**Scenario**: Three niche blogs, each targeting different markets. Goal: grow organic traffic from 0 to sustainable revenue.

**Automation implemented:**
- Keyword research bot analyzes Google Search Console data weekly, identifies content gaps, and queues new articles.
- Article generator creates 2-3 articles per site per week, each with proper SEO structure, internal links, and affiliate placements.
- WordPress publisher pushes articles on schedule with featured images and proper categories.
- Social media scheduler creates and posts promotional content for each new article.
- Weekly analytics reporter compiles traffic, rankings, and revenue data into actionable dashboards.

**Result**: 150+ articles published across 3 sites in 3 months. Content quality remains high because the templates enforce structure and the prompts include fact-checking requirements.

### Case Study 2: Digital Product Marketplace

**Scenario**: Selling digital products (templates, guides, tools) across multiple platforms — Gumroad, Chrome Web Store, VS Code Marketplace, RapidAPI.

**Automation implemented:**
- Market research agent scans competitor listings to identify product opportunities.
- Product builder agent creates the actual product content based on templates.
- Thumbnail generator creates consistent branded visuals using Python.
- Listing publisher formats metadata for each platform's requirements and creates optimized descriptions.

**Result**: 40+ products listed across 5 platforms. The entire pipeline from idea to published listing takes under an hour, compared to 4-6 hours manually.

### Case Study 3: Affiliate Revenue Optimization

**Scenario**: Monetizing blog content with affiliate links from multiple ASP networks.

**Automation implemented:**
- Centralized affiliate link database (`affiliate-links.json`) stores all active programs with URLs, categories, and priority.
- Bulk insertion script scans every article and adds contextually relevant affiliate links.
- Monthly audit checks for broken links, expired programs, and underperforming placements.
- Revenue tracker correlates click data with content to identify top-performing articles and link positions.

**Result**: Affiliate link coverage went from ~30% of eligible articles to 100%. Click-through rates improved because links are contextually placed rather than randomly inserted.

---

## Chapter 9: Advanced Patterns — Agents, Teams, and Pipelines {#chapter-9}

### Custom Agents

Claude Code supports custom agents — specialized AI assistants with specific instructions and capabilities. Define them in `.claude/agents/`:

```markdown
# SEO Researcher Agent

## Role
You are an SEO keyword research specialist.

## Instructions
1. Analyze the target niche and existing content.
2. Use web search to find keyword opportunities.
3. Prioritize keywords by: search volume, competition, commercial intent.
4. Output a structured keyword queue in CSV format.

## Output Format
keyword,search_volume_estimate,difficulty,intent,priority
```

### Team Orchestration

For complex operations, multiple agents work together:

**Content Pipeline Team:**
1. `seo-researcher` — finds the best keyword.
2. `article-writer` — generates the article.
3. `wp-publisher` — publishes to WordPress.
4. `sns-scheduler` — creates social media posts.

Each agent has a focused role and clear inputs/outputs. The orchestrator chains them together.

### Error Handling in Pipelines

Production automation must handle failures gracefully:

```python
def run_pipeline(site):
    try:
        keywords = research_keywords(site)
        article = generate_article(keywords[0])
        post_id = publish_to_wordpress(site, article)
        schedule_social(site, post_id)
        ping_healthcheck(site.check_id)
    except Exception as e:
        log_error(site, e)
        ping_healthcheck(site.check_id, status="fail")
        # Don't re-raise — let other sites continue
```

Always log errors, always alert on failure, and never let one site's error cascade to others.

---

## Chapter 10: Tips, Best Practices, and Pitfalls {#chapter-10}

### Do's

1. **Start with CLAUDE.md** — invest time in writing clear project instructions. It pays back 100x.
2. **Use config files** — never hardcode URLs, credentials, or business logic.
3. **Log everything** — every automated action should produce a log entry.
4. **Monitor with health checks** — if a task fails silently, you lose money silently.
5. **Version control your automation** — git commit your scripts. You will need to roll back.
6. **Test with dry runs** — add a `--dry-run` flag to publishing scripts that shows what *would* happen without making changes.
7. **Validate outputs** — AI-generated content should pass automated quality checks (word count, link count, required sections) before publishing.

### Don'ts

1. **Don't publish without review** — automated article generation is powerful but not infallible. Build in a review step, even if it's just a quick scan of the output.
2. **Don't ignore API rate limits** — WordPress, Google APIs, and social media all have rate limits. Add delays between batch operations.
3. **Don't store secrets in git** — use `.gitignore` and environment variables.
4. **Don't over-automate** — some tasks (strategy decisions, creative direction, relationship building) should remain human.
5. **Don't skip error handling** — the one time you skip it is the time it breaks.

### Common Pitfalls

- **Path issues on Windows**: Use forward slashes or `os.path.join()`. Never hardcode backslashes.
- **Unicode in file paths**: If your OS uses non-ASCII characters in paths (e.g., Japanese), test scripts with those paths explicitly.
- **Token limits**: Long articles may exceed Claude's output limits. Split generation into sections.
- **Stale data**: Always verify that your analytics data and keyword research is fresh. Automate the data pull, not just the analysis.

### The Automation Mindset

The goal is not to automate everything on day one. The goal is to build a system where:

1. Every manual task you do more than twice gets a script.
2. Every script gets scheduled.
3. Every scheduled task gets monitored.
4. Every monitored result feeds back into strategy.

This creates a flywheel. The more you automate, the more time you have to build better automation. Within months, your business runs with minimal daily input from you.

---

## What's Included in This Playbook

- **This guide** (you're reading it)
- **20+ ready-to-use prompts** in the `prompts/` directory, covering SEO, content, products, analytics, and more
- **generate_thumbnail.py** — Python script for creating product thumbnails

Each prompt is a complete, copy-paste-ready Claude Code prompt with clear objectives, required inputs, expected outputs, and example usage.

---

*Built from real-world experience automating 15+ online businesses with Claude Code.*
