import json, requests

def post_to_wp(site_url, username, password, title, content, categories, slug, status="draft"):
    api_url = f"{site_url}/?rest_route=/wp/v2/posts"
    data = {"title": title, "content": content, "status": status, "categories": categories, "slug": slug}
    resp = requests.post(api_url, json=data, auth=(username, password), timeout=60)
    if resp.status_code in (200, 201):
        r = resp.json()
        return r.get("id"), r.get("link")
    else:
        print(f"ERROR {resp.status_code}: {resp.text[:300]}")
        return None, None

articles = json.load(open("articles_data.json", "r", encoding="utf-8"))
results = []
for art in articles:
    print(f"Posting: {art['title'][:50]}...")
    wp_id, wp_url = post_to_wp(art["site_url"], art["username"], art["password"],
                                art["title"], art["content"], art["categories"], art["slug"])
    print(f"  ID={wp_id}")
    results.append({"site": art["site"], "title": art["title"], "wp_id": wp_id, "wp_url": wp_url})

print("\n=== RESULTS ===")
for r in results:
    print(f"  {r['site']}: ID={r['wp_id']} | {r['title'][:60]}")
