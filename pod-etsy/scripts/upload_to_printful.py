"""
Upload designs to Printful and create products via REST API.

Reads printful-ready images and creates products that sync to Etsy.
Requires PRINTFUL_API_KEY environment variable.

API Reference: https://developers.printful.com/docs/
"""
import os
import sys
import json
import time
import base64
import requests
from pathlib import Path
from datetime import datetime

BASE_DIR = Path(__file__).parent.parent
PRINTFUL_READY_DIR = BASE_DIR / 'designs' / 'printful-ready'
UPLOAD_LOG = BASE_DIR / 'designs' / 'upload-log.json'

PRINTFUL_API_KEY = os.environ.get('PRINTFUL_API_KEY', '')
PRINTFUL_BASE_URL = 'https://api.printful.com'

# Printful product IDs (catalog variants)
# See: https://developers.printful.com/docs/#tag/Catalog-API
PRODUCT_CONFIG = {
    'tshirt': {
        'product_id': 71,  # Unisex Staple T-Shirt (Bella + Canvas 3001)
        'variant_ids': [
            4011, 4012, 4013, 4014, 4017,  # S, M, L, XL, 2XL (Black)
            4018, 4019, 4020, 4021, 4024,  # S, M, L, XL, 2XL (White)
        ],
        'retail_price': '24.99',
        'placement': 'front',
    },
    'mug-11oz': {
        'product_id': 19,  # White Glossy Mug 11oz
        'variant_ids': [1320],
        'retail_price': '17.99',
        'placement': 'default',
    },
    'poster-18x24': {
        'product_id': 1,  # Enhanced Matte Paper Poster 18x24
        'variant_ids': [1],
        'retail_price': '19.99',
        'placement': 'default',
    },
}

# Niche display names for product titles
NICHE_NAMES = {
    'niche-01-japan-zen': 'Japanese Zen',
    'niche-02-south-america': 'South America',
    'niche-03-bilingual-jp-es': 'JP-ES Bilingual',
    'niche-04-digital-nomad': 'Digital Nomad',
    'niche-05-quotes': 'Inspirational Quote',
}

PRODUCT_NAMES = {
    'tshirt': 'T-Shirt',
    'mug-11oz': '11oz Mug',
    'poster-18x24': '18x24 Poster',
}


def get_headers():
    return {
        'Authorization': f'Bearer {PRINTFUL_API_KEY}',
        'Content-Type': 'application/json',
    }


def load_upload_log():
    if UPLOAD_LOG.exists():
        with open(UPLOAD_LOG, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {'uploads': {}, 'products': {}, 'errors': {}}


def save_upload_log(log):
    with open(UPLOAD_LOG, 'w', encoding='utf-8') as f:
        json.dump(log, f, indent=2, ensure_ascii=False)


def upload_file_to_printful(image_path: Path) -> dict | None:
    """
    Upload a file to Printful's file library.
    Returns file info dict or None on failure.
    """
    url = f'{PRINTFUL_BASE_URL}/files'

    # Read and base64 encode
    with open(image_path, 'rb') as f:
        image_data = base64.b64encode(f.read()).decode('utf-8')

    payload = {
        'type': 'default',
        'url': f'data:image/png;base64,{image_data}',
    }

    try:
        resp = requests.post(url, headers=get_headers(), json=payload, timeout=120)
        resp.raise_for_status()
        result = resp.json()
        return result.get('result', {})
    except Exception as e:
        print(f'    [ERROR] Upload failed: {e}')
        return None


def create_product(product_type: str, niche: str, design_name: str, file_id: int) -> dict | None:
    """
    Create a Printful product (synced to Etsy store).
    """
    config = PRODUCT_CONFIG[product_type]
    niche_label = NICHE_NAMES.get(niche, niche)
    product_label = PRODUCT_NAMES[product_type]

    # Clean design name from filename
    clean_name = design_name.replace('.png', '').replace('-', ' ').title()
    title = f'{clean_name} | {niche_label} {product_label} | AsuInk'

    url = f'{PRINTFUL_BASE_URL}/store/products'

    # Build variant list
    variants = []
    for vid in config['variant_ids']:
        variants.append({
            'variant_id': vid,
            'retail_price': config['retail_price'],
            'files': [
                {
                    'type': config['placement'],
                    'id': file_id,
                }
            ],
        })

    payload = {
        'sync_product': {
            'name': title,
            'thumbnail': file_id,
        },
        'sync_variants': variants,
    }

    try:
        resp = requests.post(url, headers=get_headers(), json=payload, timeout=60)
        resp.raise_for_status()
        result = resp.json()
        return result.get('result', {})
    except Exception as e:
        print(f'    [ERROR] Product creation failed: {e}')
        if hasattr(e, 'response') and e.response is not None:
            print(f'    Response: {e.response.text[:300]}')
        return None


def process_all():
    """Upload all printful-ready designs and create products."""
    if not PRINTFUL_API_KEY:
        print('[ERROR] PRINTFUL_API_KEY environment variable is not set.')
        print('  Set it with: export PRINTFUL_API_KEY="your-api-key"')
        sys.exit(1)

    log = load_upload_log()
    total_created = 0
    total_skipped = 0

    print('=' * 60)
    print('Printful Upload & Product Creator')
    print('=' * 60)

    for product_type in PRODUCT_CONFIG:
        product_dir = PRINTFUL_READY_DIR / product_type
        if not product_dir.exists():
            print(f'\n[SKIP] {product_type}: directory not found')
            continue

        print(f'\n--- {PRODUCT_NAMES[product_type]} ---')

        for niche_dir in sorted(product_dir.iterdir()):
            if not niche_dir.is_dir():
                continue

            niche_name = niche_dir.name
            print(f'  Niche: {niche_name}')

            for png_file in sorted(niche_dir.glob('*.png')):
                log_key = f'{product_type}/{niche_name}/{png_file.name}'

                if log_key in log['products']:
                    print(f'    SKIP: {png_file.name} (already created)')
                    total_skipped += 1
                    continue

                # Step 1: Upload file
                print(f'    Uploading: {png_file.name}...', end=' ', flush=True)
                file_info = upload_file_to_printful(png_file)

                if not file_info or 'id' not in file_info:
                    print('FAILED')
                    log['errors'][log_key] = {
                        'timestamp': datetime.now().isoformat(),
                        'step': 'upload',
                    }
                    save_upload_log(log)
                    continue

                file_id = file_info['id']
                log['uploads'][log_key] = {
                    'file_id': file_id,
                    'timestamp': datetime.now().isoformat(),
                }
                print(f'OK (file_id={file_id})')

                # Step 2: Create product
                print(f'    Creating product...', end=' ', flush=True)
                product = create_product(product_type, niche_name, png_file.name, file_id)

                if product:
                    product_id = product.get('sync_product', {}).get('id', 'unknown')
                    print(f'OK (product_id={product_id})')
                    log['products'][log_key] = {
                        'product_id': product_id,
                        'file_id': file_id,
                        'timestamp': datetime.now().isoformat(),
                    }
                    total_created += 1
                else:
                    print('FAILED')
                    log['errors'][log_key] = {
                        'timestamp': datetime.now().isoformat(),
                        'step': 'create_product',
                        'file_id': file_id,
                    }

                save_upload_log(log)
                time.sleep(2)  # Rate limiting

    print('\n' + '=' * 60)
    print(f'Done! Created: {total_created}, Skipped: {total_skipped}')
    print(f'Upload log: {UPLOAD_LOG}')
    print('=' * 60)


if __name__ == '__main__':
    process_all()
