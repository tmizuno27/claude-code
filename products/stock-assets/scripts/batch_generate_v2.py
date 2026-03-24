"""
Stock Asset Batch Generator v2
Supports expanded prompt library with multiple categories.
Generates, downloads, upscales, and creates metadata in one pipeline.
"""
import json
import os
import sys
import time
import csv
import requests
from datetime import datetime
from PIL import Image

# Configuration
API_URL = "http://localhost:7055/v1/images/generations"
API_KEY = "stockasset2026"
GS_COOKIE = "session_id=721a25cc-2232-4a9f-b2e6-4d997c9ab690:2e670da5328d8b01a5f3b6c83db930fd071cc14d7308b687863cbd6d07493772"

BASE_DIR = os.path.dirname(os.path.dirname(__file__))
IMAGE_DIR = os.path.join(BASE_DIR, "output", "images")
UPSCALED_DIR = os.path.join(BASE_DIR, "output", "upscaled")
METADATA_DIR = os.path.join(BASE_DIR, "output", "metadata")

DELAY_BETWEEN_REQUESTS = 15
MAX_RETRIES = 2
REQUEST_TIMEOUT = 120
TARGET_SIZE = 4096
RATE_LIMIT_WAIT = 330  # 5.5 minutes between rate limit checks
RATE_LIMIT_MAX_WAIT = 5 * 3600 + 600  # max 5h40m total wait


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

    total_waited = 0
    for attempt in range(MAX_RETRIES):
        try:
            resp = requests.post(
                API_URL, headers=headers, json=payload,
                timeout=REQUEST_TIMEOUT
            )
            data = resp.json()

            if "error" in data:
                err_msg = data['error'].get('message', str(data['error']))
                print(f"  API Error: {err_msg}")

                # Rate limit or cookie exhaustion -> wait for reset
                if any(kw in err_msg.lower() for kw in [
                    "temporarily unavailable", "no valid cookies",
                    "no valid task", "rate limit"
                ]):
                    if total_waited >= RATE_LIMIT_MAX_WAIT:
                        print(f"  [RATE LIMIT] Max wait time exceeded. Giving up.")
                        return None
                    now = datetime.now().strftime("%H:%M:%S")
                    print(f"  [RATE LIMIT] Detected at {now}. Waiting {RATE_LIMIT_WAIT}s for reset...")
                    time.sleep(RATE_LIMIT_WAIT)
                    total_waited += RATE_LIMIT_WAIT
                    attempt -= 1  # don't count as retry
                    continue

                if attempt < MAX_RETRIES - 1:
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
    """Download image from genspark URL."""
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


def upscale_image(src_path, dst_path):
    """Tile 2x2 and upscale to TARGET_SIZE."""
    try:
        img = Image.open(src_path).convert("RGB")
        w, h = img.size
        tiled = Image.new("RGB", (w * 2, h * 2))
        tiled.paste(img, (0, 0))
        tiled.paste(img, (w, 0))
        tiled.paste(img, (0, h))
        tiled.paste(img, (w, h))
        if tiled.size[0] != TARGET_SIZE:
            tiled = tiled.resize((TARGET_SIZE, TARGET_SIZE), Image.LANCZOS)
        tiled.save(dst_path, "JPEG", quality=95, subsampling=0)
        return True
    except Exception as e:
        print(f"  Upscale error: {e}")
        return False


def run_batch(prompts_file, start_index=0, count=50):
    """Run batch: generate → download → upscale."""
    with open(prompts_file, "r", encoding="utf-8") as f:
        prompts = json.load(f)

    end_index = min(start_index + count, len(prompts))
    batch = prompts[start_index:end_index]

    os.makedirs(IMAGE_DIR, exist_ok=True)
    os.makedirs(UPSCALED_DIR, exist_ok=True)

    print(f"\n{'='*60}")
    print(f"Stock Asset Batch Generator v2")
    print(f"Source: {os.path.basename(prompts_file)}")
    print(f"Processing: {start_index} to {end_index - 1} ({len(batch)} items)")
    print(f"{'='*60}\n")

    results = []
    success_count = 0
    fail_count = 0
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    # Use global index starting at 50 (after existing images)
    global_offset = 50

    for i, prompt_data in enumerate(batch):
        idx = global_offset + start_index + i
        category = prompt_data.get("category", "unknown")
        subcategory = prompt_data.get("subcategory", "unknown").replace(" ", "_")
        title = prompt_data.get("title", "Untitled")

        print(f"[{i+1}/{len(batch)}] {title}")
        print(f"  Cat: {category}/{subcategory}")

        # Generate
        image_url = generate_image(prompt_data)
        if not image_url:
            print(f"  [FAIL] Generation failed")
            fail_count += 1
            results.append({**prompt_data, "status": "failed", "filename": ""})
            time.sleep(DELAY_BETWEEN_REQUESTS)
            continue

        # Download PNG
        png_name = f"stock_{idx:04d}_{category}_{subcategory}.png"
        png_path = os.path.join(IMAGE_DIR, png_name)
        if not download_image(image_url, png_path):
            print(f"  [FAIL] Download failed")
            fail_count += 1
            results.append({**prompt_data, "status": "download_failed", "filename": ""})
            time.sleep(DELAY_BETWEEN_REQUESTS)
            continue

        # Upscale to JPEG
        jpg_name = png_name.replace(".png", ".jpg")
        jpg_path = os.path.join(UPSCALED_DIR, jpg_name)
        if upscale_image(png_path, jpg_path):
            size_mb = os.path.getsize(jpg_path) / (1024 * 1024)
            print(f"  [OK] {jpg_name} ({size_mb:.1f} MB)")
            success_count += 1
            results.append({
                **prompt_data,
                "status": "success",
                "filename": jpg_name,
                "file_size_mb": f"{size_mb:.1f}"
            })
        else:
            print(f"  [WARN] Generated but upscale failed")
            success_count += 1  # Image was generated successfully
            results.append({
                **prompt_data,
                "status": "upscale_failed",
                "filename": png_name,
            })

        # Rate limiting
        if i < len(batch) - 1:
            time.sleep(DELAY_BETWEEN_REQUESTS)

    # Save results
    results_file = os.path.join(
        METADATA_DIR, f"batch_v2_results_{timestamp}.csv"
    )
    with open(results_file, "w", encoding="utf-8", newline="") as f:
        fieldnames = [
            "status", "filename", "category", "subcategory",
            "style", "color_scheme", "model", "title", "tags",
            "prompt", "file_size_mb"
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
    prompts_file = os.path.join(METADATA_DIR, "prompts_expanded.json")
    start = int(sys.argv[1]) if len(sys.argv) > 1 else 0
    count = int(sys.argv[2]) if len(sys.argv) > 2 else 50
    run_batch(prompts_file, start_index=start, count=count)
