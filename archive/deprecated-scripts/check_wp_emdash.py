"""Check and fix all —— (em dash pairs) in WordPress posts, replacing with ："""
import requests, json, base64, re

creds = json.load(open('config/wp-credentials.json', encoding='utf-8'))
auth = base64.b64encode(f"{creds['username']}:{creds['app_password']}".encode()).decode()
headers = {'Authorization': f'Basic {auth}', 'Content-Type': 'application/json'}

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

# Also get pages
all_pages = []
page = 1
while True:
    r = requests.get(f"{creds['api_base']}/pages", headers=headers,
                     params={'per_page': 100, 'page': page, 'status': 'publish,draft,private'})
    if r.status_code != 200 or not r.json():
        break
    all_pages.extend(r.json())
    page += 1

print(f'Total posts: {len(all_posts)}, pages: {len(all_pages)}')

# Check posts
for post in all_posts:
    r2 = requests.get(f"{creds['api_base']}/posts/{post['id']}", headers=headers,
                      params={'context': 'edit'})
    if r2.status_code != 200:
        continue
    raw = r2.json()['content']['raw']
    # Match both —— and single — used as separator (but not in HTML comments or ---)
    matches = re.findall(r'——', raw)
    if matches:
        print(f"POST ID:{post['id']} | {post['title']['rendered'][:50]} | {len(matches)} instances")
        # Show context for each match
        for m in re.finditer(r'.{0,20}——.{0,20}', raw):
            print(f"  ...{m.group()}...")

# Check pages too
for pg in all_pages:
    r2 = requests.get(f"{creds['api_base']}/pages/{pg['id']}", headers=headers,
                      params={'context': 'edit'})
    if r2.status_code != 200:
        continue
    raw = r2.json()['content']['raw']
    matches = re.findall(r'——', raw)
    if matches:
        print(f"PAGE ID:{pg['id']} | {pg['title']['rendered'][:50]} | {len(matches)} instances")
        for m in re.finditer(r'.{0,20}——.{0,20}', raw):
            print(f"  ...{m.group()}...")
