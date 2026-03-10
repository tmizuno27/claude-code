"""
Free stock image bulk downloader using Pexels API
License: Pexels License (free for commercial use, no attribution required)
"""

import os
import time
import json
import requests
from pathlib import Path
from datetime import datetime

BASE_DIR = Path(r"c:\Users\tmizu\マイドライブ\GitHub\claude-code\blog\images\stock")

HEADERS = {"Authorization": "test"}
PEXELS_SEARCH = "https://api.pexels.com/v1/search"

CATEGORIES = {
    "paraguay-life": [
        "asuncion city", "south america landscape", "south america street",
        "tropical market", "palm tree landscape", "river sunset tropical",
        "yerba mate", "south america culture", "colonial architecture",
        "tropical garden flowers", "red earth road", "south america nature",
        "latin america plaza",
    ],
    "food-culture": [
        "barbecue grill meat", "grilled steak", "empanada",
        "south american food", "cassava food", "corn bread",
        "tropical fruit", "outdoor barbecue", "meat fire grill",
        "street food", "fresh juice", "family dinner outdoor",
    ],
    "finance-money": [
        "money transfer", "credit card hand", "online banking",
        "currency exchange", "savings piggy bank", "financial planning",
        "tax calculator", "freelancer invoice", "budget notebook",
        "coins money",
    ],
    "remote-work": [
        "remote work laptop", "digital nomad", "work from home",
        "freelancer coffee laptop", "video call", "coworking space",
        "laptop tropical", "typing keyboard", "home office desk",
        "programming code", "online meeting", "laptop nature outdoor",
    ],
    "family-education": [
        "family travel airport", "children school", "kids playing outdoor",
        "international school", "family moving boxes", "children studying",
        "parent child reading", "family dinner", "kids soccer",
        "bilingual classroom", "family suitcase", "school building",
    ],
    "immigration-visa": [
        "passport stamps", "airport departure", "moving boxes",
        "suitcase packing", "document paperwork", "checklist notebook",
        "new home keys", "airplane sky", "customs control",
        "travel documents",
    ],
    "healthcare": [
        "hospital building", "doctor patient", "health insurance",
        "pharmacy medicine", "medical checkup", "stethoscope",
        "family healthcare", "dental clinic",
    ],
    "real-estate": [
        "house tropical", "apartment exterior", "real estate",
        "living room interior", "swimming pool house", "house garden",
        "house keys", "modern house",
    ],
    "transportation": [
        "bus city", "taxi yellow", "car highway driving",
        "motorcycle traffic", "ride sharing app", "gas station",
        "road trip", "city traffic",
    ],
    "internet-vpn": [
        "wifi connection", "vpn security", "fiber optic",
        "smartphone mobile data", "cybersecurity", "router internet",
        "streaming laptop", "online privacy lock",
    ],
    "shopping-supermarket": [
        "supermarket aisle", "grocery shopping", "fresh vegetables market",
        "meat section", "shopping bags", "local market",
        "price comparison", "food ingredients",
    ],
    "blog-writing": [
        "blogging laptop", "content creation", "analytics dashboard",
        "social media marketing", "affiliate marketing", "video editing",
        "podcast microphone", "writing desk",
    ],
    "lifestyle-general": [
        "sunrise landscape", "morning coffee", "green forest nature",
        "peaceful river", "colorful flowers garden", "blue sky clouds",
        "nature walking path", "hammock tropical", "golden sunset",
        "night sky stars",
    ],
    "mental-health": [
        "meditation peaceful", "lonely person", "friends gathering",
        "happy family outdoor", "journal writing", "yoga outdoor",
        "video call family", "cultural exchange",
    ],
    "language-learning": [
        "language learning", "spanish textbook", "online class laptop",
        "conversation people", "dictionary book", "study desk",
    ],
    "climate-weather": [
        "sunny tropical weather", "tropical rain", "hot weather sun",
        "green after rain", "clear blue sky", "spring flowers",
    ],
    "kids-activities": [
        "children soccer", "kids swimming", "children art class",
        "kids piano music", "children dancing", "kids martial arts",
    ],
}

IMAGES_PER_KEYWORD = 5  # Pexels returns multiple per request


def download_pexels(query, save_dir, per_page=5):
    """Download images from Pexels API"""
    save_dir.mkdir(parents=True, exist_ok=True)
    downloaded = 0

    try:
        params = {"query": query, "per_page": per_page, "size": "large"}
        response = requests.get(PEXELS_SEARCH, headers=HEADERS, params=params, timeout=15)

        if response.status_code != 200:
            print(f"    API error: {response.status_code}")
            return 0

        data = response.json()
        photos = data.get("photos", [])

        for i, photo in enumerate(photos):
            img_url = photo.get("src", {}).get("large", "")
            if not img_url:
                continue

            safe_name = query.replace(" ", "-")[:40]
            filename = f"{safe_name}_{photo['id']}.jpg"
            filepath = save_dir / filename

            if filepath.exists():
                print(f"    - {filename} (skip)")
                continue

            try:
                img_resp = requests.get(img_url, timeout=30)
                if img_resp.status_code == 200 and len(img_resp.content) > 5000:
                    with open(filepath, "wb") as f:
                        f.write(img_resp.content)
                    downloaded += 1
                    photographer = photo.get("photographer", "unknown")
                    print(f"    OK {filename} ({len(img_resp.content)//1024}KB) by {photographer}")
                time.sleep(0.3)
            except Exception as e:
                print(f"    FAIL download: {e}")

    except Exception as e:
        print(f"    FAIL API: {e}")

    return downloaded


def main():
    print("=" * 60)
    print("Stock Image Downloader (Pexels API)")
    print(f"Save to: {BASE_DIR}")
    print(f"Categories: {len(CATEGORIES)}")
    total_kw = sum(len(v) for v in CATEGORIES.values())
    print(f"Keywords: {total_kw}")
    print(f"Max images: ~{total_kw * IMAGES_PER_KEYWORD}")
    print("=" * 60)

    total = 0
    log = {}

    for cat, keywords in CATEGORIES.items():
        print(f"\n[{cat}] ({len(keywords)} keywords)")
        cat_dir = BASE_DIR / cat
        cat_count = 0

        for kw in keywords:
            print(f"  > {kw}")
            n = download_pexels(kw, cat_dir, IMAGES_PER_KEYWORD)
            cat_count += n
            total += n
            time.sleep(1)  # rate limit

        log[cat] = cat_count
        print(f"  -> {cat}: {cat_count} images")

    # Save log
    log_data = {
        "downloaded_at": datetime.now().isoformat(),
        "source": "Pexels (pexels.com)",
        "license": "Pexels License - free commercial use, no attribution required",
        "total_images": total,
        "categories": log,
    }
    log_path = BASE_DIR / "download-log.json"
    with open(log_path, "w", encoding="utf-8") as f:
        json.dump(log_data, f, ensure_ascii=False, indent=2)

    print(f"\n{'=' * 60}")
    print(f"DONE! Total: {total} images downloaded")
    print(f"Log: {log_path}")
    print(f"{'=' * 60}")


if __name__ == "__main__":
    main()
