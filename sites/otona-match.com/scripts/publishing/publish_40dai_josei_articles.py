"""40代女性婚活記事を4本投稿するスクリプト"""
import sys
from pathlib import Path

# パスを追加
sys.path.insert(0, str(Path(__file__).parent))
from wp_publisher import publish_article, load_credentials, get_wp_client, OUTPUTS_DIR, CSV_PATH

import csv
from datetime import datetime

ARTICLES = [
    {
        "title": "婚活40代女性の現実とは？成功するための5つの戦略を解説",
        "slug": "konkatsu-40dai-josei-genjitsu",
        "file": "konkatsu-40dai-josei-genjitsu.html",
        "categories": [4],  # konkatsu
        "excerpt": "婚活40代女性の現実をデータと体験談で解説。マッチングアプリや結婚相談所での成功戦略、直面する壁と突破口を具体的にまとめました。40代でも婚活成功は可能です。",
        "focus_kw": "婚活 40代 女性 現実",
    },
    {
        "title": "婚活40代女性の服装完全ガイド｜好印象を与えるスタイリング術",
        "slug": "konkatsu-40dai-josei-fuku",
        "file": "konkatsu-40dai-josei-fuku.html",
        "categories": [4],  # konkatsu
        "excerpt": "婚活40代女性の服装選びを徹底解説。婚活パーティー・プロフィール写真・初デートそれぞれに最適なスタイリングをシーン別に紹介。清潔感と女性らしさを両立する方法を伝授。",
        "focus_kw": "婚活 40代 女性 服装",
    },
    {
        "title": "無職・専業主婦の40代女性が婚活で成功するための戦略と注意点",
        "slug": "konkatsu-40dai-josei-mushoku",
        "file": "konkatsu-40dai-josei-mushoku.html",
        "categories": [4],  # konkatsu
        "excerpt": "無職・専業主婦の40代女性が婚活で直面する現実と成功戦略を解説。プロフィールの書き方、選ぶべきサービス、費用を抑えた婚活方法を体験談とともに紹介します。",
        "focus_kw": "婚活 40代 女性 無職",
    },
    {
        "title": "婚活40代女性の条件設定ガイド｜何を妥協して何を守るべきか",
        "slug": "konkatsu-40dai-josei-joken",
        "file": "konkatsu-40dai-josei-joken.html",
        "categories": [4],  # konkatsu
        "excerpt": "婚活40代女性が設定すべき条件と妥協点を解説。NG条件・核心条件・条件設定フレームワークを具体的に紹介。体験談から学ぶ、40代婚活成功のための正しい条件の見直し方。",
        "focus_kw": "婚活 40代 女性 条件",
    },
]


def update_csv(article_id, slug, title, category):
    rows = []
    try:
        with open(CSV_PATH, "r", encoding="utf-8-sig") as f:
            reader = csv.DictReader(f)
            fieldnames = reader.fieldnames
            rows = list(reader)
    except Exception as e:
        print(f"  CSV読み込みエラー: {e}")
        return

    new_row = {
        "id": article_id,
        "slug": slug,
        "title": title,
        "status": "publish",
        "published_date": datetime.now().strftime("%Y-%m-%d"),
        "category": category,
        "type": "集客",
        "word_count": "2000",
        "affiliate_count": "3",
        "internal_links": "3",
        "\u7d2fPV": "0",
        "wp_url": f"https://otona-match.com/{slug}/",
        "notes": f"メインKW：{slug.replace('-', ' ')}",
    }

    rows.append(new_row)
    with open(CSV_PATH, "w", encoding="utf-8-sig", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)
    print(f"  CSV更新完了")


def main():
    print("=== 40代女性婚活記事 4本投稿 ===\n")
    success_count = 0

    for article in ARTICLES:
        print(f"投稿中: {article['title']}")
        html_path = OUTPUTS_DIR / article["file"]
        if not html_path.exists():
            print(f"  ファイルが見つかりません: {html_path}")
            continue

        with open(html_path, "r", encoding="utf-8") as f:
            content = f.read()

        result = publish_article(
            title=article["title"],
            slug=article["slug"],
            content=content,
            categories=article["categories"],
            excerpt=article["excerpt"],
            status="publish",
        )

        if result:
            success_count += 1
            update_csv(
                article_id=result["id"],
                slug=article["slug"],
                title=article["title"],
                category="konkatsu",
            )
            print(f"  ✓ 成功: https://otona-match.com/{article['slug']}/\n")
        else:
            print(f"  ✗ 失敗\n")

    print(f"\n=== 完了: {success_count}/{len(ARTICLES)} 本投稿成功 ===")


if __name__ == "__main__":
    main()
