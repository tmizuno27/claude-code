"""
ブログ公開リマインダー — 前日に記事生成→WPドラフト投稿→Discord通知
Task Scheduler から毎日 PYT 12:00 に発火

フロー:
  1. 翌日がJST公開日(月/木)か判定
  2. 公開日なら article_generator.py で記事生成
  3. blog_image_pipeline.py でアイキャッチ生成
  4. wp_publisher.py --status draft で WP にドラフト投稿
  5. Discord に記事プレビュー + WP編集リンク + WPプレビューリンクを通知
  6. 翌朝 blog-auto-publish.ps1 がドラフトを公開に変更

これにより、オーナーは前日にスマホからWPアプリで記事を確認・編集できる
"""

import csv
import io
import json
import subprocess
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
OUTPUTS_DIR = BLOG_DIR / "outputs"
CSV_FILE = OUTPUTS_DIR / "article-management.csv"
KW_QUEUE_FILE = BLOG_DIR / "inputs" / "keyword-queue.json"

# スクリプトパス
GENERATOR_SCRIPT = BLOG_DIR / "scripts" / "content" / "article_generator.py"
IMAGE_PIPELINE = BLOG_DIR / "scripts" / "media" / "blog_image_pipeline.py"
PUBLISHER_SCRIPT = BLOG_DIR / "scripts" / "publishing" / "wp_publisher.py"
SHEET_UPDATER = BLOG_DIR / "scripts" / "analytics" / "create_article_sheet.py"

WP_SITE_URL = "https://nambei-oyaji.com"
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


def run_script(script_path: str, args: list[str] = None) -> tuple[int, str]:
    """Pythonスクリプトを実行して結果を返す"""
    cmd = ["python", str(script_path)]
    if args:
        cmd.extend(args)
    import os
    try:
        env = {**os.environ, "PYTHONIOENCODING": "utf-8"}
        result = subprocess.run(
            cmd,
            capture_output=True,
            timeout=600,
            env=env,
        )
        output = result.stdout.decode("utf-8", errors="replace") + result.stderr.decode("utf-8", errors="replace")
        return result.returncode, output
    except Exception as e:
        return 1, f"ERROR: {e}"


def get_latest_draft_wp_id() -> tuple[int | None, str | None, str | None]:
    """CSVから最新のドラフト記事のWP ID、タイトル、パーマリンクを取得"""
    if not CSV_FILE.exists():
        return None, None, None
    try:
        with open(CSV_FILE, "r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            drafts = []
            for row in reader:
                status = row.get("ステータス", "")
                if "ドラフト" in status or "draft" in status.lower():
                    drafts.append(row)
            if not drafts:
                return None, None, None
            # 最新のドラフト（最後の行）
            latest = drafts[-1]
            # 備考からWP IDを抽出
            notes = latest.get("備考", "")
            wp_id = None
            if "WP ID:" in notes:
                try:
                    wp_id = int(notes.split("WP ID:")[1].split()[0].strip())
                except (ValueError, IndexError):
                    pass
            title = latest.get("記事タイトル", "タイトル不明")
            permalink = latest.get("パーマリンク", "")
            return wp_id, title, permalink
    except Exception as e:
        print(f"WARNING: CSV読み込みエラー - {e}")
        return None, None, None


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

    print(f"明日は公開日！記事の事前準備を開始します...")

    # === Step 1: 記事生成 ===
    print("--- Step 1: 記事生成 ---")
    gen_code, gen_output = run_script(GENERATOR_SCRIPT)
    print(f"article_generator.py: exit code {gen_code}")
    if gen_code != 0:
        print(f"WARNING: 記事生成が異常終了\n{gen_output}")

    # === Step 2: アイキャッチ画像生成 ===
    print("--- Step 2: 画像生成 ---")
    img_code, img_output = run_script(IMAGE_PIPELINE, ["--limit", "1"])
    print(f"blog_image_pipeline.py: exit code {img_code}")

    # === Step 3: WPにドラフト投稿 ===
    print("--- Step 3: WPドラフト投稿 ---")
    pub_code, pub_output = run_script(PUBLISHER_SCRIPT, ["--status", "draft", "--limit", "1"])
    print(f"wp_publisher.py (draft): exit code {pub_code}")

    # === Step 4: スプレッドシート更新 ===
    print("--- Step 4: スプレッドシート更新 ---")
    sheet_code, sheet_output = run_script(SHEET_UPDATER)
    print(f"create_article_sheet.py: exit code {sheet_code}")

    # === Step 5: Discord通知 ===
    wp_id, title, permalink = get_latest_draft_wp_id()

    if wp_id:
        edit_url = f"{WP_SITE_URL}/wp-admin/post.php?post={wp_id}&action=edit"
        preview_url = f"{WP_SITE_URL}/?p={wp_id}&preview=true"

        message = (
            f"📅 **明日はブログ公開日！** ({date_str} {dow_ja}曜日)\n"
            f"━━━━━━━━━━━━━━━\n"
            f"📝 **{title}**\n"
            f"━━━━━━━━━━━━━━━\n\n"
            f"👀 **プレビュー（読者視点で確認）:**\n{preview_url}\n\n"
            f"✏️ **編集（体験談の追記・修正）:**\n{edit_url}\n\n"
            f"**やること（15-30分）:**\n"
            f"・記事を読んで内容を確認\n"
            f"・【要追記】の箇所に体験談を追記\n"
            f"・問題なければ何もしなくてOK\n\n"
            f"⏰ 翌朝 JST 6:00-7:00 に自動公開されます"
        )
    else:
        message = (
            f"📅 **明日はブログ公開日！** ({date_str} {dow_ja}曜日)\n"
            f"━━━━━━━━━━━━━━━\n"
            f"⚠️ ドラフト記事のWP IDが取得できませんでした\n"
            f"WordPress管理画面で直接確認してください:\n"
            f"{WP_SITE_URL}/wp-admin/edit.php?post_status=draft\n\n"
            f"⏰ 翌朝 JST 6:00-7:00 に自動公開されます"
        )

    notify_discord(message)
    print("リマインダー送信完了")


if __name__ == "__main__":
    main()
