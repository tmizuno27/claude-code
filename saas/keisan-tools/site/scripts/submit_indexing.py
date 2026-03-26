"""
keisan-tools.com: Submit sitemap URLs to Google Indexing API v3.
Daily quota: 200 URLs/day. Site has ~460 URLs.
Resumes from pending file if previous run hit quota.
Usage: python scripts/submit_indexing.py
"""
import json
import xml.etree.ElementTree as ET
from datetime import datetime
from pathlib import Path

import google.auth.transport.requests
import requests
from google.oauth2 import service_account

SA_FILE = Path(
    "C:/Users/tmizu/マイドライブ/GitHub/claude-code"
    "/infrastructure/tools/sheets-sync/credentials/service-account.json"
)
SCRIPT_DIR = Path(__file__).resolve().parent
SITEMAP = SCRIPT_DIR.parent / "out" / "sitemap.xml"
PENDING_FILE = SCRIPT_DIR / "pending_urls.json"
ENDPOINT = "https://indexing.googleapis.com/v3/urlNotifications:publish"
SCOPES = ["https://www.googleapis.com/auth/indexing"]


def get_urls_from_sitemap(sitemap_path: Path) -> list[str]:
    tree = ET.parse(sitemap_path)
    root = tree.getroot()
    ns = {"s": "http://www.sitemaps.org/schemas/sitemap/0.9"}
    return [loc.text for loc in root.findall(".//s:loc", ns) if loc.text]


def load_pending() -> list[str]:
    if PENDING_FILE.exists():
        data = json.loads(PENDING_FILE.read_text(encoding="utf-8"))
        return data.get("urls", [])
    return []


def save_pending(urls: list[str]) -> None:
    payload = {"saved_at": datetime.now().isoformat(), "count": len(urls), "urls": urls}
    PENDING_FILE.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"  -> Saved {len(urls)} pending URLs to {PENDING_FILE.name}")


def clear_pending() -> None:
    if PENDING_FILE.exists():
        PENDING_FILE.unlink()


def main() -> None:
    creds = service_account.Credentials.from_service_account_file(
        str(SA_FILE), scopes=SCOPES
    )
    creds.refresh(google.auth.transport.requests.Request())

    headers = {
        "Authorization": f"Bearer {creds.token}",
        "Content-Type": "application/json",
    }

    # Resume from pending if exists, otherwise load full sitemap
    pending = load_pending()
    if pending:
        urls = pending
        print(f"Resuming: {len(urls)} pending URLs from previous run")
    else:
        urls = get_urls_from_sitemap(SITEMAP)
        print(f"Fresh run: {len(urls)} URLs from sitemap")

    success = 0
    errors = 0
    quota_hit = False
    for i, url in enumerate(urls):
        body = json.dumps({"url": url, "type": "URL_UPDATED"})
        resp = requests.post(ENDPOINT, headers=headers, data=body)
        if resp.status_code == 200:
            print(f"  [{i+1}/{len(urls)}] OK: {url}")
            success += 1
        else:
            try:
                err = resp.json().get("error", {})
                code = err.get("code", resp.status_code)
                msg = err.get("message", "")[:100]
            except Exception:
                code = resp.status_code
                msg = resp.text[:100]
            print(f"  [{i+1}/{len(urls)}] ERR {code}: {url} -> {msg}")
            errors += 1
            if code == 429:
                remaining = urls[i:]
                save_pending(remaining)
                quota_hit = True
                break

    if not quota_hit:
        clear_pending()

    print(f"\nResult: {success} success, {errors} errors, {len(urls)} total")
    if quota_hit:
        print(f"Quota hit. {len(urls) - i} URLs saved for next run.")


if __name__ == "__main__":
    main()
