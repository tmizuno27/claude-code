"""
ブログ公開リマインダー — 公開前日にDiscordで既存ドラフト記事の確認通知
Task Scheduler から毎日 PYT 12:00 に発火

フロー:
  1. 翌日がJST公開日(月/木)か判定
  2. WordPress REST API でドラフト記事を取得
  3. Discord に記事タイトル + プレビューリンク + 編集リンクを送信
  4. オーナーがスマホから記事を確認・編集（WPアプリ or ブラウザ）
  5. 翌朝 blog-auto-publish.ps1 が自動公開
"""

import base64
import io
import json
import sys
import urllib.request
from datetime import datetime, timedelta
from pathlib import Path

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

BLOG_DIR = Path(__file__).parent.parent.parent
CONFIG_DIR = BLOG_DIR / "config"
SETTINGS_FILE = CONFIG_DIR / "settings.json"
SECRETS_FILE = CONFIG_DIR / "secrets.json"
HOLIDAY_FILE = CONFIG_DIR / "jp-holidays.json"

PUBLISH_DAYS_JST = [0, 3]  # Monday=0, Thursday=3


def get_jst_tomorrow() -> datetime:
    """JST基準で明日の日時を取得（PYT+12h=JST近似）"""
    now_jst = datetime.now() + timedelta(hours=12)
    return now_jst + timedelta(days=1)


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


def load_wp_credentials() -> tuple[str, str, str]:
    """WordPress認証情報を読み込む。(site_url, username, app_password)"""
    with open(SETTINGS_FILE, "r", encoding="utf-8") as f:
        settings = json.load(f)
    site_url = settings.get("wordpress", {}).get("url", "")

    with open(SECRETS_FILE, "r", encoding="utf-8") as f:
        secrets = json.load(f)
    wp = secrets.get("wordpress", {})
    username = wp.get("username", "")
    app_password = wp.get("app_password", "")
    return site_url, username, app_password


def get_wp_drafts() -> list[dict]:
    """WordPress REST API でドラフト記事を取得"""
    try:
        site_url, username, app_password = load_wp_credentials()
        api_url = f"{site_url}/wp-json/wp/v2/posts?status=draft&per_page=10&orderby=modified&order=desc"

        # Basic認証
        credentials = base64.b64encode(f"{username}:{app_password}".encode()).decode()
        req = urllib.request.Request(
            api_url,
            headers={
                "Authorization": f"Basic {credentials}",
                "User-Agent": "BlogReminder/1.0",
            },
        )
        with urllib.request.urlopen(req, timeout=30) as response:
            posts = json.loads(response.read().decode("utf-8"))

        drafts = []
        for post in posts:
            drafts.append({
                "id": post["id"],
                "title": post["title"]["rendered"] or "(無題)",
                "modified": post["modified"],
                "link": post.get("link", ""),
            })
        return drafts
    except Exception as e:
        print(f"WARNING: WordPress API エラー - {e}")
        return []


def get_wp_published_recent() -> list[dict]:
    """最近公開された記事を取得（確認用）"""
    try:
        site_url, username, app_password = load_wp_credentials()
        api_url = f"{site_url}/wp-json/wp/v2/posts?status=publish&per_page=3&orderby=date&order=desc"

        credentials = base64.b64encode(f"{username}:{app_password}".encode()).decode()
        req = urllib.request.Request(
            api_url,
            headers={
                "Authorization": f"Basic {credentials}",
                "User-Agent": "BlogReminder/1.0",
            },
        )
        with urllib.request.urlopen(req, timeout=30) as response:
            posts = json.loads(response.read().decode("utf-8"))

        return [{"id": p["id"], "title": p["title"]["rendered"]} for p in posts]
    except Exception:
        return []


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
        print(f"明日は祝日 ({date_str})。スキップ")
        return

    # WordPress からドラフト記事を取得
    site_url = ""
    try:
        with open(SETTINGS_FILE, "r", encoding="utf-8") as f:
            site_url = json.load(f).get("wordpress", {}).get("url", "")
    except Exception:
        pass

    drafts = get_wp_drafts()
    print(f"ドラフト記事: {len(drafts)}件")

    if drafts:
        # ドラフト記事がある場合 → 各記事のリンクを送信
        draft_lines = ""
        for i, d in enumerate(drafts[:5], 1):
            title = d["title"]
            wp_id = d["id"]
            preview_url = f"{site_url}/?p={wp_id}&preview=true"
            edit_url = f"{site_url}/wp-admin/post.php?post={wp_id}&action=edit"
            draft_lines += (
                f"\n**{i}. {title}**\n"
                f"👀 プレビュー: {preview_url}\n"
                f"✏️ 編集: {edit_url}\n"
            )

        message = (
            f"📅 **明日はブログ公開日！** ({date_str} {dow_ja}曜日)\n"
            f"━━━━━━━━━━━━━━━\n"
            f"📝 公開予定のドラフト記事 ({len(drafts)}件):\n"
            f"{draft_lines}\n"
            f"━━━━━━━━━━━━━━━\n"
            f"**やること（15-30分）:**\n"
            f"・プレビューリンクから記事を確認\n"
            f"・【要追記】の箇所に体験談を追記\n"
            f"・問題なければ何もしなくてOK\n\n"
            f"⏰ 翌朝 JST 6:00-7:00 に自動公開されます"
        )
    else:
        # ドラフトがない場合 → 管理画面リンクを送信
        message = (
            f"📅 **明日はブログ公開日！** ({date_str} {dow_ja}曜日)\n"
            f"━━━━━━━━━━━━━━━\n"
            f"⚠️ ドラフト記事がありません\n\n"
            f"WordPress管理画面:\n"
            f"{site_url}/wp-admin/edit.php\n\n"
            f"翌朝の自動公開で新規記事が生成・公開されます"
        )

    notify_discord(message)
    print("リマインダー送信完了")


if __name__ == "__main__":
    main()
