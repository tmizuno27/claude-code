"""
article_generator.py
=====================
Claude API を使った SEO 最適化記事自動生成スクリプト

機能:
- inputs/keywords/ から未処理の次のキーワードを取得する
- templates/article-template.md の記事構成テンプレートを読み込む
- docs/article-writer-agent.md のエージェント定義を読み込む
- config/affiliate-links.json から関連アフィリエイトリンクを選択する
- Claude API で 2500〜3500 字の SEO 記事を生成する
- outputs/articles/YYYY-MM-DD/{keyword-slug}.md に保存する
- キーワードキューのステータスを "processed" に更新する
"""

import json
import logging
import re
import unicodedata
from datetime import date
from pathlib import Path

import anthropic

# ==============================================================================
# ロギング設定
# ==============================================================================
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
logger = logging.getLogger(__name__)

# ==============================================================================
# パス定数
# ==============================================================================
BASE_DIR = Path(__file__).resolve().parent.parent.parent
CONFIG_DIR = BASE_DIR / "config"
INPUTS_KEYWORDS_DIR = BASE_DIR / "inputs" / "keywords"
OUTPUTS_ARTICLES_DIR = BASE_DIR / "outputs" / "articles"
TEMPLATES_DIR = BASE_DIR / "templates"
AGENTS_DIR = BASE_DIR / "docs"

SETTINGS_FILE = CONFIG_DIR / "settings.json"
AFFILIATE_LINKS_FILE = CONFIG_DIR / "affiliate-links.json"
ARTICLE_TEMPLATE_FILE = TEMPLATES_DIR / "article-template.md"
ARTICLE_WRITER_AGENT_FILE = AGENTS_DIR / "article-writer-agent.md"


# ==============================================================================
# 設定ファイルの読み込み
# ==============================================================================

def load_settings() -> dict:
    """
    config/settings.json から設定を読み込む。

    Returns:
        設定辞書

    Raises:
        FileNotFoundError: 設定ファイルが存在しない場合
        ValueError: JSON フォーマットが不正な場合
    """
    if not SETTINGS_FILE.exists():
        raise FileNotFoundError(f"設定ファイルが見つかりません: {SETTINGS_FILE}")

    with open(SETTINGS_FILE, encoding="utf-8") as f:
        settings: dict = json.load(f)

    # Claude API キーを secrets.json から読み込む
    secrets_file = SETTINGS_FILE.parent / "secrets.json"
    if secrets_file.exists():
        with open(secrets_file, encoding="utf-8") as sf:
            secrets = json.load(sf)
        api_key = secrets.get("claude_api", {}).get("api_key", "")
        if api_key:
            settings.setdefault("claude_api", {})["api_key"] = api_key

    api_key = settings.get("claude_api", {}).get("api_key", "")
    if not api_key or api_key.startswith("SEE ") or api_key == "YOUR_CLAUDE_API_KEY_HERE":
        raise ValueError(
            "Claude API キーが設定されていません。"
            "config/secrets.json の claude_api.api_key を確認してください。"
        )

    logger.info("設定ファイルを読み込みました")
    return settings


def load_affiliate_links() -> dict:
    """
    config/affiliate-links.json からアフィリエイトリンク情報を読み込む。

    Returns:
        アフィリエイトリンク設定辞書

    Raises:
        FileNotFoundError: ファイルが存在しない場合
    """
    if not AFFILIATE_LINKS_FILE.exists():
        raise FileNotFoundError(
            f"アフィリエイトリンクファイルが見つかりません: {AFFILIATE_LINKS_FILE}"
        )

    with open(AFFILIATE_LINKS_FILE, encoding="utf-8") as f:
        affiliate_data: dict = json.load(f)

    logger.info("アフィリエイトリンクを読み込みました")
    return affiliate_data


# ==============================================================================
# テンプレート・エージェント定義の読み込み
# ==============================================================================

def load_template(file_path: Path, file_label: str) -> str:
    """
    テキストファイルを UTF-8 で読み込む汎用関数。

    Args:
        file_path: 読み込むファイルのパス
        file_label: ログ出力用のラベル文字列

    Returns:
        ファイルの内容文字列

    Raises:
        FileNotFoundError: ファイルが存在しない場合
    """
    if not file_path.exists():
        raise FileNotFoundError(f"{file_label}が見つかりません: {file_path}")

    content = file_path.read_text(encoding="utf-8")
    logger.info("%s を読み込みました (%d 文字)", file_label, len(content))
    return content


# ==============================================================================
# キーワードキューの操作
# ==============================================================================

def find_latest_queue_file() -> Path | None:
    """
    inputs/keywords/ 配下で最新の queue-*.json ファイルを探す。

    Returns:
        最新キューファイルのパス。見つからない場合は None。
    """
    if not INPUTS_KEYWORDS_DIR.exists():
        logger.warning(
            "キーワードディレクトリが存在しません: %s", INPUTS_KEYWORDS_DIR
        )
        return None

    queue_files = sorted(INPUTS_KEYWORDS_DIR.glob("queue-*.json"), reverse=True)

    if not queue_files:
        logger.warning("キーワードキューファイルが見つかりません")
        return None

    latest = queue_files[0]
    logger.info("最新キューファイル: %s", latest.name)
    return latest


def load_keyword_queue(queue_file: Path) -> list[dict]:
    """
    キューファイルを読み込む。

    Args:
        queue_file: キューファイルのパス

    Returns:
        キーワードエントリのリスト
    """
    with open(queue_file, encoding="utf-8") as f:
        entries: list[dict] = json.load(f)
    return entries


def find_next_keyword(queue_file: Path) -> tuple[dict | None, int]:
    """
    キューから次の未処理キーワードを取得する。

    Args:
        queue_file: キューファイルのパス

    Returns:
        (キーワードエントリ辞書, インデックス) のタプル。
        未処理がない場合は (None, -1)。
    """
    entries = load_keyword_queue(queue_file)

    for idx, entry in enumerate(entries):
        if entry.get("status", "pending") == "pending":
            logger.info(
                "次の処理対象キーワード: '%s' (優先度: %s)",
                entry.get("keyword"),
                entry.get("priority"),
            )
            return entry, idx

    logger.info("キューに未処理のキーワードがありません")
    return None, -1


def mark_keyword_as_processed(queue_file: Path, index: int, article_path: str) -> None:
    """
    指定インデックスのキーワードを処理済みに更新する。

    Args:
        queue_file: キューファイルのパス
        index: 更新するエントリのインデックス
        article_path: 生成した記事ファイルのパス（ログ用）
    """
    entries = load_keyword_queue(queue_file)

    if 0 <= index < len(entries):
        entries[index]["status"] = "processed"
        entries[index]["article_path"] = article_path
        entries[index]["processed_date"] = date.today().isoformat()

    with open(queue_file, mode="w", encoding="utf-8") as f:
        json.dump(entries, f, ensure_ascii=False, indent=2)

    logger.info(
        "キーワードのステータスを 'processed' に更新しました: '%s'",
        entries[index].get("keyword") if 0 <= index < len(entries) else "unknown",
    )


# ==============================================================================
# アフィリエイトリンクの選択
# ==============================================================================

def select_relevant_affiliate_links(
    keyword: str, affiliate_data: dict, max_links: int = 5
) -> list[dict]:
    """
    キーワードに関連するアフィリエイトリンクを選択する。

    キーワードとアフィリエイトリンクの context フィールドを照合して
    関連性の高いリンクを優先して返す。

    Args:
        keyword: 対象キーワード
        affiliate_data: アフィリエイトリンク設定辞書
        max_links: 最大返却件数

    Returns:
        選択されたアフィリエイトリンク情報のリスト
    """
    # キーワードから検索用トークンを生成
    keyword_lower = keyword.lower()
    keyword_tokens = set(keyword_lower.replace(" ", "").replace("　", ""))

    all_links: list[tuple[int, dict]] = []  # (関連スコア, リンク情報)

    categories: dict = affiliate_data.get("categories", {})

    for category_data in categories.values():
        for link in category_data.get("links", []):
            context = link.get("context", "").lower()
            link_name = link.get("name", "").lower()
            anchor_texts = " ".join(link.get("anchor_text", [])).lower()

            # 関連スコア計算
            relevance = 0

            # キーワードトークンとの一致度チェック
            for token in ["ai", "副業", "稼ぐ", "自動", "ライティング", "ブログ",
                          "プログラミング", "学習", "スキル", "フリーランス",
                          "claude", "chatgpt", "ツール", "ビジネス"]:
                if token in keyword_lower:
                    if token in context or token in link_name or token in anchor_texts:
                        relevance += 3

            # コンテキスト内のキーワードとの部分一致
            kw_parts = keyword_lower.split()
            for part in kw_parts:
                if len(part) >= 2 and part in context:
                    relevance += 2

            all_links.append((relevance, link))

    # 関連スコア降順でソートして上位を返す
    all_links.sort(key=lambda x: x[0], reverse=True)

    selected = [link for _, link in all_links[:max_links]]

    logger.info(
        "キーワード '%s' に対して %d 件のアフィリエイトリンクを選択しました",
        keyword,
        len(selected),
    )
    return selected


# ==============================================================================
# スラッグ生成
# ==============================================================================

def keyword_to_slug(keyword: str) -> str:
    """
    キーワードをファイル名に使えるスラッグ（ASCII + ハイフン）に変換する。

    日本語キーワードはローマ字変換するのではなく、
    Unicode カテゴリに基づいて英数字・ハイフンのみ残す簡易変換を行う。

    Args:
        keyword: 変換対象のキーワード

    Returns:
        スラッグ文字列 (例: "ai-fukugyou-hajimékata")
    """
    # 全角スペースを半角に
    slug = keyword.replace("\u3000", " ").replace("　", " ")

    # スペースをハイフンに変換
    slug = slug.replace(" ", "-")

    # ASCII 以外の文字を NFKD 正規化してから処理
    slug = unicodedata.normalize("NFKD", slug)

    # ASCII 英数字とハイフン以外を除去
    slug = re.sub(r"[^\w\-]", "", slug, flags=re.ASCII)

    # 複数ハイフンを1つに
    slug = re.sub(r"-+", "-", slug)

    # 先頭・末尾のハイフン除去
    slug = slug.strip("-")

    # 空になった場合はキーワードの文字コードで代替
    if not slug:
        slug = f"article-{abs(hash(keyword)) % 100000:05d}"

    # ファイル名が長すぎる場合は切り詰める
    if len(slug) > 80:
        slug = slug[:80].rstrip("-")

    return slug.lower()


# ==============================================================================
# フロントマター生成
# ==============================================================================

def build_front_matter(
    title: str,
    keyword: str,
    affiliate_links_used: list[dict],
    word_count: int = 0,
) -> str:
    """
    記事ファイル用の YAML フロントマターを生成する。

    Args:
        title: 記事タイトル
        keyword: ターゲットキーワード
        affiliate_links_used: 使用したアフィリエイトリンクのリスト
        word_count: 生成された記事の文字数

    Returns:
        フロントマター文字列（--- で囲まれた YAML ブロック）
    """
    today = date.today().isoformat()
    affiliate_names = [link.get("name", "") for link in affiliate_links_used]

    front_matter_lines = [
        "---",
        f'title: "{title}"',
        f'keyword: "{keyword}"',
        f"date: {today}",
        'status: "draft"',
        f"word_count: {word_count}",
        "affiliate_links_used:",
    ]

    for name in affiliate_names:
        front_matter_lines.append(f'  - "{name}"')

    front_matter_lines.append("---")
    return "\n".join(front_matter_lines)


# ==============================================================================
# Claude API 呼び出し
# ==============================================================================

def build_user_prompt(
    keyword: str,
    template_content: str,
    affiliate_links: list[dict],
    min_words: int,
    max_words: int,
    disclosure_text: str,
) -> str:
    """
    Claude への user プロンプトを組み立てる。

    Args:
        keyword: ターゲットキーワード
        template_content: 記事テンプレートの内容
        affiliate_links: 使用するアフィリエイトリンクのリスト
        min_words: 最小文字数
        max_words: 最大文字数
        disclosure_text: アフィリエイト開示テキスト

    Returns:
        プロンプト文字列
    """
    # アフィリエイトリンクを人間が読みやすい形式にフォーマット
    affiliate_section_lines = ["## 使用するアフィリエイトリンク\n"]
    if affiliate_links:
        for link in affiliate_links:
            name = link.get("name", "")
            url = link.get("url", "")
            anchor_texts = link.get("anchor_text", [])
            context = link.get("context", "")
            affiliate_section_lines.append(f"### {name}")
            affiliate_section_lines.append(f"- URL: {url}")
            if anchor_texts:
                affiliate_section_lines.append(
                    f"- アンカーテキスト候補: {', '.join(anchor_texts)}"
                )
            if context:
                affiliate_section_lines.append(f"- 使用場面: {context}")
            affiliate_section_lines.append("")
    else:
        affiliate_section_lines.append("(今回はアフィリエイトリンクなし)")

    affiliate_section = "\n".join(affiliate_section_lines)

    prompt = f"""# 記事生成リクエスト

## ターゲットキーワード
{keyword}

## 記事要件
- **文字数目標**: {min_words}〜{max_words} 文字（本文のみ、フロントマター除く）
- **言語**: 日本語
- **SEO最適化**: ターゲットキーワードを自然に盛り込む
- **読者対象**: パラグアイ移住・海外生活・海外からの仕事に興味を持つ日本人
- **トーン**: 親しみやすく実践的。具体的な手順や数字を含める
- **著者名**: 「南米おやじ」のみ使用すること。本名・実名は絶対に記載禁止
- **居住地**: 「アスンシオン」と表記すること

## 記事テンプレート構成
以下のテンプレート構成に従って記事を作成してください:

{template_content}

{affiliate_section}

## アフィリエイト開示
記事の冒頭（H1の直下）に以下の開示文を必ず追加してください:
{disclosure_text}

## 出力形式
- Markdown 形式で出力する
- 1行目に `# 記事タイトル` を含める（キーワードを含む魅力的なタイトル）
- H2・H3 見出しを適切に使い、読みやすい構成にする
- アフィリエイトリンクはアンカーテキストで自然にリンクする
  例: [ChatGPT Plus](https://YOUR-AFFILIATE-LINK/chatgpt)
- まとめセクションを最後に必ず入れる
"""

    return prompt


def call_claude_api(
    client: anthropic.Anthropic,
    model: str,
    max_tokens: int,
    system_prompt: str,
    user_prompt: str,
) -> str:
    """
    Claude API を呼び出して記事テキストを生成する。

    Args:
        client: Anthropic クライアントインスタンス
        model: 使用するモデル ID
        max_tokens: 最大出力トークン数
        system_prompt: システムプロンプト（エージェント定義）
        user_prompt: ユーザープロンプト（記事生成リクエスト）

    Returns:
        生成された記事テキスト

    Raises:
        anthropic.APIError: API エラーが発生した場合
    """
    logger.info("Claude API 呼び出し中 (streaming)... (モデル: %s, 最大トークン: %d)", model, max_tokens)

    generated_text = ""
    input_tokens = 0
    output_tokens = 0

    with client.messages.stream(
        model=model,
        max_tokens=max_tokens,
        system=system_prompt,
        messages=[
            {
                "role": "user",
                "content": user_prompt,
            }
        ],
    ) as stream:
        for text in stream.text_stream:
            generated_text += text

        # ストリーム完了後にusageを取得
        response = stream.get_final_message()
        input_tokens = response.usage.input_tokens
        output_tokens = response.usage.output_tokens

    logger.info(
        "API レスポンス受信: 入力 %d トークン / 出力 %d トークン",
        input_tokens,
        output_tokens,
    )

    return generated_text


# ==============================================================================
# 記事タイトルの抽出
# ==============================================================================

def extract_title_from_article(article_content: str, fallback_keyword: str) -> str:
    """
    生成された記事の Markdown テキストから H1 タイトルを抽出する。

    Args:
        article_content: 生成された記事の Markdown テキスト
        fallback_keyword: タイトルが見つからない場合のフォールバックキーワード

    Returns:
        記事タイトル文字列
    """
    for line in article_content.splitlines():
        line = line.strip()
        if line.startswith("# "):
            title = line[2:].strip()
            if title:
                return title

    # H1 が見つからない場合はキーワードから生成
    return f"{fallback_keyword}の完全ガイド"


# ==============================================================================
# 記事ファイルの保存
# ==============================================================================

def save_article(
    keyword: str,
    article_content: str,
    front_matter: str,
) -> Path:
    """
    生成された記事をファイルに保存する。

    Args:
        keyword: ターゲットキーワード
        article_content: 生成された記事の Markdown テキスト（H1 タイトルを含む）
        front_matter: YAML フロントマター文字列

    Returns:
        保存したファイルのパス
    """
    today_str = date.today().strftime("%Y-%m-%d")
    slug = keyword_to_slug(keyword)

    # 出力ディレクトリを作成
    output_dir = OUTPUTS_ARTICLES_DIR / today_str
    output_dir.mkdir(parents=True, exist_ok=True)

    output_file = output_dir / f"{slug}.md"

    # フロントマターと本文を結合
    full_content = f"{front_matter}\n\n{article_content}\n"

    with open(output_file, mode="w", encoding="utf-8") as f:
        f.write(full_content)

    logger.info("記事を保存しました: %s", output_file)
    return output_file


# ==============================================================================
# コンソールサマリー出力
# ==============================================================================

def print_summary(
    keyword: str,
    article_file: Path,
    word_count: int,
    affiliate_links_used: list[dict],
) -> None:
    """
    記事生成結果のサマリーをコンソールに出力する。

    Args:
        keyword: 処理したキーワード
        article_file: 生成した記事ファイルのパス
        word_count: 生成した記事の文字数
        affiliate_links_used: 使用したアフィリエイトリンクのリスト
    """
    print("\n" + "=" * 60)
    print("  記事生成完了")
    print("=" * 60)
    print(f"  キーワード       : {keyword}")
    print(f"  保存先ファイル   : {article_file}")
    print(f"  文字数           : {word_count:,} 文字")

    if affiliate_links_used:
        print(f"  アフィリエイト   : {len(affiliate_links_used)} 件使用")
        for link in affiliate_links_used:
            print(f"    - {link.get('name', '')}")

    print()
    print("  次のステップ: wp_publisher.py を実行して WordPress に投稿してください")
    print("=" * 60 + "\n")


# ==============================================================================
# エントリーポイント
# ==============================================================================

def main() -> None:
    """
    記事生成のメイン処理。

    1. 設定ファイルを読み込む
    2. キーワードキューから次の未処理キーワードを取得する
    3. テンプレート・エージェント定義を読み込む
    4. Claude API で記事を生成する
    5. 記事ファイルを保存する
    6. キューのステータスを更新する
    """
    logger.info("記事生成パイプライン開始")

    # --- 設定読み込み ---
    try:
        settings = load_settings()
        affiliate_data = load_affiliate_links()
    except (FileNotFoundError, ValueError) as e:
        logger.error("初期化エラー: %s", e)
        raise

    # --- Claude API 設定 ---
    claude_settings = settings.get("claude_api", {})
    api_key: str = claude_settings.get("api_key", "")
    model: str = claude_settings.get("model", "claude-sonnet-4-6")
    max_tokens: int = claude_settings.get("max_tokens", 4096)

    article_settings = settings.get("article", {})
    min_words: int = article_settings.get("min_words", 2500)
    max_words: int = article_settings.get("max_words", 3500)

    insertion_rules: dict = affiliate_data.get("insertion_rules", {})
    disclosure_text: str = insertion_rules.get(
        "disclosure_text",
        "※この記事にはアフィリエイトリンクが含まれています。",
    )
    max_affiliate_links: int = insertion_rules.get("max_affiliate_links_per_article", 5)

    # --- キーワードキューの読み込み ---
    queue_file = find_latest_queue_file()
    if queue_file is None:
        logger.error(
            "キーワードキューファイルが見つかりません。"
            "先に keyword_research.py を実行してください。"
        )
        return

    keyword_entry, keyword_index = find_next_keyword(queue_file)
    if keyword_entry is None:
        logger.info(
            "すべてのキーワードが処理済みです。"
            "keyword_research.py を再実行して新しいキーワードを取得してください。"
        )
        return

    keyword: str = keyword_entry.get("keyword", "")
    logger.info("処理対象キーワード: '%s'", keyword)

    # --- テンプレート・エージェント定義の読み込み ---
    try:
        template_content = load_template(ARTICLE_TEMPLATE_FILE, "記事テンプレート")
    except FileNotFoundError as e:
        logger.warning("%s - 空のテンプレートで続行します", e)
        template_content = "## はじめに\n## 本文\n## まとめ"

    try:
        agent_definition = load_template(ARTICLE_WRITER_AGENT_FILE, "記事ライターエージェント定義")
    except FileNotFoundError as e:
        logger.warning("%s - デフォルトシステムプロンプトで続行します", e)
        agent_definition = (
            "あなたは日本語の SEO 最適化記事を書く専門家です。"
            "読者に価値のある実践的な情報を、自然な日本語で提供してください。"
        )

    # --- アフィリエイトリンクの選択 ---
    selected_affiliate_links = select_relevant_affiliate_links(
        keyword, affiliate_data, max_links=max_affiliate_links
    )

    # --- プロンプト構築 ---
    user_prompt = build_user_prompt(
        keyword=keyword,
        template_content=template_content,
        affiliate_links=selected_affiliate_links,
        min_words=min_words,
        max_words=max_words,
        disclosure_text=disclosure_text,
    )

    # --- Claude API 呼び出し ---
    try:
        client = anthropic.Anthropic(api_key=api_key, timeout=600.0)
        generated_article = call_claude_api(
            client=client,
            model=model,
            max_tokens=max_tokens,
            system_prompt=agent_definition,
            user_prompt=user_prompt,
        )
    except anthropic.AuthenticationError:
        logger.error(
            "Claude API 認証エラー。config/settings.json の api_key を確認してください。"
        )
        raise
    except anthropic.RateLimitError:
        logger.error("Claude API レート制限エラー。しばらく待ってから再実行してください。")
        raise
    except anthropic.APIStatusError as e:
        logger.error("Claude API エラー (ステータス %s): %s", e.status_code, e.message)
        raise
    except anthropic.APIConnectionError:
        logger.error("Claude API への接続に失敗しました。ネットワーク接続を確認してください。")
        raise

    if not generated_article.strip():
        logger.error("Claude API から空のレスポンスが返されました")
        return

    # --- 記事情報の抽出 ---
    title = extract_title_from_article(generated_article, keyword)
    word_count = len(generated_article.replace(" ", "").replace("\n", ""))
    logger.info("記事タイトル: '%s'", title)
    logger.info("本文文字数: %d 文字", word_count)

    # --- フロントマター生成 ---
    front_matter = build_front_matter(
        title=title,
        keyword=keyword,
        affiliate_links_used=selected_affiliate_links,
        word_count=word_count,
    )

    # --- 記事ファイルの保存 ---
    try:
        article_file = save_article(
            keyword=keyword,
            article_content=generated_article,
            front_matter=front_matter,
        )
    except OSError as e:
        logger.error("記事ファイルの保存に失敗しました: %s", e)
        raise

    # --- キューのステータス更新 ---
    try:
        mark_keyword_as_processed(
            queue_file=queue_file,
            index=keyword_index,
            article_path=str(article_file),
        )
    except OSError as e:
        logger.warning("キューファイルの更新に失敗しました（記事は保存済み）: %s", e)

    # --- サマリー出力 ---
    print_summary(
        keyword=keyword,
        article_file=article_file,
        word_count=word_count,
        affiliate_links_used=selected_affiliate_links,
    )


if __name__ == "__main__":
    main()
