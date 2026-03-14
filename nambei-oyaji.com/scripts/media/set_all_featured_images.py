"""
全50記事にアイキャッチ画像（サムネイル）を設定するスクリプト
- 既存ストック画像から最適な画像を選定
- 不足分はPixabay APIからダウンロード
- WordPressにアップロードしてアイキャッチに設定
"""

import json
import os
import sys
import time
import requests
from pathlib import Path

# パス設定
BLOG_DIR = Path(__file__).resolve().parent.parent.parent
IMAGES_DIR = BLOG_DIR / "images"
STOCK_DIR = IMAGES_DIR / "stock"
CONFIG_DIR = BLOG_DIR / "config"
SECRETS_PATH = CONFIG_DIR / "secrets.json"
MEDIA_MAPPING_PATH = CONFIG_DIR / "media-mapping.json"

# WordPress設定
WP_BASE = "https://nambei-oyaji.com/wp-json/wp/v2"

# 全50記事 → 最適画像のマッピング
# key: 記事番号(CSV行-1), value: (ファイル名, カテゴリ, 説明)
ARTICLE_IMAGE_MAP = {
    # === 公開済み（既にアイキャッチ設定済み → スキップ） ===
    # 1: 気候 → WP:1008, media:1101 (設定済み)
    # 2: 食文化 → WP:1214, media:1105 (要確認)
    # 3: 移住費用 → WP:1065, media:1108 (設定済み)
    # 4: 生活費 → WP:1066, media:1107 (設定済み)
    # 5: 治安 → WP:1067, media:1102 (設定済み)
    # 17: 働き方 → WP:1069, media:1111 (設定済み)
    # 14: 海外送金 → WP:1070, media:1120 (設定済み)
    # 22: 子連れ移住 → WP:1068, media:1133 (設定済み)

    # === 下書き・リライト済み（アイキャッチ未設定） ===
    # 6: パラグアイ移住で失敗しないための注意点
    6: {
        "local": "stock/immigration-visa/suitcase-packing_3414018.jpg",
        "alt": "パラグアイ移住の注意点",
        "title": "パラグアイ移住で失敗しないための注意点"
    },
    # 7: パラグアイの税金が安い理由
    7: {
        "local": "stock/finance-money/savings-money_1264856.jpg",
        "alt": "パラグアイの税金・節税",
        "title": "パラグアイの税金が安い理由"
    },
    # 8: パラグアイ移住後のリアルな収入事情
    8: {
        "local": "stock/remote-work/laptop-tropical_3931996.jpg",
        "alt": "パラグアイでの収入事情",
        "title": "パラグアイ移住後のリアルな収入事情"
    },
    # 9: パラグアイの永住権の取り方
    9: {
        "local": "stock/immigration-visa/customs-border_1143485.jpg",
        "alt": "パラグアイの永住権取得",
        "title": "パラグアイの永住権の取り方完全ガイド"
    },
    # 10: パラグアイのビザの種類と取得方法
    10: {
        "local": "stock/immigration-visa/airport-departure_6911566.jpg",
        "alt": "パラグアイのビザ・渡航",
        "title": "パラグアイのビザの種類と取得方法"
    },
    # 11: 海外移住前の準備リスト完全版
    11: {
        "local": "stock/immigration-visa/checklist-notebook_2098425.jpg",
        "alt": "海外移住準備チェックリスト",
        "title": "海外移住前の準備リスト完全版"
    },
    # 12: 海外在住者向けクレジットカード比較
    12: {
        "local": "stock/finance-money/credit-card_229830.jpg",
        "alt": "海外在住者向けクレジットカード",
        "title": "海外在住者向けクレジットカード比較"
    },
    # 13: パラグアイで銀行口座を開設する方法
    13: {
        "local": "stock/finance-money/online-banking_4287684.jpg",
        "alt": "パラグアイの銀行口座開設",
        "title": "パラグアイで銀行口座を開設する方法"
    },
    # 15: パラグアイのインターネット・通信事情
    15: {
        "local": "stock/internet-vpn/fiber-optic-cable_502894.jpg",
        "alt": "パラグアイのインターネット環境",
        "title": "パラグアイのインターネット・通信事情"
    },
    # 16: 海外生活で必須のVPN おすすめ3選
    16: {
        "local": "stock/internet-vpn/cybersecurity-lock_3998798.jpg",
        "alt": "VPNセキュリティ",
        "title": "海外生活で必須のVPN おすすめ3選"
    },
    # 18: パラグアイから日本の仕事をリモートでやる方法
    18: {
        "local": "stock/remote-work/remote-work-laptop_1869820.jpg",
        "alt": "パラグアイからのリモートワーク",
        "title": "パラグアイからリモートワーク"
    },
    # 19: 海外移住者が身につけるべきスキル3選
    19: {
        "local": "stock/remote-work/freelancer-laptop_581131.jpg",
        "alt": "海外移住に必要なスキル",
        "title": "海外移住者が身につけるべきスキル"
    },
    # 20: 海外移住前に受けておくべきオンラインスクール5選
    20: {
        "local": "stock/blog-writing/content-creation_5366803.jpg",
        "alt": "オンラインスクールで学ぶ",
        "title": "海外移住前のオンラインスクール"
    },
    # 21: パラグアイの教育事情・インターナショナルスクール
    21: {
        "local": "stock/family-education/children-learning_286245.jpg",
        "alt": "パラグアイの教育・インターナショナルスクール",
        "title": "パラグアイの教育事情"
    },
    # 23: パラグアイの医療・保険事情
    23: {
        "local": "stock/healthcare/family-healthcare_1531059.jpg",
        "alt": "パラグアイの医療・病院",
        "title": "パラグアイの医療・保険事情"
    },
    # 24: 海外在住者向け保険徹底比較
    24: {
        "local": "stock/healthcare/doctor-patient_4099432.jpg",
        "alt": "海外保険の比較",
        "title": "海外在住者向け保険徹底比較"
    },
    # 25: 海外生活ブログの始め方
    25: {
        "local": "stock/blog-writing/blogging-laptop_581131.jpg",
        "alt": "ブログの始め方",
        "title": "海外生活ブログの始め方"
    },
    # 26: 海外生活ブログで収益化する方法
    26: {
        "local": "stock/blog-writing/seo-marketing_1725340.jpg",
        "alt": "ブログ収益化",
        "title": "海外生活ブログで収益化する方法"
    },
    # 27: パラグアイの言語事情
    27: {
        "local": "stock/language-learning/conversation-people_2805643.jpg",
        "alt": "パラグアイの言語・会話",
        "title": "パラグアイの言語事情"
    },
    # 28: オンラインスペイン語学習サービス比較
    28: {
        "local": "stock/language-learning/language-learning-book_1106196.jpg",
        "alt": "スペイン語オンライン学習",
        "title": "オンラインスペイン語学習サービス比較"
    },
    # 29: パラグアイの日本人コミュニティ事情
    29: {
        "local": "stock/mental-health/cultural-exchange-people_641632.jpg",
        "alt": "パラグアイの日本人コミュニティ",
        "title": "パラグアイの日本人コミュニティ"
    },
    # 30: 海外移住のホームシック対策
    30: {
        "local": "stock/mental-health/happy-family-outdoor_7318667.jpg",
        "alt": "海外移住のメンタルケア",
        "title": "海外移住のホームシック対策"
    },
    # 31: 海外移住の持ち物リスト完全版
    31: {
        "local": "stock/immigration-visa/checklist-notebook_2313804.jpg",
        "alt": "海外移住の持ち物準備",
        "title": "海外移住の持ち物リスト"
    },
    # 32: 海外在住者の年金・社会保険・手続きガイド
    32: {
        "local": "stock/finance-money/budget-spreadsheet_10144715.jpg",
        "alt": "年金・社会保険の手続き",
        "title": "海外在住者の年金・社会保険ガイド"
    },
    # 33: 海外在住者の確定申告・税金ガイド
    33: {
        "local": "stock/finance-money/tax-calculator_4097292.jpg",
        "alt": "確定申告・税金",
        "title": "海外在住者の確定申告・税金ガイド"
    },
    # 34: 海外移住後のリモートワーク完全ガイド
    34: {
        "local": "stock/remote-work/coworking-space_1702639.jpg",
        "alt": "リモートワークガイド",
        "title": "海外移住後のリモートワーク完全ガイド"
    },
    # 35: 海外在住Webライターの始め方
    35: {
        "local": "stock/remote-work/typing-keyboard_70506.jpg",
        "alt": "Webライターの仕事",
        "title": "海外在住Webライターの始め方"
    },
    # 36: 海外在住者がプログラミング副業で稼ぐ方法
    36: {
        "local": "stock/remote-work/programming-code_1283624.jpg",
        "alt": "プログラミング副業",
        "title": "海外在住者のプログラミング副業"
    },
    # 37: 動画編集・SNS運用代行で稼ぐ方法
    37: {
        "local": "stock/blog-writing/content-creation_6479291.jpg",
        "alt": "動画編集・SNS運用",
        "title": "動画編集・SNS運用代行で稼ぐ方法"
    },
    # 38: オンライン物販（eBay・メルカリ）で稼ぐ方法
    38: {
        "local": "stock/shopping-supermarket/grocery-shopping-cart_1275480.jpg",
        "alt": "オンライン物販",
        "title": "オンライン物販で稼ぐ方法"
    },
    # 39: パラグアイからリモート事務代行で稼ぐ方法
    39: {
        "local": "stock/remote-work/coworking-space_6952917.jpg",
        "alt": "リモート事務代行",
        "title": "リモート事務代行で稼ぐ方法"
    },
    # 40: 海外ノマドにおすすめの国5選
    40: {
        "local": "stock/lifestyle-general/nature-path-walking_4609870.jpg",
        "alt": "海外ノマド生活",
        "title": "海外ノマドにおすすめの国"
    },
    # 41: パラグアイの賃貸・住まい事情
    41: {
        "local": "stock/real-estate/apartment-building_5585737.jpg",
        "alt": "パラグアイの賃貸住宅",
        "title": "パラグアイの賃貸・住まい事情"
    },
    # 42: パラグアイの不動産事情
    42: {
        "local": "stock/real-estate/house-garden-tropical_169540.jpg",
        "alt": "パラグアイの不動産",
        "title": "パラグアイの不動産事情"
    },
    # 43: パラグアイで起業する方法
    43: {
        "local": "stock/finance-money/coins-money-jar_968302.jpg",
        "alt": "パラグアイでの起業",
        "title": "パラグアイで起業する方法"
    },
    # 44: パラグアイの交通事情
    44: {
        "local": "stock/transportation/bus-city-public_2730653.jpg",
        "alt": "パラグアイの交通・バス",
        "title": "パラグアイの交通事情"
    },
    # 45: パラグアイの水道・電気・ガス事情
    45: {
        "local": "stock/lifestyle-general/blue-sky-clouds_5080909.jpg",
        "alt": "パラグアイのライフライン",
        "title": "パラグアイの水道・電気・ガス事情"
    },
    # 46: パラグアイのスーパー・買い物事情
    46: {
        "local": "stock/shopping-supermarket/supermarket-aisle_3105631.jpg",
        "alt": "パラグアイのスーパーマーケット",
        "title": "パラグアイのスーパー・買い物事情"
    },
    # 47: パラグアイで日本食は食べられる？
    47: {
        "local": "stock/food-culture/street-food-latin_6056846.jpg",
        "alt": "パラグアイの日本食",
        "title": "パラグアイの日本食事情"
    },
    # 48: パラグアイの子育て・教育費
    48: {
        "local": "stock/family-education/parent-child-reading_2598005.jpg",
        "alt": "パラグアイの子育て・教育費",
        "title": "パラグアイの子育て・教育費"
    },
    # 49: パラグアイの子供の習い事・スポーツ事情
    49: {
        "local": "stock/kids-activities/children-soccer-playing_4380909.jpg",
        "alt": "パラグアイの子供の習い事",
        "title": "パラグアイの子供の習い事・スポーツ"
    },
    # 50: パラグアイの祝日・文化・イベント
    50: {
        "local": "stock/lifestyle-general/colorful-flowers_3518967.jpg",
        "alt": "パラグアイの文化・祝日",
        "title": "パラグアイの祝日・文化・イベント"
    },
}

# 公開済み記事のWP投稿IDマッピング（アイキャッチ未設定のもの含む）
# CSVの備考欄からWP IDを抽出
PUBLISHED_POSTS = {
    1: 1008,   # 気候
    2: 1214,   # 食文化
    3: 1065,   # 移住費用
    4: 1066,   # 生活費
    5: 1067,   # 治安
    17: 1069,  # 働き方
    14: 1070,  # 海外送金
    22: 1068,  # 子連れ移住
}

# 既にアイキャッチ設定済みの投稿ID
ALREADY_SET = {1008, 1065, 1066, 1067, 1068, 1069, 1070}


def load_secrets():
    with open(SECRETS_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


def load_media_mapping():
    with open(MEDIA_MAPPING_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


def save_media_mapping(mapping):
    with open(MEDIA_MAPPING_PATH, "w", encoding="utf-8") as f:
        json.dump(mapping, f, ensure_ascii=False, indent=2)


def get_wp_auth(secrets):
    username = secrets["wordpress"]["username"]
    app_password = secrets["wordpress"]["app_password"]
    return (username, app_password)


def download_from_pixabay(query, api_key, save_dir, filename_prefix):
    """Pixabay APIから画像をダウンロード"""
    url = "https://pixabay.com/api/"
    params = {
        "key": api_key,
        "q": query,
        "image_type": "photo",
        "orientation": "horizontal",
        "min_width": 1200,
        "min_height": 630,
        "safesearch": "true",
        "per_page": 5,
        "lang": "en"
    }

    resp = requests.get(url, params=params)
    if resp.status_code != 200:
        print(f"  [ERROR] Pixabay API error: {resp.status_code}")
        return None

    data = resp.json()
    if not data.get("hits"):
        print(f"  [WARN] No results for query: {query}")
        return None

    # 最初の画像を使用
    hit = data["hits"][0]
    img_url = hit["largeImageURL"]
    pixabay_id = hit["id"]

    save_path = save_dir / f"{filename_prefix}_{pixabay_id}.jpg"

    if save_path.exists():
        print(f"  [SKIP] Already downloaded: {save_path.name}")
        return save_path

    img_resp = requests.get(img_url, timeout=30)
    if img_resp.status_code != 200:
        print(f"  [ERROR] Image download failed: {img_url}")
        return None

    os.makedirs(save_dir, exist_ok=True)
    with open(save_path, "wb") as f:
        f.write(img_resp.content)

    print(f"  [OK] Downloaded: {save_path.name} (Pixabay ID: {pixabay_id})")
    return save_path


def upload_to_wordpress(image_path, title, alt_text, auth):
    """画像をWordPressにアップロード"""
    filename = image_path.name

    with open(image_path, "rb") as f:
        image_data = f.read()

    headers = {
        "Content-Disposition": f'attachment; filename="{filename}"',
        "Content-Type": "image/jpeg",
    }

    resp = requests.post(
        f"{WP_BASE}/media",
        auth=auth,
        headers=headers,
        data=image_data,
        timeout=60
    )

    if resp.status_code not in (200, 201):
        print(f"  [ERROR] Upload failed for {filename}: {resp.status_code} {resp.text[:200]}")
        return None

    media = resp.json()
    media_id = media["id"]

    # alt textを設定
    requests.post(
        f"{WP_BASE}/media/{media_id}",
        auth=auth,
        json={"alt_text": alt_text, "title": title},
        timeout=30
    )

    print(f"  [OK] Uploaded: {filename} → media_id={media_id}")
    return media_id


def set_featured_image(post_id, media_id, auth):
    """投稿のアイキャッチ画像を設定"""
    resp = requests.post(
        f"{WP_BASE}/posts/{post_id}",
        auth=auth,
        json={"featured_media": media_id},
        timeout=30
    )

    if resp.status_code != 200:
        print(f"  [ERROR] Set featured image failed for post {post_id}: {resp.status_code}")
        return False

    print(f"  [OK] Set featured image: post={post_id}, media={media_id}")
    return True


def check_post_featured_image(post_id, auth):
    """投稿の現在のアイキャッチ画像を確認"""
    resp = requests.get(f"{WP_BASE}/posts/{post_id}", auth=auth, timeout=30)
    if resp.status_code == 200:
        return resp.json().get("featured_media", 0)
    return 0


def main():
    secrets = load_secrets()
    auth = get_wp_auth(secrets)
    pixabay_key = secrets.get("pixabay", {}).get("api_key", "")
    mapping = load_media_mapping()

    # 既にWPにアップロード済みの画像ファイル名を収集
    uploaded_files = set()
    for mid, info in mapping.get("media", {}).items():
        uploaded_files.add(info.get("file", ""))

    results = {
        "uploaded": [],
        "featured_set": [],
        "skipped": [],
        "errors": []
    }

    print("=" * 60)
    print("全記事アイキャッチ画像設定スクリプト")
    print("=" * 60)

    # Step 1: 公開済み記事のアイキャッチ確認
    print("\n--- Step 1: 公開済み記事のアイキャッチ確認 ---")
    for art_num, post_id in PUBLISHED_POSTS.items():
        current = check_post_featured_image(post_id, auth)
        if current and current > 0:
            print(f"  記事#{art_num} (WP:{post_id}) → 設定済み (media:{current})")
            results["skipped"].append(f"#{art_num} WP:{post_id} already has media:{current}")
        else:
            print(f"  記事#{art_num} (WP:{post_id}) → 未設定!")

    # Step 2: 全記事の画像を処理
    print("\n--- Step 2: 画像のアップロードとアイキャッチ設定 ---")

    for art_num, img_info in sorted(ARTICLE_IMAGE_MAP.items()):
        print(f"\n[記事#{art_num}] {img_info['title']}")

        local_path = IMAGES_DIR / img_info["local"]

        # ローカル画像が存在するか確認
        if not local_path.exists():
            if img_info.get("pixabay_fallback") and pixabay_key:
                print(f"  ローカル画像なし → Pixabayからダウンロード...")
                query = img_info.get("pixabay_query", img_info["title"])
                # カテゴリディレクトリを抽出
                category = img_info["local"].split("/")[1] if "/" in img_info["local"] else "general"
                save_dir = STOCK_DIR / category
                prefix = local_path.stem.rsplit("_", 1)[0] if "_" in local_path.stem else local_path.stem

                downloaded = download_from_pixabay(query, pixabay_key, save_dir, prefix)
                if downloaded:
                    local_path = downloaded
                    img_info["local"] = f"stock/{category}/{downloaded.name}"
                else:
                    results["errors"].append(f"#{art_num}: Pixabay download failed")
                    continue
            else:
                print(f"  [SKIP] ローカル画像なし: {img_info['local']}")
                results["errors"].append(f"#{art_num}: local image not found: {img_info['local']}")
                continue

        # WPにアップロード済みか確認
        relative_path = img_info["local"]
        already_uploaded_id = None
        for mid, minfo in mapping.get("media", {}).items():
            if minfo.get("file") == relative_path:
                already_uploaded_id = int(mid)
                break

        if already_uploaded_id:
            media_id = already_uploaded_id
            print(f"  WPアップロード済み: media_id={media_id}")
        else:
            # WordPressにアップロード
            media_id = upload_to_wordpress(local_path, img_info["title"], img_info["alt"], auth)
            if not media_id:
                results["errors"].append(f"#{art_num}: upload failed")
                continue

            # media-mappingに追加
            mapping["media"][str(media_id)] = {
                "file": relative_path,
                "wp_name": local_path.name,
                "title": img_info["title"]
            }
            results["uploaded"].append(f"#{art_num}: {local_path.name} → media:{media_id}")
            time.sleep(1)  # API rate limit

        # 公開済み記事ならアイキャッチを設定
        if art_num in PUBLISHED_POSTS:
            post_id = PUBLISHED_POSTS[art_num]
            if post_id in ALREADY_SET:
                print(f"  アイキャッチ設定済み (WP:{post_id}) → スキップ")
                results["skipped"].append(f"#{art_num}: already set on WP:{post_id}")
            else:
                success = set_featured_image(post_id, media_id, auth)
                if success:
                    mapping.setdefault("post_featured_images", {})[str(post_id)] = {
                        "media_id": media_id,
                        "post_title": img_info["title"]
                    }
                    results["featured_set"].append(f"#{art_num}: WP:{post_id} → media:{media_id}")
                else:
                    results["errors"].append(f"#{art_num}: failed to set featured image on WP:{post_id}")
        else:
            # 下書き記事 → マッピングのみ記録
            mapping.setdefault("draft_featured_images", {})[str(art_num)] = {
                "media_id": media_id,
                "image_file": relative_path,
                "title": img_info["title"],
                "alt": img_info["alt"]
            }
            print(f"  下書き記事 → マッピング記録済み (media:{media_id})")

    # Step 3: media-mapping.json を保存
    print("\n--- Step 3: media-mapping.json 保存 ---")
    mapping["updated"] = "2026-03-13"
    save_media_mapping(mapping)
    print("  [OK] media-mapping.json 更新完了")

    # サマリー
    print("\n" + "=" * 60)
    print("サマリー")
    print("=" * 60)
    print(f"  アップロード: {len(results['uploaded'])} 件")
    print(f"  アイキャッチ設定: {len(results['featured_set'])} 件")
    print(f"  スキップ: {len(results['skipped'])} 件")
    print(f"  エラー: {len(results['errors'])} 件")

    if results["errors"]:
        print("\n[エラー詳細]")
        for e in results["errors"]:
            print(f"  - {e}")

    return 0 if not results["errors"] else 1


if __name__ == "__main__":
    sys.exit(main())
