import json
import requests
from google.oauth2 import service_account
from google.auth.transport.requests import Request
from datetime import datetime

SA_PATH = r"C:\Users\tmizu\マイドライブ\GitHub\claude-code\sites\nambei-oyaji.com\config\gsc-credentials.json"
LOG_PATH = r"C:\Users\tmizu\マイドライブ\GitHub\claude-code\logs\indexing-api-sim-2026-03-24.log"
WP_API = "https://sim-hikaku.online/wp-json/wp/v2/posts"
WP_USER = "t.mizuno27@gmail.com"
WP_PASS = "P4A1 P4eh Nk0z 29An hS6H 9OHq"
INDEXING_URL = "https://indexing.googleapis.com/v3/urlNotifications:publish"

# Auth
credentials = service_account.Credentials.from_service_account_file(
    SA_PATH, scopes=["https://www.googleapis.com/auth/indexing"]
)
credentials.refresh(Request())

# Get all published posts from WP
wp_resp = requests.get(WP_API, params={"per_page": 100, "status": "publish"},
                       auth=(WP_USER, WP_PASS))
wp_resp.raise_for_status()
posts = wp_resp.json()
urls = [p["link"] for p in posts]

print(f"Found {len(urls)} published posts")

# Send to Indexing API
results = []
for i, url in enumerate(urls):
    if i >= 200:
        print("Reached 200/day limit, stopping")
        break
    resp = requests.post(
        INDEXING_URL,
        headers={
            "Authorization": f"Bearer {credentials.token}",
            "Content-Type": "application/json",
        },
        json={"url": url, "type": "URL_UPDATED"},
    )
    status = resp.status_code
    body = resp.text
    line = f"[{datetime.now().isoformat()}] {status} {url} | {body}"
    results.append(line)
    print(f"{i+1}/{len(urls)} {status} {url}")

# Write log
with open(LOG_PATH, "w", encoding="utf-8") as f:
    f.write(f"Indexing API v3 - sim-hikaku.online - {datetime.now().isoformat()}\n")
    f.write(f"Total URLs: {len(urls)}, Sent: {min(len(urls), 200)}\n\n")
    for line in results:
        f.write(line + "\n")

print(f"\nDone. Log saved to {LOG_PATH}")
