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
PHOTOS_DIR = Path(__file__).parent.parent / "images" / "sns-photos"
TAGS_FILE = PHOTOS_DIR / "tags.json"

IMAGE_EXTENSIONS = {".jpg", ".jpeg", ".png", ".webp", ".gif"}

# 仕分け先フォルダとキーワードマッピング
FOLDER_KEYWORDS = {
    "food": ["食事", "料理", "アサード", "BBQ", "バーベキュー", "肉", "牛肉", "レストラン",
             "カフェ", "飲み物", "果物", "野菜", "市場", "スーパー", "テレレ", "マテ茶",
             "ビール", "ワイン", "パン", "デザート", "食べ物", "グリル", "キッチン"],
    "kids": ["子供", "子ども", "娘", "学校", "インター", "教育", "遊び", "公園",
             "プール", "家族", "運動会", "授業", "宿題", "友達", "誕生日"],
    "nature": ["自然", "空", "夕焼け", "朝焼け", "雲", "花", "木", "緑", "川", "湖",
               "動物", "鳥", "犬", "猫", "庭", "畑", "農場", "星", "月", "雨", "虹"],
    "street": ["街", "道路", "建物", "教会", "ショッピング", "看板", "車", "バス",
               "交通", "商店", "モール", "通り", "広場", "像", "噴水", "都市"],
    "daily": [],  # デフォルト（どのカテゴリにも当てはまらない場合）
}

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
  "category": "仕分けカテゴリ（food/street/nature/kids/daily のいずれか1つ）",
  "tags": ["タグ1", "タグ2", ...],
  "mood": "雰囲気（楽しい/穏やか/活気/美味しそう/感動/日常/冒険）",
  "best_time": "投稿に最適な時間帯（morning/noon/evening）",
  "season": "季節感（spring/summer/autumn/winter/none）"
}

## カテゴリの判定基準
- food: 食事、料理、飲み物、レストラン、カフェ、市場の食品売り場
- kids: 子供、学校、教育、家族の活動、公園での遊び
- nature: 自然、風景、空、動植物、庭、農場
- street: 街並み、建物、道路、交通、ショッピング
- daily: 上記のどれにも当てはまらない日常の場面

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


def determine_folder(result: dict) -> str:
    """Claude の分析結果からフォルダを決定する"""
    # Claude が返した category を優先
    category = result.get("category", "").lower()
    if category in FOLDER_KEYWORDS:
        return category

    # category が不正な場合、タグからキーワードマッチで判定
    tags = result.get("tags", [])
    desc = result.get("description", "")
    all_text = " ".join(tags) + " " + desc

    best_folder = "daily"
    best_score = 0
    for folder, keywords in FOLDER_KEYWORDS.items():
        score = sum(1 for kw in keywords if kw in all_text)
        if score > best_score:
            best_score = score
            best_folder = folder

    return best_folder


def sort_image(image_path: Path, folder: str, dry_run: bool = False) -> Path:
    """画像を適切なサブフォルダに移動する。既にサブフォルダにある場合はスキップ"""
    # 既にサブフォルダ内にある場合はそのまま
    relative = image_path.relative_to(PHOTOS_DIR)
    if len(relative.parts) > 1:
        return image_path

    # sns-photos/ 直下にある → サブフォルダに移動
    dest_dir = PHOTOS_DIR / folder
    dest_dir.mkdir(parents=True, exist_ok=True)
    dest_path = dest_dir / image_path.name

    # ファイル名が被った場合はサフィックスを追加
    if dest_path.exists() and dest_path != image_path:
        stem = image_path.stem
        suffix = image_path.suffix
        counter = 1
        while dest_path.exists():
            dest_path = dest_dir / f"{stem}_{counter}{suffix}"
            counter += 1

    if dry_run:
        print(f"  [DRY RUN] 仕分け: {image_path.name} → {folder}/")
        return dest_path

    import shutil
    shutil.move(str(image_path), str(dest_path))
    print(f"  仕分け: {image_path.name} → {folder}/")
    return dest_path


def main():
    parser = argparse.ArgumentParser(description="SNS写真の自動タグ付け＆仕分け")
    parser.add_argument("--force", action="store_true", help="全画像を再タグ付け")
    parser.add_argument("--dry-run", action="store_true", help="タグ付け・仕分けをプレビュー")
    args = parser.parse_args()

    images = find_images()
    if not images:
        print(f"画像が見つかりません: {PHOTOS_DIR}")
        print("sns-photos/ に画像を追加してください（自動でサブフォルダに仕分けます）")
        sys.exit(0)

    tags_db = load_tags()
    to_process = []

    for img in images:
        key = get_relative_key(img)
        if args.force or key not in tags_db:
            to_process.append(img)

    # sns-photos/ 直下の未仕分け画像を別途カウント
    unsorted = [img for img in to_process if len(img.relative_to(PHOTOS_DIR).parts) == 1]
    print(f"画像総数: {len(images)}, 未処理: {len(to_process)}, 未仕分け: {len(unsorted)}")

    if not to_process:
        print("全画像がタグ付け済みです")
        return

    if args.dry_run and not to_process:
        return

    api_key = load_api_key()
    client = anthropic.Anthropic(api_key=api_key)

    for i, img in enumerate(to_process, 1):
        key = get_relative_key(img)
        print(f"\n[{i}/{len(to_process)}] {key}")

        if args.dry_run:
            print(f"  [DRY RUN] タグ付け予定")
            # dry-runでは仕分け先を推測できないのでスキップ
            continue

        try:
            result = analyze_image(client, img)

            # フォルダ判定＆仕分け
            folder = determine_folder(result)
            new_path = sort_image(img, folder)
            new_key = get_relative_key(new_path)

            # 旧キーのエントリを削除（仕分けでパスが変わった場合）
            if key != new_key and key in tags_db:
                old_used_count = tags_db[key].get("used_count", 0)
                del tags_db[key]
            else:
                old_used_count = tags_db.get(key, {}).get("used_count", 0)

            result["file"] = new_key
            result["folder"] = folder
            result["used_count"] = old_used_count
            tags_db[new_key] = result
            print(f"  → {result['description']} (タグ: {len(result['tags'])}個, フォルダ: {folder})")
            save_tags(tags_db)
        except Exception as e:
            print(f"  ERROR: {e}")
            continue

    print(f"\n完了: {len(tags_db)} 画像のタグ情報を保存しました → {TAGS_FILE}")


if __name__ == "__main__":
    main()
