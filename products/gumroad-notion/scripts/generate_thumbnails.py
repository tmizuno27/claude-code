"""
Gumroad Product Thumbnail Generator
Generates 1280x720 professional thumbnails for all Gumroad products.
Output: products/gumroad-notion/thumbnails/
"""

import os
import re
import json
import textwrap
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

# ------------------------------------------------------------------ #
# Config
# ------------------------------------------------------------------ #

BASE_DIR = Path(__file__).parent.parent
OUTPUT_DIR = BASE_DIR / "thumbnails"
OUTPUT_DIR.mkdir(exist_ok=True)

WIDTH, HEIGHT = 1280, 720

# Font paths
FONT_DIR = Path("C:/Windows/Fonts")
FONT_BOLD = str(FONT_DIR / "segoeuib.ttf")
FONT_REGULAR = str(FONT_DIR / "segoeui.ttf")
FONT_LIGHT = str(FONT_DIR / "segoeuil.ttf")

# ------------------------------------------------------------------ #
# Product definitions
# ------------------------------------------------------------------ #

PRODUCTS = [
    # --- AI Prompt Packs ---
    {
        "slug": "ai-business-automation-mega-prompt-pack",
        "name": "AI Business Automation\nMega Prompt Pack",
        "subtitle": "AI Prompt Pack • 50+ Prompts",
        "category": "prompt",
        "accent": "#6C63FF",
    },
    {
        "slug": "social-media-marketing-mega-prompt-pack",
        "name": "Social Media Marketing\nMega Prompt Pack",
        "subtitle": "AI Prompt Pack • 55 Prompts",
        "category": "prompt",
        "accent": "#E91E8C",
    },
    {
        "slug": "seo-article-writer-mega-prompt-pack",
        "name": "SEO Article Writer\nMega Prompt Pack",
        "subtitle": "AI Prompt Pack • 50 Prompts",
        "category": "prompt",
        "accent": "#0EA5E9",
    },
    {
        "slug": "affiliate-content-generator",
        "name": "Affiliate Content Generator",
        "subtitle": "AI Prompt Pack • 50 Prompts",
        "category": "prompt",
        "accent": "#10B981",
    },
    {
        "slug": "wordpress-automation-prompt-kit",
        "name": "WordPress Automation\nPrompt Kit",
        "subtitle": "AI Prompt Pack • 30 Prompts + Code Snippets",
        "category": "prompt",
        "accent": "#F59E0B",
    },
    # --- Bundles ---
    {
        "slug": "ultimate-ai-blogger-bundle",
        "name": "Ultimate AI Blogger Bundle",
        "subtitle": "3 Prompt Packs • 130+ Prompts • 66% OFF",
        "category": "bundle",
        "accent": "#8B5CF6",
    },
    {
        "slug": "ai-side-hustle-starter-kit",
        "name": "AI Side Hustle Starter Kit",
        "subtitle": "Notion Template + AI Prompt Pack",
        "category": "bundle",
        "accent": "#EC4899",
    },
    {
        "slug": "ultimate-notion-template-bundle",
        "name": "Ultimate Notion\nTemplate Bundle",
        "subtitle": "All 10 Templates • 66% OFF",
        "category": "bundle",
        "accent": "#7C3AED",
    },
    # --- Notion Templates ---
    {
        "slug": "adhd-daily-planner",
        "name": "ADHD Daily Planner",
        "subtitle": "Notion Template",
        "category": "notion",
        "accent": "#06B6D4",
    },
    {
        "slug": "airbnb-host-management-hub",
        "name": "Airbnb Host\nManagement Hub",
        "subtitle": "Notion Template",
        "category": "notion",
        "accent": "#FF5A5F",
    },
    {
        "slug": "personal-finance-dashboard",
        "name": "Personal Finance Dashboard",
        "subtitle": "Notion Template",
        "category": "notion",
        "accent": "#22C55E",
    },
    {
        "slug": "habit-tracker-goal-system",
        "name": "Habit Tracker & Goal System",
        "subtitle": "Notion Template",
        "category": "notion",
        "accent": "#F97316",
    },
    {
        "slug": "travel-planner-journal",
        "name": "Travel Planner & Journal",
        "subtitle": "Notion Template",
        "category": "notion",
        "accent": "#14B8A6",
    },
    {
        "slug": "property-investment-tracker",
        "name": "Property Investment Tracker",
        "subtitle": "Notion Template",
        "category": "notion",
        "accent": "#3B82F6",
    },
    {
        "slug": "wedding-planning-hub",
        "name": "Wedding Planning Hub",
        "subtitle": "Notion Template",
        "category": "notion",
        "accent": "#F43F5E",
    },
    {
        "slug": "startup-launch-checklist",
        "name": "Startup Launch Checklist",
        "subtitle": "Notion Template",
        "category": "notion",
        "accent": "#8B5CF6",
    },
    {
        "slug": "digital-products-os",
        "name": "Digital Products OS",
        "subtitle": "Notion Template • Build, Launch & Scale",
        "category": "notion",
        "accent": "#0EA5E9",
    },
    {
        "slug": "book-learning-tracker",
        "name": "Book & Learning Tracker",
        "subtitle": "Notion Template",
        "category": "notion",
        "accent": "#A855F7",
    },
    {
        "slug": "job-search-tracker",
        "name": "Job Search Tracker",
        "subtitle": "Notion Template",
        "category": "notion",
        "accent": "#64748B",
    },
    {
        "slug": "social-media-planner-scheduler",
        "name": "Social Media Planner\n& Scheduler",
        "subtitle": "Notion Template",
        "category": "notion",
        "accent": "#EC4899",
    },
    {
        "slug": "side-hustle-tracker",
        "name": "Side Hustle Tracker",
        "subtitle": "Notion Template",
        "category": "notion",
        "accent": "#10B981",
    },
    {
        "slug": "small-business-crm",
        "name": "Small Business CRM",
        "subtitle": "Notion Template",
        "category": "notion",
        "accent": "#F59E0B",
    },
    {
        "slug": "life-os",
        "name": "Life OS",
        "subtitle": "Notion Template • Your Complete Second Brain",
        "category": "notion",
        "accent": "#6366F1",
    },
    {
        "slug": "student-study-hub",
        "name": "Student Study Hub",
        "subtitle": "Notion Template",
        "category": "notion",
        "accent": "#06B6D4",
    },
    {
        "slug": "content-creator-dashboard",
        "name": "Content Creator Dashboard",
        "subtitle": "Notion Template",
        "category": "notion",
        "accent": "#F97316",
    },
    {
        "slug": "freelance-business-os",
        "name": "Freelance Business OS",
        "subtitle": "Notion Template",
        "category": "notion",
        "accent": "#8B5CF6",
    },
    # --- n8n Templates ---
    {
        "slug": "n8n-ai-blog-content-pipeline",
        "name": "AI Blog Content Pipeline",
        "subtitle": "n8n Template • Automation Workflow",
        "category": "n8n",
        "accent": "#EA4C89",
    },
    {
        "slug": "n8n-shopify-order-automation",
        "name": "Shopify Order Automation",
        "subtitle": "n8n Template • Automation Workflow",
        "category": "n8n",
        "accent": "#96BF48",
    },
    {
        "slug": "n8n-pdf-invoice-data-extraction",
        "name": "PDF & Invoice\nData Extraction",
        "subtitle": "n8n Template • Automation Workflow",
        "category": "n8n",
        "accent": "#E67E22",
    },
    {
        "slug": "n8n-email-classification-auto-routing",
        "name": "Email Classification\n& Auto-Routing",
        "subtitle": "n8n Template • Automation Workflow",
        "category": "n8n",
        "accent": "#3498DB",
    },
    {
        "slug": "n8n-crm-pipeline-automation",
        "name": "CRM Pipeline Automation",
        "subtitle": "n8n Template • Automation Workflow",
        "category": "n8n",
        "accent": "#2ECC71",
    },
    {
        "slug": "n8n-social-media-content-factory",
        "name": "Social Media\nContent Factory",
        "subtitle": "n8n Template • Automation Workflow",
        "category": "n8n",
        "accent": "#9B59B6",
    },
    {
        "slug": "n8n-ai-customer-support-agent",
        "name": "AI Customer Support Agent",
        "subtitle": "n8n Template • Automation Workflow",
        "category": "n8n",
        "accent": "#1ABC9C",
    },
    {
        "slug": "n8n-ai-lead-gen-cold-outreach",
        "name": "AI Lead Gen &\nCold Outreach Automation",
        "subtitle": "n8n Template • Automation Workflow",
        "category": "n8n",
        "accent": "#E74C3C",
    },
    {
        "slug": "n8n-quickbooks-stripe-invoice-automation",
        "name": "QuickBooks & Stripe\nInvoice Automation",
        "subtitle": "n8n Template • Automation Workflow",
        "category": "n8n",
        "accent": "#F39C12",
    },
]

# ------------------------------------------------------------------ #
# Color palettes per category
# ------------------------------------------------------------------ #

BG_COLORS = {
    "prompt":  [(18, 10, 45), (45, 20, 90)],
    "bundle":  [(12, 8, 35), (50, 18, 85)],
    "notion":  [(8, 18, 50), (20, 40, 90)],
    "n8n":     [(10, 28, 25), (18, 55, 45)],
}

# ------------------------------------------------------------------ #
# Drawing helpers
# ------------------------------------------------------------------ #

def hex_to_rgb(hex_color: str) -> tuple:
    h = hex_color.lstrip("#")
    return tuple(int(h[i:i+2], 16) for i in (0, 2, 4))


def draw_gradient_bg(img: Image.Image, color1: tuple, color2: tuple) -> None:
    """Fill image with a vertical linear gradient."""
    draw = ImageDraw.Draw(img)
    for y in range(HEIGHT):
        t = y / HEIGHT
        r = int(color1[0] + (color2[0] - color1[0]) * t)
        g = int(color1[1] + (color2[1] - color1[1]) * t)
        b = int(color1[2] + (color2[2] - color1[2]) * t)
        draw.line([(0, y), (WIDTH, y)], fill=(r, g, b))


def draw_decorative_shapes(draw: ImageDraw.ImageDraw, accent_rgb: tuple) -> None:
    """Draw glowing geometric decoration."""
    ar, ag, ab = accent_rgb

    # Glow circle — top-right corner
    cx, cy = WIDTH - 80, -60
    for r in range(260, 0, -10):
        alpha = max(0, int(90 * (1 - r / 270)))
        draw.ellipse([cx - r, cy - r, cx + r, cy + r],
                     fill=(ar, ag, ab, alpha))

    # Glow circle — bottom-left corner
    cx2, cy2 = 60, HEIGHT + 40
    for r in range(180, 0, -10):
        alpha = max(0, int(70 * (1 - r / 190)))
        draw.ellipse([cx2 - r, cy2 - r, cx2 + r, cy2 + r],
                     fill=(ar, ag, ab, alpha))

    # Accent bar — left edge (thick, vivid)
    bar_h = 220
    bar_y = (HEIGHT - bar_h) // 2
    draw.rectangle([0, bar_y, 8, bar_y + bar_h], fill=(ar, ag, ab, 255))
    # Subtle inner glow of the bar
    draw.rectangle([8, bar_y + 20, 18, bar_y + bar_h - 20], fill=(ar, ag, ab, 80))


def draw_grid_dots(draw: ImageDraw.ImageDraw) -> None:
    """Draw subtle dot-grid background texture."""
    for x in range(80, WIDTH, 60):
        for y in range(60, HEIGHT, 60):
            draw.ellipse([x - 1, y - 1, x + 1, y + 1], fill=(255, 255, 255, 30))


def load_font(path: str, size: int) -> ImageFont.FreeTypeFont:
    try:
        return ImageFont.truetype(path, size)
    except Exception:
        return ImageFont.truetype(str(FONT_DIR / "arial.ttf"), size)


def draw_multiline_centered(
    draw: ImageDraw.ImageDraw,
    text: str,
    font: ImageFont.FreeTypeFont,
    fill: tuple,
    center_x: int,
    start_y: int,
    line_spacing: int = 8,
) -> int:
    """Draw multi-line text centered horizontally. Returns bottom y position."""
    lines = text.split("\n")
    y = start_y
    for line in lines:
        bbox = draw.textbbox((0, 0), line, font=font)
        w = bbox[2] - bbox[0]
        draw.text((center_x - w // 2, y), line, font=font, fill=fill)
        y += (bbox[3] - bbox[1]) + line_spacing
    return y


def draw_category_badge(
    draw: ImageDraw.ImageDraw,
    label: str,
    accent_rgb: tuple,
    center_x: int,
    y: int,
    font: ImageFont.FreeTypeFont,
) -> None:
    """Draw a rounded pill badge."""
    ar, ag, ab = accent_rgb
    bbox = draw.textbbox((0, 0), label, font=font)
    tw = bbox[2] - bbox[0]
    th = bbox[3] - bbox[1]
    pad_x, pad_y = 20, 8
    rx0 = center_x - tw // 2 - pad_x
    ry0 = y - pad_y
    rx1 = center_x + tw // 2 + pad_x
    ry1 = y + th + pad_y
    # Badge background
    draw.rounded_rectangle([rx0, ry0, rx1, ry1], radius=20,
                            fill=(ar, ag, ab, 200))
    # Badge text
    draw.text((center_x - tw // 2, y), label, font=font, fill=(255, 255, 255, 255))


# ------------------------------------------------------------------ #
# Main thumbnail generator
# ------------------------------------------------------------------ #

CATEGORY_LABELS = {
    "prompt": "AI Prompt Pack",
    "bundle": "Bundle",
    "notion": "Notion Template",
    "n8n":    "n8n Automation",
}


def generate_thumbnail(product: dict) -> Path:
    category = product["category"]
    accent_rgb = hex_to_rgb(product["accent"])
    bg_colors = BG_COLORS.get(category, [(10, 10, 20), (30, 30, 60)])

    # --- Base layer: gradient ---
    img = Image.new("RGBA", (WIDTH, HEIGHT), (0, 0, 0, 255))
    draw_gradient_bg(img, bg_colors[0], bg_colors[1])

    # --- Decoration layer (RGBA for alpha) ---
    overlay = Image.new("RGBA", (WIDTH, HEIGHT), (0, 0, 0, 0))
    ov_draw = ImageDraw.Draw(overlay)
    draw_grid_dots(ov_draw)
    draw_decorative_shapes(ov_draw, accent_rgb)
    img = Image.alpha_composite(img, overlay)

    # --- Text layer ---
    draw = ImageDraw.Draw(img)

    center_x = WIDTH // 2

    # Category badge (top)
    badge_font = load_font(FONT_REGULAR, 22)
    badge_label = CATEGORY_LABELS.get(category, "Digital Product")
    badge_y = 120
    draw_category_badge(draw, badge_label, accent_rgb, center_x, badge_y, badge_font)

    # Main title
    title_font = load_font(FONT_BOLD, 68)
    title_lines = product["name"].split("\n")
    line_heights = []
    for line in title_lines:
        bb = draw.textbbox((0, 0), line, font=title_font)
        line_heights.append(bb[3] - bb[1])
    total_title_h = sum(line_heights) + 12 * (len(line_heights) - 1)
    title_start_y = (HEIGHT - total_title_h) // 2 - 30

    # Shadow
    shadow_offset = 3
    for line in title_lines:
        bb = draw.textbbox((0, 0), line, font=title_font)
        lw = bb[2] - bb[0]
        draw.text((center_x - lw // 2 + shadow_offset,
                   title_start_y + shadow_offset),
                  line, font=title_font, fill=(0, 0, 0, 100))

    # Title text
    y_cursor = title_start_y
    for i, line in enumerate(title_lines):
        bb = draw.textbbox((0, 0), line, font=title_font)
        lw = bb[2] - bb[0]
        lh = bb[3] - bb[1]
        draw.text((center_x - lw // 2, y_cursor),
                  line, font=title_font, fill=(255, 255, 255, 255))
        y_cursor += lh + 12

    # Accent divider line
    divider_y = y_cursor + 20
    ar, ag, ab = accent_rgb
    draw.rectangle([center_x - 60, divider_y, center_x + 60, divider_y + 3],
                   fill=(ar, ag, ab, 220))

    # Subtitle
    subtitle_font = load_font(FONT_REGULAR, 30)
    subtitle_y = divider_y + 18
    sub_bb = draw.textbbox((0, 0), product["subtitle"], font=subtitle_font)
    sw = sub_bb[2] - sub_bb[0]
    draw.text((center_x - sw // 2, subtitle_y),
              product["subtitle"], font=subtitle_font,
              fill=(220, 220, 240, 240))

    # Bottom brand strip
    brand_font = load_font(FONT_LIGHT, 22)
    brand_text = "gumroad.com  •  Digital Products by tmizuno27"
    bb = draw.textbbox((0, 0), brand_text, font=brand_font)
    bw = bb[2] - bb[0]
    draw.text((center_x - bw // 2, HEIGHT - 45),
              brand_text, font=brand_font, fill=(150, 150, 150, 180))

    # --- Save as PNG ---
    out_path = OUTPUT_DIR / f"{product['slug']}.png"
    img.convert("RGB").save(out_path, "PNG", quality=95)
    return out_path


# ------------------------------------------------------------------ #
# Entry point
# ------------------------------------------------------------------ #

def main():
    print(f"Generating {len(PRODUCTS)} thumbnails -> {OUTPUT_DIR}")
    success = 0
    for product in PRODUCTS:
        try:
            path = generate_thumbnail(product)
            print(f"  [OK] {path.name}")
            success += 1
        except Exception as e:
            print(f"  [ERR] {product['slug']}: {e}")
    print(f"\nDone: {success}/{len(PRODUCTS)} thumbnails saved to {OUTPUT_DIR}")


if __name__ == "__main__":
    main()
