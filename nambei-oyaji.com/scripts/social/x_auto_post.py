"""
X (Twitter) 自動投稿スクリプト（Claude API連携 + 画像自動添付 + 承認フロー）
毎回Claude APIで投稿文を生成し、Discordで承認後に投稿する

使い方:
  python x_auto_post.py --slot morning   # 朝の投稿（承認フロー付き）
  python x_auto_post.py --slot noon      # 昼の投稿（承認フロー付き）
  python x_auto_post.py --slot evening   # 夜の投稿（承認フロー付き）
  python x_auto_post.py --slot morning --dry-run    # 生成のみ、投稿しない
  python x_auto_post.py --slot noon --no-image      # 画像なしで投稿
  python x_auto_post.py --slot morning --no-approval  # 承認なしで即投稿（旧動作）

承認フロー:
  1. ツイート生成 → pending-tweets.json に保存 → Discordにプレビュー送信
  2. 30分間待機（スマホからGitHub経由で編集・キャンセル可能）
  3. 30分後に自動投稿（何もしなければそのまま投稿）
  4. pending-tweets.json の status を "skip" にするとキャンセル
  5. text を編集すると編集後の内容で投稿
"""

import argparse
import io
import json
import random
import subprocess
import sys
import time
import urllib.request
from datetime import datetime, timedelta
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


BLOG_DIR = Path(__file__).parent.parent.parent
CONFIG_DIR = BLOG_DIR / "config"
SETTINGS_FILE = CONFIG_DIR / "settings.json"
SECRETS_FILE = CONFIG_DIR / "secrets.json"
X_CREDS_FILE = CONFIG_DIR / "x-credentials.json"
LOG_DIR = BLOG_DIR / "outputs" / "social"
PENDING_FILE = LOG_DIR / "pending-tweets.json"
PHOTOS_DIR = BLOG_DIR / "images" / "sns-photos"
TAGS_FILE = PHOTOS_DIR / "tags.json"

# 承認フロー設定
APPROVAL_TIMEOUT_MIN = 30  # 自動承認までの待機時間（分）
APPROVAL_CHECK_INTERVAL = 30  # チェック間隔（秒）

# GitHub上のpending-tweets.jsonへの直接編集リンク
GITHUB_EDIT_URL = "https://github.com/tmizuno27/claude-code/edit/main/blog/outputs/social/pending-tweets.json"
GITHUB_VIEW_URL = "https://github.com/tmizuno27/claude-code/blob/main/blog/outputs/social/pending-tweets.json"

# 時間帯ごとのカテゴリ設定
SLOT_CONFIG = {
    "morning": {
        "categories": ["パラグアイ生活Tips", "移住準備・手続き"],
        "weights": [0.6, 0.4],
        "description": "朝の投稿（JST 7:00-8:00）通勤時間帯。パラグアイの生活情報や移住ノウハウで「こんな暮らしがあるんだ」と興味を引く",
    },
    "noon": {
        "categories": ["パラグアイ日常", "記事告知"],
        "weights": [0.6, 0.4],
        "description": "昼の投稿（JST 12:00-13:00）昼休み。パラグアイの食事・風景・日常の一コマで癒し＆興味喚起。記事告知の場合はブログ記事の紹介",
    },
    "evening": {
        "categories": ["海外からの稼ぎ方", "パラグアイ子育て・家族"],
        "weights": [0.5, 0.5],
        "description": "夜の投稿（JST 20:30-21:30）帰宅後。海外移住後の仕事・収入の話や、家族4人のパラグアイ生活エピソードで共感を得る",
    },
}

SYSTEM_PROMPT = """あなたはX（Twitter）の投稿文を生成するアシスタントです。
以下のアカウント情報とルールに従って、1つの投稿文を生成してください。

## アカウント情報
- アカウント: @nambei_oyaji（南米おやじ）
- コンセプト: 「住んでいるから、書けることがある」— パラグアイ在住の日本人家族4人のリアルな海外生活を発信
- ペルソナ: カジュアルで正直なおやじ。数字で語る。失敗も隠さない。生活者目線

## 重要：コンテンツの方向性
- メインテーマは「パラグアイ移住・海外生活」。一次情報（実体験・現地データ）が最大の強み
- AI・ChatGPT・副業ツールの話題は禁止。AIを記事の主題にしない
- 「海外からの稼ぎ方」はOKだが、リモートワーク・フリーランス・Webライターなど具体的な働き方の話にする（AI副業NG）
- ブログ運営ネタ（PV・SEO等）も禁止。読者にとって価値のない内輪話は出さない

## 投稿ルール（厳守）
1. 140文字以内（日本語）— これは絶対に超えないこと
2. ハッシュタグは2〜3個（文字数に含む）
3. 絵文字は0〜1個（多用しない）
4. AI的な表現は禁止（「いかがでしたでしょうか」等）
5. 具体的な数字を入れる（物価・費用・気温など）
6. 自然な日本語で、おやじが日常をつぶやいている感じ
7. 「パラグアイに住んでいる人」としてのリアルな視点を必ず入れる

## メインハッシュタグ（毎回1つ選ぶ）
#パラグアイ #海外移住 #パラグアイ移住 #南米おやじ

## サブハッシュタグ（毎回1-2個選ぶ）
#海外生活 #移住生活 #パラグアイ生活 #海外子育て #南米生活 #海外移住準備 #リモートワーク

## パラグアイの実情（投稿ネタとして積極的に使う）
- 生活費が日本の1/3〜1/2（ランチ200-300円、牛肉1kg 700-900円、鶏肉1kg 300円）
- 家賃：一軒家3LDKで月3-5万円
- 所得税が最大10%、法人税10%。税金が世界的に見ても安い
- 地震・台風・津波なし。一年中温暖（冬の平均気温17-19℃、最低12-14℃程度）。自然災害リスクほぼゼロ
- 花粉ゼロ（日本では1年の1/4が花粉症で潰れていた。薬代年2万円→ゼロに）
- 小学生の娘2人がインターナショナルスクールに通学中。学費月約3万円（日本なら15-20万円）
- 英語+スペイン語+日本語のトリリンガル教育を目指している
- アサード（南米BBQ）が週末の定番。牛肉2kgで約1,500-1,800円
- テレレ（冷たいマテ茶）が国民的飲み物
- 永住権が比較的取りやすい（まず2年の一時滞在ビザ→その後永住権申請。費用は書類+銀行預金$5,000程度）
- 外国人でも土地・不動産を購入可能
- 日系社会90年の歴史がある。日本人コミュニティあり
- パラグアイから日本の仕事をリモートでやっている（時差12時間を活用）
- Wise等の海外送金サービスで日本⇔パラグアイの送金を管理
- VPNを使って日本のサービス（動画配信等）にアクセス
- 周辺国（ブラジル・アルゼンチン・ウルグアイ）への旅行がしやすい
- サッカーが生活の一部。夕方にヨーロッパサッカーが見られる

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


FACT_CHECK_PROMPT = """あなたはファクトチェッカーです。以下のX投稿文に事実誤認がないか検証してください。

## 検証基準（正しい情報）
- 生活費が日本の1/3〜1/2（ランチ200-300円、牛肉1kg 700-900円、鶏肉1kg 300円）
- 家賃：一軒家3LDKで月3-5万円
- 所得税が最大10%、法人税10%
- 地震・台風・津波なし。一年中温暖（冬の平均気温17-19℃、最低12-14℃程度）
- 花粉ゼロ（日本では薬代年2万円→ゼロに）
- 娘2人（8歳・6歳）がインターナショナルスクールに通学中。学費月約3万円
- アサード：牛肉2kgで約1,500-1,800円
- 永住権：まず2年の一時滞在ビザ→その後永住権申請。費用は書類+銀行預金$5,000程度
- 外国人でも土地・不動産を購入可能
- 日系社会90年の歴史
- 時差12時間（日本との）
- 家族4人（夫婦+娘2人）

## 判定ルール
1. 上記の基準と矛盾する数字・事実があれば「NG」
2. 基準にない数字・統計・法律・手続きの記載があり、正確性が確認できない場合も「NG」
3. 数字を含まない感想・日常ツイートや、基準と一致する情報のみの場合は「OK」

## 出力形式（厳守）
1行目に「OK」または「NG」のみ。
NGの場合、2行目に理由を簡潔に記載。"""


def fact_check_post(api_key: str, text: str) -> tuple[bool, str]:
    """生成された投稿文をファクトチェックする。(passed, reason) を返す"""
    client = anthropic.Anthropic(api_key=api_key)
    response = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=128,
        system=FACT_CHECK_PROMPT,
        messages=[{"role": "user", "content": f"投稿文:\n{text}"}],
    )
    result = response.content[0].text.strip()
    lines = result.split("\n", 1)
    verdict = lines[0].strip().upper()
    reason = lines[1].strip() if len(lines) > 1 else ""
    return verdict == "OK", reason


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


DASHBOARD_URL = "https://htmlpreview.github.io/?https://gist.githubusercontent.com/tmizuno27/16a8680cadf8aed0c207777f7468963b/raw/daily-business-dashboard.html"


def notify_discord(message: str):
    """Discord Webhookで通知を送信（ダッシュボードリンク付き）"""
    try:
        with open(SETTINGS_FILE, "r", encoding="utf-8") as f:
            settings = json.load(f)
        webhook_url = settings.get("discord", {}).get("webhook_url")
        if not webhook_url:
            print("Discord Webhook URLが設定されていません")
            return
        message_with_link = f"{message}\n\n📊 [ダッシュボード]({DASHBOARD_URL})"
        payload = json.dumps({"content": message_with_link}).encode("utf-8")
        req = urllib.request.Request(
            webhook_url,
            data=payload,
            headers={"Content-Type": "application/json", "User-Agent": "X-AutoPost/1.0"},
        )
        urllib.request.urlopen(req)
        print("Discord通知を送信しました")
    except Exception as e:
        print(f"WARNING: Discord通知の送信に失敗 - {e}")


def save_pending_tweet(text: str, slot: str, image_key: str | None, image_path: Path | None):
    """承認待ちツイートをJSONファイルに保存"""
    LOG_DIR.mkdir(parents=True, exist_ok=True)
    auto_post_at = datetime.now() + timedelta(minutes=APPROVAL_TIMEOUT_MIN)

    pending = {
        "status": "pending",  # pending / approved / skip
        "text": text,
        "slot": slot,
        "image_key": image_key,
        "image_path": str(image_path) if image_path else None,
        "created_at": datetime.now().isoformat(),
        "auto_post_at": auto_post_at.isoformat(),
        "note": "編集方法: text を変更→編集後の内容で投稿。status を skip に変更→キャンセル。何もしなければ30分後に自動投稿。",
    }

    with open(PENDING_FILE, "w", encoding="utf-8") as f:
        json.dump(pending, f, ensure_ascii=False, indent=2)
    print(f"承認待ちツイートを保存: {PENDING_FILE}")


def load_pending_tweet() -> dict | None:
    """承認待ちツイートを読み込む"""
    if not PENDING_FILE.exists():
        return None
    try:
        with open(PENDING_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except (json.JSONDecodeError, OSError):
        return None


def clear_pending_tweet():
    """承認待ちファイルをクリア"""
    if PENDING_FILE.exists():
        PENDING_FILE.unlink()


def git_pull():
    """GitHubからの変更を取得（スマホ編集を反映するため）"""
    repo_dir = BLOG_DIR.parent  # claude-code/
    try:
        result = subprocess.run(
            ["git", "pull", "--no-rebase", "origin", "main"],
            cwd=str(repo_dir),
            capture_output=True,
            text=True,
            timeout=30,
        )
        if result.returncode == 0 and "Already up to date" not in result.stdout:
            print(f"git pull: 変更を取得しました")
        return result.returncode == 0
    except Exception as e:
        print(f"WARNING: git pull 失敗 - {e}")
        return False


def notify_pending_tweet(text: str, slot: str, image_key: str | None):
    """Discordに承認待ちツイートのプレビューを送信"""
    img_info = f"\n📷 画像: {image_key}" if image_key else "\n📷 画像なし"
    auto_time = (datetime.now() + timedelta(minutes=APPROVAL_TIMEOUT_MIN)).strftime("%H:%M")

    message = (
        f"📝 **X投稿プレビュー** ({slot})\n"
        f"━━━━━━━━━━━━━━━\n"
        f"{text}\n"
        f"━━━━━━━━━━━━━━━\n"
        f"{img_info}\n"
        f"⏰ **{auto_time}** に自動投稿（{APPROVAL_TIMEOUT_MIN}分後）\n\n"
        f"✏️ 編集・キャンセルはこちら:\n{GITHUB_EDIT_URL}\n\n"
        f"・textを変更 → 編集後の内容で投稿\n"
        f"・statusを「skip」に変更 → キャンセル"
    )
    notify_discord(message)


def wait_for_approval(original_text: str) -> tuple[str, str]:
    """
    承認を待つ。戻り値: (最終テキスト, ステータス)
    ステータス: "approved"(変更なし/テキスト編集) or "skip"(キャンセル)
    """
    deadline = datetime.now() + timedelta(minutes=APPROVAL_TIMEOUT_MIN)
    check_count = 0

    print(f"承認待ち開始（{APPROVAL_TIMEOUT_MIN}分後に自動投稿）...")

    while datetime.now() < deadline:
        time.sleep(APPROVAL_CHECK_INTERVAL)
        check_count += 1

        # 2回に1回 git pull（約1分間隔）
        if check_count % 2 == 0:
            git_pull()

        # pendingファイルを再読み込み
        pending = load_pending_tweet()
        if pending is None:
            print("WARNING: pending-tweets.json が見つかりません。自動投稿します")
            return original_text, "approved"

        status = pending.get("status", "pending")

        if status == "skip":
            print("ユーザーがキャンセルしました")
            return pending.get("text", original_text), "skip"

        if status == "approved":
            final_text = pending.get("text", original_text)
            if final_text != original_text:
                print(f"ユーザーが承認（テキスト編集あり）: {final_text}")
            else:
                print("ユーザーが承認しました")
            return final_text, "approved"

        # テキストが編集されていないかチェック
        current_text = pending.get("text", original_text)
        if current_text != original_text:
            remaining = int((deadline - datetime.now()).total_seconds() / 60)
            print(f"テキストが編集されました（残り{remaining}分で自動投稿）: {current_text}")
            original_text = current_text  # 以降はこのテキストが基準

    # タイムアウト → 自動承認
    pending = load_pending_tweet()
    if pending:
        final_text = pending.get("text", original_text)
        status = pending.get("status", "pending")
        if status == "skip":
            print("タイムアウト直前にキャンセルされました")
            return final_text, "skip"
        return final_text, "approved"

    return original_text, "approved"


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
    parser = argparse.ArgumentParser(description="X自動投稿（Claude API連携 + 画像自動添付 + 承認フロー）")
    parser.add_argument("--slot", required=True, choices=["morning", "noon", "evening"],
                        help="投稿時間帯: morning/noon/evening")
    parser.add_argument("--dry-run", action="store_true", help="生成のみ、投稿しない")
    parser.add_argument("--no-image", action="store_true", help="画像なしで投稿")
    parser.add_argument("--no-delay", action="store_true", help="ランダム遅延をスキップ")
    parser.add_argument("--no-approval", action="store_true", help="承認フローをスキップして即投稿")
    args = parser.parse_args()

    # ランダム遅延: 0〜60分（Task Schedulerが基準時刻の30分前に起動するため、
    # 結果的に基準時刻の前後30分にバラける。自動投稿感を消す）
    if not args.dry_run and not args.no_delay:
        delay_seconds = random.randint(0, 60 * 60)
        delay_min = delay_seconds // 60
        delay_sec = delay_seconds % 60
        print(f"[{datetime.now().isoformat()}] ランダム遅延: {delay_min}分{delay_sec}秒後に投稿開始")
        time.sleep(delay_seconds)

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

    # ファクトチェック（最大3回再生成）
    for attempt in range(3):
        passed, reason = fact_check_post(api_key, text)
        if passed:
            print(f"ファクトチェック: OK (attempt {attempt + 1})")
            break
        print(f"ファクトチェック: NG (attempt {attempt + 1}) - {reason}")
        if attempt < 2:
            print("再生成します...")
            text = generate_post(api_key, args.slot)
            print(f"再生成された投稿 ({len(text)}文字): {text}")
        else:
            print("ERROR: 3回ファクトチェックに失敗。投稿をスキップします")
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

    # === 承認フロー ===
    if not args.no_approval:
        # 1. pending-tweets.json に保存
        save_pending_tweet(text, args.slot, image_key, image_path)

        # 2. Discordにプレビュー送信
        notify_pending_tweet(text, args.slot, image_key)

        # 3. 承認を待つ（30分間、git pullしながらファイル変更を監視）
        final_text, status = wait_for_approval(text)

        # 4. キャンセルされた場合
        if status == "skip":
            clear_pending_tweet()
            notify_discord(f"⏭️ X投稿キャンセル ({args.slot})\n\nユーザーによりスキップされました")
            print("投稿がキャンセルされました")
            return

        # テキストが編集されていた場合、ファクトチェック再実行
        if final_text != text:
            print("テキストが編集されたため、ファクトチェックを再実行...")
            passed, reason = fact_check_post(api_key, final_text)
            if not passed:
                clear_pending_tweet()
                notify_discord(f"❌ X投稿中止 ({args.slot})\n\n編集後のテキストがファクトチェックNG: {reason}\n\n{final_text}")
                print(f"ERROR: 編集後テキストのファクトチェックNG - {reason}")
                sys.exit(1)
            text = final_text
            # 編集後テキストで画像を再選定
            if not args.no_image:
                image_path = find_best_image(text, args.slot)
                if image_path:
                    image_key = str(image_path.relative_to(PHOTOS_DIR)).replace("\\", "/")
                else:
                    image_key = None
        else:
            text = final_text

        clear_pending_tweet()

    # === Xに投稿 ===
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
