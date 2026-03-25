---
title: "Automate WordPress Internal Linking with a Free API — Better Than Link Whisper for Developers"
published: false
description: "A free API that analyzes your WordPress content and suggests internal links with relevance scores. Replaces $77/year plugins with programmable SEO automation. Python & JS examples."
tags: wordpress, seo, api, webdev
---

Internal linking is one of the most underrated SEO tactics. Every audit tool tells you "add more internal links" — but none of them tell you **which links** to add or **where to put them**.

I built a free API that analyzes your WordPress content and returns specific internal link suggestions: exact anchor text, source URL, target URL, and a relevance score.

## The Problem

You have 50+ blog posts. Each new article should link to 3-5 existing posts. Manually scanning your entire archive to find relevant links doesn't scale. And as your content grows, older posts miss out on links to newer articles.

Plugins like **Link Whisper** ($77/year) solve this inside the WordPress admin — but what if you want:

- **Programmatic control** — integrate with your publishing pipeline
- **Bulk analysis** — audit hundreds of posts via script
- **Custom logic** — filter by category, set minimum relevance scores, auto-insert links before publishing
- **Headless WordPress** — internal linking for Next.js/Gatsby sites using WP as a CMS

That's where an API beats a plugin.

## How It Works

Send your article content plus a list of existing posts. The API analyzes semantic relevance and returns ranked link suggestions.

### Python — Analyze a New Post Before Publishing

```python
import requests

url = "https://wp-internal-link-api.p.rapidapi.com/analyze"
headers = {
    "X-RapidAPI-Key": "YOUR_KEY",
    "X-RapidAPI-Host": "wp-internal-link-api.p.rapidapi.com",
    "Content-Type": "application/json",
}

payload = {
    "content": "<p>Moving to Paraguay offers surprisingly low taxes and an affordable cost of living. The residency process is straightforward compared to most South American countries.</p>",
    "site_url": "https://yourblog.com",
    "existing_posts": [
        {
            "url": "/cost-of-living-paraguay",
            "title": "Cost of Living in Paraguay 2026",
            "keywords": ["cost", "living", "expenses", "paraguay"],
        },
        {
            "url": "/paraguay-visa-guide",
            "title": "Paraguay Visa & Residency Guide",
            "keywords": ["visa", "residency", "immigration", "paraguay"],
        },
        {
            "url": "/best-cities-paraguay",
            "title": "Best Cities to Live in Paraguay",
            "keywords": ["cities", "asuncion", "encarnacion", "paraguay"],
        },
    ],
}

response = requests.post(url, json=payload, headers=headers)
data = response.json()

for suggestion in data["suggestions"]:
    print(
        f"Link '{suggestion['anchor_text']}' -> {suggestion['target_url']} "
        f"(relevance: {suggestion['relevance_score']:.2f})"
    )
```

**Output:**

```json
{
  "suggestions": [
    {
      "anchor_text": "affordable cost of living",
      "target_url": "/cost-of-living-paraguay",
      "relevance_score": 0.89,
      "context": "...offers surprisingly low taxes and an affordable cost of living..."
    },
    {
      "anchor_text": "residency process",
      "target_url": "/paraguay-visa-guide",
      "relevance_score": 0.82,
      "context": "The residency process is straightforward..."
    }
  ],
  "total_suggestions": 2
}
```

### Python — Full Pipeline: Fetch from WP, Analyze, Insert Links

```python
import requests
import re

WP_URL = "https://yourblog.com/wp-json/wp/v2"
WP_AUTH = ("username", "application_password")
RAPIDAPI_HEADERS = {
    "X-RapidAPI-Key": "YOUR_KEY",
    "X-RapidAPI-Host": "wp-internal-link-api.p.rapidapi.com",
    "Content-Type": "application/json",
}


def get_all_posts():
    """Fetch all published posts from WordPress."""
    posts = []
    page = 1
    while True:
        resp = requests.get(
            f"{WP_URL}/posts",
            params={"per_page": 100, "page": page, "status": "publish"},
            auth=WP_AUTH,
        )
        batch = resp.json()
        if not batch:
            break
        posts.extend(batch)
        page += 1
    return posts


def get_link_suggestions(content: str, existing_posts: list) -> list:
    """Get internal link suggestions from the API."""
    resp = requests.post(
        "https://wp-internal-link-api.p.rapidapi.com/analyze",
        headers=RAPIDAPI_HEADERS,
        json={
            "content": content,
            "existing_posts": existing_posts,
        },
    )
    return resp.json().get("suggestions", [])


def insert_links(html: str, suggestions: list, min_score: float = 0.7) -> str:
    """Insert internal links into HTML content."""
    modified = html
    for s in suggestions:
        if s["relevance_score"] < min_score:
            continue
        anchor = s["anchor_text"]
        link = f'<a href="{s["target_url"]}">{anchor}</a>'
        # Replace first occurrence only (avoid double-linking)
        modified = modified.replace(anchor, link, 1)
    return modified


# Main workflow
posts = get_all_posts()
existing = [
    {"url": p["link"], "title": p["title"]["rendered"], "keywords": []}
    for p in posts
]

for post in posts:
    suggestions = get_link_suggestions(post["content"]["rendered"], existing)
    if not suggestions:
        continue

    updated_content = insert_links(post["content"]["rendered"], suggestions)
    if updated_content != post["content"]["rendered"]:
        requests.post(
            f"{WP_URL}/posts/{post['id']}",
            auth=WP_AUTH,
            json={"content": updated_content},
        )
        print(f"Updated: {post['title']['rendered']} (+{len(suggestions)} links)")
```

This is a complete automation: fetch posts, analyze, insert links, update WordPress. Run it weekly as a cron job.

### JavaScript — Internal Link Suggestions Widget

```javascript
async function getSuggestions(content, existingPosts) {
  const res = await fetch(
    "https://wp-internal-link-api.p.rapidapi.com/analyze",
    {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        "X-RapidAPI-Key": "YOUR_KEY",
        "X-RapidAPI-Host": "wp-internal-link-api.p.rapidapi.com",
      },
      body: JSON.stringify({ content, existing_posts: existingPosts }),
    }
  );
  return res.json();
}

// Example: Show suggestions in a sidebar while editing
async function showLinkSuggestions() {
  const content = document.querySelector("#editor").innerHTML;
  const posts = await fetch("/wp-json/wp/v2/posts?per_page=100").then((r) =>
    r.json()
  );

  const existingPosts = posts.map((p) => ({
    url: new URL(p.link).pathname,
    title: p.title.rendered,
    keywords: [],
  }));

  const { suggestions } = await getSuggestions(content, existingPosts);

  const sidebar = document.querySelector("#link-suggestions");
  sidebar.innerHTML = suggestions
    .map(
      (s) =>
        `<div class="suggestion">
          <strong>"${s.anchor_text}"</strong> →
          <a href="${s.target_url}">${s.target_url}</a>
          <span class="score">${Math.round(s.relevance_score * 100)}%</span>
        </div>`
    )
    .join("");
}
```

## How It Compares

| Feature | WP Internal Link API | Link Whisper | Yoast SEO | Rank Math |
|---------|---------------------|--------------|-----------|-----------|
| API access | Yes | No | No | No |
| Price | Free (500 req/mo) | $77/year | $99/year | $59/year |
| Bulk analysis | Yes (scripted) | Manual clicks | No | No |
| Headless WP support | Yes | No | No | No |
| Relevance scoring | 0-1.0 | Basic | None | None |
| CI/CD integration | Yes | No | No | No |

## Use Cases

1. **Content pipeline automation** — Auto-insert internal links before publishing via WP REST API
2. **Orphan page detection** — Find posts with zero incoming internal links
3. **Headless WordPress** — Internal linking for Next.js/Gatsby/Astro sites
4. **SEO audit scripts** — Analyze your entire site's internal link structure
5. **WordPress plugin backend** — Build a custom linking plugin powered by this API

## Try It Free

1. [WP Internal Link API on RapidAPI](https://rapidapi.com/miccho27-5OJaGGbBiO/api/wp-internal-link-api)
2. Free plan: 500 requests/month, no credit card
3. POST your content, get link suggestions in <100ms

---

**Do you automate internal linking?** I'd love to hear your workflow — drop a comment below.

*Part of a [collection of 24 free developer APIs](https://rapidapi.com/user/miccho27-5OJaGGbBiO) on Cloudflare Workers.*
