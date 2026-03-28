"""
WordPress Storage Cleanup Script
- Delete old revisions (keep latest 3 per post)
- Empty trash
- Test API connectivity after cleanup
"""

import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
import json
import time
from pathlib import Path


def create_session():
    """Create a requests session with retry logic."""
    s = requests.Session()
    retries = Retry(total=3, backoff_factor=2, status_forcelist=[500, 502, 503, 507])
    s.mount("https://", HTTPAdapter(max_retries=retries))
    return s


SESSION = create_session()
TIMEOUT = 120

SITES = [
    {
        "name": "otona-match.com",
        "url": "https://otona-match.com",
        "api": "https://otona-match.com/wp-json/wp/v2",
        "username": "t.mizuno27@gmail.com",
        "app_password": "Yw4j OgFf wwzT o0mn wXQ9 TjYs",
    },
    {
        "name": "sim-hikaku.online",
        "url": "https://sim-hikaku.online",
        "api": "https://sim-hikaku.online/wp-json/wp/v2",
        "username": "t.mizuno27@gmail.com",
        "app_password": "P4A1 P4eh Nk0z 29An hS6H 9OHq",
    },
]

KEEP_REVISIONS = 3


def get_auth(site):
    return (site["username"], site["app_password"])


def get_all_posts(site):
    """Get all published/draft posts and pages."""
    all_items = []
    for post_type in ["posts", "pages"]:
        page = 1
        while True:
            resp = SESSION.get(
                f"{site['api']}/{post_type}",
                auth=get_auth(site),
                params={"per_page": 100, "page": page, "status": "publish,draft,private"},
                timeout=TIMEOUT,
            )
            if resp.status_code != 200:
                break
            items = resp.json()
            if not items:
                break
            all_items.extend([(item["id"], item["title"]["rendered"], post_type) for item in items])
            page += 1
    return all_items


def delete_old_revisions(site):
    """Delete revisions keeping only the latest KEEP_REVISIONS per post."""
    posts = get_all_posts(site)
    total_deleted = 0
    print(f"\n[{site['name']}] Found {len(posts)} posts/pages. Checking revisions...")

    for post_id, title, post_type in posts:
        # Get revisions for this post
        endpoint = f"{site['api']}/{post_type}/{post_id}/revisions"
        resp = SESSION.get(endpoint, auth=get_auth(site), timeout=TIMEOUT)
        if resp.status_code != 200:
            continue
        revisions = resp.json()
        if len(revisions) <= KEEP_REVISIONS:
            continue

        # Sort by date desc (API returns newest first), delete old ones
        to_delete = revisions[KEEP_REVISIONS:]
        short_title = title[:30] if title else f"ID:{post_id}"
        print(f"  [{short_title}] {len(revisions)} revisions -> deleting {len(to_delete)}")

        for rev in to_delete:
            del_resp = SESSION.delete(
                f"{site['api']}/{post_type}/{post_id}/revisions/{rev['id']}",
                auth=get_auth(site),
                params={"force": True},
                timeout=TIMEOUT,
            )
            if del_resp.status_code == 200:
                total_deleted += 1
            else:
                print(f"    WARN: Failed to delete revision {rev['id']}: {del_resp.status_code}")
            time.sleep(0.3)

    print(f"  -> Deleted {total_deleted} revisions")
    return total_deleted


def empty_trash(site):
    """Delete all trashed posts and pages permanently."""
    total_deleted = 0
    for post_type in ["posts", "pages"]:
        page = 1
        while True:
            resp = SESSION.get(
                f"{site['api']}/{post_type}",
                auth=get_auth(site),
                params={"per_page": 100, "page": page, "status": "trash"},
                timeout=TIMEOUT,
            )
            if resp.status_code != 200:
                break
            items = resp.json()
            if not items:
                break

            for item in items:
                del_resp = SESSION.delete(
                    f"{site['api']}/{post_type}/{item['id']}",
                    auth=get_auth(site),
                    params={"force": True},
                    timeout=TIMEOUT,
                )
                if del_resp.status_code == 200:
                    total_deleted += 1
                    print(f"  Trash deleted: {item['title']['rendered'][:40]}")
                else:
                    print(f"  WARN: Failed to delete trash {item['id']}: {del_resp.status_code}")
                time.sleep(0.3)
            page += 1

    print(f"  -> Deleted {total_deleted} trashed items")
    return total_deleted


def delete_unattached_media(site):
    """Delete media not attached to any post."""
    total_deleted = 0
    page = 1
    while True:
        resp = SESSION.get(
            f"{site['api']}/media",
            auth=get_auth(site),
            params={"per_page": 100, "page": page},
            timeout=TIMEOUT,
        )
        if resp.status_code != 200:
            break
        items = resp.json()
        if not items:
            break

        for item in items:
            if item.get("post") is None or item.get("post") == 0:
                del_resp = SESSION.delete(
                    f"{site['api']}/media/{item['id']}",
                    auth=get_auth(site),
                    params={"force": True},
                    timeout=TIMEOUT,
                )
                if del_resp.status_code == 200:
                    total_deleted += 1
                else:
                    print(f"  WARN: Failed to delete media {item['id']}: {del_resp.status_code}")
                time.sleep(0.3)
        page += 1

    print(f"  -> Deleted {total_deleted} unattached media items")
    return total_deleted


def test_api(site):
    """Test if the API is responsive (507 resolved)."""
    try:
        resp = SESSION.get(
            f"{site['api']}/posts",
            auth=get_auth(site),
            params={"per_page": 1},
            timeout=TIMEOUT,
        )
        print(f"  API test: HTTP {resp.status_code}")
        return resp.status_code == 200
    except Exception as e:
        print(f"  API test failed: {e}")
        return False


def main():
    for site in SITES:
        print(f"\n{'='*60}")
        print(f"Processing: {site['name']}")
        print(f"{'='*60}")

        # 1. Delete old revisions
        rev_count = delete_old_revisions(site)

        # 2. Empty trash
        trash_count = empty_trash(site)

        # 3. Delete unattached media
        media_count = delete_unattached_media(site)

        # 4. Test API
        print(f"\n  Summary: {rev_count} revisions + {trash_count} trash + {media_count} media deleted")
        print(f"  Testing API...")
        ok = test_api(site)
        print(f"  Result: {'OK - 507 resolved!' if ok else 'Still having issues'}")


if __name__ == "__main__":
    main()
