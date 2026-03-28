"""
Batch submit URLs to Google Indexing API for sim-hikaku.online.
Fetches all URLs from wp-sitemap.xml, then submits up to 200 (daily quota).
Uses batch HTTP endpoint for efficiency.
"""

import json
import time
import sys
import xml.etree.ElementTree as ET
from pathlib import Path

import requests
from google.oauth2 import service_account
from google.auth.transport.requests import AuthorizedSession

# Config
SITE_DOMAIN = "https://sim-hikaku.online"
CREDENTIALS_PATH = Path(r"C:\Users\tmizu\マイドライブ\GitHub\claude-code\sites\nambei-oyaji.com\config\gsc-credentials.json")
SCOPES = ["https://www.googleapis.com/auth/indexing"]
INDEXING_API_URL = "https://indexing.googleapis.com/v3/urlNotifications:publish"
BATCH_URL = "https://indexing.googleapis.com/batch"
DAILY_QUOTA = 200


def get_sitemap_urls() -> list[str]:
    """Fetch all article URLs from the WordPress sitemap index."""
    urls = []
    try:
        # Get sitemap index
        resp = requests.get(f"{SITE_DOMAIN}/wp-sitemap.xml", timeout=30)
        resp.raise_for_status()
        root = ET.fromstring(resp.content)
        ns = {"sm": "http://www.sitemaps.org/schemas/sitemap/0.9"}

        sitemap_locs = [loc.text for loc in root.findall(".//sm:loc", ns)]
        print(f"Found {len(sitemap_locs)} sub-sitemaps")

        for sitemap_url in sitemap_locs:
            try:
                resp2 = requests.get(sitemap_url, timeout=30)
                resp2.raise_for_status()
                sub_root = ET.fromstring(resp2.content)
                for loc in sub_root.findall(".//sm:loc", ns):
                    if loc.text:
                        urls.append(loc.text)
            except Exception as e:
                print(f"  Error fetching {sitemap_url}: {e}")

    except Exception as e:
        print(f"Error fetching sitemap index: {e}")

    return urls


def create_batch_body(urls: list[str], boundary: str = "batch_boundary") -> str:
    """Create multipart batch request body for Indexing API."""
    parts = []
    for i, url in enumerate(urls):
        part = (
            f"--{boundary}\r\n"
            f"Content-Type: application/http\r\n"
            f"Content-ID: <item{i}>\r\n"
            f"\r\n"
            f"POST /v3/urlNotifications:publish HTTP/1.1\r\n"
            f"Content-Type: application/json\r\n"
            f"\r\n"
            f'{{"url": "{url}", "type": "URL_UPDATED"}}\r\n'
        )
        parts.append(part)
    parts.append(f"--{boundary}--\r\n")
    return "".join(parts)


def submit_batch(session: AuthorizedSession, urls: list[str]) -> tuple[int, int]:
    """Submit a batch of URLs. Returns (success_count, error_count)."""
    boundary = "batch_indexing"
    body = create_batch_body(urls, boundary)
    headers = {
        "Content-Type": f"multipart/mixed; boundary={boundary}",
    }
    resp = session.post(BATCH_URL, data=body, headers=headers)

    success = 0
    errors = 0
    if resp.status_code == 200:
        # Parse batch response to find successes and failures
        parts = resp.text.split("--batch")
        for part in parts:
            if "HTTP/1.1 200" in part:
                success += 1
            elif "HTTP/1.1 4" in part or "HTTP/1.1 5" in part:
                errors += 1
                # Extract which URL failed
                for line in part.split("\n"):
                    if '"error"' in line or "HTTP/1.1 4" in line or "HTTP/1.1 5" in line:
                        print(f"    Error detail: {line.strip()[:200]}")
                        break
    else:
        print(f"  Batch request failed: {resp.status_code} {resp.text[:500]}")
        errors = len(urls)

    return success, errors


def submit_individual(session: AuthorizedSession, urls: list[str]) -> tuple[int, int]:
    """Submit URLs one by one as fallback. Returns (success, errors)."""
    success = 0
    errors = 0
    for i, url in enumerate(urls):
        payload = {"url": url, "type": "URL_UPDATED"}
        try:
            resp = session.post(INDEXING_API_URL, json=payload)
            if resp.status_code == 200:
                success += 1
                if (i + 1) % 10 == 0:
                    print(f"  Submitted {i + 1}/{len(urls)}...")
            elif resp.status_code == 429:
                print(f"  Rate limited at {i + 1}/{len(urls)}. Waiting 60s...")
                time.sleep(60)
                resp = session.post(INDEXING_API_URL, json=payload)
                if resp.status_code == 200:
                    success += 1
                else:
                    errors += 1
                    print(f"  Still failed after retry: {resp.status_code}")
            else:
                errors += 1
                if errors <= 3:
                    print(f"  Error for {url}: {resp.status_code} {resp.text[:200]}")
        except Exception as e:
            errors += 1
            print(f"  Exception for {url}: {e}")

        # Small delay to avoid rate limiting
        if (i + 1) % 50 == 0:
            print(f"  Pausing 5s after {i + 1} requests...")
            time.sleep(5)
        else:
            time.sleep(0.5)

    return success, errors


def main():
    # 1. Get URLs
    print("Fetching URLs from sitemap...")
    urls = get_sitemap_urls()
    print(f"Found {len(urls)} URLs from sitemap")

    if not urls:
        print("No URLs found. Exiting.")
        return

    # Cap at daily quota
    if len(urls) > DAILY_QUOTA:
        print(f"Capping at {DAILY_QUOTA} URLs (daily quota)")
        urls = urls[:DAILY_QUOTA]

    # 2. Authenticate
    print("Authenticating with Google Indexing API...")
    credentials = service_account.Credentials.from_service_account_file(
        str(CREDENTIALS_PATH), scopes=SCOPES
    )
    session = AuthorizedSession(credentials)

    # 3. Try batch first (up to 100 per batch request)
    print(f"\nSubmitting {len(urls)} URLs...")

    total_success = 0
    total_errors = 0

    # Try batch in chunks of 100
    batch_size = 100
    use_batch = True

    for start in range(0, len(urls), batch_size):
        chunk = urls[start:start + batch_size]
        print(f"\nBatch {start // batch_size + 1}: {len(chunk)} URLs...")

        if use_batch:
            s, e = submit_batch(session, chunk)
            if s == 0 and e == len(chunk):
                print("  Batch endpoint failed. Falling back to individual requests...")
                use_batch = False
                s, e = submit_individual(session, chunk)
        else:
            s, e = submit_individual(session, chunk)

        total_success += s
        total_errors += e
        print(f"  Chunk result: {s} success, {e} errors")

        if start + batch_size < len(urls):
            print("  Pausing 2s between batches...")
            time.sleep(2)

    # 4. Report
    print(f"\n{'='*50}")
    print(f"RESULTS:")
    print(f"  Total URLs: {len(urls)}")
    print(f"  Submitted successfully: {total_success}")
    print(f"  Errors: {total_errors}")
    print(f"{'='*50}")


if __name__ == "__main__":
    main()
