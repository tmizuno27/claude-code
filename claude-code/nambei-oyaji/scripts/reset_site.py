#!/usr/bin/env python3
"""Reset WordPress site to initial state: delete all CSS blocks and clear pages."""

import requests
import time
from base64 import b64encode

URL = 'https://nambei-oyaji.com/wp-json/wp/v2'
CREDS = b64encode('t.mizuno27@gmail.com:agNg 2624 4lL4 QoT9 EOOZ OEZr'.encode()).decode()
HEADERS = {'Authorization': f'Basic {CREDS}', 'Content-Type': 'application/json'}


def main():
    print('=== WordPress Site Reset ===\n')

    # 1. Get all blocks
    print('[1/3] Fetching all blocks...')
    all_block_ids = []
    page = 1
    while True:
        r = requests.get(f'{URL}/blocks', headers=HEADERS,
                         params={'per_page': 100, 'page': page}, timeout=15)
        if r.status_code != 200:
            break
        blocks = r.json()
        if not blocks:
            break
        for b in blocks:
            all_block_ids.append(b['id'])
        page += 1
    print(f'  Found {len(all_block_ids)} published blocks')

    # 2. Delete all blocks
    print('\n[2/3] Deleting all blocks...')
    deleted = 0
    for bid in all_block_ids:
        try:
            r = requests.delete(f'{URL}/blocks/{bid}?force=true',
                                headers=HEADERS, timeout=10)
            if r.status_code == 200:
                deleted += 1
                if deleted % 10 == 0:
                    print(f'  Deleted {deleted}...')
            time.sleep(0.15)
        except Exception:
            pass
    print(f'  Deleted {deleted}/{len(all_block_ids)} blocks')

    # 3. Reset all pages
    print('\n[3/3] Resetting pages to empty...')
    pages = {47: 'home', 48: 'about', 49: 'contact', 50: 'privacy-policy', 51: 'sitemap'}
    for pid, slug in pages.items():
        content = f'<!-- wp:paragraph --><p>{slug} - under construction</p><!-- /wp:paragraph -->'
        r = requests.post(f'{URL}/pages/{pid}', headers=HEADERS,
                          json={'content': content}, timeout=15)
        status = 'OK' if r.status_code == 200 else f'FAILED {r.status_code}'
        print(f'  {slug} (ID={pid}): {status}')
        time.sleep(0.3)

    print('\n=== Reset complete! ===')
    print('Site is now in initial state: https://nambei-oyaji.com/')


if __name__ == '__main__':
    main()
