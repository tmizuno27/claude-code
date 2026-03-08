#!/usr/bin/env python3
"""WordPress全記事から「ランバレ」と「Rank Math 設定用」セクションを一括修正"""
import json, re, requests
from base64 import b64encode
from pathlib import Path

SECRETS = Path(__file__).parent.parent.parent / "config" / "secrets.json"
secrets = json.load(open(SECRETS, encoding="utf-8"))
wp = secrets["wordpress"]
token = b64encode(f'{wp["username"]}:{wp["app_password"]}'.encode()).decode()
headers = {"Authorization": f"Basic {token}", "Content-Type": "application/json"}
base = "https://nambei-oyaji.com/wp-json/wp/v2"

count = 0
for endpoint in ["posts", "pages"]:
    page = 1
    while True:
        r = requests.get(f"{base}/{endpoint}?per_page=100&page={page}&status=publish,draft,private", headers=headers)
        if r.status_code != 200 or not r.json():
            break
        for item in r.json():
            r2 = requests.get(f"{base}/{endpoint}/{item['id']}?context=edit", headers=headers)
            if r2.status_code != 200:
                continue
            raw = r2.json()["content"]["raw"]
            new_raw = raw

            # 1. ランバレ修正
            new_raw = new_raw.replace("パラグアイ・ランバレ在住", "パラグアイ在住")
            new_raw = new_raw.replace("ランバレ在住", "パラグアイ在住")
            new_raw = new_raw.replace("ランバレ", "")

            # 2. Rank Math セクション除去
            new_raw = re.sub(r'<hr\s*/?>\s*<span id="rank-math[^"]*"></span>\s*<h2[^>]*>Rank Math 設定用</h2>[\s\S]*$', '', new_raw)
            new_raw = re.sub(r'<span id="rank-math[^"]*"></span>\s*<h2[^>]*>Rank Math 設定用</h2>[\s\S]*$', '', new_raw)
            new_raw = re.sub(r'<hr\s*/?>\s*<h2[^>]*>Rank Math 設定用</h2>[\s\S]*$', '', new_raw)
            new_raw = re.sub(r'<h2[^>]*>Rank Math 設定用</h2>[\s\S]*$', '', new_raw)
            new_raw = new_raw.rstrip()

            if new_raw != raw:
                changes = []
                if "ランバレ" in raw:
                    changes.append("ランバレ")
                if "Rank Math" in raw and "設定用" in raw:
                    changes.append("RankMath")
                r3 = requests.post(f"{base}/{endpoint}/{item['id']}", headers=headers, json={"content": new_raw})
                title = item["title"]["rendered"][:40]
                print(f"{r3.status_code} | ID:{item['id']} | {' + '.join(changes)} | {title}")
                count += 1
        page += 1

print(f"\nTotal fixed: {count}")
