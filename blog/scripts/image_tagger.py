"""
SNS写真の自動タグ付け＆仕分けスクリプト（Claude Vision API）

sns-photos/ 直下に画像を入れるだけで、Claude Visionが分析し：
  1. 適切なサブフォルダ (food/street/nature/kids/daily) に自動移動
  2. tags.json にタグ情報を保存

使い方:
  python image_tagger.py              # 未処理の画像をタグ付け＆仕分け
  python image_tagger.py --force      # 全画像を再タグ付け
  python image_tagger.py --dry-run    # タグ付け・仕分けをプレビュー（APIコール無し）
"""

import argparse
import base64
import io
import json
import sys
from pathlib import Path

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

try:
    import anthropic
except ImportError:
    print("ERROR: anthropic がインストールされていません")
    print("  pip install anthropic")
    sys.exit(1)

CONFIG_DIR = Path(__file__).parent.parent / "config"
SECRETS_FILE = CONFIG_DIR / "secrets.json"
PHOTOS_DIR = Path(__file__).parent.parent / "assets" / "sns-photos"
TAGS_FILE = PHOTOS_DIR / "tags.json"

IMAGE_EXTENSIONS = {".jpg", ".jpeg", ".png", ".webp", ".gif"}

MEDIA_TYPE_MAP = {
    ".jpg": "image/jpeg",
    ".jpeg": "image/jpeg",
    ".png": "image/png",
    ".webp": "image/webp",
    ".gif": "image/gif",
}

SYSTEM_PROMPT = """あなたは画像分析アシスタントです。
SNS投稿に使う写真を分析し、以下の情報をJSON形式で返してください。

## 出力形式（JSONのみ、説明不要）
{
  "description": "画像の簡潔な説明（日本語、20文字以内）",
  "tags": ["タグ1", "タグ2", ...],
  "mood": "雰囲気（楽しい/穏やか/活気/美味しそう/感動/日常/冒険）",
  "best_time": "投稿に最適な時間帯（morning/noon/evening）",
  "season": "季節感（spring/summer/autumn/winter/none）"
}

## タグ付けルール
- タグは日本語で5〜10個
- 具体的な被写体（例: アサード、市場、公園）
- 抽象的なテーマ（例: 食事、家族、自然、街並み）
- パラグアイ関連のキーワード（例: パラグアイ、南米、ラテン）
- SNS投稿のカテゴリ（例: パラグアイ日常、食事、子育て、移住生活）"""


def load_api_key() -> str:
    with open(SECRETS_FILE, "r", encoding="utf-8") as f:
        secrets = json.load(f)
    return secrets["claude_api"]["api_key"]


def load_tags() -> dict:
    if TAGS_FILE.exists():
        with open(TAGS_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}


def save_tags(tags: dict):
    with open(TAGS_FILE, "w", encoding="utf-8") as f:
        json.dump(tags, f, ensure_ascii=False, indent=2)


def find_images() -> list[Path]:
    images = []
    for ext in IMAGE_EXTENSIONS:
        images.extend(PHOTOS_DIR.rglob(f"*{ext}"))
        images.extend(PHOTOS_DIR.rglob(f"*{ext.upper()}"))
    return sorted(set(images))


def get_relative_key(image_path: Path) -> str:
    return str(image_path.relative_to(PHOTOS_DIR)).replace("\\", "/")


def analyze_image(client: anthropic.Anthropic, image_path: Path) -> dict:
    with open(image_path, "rb") as f:
        image_data = base64.standard_b64encode(f.read()).decode("utf-8")

    media_type = MEDIA_TYPE_MAP.get(image_path.suffix.lower(), "image/jpeg")

    response = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=512,
        system=SYSTEM_PROMPT,
        messages=[{
            "role": "user",
            "content": [
                {
                    "type": "image",
                    "source": {
                        "type": "base64",
                        "media_type": media_type,
                        "data": image_data,
                    },
                },
                {"type": "text", "text": "この画像を分析してください。"},
            ],
        }],
    )

    text = response.content[0].text.strip()
    # JSONブロックを抽出
    if "```json" in text:
        text = text.split("```json")[1].split("```")[0].strip()
    elif "```" in text:
        text = text.split("```")[1].split("```")[0].strip()

    return json.loads(text)


def main():
    parser = argparse.ArgumentParser(description="SNS写真の自動タグ付け")
    parser.add_argument("--force", action="store_true", help="全画像を再タグ付け")
    parser.add_argument("--dry-run", action="store_true", help="画像一覧の表示のみ")
    args = parser.parse_args()

    images = find_images()
    if not images:
        print(f"画像が見つかりません: {PHOTOS_DIR}")
        print("sns-photos/ 以下のサブフォルダ (food/, street/ 等) に画像を追加してください")
        sys.exit(0)

    tags_db = load_tags()
    to_process = []

    for img in images:
        key = get_relative_key(img)
        if args.force or key not in tags_db:
            to_process.append(img)

    print(f"画像総数: {len(images)}, 未処理: {len(to_process)}")

    if not to_process:
        print("全画像がタグ付け済みです")
        return

    if args.dry_run:
        print("\n[DRY RUN] 以下の画像を処理予定:")
        for img in to_process:
            print(f"  {get_relative_key(img)}")
        return

    api_key = load_api_key()
    client = anthropic.Anthropic(api_key=api_key)

    for i, img in enumerate(to_process, 1):
        key = get_relative_key(img)
        print(f"\n[{i}/{len(to_process)}] {key}")

        try:
            result = analyze_image(client, img)
            result["file"] = key
            result["folder"] = str(Path(key).parent)
            result["used_count"] = tags_db.get(key, {}).get("used_count", 0)
            tags_db[key] = result
            print(f"  → {result['description']} (タグ: {len(result['tags'])}個)")
            save_tags(tags_db)
        except Exception as e:
            print(f"  ERROR: {e}")
            continue

    print(f"\n完了: {len(tags_db)} 画像のタグ情報を保存しました → {TAGS_FILE}")


if __name__ == "__main__":
    main()
