#!/usr/bin/env python3
"""
WordPress記事 → はてなブログ用ダイジェスト変換スクリプト

本家WordPress記事を読み込み、切り口を変えたダイジェスト版を生成する。
重複コンテンツを回避しつつ、本家への誘導リンクを付与。

使い方:
  python hatena_converter.py                    # 未変換の全記事を変換
  python hatena_converter.py --limit 3          # 3記事だけ変換
  python hatena_converter.py --article 5        # 記事#5のみ変換
  python hatena_converter.py --dry-run          # 変換せずプレビュー
"""

import argparse
import csv
import json
import logging
import random
import re
import sys
import time
from datetime import datetime
from pathlib import Path

import requests

# Log settings
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Paths
PROJECT_ROOT = Path(__file__).parent.parent.parent
SECRETS_PATH = PROJECT_ROOT / "config" / "secrets.json"
ARTICLES_DIR = PROJECT_ROOT / "outputs" / "articles"
HATENA_OUTPUT_DIR = PROJECT_ROOT / "outputs" / "hatena"
CSV_PATH = PROJECT_ROOT / "outputs" / "article-management.csv"
HATENA_LOG_PATH = PROJECT_ROOT / "published" / "hatena-log.json"

# Conversion prompt template
CONVERSION_PROMPT = """あなたは「南米おやじ」というブロガーです。
以下のWordPress記事を、はてなブログ用の「体験メモ」に変換してください。

## 変換ルール（厳守）
1. 文字数は元記事の1/3以下（目安400-800字）
2. SEO構成（H2/H3の羅列）→ 日記・体験談調に完全に書き換える
3. 見出しは最大2つまで（元記事の見出し構成をそのまま使わない）
4. 「パラグアイに住んでいる私が実際に感じたこと」という一人称の語り口
5. 元記事の文章をそのままコピーしない（表現・語順を完全に変える）
6. カジュアルで親しみやすいトーン（「〜なんですよね」「〜だったりします」OK）
7. 具体的な数字は1-2個だけ残す（全部は載せない→詳細は本家で）
8. 末尾に本家記事への誘導を自然に入れる

## 禁止事項
- 元記事の文章のコピペ（一文でも不可）
- 「いかがでしたでしょうか」等のAI的表現
- 「まとめると〜」で始まる結論
- アフィリエイトリンクの記載
- 本名（水野達也）の記載。ペンネーム「南米おやじ」のみ使用
- 居住地を「ランバレ」と書くこと。「アスンシオン」と表記

## 出力フォーマット
Markdown形式で出力してください。タイトルは含めず本文のみ。

---

### 元記事タイトル
{title}

### 元記事本文
{content}

### 本家記事URL（末尾のリンクにはこのURLをそのまま使うこと）
{url}?utm_source=hatena&utm_medium=blog&utm_campaign=digest
"""


def load_secrets():
    """Load secrets from config."""
    with open(SECRETS_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


def load_article_csv():
    """Load article management CSV and return published articles."""
    articles = []
    with open(CSV_PATH, "r", encoding="utf-8-sig") as f:
        reader = csv.DictReader(f)
        for row in reader:
            if row.get("ステータス") == "公開済":
                articles.append(row)
    return articles


def load_hatena_log():
    """Load hatena publication log."""
    if HATENA_LOG_PATH.exists():
        with open(HATENA_LOG_PATH, "r", encoding="utf-8") as f:
            return json.load(f)
    return {"converted": [], "published": []}


def save_hatena_log(log_data):
    """Save hatena publication log."""
    HATENA_LOG_PATH.parent.mkdir(parents=True, exist_ok=True)
    with open(HATENA_LOG_PATH, "w", encoding="utf-8") as f:
        json.dump(log_data, f, ensure_ascii=False, indent=2)


def get_unconverted_articles(articles, hatena_log):
    """Filter and prioritize articles by revenue potential."""
    converted_ids = {str(entry["article_id"]) for entry in hatena_log.get("converted", [])}
    unconverted = [a for a in articles if a["#"] not in converted_ids]

    # Priority scoring: revenue-first
    def priority_score(article):
        score = 0
        article_type = article.get("記事タイプ", "")
        category = article.get("カテゴリ", "")
        affiliate_count = int(article.get("アフィリ数", "0") or "0")
        pv = int(article.get("累計PV", "0") or "0")

        # Revenue articles (affiliate) get highest priority
        if "収益" in article_type or "キラー" in article_type:
            score += 100
        # Articles with affiliates are revenue drivers
        score += affiliate_count * 20
        # High PV articles drive more traffic to main site
        score += min(pv, 50)  # Cap at 50 to avoid PV-only bias
        # Work/income articles convert better than lifestyle
        if "稼ぐ" in category or "副業" in category or "お金" in category:
            score += 30

        return score

    unconverted.sort(key=priority_score, reverse=True)
    return unconverted


def read_article_file(filename):
    """Read article markdown file. Searches in subdirectories too."""
    # Direct path
    filepath = ARTICLES_DIR / filename
    if filepath.exists():
        with open(filepath, "r", encoding="utf-8") as f:
            return f.read()

    # Search in date subdirectories
    for subdir in sorted(ARTICLES_DIR.iterdir(), reverse=True):
        if subdir.is_dir() and subdir.name != "archived":
            candidate = subdir / filename
            if candidate.exists():
                with open(candidate, "r", encoding="utf-8") as f:
                    return f.read()

    return None


def fetch_article_from_wp(permalink, secrets):
    """Fetch article content from WordPress REST API by slug."""
    wp_config = secrets.get("wordpress", {})
    username = wp_config.get("username", "")
    app_password = wp_config.get("app_password", "")

    url = f"https://nambei-oyaji.com/wp-json/wp/v2/posts?slug={permalink}"
    auth = (username, app_password)

    try:
        response = requests.get(url, auth=auth, timeout=30)
        if response.status_code == 200:
            posts = response.json()
            if posts:
                # Return rendered content (HTML), strip tags for conversion
                html_content = posts[0].get("content", {}).get("rendered", "")
                # Basic HTML to text conversion
                text = re.sub(r'<[^>]+>', '', html_content)
                text = text.replace('&amp;', '&').replace('&lt;', '<').replace('&gt;', '>')
                text = text.replace('&nbsp;', ' ').replace('&#8211;', '-')
                return text.strip()
    except Exception as e:
        logger.error(f"WordPress API error: {e}")

    return None


def convert_article(api_key, title, content, url):
    """Convert WordPress article to Hatena digest using Claude API (requests)."""
    prompt = CONVERSION_PROMPT.format(
        title=title,
        content=content[:8000],
        url=url
    )

    response = requests.post(
        "https://api.anthropic.com/v1/messages",
        headers={
            "x-api-key": api_key,
            "anthropic-version": "2023-06-01",
            "content-type": "application/json"
        },
        json={
            "model": "claude-sonnet-4-6",
            "max_tokens": 2000,
            "messages": [{"role": "user", "content": prompt}]
        },
        timeout=120
    )

    if response.status_code != 200:
        raise Exception(f"API error {response.status_code}: {response.text[:200]}")

    data = response.json()
    return data["content"][0]["text"]


def convert_article_with_retry(api_key, title, content, url, max_retries=3):
    """Wrap convert_article with exponential backoff retry."""
    backoff_seconds = [5, 10, 20]
    for attempt in range(max_retries):
        try:
            return convert_article(api_key, title, content, url)
        except Exception as e:
            if attempt < max_retries - 1:
                wait = backoff_seconds[attempt]
                logger.warning(f"  → 変換失敗 (attempt {attempt + 1}/{max_retries}): {e}")
                logger.info(f"  → {wait}秒後にリトライ...")
                time.sleep(wait)
            else:
                raise


def generate_hatena_title(original_title, article_id):
    """Generate a deterministic title for Hatena blog."""
    # Remove SEO elements like 【2026年版】, pipes, etc.
    title = re.sub(r'【.*?】', '', original_title)
    title = title.split('｜')[0].strip()
    title = title.split('|')[0].strip()
    # Add casual prefix (deterministic based on article_id)
    prefixes = [
        "パラグアイ暮らしメモ：",
        "南米生活の雑記：",
        "移住者の本音：",
        "アスンシオンから：",
    ]
    prefix = prefixes[int(article_id) % len(prefixes)]
    full_title = f"{prefix}{title}"
    # Truncate if over 25 characters
    if len(full_title) > 25:
        full_title = full_title[:25] + "…"
    return full_title


def ensure_utm_link(body, original_url):
    """Ensure the converted body contains the UTM-tagged URL."""
    utm_url = f"{original_url}?utm_source=hatena&utm_medium=blog&utm_campaign=digest"
    if utm_url not in body:
        if original_url in body:
            body = body.replace(original_url, utm_url)
        else:
            body += f"\n\n---\n\n詳しくは本家記事をどうぞ → [{original_url}]({utm_url})"
    return body


def main():
    parser = argparse.ArgumentParser(description="WordPress → はてなブログ変換")
    parser.add_argument("--limit", type=int, default=0, help="変換する記事数の上限")
    parser.add_argument("--article", type=int, default=0, help="特定記事番号のみ変換")
    parser.add_argument("--dry-run", action="store_true", help="変換せずにプレビュー")
    args = parser.parse_args()

    secrets = load_secrets()
    api_key = secrets.get("claude_api", {}).get("api_key")
    if not api_key:
        logger.error("Claude API key not found in secrets.json")
        sys.exit(1)

    # Load data
    articles = load_article_csv()
    hatena_log = load_hatena_log()

    # Filter articles
    if args.article:
        targets = [a for a in articles if a["#"] == str(args.article)]
    else:
        targets = get_unconverted_articles(articles, hatena_log)

    if args.limit > 0:
        targets = targets[:args.limit]

    if not targets:
        logger.info("変換対象の記事がありません")
        return

    logger.info(f"変換対象: {len(targets)}記事")

    # Create output directory
    HATENA_OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    for article in targets:
        article_id = article["#"]
        original_title = article["記事タイトル"]
        filename = article.get("ファイル名", "")
        permalink = article.get("パーマリンク", "")
        url = f"https://nambei-oyaji.com/{permalink}/"

        logger.info(f"[#{article_id}] {original_title}")

        if args.dry_run:
            logger.info(f"  → DRY RUN: スキップ")
            continue

        # Read original article (local file first, then WP API fallback)
        content = read_article_file(filename) if filename else None
        if not content:
            logger.info(f"  → ローカルファイル無し、WordPress APIから取得中...")
            content = fetch_article_from_wp(permalink, secrets)
        if not content:
            logger.warning(f"  → 記事本文を取得できません: {filename} / {permalink}")
            continue

        # Convert
        try:
            hatena_body = convert_article_with_retry(api_key, original_title, content, url)
            hatena_title = generate_hatena_title(original_title, article_id)
            hatena_body = ensure_utm_link(hatena_body, url)
        except Exception as e:
            logger.error(f"  → 変換エラー: {e}")
            continue

        # Save converted article
        output_filename = f"hatena-{int(article_id):03d}.md"
        output_path = HATENA_OUTPUT_DIR / output_filename
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(f"---\n")
            f.write(f"title: {hatena_title}\n")
            f.write(f"original_id: {article_id}\n")
            f.write(f"original_title: {original_title}\n")
            f.write(f"original_url: {url}\n")
            f.write(f"converted_at: {datetime.now().isoformat()}\n")
            f.write(f"---\n\n")
            f.write(hatena_body)

        # Update log
        hatena_log["converted"].append({
            "article_id": article_id,
            "original_title": original_title,
            "hatena_title": hatena_title,
            "hatena_file": output_filename,
            "converted_at": datetime.now().isoformat()
        })
        save_hatena_log(hatena_log)

        logger.info(f"  → 変換完了: {output_filename}")

    logger.info(f"全変換完了: {len(targets)}記事")


if __name__ == "__main__":
    main()
