"""
X (Twitter) 自動投稿スクリプト（Claude API連携）
毎回Claude APIで投稿文を生成し、自動でXに投稿する

使い方:
  python x_auto_post.py --slot morning   # 朝の投稿（JST 7:00-8:00向け）
  python x_auto_post.py --slot noon      # 昼の投稿（JST 12:00-13:00向け）
  python x_auto_post.py --slot evening   # 夜の投稿（JST 20:00-21:00向け）
  python x_auto_post.py --slot morning --dry-run  # 生成のみ、投稿しない
"""

import argparse
import json
import random
import sys
from datetime import datetime
from pathlib import Path

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
SECRETS_FILE = CONFIG_DIR / "secrets.json"
X_CREDS_FILE = CONFIG_DIR / "x-credentials.json"
LOG_DIR = Path(__file__).parent.parent / "outputs" / "social"

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


def post_to_x(creds: dict, text: str) -> str | None:
    """Xに投稿"""
    client = tweepy.Client(
        consumer_key=creds["api_key"],
        consumer_secret=creds["api_key_secret"],
        access_token=creds["access_token"],
        access_token_secret=creds["access_token_secret"],
    )

    try:
        response = client.create_tweet(text=text)
        tweet_id = response.data["id"]
        print(f"OK: 投稿成功 (ID: {tweet_id})")
        return tweet_id
    except tweepy.errors.TweepyException as e:
        print(f"ERROR: 投稿失敗 - {e}")
        return None


def log_post(text: str, tweet_id: str, slot: str, category: str = "auto"):
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
    }

    with open(log_file, "a", encoding="utf-8") as f:
        f.write(json.dumps(entry, ensure_ascii=False) + "\n")


def main():
    parser = argparse.ArgumentParser(description="X自動投稿（Claude API連携）")
    parser.add_argument("--slot", required=True, choices=["morning", "noon", "evening"],
                        help="投稿時間帯: morning/noon/evening")
    parser.add_argument("--dry-run", action="store_true", help="生成のみ、投稿しない")
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

    if args.dry_run:
        print("[DRY RUN] 投稿はスキップされました")
        return

    # Xに投稿
    x_creds = load_x_credentials()
    tweet_id = post_to_x(x_creds, text)

    if tweet_id:
        log_post(text, tweet_id, args.slot)
        print("完了")
    else:
        sys.exit(1)


if __name__ == "__main__":
    main()
