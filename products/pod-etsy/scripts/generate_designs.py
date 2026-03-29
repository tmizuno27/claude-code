#!/usr/bin/env python3
"""
AsuInk — Ideogram API を使ったデザイン自動生成スクリプト

Ideogram APIは無料枠あり（月25クレジット）でタイポグラフィ強い。
代替: DALL-E 3 (OpenAI API), Stability AI

Usage:
    pip install requests python-dotenv

    # 環境変数設定
    export IDEOGRAM_API_KEY=your_key_here
    または .env ファイルに IDEOGRAM_API_KEY=xxx を記載

    python generate_designs.py
    python generate_designs.py --design D01 --product tshirt
    python generate_designs.py --niche "Japanese Zen" --dry-run
"""

import json
import time
import argparse
import os
from pathlib import Path

try:
    import requests
    HAS_REQUESTS = True
except ImportError:
    HAS_REQUESTS = False

try:
    from dotenv import load_dotenv
    load_dotenv()
    HAS_DOTENV = True
except ImportError:
    HAS_DOTENV = False


# ============================================================
# 50デザインのIdeogram API用プロンプト（最適化済み）
# ============================================================
DESIGN_PROMPTS = {
    "D01": {
        "name": "Wabi-Sabi Circle",
        "niche": "Japanese Zen",
        "ideogram_prompt": "Minimalist Japanese enso circle brush stroke, black ink on pure white background, authentic sumi-e calligraphy style, small kanji characters wabi-sabi inside circle, ultra-minimal composition, no gradients, professional art print design",
        "negative_prompt": "colorful, complex, busy, photographic, 3d render, text in English",
        "style": "DESIGN",
        "aspect_ratio": "ASPECT_3_4",
    },
    "D02": {
        "name": "Mount Fuji Line Art",
        "niche": "Japanese Zen",
        "ideogram_prompt": "Ultra-minimal single continuous line art of Mount Fuji silhouette, hair-thin black stroke on white background, below the mountain text 'Find Peace in Simplicity' in elegant thin serif font, modern minimalist art poster design, maximum negative space",
        "negative_prompt": "complex, detailed, colorful, photographic",
        "style": "DESIGN",
        "aspect_ratio": "ASPECT_3_4",
    },
    "D03": {
        "name": "Ikigai Diagram",
        "niche": "Japanese Zen",
        "ideogram_prompt": "Modern flat design ikigai diagram, four overlapping circles in soft pastel colors (coral, sky blue, sage green, lavender), each circle labeled Passion, Mission, Vocation, Profession, center labeled IKIGAI in bold sans-serif, clean infographic art",
        "negative_prompt": "complex, photographic, 3d",
        "style": "DESIGN",
        "aspect_ratio": "ASPECT_1_1",
    },
    "D31": {
        "name": "Laptop Beach",
        "niche": "Digital Nomad",
        "ideogram_prompt": "Bright flat illustration of open laptop on beach towel with palm tree shadow, cocktail drink beside it, tropical vibes, text 'Office Optional' in bold fun font, vivid summer colors, minimalist style",
        "negative_prompt": "photographic, realistic, dark",
        "style": "DESIGN",
        "aspect_ratio": "ASPECT_3_4",
    },
    "D41": {
        "name": "Marcus Aurelius Stoic",
        "niche": "Quotes & Philosophy",
        "ideogram_prompt": "Premium typography art print, quote 'You have power over your mind not outside events. Realize this and you will find strength.' attributed to Marcus Aurelius, elegant white serif font on deep navy background, subtle marble texture, gold accent lines, luxury art print",
        "negative_prompt": "casual, cartoonish, colorful",
        "style": "DESIGN",
        "aspect_ratio": "ASPECT_3_4",
    },
    # 他のデザインは design-prompts-all-50.md のプロンプトから変換してここに追加
    # （サンプルとして5件のみ定義）
}

IDEOGRAM_API_URL = "https://api.ideogram.ai/generate"


def generate_with_ideogram(
    design_id: str,
    prompt_data: dict,
    output_dir: Path,
    dry_run: bool = False,
) -> bool:
    """Ideogram APIでデザイン画像を生成"""
    api_key = os.environ.get("IDEOGRAM_API_KEY")
    if not api_key:
        print("エラー: IDEOGRAM_API_KEY が設定されていません")
        print("export IDEOGRAM_API_KEY=your_key または .env ファイルに記載")
        return False

    if dry_run:
        print(f"[DRY RUN] {design_id}: {prompt_data['name']}")
        print(f"  プロンプト: {prompt_data['ideogram_prompt'][:80]}...")
        return True

    payload = {
        "image_request": {
            "prompt": prompt_data["ideogram_prompt"],
            "negative_prompt": prompt_data.get("negative_prompt", ""),
            "aspect_ratio": prompt_data.get("aspect_ratio", "ASPECT_3_4"),
            "model": "V_2",  # Ideogram v2
            "style_type": prompt_data.get("style", "DESIGN"),
            "magic_prompt_option": "ON",  # プロンプト自動最適化
        }
    }

    headers = {
        "Api-Key": api_key,
        "Content-Type": "application/json",
    }

    try:
        response = requests.post(IDEOGRAM_API_URL, json=payload, headers=headers)
        response.raise_for_status()
        data = response.json()

        # 画像URLを取得してダウンロード
        image_url = data["data"][0]["url"]
        img_response = requests.get(image_url)
        img_response.raise_for_status()

        # 保存
        niche_dir = output_dir / prompt_data["niche"].lower().replace(" ", "-")
        niche_dir.mkdir(parents=True, exist_ok=True)
        filename = f"{design_id.lower()}-{prompt_data['name'].lower().replace(' ', '-')}.png"
        save_path = niche_dir / filename
        save_path.write_bytes(img_response.content)

        print(f"✓ 生成完了: {save_path}")
        return True

    except requests.exceptions.RequestException as e:
        print(f"✗ API エラー ({design_id}): {e}")
        return False


def generate_with_dalle(
    design_id: str,
    prompt_data: dict,
    output_dir: Path,
    dry_run: bool = False,
) -> bool:
    """DALL-E 3 APIでデザイン画像を生成（代替）"""
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        print("エラー: OPENAI_API_KEY が設定されていません")
        return False

    if dry_run:
        print(f"[DRY RUN DALL-E] {design_id}: {prompt_data['name']}")
        return True

    # DALL-E 3はプロンプトが1024文字以内
    dalle_prompt = f"Create a high-quality print-on-demand design: {prompt_data['ideogram_prompt']}"[:1024]

    payload = {
        "model": "dall-e-3",
        "prompt": dalle_prompt,
        "size": "1024x1792",  # 縦長（3:4に近い）
        "quality": "hd",
        "n": 1,
    }

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }

    try:
        response = requests.post(
            "https://api.openai.com/v1/images/generations",
            json=payload,
            headers=headers
        )
        response.raise_for_status()
        data = response.json()

        image_url = data["data"][0]["url"]
        img_response = requests.get(image_url)
        img_response.raise_for_status()

        niche_dir = output_dir / prompt_data["niche"].lower().replace(" ", "-")
        niche_dir.mkdir(parents=True, exist_ok=True)
        filename = f"{design_id.lower()}-{prompt_data['name'].lower().replace(' ', '-')}_dalle.png"
        save_path = niche_dir / filename
        save_path.write_bytes(img_response.content)

        print(f"✓ DALL-E 生成完了: {save_path}")
        return True

    except requests.exceptions.RequestException as e:
        print(f"✗ DALL-E エラー ({design_id}): {e}")
        return False


def main():
    parser = argparse.ArgumentParser(description="AsuInk デザイン自動生成")
    parser.add_argument("--design", help="特定のデザインID（例: D01）")
    parser.add_argument("--niche", help="特定ニッチのみ生成（例: 'Japanese Zen'）")
    parser.add_argument("--output", default="../designs/images",
                        help="出力ディレクトリ")
    parser.add_argument("--api", choices=["ideogram", "dalle"], default="ideogram",
                        help="使用するAPI（デフォルト: ideogram）")
    parser.add_argument("--dry-run", action="store_true",
                        help="実際に生成せずにプロンプト確認のみ")
    parser.add_argument("--delay", type=float, default=2.0,
                        help="API呼び出し間隔（秒）")
    args = parser.parse_args()

    output_dir = Path(__file__).parent / args.output

    # 処理対象を絞る
    targets = {}
    if args.design:
        design_id = args.design.upper()
        if design_id in DESIGN_PROMPTS:
            targets = {design_id: DESIGN_PROMPTS[design_id]}
        else:
            print(f"デザインIDが見つかりません: {design_id}")
            print(f"利用可能: {', '.join(DESIGN_PROMPTS.keys())}")
            return
    elif args.niche:
        targets = {k: v for k, v in DESIGN_PROMPTS.items() if args.niche.lower() in v["niche"].lower()}
        if not targets:
            print(f"ニッチが見つかりません: {args.niche}")
            return
    else:
        targets = DESIGN_PROMPTS

    print(f"生成対象: {len(targets)}デザイン")
    print(f"API: {args.api}")
    if args.dry_run:
        print("モード: DRY RUN（実際には生成しません）\n")

    success = 0
    failed = 0

    for i, (design_id, prompt_data) in enumerate(targets.items()):
        print(f"\n[{i+1}/{len(targets)}] {design_id}: {prompt_data['name']}")

        if args.api == "ideogram":
            ok = generate_with_ideogram(design_id, prompt_data, output_dir, args.dry_run)
        else:
            ok = generate_with_dalle(design_id, prompt_data, output_dir, args.dry_run)

        if ok:
            success += 1
        else:
            failed += 1

        # レート制限対策
        if not args.dry_run and i < len(targets) - 1:
            time.sleep(args.delay)

    print(f"\n=== 完了 ===")
    print(f"成功: {success}件, 失敗: {failed}件")
    print(f"\n次のステップ:")
    print(f"  python resize_for_printful.py --input {output_dir}")


if __name__ == "__main__":
    main()
