"""
AI Prompt Pack サムネイル自動生成スクリプト
600x600px 正方形 + 1280x720 カバー, グラデーション背景, モダンデザイン
"""

from PIL import Image, ImageDraw, ImageFont
import os
import math

OUTPUT_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "images")
os.makedirs(OUTPUT_DIR, exist_ok=True)

FONT_BOLD = "C:/Windows/Fonts/segoeuib.ttf"
FONT_REGULAR = "C:/Windows/Fonts/segoeui.ttf"

WIDTH, HEIGHT = 600, 600

PRODUCTS = [
    {
        "filename": "01-seo-article-writer-pack.png",
        "title": "SEO Article\nWriter Pack",
        "subtitle": "50 Battle-Tested Prompts\nfor Claude & ChatGPT",
        "price": "$19",
        "prompt_count": "50",
        "gradient": [(15, 30, 70), (30, 60, 130)],
        "accent": (60, 160, 255),
        "icon_shape": "pen",
    },
    {
        "filename": "02-wordpress-automation-kit.png",
        "title": "WordPress\nAutomation Kit",
        "subtitle": "30 Prompts + Production Code\nAPI Calls & Python Scripts",
        "price": "$29",
        "prompt_count": "30",
        "gradient": [(20, 50, 40), (30, 90, 70)],
        "accent": (50, 220, 160),
        "icon_shape": "gear",
    },
    {
        "filename": "03-affiliate-content-generator.png",
        "title": "Affiliate\nContent Gen",
        "subtitle": "50 High-Converting Prompts\nJapanese Market Focus",
        "price": "$19",
        "prompt_count": "50",
        "gradient": [(60, 20, 40), (110, 30, 60)],
        "accent": (255, 100, 140),
        "icon_shape": "link",
    },
    {
        "filename": "04-ultimate-bundle.png",
        "title": "Ultimate AI\nBlogger Bundle",
        "subtitle": "All 3 Packs · 130 Prompts\nSave $18 · Complete Pipeline",
        "price": "$49",
        "prompt_count": "130",
        "gradient": [(40, 15, 60), (80, 25, 45)],
        "accent": (255, 200, 60),
        "icon_shape": "star",
    },
]


def create_gradient(width, height, color1, color2):
    """Create a diagonal gradient background."""
    img = Image.new("RGB", (width, height))
    pixels = img.load()
    for y in range(height):
        for x in range(width):
            t = (x / width * 0.6) + (y / height * 0.4)
            r = int(color1[0] + (color2[0] - color1[0]) * t)
            g = int(color1[1] + (color2[1] - color1[1]) * t)
            b = int(color1[2] + (color2[2] - color1[2]) * t)
            pixels[x, y] = (r, g, b)
    return img


def draw_rounded_rect(draw, xy, radius, fill):
    """Draw a rounded rectangle."""
    x0, y0, x1, y1 = xy
    draw.rectangle([x0 + radius, y0, x1 - radius, y1], fill=fill)
    draw.rectangle([x0, y0 + radius, x1, y1 - radius], fill=fill)
    draw.pieslice([x0, y0, x0 + 2 * radius, y0 + 2 * radius], 180, 270, fill=fill)
    draw.pieslice([x1 - 2 * radius, y0, x1, y0 + 2 * radius], 270, 360, fill=fill)
    draw.pieslice([x0, y1 - 2 * radius, x0 + 2 * radius, y1], 90, 180, fill=fill)
    draw.pieslice([x1 - 2 * radius, y1 - 2 * radius, x1, y1], 0, 90, fill=fill)


def draw_icon_shape(draw, shape, accent, cx, cy):
    """Draw a geometric icon."""
    light = (255, 255, 255)
    color = accent

    if shape == "pen":
        # Pen/writing icon
        draw.polygon([(cx - 5, cy - 50), (cx + 5, cy - 50), (cx + 20, cy + 30), (cx - 20, cy + 30)],
                     outline=light, width=3)
        draw.polygon([(cx - 20, cy + 30), (cx + 20, cy + 30), (cx, cy + 50)], fill=color)
        draw.line([(cx - 12, cy - 10), (cx + 12, cy - 10)], fill=light, width=2)
        draw.line([(cx - 8, cy + 10), (cx + 8, cy + 10)], fill=light, width=2)

    elif shape == "gear":
        # Gear/cog icon
        r_outer = 45
        r_inner = 30
        teeth = 8
        points = []
        for i in range(teeth * 2):
            angle = math.radians(i * 360 / (teeth * 2) - 90)
            r = r_outer if i % 2 == 0 else r_inner
            points.append((cx + r * math.cos(angle), cy + r * math.sin(angle)))
        draw.polygon(points, outline=light, width=3)
        draw.ellipse([cx - 15, cy - 15, cx + 15, cy + 15], outline=color, width=3)

    elif shape == "link":
        # Chain link icon
        draw.arc([cx - 50, cy - 20, cx, cy + 20], 90, 270, fill=light, width=3)
        draw.line([(cx - 25, cy - 20), (cx + 10, cy - 20)], fill=light, width=3)
        draw.line([(cx - 25, cy + 20), (cx + 10, cy + 20)], fill=light, width=3)
        draw.arc([cx, cy - 20, cx + 50, cy + 20], 270, 90, fill=color, width=3)
        draw.line([(cx - 10, cy - 20), (cx + 25, cy - 20)], fill=color, width=3)
        draw.line([(cx - 10, cy + 20), (cx + 25, cy + 20)], fill=color, width=3)

    elif shape == "star":
        # 5-point star
        points = []
        for i in range(10):
            angle = math.radians(i * 36 - 90)
            r = 50 if i % 2 == 0 else 22
            points.append((cx + r * math.cos(angle), cy + r * math.sin(angle)))
        draw.polygon(points, outline=light, width=3, fill=color)


def generate_thumbnail(product):
    """Generate a single 600x600 square product thumbnail."""
    img = create_gradient(WIDTH, HEIGHT, product["gradient"][0], product["gradient"][1])
    draw = ImageDraw.Draw(img)
    accent = product["accent"]

    # Subtle diagonal lines
    for i in range(-HEIGHT, WIDTH + HEIGHT, 35):
        draw.line([(i, 0), (i + HEIGHT, HEIGHT)], fill=(255, 255, 255, 8), width=1)

    # --- Top: "AI PROMPT PACK" label ---
    font_label = ImageFont.truetype(FONT_REGULAR, 16)
    label_text = "AI PROMPT PACK"
    if product["filename"].startswith("04"):
        label_text = "AI PROMPT PACK BUNDLE"
    label_bbox = draw.textbbox((0, 0), label_text, font=font_label)
    label_w = label_bbox[2] - label_bbox[0]
    draw.text(((WIDTH - label_w) // 2, 50), label_text, fill=accent, font=font_label)

    # Accent line
    line_w = 80
    draw.rectangle([(WIDTH - line_w) // 2, 75, (WIDTH + line_w) // 2, 78], fill=accent)

    # --- Icon centered ---
    draw_icon_shape(draw, product["icon_shape"], accent, WIDTH // 2, 150)

    # --- Prompt count badge ---
    font_count = ImageFont.truetype(FONT_BOLD, 20)
    count_text = f"{product['prompt_count']} PROMPTS"
    count_bbox = draw.textbbox((0, 0), count_text, font=font_count)
    count_w = count_bbox[2] - count_bbox[0]
    badge_w = count_w + 30
    badge_x = (WIDTH - badge_w) // 2
    draw_rounded_rect(draw, (badge_x, 210, badge_x + badge_w, 240), radius=10,
                      fill=(*accent, ))
    draw.text((badge_x + 15, 213), count_text, fill=(255, 255, 255), font=font_count)

    # --- Title centered ---
    font_title = ImageFont.truetype(FONT_BOLD, 48)
    title_lines = product["title"].split("\n")
    y_pos = 260
    for line in title_lines:
        bbox = draw.textbbox((0, 0), line, font=font_title)
        tw = bbox[2] - bbox[0]
        draw.text(((WIDTH - tw) // 2, y_pos), line, fill=(255, 255, 255), font=font_title)
        y_pos += 58

    # --- Subtitle centered ---
    font_sub = ImageFont.truetype(FONT_REGULAR, 18)
    sub_lines = product["subtitle"].split("\n")
    y_pos += 10
    for line in sub_lines:
        bbox = draw.textbbox((0, 0), line, font=font_sub)
        sw = bbox[2] - bbox[0]
        draw.text(((WIDTH - sw) // 2, y_pos), line, fill=(200, 200, 220), font=font_sub)
        y_pos += 28

    # --- Price badge centered ---
    font_price = ImageFont.truetype(FONT_BOLD, 40)
    price_text = product["price"]
    price_bbox = draw.textbbox((0, 0), price_text, font=font_price)
    price_w = price_bbox[2] - price_bbox[0]
    badge_w = price_w + 50
    badge_h = 58
    badge_x = (WIDTH - badge_w) // 2
    badge_y = 480
    draw_rounded_rect(draw, (badge_x, badge_y, badge_x + badge_w, badge_y + badge_h),
                      radius=14, fill=accent)
    draw.text((badge_x + 25, badge_y + 6), price_text, fill=(255, 255, 255), font=font_price)

    # --- Bottom bar ---
    bar_y = HEIGHT - 50
    draw.rectangle([0, bar_y, WIDTH, HEIGHT], fill=(0, 0, 0, 80))
    font_bottom = ImageFont.truetype(FONT_REGULAR, 15)
    bottom_text = "AI Prompts  |  Instant Download  |  Any LLM"
    bb = draw.textbbox((0, 0), bottom_text, font=font_bottom)
    bw = bb[2] - bb[0]
    draw.text(((WIDTH - bw) // 2, bar_y + 16), bottom_text,
              fill=(180, 180, 200), font=font_bottom)

    # Save
    output_path = os.path.join(OUTPUT_DIR, product["filename"])
    img.save(output_path, "PNG", quality=95)
    print(f"OK: {product['filename']}")
    return output_path


def generate_cover(product):
    """Generate a 1280x720 horizontal cover image."""
    cw, ch = 1280, 720
    img = create_gradient(cw, ch, product["gradient"][0], product["gradient"][1])
    draw = ImageDraw.Draw(img)
    accent = product["accent"]

    # Diagonal lines
    for i in range(-ch, cw + ch, 40):
        draw.line([(i, 0), (i + ch, ch)], fill=(255, 255, 255, 8), width=1)

    # Decorative circles top-right
    for i in range(3):
        r = 80 - i * 20
        x = cw - 150 + i * 30
        y = 80 + i * 25
        draw.ellipse([x - r, y - r, x + r, y + r], outline=(*accent[:3],), width=1)

    # Icon on right side
    draw_icon_shape(draw, product["icon_shape"], accent, cw - 250, 360)

    # Label
    font_label = ImageFont.truetype(FONT_REGULAR, 22)
    label_text = "AI PROMPT PACK"
    if product["filename"].startswith("04"):
        label_text = "AI PROMPT PACK BUNDLE"
    draw.text((80, 80), label_text, fill=accent, font=font_label)
    draw.rectangle([80, 115, 200, 118], fill=accent)

    # Prompt count badge
    font_count = ImageFont.truetype(FONT_BOLD, 24)
    count_text = f"{product['prompt_count']} PROMPTS"
    count_bbox = draw.textbbox((0, 0), count_text, font=font_count)
    count_w = count_bbox[2] - count_bbox[0]
    badge_w = count_w + 30
    draw_rounded_rect(draw, (80, 130, 80 + badge_w, 162), radius=10, fill=accent)
    draw.text((95, 133), count_text, fill=(255, 255, 255), font=font_count)

    # Title
    font_title = ImageFont.truetype(FONT_BOLD, 68)
    title_lines = product["title"].split("\n")
    y_pos = 185
    for line in title_lines:
        draw.text((80, y_pos), line, fill=(255, 255, 255), font=font_title)
        y_pos += 80

    # Subtitle
    font_sub = ImageFont.truetype(FONT_REGULAR, 24)
    sub_lines = product["subtitle"].split("\n")
    y_pos += 15
    for line in sub_lines:
        draw.text((80, y_pos), line, fill=(200, 200, 220), font=font_sub)
        y_pos += 35

    # Price badge
    font_price = ImageFont.truetype(FONT_BOLD, 48)
    price_text = product["price"]
    price_bbox = draw.textbbox((0, 0), price_text, font=font_price)
    price_w = price_bbox[2] - price_bbox[0]
    badge_w = price_w + 60
    badge_h = 70
    badge_x = 80
    badge_y = y_pos + 20
    draw_rounded_rect(draw, (badge_x, badge_y, badge_x + badge_w, badge_y + badge_h),
                      radius=15, fill=accent)
    draw.text((badge_x + 30, badge_y + 8), price_text,
              fill=(255, 255, 255), font=font_price)

    # Bottom bar
    bar_y = ch - 60
    draw.rectangle([0, bar_y, cw, ch], fill=(0, 0, 0, 80))
    font_bottom = ImageFont.truetype(FONT_REGULAR, 20)
    draw.text((80, bar_y + 18), "AI Prompts  |  Instant Download  |  Works with Any LLM",
              fill=(180, 180, 200), font=font_bottom)

    # Save
    cover_name = product["filename"].replace(".png", "-cover.png")
    output_path = os.path.join(OUTPUT_DIR, cover_name)
    img.save(output_path, "PNG", quality=95)
    print(f"OK: {cover_name}")
    return output_path


if __name__ == "__main__":
    print(f"Generating {len(PRODUCTS)} thumbnails + covers...")
    print(f"Output: {OUTPUT_DIR}\n")

    for product in PRODUCTS:
        generate_thumbnail(product)
        generate_cover(product)

    print(f"\nDone! {len(PRODUCTS) * 2} images saved to {OUTPUT_DIR}")
