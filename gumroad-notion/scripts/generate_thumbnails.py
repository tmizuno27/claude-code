"""
Gumroad Notion テンプレート サムネイル自動生成スクリプト
600x600px 正方形, グラデーション背景, モダンデザイン
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
        "filename": "01-freelance-business-os.png",
        "title": "Freelance\nBusiness OS",
        "subtitle": "Clients · Projects · Invoices · Revenue\nAll in One Place",
        "price": "$19",
        "gradient": [(30, 30, 80), (80, 40, 120)],
        "accent": (140, 100, 255),
        "icon_shape": "briefcase",
    },
    {
        "filename": "02-content-creator-dashboard.png",
        "title": "Content Creator\nDashboard",
        "subtitle": "Plan · Create · Track · Grow\nAcross All Platforms",
        "price": "$15",
        "gradient": [(20, 20, 70), (60, 20, 100)],
        "accent": (180, 80, 255),
        "icon_shape": "play",
    },
    {
        "filename": "03-student-study-hub.png",
        "title": "Student\nStudy Hub",
        "subtitle": "Courses · Assignments · Notes · GPA\nYour Academic Command Center",
        "price": "$9",
        "gradient": [(15, 40, 70), (20, 80, 120)],
        "accent": (60, 180, 255),
        "icon_shape": "book",
    },
    {
        "filename": "04-life-os-second-brain.png",
        "title": "Life OS\nSecond Brain",
        "subtitle": "Goals · Habits · Finance · Health\nYour Entire Life, Organized",
        "price": "$19",
        "gradient": [(40, 25, 60), (90, 30, 80)],
        "accent": (255, 100, 180),
        "icon_shape": "brain",
    },
    {
        "filename": "05-small-business-crm.png",
        "title": "Small Business\nCRM",
        "subtitle": "Contacts · Deals · Pipeline · Revenue\nClose More, Stress Less",
        "price": "$17",
        "gradient": [(15, 50, 50), (20, 90, 80)],
        "accent": (50, 220, 180),
        "icon_shape": "handshake",
    },
    {
        "filename": "06-side-hustle-tracker.png",
        "title": "Side Hustle\nTracker",
        "subtitle": "Ideas · Revenue · Expenses · Growth\nTurn Side Projects into Income",
        "price": "$12",
        "gradient": [(60, 30, 10), (100, 50, 20)],
        "accent": (255, 170, 50),
        "icon_shape": "rocket",
    },
    {
        "filename": "07-social-media-planner.png",
        "title": "Social Media\nPlanner",
        "subtitle": "Schedule · Create · Analyze · Grow\nAll Platforms, One Dashboard",
        "price": "$14",
        "gradient": [(50, 15, 50), (100, 20, 70)],
        "accent": (255, 80, 130),
        "icon_shape": "phone",
    },
    {
        "filename": "08-job-search-tracker.png",
        "title": "Job Search\nTracker",
        "subtitle": "Applications · Interviews · Contacts · Offers\nLand Your Dream Job",
        "price": "$9",
        "gradient": [(15, 35, 60), (30, 60, 100)],
        "accent": (80, 160, 255),
        "icon_shape": "target",
    },
    {
        "filename": "09-book-learning-tracker.png",
        "title": "Book & Learning\nTracker",
        "subtitle": "Reading List · Notes · Highlights · Goals\nNever Forget What You Read",
        "price": "$9",
        "gradient": [(40, 30, 15), (70, 50, 25)],
        "accent": (220, 180, 80),
        "icon_shape": "openbook",
    },
    {
        "filename": "10-digital-products-os.png",
        "title": "Digital Products\nBusiness OS",
        "subtitle": "Products · Sales · Marketing · Analytics\nScale Your Digital Empire",
        "price": "$19",
        "gradient": [(20, 40, 40), (30, 70, 70)],
        "accent": (60, 220, 200),
        "icon_shape": "diamond",
    },
    {
        "filename": "bundle-all-10.png",
        "title": "Ultimate Bundle\nAll 10 Templates",
        "subtitle": "10 Premium Notion Templates\n66% OFF — Save $93",
        "price": "$49",
        "gradient": [(40, 15, 60), (80, 20, 40)],
        "accent": (255, 200, 60),
        "icon_shape": "star",
    },
    # ─── Product Factory 新商品（2026-03-20） ───
    {
        "filename": "11-startup-launch-checklist.png",
        "title": "Startup Launch\nChecklist",
        "subtitle": "Idea → MVP → Launch → Growth\nStep by Step",
        "price": "$12",
        "gradient": [(15, 15, 35), (26, 26, 62)],
        "accent": (108, 99, 255),
        "icon_shape": "rocket",
    },
    {
        "filename": "12-wedding-planning-hub.png",
        "title": "Wedding\nPlanning Hub",
        "subtitle": "Guests · Budget · Vendors · Timeline\nYour Dream Wedding, Organized",
        "price": "$17",
        "gradient": [(60, 30, 40), (90, 50, 60)],
        "accent": (255, 160, 180),
        "icon_shape": "star",
    },
    {
        "filename": "13-property-investment-tracker.png",
        "title": "Property\nInvestment Tracker",
        "subtitle": "Portfolio · Income · ROI · Tenants\nBuild Wealth with Real Estate",
        "price": "$19",
        "gradient": [(10, 35, 30), (20, 60, 50)],
        "accent": (46, 204, 113),
        "icon_shape": "diamond",
    },
    {
        "filename": "14-travel-planner-journal.png",
        "title": "Travel Planner\n& Journal",
        "subtitle": "Itineraries · Packing · Budget · Journal\nExplore the World, Organized",
        "price": "$12",
        "gradient": [(15, 40, 50), (30, 70, 80)],
        "accent": (80, 200, 220),
        "icon_shape": "target",
    },
    {
        "filename": "15-habit-tracker-goal-system.png",
        "title": "Habit Tracker\n& Goal System",
        "subtitle": "Daily Habits · Streaks · OKRs · Reviews\nBuild the Life You Want",
        "price": "$9",
        "gradient": [(15, 30, 50), (25, 55, 70)],
        "accent": (60, 200, 180),
        "icon_shape": "target",
    },
    {
        "filename": "16-personal-finance-dashboard.png",
        "title": "Personal Finance\nDashboard",
        "subtitle": "Income · Expenses · Savings · Net Worth\nTake Control of Your Money",
        "price": "$14",
        "gradient": [(20, 30, 50), (35, 50, 80)],
        "accent": (100, 180, 255),
        "icon_shape": "briefcase",
    },
    {
        "filename": "17-airbnb-host-management-hub.png",
        "title": "Airbnb Host\nManagement Hub",
        "subtitle": "Listings · Bookings · Cleaning · Revenue\nHost Like a Pro",
        "price": "$17",
        "gradient": [(40, 15, 20), (70, 25, 35)],
        "accent": (255, 90, 95),
        "icon_shape": "handshake",
    },
    {
        "filename": "18-ai-side-hustle-starter-kit.png",
        "title": "AI Side Hustle\nStarter Kit",
        "subtitle": "50 AI Prompts + Notion Templates\nStart Earning with AI Today",
        "price": "$19",
        "gradient": [(30, 15, 60), (60, 25, 90)],
        "accent": (200, 120, 255),
        "icon_shape": "brain",
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


def add_decorative_elements(draw, accent, width, height):
    """Add subtle geometric decorations."""
    # Top-right circle cluster
    for i in range(3):
        r = 80 - i * 20
        alpha_color = (*accent, 25 + i * 10)
        x = width - 150 + i * 30
        y = 80 + i * 25
        draw.ellipse([x - r, y - r, x + r, y + r],
                     outline=(*accent[:3],), width=1)

    # Bottom-left decorative lines
    for i in range(5):
        y = height - 120 + i * 15
        line_len = 60 - i * 8
        draw.line([(60, y), (60 + line_len, y)],
                  fill=(*accent[:3],), width=2)


def draw_icon_shape(draw, shape, accent, width, height):
    """Draw a geometric icon on the right side of the thumbnail."""
    cx, cy = width // 2, 170
    color = (*accent,)
    light = (255, 255, 255)

    if shape == "briefcase":
        # Briefcase shape
        draw.rounded_rectangle([cx-55, cy-35, cx+55, cy+40], radius=8, outline=light, width=3)
        draw.rounded_rectangle([cx-20, cy-50, cx+20, cy-35], radius=5, outline=light, width=3)
        draw.line([(cx-55, cy), (cx+55, cy)], fill=light, width=2)

    elif shape == "play":
        # Play button / clapperboard
        draw.rounded_rectangle([cx-50, cy-45, cx+50, cy+45], radius=6, outline=light, width=3)
        draw.polygon([(cx-15, cy-25), (cx-15, cy+25), (cx+25, cy)], fill=color)

    elif shape == "book":
        # Stack of books
        for i in range(3):
            y_off = -30 + i * 25
            draw.rounded_rectangle([cx-45, cy+y_off, cx+45, cy+y_off+20], radius=4, outline=light, width=2, fill=None)
        draw.line([(cx-30, cy-30), (cx-30, cy+35)], fill=color, width=2)

    elif shape == "brain":
        # Abstract brain - two connected hemispheres
        draw.arc([cx-50, cy-40, cx, cy+40], 90, 270, fill=light, width=3)
        draw.arc([cx, cy-40, cx+50, cy+40], 270, 90, fill=light, width=3)
        draw.arc([cx-35, cy-50, cx+5, cy-10], 200, 340, fill=color, width=2)
        draw.arc([cx-5, cy-50, cx+35, cy-10], 200, 340, fill=color, width=2)
        draw.arc([cx-35, cy+10, cx+5, cy+50], 20, 160, fill=color, width=2)
        draw.arc([cx-5, cy+10, cx+35, cy+50], 20, 160, fill=color, width=2)

    elif shape == "handshake":
        # Two connected arrows / handshake
        draw.arc([cx-50, cy-30, cx, cy+30], 180, 0, fill=light, width=3)
        draw.arc([cx, cy-30, cx+50, cy+30], 0, 180, fill=light, width=3)
        draw.line([(cx-50, cy), (cx+50, cy)], fill=color, width=2)

    elif shape == "rocket":
        # Rocket shape
        draw.polygon([(cx, cy-55), (cx-25, cy+15), (cx+25, cy+15)], outline=light, width=3)
        draw.polygon([(cx-25, cy+5), (cx-45, cy+35), (cx-20, cy+15)], fill=color)
        draw.polygon([(cx+25, cy+5), (cx+45, cy+35), (cx+20, cy+15)], fill=color)
        draw.ellipse([cx-8, cy+15, cx+8, cy+40], fill=color)

    elif shape == "phone":
        # Smartphone
        draw.rounded_rectangle([cx-25, cy-50, cx+25, cy+50], radius=8, outline=light, width=3)
        draw.line([(cx-25, cy-35), (cx+25, cy-35)], fill=light, width=2)
        draw.line([(cx-25, cy+35), (cx+25, cy+35)], fill=light, width=2)
        draw.ellipse([cx-5, cy+38, cx+5, cy+48], outline=light, width=2)

    elif shape == "target":
        # Target / bullseye
        for r in [45, 30, 15]:
            draw.ellipse([cx-r, cy-r, cx+r, cy+r], outline=light, width=2)
        draw.ellipse([cx-6, cy-6, cx+6, cy+6], fill=color)

    elif shape == "openbook":
        # Open book
        draw.arc([cx-50, cy-10, cx, cy+50], 180, 0, fill=light, width=3)
        draw.arc([cx, cy-10, cx+50, cy+50], 180, 0, fill=light, width=3)
        draw.line([(cx, cy-30), (cx, cy+50)], fill=light, width=2)
        draw.line([(cx-50, cy+20), (cx-10, cy-10)], fill=color, width=2)
        draw.line([(cx+50, cy+20), (cx+10, cy-10)], fill=color, width=2)

    elif shape == "diamond":
        # Diamond gem
        draw.polygon([(cx, cy-50), (cx+45, cy-5), (cx, cy+50), (cx-45, cy-5)], outline=light, width=3)
        draw.line([(cx-45, cy-5), (cx+45, cy-5)], fill=color, width=2)
        draw.line([(cx, cy-50), (cx-15, cy-5)], fill=color, width=2)
        draw.line([(cx, cy-50), (cx+15, cy-5)], fill=color, width=2)
        draw.line([(cx-15, cy-5), (cx, cy+50)], fill=color, width=1)
        draw.line([(cx+15, cy-5), (cx, cy+50)], fill=color, width=1)

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
        draw.line([(i, 0), (i + HEIGHT, HEIGHT)],
                  fill=(255, 255, 255, 8), width=1)

    # --- Top: Icon centered ---
    draw_icon_shape(draw, product["icon_shape"], accent, WIDTH, HEIGHT)

    # --- "NOTION TEMPLATE" label ---
    font_label = ImageFont.truetype(FONT_REGULAR, 16)
    label_text = "NOTION TEMPLATE"
    if product["filename"].startswith("bundle"):
        label_text = "NOTION TEMPLATE BUNDLE"
    label_bbox = draw.textbbox((0, 0), label_text, font=font_label)
    label_w = label_bbox[2] - label_bbox[0]
    draw.text(((WIDTH - label_w) // 2, 50), label_text, fill=accent, font=font_label)

    # Accent line
    line_w = 80
    draw.rectangle([(WIDTH - line_w) // 2, 75, (WIDTH + line_w) // 2, 78], fill=accent)

    # --- Title centered ---
    font_title = ImageFont.truetype(FONT_BOLD, 52)
    title_lines = product["title"].split("\n")
    y_pos = 260
    for line in title_lines:
        bbox = draw.textbbox((0, 0), line, font=font_title)
        tw = bbox[2] - bbox[0]
        draw.text(((WIDTH - tw) // 2, y_pos), line, fill=(255, 255, 255), font=font_title)
        y_pos += 62

    # --- Subtitle centered ---
    font_sub = ImageFont.truetype(FONT_REGULAR, 20)
    sub_lines = product["subtitle"].split("\n")
    y_pos += 10
    for line in sub_lines:
        bbox = draw.textbbox((0, 0), line, font=font_sub)
        sw = bbox[2] - bbox[0]
        draw.text(((WIDTH - sw) // 2, y_pos), line, fill=(200, 200, 220), font=font_sub)
        y_pos += 30

    # --- Price badge centered ---
    font_price = ImageFont.truetype(FONT_BOLD, 40)
    price_text = product["price"]
    price_bbox = draw.textbbox((0, 0), price_text, font=font_price)
    price_w = price_bbox[2] - price_bbox[0]
    badge_w = price_w + 50
    badge_h = 58
    badge_x = (WIDTH - badge_w) // 2
    badge_y = 480

    draw_rounded_rect(draw,
                      (badge_x, badge_y, badge_x + badge_w, badge_y + badge_h),
                      radius=14, fill=accent)
    draw.text((badge_x + 25, badge_y + 6), price_text,
              fill=(255, 255, 255), font=font_price)

    # --- Bottom bar ---
    bar_y = HEIGHT - 50
    draw.rectangle([0, bar_y, WIDTH, HEIGHT], fill=(0, 0, 0, 80))

    font_bottom = ImageFont.truetype(FONT_REGULAR, 15)
    bottom_text = "Notion Template  |  Instant Access  |  Free Plan OK"
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
        draw.line([(i, 0), (i + ch, ch)],
                  fill=(255, 255, 255, 8), width=1)

    # Decorative circles top-right
    for i in range(3):
        r = 80 - i * 20
        x = cw - 150 + i * 30
        y = 80 + i * 25
        draw.ellipse([x - r, y - r, x + r, y + r],
                     outline=(*accent[:3],), width=1)

    # Icon on right side
    draw_icon_shape(draw, product["icon_shape"], accent, cw + 340, 460)

    # Label
    font_label = ImageFont.truetype(FONT_REGULAR, 22)
    label_text = "NOTION TEMPLATE"
    if product["filename"].startswith("bundle"):
        label_text = "NOTION TEMPLATE BUNDLE"
    draw.text((80, 80), label_text, fill=accent, font=font_label)
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
    price_text = product["price"]
    price_bbox = draw.textbbox((0, 0), price_text, font=font_price)
    price_w = price_bbox[2] - price_bbox[0]
    badge_w = price_w + 60
    badge_h = 70
    badge_x = 80
    badge_y = y_pos + 20

    draw_rounded_rect(draw,
                      (badge_x, badge_y, badge_x + badge_w, badge_y + badge_h),
                      radius=15, fill=accent)
    draw.text((badge_x + 30, badge_y + 8), price_text,
              fill=(255, 255, 255), font=font_price)

    # Bottom bar
    bar_y = ch - 60
    draw.rectangle([0, bar_y, cw, ch], fill=(0, 0, 0, 80))
    font_bottom = ImageFont.truetype(FONT_REGULAR, 20)
    draw.text((80, bar_y + 18), "Notion Template  |  Instant Access  |  Free Plan Compatible",
              fill=(180, 180, 200), font=font_bottom)
    font_notion = ImageFont.truetype(FONT_BOLD, 22)
    draw.text((cw - 180, bar_y + 18), "N  Notion",
              fill=(255, 255, 255), font=font_notion)

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
