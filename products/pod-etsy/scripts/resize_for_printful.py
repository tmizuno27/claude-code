#!/usr/bin/env python3
"""
AsuInk — Printful用デザイン画像リサイズスクリプト

各商品タイプに合わせてデザイン画像をリサイズ・変換する。
Pillowが必要: pip install Pillow

Usage:
    python resize_for_printful.py
    python resize_for_printful.py --input ../designs/images --output ../designs/printful-ready
    python resize_for_printful.py --product tshirt  # Tシャツのみ
"""

import argparse
import shutil
from pathlib import Path

try:
    from PIL import Image
    HAS_PILLOW = True
except ImportError:
    HAS_PILLOW = False
    print("警告: Pillowがインストールされていません。")
    print("インストール: pip install Pillow")

# 商品ごとの仕様
PRODUCT_SPECS = {
    "tshirt": {
        "width": 4500,
        "height": 5400,
        "dpi": 300,
        "format": "PNG",
        "background": (255, 255, 255, 0),  # 透過
        "description": "Tシャツ (Bella+Canvas 3001) フロントプリント",
    },
    "mug_11oz": {
        "width": 2000,
        "height": 900,
        "dpi": 150,
        "format": "PNG",
        "background": (255, 255, 255, 0),
        "description": "マグ 11oz ラップアラウンドプリント",
    },
    "mug_15oz": {
        "width": 2000,
        "height": 1125,
        "dpi": 150,
        "format": "PNG",
        "background": (255, 255, 255, 0),
        "description": "マグ 15oz ラップアラウンドプリント",
    },
    "poster_8x10": {
        "width": 2400,
        "height": 3000,
        "dpi": 300,
        "format": "PNG",
        "background": (255, 255, 255, 255),
        "description": "ポスター 8×10インチ",
    },
    "poster_11x14": {
        "width": 3300,
        "height": 4200,
        "dpi": 300,
        "format": "PNG",
        "background": (255, 255, 255, 255),
        "description": "ポスター 11×14インチ",
    },
    "poster_16x20": {
        "width": 4800,
        "height": 6000,
        "dpi": 300,
        "format": "PNG",
        "background": (255, 255, 255, 255),
        "description": "ポスター 16×20インチ",
    },
    "poster_18x24": {
        "width": 5400,
        "height": 7200,
        "dpi": 300,
        "format": "PNG",
        "background": (255, 255, 255, 255),
        "description": "ポスター 18×24インチ",
    },
    "poster_24x36": {
        "width": 7200,
        "height": 10800,
        "dpi": 300,
        "format": "PNG",
        "background": (255, 255, 255, 255),
        "description": "ポスター 24×36インチ",
    },
}

# デフォルト処理対象（よく使う3サイズ）
DEFAULT_PRODUCTS = ["tshirt", "mug_11oz", "poster_11x14"]


def resize_image(
    source_path: Path,
    output_dir: Path,
    product_key: str,
    spec: dict,
    fit_mode: str = "contain",
) -> Path:
    """
    画像をPrintful仕様にリサイズして保存する。

    fit_mode:
        "contain" — アスペクト比を保って内側に収める（余白あり）
        "cover"   — アスペクト比を保って外側を埋める（クロップあり）
        "stretch" — 強制リサイズ（アスペクト比崩れる可能性あり）
    """
    if not HAS_PILLOW:
        return None

    target_w = spec["width"]
    target_h = spec["height"]
    dpi = spec["dpi"]
    fmt = spec["format"]
    bg_color = spec["background"]

    img = Image.open(source_path)

    # RGBAに変換（透過対応）
    if img.mode != "RGBA":
        img = img.convert("RGBA")

    if fit_mode == "contain":
        # アスペクト比保持でターゲットサイズに収める
        img.thumbnail((target_w, target_h), Image.LANCZOS)
        new_img = Image.new("RGBA", (target_w, target_h), bg_color)
        # センターに配置
        offset_x = (target_w - img.width) // 2
        offset_y = (target_h - img.height) // 2
        new_img.paste(img, (offset_x, offset_y), img)
        img = new_img
    elif fit_mode == "cover":
        # アスペクト比保持でクロップ
        src_ratio = img.width / img.height
        tgt_ratio = target_w / target_h
        if src_ratio > tgt_ratio:
            new_h = target_h
            new_w = int(new_h * src_ratio)
        else:
            new_w = target_w
            new_h = int(new_w / src_ratio)
        img = img.resize((new_w, new_h), Image.LANCZOS)
        left = (img.width - target_w) // 2
        top = (img.height - target_h) // 2
        img = img.crop((left, top, left + target_w, top + target_h))
    else:  # stretch
        img = img.resize((target_w, target_h), Image.LANCZOS)

    # PNGはRGBAのまま保存。JPGに変換する場合はRGBに変換
    if fmt == "JPEG":
        if img.mode == "RGBA":
            background = Image.new("RGB", img.size, (255, 255, 255))
            background.paste(img, mask=img.split()[3])
            img = background

    # 出力パス
    stem = source_path.stem
    suffix = ".png" if fmt == "PNG" else ".jpg"
    output_filename = f"{stem}_{product_key}{suffix}"
    output_path = output_dir / product_key / output_filename
    output_path.parent.mkdir(parents=True, exist_ok=True)

    img.save(output_path, format=fmt, dpi=(dpi, dpi))
    return output_path


def process_all(input_dir: Path, output_dir: Path, products: list[str]):
    if not HAS_PILLOW:
        print("Pillowが必要です: pip install Pillow")
        return

    supported_exts = {".png", ".jpg", ".jpeg", ".webp"}
    image_files = [
        f for f in input_dir.rglob("*")
        if f.suffix.lower() in supported_exts
    ]

    if not image_files:
        print(f"画像ファイルが見つかりません: {input_dir}")
        return

    print(f"処理対象: {len(image_files)}枚 × {len(products)}商品タイプ = {len(image_files)*len(products)}ファイル")

    processed = 0
    errors = 0
    for img_path in image_files:
        for product_key in products:
            if product_key not in PRODUCT_SPECS:
                print(f"不明な商品タイプ: {product_key}")
                continue
            spec = PRODUCT_SPECS[product_key]
            try:
                out = resize_image(img_path, output_dir, product_key, spec)
                if out:
                    print(f"  ✓ {img_path.name} → {product_key} ({spec['width']}x{spec['height']})")
                    processed += 1
            except Exception as e:
                print(f"  ✗ エラー: {img_path.name} / {product_key}: {e}")
                errors += 1

    print(f"\n完了: {processed}件成功, {errors}件エラー")
    print(f"出力先: {output_dir}")


def print_specs():
    print("=== Printful 商品仕様一覧 ===\n")
    for key, spec in PRODUCT_SPECS.items():
        print(f"[{key}] {spec['description']}")
        print(f"  サイズ: {spec['width']} × {spec['height']} px")
        print(f"  DPI: {spec['dpi']}, フォーマット: {spec['format']}\n")


def main():
    parser = argparse.ArgumentParser(description="AsuInk Printfulリサイズツール")
    parser.add_argument("--input", default="../designs/images",
                        help="入力画像ディレクトリ")
    parser.add_argument("--output", default="../designs/printful-ready",
                        help="出力ディレクトリ")
    parser.add_argument("--product", nargs="+",
                        choices=list(PRODUCT_SPECS.keys()) + ["all"],
                        default=DEFAULT_PRODUCTS,
                        help="処理する商品タイプ（デフォルト: tshirt mug_11oz poster_11x14）")
    parser.add_argument("--specs", action="store_true",
                        help="商品仕様一覧を表示")
    args = parser.parse_args()

    if args.specs:
        print_specs()
        return

    input_dir = Path(__file__).parent / args.input
    output_dir = Path(__file__).parent / args.output

    products = args.product
    if "all" in products:
        products = list(PRODUCT_SPECS.keys())

    if not input_dir.exists():
        input_dir.mkdir(parents=True, exist_ok=True)
        print(f"入力ディレクトリを作成しました: {input_dir}")
        print("デザイン画像をこのディレクトリに配置してから再実行してください。")
        return

    process_all(input_dir, output_dir, products)


if __name__ == "__main__":
    main()
