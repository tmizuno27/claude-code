"""
pSEO AIツール比較サイト: Submit URLs to Google Indexing API v3.
Daily quota: 200 URLs/day.
Tracks progress in submit_state.json to resume across runs.

Usage:
  python scripts/submit_indexing.py              # Submit next 200 URLs
  python scripts/submit_indexing.py --stats      # Show submission stats
  python scripts/submit_indexing.py --reset      # Reset progress tracker
"""
import json
import sys
import xml.etree.ElementTree as ET
from datetime import date
from pathlib import Path

import google.auth.transport.requests
import requests
from google.oauth2 import service_account

SA_FILE = Path(
    "C:/Users/tmizu/マイドライブ/GitHub/claude-code"
    "/infrastructure/tools/sheets-sync/credentials/service-account.json"
)
SITEMAP = Path(__file__).resolve().parent.parent / "site" / "public" / "sitemap.xml"
STATE_FILE = Path(__file__).resolve().parent / "submit_state.json"
ENDPOINT = "https://indexing.googleapis.com/v3/urlNotifications:publish"
SCOPES = ["https://www.googleapis.com/auth/indexing"]
DAILY_LIMIT = 200


def get_urls_from_sitemap(sitemap_path: Path) -> list[str]:
    tree = ET.parse(sitemap_path)
    root = tree.getroot()
    ns = {"s": "http://www.sitemaps.org/schemas/sitemap/0.9"}
    return [loc.text for loc in root.findall(".//s:loc", ns) if loc.text]


def load_state() -> dict:
    if STATE_FILE.exists():
        return json.loads(STATE_FILE.read_text(encoding="utf-8"))
    return {"submitted": [], "last_index": 0, "last_date": ""}


def save_state(state: dict) -> None:
    STATE_FILE.write_text(json.dumps(state, indent=2), encoding="utf-8")


def main() -> None:
    if "--stats" in sys.argv:
        state = load_state()
        print(f"Submitted: {len(state['submitted'])} URLs")
        print(f"Last index: {state['last_index']}")
        print(f"Last date: {state['last_date']}")
        urls = get_urls_from_sitemap(SITEMAP)
        print(f"Total URLs in sitemap: {len(urls)}")
        print(f"Remaining: {len(urls) - state['last_index']}")
        return

    if "--reset" in sys.argv:
        save_state({"submitted": [], "last_index": 0, "last_date": ""})
        print("State reset.")
        return

    creds = service_account.Credentials.from_service_account_file(
        str(SA_FILE), scopes=SCOPES
    )
    creds.refresh(google.auth.transport.requests.Request())

    headers = {
        "Authorization": f"Bearer {creds.token}",
        "Content-Type": "application/json",
    }

    urls = get_urls_from_sitemap(SITEMAP)
    state = load_state()
    start = state["last_index"]
    batch = urls[start : start + DAILY_LIMIT]

    if not batch:
        print(f"All {len(urls)} URLs already submitted!")
        return

    print(f"Submitting URLs {start+1} to {start+len(batch)} of {len(urls)}")

    success = 0
    errors = 0
    for url in batch:
        body = json.dumps({"url": url, "type": "URL_UPDATED"})
        resp = requests.post(ENDPOINT, headers=headers, data=body)
        if resp.status_code == 200:
            success += 1
            state["submitted"].append(url)
        else:
            code = resp.json().get("error", {}).get("code", resp.status_code)
            msg = resp.json().get("error", {}).get("message", "")[:100]
            print(f"  ERR {code}: {url} -> {msg}")
            errors += 1
            if code == 429:
                print("  -> Daily quota exhausted. Stopping.")
                break

    state["last_index"] = start + success + errors
    state["last_date"] = str(date.today())
    save_state(state)

    print(f"\nResult: {success}/{len(batch)} success, {errors} errors")
    print(f"Progress: {state['last_index']}/{len(urls)} ({state['last_index']*100//len(urls)}%)")


if __name__ == "__main__":
    main()
