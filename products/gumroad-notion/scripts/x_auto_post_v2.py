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
# カテゴリ: RapidAPI(15) + Gumroad(10) + Chrome/VSCode拡張(8) + keisan-tools(8) + ブログ3サイト(20) = 61本
TWEET_QUEUE = [
    # ==============================
    # RapidAPI — 価値ツイート & 宣伝
    # ==============================
    "Always validate emails before sending campaigns.\n\nSyntax ≠ deliverability. Check MX records and disposable domains too.\n\nFree email validation API:\nhttps://rapidapi.com/t-mizuno27/api/email-validation-api\n\n#EmailMarketing #Developer #API",

    "Quick SEO audit before every deploy saves hours of firefighting.\n\nCheck meta tags, headings, alt text, and broken links in one API call.\n\nhttps://rapidapi.com/t-mizuno27/api/seo-analyzer-api\n\n#SEO #WebDev #DevOps",

    "IP geolocation in < 50ms.\n\nCountry, city, timezone, ISP — one GET request, zero dependencies.\n\nFree: 100 lookups/mo\nhttps://rapidapi.com/t-mizuno27/api/ip-geolocation-api\n\n#API #WebDev #GeoIP",

    "Automate website screenshots with one API call.\n\nNo Puppeteer server to maintain. No headless Chrome.\n\nFree tier: 100 screenshots/mo\nhttps://rapidapi.com/t-mizuno27/api/website-screenshot-api\n\n#WebDev #API #Automation",

    "n8n workflow tip: validate emails before adding to your list.\n\nOne HTTP node → email validation API → branch on result.\n\nSaves you from spam complaints.\n\nhttps://rapidapi.com/t-mizuno27/api/email-validation-api\n\n#n8n #Automation #NoCode",

    "QR codes on demand — no library, no server.\n\nCustom size, colors, error correction via API.\n\nhttps://rapidapi.com/t-mizuno27/api/qr-code-generator-api\n\n#API #QRCode #WebDev",

    "Running Llama 3.1 on Cloudflare Workers = fast + cheap AI.\n\nNo OpenAI key. No GPU billing. Free tier: 100 req/mo.\n\nhttps://rapidapi.com/t-mizuno27/api/ai-text-generation-api\n\n#AI #LLM #CloudflareWorkers #IndieHacker",

    "Fraud detection starts with IP geolocation.\n\nFlag logins from unexpected countries. Block known VPN/proxy IPs.\n\nhttps://rapidapi.com/t-mizuno27/api/ip-geolocation-api\n\n#InfoSec #API #FraudPrevention",

    "High bounce rate killing your email deliverability?\n\nValidate before sending:\n✅ Syntax\n✅ Domain MX record\n✅ Not disposable\n\nhttps://rapidapi.com/t-mizuno27/api/email-validation-api\n\n#Email #SaaS #StartupTools",

    "Building a link aggregator, directory, or portfolio tool?\n\nAuto-generate website thumbnails with one API call.\n\nhttps://rapidapi.com/t-mizuno27/api/website-screenshot-api\n\n#SaaS #WebDev #BuildInPublic",

    "Paying $99/mo for Ahrefs just to run SEO audits?\n\nFree API: meta tags, headings, images, links, performance — one call.\n\n100 audits/mo, $0.\n\nhttps://rapidapi.com/t-mizuno27/api/seo-analyzer-api\n\n#SEO #API #IndieHacker",

    "Automate content creation with AI.\n\nProduct descriptions, email drafts, blog outlines — one API call.\n\nLlama 3.1 powered. Free tier to start.\n\nhttps://rapidapi.com/t-mizuno27/api/ai-text-generation-api\n\n#AI #ContentCreation #Automation",

    "Need WHOIS data in your app? Skip the manual lookups.\n\nDomain registration, expiry, registrar — one API call.\n\nFree tier available:\nhttps://rapidapi.com/t-mizuno27/api/whois-lookup-api\n\n#API #DomainTools #WebDev",

    "Currency conversion in real-time.\n\n170+ currencies, live exchange rates, historical data.\n\nPerfect for e-commerce, fintech, and travel apps.\nhttps://rapidapi.com/t-mizuno27/api/currency-exchange-rate-api\n\n#Fintech #API #WebDev",

    "Text to speech without a subscription.\n\nMultiple languages, natural voices, MP3 output.\n\nFree 100 requests/mo:\nhttps://rapidapi.com/t-mizuno27/api/text-to-speech-api\n\n#TTS #AI #API #Accessibility",

    # ==============================
    # Gumroad — Notion & AI Prompts
    # ==============================
    "15 Notion templates for indie hackers and freelancers.\n\nProject tracker, client CRM, content calendar, finance dashboard, and more.\n\nAll-in-one productivity OS:\nhttps://tatsuya27.gumroad.com\n\n#Notion #IndieHacker #Productivity",

    "Building a blog with AI? You need the right prompts.\n\n130+ proven prompts for:\n- SEO outlines\n- Article drafts\n- Meta descriptions\n- Internal linking\n\nUltimate AI Blogger Bundle → https://tatsuya27.gumroad.com\n\n#AI #Blogging #SEO",

    "ADHD brain needs a different productivity system.\n\nThis Notion template is built for non-linear thinkers:\n- Quick capture inbox\n- Time-blocked daily view\n- Energy-level task sorting\n\nhttps://tatsuya27.gumroad.com\n\n#ADHD #Notion #Productivity",

    "Manage your Airbnb like a pro — without expensive software.\n\nNotion template: guest tracker, cleaning schedule, review log, profit dashboard.\n\nhttps://tatsuya27.gumroad.com\n\n#Airbnb #NotionTemplate #PassiveIncome",

    "Track your personal finances in Notion — not Excel.\n\nMonthly budget, net worth tracker, expense categories, savings goals.\n\nOne-time $9, yours forever:\nhttps://tatsuya27.gumroad.com\n\n#PersonalFinance #Notion #MoneyManagement",

    "Run a side hustle with AI? You still need a system.\n\nAI Side Hustle Starter Kit — Notion dashboard + 50 prompts for:\n- Content creation\n- Client outreach\n- Income tracking\n\nhttps://tatsuya27.gumroad.com\n\n#SideHustle #AI #IndieHacker",

    "Social media content in 10 minutes a week.\n\nSocial Media Marketing Mega Prompt Pack — 60+ prompts for:\n- Instagram captions\n- Twitter threads\n- LinkedIn posts\n- Content calendars\n\nhttps://tatsuya27.gumroad.com\n\n#SocialMedia #AI #ContentCreation",

    "Planning a startup launch? Don't miss critical steps.\n\nStartup Launch Checklist Notion template:\n- Legal setup\n- Product validation\n- Landing page\n- Launch day checklist\n\nhttps://tatsuya27.gumroad.com\n\n#Startup #ProductLaunch #Notion",

    "Write better WordPress content with AI — 3x faster.\n\nWordPress Automation Prompt Kit: 40+ prompts for posts, pages, meta, categories.\n\nOne-time purchase, instant download:\nhttps://tatsuya27.gumroad.com\n\n#WordPress #AI #Blogging",

    "Affiliate blogging on autopilot.\n\nAffiliate Content Generator prompt pack: review templates, comparison articles, CTA frameworks — built for conversions.\n\nhttps://tatsuya27.gumroad.com\n\n#AffiliateMarketing #Blogging #AI",

    # ==============================
    # Chrome & VS Code Extensions
    # ==============================
    "Check page speed without leaving your browser.\n\nPage Speed Checker Chrome extension: Core Web Vitals, load time, performance score — one click.\n\nFree on Chrome Web Store:\nhttps://chromewebstore.google.com/search/page%20speed%20checker\n\n#WebDev #SEO #ChromeExtension",

    "Test regex patterns as you type — no more regex101 tab-switching.\n\nRegex Tester Chrome extension: live match highlighting, group capture, flags.\n\nFree:\nhttps://chromewebstore.google.com/search/regex%20tester\n\n#Developer #RegEx #ChromeExtension",

    "Hash & encode text without a single server call.\n\nMD5, SHA-256, Base64, URL encode — all in your browser.\n\nPrivacy-first Chrome extension:\nhttps://chromewebstore.google.com/search/hash%20encode%20tool\n\n#Security #Developer #ChromeExtension",

    "Pick any color from any webpage — instantly.\n\nColor Picker Chrome extension: HEX, RGB, HSL output. Copy with one click.\n\nFree:\nhttps://chromewebstore.google.com/search/color%20picker\n\n#Design #WebDev #ChromeExtension",

    "Format JSON instantly in VS Code.\n\nJSON Formatter extension: pretty print, minify, validate — keyboard shortcut ready.\n\nFree on VS Code Marketplace:\nhttps://marketplace.visualstudio.com/search?term=json%20formatter&target=VSCode\n\n#VSCode #Developer #JSON",

    "Generate Lorem Ipsum without leaving your editor.\n\nLorem Ipsum Generator VS Code extension: paragraphs, sentences, words — configurable.\n\nhttps://marketplace.visualstudio.com/search?term=lorem%20ipsum%20generator&target=VSCode\n\n#VSCode #WebDev #DeveloperTools",

    "AI-powered text rewriting in VS Code.\n\nSelect text → rewrite for tone, clarity, or SEO — powered by Claude API.\n\nhttps://marketplace.visualstudio.com/search?term=ai%20text%20rewriter&target=VSCode\n\n#VSCode #AI #Writing",

    "Inspect any webpage's SEO data without leaving Chrome.\n\nSEO Inspector extension: title, meta, headings, canonical, Open Graph — one click.\n\nFree:\nhttps://chromewebstore.google.com/search/seo%20inspector\n\n#SEO #ChromeExtension #WebDev",

    # ==============================
    # keisan-tools（計算ツールサイト）
    # ==============================
    "消費税の計算、毎回電卓で叩いてませんか？\n\nkeisan-toolsなら税込・税抜・税額を瞬時に計算。\n\n463種類の計算ツールが無料で使えます：\nhttps://keisan-tools.vercel.app/\n\n#消費税計算 #計算ツール #無料",

    "BMIの計算ってどうやるんだっけ？\n\n体重(kg) ÷ 身長(m)² = BMI。標準は18.5〜24.9。\n\nkeisan-toolsで即計算 →\nhttps://keisan-tools.vercel.app/\n\n#BMI #健康管理 #計算ツール",

    "ローンの月々の返済額、正確に計算できますか？\n\n元利均等返済なら公式があります。でも面倒なのでツールで。\n\n住宅ローン計算 →\nhttps://keisan-tools.vercel.app/\n\n#住宅ローン #ローン計算 #資産形成",

    "カロリー計算、自分でやると複雑すぎる。\n\nkeisan-toolsのカロリー消費計算ツール：\n体重・運動種類・時間を入れるだけ。\n\nhttps://keisan-tools.vercel.app/\n\n#ダイエット #カロリー計算 #健康",

    "為替レートの計算、銀行のサイトでやるの面倒くないですか？\n\nkeisan-toolsで円→ドル→円をサクッと計算。\n\nhttps://keisan-tools.vercel.app/\n\n#為替計算 #海外送金 #FX",

    "日数計算、意外とみんな間違えてる。\n\n「3月15日から4月10日は何日？」→ 26日です。\n\nkeisan-toolsで日数・期間を正確に計算：\nhttps://keisan-tools.vercel.app/\n\n#日数計算 #期間計算 #便利ツール",

    "電気代の計算、自分でやってみたことある？\n\n消費電力(W) × 使用時間 × 電気料金単価 ÷ 1000 = 円。\n\nkeisan-toolsで家電ごとの電気代を自動計算：\nhttps://keisan-tools.vercel.app/\n\n#電気代 #節約 #計算ツール",

    "退職金の手取り計算、税金で思ったより減る。\n\n退職所得控除を引いてから2分の1課税。\n\nkeisan-toolsで退職金の手取り額を計算：\nhttps://keisan-tools.vercel.app/\n\n#退職金 #税金 #老後資金",

    # ==============================
    # nambei-oyaji.com（南米おやじ）
    # ==============================
    "パラグアイ移住して3年経った。\n\n光熱費月4,500円。外食ランチ400円。牛肉1kg600円。\n\n生活費は東京時代の3分の1。でも家族の時間は3倍になった。\n\n移住の全記録 → https://nambei-oyaji.com/\n\n#パラグアイ移住 #海外生活費",

    "「パラグアイって危険じゃないの？」\n\n毎回同じ質問をされる。正直に答える。\n\n昼間のアスンシオン日本人エリアは普通に安全。東京の夜より落ち着いてる場所もある。「どの程度の注意が必要か」で判断すべき。\n\nhttps://nambei-oyaji.com/\n\n#パラグアイ #海外移住の現実",

    "パラグアイ永住権の費用、実際いくらかかったか公開する。\n\n弁護士費用18万円 + 定期預金70万円 + 書類代3万円 = 約100万円。\n\n欧米移住の5分の1以下で南米の永住権が取れる。詳細 → https://nambei-oyaji.com/paraguay-visa-guide/\n\n#パラグアイ永住権 #海外移住費用",

    "子供のスペイン語習得、移住9ヶ月で現地の子と普通に遊べるようになった。\n\n月15万円のインターナショナルスクール不要。生きた言語環境に放り込むのが最速。\n\n親の私がまだ食堂で苦戦してるのが恥ずかしい。\n\nhttps://nambei-oyaji.com/\n\n#パラグアイ子育て #バイリンガル教育",

    "移住して一番変わったのは「時間」だった。\n\n日本時代：子供の顔を見るのは寝顔だけ。\nパラグアイ：毎日お迎えに行って、夕飯を一緒に食べる。\n\n収入3割減、生活費半分以下。トータルで豊かになった。\n\nhttps://nambei-oyaji.com/\n\n#海外移住 #ワークライフバランス",

    # ==============================
    # otona-match.com（大人のマッチング）
    # ==============================
    "30代・40代でマッチングアプリを始めるのは遅い？\n\n全然そんなことない。むしろ真剣に出会いを求めてる層が多い。\n\n年齢別・目的別のおすすめアプリ比較 →\nhttps://otona-match.com/\n\n#マッチングアプリ #婚活 #30代",

    "マッチングアプリ、月5,000円以上払ってるなら見直す価値あり。\n\n同じ機能のアプリで月2,000円のものも多い。\n\n料金・機能・マッチング率を徹底比較：\nhttps://otona-match.com/\n\n#マッチングアプリ比較 #婚活費用",

    "真剣な出会いを求めるなら「ゼクシィ縁結び」一択という時代は終わった。\n\nwith、Omiai、ペアーズが逆転。理由は料金・機能・ユーザー層の変化。\n\n2026年版比較 → https://otona-match.com/\n\n#マッチングアプリ2026 #婚活",

    "マッチングアプリのプロフィール写真、1枚と5枚でマッチ率が3倍変わる。\n\n実際のデータで証明されてる話。\n\nプロフィール最適化ガイド →\nhttps://otona-match.com/\n\n#マッチングアプリ #プロフィール #婚活",

    "バツイチ・子持ちでマッチングアプリ、正直どう？\n\n実体験を交えて比較レビューしてます。\n\n理解ある相手を見つけやすいアプリ・避けるべきアプリの見分け方：\nhttps://otona-match.com/\n\n#バツイチ婚活 #再婚 #マッチングアプリ",

    # ==============================
    # sim-hikaku.online（SIM比較）
    # ==============================
    "格安SIMに乗り換えるだけで月5,000円節約できる時代。\n\n大手キャリアと格安SIMの料金差、2026年最新版で比較してます。\n\nhttps://sim-hikaku.online/\n\n#格安SIM #スマホ代節約 #SIM比較",

    "楽天モバイルって結局どうなの？\n\n3GBまで無料の時代は終わったけど、今でも安い。最新プラン・エリアカバー率・通話品質を整理しました。\n\nhttps://sim-hikaku.online/\n\n#楽天モバイル #格安SIM #スマホ代",

    "iPhoneでも格安SIMは使えます。\n\nキャリア版・SIMフリー版の違いと、動作確認済みSIMの選び方。\n\n初めての乗り換えガイド →\nhttps://sim-hikaku.online/\n\n#格安SIM #iPhone #乗り換え",

    "データ無制限プラン、本当に無制限？\n\n速度制限の条件・閾値・混雑時の実速度を比較。\n「無制限」の罠を解説します。\n\nhttps://sim-hikaku.online/\n\n#格安SIM #無制限 #データ通信",

    "家族4人のスマホ代、大手キャリアのままだと月2万円超えてる可能性。\n\n格安SIMに家族全員で乗り換えると月7,000〜9,000円が相場。\n\n家族向けプラン比較 →\nhttps://sim-hikaku.online/\n\n#格安SIM家族 #スマホ代節約 #SIM乗り換え",
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
