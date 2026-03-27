"""
Keyword Research — Apify Actor
================================
Accepts a list of seed keywords, expands each via Google Suggest
autocomplete (+ Japanese question-pattern variants), scores every
candidate keyword for longtail / question potential, and pushes the
top-N results to the Apify dataset.

Input fields (see .actor/input_schema.json):
  keywords             - list[str]  seed keywords (required)
  language             - str        Google Suggest hl param (default "ja")
  topN                 - int        number of results to output (default 20)
  requestDelaySeconds  - float      delay between HTTP requests (default 1.0)
  maxQuestionPatterns  - int        question-suffix variants per seed (default 4)
"""

from __future__ import annotations

import asyncio
import json
import logging
import re
import time
import urllib.error
import urllib.parse
import urllib.request

from apify import Actor

# ---------------------------------------------------------------------------
# Logging
# ---------------------------------------------------------------------------
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

# Japanese question / informational suffixes used to expand seed keywords
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

# High-value terms that get a scoring bonus
HIGH_VALUE_TERMS = ["稼ぐ", "副業", "収入", "収益", "稼げる", "おすすめ", "始め方", "やり方"]

GOOGLE_SUGGEST_URL = (
    "http://suggestqueries.google.com/complete/search"
    "?client=firefox&hl={lang}&q={query}"
)

DEFAULT_USER_AGENT = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
    "AppleWebKit/537.36 (KHTML, like Gecko) "
    "Chrome/120.0.0.0 Safari/537.36"
)

# ---------------------------------------------------------------------------
# Google Suggest helpers
# ---------------------------------------------------------------------------


MAX_RETRIES = 2
RETRY_DELAY_S = 2.0
FETCH_TIMEOUT_S = 15


def fetch_google_suggestions(keyword: str, language: str = "ja") -> list[str]:
    """Call Google Suggest and return a list of suggestion strings with retry."""
    encoded_query = urllib.parse.quote(keyword)
    url = GOOGLE_SUGGEST_URL.format(lang=language, query=encoded_query)

    for attempt in range(MAX_RETRIES + 1):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": DEFAULT_USER_AGENT})
            with urllib.request.urlopen(req, timeout=FETCH_TIMEOUT_S) as response:
                raw = response.read().decode("utf-8")

            # Firefox client returns: [query, [suggestion1, suggestion2, ...], ...]
            data = json.loads(raw)
            suggestions: list[str] = data[1] if len(data) > 1 else []
            logger.debug("Suggest '%s' → %d results", keyword, len(suggestions))
            return suggestions

        except urllib.error.URLError as exc:
            logger.warning("URLError for '%s' (attempt %d/%d): %s", keyword, attempt + 1, MAX_RETRIES + 1, exc)
            if attempt < MAX_RETRIES:
                time.sleep(RETRY_DELAY_S)
            else:
                return []
        except (json.JSONDecodeError, IndexError) as exc:
            logger.warning("Parse error for '%s': %s", keyword, exc)
            return []
        except Exception as exc:  # noqa: BLE001
            logger.warning("Unexpected error for '%s' (attempt %d/%d): %s", keyword, attempt + 1, MAX_RETRIES + 1, exc)
            if attempt < MAX_RETRIES:
                time.sleep(RETRY_DELAY_S)
            else:
                return []

    return []


def generate_question_patterns(seed: str, max_patterns: int = 4) -> list[str]:
    """Return seed + Japanese question suffixes (up to max_patterns)."""
    return [f"{seed}{suffix}" for suffix in QUESTION_SUFFIXES[:max_patterns]]


# ---------------------------------------------------------------------------
# Keyword normalisation & validation
# ---------------------------------------------------------------------------


def normalize_keyword(keyword: str) -> str:
    kw = keyword.replace("\u3000", " ")   # full-width space → half-width
    kw = re.sub(r"\s+", " ", kw)
    return kw.strip()


def is_valid_keyword(keyword: str) -> bool:
    if not keyword or len(keyword) < 2 or len(keyword) > 50:
        return False
    if keyword.isdigit():
        return False
    return True


# ---------------------------------------------------------------------------
# Scoring & classification
# ---------------------------------------------------------------------------


def classify_keyword(keyword: str) -> str:
    """Return 'question' | 'longtail' | 'main'."""
    for suffix in QUESTION_SUFFIXES:
        if keyword.endswith(suffix.strip()):
            return "question"

    word_count = len(keyword.split())
    char_count = len(keyword.replace(" ", ""))
    if word_count >= 3 or char_count >= 10:
        return "longtail"

    return "main"


def score_keyword(keyword: str) -> float:
    """Higher score = higher priority. Favours longtail & question keywords."""
    kw_type = classify_keyword(keyword)

    score = {"longtail": 30.0, "question": 20.0, "main": 10.0}.get(kw_type, 10.0)

    # Word-count bonus (capped)
    score += min(len(keyword.split()) * 5.0, 20.0)

    # Optimal character-count bonus
    char_count = len(keyword.replace(" ", ""))
    if 8 <= char_count <= 25:
        score += 10.0
    elif char_count > 25:
        score -= 5.0

    # High-value term bonus (once only)
    if any(term in keyword for term in HIGH_VALUE_TERMS):
        score += 5.0

    return score


# ---------------------------------------------------------------------------
# Core research logic (synchronous, called inside the async wrapper)
# ---------------------------------------------------------------------------


def collect_candidates(
    seed_keywords: list[str],
    language: str = "ja",
    request_delay: float = 1.0,
    max_question_patterns: int = 4,
) -> list[dict]:
    """
    For every seed keyword:
      1. Fetch Google Suggest suggestions for the seed itself.
      2. Generate question-pattern variants and fetch suggestions for each.
      3. Normalise, validate, deduplicate, score every candidate.

    Returns a list of dicts: {keyword, type, score, source_seed}
    """
    all_candidates: list[dict] = []
    seen: set[str] = set()
    total = len(seed_keywords)

    logger.info("Starting keyword research for %d seed keyword(s)", total)

    for idx, seed in enumerate(seed_keywords, start=1):
        logger.info("[%d/%d] Processing seed: '%s'", idx, total, seed)

        suggestions: list[str] = []

        # Seed-level suggestions
        suggestions.extend(fetch_google_suggestions(seed, language))
        time.sleep(request_delay)

        # Question-pattern suggestions
        for pattern in generate_question_patterns(seed, max_question_patterns):
            suggestions.extend(fetch_google_suggestions(pattern, language))
            time.sleep(request_delay)

        # Include seed and its question patterns as direct candidates
        suggestions.append(seed)
        suggestions.extend(generate_question_patterns(seed, max_question_patterns))

        added = 0
        for raw in suggestions:
            normalized = normalize_keyword(raw)
            if not is_valid_keyword(normalized):
                continue
            key = normalized.lower()
            if key in seen:
                continue
            seen.add(key)

            all_candidates.append(
                {
                    "keyword": normalized,
                    "type": classify_keyword(normalized),
                    "score": score_keyword(normalized),
                    "source_seed": seed,
                }
            )
            added += 1

        logger.info("  → added %d new candidates (total so far: %d)", added, len(all_candidates))

    logger.info("Candidate collection complete. Total: %d", len(all_candidates))
    return all_candidates


def select_top_keywords(candidates: list[dict], top_n: int = 20) -> list[dict]:
    """Sort by score desc (ties broken by shorter keyword) and return top_n."""
    sorted_candidates = sorted(
        candidates,
        key=lambda x: (x["score"], -len(x["keyword"])),
        reverse=True,
    )

    results = []
    for rank, item in enumerate(sorted_candidates[:top_n], start=1):
        results.append(
            {
                "priority": rank,
                "keyword": item["keyword"],
                "type": item["type"],
                "score": item["score"],
                "source_seed": item["source_seed"],
                "status": "pending",
            }
        )
    return results


# ---------------------------------------------------------------------------
# Apify Actor entry point
# ---------------------------------------------------------------------------


async def main() -> None:
    async with Actor:
        # --- Read input ---
        input_data: dict = await Actor.get_input() or {}

        seed_keywords: list[str] = input_data.get("keywords", [])
        if not seed_keywords:
            Actor.log.error("No seed keywords provided. Aborting.")
            await Actor.fail(status_message="Input 'keywords' must be a non-empty list.")
            return

        language: str = input_data.get("language", "ja")
        top_n: int = int(input_data.get("topN", 20))
        request_delay: float = float(input_data.get("requestDelaySeconds", 1.0))
        max_question_patterns: int = int(input_data.get("maxQuestionPatterns", 4))

        Actor.log.info(
            "Input: %d seed keyword(s), lang=%s, topN=%d, delay=%.1fs, questionPatterns=%d",
            len(seed_keywords),
            language,
            top_n,
            request_delay,
            max_question_patterns,
        )

        # --- Run research (blocking I/O — run in thread to keep event loop free) ---
        candidates = await asyncio.get_event_loop().run_in_executor(
            None,
            lambda: collect_candidates(
                seed_keywords,
                language=language,
                request_delay=request_delay,
                max_question_patterns=max_question_patterns,
            ),
        )

        if not candidates:
            Actor.log.warning("No keyword candidates collected. Dataset will be empty.")
            return

        # --- Select top keywords ---
        top_keywords = select_top_keywords(candidates, top_n=top_n)
        Actor.log.info("Selected top %d keyword(s)", len(top_keywords))

        # --- Push to dataset ---
        await Actor.push_data(top_keywords)

        # --- Log summary ---
        type_counts: dict[str, int] = {}
        for kw in top_keywords:
            t = kw["type"]
            type_counts[t] = type_counts.get(t, 0) + 1

        Actor.log.info("Done. Breakdown by type: %s", type_counts)
        Actor.log.info(
            "Top 5 keywords: %s",
            [kw["keyword"] for kw in top_keywords[:5]],
        )


if __name__ == "__main__":
    asyncio.run(main())
