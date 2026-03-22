"""
Generate stock site metadata CSV for all generated images.
Produces Adobe Stock and Freepik compatible metadata.
"""
import csv
import json
import os
import re

BASE_DIR = os.path.dirname(os.path.dirname(__file__))
IMAGE_DIR = os.path.join(BASE_DIR, "output", "images")
METADATA_DIR = os.path.join(BASE_DIR, "output", "metadata")
PROMPTS_FILE = os.path.join(METADATA_DIR, "prompts.json")

# Extended tag sets by subject for better discoverability
SUBJECT_TAGS = {
    "roses": [
        "rose", "peony", "roses", "peonies", "rose pattern", "peony pattern",
        "romantic", "elegant", "garden", "bouquet", "bloom", "blossom",
        "feminine", "wedding", "bridal", "spring flowers", "classic floral"
    ],
    "wildflowers": [
        "wildflower", "daisy", "daisies", "wildflowers", "meadow", "field",
        "botanical", "natural", "countryside", "cottage", "rustic",
        "garden flowers", "spring meadow", "folk", "prairie"
    ],
    "hibiscus": [
        "hibiscus", "tropical", "hawaiian", "exotic", "paradise",
        "tropical flower", "island", "summer", "beach", "aloha",
        "tropical plant", "jungle", "lush", "vacation", "resort"
    ],
    "cherry blossom": [
        "cherry blossom", "sakura", "japanese", "spring", "cherry tree",
        "hanami", "japan", "oriental", "asian", "zen", "delicate",
        "pink blossom", "petal", "spring bloom", "flowering tree"
    ],
    "sunflower": [
        "sunflower", "sunflowers", "sun", "sunny", "harvest",
        "autumn", "fall", "farm", "country", "golden", "yellow flower",
        "seed", "garden", "cheerful", "bright"
    ],
    "lavender": [
        "lavender", "herb", "herbal", "provence", "french",
        "purple flower", "aromatherapy", "calm", "relaxing", "spa",
        "field", "scented", "botanical herb", "medicinal", "natural"
    ],
}

STYLE_TAGS = {
    "flat vector": [
        "flat design", "vector", "vector art", "vector illustration",
        "flat style", "modern design", "graphic design", "clean lines",
        "minimalist", "digital art", "clipart", "simple"
    ],
    "watercolor": [
        "watercolor", "watercolour", "hand painted", "artistic",
        "soft", "gentle", "pastel", "aquarelle", "painting",
        "brushstroke", "texture", "traditional art"
    ],
    "hand-drawn": [
        "hand drawn", "sketch", "line art", "ink", "doodle",
        "illustration", "pencil", "drawing", "artistic", "handmade",
        "organic", "freehand"
    ],
}

COLOR_TAGS = {
    "pastel": ["pastel", "pastel colors", "soft colors", "light", "pale"],
    "navy": ["navy", "navy blue", "dark blue", "gold", "luxury", "premium"],
    "earth": ["earth tones", "terracotta", "sage", "brown", "natural colors", "muted"],
    "pink": ["pink", "blush", "rose pink", "soft pink", "feminine"],
    "blue": ["blue", "cornflower", "dusty blue", "cool tones"],
    "coral": ["coral", "warm", "sunset", "warm tones"],
    "mint": ["mint", "mint green", "fresh", "cool"],
    "gold": ["gold", "golden", "metallic", "luxury"],
    "purple": ["purple", "violet", "mauve", "plum"],
}

# Base tags for all seamless patterns
BASE_TAGS = [
    "seamless pattern", "seamless", "pattern", "tileable", "repeating",
    "background", "textile", "fabric", "wallpaper", "wrapping paper",
    "surface design", "print", "decor", "decorative", "ornament",
    "digital paper", "scrapbooking"
]


def detect_subject(prompt_text):
    """Detect floral subject from prompt."""
    prompt_lower = prompt_text.lower()
    for key in SUBJECT_TAGS:
        if key in prompt_lower:
            return key
    return "floral"


def detect_style(title):
    """Detect art style from title."""
    title_lower = title.lower()
    for key in STYLE_TAGS:
        if key in title_lower:
            return key
    return "flat vector"


def detect_colors(prompt_text):
    """Detect color scheme from prompt."""
    prompt_lower = prompt_text.lower()
    matched = []
    for key in COLOR_TAGS:
        if key in prompt_lower:
            matched.append(key)
    return matched if matched else ["pastel"]


def build_tags(subject, style, colors, max_tags=49):
    """Build optimized tag list (Adobe Stock max 49, Freepik max 50)."""
    tags = list(BASE_TAGS)
    tags.extend(SUBJECT_TAGS.get(subject, []))
    tags.extend(STYLE_TAGS.get(style, []))
    for c in colors:
        tags.extend(COLOR_TAGS.get(c, []))
    tags.append("floral")
    tags.append("flower")
    tags.append("nature")
    tags.append("design")
    # Deduplicate while preserving order
    seen = set()
    unique = []
    for t in tags:
        if t.lower() not in seen:
            seen.add(t.lower())
            unique.append(t)
    return unique[:max_tags]


def build_description(subject, style, colors):
    """Generate SEO-optimized description for stock sites."""
    style_desc = {
        "flat vector": "flat vector illustration style",
        "watercolor": "watercolor painting style",
        "hand-drawn": "hand-drawn sketch style",
    }
    color_desc = ", ".join(colors)
    subject_cap = subject.replace("cherry blossom", "cherry blossom (sakura)")

    return (
        f"Seamless tileable {subject_cap} pattern in {style_desc.get(style, style)} "
        f"with {color_desc} color scheme. Perfect for textile design, wallpaper, "
        f"wrapping paper, fabric printing, scrapbooking, and digital backgrounds. "
        f"High quality repeating floral design."
    )


def generate_metadata():
    """Generate metadata CSV for all existing images."""
    with open(PROMPTS_FILE, "r", encoding="utf-8") as f:
        all_prompts = json.load(f)

    # Find all generated images
    images = sorted(
        [f for f in os.listdir(IMAGE_DIR) if f.endswith(".png")],
        key=lambda x: x
    )

    print(f"Found {len(images)} images")

    rows = []
    for img_file in images:
        # Extract index from filename: stock_0000_pattern_floral.png
        match = re.match(r"stock_(\d+)_", img_file)
        if not match:
            continue
        idx = int(match.group(1))
        if idx >= len(all_prompts):
            continue

        prompt_data = all_prompts[idx]
        subject = detect_subject(prompt_data["prompt"])
        style = detect_style(prompt_data["title"])
        colors = detect_colors(prompt_data["prompt"])
        tags = build_tags(subject, style, colors)
        description = build_description(subject, style, colors)

        # Make title unique by adding color variant
        color_label = colors[0] if colors else "classic"
        unique_title = f"{prompt_data['title']} - {color_label.title()} Variant"

        rows.append({
            "filename": img_file,
            "title": unique_title,
            "description": description,
            "keywords": ", ".join(tags),
            "category": "Patterns",
            "subject": subject,
            "style": style,
            "colors": ", ".join(colors),
            "ai_generated": "Yes",
            "releases": "Not Required",
        })

    # Write Adobe Stock CSV
    adobe_csv = os.path.join(METADATA_DIR, "adobe_stock_metadata.csv")
    with open(adobe_csv, "w", encoding="utf-8", newline="") as f:
        fieldnames = [
            "filename", "title", "keywords", "category", "releases"
        ]
        writer = csv.DictWriter(f, fieldnames=fieldnames, extrasaction="ignore")
        writer.writeheader()
        for r in rows:
            writer.writerow(r)
    print(f"Adobe Stock CSV: {adobe_csv} ({len(rows)} rows)")

    # Write Freepik CSV
    freepik_csv = os.path.join(METADATA_DIR, "freepik_metadata.csv")
    with open(freepik_csv, "w", encoding="utf-8", newline="") as f:
        fieldnames = [
            "filename", "title", "description", "keywords",
            "category", "ai_generated"
        ]
        writer = csv.DictWriter(f, fieldnames=fieldnames, extrasaction="ignore")
        writer.writeheader()
        for r in rows:
            writer.writerow(r)
    print(f"Freepik CSV: {freepik_csv} ({len(rows)} rows)")

    # Write full metadata (internal reference)
    full_csv = os.path.join(METADATA_DIR, "full_metadata.csv")
    with open(full_csv, "w", encoding="utf-8", newline="") as f:
        fieldnames = [
            "filename", "title", "description", "keywords",
            "category", "subject", "style", "colors",
            "ai_generated", "releases"
        ]
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for r in rows:
            writer.writerow(r)
    print(f"Full metadata CSV: {full_csv} ({len(rows)} rows)")

    return rows


if __name__ == "__main__":
    generate_metadata()
