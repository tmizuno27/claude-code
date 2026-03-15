"""
article_generator.py — otona-match.com 記事自動生成
====================================================
Claude API でSEO最適化記事を生成し、Markdown保存 → WP投稿まで一括実行。

動作:
1. keyword-queue.json から本日 scheduled_date の pending 記事を取得
2. Claude API で 3000-5000字の記事を生成
3. outputs/articles/{slug}.md に保存
4. article-inline.css の <style> タグを先頭に付けて WP にドラフト投稿
5. article-management.csv を更新
6. keyword-queue.json のステータスを processed に更新
"""

import csv
import json
import logging
import os
import re
import sys
from datetime import date, datetime
from pathlib import Path

import anthropic
import requests

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
logger = logging.getLogger(__name__)

# パス
BASE_DIR = Path(__file__).resolve().parent.parent.parent
CONFIG_DIR = BASE_DIR / "config"
INPUTS_DIR = BASE_DIR / "inputs" / "keywords"
OUTPUTS_DIR = BASE_DIR / "outputs" / "articles"
CSS_FILE = BASE_DIR / "theme" / "css" / "article-inline.css"
CSV_FILE = BASE_DIR / "outputs" / "article-management.csv"
QUEUE_FILE = INPUTS_DIR / "keyword-queue.json"

# Healthchecks ping URL (追加時に設定)
HC_PING_URL = os.environ.get("HC_OTONA_ARTICLE", "")


def load_secrets():
    with open(CONFIG_DIR / "secrets.json", encoding="utf-8") as f:
        return json.load(f)


def load_settings():
    with open(CONFIG_DIR / "settings.json", encoding="utf-8") as f:
        return json.load(f)


def load_affiliate_links():
    with open(CONFIG_DIR / "affiliate-links.json", encoding="utf-8") as f:
        return json.load(f)


def load_queue():
    with open(QUEUE_FILE, encoding="utf-8") as f:
        return json.load(f)


def save_queue(data):
    with open(QUEUE_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def get_todays_article(queue_data):
    """本日のスケジュールに該当する pending 記事を返す"""
    today = date.today().isoformat()
    for item in queue_data["queue"]:
        if item["status"] == "pending" and item["scheduled_date"] <= today:
            return item
    return None


def generate_article(item, secrets, affiliate_links):
    """Claude API で記事を生成"""
    client = anthropic.Anthropic(api_key=secrets["claude_api"]["api_key"])

    # アフィリエイトリンク情報を整理
    aff_info = []
    for cat in affiliate_links.get("categories", {}).values():
        for link in cat.get("links", []):
            aff_info.append(f"- {link['name']}: {link['url']} ({link['commission']})")
    aff_text = "\n".join(aff_info) if aff_info else "アフィリエイトリンクは未設定"

    # 内部リンク情報
    internal = ", ".join(item.get("internal_links", []))

    prompt = f"""あなたは「大人のマッチングナビ」(otona-match.com)の記事ライターです。
30代・40代向けのマッチングアプリ比較メディアとして、以下の記事を生成してください。

## 記事情報
- タイトル: {item['title']}
- slug: {item['slug']}
- カテゴリ: {item['category']}
- 記事タイプ: {item['type']}
- メインキーワード: {item['main_keyword']}
- 内部リンク先: {internal}

## ライティングルール
1. 文字数: 3000〜5000字
2. HTML形式で出力（WordPressに直接投稿する）
3. H2, H3, H4の見出し階層を正しく使う
4. 比較表・ランキングを積極的に使用
5. 具体的な料金・会員数・年齢層データを含める（最新の数字を使用）
6. 重要部分に<strong>タグと<span class="marker-yellow">（結論・数字）、<span class="marker-pink">（注意点）、<span class="marker-blue">（メリット）を5-10箇所使用
7. 内部リンクを3本以上含める（形式: <a href="/slug/">テキスト</a>）
8. 記事冒頭に免責文を配置: ※この記事にはアフィリエイトリンクが含まれています...
9. 最後に「関連記事」セクションを追加

## 禁止事項
- 「いかがでしたでしょうか」「〜と言えるでしょう」等のAI的表現
- 特定アプリを過度に推す（公平な比較を維持）
- 性的・過激な表現
- 根拠のない断定（「絶対に出会える」等）

## アフィリエイトリンク（記事タイプが「キラー」「収益」の場合のみ使用）
{aff_text}

## 出力形式
HTMLのみを出力してください。<style>タグ、<html>、<body>タグは不要です。
記事本文のHTMLのみ（H2から始まる）を出力してください。
冒頭に導入文（p タグ）を配置し、その後見出し構造で本文を展開してください。
"""

    logger.info(f"Generating article: {item['slug']}...")
    response = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=8192,
        messages=[{"role": "user", "content": prompt}],
    )
    return response.content[0].text


def publish_to_wordpress(item, html_content, secrets, settings):
    """WordPressにドラフト投稿"""
    # article-inline.css を読み込んで先頭に付与
    if CSS_FILE.exists():
        with open(CSS_FILE, "r", encoding="utf-8") as f:
            css = f.read().strip()
        full_content = f"<style>{css}</style>\n{html_content}"
    else:
        full_content = html_content

    # カテゴリID取得
    categories = settings.get("wordpress", {}).get("categories", {})
    cat_info = categories.get(item["category"], {})
    cat_id = cat_info.get("id", 1)

    wp_url = settings["wordpress"]["rest_api_url"]
    auth = (secrets["wordpress"]["username"], secrets["wordpress"]["app_password"])

    r = requests.post(
        f"{wp_url}/posts",
        auth=auth,
        json={
            "title": item["title"],
            "slug": item["slug"],
            "content": full_content,
            "status": "draft",
            "categories": [cat_id],
        },
    )

    if r.status_code == 201:
        post = r.json()
        logger.info(f"Published draft: ID={post['id']} URL={post['link']}")
        return post
    else:
        logger.error(f"WP publish failed: {r.status_code} {r.text[:300]}")
        return None


def update_csv(item, wp_post):
    """article-management.csv に行を追加"""
    CSV_FILE.parent.mkdir(parents=True, exist_ok=True)

    rows = []
    if CSV_FILE.exists():
        with open(CSV_FILE, "r", encoding="utf-8") as f:
            reader = csv.reader(f)
            rows = list(reader)

    wp_id = wp_post["id"] if wp_post else ""
    wp_url = wp_post["link"] if wp_post else ""

    new_row = [
        str(wp_id),
        item["slug"],
        item["title"],
        "draft",
        date.today().isoformat(),
        item["category"],
        item["type"],
        "0",  # word_count (later update)
        "0",
        str(len(item.get("internal_links", []))),
        wp_url,
        f"auto-generated {datetime.now().strftime('%Y-%m-%d %H:%M')}",
    ]

    rows.append(new_row)

    with open(CSV_FILE, "w", encoding="utf-8", newline="") as f:
        writer = csv.writer(f)
        writer.writerows(rows)

    logger.info(f"CSV updated: {item['slug']}")


def ping_healthchecks(status="success"):
    if not HC_PING_URL:
        return
    try:
        url = HC_PING_URL if status == "success" else f"{HC_PING_URL}/fail"
        requests.get(url, timeout=10)
    except Exception:
        pass


def main():
    try:
        # 開始ping
        if HC_PING_URL:
            requests.get(f"{HC_PING_URL}/start", timeout=10)

        secrets = load_secrets()
        settings = load_settings()
        affiliate_links = load_affiliate_links()
        queue_data = load_queue()

        item = get_todays_article(queue_data)
        if not item:
            logger.info("No article scheduled for today. Exiting.")
            ping_healthchecks("success")
            return

        logger.info(f"Today's article: {item['slug']} ({item['title']})")

        # 1. 記事生成
        html = generate_article(item, secrets, affiliate_links)

        # 2. Markdown保存
        OUTPUTS_DIR.mkdir(parents=True, exist_ok=True)
        out_file = OUTPUTS_DIR / f"{item['slug']}.html"
        with open(out_file, "w", encoding="utf-8") as f:
            f.write(html)
        logger.info(f"Saved: {out_file}")

        # 3. WP投稿
        wp_post = publish_to_wordpress(item, html, secrets, settings)

        # 4. CSV更新
        update_csv(item, wp_post)

        # 5. キューステータス更新
        item["status"] = "processed"
        item["processed_date"] = date.today().isoformat()
        if wp_post:
            item["wp_id"] = wp_post["id"]
        save_queue(queue_data)

        logger.info(f"Done! Article '{item['slug']}' generated and published as draft.")
        ping_healthchecks("success")

    except Exception as e:
        logger.error(f"Error: {e}", exc_info=True)
        ping_healthchecks("fail")
        sys.exit(1)


if __name__ == "__main__":
    main()
