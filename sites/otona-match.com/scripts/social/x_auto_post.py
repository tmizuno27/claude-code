"""
X (Twitter) 自動投稿スクリプト — otona-match.com用
Claude APIで投稿文を生成し、X APIで投稿する。

使い方:
  python x_auto_post.py --slot morning
  python x_auto_post.py --slot noon
  python x_auto_post.py --slot evening
  python x_auto_post.py --slot morning --dry-run    # 生成のみ
  python x_auto_post.py --slot noon --no-delay       # 遅延なし

注意:
  X API Free Tierでは投稿APIが制限されている場合があります。
  Basic plan ($100/mo) 以上が必要な可能性あり。
  詳細: https://developer.x.com/en/docs/twitter-api/getting-started/about-twitter-api
"""

import argparse
import io
import json
import random
import sys
import time
import urllib.request
from datetime import datetime
from pathlib import Path

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding="utf-8", errors="replace")

try:
    import anthropic
except ImportError:
    print("ERROR: anthropic がインストールされていません: pip install anthropic")
    sys.exit(1)

try:
    import tweepy
except ImportError:
    print("ERROR: tweepy がインストールされていません: pip install tweepy")
    sys.exit(1)


SITE_DIR = Path(__file__).parent.parent.parent
CONFIG_DIR = SITE_DIR / "config"
SECRETS_FILE = CONFIG_DIR / "secrets.json"
SETTINGS_FILE = CONFIG_DIR / "settings.json"
X_CREDS_FILE = CONFIG_DIR / "x-credentials.json"
LOG_DIR = SITE_DIR / "outputs" / "social"

COOLDOWN_MINUTES = 15

# otona-match.com 向けの時間帯設定
SLOT_CONFIG = {
    "morning": {
        "categories": ["マッチングアプリ活用術", "安全な出会い方"],
        "weights": [0.6, 0.4],
        "description": "朝の投稿。通勤時間帯に読まれやすい実用的なTips",
    },
    "noon": {
        "categories": ["体験談・リアルな声", "記事告知"],
        "weights": [0.5, 0.5],
        "description": "昼の投稿。昼休みに読まれるリアルな体験談や最新記事の紹介",
    },
    "evening": {
        "categories": ["年代別アドバイス", "デート・恋愛テクニック"],
        "weights": [0.5, 0.5],
        "description": "夜の投稿。帰宅後のリラックス時間に読まれる深めのアドバイス",
    },
}

SYSTEM_PROMPT = """あなたはX（Twitter）の投稿文を生成するアシスタントです。
以下のアカウント情報とルールに従って、1つの投稿文を生成してください。

## サイト情報
- サイト: 大人のマッチングナビ（otona-match.com）
- コンセプト: 30代・40代のための出会い系・マッチングアプリ徹底比較ガイド
- ターゲット: 30代〜40代の男女、真剣な出会いを探している人

## 投稿ルール（厳守）
1. 140文字以内（日本語）— 絶対に超えないこと
2. ハッシュタグは2〜3個（文字数に含む）
3. 絵文字は0〜1個
4. AI的な表現は禁止（「いかがでしたでしょうか」等）
5. 具体的な数字を入れる（料金・年齢層・成功率など）
6. 30代・40代の視点を必ず入れる
7. 自然な日本語で、親しみやすい語り口

## ハッシュタグ候補
メイン: #マッチングアプリ #出会い #婚活
サブ: #30代婚活 #40代婚活 #マッチングアプリ比較 #恋活 #出会い系

## コンテンツ方針
- 各アプリの料金・特徴の比較情報
- 30代・40代ならではのプロフィール改善アドバイス
- 安全に使うためのTips（詐欺対策・身バレ防止）
- 成功体験やデータに基づくアドバイス
- 最新のキャンペーン情報やアプリ動向

## 禁止事項
- 下品・露骨な表現
- 特定アプリの過度な宣伝（比較サイトとしての中立性を保つ）
- 未確認の成功率や統計の捏造
- ブログ運営ネタ（PV・SEO等）

## 出力形式
投稿文のみを出力してください。説明や前置きは不要です。"""


def get_last_post_time() -> datetime | None:
    """Read last successful post timestamp from log."""
    log_file = LOG_DIR / "x-post-log.jsonl"
    if not log_file.exists():
        return None
    try:
        lines = log_file.read_text(encoding="utf-8").strip().split("\n")
        for line in reversed(lines):
            try:
                entry = json.loads(line)
                ts = entry.get("timestamp")
                if ts:
                    return datetime.fromisoformat(ts)
            except (json.JSONDecodeError, KeyError, ValueError):
                continue
        return None
    except Exception:
        return None


def load_secrets() -> str:
    """Claude API key."""
    with open(SECRETS_FILE, "r", encoding="utf-8") as f:
        secrets = json.load(f)
    return secrets["claude_api"]["api_key"]


def load_x_credentials() -> dict:
    """X API credentials."""
    with open(X_CREDS_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def get_recent_posts() -> list[str]:
    """Get recent posts to avoid duplicates."""
    log_file = LOG_DIR / "x-post-log.jsonl"
    if not log_file.exists():
        return []
    posts = []
    lines = log_file.read_text(encoding="utf-8").strip().split("\n")
    for line in lines[-10:]:
        try:
            entry = json.loads(line)
            posts.append(entry["text"])
        except (json.JSONDecodeError, KeyError):
            continue
    return posts


def get_latest_articles() -> list[dict]:
    """Get latest articles from WordPress for article promotion tweets."""
    try:
        with open(SECRETS_FILE, "r", encoding="utf-8") as f:
            secrets = json.load(f)
        with open(SETTINGS_FILE, "r", encoding="utf-8") as f:
            settings = json.load(f)

        api_url = settings["wordpress"]["rest_api_url"]
        url = f"{api_url}/posts?per_page=5&status=publish&orderby=date&order=desc"

        import base64
        username = secrets["wordpress"]["username"]
        password = secrets["wordpress"]["app_password"]
        credentials = base64.b64encode(f"{username}:{password}".encode()).decode()

        req = urllib.request.Request(url)
        req.add_header("Authorization", f"Basic {credentials}")
        with urllib.request.urlopen(req, timeout=15) as resp:
            posts = json.loads(resp.read().decode("utf-8"))

        return [
            {"title": p["title"]["rendered"], "url": p["link"]}
            for p in posts[:5]
        ]
    except Exception as e:
        print(f"WARNING: 最新記事の取得に失敗 - {e}")
        return []


def generate_post(api_key: str, slot: str) -> str:
    """Generate tweet text via Claude API."""
    config = SLOT_CONFIG[slot]
    category = random.choices(config["categories"], weights=config["weights"], k=1)[0]

    recent = get_recent_posts()
    recent_text = ""
    if recent:
        recent_text = "\n\n## 直近の投稿（これらと似た内容は避けること）\n"
        for p in recent[-5:]:
            recent_text += f"- {p}\n"

    # Record promotion: include latest article info
    articles_text = ""
    if category == "記事告知":
        articles = get_latest_articles()
        if articles:
            articles_text = "\n\n## 最新記事（1つ選んで紹介してください）\n"
            for a in articles:
                articles_text += f"- {a['title']}: {a['url']}\n"

    user_prompt = f"""カテゴリ「{category}」の投稿を1つ生成してください。
{config['description']}

今日の日付: {datetime.now().strftime('%Y年%m月%d日')}
{recent_text}{articles_text}"""

    client = anthropic.Anthropic(api_key=api_key)
    response = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=256,
        system=SYSTEM_PROMPT,
        messages=[{"role": "user", "content": user_prompt}],
    )

    text = response.content[0].text.strip()
    if text.startswith('"') and text.endswith('"'):
        text = text[1:-1]
    if text.startswith("\u300c") and text.endswith("\u300d"):
        text = text[1:-1]
    return text


def post_to_x(creds: dict, text: str) -> str | None:
    """Post to X via v2 API."""
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


def notify_discord(message: str):
    """Send Discord notification."""
    try:
        with open(SETTINGS_FILE, "r", encoding="utf-8") as f:
            settings = json.load(f)
        webhook_url = settings.get("discord", {}).get("webhook_url")
        if not webhook_url:
            return
        payload = json.dumps({"content": message}).encode("utf-8")
        req = urllib.request.Request(
            webhook_url,
            data=payload,
            headers={"Content-Type": "application/json", "User-Agent": "X-AutoPost/1.0"},
        )
        urllib.request.urlopen(req)
    except Exception as e:
        print(f"WARNING: Discord通知失敗 - {e}")


def log_post(text: str, tweet_id: str, slot: str, category: str = "auto"):
    """Save post log."""
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
    parser = argparse.ArgumentParser(description="X自動投稿 — otona-match.com")
    parser.add_argument("--slot", required=True, choices=["morning", "noon", "evening"])
    parser.add_argument("--dry-run", action="store_true", help="生成のみ")
    parser.add_argument("--no-delay", action="store_true", help="ランダム遅延スキップ")
    args = parser.parse_args()

    # Cooldown check
    if not args.dry_run:
        last_post = get_last_post_time()
        if last_post:
            elapsed = (datetime.now() - last_post).total_seconds() / 60
            if elapsed < COOLDOWN_MINUTES:
                print(f"SKIP: 前回投稿から{int(elapsed)}分（cooldown: {COOLDOWN_MINUTES}分）")
                return

    # Random delay (0-60min)
    if not args.dry_run and not args.no_delay:
        delay_seconds = random.randint(0, 60 * 60)
        print(f"[{datetime.now().isoformat()}] ランダム遅延: {delay_seconds // 60}分{delay_seconds % 60}秒")
        time.sleep(delay_seconds)

    print(f"[{datetime.now().isoformat()}] X自動投稿開始 (slot: {args.slot}, site: otona-match.com)")

    api_key = load_secrets()
    print("Claude APIで投稿文を生成中...")
    text = generate_post(api_key, args.slot)
    print(f"生成された投稿 ({len(text)}文字): {text}")

    if len(text) > 280:
        print(f"WARNING: 文字数超過 ({len(text)}文字)。スキップ")
        sys.exit(1)

    if args.dry_run:
        print("[DRY RUN] 投稿はスキップされました")
        return

    # Check if x-credentials.json exists
    if not X_CREDS_FILE.exists():
        print(f"ERROR: X認証ファイルが見つかりません: {X_CREDS_FILE}")
        print("otona-match.com用のXアカウントを設定してください")
        log_post(text, "no-credentials", args.slot, category="failed")
        sys.exit(1)

    x_creds = load_x_credentials()
    tweet_id = post_to_x(x_creds, text)

    if tweet_id:
        log_post(text, tweet_id, args.slot)
        account = x_creds.get("account", "unknown")
        notify_discord(f"[otona-match] X投稿完了 ({args.slot})\n\n{text}\n\nhttps://x.com/{account}/status/{tweet_id}")
        print("完了")
    else:
        notify_discord(f"[otona-match] X投稿失敗 ({args.slot})\n\n{text}")
        sys.exit(1)


if __name__ == "__main__":
    main()
