"""
3サイト一括 内部リンク自動挿入スクリプト
- WP REST APIで全公開記事を取得
- 内部リンク2本未満の記事を検出
- 関連記事を選定し末尾に挿入
"""

import requests
import re
import json
import sys
from urllib.parse import urlparse
from difflib import SequenceMatcher

# サイト設定
SITES = [
    {
        "name": "nambei-oyaji.com",
        "url": "https://nambei-oyaji.com",
        "api_base": "https://nambei-oyaji.com/wp-json/wp/v2",
        "username": "t.mizuno27@gmail.com",
        "app_password": "WutS MaRq ukGx OcQ8 uhBj Ej0D",
    },
    {
        "name": "otona-match.com",
        "url": "https://otona-match.com",
        "api_base": "https://otona-match.com/?rest_route=/wp/v2",
        "username": "t.mizuno27@gmail.com",
        "app_password": "Yw4j OgFf wwzT o0mn wXQ9 TjYs",
    },
    {
        "name": "sim-hikaku.online",
        "url": "https://sim-hikaku.online",
        "api_base": "https://sim-hikaku.online/wp-json/wp/v2",
        "username": "t.mizuno27@gmail.com",
        "app_password": "P4A1 P4eh Nk0z 29An hS6H 9OHq",
    },
]

MAX_UPDATES_PER_SITE = 10
MIN_RELATED = 1  # At least 1 related article to insert


def fetch_all_posts(site):
    """Fetch all published posts with pagination."""
    posts = []
    page = 1
    while True:
        url = f"{site['api_base']}/posts"
        params = {"per_page": 100, "status": "publish", "page": page}
        resp = requests.get(url, params=params, auth=(site["username"], site["app_password"]), timeout=30)
        if resp.status_code != 200:
            print(f"  [ERROR] Failed to fetch posts page {page}: {resp.status_code}")
            break
        data = resp.json()
        if not data:
            break
        posts.extend(data)
        total_pages = int(resp.headers.get("X-WP-TotalPages", 1))
        if page >= total_pages:
            break
        page += 1
    return posts


def count_internal_links(html, domain):
    """Count internal links in HTML content."""
    pattern = r'<a\s[^>]*href=["\']([^"\']+)["\'][^>]*>'
    links = re.findall(pattern, html, re.IGNORECASE)
    count = 0
    for link in links:
        parsed = urlparse(link)
        link_domain = parsed.netloc.lower().replace("www.", "")
        if link_domain == domain or (not parsed.netloc and link.startswith("/")):
            count += 1
    return count


def has_auto_links(html):
    """Check if auto-inserted links already exist."""
    return "internal-links-auto" in html


def extract_keywords(title, slug):
    """Extract keywords from title and slug for matching."""
    # Remove common Japanese particles and combine
    words = set()
    # From slug
    for part in slug.split("-"):
        if len(part) > 2:
            words.add(part.lower())
    # From title - extract meaningful chunks
    title_clean = re.sub(r'[【】\[\]「」（）()｜|！!？?、。・]', ' ', title)
    for w in title_clean.split():
        if len(w) >= 2:
            words.add(w.lower())
    return words


def find_related_posts(target_post, all_posts, domain, max_results=3):
    """Find related posts based on title/slug similarity."""
    target_kw = extract_keywords(
        target_post["title"]["rendered"],
        target_post["slug"]
    )
    if not target_kw:
        return []

    scores = []
    for post in all_posts:
        if post["id"] == target_post["id"]:
            continue
        post_kw = extract_keywords(post["title"]["rendered"], post["slug"])
        # Calculate overlap
        if not post_kw:
            continue
        overlap = len(target_kw & post_kw)
        # Also check title similarity
        title_sim = SequenceMatcher(
            None,
            target_post["title"]["rendered"],
            post["title"]["rendered"]
        ).ratio()
        # Combined score
        score = overlap * 2 + title_sim
        if score > 0.3:
            scores.append((score, post))

    scores.sort(key=lambda x: x[0], reverse=True)
    return [p for _, p in scores[:max_results]]


def build_link_section(related_posts, domain):
    """Build the HTML for related links section."""
    if not related_posts:
        return ""
    items = []
    for post in related_posts:
        url = post["link"]
        title = post["title"]["rendered"]
        items.append(f'<li><a href="{url}">{title}</a></li>')
    return (
        '<div class="internal-links-auto">'
        '<h3>あわせて読みたい</h3>'
        '<ul>' + ''.join(items) + '</ul>'
        '</div>'
    )


def insert_links_at_end(content, link_section):
    """Insert link section before the last closing </p> tag."""
    # Find last </p>
    last_p = content.rfind("</p>")
    if last_p == -1:
        # No </p> found, append at end
        return content + link_section
    return content[:last_p + 4] + "\n" + link_section + content[last_p + 4:]


def update_post(site, post_id, new_content):
    """Update post content via WP REST API."""
    url = f"{site['api_base']}/posts/{post_id}"
    resp = requests.post(
        url,
        json={"content": new_content},
        auth=(site["username"], site["app_password"]),
        timeout=30,
    )
    return resp.status_code == 200, resp.status_code


def process_site(site):
    """Process a single site."""
    domain = urlparse(site["url"]).netloc.replace("www.", "")
    print(f"\n{'='*60}")
    print(f"Processing: {site['name']}")
    print(f"{'='*60}")

    # Fetch all posts
    posts = fetch_all_posts(site)
    print(f"  Total published posts: {len(posts)}")

    if not posts:
        return 0, 0

    # Find posts with < 2 internal links
    deficient = []
    for post in posts:
        content = post["content"]["rendered"]
        if has_auto_links(content):
            continue
        link_count = count_internal_links(content, domain)
        if link_count < 2:
            deficient.append((post, link_count))

    print(f"  Posts with < 2 internal links: {len(deficient)}")

    if not deficient:
        print("  All posts have sufficient internal links!")
        return 0, 0

    # Process up to MAX_UPDATES_PER_SITE
    updated = 0
    total_links_added = 0

    for post, current_links in deficient[:MAX_UPDATES_PER_SITE]:
        title = post["title"]["rendered"]
        related = find_related_posts(post, posts, domain, max_results=3)

        if len(related) < MIN_RELATED:
            print(f"  SKIP: [{post['id']}] {title} — no related posts found")
            continue

        link_section = build_link_section(related, domain)
        # Use raw content for update
        # We need to get the raw content
        raw_content = post["content"].get("raw", post["content"]["rendered"])

        # If raw is same as rendered (no raw available), fetch raw
        if "raw" not in post["content"]:
            fetch_url = f"{site['api_base']}/posts/{post['id']}?context=edit"
            resp = requests.get(
                fetch_url,
                auth=(site["username"], site["app_password"]),
                timeout=30,
            )
            if resp.status_code == 200:
                raw_content = resp.json()["content"]["raw"]
            else:
                raw_content = post["content"]["rendered"]

        if has_auto_links(raw_content):
            print(f"  SKIP: [{post['id']}] {title} — already has auto links (raw)")
            continue

        new_content = insert_links_at_end(raw_content, link_section)
        success, status = update_post(site, post["id"], new_content)

        if success:
            updated += 1
            total_links_added += len(related)
            related_titles = [r["title"]["rendered"] for r in related]
            print(f"  OK: [{post['id']}] {title} — +{len(related)} links")
            for rt in related_titles:
                print(f"       -> {rt}")
        else:
            print(f"  FAIL: [{post['id']}] {title} — HTTP {status}")

    return updated, total_links_added


def main():
    print("=" * 60)
    print("Internal Link Auto-Inserter — 3 Sites")
    print("=" * 60)

    grand_updated = 0
    grand_links = 0

    for site in SITES:
        updated, links = process_site(site)
        grand_updated += updated
        grand_links += links

    print(f"\n{'='*60}")
    print(f"SUMMARY")
    print(f"{'='*60}")
    print(f"Total posts updated: {grand_updated}")
    print(f"Total links added:   {grand_links}")


if __name__ == "__main__":
    main()
