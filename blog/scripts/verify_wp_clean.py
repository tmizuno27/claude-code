"""Final verification: check all WP posts for any remaining dash separators or placeholders"""
import requests, json, base64, re, sys
sys.stdout.reconfigure(encoding='utf-8')

creds = json.load(open('config/wp-credentials.json', encoding='utf-8'))
auth = base64.b64encode(f"{creds['username']}:{creds['app_password']}".encode()).decode()
headers = {'Authorization': f'Basic {auth}'}

all_posts = []
page = 1
while True:
    r = requests.get(f"{creds['api_base']}/posts", headers=headers,
                     params={'per_page': 100, 'page': page, 'status': 'publish,draft,private'})
    if r.status_code != 200 or not r.json():
        break
    all_posts.extend(r.json())
    page += 1

issues = 0
for post in all_posts:
    rendered = post['content']['rendered']
    # Check all dash variants
    dash_pattern = re.compile(r'[\u2014\u2015\u2013]{2,}')
    placeholder_pattern = re.compile(r'【[^】]*】')

    for pat, name in [(dash_pattern, 'double-dash'), (placeholder_pattern, 'placeholder')]:
        for m in pat.finditer(rendered):
            ctx = rendered[max(0,m.start()-20):m.end()+20]
            ctx_clean = re.sub(r'<[^>]+>', '', ctx)
            print(f"ID:{post['id']} [{name}]: ...{ctx_clean}...")
            issues += 1

print(f"\nTotal remaining issues: {issues}")
