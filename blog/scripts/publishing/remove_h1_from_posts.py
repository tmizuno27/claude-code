#!/usr/bin/env python3
"""全記事の本文内H1タグを削除（テンプレートのタイトルと重複するため）"""
import json, re, requests, sys
sys.stdout.reconfigure(encoding='utf-8')
from base64 import b64encode
from pathlib import Path

secrets = json.load(open(Path(__file__).parent.parent.parent / "config" / "secrets.json", encoding="utf-8"))
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
            new_raw = re.sub(r"<h1[^>]*>.*?</h1>\s*", "", raw, flags=re.DOTALL)
            if new_raw != raw:
                r3 = requests.post(f"{base}/{endpoint}/{item['id']}", headers=headers, json={"content": new_raw})
                title = item["title"]["rendered"][:50]
                print(f"{r3.status_code} | ID:{item['id']} | {title}")
                count += 1
        page += 1

print(f"\nRemoved H1 from {count} items")
