"""
X (Twitter) 自動投稿スクリプト（Claude API連携 + 画像自動添付）
毎回Claude APIで投稿文を生成し、最適な画像を自動選定して投稿する

使い方:
  python x_auto_post.py --slot morning   # 朝の投稿（JST 7:00-8:00向け）
  python x_auto_post.py --slot noon      # 昼の投稿（JST 12:00-13:00向け）
  python x_auto_post.py --slot evening   # 夜の投稿（JST 20:00-21:00向け）
  python x_auto_post.py --slot morning --dry-run    # 生成のみ、投稿しない
  python x_auto_post.py --slot noon --no-image      # 画像なしで投稿
"""

import argparse
import io
import json
import random
import sys
import urllib.request
from datetime import datetime
from pathlib import Path

# Windows cp932 で絵文字が出力できない問題を回避
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

try:
    import anthropic
except ImportError:
    print("ERROR: anthropic がインストールされていません")
    print("  pip install anthropic")
    sys.exit(1)

try:
    import tweepy
except ImportError:
    print("ERROR: tweepy がインストールされていません")
    print("  pip install tweepy")
    sys.exit(1)


CONFIG_DIR = Path(__file__).parent.parent / "config"
SETTINGS_FILE = CONFIG_DIR / "settings.json"
SECRETS_FILE = CONFIG_DIR / "secrets.json"
X_CREDS_FILE = CONFIG_DIR / "x-credentials.json"
LOG_DIR = Path(__file__).parent.parent / "outputs" / "social"
PHOTOS_DIR = Path(__file__).parent.parent / "assets" / "sns-photos"
TAGS_FILE = PHOTOS_DIR / "tags.json"

# 時間帯ごとのカテゴリ設定
SLOT_CONFIG = {
    "morning": {
        "categories": ["実験報告", "AI Tips"],
        "weights": [0.5, 0.5],
        "description": "朝の投稿（JST 7:00-8:00）通勤時間帯、情報収集モード",
    },
    "noon": {
        "categories": ["パラグアイ日常", "記事告知"],
        "weights": [0.7, 0.3],
        "description": "昼の投稿（JST 12:00-13:00）昼休み、リラックスモード",
    },
    "evening": {
        "categories": ["実験報告", "AI Tips"],
        "weights": [0.5, 0.5],
        "description": "夜の投稿（JST 20:00-21:00）帰宅後、副業検討モード",
    },
}

SYSTEM_PROMPT = """あなたはX（Twitter）の投稿文を生成するアシスタントです。
以下のアカウント情報とルールに従って、1つの投稿文を生成してください。

## アカウント情報
- アカウント: @nambei_oyaji（南米おやじ）
- コンセプト: パラグアイ在住の日本人おやじが海外生活と副業に挑戦する実録
- ペルソナ: カジュアルで正直。数字をオープンにする。失敗も隠さない

## 投稿ルール（厳守）
1. 140文字以内（日本語）— これは絶対に超えないこと
2. ハッシュタグは2〜3個（文字数に含む）
3. 絵文字は1〜2個
4. AI的な表現は禁止（「いかがでしたでしょうか」等）
5. 具体的な数字を入れる
6. 自然な日本語で、おやじがつぶやいている感じ

## メインハッシュタグ（毎回1つ選ぶ）
#海外移住 #海外ノマド #パラグアイ #南米おやじ

## サブハッシュタグ（毎回1-2個選ぶ）
#副業実験 #海外生活 #ブログ運営 #フリーランス #ノマドワーカー #移住生活 #パラグアイ生活

## パラグアイの実情（投稿ネタとして使ってOK）
- 生活費が日本の1/3〜1/2（ランチ200-300円、牛肉1kg 500円等）
- 所得税が最大10%で手取りが多い
- 地震・台風・津波なし、一年中温暖
- 娘2人（8歳・6歳）がインターに通学中（英語+スペイン語）
- 花粉ゼロ（日本では1年の1/4が花粉症で潰れていた）
- アサード（南米BBQ）が最高
- ブログ「南米おやじの海外生活ラボ」(nambei-oyaji.com) を運営中

## 出力形式
投稿文のみを出力してください。説明や前置きは不要です。"""


def load_secrets() -> str:
    """Claude API キーを読み込む"""
    with open(SECRETS_FILE, "r", encoding="utf-8") as f:
        secrets = json.load(f)
    return secrets["claude_api"]["api_key"]


def load_x_credentials() -> dict:
    """X API認証情報を読み込む"""
    with open(X_CREDS_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def get_recent_posts() -> list[str]:
    """直近の投稿ログから重複を避けるために最近の投稿を取得"""
    log_file = LOG_DIR / "x-post-log.jsonl"
    if not log_file.exists():
        return []

    posts = []
    lines = log_file.read_text(encoding="utf-8").strip().split("\n")
    for line in lines[-10:]:  # 直近10件
        try:
            entry = json.loads(line)
            posts.append(entry["text"])
        except (json.JSONDecodeError, KeyError):
            continue
    return posts


def generate_post(api_key: str, slot: str) -> str:
    """Claude APIで投稿文を生成"""
    config = SLOT_CONFIG[slot]

    # カテゴリをランダム選択（重み付き）
    category = random.choices(config["categories"], weights=config["weights"], k=1)[0]

    # 直近の投稿を取得して重複回避
    recent = get_recent_posts()
    recent_text = ""
    if recent:
        recent_text = "\n\n## 直近の投稿（これらと似た内容は避けること）\n"
        for p in recent[-5:]:
            recent_text += f"- {p}\n"

    user_prompt = f"""カテゴリ「{category}」の投稿を1つ生成してください。
{config['description']}

今日の日付: {datetime.now().strftime('%Y年%m月%d日')}
{recent_text}"""

    client = anthropic.Anthropic(api_key=api_key)
    response = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=256,
        system=SYSTEM_PROMPT,
        messages=[{"role": "user", "content": user_prompt}],
    )

    text = response.content[0].text.strip()

    # 前後の引用符を除去（Claude が "" で囲むことがある）
    if text.startswith('"') and text.endswith('"'):
        text = text[1:-1]
    if text.startswith('「') and text.endswith('」'):
        text = text[1:-1]

    return text


def find_best_image(post_text: str, slot: str) -> Path | None:
    """投稿文に最も合う画像をtags.jsonから選定する"""
    if not TAGS_FILE.exists():
        print("画像タグファイルが見つかりません（image_tagger.py を先に実行してください）")
        return None

    with open(TAGS_FILE, "r", encoding="utf-8") as f:
        tags_db = json.load(f)

    if not tags_db:
        print("タグ付き画像がありません")
        return None

    post_lower = post_text.lower()
    candidates = []

    for key, info in tags_db.items():
        # 使用回数が少ない画像を優先（同じ写真の連続使用防止）
        used_count = info.get("used_count", 0)

        # タグマッチングスコアを計算
        score = 0
        tags = info.get("tags", [])
        for tag in tags:
            if tag in post_text:
                score += 3  # 完全一致は高スコア
            elif tag.lower() in post_lower:
                score += 2

        # 説明文とのマッチ
        desc = info.get("description", "")
        for word in desc:
            if word in post_text:
                score += 1

        # 時間帯マッチ（best_time が slot と一致すればボーナス）
        if info.get("best_time") == slot:
            score += 2

        # 使用回数でペナルティ（よく使われた画像は優先度下げる）
        score -= used_count * 2

        if score > 0:
            candidates.append((key, score, used_count))

    if not candidates:
        # スコアが付かなかった場合、未使用 or 使用回数最少の画像をランダムに選ぶ
        unused = [(k, v.get("used_count", 0)) for k, v in tags_db.items()]
        unused.sort(key=lambda x: x[1])
        if unused:
            # 使用回数が最少のグループからランダム選択
            min_count = unused[0][1]
            least_used = [k for k, c in unused if c == min_count]
            key = random.choice(least_used)
            image_path = PHOTOS_DIR / key
            if image_path.exists():
                print(f"画像選定: タグマッチなし → 未使用画像からランダム選択: {key}")
                return image_path
        return None

    # スコア順にソート（同スコアなら使用回数が少ない方を優先）
    candidates.sort(key=lambda x: (-x[1], x[2]))
    best_key = candidates[0][0]
    best_score = candidates[0][1]

    image_path = PHOTOS_DIR / best_key
    if not image_path.exists():
        print(f"WARNING: タグDBに存在するが画像ファイルがない: {best_key}")
        return None

    print(f"画像選定: {best_key} (スコア: {best_score})")
    return image_path


def mark_image_used(image_key: str):
    """画像の使用回数をインクリメント"""
    if not TAGS_FILE.exists():
        return
    with open(TAGS_FILE, "r", encoding="utf-8") as f:
        tags_db = json.load(f)
    if image_key in tags_db:
        tags_db[image_key]["used_count"] = tags_db[image_key].get("used_count", 0) + 1
        with open(TAGS_FILE, "w", encoding="utf-8") as f:
            json.dump(tags_db, f, ensure_ascii=False, indent=2)


def post_to_x(creds: dict, text: str, image_path: Path = None) -> str | None:
    """Xに投稿（v2 API + v1.1 media upload）"""
    auth = tweepy.OAuth1UserHandler(
        creds["api_key"],
        creds["api_key_secret"],
        creds["access_token"],
        creds["access_token_secret"],
    )

    # v2 Client（テキスト投稿用）
    client = tweepy.Client(
        consumer_key=creds["api_key"],
        consumer_secret=creds["api_key_secret"],
        access_token=creds["access_token"],
        access_token_secret=creds["access_token_secret"],
    )

    try:
        kwargs = {"text": text}

        # 画像がある場合は v1.1 で media upload してから v2 で投稿
        if image_path:
            api = tweepy.API(auth)
            media = api.media_upload(filename=str(image_path))
            kwargs["media_ids"] = [media.media_id]
            print(f"OK: 画像アップロード成功 (画像: {image_path.name})")

        response = client.create_tweet(**kwargs)
        tweet_id = response.data["id"]
        print(f"OK: 投稿成功 (ID: {tweet_id})")
        return tweet_id
    except tweepy.errors.TweepyException as e:
        print(f"ERROR: 投稿失敗 - {e}")
        return None


def notify_discord(message: str):
    """Discord Webhookで通知を送信"""
    try:
        with open(SETTINGS_FILE, "r", encoding="utf-8") as f:
            settings = json.load(f)
        webhook_url = settings.get("discord", {}).get("webhook_url")
        if not webhook_url:
            print("Discord Webhook URLが設定されていません")
            return
        payload = json.dumps({"content": message}).encode("utf-8")
        req = urllib.request.Request(
            webhook_url,
            data=payload,
            headers={"Content-Type": "application/json"},
        )
        urllib.request.urlopen(req)
        print("Discord通知を送信しました")
    except Exception as e:
        print(f"WARNING: Discord通知の送信に失敗 - {e}")


def log_post(text: str, tweet_id: str, slot: str, category: str = "auto", image: str = None):
    """投稿ログを保存"""
    LOG_DIR.mkdir(parents=True, exist_ok=True)
    log_file = LOG_DIR / "x-post-log.jsonl"

    entry = {
        "timestamp": datetime.now().isoformat(),
        "tweet_id": tweet_id,
        "slot": slot,
        "category": category,
        "text": text,
        "char_count": len(text),
        "image": image,
    }

    with open(log_file, "a", encoding="utf-8") as f:
        f.write(json.dumps(entry, ensure_ascii=False) + "\n")


def main():
    parser = argparse.ArgumentParser(description="X自動投稿（Claude API連携 + 画像自動添付）")
    parser.add_argument("--slot", required=True, choices=["morning", "noon", "evening"],
                        help="投稿時間帯: morning/noon/evening")
    parser.add_argument("--dry-run", action="store_true", help="生成のみ、投稿しない")
    parser.add_argument("--no-image", action="store_true", help="画像なしで投稿")
    args = parser.parse_args()

    print(f"[{datetime.now().isoformat()}] X自動投稿開始 (slot: {args.slot})")

    # 投稿文を生成
    api_key = load_secrets()
    print("Claude APIで投稿文を生成中...")
    text = generate_post(api_key, args.slot)
    print(f"生成された投稿 ({len(text)}文字):")
    print(f"  {text}")

    if len(text) > 280:
        print(f"WARNING: 文字数超過 ({len(text)}文字)。投稿をスキップします")
        sys.exit(1)

    # 最適な画像を選定
    image_path = None
    image_key = None
    if not args.no_image:
        image_path = find_best_image(text, args.slot)
        if image_path:
            image_key = str(image_path.relative_to(PHOTOS_DIR)).replace("\\", "/")
        else:
            print("画像なしで投稿します")

    if args.dry_run:
        print("[DRY RUN] 投稿はスキップされました")
        if image_path:
            print(f"[DRY RUN] 添付予定の画像: {image_key}")
        return

    # Xに投稿
    x_creds = load_x_credentials()
    tweet_id = post_to_x(x_creds, text, image_path=image_path)

    if tweet_id:
        log_post(text, tweet_id, args.slot, image=image_key)
        if image_key:
            mark_image_used(image_key)
        # Discord通知（成功）
        img_info = f"\n画像: {image_key}" if image_key else ""
        notify_discord(f"✅ X投稿完了 ({args.slot})\n\n{text}\n\nhttps://x.com/nambei_oyaji/status/{tweet_id}{img_info}")
        print("完了")
    else:
        # Discord通知（失敗）
        notify_discord(f"❌ X投稿失敗 ({args.slot})\n\n{text}")
        sys.exit(1)


if __name__ == "__main__":
    main()
