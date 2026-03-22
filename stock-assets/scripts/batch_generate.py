"""
Stock Asset Batch Generator
Generates images via genspark2api, downloads them, and creates metadata CSV.
"""
import json
import os
import sys
import time
import csv
import requests
from datetime import datetime

# Configuration
API_URL = "http://localhost:7055/v1/images/generations"
API_KEY = "stockasset2026"
GS_COOKIE = "session_id=990a262e-eac3-4a0b-8871-3f7eefebb138:e4f283fee18d7fbd247642f215caeb6806a64e313a444e16abb535b20cbed73c"

BASE_DIR = os.path.dirname(os.path.dirname(__file__))
IMAGE_DIR = os.path.join(BASE_DIR, "output", "images")
METADATA_DIR = os.path.join(BASE_DIR, "output", "metadata")
PROMPTS_FILE = os.path.join(METADATA_DIR, "prompts.json")

# Rate limiting
DELAY_BETWEEN_REQUESTS = 15  # seconds between requests to avoid rate limits
MAX_RETRIES = 2
REQUEST_TIMEOUT = 120  # seconds


def generate_image(prompt_data):
    """Call genspark2api to generate an image."""
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {API_KEY}"
    }
    payload = {
        "model": prompt_data.get("model", "recraft-v3"),
        "prompt": prompt_data["prompt"],
        "n": 1,
        "size": "1024x1024"
    }

    for attempt in range(MAX_RETRIES):
        try:
            resp = requests.post(
                API_URL, headers=headers, json=payload,
                timeout=REQUEST_TIMEOUT
            )
            data = resp.json()

            if "error" in data:
                print(f"  API Error: {data['error']['message']}")
                if attempt < MAX_RETRIES - 1:
                    print(f"  Retrying in {DELAY_BETWEEN_REQUESTS}s...")
                    time.sleep(DELAY_BETWEEN_REQUESTS)
                    continue
                return None

            if "data" in data and len(data["data"]) > 0:
                return data["data"][0].get("url")

        except requests.exceptions.Timeout:
            print(f"  Timeout (attempt {attempt + 1})")
            if attempt < MAX_RETRIES - 1:
                time.sleep(DELAY_BETWEEN_REQUESTS)
                continue
        except Exception as e:
            print(f"  Error: {e}")
            return None

    return None


def download_image(url, filepath):
    """Download image from genspark URL (requires cookie auth)."""
    cookies = {}
    for part in GS_COOKIE.split("; "):
        if "=" in part:
            key, val = part.split("=", 1)
            cookies[key] = val

    try:
        resp = requests.get(url, cookies=cookies, timeout=60)
        if resp.status_code == 200 and len(resp.content) > 1000:
            with open(filepath, "wb") as f:
                f.write(resp.content)
            return True
        else:
            print(f"  Download failed: status={resp.status_code}, size={len(resp.content)}")
            return False
    except Exception as e:
        print(f"  Download error: {e}")
        return False


def run_batch(start_index=0, count=10):
    """Run batch image generation."""
    with open(PROMPTS_FILE, "r", encoding="utf-8") as f:
        prompts = json.load(f)

    end_index = min(start_index + count, len(prompts))
    batch = prompts[start_index:end_index]

    print(f"\n{'='*60}")
    print(f"Stock Asset Batch Generator")
    print(f"Processing prompts {start_index} to {end_index - 1} ({len(batch)} items)")
    print(f"{'='*60}\n")

    results = []
    success_count = 0
    fail_count = 0
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    for i, prompt_data in enumerate(batch):
        idx = start_index + i
        print(f"[{i+1}/{len(batch)}] {prompt_data['title']}")
        print(f"  Model: {prompt_data['model']}")

        # Generate
        image_url = generate_image(prompt_data)
        if not image_url:
            print(f"  [FAIL] Generation failed")
            fail_count += 1
            results.append({**prompt_data, "status": "failed", "filename": ""})
            time.sleep(DELAY_BETWEEN_REQUESTS)
            continue

        print(f"  [OK] Generated: {image_url[:80]}...")

        # Download
        filename = f"stock_{idx:04d}_{prompt_data['type']}_{prompt_data['category']}.png"
        filepath = os.path.join(IMAGE_DIR, filename)

        if download_image(image_url, filepath):
            size_kb = os.path.getsize(filepath) / 1024
            print(f"  [DL] Downloaded: {filename} ({size_kb:.0f} KB)")
            success_count += 1
            results.append({
                **prompt_data,
                "status": "success",
                "filename": filename,
                "url": image_url,
                "file_size_kb": f"{size_kb:.0f}"
            })
        else:
            print(f"  [FAIL] Download failed")
            fail_count += 1
            results.append({**prompt_data, "status": "download_failed", "filename": ""})

        # Rate limiting
        if i < len(batch) - 1:
            print(f"  [WAIT] {DELAY_BETWEEN_REQUESTS}s...")
            time.sleep(DELAY_BETWEEN_REQUESTS)

    # Save results CSV
    results_file = os.path.join(METADATA_DIR, f"batch_results_{timestamp}.csv")
    with open(results_file, "w", encoding="utf-8", newline="") as f:
        fieldnames = [
            "status", "filename", "type", "category", "model",
            "title", "tags", "prompt", "url", "file_size_kb"
        ]
        writer = csv.DictWriter(f, fieldnames=fieldnames, extrasaction="ignore")
        writer.writeheader()
        for r in results:
            row = {**r}
            if isinstance(row.get("tags"), list):
                row["tags"] = "; ".join(row["tags"])
            writer.writerow(row)

    print(f"\n{'='*60}")
    print(f"Batch Complete!")
    print(f"  Success: {success_count}")
    print(f"  Failed:  {fail_count}")
    print(f"  Results: {results_file}")
    print(f"{'='*60}")

    return success_count, fail_count


if __name__ == "__main__":
    start = int(sys.argv[1]) if len(sys.argv) > 1 else 0
    count = int(sys.argv[2]) if len(sys.argv) > 2 else 10

    run_batch(start_index=start, count=count)
