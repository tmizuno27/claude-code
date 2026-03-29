"""残り2本の40代女性記事を投稿"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
from wp_publisher import publish_article, OUTPUTS_DIR, CSV_PATH
import csv
from datetime import datetime

ARTICLES = [
    {
        "title": "無職・専業主婦の40代女性が婚活で成功するための戦略と注意点",
        "slug": "konkatsu-40dai-josei-mushoku",
        "file": "konkatsu-40dai-josei-mushoku.html",
        "categories": [4],
        "excerpt": "無職・専業主婦の40代女性が婚活で直面する現実と成功戦略を解説。プロフィールの書き方、選ぶべきサービス、費用を抑えた婚活方法を体験談とともに紹介します。",
    },
    {
        "title": "婚活40代女性の条件設定ガイド｜何を妥協して何を守るべきか",
        "slug": "konkatsu-40dai-josei-joken",
        "file": "konkatsu-40dai-josei-joken.html",
        "categories": [4],
        "excerpt": "婚活40代女性が設定すべき条件と妥協点を解説。NG条件・核心条件・条件設定フレームワークを具体的に紹介。体験談から学ぶ、40代婚活成功のための正しい条件の見直し方。",
    },
]

def update_csv(article_id, slug, title):
    with open(CSV_PATH, "r", encoding="utf-8-sig") as f:
        reader = csv.DictReader(f)
        fieldnames = reader.fieldnames
        rows = list(reader)

    new_row = {fn: "" for fn in fieldnames}
    new_row["id"] = str(article_id)
    new_row["slug"] = slug
    new_row["title"] = title
    new_row["status"] = "publish"
    new_row["published_date"] = datetime.now().strftime("%Y-%m-%d")
    new_row["category"] = "konkatsu"
    new_row["type"] = "collecter"
    new_row["word_count"] = "2200"
    new_row["affiliate_count"] = "3"
    new_row["internal_links"] = "3"
    new_row["wp_url"] = f"https://otona-match.com/{slug}/"
    new_row["notes"] = "40dai-josei series"
    # 累計PV field name
    for fn in fieldnames:
        if "PV" in fn:
            new_row[fn] = "0"

    rows.append(new_row)
    with open(CSV_PATH, "w", encoding="utf-8-sig", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

for article in ARTICLES:
    print("Posting:", article["slug"])
    html_path = OUTPUTS_DIR / article["file"]
    content = html_path.read_text(encoding="utf-8")
    result = publish_article(
        title=article["title"],
        slug=article["slug"],
        content=content,
        categories=article["categories"],
        excerpt=article["excerpt"],
        status="publish",
    )
    if result:
        update_csv(result["id"], article["slug"], article["title"])
        print("  OK ID:", result["id"])
    else:
        print("  FAILED")
