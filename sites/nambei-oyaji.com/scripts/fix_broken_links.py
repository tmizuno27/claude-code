#!/usr/bin/env python3
"""Fix broken internal links in WordPress posts by removing <a> tags and keeping anchor text."""

import re
import requests
from requests.auth import HTTPBasicAuth

# Auth
API_BASE = "https://nambei-oyaji.com/wp-json/wp/v2"
USERNAME = "t.mizuno27@gmail.com"
APP_PASSWORD = "WutS MaRq ukGx OcQ8 uhBj Ej0D"
auth = HTTPBasicAuth(USERNAME, APP_PASSWORD)

# Broken internal slugs to remove links for (404 only, not external 403/405)
BROKEN_SLUGS = [
    "kaigai-web-writer",
    "kaigai-blog-hajimekata",
    "kaigai-ijuu-junbi-list",
    "kaigai-vpn-osusume",
    "paraguay-eijuuken-torikata",
    "paraguay-kyouiku",
    "kaigai-ijuusha-skill",
    "paraguay-iryou-hoken",
    "paraguay-eijuuken",
    "paraguay-ginkou-kouzakaisetsu",
]

# Affected post IDs
POST_IDS = [1069, 1068, 1067, 1066, 1065]

def remove_broken_links(content, broken_slugs):
    """Remove <a> tags pointing to broken internal URLs, keeping anchor text."""
    changes = []
    for slug in broken_slugs:
        # Match <a href="...slug...">text</a> - handles attributes like target, rel, class etc.
        pattern = r'<a\s[^>]*href=["\']https://nambei-oyaji\.com/' + re.escape(slug) + r'/["\'][^>]*>(.*?)</a>'
        matches = re.findall(pattern, content, re.DOTALL | re.IGNORECASE)
        if matches:
            content = re.sub(pattern, r'\1', content, flags=re.DOTALL | re.IGNORECASE)
            changes.append(f"  - Removed {len(matches)} link(s) to /{slug}/: {matches}")
    return content, changes

def fix_post(post_id):
    print(f"\n=== Processing post ID {post_id} ===")

    # Fetch post with context=edit
    resp = requests.get(f"{API_BASE}/posts/{post_id}?context=edit", auth=auth)
    if resp.status_code != 200:
        print(f"  ERROR fetching post: {resp.status_code} {resp.text[:200]}")
        return False

    post = resp.json()
    title = post.get("title", {}).get("raw", "")
    content = post.get("content", {}).get("raw", "")

    print(f"  Title: {title}")
    print(f"  Content length: {len(content)} chars")

    # Fix broken links
    new_content, changes = remove_broken_links(content, BROKEN_SLUGS)

    if not changes:
        print("  No broken internal links found in this post.")
        return True

    print(f"  Changes made:")
    for c in changes:
        print(c)

    # Update post
    update_resp = requests.post(
        f"{API_BASE}/posts/{post_id}",
        auth=auth,
        json={"content": new_content}
    )

    if update_resp.status_code in (200, 201):
        print(f"  SUCCESS: Post updated.")
        return True
    else:
        print(f"  ERROR updating post: {update_resp.status_code} {update_resp.text[:300]}")
        return False

if __name__ == "__main__":
    print("Starting broken link fix...")
    results = {}
    for post_id in POST_IDS:
        results[post_id] = fix_post(post_id)

    print("\n=== Summary ===")
    for pid, success in results.items():
        status = "OK" if success else "FAILED"
        print(f"  Post {pid}: {status}")
