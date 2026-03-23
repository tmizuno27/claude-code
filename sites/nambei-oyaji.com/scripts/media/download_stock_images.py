"""
Free stock image bulk downloader
Uses Pixabay API (free key required) to download blog images by category.

Setup:
1. Go to https://pixabay.com/api/docs/ and sign up (free)
2. Copy your API key
3. Add to blog/config/secrets.json: {"pixabay": {"api_key": "YOUR_KEY"}}

License: Pixabay License - free for commercial use, no attribution required
"""

import os
import sys
import time
import json
import requests
from pathlib import Path
from datetime import datetime

BASE_DIR = Path(r"c:\Users\tmizu\マイドライブ\GitHub\claude-code\sites\nambei-oyaji.com\images\stock")
SECRETS_PATH = Path(r"c:\Users\tmizu\マイドライブ\GitHub\claude-code\sites\nambei-oyaji.com\config\secrets.json")

PIXABAY_SEARCH = "https://pixabay.com/api/"

CATEGORIES = {
    "paraguay-life": [
        "asuncion+city", "south+america+landscape", "south+america+street",
        "tropical+market", "palm+tree+landscape", "river+sunset",
        "yerba+mate", "colonial+architecture", "tropical+garden",
        "south+america+nature", "latin+america+plaza", "subtropical+forest",
        "terracotta+road",
    ],
    "food-culture": [
        "barbecue+grill", "grilled+steak", "empanada",
        "cassava+food", "corn+bread+rustic", "tropical+fruit+market",
        "outdoor+barbecue", "meat+fire", "street+food+latin",
        "fresh+juice+tropical", "family+dinner+outdoor", "beef+roast",
    ],
    "finance-money": [
        "money+transfer", "credit+card", "online+banking",
        "currency+exchange", "savings+money", "financial+planning",
        "tax+calculator", "invoice+laptop", "budget+spreadsheet",
        "coins+money+jar",
    ],
    "remote-work": [
        "remote+work+laptop", "digital+nomad+cafe", "work+from+home",
        "freelancer+laptop", "video+call+laptop", "coworking+space",
        "laptop+tropical", "typing+keyboard", "home+office",
        "programming+code", "online+meeting", "laptop+outdoor+nature",
    ],
    "family-education": [
        "family+travel+airport", "children+school", "kids+playing+outdoor",
        "international+school", "family+moving", "children+studying",
        "parent+child+reading", "family+dinner", "kids+soccer",
        "family+suitcase", "school+classroom", "children+learning",
    ],
    "immigration-visa": [
        "passport+stamps", "airport+departure", "moving+boxes",
        "suitcase+packing", "paperwork+documents", "checklist+notebook",
        "new+home+keys", "airplane+sky", "travel+documents",
        "customs+border",
    ],
    "healthcare": [
        "hospital+building", "doctor+patient", "health+insurance",
        "pharmacy+medicine", "medical+checkup", "stethoscope+doctor",
        "family+healthcare", "dental+clinic",
    ],
    "real-estate": [
        "tropical+house", "apartment+building", "real+estate+agent",
        "living+room+modern", "swimming+pool+house", "house+garden+tropical",
        "house+keys", "modern+house+exterior",
    ],
    "transportation": [
        "bus+city+public", "taxi+ride", "car+highway",
        "motorcycle+city", "ride+sharing", "gas+station",
        "road+trip+scenery", "city+traffic",
    ],
    "internet-vpn": [
        "wifi+internet", "cybersecurity+lock", "fiber+optic+cable",
        "smartphone+data", "network+security", "router+modem",
        "streaming+laptop", "privacy+online",
    ],
    "shopping-supermarket": [
        "supermarket+aisle", "grocery+shopping+cart", "vegetables+market",
        "meat+section", "shopping+bags+groceries", "local+market+produce",
        "price+tag", "food+ingredients+cooking",
    ],
    "blog-writing": [
        "blogging+laptop", "content+creation", "analytics+dashboard",
        "social+media+marketing", "writing+desk+notebook",
        "podcast+microphone", "seo+marketing", "video+editing+screen",
    ],
    "lifestyle-general": [
        "sunrise+landscape", "morning+coffee+routine", "green+forest",
        "river+peaceful", "colorful+flowers", "blue+sky+clouds",
        "nature+path+walking", "hammock+tropical", "sunset+golden",
        "starry+night+sky",
    ],
    "mental-health": [
        "meditation+peaceful", "lonely+window", "friends+gathering",
        "happy+family+outdoor", "journaling+notebook", "yoga+outdoor",
        "video+call+family", "cultural+exchange+people",
    ],
    "language-learning": [
        "language+learning+book", "spanish+textbook", "online+class",
        "conversation+people", "dictionary+book", "study+desk+lamp",
    ],
    "climate-weather": [
        "sunny+tropical", "tropical+rain+storm", "hot+weather",
        "green+nature+rain", "clear+blue+sky", "spring+flowers+bloom",
    ],
    "kids-activities": [
        "children+soccer+playing", "kids+swimming+pool", "children+art",
        "kids+piano+music", "children+dancing", "kids+martial+arts",
    ],
}

IMAGES_PER_KEYWORD = 5


def get_api_key():
    """Get Pixabay API key from secrets.json"""
    try:
        with open(SECRETS_PATH, "r", encoding="utf-8") as f:
            secrets = json.load(f)
        key = secrets.get("pixabay", {}).get("api_key", "")
        if key:
            return key
    except Exception:
        pass

    print("ERROR: Pixabay API key not found in secrets.json")
    print("Setup:")
    print("  1. Go to https://pixabay.com/api/docs/ and sign up (free)")
    print("  2. Copy your API key")
    print('  3. Add to secrets.json: "pixabay": {"api_key": "YOUR_KEY"}')
    sys.exit(1)


def download_pixabay(api_key, query, save_dir, per_page=5):
    """Download images from Pixabay API"""
    save_dir.mkdir(parents=True, exist_ok=True)
    downloaded = 0

    try:
        params = {
            "key": api_key,
            "q": query,
            "per_page": per_page,
            "image_type": "photo",
            "min_width": 1200,
            "safesearch": "true",
            "order": "popular",
        }
        response = requests.get(PIXABAY_SEARCH, params=params, timeout=15)

        if response.status_code != 200:
            print(f"    API error: {response.status_code}")
            return 0

        data = response.json()
        hits = data.get("hits", [])

        for photo in hits:
            img_url = photo.get("largeImageURL", "")
            if not img_url:
                continue

            safe_name = query.replace("+", "-")[:40]
            filename = f"{safe_name}_{photo['id']}.jpg"
            filepath = save_dir / filename

            if filepath.exists():
                continue

            try:
                img_resp = requests.get(img_url, timeout=30)
                if img_resp.status_code == 200 and len(img_resp.content) > 5000:
                    with open(filepath, "wb") as f:
                        f.write(img_resp.content)
                    downloaded += 1
                    print(f"    OK {filename} ({len(img_resp.content)//1024}KB)")
                time.sleep(0.2)
            except Exception as e:
                print(f"    FAIL: {e}")

    except Exception as e:
        print(f"    API error: {e}")

    return downloaded


def main():
    api_key = get_api_key()

    print("=" * 60)
    print("Stock Image Downloader (Pixabay API)")
    print(f"Categories: {len(CATEGORIES)}")
    total_kw = sum(len(v) for v in CATEGORIES.values())
    print(f"Keywords: {total_kw}, Max images: ~{total_kw * IMAGES_PER_KEYWORD}")
    print("=" * 60)

    total = 0
    log = {}

    for cat, keywords in CATEGORIES.items():
        print(f"\n[{cat}] ({len(keywords)} keywords)")
        cat_dir = BASE_DIR / cat
        cat_count = 0

        for kw in keywords:
            print(f"  > {kw.replace('+', ' ')}")
            n = download_pixabay(api_key, kw, cat_dir, IMAGES_PER_KEYWORD)
            cat_count += n
            total += n
            time.sleep(0.5)

        log[cat] = cat_count
        print(f"  -> {cat}: {cat_count} images")

    log_data = {
        "downloaded_at": datetime.now().isoformat(),
        "source": "Pixabay (pixabay.com)",
        "license": "Pixabay License - free commercial use, no attribution required",
        "total_images": total,
        "categories": log,
    }
    log_path = BASE_DIR / "download-log.json"
    log_path.parent.mkdir(parents=True, exist_ok=True)
    with open(log_path, "w", encoding="utf-8") as f:
        json.dump(log_data, f, ensure_ascii=False, indent=2)

    print(f"\n{'=' * 60}")
    print(f"DONE! Total: {total} images downloaded")
    print(f"{'=' * 60}")


if __name__ == "__main__":
    main()
