"""Check ALL posts rendered content for —— or similar dash separators used in headings/titles"""
import requests, json, base64, re, sys, html as htmlmod
sys.stdout.reconfigure(encoding='utf-8')

creds = json.load(open('config/wp-credentials.json', encoding='utf-8'))
auth = base64.b64encode(f"{creds['username']}:{creds['app_password']}".encode()).decode()
headers = {'Authorization': f'Basic {auth}', 'Content-Type': 'application/json'}

# Get all posts with rendered content
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

# Check rendered content for dash patterns
dash_chars = '\u2014\u2015\u2013'  # em dash, horiz bar, en dash
pattern = re.compile(f'[{dash_chars}]{{2,}}')

for post in all_posts:
    rendered = post['content']['rendered']
    title = htmlmod.unescape(post['title']['rendered'])
    matches = pattern.findall(rendered)
    if matches:
        print(f"\nID:{post['id']} ({title})")
        for m in pattern.finditer(rendered):
            start = max(0, m.start()-30)
            end = min(len(rendered), m.end()+30)
            ctx = rendered[start:end]
            # Strip HTML tags for readability
            ctx_clean = re.sub(r'<[^>]+>', '', ctx)
            print(f"  {ctx_clean}")

# Also check the actual website by fetching the page
print("\n\n=== Checking via website fetch ===")
for post in all_posts:
    link = post['link']
    title = htmlmod.unescape(post['title']['rendered'])
    try:
        r = requests.get(link, timeout=15)
        content = r.text
        # Look for —— in the page HTML
        for variant in ['——', '\u2014\u2014', '&#8212;&#8212;']:
            if variant in content:
                count = content.count(variant)
                print(f"\nID:{post['id']} ({title}) - {count} instances of {repr(variant)} on live site")
                for m in re.finditer(f'.{{0,40}}{re.escape(variant)}.{{0,40}}', content):
                    clean = re.sub(r'<[^>]+>', '', m.group())
                    if clean.strip():
                        print(f"  {clean.strip()}")
    except Exception as e:
        print(f"Error fetching {link}: {e}")
