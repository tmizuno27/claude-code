"""
X (@prodhq27) 自動投稿スクリプト v2
Gumroad + RapidAPI 宣伝ツイートをキューからローテーションして投稿する。

使い方:
  python x_auto_post_v2.py           # キューから次のツイートを投稿
  python x_auto_post_v2.py --dry-run # 投稿せずに内容のみ表示

認証ファイル:
  gumroad-notion/config/x-credentials.json
  {
    "api_key": "...",
    "api_key_secret": "...",
    "access_token": "...",
    "access_token_secret": "..."
  }

ログ:
  logs/misc/x-prodhq27-posts.log

キュー管理:
  gumroad-notion/config/x-queue-state.json  (投稿済みインデックスを保持)
"""

import argparse
import io
import json
import random
import sys
import time
from datetime import datetime
from pathlib import Path

# Windows cp932 エンコードエラー回避
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding="utf-8", errors="replace")

try:
    import tweepy
except ImportError:
    print("ERROR: tweepy がインストールされていません。pip install tweepy")
    sys.exit(1)

# ---- パス設定 ----
BASE_DIR = Path(__file__).parent.parent  # gumroad-notion/
CONFIG_DIR = BASE_DIR / "config"
X_CREDS_FILE = CONFIG_DIR / "x-credentials.json"
QUEUE_STATE_FILE = CONFIG_DIR / "x-queue-state.json"
LOG_FILE = (
    Path(__file__).parent.parent.parent.parent  # claude-code/
    / "logs" / "misc" / "x-prodhq27-posts.log"
)

# ---- ツイートキュー ----
# 価値ツイート 8割: 宣伝 2割 のルールに基づき編成
# RapidAPI 宣伝 10本 + Gumroad 宣伝 5本 = 15本 → 1サイクル
TWEET_QUEUE = [
    # ---- Value tweets (developer tips) ----
    "Always validate emails before sending campaigns.\n\nSyntax ≠ deliverability. Check MX records and disposable domains too.\n\nFree email validation API:\nhttps://rapidapi.com/t-mizuno27/api/email-validation-api\n\n#EmailMarketing #Developer #API",

    "Quick SEO audit before every deploy saves hours of firefighting.\n\nCheck meta tags, headings, alt text, and broken links in one API call.\n\nhttps://rapidapi.com/t-mizuno27/api/seo-analyzer-api\n\n#SEO #WebDev #DevOps",

    "IP geolocation in < 50ms.\n\nCountry, city, timezone, ISP — one GET request, zero dependencies.\n\nFree: 100 lookups/mo\nhttps://rapidapi.com/t-mizuno27/api/ip-geolocation-api\n\n#API #WebDev #GeoIP",

    "Building a Notion productivity system that actually sticks?\n\nMost people over-engineer it. Start with:\n- Daily note\n- Task inbox\n- Weekly review\n\nTemplate → https://tatsuya27.gumroad.com\n\n#Notion #Productivity #PKM",

    "Automate website screenshots with one API call.\n\nNo Puppeteer server to maintain. No headless Chrome.\n\nFree tier: 100 screenshots/mo\nhttps://rapidapi.com/t-mizuno27/api/website-screenshot-api\n\n#WebDev #API #Automation",

    "n8n workflow tip: validate emails before adding to your list.\n\nOne HTTP node → email validation API → branch on result.\n\nSaves you from spam complaints.\n\nhttps://rapidapi.com/t-mizuno27/api/email-validation-api\n\n#n8n #Automation #NoCode",

    "QR codes on demand — no library, no server.\n\nCustom size, colors, error correction via API.\n\nhttps://rapidapi.com/t-mizuno27/api/qr-code-generator-api\n\n#API #QRCode #WebDev",

    "Running Llama 3.1 on Cloudflare Workers = fast + cheap AI.\n\nNo OpenAI key. No GPU billing. Free tier: 100 req/mo.\n\nhttps://rapidapi.com/t-mizuno27/api/ai-text-generation-api\n\n#AI #LLM #CloudflareWorkers #IndieHacker",

    # ---- Gumroad product tweets ----
    "15 Notion templates for indie hackers and freelancers.\n\nProject tracker, client CRM, content calendar, finance dashboard, and more.\n\nAll-in-one productivity OS:\nhttps://tatsuya27.gumroad.com\n\n#Notion #IndieHacker #Productivity",

    "Stop building the same n8n workflows from scratch.\n\nDone-for-you automation templates:\n- Lead capture\n- Email sequences\n- Content publishing\n- Invoice automation\n\nhttps://tatsuya27.gumroad.com\n\n#n8n #Automation #NoCode",

    # ---- More value tweets ----
    "Fraud detection starts with IP geolocation.\n\nFlag logins from unexpected countries. Block known VPN/proxy IPs.\n\nhttps://rapidapi.com/t-mizuno27/api/ip-geolocation-api\n\n#InfoSec #API #FraudPrevention",

    "High bounce rate killing your email deliverability?\n\nValidate before sending:\n✅ Syntax\n✅ Domain MX record\n✅ Not disposable\n\nhttps://rapidapi.com/t-mizuno27/api/email-validation-api\n\n#Email #SaaS #StartupTools",

    "Building a link aggregator, directory, or portfolio tool?\n\nAuto-generate website thumbnails with one API call.\n\nhttps://rapidapi.com/t-mizuno27/api/website-screenshot-api\n\n#SaaS #WebDev #BuildInPublic",

    "Paying $99/mo for Ahrefs just to run SEO audits?\n\nFree API: meta tags, headings, images, links, performance — one call.\n\n100 audits/mo, $0.\n\nhttps://rapidapi.com/t-mizuno27/api/seo-analyzer-api\n\n#SEO #API #IndieHacker",

    "Automate content creation with AI.\n\nProduct descriptions, email drafts, blog outlines — one API call.\n\nLlama 3.1 powered. Free tier to start.\n\nhttps://rapidapi.com/t-mizuno27/api/ai-text-generation-api\n\n#AI #ContentCreation #Automation",
]

COOLDOWN_MINUTES = 60  # 前回投稿からの最小間隔（分）


def load_credentials() -> dict:
    if not X_CREDS_FILE.exists():
        print(f"ERROR: 認証ファイルが見つかりません: {X_CREDS_FILE}")
        print("以下の形式で作成してください:")
        print(json.dumps({
            "api_key": "YOUR_API_KEY",
            "api_key_secret": "YOUR_API_KEY_SECRET",
            "access_token": "YOUR_ACCESS_TOKEN",
            "access_token_secret": "YOUR_ACCESS_TOKEN_SECRET"
        }, indent=2))
        sys.exit(1)
    return json.loads(X_CREDS_FILE.read_text(encoding="utf-8"))


def load_queue_state() -> dict:
    if not QUEUE_STATE_FILE.exists():
        return {"next_index": 0, "last_post_at": None}
    try:
        return json.loads(QUEUE_STATE_FILE.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError):
        return {"next_index": 0, "last_post_at": None}


def save_queue_state(state: dict):
    CONFIG_DIR.mkdir(parents=True, exist_ok=True)
    QUEUE_STATE_FILE.write_text(
        json.dumps(state, ensure_ascii=False, indent=2), encoding="utf-8"
    )


def log_result(status: str, tweet_id: str | None, text: str):
    LOG_FILE.parent.mkdir(parents=True, exist_ok=True)
    ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    if status == "OK" and tweet_id:
        line = f"[{ts}] OK: {text[:60].replace(chr(10), ' ')} - Tweet ID: {tweet_id}\n"
    else:
        line = f"[{ts}] ERROR: {status}\n"
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(line)


def get_next_tweet(state: dict) -> tuple[str, int]:
    """キューから次のツイートを取得。インデックスをローテーション"""
    idx = state.get("next_index", 0) % len(TWEET_QUEUE)
    return TWEET_QUEUE[idx], idx


def post_tweet(creds: dict, text: str, max_retries: int = 3) -> str | None:
    client = tweepy.Client(
        consumer_key=creds["api_key"],
        consumer_secret=creds["api_key_secret"],
        access_token=creds["access_token"],
        access_token_secret=creds["access_token_secret"],
    )

    for attempt in range(1, max_retries + 1):
        try:
            response = client.create_tweet(text=text)
            tweet_id = response.data["id"]
            print(f"OK: 投稿成功 (ID: {tweet_id})")
            return tweet_id
        except tweepy.errors.Forbidden as e:
            err_msg = str(e)
            print(f"WARNING: 403 Forbidden (attempt {attempt}/{max_retries}) - {err_msg}")
            if "duplicate" in err_msg.lower():
                # 重複エラーはリトライしても無意味
                print("ERROR: 重複ツイートのためスキップします")
                return None
            if attempt < max_retries:
                wait = 60 * attempt
                print(f"  {wait}秒後にリトライ...")
                time.sleep(wait)
            else:
                print("ERROR: 403エラーが続きます。X Developer Portalでアプリ権限(Read and Write)を確認してください")
                log_result("403 Forbidden - You are not permitted to perform this action.", None, text)
                return None
        except tweepy.errors.TooManyRequests as e:
            print(f"WARNING: 429 Rate Limit (attempt {attempt}/{max_retries}) - {e}")
            if attempt < max_retries:
                wait = 120 * attempt
                print(f"  {wait}秒後にリトライ...")
                time.sleep(wait)
            else:
                log_result("429 Too Many Requests", None, text)
                return None
        except tweepy.errors.TweepyException as e:
            print(f"ERROR: 投稿失敗 - {e}")
            log_result(str(e), None, text)
            return None
    return None


def main():
    parser = argparse.ArgumentParser(description="@prodhq27 X自動投稿")
    parser.add_argument("--dry-run", action="store_true", help="投稿せずに内容を表示")
    args = parser.parse_args()

    state = load_queue_state()

    # クールダウンチェック
    if not args.dry_run and state.get("last_post_at"):
        try:
            last = datetime.fromisoformat(state["last_post_at"])
            elapsed = (datetime.now() - last).total_seconds() / 60
            if elapsed < COOLDOWN_MINUTES:
                print(f"SKIP: 前回投稿から{int(elapsed)}分 (クールダウン: {COOLDOWN_MINUTES}分)")
                return
        except (ValueError, TypeError):
            pass

    text, idx = get_next_tweet(state)

    print(f"投稿内容 (キュー {idx + 1}/{len(TWEET_QUEUE)}):")
    print("-" * 50)
    print(text)
    print("-" * 50)
    print(f"文字数: {len(text)}")

    if args.dry_run:
        print("[DRY RUN] 投稿スキップ")
        return

    creds = load_credentials()
    tweet_id = post_tweet(creds, text)

    if tweet_id:
        log_result("OK", tweet_id, text)
        state["next_index"] = (idx + 1) % len(TWEET_QUEUE)
        state["last_post_at"] = datetime.now().isoformat()
        save_queue_state(state)
        print("完了")
    else:
        # 重複エラーの場合はインデックスを進めて次回は別のツイートを試みる
        state["next_index"] = (idx + 1) % len(TWEET_QUEUE)
        save_queue_state(state)
        sys.exit(1)


if __name__ == "__main__":
    main()
