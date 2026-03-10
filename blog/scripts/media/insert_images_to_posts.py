"""
Insert stock images into WordPress published posts.
- Upload stock images to WordPress media library
- Insert <figure> blocks after H2 headings (every 2-3 H2s)
- Update posts via REST API
"""

import json
import re
import os
import requests
from pathlib import Path

BASE = Path(r"c:\Users\tmizu\マイドライブ\GitHub\claude-code\blog")
STOCK = BASE / "images" / "stock"
SECRETS = json.load(open(BASE / "config" / "secrets.json", "r", encoding="utf-8"))
MAPPING = json.load(open(BASE / "config" / "media-mapping.json", "r", encoding="utf-8"))

WP_URL = "https://nambei-oyaji.com/wp-json/wp/v2"
AUTH = (SECRETS["wordpress"]["username"], SECRETS["wordpress"]["app_password"])

# Post ID -> which stock categories & specific images to use
# Each entry: list of (stock_category, keyword_prefix, alt_text_ja)
POST_IMAGE_MAP = {
    1008: [  # パラグアイの気候と天気
        ("climate-weather", "sunny-tropical", "パラグアイの晴天と熱帯の空"),
        ("paraguay-life", "palm-tree-landscape", "パラグアイのヤシの木と風景"),
        ("lifestyle-general", "blue-sky-clouds", "パラグアイの青空"),
    ],
    1065: [  # パラグアイ移住の費用
        ("immigration-visa", "suitcase-packing", "海外移住の荷造り準備"),
        ("finance-money", "currency-exchange", "外貨両替・為替"),
        ("immigration-visa", "new-home-keys", "新居の鍵を受け取る"),
    ],
    1066: [  # パラグアイの生活費
        ("shopping-supermarket", "supermarket-aisle", "パラグアイのスーパーマーケット"),
        ("food-culture", "tropical-fruit-market", "トロピカルフルーツが並ぶ市場"),
        ("finance-money", "savings-money", "家計の節約・貯金"),
    ],
    1067: [  # パラグアイの治安
        ("paraguay-life", "south-america-street", "南米の街並み"),
        ("paraguay-life", "colonial-architecture", "コロニアル建築の街並み"),
        ("lifestyle-general", "nature-path-walking", "自然の中の散歩道"),
    ],
    1068: [  # 子連れ海外移住
        ("family-education", "children-school", "学校で学ぶ子どもたち"),
        ("family-education", "kids-playing-outdoor", "外で遊ぶ子どもたち"),
        ("family-education", "parent-child-reading", "親子で読書する風景"),
    ],
    1069: [  # 海外移住後の働き方
        ("remote-work", "remote-work-laptop", "リモートワークのイメージ"),
        ("remote-work", "coworking-space", "コワーキングスペース"),
        ("remote-work", "laptop-tropical", "熱帯の環境でパソコン作業"),
    ],
    1070: [  # 海外送金サービス比較
        ("finance-money", "money-transfer", "海外送金のイメージ"),
        ("finance-money", "online-banking", "オンラインバンキング"),
        ("finance-money", "credit-card", "クレジットカード"),
    ],
    1214: [  # パラグアイの食文化
        ("food-culture", "barbecue-grill", "アサード（南米BBQ）"),
        ("food-culture", "empanada", "エンパナーダ"),
        ("food-culture", "fresh-juice-tropical", "トロピカルフレッシュジュース"),
    ],
}


def find_stock_image(category, keyword_prefix):
    """Find a stock image file matching the category and keyword prefix"""
    cat_dir = STOCK / category
    if not cat_dir.exists():
        return None
    for f in sorted(cat_dir.glob(f"{keyword_prefix}*.jpg")):
        return f
    return None


def upload_to_wordpress(image_path, alt_text):
    """Upload image to WordPress and return media_id"""
    filename = image_path.name
    # Check if already uploaded by checking mapping
    for mid, info in MAPPING.get("media", {}).items():
        if info.get("wp_name", "") == filename:
            print(f"    Already uploaded: {filename} -> media_id {mid}")
            return int(mid)

    with open(image_path, "rb") as f:
        data = f.read()

    headers = {
        "Content-Disposition": f'attachment; filename="{filename}"',
        "Content-Type": "image/jpeg",
    }
    r = requests.post(
        f"{WP_URL}/media",
        headers=headers,
        data=data,
        auth=AUTH,
        timeout=60,
    )
    if r.status_code in (200, 201):
        media_id = r.json()["id"]
        # Update alt text
        requests.post(
            f"{WP_URL}/media/{media_id}",
            json={"alt_text": alt_text},
            auth=AUTH,
            timeout=15,
        )
        # Update mapping
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
    """Get the URL of an uploaded WordPress media item"""
    r = requests.get(f"{WP_URL}/media/{media_id}", auth=AUTH, timeout=15)
    if r.status_code == 200:
        data = r.json()
        # Try to get medium_large or large size
        sizes = data.get("media_details", {}).get("sizes", {})
        for size_key in ["large", "medium_large", "full"]:
            if size_key in sizes:
                return sizes[size_key]["source_url"]
        return data.get("source_url", "")
    return ""


def insert_images_into_content(html, images_data):
    """Insert figure blocks after every 2-3 H2 headings.
    images_data: list of (media_id, image_url, alt_text)
    """
    # Find all H2 positions (end of H2 + following paragraph)
    h2_pattern = re.compile(r'(</h2>)', re.IGNORECASE)
    h2_positions = [m.end() for m in h2_pattern.finditer(html)]

    if not h2_positions or not images_data:
        return html

    # Determine insertion points: after H2 #2, #4, #6 (or evenly spaced)
    num_h2 = len(h2_positions)
    num_images = len(images_data)

    if num_h2 <= 3:
        insert_after = [0]  # After first H2
    else:
        # Space images evenly among H2s
        step = max(2, num_h2 // (num_images + 1))
        insert_after = []
        for i in range(num_images):
            idx = min((i + 1) * step - 1, num_h2 - 1)
            if idx not in insert_after:
                insert_after.append(idx)

    # Insert from back to front to preserve positions
    result = html
    for i in range(min(len(insert_after), len(images_data)) - 1, -1, -1):
        h2_idx = insert_after[i]
        pos = h2_positions[h2_idx]
        media_id, img_url, alt_text = images_data[i]

        figure_html = (
            f'\n\n<!-- wp:image {{"id":{media_id},"sizeSlug":"large","linkDestination":"none"}} -->\n'
            f'<figure class="wp-block-image size-large">'
            f'<img src="{img_url}" alt="{alt_text}" class="wp-image-{media_id}"/>'
            f'<figcaption class="wp-element-caption">{alt_text}</figcaption>'
            f'</figure>\n'
            f'<!-- /wp:image -->\n\n'
        )
        result = result[:pos] + figure_html + result[pos:]

    return result


def process_post(post_id, image_specs):
    """Process a single post: upload images, insert into content, update post"""
    print(f"\n--- Post ID: {post_id} ---")

    # Get current post content
    r = requests.get(f"{WP_URL}/posts/{post_id}", auth=AUTH, timeout=15)
    if r.status_code != 200:
        print(f"  Failed to get post: {r.status_code}")
        return False

    post = r.json()
    title = post["title"]["rendered"]
    content = post["content"]["rendered"]
    print(f"  Title: {title[:50]}")

    # Check if images already inserted
    existing_imgs = len(re.findall(r'<img ', content))
    if existing_imgs > 0:
        print(f"  Already has {existing_imgs} images, skipping")
        return False

    # Upload images and collect data
    images_data = []
    for category, keyword_prefix, alt_text in image_specs:
        img_path = find_stock_image(category, keyword_prefix)
        if not img_path:
            print(f"  Image not found: {category}/{keyword_prefix}")
            continue

        media_id = upload_to_wordpress(img_path, alt_text)
        if media_id:
            img_url = get_wp_image_url(media_id)
            if img_url:
                images_data.append((media_id, img_url, alt_text))

    if not images_data:
        print("  No images to insert")
        return False

    # Insert images into content
    new_content = insert_images_into_content(content, images_data)

    # Update the post
    update_r = requests.post(
        f"{WP_URL}/posts/{post_id}",
        json={"content": new_content},
        auth=AUTH,
        timeout=30,
    )
    if update_r.status_code == 200:
        print(f"  Updated! {len(images_data)} images inserted")
        return True
    else:
        print(f"  Update FAILED: {update_r.status_code} {update_r.text[:200]}")
        return False


def main():
    print("=" * 60)
    print("Insert Stock Images into WordPress Posts")
    print("=" * 60)

    total_updated = 0
    for post_id, specs in POST_IMAGE_MAP.items():
        if process_post(post_id, specs):
            total_updated += 1

    # Save updated mapping
    with open(BASE / "config" / "media-mapping.json", "w", encoding="utf-8") as f:
        json.dump(MAPPING, f, ensure_ascii=False, indent=2)

    print(f"\n{'=' * 60}")
    print(f"Done! {total_updated} posts updated")
    print(f"{'=' * 60}")


if __name__ == "__main__":
    main()
