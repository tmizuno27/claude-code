"""
Upscale stock images to meet platform requirements.
Adobe Stock: min 4MP (2000x2000+)
Freepik: 2000-10000px per side

Strategy for seamless patterns:
1. Tile 2x2 (1024→2048) then Lanczos upscale to 4096
   This preserves seamless quality better than pure upscale.
"""
import os
import sys
from PIL import Image

BASE_DIR = os.path.dirname(os.path.dirname(__file__))
INPUT_DIR = os.path.join(BASE_DIR, "output", "images")
OUTPUT_DIR = os.path.join(BASE_DIR, "output", "upscaled")
TARGET_SIZE = 4096  # 4096x4096 = 16.7MP (well above 4MP minimum)


def tile_and_upscale(img, target):
    """Tile 2x2 then upscale to target size."""
    w, h = img.size
    # Create 2x2 tiled version (doubles resolution naturally)
    tiled = Image.new(img.mode, (w * 2, h * 2))
    tiled.paste(img, (0, 0))
    tiled.paste(img, (w, 0))
    tiled.paste(img, (0, h))
    tiled.paste(img, (w, h))
    # Upscale from 2048 to target using Lanczos
    if tiled.size[0] != target:
        tiled = tiled.resize((target, target), Image.LANCZOS)
    return tiled


def upscale_all(method="tile"):
    """Upscale all images in the input directory."""
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    files = sorted([f for f in os.listdir(INPUT_DIR) if f.endswith(".png")])
    print(f"Upscaling {len(files)} images to {TARGET_SIZE}x{TARGET_SIZE}")
    print(f"Method: {'2x2 tile + Lanczos' if method == 'tile' else 'Direct Lanczos'}")
    print(f"Output: {OUTPUT_DIR}\n")

    success = 0
    for i, fname in enumerate(files):
        src = os.path.join(INPUT_DIR, fname)
        # Output as JPEG for stock sites (smaller file, widely accepted)
        out_name = fname.replace(".png", ".jpg")
        dst = os.path.join(OUTPUT_DIR, out_name)

        try:
            img = Image.open(src).convert("RGB")

            if method == "tile":
                result = tile_and_upscale(img, TARGET_SIZE)
            else:
                result = img.resize((TARGET_SIZE, TARGET_SIZE), Image.LANCZOS)

            # Save as high-quality JPEG (stock sites prefer JPEG)
            result.save(dst, "JPEG", quality=95, subsampling=0)
            size_mb = os.path.getsize(dst) / (1024 * 1024)
            print(f"[{i+1}/{len(files)}] {out_name} ({size_mb:.1f} MB)")
            success += 1
        except Exception as e:
            print(f"[{i+1}/{len(files)}] FAIL {fname}: {e}")

    print(f"\nDone: {success}/{len(files)} upscaled")
    total_mb = sum(
        os.path.getsize(os.path.join(OUTPUT_DIR, f)) / (1024 * 1024)
        for f in os.listdir(OUTPUT_DIR) if f.endswith(".jpg")
    )
    print(f"Total size: {total_mb:.0f} MB")


if __name__ == "__main__":
    method = sys.argv[1] if len(sys.argv) > 1 else "tile"
    upscale_all(method=method)
