"""
pSEO Starter Kit — Gumroad thumbnail generator
600x600px, dark gradient background, code-themed design
"""

from PIL import Image, ImageDraw, ImageFont
import os

OUTPUT_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "images")
os.makedirs(OUTPUT_DIR, exist_ok=True)

FONT_BOLD = "C:/Windows/Fonts/segoeuib.ttf"
FONT_REGULAR = "C:/Windows/Fonts/segoeui.ttf"

WIDTH, HEIGHT = 600, 600


def draw_gradient(draw: ImageDraw.ImageDraw, color1: tuple, color2: tuple):
    for y in range(HEIGHT):
        ratio = y / HEIGHT
        r = int(color1[0] + (color2[0] - color1[0]) * ratio)
        g = int(color1[1] + (color2[1] - color1[1]) * ratio)
        b = int(color1[2] + (color2[2] - color1[2]) * ratio)
        draw.line([(0, y), (WIDTH, y)], fill=(r, g, b))


def create_thumbnail():
    img = Image.new("RGB", (WIDTH, HEIGHT))
    draw = ImageDraw.Draw(img)

    # Dark blue-to-purple gradient
    draw_gradient(draw, (10, 15, 40), (40, 20, 80))

    # Decorative code lines (faded)
    code_font = ImageFont.truetype(FONT_REGULAR, 11)
    code_lines = [
        "export async function generateStaticParams() {",
        "  const items = await getAllItems();",
        "  return items.map(i => ({ slug: i.slug }));",
        "}",
        "",
        "// 5,000 pages generated at build time",
        "// $0/month hosting on Vercel",
    ]
    for i, line in enumerate(code_lines):
        draw.text(
            (30, 30 + i * 16),
            line,
            fill=(80, 100, 140),
            font=code_font,
        )

    # Main title
    title_font = ImageFont.truetype(FONT_BOLD, 40)
    draw.text((40, 200), "pSEO Site\nBuilder", fill=(255, 255, 255), font=title_font)

    # Subtitle
    sub_font = ImageFont.truetype(FONT_BOLD, 22)
    draw.text(
        (40, 320),
        "Starter Kit",
        fill=(100, 200, 255),
        font=sub_font,
    )

    # Description line
    desc_font = ImageFont.truetype(FONT_REGULAR, 15)
    draw.text(
        (40, 370),
        "Build 1,000+ page SEO sites\nwith Next.js & TypeScript",
        fill=(180, 190, 220),
        font=desc_font,
    )

    # Feature pills
    pill_font = ImageFont.truetype(FONT_REGULAR, 12)
    pills = ["Next.js 16", "TypeScript", "SSG", "Vercel", "$0 hosting"]
    x_offset = 40
    for pill in pills:
        bbox = draw.textbbox((0, 0), pill, font=pill_font)
        pw = bbox[2] - bbox[0] + 16
        if x_offset + pw > WIDTH - 30:
            break
        draw.rounded_rectangle(
            [x_offset, 440, x_offset + pw, 464],
            radius=4,
            fill=(60, 70, 120),
        )
        draw.text((x_offset + 8, 445), pill, fill=(180, 200, 255), font=pill_font)
        x_offset += pw + 8

    # Price
    price_font = ImageFont.truetype(FONT_BOLD, 28)
    draw.text((40, 510), "$29.99", fill=(100, 255, 180), font=price_font)

    # Save
    filename = "pseo-starter-kit.png"
    filepath = os.path.join(OUTPUT_DIR, filename)
    img.save(filepath, "PNG", quality=95)
    print(f"Thumbnail saved: {filepath}")

    # Also save cover version (1280x720 for Gumroad cover)
    cover = img.resize((1280, 720), Image.LANCZOS)
    cover_path = os.path.join(OUTPUT_DIR, "pseo-starter-kit-cover.png")
    cover.save(cover_path, "PNG", quality=95)
    print(f"Cover saved: {cover_path}")


if __name__ == "__main__":
    create_thumbnail()
