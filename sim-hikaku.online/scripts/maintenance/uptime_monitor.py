#!/usr/bin/env python3
"""サイト死活監視 — sim-hikaku.online のダウン検知 → Discord通知

Usage:
    python uptime_monitor.py                # チェック実行
    python uptime_monitor.py --no-discord   # 通知なし
"""
import argparse
import io
import json
import logging
import sys
from datetime import datetime
from pathlib import Path

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
LOG_FILE = OUTPUTS_DIR / "uptime-monitor.log"
STATUS_FILE = OUTPUTS_DIR / "uptime-status.json"

OUTPUTS_DIR.mkdir(parents=True, exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler(LOG_FILE, encoding="utf-8"),
    ],
)
logger = logging.getLogger(__name__)

SITE_URL = "https://sim-hikaku.online"
CHECK_ENDPOINTS = [
    "/",
    "/wp-json/wp/v2/posts?per_page=1",
]
TIMEOUT = 20


def load_secrets():
    path = CONFIG_DIR / "secrets.json"
    if not path.exists():
        return {}
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def load_status():
    if STATUS_FILE.exists():
        with open(STATUS_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {"last_check": None, "status": "unknown", "consecutive_failures": 0}


def save_status(status):
    with open(STATUS_FILE, "w", encoding="utf-8") as f:
        json.dump(status, f, ensure_ascii=False, indent=2)


def check_endpoint(url):
    """エンドポイントをチェック。(ok, status_code, response_time_ms, error)"""
    try:
        start = datetime.now()
        resp = requests.get(url, timeout=TIMEOUT, headers={
            "User-Agent": "UptimeMonitor/1.0 sim-hikaku.online"
        })
        elapsed_ms = int((datetime.now() - start).total_seconds() * 1000)
        ok = 200 <= resp.status_code < 400
        return ok, resp.status_code, elapsed_ms, None
    except requests.exceptions.Timeout:
        return False, None, None, "Timeout"
    except requests.exceptions.ConnectionError:
        return False, None, None, "Connection Error"
    except Exception as e:
        return False, None, None, str(e)[:100]


def send_discord_alert(secrets, message, is_down=True):
    webhook_url = secrets.get("discord", {}).get("webhook_url", "")
    if not webhook_url or webhook_url.startswith("YOUR"):
        logger.info("Discord Webhook未設定。通知スキップ。")
        return

    color = 0xFF0000 if is_down else 0x00FF00
    title = "サイトダウン検知 (sim-hikaku)" if is_down else "サイト復旧確認 (sim-hikaku)"

    payload = {
        "embeds": [{
            "title": title,
            "description": message,
            "color": color,
            "timestamp": datetime.utcnow().isoformat(),
        }]
    }
    try:
        requests.post(webhook_url, json=payload, timeout=10)
        logger.info("Discord通知送信完了")
    except Exception as e:
        logger.warning(f"Discord通知失敗: {e}")


def main():
    parser = argparse.ArgumentParser(description="サイト死活監視 (sim-hikaku.online)")
    parser.add_argument("--no-discord", action="store_true")
    args = parser.parse_args()

    now = datetime.now()
    logger.info(f"死活監視チェック: {now.strftime('%Y-%m-%d %H:%M:%S')}")

    secrets = load_secrets()
    prev_status = load_status()

    all_ok = True
    results = []

    for endpoint in CHECK_ENDPOINTS:
        url = SITE_URL + endpoint
        ok, status_code, elapsed_ms, error = check_endpoint(url)
        results.append({
            "endpoint": endpoint,
            "ok": ok,
            "status_code": status_code,
            "response_time_ms": elapsed_ms,
            "error": error,
        })

        if ok:
            logger.info(f"  OK {endpoint} [{status_code}] {elapsed_ms}ms")
        else:
            logger.warning(f"  NG {endpoint} [{status_code or 'ERR'}] {error}")
            all_ok = False

    new_status = {
        "last_check": now.isoformat(),
        "status": "up" if all_ok else "down",
        "consecutive_failures": 0 if all_ok else prev_status.get("consecutive_failures", 0) + 1,
        "last_results": results,
    }

    if all_ok:
        new_status["last_up"] = now.isoformat()
    else:
        new_status["last_down"] = now.isoformat()
        new_status["last_up"] = prev_status.get("last_up")

    save_status(new_status)

    if not args.no_discord:
        was_up = prev_status.get("status") in ("up", "unknown")
        was_down = prev_status.get("status") == "down"

        if not all_ok and was_up:
            failures = [r for r in results if not r["ok"]]
            msg = f"**{SITE_URL}** がダウンしています\n\n"
            for f in failures:
                msg += f"- `{f['endpoint']}` -> {f['error'] or f'HTTP {f[\"status_code\"]}'}\n"
            send_discord_alert(secrets, msg, is_down=True)

        elif all_ok and was_down:
            down_count = prev_status.get("consecutive_failures", 0)
            msg = f"**{SITE_URL}** が復旧しました\n"
            msg += f"ダウン回数: {down_count}回連続\n"
            for r in results:
                msg += f"- `{r['endpoint']}` -> {r['response_time_ms']}ms\n"
            send_discord_alert(secrets, msg, is_down=False)

    status_label = "UP" if all_ok else "DOWN"
    logger.info(f"結果: {status_label}")


if __name__ == "__main__":
    main()
