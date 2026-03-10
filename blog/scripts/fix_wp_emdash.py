"""Find and fix all —— in WordPress posts/pages, replacing with ："""
import requests, json, base64, re, sys
sys.stdout.reconfigure(encoding='utf-8')

creds = json.load(open('config/wp-credentials.json', encoding='utf-8'))
auth = base64.b64encode(f"{creds['username']}:{creds['app_password']}".encode()).decode()
headers = {'Authorization': f'Basic {auth}', 'Content-Type': 'application/json'}

def get_all(endpoint):
    items = []
    page = 1
    while True:
        r = requests.get(f"{creds['api_base']}/{endpoint}", headers=headers,
                         params={'per_page': 100, 'page': page, 'status': 'publish,draft,private'})
        if r.status_code != 200 or not r.json():
            break
        items.extend(r.json())
        page += 1
    return items

all_posts = get_all('posts')
all_pages = get_all('pages')
print(f'Posts: {len(all_posts)}, Pages: {len(all_pages)}')

def fix_emdash(endpoint, item):
    r2 = requests.get(f"{creds['api_base']}/{endpoint}/{item['id']}", headers=headers,
                      params={'context': 'edit'})
    if r2.status_code != 200:
        return False
    raw = r2.json()['content']['raw']
    count = raw.count('——')
    if count == 0:
        return False

    # Show what we're changing
    for m in re.finditer(r'.{0,30}——.{0,30}', raw):
        print(f"  {m.group()}")

    new_raw = raw.replace('——', '：')
    r3 = requests.post(f"{creds['api_base']}/{endpoint}/{item['id']}", headers=headers,
                       json={'content': new_raw})
    if r3.status_code == 200:
        print(f"  -> FIXED {count} instances")
        return True
    else:
        print(f"  -> ERROR {r3.status_code}")
        return False

total_fixed = 0
for post in all_posts:
    r2 = requests.get(f"{creds['api_base']}/posts/{post['id']}", headers=headers,
                      params={'context': 'edit'})
    if r2.status_code != 200:
        continue
    raw = r2.json()['content']['raw']
    count = raw.count('——')
    if count > 0:
        title = post['title']['rendered']
        print(f"\nPOST ID:{post['id']} ({title}) - {count} instances:")
        if fix_emdash('posts', post):
            total_fixed += 1

for pg in all_pages:
    r2 = requests.get(f"{creds['api_base']}/pages/{pg['id']}", headers=headers,
                      params={'context': 'edit'})
    if r2.status_code != 200:
        continue
    raw = r2.json()['content']['raw']
    count = raw.count('——')
    if count > 0:
        title = pg['title']['rendered']
        print(f"\nPAGE ID:{pg['id']} ({title}) - {count} instances:")
        if fix_emdash('pages', pg):
            total_fixed += 1

print(f'\n=== Total items fixed: {total_fixed} ===')
