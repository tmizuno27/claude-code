#!/usr/bin/env python3
"""修正漏れがないか確認"""
import json, requests
from base64 import b64encode
from pathlib import Path

secrets = json.load(open(Path(__file__).parent.parent.parent / "config" / "secrets.json", encoding="utf-8"))
wp = secrets["wordpress"]
token = b64encode(f'{wp["username"]}:{wp["app_password"]}'.encode()).decode()
headers = {"Authorization": f"Basic {token}"}
base = "https://nambei-oyaji.com/wp-json/wp/v2"

found = 0
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
            issues = []
            if "ランバレ" in raw:
                issues.append("ランバレ")
            if "Rank Math" in raw and "設定用" in raw:
                issues.append("RankMath")
            if issues:
                print(f"REMAINING: ID:{item['id']} | {issues} | {item['title']['rendered'][:40]}")
                found += 1
        page += 1

print(f"\nRemaining issues: {found}")
