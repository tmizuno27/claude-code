"""
06-AI Business Automation Mega Prompt Pack サムネイル生成
既存シリーズと統一感のあるデザイン（緑〜ティール系）
"""

from PIL import Image, ImageDraw, ImageFont
import os
import math

OUTPUT_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "images")
os.makedirs(OUTPUT_DIR, exist_ok=True)

FONT_BOLD = "C:/Windows/Fonts/segoeuib.ttf"
FONT_REGULAR = "C:/Windows/Fonts/segoeui.ttf"

PRODUCT = {
    "filename": "06-business-automation-pack.png",
    "title": "Business\nAutomation",
    "subtitle": "50+ Prompts to Run Your\nBusiness on Autopilot",
    "price": "$12",
    "prompt_count": "50+",
    "gradient": [(8, 40, 35), (15, 80, 70)],
    "accent": (0, 230, 180),
    "icon_shape": "robot",
}


def create_gradient(width, height, color1, color2):
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
    x0, y0, x1, y1 = xy
    draw.rectangle([x0 + radius, y0, x1 - radius, y1], fill=fill)
    draw.rectangle([x0, y0 + radius, x1, y1 - radius], fill=fill)
    draw.pieslice([x0, y0, x0 + 2 * radius, y0 + 2 * radius], 180, 270, fill=fill)
    draw.pieslice([x1 - 2 * radius, y0, x1, y0 + 2 * radius], 270, 360, fill=fill)
    draw.pieslice([x0, y1 - 2 * radius, x0 + 2 * radius, y1], 90, 180, fill=fill)
    draw.pieslice([x1 - 2 * radius, y1 - 2 * radius, x1, y1], 0, 90, fill=fill)


def draw_robot(draw, accent, cx, cy):
    """Draw a robot/automation icon."""
    light = (255, 255, 255)
    # Robot head
    draw.rounded_rectangle(
        [cx - 30, cy - 35, cx + 30, cy + 10], radius=8, outline=light, width=3
    )
    # Eyes
    draw.ellipse([cx - 18, cy - 22, cx - 8, cy - 12], fill=accent)
    draw.ellipse([cx + 8, cy - 22, cx + 18, cy - 12], fill=accent)
    # Antenna
    draw.line([(cx, cy - 35), (cx, cy - 50)], fill=light, width=3)
    draw.ellipse([cx - 5, cy - 55, cx + 5, cy - 45], fill=accent)
    # Body
    draw.rounded_rectangle(
        [cx - 25, cy + 14, cx + 25, cy + 45], radius=6, outline=light, width=3
    )
    # Gear on body (automation symbol)
    gear_cx, gear_cy = cx, cy + 29
    r_outer = 10
    r_inner = 7
    teeth = 6
    points = []
    for i in range(teeth * 2):
        angle = math.radians(i * 360 / (teeth * 2) - 90)
        r = r_outer if i % 2 == 0 else r_inner
        points.append((gear_cx + r * math.cos(angle), gear_cy + r * math.sin(angle)))
    draw.polygon(points, fill=accent)
    # Circuit lines from sides
    draw.line([(cx - 30, cy - 10), (cx - 45, cy - 10)], fill=accent, width=2)
    draw.line([(cx + 30, cy - 10), (cx + 45, cy - 10)], fill=accent, width=2)
    draw.ellipse([cx - 48, cy - 13, cx - 42, cy - 7], fill=accent)
    draw.ellipse([cx + 42, cy - 13, cx + 48, cy - 7], fill=accent)


def generate_thumbnail(product):
    width, height = 600, 600
    img = create_gradient(width, height, product["gradient"][0], product["gradient"][1])
    draw = ImageDraw.Draw(img)
    accent = product["accent"]

    for i in range(-height, width + height, 35):
        draw.line([(i, 0), (i + height, height)], fill=(255, 255, 255, 8), width=1)

    font_label = ImageFont.truetype(FONT_REGULAR, 16)
    label_text = "AI PROMPT PACK"
    label_bbox = draw.textbbox((0, 0), label_text, font=font_label)
    label_w = label_bbox[2] - label_bbox[0]
    draw.text(((width - label_w) // 2, 50), label_text, fill=accent, font=font_label)

    line_w = 80
    draw.rectangle([(width - line_w) // 2, 75, (width + line_w) // 2, 78], fill=accent)

    draw_robot(draw, accent, width // 2, 150)

    font_count = ImageFont.truetype(FONT_BOLD, 20)
    count_text = f"{product['prompt_count']} PROMPTS"
    count_bbox = draw.textbbox((0, 0), count_text, font=font_count)
    count_w = count_bbox[2] - count_bbox[0]
    badge_w = count_w + 30
    badge_x = (width - badge_w) // 2
    draw_rounded_rect(draw, (badge_x, 210, badge_x + badge_w, 240), radius=10, fill=accent)
    draw.text((badge_x + 15, 213), count_text, fill=(255, 255, 255), font=font_count)

    font_title = ImageFont.truetype(FONT_BOLD, 48)
    title_lines = product["title"].split("\n")
    y_pos = 260
    for line in title_lines:
        bbox = draw.textbbox((0, 0), line, font=font_title)
        tw = bbox[2] - bbox[0]
        draw.text(((width - tw) // 2, y_pos), line, fill=(255, 255, 255), font=font_title)
        y_pos += 58

    font_sub = ImageFont.truetype(FONT_REGULAR, 18)
    sub_lines = product["subtitle"].split("\n")
    y_pos += 10
    for line in sub_lines:
        bbox = draw.textbbox((0, 0), line, font=font_sub)
        sw = bbox[2] - bbox[0]
        draw.text(((width - sw) // 2, y_pos), line, fill=(200, 200, 220), font=font_sub)
        y_pos += 28

    font_price = ImageFont.truetype(FONT_BOLD, 40)
    price_text = product["price"]
    price_bbox = draw.textbbox((0, 0), price_text, font=font_price)
    price_w = price_bbox[2] - price_bbox[0]
    badge_w = price_w + 50
    badge_h = 58
    badge_x = (width - badge_w) // 2
    badge_y = 480
    draw_rounded_rect(draw, (badge_x, badge_y, badge_x + badge_w, badge_y + badge_h),
                      radius=14, fill=accent)
    draw.text((badge_x + 25, badge_y + 6), price_text, fill=(255, 255, 255), font=font_price)

    bar_y = height - 50
    draw.rectangle([0, bar_y, width, height], fill=(0, 0, 0, 80))
    font_bottom = ImageFont.truetype(FONT_REGULAR, 15)
    bottom_text = "AI Prompts  |  Instant Download  |  Any LLM"
    bb = draw.textbbox((0, 0), bottom_text, font=font_bottom)
    bw = bb[2] - bb[0]
    draw.text(((width - bw) // 2, bar_y + 16), bottom_text,
              fill=(180, 180, 200), font=font_bottom)

    output_path = os.path.join(OUTPUT_DIR, product["filename"])
    img.save(output_path, "PNG", quality=95)
    print(f"OK: {product['filename']}")
    return output_path


def generate_cover(product):
    cw, ch = 1280, 720
    img = create_gradient(cw, ch, product["gradient"][0], product["gradient"][1])
    draw = ImageDraw.Draw(img)
    accent = product["accent"]

    for i in range(-ch, cw + ch, 40):
        draw.line([(i, 0), (i + ch, ch)], fill=(255, 255, 255, 8), width=1)

    for i in range(3):
        r = 80 - i * 20
        x = cw - 150 + i * 30
        y = 80 + i * 25
        draw.ellipse([x - r, y - r, x + r, y + r], outline=accent, width=1)

    draw_robot(draw, accent, cw - 250, 360)

    font_label = ImageFont.truetype(FONT_REGULAR, 22)
    draw.text((80, 80), "AI PROMPT PACK", fill=accent, font=font_label)
    draw.rectangle([80, 115, 200, 118], fill=accent)

    font_count = ImageFont.truetype(FONT_BOLD, 24)
    count_text = f"{product['prompt_count']} PROMPTS"
    count_bbox = draw.textbbox((0, 0), count_text, font=font_count)
    count_w = count_bbox[2] - count_bbox[0]
    badge_w = count_w + 30
    draw_rounded_rect(draw, (80, 130, 80 + badge_w, 162), radius=10, fill=accent)
    draw.text((95, 133), count_text, fill=(255, 255, 255), font=font_count)

    font_title = ImageFont.truetype(FONT_BOLD, 68)
    title_lines = product["title"].split("\n")
    y_pos = 185
    for line in title_lines:
        draw.text((80, y_pos), line, fill=(255, 255, 255), font=font_title)
        y_pos += 80

    font_sub = ImageFont.truetype(FONT_REGULAR, 24)
    sub_lines = product["subtitle"].split("\n")
    y_pos += 15
    for line in sub_lines:
        draw.text((80, y_pos), line, fill=(200, 200, 220), font=font_sub)
        y_pos += 35

    font_price = ImageFont.truetype(FONT_BOLD, 48)
    price_bbox = draw.textbbox((0, 0), product["price"], font=font_price)
    price_w = price_bbox[2] - price_bbox[0]
    badge_w = price_w + 60
    badge_h = 70
    badge_x = 80
    badge_y = y_pos + 20
    draw_rounded_rect(draw, (badge_x, badge_y, badge_x + badge_w, badge_y + badge_h),
                      radius=15, fill=accent)
    draw.text((badge_x + 30, badge_y + 8), product["price"],
              fill=(255, 255, 255), font=font_price)

    bar_y = ch - 60
    draw.rectangle([0, bar_y, cw, ch], fill=(0, 0, 0, 80))
    font_bottom = ImageFont.truetype(FONT_REGULAR, 20)
    draw.text((80, bar_y + 18), "AI Prompts  |  Instant Download  |  Works with Any LLM",
              fill=(180, 180, 200), font=font_bottom)

    cover_name = product["filename"].replace(".png", "-cover.png")
    output_path = os.path.join(OUTPUT_DIR, cover_name)
    img.save(output_path, "PNG", quality=95)
    print(f"OK: {cover_name}")
    return output_path


if __name__ == "__main__":
    print("Generating AI Business Automation Pack thumbnails...")
    print(f"Output: {OUTPUT_DIR}\n")
    generate_thumbnail(PRODUCT)
    generate_cover(PRODUCT)
    print("\nDone! 2 images saved.")
