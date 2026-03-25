"""Generate Gumroad thumbnails for 5 new products using Pillow."""
import json
import os
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

BASE_DIR = Path(__file__).parent
PRODUCTS = [
    "solopreneur-ai-business-toolkit",
    "email-marketing-prompt-pack",
    "content-repurposing-system",
    "client-onboarding-kit",
    "digital-product-launch-playbook",
]

# Icon unicode characters (simple geometric shapes as fallback)
ICON_MAP = {
    "rocket": "\u25B2",      # triangle up
    "email": "\u2709",       # envelope
    "recycle": "\u267B",     # recycling
    "handshake": "\u2764",   # heart (handshake not in basic unicode)
    "launch": "\u2605",      # star
}

WIDTH, HEIGHT = 1280, 720


def create_thumbnail(product_dir: str) -> None:
    listing_path = BASE_DIR / product_dir / "listing.json"
    with open(listing_path, "r", encoding="utf-8") as f:
        listing = json.load(f)

    thumb = listing["thumbnail"]
    title = thumb["title"]
    subtitle = thumb["subtitle"]
    color_primary = thumb["color_primary"]
    color_secondary = thumb["color_secondary"]
    icon_key = thumb.get("icon", "")
    price = listing["price_usd"]

    img = Image.new("RGB", (WIDTH, HEIGHT), color_primary)
    draw = ImageDraw.Draw(img)

    # Gradient effect: draw rectangles from bottom
    for y in range(HEIGHT // 2, HEIGHT):
        ratio = (y - HEIGHT // 2) / (HEIGHT // 2)
        r1, g1, b1 = _hex_to_rgb(color_primary)
        r2, g2, b2 = _hex_to_rgb(color_secondary)
        r = int(r1 + (r2 - r1) * ratio)
        g = int(g1 + (g2 - g1) * ratio)
        b = int(b1 + (b2 - b1) * ratio)
        draw.line([(0, y), (WIDTH, y)], fill=(r, g, b))

    # Decorative circle
    draw.ellipse([WIDTH - 300, -100, WIDTH + 100, 300], fill=color_secondary + "40", outline=None)
    draw.ellipse([-150, HEIGHT - 250, 250, HEIGHT + 150], fill=color_secondary + "40", outline=None)

    # Icon
    icon_char = ICON_MAP.get(icon_key, "\u25CF")
    try:
        icon_font = ImageFont.truetype("arial.ttf", 80)
    except OSError:
        icon_font = ImageFont.load_default()
    draw.text((80, 60), icon_char, fill="white", font=icon_font)

    # Title
    try:
        title_font = ImageFont.truetype("arialbd.ttf", 72)
    except OSError:
        try:
            title_font = ImageFont.truetype("arial.ttf", 72)
        except OSError:
            title_font = ImageFont.load_default()

    y_offset = 180
    for line in title.split("\n"):
        draw.text((80, y_offset), line, fill="white", font=title_font)
        y_offset += 90

    # Subtitle
    try:
        sub_font = ImageFont.truetype("arial.ttf", 36)
    except OSError:
        sub_font = ImageFont.load_default()
    draw.text((80, y_offset + 30), subtitle, fill="white", font=sub_font)

    # Price badge
    try:
        price_font = ImageFont.truetype("arialbd.ttf", 48)
    except OSError:
        try:
            price_font = ImageFont.truetype("arial.ttf", 48)
        except OSError:
            price_font = ImageFont.load_default()
    price_text = f"${price}"
    badge_x, badge_y = WIDTH - 220, HEIGHT - 120
    draw.rounded_rectangle(
        [badge_x, badge_y, badge_x + 160, badge_y + 70],
        radius=15,
        fill="white",
    )
    draw.text((badge_x + 25, badge_y + 8), price_text, fill=color_primary, font=price_font)

    # "AI-Powered" label
    try:
        label_font = ImageFont.truetype("arial.ttf", 24)
    except OSError:
        label_font = ImageFont.load_default()
    draw.rounded_rectangle([80, HEIGHT - 80, 280, HEIGHT - 40], radius=10, fill="white")
    draw.text((100, HEIGHT - 75), "AI-Powered", fill=color_primary, font=label_font)

    out_path = BASE_DIR / product_dir / "thumbnail.png"
    img.save(out_path, "PNG", quality=95)
    print(f"  Created: {out_path}")


def _hex_to_rgb(hex_color: str) -> tuple:
    hex_color = hex_color.lstrip("#")
    return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))


def main() -> None:
    print("Generating thumbnails for 5 products...")
    for product in PRODUCTS:
        create_thumbnail(product)
    print("Done! All 5 thumbnails generated.")


if __name__ == "__main__":
    main()
