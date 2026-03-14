"""otona-match.com WordPress setup script"""
import urllib.request
import urllib.error
import json
import base64
import ssl
import time

BASE = "https://otona-match.com/?rest_route="
AUTH = base64.b64encode(b"t.mizuno27@gmail.com:Yw4j OgFf wwzT o0mn wXQ9 TjYs").decode()
ctx = ssl.create_default_context()

def wp_post(endpoint, data):
    body = json.dumps(data).encode('utf-8')
    req = urllib.request.Request(BASE + endpoint, data=body, method='POST')
    req.add_header('Content-Type', 'application/json; charset=utf-8')
    req.add_header('Authorization', f'Basic {AUTH}')
    try:
        with urllib.request.urlopen(req, context=ctx, timeout=30) as resp:
            return json.loads(resp.read())
    except urllib.error.HTTPError as e:
        err = e.read().decode()
        print(f"Error {e.code}: {err[:300]}")
        return None
    except Exception as e:
        print(f"Exception: {e}")
        return None

def wp_get(endpoint):
    req = urllib.request.Request(BASE + endpoint)
    req.add_header('Authorization', f'Basic {AUTH}')
    try:
        with urllib.request.urlopen(req, context=ctx, timeout=30) as resp:
            return json.loads(resp.read())
    except Exception as e:
        print(f"GET Error: {e}")
        return None

# Step 1: Create categories
print("=== Creating Categories ===")
categories = [
    {"name": "マッチングアプリ", "slug": "matching-apps"},
    {"name": "出会い系サイト", "slug": "deaikei"},
    {"name": "婚活", "slug": "konkatsu"},
    {"name": "恋愛テクニック", "slug": "renai-technique"},
    {"name": "安全・トラブル対策", "slug": "safety"},
    {"name": "体験談・口コミ", "slug": "reviews"},
]

cat_ids = {}
for c in categories:
    result = wp_post("/wp/v2/categories", c)
    if result and "id" in result:
        cat_ids[c["slug"]] = result["id"]
        print(f"  Created: {c['name']} (ID:{result['id']})")
    else:
        print(f"  Failed: {c['name']}")
    time.sleep(0.5)

print(f"\nCategory IDs: {cat_ids}")

# Save for later
with open('c:/Users/tmizu/otona_cat_ids.json', 'w', encoding='utf-8') as f:
    json.dump(cat_ids, f, ensure_ascii=False)

print("\nDone! Category IDs saved.")
