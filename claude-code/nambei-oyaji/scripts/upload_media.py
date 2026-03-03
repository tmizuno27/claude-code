#!/usr/bin/env python3
"""Upload site assets to WordPress media library."""

import requests
from base64 import b64encode
from pathlib import Path

URL = 'https://nambei-oyaji.com/wp-json/wp/v2'
CREDS = b64encode('t.mizuno27@gmail.com:agNg 2624 4lL4 QoT9 EOOZ OEZr'.encode()).decode()

ASSETS = Path(__file__).parent.parent / 'assets'

# Files to upload with descriptive names
FILES = {
    'logo-touka_white.png': 'logo-white',
    'logo-touka_black.png': 'logo-black',
    'nambei-oyaji_white.png': 'logotype-white',
    'nambei-oyaji_black.png': 'logotype-black',
    'profile.png': 'profile-avatar',
    'top.png': 'hero-banner',
    'Modify_this_family_illustration_Change_the_mother-1768155963782.png': 'family-illustration',
    'note.png': 'logo-grey-circle',
}


def upload(filename, slug):
    filepath = ASSETS / filename
    if not filepath.exists():
        print(f'  SKIP: {filename} not found')
        return None

    headers = {
        'Authorization': f'Basic {CREDS}',
        'Content-Disposition': f'attachment; filename="{slug}.png"',
        'Content-Type': 'image/png',
    }

    data = filepath.read_bytes()
    r = requests.post(f'{URL}/media', headers=headers, data=data, timeout=60)

    if r.status_code == 201:
        info = r.json()
        return {'id': info['id'], 'url': info['source_url'], 'slug': slug}
    else:
        print(f'  FAIL: {slug} -> {r.status_code}')
        # Try smaller chunk if WAF blocks
        if r.status_code == 403 and len(data) > 500000:
            print(f'    File too large ({len(data)} bytes), skipping')
        return None


def main():
    print('=== Uploading Media Assets ===\n')
    results = {}

    for filename, slug in FILES.items():
        result = upload(filename, slug)
        if result:
            results[slug] = result
            print(f'  {slug}: ID={result["id"]} -> {result["url"]}')
        else:
            print(f'  {slug}: failed')

    print(f'\n=== Uploaded {len(results)}/{len(FILES)} files ===')
    print('\nMedia URLs:')
    for slug, info in results.items():
        print(f'  {slug}: {info["url"]}')

    return results


if __name__ == '__main__':
    main()
