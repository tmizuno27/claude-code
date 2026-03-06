#!/usr/bin/env python3
"""
Notion ブログ管理ダッシュボード同期スクリプト

CSV + Markdown記事 → Notion Database へ同期
WordPress公開状態も自動反映

使い方:
  python notion_sync.py              # 全記事を同期
  python notion_sync.py --init       # Notionデータベースを新規作成
  python notion_sync.py --status     # WordPress公開状態のみ更新
"""

import argparse
import csv
import json
import logging
import re
import sys
from datetime import datetime
from pathlib import Path

try:
    from notion_client import Client
except ImportError:
    print("notion-client がインストールされていません。")
    print("実行: pip install notion-client")
    sys.exit(1)

try:
    import requests
except ImportError:
    requests = None

# ログ設定
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

# パス定義
PROJECT_ROOT = Path(__file__).parent.parent.parent
CONFIG_DIR = PROJECT_ROOT / "config"
SECRETS_PATH = CONFIG_DIR / "secrets.json"
CSV_PATH = PROJECT_ROOT / "outputs" / "article-management.csv"
ARTICLES_DIR = PROJECT_ROOT / "outputs" / "articles"
NOTION_CONFIG_PATH = CONFIG_DIR / "notion-config.json"

# ステータスの色マッピング
STATUS_COLORS = {
    "公開済": "green",
    "リライト済": "blue",
    "下書き": "yellow",
    "予約済": "purple",
    "執筆中": "orange",
    "計画中": "gray",
}

# 記事タイプの色マッピング
TYPE_COLORS = {
    "集客記事": "blue",
    "収益記事": "green",
    "キラー記事": "red",
    "実験記事": "purple",
}

# カテゴリの色マッピング
PILLAR_COLORS = {
    "パラグアイ生活": "orange",
    "海外の働き方": "blue",
}


def load_secrets():
    """secrets.json からNotion/WordPress認証情報を読み込む"""
    if not SECRETS_PATH.exists():
        logger.error(f"secrets.json が見つかりません: {SECRETS_PATH}")
        sys.exit(1)

    with open(SECRETS_PATH, "r", encoding="utf-8") as f:
        secrets = json.load(f)

    if "notion" not in secrets:
        logger.error("secrets.json に 'notion' セクションがありません。")
        logger.error('追加してください: "notion": {"api_key": "ntn_xxx", "parent_page_id": "xxx"}')
        sys.exit(1)

    return secrets


def load_notion_config():
    """notion-config.json からDB IDなどを読み込む"""
    if NOTION_CONFIG_PATH.exists():
        with open(NOTION_CONFIG_PATH, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}


def save_notion_config(config):
    """notion-config.json を保存"""
    with open(NOTION_CONFIG_PATH, "w", encoding="utf-8") as f:
        json.dump(config, f, ensure_ascii=False, indent=2)
    logger.info(f"Notion設定を保存: {NOTION_CONFIG_PATH}")


def get_notion_client(secrets):
    """Notionクライアントを初期化"""
    return Client(auth=secrets["notion"]["api_key"])


def create_database(notion, parent_page_id):
    """Notionデータベースを新規作成"""
    logger.info("Notionデータベースを作成中...")

    db = notion.databases.create(
        parent={"type": "page_id", "page_id": parent_page_id},
        title=[{"type": "text", "text": {"content": "南米おやじ 記事管理"}}],
        icon={"type": "emoji", "emoji": "📝"},
        properties={
            "タイトル": {"title": {}},
            "ステータス": {
                "select": {
                    "options": [
                        {"name": name, "color": color}
                        for name, color in STATUS_COLORS.items()
                    ]
                }
            },
            "公開日": {"date": {}},
            "公開順": {"number": {}},
            "柱": {
                "select": {
                    "options": [
                        {"name": name, "color": color}
                        for name, color in PILLAR_COLORS.items()
                    ]
                }
            },
            "記事タイプ": {
                "select": {
                    "options": [
                        {"name": name, "color": color}
                        for name, color in TYPE_COLORS.items()
                    ]
                }
            },
            "カテゴリ": {
                "select": {
                    "options": [
                        {"name": "パラグアイ生活", "color": "orange"},
                        {"name": "海外移住の働き方", "color": "blue"},
                    ]
                }
            },
            "メインKW": {"rich_text": {}},
            "文字数": {"number": {}},
            "アフィリ数": {"number": {}},
            "内部リンク数": {"number": {}},
            "ファイル名": {"rich_text": {}},
            "WordPress URL": {"url": {}},
            "備考": {"rich_text": {}},
        },
    )

    db_id = db["id"]
    logger.info(f"データベース作成完了: {db_id}")

    # 設定を保存
    config = load_notion_config()
    config["database_id"] = db_id
    config["created_at"] = datetime.now().isoformat()
    save_notion_config(config)

    return db_id


def load_csv():
    """CSVから記事データを読み込む"""
    if not CSV_PATH.exists():
        logger.error(f"CSVが見つかりません: {CSV_PATH}")
        return []

    articles = []
    with open(CSV_PATH, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            articles.append(row)

    logger.info(f"CSV読み込み: {len(articles)}記事")
    return articles


def find_article_md(filename):
    """記事のMarkdownファイルを探して内容を返す"""
    if not filename:
        return None

    # 日付ディレクトリを検索
    for md_path in ARTICLES_DIR.rglob(filename):
        if md_path.is_file():
            with open(md_path, "r", encoding="utf-8") as f:
                return f.read()
    return None


def md_to_notion_blocks(md_content, max_blocks=95):
    """MarkdownをNotionブロックに変換（簡易版）

    Notion APIは1回のリクエストで最大100ブロックまで。
    記事本文を見やすく表示するために主要な要素を変換する。
    """
    blocks = []
    lines = md_content.split("\n")
    i = 0

    while i < len(lines) and len(blocks) < max_blocks:
        line = lines[i]

        # 見出し
        if line.startswith("### "):
            blocks.append({
                "object": "block",
                "type": "heading_3",
                "heading_3": {
                    "rich_text": [{"type": "text", "text": {"content": line[4:].strip()}}]
                },
            })
        elif line.startswith("## "):
            blocks.append({
                "object": "block",
                "type": "heading_2",
                "heading_2": {
                    "rich_text": [{"type": "text", "text": {"content": line[3:].strip()}}]
                },
            })
        elif line.startswith("# "):
            blocks.append({
                "object": "block",
                "type": "heading_1",
                "heading_1": {
                    "rich_text": [{"type": "text", "text": {"content": line[2:].strip()}}]
                },
            })
        # 箇条書き
        elif line.strip().startswith("- ") or line.strip().startswith("* "):
            text = line.strip()[2:]
            blocks.append({
                "object": "block",
                "type": "bulleted_list_item",
                "bulleted_list_item": {
                    "rich_text": [{"type": "text", "text": {"content": text}}]
                },
            })
        # 番号付きリスト
        elif re.match(r"^\d+\.\s", line.strip()):
            text = re.sub(r"^\d+\.\s", "", line.strip())
            blocks.append({
                "object": "block",
                "type": "numbered_list_item",
                "numbered_list_item": {
                    "rich_text": [{"type": "text", "text": {"content": text}}]
                },
            })
        # 区切り線
        elif line.strip() in ("---", "***", "___"):
            blocks.append({
                "object": "block",
                "type": "divider",
                "divider": {},
            })
        # 通常の段落（空行はスキップ）
        elif line.strip():
            # Notion APIはrich_textの1要素あたり2000文字制限
            text = line.strip()
            if len(text) > 2000:
                text = text[:1997] + "..."
            blocks.append({
                "object": "block",
                "type": "paragraph",
                "paragraph": {
                    "rich_text": [{"type": "text", "text": {"content": text}}]
                },
            })

        i += 1

    if len(blocks) >= max_blocks:
        blocks.append({
            "object": "block",
            "type": "callout",
            "callout": {
                "icon": {"type": "emoji", "emoji": "📄"},
                "rich_text": [{"type": "text", "text": {
                    "content": f"（全文は {len(lines)} 行あります。続きはローカルMDファイルを参照）"
                }}],
            },
        })

    return blocks


def get_existing_pages(notion, database_id):
    """既存のNotionページを取得（ファイル名でマッピング）"""
    pages = {}
    has_more = True
    start_cursor = None

    while has_more:
        kwargs = {"database_id": database_id, "page_size": 100}
        if start_cursor:
            kwargs["start_cursor"] = start_cursor

        response = notion.databases.query(**kwargs)

        for page in response["results"]:
            props = page["properties"]
            filename_prop = props.get("ファイル名", {})
            rich_text = filename_prop.get("rich_text", [])
            if rich_text:
                fname = rich_text[0]["plain_text"]
                pages[fname] = page["id"]

        has_more = response.get("has_more", False)
        start_cursor = response.get("next_cursor")

    return pages


def safe_int(value):
    """安全にintに変換"""
    try:
        return int(value)
    except (ValueError, TypeError):
        return 0


def build_page_properties(article):
    """CSV行からNotionプロパティを構築"""
    props = {
        "タイトル": {
            "title": [{"type": "text", "text": {"content": article.get("記事タイトル", "無題")}}]
        },
        "メインKW": {
            "rich_text": [{"type": "text", "text": {"content": article.get("メインKW", "")}}]
        },
        "ファイル名": {
            "rich_text": [{"type": "text", "text": {"content": article.get("ファイル名", "")}}]
        },
        "備考": {
            "rich_text": [{"type": "text", "text": {"content": article.get("備考", "")}}]
        },
    }

    # ステータス
    status = article.get("ステータス", "").strip()
    if status and status in STATUS_COLORS:
        props["ステータス"] = {"select": {"name": status}}

    # 柱
    pillar = article.get("柱", "").strip()
    if pillar and pillar in PILLAR_COLORS:
        props["柱"] = {"select": {"name": pillar}}

    # 記事タイプ
    article_type = article.get("記事タイプ", "").strip()
    if article_type and article_type in TYPE_COLORS:
        props["記事タイプ"] = {"select": {"name": article_type}}

    # カテゴリ
    category = article.get("カテゴリ", "").strip()
    if category:
        props["カテゴリ"] = {"select": {"name": category}}

    # 公開順
    order = safe_int(article.get("公開順", "").replace("W", ""))
    if order:
        props["公開順"] = {"number": order}

    # 公開日
    pub_date = article.get("公開日", "").strip()
    if pub_date and pub_date != "":
        props["公開日"] = {"date": {"start": pub_date}}

    # 数値
    word_count = safe_int(article.get("文字数", ""))
    if word_count:
        props["文字数"] = {"number": word_count}

    affili = safe_int(article.get("アフィリ数", ""))
    props["アフィリ数"] = {"number": affili}

    internal_links = safe_int(article.get("内部リンク数", ""))
    props["内部リンク数"] = {"number": internal_links}

    return props


def sync_articles(notion, database_id):
    """CSVの記事データをNotionに同期"""
    articles = load_csv()
    if not articles:
        return

    existing = get_existing_pages(notion, database_id)
    logger.info(f"既存Notionページ: {len(existing)}件")

    created = 0
    updated = 0

    for article in articles:
        filename = article.get("ファイル名", "")
        title = article.get("記事タイトル", "無題")
        props = build_page_properties(article)

        # 記事本文を取得
        md_content = find_article_md(filename)

        if filename in existing:
            # 既存ページを更新
            page_id = existing[filename]
            try:
                notion.pages.update(page_id=page_id, properties=props)

                # 本文も更新（既存ブロックを削除して再追加）
                if md_content:
                    # 既存の子ブロックを取得して削除
                    children = notion.blocks.children.list(block_id=page_id)
                    for block in children["results"]:
                        notion.blocks.delete(block_id=block["id"])

                    # 新しいブロックを追加
                    blocks = md_to_notion_blocks(md_content)
                    if blocks:
                        # Notion APIは100ブロック/リクエスト制限
                        for chunk_start in range(0, len(blocks), 100):
                            chunk = blocks[chunk_start:chunk_start + 100]
                            notion.blocks.children.append(
                                block_id=page_id, children=chunk
                            )

                updated += 1
                logger.info(f"  更新: {title[:40]}...")
            except Exception as e:
                logger.error(f"  更新失敗: {title[:40]}... - {e}")
        else:
            # 新規ページを作成
            try:
                children = []
                if md_content:
                    children = md_to_notion_blocks(md_content)

                # 最初の100ブロックでページ作成
                first_chunk = children[:100]
                remaining = children[100:]

                new_page = notion.pages.create(
                    parent={"database_id": database_id},
                    properties=props,
                    children=first_chunk,
                )

                # 残りのブロックを追加
                if remaining:
                    for chunk_start in range(0, len(remaining), 100):
                        chunk = remaining[chunk_start:chunk_start + 100]
                        notion.blocks.children.append(
                            block_id=new_page["id"], children=chunk
                        )

                created += 1
                logger.info(f"  作成: {title[:40]}...")
            except Exception as e:
                logger.error(f"  作成失敗: {title[:40]}... - {e}")

    logger.info(f"同期完了: 新規 {created}件, 更新 {updated}件")


def sync_wordpress_status(notion, database_id, secrets):
    """WordPressの公開状態をNotionに反映"""
    if requests is None:
        logger.warning("requests がインストールされていません。WordPress同期をスキップ。")
        return

    wp = secrets.get("wordpress", {})
    if not wp.get("username") or not wp.get("app_password"):
        logger.warning("WordPress認証情報がありません。スキップ。")
        return

    site_url = "https://nambei-oyaji.com"
    api_url = f"{site_url}/wp-json/wp/v2/posts"

    logger.info("WordPress公開状態を取得中...")

    # 全記事を取得
    wp_posts = []
    page = 1
    while True:
        resp = requests.get(
            api_url,
            params={"per_page": 50, "page": page, "status": "publish,draft,future"},
            auth=(wp.get("username"), wp.get("app_password")),
            timeout=30,
        )
        if resp.status_code != 200:
            break
        posts = resp.json()
        if not posts:
            break
        wp_posts.extend(posts)
        page += 1

    logger.info(f"WordPress記事: {len(wp_posts)}件")

    # slug→URL/statusのマッピング
    wp_map = {}
    for post in wp_posts:
        wp_map[post["slug"]] = {
            "url": post["link"],
            "status": post["status"],
            "date": post.get("date", "")[:10],
        }

    # Notionページを更新
    existing = get_existing_pages(notion, database_id)
    updated = 0

    for filename, page_id in existing.items():
        # ファイル名からslugを推定（article-xxx.md → xxx）
        slug = filename.replace("article-", "").replace(".md", "")

        if slug in wp_map:
            wp_info = wp_map[slug]
            update_props = {}

            if wp_info["url"]:
                update_props["WordPress URL"] = {"url": wp_info["url"]}

            if wp_info["status"] == "publish":
                update_props["ステータス"] = {"select": {"name": "公開済"}}
                if wp_info["date"]:
                    update_props["公開日"] = {"date": {"start": wp_info["date"]}}
            elif wp_info["status"] == "future":
                update_props["ステータス"] = {"select": {"name": "予約済"}}

            if update_props:
                try:
                    notion.pages.update(page_id=page_id, properties=update_props)
                    updated += 1
                except Exception as e:
                    logger.error(f"WP状態更新失敗: {filename} - {e}")

    logger.info(f"WordPress状態更新: {updated}件")


def main():
    parser = argparse.ArgumentParser(description="Notion ブログ管理同期")
    parser.add_argument("--init", action="store_true", help="Notionデータベースを新規作成")
    parser.add_argument("--status", action="store_true", help="WordPress公開状態のみ更新")
    args = parser.parse_args()

    secrets = load_secrets()
    notion = get_notion_client(secrets)

    if args.init:
        # データベース新規作成
        parent_page_id = secrets["notion"].get("parent_page_id", "")
        if not parent_page_id:
            logger.error("secrets.json の notion.parent_page_id を設定してください。")
            sys.exit(1)

        db_id = create_database(notion, parent_page_id)
        logger.info(f"データベースID: {db_id}")
        logger.info("次回からは --init なしで実行してください。")
        return

    # DB ID取得
    config = load_notion_config()
    db_id = config.get("database_id", "")
    if not db_id:
        logger.error("データベースIDが未設定です。先に --init を実行してください。")
        sys.exit(1)

    if args.status:
        # WordPress状態のみ更新
        sync_wordpress_status(notion, db_id, secrets)
    else:
        # 全同期
        sync_articles(notion, db_id)
        sync_wordpress_status(notion, db_id, secrets)

    logger.info("全処理完了")


if __name__ == "__main__":
    main()
