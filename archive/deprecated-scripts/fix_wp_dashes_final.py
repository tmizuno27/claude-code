"""Fix all double-dash separator patterns in WordPress posts, replacing with ："""
import requests, json, base64, re, sys, html as htmlmod
sys.stdout.reconfigure(encoding='utf-8')

creds = json.load(open('config/wp-credentials.json', encoding='utf-8'))
auth = base64.b64encode(f"{creds['username']}:{creds['app_password']}".encode()).decode()
headers = {'Authorization': f'Basic {auth}', 'Content-Type': 'application/json'}

all_posts = []
page = 1
while True:
    r = requests.get(f"{creds['api_base']}/posts", headers=headers,
                     params={'per_page': 100, 'page': page, 'status': 'publish,draft,private'})
    if r.status_code != 200 or not r.json():
        break
    all_posts.extend(r.json())
    page += 1

print(f'Posts: {len(all_posts)}')

# All possible double-dash variants
dash_variants = [
    '\u2014\u2014',  # em dash x2
    '\u2015\u2015',  # horizontal bar x2
    '\u2013\u2013',  # en dash x2
    '——',            # fullwidth em dash x2
    '――',            # another variant
]

total_fixed = 0
for post in all_posts:
    r2 = requests.get(f"{creds['api_base']}/posts/{post['id']}", headers=headers,
                      params={'context': 'edit'})
    if r2.status_code != 200:
        continue
    raw = r2.json()['content']['raw']
    title = htmlmod.unescape(post['title']['rendered'])

    new_raw = raw
    total_replacements = 0
    for variant in dash_variants:
        count = new_raw.count(variant)
        if count > 0:
            total_replacements += count
            new_raw = new_raw.replace(variant, '：')

    if total_replacements > 0:
        print(f"\nID:{post['id']} ({title}) - {total_replacements} replacements")
        # Show what changed
        for line_old, line_new in zip(raw.split('\n'), new_raw.split('\n')):
            if line_old != line_new:
                print(f"  OLD: {line_old[:120]}")
                print(f"  NEW: {line_new[:120]}")

        r3 = requests.post(f"{creds['api_base']}/posts/{post['id']}", headers=headers,
                           json={'content': new_raw})
        if r3.status_code == 200:
            print(f"  -> FIXED!")
            total_fixed += 1
        else:
            print(f"  -> ERROR {r3.status_code}")

print(f'\n=== Fixed {total_fixed} posts ===')
