"""
はてなブログ既存記事のCDATA修正スクリプト
XMLエスケープバグを修正するため、全記事をAtomPub API PUTで再投稿する
"""

import json
import base64
import time
import re
import urllib.request
import xml.etree.ElementTree as ET
from pathlib import Path

BASE_DIR = Path(r"C:\Users\tmizu\マイドライブ\GitHub\claude-code\sites\nambei-oyaji.com")

# 認証情報読み込み
with open(BASE_DIR / "config" / "secrets.json", encoding="utf-8") as f:
    secrets = json.load(f)

hatena = secrets["hatena"]
HATENA_ID = hatena["hatena_id"]
BLOG_ID = hatena["blog_id"]
API_KEY = hatena["api_key"]

# Basic認証ヘッダー
auth_str = base64.b64encode(f"{HATENA_ID}:{API_KEY}".encode()).decode()
AUTH_HEADER = f"Basic {auth_str}"

# hatena-log.json読み込み
with open(BASE_DIR / "published" / "hatena-log.json", encoding="utf-8") as f:
    hatena_log = json.load(f)


def get_entry_id_from_url(hatena_url: str) -> str:
    """ブログURLからentry_idを取得するため、AtomPub一覧APIで探す"""
    # まず一覧を取得してURLとentry_idのマッピングを作る
    pass


def fetch_all_entries() -> dict:
    """AtomPub APIから全エントリを取得し、alternate URLからatom edit URLへのマッピングを返す"""
    url = f"https://blog.hatena.ne.jp/{HATENA_ID}/{BLOG_ID}/atom/entry"
    mapping = {}

    while url:
        req = urllib.request.Request(url, headers={"Authorization": AUTH_HEADER})
        with urllib.request.urlopen(req) as resp:
            body = resp.read().decode("utf-8")

        ns = {
            "atom": "http://www.w3.org/2005/Atom",
            "app": "http://www.w3.org/2007/app",
        }
        root = ET.fromstring(body)

        for entry in root.findall("atom:entry", ns):
            # edit URL
            edit_link = None
            alternate_link = None
            for link in entry.findall("atom:link", ns):
                if link.get("rel") == "edit":
                    edit_link = link.get("href")
                if link.get("rel") == "alternate":
                    alternate_link = link.get("href")
            if edit_link and alternate_link:
                mapping[alternate_link] = edit_link

        # next page
        url = None
        for link in root.findall("atom:link", ns):
            if link.get("rel") == "next":
                url = link.get("href")
                break

    return mapping


def parse_frontmatter(content: str) -> tuple:
    """フロントマターからtitleと本文を分離"""
    match = re.match(r"^---\s*\n(.*?)\n---\s*\n(.*)$", content, re.DOTALL)
    if not match:
        return None, content

    frontmatter = match.group(1)
    body = match.group(2)

    title = None
    for line in frontmatter.split("\n"):
        m = re.match(r'^title:\s*["\']?(.*?)["\']?\s*$', line)
        if m:
            title = m.group(1)
            break

    return title, body


def escape_xml(text: str) -> str:
    """XMLタイトル用エスケープ"""
    return (
        text.replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
        .replace('"', "&quot;")
        .replace("'", "&apos;")
    )


def build_atom_xml(title: str, body: str) -> bytes:
    """CDATA形式のAtom XMLを構築"""
    escaped_title = escape_xml(title)
    xml = f"""<?xml version="1.0" encoding="utf-8"?>
<entry xmlns="http://www.w3.org/2005/Atom"
       xmlns:app="http://www.w3.org/2007/app">
  <title>{escaped_title}</title>
  <author><name>{HATENA_ID}</name></author>
  <content type="text/x-markdown"><![CDATA[{body}]]></content>
  <app:control>
    <app:draft>no</app:draft>
  </app:control>
</entry>"""
    return xml.encode("utf-8")


def update_entry(edit_url: str, title: str, body: str) -> bool:
    """AtomPub API PUTで記事を更新"""
    xml_data = build_atom_xml(title, body)
    req = urllib.request.Request(
        edit_url,
        data=xml_data,
        headers={
            "Authorization": AUTH_HEADER,
            "Content-Type": "application/atom+xml; charset=utf-8",
        },
        method="PUT",
    )
    try:
        with urllib.request.urlopen(req) as resp:
            status = resp.status
            print(f"  -> HTTP {status} OK")
            return True
    except urllib.error.HTTPError as e:
        print(f"  -> HTTP {e.code} ERROR: {e.read().decode('utf-8', errors='replace')[:200]}")
        return False


def main():
    print("=== はてなブログ CDATA修正スクリプト ===\n")

    # Step 1: AtomPub APIから全エントリのedit URLを取得
    print("[1] AtomPub APIからエントリ一覧を取得中...")
    url_mapping = fetch_all_entries()
    print(f"  取得済み: {len(url_mapping)} エントリ\n")

    # Step 2: published記事を処理
    published = hatena_log["published"]
    results = []

    for i, entry in enumerate(published):
        article_id = entry["article_id"]
        hatena_url = entry["hatena_url"]
        hatena_title = entry["hatena_title"]

        print(f"[{i+1}/{len(published)}] 記事ID {article_id}: {hatena_title}")

        # edit URL取得
        edit_url = url_mapping.get(hatena_url)
        if not edit_url:
            print(f"  -> SKIP: edit URLが見つかりません (URL: {hatena_url})")
            results.append({"article_id": article_id, "status": "skip", "reason": "edit URL not found"})
            continue

        # 対応するMDファイルを探す
        converted = [c for c in hatena_log["converted"] if c["article_id"] == article_id]
        if not converted:
            print(f"  -> SKIP: converted情報なし")
            results.append({"article_id": article_id, "status": "skip", "reason": "no converted entry"})
            continue

        md_file = BASE_DIR / "outputs" / "hatena" / converted[0]["hatena_file"]
        if not md_file.exists():
            print(f"  -> SKIP: ファイルなし ({md_file.name})")
            results.append({"article_id": article_id, "status": "skip", "reason": "file not found"})
            continue

        # MD読み込み・パース
        content = md_file.read_text(encoding="utf-8")
        title, body = parse_frontmatter(content)
        if not title:
            title = hatena_title

        print(f"  タイトル: {title}")
        print(f"  本文: {len(body)} 文字")
        print(f"  edit URL: {edit_url}")

        # PUT更新
        success = update_entry(edit_url, title, body)
        results.append({"article_id": article_id, "status": "success" if success else "failed"})

        # 30秒待機（最後以外）
        if i < len(published) - 1:
            print(f"  30秒待機中...\n")
            time.sleep(30)
        else:
            print()

    # 結果サマリー
    print("\n=== 結果サマリー ===")
    success_count = sum(1 for r in results if r["status"] == "success")
    fail_count = sum(1 for r in results if r["status"] == "failed")
    skip_count = sum(1 for r in results if r["status"] == "skip")
    print(f"成功: {success_count}, 失敗: {fail_count}, スキップ: {skip_count}")
    for r in results:
        print(f"  記事ID {r['article_id']}: {r['status']}" + (f" ({r.get('reason', '')})" if r.get("reason") else ""))


if __name__ == "__main__":
    main()
