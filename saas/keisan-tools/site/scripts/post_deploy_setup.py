"""
keisan-tools.com: Post-deploy setup script.
1. Submit sitemap to GSC (Search Console API: sitemaps.submit)
2. Submit all URLs from sitemap.xml to Google Indexing API v3

Run once after initial Vercel deploy.
Usage: python scripts/post_deploy_setup.py
"""
import json
import logging
import xml.etree.ElementTree as ET
from pathlib import Path

import google.auth.transport.requests
import requests
from google.oauth2 import service_account

SA_FILE = Path(
    "C:/Users/tmizu/マイドライブ/GitHub/claude-code"
    "/infrastructure/tools/sheets-sync/credentials/service-account.json"
)
SITEMAP_PATH = Path(__file__).resolve().parent.parent / "public" / "sitemap.xml"
SITE_URL = "https://keisan-tools.com"
SITEMAP_URL = f"{SITE_URL}/sitemap.xml"
INDEXING_ENDPOINT = "https://indexing.googleapis.com/v3/urlNotifications:publish"
SCOPES = [
    "https://www.googleapis.com/auth/indexing",
    "https://www.googleapis.com/auth/webmasters",
]

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
log = logging.getLogger(__name__)


def get_credentials() -> service_account.Credentials:
    creds = service_account.Credentials.from_service_account_file(
        str(SA_FILE), scopes=SCOPES
    )
    creds.refresh(google.auth.transport.requests.Request())
    return creds


def get_urls_from_sitemap(sitemap_path: Path) -> list[str]:
    tree = ET.parse(sitemap_path)
    root = tree.getroot()
    ns = {"s": "http://www.sitemaps.org/schemas/sitemap/0.9"}
    return [loc.text for loc in root.findall(".//s:loc", ns) if loc.text]


def submit_sitemap_to_gsc(creds: service_account.Credentials) -> bool:
    """Submit sitemap.xml to Google Search Console via Webmasters API."""
    log.info("=== GSC Sitemap Submit ===")
    encoded_site = SITE_URL.replace(":", "%3A").replace("/", "%2F")
    encoded_sitemap = SITEMAP_URL.replace(":", "%3A").replace("/", "%2F")
    url = (
        f"https://www.googleapis.com/webmasters/v3"
        f"/sites/{encoded_site}/sitemaps/{encoded_sitemap}"
    )
    headers = {
        "Authorization": f"Bearer {creds.token}",
        "Content-Type": "application/json",
    }
    resp = requests.put(url, headers=headers)
    if resp.status_code in (200, 204):
        log.info(f"Sitemap submitted OK: {SITEMAP_URL}")
        return True
    else:
        log.error(
            f"Sitemap submit failed ({resp.status_code}): "
            f"{resp.text[:200]}"
        )
        return False


def submit_urls_to_indexing(creds: service_account.Credentials) -> tuple[int, int]:
    """Submit all URLs from sitemap.xml to Google Indexing API v3."""
    log.info("=== Indexing API Submit ===")
    headers = {
        "Authorization": f"Bearer {creds.token}",
        "Content-Type": "application/json",
    }
    urls = get_urls_from_sitemap(SITEMAP_PATH)
    log.info(f"Found {len(urls)} URLs in {SITEMAP_PATH}")

    success = 0
    errors = 0
    for url in urls:
        body = json.dumps({"url": url, "type": "URL_UPDATED"})
        resp = requests.post(INDEXING_ENDPOINT, headers=headers, data=body)
        if resp.status_code == 200:
            log.info(f"  OK: {url}")
            success += 1
        else:
            err = resp.json().get("error", {})
            code = err.get("code", resp.status_code)
            msg = err.get("message", "")[:100]
            log.error(f"  ERR {code}: {url} -> {msg}")
            errors += 1
            if code == 429:
                log.warning("Daily quota exhausted. Stopping.")
                break

    return success, errors


def main() -> None:
    log.info("===== keisan-tools.com Post-Deploy Setup START =====")

    creds = get_credentials()

    sitemap_ok = submit_sitemap_to_gsc(creds)

    success, errors = submit_urls_to_indexing(creds)

    log.info("===== Summary =====")
    log.info(f"GSC Sitemap: {'OK' if sitemap_ok else 'FAILED'}")
    log.info(f"Indexing API: {success} success, {errors} errors")
    log.info("===== Post-Deploy Setup DONE =====")


if __name__ == "__main__":
    main()
