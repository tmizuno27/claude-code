#!/usr/bin/env python3
"""
CTR最適化スクリプト — sim-hikaku.online

GSCデータから「表示されているのにクリックされない記事」を特定し、
タイトル・メタディスクリプションをWordPress REST APIで更新する。

使い方:
  python ctr_optimizer.py                  # GSCデータ取得+分析のみ（dry-run）
  python ctr_optimizer.py --apply          # 実際にWordPressを更新
  python ctr_optimizer.py --days 28        # 過去28日間のデータで分析（デフォルト14日）
  python ctr_optimizer.py --min-impressions 5  # 最低表示回数の閾値（デフォルト3）
"""

import sys
import os
import json
import base64
import time
import re
from pathlib import Path
from datetime import datetime, timezone, timedelta

if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")

import requests

# ──────────────────────────────────────────────
# パス設定
# ──────────────────────────────────────────────
SCRIPT_DIR = Path(__file__).resolve().parent
SITE_DIR = SCRIPT_DIR.parent.parent  # sim-hikaku.online/
CONFIG_DIR = SITE_DIR / "config"
REPORTS_DIR = SITE_DIR / "outputs" / "reports"
REPORTS_DIR.mkdir(parents=True, exist_ok=True)

JST = timezone(timedelta(hours=9))


# ──────────────────────────────────────────────
# GSCデータ取得
# ──────────────────────────────────────────────
def fetch_gsc_page_data(days=14):
    """GSCからページ別の表示回数・クリック・CTR・順位を取得"""
    settings_path = CONFIG_DIR / "settings.json"
    with open(settings_path, encoding="utf-8") as f:
        settings = json.load(f)

    sc_config = settings.get("search_console", {})
    site_url = sc_config.get("site_url", "")
    cred_path = sc_config.get("credentials_file", "gsc-credentials.json")
    cred_file = CONFIG_DIR / cred_path

    if not site_url or not cred_file.exists():
        print("ERROR: Search Console 認証情報がありません")
        return []

    from google.oauth2 import service_account
    from googleapiclient.discovery import build

    credentials = service_account.Credentials.from_service_account_file(
        str(cred_file),
        scopes=["https://www.googleapis.com/auth/webmasters.readonly"],
    )
    service = build("searchconsole", "v1", credentials=credentials)

    end_date = datetime.now() - timedelta(days=3)  # GSCデータは3日遅れ
    start_date = end_date - timedelta(days=days)

    # ページ別データ取得
    response = service.searchanalytics().query(
        siteUrl=site_url,
        body={
            "startDate": start_date.strftime("%Y-%m-%d"),
            "endDate": end_date.strftime("%Y-%m-%d"),
            "dimensions": ["page"],
            "rowLimit": 500,
        },
    ).execute()

    pages = []
    for row in response.get("rows", []):
        pages.append({
            "page": row["keys"][0],
            "clicks": row.get("clicks", 0),
            "impressions": row.get("impressions", 0),
            "ctr": round(row.get("ctr", 0) * 100, 2),
            "position": round(row.get("position", 0), 1),
        })

    # クエリ別データも取得（ページとクエリの組み合わせ）
    query_response = service.searchanalytics().query(
        siteUrl=site_url,
        body={
            "startDate": start_date.strftime("%Y-%m-%d"),
            "endDate": end_date.strftime("%Y-%m-%d"),
            "dimensions": ["page", "query"],
            "rowLimit": 1000,
        },
    ).execute()

    page_queries = {}
    for row in query_response.get("rows", []):
        page_url = row["keys"][0]
        query = row["keys"][1]
        if page_url not in page_queries:
            page_queries[page_url] = []
        page_queries[page_url].append({
            "query": query,
            "clicks": row.get("clicks", 0),
            "impressions": row.get("impressions", 0),
            "ctr": round(row.get("ctr", 0) * 100, 2),
            "position": round(row.get("position", 0), 1),
        })

    return pages, page_queries


# ──────────────────────────────────────────────
# WordPress API
# ──────────────────────────────────────────────
def load_wp_auth():
    """WordPress認証情報を取得"""
    with open(CONFIG_DIR / "secrets.json", encoding="utf-8") as f:
        secrets = json.load(f)
    wp = secrets["wordpress"]
    creds = base64.b64encode(
        f"{wp['username']}:{wp['app_password']}".encode()
    ).decode()
    return {
        "api_url": wp["api_url"],
        "headers": {
            "Authorization": f"Basic {creds}",
            "Content-Type": "application/json",
        },
    }


def fetch_all_wp_posts(api_url, headers):
    """全公開記事を取得"""
    all_posts = []
    page = 1
    while True:
        resp = requests.get(
            f"{api_url}/posts",
            headers=headers,
            params={
                "per_page": 100,
                "page": page,
                "status": "publish",
                "_fields": "id,title,slug,link,excerpt",
            },
            timeout=30,
        )
        if resp.status_code != 200:
            break
        posts = resp.json()
        if not posts:
            break
        all_posts.extend(posts)
        if len(posts) < 100:
            break
        page += 1
    return all_posts


def update_wp_post(api_url, headers, post_id, data):
    """記事を更新（リトライ付き）"""
    for attempt in range(3):
        try:
            resp = requests.post(
                f"{api_url}/posts/{post_id}",
                headers=headers,
                json=data,
                timeout=30,
            )
            resp.raise_for_status()
            return resp.json()
        except Exception as e:
            if attempt == 2:
                raise
            time.sleep(2)


# ──────────────────────────────────────────────
# CTR改善ロジック
# ──────────────────────────────────────────────
def identify_low_ctr_pages(pages, page_queries, min_impressions=3):
    """
    CTR改善が必要なページを特定:
    - 表示回数 >= min_impressions
    - CTR < 3%（10位以内）or CTR < 1.5%（11-20位）
    - impressionsでソート（改善インパクト大）
    """
    candidates = []
    for p in pages:
        impressions = p["impressions"]
        ctr = p["ctr"]
        position = p["position"]

        if impressions < min_impressions:
            continue

        # CTR閾値: 順位に応じた期待CTR
        if position <= 3:
            expected_ctr = 8.0
        elif position <= 5:
            expected_ctr = 5.0
        elif position <= 10:
            expected_ctr = 3.0
        elif position <= 20:
            expected_ctr = 1.5
        else:
            expected_ctr = 0.5

        if ctr < expected_ctr:
            top_queries = sorted(
                page_queries.get(p["page"], []),
                key=lambda q: q["impressions"],
                reverse=True,
            )[:5]
            candidates.append({
                **p,
                "expected_ctr": expected_ctr,
                "gap": round(expected_ctr - ctr, 2),
                "top_queries": top_queries,
            })

    # インパクト順（表示回数 x CTRギャップ）
    candidates.sort(key=lambda x: x["impressions"] * x["gap"], reverse=True)
    return candidates


def generate_optimized_title(old_title, top_queries, position):
    """検索クエリに基づいてタイトルを最適化（CTR 0%対策で積極的に変更）"""
    new_title = old_title

    # 年号を2026年に統一
    new_title = re.sub(r"【202[0-5]年[^】]*】", "【2026年最新】", new_title)

    # 年号がなければ追加（比較・おすすめ・レビュー系）
    ctr_keywords = ["評判", "口コミ", "おすすめ", "比較", "ランキング", "乗り換え", "選び方", "料金"]
    has_year = bool(re.search(r"202[4-6]年", new_title))
    has_keyword = any(kw in new_title for kw in ctr_keywords)
    if not has_year and has_keyword:
        new_title = "【2026年最新】" + new_title

    # 上位検索クエリのキーワードをタイトルに反映
    if top_queries:
        top_query = top_queries[0]["query"]
        # 「評判」「口コミ」が検索されているのにタイトルにない場合
        for kw in ["評判", "口コミ", "デメリット", "メリット"]:
            if kw in top_query and kw not in new_title:
                if "｜" in new_title:
                    parts = new_title.split("｜", 1)
                    new_title = f"{parts[0]}の{kw}｜{parts[1]}"
                break

        # 検索クエリに「価格」があるのにタイトルに「料金」しかない場合、両方入れる
        query_words = set()
        for q in top_queries[:3]:
            query_words.update(q["query"].split())

        # 「価格」が検索されてるなら「料金・価格」にする
        if "価格" in query_words and "価格" not in new_title and "料金" in new_title:
            new_title = new_title.replace("料金比較", "料金・価格比較", 1)

        # GB数が検索KWにあればタイトルに反映
        for word in query_words:
            gb_match = re.match(r"(\d+)gb", word, re.IGNORECASE)
            if gb_match and gb_match.group(0).lower() not in new_title.lower():
                # 「一覧表」の前に具体的GB数を追加
                if "一覧" in new_title and "1GB" not in new_title:
                    new_title = new_title.replace(
                        "一覧表", f"一覧表｜1GB〜{gb_match.group(1)}GBの最安がわかる", 1
                    )
                    break

    # CTRパワーワード追加（積極的）
    # 「最安プランはどこ？」→「最安プランはここだ！元通信社員が厳選」
    if "最安プランはどこ" in new_title:
        new_title = new_title.replace("最安プランはどこ？", "最安プランを元通信社員が厳選")

    # 「完全ガイド」→「完全攻略ガイド」
    if "完全ガイド" in new_title and "攻略" not in new_title:
        new_title = new_title.replace("完全ガイド", "完全攻略ガイド")

    # 「あなたに最適なSIMが見つかる」→ もっと具体的に
    if "あなたに最適なSIMが見つかる" in new_title:
        new_title = new_title.replace(
            "あなたに最適なSIMが見つかる", "3分診断で最適SIMがわかる"
        )

    # 「月額0円〜」系の数字はそのまま活かす（具体的数字はCTR高い）

    # 「障害対策も万全」→ もっと緊急感
    if "障害対策も万全" in new_title:
        new_title = new_title.replace("障害対策も万全", "通信障害に備える保険SIM")

    # 数字を強調（CTR向上に効果的）
    has_number = bool(re.search(r"\d+選|\d+社|\d+ステップ|\d+つ|\d+個", new_title))
    if not has_number and "比較" in new_title:
        if "プロが" not in new_title and "徹底" in new_title:
            new_title = new_title.replace("徹底比較", "プロが徹底比較", 1)
            new_title = new_title.replace("徹底検証", "プロが徹底検証", 1)

    # 二重括弧修正
    new_title = re.sub(r"【(\d{4}年[^】]*)】【([^】]+)】", r"【\1・\2】", new_title)

    # タイトル長制限（60文字以内）
    if len(new_title) > 60:
        if "｜" in new_title:
            parts = new_title.split("｜")
            main = parts[0]
            sub = "｜".join(parts[1:])
            if len(sub) > 25:
                sub = sub[:22] + "..."
            new_title = f"{main}｜{sub}"

    return new_title


def generate_meta_description(title, top_queries, slug):
    """検索クエリに基づいてメタディスクリプションを生成"""
    # タイトルから装飾を除去
    base = re.sub(r"【[^】]+】", "", title).strip()

    # 上位クエリを含める
    query_keywords = set()
    for q in top_queries[:3]:
        for word in q["query"].split():
            if len(word) >= 2:
                query_keywords.add(word)

    # 120文字以内のメタディスクリプション
    desc = f"2026年最新版。{base}。"

    # クエリキーワードを自然に含める
    kw_phrases = []
    if any("料金" in kw for kw in query_keywords):
        kw_phrases.append("料金プランを詳細比較")
    if any("速度" in kw for kw in query_keywords):
        kw_phrases.append("通信速度の実測データ付き")
    if any("評判" in kw or "口コミ" in kw for kw in query_keywords):
        kw_phrases.append("実際の利用者の口コミを分析")
    if any("乗り換え" in kw for kw in query_keywords):
        kw_phrases.append("乗り換え手順を図解で解説")

    if kw_phrases:
        desc += "・".join(kw_phrases[:2]) + "。"

    desc += "あなたに最適なプランが見つかります。"

    if len(desc) > 120:
        desc = desc[:117] + "..."

    return desc


# ──────────────────────────────────────────────
# メイン処理
# ──────────────────────────────────────────────
def main():
    import argparse
    parser = argparse.ArgumentParser(description="CTR最適化スクリプト")
    parser.add_argument("--apply", action="store_true", help="実際にWordPressを更新")
    parser.add_argument("--days", type=int, default=14, help="GSCデータの期間（日数）")
    parser.add_argument("--min-impressions", type=int, default=3, help="最低表示回数")
    args = parser.parse_args()

    print("=" * 60)
    print("  SIM比較オンライン — CTR最適化")
    print(f"  期間: 過去{args.days}日間 / 最低表示回数: {args.min_impressions}")
    if not args.apply:
        print("  モード: DRY-RUN（--apply で実際に更新）")
    print("=" * 60)

    # 1. GSCデータ取得
    print("\n[1/4] GSCデータを取得中...")
    try:
        pages, page_queries = fetch_gsc_page_data(days=args.days)
    except Exception as e:
        print(f"  GSCデータ取得エラー: {e}")
        print("  → Search Console APIの認証情報を確認してください")
        print("  → gsc-credentials.json のサービスアカウントに")
        print("    Search Consoleの読み取り権限が付与されているか確認")
        return

    print(f"  取得ページ数: {len(pages)}")

    if not pages:
        print("\n  GSCデータが0件です。考えられる原因:")
        print("  1. サイトがまだインデックスされていない")
        print("  2. サービスアカウントにGSCの権限がない")
        print("  3. GSCのプロパティURLが正しくない")
        print("\n  対処法:")
        print("  - Google Search Console で手動でURL検査・インデックス登録を実行")
        print("  - gsc_index_request.py で全URLのインデックス登録を送信")
        print("  - サービスアカウントのメールアドレスをGSCのユーザーに追加")

        # GSCデータなしでもWordPressの記事を取得してルールベースで最適化
        print("\n  → GSCデータなしでルールベース最適化を実行します...")
        run_rule_based_optimization(args.apply)
        return

    # 全ページの合計を表示
    total_impressions = sum(p["impressions"] for p in pages)
    total_clicks = sum(p["clicks"] for p in pages)
    avg_ctr = round(total_clicks / total_impressions * 100, 2) if total_impressions > 0 else 0
    print(f"  合計表示回数: {total_impressions}")
    print(f"  合計クリック数: {total_clicks}")
    print(f"  平均CTR: {avg_ctr}%")

    # 2. 低CTRページを特定
    print(f"\n[2/4] CTR改善候補を特定中...")
    candidates = identify_low_ctr_pages(pages, page_queries, args.min_impressions)
    print(f"  改善候補: {len(candidates)}件")

    if not candidates:
        print("  CTR改善が必要なページはありません。")
        return

    # 3. WordPress記事を取得してマッチング
    print(f"\n[3/4] WordPress記事を取得中...")
    wp = load_wp_auth()
    wp_posts = fetch_all_wp_posts(wp["api_url"], wp["headers"])
    print(f"  公開記事数: {len(wp_posts)}")

    # URL → WP記事のマッピング
    url_to_post = {}
    for post in wp_posts:
        url_to_post[post["link"].rstrip("/")] = post

    # 4. タイトル・メタ改善案を生成
    print(f"\n[4/4] 改善案を生成中...\n")

    changes = []
    for i, candidate in enumerate(candidates[:20], 1):  # 上位20件
        page_url = candidate["page"].rstrip("/")
        post = url_to_post.get(page_url)

        if not post:
            continue

        old_title = post["title"]["rendered"]
        old_excerpt = post.get("excerpt", {}).get("rendered", "")

        new_title = generate_optimized_title(
            old_title,
            candidate["top_queries"],
            candidate["position"],
        )
        new_meta = generate_meta_description(
            new_title,
            candidate["top_queries"],
            post.get("slug", ""),
        )

        title_changed = new_title != old_title

        if not title_changed:
            # タイトル変更なしでもメタは更新
            pass

        change = {
            "post_id": post["id"],
            "url": page_url,
            "old_title": old_title,
            "new_title": new_title,
            "title_changed": title_changed,
            "new_meta": new_meta,
            "impressions": candidate["impressions"],
            "clicks": candidate["clicks"],
            "ctr": candidate["ctr"],
            "position": candidate["position"],
            "expected_ctr": candidate["expected_ctr"],
            "top_queries": [q["query"] for q in candidate["top_queries"][:3]],
        }
        changes.append(change)

        # 表示
        status = "TITLE+META" if title_changed else "META ONLY"
        print(f"  [{i}] {status} | ID:{post['id']} | 表示:{candidate['impressions']} "
              f"CTR:{candidate['ctr']}% → 目標:{candidate['expected_ctr']}% "
              f"順位:{candidate['position']}")
        if title_changed:
            print(f"      旧: {old_title}")
            print(f"      新: {new_title}")
        print(f"      Meta: {new_meta[:80]}...")
        print(f"      検索KW: {', '.join(change['top_queries'])}")
        print()

    if not changes:
        print("  更新対象なし。")
        return

    # 適用
    if args.apply:
        print(f"\n  WordPress更新を実行中（{len(changes)}件）...")
        success = 0
        errors = []
        for c in changes:
            try:
                update_data = {"excerpt": c["new_meta"]}
                if c["title_changed"]:
                    update_data["title"] = c["new_title"]
                update_wp_post(wp["api_url"], wp["headers"], c["post_id"], update_data)
                success += 1
                label = "タイトル+メタ" if c["title_changed"] else "メタのみ"
                print(f"    OK ID:{c['post_id']} ({label})")
                time.sleep(0.5)
            except Exception as e:
                errors.append({"post_id": c["post_id"], "error": str(e)})
                print(f"    NG ID:{c['post_id']} - {e}")
        print(f"\n  完了: {success}件成功 / {len(errors)}件エラー")
    else:
        print("  ※ dry-runモード。--apply で実行します。")

    # レポート保存
    save_report(changes, pages, total_impressions, total_clicks, avg_ctr, args)


def run_rule_based_optimization(apply=False):
    """GSCデータなしの場合、ルールベースでタイトル・メタを最適化"""
    wp = load_wp_auth()
    wp_posts = fetch_all_wp_posts(wp["api_url"], wp["headers"])
    print(f"  公開記事数: {len(wp_posts)}")

    changes = []
    for post in wp_posts:
        old_title = post["title"]["rendered"]
        new_title = generate_optimized_title(old_title, [], 10)

        # メタディスクリプション生成
        new_meta = generate_meta_description(new_title, [], post.get("slug", ""))

        # excerptが空または自動生成の場合のみ更新
        old_excerpt = post.get("excerpt", {}).get("rendered", "").strip()
        has_custom_excerpt = bool(old_excerpt) and len(old_excerpt) > 50

        title_changed = new_title != old_title
        meta_needed = not has_custom_excerpt

        if not title_changed and not meta_needed:
            continue

        changes.append({
            "post_id": post["id"],
            "url": post.get("link", ""),
            "old_title": old_title,
            "new_title": new_title,
            "title_changed": title_changed,
            "new_meta": new_meta if meta_needed else None,
        })

    print(f"\n  変更対象: {len(changes)}件")

    for i, c in enumerate(changes[:30], 1):
        parts = []
        if c["title_changed"]:
            parts.append("TITLE")
        if c["new_meta"]:
            parts.append("META")
        label = "+".join(parts)
        print(f"  [{i}] {label} | ID:{c['post_id']}")
        if c["title_changed"]:
            print(f"      旧: {c['old_title']}")
            print(f"      新: {c['new_title']}")
        if c["new_meta"]:
            print(f"      Meta: {c['new_meta'][:80]}...")
        print()

    if apply and changes:
        print(f"\n  WordPress更新を実行中（{len(changes)}件）...")
        success = 0
        for c in changes:
            try:
                update_data = {}
                if c["title_changed"]:
                    update_data["title"] = c["new_title"]
                if c["new_meta"]:
                    update_data["excerpt"] = c["new_meta"]
                if update_data:
                    update_wp_post(wp["api_url"], wp["headers"], c["post_id"], update_data)
                    success += 1
                    print(f"    OK ID:{c['post_id']}")
                    time.sleep(0.5)
            except Exception as e:
                print(f"    NG ID:{c['post_id']} - {e}")
        print(f"\n  完了: {success}件")
    elif not apply:
        print("  ※ dry-runモード。--apply で実行します。")


def save_report(changes, pages, total_impressions, total_clicks, avg_ctr, args):
    """レポートを保存"""
    now = datetime.now(JST).strftime("%Y-%m-%d")
    report_path = REPORTS_DIR / f"ctr-optimization-{now}.md"

    lines = [
        f"# CTR最適化レポート — {now}\n\n",
        f"## サマリー\n\n",
        f"- 分析期間: 過去{args.days}日間\n",
        f"- 合計表示回数: {total_impressions}\n",
        f"- 合計クリック数: {total_clicks}\n",
        f"- 平均CTR: {avg_ctr}%\n",
        f"- 改善対象: {len(changes)}件\n\n",
        f"## 改善内容\n\n",
        "| # | ID | 表示 | CTR | 順位 | 変更 | 検索KW |\n",
        "|---|---|---|---|---|---|---|\n",
    ]

    for i, c in enumerate(changes, 1):
        kws = ", ".join(c.get("top_queries", [])[:2])
        change_type = "Title+Meta" if c["title_changed"] else "Meta"
        lines.append(
            f"| {i} | {c['post_id']} | {c.get('impressions', '-')} | "
            f"{c.get('ctr', '-')}% | {c.get('position', '-')} | "
            f"{change_type} | {kws} |\n"
        )

    lines.append("\n## タイトル変更詳細\n\n")
    for c in changes:
        if c["title_changed"]:
            lines.append(f"### ID:{c['post_id']}\n")
            lines.append(f"- 旧: {c['old_title']}\n")
            lines.append(f"- 新: {c['new_title']}\n\n")

    with open(report_path, "w", encoding="utf-8") as f:
        f.writelines(lines)

    print(f"\nレポート保存: {report_path}")


if __name__ == "__main__":
    main()
