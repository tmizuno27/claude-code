"""
ブログ公開リマインダー — 公開前日にDiscordで事前通知
Task Scheduler から毎日 PYT 12:00 に発火し、翌日がJST公開日(月/木)なら通知

PYT 12:00 = JST 翌日 00:00 なので、翌日のJST曜日で判定する
"""

import io
import json
import sys
import urllib.request
from datetime import datetime, timedelta, timezone
from pathlib import Path

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

BLOG_DIR = Path(__file__).parent.parent.parent
CONFIG_DIR = BLOG_DIR / "config"
SETTINGS_FILE = CONFIG_DIR / "settings.json"
HOLIDAY_FILE = CONFIG_DIR / "jp-holidays.json"
OUTPUTS_DIR = BLOG_DIR / "outputs"
KW_QUEUE_FILE = BLOG_DIR / "inputs" / "keyword-queue.json"

PUBLISH_DAYS_JST = [0, 3]  # Monday=0, Thursday=3


def get_jst_tomorrow() -> datetime:
    """JST基準で明日の日時を取得（PYT+12h=JST近似）"""
    now_jst = datetime.now() + timedelta(hours=12)
    tomorrow_jst = now_jst + timedelta(days=1)
    return tomorrow_jst


def is_holiday(date_str: str) -> bool:
    """祝日かどうかチェック"""
    if not HOLIDAY_FILE.exists():
        return False
    try:
        with open(HOLIDAY_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
        year = date_str[:4]
        holidays = data.get("holidays", {}).get(year, [])
        return date_str in holidays
    except Exception:
        return False


def get_next_article_info() -> str:
    """次に公開予定の記事情報を取得（キューから）"""
    if not KW_QUEUE_FILE.exists():
        return "（キュー情報なし）"
    try:
        with open(KW_QUEUE_FILE, "r", encoding="utf-8") as f:
            queue = json.load(f)
        if isinstance(queue, list) and queue:
            next_item = queue[0]
            kw = next_item.get("keyword", "不明")
            pillar = next_item.get("pillar", "")
            return f"KW: {kw}" + (f" ({pillar})" if pillar else "")
        return "（キューが空です）"
    except Exception:
        return "（キュー読み込みエラー）"


def get_pending_drafts() -> str:
    """outputs/ 内の未公開ドラフト記事を確認"""
    articles_dir = OUTPUTS_DIR / "articles"
    if not articles_dir.exists():
        return "ドラフト記事なし"
    drafts = list(articles_dir.glob("*.md"))
    if not drafts:
        return "ドラフト記事なし"
    # 最新3件のファイル名を表示
    drafts.sort(key=lambda p: p.stat().st_mtime, reverse=True)
    names = [d.stem for d in drafts[:3]]
    return f"ドラフト{len(drafts)}件: " + ", ".join(names)


def notify_discord(message: str):
    """Discord Webhookで通知"""
    try:
        with open(SETTINGS_FILE, "r", encoding="utf-8") as f:
            settings = json.load(f)
        webhook_url = settings.get("discord", {}).get("webhook_url")
        if not webhook_url:
            print("Discord Webhook URLが設定されていません")
            return
        payload = json.dumps({"content": message}).encode("utf-8")
        req = urllib.request.Request(
            webhook_url,
            data=payload,
            headers={"Content-Type": "application/json", "User-Agent": "BlogReminder/1.0"},
        )
        urllib.request.urlopen(req)
        print("Discord通知を送信しました")
    except Exception as e:
        print(f"WARNING: Discord通知失敗 - {e}")


def main():
    tomorrow_jst = get_jst_tomorrow()
    dow = tomorrow_jst.weekday()  # 0=Monday
    date_str = tomorrow_jst.strftime("%Y-%m-%d")
    dow_ja = ["月", "火", "水", "木", "金", "土", "日"][dow]

    print(f"明日(JST): {date_str} ({dow_ja}曜日)")

    # 公開日でなければ終了
    if dow not in PUBLISH_DAYS_JST:
        print(f"明日は公開日ではありません（{dow_ja}曜日）。終了")
        return

    # 祝日チェック
    if is_holiday(date_str):
        print(f"明日は祝日 ({date_str})。リマインダーをスキップ")
        return

    # 記事情報を収集
    draft_info = get_pending_drafts()
    next_article = get_next_article_info()

    message = (
        f"📅 **明日はブログ公開日です！** ({date_str} {dow_ja}曜日)\n"
        f"━━━━━━━━━━━━━━━\n"
        f"📝 {draft_info}\n"
        f"🔑 次の記事: {next_article}\n"
        f"━━━━━━━━━━━━━━━\n\n"
        f"**やること（15-30分）:**\n"
        f"1. 自動生成された記事ドラフトを確認\n"
        f"2. 体験談・一次情報を追記\n"
        f"3. 翌朝JST 6:00-7:00に自動公開されます\n\n"
        f"※ 記事が問題なければ何もしなくてOK（自動公開）"
    )

    notify_discord(message)
    print("リマインダー送信完了")


if __name__ == "__main__":
    main()
