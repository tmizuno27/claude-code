"""
3サイトのarticle-management.csvをWordPress REST APIから最新データで更新するスクリプト。
- 既存行の手動編集（備考等）は上書きしない
- 新しい記事のみCSVに追加
- 各サイトのCSVカラム構成を維持
"""

import csv
import json
import re
import sys
import html
from pathlib import Path
from base64 import b64encode
from urllib.request import Request, urlopen
from urllib.parse import urlencode

BASE = Path(r"C:\Users\tmizu\マイドライブ\GitHub\claude-code")


def wp_api_get(api_url, username, app_password):
    """WordPress REST APIから全公開記事を取得"""
    credentials = b64encode(f"{username}:{app_password}".encode()).decode()
    all_posts = []
    page = 1
    while True:
        params = urlencode({"per_page": 100, "page": page, "status": "publish"})
        url = f"{api_url}&{params}" if "?" in api_url else f"{api_url}?{params}"
        req = Request(url, headers={"Authorization": f"Basic {credentials}"})
        try:
            with urlopen(req, timeout=30) as resp:
                posts = json.loads(resp.read().decode("utf-8"))
                if not posts:
                    break
                all_posts.extend(posts)
                page += 1
        except Exception as e:
            # Try alternate URL format
            if page == 1 and "wp-json" in api_url:
                alt = api_url.replace("/wp-json/wp/v2/", "/?rest_route=/wp/v2/")
                return wp_api_get(alt + "posts", username, app_password)
            print(f"  API error page {page}: {e}")
            break
    return all_posts


def decode_title(post):
    return html.unescape(post["title"]["rendered"])


def count_words(post):
    """HTMLコンテンツから大まかな文字数を取得"""
    content = re.sub(r"<[^>]+>", "", post.get("content", {}).get("rendered", ""))
    return len(content)


# ── サイト定義 ──
SITES = [
    {
        "name": "nambei-oyaji.com",
        "dir": BASE / "nambei-oyaji.com",
        "api_url": "https://nambei-oyaji.com/wp-json/wp/v2/posts",
    },
    {
        "name": "otona-match.com",
        "dir": BASE / "otona-match.com",
        "api_url": "https://otona-match.com/?rest_route=/wp/v2/posts",
    },
    {
        "name": "sim-hikaku.online",
        "dir": BASE / "sim-hikaku.online",
        "api_url": "https://sim-hikaku.online/wp-json/wp/v2/posts",
    },
]


def update_nambei(site, posts):
    csv_path = site["dir"] / "outputs" / "article-management.csv"
    with open(csv_path, "r", encoding="utf-8-sig") as f:
        reader = csv.reader(f)
        header = next(reader)
        rows = list(reader)

    # 既存のWP IDとslugを収集
    existing_wp_ids = set()
    existing_slugs = set()
    for row in rows:
        if len(row) > 18:  # 備考カラム
            m = re.search(r"WP ID:(\d+)", row[18])
            if m:
                existing_wp_ids.add(int(m.group(1)))
        if len(row) > 14:  # パーマリンクカラム
            existing_slugs.add(row[14])

    new_count = 0
    next_num = len(rows) + 1
    for p in posts:
        wp_id = p["id"]
        slug = p["slug"]
        if wp_id in existing_wp_ids or slug in existing_slugs:
            continue
        # 新記事追加
        title = decode_title(p)
        pub_date = p["date"][:10]
        new_row = [
            str(next_num),  # #
            "",  # 公開順
            "",  # 柱
            "",  # 記事タイプ
            "",  # カテゴリ
            "",  # メインKW
            title,  # 記事タイトル
            "公開済",  # ステータス
            str(count_words(p)),  # 文字数
            "",  # 要追記箇所
            "",  # 写真指示
            "0",  # アフィリ数
            "0",  # 内部リンク数
            "",  # ファイル名
            slug,  # パーマリンク
            "0",  # 累計PV
            pub_date,  # 作成日
            pub_date,  # 公開日
            f"WP ID:{wp_id}｜API自動追加",  # 備考
        ]
        # Pad to match header length
        while len(new_row) < len(header):
            new_row.append("")
        rows.append(new_row)
        next_num += 1
        new_count += 1

    with open(csv_path, "w", encoding="utf-8-sig", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(header)
        writer.writerows(rows)

    return len(posts), new_count


def update_otona(site, posts):
    csv_path = site["dir"] / "outputs" / "article-management.csv"
    with open(csv_path, "r", encoding="utf-8-sig") as f:
        reader = csv.reader(f)
        header = next(reader)
        rows = list(reader)

    existing_ids = set()
    for row in rows:
        if row and row[0].strip().isdigit():
            existing_ids.add(int(row[0]))

    new_count = 0
    for p in posts:
        wp_id = p["id"]
        if wp_id in existing_ids:
            continue
        title = decode_title(p)
        slug = p["slug"]
        pub_date = p["date"][:10]
        wp_url = p["link"]
        new_row = [
            str(wp_id),  # id
            slug,  # slug
            title,  # title
            "publish",  # status
            pub_date,  # published_date
            "",  # category
            "",  # type
            str(count_words(p)),  # word_count
            "0",  # affiliate_count
            "0",  # internal_links
            "0",  # 累計PV
            wp_url,  # wp_url
            "API自動追加",  # notes
        ]
        while len(new_row) < len(header):
            new_row.append("")
        rows.append(new_row)
        new_count += 1

    with open(csv_path, "w", encoding="utf-8-sig", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(header)
        writer.writerows(rows)

    return len(posts), new_count


def update_sim(site, posts):
    csv_path = site["dir"] / "outputs" / "article-management.csv"
    with open(csv_path, "r", encoding="utf-8-sig") as f:
        reader = csv.reader(f)
        header = next(reader)
        rows = list(reader)

    existing_ids = set()
    for row in rows:
        if len(row) > 13 and row[13].strip().isdigit():
            existing_ids.add(int(row[13]))

    new_count = 0
    next_order = len(rows) + 1
    for p in posts:
        wp_id = p["id"]
        if wp_id in existing_ids:
            continue
        title = decode_title(p)
        slug = p["slug"]
        pub_date = p["date"][:10]
        wp_url = p["link"]
        new_row = [
            str(next_order),  # 公開順
            title,  # タイトル
            "公開済",  # ステータス
            pub_date,  # 公開日
            "",  # 柱
            "",  # 記事タイプ
            "",  # カテゴリ
            "",  # メインKW
            str(count_words(p)),  # 文字数
            "0",  # アフィリ数
            "0",  # 内部リンク数
            "0",  # 累計PV
            slug,  # ファイル名
            str(wp_id),  # WordPress ID
            wp_url,  # WordPress URL
            "API自動追加",  # 備考
        ]
        while len(new_row) < len(header):
            new_row.append("")
        rows.append(new_row)
        next_order += 1
        new_count += 1

    with open(csv_path, "w", encoding="utf-8-sig", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(header)
        writer.writerows(rows)

    return len(posts), new_count


def main():
    updaters = [update_nambei, update_otona, update_sim]

    for site, updater in zip(SITES, updaters):
        print(f"\n{'='*50}")
        print(f"処理中: {site['name']}")
        print(f"{'='*50}")

        secrets_path = site["dir"] / "config" / "secrets.json"
        with open(secrets_path, "r", encoding="utf-8") as f:
            secrets = json.load(f)

        wp = secrets["wordpress"]
        username = wp["username"]
        app_password = wp["app_password"]

        print(f"  API取得中: {site['api_url']}")
        posts = wp_api_get(site["api_url"], username, app_password)
        print(f"  取得記事数: {len(posts)}")

        if not posts:
            print("  ※ 記事が取得できませんでした。スキップします。")
            continue

        total, new = updater(site, posts)
        print(f"  CSV更新完了: WordPress {total}記事 / 新規追加 {new}件")

    print(f"\n{'='*50}")
    print("全サイト完了!")
    print(f"{'='*50}")


if __name__ == "__main__":
    main()
