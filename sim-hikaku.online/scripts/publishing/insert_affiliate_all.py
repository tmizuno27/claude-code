#!/usr/bin/env python3
"""
sim-hikaku.online — 全記事アフィリエイトリンク一括挿入スクリプト
WordPress REST API経由で全公開記事を取得し、提携済みリンクをキーワードマッチで挿入する。

使い方:
  python insert_affiliate_all.py           # dry-run（確認のみ）
  python insert_affiliate_all.py --apply   # 実際に更新
"""

import sys
import re
import json
import time
from pathlib import Path
from base64 import b64encode

import requests as req_lib

if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
CONFIG_DIR = PROJECT_ROOT / "config"

# ── 設定読み込み ──
def load_secrets():
    with open(CONFIG_DIR / "secrets.json", encoding="utf-8") as f:
        return json.load(f)

def load_affiliates():
    with open(CONFIG_DIR / "affiliate-links.json", encoding="utf-8") as f:
        return json.load(f)

# ── WordPress API ──
class WPClient:
    def __init__(self, secrets):
        wp = secrets["wordpress"]
        api_url = wp.get("api_url", "https://sim-hikaku.online/wp-json/wp/v2")
        self.base_url = api_url
        creds = f"{wp['username']}:{wp['app_password']}"
        token = b64encode(creds.encode()).decode()
        self.headers = {
            "Authorization": f"Basic {token}",
            "Content-Type": "application/json",
        }

    def get_all_posts(self):
        posts = []
        page = 1
        while True:
            url = f"{self.base_url}/posts?status=publish&per_page=100&page={page}&context=edit"
            resp = req_lib.get(url, headers=self.headers, timeout=30)
            if resp.status_code != 200:
                break
            batch = resp.json()
            if not batch:
                break
            posts.extend(batch)
            page += 1
            time.sleep(0.3)
        return posts

    def update_post(self, post_id, content):
        url = f"{self.base_url}/posts/{post_id}"
        resp = req_lib.post(url, headers=self.headers, json={"content": content}, timeout=30)
        return resp.status_code == 200

# ── HTML内キーワード置換ロジック ──
def is_inside_tag(text, pos):
    before = text[:pos]
    return before.rfind('<') > before.rfind('>')

def is_inside_a_tag(text, pos):
    before = text[:pos]
    return len(re.findall(r'<a\b', before, re.IGNORECASE)) > len(re.findall(r'</a>', before, re.IGNORECASE))

def is_inside_heading(text, pos):
    before = text[:pos]
    for tag in ('h1', 'h2', 'h3', 'h4'):
        opens = len(re.findall(rf'<{tag}\b', before, re.IGNORECASE))
        closes = len(re.findall(rf'</{tag}>', before, re.IGNORECASE))
        if opens > closes:
            return True
    return False

def replace_keyword(content, keyword, link_html, affiliate_url, max_replace=2):
    count = 0
    result = []
    pos = 0
    pattern = re.compile(re.escape(keyword))

    for m in pattern.finditer(content):
        if count >= max_replace:
            break
        start, end = m.start(), m.end()

        if is_inside_tag(content, start):
            continue
        if is_inside_a_tag(content, start):
            continue
        if is_inside_heading(content, start):
            continue

        ctx_start = max(0, start - 300)
        ctx_end = min(len(content), end + 300)
        if affiliate_url in content[ctx_start:ctx_end]:
            continue

        result.append(content[pos:start])
        result.append(link_html)
        pos = end
        count += 1

    result.append(content[pos:])
    return ''.join(result), count


def build_link_rules(affiliates):
    """affiliate-links.json から挿入ルールリストを構築。
    提携済のもののみ使用。carriers + esim_services 両方を処理。"""
    rules = []

    # carriers
    carriers = affiliates.get("carriers", {})
    for key, carrier in carriers.items():
        if carrier.get("status") != "提携済":
            continue
        url = carrier.get("url")
        if not url or "YOUR-AFFILIATE-LINK" in url:
            continue
        name = carrier["name"]
        tracking_img_url = carrier.get("tracking_img", "")

        # キャリア名でマッチ
        keywords = [name]
        # ワイモバイル → Y!mobile も追加
        if "ワイモバイル" in name:
            keywords.extend(["ワイモバイル", "Y!mobile", "Ymobile"])

        for kw in keywords:
            link_html = f'<a href="{url}" rel="nofollow" target="_blank">{kw}</a>'
            rules.append({
                "keyword": kw,
                "link_html": link_html,
                "url": url,
                "name": name,
                "tracking_img_url": tracking_img_url,
            })

    # esim_services
    esim = affiliates.get("esim_services", {})
    for key, svc in esim.items():
        if svc.get("status") != "提携済":
            continue
        url = svc.get("url")
        if not url or "YOUR-AFFILIATE-LINK" in url:
            continue
        name = svc["name"]
        tracking_img_url = svc.get("tracking_img", "")

        # サービス名の各表記でマッチ
        keywords = [name]
        if "TRAVeSIM" in name:
            keywords.extend(["TRAVeSIM", "トラベシム"])
        elif "Voye" in name:
            keywords.extend(["Voye Global", "ボイエ"])
        elif "trifa" in name:
            keywords.extend(["trifa", "トリファ"])

        # 重複除去
        keywords = list(dict.fromkeys(keywords))

        for kw in keywords:
            link_html = f'<a href="{url}" rel="nofollow" target="_blank">{kw}</a>'
            rules.append({
                "keyword": kw,
                "link_html": link_html,
                "url": url,
                "name": name,
                "tracking_img_url": tracking_img_url,
            })

    return rules


def process_post(post, rules):
    post_id = post["id"]
    title = post.get("title", {}).get("rendered", "")
    content = post.get("content", {}).get("raw", "")
    if not content:
        return None

    total_changes = []
    new_content = content

    applied_services = set()
    for rule in rules:
        if rule["name"] in applied_services:
            continue
        updated, count = replace_keyword(new_content, rule["keyword"], rule["link_html"], rule["url"], max_replace=2)
        if count > 0:
            new_content = updated
            total_changes.append(f"{rule['name']}({rule['keyword']}) x{count}")
            applied_services.add(rule["name"])

    # トラッキング画像追加
    for rule in rules:
        if rule["name"] in applied_services and rule.get("tracking_img_url"):
            img_url = rule["tracking_img_url"]
            if img_url not in new_content:
                img_tag = f'<img src="{img_url}" width="1" height="1" style="border:none;" alt="" />'
                new_content += "\n" + img_tag

    if not total_changes:
        return None

    return {
        "post_id": post_id,
        "title": title,
        "content": new_content,
        "changes": total_changes,
    }


def main():
    dry_run = "--apply" not in sys.argv
    secrets = load_secrets()
    affiliates = load_affiliates()
    rules = build_link_rules(affiliates)

    print(f"=== sim-hikaku.online アフィリエイトリンク一括挿入 ===")
    print(f"モード: {'DRY RUN（--apply で実行）' if dry_run else '本番実行'}")
    print(f"有効なルール: {len(rules)}件")
    seen = set()
    for r in rules:
        if r["name"] not in seen:
            print(f"  - {r['name']}: {r['keyword']}")
            seen.add(r["name"])
    print()

    wp = WPClient(secrets)
    print("全公開記事を取得中...")
    posts = wp.get_all_posts()
    print(f"取得完了: {len(posts)}件\n")

    updated = 0
    skipped = 0

    for post in posts:
        result = process_post(post, rules)
        if result is None:
            skipped += 1
            continue

        changes_str = ", ".join(result["changes"])
        print(f"[{'予定' if dry_run else '更新'}] ID:{result['post_id']} {result['title']}")
        print(f"  → {changes_str}")

        if not dry_run:
            success = wp.update_post(result["post_id"], result["content"])
            print(f"  {'SUCCESS' if success else 'FAILED'}")
            time.sleep(0.5)

        updated += 1

    print(f"\n=== 結果 ===")
    print(f"更新{'予定' if dry_run else '完了'}: {updated}件")
    print(f"変更なし: {skipped}件")
    if dry_run:
        print(f"\n実行するには: python insert_affiliate_all.py --apply")


if __name__ == "__main__":
    main()
