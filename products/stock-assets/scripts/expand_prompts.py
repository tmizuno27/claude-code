"""
Expand prompt library to 500+ prompts across multiple categories.
Covers high-demand stock pattern niches beyond florals.
"""
import json
import os

BASE_DIR = os.path.dirname(os.path.dirname(__file__))
METADATA_DIR = os.path.join(BASE_DIR, "output", "metadata")
OUTPUT_FILE = os.path.join(METADATA_DIR, "prompts_expanded.json")

# Category definitions: (subject, subcategory, prompt_elements)
CATEGORIES = {
    "geometric": [
        ("art deco", "Art deco geometric pattern with golden lines, fan shapes, and symmetrical arches"),
        ("moroccan tile", "Moroccan zellige tile pattern with intricate geometric shapes and mosaic design"),
        ("hexagonal", "Hexagonal honeycomb geometric pattern with clean lines"),
        ("chevron", "Chevron zigzag pattern with alternating stripes"),
        ("terrazzo", "Terrazzo stone pattern with colorful chips and fragments on neutral background"),
        ("mid century", "Mid-century modern geometric pattern with atomic age shapes, boomerangs, and starbursts"),
    ],
    "botanical": [
        ("monstera leaves", "Tropical monstera deliciosa leaves pattern with large split leaves"),
        ("eucalyptus", "Eucalyptus branches and leaves pattern with silver-green foliage"),
        ("palm leaves", "Tropical palm leaf pattern with fan-shaped fronds"),
        ("fern", "Delicate fern fronds pattern with detailed pinnate leaves"),
        ("olive branch", "Mediterranean olive branch pattern with small leaves and olives"),
        ("bamboo", "Asian bamboo stalks and leaves pattern"),
    ],
    "abstract": [
        ("marble texture", "Luxurious marble texture pattern with veining and natural stone look"),
        ("watercolor wash", "Abstract watercolor wash pattern with soft blending colors"),
        ("brush strokes", "Dynamic brush stroke pattern with artistic paint marks"),
        ("ink splatter", "Abstract ink splatter and splash pattern"),
        ("gradient mesh", "Smooth gradient mesh pattern with flowing color transitions"),
        ("minimalist shapes", "Minimalist abstract shapes pattern with circles, lines, and dots"),
    ],
    "nature": [
        ("ocean waves", "Ocean wave pattern with flowing water curves and sea foam"),
        ("mountain landscape", "Mountain silhouette pattern with layered peaks"),
        ("stars constellation", "Night sky constellation pattern with stars and connecting lines"),
        ("clouds", "Soft fluffy cloud pattern on light blue sky background"),
        ("autumn leaves", "Falling autumn leaves pattern with maple, oak, and birch leaves"),
        ("snowflakes", "Delicate snowflake crystal pattern with intricate ice designs"),
    ],
    "food": [
        ("fruits citrus", "Fresh citrus fruit pattern with oranges, lemons, and limes slices"),
        ("berries", "Mixed berries pattern with strawberries, blueberries, and raspberries"),
        ("herbs kitchen", "Kitchen herbs pattern with basil, rosemary, thyme, and sage"),
        ("coffee beans", "Coffee beans and coffee plant leaves pattern"),
        ("avocado", "Cute avocado pattern with whole and half avocados"),
        ("mushrooms", "Woodland mushroom and toadstool pattern with various species"),
    ],
    "animal": [
        ("butterflies", "Colorful butterfly pattern with various species in flight"),
        ("birds", "Small songbird pattern with branches and leaves"),
        ("fish koi", "Japanese koi fish pattern with water ripples"),
        ("sea creatures", "Ocean sea creatures pattern with shells, starfish, and seahorses"),
        ("cats silhouette", "Playful cat silhouette pattern in various poses"),
        ("bees", "Honey bee and honeycomb pattern with flowers"),
    ],
    "cultural": [
        ("japanese wave", "Japanese ukiyo-e wave pattern (seigaiha) with traditional ocean waves"),
        ("paisley", "Ornate paisley pattern with intricate teardrop and curved shapes"),
        ("damask", "Classic damask pattern with ornamental baroque flourishes"),
        ("scandinavian folk", "Scandinavian folk art pattern with simple flowers, hearts, and birds"),
        ("mexican otomi", "Mexican Otomi embroidery-inspired pattern with animals and flowers"),
        ("ikat", "Traditional ikat pattern with blurred-edge geometric dye design"),
    ],
    "seasonal": [
        ("christmas", "Christmas holiday pattern with candy canes, ornaments, and holly"),
        ("halloween", "Halloween pattern with pumpkins, bats, ghosts, and spiderwebs"),
        ("valentines", "Valentine's Day pattern with hearts, roses, and love letters"),
        ("easter", "Easter pattern with decorated eggs, bunnies, and spring flowers"),
        ("summer beach", "Summer beach pattern with palm trees, surfboards, and sunglasses"),
        ("back to school", "Back to school pattern with notebooks, pencils, and school supplies"),
    ],
}

STYLES = [
    ("flat vector", "flat vector style, clean lines, modern design, vector illustration"),
    ("watercolor", "watercolor painting style, soft brushstrokes, artistic texture"),
    ("hand-drawn", "hand-drawn sketch style, ink line art, organic freehand illustration"),
]

COLOR_SCHEMES = [
    ("pastel", "pastel pink, mint green, soft yellow, lavender"),
    ("navy gold", "navy blue, gold, white, dark blue"),
    ("earth tones", "earth tones, terracotta, sage green, brown, beige"),
    ("monochrome", "monochrome, black, white, gray, charcoal"),
    ("warm sunset", "warm sunset colors, coral, orange, peach, amber"),
    ("cool ocean", "cool ocean tones, teal, aqua, navy, seafoam"),
]


def generate_all_prompts():
    """Generate expanded prompt library."""
    prompts = []
    idx = 50  # Start after existing 50 images

    for category, subjects in CATEGORIES.items():
        for subject_name, subject_desc in subjects:
            for style_name, style_desc in STYLES:
                for color_name, color_desc in COLOR_SCHEMES:
                    prompt = (
                        f"Seamless tileable pattern of {subject_desc}, "
                        f"{style_desc}, {color_desc}, white background, "
                        f"high quality, repeating pattern design"
                    )
                    title_parts = subject_name.title().split()
                    style_parts = style_name.title().split()
                    title = f"{''.join(w.capitalize() if w[0].islower() else w for w in title_parts)} "
                    title += f"{''.join(w.capitalize() if w[0].islower() else w for w in style_parts)} "
                    title += "Seamless Pattern"
                    title = " ".join(title.split())  # normalize spaces

                    # Build tags
                    base_tags = [
                        "seamless", "pattern", "tileable", "repeating",
                        "background", "textile", "wallpaper", "fabric",
                        "surface design", "digital paper"
                    ]
                    subject_tags = subject_name.split() + category.split()
                    style_tags = style_name.split()
                    color_tags = color_name.split()

                    all_tags = list(dict.fromkeys(
                        base_tags + subject_tags + style_tags + color_tags
                    ))

                    prompts.append({
                        "type": "pattern",
                        "category": category,
                        "subcategory": subject_name,
                        "prompt": prompt,
                        "model": "recraft-v3",
                        "tags": all_tags,
                        "title": title,
                        "color_scheme": color_name,
                        "style": style_name,
                    })

    print(f"Generated {len(prompts)} new prompts")
    print(f"\nBreakdown by category:")
    for cat in CATEGORIES:
        count = sum(1 for p in prompts if p["category"] == cat)
        print(f"  {cat}: {count}")

    # Save
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(prompts, f, indent=2, ensure_ascii=False)
    print(f"\nSaved to: {OUTPUT_FILE}")

    return prompts


if __name__ == "__main__":
    generate_all_prompts()
