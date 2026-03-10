"""
フリー画像一括ダウンロードスクリプト
Unsplash Source API（APIキー不要）を使用して、ブログカテゴリ別に画像を収集

使用ライセンス: Unsplash License（商用利用可・クレジット不要だが推奨）
"""

import os
import time
import hashlib
import json
import requests
from pathlib import Path
from datetime import datetime

# ベースパス
BASE_DIR = Path(r"c:\Users\tmizu\マイドライブ\GitHub\claude-code\blog\images\stock")

# カテゴリ別の検索キーワード（英語のほうが結果が良い）
CATEGORIES = {
    "paraguay-life": [
        "asuncion paraguay", "paraguay landscape", "south america city",
        "south america street", "south america market", "subtropical garden",
        "palm tree tropical", "red soil road", "lapacho tree flower",
        "rio paraguay river", "south american sunset",
        "yerba mate drink", "terere cold drink",
    ],
    "food-culture": [
        "asado barbecue south america", "grilled meat bbq",
        "empanada food", "south american food", "mandioca cassava",
        "chipa bread", "sopa paraguaya", "tropical fruit market",
        "outdoor barbecue family", "meat grill fire",
        "street food latin america", "fresh juice tropical",
    ],
    "finance-money": [
        "money transfer international", "credit card payment",
        "online banking laptop", "currency exchange",
        "savings money jar", "financial planning desk",
        "wise transfer app", "tax document calculator",
        "invoice laptop freelance", "budget spreadsheet",
    ],
    "remote-work": [
        "remote work laptop", "digital nomad cafe",
        "work from home desk", "freelancer laptop coffee",
        "video call laptop", "coworking space modern",
        "laptop tropical location", "online meeting zoom",
        "programming code screen", "writing blog laptop",
        "home office minimal", "typing keyboard hands",
    ],
    "family-education": [
        "family moving abroad", "children school international",
        "kids playing outdoor", "family travel airport",
        "school classroom diverse", "children studying",
        "parent child reading", "family dinner table",
        "kids sports soccer", "international school building",
        "bilingual education", "family suitcase travel",
    ],
    "immigration-visa": [
        "passport visa stamp", "immigration airport",
        "moving boxes packing", "suitcase travel preparation",
        "document paperwork official", "embassy building",
        "checklist planning notebook", "new home keys",
        "airplane departure", "customs border control",
    ],
    "healthcare": [
        "hospital modern building", "doctor consultation",
        "health insurance card", "pharmacy medicine",
        "medical checkup", "stethoscope doctor",
        "family health care", "dental clinic",
    ],
    "real-estate": [
        "house modern tropical", "apartment building exterior",
        "real estate agent", "house interior living room",
        "swimming pool house", "gated community",
        "house for sale sign", "garden tropical house",
    ],
    "transportation": [
        "bus public transport", "taxi ride city",
        "car driving highway", "motorcycle city traffic",
        "uber ride sharing", "gas station",
        "road trip south america", "city traffic latin america",
    ],
    "internet-vpn": [
        "wifi internet connection", "vpn security shield",
        "fiber optic cable", "smartphone data mobile",
        "cybersecurity lock", "router modem internet",
        "streaming video laptop", "online privacy",
    ],
    "shopping-supermarket": [
        "supermarket aisle", "grocery shopping cart",
        "fresh vegetables market", "meat section supermarket",
        "shopping bag groceries", "local market produce",
        "price tag comparison", "japanese food ingredients",
    ],
    "blog-writing": [
        "blog writing desk", "content creation laptop",
        "seo analytics screen", "wordpress dashboard",
        "social media marketing", "affiliate marketing",
        "youtube video editing", "podcast microphone",
    ],
    "lifestyle-general": [
        "sunrise landscape beautiful", "coffee morning routine",
        "nature green forest", "river peaceful",
        "garden flowers colorful", "blue sky clouds",
        "walking path nature", "hammock relaxation tropical",
        "sunset golden hour", "stars night sky",
    ],
    "mental-health": [
        "meditation peaceful", "homesick lonely",
        "community gathering friends", "happy family outdoor",
        "journaling notebook pen", "exercise yoga outdoor",
        "phone call family", "cultural exchange people",
    ],
    "language-learning": [
        "spanish language learning", "language textbook study",
        "online class laptop", "conversation practice people",
        "dictionary language", "flashcard study",
    ],
    "climate-weather": [
        "sunny weather tropical", "rainstorm tropical",
        "thermometer hot weather", "green nature after rain",
        "clear blue sky", "spring flowers bloom",
    ],
    "kids-activities": [
        "children soccer playing", "kids swimming pool",
        "children art class", "kids music piano",
        "children dance class", "kids martial arts",
    ],
}

# 1カテゴリあたりのダウンロード枚数
IMAGES_PER_KEYWORD = 3

def download_unsplash(query, save_dir, count=3):
    """Unsplash Source APIで画像をダウンロード"""
    save_dir.mkdir(parents=True, exist_ok=True)
    downloaded = 0

    for i in range(count):
        # Unsplash source URL（ランダム画像を返す）
        # sigパラメータを変えることで異なる画像を取得
        url = f"https://source.unsplash.com/1200x800/?{query.replace(' ', ',')}&sig={i}"

        try:
            response = requests.get(url, timeout=30, allow_redirects=True)
            if response.status_code == 200 and len(response.content) > 10000:
                # ファイル名: カテゴリ_キーワード_番号.jpg
                safe_name = query.replace(" ", "-").replace("/", "-")[:40]
                filename = f"{safe_name}_{i+1}.jpg"
                filepath = save_dir / filename

                if not filepath.exists():
                    with open(filepath, "wb") as f:
                        f.write(response.content)
                    downloaded += 1
                    print(f"  OK {filename} ({len(response.content)//1024}KB)")
                else:
                    print(f"  - {filename} (既存スキップ)")
            else:
                print(f"  FAIL {query} #{i+1} - status:{response.status_code} size:{len(response.content)}")
        except Exception as e:
            print(f"  FAIL {query} #{i+1} - エラー: {e}")

        # レート制限対策
        time.sleep(1.5)

    return downloaded


def main():
    print("=" * 60)
    print("フリー画像一括ダウンロード（Unsplash Source）")
    print(f"保存先: {BASE_DIR}")
    print(f"カテゴリ数: {len(CATEGORIES)}")
    total_keywords = sum(len(kws) for kws in CATEGORIES.values())
    print(f"総キーワード数: {total_keywords}")
    print(f"予想ダウンロード数: 最大 {total_keywords * IMAGES_PER_KEYWORD} 枚")
    print("=" * 60)

    total_downloaded = 0
    log = {}

    for category, keywords in CATEGORIES.items():
        print(f"\n[{category}] ({len(keywords)} keywords)")
        category_dir = BASE_DIR / category
        category_count = 0

        for keyword in keywords:
            print(f"  > {keyword}")
            count = download_unsplash(keyword, category_dir, IMAGES_PER_KEYWORD)
            category_count += count
            total_downloaded += count

        log[category] = category_count
        print(f"  -> {category}: {category_count} images done")

    # ダウンロードログを保存
    log_data = {
        "downloaded_at": datetime.now().isoformat(),
        "source": "Unsplash (source.unsplash.com)",
        "license": "Unsplash License - 商用利用可・クレジット推奨",
        "total_images": total_downloaded,
        "categories": log,
    }
    log_path = BASE_DIR / "download-log.json"
    with open(log_path, "w", encoding="utf-8") as f:
        json.dump(log_data, f, ensure_ascii=False, indent=2)

    print(f"\n{'=' * 60}")
    print(f"DONE! Total: {total_downloaded} images downloaded")
    print(f"Log: {log_path}")
    print(f"{'=' * 60}")


if __name__ == "__main__":
    main()
