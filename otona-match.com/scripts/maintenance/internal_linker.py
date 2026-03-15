#!/usr/bin/env python3
"""otona-match.com 内部リンク自動挿入スクリプト"""

import requests
import json
import re
import time
from datetime import datetime

# WordPress API設定
BASE_URL = "https://otona-match.com/?rest_route=/wp/v2/"
AUTH = ("t.mizuno27@gmail.com", "Yw4j OgFf wwzT o0mn wXQ9 TjYs")

# リンクマップ定義: source_slug -> [(target_slug, anchor_text)]
LINK_MAP = {
    # HIGHEST PRIORITY - Isolated articles
    "kekkon-soudan-ryoukin-hikaku": [("kekkon-soudan-30dai-josei", "30代女性の結婚相談所選び")],
    "kekkon-soudan-seikon-ritsu": [
        ("kekkon-soudan-30dai-josei", "30代女性におすすめの結婚相談所"),
        ("kekkon-soudan-mendan-nagare", "結婚相談所の面談の流れ"),
    ],
    "kekkon-soudan-osusume": [("kekkon-soudan-mendan-nagare", "結婚相談所の面談の流れと準備")],
    "matching-app-shinjitsu-uso": [("matching-app-nenrei-sasyou", "マッチングアプリの年齢詐称の実態")],
    "sakura-gyosha-miwakekata": [
        ("matching-app-nenrei-sasyou", "年齢詐称の見分け方"),
        ("matching-app-kiken-jinbutsu", "マッチングアプリの危険人物の特徴"),
    ],
    "anzen-checklist": [("matching-app-kiken-jinbutsu", "危険人物を見分けるチェックリスト")],
    "konkatsu-40dai": [("konkatsu-dansei-shippai", "婚活で失敗する男性の共通点")],
    "konkatsu-app-osusume": [
        ("konkatsu-dansei-shippai", "男性が婚活で失敗しないためのポイント"),
        ("youbride-review", "ユーブライドの口コミ・評判"),
        ("omiai-review", "Omiaiの口コミ・評判"),
        ("marrish-review", "マリッシュの口コミ・評判"),
        ("kekkon-soudan-vs-app", "結婚相談所とマッチングアプリの比較"),
    ],
    "matching-app-tomodachi-kara": [("matching-app-inja-mukidashi", "マッチングアプリは陰キャにも向いている")],
    "matching-app-profile-kakikata": [("matching-app-inja-mukidashi", "陰キャでも成功するプロフィールの書き方")],
    "matching-app-nentai-betsu": [("matching-app-igirisu-gaikokujin", "外国人と出会えるマッチングアプリ")],
    # PILLAR STRENGTHENING
    "matching-app-ranking-2026": [
        ("matching-app-nentai-betsu", "年代別おすすめマッチングアプリ"),
        ("konkatsu-app-osusume", "婚活アプリおすすめランキング"),
        ("sakura-gyosha-miwakekata", "サクラ・業者の見分け方"),
        ("matching-app-saiyasune", "マッチングアプリの最安値比較"),
    ],
    "deaikei-vs-matching-app": [
        ("happy-mail-review", "ハッピーメールの口コミ・評判"),
        ("pcmax-review", "PCMAXの口コミ・評判"),
        ("wakuwaku-mail-review", "ワクワクメールの口コミ・評判"),
        ("sakura-gyosha-miwakekata", "サクラ・業者の見分け方"),
    ],
    # CROSS-CATEGORY
    "pairs-review": [
        ("matching-app-30dai-osusume", "30代におすすめのマッチングアプリ"),
        ("omiai-review", "Omiaiの口コミ・評判"),
        ("matching-app-jikoshoukai", "マッチングアプリの自己紹介の書き方"),
    ],
    "with-review": [
        ("tapple-review", "タップルの口コミ・評判"),
        ("matching-app-ranking-2026", "マッチングアプリおすすめランキング2026"),
        ("matching-app-first-message", "マッチングアプリの最初のメッセージ"),
    ],
    "omiai-review": [
        ("matching-app-30dai-osusume", "30代におすすめのマッチングアプリ"),
        ("kekkon-soudan-vs-app", "結婚相談所とマッチングアプリどっちがいい？"),
    ],
    "marrish-review": [
        ("matching-app-batuichi-saikon", "バツイチ・再婚向けマッチングアプリ"),
        ("matching-app-40dai-osusume", "40代におすすめのマッチングアプリ"),
    ],
    "kekkon-soudan-vs-app": [
        ("kekkon-soudan-osusume", "おすすめの結婚相談所"),
        ("kekkon-soudan-ryoukin-hikaku", "結婚相談所の料金比較"),
        ("konkatsu-app-osusume", "婚活アプリおすすめランキング"),
        ("online-kekkon-soudan-hikaku", "オンライン結婚相談所の比較"),
    ],
    "kekkon-soudan-osusume": [
        ("kekkon-soudan-ryoukin-hikaku", "結婚相談所の料金を徹底比較"),
        ("kekkon-soudan-seikon-ritsu", "結婚相談所の成婚率ランキング"),
        ("kekkon-soudan-mendan-nagare", "結婚相談所の面談の流れ"),
    ],
    "sakura-gyosha-miwakekata-cross": [],  # already handled above, skip duplicate key
    "anzen-checklist-cross": [],  # already handled above
    "happy-mail-review": [
        ("deaikei-vs-matching-app", "出会い系とマッチングアプリの違い"),
        ("deaikei-anzen-tsukaikata", "出会い系アプリの安全な使い方"),
        ("wakuwaku-mail-review", "ワクワクメールの口コミ・評判"),
    ],
    "pcmax-review": [
        ("deaikei-vs-matching-app", "出会い系とマッチングアプリの違い"),
        ("deaikei-anzen-tsukaikata", "出会い系アプリの安全な使い方"),
        ("happy-mail-review", "ハッピーメールの口コミ・評判"),
    ],
}

# Additional entries for sakura/anzen cross-category (merge into existing keys)
LINK_MAP.setdefault("sakura-gyosha-miwakekata", []).extend([
    ("anzen-checklist", "マッチングアプリの安全チェックリスト"),
    ("matching-app-shinjitsu-uso", "マッチングアプリの嘘と真実"),
    ("matching-app-mibare-taisaku", "マッチングアプリの身バレ対策"),
])
LINK_MAP.setdefault("anzen-checklist", []).extend([
    ("sakura-gyosha-miwakekata", "サクラ・業者の見分け方"),
    ("matching-app-mibare-taisaku", "身バレ対策の完全ガイド"),
    ("matching-app-shinjitsu-uso", "マッチングアプリの嘘を見抜く方法"),
])

# Deduplicate targets per source
for k in LINK_MAP:
    seen = set()
    deduped = []
    for slug, anchor in LINK_MAP[k]:
        if slug not in seen:
            seen.add(slug)
            deduped.append((slug, anchor))
    LINK_MAP[k] = deduped

MAX_NEW_LINKS = 4


def fetch_all_posts():
    """全公開記事を取得"""
    posts = []
    page = 1
    while True:
        r = requests.get(
            BASE_URL + "posts",
            params={"per_page": 100, "page": page, "status": "publish"},
            auth=AUTH,
        )
        if r.status_code != 200:
            break
        data = r.json()
        if not data:
            break
        posts.extend(data)
        if len(data) < 100:
            break
        page += 1
    return posts


def build_slug_map(posts):
    """slug → {id, url, title} マップ"""
    m = {}
    for p in posts:
        m[p["slug"]] = {
            "id": p["id"],
            "url": p["link"],
            "title": p["title"]["rendered"],
        }
    return m


def build_related_box(links):
    """あわせて読みたいボックスHTML生成"""
    items = "\n".join(f'<li><a href="{url}">{title}</a></li>' for url, title in links)
    return (
        '\n<!-- internal-links-auto -->\n'
        '<div class="related-box" style="background:#f8f9fa;border-left:4px solid #4285f4;'
        'padding:16px;margin:24px 0;border-radius:4px;">\n'
        '<p style="font-weight:bold;margin:0 0 8px;">あわせて読みたい</p>\n'
        f'<ul style="margin:0;padding-left:20px;">\n{items}\n</ul>\n'
        '</div>\n'
    )


def insert_links(content, new_links):
    """記事本文にリンクボックスを挿入"""
    box = build_related_box(new_links)
    # Try to insert before the last closing </div> or </section>
    # Find last substantial closing tag
    last_div = content.rfind("</div>")
    if last_div > len(content) // 2:
        return content[:last_div] + box + content[last_div:]
    # Fallback: append
    return content + box


def main():
    print(f"=== otona-match.com 内部リンク挿入 === {datetime.now()}")
    print("記事取得中...")
    posts = fetch_all_posts()
    print(f"  {len(posts)}件取得")

    slug_map = build_slug_map(posts)
    post_content_cache = {p["slug"]: p["content"]["rendered"] for p in posts}

    total_updated = 0
    total_links_added = 0
    log = []

    for source_slug, targets in LINK_MAP.items():
        if not targets:
            continue
        if source_slug not in slug_map:
            print(f"  SKIP: {source_slug} (記事が見つかりません)")
            continue

        source = slug_map[source_slug]
        # Fetch fresh content for editing (raw)
        r = requests.get(
            BASE_URL + f"posts/{source['id']}",
            params={"context": "edit"},
            auth=AUTH,
        )
        if r.status_code != 200:
            print(f"  ERROR: {source_slug} fetch failed ({r.status_code})")
            continue

        raw_content = r.json()["content"]["raw"]

        # Check which links already exist
        new_links = []
        for target_slug, anchor in targets:
            if target_slug not in slug_map:
                print(f"    SKIP target: {target_slug} (記事なし)")
                continue
            target = slug_map[target_slug]
            # Check if URL already in content
            if target["url"] in raw_content or f"/{target_slug}" in raw_content:
                continue
            new_links.append((target["url"], anchor))
            if len(new_links) >= MAX_NEW_LINKS:
                break

        if not new_links:
            continue

        # Insert links
        updated_content = insert_links(raw_content, new_links)

        # Update post
        r = requests.post(
            BASE_URL + f"posts/{source['id']}",
            json={"content": updated_content},
            auth=AUTH,
        )
        if r.status_code == 200:
            total_updated += 1
            total_links_added += len(new_links)
            link_names = [anchor for _, anchor in new_links]
            log.append(f"  OK {source_slug} (ID:{source['id']}): +{len(new_links)} links -> {link_names}")
            print(log[-1])
        else:
            print(f"  ERROR: {source_slug} update failed ({r.status_code}): {r.text[:200]}")

        time.sleep(0.5)  # rate limit

    print("\n=== 結果サマリー ===")
    print(f"更新記事数: {total_updated}")
    print(f"追加リンク数: {total_links_added}")
    print("\n詳細:")
    for entry in log:
        print(entry)


if __name__ == "__main__":
    main()
