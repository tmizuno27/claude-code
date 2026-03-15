"""
internal_linker.py
==================
WordPressの公開済み記事間に内部リンクを自動挿入するスクリプト。
SIM比較オンライン (sim-hikaku.online) 版。

処理フロー:
1. secrets.json からWordPress認証情報を読み込む
2. WP REST API で公開済み記事を全件取得
3. 各記事のID・タイトル・URL・キーワードを抽出
4. 記事ペアの関連性スコアを計算
5. 各記事について未リンクの上位3記事を特定
6. 関連記事へのリンクを本文末尾のセクションとして追加
7. WP REST API で記事を更新
8. 変更ログを outputs/reports/internal-links-YYYY-MM-DD.json に保存
"""

import io
import json
import re
import logging
import argparse
import sys
from pathlib import Path
from datetime import date
from collections import defaultdict
from itertools import combinations
from base64 import b64encode

# Windows UTF-8 出力修正
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding="utf-8", errors="replace")

try:
    import requests
except ImportError:
    requests = None

# ロギング設定
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
logger = logging.getLogger(__name__)

# プロジェクトルート
PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
CONFIG_PATH = PROJECT_ROOT / "config" / "settings.json"
SECRETS_PATH = PROJECT_ROOT / "config" / "secrets.json"
REPORTS_DIR = PROJECT_ROOT / "outputs" / "reports"


# ---------------------------------------------------------------------------
# 設定読み込み
# ---------------------------------------------------------------------------

def load_settings() -> dict:
    """secrets.json を読み込み、settings.json があればマージして返す。"""
    config = {}
    if CONFIG_PATH.exists():
        logger.info("設定ファイルを読み込んでいます: %s", CONFIG_PATH)
        with CONFIG_PATH.open(encoding="utf-8") as f:
            config = json.load(f)

    if SECRETS_PATH.exists():
        with SECRETS_PATH.open(encoding="utf-8") as f:
            secrets = json.load(f)
        # wordpress セクションをマージ
        if "wordpress" not in config:
            config["wordpress"] = {}
        wp_secrets = secrets.get("wordpress", {})
        config["wordpress"].update(wp_secrets)
        # rest_api_url がなければ secrets から構築
        if "rest_api_url" not in config.get("wordpress", {}):
            api_url = wp_secrets.get("api_url", "https://sim-hikaku.online/wp-json/wp/v2")
            config["wordpress"]["rest_api_url"] = api_url

    return config


# ---------------------------------------------------------------------------
# WordPress API ヘルパー
# ---------------------------------------------------------------------------

def build_auth_header(username: str, app_password: str) -> dict:
    """Basic 認証ヘッダーを生成する。"""
    token = b64encode(f"{username}:{app_password}".encode()).decode()
    return {"Authorization": f"Basic {token}"}


def fetch_all_posts(rest_api_url: str, headers: dict) -> list[dict]:
    """公開済み記事を全件取得する。"""
    if requests is None:
        raise ImportError("requests ライブラリが見つかりません。pip install requests を実行してください。")

    all_posts: list[dict] = []
    page = 1

    while True:
        params = {
            "per_page": 100,
            "status": "publish",
            "page": page,
            "_fields": "id,title,link,content,excerpt",
        }
        logger.info("記事を取得中 (page=%d)...", page)
        response = requests.get(
            f"{rest_api_url}/posts",
            params=params,
            headers=headers,
            timeout=30,
        )

        if response.status_code == 400:
            break
        response.raise_for_status()

        posts = response.json()
        if not posts:
            break

        all_posts.extend(posts)
        logger.info("  -> %d 件取得 (累計 %d 件)", len(posts), len(all_posts))

        total_pages = int(response.headers.get("X-WP-TotalPages", 1))
        if page >= total_pages:
            break
        page += 1

    logger.info("合計 %d 件の記事を取得しました。", len(all_posts))
    return all_posts


def update_post_content(rest_api_url: str, headers: dict, post_id: int, new_content: str) -> dict:
    """記事の本文を更新する。"""
    if requests is None:
        raise ImportError("requests ライブラリが見つかりません。")

    payload = {"content": new_content}
    response = requests.post(
        f"{rest_api_url}/posts/{post_id}",
        json=payload,
        headers={**headers, "Content-Type": "application/json"},
        timeout=30,
    )
    response.raise_for_status()
    return response.json()


# ---------------------------------------------------------------------------
# キーワード抽出・関連性スコア計算
# ---------------------------------------------------------------------------

STOP_WORDS = {
    "の", "に", "は", "を", "が", "で", "と", "て", "た", "し",
    "な", "も", "や", "か", "から", "まで", "より", "へ", "で", "ね",
    "よ", "わ", "さ", "れ", "る", "する", "ある", "いる", "なる",
    "こと", "もの", "ため", "それ", "これ", "あの", "その", "この",
    "など", "ずつ", "だけ", "でも", "など", "ほど", "まま", "ながら",
    "について", "として", "による", "において", "における",
}

RE_HTML_TAG = re.compile(r"<[^>]+>")
RE_NON_WORD = re.compile(r"[^\w\u3000-\u9fff\uff00-\uffef]")


def extract_text(html_content: str) -> str:
    text = RE_HTML_TAG.sub(" ", html_content or "")
    return text.strip()


def tokenize(text: str) -> list[str]:
    text = RE_NON_WORD.sub(" ", text)
    tokens = [t.strip() for t in text.split() if len(t.strip()) >= 2]
    return [t for t in tokens if t not in STOP_WORDS]


def extract_ngrams(tokens: list[str], n: int = 2) -> list[str]:
    return [" ".join(tokens[i:i+n]) for i in range(len(tokens) - n + 1)]


def build_keyword_set(title: str, content_html: str) -> set[str]:
    title_text = extract_text(title)
    body_text = extract_text(content_html)
    combined = f"{title_text} {body_text}"
    tokens = tokenize(combined)
    unigrams = set(tokens)
    bigrams = set(extract_ngrams(tokens, 2))
    return unigrams | bigrams


def compute_relevance(kw_a: set[str], kw_b: set[str]) -> int:
    return len(kw_a & kw_b)


# ---------------------------------------------------------------------------
# 内部リンクの挿入
# ---------------------------------------------------------------------------

LINK_SECTION_MARKER = "<!-- internal-links-section -->"


def already_linked(content_html: str, target_url: str) -> bool:
    return target_url in content_html


def build_related_links_html(related_posts: list[dict]) -> str:
    items = "\n".join(
        f'  <li><a href="{p["url"]}">{p["title"]}</a></li>'
        for p in related_posts
    )
    return (
        f"\n{LINK_SECTION_MARKER}\n"
        "<div class=\"related-articles\">\n"
        "<h3>関連記事</h3>\n"
        f"<ul>\n{items}\n</ul>\n"
        "</div>\n"
    )


def insert_links(original_content: str, related_posts: list[dict]) -> str:
    if LINK_SECTION_MARKER in original_content:
        idx = original_content.index(LINK_SECTION_MARKER)
        original_content = original_content[:idx].rstrip()

    links_html = build_related_links_html(related_posts)
    return original_content + links_html


# ---------------------------------------------------------------------------
# メイン処理
# ---------------------------------------------------------------------------

def process_posts(dry_run: bool = False) -> list[dict]:
    settings = load_settings()
    wp = settings["wordpress"]
    rest_api_url = wp.get("rest_api_url", "https://sim-hikaku.online/wp-json/wp/v2")
    auth_headers = build_auth_header(wp["username"], wp["app_password"])

    posts = fetch_all_posts(rest_api_url, auth_headers)
    if not posts:
        logger.warning("記事が0件でした。処理を終了します。")
        return []

    post_meta: list[dict] = []
    for post in posts:
        content_html = post.get("content", {}).get("rendered", "") if isinstance(post.get("content"), dict) else str(post.get("content", ""))
        title_html = post.get("title", {}).get("rendered", "") if isinstance(post.get("title"), dict) else str(post.get("title", ""))
        title_text = extract_text(title_html)
        kw_set = build_keyword_set(title_text, content_html)
        post_meta.append({
            "id": post["id"],
            "title": title_text,
            "url": post.get("link", ""),
            "content": content_html,
            "keywords": kw_set,
        })

    logger.info("キーワード抽出完了。記事数: %d", len(post_meta))

    logger.info("関連性スコアを計算しています...")
    relevance: dict[tuple[int, int], int] = {}
    for a, b in combinations(range(len(post_meta)), 2):
        score = compute_relevance(post_meta[a]["keywords"], post_meta[b]["keywords"])
        relevance[(a, b)] = score

    changes: list[dict] = []
    TOP_N = 3

    for idx, post in enumerate(post_meta):
        logger.info("記事処理中: [%d] %s", post["id"], post["title"])

        scored: list[tuple[int, int]] = []
        for jdx, other in enumerate(post_meta):
            if idx == jdx:
                continue
            key = (min(idx, jdx), max(idx, jdx))
            score = relevance.get(key, 0)
            if already_linked(post["content"], other["url"]):
                logger.debug("  スキップ（既リンク）: %s", other["title"])
                continue
            scored.append((score, jdx))

        scored.sort(key=lambda x: x[0], reverse=True)
        top_related = [
            {"title": post_meta[jdx]["title"], "url": post_meta[jdx]["url"], "score": score}
            for score, jdx in scored[:TOP_N]
            if score > 0
        ]

        if not top_related:
            logger.info("  -> 関連記事なし（スキップ）")
            continue

        logger.info("  -> 関連記事: %s", [r["title"] for r in top_related])

        new_content = insert_links(post["content"], top_related)

        change_record = {
            "post_id": post["id"],
            "post_title": post["title"],
            "post_url": post["url"],
            "related_links_added": top_related,
            "status": "skipped_dry_run" if dry_run else "pending",
        }

        if not dry_run:
            try:
                update_post_content(rest_api_url, auth_headers, post["id"], new_content)
                change_record["status"] = "updated"
                logger.info("  -> 更新完了: post_id=%d", post["id"])
            except Exception as exc:
                change_record["status"] = f"error: {exc}"
                logger.error("  -> 更新失敗: %s", exc)
        else:
            logger.info("  -> [DRY RUN] 更新をスキップしました。")

        changes.append(change_record)

    return changes


def save_report(changes: list[dict]) -> Path:
    REPORTS_DIR.mkdir(parents=True, exist_ok=True)
    today = date.today().strftime("%Y-%m-%d")
    report_path = REPORTS_DIR / f"internal-links-{today}.json"

    report = {
        "generated_at": today,
        "total_posts_updated": sum(1 for c in changes if c.get("status") == "updated"),
        "changes": changes,
    }

    with report_path.open("w", encoding="utf-8") as f:
        json.dump(report, f, ensure_ascii=False, indent=2)

    logger.info("レポートを保存しました: %s", report_path)
    return report_path


# ---------------------------------------------------------------------------
# エントリーポイント
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(
        description="WordPress記事間に内部リンクを自動挿入するスクリプト (sim-hikaku.online)"
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="実際の更新を行わずに処理結果を確認する",
    )
    args = parser.parse_args()

    logger.info("=== 内部リンク自動挿入スクリプト 開始 (sim-hikaku.online) ===")
    if args.dry_run:
        logger.info("[DRY RUN モード] 実際の更新は行いません。")

    try:
        changes = process_posts(dry_run=args.dry_run)
        report_path = save_report(changes)

        updated = sum(1 for c in changes if c.get("status") == "updated")
        dry_run_count = sum(1 for c in changes if c.get("status") == "skipped_dry_run")
        errors = sum(1 for c in changes if str(c.get("status", "")).startswith("error"))

        logger.info("=== 処理完了 ===")
        logger.info("  更新成功: %d 件", updated)
        logger.info("  DRY RUN スキップ: %d 件", dry_run_count)
        logger.info("  エラー: %d 件", errors)
        logger.info("  レポート: %s", report_path)

    except Exception as exc:
        logger.exception("予期しないエラーが発生しました: %s", exc)
        raise SystemExit(1)


if __name__ == "__main__":
    main()
