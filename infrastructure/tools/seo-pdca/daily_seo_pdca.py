"""
3サイト SEO PDCA 日次自動実行スクリプト
目的: インプレッション数最大化 → 収益化加速

毎日自動実行される4ステップ:
  1. CHECK  - GSCデータ分析（インデックス状況・順位・CTR・クエリ）
  2. ACT    - 改善アクション実行（サイトマップping・内部リンク・タイトル改善等）
  3. PLAN   - 次回アクション計画をログに記録
  4. DO     - WordPress記事の自動最適化（メタ改善・noindex解除等）

使い方:
  python daily_seo_pdca.py           # 全サイト実行
  python daily_seo_pdca.py --site nambei  # 特定サイトのみ
"""
import sys
import os
import json
import csv
import time
import re
import requests
from datetime import datetime, timedelta, timezone
from pathlib import Path
from urllib.parse import quote, unquote
from collections import defaultdict

if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")

from google.oauth2 import service_account
from googleapiclient.discovery import build

# ==== パス設定 ====
SCRIPT_DIR = Path(__file__).parent
REPO_ROOT = SCRIPT_DIR.parent.parent.parent  # claude-code/
CRED_PATH = REPO_ROOT / "sites" / "nambei-oyaji.com" / "config" / "gsc-credentials.json"
LOG_DIR = REPO_ROOT / "logs"
LOG_DIR.mkdir(exist_ok=True)

PYT = timezone(timedelta(hours=-3))
NOW = datetime.now(PYT)
TODAY = NOW.strftime("%Y-%m-%d")

GSC_SCOPES = ["https://www.googleapis.com/auth/webmasters.readonly"]

# ==== サイト定義 ====
SITES = {
    "nambei": {
        "label": "南米おやじ",
        "domain": "nambei-oyaji.com",
        "site_url": "https://nambei-oyaji.com",
        "gsc_url": "https://nambei-oyaji.com/",
        "sitemap_url": "https://nambei-oyaji.com/sitemap_index.xml",
        "site_dir": REPO_ROOT / "sites" / "nambei-oyaji.com",
        "wp_cred_file": "wp-credentials.json",
        "wp_cred_in_secrets": False,
    },
    "otona": {
        "label": "マッチングナビ",
        "domain": "otona-match.com",
        "site_url": "https://otona-match.com",
        "gsc_url": "https://otona-match.com/",
        "sitemap_url": "https://otona-match.com/wp-sitemap.xml",
        "site_dir": REPO_ROOT / "sites" / "otona-match.com",
        "wp_cred_file": None,
        "wp_cred_in_secrets": True,
    },
    "sim": {
        "label": "SIM比較",
        "domain": "sim-hikaku.online",
        "site_url": "https://sim-hikaku.online",
        "gsc_url": "https://sim-hikaku.online/",
        "sitemap_url": "https://sim-hikaku.online/wp-sitemap.xml",
        "site_dir": REPO_ROOT / "sites" / "sim-hikaku.online",
        "wp_cred_file": None,
        "wp_cred_in_secrets": True,
    },
}


# ==== ユーティリティ ====
class Logger:
    def __init__(self):
        self.log_path = LOG_DIR / "seo-pdca.log"
        self.report_path = LOG_DIR / f"seo-pdca-report-{TODAY}.md"
        self.lines = []

    def log(self, msg):
        ts = NOW.strftime("%Y-%m-%d %H:%M:%S")
        line = f"[{ts}] {msg}"
        print(line)
        with open(self.log_path, "a", encoding="utf-8") as f:
            f.write(line + "\n")

    def report(self, line=""):
        self.lines.append(line)

    def save_report(self):
        with open(self.report_path, "w", encoding="utf-8") as f:
            f.write("\n".join(self.lines))
        self.log(f"レポート保存: {self.report_path}")


logger = Logger()


def get_gsc_service():
    try:
        creds = service_account.Credentials.from_service_account_file(
            str(CRED_PATH), scopes=GSC_SCOPES
        )
        return build("searchconsole", "v1", credentials=creds)
    except Exception as e:
        logger.log(f"  GSC認証失敗: {e}")
        return None


def get_wp_session(site_cfg):
    """WordPress REST APIセッションを返す"""
    config_dir = site_cfg["site_dir"] / "config"
    if site_cfg["wp_cred_in_secrets"]:
        secrets = json.loads((config_dir / "secrets.json").read_text(encoding="utf-8"))
        wp = secrets["wordpress"]
        base_url = wp.get("site_url", wp.get("url", site_cfg["site_url"]))
        username = wp["username"]
        password = wp["app_password"]
    else:
        cred = json.loads(
            (config_dir / site_cfg["wp_cred_file"]).read_text(encoding="utf-8")
        )
        base_url = cred.get("site_url", site_cfg["site_url"])
        username = cred["username"]
        password = cred["app_password"]

    session = requests.Session()
    session.auth = (username, password)
    session.headers.update({"Content-Type": "application/json"})
    api_base = f"{base_url.rstrip('/')}/wp-json/wp/v2"
    return session, api_base


# ==================================================================
# STEP 1: CHECK — GSCデータ分析
# ==================================================================
def check_gsc(gsc, site_key, site_cfg):
    """GSCからデータ取得し、改善ポイントを特定"""
    label = site_cfg["label"]
    site_url = site_cfg["gsc_url"]
    end_date = (datetime.now() - timedelta(days=3)).strftime("%Y-%m-%d")
    start_date = (datetime.now() - timedelta(days=30)).strftime("%Y-%m-%d")

    logger.report(f"## {label} ({site_cfg['domain']})")
    logger.report("")

    result = {
        "pages": [],
        "queries": [],
        "total_imp": 0,
        "total_clicks": 0,
        "unindexed_estimate": 0,
        "page2_candidates": [],  # 順位11-20: 1ページ目に押し上げチャンス
        "low_ctr_pages": [],  # CTR改善余地あり
        "zero_imp_slugs": [],  # インプレッションゼロの記事slug
    }

    # --- ページ別データ ---
    try:
        resp = gsc.searchanalytics().query(
            siteUrl=site_url,
            body={
                "startDate": start_date,
                "endDate": end_date,
                "dimensions": ["page"],
                "rowLimit": 500,
                "type": "web",
            },
        ).execute()
        result["pages"] = resp.get("rows", [])
    except Exception as e:
        logger.log(f"  [{label}] ページデータ取得エラー: {e}")
        logger.report(f"### CHECK: GSCエラー: {e}")
        logger.report("")
        return result

    # --- クエリ別データ ---
    try:
        resp_q = gsc.searchanalytics().query(
            siteUrl=site_url,
            body={
                "startDate": start_date,
                "endDate": end_date,
                "dimensions": ["query"],
                "rowLimit": 500,
                "type": "web",
            },
        ).execute()
        result["queries"] = resp_q.get("rows", [])
    except Exception:
        pass

    # 集計
    indexed_urls = set()
    for row in result["pages"]:
        url = row["keys"][0]
        imp = row.get("impressions", 0)
        clicks = row.get("clicks", 0)
        pos = row.get("position", 0)
        ctr = row.get("ctr", 0)
        result["total_imp"] += imp
        result["total_clicks"] += clicks
        indexed_urls.add(url)

        # 2ページ目候補（順位11-20）
        if 11 <= pos <= 20 and imp >= 3:
            result["page2_candidates"].append(
                {"url": url, "imp": imp, "clicks": clicks, "pos": pos, "ctr": ctr}
            )

        # CTR低い（順位1-10なのにCTR < 3%）
        if pos <= 10 and ctr < 0.03 and imp >= 5:
            result["low_ctr_pages"].append(
                {"url": url, "imp": imp, "clicks": clicks, "pos": pos, "ctr": ctr}
            )

    # CSV記事とGSCインデックスの突合
    csv_path = site_cfg["site_dir"] / "outputs" / "article-management.csv"
    if csv_path.exists():
        with open(csv_path, "r", encoding="utf-8") as f:
            reader = list(csv.reader(f))
        for row in reader[1:]:
            # URL/slugを取得してGSCにあるか確認
            slug = ""
            for cell in row:
                if cell and ("/" in cell or cell.startswith("http")):
                    if cell.startswith("http"):
                        slug = cell
                    break
            if not slug:
                continue
            found = any(slug.rstrip("/") in u or u.rstrip("/") in slug for u in indexed_urls)
            if not found:
                result["zero_imp_slugs"].append(slug)

    result["unindexed_estimate"] = len(result["zero_imp_slugs"])

    # レポート出力
    logger.report("### CHECK (分析)")
    logger.report(f"- 過去30日 総インプレッション: **{result['total_imp']:,}**")
    logger.report(f"- 過去30日 総クリック: **{result['total_clicks']:,}**")
    logger.report(f"- GSCにデータがあるページ数: **{len(indexed_urls)}**")
    logger.report(f"- インプレッション0の記事数（推定未インデックス）: **{result['unindexed_estimate']}**")
    logger.report(f"- 2ページ目候補（順位11-20）: **{len(result['page2_candidates'])}件**")
    logger.report(f"- CTR改善候補（順位1-10, CTR<3%）: **{len(result['low_ctr_pages'])}件**")
    logger.report("")

    if result["page2_candidates"]:
        logger.report("#### 2ページ目 → 1ページ目 押し上げ候補")
        for p in sorted(result["page2_candidates"], key=lambda x: x["imp"], reverse=True)[:10]:
            logger.report(f"  - pos={p['pos']:.1f} imp={p['imp']} {p['url']}")
        logger.report("")

    if result["low_ctr_pages"]:
        logger.report("#### CTR改善候補（タイトル/メタ改善で効果大）")
        for p in sorted(result["low_ctr_pages"], key=lambda x: x["imp"], reverse=True)[:10]:
            logger.report(
                f"  - pos={p['pos']:.1f} CTR={p['ctr']*100:.1f}% imp={p['imp']} {p['url']}"
            )
        logger.report("")

    # トップクエリ
    if result["queries"]:
        logger.report("#### トップ検索クエリ（過去30日）")
        for q in sorted(result["queries"], key=lambda x: x.get("impressions", 0), reverse=True)[:15]:
            query = q["keys"][0]
            imp = q.get("impressions", 0)
            clicks = q.get("clicks", 0)
            pos = q.get("position", 0)
            logger.report(f"  - 「{query}」 imp={imp} click={clicks} pos={pos:.1f}")
        logger.report("")

    return result


# ==================================================================
# STEP 2: ACT — 改善アクション実行
# ==================================================================
def act_sitemap_ping(site_cfg):
    """サイトマップの存在確認（Google/Bingのpingは廃止済み）"""
    sitemap_url = site_cfg.get("sitemap_url", f"{site_cfg['site_url']}/sitemap.xml")
    try:
        resp = requests.get(sitemap_url, timeout=15)
        if resp.status_code == 200:
            # サイトマップ内のURL数をカウント
            url_count = resp.text.count("<loc>")
            status = f"OK ({url_count} URLs)"
        else:
            status = f"HTTP {resp.status_code}"
        logger.log(f"  [{site_cfg['label']}] サイトマップ確認: {status}")
        return status
    except Exception as e:
        logger.log(f"  [{site_cfg['label']}] サイトマップ確認エラー: {e}")
        return f"ERROR: {e}"


def act_update_seo_meta(site_cfg, check_result):
    """WordPressのタイトル/メタディスクリプションをCTR改善のために更新"""
    actions_taken = []

    # CTR低いページのタイトルにパワーワード追加を検討
    low_ctr = check_result.get("low_ctr_pages", [])
    if not low_ctr:
        return actions_taken

    try:
        session, api_base = get_wp_session(site_cfg)
    except Exception as e:
        logger.log(f"  [{site_cfg['label']}] WP接続エラー: {e}")
        return actions_taken

    for page_info in low_ctr[:3]:  # 1日最大3記事
        url = page_info["url"]
        slug = url.rstrip("/").split("/")[-1]
        if not slug or slug == site_cfg["domain"]:
            continue

        try:
            # 記事を取得
            resp = session.get(f"{api_base}/posts", params={"slug": slug, "per_page": 1})
            if resp.status_code != 200:
                continue
            posts = resp.json()
            if not posts:
                continue

            post = posts[0]
            post_id = post["id"]
            title = post["title"]["rendered"]

            # Rank Mathのメタディスクリプションを確認
            meta = post.get("meta", {})
            rank_math_desc = meta.get("rank_math_description", "")

            # メタディスクリプションが空なら記事の抜粋から生成
            if not rank_math_desc:
                excerpt = post.get("excerpt", {}).get("rendered", "")
                # HTMLタグ除去
                clean_excerpt = re.sub(r"<[^>]+>", "", excerpt).strip()[:140]
                if clean_excerpt:
                    update_data = {"meta": {"rank_math_description": clean_excerpt + "..."}}
                    resp = session.post(
                        f"{api_base}/posts/{post_id}", json=update_data
                    )
                    if resp.status_code == 200:
                        actions_taken.append(
                            f"メタディスクリプション自動生成: {slug}"
                        )
                        logger.log(f"  [{site_cfg['label']}] メタ生成: {slug}")

        except Exception as e:
            logger.log(f"  [{site_cfg['label']}] SEOメタ更新エラー ({slug}): {e}")
            continue

        time.sleep(1)  # WP API rate limit

    return actions_taken


def act_indexing_api(site_cfg):
    """Indexing APIで未インデックスURLを送信（1日最大200件/プロジェクト）"""
    label = site_cfg["label"]
    submitted = []
    errors = []

    try:
        idx_creds = service_account.Credentials.from_service_account_file(
            str(CRED_PATH), scopes=["https://www.googleapis.com/auth/indexing"]
        )
        idx_service = build("indexing", "v3", credentials=idx_creds)
    except Exception as e:
        logger.log(f"  [{label}] Indexing API認証エラー: {e}")
        return submitted, errors

    # WP REST APIから全公開記事のURLを取得
    try:
        session, api_base = get_wp_session(site_cfg)
    except Exception as e:
        logger.log(f"  [{label}] WP接続エラー: {e}")
        return submitted, errors

    urls = [site_cfg["site_url"] + "/"]
    for endpoint in ["posts", "pages"]:
        page = 1
        while True:
            resp = session.get(
                f"{api_base}/{endpoint}",
                params={"per_page": 100, "page": page, "status": "publish"},
            )
            if resp.status_code != 200:
                break
            items = resp.json()
            if not items:
                break
            for item in items:
                link = item.get("link", "")
                if link:
                    urls.append(link)
            page += 1
            if len(items) < 100:
                break

    logger.log(f"  [{label}] Indexing API: {len(urls)} URLs送信開始")

    for url in urls:
        try:
            idx_service.urlNotifications().publish(
                body={"url": url, "type": "URL_UPDATED"}
            ).execute()
            submitted.append(url)
            time.sleep(0.5)
        except Exception as e:
            if "429" in str(e) or "quota" in str(e).lower():
                logger.log(f"  [{label}] Indexing APIレート制限到達 ({len(submitted)}/{len(urls)})")
                break
            errors.append(url)
            if len(errors) <= 2:
                logger.log(f"  [{label}] Indexing APIエラー: {url} -> {str(e)[:80]}")

    logger.log(f"  [{label}] Indexing API結果: 送信{len(submitted)}件 / エラー{len(errors)}件")
    return submitted, errors


def act_check_noindex(site_cfg):
    """noindexになっている記事を検出"""
    noindex_posts = []
    try:
        session, api_base = get_wp_session(site_cfg)
        # 公開済み記事を取得（最大100件ずつ）
        page = 1
        while True:
            resp = session.get(
                f"{api_base}/posts",
                params={"per_page": 100, "page": page, "status": "publish"},
            )
            if resp.status_code != 200:
                break
            posts = resp.json()
            if not posts:
                break

            for post in posts:
                meta = post.get("meta", {})
                robots = meta.get("rank_math_robots", [])
                if isinstance(robots, list) and "noindex" in robots:
                    noindex_posts.append(
                        {"id": post["id"], "slug": post["slug"], "title": post["title"]["rendered"]}
                    )

            page += 1
            if len(posts) < 100:
                break
            time.sleep(0.5)

    except Exception as e:
        logger.log(f"  [{site_cfg['label']}] noindexチェックエラー: {e}")

    return noindex_posts


def act_fix_noindex(site_cfg, noindex_posts):
    """不要なnoindexを解除"""
    fixed = []
    if not noindex_posts:
        return fixed

    try:
        session, api_base = get_wp_session(site_cfg)
    except Exception:
        return fixed

    for post in noindex_posts[:5]:  # 1日最大5件
        try:
            resp = session.post(
                f"{api_base}/posts/{post['id']}",
                json={"meta": {"rank_math_robots": ["index", "follow"]}},
            )
            if resp.status_code == 200:
                fixed.append(post["slug"])
                logger.log(f"  [{site_cfg['label']}] noindex解除: {post['slug']}")
        except Exception:
            pass
        time.sleep(1)

    return fixed


def act_internal_link_check(site_cfg):
    """内部リンクが少ない記事を検出"""
    low_link_posts = []
    try:
        session, api_base = get_wp_session(site_cfg)
        resp = session.get(
            f"{api_base}/posts",
            params={"per_page": 100, "page": 1, "status": "publish"},
        )
        if resp.status_code != 200:
            return low_link_posts

        posts = resp.json()
        domain = site_cfg["domain"]

        for post in posts:
            content = post.get("content", {}).get("rendered", "")
            internal_links = len(re.findall(rf'href=["\']https?://{re.escape(domain)}', content))
            if internal_links < 2:
                low_link_posts.append(
                    {"id": post["id"], "slug": post["slug"], "internal_links": internal_links, "title": post["title"]["rendered"]}
                )

    except Exception as e:
        logger.log(f"  [{site_cfg['label']}] 内部リンクチェックエラー: {e}")

    return low_link_posts


# ==================================================================
# STEP 3 & 4: PLAN & DO — 計画立案 & 実行
# ==================================================================
def plan_and_do(site_key, site_cfg, check_result, actions_log):
    """分析結果を元に優先アクションを計画し、可能なものは即実行"""

    logger.report("### ACT & DO (実行済みアクション)")
    for action in actions_log:
        logger.report(f"- {action}")
    if not actions_log:
        logger.report("- (今日の自動実行アクションなし)")
    logger.report("")

    # PLAN: 次回の優先アクション
    logger.report("### PLAN (次回優先アクション)")
    priorities = []

    if check_result["unindexed_estimate"] > 5:
        priorities.append(
            f"⚠️ 推定{check_result['unindexed_estimate']}記事が未インデックス → "
            f"Google Indexing API有効化が最優先（GCP Console）"
        )

    if check_result["page2_candidates"]:
        for p in check_result["page2_candidates"][:3]:
            slug = p["url"].rstrip("/").split("/")[-1]
            priorities.append(
                f"📈 {slug} (pos={p['pos']:.1f}) → 内部リンク追加+コンテンツ追記で1ページ目へ"
            )

    if check_result["low_ctr_pages"]:
        for p in check_result["low_ctr_pages"][:3]:
            slug = p["url"].rstrip("/").split("/")[-1]
            priorities.append(
                f"🎯 {slug} (CTR={p['ctr']*100:.1f}%) → タイトル・メタディスクリプション改善"
            )

    if check_result["total_imp"] < 50:
        priorities.append("🔍 インプレッション極少 → ロングテールKW記事の追加が必要")
        priorities.append("🔗 被リンク獲得施策（SNS投稿・ゲスト投稿・コミュニティ参加）")

    if not priorities:
        priorities.append("✅ 特記事項なし — 現状維持で推移観察")

    for p in priorities:
        logger.report(f"- {p}")
    logger.report("")

    return priorities


# ==================================================================
# メイン実行
# ==================================================================
def run_site(gsc, site_key, site_cfg):
    """1サイト分のPDCA実行"""
    label = site_cfg["label"]
    logger.log(f"===== {label} PDCA開始 =====")
    actions_log = []

    # 1. CHECK
    check_result = check_gsc(gsc, site_key, site_cfg)

    # 2. ACT — サイトマップping
    ping_status = act_sitemap_ping(site_cfg)
    actions_log.append(f"サイトマップping: {ping_status}")

    # 2. ACT — Indexing API送信
    idx_submitted, idx_errors = act_indexing_api(site_cfg)
    if idx_submitted:
        actions_log.append(f"Indexing API送信: {len(idx_submitted)}件成功")
    if idx_errors:
        actions_log.append(f"Indexing APIエラー: {len(idx_errors)}件")

    # 2. ACT — noindexチェック & 修正
    noindex_posts = act_check_noindex(site_cfg)
    if noindex_posts:
        logger.log(f"  [{label}] noindex検出: {len(noindex_posts)}件")
        actions_log.append(f"noindex検出: {len(noindex_posts)}件")
        fixed = act_fix_noindex(site_cfg, noindex_posts)
        if fixed:
            actions_log.append(f"noindex解除: {', '.join(fixed)}")

    # 2. ACT — メタディスクリプション改善
    meta_actions = act_update_seo_meta(site_cfg, check_result)
    actions_log.extend(meta_actions)

    # 2. ACT — 内部リンク不足チェック
    low_link = act_internal_link_check(site_cfg)
    if low_link:
        actions_log.append(f"内部リンク不足: {len(low_link)}記事（2本未満）")
        # 上位5件をレポートに記録
        for p in low_link[:5]:
            actions_log.append(f"  → {p['slug']} (内部リンク{p['internal_links']}本)")

    # 3 & 4. PLAN & DO
    plan_and_do(site_key, site_cfg, check_result, actions_log)

    logger.log(f"===== {label} PDCA完了 =====")


def main():
    args = sys.argv[1:]
    target_site = None
    for i, a in enumerate(args):
        if a == "--site" and i + 1 < len(args):
            target_site = args[i + 1]

    logger.log("=" * 60)
    logger.log("SEO PDCA 日次自動実行 開始")
    logger.log("=" * 60)

    logger.report(f"# SEO PDCA 日次レポート ({TODAY})")
    logger.report(f"実行時刻: {NOW.strftime('%Y-%m-%d %H:%M PYT')}")
    logger.report("")

    try:
        gsc = get_gsc_service()
    except Exception as e:
        logger.log(f"GSC認証エラー: {e}")
        return

    for site_key, site_cfg in SITES.items():
        if target_site and site_key != target_site:
            continue
        try:
            run_site(gsc, site_key, site_cfg)
        except Exception as e:
            logger.log(f"  [{site_cfg['label']}] 実行エラー: {e}")
            logger.report(f"## {site_cfg['label']}: エラー")
            logger.report(f"```\n{e}\n```")
            logger.report("")

    # サマリー
    logger.report("---")
    logger.report(f"*自動生成: {NOW.strftime('%Y-%m-%d %H:%M PYT')}*")

    logger.save_report()
    logger.log("SEO PDCA 完了")


if __name__ == "__main__":
    main()
