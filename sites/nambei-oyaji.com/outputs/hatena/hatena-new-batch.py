#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
はてなブログ新規記事5本を生成・投稿するスクリプト
"""

import json
import time
import requests
from base64 import b64encode
from datetime import datetime
from pathlib import Path

# 設定
SECRETS_PATH = Path(r"C:\Users\tmizu\マイドライブ\GitHub\claude-code\sites\nambei-oyaji.com\config\secrets.json")
HATENA_LOG_PATH = Path(r"C:\Users\tmizu\マイドライブ\GitHub\claude-code\sites\nambei-oyaji.com\published\hatena-log.json")
HATENA_OUTPUT_DIR = Path(r"C:\Users\tmizu\マイドライブ\GitHub\claude-code\sites\nambei-oyaji.com\outputs\hatena")

# はてなブログ投稿する5記事（タイトル・URL・本文）
ARTICLES = [
    {
        "wp_id": 3513,
        "hatena_title": "パラグアイで不動産を買う方法｜外国人でも購入できる？アスンシオン在住者が解説",
        "url": "https://nambei-oyaji.com/paraguay-real-estate-buy-property/?utm_source=hatena&utm_medium=blog&utm_campaign=digest",
        "tags": ["パラグアイ", "海外移住", "不動産", "アスンシオン"],
        "body": """アスンシオンに移住してから「パラグアイで家を買えるの？」という質問をよく受ける。

結論から言うと、**外国人でも日本人でも、パラグアイでは不動産を購入できる**。しかも手続きが比較的シンプルで、日本と比べてかなりハードルが低い。

パラグアイの不動産価格は日本と比べてかなり安い。アスンシオン中心部のマンションでも、東京の郊外の中古物件より安く買えることも多い。

ただし、実際に購入するとなると気をつけるべき点がいくつかある。

**外国人が不動産購入で注意すべき3つのポイント**

1. **登記の確認**：パラグアイでは土地の所有権登記が不完全なケースがある。信頼できる現地弁護士に権利関係の確認を依頼するのが必須

2. **支払い方法**：現金一括が基本。住宅ローンの制度はあるが、外国人が借りるのはハードルが高い

3. **エリア選定**：アスンシオン市内でも治安の差が大きい。在住者の口コミを参考にエリアを絞ること

移住してから買うか、投資目的で買うかによっても選び方が変わる。詳しい手順・費用・注意点は本家記事にまとめた。

→ <a href="https://nambei-oyaji.com/paraguay-real-estate-buy-property/?utm_source=hatena&utm_medium=blog&utm_campaign=digest">パラグアイの不動産購入方法【完全ガイド】外国人でも買える手順・費用・注意点</a>
"""
    },
    {
        "wp_id": 3512,
        "hatena_title": "パラグアイで日本人が働く方法｜仕事の見つけ方・職種・リモートワーク事情",
        "url": "https://nambei-oyaji.com/paraguay-japanese-jobs-work/?utm_source=hatena&utm_medium=blog&utm_campaign=digest",
        "tags": ["パラグアイ", "海外移住", "仕事", "リモートワーク"],
        "body": """「パラグアイに移住したいけど、仕事はどうするの？」

アスンシオンに移住してから1年以上。現地で実際に働いている日本人と話してきた経験から言うと、パラグアイで日本人が稼ぐ方法は大きく3パターンある。

**パターン1：リモートワーク（日本の仕事を継続）**
一番現実的なのがこれ。プログラマー・ライター・デザイナー・コンサルタントなど、場所を選ばないスキル職なら日本のクライアントから収入を得ながら生活できる。パラグアイは物価が安いので、日本円収入があれば余裕のある生活が可能。

**パターン2：現地日系企業への就職**
パラグアイには日系企業もあり、日本語を活かした仕事も一部ある。ただし求人数は少なく競争率も高い。

**パターン3：現地で起業・フリーランス**
農業・飲食・貿易など、パラグアイならではのビジネスチャンスを掴む人もいる。スペイン語が一定レベル必要だが、チャンスは大きい。

移住前に稼げるスキルを身につけておくことが、パラグアイ生活成功の鍵だと思っている。

詳しい職種・収入目安・仕事の探し方は本家で解説している。

→ <a href="https://nambei-oyaji.com/paraguay-japanese-jobs-work/?utm_source=hatena&utm_medium=blog&utm_campaign=digest">パラグアイで日本人が働く方法｜仕事の見つけ方・職種・リモートワーク事情【2026年版】</a>
"""
    },
    {
        "wp_id": 2152,
        "hatena_title": "海外移住前に作っておくべきクレジットカード5選【2026年版】",
        "url": "https://nambei-oyaji.com/credit-cards-before-moving-abroad/?utm_source=hatena&utm_medium=blog&utm_campaign=digest",
        "tags": ["海外移住", "クレジットカード", "海外生活", "パラグアイ"],
        "body": """パラグアイに移住してから痛感したのが、「海外移住前にクレジットカードを作っておくべきだった」ということ。

海外在住者は日本のクレカを新規発行しにくい。住所が海外になった時点で審査に通りにくくなるケースが多い。**だから移住前に必要枚数を作っておくのが鉄則。**

実際にアスンシオンで生活してみて、海外移住者に特に役立つカードの条件は：

- **海外での決済手数料が低い**（現地払いが多い）
- **海外ATMでキャッシュが引き出せる**（現地通貨を引き出せると便利）
- **旅行保険が充実**（海外移住者にとっては保険の代わりになることも）
- **電子マネー・Apple Pay対応**

移住前に作っておくべきカードは5枚に絞って比較した。年会費・還元率・海外対応力それぞれの観点で選んでいる。

→ <a href="https://nambei-oyaji.com/credit-cards-before-moving-abroad/?utm_source=hatena&utm_medium=blog&utm_campaign=digest">海外移住前に作っておくべきクレジットカード5選【2026年版】おすすめ比較</a>
"""
    },
    {
        "wp_id": 3305,
        "hatena_title": "パラグアイに日本人が移住するメリット・デメリット｜在住者のリアルな本音",
        "url": "https://nambei-oyaji.com/paraguay-japanese-merit-demerit/?utm_source=hatena&utm_medium=blog&utm_campaign=digest",
        "tags": ["パラグアイ", "海外移住", "アスンシオン", "移住生活"],
        "body": """「パラグアイってどうなの？本当に住みやすいの？」

アスンシオンに実際に移住してみて、正直に言う。**良い面も悪い面も、ネットの情報と現実はけっこう違う。**

**実際に住んでみて感じたメリット**

- **物価の安さ**：日本の約1/3〜1/4で生活できる。外食も安く、1食200〜400円で普通に食べられる
- **税制の優遇**：海外所得への課税がなく、資産形成しやすい環境
- **永住権が取りやすい**：条件を満たせば比較的シンプルに永住権が取得できる
- **南米の中では治安が良い**：ブラジル・コロンビアと比べるとだいぶ安全

**正直なデメリット**

- **スペイン語必須**：英語はほとんど通じない。スペイン語ゼロだと最初はかなり苦労する
- **インフラの不安定さ**：停電・断水が予告なしに起きることがある
- **医療レベルの差**：日本語対応の病院がなく、重篤な場合はブラジルへ

移住検討中なら、メリット・デメリットを冷静に把握した上で判断してほしい。詳細は本家記事で。

→ <a href="https://nambei-oyaji.com/paraguay-japanese-merit-demerit/?utm_source=hatena&utm_medium=blog&utm_campaign=digest">パラグアイに日本人が移住するメリット・デメリット｜在住者のリアルな本音【2026年版】</a>
"""
    },
    {
        "wp_id": 3304,
        "hatena_title": "パラグアイ永住権の費用と申請手順｜在住者が解説【2026年版】",
        "url": "https://nambei-oyaji.com/paraguay-permanent-residence/?utm_source=hatena&utm_medium=blog&utm_campaign=digest",
        "tags": ["パラグアイ", "永住権", "海外移住", "ビザ"],
        "body": """パラグアイの永住権は「南米で一番取りやすい永住権のひとつ」と言われている。実際にアスンシオンで手続きを経験した立場から、リアルな費用と手順を解説する。

**パラグアイ永住権の基本条件**

主な取得方法は「退職者ビザ（レンティスタ）」と「投資家ビザ」の2つ。退職者ビザは月収が一定以上あることを証明できれば申請できる。

**実際にかかった費用（目安）**

- 書類翻訳・公証費用：3〜5万円程度
- 現地弁護士費用：5〜15万円（業者によって差が大きい）
- 申請手数料：数万円
- **合計：20〜30万円が目安**

ただし、弁護士の選択で費用も結果も大きく変わる。安すぎる業者には注意が必要。

**申請から取得までの期間**

書類が揃っていれば3〜6ヶ月程度が目安。ただし書類の不備があると大幅に延びる。

詳しい書類一覧・申請フロー・信頼できる弁護士の選び方は本家記事で詳しく解説している。

→ <a href="https://nambei-oyaji.com/paraguay-permanent-residence/?utm_source=hatena&utm_medium=blog&utm_campaign=digest">パラグアイ永住権の費用と申請手順【2026年最新版】在住者が解説</a>
"""
    },
]


def load_secrets():
    with open(SECRETS_PATH, encoding="utf-8") as f:
        return json.load(f)


def load_hatena_log():
    if HATENA_LOG_PATH.exists():
        with open(HATENA_LOG_PATH, encoding="utf-8") as f:
            return json.load(f)
    return {"converted": [], "published": []}


def save_hatena_log(log_data):
    with open(HATENA_LOG_PATH, "w", encoding="utf-8") as f:
        json.dump(log_data, f, ensure_ascii=False, indent=2)


def post_to_hatena(hatena_id: str, blog_id: str, api_key: str, title: str, body: str, tags: list, draft: bool = False) -> dict:
    """AtomPub APIではてなブログに投稿"""
    endpoint = f"https://blog.hatena.ne.jp/{hatena_id}/{blog_id}/atom/entry"

    # Basic認証
    credentials = b64encode(f"{hatena_id}:{api_key}".encode()).decode()

    # カテゴリXML
    categories_xml = "\n".join([f'<category term="{tag}" />' for tag in tags])

    # 下書きフラグ
    draft_xml = "<app:draft>yes</app:draft>" if draft else "<app:draft>no</app:draft>"

    # AtomPubエントリXML
    entry_xml = f"""<?xml version="1.0" encoding="utf-8"?>
<entry xmlns="http://www.w3.org/2005/Atom"
       xmlns:app="http://www.w3.org/2007/app">
  <title>{title}</title>
  <author><name>{hatena_id}</name></author>
  <content type="text/html"><![CDATA[{body}]]></content>
  {categories_xml}
  <app:control>
    {draft_xml}
  </app:control>
</entry>"""

    headers = {
        "Content-Type": "application/atom+xml; charset=utf-8",
        "Authorization": f"Basic {credentials}",
    }

    resp = requests.post(endpoint, data=entry_xml.encode("utf-8"), headers=headers, timeout=30)
    return resp


def main():
    secrets = load_secrets()
    hatena_config = secrets["hatena"]
    hatena_id = hatena_config["hatena_id"]
    blog_id = hatena_config["blog_id"]
    api_key = hatena_config["api_key"]

    log_data = load_hatena_log()
    published_ids = {str(p.get("article_id", "")) for p in log_data.get("published", [])}

    print(f"はてなブログ投稿開始: {hatena_id} / {blog_id}")
    print(f"既投稿: {len(published_ids)}件")
    print()

    success_count = 0
    for article in ARTICLES:
        wp_id = str(article["wp_id"])
        if wp_id in published_ids:
            print(f"スキップ（投稿済み）: ID={wp_id} {article['hatena_title'][:40]}")
            continue

        print(f"投稿中: {article['hatena_title'][:60]}")

        resp = post_to_hatena(
            hatena_id=hatena_id,
            blog_id=blog_id,
            api_key=api_key,
            title=article["hatena_title"],
            body=article["body"],
            tags=article["tags"],
            draft=False
        )

        if resp.status_code in (200, 201):
            print(f"  OK 投稿成功 (HTTP {resp.status_code})")

            # ログに記録
            log_entry = {
                "article_id": wp_id,
                "title": article["hatena_title"],
                "original_url": article["url"],
                "published_at": datetime.now().isoformat(),
                "hatena_response_status": resp.status_code,
            }

            # レスポンスからはてな記事URLを取得
            import xml.etree.ElementTree as ET
            try:
                root = ET.fromstring(resp.text)
                ns = {"atom": "http://www.w3.org/2005/Atom"}
                for link in root.findall("atom:link", ns):
                    if link.get("rel") == "alternate":
                        log_entry["hatena_url"] = link.get("href", "")
                        print(f"  URL: {log_entry['hatena_url']}")
                        break
            except Exception as e:
                print(f"  URLパースエラー: {e}")

            log_data["published"].append(log_entry)
            save_hatena_log(log_data)
            success_count += 1
        else:
            print(f"  × 投稿失敗 (HTTP {resp.status_code})")
            print(f"  Response: {resp.text[:300]}")

        time.sleep(2)  # API制限対策

    print()
    print(f"完了: {success_count}/{len(ARTICLES)}件投稿成功")


if __name__ == "__main__":
    main()
