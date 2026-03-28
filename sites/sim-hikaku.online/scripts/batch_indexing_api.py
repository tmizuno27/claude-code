"""
Batch submit URLs to Google Indexing API for sim-hikaku.online.
Fetches all URLs from wp-sitemap.xml, skips already-submitted URLs,
then submits remaining URLs up to the daily quota (200).
Tracks submitted URLs in a JSON log file for resumption across days.
"""

import json
import time
import xml.etree.ElementTree as ET
from datetime import datetime, timezone
from pathlib import Path

import requests
from google.oauth2 import service_account
from google.auth.transport.requests import AuthorizedSession

# Config
SITE_DOMAIN = "https://sim-hikaku.online"
SCRIPT_DIR = Path(__file__).parent.parent / "outputs"
SENT_LOG_PATH = SCRIPT_DIR / "indexing-sent-log.json"
CREDENTIALS_PATH = Path(
    r"C:\Users\tmizu\マイドライブ\GitHub\claude-code"
    r"\sites\nambei-oyaji.com\config\gsc-credentials.json"
)
SCOPES = ["https://www.googleapis.com/auth/indexing"]
INDEXING_API_URL = "https://indexing.googleapis.com/v3/urlNotifications:publish"
BATCH_URL = "https://indexing.googleapis.com/batch"
DAILY_QUOTA = 200


def load_sent_urls() -> dict[str, str]:
    """Load previously sent URLs with their submission timestamps."""
    if SENT_LOG_PATH.exists():
        data = json.loads(SENT_LOG_PATH.read_text(encoding="utf-8"))
        return data.get("sent", {})
    return {}


def save_sent_urls(sent: dict[str, str]) -> None:
    """Save sent URLs log."""
    data = {
        "updated_at": datetime.now(timezone.utc).isoformat(),
        "count": len(sent),
        "sent": sent,
    }
    SENT_LOG_PATH.write_text(
        json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8"
    )


def get_sitemap_urls() -> list[str]:
    """Fetch all article URLs from the WordPress sitemap index."""
    urls: list[str] = []
    resp = requests.get(f"{SITE_DOMAIN}/wp-sitemap.xml", timeout=30)
    resp.raise_for_status()
    root = ET.fromstring(resp.content)
    ns = {"sm": "http://www.sitemaps.org/schemas/sitemap/0.9"}

    sitemap_locs = [loc.text for loc in root.findall(".//sm:loc", ns)]
    print(f"Found {len(sitemap_locs)} sub-sitemaps")

    for sitemap_url in sitemap_locs:
        resp2 = requests.get(sitemap_url, timeout=30)
        resp2.raise_for_status()
        sub_root = ET.fromstring(resp2.content)
        for loc in sub_root.findall(".//sm:loc", ns):
            if loc.text:
                urls.append(loc.text)

    return urls


def create_batch_body(urls: list[str], boundary: str) -> str:
    """Create multipart batch request body for Indexing API."""
    parts = []
    for i, url in enumerate(urls):
        parts.append(
            f"--{boundary}\r\n"
            f"Content-Type: application/http\r\n"
            f"Content-ID: <item{i}>\r\n"
            f"\r\n"
            f"POST /v3/urlNotifications:publish HTTP/1.1\r\n"
            f"Content-Type: application/json\r\n"
            f"\r\n"
            f'{{"url": "{url}", "type": "URL_UPDATED"}}\r\n'
        )
    parts.append(f"--{boundary}--\r\n")
    return "".join(parts)


def submit_individual(
    session: AuthorizedSession,
    urls: list[str],
    sent: dict[str, str],
) -> tuple[int, int]:
    """Submit URLs one by one. Updates sent dict in-place. Returns (ok, err)."""
    ok = 0
    err = 0
    now_str = datetime.now(timezone.utc).isoformat()

    for i, url in enumerate(urls):
        payload = {"url": url, "type": "URL_UPDATED"}
        resp = session.post(INDEXING_API_URL, json=payload)

        if resp.status_code == 200:
            ok += 1
            sent[url] = now_str
            if (i + 1) % 10 == 0:
                print(f"  Submitted {i + 1}/{len(urls)}...")
                save_sent_urls(sent)  # checkpoint
        elif resp.status_code == 429:
            print(f"  Rate limited at URL #{i + 1}. Daily quota likely exhausted.")
            print(f"  Saving progress ({ok} sent this run). Re-run tomorrow.")
            save_sent_urls(sent)
            return ok, len(urls) - i
        else:
            err += 1
            print(f"  Error {resp.status_code} for {url}: {resp.text[:150]}")

        time.sleep(0.5)

    save_sent_urls(sent)
    return ok, err


def main() -> None:
    # 1. Get all URLs from sitemap
    print("Fetching URLs from sitemap...")
    all_urls = get_sitemap_urls()
    print(f"Total URLs in sitemap: {len(all_urls)}")

    # 2. Load sent log and filter
    sent = load_sent_urls()
    pending = [u for u in all_urls if u not in sent]
    print(f"Already submitted: {len(sent)}")
    print(f"Pending: {len(pending)}")

    if not pending:
        print("All URLs already submitted! Nothing to do.")
        return

    # Cap at daily quota
    to_submit = pending[:DAILY_QUOTA]
    print(f"Will submit: {len(to_submit)} URLs (daily quota: {DAILY_QUOTA})")

    # 3. Authenticate
    print("Authenticating...")
    credentials = service_account.Credentials.from_service_account_file(
        str(CREDENTIALS_PATH), scopes=SCOPES
    )
    session = AuthorizedSession(credentials)

    # 4. Submit individually (more reliable than batch for quota tracking)
    print(f"\nSubmitting {len(to_submit)} URLs...")
    ok, err = submit_individual(session, to_submit, sent)

    # 5. Report
    print(f"\n{'=' * 50}")
    print(f"RESULTS:")
    print(f"  Submitted this run: {ok}")
    print(f"  Errors/remaining: {err}")
    print(f"  Total submitted (all time): {len(sent)}")
    print(f"  Still pending: {len(all_urls) - len(sent)}")
    print(f"  Log saved to: {SENT_LOG_PATH}")
    print(f"{'=' * 50}")


if __name__ == "__main__":
    main()
