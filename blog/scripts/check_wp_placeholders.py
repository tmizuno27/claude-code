"""Check all WordPress posts for placeholder text like 【写真:...】【要追記】【要確認】"""
import requests, json, base64, re

creds = json.load(open('config/wp-credentials.json', encoding='utf-8'))
auth = base64.b64encode(f"{creds['username']}:{creds['app_password']}".encode()).decode()
headers = {'Authorization': f'Basic {auth}'}

# Get all posts
all_posts = []
page = 1
while True:
    r = requests.get(f"{creds['api_base']}/posts", headers=headers,
                     params={'per_page': 100, 'page': page, 'status': 'publish,draft,private'})
    if r.status_code != 200 or not r.json():
        break
    all_posts.extend(r.json())
    page += 1

print(f'Total posts: {len(all_posts)}')

# Search for placeholder patterns
patterns = [
    r'【写真[^】]*】',
    r'【要追記[^】]*】',
    r'【要確認[^】]*】',
]
found_posts = {}
for post in all_posts:
    content = post['content']['rendered']
    matches = []
    for pat in patterns:
        matches.extend(re.findall(pat, content))
    if matches:
        found_posts[post['id']] = {
            'title': post['title']['rendered'],
            'matches': matches
        }
        for m in matches:
            print(f"ID:{post['id']} | {post['title']['rendered'][:50]} | {m[:100]}")

print(f'\nTotal posts with placeholders: {len(found_posts)}')
print(f'Total placeholder instances: {sum(len(v["matches"]) for v in found_posts.values())}')

# Save results for cleanup script
json.dump(found_posts, open('outputs/wp-placeholders-found.json', 'w', encoding='utf-8'),
          ensure_ascii=False, indent=2)
