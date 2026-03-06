"""
image_generator.py
==================
Google Gemini API を使ったブログ用アイキャッチ画像自動生成スクリプト

機能:
- 記事タイトル/キーワードからアイキャッチ画像を自動生成
- Gemini 2.0 Flash (無料枠: 500枚/日) を使用
- 生成画像を blog/images/branding/ に保存
- media-mapping.json に記録を追加

使い方:
    python image_generator.py "パラグアイ移住の費用" --style photo
    python image_generator.py "海外送金の比較" --style illustration --aspect 16:9
    python image_generator.py --batch keywords.txt
"""

import argparse
import base64
import json
import logging
import re
import sys
import unicodedata
from datetime import datetime
from pathlib import Path

from google import genai
from google.genai import types

# ==============================================================================
# 設定
# ==============================================================================
SCRIPT_DIR = Path(__file__).resolve().parent
BLOG_DIR = SCRIPT_DIR.parent.parent
CONFIG_DIR = BLOG_DIR / "config"
ASSETS_DIR = BLOG_DIR / "images" / "branding"
SECRETS_FILE = CONFIG_DIR / "secrets.json"
MEDIA_MAPPING_FILE = ASSETS_DIR / "media-mapping.json"

# 画像生成モデル
MODEL_NAME = "gemini-2.5-flash-image"

# デフォルトのスタイルプリセット
STYLE_PRESETS = {
    "photo": (
        "Professional blog header photo, high quality, modern, clean composition, "
        "natural lighting, editorial style. "
        "No text, no watermark, no logos."
    ),
    "illustration": (
        "Modern flat illustration, clean vector style, vibrant colors, "
        "minimalist design suitable for a blog header. "
        "No text, no watermark, no logos."
    ),
    "watercolor": (
        "Beautiful watercolor painting style, soft colors, artistic, "
        "warm tones suitable for a blog header. "
        "No text, no watermark, no logos."
    ),
    "minimal": (
        "Minimalist design, simple geometric shapes, muted colors, "
        "lots of white space, modern and clean. "
        "No text, no watermark, no logos."
    ),
}

# ブログのテーマに合わせた追加コンテキスト
BLOG_CONTEXT = (
    "This image is for a Japanese blog about living in Paraguay and South America. "
    "The blog covers topics like immigration, daily life, education, and working abroad. "
    "The style should feel warm, inviting, and authentic."
)

# ロギング
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
)
logger = logging.getLogger(__name__)


# ==============================================================================
# ユーティリティ
# ==============================================================================
def load_api_key() -> str:
    """secrets.json から Gemini API キーを読み込む"""
    if not SECRETS_FILE.exists():
        logger.error(f"secrets.json が見つかりません: {SECRETS_FILE}")
        sys.exit(1)

    with open(SECRETS_FILE, encoding="utf-8") as f:
        secrets = json.load(f)

    api_key = secrets.get("gemini", {}).get("api_key", "")
    if not api_key or api_key == "YOUR_GEMINI_API_KEY":
        logger.error(
            "Gemini API キーが設定されていません。\n"
            "1. https://aistudio.google.com/apikey でAPIキーを取得\n"
            "2. blog/config/secrets.json の gemini.api_key に設定してください"
        )
        sys.exit(1)

    return api_key


def slugify(text: str) -> str:
    """日本語テキストをファイル名用のスラッグに変換"""
    text = unicodedata.normalize("NFKC", text)
    text = re.sub(r"[^\w\s-]", "", text)
    text = re.sub(r"[\s_]+", "-", text.strip())
    text = re.sub(r"-+", "-", text).strip("-")
    if not text or text == "-":
        text = datetime.now().strftime("%Y%m%d-%H%M%S")
    return text.lower()


def load_media_mapping() -> dict:
    """media-mapping.json を読み込む（なければ空辞書）"""
    if MEDIA_MAPPING_FILE.exists():
        with open(MEDIA_MAPPING_FILE, encoding="utf-8") as f:
            return json.load(f)
    return {}


def save_media_mapping(mapping: dict) -> None:
    """media-mapping.json に保存"""
    MEDIA_MAPPING_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(MEDIA_MAPPING_FILE, "w", encoding="utf-8") as f:
        json.dump(mapping, f, ensure_ascii=False, indent=2)


# ==============================================================================
# 画像生成
# ==============================================================================
def generate_image(
    topic: str,
    style: str = "photo",
    aspect_ratio: str = "16:9",
    api_key: str = "",
) -> bytes | None:
    """
    Gemini API で画像を生成する

    Args:
        topic: 記事のタイトルまたはキーワード
        style: スタイルプリセット名 (photo/illustration/watercolor/minimal)
        aspect_ratio: アスペクト比 (16:9, 4:3, 1:1, 9:16)
        api_key: Gemini API キー

    Returns:
        生成された画像のバイトデータ（失敗時はNone）
    """
    client = genai.Client(api_key=api_key)

    style_prompt = STYLE_PRESETS.get(style, STYLE_PRESETS["photo"])
    full_prompt = f"{style_prompt}\n\nTopic: {topic}\n\n{BLOG_CONTEXT}"

    logger.info(f"画像生成中: '{topic}' (スタイル: {style}, アスペクト比: {aspect_ratio})")

    try:
        response = client.models.generate_content(
            model=MODEL_NAME,
            contents=full_prompt,
            config=types.GenerateContentConfig(
                response_modalities=["TEXT", "IMAGE"],
            ),
        )

        if response.candidates and response.candidates[0].content.parts:
            for part in response.candidates[0].content.parts:
                if part.inline_data is not None:
                    logger.info("画像生成成功")
                    return part.inline_data.data

        logger.warning("画像データがレスポンスに含まれていません")
        return None

    except Exception as e:
        logger.error(f"画像生成エラー: {e}")
        return None


def save_image(
    image_data: bytes,
    topic: str,
    style: str,
) -> Path | None:
    """
    画像をファイルに保存し、media-mapping.json を更新する

    Returns:
        保存先のPath（失敗時はNone）
    """
    ASSETS_DIR.mkdir(parents=True, exist_ok=True)

    slug = slugify(topic)
    timestamp = datetime.now().strftime("%Y%m%d")
    filename = f"{timestamp}-{slug}.png"
    filepath = ASSETS_DIR / filename

    # 同名ファイルがあればサフィックス追加
    counter = 1
    while filepath.exists():
        filename = f"{timestamp}-{slug}-{counter}.png"
        filepath = ASSETS_DIR / filename
        counter += 1

    filepath.write_bytes(image_data)
    logger.info(f"画像保存: {filepath}")

    # media-mapping.json を更新
    mapping = load_media_mapping()
    mapping[filename] = {
        "topic": topic,
        "style": style,
        "generated_at": datetime.now().isoformat(),
        "wordpress_media_id": None,
    }
    save_media_mapping(mapping)

    return filepath


# ==============================================================================
# バッチ処理
# ==============================================================================
def batch_generate(
    keywords_file: Path,
    style: str = "photo",
    aspect_ratio: str = "16:9",
    api_key: str = "",
) -> list[Path]:
    """
    キーワードファイルから一括で画像を生成する

    キーワードファイルは1行1キーワードのテキストファイル
    """
    if not keywords_file.exists():
        logger.error(f"キーワードファイルが見つかりません: {keywords_file}")
        return []

    keywords = [
        line.strip()
        for line in keywords_file.read_text(encoding="utf-8").splitlines()
        if line.strip() and not line.startswith("#")
    ]

    logger.info(f"バッチ生成開始: {len(keywords)} 件")
    results = []

    for i, keyword in enumerate(keywords, 1):
        logger.info(f"[{i}/{len(keywords)}] {keyword}")
        image_data = generate_image(keyword, style, aspect_ratio, api_key)
        if image_data:
            filepath = save_image(image_data, keyword, style)
            if filepath:
                results.append(filepath)

    logger.info(f"バッチ生成完了: {len(results)}/{len(keywords)} 件成功")
    return results


# ==============================================================================
# メイン
# ==============================================================================
def main():
    parser = argparse.ArgumentParser(
        description="Gemini API でブログ用アイキャッチ画像を生成"
    )
    parser.add_argument(
        "topic",
        nargs="?",
        help="記事のタイトルまたはキーワード",
    )
    parser.add_argument(
        "--style",
        choices=list(STYLE_PRESETS.keys()),
        default="photo",
        help="画像スタイル (default: photo)",
    )
    parser.add_argument(
        "--aspect",
        default="16:9",
        choices=["16:9", "4:3", "1:1", "9:16"],
        help="アスペクト比 (default: 16:9)",
    )
    parser.add_argument(
        "--batch",
        type=Path,
        help="キーワードファイルで一括生成（1行1キーワード）",
    )

    args = parser.parse_args()

    if not args.topic and not args.batch:
        parser.print_help()
        sys.exit(1)

    api_key = load_api_key()

    if args.batch:
        results = batch_generate(args.batch, args.style, args.aspect, api_key)
        for path in results:
            print(f"  ✓ {path}")
    else:
        image_data = generate_image(args.topic, args.style, args.aspect, api_key)
        if image_data:
            filepath = save_image(image_data, args.topic, args.style)
            if filepath:
                print(f"✓ 画像生成完了: {filepath}")
            else:
                print("✗ 画像保存に失敗しました")
                sys.exit(1)
        else:
            print("✗ 画像生成に失敗しました")
            sys.exit(1)


if __name__ == "__main__":
    main()
