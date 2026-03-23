"""
POD Design Generator using Google Gemini API (REST)
Generates 50 designs from prompts in ../designs/prompts/
Saves output to ../designs/generated/
Uses direct REST API calls to Imagen 3 (no SDK import issues)
"""
import os
import json
import re
import time
import sys
import base64
import requests
from pathlib import Path
from datetime import datetime

# Configuration
GEMINI_API_KEY = os.environ.get('GEMINI_API_KEY', '')
BASE_DIR = Path(__file__).parent.parent
OUTPUT_DIR = BASE_DIR / 'designs' / 'generated'
PROMPTS_DIR = BASE_DIR / 'designs' / 'prompts'
PROGRESS_FILE = OUTPUT_DIR / 'progress.json'

REQUEST_DELAY = 5
MAX_RETRIES = 3
RETRY_DELAY = 15

NICHE_FILES = [
    'niche-01-japan-zen.md',
    'niche-02-south-america.md',
    'niche-03-bilingual-jp-es.md',
    'niche-04-digital-nomad.md',
    'niche-05-quotes.md',
]

# Imagen 4.0 REST endpoint (requires paid plan)
IMAGEN_URL = "https://generativelanguage.googleapis.com/v1beta/models/imagen-4.0-generate-001:predict"
# Gemini 2.5 Flash Image (requires paid plan or quota)
GEMINI_URL = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash-image:generateContent"


def load_progress():
    if PROGRESS_FILE.exists():
        with open(PROGRESS_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {'generated': {}, 'errors': {}, 'started_at': datetime.now().isoformat()}


def save_progress(progress):
    PROGRESS_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(PROGRESS_FILE, 'w', encoding='utf-8') as f:
        json.dump(progress, f, indent=2, ensure_ascii=False)


def parse_prompts(prompt_file: Path) -> list[dict]:
    text = prompt_file.read_text(encoding='utf-8')
    designs = []
    blocks = re.split(r'^## Design (\d+):\s*(.+)$', text, flags=re.MULTILINE)
    i = 1
    while i < len(blocks) - 2:
        number = int(blocks[i])
        title = blocks[i + 1].strip()
        content = blocks[i + 2]
        fn_match = re.search(r'\*\*Filename\*\*:\s*`([^`]+)`', content)
        filename = fn_match.group(1) if fn_match else f'design-{number:02d}.png'
        prompt_match = re.search(r'```\n(.*?)\n```', content, re.DOTALL)
        prompt = prompt_match.group(1).strip() if prompt_match else ''
        if prompt:
            designs.append({'number': number, 'title': title, 'filename': filename, 'prompt': prompt})
        i += 3
    return designs


def generate_with_imagen(prompt: str, output_path: Path) -> bool:
    """Generate image using Imagen 3 REST API."""
    payload = {
        "instances": [{"prompt": prompt}],
        "parameters": {
            "sampleCount": 1,
            "aspectRatio": "4:5",
            "outputOptions": {"mimeType": "image/png"}
        }
    }
    resp = requests.post(
        f"{IMAGEN_URL}?key={GEMINI_API_KEY}",
        json=payload,
        timeout=120,
    )
    if resp.status_code == 200:
        data = resp.json()
        if 'predictions' in data and data['predictions']:
            img_b64 = data['predictions'][0].get('bytesBase64Encoded', '')
            if img_b64:
                output_path.parent.mkdir(parents=True, exist_ok=True)
                with open(output_path, 'wb') as f:
                    f.write(base64.b64decode(img_b64))
                return True
    return False


def generate_with_gemini_flash(prompt: str, output_path: Path) -> bool:
    """Fallback: Generate image using Gemini 2.0 Flash."""
    payload = {
        "contents": [{"parts": [{"text": prompt}]}],
        "generationConfig": {
            "responseModalities": ["IMAGE", "TEXT"]
        }
    }
    resp = requests.post(
        f"{GEMINI_URL}?key={GEMINI_API_KEY}",
        json=payload,
        timeout=120,
    )
    if resp.status_code == 200:
        data = resp.json()
        candidates = data.get('candidates', [])
        if candidates:
            for part in candidates[0].get('content', {}).get('parts', []):
                inline = part.get('inlineData', {})
                if inline.get('mimeType', '').startswith('image/'):
                    output_path.parent.mkdir(parents=True, exist_ok=True)
                    with open(output_path, 'wb') as f:
                        f.write(base64.b64decode(inline['data']))
                    return True
    return False


def generate_design(prompt: str, output_path: Path, retries: int = MAX_RETRIES) -> bool:
    """Try Imagen 3 first, fall back to Gemini Flash."""
    for attempt in range(1, retries + 1):
        try:
            # Try Imagen 3
            if generate_with_imagen(prompt, output_path):
                return True
            # Fallback to Gemini Flash
            print(f'    [INFO] Imagen returned no image, trying Gemini Flash...', flush=True)
            if generate_with_gemini_flash(prompt, output_path):
                return True
            print(f'    [WARN] Attempt {attempt}/{retries}: No image from either model', flush=True)
        except Exception as e:
            print(f'    [ERROR] Attempt {attempt}/{retries}: {str(e)[:200]}', flush=True)

        if attempt < retries:
            print(f'    Retrying in {RETRY_DELAY}s...', flush=True)
            time.sleep(RETRY_DELAY)

    return False


def process_all_niches():
    if not GEMINI_API_KEY:
        print('[ERROR] GEMINI_API_KEY not set.', flush=True)
        sys.exit(1)

    progress = load_progress()
    total_generated = 0
    total_skipped = 0
    total_errors = 0

    print('=' * 60, flush=True)
    print('POD Design Generator - Gemini Imagen 3 (REST API)', flush=True)
    print(f'Output: {OUTPUT_DIR}', flush=True)
    print('=' * 60, flush=True)

    for niche_file in NICHE_FILES:
        prompt_path = PROMPTS_DIR / niche_file
        if not prompt_path.exists():
            print(f'\n[SKIP] {niche_file} not found', flush=True)
            continue

        niche_name = niche_file.replace('.md', '')
        niche_dir = OUTPUT_DIR / niche_name
        niche_dir.mkdir(parents=True, exist_ok=True)

        print(f'\n--- {niche_name} ---', flush=True)
        designs = parse_prompts(prompt_path)
        print(f'  Found {len(designs)} prompts', flush=True)

        for design in designs:
            output_path = niche_dir / design['filename']
            progress_key = f'{niche_name}/{design["filename"]}'

            if output_path.exists():
                print(f'  [{design["number"]:02d}] SKIP (exists): {design["filename"]}', flush=True)
                total_skipped += 1
                continue

            if progress_key in progress.get('generated', {}):
                total_skipped += 1
                continue

            print(f'  [{design["number"]:02d}] Generating: {design["title"]}...', flush=True)
            success = generate_design(design['prompt'], output_path)

            if success:
                file_size = output_path.stat().st_size / 1024
                print(f'         -> Saved: {design["filename"]} ({file_size:.0f} KB)', flush=True)
                progress['generated'][progress_key] = {
                    'timestamp': datetime.now().isoformat(),
                    'title': design['title'],
                }
                total_generated += 1
            else:
                print(f'         -> FAILED: {design["filename"]}', flush=True)
                progress['errors'][progress_key] = {
                    'timestamp': datetime.now().isoformat(),
                    'title': design['title'],
                    'prompt_preview': design['prompt'][:100],
                }
                total_errors += 1

            save_progress(progress)
            time.sleep(REQUEST_DELAY)

    progress['last_run'] = datetime.now().isoformat()
    save_progress(progress)

    print('\n' + '=' * 60, flush=True)
    print(f'Done! Generated: {total_generated}, Skipped: {total_skipped}, Errors: {total_errors}', flush=True)
    print('=' * 60, flush=True)


if __name__ == '__main__':
    process_all_niches()
