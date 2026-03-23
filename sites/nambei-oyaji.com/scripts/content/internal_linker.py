"""
internal_linker.py
==================
WordPressの公開済み記事間に内部リンクを自動挿入するスクリプト。

処理フロー:
1. settings.json からWordPress認証情報を読み込む
2. WP REST API で公開済み記事を全件取得
3. 各記事のID・タイトル・URL・キーワードを抽出
4. 記事ペアの関連性スコアを計算（タイトル・本文の共通キーワード数）
5. 各記事について未リンクの上位3記事を特定
6. 関連記事へのリンクを本文末尾のセクションとして追加
7. WP REST API で記事を更新
8. 変更ログを outputs/reports/internal-links-YYYY-MM-DD.json に保存
"""

import json
import re
import logging
import argparse
from pathlib import Path
from datetime import date
from collections import defaultdict
from itertools import combinations
from base64 import b64encode

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
    """settings.json を読み込み、secrets.json の認証情報をマージして返す。"""
    logger.info("設定ファイルを読み込んでいます: %s", CONFIG_PATH)
    with CONFIG_PATH.open(encoding="utf-8") as f:
        config = json.load(f)
    if SECRETS_PATH.exists():
        with SECRETS_PATH.open(encoding="utf-8") as f:
            secrets = json.load(f)
        for section, values in secrets.items():
            if isinstance(values, dict) and section in config:
                config[section].update(values)
    return config


# ---------------------------------------------------------------------------
# WordPress API ヘルパー
# ---------------------------------------------------------------------------

def build_auth_header(username: str, app_password: str) -> dict:
    """Basic 認証ヘッダーを生成する。"""
    token = b64encode(f"{username}:{app_password}".encode()).decode()
    return {"Authorization": f"Basic {token}"}


def fetch_all_posts(rest_api_url: str, headers: dict) -> list[dict]:
    """
    公開済み記事を全件取得する。
    WP REST API は per_page 最大100件のため、ページネーションで全件取得する。
    """
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
            # WP は範囲外ページで 400 を返すことがある
            break
        response.raise_for_status()

        posts = response.json()
        if not posts:
            break

        all_posts.extend(posts)
        logger.info("  -> %d 件取得 (累計 %d 件)", len(posts), len(all_posts))

        # X-WP-TotalPages ヘッダーで最終ページを判断
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

# 日本語ストップワード（簡易版）
STOP_WORDS = {
    "の", "に", "は", "を", "が", "で", "と", "て", "た", "し",
    "な", "も", "や", "か", "から", "まで", "より", "へ", "で", "ね",
    "よ", "わ", "さ", "れ", "る", "する", "ある", "いる", "なる",
    "こと", "もの", "ため", "それ", "これ", "あの", "その", "この",
    "など", "ずつ", "だけ", "でも", "など", "ほど", "まま", "ながら",
    "について", "として", "による", "において", "における",
}

# HTMLタグを除去する正規表現
RE_HTML_TAG = re.compile(r"<[^>]+>")
# 英数字以外の区切り文字
RE_NON_WORD = re.compile(r"[^\w\u3000-\u9fff\uff00-\uffef]")


def extract_text(html_content: str) -> str:
    """HTML から純テキストを抽出する。"""
    text = RE_HTML_TAG.sub(" ", html_content or "")
    return text.strip()


def tokenize(text: str) -> list[str]:
    """
    簡易トークナイズ。
    スペース・記号で分割し、2文字以上かつストップワード以外を返す。
    """
    text = RE_NON_WORD.sub(" ", text)
    tokens = [t.strip() for t in text.split() if len(t.strip()) >= 2]
    return [t for t in tokens if t not in STOP_WORDS]


def extract_ngrams(tokens: list[str], n: int = 2) -> list[str]:
    """連続するトークンから n-gram フレーズを生成する。"""
    return [" ".join(tokens[i:i+n]) for i in range(len(tokens) - n + 1)]


def build_keyword_set(title: str, content_html: str) -> set[str]:
    """記事タイトルと本文からキーワードセットを構築する。"""
    title_text = extract_text(title)
    body_text = extract_text(content_html)
    combined = f"{title_text} {body_text}"
    tokens = tokenize(combined)
    unigrams = set(tokens)
    bigrams = set(extract_ngrams(tokens, 2))
    return unigrams | bigrams


def compute_relevance(kw_a: set[str], kw_b: set[str]) -> int:
    """2つのキーワードセット間の共通キーワード数を関連性スコアとして返す。"""
    return len(kw_a & kw_b)


# ---------------------------------------------------------------------------
# 内部リンクの挿入
# ---------------------------------------------------------------------------

LINK_SECTION_MARKER = "<!-- internal-links-section -->"


def already_linked(content_html: str, target_url: str) -> bool:
    """記事本文に既にターゲットURLへのリンクが含まれているか確認する。"""
    return target_url in content_html


def build_related_links_html(related_posts: list[dict]) -> str:
    """関連記事リンクセクションのHTMLを構築する。"""
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
    """
    本文末尾に関連記事セクションを追加する。
    既存の内部リンクセクションは置換する。
    """
    # 既存のセクションを除去
    if LINK_SECTION_MARKER in original_content:
        idx = original_content.index(LINK_SECTION_MARKER)
        original_content = original_content[:idx].rstrip()

    links_html = build_related_links_html(related_posts)
    return original_content + links_html


# ---------------------------------------------------------------------------
# メイン処理
# ---------------------------------------------------------------------------

def process_posts(dry_run: bool = False) -> list[dict]:
    """
    全記事を処理し、内部リンクを追加する。
    dry_run=True の場合は実際の更新を行わない。
    """
    settings = load_settings()
    wp = settings["wordpress"]
    rest_api_url = wp["rest_api_url"]
    auth_headers = build_auth_header(wp["username"], wp["app_password"])

    # 全記事取得
    posts = fetch_all_posts(rest_api_url, auth_headers)
    if not posts:
        logger.warning("記事が0件でした。処理を終了します。")
        return []

    # 各記事のメタデータとキーワードセットを構築
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

    # 記事ペアの関連性スコアを計算
    logger.info("関連性スコアを計算しています...")
    relevance: dict[tuple[int, int], int] = {}
    for a, b in combinations(range(len(post_meta)), 2):
        score = compute_relevance(post_meta[a]["keywords"], post_meta[b]["keywords"])
        relevance[(a, b)] = score

    # 各記事について上位3件の関連記事を特定し、リンクを挿入
    changes: list[dict] = []
    TOP_N = 3

    for idx, post in enumerate(post_meta):
        logger.info("記事処理中: [%d] %s", post["id"], post["title"])

        # このポストとの関連スコアを取得
        scored: list[tuple[int, int]] = []
        for jdx, other in enumerate(post_meta):
            if idx == jdx:
                continue
            key = (min(idx, jdx), max(idx, jdx))
            score = relevance.get(key, 0)
            # 既にリンク済みはスキップ
            if already_linked(post["content"], other["url"]):
                logger.debug("  スキップ（既リンク）: %s", other["title"])
                continue
            scored.append((score, jdx))

        # スコア降順でソートし上位N件を選択
        scored.sort(key=lambda x: x[0], reverse=True)
        top_related = [
            {"title": post_meta[jdx]["title"], "url": post_meta[jdx]["url"], "score": score}
            for score, jdx in scored[:TOP_N]
            if score > 0  # スコアが0より大きいもののみ
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
    """変更ログを JSON ファイルに保存する。"""
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
        description="WordPress記事間に内部リンクを自動挿入するスクリプト"
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="実際の更新を行わずに処理結果を確認する",
    )
    args = parser.parse_args()

    logger.info("=== 内部リンク自動挿入スクリプト 開始 ===")
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
