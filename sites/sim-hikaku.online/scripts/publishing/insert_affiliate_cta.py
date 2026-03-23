"""
SIM比較オンライン — アフィリエイトCTA一括挿入スクリプト
提携済みアフィリエイトリンクを対象記事に挿入する。

使い方:
  python insert_affiliate_cta.py           # dry-run（確認のみ）
  python insert_affiliate_cta.py --apply   # 実際に挿入
"""

import sys
import os
import json
import re
from pathlib import Path

if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")

BASE_DIR = Path(__file__).resolve().parent.parent.parent
OUTPUTS_DIR = BASE_DIR / "outputs"
CONFIG_DIR = BASE_DIR / "config"
AFFILIATE_FILE = CONFIG_DIR / "affiliate-links.json"

# CTA挿入対象マッピング: filename -> 挿入するアフィリエイトキー
# 海外SIM記事にはTRAVeSIM・Voye Globalを挿入
ARTICLE_AFFILIATE_MAP = {
    # 海外SIM柱（6記事）→ TRAVeSIM + Voye Global
    "kaigai-sim-esim-hikaku-pillar": ["travesim", "voye-global"],
    "kaigai-ryokou-esim-osusume": ["travesim", "voye-global"],
    "nanbei-sim-esim-guide": ["travesim", "voye-global"],
    "kaigai-nihon-bango-iji": ["travesim", "voye-global"],
    "ryugakusei-sim-senryaku": ["travesim", "voye-global"],
    "airalo-trifa-ubigi-hikaku": ["travesim", "voye-global"],
    # eSIM対応記事にもeSIMサービスCTA
    "kakuyasu-sim-esim-taiou": ["travesim", "voye-global"],
}

# CTA HTMLテンプレート
CTA_TEMPLATE = """
---

## 海外eSIMをお探しの方へ

<div style="background: linear-gradient(135deg, #f0f7ff 0%, #e8f4fd 100%); border: 2px solid #0066CC; border-radius: 12px; padding: 24px; margin: 24px 0;">

{cta_items}

</div>
"""

CTA_ITEM_TEMPLATE = """<div style="background: white; border-radius: 8px; padding: 20px; margin-bottom: 16px; box-shadow: 0 2px 8px rgba(0,0,0,0.06);">
<p style="margin: 0 0 8px 0; font-weight: 700; font-size: 1.1em; color: #333;">{icon} {name}</p>
<p style="margin: 0 0 12px 0; color: #666; font-size: 0.95em;">{description}</p>
<p style="margin: 0; text-align: center;">
<a href="{url}" rel="nofollow" style="display: inline-block; background: #0066CC; color: white; padding: 12px 32px; border-radius: 8px; text-decoration: none; font-weight: 600; font-size: 1em;">{cta_text}</a>
</p>
{tracking_img}
</div>"""

CTA_ITEM_LAST_TEMPLATE = """<div style="background: white; border-radius: 8px; padding: 20px; box-shadow: 0 2px 8px rgba(0,0,0,0.06);">
<p style="margin: 0 0 8px 0; font-weight: 700; font-size: 1.1em; color: #333;">{icon} {name}</p>
<p style="margin: 0 0 12px 0; color: #666; font-size: 0.95em;">{description}</p>
<p style="margin: 0; text-align: center;">
<a href="{url}" rel="nofollow" style="display: inline-block; background: #0066CC; color: white; padding: 12px 32px; border-radius: 8px; text-decoration: none; font-weight: 600; font-size: 1em;">{cta_text}</a>
</p>
{tracking_img}
</div>"""

# サービス別の説明文
SERVICE_INFO = {
    "travesim": {
        "icon": "🌏",
        "name": "TRAVeSIM（トラベシム）",
        "description": "140カ国以上対応の海外eSIM。アジア・ヨーロッパ・北米など主要エリアをカバー。日本語対応で初めてのeSIMでも安心。",
        "cta_text": "TRAVeSIMの料金プランを見る",
    },
    "voye-global": {
        "icon": "✈️",
        "name": "Voye Global（ボイエグローバル）",
        "description": "各国最低2回線を確保した高品質eSIM。現地の通信障害時も別回線に切り替え可能で、安定した通信を実現。",
        "cta_text": "Voye Globalのプランを見る",
    },
}

# CTA挿入マーカー
CTA_MARKER = "## 海外eSIMをお探しの方へ"


def load_affiliates():
    with open(AFFILIATE_FILE, encoding="utf-8") as f:
        return json.load(f)


def build_cta_block(affiliate_keys, affiliates):
    """提携済みリンクのみでCTAブロックを構築"""
    esim = affiliates.get("esim_services", {})
    items = []
    active_keys = []

    for key in affiliate_keys:
        svc = esim.get(key)
        if not svc or svc.get("status") != "提携済":
            continue
        active_keys.append(key)

    if not active_keys:
        return None

    for i, key in enumerate(active_keys):
        svc = esim[key]
        info = SERVICE_INFO.get(key, {})
        tracking = ""
        if svc.get("tracking_img"):
            tracking = f'<img src="{svc["tracking_img"]}" width="1" height="1" style="border:0;" alt="">'

        template = CTA_ITEM_LAST_TEMPLATE if i == len(active_keys) - 1 else CTA_ITEM_TEMPLATE
        item = template.format(
            icon=info.get("icon", "📱"),
            name=info.get("name", svc["name"]),
            description=info.get("description", ""),
            url=svc["url"],
            cta_text=info.get("cta_text", f"{svc['name']}を見る"),
            tracking_img=tracking,
        )
        items.append(item)

    return CTA_TEMPLATE.format(cta_items="\n\n".join(items))


def insert_cta_into_article(filepath, cta_block, dry_run=True):
    """記事にCTAブロックを挿入。FAQ直前に挿入。"""
    with open(filepath, encoding="utf-8") as f:
        content = f.read()

    # 既にCTAが挿入済みならスキップ
    if CTA_MARKER in content:
        return "skip_exists"

    # FAQ直前に挿入
    faq_pattern = r"\n## よくある質問"
    match = re.search(faq_pattern, content)
    if not match:
        # FAQがなければ「まとめ」直前
        match = re.search(r"\n## まとめ", content)

    if not match:
        return "skip_no_target"

    insert_pos = match.start()
    new_content = content[:insert_pos] + "\n" + cta_block + "\n" + content[insert_pos:]

    if not dry_run:
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(new_content)

    return "inserted"


def main():
    dry_run = "--apply" not in sys.argv
    affiliates = load_affiliates()

    if dry_run:
        print("=== DRY RUN（--apply で実行） ===\n")

    results = {"inserted": 0, "skip_exists": 0, "skip_no_target": 0, "skip_no_cta": 0}

    for filename, keys in ARTICLE_AFFILIATE_MAP.items():
        filepath = OUTPUTS_DIR / f"{filename}.md"
        if not filepath.exists():
            print(f"  [NG] {filename} — ファイルなし")
            continue

        cta_block = build_cta_block(keys, affiliates)
        if not cta_block:
            print(f"  [--] {filename} — 提携済みリンクなし")
            results["skip_no_cta"] += 1
            continue

        result = insert_cta_into_article(filepath, cta_block, dry_run)
        if result == "inserted":
            print(f"  [OK] {filename} — CTA挿入{'予定' if dry_run else '完了'}")
            results["inserted"] += 1
        elif result == "skip_exists":
            print(f"  [OK] {filename} — CTA挿入済み（スキップ）")
            results["skip_exists"] += 1
        else:
            print(f"  [NG] {filename} — 挿入位置が見つからない")
            results["skip_no_target"] += 1

    print(f"\n--- 結果 ---")
    print(f"  挿入: {results['inserted']}件")
    print(f"  既存: {results['skip_exists']}件")
    print(f"  対象外: {results['skip_no_target'] + results['skip_no_cta']}件")

    if dry_run:
        print("\n実行するには: python insert_affiliate_cta.py --apply")


if __name__ == "__main__":
    main()
