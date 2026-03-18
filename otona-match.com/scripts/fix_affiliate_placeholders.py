#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
otona-match.com の全公開記事から YOUR-AFFILIATE-LINK プレースホルダーを修正するスクリプト

URL形式: https://YOUR-AFFILIATE-LINK/{service-slug}
- affiliate-links.json に実URLがあるサービスは実URLに置換
- 実URLがないサービス（pending_approval等）は <a> タグを除去してテキストのみ残す
"""

import sys
import json
import re
import requests
from requests.auth import HTTPBasicAuth
from pathlib import Path

BASE_DIR = Path(__file__).parent.parent
SECRETS_FILE = BASE_DIR / "config" / "secrets.json"
AFFILIATE_FILE = BASE_DIR / "config" / "affiliate-links.json"
WP_API = "https://otona-match.com/?rest_route=/wp/v2"

DRY_RUN = "--apply" not in sys.argv


def load_json(path):
    with open(path, encoding="utf-8") as f:
        return json.load(f)


# slug → サービス情報のマップ
SLUG_MAP = {
    "pairs": {
        "name": "Pairs（ペアーズ）",
        "status": "pending_approval",
        "url": None,
        "asp": "未提携",
    },
    "with": {
        "name": "with（ウィズ）",
        "status": "pending_approval",
        "url": None,
        "asp": "未提携",
    },
    "tapple": {
        "name": "タップル",
        "status": "pending_approval",
        "url": None,
        "asp": "未提携",
    },
    "omiai": {
        "name": "Omiai（オミアイ）",
        "status": "pending_approval",
        "url": None,
        "asp": "未提携",
    },
    "marrish": {
        "name": "marrish（マリッシュ）",
        "status": "active",
        "asp": "A8.net",
        "html": '<a href="https://px.a8.net/svt/ejp?a8mat=4AZGCF+DRY4GQ+3N2M+67JUA" rel="nofollow">無料の出会いは(マリッシュ)<br>いいねから始まる恋婚/R18</a><img border="0" width="1" height="1" src="https://www10.a8.net/0.gif?a8mat=4AZGCF+DRY4GQ+3N2M+67JUA" alt="">',
        "url": "https://px.a8.net/svt/ejp?a8mat=4AZGCF+DRY4GQ+3N2M+67JUA",
    },
    "ibj-members": {
        "name": "IBJメンバーズ",
        "status": "pending_approval",
        "url": None,
        "asp": "アクセストレード",
    },
    "partner-agent": {
        "name": "パートナーエージェント",
        "status": "active",
        "url": "https://h.accesstrade.net/sp/cc?rk=0100dq7e00opif",
        "tracking_img": "https://h.accesstrade.net/sp/rr?rk=0100dq7e00opif",
        "asp": "アクセストレード",
    },
    "en-konkatsu": {
        "name": "エン婚活エージェント",
        "status": "pending_approval",
        "url": None,
        "asp": "アクセストレード",
    },
    "sumariage": {
        "name": "スマリッジ（サブスク婚活）",
        "status": "active",
        "url": "//af.moshimo.com/af/c/click?a_id=5432442&p_id=3509&pc_id=8461&pl_id=49639",
        "tracking_img_moshimo": "//i.moshimo.com/af/i/impression?a_id=5432442&p_id=3509&pc_id=8461&pl_id=49639",
        "asp": "もしもアフィリエイト",
    },
    "naco-do": {
        "name": "naco-do（ナコード）",
        "status": "active",
        "url": "https://h.accesstrade.net/sp/cc?rk=0100o94500opif",
        "tracking_img": "https://h.accesstrade.net/sp/rr?rk=0100o94500opif",
        "asp": "アクセストレード",
    },
    "youbride": {
        "name": "youbride（ユーブライド）",
        "status": "pending_approval",
        "url": None,
        "asp": "未提携",
    },
    "bridal-net": {
        "name": "ブライダルネット",
        "status": "pending_approval",
        "url": None,
        "asp": "A8.net",
    },
    "concoi": {
        "name": "concoi（こんこい）",
        "status": "active",
        "url": "https://h.accesstrade.net/sp/cc?rk=0100pvup00opif",
        "tracking_img": "https://h.accesstrade.net/sp/rr?rk=0100pvup00opif",
        "asp": "アクセストレード",
    },
}


def build_slug_map_from_affiliate(affiliate_data):
    """affiliate-links.json からも補完（anchor_text のスラグ推定）"""
    # 上記の SLUG_MAP を基本として使用。必要に応じて拡張
    return SLUG_MAP


def replace_placeholder_links(content, slug_map):
    """
    href="https://YOUR-AFFILIATE-LINK/{slug}" を持つ <a> タグを処理する。
    """
    changes = []

    pattern = re.compile(
        r'<a\s([^>]*)href=["\']https://YOUR-AFFILIATE-LINK/([^"\'>\s]+)["\']([^>]*)>(.*?)</a>',
        re.IGNORECASE | re.DOTALL
    )

    def replacer(m):
        attrs_before = m.group(1)
        slug = m.group(2).rstrip('/')
        attrs_after = m.group(3)
        inner_html = m.group(4)
        full_tag = m.group(0)
        anchor_text = re.sub(r'<[^>]+>', '', inner_html).strip()

        info = slug_map.get(slug)
        if info is None:
            # 不明なスラグ → テキストのみ残す
            changes.append({
                "action": "text_only (unknown slug)",
                "slug": slug,
                "anchor": anchor_text,
                "original": full_tag[:120],
                "result": anchor_text,
            })
            return anchor_text

        status = info.get("status", "unknown")

        if status == "active" and (info.get("url") or info.get("html")):
            if info.get("html"):
                # A8.net バナーHTMLそのまま使う場合は、ボタンスタイルを維持したい
                # ここでは href だけ差し替える
                url = info.get("url")
                new_tag = f'<a {attrs_before}href="{url}"{attrs_after} rel="nofollow">{inner_html}</a>'
                tracking = info.get("tracking_img") or info.get("tracking_img_moshimo")
                if tracking:
                    new_tag += f'<img src="{tracking}" width="1" height="1" style="border:none;display:block;">'
                changes.append({
                    "action": "replaced with url",
                    "slug": slug,
                    "anchor": anchor_text,
                    "service": info["name"],
                    "asp": info.get("asp", ""),
                    "url": url,
                    "original": full_tag[:120],
                    "result": new_tag[:120],
                })
                return new_tag
            else:
                url = info["url"]
                new_tag = f'<a {attrs_before}href="{url}"{attrs_after}>{inner_html}</a>'
                tracking = info.get("tracking_img") or info.get("tracking_img_moshimo")
                if tracking:
                    new_tag += f'<img src="{tracking}" width="1" height="1" style="border:none;display:block;">'
                changes.append({
                    "action": "replaced with url",
                    "slug": slug,
                    "anchor": anchor_text,
                    "service": info["name"],
                    "asp": info.get("asp", ""),
                    "url": url,
                    "original": full_tag[:120],
                    "result": new_tag[:120],
                })
                return new_tag
        else:
            # pending / no url → テキストのみ
            changes.append({
                "action": f"text_only ({status})",
                "slug": slug,
                "anchor": anchor_text,
                "service": info["name"],
                "asp": info.get("asp", ""),
                "original": full_tag[:120],
                "result": anchor_text,
            })
            return anchor_text

    new_content = pattern.sub(replacer, content)
    return new_content, changes


def get_all_published_posts(auth):
    posts = []
    page = 1
    while True:
        resp = requests.get(
            f"{WP_API}/posts",
            params={"status": "publish", "per_page": 100, "page": page, "context": "edit"},
            auth=auth,
            timeout=30,
        )
        if resp.status_code == 400:
            break
        resp.raise_for_status()
        batch = resp.json()
        if not batch:
            break
        posts.extend(batch)
        total_pages = int(resp.headers.get("X-WP-TotalPages", 1))
        if page >= total_pages:
            break
        page += 1
    return posts


def main():
    secrets = load_json(SECRETS_FILE)
    affiliate_data = load_json(AFFILIATE_FILE)
    auth = HTTPBasicAuth(secrets["wordpress"]["username"], secrets["wordpress"]["app_password"])
    slug_map = build_slug_map_from_affiliate(affiliate_data)

    mode = "[DRY-RUN]" if DRY_RUN else "[APPLY]"
    print(f"{mode} 実行開始")
    print(f"  WP API: {WP_API}")
    print(f"  スラグマップ: {len(slug_map)} エントリ\n")

    posts = get_all_published_posts(auth)
    print(f"公開記事数: {len(posts)} 件\n")

    total_changes = 0
    updated_articles = []
    failed_articles = []

    for post in posts:
        post_id = post["id"]
        title_raw = post.get("title", {}).get("rendered", "(no title)")
        content_raw = post.get("content", {}).get("raw", "")

        if "YOUR-AFFILIATE-LINK" not in content_raw:
            continue

        new_content, changes = replace_placeholder_links(content_raw, slug_map)

        if not changes:
            print(f"  [SKIP] ID:{post_id} プレースホルダーあるが変換0件（パターン未マッチ）")
            continue

        total_changes += len(changes)
        updated_articles.append(post_id)

        print(f"━━━ 記事 ID:{post_id} ━━━")
        print(f"  タイトル: {title_raw}")
        for c in changes:
            svc = c.get("service", "?")
            print(f"  [{c['action']}] slug={c.get('slug','?')} service={svc} asp={c.get('asp','?')}")
            print(f"    anchor : {c['anchor'][:60]}")
            print(f"    Before : {c['original'][:80]}...")
            print(f"    After  : {c['result'][:80]}...")
        print()

        if not DRY_RUN:
            update_resp = requests.post(
                f"{WP_API}/posts/{post_id}",
                json={"content": new_content},
                auth=auth,
                timeout=30,
            )
            if update_resp.status_code in (200, 201):
                print(f"  ✅ 更新完了: ID {post_id}")
            else:
                print(f"  ❌ 更新失敗: ID {post_id} status={update_resp.status_code}")
                print(f"     {update_resp.text[:300]}")
                failed_articles.append(post_id)
        print()

    print("=" * 70)
    print(f"処理完了 ({mode})")
    print(f"  変更対象記事数: {len(updated_articles)} 件")
    print(f"  IDs: {updated_articles}")
    print(f"  総置換/修正数 : {total_changes} 件")
    if failed_articles:
        print(f"  ❌ 失敗記事   : {failed_articles}")
    if DRY_RUN:
        print("\n  ※ DRY-RUN モードのため実際の更新は行っていません。")


if __name__ == "__main__":
    main()
