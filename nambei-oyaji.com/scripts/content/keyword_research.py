"""
keyword_research.py
====================
自動キーワードリサーチパイプライン

機能:
- content-calendar.json からシードキーワードを読み込む
- Google Suggest API を使って関連キーワードを取得する
- 日本語の質問パターンでキーワードを拡張する
- 長尾キーワードを優先してスコアリングする
- 重複排除・公開済みフィルタリングを行う
- 上位20件を inputs/keywords/queue-YYYY-MM-DD.json に出力する
"""

import json
import logging
import re
import time
import urllib.parse
import urllib.request
from datetime import date
from pathlib import Path

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
# パス定数 (プロジェクトルートを基準にする)
# ==============================================================================
BASE_DIR = Path(__file__).resolve().parent.parent.parent
CONFIG_DIR = BASE_DIR / "config"
INPUTS_KEYWORDS_DIR = BASE_DIR / "inputs" / "keywords"
PUBLISHED_LOG = BASE_DIR / "published" / "wordpress-log.json"

CONTENT_CALENDAR_FILE = CONFIG_DIR / "content-calendar.json"

# Google Suggest API エンドポイント (無料・APIキー不要)
GOOGLE_SUGGEST_URL = (
    "http://suggestqueries.google.com/complete/search"
    "?client=firefox&hl=ja&q={query}"
)

# 日本語の質問・情報系サフィックスパターン
QUESTION_SUFFIXES = [
    " とは",
    " 始め方",
    " おすすめ",
    " 稼ぎ方",
    " やり方",
    " メリット",
    " デメリット",
    " 注意点",
    " 比較",
    " 無料",
    " 方法",
    " コツ",
]

# 1リクエストあたりの待機時間（秒） - Google に対して礼儀正しくする
REQUEST_DELAY_SECONDS = 1.0

# 最終出力する上位キーワード数
TOP_N = 20


# ==============================================================================
# Google Suggest API 呼び出し
# ==============================================================================

def fetch_google_suggestions(keyword: str) -> list[str]:
    """
    Google Suggest API からサジェストキーワードを取得する。

    Args:
        keyword: 検索クエリ文字列

    Returns:
        サジェストキーワードのリスト。エラー時は空リスト。
    """
    encoded_query = urllib.parse.quote(keyword)
    url = GOOGLE_SUGGEST_URL.format(query=encoded_query)

    try:
        req = urllib.request.Request(
            url,
            headers={
                "User-Agent": (
                    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                    "AppleWebKit/537.36 (KHTML, like Gecko) "
                    "Chrome/120.0.0.0 Safari/537.36"
                )
            },
        )
        with urllib.request.urlopen(req, timeout=10) as response:
            raw = response.read().decode("utf-8")

        # Firefox クライアントは JSON 配列を返す: [query, [suggestion1, ...], ...]
        data = json.loads(raw)
        suggestions: list[str] = data[1] if len(data) > 1 else []
        logger.debug(
            "Google Suggest: '%s' -> %d 件のサジェスト取得", keyword, len(suggestions)
        )
        return suggestions

    except urllib.error.URLError as e:
        logger.warning("Google Suggest API 接続エラー ('%s'): %s", keyword, e)
        return []
    except (json.JSONDecodeError, IndexError) as e:
        logger.warning("Google Suggest レスポンス解析エラー ('%s'): %s", keyword, e)
        return []
    except Exception as e:
        logger.warning("Google Suggest 予期しないエラー ('%s'): %s", keyword, e)
        return []


# ==============================================================================
# 質問パターン生成
# ==============================================================================

def generate_question_patterns(seed_keyword: str) -> list[str]:
    """
    シードキーワードに日本語の質問サフィックスを付与してキーワードリストを生成する。

    Args:
        seed_keyword: 元になるキーワード

    Returns:
        生成されたキーワードパターンのリスト
    """
    patterns = []
    for suffix in QUESTION_SUFFIXES:
        pattern = f"{seed_keyword}{suffix}"
        patterns.append(pattern)
    return patterns


# ==============================================================================
# キーワードスコアリング
# ==============================================================================

def classify_keyword(keyword: str) -> str:
    """
    キーワードのタイプを判定する。

    Args:
        keyword: 判定対象のキーワード

    Returns:
        "question" | "longtail" | "main"
    """
    # 質問系サフィックスを含むか判定
    for suffix in QUESTION_SUFFIXES:
        if keyword.endswith(suffix.strip()):
            return "question"

    # スペース区切りで3語以上 or 文字数が多い = ロングテール
    word_count = len(keyword.split())
    char_count = len(keyword.replace(" ", ""))
    if word_count >= 3 or char_count >= 10:
        return "longtail"

    return "main"


def score_keyword(keyword: str) -> float:
    """
    キーワードの競合度スコアを計算する（高いほど優先度が高い）。

    スコアリングロジック:
    - ロングテールキーワード (3語以上) に高スコア
    - 質問系キーワードに中スコア
    - メインキーワードに基本スコア
    - キーワードの文字数が適切な範囲にボーナス

    Args:
        keyword: スコアリング対象のキーワード

    Returns:
        スコア値 (float)
    """
    score = 0.0
    kw_type = classify_keyword(keyword)

    if kw_type == "longtail":
        score += 30.0
    elif kw_type == "question":
        score += 20.0
    else:
        score += 10.0

    # 単語数ボーナス (多い方がロングテール)
    word_count = len(keyword.split())
    score += min(word_count * 5.0, 20.0)

    # 適切な文字数ボーナス (8〜25文字が狙い目)
    char_count = len(keyword.replace(" ", ""))
    if 8 <= char_count <= 25:
        score += 10.0
    elif char_count > 25:
        score -= 5.0  # 長すぎるキーワードは検索されにくい

    # 副業・AI・稼ぐ など収益性の高いキーワードを含む場合にボーナス
    high_value_terms = ["稼ぐ", "副業", "収入", "収益", "稼げる", "おすすめ", "始め方", "やり方"]
    for term in high_value_terms:
        if term in keyword:
            score += 5.0
            break  # 1回だけボーナス

    return score


# ==============================================================================
# 公開済みキーワードの読み込み
# ==============================================================================

def load_published_keywords() -> set[str]:
    """
    wordpress-log.json から公開済み記事のキーワードを読み込む。

    Returns:
        公開済みキーワードの集合。ファイルが存在しない場合は空集合。
    """
    if not PUBLISHED_LOG.exists():
        logger.info("公開済みログが見つかりません。新規スタートとして処理します: %s", PUBLISHED_LOG)
        return set()

    try:
        with open(PUBLISHED_LOG, encoding="utf-8") as f:
            raw_data = json.load(f)

        # Support both list format and dict with "posts" key
        if isinstance(raw_data, dict):
            log_data: list[dict] = raw_data.get("posts", [])
        else:
            log_data = raw_data

        published = set()
        for entry in log_data:
            if not isinstance(entry, dict):
                continue
            kw = entry.get("keyword", "").strip()
            if kw:
                published.add(kw)

        logger.info("公開済みキーワード %d 件を読み込みました", len(published))
        return published

    except (json.JSONDecodeError, ValueError) as e:
        logger.warning("公開済みログの解析に失敗しました: %s", e)
        return set()


# ==============================================================================
# シードキーワードの読み込み
# ==============================================================================

def load_seed_keywords() -> list[str]:
    """
    content-calendar.json からシードキーワードを読み込む。

    Returns:
        シードキーワードのリスト

    Raises:
        FileNotFoundError: 設定ファイルが存在しない場合
        ValueError: JSONフォーマットが不正な場合
    """
    if not CONTENT_CALENDAR_FILE.exists():
        raise FileNotFoundError(
            f"コンテンツカレンダーが見つかりません: {CONTENT_CALENDAR_FILE}"
        )

    with open(CONTENT_CALENDAR_FILE, encoding="utf-8") as f:
        calendar: dict = json.load(f)

    seeds: list[str] = calendar.get("seed_keywords", [])

    # content_pillars 内の seed_keywords も収集する
    if not seeds:
        pillars = calendar.get("content_pillars", {})
        for pillar_data in pillars.values():
            if isinstance(pillar_data, dict):
                pillar_seeds = pillar_data.get("seed_keywords", [])
                seeds.extend(pillar_seeds)

    if not seeds:
        raise ValueError("content-calendar.json に seed_keywords が定義されていません")

    logger.info("シードキーワード %d 件を読み込みました", len(seeds))
    return seeds


# ==============================================================================
# 既存のキューファイルから処理済みキーワードを読み込む
# ==============================================================================

def load_already_queued_keywords() -> set[str]:
    """
    inputs/keywords/ 配下の既存キューファイルに含まれるキーワードを収集する。
    同じキーワードを重複してキューに入れないようにするため。

    Returns:
        既存のキューに含まれるキーワードの集合
    """
    queued: set[str] = set()
    if not INPUTS_KEYWORDS_DIR.exists():
        return queued

    for queue_file in INPUTS_KEYWORDS_DIR.glob("queue-*.json"):
        try:
            with open(queue_file, encoding="utf-8") as f:
                entries: list[dict] = json.load(f)
            for entry in entries:
                kw = entry.get("keyword", "").strip()
                if kw:
                    queued.add(kw)
        except (json.JSONDecodeError, OSError) as e:
            logger.warning("キューファイルの読み込みエラー (%s): %s", queue_file.name, e)

    logger.info("既存キュー内キーワード %d 件を確認しました", len(queued))
    return queued


# ==============================================================================
# キーワード正規化・クリーニング
# ==============================================================================

def normalize_keyword(keyword: str) -> str:
    """
    キーワードを正規化する（空白の統一、前後トリムなど）。

    Args:
        keyword: 正規化前のキーワード

    Returns:
        正規化済みキーワード
    """
    # 全角スペースを半角に統一
    kw = keyword.replace("\u3000", " ")
    # 連続スペースを1つに
    kw = re.sub(r"\s+", " ", kw)
    # 前後の空白を除去
    kw = kw.strip()
    return kw


def is_valid_keyword(keyword: str) -> bool:
    """
    キーワードとして有効かチェックする。

    Args:
        keyword: チェック対象のキーワード

    Returns:
        有効な場合 True、無効な場合 False
    """
    if not keyword:
        return False
    # 2文字未満は除外
    if len(keyword) < 2:
        return False
    # 50文字超えは除外 (実用的でない)
    if len(keyword) > 50:
        return False
    # 数字のみは除外
    if keyword.isdigit():
        return False
    return True


# ==============================================================================
# メインのキーワードリサーチ処理
# ==============================================================================

def research_keywords() -> list[dict]:
    """
    全シードキーワードに対してキーワードリサーチを実行し、
    スコアリング・フィルタリング済みのキーワードリストを返す。

    Returns:
        スコアリング済みキーワード辞書のリスト
        形式: [{"keyword": str, "type": str, "score": float, "source_seed": str}]
    """
    # --- データ読み込み ---
    seed_keywords = load_seed_keywords()
    published_keywords = load_published_keywords()
    already_queued = load_already_queued_keywords()

    # 除外対象キーワード集合 (公開済み + 既存キュー済み)
    exclude_keywords = published_keywords | already_queued

    all_candidates: list[dict] = []
    seen_normalized: set[str] = set()  # 重複排除用

    total_seeds = len(seed_keywords)
    logger.info("=" * 60)
    logger.info("キーワードリサーチ開始: シードキーワード %d 件", total_seeds)
    logger.info("=" * 60)

    for idx, seed in enumerate(seed_keywords, start=1):
        logger.info("[%d/%d] シードキーワード処理中: '%s'", idx, total_seeds, seed)

        # 1. Google Suggest API でサジェスト取得
        suggestions = fetch_google_suggestions(seed)
        time.sleep(REQUEST_DELAY_SECONDS)

        # 2. 質問パターンの生成 + 各パターンのサジェスト取得
        question_patterns = generate_question_patterns(seed)
        for pattern in question_patterns[:4]:  # リクエスト数を抑える (最初の4パターン)
            pattern_suggestions = fetch_google_suggestions(pattern)
            suggestions.extend(pattern_suggestions)
            time.sleep(REQUEST_DELAY_SECONDS)

        # シードキーワード自体と質問パターンも候補に加える
        suggestions.append(seed)
        suggestions.extend(question_patterns)

        # 3. 各サジェストを処理
        for raw_kw in suggestions:
            normalized = normalize_keyword(raw_kw)

            # バリデーション
            if not is_valid_keyword(normalized):
                continue

            # 重複チェック
            lower_kw = normalized.lower()
            if lower_kw in seen_normalized:
                continue
            seen_normalized.add(lower_kw)

            # 公開済み・既存キュー済みキーワードをフィルタリング
            if normalized in exclude_keywords:
                logger.debug("スキップ (処理済み): '%s'", normalized)
                continue

            # スコアリング
            kw_score = score_keyword(normalized)
            kw_type = classify_keyword(normalized)

            all_candidates.append(
                {
                    "keyword": normalized,
                    "type": kw_type,
                    "score": kw_score,
                    "source_seed": seed,
                }
            )

        logger.info(
            "  -> 現在の候補数: %d 件 (今回追加: %d 件)",
            len(all_candidates),
            len(suggestions),
        )

    logger.info("全シードキーワード処理完了。候補総数: %d 件", len(all_candidates))
    return all_candidates


# ==============================================================================
# 上位キーワードの選択と出力形式への変換
# ==============================================================================

def select_top_keywords(candidates: list[dict], top_n: int = TOP_N) -> list[dict]:
    """
    候補キーワードをスコア降順にソートして上位 N 件を選択し、
    出力形式に変換する。

    Args:
        candidates: スコアリング済みキーワード候補リスト
        top_n: 選択する上位件数

    Returns:
        出力形式のキーワードリスト
        形式: [{"keyword": str, "type": str, "priority": int}]
    """
    # スコア降順でソート (同スコアは文字数が少ない方を優先)
    sorted_candidates = sorted(
        candidates,
        key=lambda x: (x["score"], -len(x["keyword"])),
        reverse=True,
    )

    top = sorted_candidates[:top_n]

    # 出力形式に変換 (priority は 1 が最高優先度)
    output_keywords = []
    for rank, item in enumerate(top, start=1):
        output_keywords.append(
            {
                "keyword": item["keyword"],
                "type": item["type"],
                "priority": rank,
                "status": "pending",
            }
        )

    return output_keywords


# ==============================================================================
# キューファイルへの保存
# ==============================================================================

def save_keyword_queue(keywords: list[dict]) -> Path:
    """
    キーワードリストを日付付きキューファイルに保存する。

    Args:
        keywords: 保存するキーワードリスト

    Returns:
        保存したファイルのパス

    Raises:
        OSError: ファイル書き込みに失敗した場合
    """
    # 出力ディレクトリを作成
    INPUTS_KEYWORDS_DIR.mkdir(parents=True, exist_ok=True)

    today_str = date.today().strftime("%Y-%m-%d")
    output_file = INPUTS_KEYWORDS_DIR / f"queue-{today_str}.json"

    # 既に同日のファイルが存在する場合は上書き確認のログを出す
    if output_file.exists():
        logger.warning("同日のキューファイルが既に存在します。上書きします: %s", output_file.name)

    with open(output_file, mode="w", encoding="utf-8") as f:
        json.dump(keywords, f, ensure_ascii=False, indent=2)

    logger.info("キューファイルを保存しました: %s", output_file)
    return output_file


# ==============================================================================
# コンソールサマリー出力
# ==============================================================================

def print_summary(output_file: Path, keywords: list[dict]) -> None:
    """
    処理結果のサマリーをコンソールに出力する。

    Args:
        output_file: 保存したキューファイルのパス
        keywords: 保存したキーワードリスト
    """
    print("\n" + "=" * 60)
    print("  キーワードリサーチ完了")
    print("=" * 60)
    print(f"  出力ファイル : {output_file}")
    print(f"  取得件数     : {len(keywords)} 件")
    print()

    # タイプ別集計
    type_counts: dict[str, int] = {}
    for kw in keywords:
        t = kw.get("type", "unknown")
        type_counts[t] = type_counts.get(t, 0) + 1

    print("  タイプ別内訳:")
    for kw_type, count in sorted(type_counts.items()):
        print(f"    {kw_type:12s} : {count} 件")

    print()
    print("  上位10キーワード:")
    for kw in keywords[:10]:
        priority = kw.get("priority", "-")
        keyword = kw.get("keyword", "")
        kw_type = kw.get("type", "")
        print(f"    [{priority:2}] ({kw_type:10s}) {keyword}")

    print()
    print("  次のステップ: article_generator.py を実行して記事を生成してください")
    print("=" * 60 + "\n")


# ==============================================================================
# エントリーポイント
# ==============================================================================

def main() -> None:
    """
    キーワードリサーチのメイン処理。

    1. シードキーワードを読み込む
    2. Google Suggest + 質問パターンでキーワードを収集する
    3. スコアリング・フィルタリングを行う
    4. 上位20件をキューファイルに保存する
    """
    logger.info("キーワードリサーチパイプライン開始")

    try:
        # キーワードリサーチ実行
        candidates = research_keywords()

        if not candidates:
            logger.error("有効なキーワード候補が見つかりませんでした。処理を終了します。")
            return

        # 上位キーワードを選択
        top_keywords = select_top_keywords(candidates, top_n=TOP_N)
        logger.info("上位 %d 件のキーワードを選択しました", len(top_keywords))

        # キューファイルに保存
        output_file = save_keyword_queue(top_keywords)

        # サマリー出力
        print_summary(output_file, top_keywords)

    except FileNotFoundError as e:
        logger.error("設定ファイルが見つかりません: %s", e)
        raise
    except ValueError as e:
        logger.error("設定ファイルの内容が不正です: %s", e)
        raise
    except KeyboardInterrupt:
        logger.info("ユーザーによって処理が中断されました")
    except Exception as e:
        logger.exception("予期しないエラーが発生しました: %s", e)
        raise


if __name__ == "__main__":
    main()
