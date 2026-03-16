"""
POD Design Generator using Google Gemini API
Generates 50 designs from prompts in ../designs/prompts/
Saves output to ../designs/generated/
Progress tracked in ../designs/generated/progress.json
"""
import google.generativeai as genai
import os
import json
import re
import time
import sys
from pathlib import Path
from datetime import datetime

# Configuration
GEMINI_API_KEY = os.environ.get('GEMINI_API_KEY', '')
BASE_DIR = Path(__file__).parent.parent
OUTPUT_DIR = BASE_DIR / 'designs' / 'generated'
PROMPTS_DIR = BASE_DIR / 'designs' / 'prompts'
PROGRESS_FILE = OUTPUT_DIR / 'progress.json'

# Rate limiting
REQUEST_DELAY = 3  # seconds between requests
MAX_RETRIES = 3
RETRY_DELAY = 10  # seconds before retry

NICHE_FILES = [
    'niche-01-japan-zen.md',
    'niche-02-south-america.md',
    'niche-03-bilingual-jp-es.md',
    'niche-04-digital-nomad.md',
    'niche-05-quotes.md',
]


def setup_gemini():
    """Configure and return Gemini model with image generation."""
    if not GEMINI_API_KEY:
        print('[ERROR] GEMINI_API_KEY environment variable is not set.')
        print('  Set it with: export GEMINI_API_KEY="your-api-key"')
        sys.exit(1)

    genai.configure(api_key=GEMINI_API_KEY)
    model = genai.GenerativeModel('gemini-2.0-flash-exp')
    return model


def load_progress():
    """Load progress tracking file."""
    if PROGRESS_FILE.exists():
        with open(PROGRESS_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {'generated': {}, 'errors': {}, 'started_at': datetime.now().isoformat()}


def save_progress(progress):
    """Save progress tracking file."""
    PROGRESS_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(PROGRESS_FILE, 'w', encoding='utf-8') as f:
        json.dump(progress, f, indent=2, ensure_ascii=False)


def parse_prompts(prompt_file: Path) -> list[dict]:
    """
    Parse a prompt markdown file and extract individual prompts.

    Expected format per design:
        ## Design NN: Title
        **Filename**: `filename.png`
        ```
        prompt text here
        ```

    Returns list of dicts with keys: number, title, filename, prompt
    """
    text = prompt_file.read_text(encoding='utf-8')
    designs = []

    # Split by ## Design headers
    blocks = re.split(r'^## Design (\d+):\s*(.+)$', text, flags=re.MULTILINE)
    # blocks[0] = header text before first design
    # then groups of 3: (number, title, content)

    i = 1
    while i < len(blocks) - 2:
        number = int(blocks[i])
        title = blocks[i + 1].strip()
        content = blocks[i + 2]

        # Extract filename
        fn_match = re.search(r'\*\*Filename\*\*:\s*`([^`]+)`', content)
        filename = fn_match.group(1) if fn_match else f'design-{number:02d}.png'

        # Extract prompt from code block
        prompt_match = re.search(r'```\n(.*?)\n```', content, re.DOTALL)
        prompt = prompt_match.group(1).strip() if prompt_match else ''

        if prompt:
            designs.append({
                'number': number,
                'title': title,
                'filename': filename,
                'prompt': prompt,
            })

        i += 3

    return designs


def generate_design(model, prompt: str, output_path: Path, retries: int = MAX_RETRIES) -> bool:
    """
    Generate a single design image using Gemini.
    Returns True on success, False on failure.
    """
    for attempt in range(1, retries + 1):
        try:
            response = model.generate_content(
                prompt,
                generation_config=genai.GenerationConfig(
                    response_mime_type='image/png',
                ),
            )

            # Check if response contains image data
            if response.candidates and response.candidates[0].content.parts:
                for part in response.candidates[0].content.parts:
                    if hasattr(part, 'inline_data') and part.inline_data:
                        image_data = part.inline_data.data
                        output_path.parent.mkdir(parents=True, exist_ok=True)
                        with open(output_path, 'wb') as f:
                            f.write(image_data)
                        return True

            # Fallback: try using Imagen via Gemini if available
            if hasattr(response, 'images') and response.images:
                img = response.images[0]
                output_path.parent.mkdir(parents=True, exist_ok=True)
                img.save(str(output_path))
                return True

            print(f'    [WARN] Attempt {attempt}/{retries}: No image data in response')

        except Exception as e:
            print(f'    [ERROR] Attempt {attempt}/{retries}: {e}')
            if attempt < retries:
                print(f'    Retrying in {RETRY_DELAY}s...')
                time.sleep(RETRY_DELAY)

    return False


def process_all_niches():
    """Process all 5 niche prompt files and generate designs."""
    model = setup_gemini()
    progress = load_progress()

    total_generated = 0
    total_skipped = 0
    total_errors = 0

    print('=' * 60)
    print('POD Design Generator - Google Gemini')
    print(f'Output: {OUTPUT_DIR}')
    print('=' * 60)

    for niche_file in NICHE_FILES:
        prompt_path = PROMPTS_DIR / niche_file
        if not prompt_path.exists():
            print(f'\n[SKIP] {niche_file} not found')
            continue

        niche_name = niche_file.replace('.md', '')
        niche_dir = OUTPUT_DIR / niche_name
        niche_dir.mkdir(parents=True, exist_ok=True)

        print(f'\n--- {niche_name} ---')
        designs = parse_prompts(prompt_path)
        print(f'  Found {len(designs)} prompts')

        for design in designs:
            output_path = niche_dir / design['filename']
            progress_key = f'{niche_name}/{design["filename"]}'

            # Skip if already generated
            if output_path.exists():
                print(f'  [{design["number"]:02d}] SKIP (exists): {design["filename"]}')
                total_skipped += 1
                continue

            # Skip if previously marked as generated in progress
            if progress_key in progress['generated']:
                print(f'  [{design["number"]:02d}] SKIP (logged): {design["filename"]}')
                total_skipped += 1
                continue

            print(f'  [{design["number"]:02d}] Generating: {design["title"]}...')
            success = generate_design(model, design['prompt'], output_path)

            if success:
                print(f'         -> Saved: {design["filename"]}')
                progress['generated'][progress_key] = {
                    'timestamp': datetime.now().isoformat(),
                    'title': design['title'],
                }
                total_generated += 1
            else:
                print(f'         -> FAILED: {design["filename"]}')
                progress['errors'][progress_key] = {
                    'timestamp': datetime.now().isoformat(),
                    'title': design['title'],
                    'prompt_preview': design['prompt'][:100],
                }
                total_errors += 1

            save_progress(progress)
            time.sleep(REQUEST_DELAY)

    # Summary
    progress['last_run'] = datetime.now().isoformat()
    save_progress(progress)

    print('\n' + '=' * 60)
    print(f'Done! Generated: {total_generated}, Skipped: {total_skipped}, Errors: {total_errors}')
    print(f'Progress log: {PROGRESS_FILE}')
    print('=' * 60)


if __name__ == '__main__':
    process_all_niches()
