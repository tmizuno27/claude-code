#!/usr/bin/env python3
"""
WordPress自動投稿スクリプト

Markdown記事をWordPressに投稿する。
デフォルトはドラフト投稿。--status publish で即時公開。

使い方:
  python wp_publisher.py                          # 全未投稿をドラフト投稿
  python wp_publisher.py --status publish          # 全未投稿を即時公開
  python wp_publisher.py --status publish --limit 1  # 1記事だけ即時公開
  python wp_publisher.py --dry-run                 # 投稿せずにプレビュー
"""

import argparse
import json
import logging
import re
import sys
import urllib.request
from base64 import b64encode
from datetime import datetime
from pathlib import Path

import markdown
import requests
import subprocess

try:
    import anthropic
except ImportError:
    anthropic = None

# ログ設定
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# プロジェクトルート
PROJECT_ROOT = Path(__file__).parent.parent.parent
CONFIG_PATH = PROJECT_ROOT / "config" / "settings.json"
SECRETS_PATH = PROJECT_ROOT / "config" / "secrets.json"
ARTICLES_DIR = PROJECT_ROOT / "outputs" / "articles"
WP_LOG_PATH = PROJECT_ROOT / "published" / "wordpress-log.json"
MEDIA_MAPPING_PATH = PROJECT_ROOT / "config" / "media-mapping.json"


def load_config():
    """設定ファイルを読み込み、secrets.json の認証情報をマージする"""
    with open(CONFIG_PATH, "r", encoding="utf-8") as f:
        config = json.load(f)
    if SECRETS_PATH.exists():
        with open(SECRETS_PATH, "r", encoding="utf-8") as f:
            secrets = json.load(f)
        for section, values in secrets.items():
            if isinstance(values, dict) and section in config:
                config[section].update(values)
    return config


def load_wp_log():
    """WordPress投稿履歴を読み込む"""
    if WP_LOG_PATH.exists():
        with open(WP_LOG_PATH, "r", encoding="utf-8") as f:
            return json.load(f)
    return {"posts": []}


def save_wp_log(log_data):
    """WordPress投稿履歴を保存する"""
    WP_LOG_PATH.parent.mkdir(parents=True, exist_ok=True)
    with open(WP_LOG_PATH, "w", encoding="utf-8") as f:
        json.dump(log_data, f, ensure_ascii=False, indent=2)


def parse_front_matter(content):
    """Markdownファイルからフロントマターとボディを分離する"""
    front_matter = {}
    body = content

    # --- で囲まれたフロントマターを解析
    fm_match = re.match(r'^---\s*\n(.*?)\n---\s*\n(.*)', content, re.DOTALL)
    if fm_match:
        fm_text = fm_match.group(1)
        body = fm_match.group(2)

        for line in fm_text.strip().split('\n'):
            if ':' in line:
                key, value = line.split(':', 1)
                front_matter[key.strip()] = value.strip().strip('"').strip("'")

    return front_matter, body


def find_unpublished_articles():
    """未投稿のMarkdown記事を検索する"""
    unpublished = []

    if not ARTICLES_DIR.exists():
        logger.warning(f"記事ディレクトリが存在しません: {ARTICLES_DIR}")
        return unpublished

    # 日付フォルダとルート直下の両方を検索
    md_files = list(ARTICLES_DIR.rglob("*.md"))

    # 既に投稿済みのファイルを除外
    wp_log = load_wp_log()
    published_files = {p.get("source_file") for p in wp_log.get("posts", [])}

    for md_file in md_files:
        relative_path = str(md_file.relative_to(PROJECT_ROOT))
        if relative_path in published_files:
            continue

        content = md_file.read_text(encoding="utf-8")
        front_matter, body = parse_front_matter(content)

        # status が "draft" または フロントマターなしの記事を対象
        status = front_matter.get("status", "draft")
        if status in ("draft", ""):
            unpublished.append({
                "path": md_file,
                "relative_path": relative_path,
                "front_matter": front_matter,
                "body": body
            })

    return unpublished


def strip_rank_math_section(md_text):
    """Rank Math 設定用セクションを本文から除去する（メタ情報であり本文に不要）"""
    # "## Rank Math 設定用" 以降を削除（直前の --- 区切りも含む）
    pattern = r'\n---\s*\n\s*<span id="rank-math-設定用"></span>\s*\n## Rank Math 設定用.*'
    cleaned = re.sub(pattern, '', md_text, flags=re.DOTALL)
    if cleaned == md_text:
        # アンカーなしパターン
        cleaned = re.sub(r'\n---\s*\n\s*## Rank Math 設定用.*', '', cleaned, flags=re.DOTALL)
    if cleaned == md_text:
        # 区切りなしパターン
        cleaned = re.sub(r'\n## Rank Math 設定用.*', '', cleaned, flags=re.DOTALL)
    return cleaned


def strip_h1_from_html(html):
    """本文内のH1タグを除去する（テンプレート側のタイトルと重複するため）"""
    return re.sub(r'<h1[^>]*>.*?</h1>\s*', '', html, flags=re.DOTALL)


def markdown_to_html(md_text):
    """MarkdownをHTMLに変換する"""
    md_text = strip_rank_math_section(md_text)
    extensions = [
        'markdown.extensions.tables',
        'markdown.extensions.fenced_code',
        'markdown.extensions.toc',
        'markdown.extensions.nl2br'
    ]
    html = markdown.markdown(md_text, extensions=extensions)
    return strip_h1_from_html(html)


def find_featured_media(title, keyword):
    """media-mapping.json からタイトル/キーワードに一致する画像のメディアIDを検索"""
    if not MEDIA_MAPPING_PATH.exists():
        return None
    try:
        with open(MEDIA_MAPPING_PATH, "r", encoding="utf-8") as f:
            mapping = json.load(f)
        for media_id, info in mapping.get("media", {}).items():
            if info.get("title") == title or info.get("keyword") == keyword:
                logger.info(f"アイキャッチ画像発見: media_id={media_id}")
                return int(media_id)
    except Exception as e:
        logger.warning(f"media-mapping.json の読み込みに失敗: {e}")
    return None


def update_post_featured_image(mapping_path, post_id, media_id, title):
    """media-mapping.json の post_featured_images を更新"""
    try:
        with open(mapping_path, "r", encoding="utf-8") as f:
            mapping = json.load(f)
        if "post_featured_images" not in mapping:
            mapping["post_featured_images"] = {}
        mapping["post_featured_images"][str(post_id)] = {
            "media_id": media_id,
            "post_title": title,
        }
        with open(mapping_path, "w", encoding="utf-8") as f:
            json.dump(mapping, f, ensure_ascii=False, indent=2)
    except Exception as e:
        logger.warning(f"post_featured_images の更新に失敗: {e}")


ARTICLE_FACT_CHECK_PROMPT = """あなたはファクトチェッカーです。以下のブログ記事に事実誤認がないか検証してください。

## 検証基準（パラグアイ関連の正しい情報）
- 生活費が日本の1/3〜1/2（ランチ200-300円、牛肉1kg 700-900円、鶏肉1kg 300円）
- 家賃：一軒家3LDKで月3-5万円
- 所得税が最大10%、法人税10%
- 地震・台風・津波なし。一年中温暖（冬の平均気温17-19℃）
- 花粉ゼロ
- インターナショナルスクール学費月約3万円（日本なら15-20万円）
- アサード：牛肉2kgで約1,500-1,800円
- 永住権：まず2年の一時滞在ビザ→その後永住権申請。費用は書類+銀行預金$5,000程度
- 外国人でも土地・不動産を購入可能
- 日系社会90年の歴史
- 時差12時間（日本との）
- 家族4人（夫婦+娘2人、8歳・6歳）
- 著者: 南米おやじ（パラグアイ在住）

## 判定ルール
1. 上記基準と矛盾する数字・事実があれば「NG」
2. 基準にない具体的な数字・統計・法律・手続き・料金が記載されており、正確性が確認できない場合も「NG」
3. 一般的に正しい情報（例: クラウドソーシングの説明、ツールの基本的な説明）は「OK」
4. 「【要確認】」マーカーが残っている場合は「NG」（未検証の情報が残っている）

## 出力形式（厳守）
1行目に「OK」または「NG」のみ。
NGの場合、2行目以降に問題箇所と理由を箇条書きで記載。"""


def fact_check_article(config, body_text):
    """記事本文をファクトチェックする。(passed, reason) を返す"""
    if anthropic is None:
        logger.warning("anthropicライブラリ未インストール。ファクトチェックをスキップします")
        return True, ""

    api_key = config.get("claude_api", {}).get("api_key", "")
    if not api_key or "YOUR" in api_key:
        logger.warning("Claude API キー未設定。ファクトチェックをスキップします")
        return True, ""

    # 記事が長い場合は先頭5000文字に制限（コスト抑制）
    check_text = body_text[:5000] if len(body_text) > 5000 else body_text

    try:
        client = anthropic.Anthropic(api_key=api_key)
        response = client.messages.create(
            model="claude-sonnet-4-6",
            max_tokens=512,
            system=ARTICLE_FACT_CHECK_PROMPT,
            messages=[{"role": "user", "content": f"記事本文:\n{check_text}"}],
        )
        result = response.content[0].text.strip()
        lines = result.split("\n", 1)
        verdict = lines[0].strip().upper()
        reason = lines[1].strip() if len(lines) > 1 else ""
        return verdict == "OK", reason
    except Exception as e:
        logger.error(f"ファクトチェックAPI呼び出し失敗: {e}")
        # API失敗時は安全側に倒してNGとする
        return False, f"ファクトチェックAPI呼び出し失敗: {e}"


def publish_to_wordpress(config, article, status="draft"):
    """記事をWordPressに投稿する"""
    wp_config = config["wordpress"]
    url = f"{wp_config['rest_api_url']}/posts"

    # Basic認証ヘッダー
    credentials = f"{wp_config['username']}:{wp_config['app_password']}"
    token = b64encode(credentials.encode()).decode()
    headers = {
        "Authorization": f"Basic {token}",
        "Content-Type": "application/json"
    }

    # 記事データ
    title = article["front_matter"].get("title", "無題の記事")
    keyword = article["front_matter"].get("keyword", "")
    html_content = markdown_to_html(article["body"])

    post_data = {
        "title": title,
        "content": html_content,
        "status": status,
    }

    # アイキャッチ画像の自動設定
    media_id = find_featured_media(title, keyword)
    if media_id:
        post_data["featured_media"] = media_id
        logger.info(f"アイキャッチ画像を設定: media_id={media_id}")

    logger.info(f"投稿中 (status={status}): {title}")

    response = requests.post(url, headers=headers, json=post_data, timeout=30)

    if response.status_code in (200, 201):
        post = response.json()
        result = {
            "post_id": post["id"],
            "title": title,
            "keyword": keyword,
            "url": post["link"],
            "edit_url": f"{wp_config['url']}/wp-admin/post.php?post={post['id']}&action=edit",
            "status": status,
            "source_file": article["relative_path"],
            "published_at": datetime.now().isoformat()
        }
        logger.info(f"投稿成功! ID: {post['id']} (status: {status})")
        logger.info(f"  URL: {result['url']}")

        # post_featured_images を更新
        if media_id:
            update_post_featured_image(MEDIA_MAPPING_PATH, post["id"], media_id, title)

        return result
    else:
        logger.error(f"投稿失敗: {response.status_code} - {response.text}")
        return None


DASHBOARD_URL = "https://htmlpreview.github.io/?https://gist.githubusercontent.com/tmizuno27/16a8680cadf8aed0c207777f7468963b/raw/daily-business-dashboard.html"


def notify_discord(message):
    """Discord Webhookで通知を送信（ダッシュボードリンク付き）"""
    try:
        settings_file = CONFIG_PATH
        with open(settings_file, "r", encoding="utf-8") as f:
            settings = json.load(f)
        webhook_url = settings.get("discord", {}).get("webhook_url")
        if not webhook_url:
            return
        message_with_link = f"{message}\n\n📊 [ダッシュボード]({DASHBOARD_URL})"
        payload = json.dumps({"content": message_with_link}).encode("utf-8")
        req = urllib.request.Request(
            webhook_url,
            data=payload,
            headers={"Content-Type": "application/json", "User-Agent": "BlogPublisher/1.0"},
        )
        urllib.request.urlopen(req)
        logger.info("Discord通知を送信しました")
    except Exception as e:
        logger.warning(f"Discord通知の送信に失敗: {e}")


TWEET_GENERATION_PROMPT = """あなたはX（Twitter）投稿のコピーライターです。
ブログ記事のタイトルと本文の冒頭から、クリックしたくなるX投稿文を1つ生成してください。

## ルール（厳守）
1. 「ブログ更新しました」「記事書きました」等の告知型は絶対禁止
2. 記事の一番刺さるポイント（数字・意外性・共感）を1〜2文で書く
3. 最後に「👇」や「詳しくはこちら」等でURLへ誘導（URLは{url}と書く）
4. ハッシュタグは2個（#パラグアイ移住 #海外生活 を固定）
5. 全体で140文字以内（URL・ハッシュタグ含まず）
6. 一人称は「私」、カジュアルだが信頼感のあるトーン
7. 絵文字は0〜1個

## 出力形式
投稿文のみを出力。説明や前置きは不要。"""


def generate_tweet_text(config, post):
    """記事内容からClaude APIでX投稿文を生成する。失敗時はフォールバック"""
    url = post["url"]
    title = post["title"]

    # フォールバック用
    fallback = f"{title}\n{url}\n\n#パラグアイ移住 #海外生活"

    if anthropic is None:
        return fallback

    api_key = config.get("claude_api", {}).get("api_key", "")
    if not api_key or "YOUR" in api_key:
        return fallback

    # 投稿済み記事の本文冒頭を取得（published_postsのsource_fileから）
    source_file = post.get("source_file", "")
    body_preview = ""
    if source_file:
        source_path = PROJECT_ROOT / source_file
        if source_path.exists():
            content = source_path.read_text(encoding="utf-8")
            _, body = parse_front_matter(content)
            body_preview = body[:1500]

    try:
        client = anthropic.Anthropic(api_key=api_key)
        prompt = TWEET_GENERATION_PROMPT.replace("{url}", url)
        user_msg = f"タイトル: {title}\n\n本文冒頭:\n{body_preview}" if body_preview else f"タイトル: {title}"
        response = client.messages.create(
            model="claude-sonnet-4-6",
            max_tokens=256,
            system=prompt,
            messages=[{"role": "user", "content": user_msg}],
        )
        tweet = response.content[0].text.strip().strip('"')
        # {url}プレースホルダーを実際のURLに置換
        tweet = tweet.replace("{url}", url)
        # URLが含まれていなければ追加
        if url not in tweet:
            tweet = f"{tweet}\n{url}"
        # ハッシュタグが含まれていなければ追加
        if "#パラグアイ移住" not in tweet:
            tweet = f"{tweet}\n\n#パラグアイ移住 #海外生活"
        logger.info(f"X投稿文を生成しました: {tweet[:50]}...")
        return tweet
    except Exception as e:
        logger.warning(f"X投稿文の生成に失敗、フォールバック使用: {e}")
        return fallback


def main():
    """メイン処理"""
    parser = argparse.ArgumentParser(description="WordPress自動投稿スクリプト")
    parser.add_argument("--status", default="draft", choices=["draft", "publish"],
                        help="投稿ステータス: draft(下書き) / publish(即時公開)")
    parser.add_argument("--limit", type=int, default=0,
                        help="投稿する記事数の上限 (0=全件)")
    parser.add_argument("--dry-run", action="store_true",
                        help="投稿せずにプレビューのみ")
    args = parser.parse_args()

    logger.info("=== WordPress自動投稿スクリプト開始 ===")
    logger.info(f"  ステータス: {args.status} / 上限: {'全件' if args.limit == 0 else f'{args.limit}件'}")

    # 設定読み込み
    try:
        config = load_config()
    except FileNotFoundError:
        logger.error(f"設定ファイルが見つかりません: {CONFIG_PATH}")
        sys.exit(1)

    # WordPress設定チェック
    wp_url = config.get("wordpress", {}).get("url", "")
    if "YOUR" in wp_url or not wp_url:
        logger.error("WordPress URLが未設定です。config/settings.json を編集してください。")
        sys.exit(1)

    # 未投稿記事を検索
    articles = find_unpublished_articles()
    if not articles:
        logger.info("未投稿の記事はありません。")
        return

    # limit が指定されている場合は制限
    if args.limit > 0:
        articles = articles[:args.limit]

    logger.info(f"投稿対象の記事: {len(articles)}件")

    if args.dry_run:
        for article in articles:
            title = article["front_matter"].get("title", "無題")
            logger.info(f"  [DRY RUN] {title} → {args.status}")
        return

    # 投稿履歴の読み込み
    wp_log = load_wp_log()

    # 各記事を投稿
    success_count = 0
    skip_count = 0
    published_posts = []
    for article in articles:
        # publish時はファクトチェック必須
        if args.status == "publish":
            title = article["front_matter"].get("title", "無題")
            logger.info(f"ファクトチェック中: {title}")
            passed, reason = fact_check_article(config, article["body"])
            if not passed:
                logger.warning(f"ファクトチェックNG — スキップ: {title}")
                logger.warning(f"  理由: {reason}")
                notify_discord(
                    f"⚠️ ファクトチェックNG — 公開スキップ\n\n"
                    f"**{title}**\n理由: {reason}"
                )
                skip_count += 1
                continue
            logger.info(f"ファクトチェックOK: {title}")

        try:
            result = publish_to_wordpress(config, article, status=args.status)
            if result:
                wp_log["posts"].append(result)
                published_posts.append(result)
                success_count += 1
        except requests.RequestException as e:
            logger.error(f"ネットワークエラー: {e}")
        except Exception as e:
            logger.error(f"予期しないエラー: {e}")

    # 投稿成功した記事にアフィリエイトリンクを自動挿入
    if success_count > 0:
        affiliate_script = Path(__file__).parent / "insert_affiliate_all.py"
        if affiliate_script.exists():
            try:
                import subprocess
                result_aff = subprocess.run(
                    [sys.executable, str(affiliate_script), "--apply"],
                    capture_output=True, text=True, timeout=120
                )
                if result_aff.returncode == 0:
                    logger.info("アフィリエイトリンク自動挿入完了")
                else:
                    logger.warning(f"アフィリエイトリンク挿入失敗: {result_aff.stderr[:200]}")
            except Exception as e:
                logger.warning(f"アフィリエイトリンク挿入エラー: {e}")

    # 履歴を保存
    save_wp_log(wp_log)

    # サマリー
    logger.info(f"\n=== 結果サマリー ===")
    logger.info(f"投稿成功: {success_count}/{len(articles)}件 (status: {args.status})")
    if skip_count > 0:
        logger.warning(f"ファクトチェックNGでスキップ: {skip_count}件")

    # Discord通知 + X自動投稿
    if success_count > 0 and args.status == "publish":
        for post in published_posts:
            notify_discord(
                f"📝 ブログ記事を公開しました\n\n"
                f"**{post['title']}**\n"
                f"{post['url']}"
            )
            # X (Twitter) に自動投稿（Claude APIでキャッチコピー生成）
            x_poster_path = Path(__file__).parent.parent / "social" / "x_poster.py"
            if x_poster_path.exists():
                tweet_text = generate_tweet_text(config, post)
                try:
                    result = subprocess.run(
                        [sys.executable, str(x_poster_path), "--text", tweet_text],
                        capture_output=True, text=True, timeout=30
                    )
                    if result.returncode == 0:
                        logger.info(f"X投稿成功: {post['title']}")
                        notify_discord(
                            f"🐦 X自動投稿しました\n\n"
                            f"**{post['title']}**\n"
                            f"{post['url']}"
                        )
                    else:
                        logger.warning(f"X投稿失敗: {result.stderr}")
                        notify_discord(
                            f"⚠️ X自動投稿に失敗しました\n\n"
                            f"**{post['title']}**\n"
                            f"エラー: {result.stderr[:200]}"
                        )
                except Exception as e:
                    logger.warning(f"X投稿エラー: {e}")
            else:
                logger.warning(f"x_poster.py が見つかりません: {x_poster_path}")
    elif success_count > 0:
        logger.info(f"\nWordPress管理画面でドラフトを確認し、「公開」ボタンを押してください。")
        for post in published_posts:
            logger.info(f"  → {post['title']}")
            logger.info(f"    編集: {post['edit_url']}")


def _trigger_dashboard_sync():
    """ダッシュボードのステータスを即時同期"""
    try:
        import subprocess as _sp
        sync_script = Path(__file__).parent.parent / "analytics" / "dashboard_status_sync.py"
        if sync_script.exists():
            _sp.Popen([sys.executable, str(sync_script)], start_new_session=True)
            logger.info("ダッシュボードステータス同期をトリガー")
    except Exception:
        pass


if __name__ == "__main__":
    main()
    _trigger_dashboard_sync()
