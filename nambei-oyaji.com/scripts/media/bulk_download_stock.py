"""
Pixabay APIから大量のストック画像を一括ダウンロードするスクリプト
既存画像と重複しないように、Pixabay IDベースで管理
"""

import json
import os
import sys
import time
import requests
from pathlib import Path
from datetime import datetime

BLOG_DIR = Path(__file__).resolve().parent.parent.parent
STOCK_DIR = BLOG_DIR / "images" / "stock"
SECRETS_PATH = BLOG_DIR / "config" / "secrets.json"
LOG_PATH = STOCK_DIR / "download-log.json"

# Pixabay API制限: 100リクエスト/分
RATE_LIMIT_DELAY = 0.7  # 秒

# ダウンロード対象: カテゴリ → 検索クエリリスト
# 既存カテゴリの補強 + 新カテゴリの追加
DOWNLOAD_PLAN = {
    # === パラグアイ生活（メイン柱）===
    "paraguay-life": [
        "Paraguay Asuncion cityscape",
        "Paraguay flag country",
        "south america colonial town",
        "south america colorful houses",
        "south america rural countryside",
        "tropical garden hammock relax",
        "mate tea terere drink",
        "south america church cathedral",
        "south america plaza fountain",
        "guarani indigenous craft",
        "south america sunset river",
        "red earth road south america",
        "lapacho tree pink flowers",
        "south america farm ranch",
        "outdoor patio tropical house",
    ],

    # === 食文化 ===
    "food-culture": [
        "japanese food sushi restaurant",
        "japanese ramen noodle bowl",
        "japanese bento box lunch",
        "asian grocery store",
        "soy sauce japanese ingredients",
        "chipa bread cheese",
        "mandioca cassava dish",
        "south america steak restaurant",
        "outdoor dining tropical",
        "cooking kitchen home meal",
        "farmer market south america",
    ],

    # === 移住・ビザ ===
    "immigration-visa": [
        "passport travel document",
        "airport terminal departure",
        "moving boxes new home",
        "family moving abroad",
        "visa application form",
        "embassy government building",
        "luggage airport travel",
        "customs immigration officer",
        "documents paperwork official",
        "new life adventure road",
        "world map travel planning",
    ],

    # === 金融・お金 ===
    "finance-money": [
        "money transfer smartphone app",
        "wise revolut digital banking",
        "credit card payment shopping",
        "insurance policy document",
        "pension retirement savings",
        "tax form filing papers",
        "budget planning notebook",
        "cryptocurrency bitcoin digital",
        "japanese yen currency",
        "guarani currency money",
        "piggy bank saving money",
        "financial planning calculator",
        "bank counter service",
    ],

    # === リモートワーク ===
    "remote-work": [
        "digital nomad cafe laptop",
        "home office tropical window",
        "video call zoom meeting",
        "freelancer working beach",
        "coworking space modern",
        "time zone world clock",
        "online meeting headphones",
        "writing content creation desk",
        "graphic design computer monitor",
        "virtual assistant work",
        "data entry computer typing",
    ],

    # === 家族・教育 ===
    "family-education": [
        "international school classroom",
        "bilingual education children",
        "school uniform students",
        "family airport travel children",
        "children painting art class",
        "family dinner table happy",
        "school bus children morning",
        "graduation ceremony students",
        "homework study children desk",
        "school playground children playing",
        "parent teacher meeting",
    ],

    # === 子供の習い事・スポーツ ===
    "kids-activities": [
        "children swimming pool lesson",
        "kids martial arts karate",
        "children ballet dance class",
        "kids piano music lesson",
        "children tennis court",
        "kids basketball team",
        "children gymnastics",
        "kids painting art creative",
        "children playing park outdoor",
        "kids birthday party celebration",
        "children camping outdoor nature",
    ],

    # === 医療・健康 ===
    "healthcare": [
        "pharmacy medicine pills",
        "hospital room modern",
        "dental clinic checkup",
        "pediatrician children doctor",
        "health insurance card",
        "ambulance emergency",
        "vaccination injection nurse",
        "medical clinic waiting room",
        "tropical disease prevention",
    ],

    # === 不動産・住居 ===
    "real-estate": [
        "tropical house garden pool",
        "apartment balcony city view",
        "modern house interior living room",
        "gated community entrance",
        "house keys real estate agent",
        "construction new house building",
        "neighborhood residential street",
        "rental apartment interior modern",
        "house plan blueprint architecture",
        "swimming pool backyard tropical",
    ],

    # === 交通 ===
    "transportation": [
        "taxi ride city urban",
        "motorcycle scooter street",
        "car driving highway road",
        "uber ride sharing app",
        "bicycle city commute",
        "gas station fuel car",
        "parking lot shopping center",
        "bus stop waiting people",
        "road intersection traffic light",
    ],

    # === インターネット・VPN ===
    "internet-vpn": [
        "smartphone mobile internet 5g",
        "sim card mobile phone",
        "wifi signal connection",
        "streaming video entertainment",
        "vpn security privacy shield",
        "internet speed test",
        "satellite dish antenna rural",
    ],

    # === ブログ・コンテンツ作成 ===
    "blog-writing": [
        "wordpress website design",
        "social media marketing strategy",
        "affiliate marketing income",
        "youtube video camera recording",
        "podcast recording studio microphone",
        "instagram post smartphone",
        "email marketing newsletter",
        "seo search engine optimization",
        "google analytics dashboard screen",
        "ebook digital product creation",
    ],

    # === 買い物・スーパー ===
    "shopping-supermarket": [
        "supermarket checkout cashier",
        "fresh fruits vegetables display",
        "meat butcher shop display",
        "bakery bread pastry shop",
        "shopping mall entrance",
        "online shopping package delivery",
        "marketplace vendor stall",
        "organic food natural products",
    ],

    # === 言語学習 ===
    "language-learning": [
        "spanish language textbook",
        "language exchange conversation",
        "online tutoring video call",
        "flashcards study language",
        "spanish flag spain culture",
        "translator app smartphone",
        "classroom whiteboard teacher",
    ],

    # === メンタルヘルス・コミュニティ ===
    "mental-health": [
        "meditation mindfulness peace",
        "journal writing therapy",
        "community gathering people",
        "video call family friends",
        "loneliness alone window",
        "support group people talking",
        "exercise yoga outdoor nature",
        "volunteer community service",
    ],

    # === 気候・天気 ===
    "climate-weather": [
        "sunny weather blue sky",
        "tropical storm rain thunder",
        "hot summer temperature thermometer",
        "spring flowers blooming garden",
        "winter cold frost morning",
        "rainbow after rain nature",
        "drought dry land heat",
        "clear night stars sky",
    ],

    # === ライフスタイル全般 ===
    "lifestyle-general": [
        "sunrise morning coffee routine",
        "barbecue friends outdoor party",
        "festival celebration music dance",
        "christmas celebration south america",
        "new year fireworks celebration",
        "carnival costume colorful parade",
        "church sunday service worship",
        "street art graffiti urban",
        "pet dog family park",
        "garden plants tropical flowers",
    ],

    # === 新カテゴリ: 起業・ビジネス ===
    "business-startup": [
        "startup business meeting office",
        "entrepreneur laptop working",
        "business plan strategy whiteboard",
        "small business store shop",
        "handshake business deal agreement",
        "company registration documents",
        "accounting bookkeeping ledger",
        "ecommerce online store website",
        "import export cargo shipping",
        "presentation business slide",
    ],

    # === 新カテゴリ: ライフライン（電気・水道・ガス） ===
    "utilities-lifeline": [
        "electricity power lines tower",
        "water tap faucet kitchen",
        "gas stove cooking flame",
        "solar panel energy renewable",
        "water tank roof building",
        "electric meter reading",
        "plumber fixing pipes",
        "generator backup power",
        "air conditioning unit tropical",
        "water filter purification",
    ],

    # === 新カテゴリ: 祝日・文化・イベント ===
    "culture-events": [
        "south america festival parade",
        "traditional dance folklore",
        "national holiday celebration flag",
        "christmas lights decoration tropical",
        "easter celebration tradition",
        "cultural event music performance",
        "fireworks new year celebration",
        "carnival dancers colorful costumes",
        "religious procession catholic",
        "craft market artisan handmade",
    ],

    # === 新カテゴリ: 安全・治安 ===
    "safety-security": [
        "security camera surveillance cctv",
        "safe neighborhood residential",
        "police patrol car city",
        "home security system alarm",
        "street lighting night safety",
        "padlock door lock security",
        "safety first warning sign",
        "guard gate entrance security",
    ],
}


def load_existing_ids():
    """既にダウンロード済みのPixabay IDを取得"""
    existing = set()
    for category_dir in STOCK_DIR.iterdir():
        if not category_dir.is_dir():
            continue
        for img_file in category_dir.iterdir():
            if img_file.suffix in (".jpg", ".png"):
                # ファイル名末尾の _PIXABAYID.jpg からID抽出
                stem = img_file.stem
                parts = stem.rsplit("_", 1)
                if len(parts) == 2 and parts[1].isdigit():
                    existing.add(int(parts[1]))
    return existing


def download_images(api_key):
    existing_ids = load_existing_ids()
    print(f"既存Pixabay ID数: {len(existing_ids)}")

    stats = {}
    total_new = 0
    total_skipped = 0
    total_errors = 0
    request_count = 0

    for category, queries in DOWNLOAD_PLAN.items():
        category_dir = STOCK_DIR / category
        category_dir.mkdir(parents=True, exist_ok=True)
        cat_new = 0

        print(f"\n{'='*50}")
        print(f"カテゴリ: {category} ({len(queries)} クエリ)")
        print(f"{'='*50}")

        for query in queries:
            # レート制限
            if request_count > 0 and request_count % 90 == 0:
                print("  [PAUSE] レート制限回避のため10秒待機...")
                time.sleep(10)

            time.sleep(RATE_LIMIT_DELAY)
            request_count += 1

            params = {
                "key": api_key,
                "q": query,
                "image_type": "photo",
                "orientation": "horizontal",
                "min_width": 1200,
                "min_height": 630,
                "safesearch": "true",
                "per_page": 10,
                "lang": "en",
                "order": "popular"
            }

            try:
                resp = requests.get("https://pixabay.com/api/", params=params, timeout=15)
                if resp.status_code != 200:
                    print(f"  [ERROR] API {resp.status_code}: {query}")
                    total_errors += 1
                    continue

                data = resp.json()
                hits = data.get("hits", [])

                if not hits:
                    print(f"  [EMPTY] {query}")
                    continue

                downloaded_this_query = 0
                for hit in hits:
                    pixabay_id = hit["id"]

                    if pixabay_id in existing_ids:
                        total_skipped += 1
                        continue

                    # ファイル名生成: クエリのキーワードからプレフィックス
                    prefix = query.replace(" ", "-").lower()[:40]
                    filename = f"{prefix}_{pixabay_id}.jpg"
                    filepath = category_dir / filename

                    # ダウンロード
                    img_url = hit.get("largeImageURL", hit.get("webformatURL"))
                    try:
                        img_resp = requests.get(img_url, timeout=30)
                        if img_resp.status_code == 200:
                            with open(filepath, "wb") as f:
                                f.write(img_resp.content)
                            existing_ids.add(pixabay_id)
                            cat_new += 1
                            total_new += 1
                            downloaded_this_query += 1
                        else:
                            total_errors += 1
                    except Exception as e:
                        total_errors += 1

                    time.sleep(0.3)  # 画像DL間の待機

                if downloaded_this_query > 0:
                    print(f"  [OK] {query}: {downloaded_this_query}枚")
                else:
                    print(f"  [SKIP] {query}: 全て既存")

            except Exception as e:
                print(f"  [ERROR] {query}: {e}")
                total_errors += 1

        stats[category] = cat_new
        print(f"  → {category}: 新規{cat_new}枚")

    return stats, total_new, total_skipped, total_errors


def update_log(stats, total_new):
    """ダウンロードログを更新"""
    log = {}
    if LOG_PATH.exists():
        with open(LOG_PATH, "r", encoding="utf-8") as f:
            log = json.load(f)

    # カテゴリ別の合計を再集計
    category_totals = {}
    for cat_dir in STOCK_DIR.iterdir():
        if cat_dir.is_dir():
            count = sum(1 for f in cat_dir.iterdir() if f.suffix in (".jpg", ".png"))
            if count > 0:
                category_totals[cat_dir.name] = count

    log["downloaded_at"] = datetime.now().isoformat()
    log["source"] = "Pixabay (pixabay.com)"
    log["license"] = "Pixabay License - free commercial use, no attribution required"
    log["total_images"] = sum(category_totals.values())
    log["categories"] = dict(sorted(category_totals.items(), key=lambda x: -x[1]))
    log["last_batch"] = {
        "date": datetime.now().strftime("%Y-%m-%d"),
        "new_images": total_new,
        "additions_by_category": {k: v for k, v in stats.items() if v > 0}
    }

    with open(LOG_PATH, "w", encoding="utf-8") as f:
        json.dump(log, f, ensure_ascii=False, indent=2)


def main():
    with open(SECRETS_PATH, "r", encoding="utf-8") as f:
        secrets = json.load(f)

    api_key = secrets.get("pixabay", {}).get("api_key", "")
    if not api_key:
        print("ERROR: Pixabay API key not found")
        return 1

    total_queries = sum(len(q) for q in DOWNLOAD_PLAN.values())
    print(f"ダウンロード計画: {len(DOWNLOAD_PLAN)}カテゴリ, {total_queries}クエリ")
    print(f"最大新規画像数: ~{total_queries * 10}枚\n")

    stats, total_new, total_skipped, total_errors = download_images(api_key)

    update_log(stats, total_new)

    print(f"\n{'='*50}")
    print(f"完了!")
    print(f"{'='*50}")
    print(f"  新規ダウンロード: {total_new}枚")
    print(f"  スキップ（既存）: {total_skipped}枚")
    print(f"  エラー: {total_errors}枚")

    if stats:
        print(f"\n[カテゴリ別 新規]")
        for cat, count in sorted(stats.items(), key=lambda x: -x[1]):
            if count > 0:
                print(f"  {cat}: +{count}")

    return 0


if __name__ == "__main__":
    sys.exit(main())
