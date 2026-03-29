"""
generate_business_prompts.py
-----------------------------
需要の高いビジネス・テクノロジー・ライフスタイルカテゴリの
追加プロンプト（各カテゴリ×スタイル×カラー）を生成し、
prompts_expanded.json に追記する。
"""
import json
import os
from itertools import product as iproduct
from typing import Any

BASE_DIR = os.path.dirname(os.path.dirname(__file__))
METADATA_DIR = os.path.join(BASE_DIR, "output", "metadata")
PROMPTS_FILE = os.path.join(METADATA_DIR, "prompts_expanded.json")
OUTPUT_FILE = os.path.join(METADATA_DIR, "prompts_business.json")

# ─── 新規カテゴリ定義 ──────────────────────────────────────

NEW_CATEGORIES: list[dict[str, Any]] = [

    # ──── BUSINESS ────────────────────────────────────────
    {
        "category": "business",
        "subcategory": "finance",
        "subjects": [
            ("coins and dollar signs", ["gold", "navy blue", "white"], "modern business icons"),
            ("stock chart and graphs", ["blue", "green", "white"], "data visualization"),
            ("credit cards and cryptocurrency symbols", ["dark", "gold", "purple"], "fintech"),
            ("piggy bank and savings icons", ["pastel pink", "mint", "white"], "personal finance"),
        ],
    },
    {
        "category": "business",
        "subcategory": "office",
        "subjects": [
            ("laptop and coffee workspace", ["warm gray", "gold", "cream"], "remote work"),
            ("calendar planner and stationery", ["pastel blue", "coral", "white"], "productivity"),
            ("business chart and arrow icons", ["navy", "teal", "white"], "corporate"),
            ("handshake and teamwork icons", ["blue", "orange", "white"], "partnership"),
        ],
    },
    {
        "category": "business",
        "subcategory": "ecommerce",
        "subjects": [
            ("shopping cart and package delivery icons", ["teal", "orange", "white"], "online shopping"),
            ("price tag and sale badge icons", ["red", "gold", "white"], "retail promotion"),
            ("star rating and review icons", ["yellow", "gray", "white"], "customer review"),
        ],
    },

    # ──── TECHNOLOGY ─────────────────────────────────────
    {
        "category": "technology",
        "subcategory": "ai",
        "subjects": [
            ("neural network nodes and connections", ["purple", "cyan", "dark"], "artificial intelligence"),
            ("robot and circuit board", ["blue neon", "black", "silver"], "robotics"),
            ("brain and microchip", ["purple", "white", "dark navy"], "machine learning"),
        ],
    },
    {
        "category": "technology",
        "subcategory": "digital",
        "subjects": [
            ("code brackets and binary numbers", ["green neon", "black", "dark"], "programming"),
            ("smartphone and app icons", ["blue", "pink", "white"], "mobile tech"),
            ("cloud computing and wifi symbols", ["light blue", "white", "gray"], "cloud services"),
            ("lock and shield security icons", ["dark blue", "gold", "white"], "cybersecurity"),
            ("globe and network connection", ["teal", "blue", "white"], "internet connectivity"),
        ],
    },

    # ──── LIFESTYLE ──────────────────────────────────────
    {
        "category": "lifestyle",
        "subcategory": "wellness",
        "subjects": [
            ("yoga pose silhouettes", ["sage green", "white", "lavender"], "yoga meditation"),
            ("meditation and mindfulness symbols", ["purple", "gold", "white"], "spiritual wellness"),
            ("healthy food and vegetables", ["green", "orange", "white"], "healthy eating"),
            ("running and fitness icons", ["coral", "teal", "white"], "active lifestyle"),
            ("sleep and moon stars", ["navy", "silver", "dark blue"], "sleep wellness"),
        ],
    },
    {
        "category": "lifestyle",
        "subcategory": "travel",
        "subjects": [
            ("passport suitcase and airplane", ["navy", "gold", "cream"], "travel adventure"),
            ("world map and compass", ["vintage brown", "cream", "gold"], "world exploration"),
            ("beach and palm tree icons", ["turquoise", "yellow", "sand"], "tropical vacation"),
            ("mountain and hiking icons", ["forest green", "brown", "cream"], "mountain adventure"),
            ("city skyline and landmark icons", ["black", "gold", "white"], "urban travel"),
        ],
    },
    {
        "category": "lifestyle",
        "subcategory": "beauty",
        "subjects": [
            ("makeup brush and lipstick icons", ["rose gold", "pink", "white"], "beauty cosmetics"),
            ("skincare bottle and serum", ["mint", "lavender", "white"], "skincare routine"),
            ("perfume bottle and flowers", ["gold", "blush pink", "white"], "luxury fragrance"),
            ("nail polish and manicure tools", ["pastel rainbow", "white", "gold"], "nail art"),
        ],
    },
    {
        "category": "lifestyle",
        "subcategory": "home",
        "subjects": [
            ("interior furniture and plant icons", ["terracotta", "sage", "cream"], "home decor"),
            ("kitchen utensil and cookware", ["red", "white", "gray"], "kitchen cooking"),
            ("candle and cozy home icons", ["warm amber", "cream", "brown"], "cozy hygge"),
            ("tools and DIY icons", ["steel blue", "orange", "white"], "home improvement"),
        ],
    },

    # ──── EDUCATION ─────────────────────────────────────
    {
        "category": "education",
        "subcategory": "science",
        "subjects": [
            ("atom and molecule icons", ["blue", "teal", "white"], "science chemistry"),
            ("DNA helix and laboratory flask", ["purple", "green", "white"], "biology"),
            ("planet and telescope", ["dark navy", "gold", "purple"], "astronomy space"),
            ("math formula and calculator", ["yellow", "gray", "white"], "mathematics"),
        ],
    },
    {
        "category": "education",
        "subcategory": "learning",
        "subjects": [
            ("open book and graduation cap", ["dark blue", "gold", "white"], "education graduation"),
            ("lightbulb and idea icons", ["yellow", "teal", "white"], "creative ideas"),
            ("certificate and award ribbon", ["gold", "navy", "white"], "achievement"),
        ],
    },

    # ──── SUSTAINABILITY ──────────────────────────────────
    {
        "category": "sustainability",
        "subcategory": "eco",
        "subjects": [
            ("recycling arrows and leaf icons", ["green", "white", "earth tones"], "eco friendly"),
            ("solar panel and wind turbine", ["sky blue", "yellow", "green"], "renewable energy"),
            ("water drop and earth globe", ["blue", "green", "white"], "environmental protection"),
            ("reusable bag and zero waste icons", ["kraft brown", "green", "white"], "zero waste lifestyle"),
        ],
    },
]

# スタイルバリエーション
STYLES = [
    ("flat vector style, clean lines, modern design, vector illustration", "FlatVector"),
    ("minimal line art style, simple strokes, outline icons", "LineArt"),
    ("isometric 3D style, clean perspective, modern graphic", "Isometric"),
]

# カラースキーム付加（背景）
COLOR_BG = [
    ("white background", "white"),
    ("light gray background", "light gray"),
]


def make_prompt(subject_desc: str, colors_str: str, context: str,
                style_desc: str, bg: str) -> str:
    return (
        f"Seamless tileable pattern of {subject_desc} with {context}, "
        f"{style_desc}, {colors_str}, {bg}, "
        f"high quality, repeating pattern design"
    )


def make_title(subcategory: str, subject_desc: str, style_name: str) -> str:
    words = subject_desc.split()[:4]
    subject_short = " ".join(words).title()
    return f"{subject_short} {style_name} Seamless Pattern"


def generate_business_prompts() -> list[dict[str, Any]]:
    new_prompts: list[dict[str, Any]] = []

    for cat_def in NEW_CATEGORIES:
        category = cat_def["category"]
        subcategory = cat_def["subcategory"]

        for subject_desc, colors_list, context in cat_def["subjects"]:
            colors_str = ", ".join(colors_list)
            tags_base = [
                "seamless", "pattern", "tileable", "repeating",
                "background", "textile", "wallpaper", "fabric",
                "surface design", "digital paper",
                category, subcategory,
            ] + [w for w in subject_desc.split() if len(w) > 3]

            # スタイル × 背景 の組み合わせ
            for (style_desc, style_name), (bg, bg_name) in iproduct(STYLES, COLOR_BG):
                prompt_text = make_prompt(subject_desc, colors_str, context, style_desc, bg)
                title = make_title(subcategory, subject_desc, style_name)

                new_prompts.append({
                    "type": "pattern",
                    "category": category,
                    "subcategory": subcategory,
                    "prompt": prompt_text,
                    "model": "recraft-v3",
                    "tags": tags_base[:15],
                    "title": title,
                    "color_scheme": colors_str,
                    "style": style_name.lower(),
                    "bg": bg_name,
                })

    return new_prompts


def main() -> None:
    # 既存プロンプトを読み込み
    with open(PROMPTS_FILE, "r", encoding="utf-8") as f:
        existing: list[dict[str, Any]] = json.load(f)

    new_prompts = generate_business_prompts()
    print(f"New prompts generated: {len(new_prompts)}")

    # 新規プロンプト単体ファイル（生成用）
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(new_prompts, f, ensure_ascii=False, indent=2)
    print(f"Saved to: {OUTPUT_FILE}")

    # カテゴリ集計
    from collections import Counter
    cats = Counter(p["category"] for p in new_prompts)
    subs = Counter(p["subcategory"] for p in new_prompts)
    print("\nNew prompt breakdown by category:")
    for cat, cnt in cats.most_common():
        print(f"  {cat}: {cnt}")
    print("\nBy subcategory:")
    for sub, cnt in subs.most_common():
        print(f"  {sub}: {cnt}")

    # 合算統計（既存 + 新規）
    total = len(existing) + len(new_prompts)
    print(f"\nTotal prompts (existing {len(existing)} + new {len(new_prompts)}) = {total}")
    print(f"Estimated images if generated: {total} (upscaled: {total})")
    print(f"New prompts file: {OUTPUT_FILE}")


if __name__ == "__main__":
    main()
