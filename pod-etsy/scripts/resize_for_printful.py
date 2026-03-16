"""
Resize designs for Printful product specifications.

Input:  ../designs/generated/{niche}/*.png
Output: ../designs/printful-ready/{product-type}/{niche}/*.png

Resizes each design to fit Printful's required dimensions while maintaining
aspect ratio and adding transparent padding where needed.
"""
from PIL import Image
from pathlib import Path
import sys

BASE_DIR = Path(__file__).parent.parent
INPUT_DIR = BASE_DIR / 'designs' / 'generated'
OUTPUT_DIR = BASE_DIR / 'designs' / 'printful-ready'

# Printful product specifications
PRODUCT_SPECS = {
    'tshirt': {
        'width': 4500,
        'height': 5400,
        'dpi': 300,
        'description': 'T-shirt (DTG)',
    },
    'mug-11oz': {
        'width': 2700,
        'height': 1050,
        'dpi': 150,
        'description': 'Mug 11oz (wrap)',
    },
    'poster-18x24': {
        'width': 5400,
        'height': 7200,
        'dpi': 300,
        'description': 'Poster 18x24 inch',
    },
}


def resize_and_pad(img: Image.Image, target_w: int, target_h: int) -> Image.Image:
    """
    Resize image to fit within target dimensions, maintaining aspect ratio.
    Centers the image on a transparent canvas of the target size.
    """
    # Ensure RGBA for transparency
    if img.mode != 'RGBA':
        img = img.convert('RGBA')

    orig_w, orig_h = img.size
    ratio = min(target_w / orig_w, target_h / orig_h)

    new_w = int(orig_w * ratio)
    new_h = int(orig_h * ratio)

    # High-quality resize
    resized = img.resize((new_w, new_h), Image.LANCZOS)

    # Create transparent canvas and paste centered
    canvas = Image.new('RGBA', (target_w, target_h), (0, 0, 0, 0))
    offset_x = (target_w - new_w) // 2
    offset_y = (target_h - new_h) // 2
    canvas.paste(resized, (offset_x, offset_y), resized)

    return canvas


def process_all():
    """Process all generated designs for all product types."""
    # Find all niche directories
    niche_dirs = [d for d in INPUT_DIR.iterdir() if d.is_dir()]

    if not niche_dirs:
        print(f'[ERROR] No niche directories found in {INPUT_DIR}')
        print('  Run generate_designs.py first.')
        sys.exit(1)

    total = 0

    for product_type, spec in PRODUCT_SPECS.items():
        print(f'\n=== {spec["description"]} ({spec["width"]}x{spec["height"]} @ {spec["dpi"]} DPI) ===')

        for niche_dir in sorted(niche_dirs):
            niche_name = niche_dir.name
            out_dir = OUTPUT_DIR / product_type / niche_name
            out_dir.mkdir(parents=True, exist_ok=True)

            png_files = sorted(niche_dir.glob('*.png'))
            if not png_files:
                continue

            print(f'  {niche_name}: {len(png_files)} files')

            for png_file in png_files:
                out_path = out_dir / png_file.name

                if out_path.exists():
                    print(f'    SKIP: {png_file.name}')
                    continue

                try:
                    img = Image.open(png_file)
                    result = resize_and_pad(img, spec['width'], spec['height'])

                    # Save with DPI metadata
                    result.save(
                        str(out_path),
                        'PNG',
                        dpi=(spec['dpi'], spec['dpi']),
                    )
                    print(f'    OK: {png_file.name}')
                    total += 1

                except Exception as e:
                    print(f'    ERROR: {png_file.name} - {e}')

    print(f'\nDone! Processed {total} images.')
    print(f'Output: {OUTPUT_DIR}')


if __name__ == '__main__':
    process_all()
