"""
3サイト一括 内部リンク不足記事検出 & 自動挿入スクリプト
"""
import sys
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

import requests
import re
import json
import time
from urllib.parse import urlparse
from html.parser import HTMLParser

# --- Site configurations ---
SITES = [
    {
        "name": "nambei-oyaji.com",
        "domain": "nambei-oyaji.com",
        "api_base": "https://nambei-oyaji.com/wp-json/wp/v2",
        "username": "t.mizuno27@gmail.com",
        "app_password": "WutS MaRq ukGx OcQ8 uhBj Ej0D",
    },
    {
        "name": "otona-match.com",
        "domain": "otona-match.com",
        # otona-match uses ?rest_route= style
        "api_base": "https://otona-match.com/?rest_route=/wp/v2",
        "username": "t.mizuno27@gmail.com",
        "app_password": "Yw4j OgFf wwzT o0mn wXQ9 TjYs",
    },
    {
        "name": "sim-hikaku.online",
        "domain": "sim-hikaku.online",
        "api_base": "https://sim-hikaku.online/wp-json/wp/v2",
        "username": "t.mizuno27@gmail.com",
        "app_password": "P4A1 P4eh Nk0z 29An hS6H 9OHq",
    },
]

MAX_UPDATES_PER_SITE = 10
MIN_INTERNAL_LINKS = 2
MAX_LINKS_TO_ADD = 3


def get_auth(site):
    return (site["username"], site["app_password"])


def fetch_all_posts(site):
    """Fetch all published posts with pagination."""
    posts = []
    page = 1
    while True:
        sep = "&" if "?" in site["api_base"] else "?"
        url = f"{site['api_base']}/posts{sep}per_page=100&page={page}&status=publish&_fields=id,title,slug,link,content"
        try:
            r = requests.get(url, auth=get_auth(site), timeout=30)
        except Exception as e:
            print(f"  [ERROR] Request failed page {page}: {e}")
            break
        if r.status_code != 200:
            print(f"  [WARN] Status {r.status_code} on page {page}")
            break
        data = r.json()
        if not data:
            break
        posts.extend(data)
        total_pages = int(r.headers.get("X-WP-TotalPages", 1))
        if page >= total_pages:
            break
        page += 1
        time.sleep(0.3)
    return posts


def count_internal_links(html, domain):
    """Count <a> tags pointing to the same domain."""
    pattern = re.compile(r'<a\s[^>]*href=["\']([^"\']+)["\']', re.IGNORECASE)
    count = 0
    for match in pattern.finditer(html):
        href = match.group(1)
        parsed = urlparse(href)
        if parsed.netloc == "" or domain in parsed.netloc:
            # skip anchors and empty
            if href.startswith("#") or href == "":
                continue
            count += 1
    return count


def has_auto_links(html):
    return "internal-links-auto" in html


def simple_keyword_match(post_title, post_content, candidate_title, candidate_slug):
    """Simple relevance scoring based on shared words."""
    # Extract meaningful words from target post title
    title_text = re.sub(r'<[^>]+>', '', post_title).lower()
    # Japanese: split by common particles/spaces; also keep full title for substring match
    words = set(re.findall(r'[\w\u3040-\u9fff]+', title_text))

    cand_title_text = re.sub(r'<[^>]+>', '', candidate_title).lower()
    cand_slug_text = candidate_slug.lower().replace("-", " ")
    cand_words = set(re.findall(r'[\w\u3040-\u9fff]+', cand_title_text + " " + cand_slug_text))

    # Score: number of overlapping meaningful words (len >= 2)
    meaningful = {w for w in words if len(w) >= 2}
    cand_meaningful = {w for w in cand_words if len(w) >= 2}
    overlap = meaningful & cand_meaningful
    return len(overlap)


def select_related_posts(target_post, all_posts, max_count=3):
    """Select top related posts by keyword overlap."""
    target_id = target_post["id"]
    target_title = target_post["title"]["rendered"]
    target_content = target_post["content"]["rendered"]

    scored = []
    for p in all_posts:
        if p["id"] == target_id:
            continue
        score = simple_keyword_match(
            target_title, target_content,
            p["title"]["rendered"], p["slug"]
        )
        if score > 0:
            scored.append((score, p))

    scored.sort(key=lambda x: -x[0])
    return [p for _, p in scored[:max_count]]


def build_links_html(related_posts):
    items = ""
    for p in related_posts:
        title = re.sub(r'<[^>]+>', '', p["title"]["rendered"])
        url = p["link"]
        items += f'<li><a href="{url}">{title}</a></li>'
    return f'<div class="internal-links-auto"><h3>あわせて読みたい</h3><ul>{items}</ul></div>'


def insert_links_before_last_p(html, links_html):
    """Insert before the last </p>."""
    # Find last </p>
    idx = html.rfind("</p>")
    if idx == -1:
        # fallback: append
        return html + links_html
    return html[:idx] + "</p>" + links_html + html[idx+4:]


def update_post(site, post_id, new_content):
    sep = "&" if "?" in site["api_base"] else "?"
    url = f"{site['api_base']}/posts/{post_id}"
    r = requests.post(
        url,
        auth=get_auth(site),
        json={"content": new_content},
        timeout=30,
    )
    return r.status_code, r.text


def process_site(site):
    print(f"\n{'='*60}")
    print(f"Processing: {site['name']}")
    print(f"{'='*60}")

    posts = fetch_all_posts(site)
    print(f"  Total published posts: {len(posts)}")

    if not posts:
        print("  No posts found. Skipping.")
        return

    # Find posts with insufficient internal links
    lacking = []
    for p in posts:
        html = p["content"]["rendered"]
        if has_auto_links(html):
            continue
        count = count_internal_links(html, site["domain"])
        if count < MIN_INTERNAL_LINKS:
            lacking.append((p, count))

    print(f"  Posts with < {MIN_INTERNAL_LINKS} internal links: {len(lacking)}")

    if not lacking:
        print("  All posts have sufficient internal links!")
        return

    # Sort by fewest links first
    lacking.sort(key=lambda x: x[1])

    updated_count = 0
    total_links_added = 0

    for post, current_count in lacking[:MAX_UPDATES_PER_SITE]:
        title = re.sub(r'<[^>]+>', '', post["title"]["rendered"])
        print(f"\n  [{post['id']}] {title} (current internal links: {current_count})")

        related = select_related_posts(post, posts, MAX_LINKS_TO_ADD)
        if not related:
            print(f"    -> No related posts found. Skipping.")
            continue

        links_html = build_links_html(related)
        original_html = post["content"]["rendered"]
        new_html = insert_links_before_last_p(original_html, links_html)

        status, resp = update_post(site, post["id"], new_html)
        if status == 200:
            num_added = len(related)
            total_links_added += num_added
            updated_count += 1
            rel_titles = [re.sub(r'<[^>]+>', '', r["title"]["rendered"]) for r in related]
            print(f"    -> Added {num_added} links: {', '.join(rel_titles)}")
        else:
            print(f"    -> UPDATE FAILED (status {status}): {resp[:200]}")

        time.sleep(0.5)

    print(f"\n  --- {site['name']} Summary ---")
    print(f"  Updated: {updated_count} posts")
    print(f"  Total links added: {total_links_added}")


def main():
    print("=" * 60)
    print("Internal Link Auto-Inserter — 3 Sites")
    print("=" * 60)

    for site in SITES:
        try:
            process_site(site)
        except Exception as e:
            print(f"\n  [CRITICAL ERROR] {site['name']}: {e}")

    print("\n" + "=" * 60)
    print("All sites processed.")
    print("=" * 60)


if __name__ == "__main__":
    main()
