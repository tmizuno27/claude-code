"""
Stock Asset Prompt Generator
Generate batch prompts for seamless patterns, icons, and backgrounds.
"""
import json
import csv
import os
from datetime import datetime

OUTPUT_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "output", "metadata")

PATTERN_STYLES = [
    "flat vector", "watercolor", "hand-drawn sketch", "geometric minimal",
    "line art", "retro vintage", "modern abstract", "botanical illustration"
]

PATTERN_SUBJECTS = {
    "floral": [
        "roses and peonies", "wildflowers and daisies", "tropical hibiscus",
        "cherry blossom sakura", "sunflowers", "lavender sprigs",
        "tulips", "magnolia flowers", "lotus flowers", "dandelions"
    ],
    "geometric": [
        "hexagonal honeycomb", "triangles and diamonds", "concentric circles",
        "chevron zigzag", "polka dots", "herringbone", "moroccan tiles",
        "art deco fan shapes", "celtic knots", "isometric cubes"
    ],
    "nature": [
        "tropical monstera leaves", "autumn maple leaves", "pine trees forest",
        "ocean waves", "mountain landscape", "cactus succulents",
        "feathers", "seashells", "bamboo stalks", "mushrooms and ferns"
    ],
    "food": [
        "fruits citrus lemon orange", "coffee cups and beans",
        "cupcakes and pastries", "sushi and chopsticks", "pizza slices",
        "avocado halves", "berries strawberry blueberry", "wine glasses",
        "tacos and burritos", "donuts sprinkles"
    ],
    "seasonal": [
        "christmas snowflakes holly", "halloween pumpkins bats",
        "valentines hearts and roses", "easter eggs and bunnies",
        "thanksgiving autumn harvest", "spring butterflies",
        "summer beach umbrella", "winter cozy sweater knit",
        "new year fireworks", "fall acorns and leaves"
    ],
    "abstract": [
        "marble texture swirls", "terrazzo speckles", "brushstrokes splatter",
        "gradient mesh blobs", "noise grain texture", "organic fluid shapes",
        "memphis style shapes", "bauhaus geometric", "pixel art blocks",
        "halftone dots pattern"
    ]
}

COLOR_PALETTES = [
    "pastel pink, mint green, soft yellow",
    "navy blue, gold, white",
    "earth tones brown, terracotta, sage green",
    "monochrome black and white",
    "coral, teal, cream",
    "lavender purple, dusty rose, gray",
    "forest green, burgundy, cream",
    "sky blue, peach, white",
    "sunset orange, magenta, deep purple",
    "muted sage, blush, warm beige"
]

ICON_CATEGORIES = {
    "business": [
        "briefcase", "chart graph", "handshake", "lightbulb idea",
        "target goal", "calendar schedule", "email envelope", "cloud computing",
        "rocket launch", "puzzle piece"
    ],
    "health": [
        "heart pulse", "stethoscope", "pill capsule", "apple nutrition",
        "dumbbell fitness", "meditation yoga", "tooth dental",
        "brain mind", "eye vision", "leaf organic"
    ],
    "travel": [
        "airplane", "suitcase luggage", "compass navigation", "passport",
        "camera photography", "globe world", "tent camping", "anchor marine",
        "hot air balloon", "bicycle"
    ],
    "technology": [
        "smartphone mobile", "laptop computer", "wifi signal", "battery charging",
        "lock security", "code brackets", "robot AI", "microchip processor",
        "satellite", "VR headset"
    ]
}

BACKGROUND_TYPES = [
    "soft gradient blur", "bokeh light circles", "abstract waves flow",
    "minimal geometric lines", "watercolor wash", "paper texture subtle",
    "holographic iridescent", "starry night sky", "marble stone surface",
    "wood grain natural"
]


def generate_pattern_prompts():
    """Generate seamless pattern prompts."""
    prompts = []
    for category, subjects in PATTERN_SUBJECTS.items():
        for subject in subjects:
            for style in PATTERN_STYLES[:3]:  # Top 3 styles per subject
                for palette in COLOR_PALETTES[:3]:  # Top 3 palettes
                    prompt = {
                        "type": "pattern",
                        "category": category,
                        "prompt": (
                            f"Seamless tileable pattern of {subject}, "
                            f"{style} style, {palette}, "
                            f"white background, high quality, "
                            f"repeating pattern design, vector illustration"
                        ),
                        "model": "recraft-v3",
                        "tags": [
                            "seamless", "pattern", "tileable", category,
                            subject.split()[0], style.split()[0], "vector",
                            "background", "textile", "wallpaper"
                        ],
                        "title": f"{subject.title()} {style.title()} Seamless Pattern"
                    }
                    prompts.append(prompt)
    return prompts


def generate_icon_prompts():
    """Generate flat icon set prompts."""
    prompts = []
    for category, icons in ICON_CATEGORIES.items():
        for icon in icons:
            prompt = {
                "type": "icon",
                "category": category,
                "prompt": (
                    f"Single flat design icon of {icon}, "
                    f"minimal vector style, solid colors, "
                    f"clean lines, centered on white background, "
                    f"professional UI icon, high quality"
                ),
                "model": "recraft-v3",
                "tags": [
                    "icon", "flat", "vector", "minimal", category,
                    icon.split()[0], "UI", "design", "symbol", "clipart"
                ],
                "title": f"{icon.title()} Flat Vector Icon"
            }
            prompts.append(prompt)
    return prompts


def generate_background_prompts():
    """Generate background/texture prompts."""
    prompts = []
    for bg_type in BACKGROUND_TYPES:
        for palette in COLOR_PALETTES[:5]:
            prompt = {
                "type": "background",
                "category": "background",
                "prompt": (
                    f"{bg_type} background, {palette}, "
                    f"high resolution, abstract, clean, "
                    f"professional presentation background, 4K quality"
                ),
                "model": "dall-e-3",
                "tags": [
                    "background", "abstract", "texture", "wallpaper",
                    bg_type.split()[0], "presentation", "desktop",
                    "banner", "header", "design"
                ],
                "title": f"{bg_type.title()} Background"
            }
            prompts.append(prompt)
    return prompts


def save_prompts(prompts, filename="prompts.json"):
    """Save prompts to JSON file."""
    filepath = os.path.join(OUTPUT_DIR, filename)
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(prompts, f, indent=2, ensure_ascii=False)
    return filepath


def save_prompts_csv(prompts, filename="prompts.csv"):
    """Save prompts to CSV for easy review."""
    filepath = os.path.join(OUTPUT_DIR, filename)
    with open(filepath, "w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=[
            "type", "category", "model", "title", "prompt", "tags"
        ])
        writer.writeheader()
        for p in prompts:
            row = {**p, "tags": "; ".join(p["tags"])}
            writer.writerow(row)
    return filepath


if __name__ == "__main__":
    all_prompts = []

    patterns = generate_pattern_prompts()
    icons = generate_icon_prompts()
    backgrounds = generate_background_prompts()

    all_prompts.extend(patterns)
    all_prompts.extend(icons)
    all_prompts.extend(backgrounds)

    json_path = save_prompts(all_prompts)
    csv_path = save_prompts_csv(all_prompts)

    print(f"Generated {len(all_prompts)} prompts total:")
    print(f"  Patterns:    {len(patterns)}")
    print(f"  Icons:       {len(icons)}")
    print(f"  Backgrounds: {len(backgrounds)}")
    print(f"  JSON: {json_path}")
    print(f"  CSV:  {csv_path}")
