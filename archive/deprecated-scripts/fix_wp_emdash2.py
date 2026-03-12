"""Find and fix all —— variants in WordPress posts/pages"""
import requests, json, base64, re, sys, html
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
print(f'Posts: {len(all_posts)}')

# First, let's see what the actual characters are in the rendered content
for post in all_posts:
    rendered = post['content']['rendered']
    # Check for various em-dash patterns: ——, --, &#8212;, etc.
    # Unicode em dash is U+2014
    emdash_double = '\u2014\u2014'
    if emdash_double in rendered:
        title = html.unescape(post['title']['rendered'])
        count = rendered.count(emdash_double)
        print(f"\nPOST ID:{post['id']} ({title}) - {count} in rendered")

        # Get raw content
        r2 = requests.get(f"{creds['api_base']}/posts/{post['id']}", headers=headers,
                          params={'context': 'edit'})
        if r2.status_code == 200:
            raw = r2.json()['content']['raw']
            # Check what form the dashes are in raw
            raw_count = raw.count(emdash_double)
            print(f"  Raw has {raw_count} instances of \\u2014\\u2014")

            # Also check for HTML entity versions
            for variant in ['——', '--', '&#8212;&#8212;', '&mdash;&mdash;']:
                vc = raw.count(variant)
                if vc:
                    print(f"  Raw has {vc} instances of '{variant}'")

            # Show first 5 contexts from raw
            for i, m in enumerate(re.finditer(r'.{0,30}[\u2014—]{2,}.{0,30}', raw)):
                if i >= 5: break
                print(f"  Context: {m.group()}")

            # Do the replacement in raw
            new_raw = raw.replace(emdash_double, '：')
            new_raw = new_raw.replace('——', '：')  # fullwidth

            if new_raw != raw:
                r3 = requests.post(f"{creds['api_base']}/posts/{post['id']}", headers=headers,
                                   json={'content': new_raw})
                if r3.status_code == 200:
                    print(f"  -> FIXED!")
                else:
                    print(f"  -> ERROR {r3.status_code}: {r3.text[:200]}")
            else:
                print(f"  -> No change in raw (rendered-only issue?)")
                # Try checking if it's in blocks
                for i, m in enumerate(re.finditer(r'.{0,40}', raw[:500])):
                    if i >= 3: break
                    print(f"  Raw start: {repr(raw[:200])}")
                    break
