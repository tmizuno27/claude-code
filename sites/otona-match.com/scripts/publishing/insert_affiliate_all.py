#!/usr/bin/env python3
"""
otona-match.com — 全記事アフィリエイトリンク一括挿入スクリプト
WordPress REST API経由で全公開記事を取得し、設定済みリンクをキーワードマッチで挿入する。

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

import requests

if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
CONFIG_DIR = PROJECT_ROOT / "config"

# ── 設定読み込み ──
def load_config():
    with open(CONFIG_DIR / "settings.json", encoding="utf-8") as f:
        config = json.load(f)
    secrets_path = CONFIG_DIR / "secrets.json"
    if secrets_path.exists():
        with open(secrets_path, encoding="utf-8") as f:
            secrets = json.load(f)
        for section, values in secrets.items():
            if isinstance(values, dict) and section in config:
                config[section].update(values)
    return config

def load_affiliates():
    with open(CONFIG_DIR / "affiliate-links.json", encoding="utf-8") as f:
        return json.load(f)

# ── WordPress API ──
class WPClient:
    def __init__(self, config):
        wp = config["wordpress"]
        self.base_url = wp["rest_api_url"]
        creds = f"{wp['username']}:{wp['app_password']}"
        token = b64encode(creds.encode()).decode()
        self.headers = {
            "Authorization": f"Basic {token}",
            "Content-Type": "application/json",
        }

    def get_all_posts(self):
        """全公開記事を取得"""
        posts = []
        page = 1
        while True:
            sep = "&" if "?" in self.base_url else "?"
            url = f"{self.base_url}/posts{sep}status=publish&per_page=100&page={page}&context=edit"
            resp = requests.get(url, headers=self.headers, timeout=30)
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
        resp = requests.post(url, headers=self.headers, json={"content": content}, timeout=30)
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
    # h1-h4タグ内かチェック
    for tag in ('h1', 'h2', 'h3', 'h4'):
        opens = len(re.findall(rf'<{tag}\b', before, re.IGNORECASE))
        closes = len(re.findall(rf'</{tag}>', before, re.IGNORECASE))
        if opens > closes:
            return True
    return False

def replace_keyword(content, keyword, link_html, affiliate_url, max_replace=2):
    """キーワードをアフィリエイトリンクに置換。安全チェック付き。"""
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

        # 近くに既にアフィリエイトURLがあればスキップ
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


def _extract_url_from_html(html_str):
    """HTMLタグからhref URLを抽出"""
    m = re.search(r'href="([^"]+)"', html_str)
    return m.group(1) if m else ""


def _extract_tracking_from_html(html_str):
    """A8.net等のHTML素材からトラッキング画像URLを抽出"""
    m = re.search(r'<img[^>]+src="([^"]+)"', html_str)
    return m.group(1) if m else ""


def build_link_rules(affiliates):
    """affiliate-links.json から挿入ルールリストを構築。
    プレースホルダーや承認待ちはスキップ。
    url フィールドと html / html_a8 フィールドの両方に対応。"""
    rules = []
    categories = affiliates.get("categories", {})
    for cat_key, cat in categories.items():
        for link in cat.get("links", []):
            if link.get("status") in ("pending_approval", "rejected"):
                continue

            url = link.get("url", "")
            html_raw = link.get("html", "")
            html_a8 = link.get("html_a8", "")

            # url も html も無ければスキップ
            if not url and not html_raw and not html_a8:
                continue
            if url and "YOUR-AFFILIATE-LINK" in url:
                continue

            # A8.net HTMLが優先（CTRが高い素材を選定済み）、次にhtml、最後にurl
            if html_a8:
                use_html = html_a8
                use_url = _extract_url_from_html(html_a8)
                tracking_img_url = _extract_tracking_from_html(html_a8)
            elif html_raw:
                use_html = html_raw
                use_url = _extract_url_from_html(html_raw)
                tracking_img_url = _extract_tracking_from_html(html_raw)
            else:
                use_html = ""
                use_url = url
                # tracking_img の抽出（従来ロジック）
                tracking_img_url = ""
                tracking_img_raw = link.get("tracking_img", "")
                tracking_img_moshimo = link.get("tracking_img_moshimo", "")
                tracking_img_vc = link.get("tracking_img_vc", "")

                if tracking_img_raw:
                    img_match = re.search(r'src="([^"]+)"', tracking_img_raw)
                    if img_match:
                        tracking_img_url = img_match.group(1)
                    elif not tracking_img_raw.startswith("<"):
                        tracking_img_url = tracking_img_raw
                elif tracking_img_moshimo:
                    tracking_img_url = tracking_img_moshimo
                elif tracking_img_vc:
                    tracking_img_url = tracking_img_vc

            keywords = link.get("anchor_text", [link["name"]])

            for kw in keywords:
                if use_html:
                    # HTML素材からリンク部分だけ抽出し、アンカーテキストを差し替え
                    a_match = re.search(r'(<a\b[^>]+>)(.*?)(</a>)', use_html, re.DOTALL)
                    if a_match:
                        link_html = f'{a_match.group(1)}{kw}{a_match.group(3)}'
                    else:
                        link_html = use_html
                else:
                    link_html = f'<a href="{use_url}" rel="nofollow" target="_blank">{kw}</a>'

                rules.append({
                    "keyword": kw,
                    "link_html": link_html,
                    "url": use_url,
                    "name": link["name"],
                    "tracking_img_url": tracking_img_url,
                })

    return rules


def process_post(post, rules, dry_run=True):
    """1記事を処理。変更があれば (post_id, new_content, changes) を返す。"""
    post_id = post["id"]
    title = post.get("title", {}).get("rendered", "")
    content = post.get("content", {}).get("raw", "")
    if not content:
        return None

    total_changes = []
    new_content = content

    # 各ルールでキーワード置換
    applied_services = set()
    for rule in rules:
        # 同じサービスは1記事あたり1回だけ適用（anchor_textが複数ある場合）
        if rule["name"] in applied_services:
            continue
        updated, count = replace_keyword(new_content, rule["keyword"], rule["link_html"], rule["url"], max_replace=2)
        if count > 0:
            new_content = updated
            total_changes.append(f"{rule['name']}({rule['keyword']}) x{count}")
            applied_services.add(rule["name"])

    # トラッキング画像追加（変更があったサービスのみ）
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
    config = load_config()
    affiliates = load_affiliates()
    rules = build_link_rules(affiliates)

    print(f"=== otona-match.com アフィリエイトリンク一括挿入 ===")
    print(f"モード: {'DRY RUN（--apply で実行）' if dry_run else '本番実行'}")
    print(f"挿入ルール: {len(rules)}件")
    seen = set()
    for r in rules:
        if r["name"] not in seen:
            print(f"  - {r['name']}: {r['keyword']}")
            seen.add(r["name"])
    print()

    wp = WPClient(config)
    print("全公開記事を取得中...")
    posts = wp.get_all_posts()
    print(f"取得完了: {len(posts)}件\n")

    updated = 0
    skipped = 0

    for post in posts:
        result = process_post(post, rules, dry_run)
        if result is None:
            skipped += 1
            continue

        changes_str = ", ".join(result["changes"])
        print(f"[{'予定' if dry_run else '更新'}] ID:{result['post_id']} {result['title']}")
        print(f"  → {changes_str}")

        if not dry_run:
            success = wp.update_post(result["post_id"], result["content"])
            print(f"  {'SUCCESS' if success else 'FAILED'}")
            time.sleep(0.5)  # API負荷軽減

        updated += 1

    print(f"\n=== 結果 ===")
    print(f"更新{'予定' if dry_run else '完了'}: {updated}件")
    print(f"変更なし: {skipped}件")
    if dry_run:
        print(f"\n実行するには: python insert_affiliate_all.py --apply")


if __name__ == "__main__":
    main()
