import requests
import json
from requests.auth import HTTPBasicAuth

WP_URL = "https://otona-match.com/?rest_route=/wp/v2/posts"
AUTH = HTTPBasicAuth("t.mizuno27@gmail.com", "Yw4j OgFf wwzT o0mn wXQ9 TjYs")

articles = [
    {
        "slug": "matching-app-video-tsuwwa",
        "title": "マッチングアプリのビデオ通話のコツ｜会う前に好印象を与える方法",
        "category": 5,
        "file": r"c:\Users\tmizu\マイドライブ\GitHub\claude-code\otona-match.com\outputs\matching-app-video-tsuwwa.html",
    },
    {
        "slug": "matching-app-nenrei-sasyou",
        "title": "マッチングアプリの年齢詐称はバレる？リスクと見抜き方を解説",
        "category": 6,
        "file": r"c:\Users\tmizu\マイドライブ\GitHub\claude-code\otona-match.com\outputs\matching-app-nenrei-sasyou.html",
    },
    {
        "slug": "matching-app-saiyasune",
        "title": "マッチングアプリを最安で使う方法｜無料プラン活用＆割引テクニック",
        "category": 2,
        "file": r"c:\Users\tmizu\マイドライブ\GitHub\claude-code\otona-match.com\outputs\matching-app-saiyasune.html",
    },
]

for art in articles:
    with open(art["file"], "r", encoding="utf-8") as f:
        content = f.read()

    data = {
        "title": art["title"],
        "slug": art["slug"],
        "content": content,
        "status": "publish",
        "categories": [art["category"]],
    }

    resp = requests.post(WP_URL, json=data, auth=AUTH)
    if resp.status_code == 201:
        result = resp.json()
        print(f"OK: {art['slug']} -> WP ID: {result['id']}, URL: {result['link']}")
    else:
        print(f"FAIL: {art['slug']} -> {resp.status_code}: {resp.text[:300]}")
