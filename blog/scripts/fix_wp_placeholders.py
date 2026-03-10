"""Remove all placeholder text from WordPress posts."""
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

print(f'Total posts: {len(all_posts)}')

# Patterns to remove
patterns = [
    # Full paragraph/line containing only a photo placeholder
    r'<p>\s*【写真[^】]*】\s*</p>',
    r'<p>\s*【要追記[^】]*】\s*</p>',
    r'<p>\s*【要確認[^】]*】\s*</p>',
    # Inline placeholders (within other content)
    r'【写真[^】]*】',
    r'【要追記[^】]*】',
    r'【要確認[^】]*】',
]

fixed = 0
for post in all_posts:
    content_raw = post['content']['rendered']
    new_content = content_raw

    for pat in patterns:
        new_content = re.sub(pat, '', new_content)

    # Clean up empty paragraphs left behind
    new_content = re.sub(r'<p>\s*</p>', '', new_content)

    if new_content != content_raw:
        # Count removals
        removals = len(re.findall(r'【[^】]*】', content_raw)) - len(re.findall(r'【[^】]*】', new_content))

        # Update post - use raw content from API
        r2 = requests.get(f"{creds['api_base']}/posts/{post['id']}", headers=headers,
                          params={'context': 'edit'})
        if r2.status_code == 200:
            raw_content = r2.json()['content']['raw']
            new_raw = raw_content
            for pat in patterns:
                new_raw = re.sub(pat, '', new_raw)
            # Clean up empty lines
            new_raw = re.sub(r'\n\s*\n\s*\n', '\n\n', new_raw)

            r3 = requests.post(f"{creds['api_base']}/posts/{post['id']}", headers=headers,
                               json={'content': new_raw})
            if r3.status_code == 200:
                print(f"FIXED ID:{post['id']} - removed {removals} placeholders")
                fixed += 1
            else:
                print(f"ERROR ID:{post['id']} - {r3.status_code}: {r3.text[:200]}")

print(f'\nFixed {fixed} posts')
