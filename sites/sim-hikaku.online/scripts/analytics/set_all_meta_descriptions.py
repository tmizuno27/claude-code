#!/usr/bin/env python3
"""
全公開記事にメタディスクリプション（excerpt）を一括設定するスクリプト。
excerptが空の記事にのみ設定する。

使い方:
  python set_all_meta_descriptions.py          # dry-run
  python set_all_meta_descriptions.py --apply  # 実行
"""

import sys
import os
import json
import base64
import re
import time
from pathlib import Path

if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")

import requests

SITE_DIR = Path(__file__).resolve().parent.parent.parent
CONFIG_DIR = SITE_DIR / "config"


def load_wp():
    with open(CONFIG_DIR / "secrets.json", encoding="utf-8") as f:
        secrets = json.load(f)
    wp = secrets["wordpress"]
    creds = base64.b64encode(
        f"{wp['username']}:{wp['app_password']}".encode()
    ).decode()
    return wp["api_url"], {
        "Authorization": f"Basic {creds}",
        "Content-Type": "application/json",
    }


def generate_meta(title):
    """タイトルからメタディスクリプションを生成（120文字以内）"""
    base = re.sub(r"【[^】]+】", "", title).strip()

    # キーワード別テンプレート
    if "評判" in title or "口コミ" in title:
        desc = f"{base}。実際の利用者の声を元に料金・速度・サポートを徹底分析。乗り換え前に必読の情報をまとめました。"
    elif "比較" in title or "ランキング" in title:
        desc = f"2026年最新版。{base}。料金・速度・口コミを比較して、あなたに最適なプランがすぐ見つかります。"
    elif "乗り換え" in title or "MNP" in title:
        desc = f"{base}。初心者でも失敗しない手順を図解で解説。キャンペーン情報も随時更新中。"
    elif "おすすめ" in title:
        desc = f"2026年最新版。{base}。料金・速度・特徴を徹底比較して厳選しました。"
    elif "海外" in title or "eSIM" in title:
        desc = f"{base}。現地在住者が実体験をもとに料金・通信品質・設定方法を解説します。"
    else:
        desc = f"2026年最新版。{base}。格安SIM専門家が分かりやすく解説します。"

    if len(desc) > 120:
        desc = desc[:117] + "..."
    return desc


def main():
    apply = "--apply" in sys.argv

    api_url, headers = load_wp()

    # 全公開記事取得
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
                "_fields": "id,title,slug,excerpt",
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

    print(f"公開記事数: {len(all_posts)}")

    # excerptが空の記事を抽出
    targets = []
    for post in all_posts:
        excerpt_html = post.get("excerpt", {}).get("rendered", "")
        # HTMLタグを除去して中身を確認
        excerpt_text = re.sub(r"<[^>]+>", "", excerpt_html).strip()
        # 空 or 自動生成（記事冒頭の切り取り = 150文字超）のものを対象
        if len(excerpt_text) < 10:
            title = post["title"]["rendered"]
            meta = generate_meta(title)
            targets.append({
                "id": post["id"],
                "title": title,
                "meta": meta,
            })

    print(f"メタ未設定: {len(targets)}件\n")

    for i, t in enumerate(targets, 1):
        print(f"  [{i}] ID:{t['id']} {t['title'][:40]}...")
        print(f"      Meta: {t['meta'][:80]}...")

    if apply and targets:
        print(f"\n更新実行中（{len(targets)}件）...")
        ok = 0
        for t in targets:
            try:
                resp = requests.post(
                    f"{api_url}/posts/{t['id']}",
                    headers=headers,
                    json={"excerpt": t["meta"]},
                    timeout=30,
                )
                resp.raise_for_status()
                ok += 1
                print(f"  OK ID:{t['id']}")
                time.sleep(0.5)
            except Exception as e:
                print(f"  NG ID:{t['id']} - {e}")
        print(f"\n完了: {ok}件")
    elif not apply:
        print("\n※ dry-runモード。--apply で実行します。")


if __name__ == "__main__":
    main()
