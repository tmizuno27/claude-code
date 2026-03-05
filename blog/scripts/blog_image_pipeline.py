#!/usr/bin/env python3
"""
blog_image_pipeline.py
======================
ブログ記事のアイキャッチ画像を自動生成し、WordPressにアップロードするパイプライン。

フロー:
  1. outputs/articles/ から未公開記事を検索
  2. media-mapping.json に画像がない記事を特定
  3. Gemini API で画像生成
  4. WordPress REST API でメディアアップロード
  5. media-mapping.json に wordpress_media_id を記録

使い方:
  python blog_image_pipeline.py              # 全未処理記事の画像を生成
  python blog_image_pipeline.py --limit 1    # 1記事分だけ生成
  python blog_image_pipeline.py --dry-run    # 生成せずにプレビュー
"""

import argparse
import json
import logging
import re
import sys
import unicodedata
from datetime import datetime
from pathlib import Path

import requests
from base64 import b64encode
from google import genai
from google.genai import types

# ==============================================================================
# 設定
# ==============================================================================
SCRIPT_DIR = Path(__file__).resolve().parent
BLOG_DIR = SCRIPT_DIR.parent
CONFIG_DIR = BLOG_DIR / "config"
IMAGES_DIR = BLOG_DIR / "images"
ARTICLES_DIR = BLOG_DIR / "outputs" / "articles"
PUBLISHED_DIR = BLOG_DIR / "published"

SETTINGS_FILE = CONFIG_DIR / "settings.json"
SECRETS_FILE = CONFIG_DIR / "secrets.json"
MEDIA_MAPPING_FILE = IMAGES_DIR / "media-mapping.json"
WP_LOG_FILE = PUBLISHED_DIR / "wordpress-log.json"

# Gemini 画像生成モデル
GEMINI_MODEL = "gemini-2.5-flash-image"

# 画像生成プロンプト
STYLE_PROMPT = (
    "Professional blog header photo, high quality, modern, clean composition, "
    "natural lighting, editorial style. "
    "No text, no watermark, no logos."
)

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
def load_secrets() -> dict:
    """secrets.json を読み込む"""
    if not SECRETS_FILE.exists():
        logger.error(f"secrets.json が見つかりません: {SECRETS_FILE}")
        sys.exit(1)
    with open(SECRETS_FILE, encoding="utf-8") as f:
        return json.load(f)


def load_settings() -> dict:
    """settings.json を読み込む"""
    with open(SETTINGS_FILE, encoding="utf-8") as f:
        return json.load(f)


def load_media_mapping() -> dict:
    """media-mapping.json を読み込む"""
    if MEDIA_MAPPING_FILE.exists():
        with open(MEDIA_MAPPING_FILE, encoding="utf-8") as f:
            return json.load(f)
    return {"description": "WordPress Media ID mapping", "updated": "", "media": {}, "post_featured_images": {}}


def save_media_mapping(mapping: dict) -> None:
    """media-mapping.json を保存する"""
    mapping["updated"] = datetime.now().strftime("%Y-%m-%d")
    MEDIA_MAPPING_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(MEDIA_MAPPING_FILE, "w", encoding="utf-8") as f:
        json.dump(mapping, f, ensure_ascii=False, indent=2)


def slugify(text: str) -> str:
    """日本語テキストをファイル名用スラッグに変換"""
    text = unicodedata.normalize("NFKC", text)
    text = re.sub(r"[^\w\s-]", "", text)
    text = re.sub(r"[\s_]+", "-", text.strip())
    text = re.sub(r"-+", "-", text).strip("-")
    if not text or text == "-":
        text = datetime.now().strftime("%Y%m%d-%H%M%S")
    return text.lower()


def parse_front_matter(content: str) -> dict:
    """Markdownからフロントマターを抽出"""
    fm_match = re.match(r'^---\s*\n(.*?)\n---\s*\n', content, re.DOTALL)
    if not fm_match:
        return {}
    front_matter = {}
    for line in fm_match.group(1).strip().split('\n'):
        if ':' in line:
            key, value = line.split(':', 1)
            front_matter[key.strip()] = value.strip().strip('"').strip("'")
    return front_matter


# ==============================================================================
# 未処理記事の検索
# ==============================================================================
def find_articles_needing_images() -> list[dict]:
    """画像が未生成の記事を検索する"""
    if not ARTICLES_DIR.exists():
        logger.warning(f"記事ディレクトリが存在しません: {ARTICLES_DIR}")
        return []

    mapping = load_media_mapping()
    # 既存の post_featured_images からキーワードを収集（すでに画像がある記事のタイトル）
    existing_titles = set()
    for info in mapping.get("post_featured_images", {}).values():
        existing_titles.add(info.get("post_title", ""))

    # generated_images: キーワードベースで既に画像生成済みのトピックを追跡
    generated_topics = set()
    for media_id, info in mapping.get("media", {}).items():
        if info.get("title"):
            generated_topics.add(info["title"])

    articles = []
    for md_file in sorted(ARTICLES_DIR.rglob("*.md")):
        content = md_file.read_text(encoding="utf-8")
        fm = parse_front_matter(content)

        title = fm.get("title", "")
        keyword = fm.get("keyword", "")

        if not title and not keyword:
            continue

        # タイトルが既に featured_images に登録済みならスキップ
        if title in existing_titles:
            continue

        articles.append({
            "path": md_file,
            "title": title,
            "keyword": keyword,
            "relative_path": str(md_file.relative_to(BLOG_DIR)),
        })

    return articles


# ==============================================================================
# 画像生成（Gemini API）
# ==============================================================================
def generate_image(topic: str, api_key: str) -> bytes | None:
    """Gemini API で画像を生成する"""
    client = genai.Client(api_key=api_key)
    full_prompt = f"{STYLE_PROMPT}\n\nTopic: {topic}\n\n{BLOG_CONTEXT}"

    logger.info(f"画像生成中: '{topic}'")

    try:
        response = client.models.generate_content(
            model=GEMINI_MODEL,
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


# ==============================================================================
# WordPress メディアアップロード
# ==============================================================================
def upload_to_wordpress(image_data: bytes, filename: str, title: str, settings: dict, secrets: dict) -> int | None:
    """画像をWordPressにアップロードし、メディアIDを返す"""
    wp_url = settings["wordpress"]["rest_api_url"]
    username = secrets["wordpress"]["username"]
    app_password = secrets["wordpress"]["app_password"]

    credentials = f"{username}:{app_password}"
    token = b64encode(credentials.encode()).decode()

    headers = {
        "Authorization": f"Basic {token}",
        "Content-Disposition": f'attachment; filename="{filename}"',
        "Content-Type": "image/png",
    }

    logger.info(f"WordPressにアップロード中: {filename}")

    try:
        response = requests.post(
            f"{wp_url}/media",
            headers=headers,
            data=image_data,
            timeout=60,
        )

        if response.status_code in (200, 201):
            media = response.json()
            media_id = media["id"]
            logger.info(f"アップロード成功: media_id={media_id}")
            return media_id
        else:
            logger.error(f"アップロード失敗: {response.status_code} - {response.text}")
            return None
    except Exception as e:
        logger.error(f"アップロードエラー: {e}")
        return None


# ==============================================================================
# メインパイプライン
# ==============================================================================
def run_pipeline(limit: int = 0, dry_run: bool = False) -> int:
    """画像生成パイプラインを実行する"""
    secrets = load_secrets()
    settings = load_settings()

    gemini_key = secrets.get("gemini", {}).get("api_key", "")
    if not gemini_key or gemini_key == "YOUR_GEMINI_API_KEY":
        logger.error("Gemini API キーが未設定です")
        return 0

    articles = find_articles_needing_images()
    if not articles:
        logger.info("画像が必要な記事はありません")
        return 0

    if limit > 0:
        articles = articles[:limit]

    logger.info(f"画像生成対象: {len(articles)}件")

    if dry_run:
        for a in articles:
            logger.info(f"  [DRY RUN] {a['title']} (keyword: {a['keyword']})")
        return 0

    mapping = load_media_mapping()
    success_count = 0

    for article in articles:
        topic = article["keyword"] or article["title"]
        slug = slugify(topic)
        timestamp = datetime.now().strftime("%Y%m%d")
        filename = f"nao-{timestamp}-{slug}.png"

        # 1. 画像生成
        image_data = generate_image(topic, gemini_key)
        if not image_data:
            continue

        # 2. ローカル保存
        category = _guess_category(topic)
        save_dir = IMAGES_DIR / category
        save_dir.mkdir(parents=True, exist_ok=True)
        local_path = save_dir / filename
        local_path.write_bytes(image_data)
        logger.info(f"ローカル保存: {local_path}")

        # 3. WordPress アップロード
        media_id = upload_to_wordpress(image_data, filename, topic, settings, secrets)
        if not media_id:
            continue

        # 4. media-mapping.json 更新
        mapping["media"][str(media_id)] = {
            "file": f"{category}/{filename}",
            "wp_name": filename,
            "title": article["title"],
            "keyword": article["keyword"],
            "generated_at": datetime.now().isoformat(),
        }
        save_media_mapping(mapping)
        success_count += 1

        logger.info(f"完了: {article['title']} → media_id={media_id}")

    logger.info(f"画像パイプライン完了: {success_count}/{len(articles)}件成功")
    return success_count


def _guess_category(topic: str) -> str:
    """トピックからカテゴリフォルダを推定"""
    topic_lower = topic.lower()
    if any(w in topic_lower for w in ["移住", "移民", "ビザ", "永住", "パスポート"]):
        return "immigration"
    if any(w in topic_lower for w in ["生活", "気候", "治安", "物価", "パラグアイ", "アサード"]):
        return "paraguay-life"
    if any(w in topic_lower for w in ["仕事", "副業", "リモート", "フリーランス", "稼"]):
        return "remote-work"
    if any(w in topic_lower for w in ["子育て", "教育", "学校", "インター"]):
        return "family-education"
    if any(w in topic_lower for w in ["送金", "銀行", "費用", "お金", "税金"]):
        return "finance"
    return "general"


def main():
    parser = argparse.ArgumentParser(description="ブログ画像自動生成パイプライン")
    parser.add_argument("--limit", type=int, default=0, help="処理する記事数の上限 (0=全件)")
    parser.add_argument("--dry-run", action="store_true", help="生成せずにプレビューのみ")
    args = parser.parse_args()

    logger.info("=== 画像自動生成パイプライン開始 ===")
    success = run_pipeline(limit=args.limit, dry_run=args.dry_run)
    logger.info(f"=== パイプライン終了 (成功: {success}件) ===")


if __name__ == "__main__":
    main()
