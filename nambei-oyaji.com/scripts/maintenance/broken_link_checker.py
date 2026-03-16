#!/usr/bin/env python3
"""リンク切れチェッカー — 全公開記事の外部リンク・アフィリリンクをスキャン

Usage:
    python broken_link_checker.py              # 全記事チェック
    python broken_link_checker.py --limit 5    # 5記事だけ
    python broken_link_checker.py --dry-run    # URLリスト表示のみ
"""
import argparse
import io
import json
import logging
import re
import sys
import time
from datetime import datetime
from pathlib import Path
from urllib.parse import urlparse

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding="utf-8", errors="replace")

try:
    import requests
except ImportError:
    print("ERROR: requests が必要です: pip install requests")
    sys.exit(1)

# --- Paths ---
SCRIPT_DIR = Path(__file__).parent
PROJECT_ROOT = SCRIPT_DIR.parent.parent
CONFIG_DIR = PROJECT_ROOT / "config"
OUTPUTS_DIR = PROJECT_ROOT / "outputs"
REPORTS_DIR = OUTPUTS_DIR / "maintenance-reports"
LOG_FILE = OUTPUTS_DIR / "broken-link-check.log"

REPORTS_DIR.mkdir(parents=True, exist_ok=True)

# --- Logging ---
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler(LOG_FILE, encoding="utf-8"),
    ],
)
logger = logging.getLogger(__name__)


def load_secrets():
    path = CONFIG_DIR / "secrets.json"
    if not path.exists():
        logger.error(f"secrets.json が見つかりません: {path}")
        return {}
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def get_wp_session(secrets):
    """WordPress REST API セッション作成"""
    from base64 import b64encode

    wp = secrets.get("wordpress", {})
    username = wp.get("username", "")
    app_password = wp.get("app_password", "")
    token = b64encode(f"{username}:{app_password}".encode()).decode()

    session = requests.Session()
    session.headers.update({
        "Authorization": f"Basic {token}",
        "Content-Type": "application/json",
    })
    return session


def fetch_published_posts(session, limit=100):
    """公開済み全記事を取得"""
    posts = []
    page = 1
    per_page = 50
    while True:
        url = f"https://nambei-oyaji.com/wp-json/wp/v2/posts?status=publish&per_page={per_page}&page={page}"
        resp = session.get(url, timeout=30)
        if resp.status_code != 200:
            break
        batch = resp.json()
        if not batch:
            break
        posts.extend(batch)
        if len(batch) < per_page or (limit and len(posts) >= limit):
            break
        page += 1
    return posts[:limit] if limit else posts


def extract_urls(html_content):
    """HTMLからURLを抽出"""
    pattern = r'href=["\']([^"\']+)["\']'
    urls = re.findall(pattern, html_content)
    # 外部URLのみ（#アンカー、mailto、tel除外）
    external = []
    for url in urls:
        if url.startswith(("http://", "https://")) and "nambei-oyaji.com" not in url:
            external.append(url)
    # 内部リンクも別途チェック
    internal = []
    for url in urls:
        if "nambei-oyaji.com" in url:
            internal.append(url)
    return external, internal


def check_url(url, timeout=15):
    """URLの死活チェック（HEADリクエスト→失敗時GET）"""
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
    }
    try:
        resp = requests.head(url, headers=headers, timeout=timeout, allow_redirects=True)
        if resp.status_code == 405:  # Method Not Allowed → GETで再試行
            resp = requests.get(url, headers=headers, timeout=timeout, allow_redirects=True)
        return resp.status_code, None
    except requests.exceptions.Timeout:
        return None, "Timeout"
    except requests.exceptions.ConnectionError:
        return None, "Connection Error"
    except Exception as e:
        return None, str(e)[:100]


def send_discord_notification(secrets, report_summary):
    """Discord Webhook で通知"""
    webhook_url = secrets.get("discord", {}).get("webhook_url", "")
    if not webhook_url or webhook_url.startswith("YOUR"):
        logger.info("Discord Webhook未設定。通知スキップ。")
        return

    dashboard_url = "https://htmlpreview.github.io/?https://gist.githubusercontent.com/tmizuno27/16a8680cadf8aed0c207777f7468963b/raw/daily-business-dashboard.html"
    payload = {
        "embeds": [{
            "title": "🔗 リンク切れチェック結果",
            "url": dashboard_url,
            "description": report_summary,
            "color": 0xFF4444 if "broken" in report_summary.lower() else 0x44FF44,
            "timestamp": datetime.now().isoformat(),
        }]
    }
    try:
        requests.post(webhook_url, json=payload, timeout=10)
    except Exception as e:
        logger.warning(f"Discord通知失敗: {e}")


def main():
    parser = argparse.ArgumentParser(description="リンク切れチェッカー")
    parser.add_argument("--limit", type=int, default=0, help="チェック記事数の上限（0=全件）")
    parser.add_argument("--dry-run", action="store_true", help="URLリスト表示のみ")
    parser.add_argument("--no-discord", action="store_true", help="Discord通知スキップ")
    args = parser.parse_args()

    logger.info("========== リンク切れチェック 開始 ==========")
    secrets = load_secrets()
    session = get_wp_session(secrets)

    # 記事取得
    posts = fetch_published_posts(session, limit=args.limit or None)
    logger.info(f"チェック対象: {len(posts)}記事")

    # アフィリエイトリンクも追加チェック
    affiliate_path = CONFIG_DIR / "affiliate-links.json"
    affiliate_urls = []
    if affiliate_path.exists():
        with open(affiliate_path, "r", encoding="utf-8") as f:
            aff_data = json.load(f)
        for service in aff_data.values():
            if isinstance(service, dict):
                url = service.get("url", "")
                if url and not url.startswith("https://YOUR"):
                    affiliate_urls.append(url)

    broken_links = []
    checked = 0
    total_urls = 0

    for post in posts:
        title = post.get("title", {}).get("rendered", "No Title")
        content = post.get("content", {}).get("rendered", "")
        post_id = post.get("id")
        post_url = post.get("link", "")

        external_urls, internal_urls = extract_urls(content)
        all_urls = external_urls + internal_urls

        if args.dry_run:
            if all_urls:
                logger.info(f"[{post_id}] {title}: {len(all_urls)} URLs")
                for u in all_urls:
                    logger.info(f"  → {u}")
            continue

        for url in all_urls:
            total_urls += 1
            status_code, error = check_url(url)

            if error or (status_code and status_code >= 400):
                broken_links.append({
                    "post_id": post_id,
                    "post_title": title,
                    "post_url": post_url,
                    "broken_url": url,
                    "status": status_code,
                    "error": error,
                })
                logger.warning(f"  ✗ [{status_code or 'ERR'}] {url} (in: {title})")
            else:
                logger.debug(f"  ✓ [{status_code}] {url}")

            time.sleep(0.5)  # サーバー負荷軽減

        checked += 1

    # アフィリエイトリンクチェック
    if not args.dry_run and affiliate_urls:
        logger.info(f"アフィリエイトリンク: {len(affiliate_urls)}件チェック")
        for url in affiliate_urls:
            total_urls += 1
            status_code, error = check_url(url)
            if error or (status_code and status_code >= 400):
                broken_links.append({
                    "post_id": "affiliate",
                    "post_title": "アフィリエイトリンク",
                    "post_url": "",
                    "broken_url": url,
                    "status": status_code,
                    "error": error,
                })
                logger.warning(f"  ✗ アフィリ [{status_code or 'ERR'}] {url}")
            time.sleep(0.5)

    if args.dry_run:
        logger.info("Dry-run完了。")
        return

    # レポート生成
    today = datetime.now().strftime("%Y-%m-%d")
    report_path = REPORTS_DIR / f"broken-links-{today}.json"
    report = {
        "date": today,
        "posts_checked": checked,
        "urls_checked": total_urls,
        "broken_count": len(broken_links),
        "broken_links": broken_links,
    }
    with open(report_path, "w", encoding="utf-8") as f:
        json.dump(report, f, ensure_ascii=False, indent=2)

    logger.info(f"チェック完了: {total_urls} URL中 {len(broken_links)}件のリンク切れ")
    logger.info(f"レポート: {report_path}")

    # Discord通知
    if not args.no_discord:
        summary = f"**{checked}記事 / {total_urls} URL チェック完了**\n"
        if broken_links:
            summary += f"⚠️ **{len(broken_links)}件のリンク切れ検出**\n"
            for bl in broken_links[:5]:
                summary += f"- [{bl['status'] or 'ERR'}] `{bl['broken_url'][:60]}` in {bl['post_title'][:30]}\n"
            if len(broken_links) > 5:
                summary += f"... 他{len(broken_links)-5}件"
        else:
            summary += "✅ リンク切れなし"
        send_discord_notification(secrets, summary)

    logger.info("========== リンク切れチェック 終了 ==========")


if __name__ == "__main__":
    main()
