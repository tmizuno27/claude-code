"""
n8n テンプレート サムネイル・Cover自動生成スクリプト
Thumbnail: 600x600px正方形 / Cover: 1280x720px横長
"""

from PIL import Image, ImageDraw, ImageFont
import os
import math

OUTPUT_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "images")
os.makedirs(OUTPUT_DIR, exist_ok=True)

FONT_BOLD = "C:/Windows/Fonts/segoeuib.ttf"
FONT_REGULAR = "C:/Windows/Fonts/segoeui.ttf"

PRODUCTS = [
    {
        "filename": "01-ai-blog-content-pipeline.png",
        "title": "AI Blog Content\nPipeline",
        "subtitle": "Research + Write + Publish\nFully Automated SEO Articles",
        "price": "$49",
        "gradient": [(20, 35, 65), (40, 70, 120)],
        "accent": (70, 160, 255),
        "icon_shape": "pencil",
    },
    {
        "filename": "02-shopify-order-automation.png",
        "title": "Shopify Order\nAutomation",
        "subtitle": "Orders + Inventory + Emails\nZero Manual Fulfillment",
        "price": "$59",
        "gradient": [(20, 50, 30), (40, 100, 50)],
        "accent": (80, 200, 100),
        "icon_shape": "cart",
    },
    {
        "filename": "03-pdf-invoice-extraction.png",
        "title": "PDF & Invoice\nData Extraction",
        "subtitle": "PDF to Spreadsheet + QuickBooks\nAI-Powered OCR Pipeline",
        "price": "$79",
        "gradient": [(50, 25, 25), (100, 40, 40)],
        "accent": (255, 100, 100),
        "icon_shape": "document",
    },
    {
        "filename": "04-email-classification.png",
        "title": "Email Classification\n& Auto-Routing",
        "subtitle": "AI Sorts Every Email\nUrgent + Client + Invoice + Spam",
        "price": "$49",
        "gradient": [(25, 25, 55), (50, 40, 100)],
        "accent": (150, 120, 255),
        "icon_shape": "envelope",
    },
    {
        "filename": "05-crm-pipeline-automation.png",
        "title": "CRM Pipeline\nAutomation",
        "subtitle": "Forms to HubSpot + AI Lead Scoring\nAuto-Route Hot Leads",
        "price": "$69",
        "gradient": [(15, 45, 55), (25, 80, 90)],
        "accent": (50, 210, 200),
        "icon_shape": "funnel",
    },
    {
        "filename": "06-social-media-factory.png",
        "title": "Social Media\nContent Factory",
        "subtitle": "AI Generates a Full Week\nTwitter + LinkedIn + Instagram",
        "price": "$49",
        "gradient": [(55, 20, 45), (100, 30, 70)],
        "accent": (255, 80, 160),
        "icon_shape": "megaphone",
    },
    {
        "filename": "07-ai-customer-support.png",
        "title": "AI Customer\nSupport Agent",
        "subtitle": "Auto-Classify + Auto-Reply\nEscalate When Needed",
        "price": "$99",
        "gradient": [(30, 30, 50), (60, 50, 90)],
        "accent": (200, 150, 255),
        "icon_shape": "headset",
    },
    {
        "filename": "08-ai-lead-gen.png",
        "title": "AI Lead Gen &\nCold Outreach",
        "subtitle": "Find + Research + Email + Follow Up\nFull Sales Autopilot",
        "price": "$79",
        "gradient": [(50, 30, 10), (90, 55, 20)],
        "accent": (255, 180, 50),
        "icon_shape": "lightning",
    },
    {
        "filename": "09-quickbooks-stripe.png",
        "title": "QuickBooks &\nStripe Invoice",
        "subtitle": "Auto-Sync Payments\nZero Manual Bookkeeping",
        "price": "$69",
        "gradient": [(15, 40, 35), (30, 75, 60)],
        "accent": (60, 220, 170),
        "icon_shape": "dollar",
    },
]


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


def draw_icon_shape(draw, shape, accent, cx, cy):
    color = (*accent,)
    light = (255, 255, 255)

    if shape == "pencil":
        draw.polygon([(cx-5, cy-50), (cx+5, cy-50), (cx+15, cy+30), (cx-15, cy+30)], outline=light, width=2)
        draw.polygon([(cx-15, cy+30), (cx+15, cy+30), (cx, cy+50)], fill=color)
        draw.line([(cx-10, cy-20), (cx+10, cy-20)], fill=light, width=2)

    elif shape == "cart":
        draw.arc([cx-40, cy-20, cx+40, cy+40], 0, 180, fill=light, width=3)
        draw.line([(cx-50, cy-30), (cx-35, cy-30), (cx-25, cy+20), (cx+25, cy+20), (cx+35, cy-30), (cx+50, cy-30)], fill=light, width=3)
        draw.ellipse([cx-20, cy+25, cx-10, cy+35], fill=color)
        draw.ellipse([cx+10, cy+25, cx+20, cy+35], fill=color)

    elif shape == "document":
        draw.rounded_rectangle([cx-30, cy-45, cx+30, cy+45], radius=5, outline=light, width=3)
        draw.polygon([(cx+10, cy-45), (cx+30, cy-25), (cx+10, cy-25)], outline=light, width=2)
        for i in range(4):
            draw.line([(cx-18, cy-10+i*15), (cx+18, cy-10+i*15)], fill=color, width=2)

    elif shape == "envelope":
        draw.rounded_rectangle([cx-45, cy-25, cx+45, cy+30], radius=5, outline=light, width=3)
        draw.line([(cx-45, cy-25), (cx, cy+5), (cx+45, cy-25)], fill=light, width=2)

    elif shape == "funnel":
        draw.polygon([(cx-45, cy-40), (cx+45, cy-40), (cx+10, cy+10), (cx+10, cy+45), (cx-10, cy+45), (cx-10, cy+10)], outline=light, width=3)
        draw.line([(cx-30, cy-20), (cx+30, cy-20)], fill=color, width=2)

    elif shape == "megaphone":
        draw.polygon([(cx-40, cy-10), (cx+20, cy-40), (cx+20, cy+40), (cx-40, cy+10)], outline=light, width=3)
        draw.rounded_rectangle([cx-45, cy-10, cx-35, cy+10], radius=3, fill=color)
        draw.arc([cx+15, cy-30, cx+45, cy+30], 300, 60, fill=color, width=3)

    elif shape == "headset":
        draw.arc([cx-35, cy-35, cx+35, cy+20], 180, 0, fill=light, width=3)
        draw.rounded_rectangle([cx-45, cy-10, cx-30, cy+20], radius=5, fill=color)
        draw.rounded_rectangle([cx+30, cy-10, cx+45, cy+20], radius=5, fill=color)
        draw.arc([cx-15, cy+15, cx+15, cy+40], 0, 180, fill=light, width=2)

    elif shape == "lightning":
        draw.polygon([(cx-5, cy-50), (cx+25, cy-50), (cx+5, cy-5), (cx+30, cy-5), (cx-15, cy+50), (cx, cy+5), (cx-25, cy+5)], fill=color, outline=light, width=2)

    elif shape == "dollar":
        draw.ellipse([cx-35, cy-35, cx+35, cy+35], outline=light, width=3)
        font_dollar = ImageFont.truetype(FONT_BOLD, 45)
        bbox = draw.textbbox((0, 0), "$", font=font_dollar)
        dw = bbox[2] - bbox[0]
        dh = bbox[3] - bbox[1]
        draw.text((cx - dw // 2, cy - dh // 2 - 5), "$", fill=color, font=font_dollar)


def generate_thumbnail(product):
    """Generate 600x600 square thumbnail."""
    W, H = 600, 600
    img = create_gradient(W, H, product["gradient"][0], product["gradient"][1])
    draw = ImageDraw.Draw(img)
    accent = product["accent"]

    for i in range(-H, W + H, 35):
        draw.line([(i, 0), (i + H, H)], fill=(255, 255, 255, 8), width=1)

    # Label
    font_label = ImageFont.truetype(FONT_REGULAR, 16)
    label_text = "n8n WORKFLOW TEMPLATE"
    label_bbox = draw.textbbox((0, 0), label_text, font=font_label)
    label_w = label_bbox[2] - label_bbox[0]
    draw.text(((W - label_w) // 2, 50), label_text, fill=accent, font=font_label)
    draw.rectangle([(W - 80) // 2, 75, (W + 80) // 2, 78], fill=accent)

    # Icon
    draw_icon_shape(draw, product["icon_shape"], accent, W // 2, 170)

    # Title
    font_title = ImageFont.truetype(FONT_BOLD, 48)
    title_lines = product["title"].split("\n")
    y_pos = 260
    for line in title_lines:
        bbox = draw.textbbox((0, 0), line, font=font_title)
        tw = bbox[2] - bbox[0]
        draw.text(((W - tw) // 2, y_pos), line, fill=(255, 255, 255), font=font_title)
        y_pos += 58

    # Subtitle
    font_sub = ImageFont.truetype(FONT_REGULAR, 18)
    sub_lines = product["subtitle"].split("\n")
    y_pos += 10
    for line in sub_lines:
        bbox = draw.textbbox((0, 0), line, font=font_sub)
        sw = bbox[2] - bbox[0]
        draw.text(((W - sw) // 2, y_pos), line, fill=(200, 200, 220), font=font_sub)
        y_pos += 28

    # Price badge
    font_price = ImageFont.truetype(FONT_BOLD, 40)
    price_bbox = draw.textbbox((0, 0), product["price"], font=font_price)
    price_w = price_bbox[2] - price_bbox[0]
    badge_w = price_w + 50
    badge_h = 58
    badge_x = (W - badge_w) // 2
    badge_y = 478
    draw_rounded_rect(draw, (badge_x, badge_y, badge_x + badge_w, badge_y + badge_h), radius=14, fill=accent)
    draw.text((badge_x + 25, badge_y + 6), product["price"], fill=(255, 255, 255), font=font_price)

    # Bottom bar
    bar_y = H - 50
    draw.rectangle([0, bar_y, W, H], fill=(0, 0, 0, 80))
    font_bottom = ImageFont.truetype(FONT_REGULAR, 15)
    bottom_text = "n8n Template  |  One-Click Import  |  Setup Guide"
    bb = draw.textbbox((0, 0), bottom_text, font=font_bottom)
    bw = bb[2] - bb[0]
    draw.text(((W - bw) // 2, bar_y + 16), bottom_text, fill=(180, 180, 200), font=font_bottom)

    output_path = os.path.join(OUTPUT_DIR, product["filename"])
    img.save(output_path, "PNG", quality=95)
    print(f"OK: {product['filename']}")


def generate_cover(product):
    """Generate 1280x720 horizontal cover."""
    cw, ch = 1280, 720
    img = create_gradient(cw, ch, product["gradient"][0], product["gradient"][1])
    draw = ImageDraw.Draw(img)
    accent = product["accent"]

    for i in range(-ch, cw + ch, 40):
        draw.line([(i, 0), (i + ch, ch)], fill=(255, 255, 255, 8), width=1)

    # Decorative circles
    for i in range(3):
        r = 80 - i * 20
        x = cw - 150 + i * 30
        y = 80 + i * 25
        draw.ellipse([x - r, y - r, x + r, y + r], outline=(*accent[:3],), width=1)

    # Icon
    draw_icon_shape(draw, product["icon_shape"], accent, cw - 280, 230)

    # Label
    font_label = ImageFont.truetype(FONT_REGULAR, 22)
    draw.text((80, 80), "n8n WORKFLOW TEMPLATE", fill=accent, font=font_label)
    draw.rectangle([80, 115, 200, 118], fill=accent)

    # Title
    font_title = ImageFont.truetype(FONT_BOLD, 72)
    title_lines = product["title"].split("\n")
    y_pos = 145
    for line in title_lines:
        draw.text((80, y_pos), line, fill=(255, 255, 255), font=font_title)
        y_pos += 85

    # Subtitle
    font_sub = ImageFont.truetype(FONT_REGULAR, 26)
    sub_lines = product["subtitle"].split("\n")
    y_pos += 20
    for line in sub_lines:
        draw.text((80, y_pos), line, fill=(200, 200, 220), font=font_sub)
        y_pos += 38

    # Price badge
    font_price = ImageFont.truetype(FONT_BOLD, 48)
    price_bbox = draw.textbbox((0, 0), product["price"], font=font_price)
    price_w = price_bbox[2] - price_bbox[0]
    badge_w = price_w + 60
    badge_h = 70
    draw_rounded_rect(draw, (80, y_pos + 20, 80 + badge_w, y_pos + 20 + badge_h), radius=15, fill=accent)
    draw.text((110, y_pos + 28), product["price"], fill=(255, 255, 255), font=font_price)

    # Bottom bar
    bar_y = ch - 60
    draw.rectangle([0, bar_y, cw, ch], fill=(0, 0, 0, 80))
    font_bottom = ImageFont.truetype(FONT_REGULAR, 20)
    draw.text((80, bar_y + 18), "n8n Workflow Template  |  One-Click Import  |  Setup Guide Included", fill=(180, 180, 200), font=font_bottom)
    font_n8n = ImageFont.truetype(FONT_BOLD, 22)
    draw.text((cw - 140, bar_y + 18), "n8n", fill=(255, 255, 255), font=font_n8n)

    cover_name = product["filename"].replace(".png", "-cover.png")
    output_path = os.path.join(OUTPUT_DIR, cover_name)
    img.save(output_path, "PNG", quality=95)
    print(f"OK: {cover_name}")


if __name__ == "__main__":
    print(f"Generating {len(PRODUCTS)} thumbnails + covers...")
    print(f"Output: {OUTPUT_DIR}\n")

    for product in PRODUCTS:
        generate_thumbnail(product)
        generate_cover(product)

    print(f"\nDone! {len(PRODUCTS) * 2} images saved to {OUTPUT_DIR}")
