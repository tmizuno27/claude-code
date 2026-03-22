#!/usr/bin/env python3
"""
日次優先アクション自動実行スクリプト

daily_business_report.py の後に実行され、action-status.json の
未完了アクションのうち自動実行可能なものを実行し、完了マークを付ける。

使い方:
  python daily_auto_actions.py          # 通常実行
  python daily_auto_actions.py --dry    # ドライラン（実行せずにログのみ）
"""

import fnmatch
import json
import logging
import os
import subprocess
import sys
from base64 import b64encode
from datetime import date, datetime, timedelta
from pathlib import Path

import requests

# ── パス定義 ──────────────────────────────────────────────
PROJECT_ROOT = Path(__file__).parent.parent.parent  # nambei-oyaji.com/
WORKSPACE_ROOT = PROJECT_ROOT.parent  # claude-code/
REPORTS_DIR = PROJECT_ROOT / "outputs" / "reports"
ACTION_STATUS_PATH = REPORTS_DIR / "action-status.json"
LOG_PATH = WORKSPACE_ROOT / "logs" / "daily-auto-actions.log"

# ── ログ設定 ──────────────────────────────────────────────
LOG_PATH.parent.mkdir(parents=True, exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler(str(LOG_PATH), encoding="utf-8"),
        logging.StreamHandler(),
    ],
)
logger = logging.getLogger(__name__)

# ── サイト設定 ────────────────────────────────────────────
SITE_CONFIGS = {
    "nambei-oyaji.com": {
        "config_path": WORKSPACE_ROOT / "nambei-oyaji.com" / "config" / "settings.json",
        "secrets_path": WORKSPACE_ROOT / "nambei-oyaji.com" / "config" / "secrets.json",
        "csv_path": WORKSPACE_ROOT / "nambei-oyaji.com" / "outputs" / "article-management.csv",
        "display_name": "南米おやじの海外生活ラボ",
    },
    "otona-match.com": {
        "config_path": WORKSPACE_ROOT / "otona-match.com" / "config" / "settings.json",
        "secrets_path": WORKSPACE_ROOT / "otona-match.com" / "config" / "secrets.json",
        "csv_path": WORKSPACE_ROOT / "otona-match.com" / "outputs" / "article-management.csv",
        "display_name": "大人のマッチングナビ",
    },
    "sim-hikaku.online": {
        "config_path": WORKSPACE_ROOT / "sim-hikaku.online" / "config" / "settings.json",
        "secrets_path": WORKSPACE_ROOT / "sim-hikaku.online" / "config" / "secrets.json",
        "csv_path": WORKSPACE_ROOT / "sim-hikaku.online" / "outputs" / "article-management.csv",
        "display_name": "SIM比較ナビ",
    },
}

# ── アクションカテゴリ定義 ────────────────────────────────
ACTION_PATTERNS = {
    "ctr": ["*ctr*", "*title*", "*meta*"],
    "content": ["*content*", "*boost*", "*rewrite*", "*article*"],
    "traffic": ["*traffic*", "*audit*", "*analytics*"],
    "sns": ["*x-*", "*post*", "*tweet*", "*sns*"],
}


# ── ユーティリティ ────────────────────────────────────────
def load_json(path: Path) -> dict:
    """JSONファイルを読み込む（存在しなければ空dictを返す）"""
    if not path.exists():
        logger.warning(f"ファイルが見つかりません: {path}")
        return {}
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception as e:
        logger.error(f"JSON読み込みエラー {path}: {e}")
        return {}


def classify_action(action_id: str) -> str | None:
    """アクションIDをカテゴリに分類する。マッチしなければNone"""
    lower_id = action_id.lower()
    for category, patterns in ACTION_PATTERNS.items():
        for pattern in patterns:
            if fnmatch.fnmatch(lower_id, pattern):
                return category
    return None


def mark_action_done(action_id: str) -> bool:
    """dashboard_updater.pyのmark_action関数を呼び出して完了マーク"""
    try:
        from dashboard_updater import mark_action
        return mark_action(action_id, done=True)
    except ImportError:
        # 直接パスを指定してインポート
        updater_path = Path(__file__).parent / "dashboard_updater.py"
        if not updater_path.exists():
            logger.error("dashboard_updater.py が見つかりません")
            return False
        import importlib.util
        spec = importlib.util.spec_from_file_location("dashboard_updater", str(updater_path))
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
        return mod.mark_action(action_id, done=True)


# ── Search Console API ────────────────────────────────────
def fetch_low_ctr_pages(site_key: str, site_meta: dict) -> list[dict]:
    """Search Console APIで表示回数上位かつCTR5%以下のページを取得"""
    config = load_json(site_meta["config_path"])
    sc_config = config.get("search_console", {})
    site_url = sc_config.get("site_url", "")
    cred_path = sc_config.get("credentials_file", "gsc-credentials.json")

    site_dir = site_meta["config_path"].parent
    cred_file = site_dir / cred_path

    if not site_url or not cred_file.exists():
        logger.info(f"[{site_key}] Search Console 未設定、スキップ")
        return []

    try:
        os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = str(cred_file)
        from google.oauth2 import service_account
        from googleapiclient.discovery import build

        credentials = service_account.Credentials.from_service_account_file(
            str(cred_file),
            scopes=["https://www.googleapis.com/auth/webmasters.readonly"],
        )
        service = build("searchconsole", "v1", credentials=credentials)

        end_date = date.today() - timedelta(days=3)
        start_date = end_date - timedelta(days=28)

        response = service.searchanalytics().query(
            siteUrl=site_url,
            body={
                "startDate": start_date.strftime("%Y-%m-%d"),
                "endDate": end_date.strftime("%Y-%m-%d"),
                "dimensions": ["page"],
                "rowLimit": 50,
                "orderBy": [{"fieldName": "impressions", "sortOrder": "DESCENDING"}],
            },
        ).execute()

        low_ctr_pages = []
        for row in response.get("rows", []):
            impressions = row.get("impressions", 0)
            ctr = row.get("ctr", 0) * 100
            if impressions >= 50 and ctr < 5.0:
                low_ctr_pages.append({
                    "page": row["keys"][0],
                    "impressions": impressions,
                    "clicks": row.get("clicks", 0),
                    "ctr": round(ctr, 2),
                    "position": round(row.get("position", 0), 1),
                })
        return low_ctr_pages

    except Exception as e:
        logger.error(f"[{site_key}] Search Console API エラー: {e}")
        return []


# ── WordPress API ─────────────────────────────────────────
def get_wp_auth_headers(secrets: dict) -> dict | None:
    """WordPress REST API用の認証ヘッダーを生成"""
    wp = secrets.get("wordpress", {})
    username = wp.get("username", "")
    app_password = wp.get("app_password", "")
    if not username or not app_password:
        return None
    token = b64encode(f"{username}:{app_password}".encode()).decode()
    return {"Authorization": f"Basic {token}"}


def improve_title(original_title: str) -> str:
    """タイトル改善: 数字追加、パワーワード追加、30-32文字に調整"""
    improved = original_title

    # 既に短い場合はパワーワード追加
    power_words = ["【完全版】", "【最新】", "【保存版】", "【徹底解説】"]
    has_brackets = "【" in improved
    if not has_brackets and len(improved) < 28:
        improved = f"【2026年最新】{improved}"

    # 長すぎる場合は末尾を切って調整
    if len(improved) > 35:
        # 末尾の「〜について」「〜のまとめ」等を除去
        for suffix in ["について", "のまとめ", "を解説", "を紹介", "をご紹介"]:
            if improved.endswith(suffix):
                improved = improved[: -len(suffix)]
                break

    # それでも長い場合は32文字で切る
    if len(improved) > 35:
        improved = improved[:32]

    return improved


def update_wp_post_title(rest_api_url: str, post_id: int, new_title: str, headers: dict) -> bool:
    """WordPress REST APIで記事タイトルを更新"""
    try:
        url = f"{rest_api_url}/posts/{post_id}"
        resp = requests.post(url, json={"title": new_title}, headers=headers, timeout=30)
        resp.raise_for_status()
        return True
    except Exception as e:
        logger.error(f"WP記事更新エラー (post_id={post_id}): {e}")
        return False


# ── アクション実行関数 ────────────────────────────────────
def execute_ctr_action(action: dict, dry_run: bool = False) -> bool:
    """CTR改善系アクションを実行"""
    logger.info(f"[CTR改善] {action['title']} を実行中...")
    results = []

    for site_key, site_meta in SITE_CONFIGS.items():
        secrets = load_json(site_meta["secrets_path"])
        if not secrets:
            logger.warning(f"[{site_key}] secrets.json がないためスキップ")
            continue

        config = load_json(site_meta["config_path"])
        wp_config = config.get("wordpress", {})
        rest_api_url = wp_config.get("rest_api_url", "")
        if not rest_api_url:
            logger.warning(f"[{site_key}] REST API URL 未設定、スキップ")
            continue

        headers = get_wp_auth_headers(secrets)
        if not headers:
            logger.warning(f"[{site_key}] WordPress認証情報なし、スキップ")
            continue

        low_ctr_pages = fetch_low_ctr_pages(site_key, site_meta)
        if not low_ctr_pages:
            logger.info(f"[{site_key}] CTR改善対象なし")
            continue

        logger.info(f"[{site_key}] CTR改善対象: {len(low_ctr_pages)}件")

        # 上位5件のみ処理
        for page_info in low_ctr_pages[:5]:
            page_url = page_info["page"]
            logger.info(
                f"  {page_url} (表示:{page_info['impressions']}, "
                f"CTR:{page_info['ctr']}%, 順位:{page_info['position']})"
            )

            if dry_run:
                logger.info("  [DRY RUN] タイトル改善をスキップ")
                continue

            # WP APIから記事IDとタイトルを取得
            try:
                slug = page_url.rstrip("/").split("/")[-1]
                resp = requests.get(
                    f"{rest_api_url}/posts",
                    params={"slug": slug, "per_page": 1},
                    headers=headers,
                    timeout=30,
                )
                resp.raise_for_status()
                posts = resp.json()
                if not posts:
                    logger.warning(f"  記事が見つかりません: {slug}")
                    continue

                post = posts[0]
                original_title = post["title"]["rendered"]
                new_title = improve_title(original_title)

                if new_title == original_title:
                    logger.info(f"  タイトル変更不要: {original_title}")
                    continue

                logger.info(f"  タイトル変更: {original_title} → {new_title}")
                if update_wp_post_title(rest_api_url, post["id"], new_title, headers):
                    results.append({
                        "site": site_key,
                        "post_id": post["id"],
                        "old_title": original_title,
                        "new_title": new_title,
                    })
            except Exception as e:
                logger.error(f"  記事処理エラー ({page_url}): {e}")
                continue

    if results:
        # 変更ログを保存
        log_path = REPORTS_DIR / f"ctr-improvements-{date.today()}.json"
        log_path.write_text(
            json.dumps(results, ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8",
        )
        logger.info(f"CTR改善ログ保存: {log_path}")

    logger.info(f"[CTR改善] 完了 ({len(results)}件更新)")
    return True


def execute_content_action(action: dict, dry_run: bool = False) -> bool:
    """記事強化系アクションを実行（内部リンク挿入）"""
    logger.info(f"[記事強化] {action['title']} を実行中...")

    linker_script = PROJECT_ROOT / "scripts" / "content" / "internal_linker.py"
    if not linker_script.exists():
        logger.error(f"internal_linker.py が見つかりません: {linker_script}")
        return False

    if dry_run:
        logger.info("[DRY RUN] 内部リンク挿入をスキップ")
        return True

    try:
        result = subprocess.run(
            [sys.executable, str(linker_script)],
            capture_output=True,
            text=True,
            timeout=300,
            cwd=str(PROJECT_ROOT),
        )
        if result.returncode == 0:
            logger.info(f"[記事強化] 内部リンク挿入完了")
            if result.stdout:
                for line in result.stdout.strip().split("\n")[-5:]:
                    logger.info(f"  {line}")
        else:
            logger.warning(f"[記事強化] internal_linker.py 終了コード: {result.returncode}")
            if result.stderr:
                logger.warning(f"  stderr: {result.stderr[:500]}")
        return True
    except subprocess.TimeoutExpired:
        logger.error("[記事強化] internal_linker.py タイムアウト (300秒)")
        return False
    except Exception as e:
        logger.error(f"[記事強化] 実行エラー: {e}")
        return False


def execute_traffic_action(action: dict, dry_run: bool = False) -> bool:
    """流入分析系アクションを実行"""
    logger.info(f"[流入分析] {action['title']} を実行中...")

    rapidapi_stats = WORKSPACE_ROOT / "api-services" / "rapidapi-stats.json"

    if rapidapi_stats.exists():
        stats = load_json(rapidapi_stats)
        if stats:
            total_calls = sum(
                api.get("calls", 0) for api in stats.get("apis", [])
            )
            active_apis = sum(
                1 for api in stats.get("apis", []) if api.get("calls", 0) > 0
            )
            total_apis = len(stats.get("apis", []))
            logger.info(f"  RapidAPI統計: {total_apis}本中 {active_apis}本アクティブ, 総コール数: {total_calls}")
        else:
            logger.info("  RapidAPI統計: データなし")
    else:
        logger.info("  RapidAPI統計ファイルが見つかりません")

    # 各サイトのSearch Consoleサマリーを出力
    for site_key, site_meta in SITE_CONFIGS.items():
        low_ctr = fetch_low_ctr_pages(site_key, site_meta)
        if low_ctr:
            logger.info(f"  [{site_key}] CTR<5%のページ: {len(low_ctr)}件")
        else:
            logger.info(f"  [{site_key}] Search Consoleデータなし or 問題なし")

    logger.info("[流入分析] レポート生成完了")
    return True


def execute_sns_action(action: dict, dry_run: bool = False) -> bool:
    """X投稿系アクションを実行（自動投稿の稼働確認）"""
    logger.info(f"[SNS確認] {action['title']} を実行中...")

    # X自動投稿の最新ログを確認
    x_log_patterns = [
        WORKSPACE_ROOT / "logs" / "x-auto-post.log",
        WORKSPACE_ROOT / "logs" / "sns-scheduler.log",
        WORKSPACE_ROOT / "logs" / "x-posting.log",
    ]

    log_found = False
    for log_path in x_log_patterns:
        if log_path.exists():
            log_found = True
            try:
                content = log_path.read_text(encoding="utf-8", errors="replace")
                lines = content.strip().split("\n")
                recent_lines = lines[-10:] if len(lines) > 10 else lines
                last_line = lines[-1] if lines else ""
                logger.info(f"  X投稿ログ ({log_path.name}): 最新行 = {last_line[:100]}")

                # 最終投稿が24時間以内かチェック
                today_str = date.today().strftime("%Y-%m-%d")
                yesterday_str = (date.today() - timedelta(days=1)).strftime("%Y-%m-%d")
                recent_posts = [
                    l for l in recent_lines
                    if today_str in l or yesterday_str in l
                ]
                if recent_posts:
                    logger.info(f"  直近24時間の投稿ログ: {len(recent_posts)}件 ✓")
                else:
                    logger.warning(f"  直近24時間の投稿ログなし ⚠ 自動投稿が停止している可能性")
            except Exception as e:
                logger.error(f"  ログ読み取りエラー ({log_path}): {e}")

    if not log_found:
        logger.warning("  X投稿ログファイルが見つかりません")

    logger.info("[SNS確認] 完了")
    return True


# ── メイン処理 ────────────────────────────────────────────
CATEGORY_HANDLERS = {
    "ctr": execute_ctr_action,
    "content": execute_content_action,
    "traffic": execute_traffic_action,
    "sns": execute_sns_action,
}


def run_auto_actions(dry_run: bool = False):
    """未完了アクションをループして自動実行"""
    logger.info("=" * 60)
    logger.info(f"日次優先アクション自動実行 開始 ({datetime.now().strftime('%Y-%m-%d %H:%M')})")
    logger.info("=" * 60)

    data = load_json(ACTION_STATUS_PATH)
    if not data:
        logger.error("action-status.json を読み込めません")
        return

    actions = data.get("actions", [])
    pending_actions = [a for a in actions if not a.get("done", False)]

    if not pending_actions:
        logger.info("未完了アクションなし。終了します。")
        return

    logger.info(f"未完了アクション: {len(pending_actions)}件")

    executed_count = 0
    skipped_count = 0
    failed_count = 0

    for action in pending_actions:
        action_id = action.get("id", "")
        title = action.get("title", "")
        category = classify_action(action_id)

        if category is None:
            logger.info(f"手動対応必要: {title} (id={action_id})")
            skipped_count += 1
            continue

        handler = CATEGORY_HANDLERS.get(category)
        if handler is None:
            logger.info(f"手動対応必要: {title} (category={category})")
            skipped_count += 1
            continue

        try:
            success = handler(action, dry_run=dry_run)
            if success and not dry_run:
                mark_action_done(action_id)
                executed_count += 1
            elif success and dry_run:
                logger.info(f"[DRY RUN] 完了マークをスキップ: {title}")
                executed_count += 1
            else:
                logger.warning(f"アクション実行失敗: {title}")
                failed_count += 1
        except Exception as e:
            logger.error(f"アクション実行エラー ({title}): {e}")
            failed_count += 1

    logger.info("-" * 60)
    logger.info(
        f"実行結果: 成功={executed_count}, スキップ(手動)={skipped_count}, 失敗={failed_count}"
    )
    logger.info("日次優先アクション自動実行 完了")


def main():
    dry_run = "--dry" in sys.argv
    if dry_run:
        logger.info("*** ドライランモード ***")
    run_auto_actions(dry_run=dry_run)


if __name__ == "__main__":
    main()
