#!/usr/bin/env python3
"""Replace CSS blocks with South America design and update all pages.

Splits CSS at /* @mobile */ marker so mobile rules are wrapped
per-chunk in @media(max-width:768px){...}, preventing broken
@media blocks when CSS is split across multiple <style> tags.
"""

import re
import requests
import time
from base64 import b64encode
from pathlib import Path

URL = 'https://nambei-oyaji.com/wp-json/wp/v2'
CREDS = b64encode('t.mizuno27@gmail.com:agNg 2624 4lL4 QoT9 EOOZ OEZr'.encode()).decode()
HEADERS = {'Authorization': f'Basic {CREDS}', 'Content-Type': 'application/json'}

CSS_FILE = Path(__file__).parent.parent / 'design' / 'nao-global.css'

OLD_BLOCK_IDS = [896, 897, 898, 899, 900, 901, 902, 903, 904, 905, 906, 907, 908, 909, 910, 911, 912, 913, 914, 915, 916, 917, 918, 924, 925]


def minify_css(raw):
    css = re.sub(r'/\*.*?\*/', '', raw, flags=re.DOTALL)
    css = re.sub(r'\s+', ' ', css)
    for ch in '{}:;,':
        css = re.sub(rf'\s*\{re.escape(ch)}\s*', ch, css)
    return css.strip()


def chunk_css(css, max_len=1500):
    rules = re.split(r'(})', css)
    chunks, temp = [], ''
    for i in range(0, len(rules) - 1, 2):
        rule = rules[i] + (rules[i + 1] if i + 1 < len(rules) else '')
        if len(temp) + len(rule) > max_len and temp:
            chunks.append(temp)
            temp = rule
        else:
            temp += rule
    if temp.strip():
        chunks.append(temp)
    return chunks


def create_block(title, css_chunk, mobile=False):
    if mobile:
        inner = f'@media(max-width:768px){{{css_chunk}}}'
    else:
        inner = css_chunk
    content = f'<!-- wp:html --><style>{inner}</style><!-- /wp:html -->'
    r = requests.post(f'{URL}/blocks', headers=HEADERS, json={
        'title': title, 'content': content, 'status': 'publish'
    }, timeout=15)
    if r.status_code == 201:
        return r.json()['id']
    # WAF blocked - split further
    mid = len(css_chunk) // 2
    sp = css_chunk.find('}', mid) + 1
    ids = []
    for label, part in [('a', css_chunk[:sp]), ('b', css_chunk[sp:])]:
        if not part.strip():
            continue
        if mobile:
            inner2 = f'@media(max-width:768px){{{part}}}'
        else:
            inner2 = part
        c = f'<!-- wp:html --><style>{inner2}</style><!-- /wp:html -->'
        r2 = requests.post(f'{URL}/blocks', headers=HEADERS, json={
            'title': f'{title}-{label}', 'content': c, 'status': 'publish'
        }, timeout=15)
        if r2.status_code == 201:
            ids.append(r2.json()['id'])
        else:
            print(f'    FAIL: {title}-{label} ({r2.status_code})')
    return ids if ids else None


def main():
    print('=== South America Design Update ===\n')

    # 1. Delete old CSS blocks
    print('[1/3] Deleting old CSS blocks...')
    for bid in OLD_BLOCK_IDS:
        requests.post(f'{URL}/blocks/{bid}', headers=HEADERS,
                      json={'status': 'trash'}, timeout=10)
    print(f'  Trashed {len(OLD_BLOCK_IDS)} old blocks')

    # 2. Read and split CSS at /* @mobile */ marker
    print('\n[2/3] Creating new CSS blocks...')
    raw_css = CSS_FILE.read_text(encoding='utf-8')

    parts = raw_css.split('/* @mobile */')
    desktop_raw = parts[0]
    mobile_raw = parts[1] if len(parts) > 1 else ''

    # Desktop CSS
    desktop_mini = minify_css(desktop_raw)
    print(f'  Desktop CSS: {len(desktop_mini)} chars')
    desktop_chunks = chunk_css(desktop_mini)
    print(f'  Desktop chunks: {len(desktop_chunks)}')

    # Mobile CSS (rules without @media wrapper - we add it per chunk)
    mobile_mini = minify_css(mobile_raw)
    print(f'  Mobile CSS: {len(mobile_mini)} chars')
    mobile_chunks = chunk_css(mobile_mini, max_len=1300)  # smaller to fit @media wrapper
    print(f'  Mobile chunks: {len(mobile_chunks)}')

    new_ids = []

    # Create desktop blocks
    for i, chunk in enumerate(desktop_chunks):
        result = create_block(f'NAO v8 Desktop {i + 1}', chunk, mobile=False)
        if isinstance(result, list):
            new_ids.extend(result)
            print(f'  Desktop {i + 1}: split into {len(result)} sub-blocks')
        elif result:
            new_ids.append(result)
            print(f'  Desktop {i + 1}: ID={result} ({len(chunk)} chars)')
        else:
            print(f'  Desktop {i + 1}: FAILED')
        time.sleep(0.3)

    # Create mobile blocks (each wrapped in @media)
    for i, chunk in enumerate(mobile_chunks):
        result = create_block(f'NAO v8 Mobile {i + 1}', chunk, mobile=True)
        if isinstance(result, list):
            new_ids.extend(result)
            print(f'  Mobile {i + 1}: split into {len(result)} sub-blocks')
        elif result:
            new_ids.append(result)
            print(f'  Mobile {i + 1}: ID={result} ({len(chunk)} chars)')
        else:
            print(f'  Mobile {i + 1}: FAILED')
        time.sleep(0.3)

    print(f'\n  New block IDs: {new_ids}')

    # Build block refs
    refs = ''.join([f'<!-- wp:block {{"ref":{bid}}} /-->\n' for bid in new_ids])

    # 3. Update all pages
    print('\n[3/3] Updating pages...')
    pages = {47: 'home', 48: 'about', 49: 'contact', 50: 'privacy-policy', 51: 'sitemap'}

    for pid, slug in pages.items():
        r = requests.get(f'{URL}/pages/{pid}', headers=HEADERS,
                        params={'context': 'edit'}, timeout=15)
        if r.status_code != 200:
            print(f'  {slug}: GET failed {r.status_code}')
            continue

        raw_content = r.json()['content']['raw']
        cleaned = re.sub(r'<!-- wp:block \{"ref":\d+\} /-->\s*', '', raw_content)
        new_content = refs + cleaned

        r2 = requests.post(f'{URL}/pages/{pid}', headers=HEADERS,
                           json={'content': new_content}, timeout=30)
        if r2.status_code == 200:
            print(f'  {slug}: updated OK')
        else:
            print(f'  {slug}: update FAILED {r2.status_code}')
        time.sleep(0.5)

    print('\n=== Done! Check https://nambei-oyaji.com/ ===')


if __name__ == '__main__':
    main()
