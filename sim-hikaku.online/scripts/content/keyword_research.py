"""
keyword_research.py
====================
自動キーワードリサーチパイプライン
SIM比較オンライン (sim-hikaku.online) 版。

機能:
- content-calendar.json からシードキーワードを読み込む
- Google Suggest API を使って関連キーワードを取得する
- 日本語の質問パターンでキーワードを拡張する
- 長尾キーワードを優先してスコアリングする
- 重複排除・公開済みフィルタリングを行う
- 上位20件を inputs/keywords/queue-YYYY-MM-DD.json に出力する
"""

import io
import json
import logging
import re
import sys
import time
import urllib.parse
import urllib.request
from datetime import date
from pathlib import Path

# Windows UTF-8 出力修正
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding="utf-8", errors="replace")

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
PUBLISHED_LOG = BASE_DIR / "published" / "wordpress-log.json"

CONTENT_CALENDAR_FILE = CONFIG_DIR / "content-calendar.json"

# Google Suggest API エンドポイント
GOOGLE_SUGGEST_URL = (
    "http://suggestqueries.google.com/complete/search"
    "?client=firefox&hl=ja&q={query}"
)

# 日本語の質問・情報系サフィックスパターン
QUESTION_SUFFIXES = [
    " とは",
    " おすすめ",
    " 比較",
    " 料金",
    " 速度",
    " 評判",
    " デメリット",
    " メリット",
    " 乗り換え",
    " キャンペーン",
    " 方法",
    " 設定",
]

REQUEST_DELAY_SECONDS = 1.0
TOP_N = 20


# ==============================================================================
# Google Suggest API 呼び出し
# ==============================================================================

def fetch_google_suggestions(keyword: str) -> list[str]:
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
    patterns = []
    for suffix in QUESTION_SUFFIXES:
        pattern = f"{seed_keyword}{suffix}"
        patterns.append(pattern)
    return patterns


# ==============================================================================
# キーワードスコアリング
# ==============================================================================

def classify_keyword(keyword: str) -> str:
    for suffix in QUESTION_SUFFIXES:
        if keyword.endswith(suffix.strip()):
            return "question"

    word_count = len(keyword.split())
    char_count = len(keyword.replace(" ", ""))
    if word_count >= 3 or char_count >= 10:
        return "longtail"

    return "main"


def score_keyword(keyword: str) -> float:
    score = 0.0
    kw_type = classify_keyword(keyword)

    if kw_type == "longtail":
        score += 30.0
    elif kw_type == "question":
        score += 20.0
    else:
        score += 10.0

    word_count = len(keyword.split())
    score += min(word_count * 5.0, 20.0)

    char_count = len(keyword.replace(" ", ""))
    if 8 <= char_count <= 25:
        score += 10.0
    elif char_count > 25:
        score -= 5.0

    # 格安SIM関連の高収益キーワードボーナス
    high_value_terms = ["おすすめ", "比較", "料金", "乗り換え", "キャンペーン", "速度", "評判", "最安"]
    for term in high_value_terms:
        if term in keyword:
            score += 5.0
            break

    return score


# ==============================================================================
# 公開済みキーワードの読み込み
# ==============================================================================

def load_published_keywords() -> set[str]:
    if not PUBLISHED_LOG.exists():
        logger.info("公開済みログが見つかりません。新規スタートとして処理します: %s", PUBLISHED_LOG)
        return set()

    try:
        with open(PUBLISHED_LOG, encoding="utf-8") as f:
            log_data: list[dict] = json.load(f)

        published = set()
        for entry in log_data:
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
    if not CONTENT_CALENDAR_FILE.exists():
        raise FileNotFoundError(
            f"コンテンツカレンダーが見つかりません: {CONTENT_CALENDAR_FILE}"
        )

    with open(CONTENT_CALENDAR_FILE, encoding="utf-8") as f:
        calendar: dict = json.load(f)

    seeds: list[str] = calendar.get("seed_keywords", [])
    if not seeds:
        raise ValueError("content-calendar.json に seed_keywords が定義されていません")

    logger.info("シードキーワード %d 件を読み込みました", len(seeds))
    return seeds


# ==============================================================================
# 既存キューファイルから処理済みキーワードを読み込む
# ==============================================================================

def load_already_queued_keywords() -> set[str]:
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
    kw = keyword.replace("\u3000", " ")
    kw = re.sub(r"\s+", " ", kw)
    kw = kw.strip()
    return kw


def is_valid_keyword(keyword: str) -> bool:
    if not keyword:
        return False
    if len(keyword) < 2:
        return False
    if len(keyword) > 50:
        return False
    if keyword.isdigit():
        return False
    return True


# ==============================================================================
# メインのキーワードリサーチ処理
# ==============================================================================

def research_keywords() -> list[dict]:
    seed_keywords = load_seed_keywords()
    published_keywords = load_published_keywords()
    already_queued = load_already_queued_keywords()

    exclude_keywords = published_keywords | already_queued

    all_candidates: list[dict] = []
    seen_normalized: set[str] = set()

    total_seeds = len(seed_keywords)
    logger.info("=" * 60)
    logger.info("キーワードリサーチ開始: シードキーワード %d 件", total_seeds)
    logger.info("=" * 60)

    for idx, seed in enumerate(seed_keywords, start=1):
        logger.info("[%d/%d] シードキーワード処理中: '%s'", idx, total_seeds, seed)

        suggestions = fetch_google_suggestions(seed)
        time.sleep(REQUEST_DELAY_SECONDS)

        question_patterns = generate_question_patterns(seed)
        for pattern in question_patterns[:4]:
            pattern_suggestions = fetch_google_suggestions(pattern)
            suggestions.extend(pattern_suggestions)
            time.sleep(REQUEST_DELAY_SECONDS)

        suggestions.append(seed)
        suggestions.extend(question_patterns)

        for raw_kw in suggestions:
            normalized = normalize_keyword(raw_kw)

            if not is_valid_keyword(normalized):
                continue

            lower_kw = normalized.lower()
            if lower_kw in seen_normalized:
                continue
            seen_normalized.add(lower_kw)

            if normalized in exclude_keywords:
                logger.debug("スキップ (処理済み): '%s'", normalized)
                continue

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
# 上位キーワードの選択と出力
# ==============================================================================

def select_top_keywords(candidates: list[dict], top_n: int = TOP_N) -> list[dict]:
    sorted_candidates = sorted(
        candidates,
        key=lambda x: (x["score"], -len(x["keyword"])),
        reverse=True,
    )

    top = sorted_candidates[:top_n]

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
    INPUTS_KEYWORDS_DIR.mkdir(parents=True, exist_ok=True)

    today_str = date.today().strftime("%Y-%m-%d")
    output_file = INPUTS_KEYWORDS_DIR / f"queue-{today_str}.json"

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
    print("\n" + "=" * 60)
    print("  キーワードリサーチ完了 — SIM比較オンライン")
    print("=" * 60)
    print(f"  出力ファイル : {output_file}")
    print(f"  取得件数     : {len(keywords)} 件")
    print()

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
    logger.info("キーワードリサーチパイプライン開始 (sim-hikaku.online)")

    try:
        candidates = research_keywords()

        if not candidates:
            logger.error("有効なキーワード候補が見つかりませんでした。処理を終了します。")
            return

        top_keywords = select_top_keywords(candidates, top_n=TOP_N)
        logger.info("上位 %d 件のキーワードを選択しました", len(top_keywords))

        output_file = save_keyword_queue(top_keywords)

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
