# WordPress Internal Link API - The Only REST API for Internal Link Optimization

**Every WordPress plugin does internal linking. No REST API does.** Link Whisper, Yoast, Internal Link Juicer -- they're all locked inside WordPress admin. This API lets you automate internal link suggestions from any script, CI/CD pipeline, headless CMS, or custom tool.

> Free tier: 100 analyses/month | Keyword matching + relevance scoring | Works with any CMS, not just WordPress

## Why WordPress Developers Need This

Internal linking is the most neglected SEO lever. Studies show sites with strong internal linking rank 40% higher for competitive keywords. But manually finding link opportunities across 100+ posts is brutal.

**This API analyzes your article content against your sitemap or page list and returns ranked link suggestions with anchor text, target URL, and relevance score (0-100).**

## How It Compares to WordPress Plugins

| | **This API** | Link Whisper | Yoast Internal | Internal Link Juicer |
|---|---|---|---|---|
| **API access** | **REST API** | No (WP plugin) | No (WP plugin) | No (WP plugin) |
| **Free tier** | 100 req/mo | None ($77/yr) | Yoast Premium ($99/yr) | Free (limited) |
| **Headless CMS support** | **Yes** | No | No | No |
| **CI/CD integration** | **Yes** | No | No | No |
| **Bulk analysis** | **Yes (via API loop)** | Yes (WP admin) | No | No |
| **Custom tool integration** | **Yes (any language)** | No | No | No |
| **Relevance scoring** | 0-100 | Yes | Basic | Basic |
| **Works outside WordPress** | **Yes** | No | No | No |
| **Platform** | Any (Python, JS, PHP, etc.) | WordPress only | WordPress only | WordPress only |

## Quick Start - Python (WordPress Integration)

```python
import requests

# Analyze an article against your site's other posts
url = "https://wp-internal-link-api.p.rapidapi.com/analyze"
headers = {
    "X-RapidAPI-Key": "YOUR_KEY",
    "X-RapidAPI-Host": "wp-internal-link-api.p.rapidapi.com",
    "Content-Type": "application/json"
}

payload = {
    "article_html": "<p>WordPress performance optimization is critical for SEO. Page speed affects rankings, and caching can reduce load times by 50%. Consider using a CDN for static assets.</p>",
    "article_title": "How to Speed Up WordPress",
    "pages": [
        {"url": "/wordpress-caching-guide", "title": "Complete WordPress Caching Guide"},
        {"url": "/cdn-setup-tutorial", "title": "How to Set Up a CDN for WordPress"},
        {"url": "/seo-checklist", "title": "WordPress SEO Checklist for 2024"},
        {"url": "/plugin-recommendations", "title": "Best WordPress Plugins"}
    ]
}

response = requests.post(url, headers=headers, json=payload)
suggestions = response.json()["suggestions"]

for s in suggestions:
    print(f"Link \"{s['anchor']}\" -> {s['url']} (relevance: {s['score']}/100)")
# Output:
# Link "caching" -> /wordpress-caching-guide (relevance: 92/100)
# Link "CDN" -> /cdn-setup-tutorial (relevance: 88/100)
# Link "SEO" -> /seo-checklist (relevance: 71/100)
```

## Quick Start - JavaScript / Node.js

```javascript
const axios = require("axios");

const { data } = await axios.post(
  "https://wp-internal-link-api.p.rapidapi.com/analyze",
  {
    article_html: "<p>Your article about WordPress security best practices...</p>",
    sitemap_url: "https://your-wordpress-site.com/sitemap.xml"
  },
  {
    headers: {
      "X-RapidAPI-Key": "YOUR_KEY",
      "X-RapidAPI-Host": "wp-internal-link-api.p.rapidapi.com",
    },
  }
);

// Insert top suggestions into article
data.suggestions
  .filter(s => s.score >= 70)
  .forEach(s => {
    console.log(`Add link: "${s.anchor}" -> ${s.url} (score: ${s.score})`);
  });
```

## Quick Start - PHP (WordPress Plugin Integration)

```php
<?php
// Use inside a WordPress plugin or custom function
$response = wp_remote_post(
    'https://wp-internal-link-api.p.rapidapi.com/analyze',
    array(
        'headers' => array(
            'X-RapidAPI-Key' => 'YOUR_KEY',
            'X-RapidAPI-Host' => 'wp-internal-link-api.p.rapidapi.com',
            'Content-Type' => 'application/json',
        ),
        'body' => json_encode(array(
            'article_html' => get_the_content(),
            'article_title' => get_the_title(),
            'sitemap_url' => home_url('/sitemap.xml'),
        )),
    )
);

$suggestions = json_decode(wp_remote_retrieve_body($response), true)['suggestions'];

foreach ($suggestions as $s) {
    if ($s['score'] >= 70) {
        echo "Link '{$s['anchor']}' to {$s['url']} (score: {$s['score']})\n";
    }
}
```

## Automated WordPress Workflow

### Scenario: Auto-Link New Posts on Publish

```python
import requests
import json

WP_URL = "https://your-site.com/wp-json/wp/v2"
WP_AUTH = ("username", "application_password")
RAPIDAPI_KEY = "YOUR_KEY"

# 1. Get the new post content
post = requests.get(f"{WP_URL}/posts/123", auth=WP_AUTH).json()

# 2. Get link suggestions from API
suggestions = requests.post(
    "https://wp-internal-link-api.p.rapidapi.com/analyze",
    headers={
        "X-RapidAPI-Key": RAPIDAPI_KEY,
        "X-RapidAPI-Host": "wp-internal-link-api.p.rapidapi.com",
        "Content-Type": "application/json"
    },
    json={
        "article_html": post["content"]["rendered"],
        "article_title": post["title"]["rendered"],
        "sitemap_url": "https://your-site.com/sitemap.xml"
    }
).json()["suggestions"]

# 3. Auto-insert high-confidence links
content = post["content"]["rendered"]
for s in suggestions:
    if s["score"] >= 80:
        content = content.replace(
            s["anchor"],
            f'<a href="{s["url"]}">{s["anchor"]}</a>',
            1  # Replace first occurrence only
        )

# 4. Update post with linked content
requests.post(
    f"{WP_URL}/posts/123",
    auth=WP_AUTH,
    json={"content": content}
)
print(f"Inserted {len([s for s in suggestions if s['score'] >= 80])} internal links")
```

## Endpoints

| Endpoint | Method | Description | Input |
|----------|--------|-------------|-------|
| `/analyze` | POST | Full link analysis with ranked suggestions | article_html + sitemap_url or pages array |
| `/suggest` | POST | Quick keyword-to-URL matching | article_text + pages array |
| `/health` | GET | API health check | None |

### `/analyze` Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `article_html` | string | Yes | HTML content of the article to analyze |
| `article_title` | string | No | Article title (improves accuracy) |
| `sitemap_url` | string | No* | URL of your XML sitemap |
| `pages` | array | No* | Array of `{url, title, content}` objects |

*Provide either `sitemap_url` or `pages`.

### `/suggest` Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `article_text` | string | Yes | Plain text content |
| `pages` | array | Yes | Array of `{url, title}` objects |

## Use Cases for WordPress Developers

### WP-CLI Script for Bulk Internal Linking
Iterate all published posts, analyze each against your sitemap, and auto-insert links for suggestions scoring 80+. Run monthly as a cron job.

### Gutenberg Block / Plugin
Build a sidebar panel in the block editor that shows link suggestions in real-time as the author writes. Click to insert.

### Headless WordPress (Next.js, Gatsby, Astro)
If you're using WordPress as a headless CMS with a JS frontend, traditional WP plugins don't work. This API gives you the same internal linking intelligence via REST.

### Content Migration
Moving to WordPress from another CMS? Analyze all migrated content and build internal links from scratch. The API identifies opportunities your old CMS never surfaced.

### Multi-Site Management (Agencies)
Manage 10+ WordPress sites? Run link analysis across all sites in a single script. No need to install and configure plugins on each site.

## Pricing

| Plan | Price | Analyses/mo | Rate Limit | Best For |
|------|-------|-------------|------------|----------|
| **Basic (FREE)** | $0 | 100 | 1/sec | Single blog, testing |
| **Pro** | $9.99 | 1,000 | 5/sec | Active blog (50-200 posts) |
| **Ultra** | $29.99 | 10,000 | 20/sec | Agency, multi-site |

## FAQ

**Q: Do I need a WordPress site to use this?**
A: No. While designed for WordPress workflows, the API works with any HTML content and page list. Use it with Ghost, Hugo, Astro, or any CMS.

**Q: How are suggestions scored?**
A: 0-100 relevance score based on keyword match quality, position in content, and contextual relevance. We recommend inserting links with score >= 70.

**Q: Can I pass my full sitemap?**
A: Yes. The `sitemap_url` parameter accepts a standard XML sitemap URL. The API will parse it and match your content against all listed pages.

**Q: How many pages can I include?**
A: Up to 500 pages in the `pages` array. For larger sites, use `sitemap_url` or batch with relevant subsets.

**Q: Will this work with Gutenberg block content?**
A: Yes. The API analyzes raw HTML, which is what Gutenberg produces. Pass `post.content.rendered` from the WP REST API.


## Also From This Publisher

Build powerful workflows by combining APIs:

| API | Why Combine? |
|-----|-------------|
| **SEO Analyzer API** | Full SEO audit alongside link optimization |
| **Link Preview API** | Extract metadata for link context |
| **Text Analysis API** | Analyze content for keyword relevance |
| **AI Text API** | Generate anchor text suggestions |

> All APIs include a free tier. Subscribe to one, discover the full toolkit on [our RapidAPI profile](https://rapidapi.com/miccho27-5OJaGGbBiO).

## Keywords

`wordpress internal link api`, `internal linking api`, `wp seo api`, `link suggestion api`, `internal link optimization`, `wordpress developer api`, `link whisper alternative`, `headless wordpress seo`, `anchor text api`, `content linking automation`, `wordpress rest api seo`, `internal link audit`
