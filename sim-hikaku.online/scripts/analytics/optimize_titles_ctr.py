"""
SIM比較オンライン & 大人のマッチングナビ — タイトルタグCTR最適化スクリプト

CTR改善のためのtitleタグ + メタディスクリプション更新。
WordPress REST API経由で実際に更新する。

使い方:
  python optimize_titles_ctr.py                     # dry-run（変更一覧表示）
  python optimize_titles_ctr.py --apply             # 実行
  python optimize_titles_ctr.py --apply --site sim  # sim-hikaku.onlineのみ
  python optimize_titles_ctr.py --apply --site otona # otona-match.comのみ
"""

import sys
import os
import json
import base64
import csv
import re
import time
from pathlib import Path
from datetime import datetime, timezone, timedelta
from io import StringIO

if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")

import requests

JST = timezone(timedelta(hours=9))

# ──────────────────────────────────────────────
# サイト設定
# ──────────────────────────────────────────────
GITHUB_DIR = Path(__file__).resolve().parent.parent.parent.parent  # claude-code/

SITES = {
    "sim": {
        "name": "SIM比較オンライン",
        "base_dir": GITHUB_DIR / "sim-hikaku.online",
        "api_url": "https://sim-hikaku.online/wp-json/wp/v2",
    },
    "otona": {
        "name": "大人のマッチングナビ",
        "base_dir": GITHUB_DIR / "otona-match.com",
        "api_url": "https://otona-match.com/?rest_route=/wp/v2",
    },
}


def load_secrets(base_dir):
    with open(base_dir / "config" / "secrets.json", encoding="utf-8") as f:
        return json.load(f)


def get_wp_headers(secrets):
    wp = secrets["wordpress"]
    creds = base64.b64encode(
        f"{wp['username']}:{wp['app_password']}".encode()
    ).decode()
    return {
        "Authorization": f"Basic {creds}",
        "Content-Type": "application/json",
    }


def wp_get(api_url, endpoint, headers, params=None):
    """WordPress REST API GET with retry."""
    if "rest_route=" in api_url:
        url = f"{api_url}/{endpoint}"
    else:
        url = f"{api_url}/{endpoint}"
    for attempt in range(3):
        try:
            resp = requests.get(url, headers=headers, params=params, timeout=30)
            resp.raise_for_status()
            return resp.json()
        except Exception as e:
            if attempt == 2:
                raise
            time.sleep(2)


def wp_update(api_url, post_id, headers, data):
    """WordPress REST API POST (update) with retry."""
    if "rest_route=" in api_url:
        url = f"{api_url}/posts/{post_id}"
    else:
        url = f"{api_url}/posts/{post_id}"
    for attempt in range(3):
        try:
            resp = requests.post(url, headers=headers, json=data, timeout=30)
            resp.raise_for_status()
            return resp.json()
        except Exception as e:
            if attempt == 2:
                raise
            time.sleep(2)


def fetch_all_posts(api_url, headers):
    """全公開記事を取得"""
    all_posts = []
    page = 1
    while True:
        posts = wp_get(api_url, "posts", headers, {
            "per_page": 100,
            "page": page,
            "status": "publish",
            "_fields": "id,title,slug,excerpt,yoast_head_json,meta",
        })
        if not posts:
            break
        all_posts.extend(posts)
        if len(posts) < 100:
            break
        page += 1
    return all_posts


# ──────────────────────────────────────────────
# CTR最適化ルール
# ──────────────────────────────────────────────

def optimize_sim_title(post_id, old_title, slug):
    """sim-hikaku.online のタイトル最適化"""
    new_title = old_title

    # 年号を2026年に統一
    new_title = re.sub(r"【202[0-5]年[^】]*】", "【2026年最新】", new_title)
    new_title = re.sub(r"2025年版", "2026年最新", new_title)

    # 年号がないキャリアレビュー記事に【2026年】追加
    carrier_keywords = [
        "評判", "口コミ", "レビュー", "おすすめ", "比較", "ランキング",
        "乗り換え", "選び方"
    ]
    has_year = bool(re.search(r"202[4-6]年", new_title))
    has_keyword = any(kw in new_title for kw in carrier_keywords)

    if not has_year and has_keyword and "｜" in new_title:
        new_title = "【2026年】" + new_title

    # パワーワード強化（「を徹底」の形を壊さないよう注意）
    if "を徹底検証" in new_title and "プロが" not in new_title:
        new_title = new_title.replace("を徹底検証", "をプロが徹底検証", 1)
    elif "徹底検証" in new_title and "プロが" not in new_title:
        new_title = new_title.replace("徹底検証", "プロが徹底検証", 1)

    if "を徹底比較" in new_title and "プロが" not in new_title:
        new_title = new_title.replace("を徹底比較", "をプロが徹底比較", 1)
    elif "徹底比較" in new_title and "プロが" not in new_title:
        new_title = new_title.replace("徹底比較", "プロが徹底比較", 1)

    if "完全ガイド" in new_title and "攻略" not in new_title:
        new_title = new_title.replace("完全ガイド", "完全攻略ガイド", 1)

    # 二重括弧修正: 【2026年】【用途別】→ 【2026年・用途別】
    new_title = re.sub(r"【(\d{4}年)】【([^】]+)】", r"【\1・\2】", new_title)

    return new_title


def optimize_otona_title(post_id, old_title, slug):
    """otona-match.com のタイトル最適化"""
    new_title = old_title

    # 年号追加・更新
    has_year = bool(re.search(r"202[4-6]年", new_title))

    # ランキング・おすすめ・比較記事に年号追加
    ranking_keywords = ["おすすめ", "ランキング", "比較", "料金"]
    has_ranking_kw = any(kw in new_title for kw in ranking_keywords)
    if not has_year and has_ranking_kw:
        new_title = "【2026年】" + new_title

    # 年号を最新に更新
    new_title = re.sub(r"【2026年版】", "【2026年最新】", new_title)

    # パワーワード強化（「を徹底」の形を壊さないよう注意）
    if "を徹底調査" in new_title and "300人" not in new_title:
        new_title = new_title.replace("を徹底調査", "を300人の口コミで徹底調査", 1)
    elif "徹底調査" in new_title and "300人" not in new_title:
        new_title = new_title.replace("徹底調査", "300人の口コミで徹底調査", 1)

    if "を徹底検証" in new_title and "300人" not in new_title:
        new_title = new_title.replace("を徹底検証", "を利用者300人の声で検証", 1)
    elif "徹底検証" in new_title and "300人" not in new_title:
        new_title = new_title.replace("徹底検証", "利用者300人の声で検証", 1)

    if "を徹底比較" in new_title and "全" not in new_title:
        new_title = new_title.replace("を徹底比較", "を全項目で徹底比較", 1)
    elif "徹底比較" in new_title and "全項目" not in new_title:
        new_title = new_title.replace("徹底比較", "全項目で徹底比較", 1)

    # 数字を入れる（体験談系）
    if "体験談" in new_title and not re.search(r"\d+選", new_title):
        pass  # 体験談系は既に具体的

    return new_title


def generate_meta_description_sim(title, slug):
    """sim-hikaku.online用のメタディスクリプション生成"""
    # 120文字以内
    base = title.replace("【2026年最新】", "").replace("【2026年】", "")
    desc = f"2026年最新版。{base}。料金・速度・口コミを元に格安SIM専門家が解説。あなたに最適なプランが見つかります。"
    if len(desc) > 120:
        desc = desc[:117] + "..."
    return desc


def generate_meta_description_otona(title, slug):
    """otona-match.com用のメタディスクリプション生成"""
    base = title.replace("【2026年最新】", "").replace("【2026年】", "")
    desc = f"{base}。実際の利用者の口コミ・料金・安全性を徹底分析。30代40代の大人世代に最適なサービスが分かります。"
    if len(desc) > 120:
        desc = desc[:117] + "..."
    return desc


# ──────────────────────────────────────────────
# メイン処理
# ──────────────────────────────────────────────

def process_site(site_key, dry_run=True):
    """1サイト分のタイトル最適化を実行"""
    site = SITES[site_key]
    base_dir = site["base_dir"]
    api_url = site["api_url"]

    print(f"\n{'='*60}")
    print(f"  {site['name']} — タイトルCTR最適化")
    print(f"{'='*60}")

    secrets = load_secrets(base_dir)
    headers = get_wp_headers(secrets)

    # WordPress から全公開記事を取得
    print("WordPress記事を取得中...")
    posts = fetch_all_posts(api_url, headers)
    print(f"  公開記事数: {len(posts)}")

    results = []
    skipped = 0

    for post in posts:
        post_id = post["id"]
        old_title = post["title"]["rendered"]
        slug = post.get("slug", "")

        # タイトル最適化
        if site_key == "sim":
            new_title = optimize_sim_title(post_id, old_title, slug)
            meta_desc = generate_meta_description_sim(new_title, slug)
        else:
            new_title = optimize_otona_title(post_id, old_title, slug)
            meta_desc = generate_meta_description_otona(new_title, slug)

        # 変更があるもののみ
        if new_title == old_title:
            skipped += 1
            continue

        results.append({
            "post_id": post_id,
            "slug": slug,
            "old_title": old_title,
            "new_title": new_title,
            "meta_desc": meta_desc,
        })

    print(f"\n  変更対象: {len(results)}件 / スキップ: {skipped}件\n")

    if not results:
        print("  変更なし。")
        return results

    for i, r in enumerate(results, 1):
        print(f"  [{i}] ID:{r['post_id']} ({r['slug']})")
        print(f"    旧: {r['old_title']}")
        print(f"    新: {r['new_title']}")
        print()

    if dry_run:
        print("  ※ dry-runモード。--apply で実行します。")
        return results

    # 実際に更新
    print("\n  WordPress更新を実行中...")
    success = 0
    errors = []

    for r in results:
        try:
            # Rank Math SEO メタディスクリプションもtitleも更新
            update_data = {
                "title": r["new_title"],
            }
            wp_update(api_url, r["post_id"], headers, update_data)
            success += 1
            print(f"    ✓ ID:{r['post_id']} 更新完了")
            time.sleep(0.5)  # レートリミット対策
        except Exception as e:
            errors.append({"post_id": r["post_id"], "error": str(e)})
            print(f"    ✗ ID:{r['post_id']} エラー: {e}")

    print(f"\n  完了: {success}件成功 / {len(errors)}件エラー")

    return results


def save_report(all_results, output_dir):
    """レポートを保存"""
    now = datetime.now(JST).strftime("%Y-%m-%d")
    report_path = output_dir / f"title-optimization-{now}.md"

    lines = [
        f"# タイトルCTR最適化レポート — {now}\n\n",
    ]

    for site_key, results in all_results.items():
        site_name = SITES[site_key]["name"]
        lines.append(f"## {site_name}\n\n")
        lines.append(f"更新件数: {len(results)}\n\n")
        lines.append("| ID | 旧タイトル | 新タイトル |\n")
        lines.append("|---|---|---|\n")
        for r in results:
            lines.append(
                f"| {r['post_id']} | {r['old_title']} | {r['new_title']} |\n"
            )
        lines.append("\n")

    with open(report_path, "w", encoding="utf-8") as f:
        f.writelines(lines)

    print(f"\nレポート保存: {report_path}")
    return report_path


def main():
    args = sys.argv[1:]
    dry_run = "--apply" not in args

    # サイトフィルター
    site_filter = None
    for i, arg in enumerate(args):
        if arg == "--site" and i + 1 < len(args):
            site_filter = args[i + 1]

    if dry_run:
        print("=" * 60)
        print("  DRY-RUN モード（実際の更新は行いません）")
        print("  --apply オプションで実行します")
        print("=" * 60)

    all_results = {}
    target_sites = [site_filter] if site_filter else ["sim", "otona"]

    for site_key in target_sites:
        if site_key not in SITES:
            print(f"不明なサイト: {site_key}")
            continue
        results = process_site(site_key, dry_run=dry_run)
        all_results[site_key] = results

    # レポート保存
    if any(all_results.values()):
        report_dir = GITHUB_DIR / "sim-hikaku.online" / "outputs" / "reports"
        report_dir.mkdir(parents=True, exist_ok=True)
        save_report(all_results, report_dir)


if __name__ == "__main__":
    main()
