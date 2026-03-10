"""
Insert additional stock images into WordPress posts.
Finds H2 sections without images and adds relevant stock photos.
"""

import json
import re
import requests
from pathlib import Path

BASE = Path(r"c:\Users\tmizu\マイドライブ\GitHub\claude-code\blog")
STOCK = BASE / "images" / "stock"
SECRETS = json.load(open(BASE / "config" / "secrets.json", "r", encoding="utf-8"))
MAPPING = json.load(open(BASE / "config" / "media-mapping.json", "r", encoding="utf-8"))

WP_URL = "https://nambei-oyaji.com/wp-json/wp/v2"
AUTH = (SECRETS["wordpress"]["username"], SECRETS["wordpress"]["app_password"])

# Post ID -> additional images to insert (beyond existing ones)
# Each: (stock_category, keyword_prefix, alt_text, target_h2_index)
# target_h2_index: which H2 to insert after (0-based), -1 = auto-find empty spots
POST_EXTRA_IMAGES = {
    1008: [  # 気候と天気 - has 8 H2s, 2 imgs
        ("lifestyle-general", "blue-sky-clouds", "パラグアイの澄み切った青空", 3),
        ("lifestyle-general", "sunset-golden", "パラグアイの美しい夕焼け", 5),
        ("climate-weather", "spring-flowers", "パラグアイに咲く花々", 6),
    ],
    1065: [  # 移住の費用 - 7 H2s, 3 imgs
        ("immigration-visa", "checklist-notebook", "移住準備のチェックリスト", 4),
        ("immigration-visa", "airplane-sky", "パラグアイへのフライト", 5),
    ],
    1066: [  # 生活費 - 9 H2s, 2 imgs
        ("shopping-supermarket", "vegetables-market", "パラグアイの新鮮な野菜", 2),
        ("shopping-supermarket", "local-market-produce", "ローカルマーケットの食材", 4),
        ("food-culture", "family-dinner-outdoor", "家族の食卓", 6),
    ],
    1067: [  # 治安 - 9 H2s, 3 imgs
        ("paraguay-life", "latin-america-plaza", "南米の広場", 3),
        ("lifestyle-general", "nature-path-walking", "パラグアイの自然散策路", 5),
        ("paraguay-life", "asuncion-city", "アスンシオンの街並み", 7),
    ],
    1068: [  # 子連れ海外移住 - 10 H2s, 2 imgs
        ("family-education", "family-suitcase", "家族での引っ越し準備", 2),
        ("family-education", "kids-soccer", "サッカーを楽しむ子どもたち", 4),
        ("family-education", "school-classroom", "学校の教室風景", 6),
        ("family-education", "family-dinner", "家族の団らん", 8),
    ],
    1069: [  # 海外移住後の働き方 - 10 H2s, 2 imgs
        ("remote-work", "home-office", "自宅のホームオフィス", 2),
        ("remote-work", "typing-keyboard", "パソコンでの作業風景", 4),
        ("remote-work", "programming-code", "プログラミング画面", 6),
        ("blog-writing", "blogging-laptop", "ブログ執筆の様子", 8),
    ],
    1070: [  # 海外送金比較 - 10 H2s, 2 imgs
        ("finance-money", "credit-card", "クレジットカードでの決済", 2),
        ("finance-money", "currency-exchange", "外貨の両替", 4),
        ("finance-money", "savings-money", "送金コストの節約", 6),
        ("finance-money", "tax-calculator", "手数料の計算", 8),
    ],
    1214: [  # 食文化 - 8 H2s, 2 imgs
        ("food-culture", "grilled-steak", "ジューシーなグリルステーキ", 2),
        ("food-culture", "outdoor-barbecue", "屋外でのBBQ風景", 4),
        ("food-culture", "cassava-food", "マンディオカ（キャッサバ）料理", 6),
    ],
}


def find_stock_image(category, keyword_prefix):
    cat_dir = STOCK / category
    if not cat_dir.exists():
        return None
    for f in sorted(cat_dir.glob(f"{keyword_prefix}*.jpg")):
        return f
    return None


def upload_to_wordpress(image_path, alt_text):
    filename = image_path.name
    for mid, info in MAPPING.get("media", {}).items():
        if info.get("wp_name", "") == filename:
            return int(mid)

    with open(image_path, "rb") as f:
        data = f.read()

    headers = {
        "Content-Disposition": f'attachment; filename="{filename}"',
        "Content-Type": "image/jpeg",
    }
    r = requests.post(f"{WP_URL}/media", headers=headers, data=data, auth=AUTH, timeout=60)
    if r.status_code in (200, 201):
        media_id = r.json()["id"]
        requests.post(f"{WP_URL}/media/{media_id}", json={"alt_text": alt_text}, auth=AUTH, timeout=15)
        MAPPING["media"][str(media_id)] = {
            "file": f"stock/{image_path.parent.name}/{filename}",
            "wp_name": filename,
            "title": alt_text,
        }
        print(f"    Uploaded: {filename} -> media_id {media_id}")
        return media_id
    else:
        print(f"    Upload FAILED: {r.status_code} {r.text[:200]}")
        return None


def get_wp_image_url(media_id):
    r = requests.get(f"{WP_URL}/media/{media_id}", auth=AUTH, timeout=15)
    if r.status_code == 200:
        data = r.json()
        sizes = data.get("media_details", {}).get("sizes", {})
        for size_key in ["large", "medium_large", "full"]:
            if size_key in sizes:
                return sizes[size_key]["source_url"]
        return data.get("source_url", "")
    return ""


def find_h2_sections(raw_content):
    """Split content into sections by H2 headings. Returns list of (h2_line_index, has_image)"""
    lines = raw_content.split("\n")
    sections = []
    current_h2_idx = -1

    for i, line in enumerate(lines):
        if re.search(r'<h2[^>]*>', line, re.IGNORECASE):
            if current_h2_idx >= 0:
                # Check if previous section had images
                section_text = "\n".join(lines[current_h2_idx:i])
                has_img = bool(re.search(r'wp:image|<img ', section_text, re.IGNORECASE))
                sections.append((current_h2_idx, has_img))
            current_h2_idx = i

    # Last section
    if current_h2_idx >= 0:
        section_text = "\n".join(lines[current_h2_idx:])
        has_img = bool(re.search(r'wp:image|<img ', section_text, re.IGNORECASE))
        sections.append((current_h2_idx, has_img))

    return sections


def make_image_block(media_id, img_url, alt_text):
    return (
        f'\n<!-- wp:image {{"id":{media_id},"sizeSlug":"large","linkDestination":"none"}} -->\n'
        f'<figure class="wp-block-image size-large">'
        f'<img src="{img_url}" alt="{alt_text}" class="wp-image-{media_id}"/>'
        f'<figcaption class="wp-element-caption">{alt_text}</figcaption>'
        f'</figure>\n'
        f'<!-- /wp:image -->\n'
    )


def process_post(post_id, extra_images):
    print(f"\n--- Post ID: {post_id} ---")

    r = requests.get(f"{WP_URL}/posts/{post_id}?context=edit", auth=AUTH, timeout=15)
    if r.status_code != 200:
        print(f"  Failed to get post: {r.status_code}")
        return False

    post = r.json()
    raw = post["content"]["raw"]
    print(f"  Current images: {len(re.findall(r'wp:image', raw))}")

    sections = find_h2_sections(raw)
    print(f"  H2 sections: {len(sections)}")

    # Upload images and prepare insertions
    insertions = []  # (h2_line_index, image_block_html)
    for category, keyword_prefix, alt_text, target_h2 in extra_images:
        if target_h2 >= len(sections):
            target_h2 = len(sections) - 1

        # Skip if that section already has an image
        if sections[target_h2][1]:
            print(f"  H2#{target_h2} already has image, trying next")
            # Try adjacent sections
            found = False
            for offset in [1, -1, 2, -2]:
                alt_idx = target_h2 + offset
                if 0 <= alt_idx < len(sections) and not sections[alt_idx][1]:
                    target_h2 = alt_idx
                    found = True
                    break
            if not found:
                print(f"  No empty section found, skipping {keyword_prefix}")
                continue

        img_path = find_stock_image(category, keyword_prefix)
        if not img_path:
            print(f"  Image not found: {category}/{keyword_prefix}")
            continue

        media_id = upload_to_wordpress(img_path, alt_text)
        if not media_id:
            continue

        img_url = get_wp_image_url(media_id)
        if not img_url:
            continue

        block_html = make_image_block(media_id, img_url, alt_text)
        insertions.append((sections[target_h2][0], block_html))
        sections[target_h2] = (sections[target_h2][0], True)  # Mark as having image
        print(f"  Will insert {keyword_prefix} after H2#{target_h2}")

    if not insertions:
        print("  No insertions needed")
        return False

    # Apply insertions (sort by line index, insert from bottom up)
    lines = raw.split("\n")
    insertions.sort(key=lambda x: x[0], reverse=True)

    for h2_line_idx, block_html in insertions:
        # Find the end of this H2 line
        insert_pos = h2_line_idx + 1
        # Skip past any empty lines right after H2
        while insert_pos < len(lines) and lines[insert_pos].strip() == "":
            insert_pos += 1
        # Insert the image block after the first paragraph following the H2
        # Find next empty line or next block
        while insert_pos < len(lines) and lines[insert_pos].strip() != "" and not lines[insert_pos].strip().startswith("<h"):
            insert_pos += 1
        lines.insert(insert_pos, block_html)

    new_content = "\n".join(lines)

    update_r = requests.post(
        f"{WP_URL}/posts/{post_id}",
        json={"content": new_content},
        auth=AUTH,
        timeout=30,
    )
    if update_r.status_code == 200:
        print(f"  SUCCESS: {len(insertions)} images inserted")
        return True
    else:
        print(f"  Update FAILED: {update_r.status_code} {update_r.text[:300]}")
        return False


def main():
    print("=" * 60)
    print("Insert Additional Stock Images into Posts")
    print("=" * 60)

    total = 0
    for post_id, specs in POST_EXTRA_IMAGES.items():
        if process_post(post_id, specs):
            total += 1

    with open(BASE / "config" / "media-mapping.json", "w", encoding="utf-8") as f:
        json.dump(MAPPING, f, ensure_ascii=False, indent=2)

    print(f"\n{'=' * 60}")
    print(f"Done! {total} posts updated with additional images")
    print(f"{'=' * 60}")


if __name__ == "__main__":
    main()
