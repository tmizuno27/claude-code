"""
X Profile Image Generator for Productivity HQ
Profile: 400x400px / Banner: 1500x500px
"""

from PIL import Image, ImageDraw, ImageFont
import os

OUTPUT_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "images")
os.makedirs(OUTPUT_DIR, exist_ok=True)

FONT_BOLD = "C:/Windows/Fonts/segoeuib.ttf"
FONT_REGULAR = "C:/Windows/Fonts/segoeui.ttf"


def create_gradient(width, height, color1, color2):
    img = Image.new("RGB", (width, height))
    pixels = img.load()
    for y in range(height):
        for x in range(width):
            t = (x / width * 0.4) + (y / height * 0.6)
            r = int(color1[0] + (color2[0] - color1[0]) * t)
            g = int(color1[1] + (color2[1] - color1[1]) * t)
            b = int(color1[2] + (color2[2] - color1[2]) * t)
            pixels[x, y] = (r, g, b)
    return img


def generate_profile_icon():
    """400x400 profile icon - bold 'P' with accent circle."""
    W, H = 400, 400
    # Dark gradient background
    img = create_gradient(W, H, (15, 20, 40), (30, 45, 80))
    draw = ImageDraw.Draw(img)

    accent = (70, 160, 255)

    # Outer circle
    margin = 30
    draw.ellipse([margin, margin, W - margin, H - margin], outline=accent, width=6)

    # Inner accent arc (decorative)
    draw.arc([margin + 20, margin + 20, W - margin - 20, H - margin - 20], 220, 320, fill=accent, width=3)

    # Bold "P" letter
    font_p = ImageFont.truetype(FONT_BOLD, 200)
    bbox = draw.textbbox((0, 0), "P", font=font_p)
    pw = bbox[2] - bbox[0]
    ph = bbox[3] - bbox[1]
    draw.text(((W - pw) // 2 + 5, 40), "P", fill=(255, 255, 255), font=font_p)

    # Small "HQ" below with clear gap
    font_hq = ImageFont.truetype(FONT_BOLD, 50)
    bbox_hq = draw.textbbox((0, 0), "HQ", font=font_hq)
    hqw = bbox_hq[2] - bbox_hq[0]
    draw.text(((W - hqw) // 2, 265), "HQ", fill=accent, font=font_hq)

    path = os.path.join(OUTPUT_DIR, "x-profile-icon-v2.png")
    img.save(path, "PNG", quality=95)
    print(f"OK: x-profile-icon.png (400x400)")


def generate_banner():
    """1500x500 banner image."""
    W, H = 1500, 500
    img = create_gradient(W, H, (15, 20, 40), (35, 50, 90))
    draw = ImageDraw.Draw(img)

    accent = (70, 160, 255)

    # Diagonal lines (subtle texture)
    for i in range(-H, W + H, 50):
        draw.line([(i, 0), (i + H, H)], fill=(255, 255, 255, 10), width=1)

    # Decorative circles (right side)
    for i in range(4):
        r = 120 - i * 25
        x = W - 200 + i * 40
        y = H // 2 - 30 + i * 20
        draw.ellipse([x - r, y - r, x + r, y + r], outline=(*accent,), width=2)

    # Main text
    font_title = ImageFont.truetype(FONT_BOLD, 80)
    draw.text((100, 100), "Productivity HQ", fill=(255, 255, 255), font=font_title)

    # Accent line
    draw.rectangle([100, 200, 500, 206], fill=accent)

    # Subtitle
    font_sub = ImageFont.truetype(FONT_REGULAR, 36)
    draw.text((100, 230), "Notion Templates  |  Automation Workflows  |  Digital Tools", fill=(180, 190, 220), font=font_sub)

    # Tagline
    font_tag = ImageFont.truetype(FONT_REGULAR, 28)
    draw.text((100, 310), "Free yourself from busywork.", fill=accent, font=font_tag)

    # Bottom bar
    draw.rectangle([0, H - 8, W, H], fill=accent)

    path = os.path.join(OUTPUT_DIR, "x-banner.png")
    img.save(path, "PNG", quality=95)
    print(f"OK: x-banner.png (1500x500)")


if __name__ == "__main__":
    generate_profile_icon()
    generate_banner()
    print("\nDone!")
