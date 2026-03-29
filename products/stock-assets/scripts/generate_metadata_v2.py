"""
generate_metadata_v2.py
-----------------------
914枚全画像のメタデータを生成。
- prompts_expanded.json (864件) を優先使用し、不足分はファイル名から推定
- Adobe Stock / Freepik / Shutterstock 対応 CSV を出力
"""
import csv
import json
import os
import re
from typing import Any

BASE_DIR = os.path.dirname(os.path.dirname(__file__))
IMAGE_DIR = os.path.join(BASE_DIR, "output", "images")
METADATA_DIR = os.path.join(BASE_DIR, "output", "metadata")
PROMPTS_FILE = os.path.join(METADATA_DIR, "prompts_expanded.json")

# ─── タグ辞書 ──────────────────────────────────────────────

BASE_TAGS = [
    "seamless pattern", "seamless", "pattern", "tileable", "repeating",
    "background", "textile", "fabric", "wallpaper", "wrapping paper",
    "surface design", "print", "decor", "decorative", "ornament",
    "digital paper", "scrapbooking",
]

CATEGORY_TAGS: dict[str, list[str]] = {
    "floral": [
        "floral", "flower", "flowers", "botanical", "bloom", "blossom",
        "spring", "nature", "garden", "petal", "feminine", "elegant",
    ],
    "botanical": [
        "botanical", "plant", "leaf", "leaves", "foliage", "green",
        "nature", "organic", "herb", "garden", "tropical", "jungle",
    ],
    "geometric": [
        "geometric", "geometry", "shape", "abstract", "modern", "minimal",
        "lines", "triangle", "circle", "polygon", "grid", "lattice",
    ],
    "abstract": [
        "abstract", "modern", "artistic", "creative", "digital art",
        "contemporary", "graphic", "design", "colorful",
    ],
    "nature": [
        "nature", "natural", "organic", "earth", "landscape", "outdoor",
        "environment", "eco", "green",
    ],
    "food": [
        "food", "kitchen", "cooking", "cuisine", "cafe", "restaurant",
        "ingredient", "recipe", "yummy", "delicious",
    ],
    "animal": [
        "animal", "wildlife", "cute", "adorable", "creature", "pet",
        "nature", "fauna",
    ],
    "cultural": [
        "cultural", "ethnic", "traditional", "folk", "world", "heritage",
        "handcraft", "artisan",
    ],
    "seasonal": [
        "seasonal", "holiday", "celebration", "festive", "occasion",
        "event", "special",
    ],
}

SUBCATEGORY_TAGS: dict[str, list[str]] = {
    "roses": ["rose", "peony", "romantic", "wedding", "bridal", "bouquet"],
    "wildflowers": ["wildflower", "daisy", "meadow", "cottage", "rustic"],
    "hibiscus": ["hibiscus", "tropical", "hawaiian", "exotic", "island"],
    "cherry blossom": ["cherry blossom", "sakura", "japanese", "zen", "spring"],
    "sunflower": ["sunflower", "sunny", "harvest", "golden", "yellow"],
    "lavender": ["lavender", "provence", "spa", "herbal", "purple"],
    "art deco": ["art deco", "deco", "1920s", "gatsby", "geometric", "gold", "luxury"],
    "moroccan tile": ["moroccan", "morocco", "arabesque", "islamic", "mandala", "boho"],
    "hexagonal": ["hexagon", "honeycomb", "hex", "beehive", "geometric"],
    "chevron": ["chevron", "zigzag", "arrow", "stripe", "diagonal"],
    "polka dot": ["polka dot", "dot", "circle", "spotted", "playful", "fun"],
    "plaid": ["plaid", "tartan", "checkered", "scottish", "preppy"],
    "tropical": ["tropical", "palm", "exotic", "summer", "beach", "island"],
    "succulents": ["succulent", "cactus", "desert", "boho", "plant"],
    "mushroom": ["mushroom", "forest", "fairy", "woodland", "fungi", "whimsical"],
    "ocean": ["ocean", "sea", "wave", "marine", "nautical", "underwater"],
    "christmas": ["christmas", "xmas", "holiday", "santa", "winter", "festive"],
    "halloween": ["halloween", "spooky", "ghost", "pumpkin", "scary", "october"],
    "bees": ["bee", "honey", "honeycomb", "bumblebee", "hive", "pollinator"],
    "butterflies": ["butterfly", "butterflies", "moth", "insect", "wings", "spring"],
    "cats": ["cat", "kitten", "feline", "cute", "pet", "meow"],
    "birds": ["bird", "avian", "feather", "tweet", "nature"],
    "coffee": ["coffee", "cafe", "latte", "espresso", "barista", "cup"],
    "fruits": ["fruit", "berry", "citrus", "tropical fruit", "fresh"],
    "vegetables": ["vegetable", "veggie", "farm", "garden", "healthy"],
    "japanese": ["japanese", "japan", "asian", "oriental", "zen"],
    "mexican": ["mexican", "mexico", "fiesta", "colorful", "latin"],
    "indian": ["indian", "india", "mandala", "henna", "paisley"],
    "back to school": ["school", "education", "student", "pencil", "notebook"],
    "spring": ["spring", "bloom", "fresh", "pastel", "renewal"],
    "summer": ["summer", "sunny", "beach", "vacation", "warm"],
    "autumn": ["autumn", "fall", "harvest", "cozy", "orange", "maple"],
    "winter": ["winter", "snow", "cold", "cozy", "ice", "frost"],
}

STYLE_TAGS: dict[str, list[str]] = {
    "flat vector": [
        "flat design", "vector", "vector art", "vector illustration",
        "flat style", "modern design", "graphic design", "clean lines",
        "minimalist", "digital art", "clipart", "simple",
    ],
    "watercolor": [
        "watercolor", "watercolour", "hand painted", "artistic",
        "soft", "gentle", "aquarelle", "painting", "brushstroke",
    ],
    "hand-drawn": [
        "hand drawn", "sketch", "line art", "ink", "doodle",
        "illustration", "drawing", "handmade", "organic", "freehand",
    ],
    "vintage": [
        "vintage", "retro", "classic", "antique", "old fashioned",
        "nostalgic", "traditional",
    ],
}

COLOR_TAGS: dict[str, list[str]] = {
    "pastel": ["pastel", "pastel colors", "soft colors", "light", "pale"],
    "navy": ["navy", "navy blue", "dark blue", "gold", "luxury", "premium"],
    "earth": ["earth tones", "terracotta", "sage", "natural colors", "muted"],
    "pink": ["pink", "blush", "rose pink", "soft pink", "feminine"],
    "blue": ["blue", "cornflower", "dusty blue", "cool tones"],
    "coral": ["coral", "warm", "sunset", "warm tones"],
    "mint": ["mint", "mint green", "fresh", "cool"],
    "gold": ["gold", "golden", "metallic", "luxury"],
    "purple": ["purple", "violet", "mauve", "plum"],
    "green": ["green", "sage", "olive", "natural"],
    "red": ["red", "crimson", "ruby", "bold"],
    "multicolor": ["colorful", "rainbow", "vibrant", "vivid", "multicolor"],
    "cool ocean": ["blue", "teal", "aqua", "ocean", "sea", "cool"],
    "warm autumn": ["orange", "brown", "red", "autumn", "warm"],
}

ADOBE_CATEGORIES = [
    "Backgrounds/Textures", "Abstract", "Patterns", "Nature",
    "Food and Drink", "Animals/Wildlife", "Arts/Entertainment",
    "Holidays/Celebrations",
]

SHUTTERSTOCK_CATEGORIES = {
    "floral": "Flowers",
    "botanical": "Plants",
    "geometric": "Geometric",
    "abstract": "Abstract",
    "nature": "Nature",
    "food": "Food and Beverage",
    "animal": "Animals",
    "cultural": "Arts and Crafts",
    "seasonal": "Holidays",
}


# ─── ヘルパー関数 ─────────────────────────────────────────

def detect_category(data: dict[str, Any]) -> str:
    return data.get("category", "floral")


def detect_subcategory(data: dict[str, Any]) -> str:
    sub = data.get("subcategory", "")
    if not sub:
        # ファイル名やプロンプトから推定
        prompt = data.get("prompt", "").lower()
        for key in SUBCATEGORY_TAGS:
            if key in prompt:
                return key
    return sub.lower()


def detect_style(data: dict[str, Any]) -> str:
    style = data.get("style", "").lower()
    for key in STYLE_TAGS:
        if key in style:
            return key
    title = data.get("title", "").lower()
    for key in STYLE_TAGS:
        if key in title:
            return key
    return "flat vector"


def detect_colors(data: dict[str, Any]) -> list[str]:
    scheme = data.get("color_scheme", "").lower()
    prompt = data.get("prompt", "").lower()
    matched = []
    text = scheme + " " + prompt
    for key in COLOR_TAGS:
        if key in text:
            matched.append(key)
    return matched if matched else ["pastel"]


def build_tags(category: str, subcategory: str, style: str, colors: list[str], max_tags: int = 49) -> list[str]:
    tags: list[str] = list(BASE_TAGS)
    tags.extend(CATEGORY_TAGS.get(category, []))
    if subcategory:
        tags.extend(SUBCATEGORY_TAGS.get(subcategory, []))
    tags.extend(STYLE_TAGS.get(style, []))
    for c in colors:
        tags.extend(COLOR_TAGS.get(c, []))

    seen: set[str] = set()
    unique: list[str] = []
    for t in tags:
        tl = t.lower()
        if tl not in seen:
            seen.add(tl)
            unique.append(t)
    return unique[:max_tags]


def build_description(category: str, subcategory: str, style: str, colors: list[str]) -> str:
    style_map = {
        "flat vector": "flat vector illustration style",
        "watercolor": "watercolor painting style",
        "hand-drawn": "hand-drawn sketch style",
        "vintage": "vintage illustration style",
    }
    subject = subcategory if subcategory else category
    color_str = ", ".join(colors)
    use_cases = "textile design, wallpaper, wrapping paper, fabric printing, scrapbooking, and digital backgrounds"

    return (
        f"Seamless tileable {subject} pattern in {style_map.get(style, style)} "
        f"with {color_str} color scheme. Perfect for {use_cases}. "
        f"High quality repeating design."
    )


def build_title(data: dict[str, Any], color_label: str, idx: int) -> str:
    base = data.get("title", "")
    if not base:
        base = f"Pattern {idx:04d}"
    # 重複回避のためにカラーバリアントを付与
    return f"{base} - {color_label.title()} Variant"


def infer_from_filename(filename: str) -> dict[str, Any]:
    """ファイル名から category/subcategory を推定（プロンプトデータがない場合用）。"""
    name = filename.replace(".png", "").replace(".jpg", "")
    parts = name.split("_", 2)
    if len(parts) >= 3:
        rest = parts[2]
        for key in SUBCATEGORY_TAGS:
            if key.replace(" ", "_") in rest or key in rest:
                return {"category": "floral", "subcategory": key, "title": rest.replace("_", " ").title(), "prompt": rest, "style": "flat vector", "color_scheme": "pastel"}
        category = rest.split("_")[0] if "_" in rest else rest
        subcategory = "_".join(rest.split("_")[1:]) if "_" in rest else ""
        return {
            "category": category,
            "subcategory": subcategory.replace("_", " "),
            "title": rest.replace("_", " ").title(),
            "prompt": rest,
            "style": "flat vector",
            "color_scheme": "pastel",
        }
    return {"category": "floral", "subcategory": "", "title": filename, "prompt": "", "style": "flat vector", "color_scheme": "pastel"}


def adobe_category(category: str) -> str:
    mapping = {
        "floral": "Backgrounds/Textures",
        "botanical": "Backgrounds/Textures",
        "geometric": "Abstract",
        "abstract": "Abstract",
        "nature": "Nature",
        "food": "Food and Drink",
        "animal": "Animals/Wildlife",
        "cultural": "Arts/Entertainment",
        "seasonal": "Holidays/Celebrations",
    }
    return mapping.get(category, "Backgrounds/Textures")


def shutterstock_category(category: str) -> str:
    return SHUTTERSTOCK_CATEGORIES.get(category, "Backgrounds")


# ─── メイン処理 ───────────────────────────────────────────

def generate_metadata() -> None:
    with open(PROMPTS_FILE, "r", encoding="utf-8") as f:
        all_prompts: list[dict[str, Any]] = json.load(f)

    prompt_map: dict[int, dict[str, Any]] = {i: p for i, p in enumerate(all_prompts)}

    images = sorted(
        [f for f in os.listdir(IMAGE_DIR) if f.endswith(".png")],
    )
    print(f"Found {len(images)} images, {len(all_prompts)} prompt entries")

    rows: list[dict[str, Any]] = []

    for img_file in images:
        match = re.match(r"stock_(\d+)_", img_file)
        if not match:
            continue
        idx = int(match.group(1))

        data = prompt_map.get(idx) or infer_from_filename(img_file)

        category = detect_category(data)
        subcategory = detect_subcategory(data)
        style = detect_style(data)
        colors = detect_colors(data)
        tags = build_tags(category, subcategory, style, colors)
        description = build_description(category, subcategory, style, colors)
        color_label = colors[0] if colors else "pastel"
        title = build_title(data, color_label, idx)

        rows.append({
            "filename": img_file,
            "title": title,
            "description": description,
            "keywords": ", ".join(tags),
            "category": category,
            "subcategory": subcategory,
            "style": style,
            "colors": ", ".join(colors),
            "ai_generated": "Yes",
            "releases": "Not Required",
            # platform-specific
            "adobe_category": adobe_category(category),
            "shutterstock_category": shutterstock_category(category),
            "editorial_use_only": "No",
        })

    _write_adobe_csv(rows)
    _write_freepik_csv(rows)
    _write_shutterstock_csv(rows)
    _write_full_csv(rows)
    print(f"\nDone. Total: {len(rows)} images processed.")


def _write_adobe_csv(rows: list[dict[str, Any]]) -> None:
    path = os.path.join(METADATA_DIR, "adobe_stock_metadata.csv")
    fieldnames = ["filename", "title", "keywords", "category", "releases"]
    with open(path, "w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)
    print(f"Adobe Stock CSV  : {path} ({len(rows)} rows)")


def _write_freepik_csv(rows: list[dict[str, Any]]) -> None:
    path = os.path.join(METADATA_DIR, "freepik_metadata.csv")
    fieldnames = ["filename", "title", "description", "keywords", "category", "ai_generated"]
    with open(path, "w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)
    print(f"Freepik CSV      : {path} ({len(rows)} rows)")


def _write_shutterstock_csv(rows: list[dict[str, Any]]) -> None:
    """Shutterstock CSV Bulk Upload 形式。
    必須列: filename, description, keywords, categories, editorial
    参考: https://www.shutterstock.com/contributorsupport/articles/kbat02/Submitting-Content-via-CSV
    """
    path = os.path.join(METADATA_DIR, "shutterstock_metadata.csv")
    fieldnames = [
        "filename", "description", "keywords",
        "categories", "editorial", "mature_content",
    ]
    with open(path, "w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames, extrasaction="ignore")
        writer.writeheader()
        for r in rows:
            writer.writerow({
                "filename": r["filename"],
                "description": r["title"],   # Shutterstock は description = タイトル扱い
                "keywords": r["keywords"],
                "categories": r["shutterstock_category"],
                "editorial": "No",
                "mature_content": "No",
            })
    print(f"Shutterstock CSV : {path} ({len(rows)} rows)")


def _write_full_csv(rows: list[dict[str, Any]]) -> None:
    path = os.path.join(METADATA_DIR, "full_metadata.csv")
    fieldnames = [
        "filename", "title", "description", "keywords",
        "category", "subcategory", "style", "colors",
        "ai_generated", "releases",
        "adobe_category", "shutterstock_category",
    ]
    with open(path, "w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)
    print(f"Full metadata CSV: {path} ({len(rows)} rows)")


if __name__ == "__main__":
    generate_metadata()
