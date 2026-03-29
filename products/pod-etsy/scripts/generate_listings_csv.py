#!/usr/bin/env python3
"""
AsuInk POD Etsy Listings CSV Generator
50デザイン × 3商品 = 150リスティングのCSVを生成

Usage:
    python generate_listings_csv.py
    python generate_listings_csv.py --output custom_output.csv
"""

import csv
import json
import argparse
from pathlib import Path

# ============================================================
# 50デザイン定義（5ニッチ × 10デザイン）
# ============================================================
DESIGNS = [
    # Niche 1: 日本禅・ミニマリスト
    {"id": "D01", "niche": "Japanese Zen", "name": "Wabi-Sabi Circle",
     "keywords": ["wabi sabi", "zen", "enso circle", "japanese minimalist", "mindfulness"],
     "mood": "serene, philosophical"},
    {"id": "D02", "niche": "Japanese Zen", "name": "Mount Fuji Line Art",
     "keywords": ["mount fuji", "japan", "minimalist", "find peace", "japanese art"],
     "mood": "peaceful, majestic"},
    {"id": "D03", "niche": "Japanese Zen", "name": "Ikigai Diagram",
     "keywords": ["ikigai", "purpose", "life meaning", "japanese philosophy", "wellness"],
     "mood": "purposeful, motivational"},
    {"id": "D04", "niche": "Japanese Zen", "name": "Zen Garden",
     "keywords": ["zen garden", "be still", "meditation", "japanese garden", "calm"],
     "mood": "tranquil, minimalist"},
    {"id": "D05", "niche": "Japanese Zen", "name": "Cherry Blossom Branch",
     "keywords": ["cherry blossom", "sakura", "mono no aware", "japanese flower", "spring"],
     "mood": "delicate, fleeting"},
    {"id": "D06", "niche": "Japanese Zen", "name": "Origami Crane",
     "keywords": ["origami crane", "1000 cranes", "japanese culture", "geometric", "gold"],
     "mood": "elegant, hopeful"},
    {"id": "D07", "niche": "Japanese Zen", "name": "Yin-Yang Minimalist",
     "keywords": ["yin yang", "balance", "minimalist", "zen symbol", "harmony"],
     "mood": "balanced, pure"},
    {"id": "D08", "niche": "Japanese Zen", "name": "Torii Gate Sunset",
     "keywords": ["torii gate", "japan", "sunset", "spiritual", "journey within"],
     "mood": "spiritual, beautiful"},
    {"id": "D09", "niche": "Japanese Zen", "name": "Kokoro Kanji",
     "keywords": ["kokoro", "kanji", "heart mind", "japanese calligraphy", "soul"],
     "mood": "deep, introspective"},
    {"id": "D10", "niche": "Japanese Zen", "name": "Forest Bathing",
     "keywords": ["shinrin yoku", "forest bathing", "bamboo", "nature therapy", "japanese"],
     "mood": "refreshing, healing"},

    # Niche 2: 南米バイブス
    {"id": "D11", "niche": "South America", "name": "Paraguay Map Art",
     "keywords": ["paraguay", "south america", "map art", "guarani", "travel"],
     "mood": "proud, cultural"},
    {"id": "D12", "niche": "South America", "name": "Mate Culture",
     "keywords": ["mate", "yerba mate", "south america", "paraguay", "latin culture"],
     "mood": "warm, social"},
    {"id": "D13", "niche": "South America", "name": "Iguazu Falls",
     "keywords": ["iguazu falls", "south america wonder", "waterfall", "travel", "nature"],
     "mood": "powerful, awe-inspiring"},
    {"id": "D14", "niche": "South America", "name": "Condor Silhouette",
     "keywords": ["condor", "andes", "libre", "freedom", "south america"],
     "mood": "free, soaring"},
    {"id": "D15", "niche": "South America", "name": "Guarani Pattern",
     "keywords": ["guarani pattern", "indigenous art", "south america", "tribal", "ethnic"],
     "mood": "rich, cultural"},
    {"id": "D16", "niche": "South America", "name": "Asuncion Skyline",
     "keywords": ["asuncion", "paraguay city", "skyline", "travel", "south america"],
     "mood": "urban, proud"},
    {"id": "D17", "niche": "South America", "name": "Expat Life",
     "keywords": ["expat life", "citizen of world", "travel", "nomad", "globe"],
     "mood": "adventurous, free"},
    {"id": "D18", "niche": "South America", "name": "Tropical Parrot",
     "keywords": ["tropical parrot", "macaw", "tropical", "colorful", "rainforest"],
     "mood": "vibrant, lively"},
    {"id": "D19", "niche": "South America", "name": "Dulce de Leche",
     "keywords": ["dulce de leche", "caramel", "latin food", "sweet", "foodie"],
     "mood": "sweet, playful"},
    {"id": "D20", "niche": "South America", "name": "South American Sunset",
     "keywords": ["pampas sunset", "south america", "travel poster", "retro", "adventure"],
     "mood": "nostalgic, wanderlust"},

    # Niche 3: 日西バイリンガル
    {"id": "D21", "niche": "Bilingual JP-ES", "name": "Gracias Arigatou",
     "keywords": ["gracias", "arigatou", "bilingual", "japanese spanish", "thank you"],
     "mood": "grateful, multicultural"},
    {"id": "D22", "niche": "Bilingual JP-ES", "name": "Amor Ai",
     "keywords": ["amor", "ai love", "bilingual", "japanese spanish", "love"],
     "mood": "romantic, connecting"},
    {"id": "D23", "niche": "Bilingual JP-ES", "name": "Language Bridge",
     "keywords": ["language learning", "bilingual", "spanish japanese", "words connect", "polyglot"],
     "mood": "connecting, cheerful"},
    {"id": "D24", "niche": "Bilingual JP-ES", "name": "Wasabi Chimichurri",
     "keywords": ["wasabi chimichurri", "fusion food", "bilingual", "japanese latin", "foodie"],
     "mood": "funny, foodie"},
    {"id": "D25", "niche": "Bilingual JP-ES", "name": "Sushi Taco Fusion",
     "keywords": ["sushi taco", "fusion", "bilingual", "best of both worlds", "funny food"],
     "mood": "fun, fusion"},
    {"id": "D26", "niche": "Bilingual JP-ES", "name": "Ninja Gaucho",
     "keywords": ["ninja gaucho", "east meets west", "bilingual", "japan latin", "humor"],
     "mood": "witty, cultural"},
    {"id": "D27", "niche": "Bilingual JP-ES", "name": "Ramen Asado",
     "keywords": ["ramen asado", "no borders", "bilingual", "food fusion", "international"],
     "mood": "warm, inclusive"},
    {"id": "D28", "niche": "Bilingual JP-ES", "name": "Sakura Jacaranda",
     "keywords": ["sakura jacaranda", "flowers", "japan latin america", "nature", "bilingual art"],
     "mood": "beautiful, symbolic"},
    {"id": "D29", "niche": "Bilingual JP-ES", "name": "Konnichiwa Hola",
     "keywords": ["konnichiwa hola", "greeting", "bilingual", "japanese spanish", "multicultural"],
     "mood": "friendly, bright"},
    {"id": "D30", "niche": "Bilingual JP-ES", "name": "Shogun Conquistador",
     "keywords": ["shogun conquistador", "history", "east west", "bilingual", "cultural art"],
     "mood": "historical, epic"},

    # Niche 4: デジタルノマド
    {"id": "D31", "niche": "Digital Nomad", "name": "Laptop Beach",
     "keywords": ["digital nomad", "office optional", "remote work", "beach work", "freedom"],
     "mood": "aspirational, free"},
    {"id": "D32", "niche": "Digital Nomad", "name": "Time Zone Map",
     "keywords": ["time zones", "remote work", "world map", "nomad life", "travel worker"],
     "mood": "global, clever"},
    {"id": "D33", "niche": "Digital Nomad", "name": "Wifi Coffee Repeat",
     "keywords": ["wifi coffee repeat", "digital nomad", "remote work", "coffee lover", "freelancer"],
     "mood": "relatable, fun"},
    {"id": "D34", "niche": "Digital Nomad", "name": "Nomad Checklist",
     "keywords": ["nomad essentials", "checklist", "digital nomad", "travel", "freelance life"],
     "mood": "practical, cute"},
    {"id": "D35", "niche": "Digital Nomad", "name": "Work from Paradise",
     "keywords": ["work from paradise", "hammock", "tropical work", "remote", "nomad dream"],
     "mood": "dreamy, aspirational"},
    {"id": "D36", "niche": "Digital Nomad", "name": "Freedom vs Security",
     "keywords": ["choose your hard", "freedom", "digital nomad", "life choice", "motivational"],
     "mood": "thought-provoking, bold"},
    {"id": "D37", "niche": "Digital Nomad", "name": "Coworking Globe",
     "keywords": ["coworking", "no walls", "globe", "remote work", "digital nomad"],
     "mood": "global, upbeat"},
    {"id": "D38", "niche": "Digital Nomad", "name": "Startup Nomad",
     "keywords": ["startup", "building everywhere", "entrepreneur", "nomad", "tech founder"],
     "mood": "ambitious, modern"},
    {"id": "D39", "niche": "Digital Nomad", "name": "Remote Work Mantra",
     "keywords": ["work hard travel far", "mantra", "digital nomad", "motivational", "remote"],
     "mood": "inspiring, typographic"},
    {"id": "D40", "niche": "Digital Nomad", "name": "Around World 80 Coffees",
     "keywords": ["80 coffees", "coffee travel", "world map", "travel lover", "coffee art"],
     "mood": "quirky, coffee lover"},

    # Niche 5: 名言哲学
    {"id": "D41", "niche": "Quotes & Philosophy", "name": "Marcus Aurelius Stoic",
     "keywords": ["marcus aurelius", "stoic quote", "stoicism", "philosophy", "mindset"],
     "mood": "powerful, wise"},
    {"id": "D42", "niche": "Quotes & Philosophy", "name": "Wabi-Sabi Philosophy",
     "keywords": ["wabi sabi quote", "imperfection", "beauty", "japanese philosophy", "mindfulness"],
     "mood": "gentle, wise"},
    {"id": "D43", "niche": "Quotes & Philosophy", "name": "Kaizen Mindset",
     "keywords": ["kaizen", "small improvements", "growth mindset", "japanese", "self improvement"],
     "mood": "progressive, motivating"},
    {"id": "D44", "niche": "Quotes & Philosophy", "name": "Carpe Diem",
     "keywords": ["carpe diem", "seize the day", "motivation", "latin quote", "bold typography"],
     "mood": "bold, urgent"},
    {"id": "D45", "niche": "Quotes & Philosophy", "name": "Ikigai Quote",
     "keywords": ["ikigai", "purpose", "life meaning", "japanese philosophy", "diagram"],
     "mood": "meaningful, clear"},
    {"id": "D46", "niche": "Quotes & Philosophy", "name": "Obstacle is the Way",
     "keywords": ["obstacle is the way", "stoicism", "ryan holiday", "growth", "resilience"],
     "mood": "stoic, strong"},
    {"id": "D47", "niche": "Quotes & Philosophy", "name": "Present Moment",
     "keywords": ["present moment", "thich nhat hanh", "mindfulness", "buddhist", "zen quote"],
     "mood": "calm, present"},
    {"id": "D48", "niche": "Quotes & Philosophy", "name": "Fall Seven Stand Eight",
     "keywords": ["nana korobi ya oki", "japanese proverb", "resilience", "never give up", "perseverance"],
     "mood": "resilient, powerful"},
    {"id": "D49", "niche": "Quotes & Philosophy", "name": "Growth Mindset Tree",
     "keywords": ["grow through it", "growth mindset", "tree art", "motivation", "personal growth"],
     "mood": "growing, hopeful"},
    {"id": "D50", "niche": "Quotes & Philosophy", "name": "Be Here Now",
     "keywords": ["be here now", "minimalist", "zen quote", "mindfulness", "present"],
     "mood": "ultra-minimal, profound"},
]

# ============================================================
# 商品タイプ定義
# ============================================================
PRODUCT_TYPES = {
    "tshirt": {
        "label": "Unisex T-Shirt",
        "price": 24.99,
        "suffix": "T-Shirt | Unisex Cotton Tee",
        "category": "Clothing > Shirts & Tops > T-Shirts",
        "tags_extra": ["unisex tshirt", "cotton tee", "graphic tee", "gift tshirt"],
        "description_suffix": "\n\n✦ PRODUCT DETAILS:\n• Unisex fitted tee\n• 100% combed ringspun cotton\n• Shoulder-to-shoulder taping, side-seamed\n• Sizes: XS–3XL\n• Machine wash cold, tumble dry low",
    },
    "mug": {
        "label": "Coffee Mug",
        "price": 17.99,
        "suffix": "Coffee Mug | 11oz Ceramic Cup",
        "category": "Home & Living > Kitchen & Dining > Mugs",
        "tags_extra": ["coffee mug", "ceramic mug", "tea mug", "gift mug"],
        "description_suffix": "\n\n✦ PRODUCT DETAILS:\n• 11 fl oz ceramic mug\n• Lead and BPA-free\n• Dishwasher and microwave safe\n• Available in white or black",
    },
    "poster": {
        "label": "Art Print",
        "price": 19.99,
        "suffix": "Art Print | Wall Decor Poster",
        "category": "Art & Collectibles > Prints > Digital Prints",
        "tags_extra": ["wall art", "art print", "home decor", "poster print"],
        "description_suffix": "\n\n✦ PRODUCT DETAILS:\n• Premium matte poster paper\n• Available: 8×10, 11×14, 16×20, 18×24, 24×36 inches\n• Fade-resistant print\n• Ships in protective tube\n• Unframed",
    },
}

SHIPPING_NOTICE = "\n\n✦ SHIPPING:\nAll items are printed on demand. Please allow 3-7 business days for production + shipping time."
RETURN_POLICY = "\n\nAll sales are final for custom print-on-demand items unless damaged/defective."


def build_title(design: dict, product_key: str) -> str:
    product = PRODUCT_TYPES[product_key]
    base = design["name"]
    niche_label = design["niche"]
    suffix = product["suffix"]
    # Etsy title max 140 chars
    title = f"{base} {suffix} | {niche_label} Gift"
    return title[:140]


def build_tags(design: dict, product_key: str) -> str:
    product = PRODUCT_TYPES[product_key]
    base_tags = design["keywords"][:9]  # max 13 total
    extra_tags = product["tags_extra"][:4]
    all_tags = base_tags + extra_tags
    # Etsy: max 13 tags, each max 20 chars
    valid_tags = []
    for tag in all_tags:
        tag = tag[:20]
        if tag not in valid_tags:
            valid_tags.append(tag)
    return ", ".join(valid_tags[:13])


def build_description(design: dict, product_key: str) -> str:
    product = PRODUCT_TYPES[product_key]
    desc = f"✦ {design['name'].upper()}\n\n"
    desc += f"A {design['mood']} design from the AsuInk {design['niche']} collection.\n\n"
    desc += "✦ PERFECT FOR:\n"
    keywords = design["keywords"][:5]
    for kw in keywords:
        desc += f"• Fans of {kw}\n"
    desc += product["description_suffix"]
    desc += SHIPPING_NOTICE
    desc += RETURN_POLICY
    return desc


def generate_csv(output_path: Path):
    fieldnames = [
        "TITLE", "DESCRIPTION", "PRICE", "QUANTITY", "TAGS",
        "MATERIALS", "WHO_MADE", "IS_SUPPLY", "WHEN_MADE",
        "CATEGORY", "SHIPPING_PROFILE", "SECTION",
        "VARIATION_1_NAME", "VARIATION_1_VALUES",
        "SKU", "DESIGN_ID", "PRODUCT_TYPE", "NICHE"
    ]

    rows = []
    listing_num = 1

    for design in DESIGNS:
        for product_key, product in PRODUCT_TYPES.items():
            title = build_title(design, product_key)
            tags = build_tags(design, product_key)
            description = build_description(design, product_key)

            # バリエーション設定
            if product_key == "tshirt":
                var1_name = "Size"
                var1_values = "XS, S, M, L, XL, 2XL, 3XL"
            elif product_key == "mug":
                var1_name = "Color"
                var1_values = "White, Black"
            else:  # poster
                var1_name = "Size"
                var1_values = "8x10, 11x14, 16x20, 18x24, 24x36"

            row = {
                "TITLE": title,
                "DESCRIPTION": description,
                "PRICE": product["price"],
                "QUANTITY": 999,
                "TAGS": tags,
                "MATERIALS": "Cotton, Ceramic, Poster Paper",
                "WHO_MADE": "i_did",
                "IS_SUPPLY": "FALSE",
                "WHEN_MADE": "made_to_order",
                "CATEGORY": product["category"],
                "SHIPPING_PROFILE": "Standard Shipping",
                "SECTION": f"{design['niche']} Collection",
                "VARIATION_1_NAME": var1_name,
                "VARIATION_1_VALUES": var1_values,
                "SKU": f"ASUINK-{design['id']}-{product_key[:2].upper()}",
                "DESIGN_ID": design["id"],
                "PRODUCT_TYPE": product["label"],
                "NICHE": design["niche"],
            }
            rows.append(row)
            listing_num += 1

    with open(output_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

    print(f"CSVを生成しました: {output_path}")
    print(f"総リスティング数: {len(rows)}")
    return rows


def main():
    parser = argparse.ArgumentParser(description="AsuInk Etsy Listings CSV Generator")
    parser.add_argument("--output", default="../csv-upload/etsy-listings-150.csv",
                        help="出力CSVファイルパス")
    args = parser.parse_args()

    output_path = Path(__file__).parent / args.output
    output_path.parent.mkdir(parents=True, exist_ok=True)
    rows = generate_csv(output_path)

    # サマリー表示
    from collections import Counter
    niche_counts = Counter(r["NICHE"] for r in rows)
    product_counts = Counter(r["PRODUCT_TYPE"] for r in rows)
    print("\n--- ニッチ別内訳 ---")
    for niche, count in niche_counts.items():
        print(f"  {niche}: {count}件")
    print("\n--- 商品タイプ別内訳 ---")
    for ptype, count in product_counts.items():
        print(f"  {ptype}: {count}件")


if __name__ == "__main__":
    main()
