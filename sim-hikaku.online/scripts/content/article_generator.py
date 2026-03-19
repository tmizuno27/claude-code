"""
article_generator.py
=====================
Claude API を使った SEO 最適化記事自動生成スクリプト
SIM比較オンライン (sim-hikaku.online) 版。

機能:
- inputs/keywords/ から未処理の次のキーワードを取得する
- config/affiliate-links.json から関連アフィリエイトリンクを選択する
- Claude API で 3000〜5000 字の SEO 記事を生成する
- outputs/articles/YYYY-MM-DD/{keyword-slug}.md に保存する
- キーワードキューのステータスを "processed" に更新する
"""

import io
import json
import logging
import re
import sys
import unicodedata
from datetime import date
from pathlib import Path

# Windows UTF-8 出力修正
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding="utf-8", errors="replace")

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

SETTINGS_FILE = CONFIG_DIR / "settings.json"
SECRETS_FILE = CONFIG_DIR / "secrets.json"
AFFILIATE_LINKS_FILE = CONFIG_DIR / "affiliate-links.json"

# 格安SIMキャリア名マッピング（キーワードマッチ用）
CARRIER_KEYWORDS = {
    "ahamo": ["ahamo", "アハモ"],
    "linemo": ["linemo", "ラインモ"],
    "povo": ["povo", "ポヴォ"],
    "rakuten-mobile": ["楽天モバイル", "rakuten"],
    "uq-mobile": ["uqモバイル", "uq mobile", "uq"],
    "ymobile": ["ワイモバイル", "ymobile", "y!mobile"],
    "mineo": ["mineo", "マイネオ"],
    "iijmio": ["iijmio", "iij"],
    "his-mobile": ["hisモバイル", "his mobile"],
    "libmo": ["libmo", "リブモ"],
    "nuro-mobile": ["nuroモバイル", "nuro mobile"],
    "aeon-mobile": ["イオンモバイル", "aeon mobile"],
    "nihon-tsushin": ["日本通信", "日本通信sim"],
    "biglobe-mobile": ["biglobeモバイル", "biglobe"],
    "tone-mobile": ["toneモバイル", "tone mobile"],
}


# ==============================================================================
# 設定ファイルの読み込み
# ==============================================================================

def load_settings() -> dict:
    if not SETTINGS_FILE.exists():
        raise FileNotFoundError(f"設定ファイルが見つかりません: {SETTINGS_FILE}")

    with open(SETTINGS_FILE, encoding="utf-8") as f:
        settings: dict = json.load(f)

    # secrets.json から API キーを読み込む
    if SECRETS_FILE.exists():
        with open(SECRETS_FILE, encoding="utf-8") as sf:
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
    if not AFFILIATE_LINKS_FILE.exists():
        raise FileNotFoundError(
            f"アフィリエイトリンクファイルが見つかりません: {AFFILIATE_LINKS_FILE}"
        )

    with open(AFFILIATE_LINKS_FILE, encoding="utf-8") as f:
        affiliate_data: dict = json.load(f)

    logger.info("アフィリエイトリンクを読み込みました")
    return affiliate_data


# ==============================================================================
# キーワードキューの操作
# ==============================================================================

def find_latest_queue_file() -> Path | None:
    if not INPUTS_KEYWORDS_DIR.exists():
        logger.warning("キーワードディレクトリが存在しません: %s", INPUTS_KEYWORDS_DIR)
        return None

    queue_files = sorted(INPUTS_KEYWORDS_DIR.glob("queue-*.json"), reverse=True)
    if not queue_files:
        logger.warning("キーワードキューファイルが見つかりません")
        return None

    latest = queue_files[0]
    logger.info("最新キューファイル: %s", latest.name)
    return latest


def load_keyword_queue(queue_file: Path) -> list[dict]:
    with open(queue_file, encoding="utf-8") as f:
        entries: list[dict] = json.load(f)
    return entries


def find_next_keyword(queue_file: Path) -> tuple[dict | None, int]:
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
    """キーワードに関連するアフィリエイトリンクを選択する（提携済みのみ）"""
    keyword_lower = keyword.lower()

    all_links: list[tuple[int, dict]] = []

    for category_key, category_data in affiliate_data.items():
        if not isinstance(category_data, dict):
            continue

        for carrier_key, link in category_data.items():
            if not isinstance(link, dict):
                continue

            # 提携済みかつURLがあるもののみ
            status = link.get("status", "")
            url = link.get("url")
            if status != "提携済" or not url or "YOUR-AFFILIATE-LINK" in str(url):
                continue

            relevance = 0

            # キャリア名の直接マッチ
            carrier_aliases = CARRIER_KEYWORDS.get(carrier_key, [])
            link_name = link.get("name", "").lower()
            for alias in carrier_aliases:
                if alias.lower() in keyword_lower:
                    relevance += 10
                    break

            if link_name and link_name.lower() in keyword_lower:
                relevance += 10

            # カテゴリ関連性
            if category_key == "carriers" and any(
                term in keyword_lower
                for term in ["格安sim", "sim", "キャリア", "乗り換え", "mnp", "料金", "プラン"]
            ):
                relevance += 3

            if category_key == "wifi_wimax" and any(
                term in keyword_lower
                for term in ["wifi", "wimax", "ポケットwifi", "モバイルルーター", "データ無制限"]
            ):
                relevance += 3

            if category_key == "esim_services" and any(
                term in keyword_lower
                for term in ["esim", "海外", "旅行"]
            ):
                relevance += 3

            # 高報酬ボーナス
            commission = link.get("commission", 0)
            if isinstance(commission, (int, float)) and commission >= 5000:
                relevance += 2

            all_links.append((relevance, link))

    # 関連スコア降順でソート
    all_links.sort(key=lambda x: (-x[0], x[1].get("priority", 99)))

    selected = [link for _, link in all_links[:max_links] if _ > 0]

    # 関連リンクが足りない場合、提携済みの高優先度キャリアで埋める
    if len(selected) < 3:
        for category_key, category_data in affiliate_data.items():
            if not isinstance(category_data, dict):
                continue
            for carrier_key, link in category_data.items():
                if not isinstance(link, dict):
                    continue
                if link.get("status") == "提携済" and link.get("url") and "YOUR-AFFILIATE-LINK" not in str(link.get("url", "")):
                    if link not in selected:
                        selected.append(link)
                        if len(selected) >= max_links:
                            break
            if len(selected) >= max_links:
                break

    logger.info(
        "キーワード '%s' に対して %d 件のアフィリエイトリンクを選択しました",
        keyword, len(selected),
    )
    return selected


# ==============================================================================
# スラッグ生成
# ==============================================================================

def keyword_to_slug(keyword: str) -> str:
    """キーワードをファイル名用スラッグに変換。日本語はハッシュベースで生成。"""
    slug = keyword.replace("\u3000", " ").replace("　", " ")
    slug = slug.replace(" ", "-")
    slug = unicodedata.normalize("NFKD", slug)
    # ASCII英数字とハイフン以外を除去
    slug = re.sub(r"[^\w\-]", "", slug, flags=re.ASCII)
    slug = re.sub(r"-+", "-", slug)
    slug = slug.strip("-")

    # 日本語キーワードの場合、ASCII部分が短すぎるのでハッシュで補強
    if not slug or len(slug) < 3:
        import hashlib
        kw_hash = hashlib.md5(keyword.encode("utf-8")).hexdigest()[:8]
        if slug:
            slug = f"{slug}-{kw_hash}"
        else:
            slug = f"article-{kw_hash}"

    if len(slug) > 80:
        slug = slug[:80].rstrip("-")

    return slug.lower()


# ==============================================================================
# フロントマター生成
# ==============================================================================

def build_front_matter(
    title: str, keyword: str, affiliate_links_used: list[dict], word_count: int = 0,
) -> str:
    today = date.today().isoformat()
    affiliate_names = [link.get("name", "") for link in affiliate_links_used]

    lines = [
        "---",
        f'title: "{title}"',
        f'keyword: "{keyword}"',
        f"date: {today}",
        'status: "draft"',
        f"word_count: {word_count}",
        "affiliate_links_used:",
    ]
    for name in affiliate_names:
        lines.append(f'  - "{name}"')
    lines.append("---")
    return "\n".join(lines)


# ==============================================================================
# Claude API 呼び出し
# ==============================================================================

def build_system_prompt() -> str:
    return """あなたは日本の格安SIM・通信サービスに精通したSEO記事ライターです。

## 執筆ルール
- 一人称は「私」、著者名は「南米おやじ」のみ使用。本名は絶対に記載禁止
- 読者目線でわかりやすく、具体的な料金・速度・プラン情報を含める
- 比較記事には必ず料金比較表を含める（Markdown テーブル形式）
- 景品表示法に注意：根拠なしの「No.1」「最安」等の断定表現は避ける
- 公平な比較を心がけ、メリット・デメリットを両方記載する
- E-E-A-T重視：実際の利用体験や速度測定データに言及する

## 禁止表現
- 「いかがでしたでしょうか」「〜と言えるでしょう」等のAI的表現
- 「まとめると〜」で始まる結論
- 「〜することが大切です」の羅列
- 過度な敬語の積み重ね

## 記事フォーマット
- Markdown形式で出力
- 1行目に `# 記事タイトル`（キーワードを含む魅力的なタイトル、32文字以内）
- H2・H3見出しを適切に使い、読みやすい構成にする
- アフィリエイトリンクはアンカーテキストで自然にリンク（1記事最大5リンク、間隔300文字以上）
- 最後に「まとめ」セクションを入れる
"""


def build_user_prompt(
    keyword: str, affiliate_links: list[dict], min_words: int, max_words: int,
) -> str:
    # アフィリエイトリンクセクション
    aff_lines = ["## 使用するアフィリエイトリンク\n"]
    if affiliate_links:
        for link in affiliate_links:
            name = link.get("name", "")
            url = link.get("url", "")
            aff_lines.append(f"- **{name}**: {url}")
        aff_lines.append("")
    else:
        aff_lines.append("(今回はアフィリエイトリンクなし)\n")

    aff_section = "\n".join(aff_lines)

    return f"""# 記事生成リクエスト

## ターゲットキーワード
{keyword}

## 記事要件
- **文字数目標**: {min_words}〜{max_words} 文字（本文のみ）
- **言語**: 日本語
- **SEO最適化**: ターゲットキーワードをタイトル・H2・本文に自然に盛り込む
- **読者対象**: 格安SIMへの乗り換えを検討している日本人
- **トーン**: 親しみやすく実践的。具体的な料金・数字を含める

## 必須セクション
1. **導入**: キーワードに関する読者の悩み・疑問に共感
2. **概要/基礎知識**: キーワードに関する基本情報
3. **比較・詳細**: 料金表・速度比較・メリットデメリット（Markdownテーブル使用）
4. **選び方のポイント**: 用途別おすすめ
5. **乗り換え手順**（該当する場合）: MNP手続きの簡単な流れ
6. **まとめ**: 結論とおすすめ

## アフィリエイト開示
記事の冒頭（H1の直下）に以下を追加:
※この記事にはプロモーションが含まれています。

{aff_section}

## 出力形式
- Markdown 形式で出力
- 1行目に `# 記事タイトル`
- アフィリエイトリンクはアンカーテキストで自然にリンク
  例: [HISモバイル公式サイト](https://affiliate-url)
"""


def call_claude_api(
    client: anthropic.Anthropic, model: str, max_tokens: int,
    system_prompt: str, user_prompt: str,
) -> str:
    logger.info("Claude API 呼び出し中 (streaming)... (モデル: %s)", model)

    generated_text = ""

    with client.messages.stream(
        model=model,
        max_tokens=max_tokens,
        system=system_prompt,
        messages=[{"role": "user", "content": user_prompt}],
    ) as stream:
        for text in stream.text_stream:
            generated_text += text

        response = stream.get_final_message()
        input_tokens = response.usage.input_tokens
        output_tokens = response.usage.output_tokens

    logger.info(
        "API レスポンス受信: 入力 %d トークン / 出力 %d トークン",
        input_tokens, output_tokens,
    )
    return generated_text


# ==============================================================================
# 記事タイトルの抽出
# ==============================================================================

def extract_title_from_article(article_content: str, fallback_keyword: str) -> str:
    for line in article_content.splitlines():
        line = line.strip()
        if line.startswith("# "):
            title = line[2:].strip()
            if title:
                return title
    return f"{fallback_keyword}の完全ガイド"


# ==============================================================================
# 記事ファイルの保存
# ==============================================================================

def save_article(keyword: str, article_content: str, front_matter: str) -> Path:
    today_str = date.today().strftime("%Y-%m-%d")
    slug = keyword_to_slug(keyword)

    output_dir = OUTPUTS_ARTICLES_DIR / today_str
    output_dir.mkdir(parents=True, exist_ok=True)

    output_file = output_dir / f"{slug}.md"

    # Claude APIの出力にフロントマターが含まれている場合は除去（二重挿入防止）
    if article_content.strip().startswith('---'):
        article_content = re.sub(r'^---\s*\n.*?\n---\s*\n', '', article_content, count=1, flags=re.DOTALL)

    full_content = f"{front_matter}\n\n{article_content}\n"

    with open(output_file, mode="w", encoding="utf-8") as f:
        f.write(full_content)

    logger.info("記事を保存しました: %s", output_file)
    return output_file


# ==============================================================================
# コンソールサマリー出力
# ==============================================================================

def print_summary(keyword: str, article_file: Path, word_count: int, affiliate_links_used: list[dict]) -> None:
    print("\n" + "=" * 60)
    print("  記事生成完了 — SIM比較オンライン")
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
    logger.info("記事生成パイプライン開始 (sim-hikaku.online)")

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
    max_tokens: int = claude_settings.get("max_tokens", 8192)

    article_settings = settings.get("article", {})
    min_words: int = article_settings.get("min_words", 3000)
    max_words: int = article_settings.get("max_words", 5000)
    max_affiliate_links: int = article_settings.get("max_affiliate_links", 5)

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

    # --- アフィリエイトリンクの選択 ---
    selected_affiliate_links = select_relevant_affiliate_links(
        keyword, affiliate_data, max_links=max_affiliate_links
    )

    # --- プロンプト構築 ---
    system_prompt = build_system_prompt()
    user_prompt = build_user_prompt(
        keyword=keyword,
        affiliate_links=selected_affiliate_links,
        min_words=min_words,
        max_words=max_words,
    )

    # --- Claude API 呼び出し ---
    try:
        client = anthropic.Anthropic(api_key=api_key, timeout=600.0)
        generated_article = call_claude_api(
            client=client,
            model=model,
            max_tokens=max_tokens,
            system_prompt=system_prompt,
            user_prompt=user_prompt,
        )
    except anthropic.AuthenticationError:
        logger.error("Claude API 認証エラー。config/secrets.json の api_key を確認してください。")
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
