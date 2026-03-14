"""Inject article CSS into all published articles."""
import requests, re, os

AUTH = ("t.mizuno27@gmail.com", "Yw4j OgFf wwzT o0mn wXQ9 TjYs")
BASE = "https://otona-match.com/?rest_route=/wp/v2"
DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Read minified article CSS
with open(os.path.join(DIR, "theme", "css", "article-inline.css"), "r", encoding="utf-8") as f:
    css = f.read().strip()

style_tag = f'<style>{css}</style>'
print(f"CSS style tag: {len(style_tag)} chars")

# Process articles 10-28 (skip 9 which is corrupted)
for post_id in range(10, 29):
    r = requests.get(f"{BASE}/posts/{post_id}", auth=AUTH)
    if r.status_code != 200:
        print(f"  ID:{post_id} - SKIP (status {r.status_code})")
        continue

    data = r.json()
    rendered = data.get("content", {}).get("rendered", "")
    title = data.get("title", {}).get("rendered", "")[:30]

    if not rendered or len(rendered) < 100:
        print(f"  ID:{post_id} - SKIP (empty/short content)")
        continue

    # Check if CSS is already injected
    if "font-smoothing:antialiased" in rendered:
        print(f"  ID:{post_id} - SKIP (CSS already present) {title}")
        continue

    # Prepend CSS to content
    new_content = style_tag + "\n" + rendered

    r2 = requests.post(
        f"{BASE}/posts/{post_id}",
        auth=AUTH,
        json={"content": new_content}
    )

    if r2.status_code == 200:
        print(f"  ID:{post_id} - OK {title}")
    else:
        print(f"  ID:{post_id} - FAIL ({r2.status_code}) {title}")
        if r2.status_code == 403:
            print(f"    WAF blocked. Trying without comments...")
            # Already no comments in minified CSS, must be another trigger
            print(f"    Content length: {len(new_content)}")

print("\nDone!")
