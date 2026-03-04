#!/usr/bin/env python3
"""
コンテンツカレンダー自動生成スクリプト

キーワード調査結果から4週間分のコンテンツカレンダーを生成する。
"""

import json
import logging
import sys
from datetime import datetime, timedelta
from pathlib import Path

# ログ設定
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# プロジェクトルート
PROJECT_ROOT = Path(__file__).parent.parent
CONFIG_PATH = PROJECT_ROOT / "config" / "settings.json"
CALENDAR_PATH = PROJECT_ROOT / "config" / "content-calendar.json"
KEYWORDS_DIR = PROJECT_ROOT / "inputs" / "keywords"
WP_LOG_PATH = PROJECT_ROOT / "published" / "wordpress-log.json"

# 記事タイプの分布
ARTICLE_TYPES = [
    {"type": "how-to", "label": "ハウツー", "ratio": 0.4},
    {"type": "comparison", "label": "比較", "ratio": 0.3},
    {"type": "listicle", "label": "まとめ", "ratio": 0.2},
    {"type": "news", "label": "最新情報", "ratio": 0.1},
]

# 投稿曜日（火・木・土）
PUBLISH_DAYS = [1, 3, 5]  # 0=月, 1=火, ..., 5=土


def load_latest_keywords():
    """最新のキーワードキューを読み込む"""
    if not KEYWORDS_DIR.exists():
        return []

    queue_files = sorted(KEYWORDS_DIR.glob("queue-*.json"), reverse=True)
    if not queue_files:
        return []

    latest = queue_files[0]
    logger.info(f"キーワードファイル読み込み: {latest.name}")

    with open(latest, "r", encoding="utf-8") as f:
        return json.load(f)


def load_published_keywords():
    """公開済み記事のキーワードを取得する"""
    if not WP_LOG_PATH.exists():
        return set()

    with open(WP_LOG_PATH, "r", encoding="utf-8") as f:
        log = json.load(f)

    return {post.get("keyword", "").lower() for post in log.get("posts", [])}


def assign_article_types(keywords):
    """キーワードに記事タイプを割り当てる"""
    total = len(keywords)
    assigned = []

    # 比率に基づいてタイプを割り当て
    type_index = 0
    type_counts = {}
    for at in ARTICLE_TYPES:
        type_counts[at["type"]] = max(1, int(total * at["ratio"]))

    for i, kw in enumerate(keywords):
        # タイプを順番に割り当て
        current_type = ARTICLE_TYPES[type_index % len(ARTICLE_TYPES)]
        while type_counts.get(current_type["type"], 0) <= 0:
            type_index += 1
            current_type = ARTICLE_TYPES[type_index % len(ARTICLE_TYPES)]

        kw["article_type"] = current_type["type"]
        kw["article_type_label"] = current_type["label"]
        type_counts[current_type["type"]] -= 1
        assigned.append(kw)
        type_index += 1

    return assigned


def generate_calendar(keywords, weeks=4, articles_per_week=3):
    """4週間分のコンテンツカレンダーを生成する"""
    today = datetime.now()
    # 次の月曜日を起点にする
    days_until_monday = (7 - today.weekday()) % 7
    if days_until_monday == 0:
        days_until_monday = 7
    start_date = today + timedelta(days=days_until_monday)

    calendar_weeks = []
    kw_index = 0

    for week_num in range(weeks):
        week_start = start_date + timedelta(weeks=week_num)
        week_articles = []

        for day_offset in PUBLISH_DAYS:
            if kw_index >= len(keywords):
                break

            publish_date = week_start + timedelta(days=day_offset)
            kw = keywords[kw_index]

            week_articles.append({
                "date": publish_date.strftime("%Y-%m-%d"),
                "day_name": ["月", "火", "水", "木", "金", "土", "日"][publish_date.weekday()],
                "keyword": kw.get("keyword", "未定"),
                "article_type": kw.get("article_type", "how-to"),
                "article_type_label": kw.get("article_type_label", "ハウツー"),
                "priority": kw.get("priority", kw_index + 1),
                "status": "planned"
            })
            kw_index += 1

        calendar_weeks.append({
            "week": week_num + 1,
            "start_date": week_start.strftime("%Y-%m-%d"),
            "end_date": (week_start + timedelta(days=6)).strftime("%Y-%m-%d"),
            "articles": week_articles
        })

    return calendar_weeks


def print_calendar(calendar_weeks):
    """カレンダーをテーブル形式で表示する"""
    print("\n" + "=" * 80)
    print("コンテンツカレンダー")
    print("=" * 80)

    for week in calendar_weeks:
        print(f"\n--- Week {week['week']} ({week['start_date']} 〜 {week['end_date']}) ---")
        print(f"{'日付':<14} {'曜日':<4} {'タイプ':<10} {'キーワード'}")
        print("-" * 60)

        for article in week["articles"]:
            print(f"{article['date']:<14} {article['day_name']:<4} "
                  f"{article['article_type_label']:<10} {article['keyword']}")

    total = sum(len(w["articles"]) for w in calendar_weeks)
    print(f"\n合計: {total}記事（{len(calendar_weeks)}週間）")


def main():
    """メイン処理"""
    logger.info("=== コンテンツカレンダー生成開始 ===")

    # キーワード読み込み
    keywords = load_latest_keywords()

    if not keywords:
        logger.warning("キーワードが見つかりません。先に keyword_research.py を実行してください。")
        # シードキーワードから仮のカレンダーを生成
        if CALENDAR_PATH.exists():
            with open(CALENDAR_PATH, "r", encoding="utf-8") as f:
                cal_data = json.load(f)
            seeds = cal_data.get("seed_keywords", [])
            keywords = [{"keyword": kw, "priority": i + 1} for i, kw in enumerate(seeds)]
        else:
            logger.error("シードキーワードも見つかりません。")
            sys.exit(1)

    # 公開済みキーワードを除外
    published = load_published_keywords()
    keywords = [kw for kw in keywords if kw.get("keyword", "").lower() not in published]

    logger.info(f"利用可能キーワード: {len(keywords)}件")

    # 記事タイプを割り当て
    keywords = assign_article_types(keywords[:12])  # 4週×3記事=12記事分

    # カレンダー生成
    calendar_weeks = generate_calendar(keywords)

    # content-calendar.json を更新
    if CALENDAR_PATH.exists():
        with open(CALENDAR_PATH, "r", encoding="utf-8") as f:
            calendar_data = json.load(f)
    else:
        calendar_data = {}

    calendar_data["meta"] = {
        "generated_at": datetime.now().isoformat(),
        "period": f"{calendar_weeks[0]['start_date']} to {calendar_weeks[-1]['end_date']}",
        "articles_per_week": 3
    }
    calendar_data["weekly_schedule"] = calendar_weeks

    with open(CALENDAR_PATH, "w", encoding="utf-8") as f:
        json.dump(calendar_data, f, ensure_ascii=False, indent=2)

    logger.info(f"カレンダー保存先: {CALENDAR_PATH}")

    # テーブル表示
    print_calendar(calendar_weeks)

    logger.info("=== コンテンツカレンダー生成完了 ===")


if __name__ == "__main__":
    main()
