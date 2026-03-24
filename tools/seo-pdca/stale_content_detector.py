"""
古い記事・パフォーマンス低下記事の自動検出スクリプト
3サイト共通で以下を検出:
  1. 公開60日以上でインプレッション0の記事（GSCで未露出）
  2. 過去30日のインプレッションが前30日比で50%以上減少した記事
  3. CTR 1%未満の記事（順位10位以内なのにクリックされない）

daily_all_business_pdca.py から呼ばれる + 単独実行も可

出力: logs/stale-content-YYYY-MM-DD.md
"""
import sys
import json
import time
import re
from datetime import datetime, timedelta, timezone
from pathlib import Path

if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")

import requests
from google.oauth2 import service_account
from googleapiclient.discovery import build

SCRIPT_DIR = Path(__file__).parent
REPO_ROOT = SCRIPT_DIR.parent.parent.parent
SITES_DIR = REPO_ROOT / "sites"
CRED_PATH = REPO_ROOT / "infrastructure" / "tools" / "sheets-sync" / "credentials" / "service-account.json"
LOG_DIR = REPO_ROOT / "logs"
PYT = timezone(timedelta(hours=-3))
NOW = datetime.now(PYT)
TODAY = NOW.strftime("%Y-%m-%d")

SITES = {
    "nambei": {
        "label": "南米おやじ",
        "domain": "nambei-oyaji.com",
        "site_url": "https://nambei-oyaji.com",
        "gsc_url": "https://nambei-oyaji.com/",
        "use_secrets": False,
    },
    "otona": {
        "label": "マッチングナビ",
        "domain": "otona-match.com",
        "site_url": "https://otona-match.com",
        "gsc_url": "https://otona-match.com/",
        "use_secrets": True,
    },
    "sim": {
        "label": "SIM比較",
        "domain": "sim-hikaku.online",
        "site_url": "https://sim-hikaku.online",
        "gsc_url": "https://sim-hikaku.online/",
        "use_secrets": True,
    },
}


def get_wp_session(site_dir, site_url, use_secrets):
    config_dir = site_dir / "config"
    if use_secrets:
        secrets = json.loads((config_dir / "secrets.json").read_text(encoding="utf-8"))
        wp = secrets.get("wordpress", {})
        base_url = wp.get("site_url", wp.get("url", site_url))
        username, password = wp.get("username", ""), wp.get("app_password", "")
    else:
        cred = json.loads((config_dir / "wp-credentials.json").read_text(encoding="utf-8"))
        base_url = cred.get("site_url", site_url)
        username, password = cred.get("username", ""), cred.get("app_password", "")
    if not username:
        return None, None
    s = requests.Session()
    s.auth = (username, password)
    return s, f"{base_url.rstrip('/')}/wp-json/wp/v2"


def detect_stale(gsc, site_key, cfg):
    """1サイト分の古い記事検出"""
    label = cfg["label"]
    site_dir = SITES_DIR / cfg["domain"]
    results = {"zero_imp": [], "declining": [], "low_ctr": []}

    # WPから全公開記事取得
    session, api_base = get_wp_session(site_dir, cfg["site_url"], cfg["use_secrets"])
    if not session:
        return results

    all_posts = []
    page = 1
    while True:
        resp = session.get(f"{api_base}/posts", params={"per_page": 100, "page": page, "status": "publish"})
        if resp.status_code != 200:
            break
        posts = resp.json()
        if not posts:
            break
        all_posts.extend(posts)
        page += 1
        if len(posts) < 100:
            break

    # GSC: 過去30日 & 前30日
    end = (datetime.now() - timedelta(days=3)).strftime("%Y-%m-%d")
    start_now = (datetime.now() - timedelta(days=33)).strftime("%Y-%m-%d")
    start_prev = (datetime.now() - timedelta(days=63)).strftime("%Y-%m-%d")
    end_prev = (datetime.now() - timedelta(days=33)).strftime("%Y-%m-%d")

    try:
        resp_now = gsc.searchanalytics().query(
            siteUrl=cfg["gsc_url"],
            body={"startDate": start_now, "endDate": end, "dimensions": ["page"], "rowLimit": 1000, "type": "web"},
        ).execute()
        resp_prev = gsc.searchanalytics().query(
            siteUrl=cfg["gsc_url"],
            body={"startDate": start_prev, "endDate": end_prev, "dimensions": ["page"], "rowLimit": 1000, "type": "web"},
        ).execute()
    except Exception as e:
        print(f"  [{label}] GSCエラー: {e}")
        return results

    now_data = {r["keys"][0]: r for r in resp_now.get("rows", [])}
    prev_data = {r["keys"][0]: r for r in resp_prev.get("rows", [])}

    for post in all_posts:
        link = post.get("link", "")
        title = post.get("title", {}).get("rendered", "?")
        pub_date_str = post.get("date", "")[:10]
        slug = post.get("slug", "")

        # 公開日チェック
        try:
            pub_date = datetime.strptime(pub_date_str, "%Y-%m-%d")
            days_old = (datetime.now() - pub_date).days
        except Exception:
            days_old = 0

        # GSCデータ照合
        now_row = now_data.get(link) or now_data.get(link.rstrip("/") + "/") or now_data.get(link.rstrip("/"))
        prev_row = prev_data.get(link) or prev_data.get(link.rstrip("/") + "/") or prev_data.get(link.rstrip("/"))

        now_imp = now_row.get("impressions", 0) if now_row else 0
        prev_imp = prev_row.get("impressions", 0) if prev_row else 0
        now_ctr = now_row.get("ctr", 0) if now_row else 0
        now_pos = now_row.get("position", 99) if now_row else 99

        # 1. 公開60日以上でインプレッション0
        if days_old >= 60 and now_imp == 0:
            results["zero_imp"].append({"slug": slug, "title": title[:50], "days_old": days_old})

        # 2. インプレッション50%以上減少
        if prev_imp >= 5 and now_imp < prev_imp * 0.5:
            results["declining"].append({
                "slug": slug, "title": title[:50],
                "now_imp": now_imp, "prev_imp": prev_imp,
                "decline_pct": round((1 - now_imp / prev_imp) * 100),
            })

        # 3. 順位10位以内でCTR 1%未満
        if now_pos <= 10 and now_ctr < 0.01 and now_imp >= 10:
            results["low_ctr"].append({
                "slug": slug, "title": title[:50],
                "pos": round(now_pos, 1), "ctr": round(now_ctr * 100, 2), "imp": now_imp,
            })

    return results


def main():
    print("古い記事検出 開始...")
    creds = service_account.Credentials.from_service_account_file(
        str(CRED_PATH), scopes=["https://www.googleapis.com/auth/webmasters.readonly"]
    )
    gsc = build("searchconsole", "v1", credentials=creds)

    report = [f"# 古い記事・パフォーマンス低下 検出レポート ({TODAY})", ""]

    for site_key, cfg in SITES.items():
        label = cfg["label"]
        print(f"  [{label}] 検出中...")
        results = detect_stale(gsc, site_key, cfg)

        report.append(f"## {label}")
        report.append("")

        if results["zero_imp"]:
            report.append(f"### インプレッション0（公開60日以上）: {len(results['zero_imp'])}件")
            for r in results["zero_imp"][:10]:
                report.append(f"- `{r['slug']}` ({r['days_old']}日前公開)")
            report.append("")

        if results["declining"]:
            report.append(f"### インプレッション急減（50%以上減）: {len(results['declining'])}件")
            for r in results["declining"]:
                report.append(f"- `{r['slug']}` {r['prev_imp']}→{r['now_imp']} (-{r['decline_pct']}%)")
            report.append("")

        if results["low_ctr"]:
            report.append(f"### CTR改善候補（順位10位内・CTR<1%）: {len(results['low_ctr'])}件")
            for r in results["low_ctr"]:
                report.append(f"- `{r['slug']}` pos={r['pos']} CTR={r['ctr']}% imp={r['imp']}")
            report.append("")

        if not results["zero_imp"] and not results["declining"] and not results["low_ctr"]:
            report.append("- 特記事項なし")
            report.append("")

    report.append("---")
    report.append(f"*自動生成: {NOW.strftime('%Y-%m-%d %H:%M PYT')}*")

    out_path = LOG_DIR / f"stale-content-{TODAY}.md"
    out_path.write_text("\n".join(report), encoding="utf-8")
    print(f"レポート保存: {out_path}")

    return report


if __name__ == "__main__":
    main()
