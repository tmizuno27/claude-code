"""
keisan-tools.com: Submit all sitemap URLs to Google Indexing API v3.
Daily quota: 200 URLs/day. Current site has 33 URLs.
Usage: python scripts/submit_indexing.py
"""
import json
import xml.etree.ElementTree as ET
from pathlib import Path

import google.auth.transport.requests
import requests
from google.oauth2 import service_account

SA_FILE = Path(
    "C:/Users/tmizu/マイドライブ/GitHub/claude-code"
    "/infrastructure/tools/sheets-sync/credentials/service-account.json"
)
SITEMAP = Path(__file__).resolve().parent.parent / "public" / "sitemap.xml"
ENDPOINT = "https://indexing.googleapis.com/v3/urlNotifications:publish"
SCOPES = ["https://www.googleapis.com/auth/indexing"]


def get_urls_from_sitemap(sitemap_path: Path) -> list[str]:
    tree = ET.parse(sitemap_path)
    root = tree.getroot()
    ns = {"s": "http://www.sitemaps.org/schemas/sitemap/0.9"}
    return [loc.text for loc in root.findall(".//s:loc", ns) if loc.text]


def main() -> None:
    creds = service_account.Credentials.from_service_account_file(
        str(SA_FILE), scopes=SCOPES
    )
    creds.refresh(google.auth.transport.requests.Request())

    headers = {
        "Authorization": f"Bearer {creds.token}",
        "Content-Type": "application/json",
    }

    urls = get_urls_from_sitemap(SITEMAP)
    print(f"Submitting {len(urls)} URLs from {SITEMAP}")

    success = 0
    errors = 0
    for url in urls:
        body = json.dumps({"url": url, "type": "URL_UPDATED"})
        resp = requests.post(ENDPOINT, headers=headers, data=body)
        if resp.status_code == 200:
            print(f"  OK: {url}")
            success += 1
        else:
            code = resp.json().get("error", {}).get("code", resp.status_code)
            msg = resp.json().get("error", {}).get("message", "")[:100]
            print(f"  ERR {code}: {url} -> {msg}")
            errors += 1
            if code == 429:
                print("  -> Daily quota exhausted. Stopping.")
                break

    print(f"\nResult: {success}/{len(urls)} success, {errors} errors")


if __name__ == "__main__":
    main()
