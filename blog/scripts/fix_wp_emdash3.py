"""Debug: dump all post content to find the actual —— characters"""
import requests, json, base64, re, sys
sys.stdout.reconfigure(encoding='utf-8')

creds = json.load(open('config/wp-credentials.json', encoding='utf-8'))
auth = base64.b64encode(f"{creds['username']}:{creds['app_password']}".encode()).decode()
headers = {'Authorization': f'Basic {auth}', 'Content-Type': 'application/json'}

# Check post 1214 specifically (food culture article had 12 instances)
r = requests.get(f"{creds['api_base']}/posts/1214", headers=headers, params={'context': 'edit'})
raw = r.json()['content']['raw']
title = r.json()['title']['raw']
print(f"Post 1214: {title}")
print(f"Raw length: {len(raw)}")

# Search for any dash-like characters near Japanese text
# Em dash U+2014, En dash U+2013, Horizontal bar U+2015, Fullwidth dash U+FF0D
# Also check ― (U+2015) and ー (katakana prolonged sound U+30FC)
patterns_to_check = {
    'U+2014 (em dash)': '\u2014',
    'U+2014x2': '\u2014\u2014',
    'U+2015 (horiz bar)': '\u2015',
    'U+2015x2': '\u2015\u2015',
    'U+2013 (en dash)': '\u2013',
    'U+2013x2': '\u2013\u2013',
    'U+FF0D (fullwidth minus)': '\uff0d',
    'U+30FC (katakana dash)': '\u30fc',
    '-- (ascii)': '--',
    '--- (ascii)': '---',
    '—— (fullwidth)': '——',
}

for name, pat in patterns_to_check.items():
    count = raw.count(pat)
    if count > 0:
        print(f"  {name}: {count} instances")

# Also just search for any heading patterns with separators
for m in re.finditer(r'(#{1,6}\s+.{0,80})', raw):
    line = m.group()
    if any(c in line for c in ['\u2014', '\u2015', '\u2013', '—', '–', '--']):
        print(f"  Heading: {line}")

# Broader: find lines with common separator patterns
for line in raw.split('\n'):
    for sep in ['——', '\u2014\u2014', '\u2015\u2015', '\u2013\u2013', '--']:
        if sep in line:
            print(f"  Line with '{sep}': {line[:100]}")
            break
