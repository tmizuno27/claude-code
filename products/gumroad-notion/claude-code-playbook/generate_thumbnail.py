"""
Generate thumbnail and cover images for the Claude Code Automation Playbook.
Outputs:
  - cover (1280x720) for Gumroad product page
  - thumbnail (600x600) for Gumroad grid
"""

from PIL import Image, ImageDraw, ImageFont
import os

OUTPUT_DIR = os.path.join(os.path.dirname(__file__), "..", "images")


def get_font(size: int) -> ImageFont.FreeTypeFont:
    """Try common system fonts, fall back to default."""
    candidates = [
        "C:/Windows/Fonts/segoeui.ttf",
        "C:/Windows/Fonts/arial.ttf",
        "C:/Windows/Fonts/calibri.ttf",
        "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
        "/System/Library/Fonts/Helvetica.ttc",
    ]
    for path in candidates:
        if os.path.exists(path):
            return ImageFont.truetype(path, size)
    return ImageFont.load_default()


def get_bold_font(size: int) -> ImageFont.FreeTypeFont:
    """Try common bold system fonts."""
    candidates = [
        "C:/Windows/Fonts/segoeuib.ttf",
        "C:/Windows/Fonts/arialbd.ttf",
        "C:/Windows/Fonts/calibrib.ttf",
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
    ]
    for path in candidates:
        if os.path.exists(path):
            return ImageFont.truetype(path, size)
    return get_font(size)


def draw_rounded_rect(draw, xy, radius, fill):
    """Draw a rounded rectangle."""
    x0, y0, x1, y1 = xy
    draw.rectangle([x0 + radius, y0, x1 - radius, y1], fill=fill)
    draw.rectangle([x0, y0 + radius, x1, y1 - radius], fill=fill)
    draw.pieslice([x0, y0, x0 + 2 * radius, y0 + 2 * radius], 180, 270, fill=fill)
    draw.pieslice([x1 - 2 * radius, y0, x1, y0 + 2 * radius], 270, 360, fill=fill)
    draw.pieslice([x0, y1 - 2 * radius, x0 + 2 * radius, y1], 90, 180, fill=fill)
    draw.pieslice([x1 - 2 * radius, y1 - 2 * radius, x1, y1], 0, 90, fill=fill)


def create_cover(output_path: str):
    """Create 1280x720 cover image."""
    width, height = 1280, 720

    # Dark gradient background
    img = Image.new("RGB", (width, height), "#0f0f23")
    draw = ImageDraw.Draw(img)

    # Decorative gradient stripes
    for i in range(height):
        r = int(15 + (i / height) * 20)
        g = int(15 + (i / height) * 15)
        b = int(35 + (i / height) * 40)
        draw.line([(0, i), (width, i)], fill=(r, g, b))

    # Accent line at top
    draw.rectangle([0, 0, width, 6], fill="#7c3aed")

    # Decorative dots pattern (top right)
    for row in range(8):
        for col in range(8):
            x = 900 + col * 30
            y = 80 + row * 30
            opacity = max(40, 120 - (row + col) * 10)
            draw.ellipse([x, y, x + 4, y + 4], fill=(124, 58, 237, opacity))

    # Terminal-style code block decoration (right side)
    draw_rounded_rect(draw, (820, 350, 1220, 600), 12, "#1a1a3e")
    draw.rectangle([820, 350, 1220, 385], fill="#252550")
    # Terminal dots
    draw.ellipse([835, 360, 847, 372], fill="#ff5f57")
    draw.ellipse([855, 360, 867, 372], fill="#ffbd2e")
    draw.ellipse([875, 360, 887, 372], fill="#28c840")

    code_font = get_font(16)
    code_lines = [
        ("$ claude", "#a78bfa"),
        ("", "#666"),
        ("> Automate SEO workflow", "#10b981"),
        ("  Researching keywords...", "#6b7280"),
        ("  Generating article...", "#6b7280"),
        ("  Publishing to WP...", "#6b7280"),
        ("  Scheduling social...", "#6b7280"),
        ('  Done. 4 tasks in 2m.', "#10b981"),
    ]
    for i, (line, color) in enumerate(code_lines):
        draw.text((845, 400 + i * 24), line, fill=color, font=code_font)

    # Main title
    title_font = get_bold_font(52)
    subtitle_font = get_font(28)
    badge_font = get_bold_font(18)
    small_font = get_font(20)

    # Badge
    draw_rounded_rect(draw, (60, 100, 340, 138), 16, "#7c3aed")
    draw.text((80, 105), "CLAUDE CODE PLAYBOOK", fill="white", font=badge_font)

    # Title
    draw.text((60, 170), "Automate Your", fill="white", font=title_font)
    draw.text((60, 235), "Entire Business", fill="#a78bfa", font=title_font)
    draw.text((60, 300), "with AI", fill="white", font=title_font)

    # Subtitle
    draw.text(
        (60, 390),
        "20+ ready-to-use prompts for SEO,",
        fill="#9ca3af",
        font=subtitle_font,
    )
    draw.text(
        (60, 425),
        "content, WordPress, products & more",
        fill="#9ca3af",
        font=subtitle_font,
    )

    # Feature pills
    features = ["SEO", "WordPress", "Products", "Analytics", "Social"]
    x_pos = 60
    for feat in features:
        bbox = draw.textbbox((0, 0), feat, font=small_font)
        fw = bbox[2] - bbox[0]
        draw_rounded_rect(
            draw, (x_pos, 500, x_pos + fw + 28, 533), 14, "#1e1e3f"
        )
        draw.text((x_pos + 14, 504), feat, fill="#a78bfa", font=small_font)
        x_pos += fw + 44

    # Price badge
    price_font = get_bold_font(32)
    draw_rounded_rect(draw, (60, 580, 220, 640), 16, "#10b981")
    draw.text((82, 588), "$19.99", fill="white", font=price_font)

    # Bottom accent line
    draw.rectangle([0, 714, width, 720], fill="#7c3aed")

    img.save(output_path, quality=95)
    print(f"Cover saved: {output_path}")


def create_thumbnail(output_path: str):
    """Create 600x600 thumbnail image."""
    size = 600
    img = Image.new("RGB", (size, size), "#0f0f23")
    draw = ImageDraw.Draw(img)

    # Gradient background
    for i in range(size):
        r = int(15 + (i / size) * 25)
        g = int(15 + (i / size) * 15)
        b = int(35 + (i / size) * 45)
        draw.line([(0, i), (size, i)], fill=(r, g, b))

    # Top accent
    draw.rectangle([0, 0, size, 5], fill="#7c3aed")

    title_font = get_bold_font(38)
    sub_font = get_font(22)
    badge_font = get_bold_font(16)
    price_font = get_bold_font(28)

    # Badge
    draw_rounded_rect(draw, (40, 60, 280, 95), 14, "#7c3aed")
    draw.text((58, 65), "CLAUDE CODE PLAYBOOK", fill="white", font=badge_font)

    # Title
    draw.text((40, 130), "Automate", fill="white", font=title_font)
    draw.text((40, 178), "Your Entire", fill="#a78bfa", font=title_font)
    draw.text((40, 226), "Business", fill="white", font=title_font)

    # Subtitle
    draw.text((40, 300), "20+ Business Prompts", fill="#9ca3af", font=sub_font)
    draw.text((40, 330), "SEO | WordPress | Products", fill="#6b7280", font=sub_font)

    # Mini terminal
    draw_rounded_rect(draw, (40, 385, 560, 510), 10, "#1a1a3e")
    draw.rectangle([40, 385, 560, 412], fill="#252550")
    draw.ellipse([55, 392, 65, 402], fill="#ff5f57")
    draw.ellipse([72, 392, 82, 402], fill="#ffbd2e")
    draw.ellipse([89, 392, 99, 402], fill="#28c840")
    mini_font = get_font(15)
    draw.text((60, 420), "$ claude", fill="#a78bfa", font=mini_font)
    draw.text((60, 442), "> Automate everything...", fill="#10b981", font=mini_font)
    draw.text((60, 464), '  Done. 4 tasks in 2m.', fill="#10b981", font=mini_font)

    # Price
    draw_rounded_rect(draw, (40, 535, 170, 575), 14, "#10b981")
    draw.text((58, 540), "$19.99", fill="white", font=price_font)

    # Bottom accent
    draw.rectangle([0, 595, size, 600], fill="#7c3aed")

    img.save(output_path, quality=95)
    print(f"Thumbnail saved: {output_path}")


def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    cover_path = os.path.join(OUTPUT_DIR, "claude-code-playbook-cover.png")
    thumb_path = os.path.join(OUTPUT_DIR, "claude-code-playbook-thumb.png")
    create_cover(cover_path)
    create_thumbnail(thumb_path)
    print("All images generated.")


if __name__ == "__main__":
    main()
