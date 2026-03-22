"""
sim-hikaku.online 重複記事統合スクリプト
- 重複記事を下書きに変更（WP REST API）
- 301リダイレクトルール生成（Cocoonテーマのリダイレクト機能 or .htaccess）
- 統合レポート出力

使い方:
  python consolidate_duplicates.py --dry-run    # 確認のみ
  python consolidate_duplicates.py              # 実行
"""

import json
import sys
import requests
from pathlib import Path
from datetime import datetime

# === 設定 ===
SCRIPT_DIR = Path(__file__).resolve().parent
CONFIG_DIR = SCRIPT_DIR.parent / "config"
LOGS_DIR = SCRIPT_DIR.parent.parent / "logs"

with open(CONFIG_DIR / "secrets.json", encoding="utf-8") as f:
    secrets = json.load(f)

WP_API = secrets["wordpress"]["api_url"]
WP_USER = secrets["wordpress"]["username"]
WP_PASS = secrets["wordpress"]["app_password"]
AUTH = (WP_USER, WP_PASS)

# === 重複マッピング ===
# (keep_wp_id, keep_slug, redirect_from_wp_id, redirect_from_slug, reason)
CONSOLIDATION_MAP = [
    # --- UQモバイル評判 (4本→1本) --- キープ: #4 (WP:26, 8200字)
    (26, "uq-mobile-hyoban-kuchikomi", 445, "uq-f320e879", "UQモバイル評判重複(悪い?)"),
    (26, "uq-mobile-hyoban-kuchikomi", 466, "uq-40dd0143", "UQモバイル評判重複(地方)"),
    (26, "uq-mobile-hyoban-kuchikomi", 468, "uq-mobile-reputation-bad", "UQモバイル評判重複(悪い7つ)"),

    # --- 楽天モバイル (6本→1本) --- キープ: #10 (WP:106, 8500字)
    (106, "rakuten-mobile-hyoban", 687, "rakuten-mobile-review", "楽天モバイル評判重複(レビュー)"),
    (106, "rakuten-mobile-hyoban", 442, "article-0d7dc43b", "楽天モバイル重複(田舎1)"),
    (106, "rakuten-mobile-hyoban", 394, "article-c60c5a37", "楽天モバイル重複(大阪)"),
    (106, "rakuten-mobile-hyoban", 392, "article-0a0c1d12", "楽天モバイル重複(最新)"),
    (106, "rakuten-mobile-hyoban", 391, "article-04622", "楽天モバイル重複(田舎2)"),

    # --- LINEMO (3本→1本) --- キープ: #11 (WP:108, 8500字)
    (108, "linemo-hyoban", 665, "linemo-review", "LINEMO評判重複(レビュー)"),
    (108, "linemo-hyoban", 787, "linemo", "LINEMO評判重複(悪い)"),

    # --- ahamo (3本→1本) --- キープ: #21 (WP:265, 8200字)
    (265, "ahamo-hyoban", 632, "ahamo-review", "ahamo評判重複(レビュー)"),
    (265, "ahamo-hyoban", 784, "ahamo", "ahamo評判重複(知恵袋)"),

    # --- IIJmio (2本→1本) --- キープ: #23 (WP:267, 8100字)
    (267, "iijmio-hyoban", 641, "iijmio-review", "IIJmio評判重複"),

    # --- mineo (3本→1本) --- キープ: #12 (WP:110, 8300字)
    (110, "mineo-hyoban", 668, "mineo-review", "mineo評判重複(レビュー)"),
    (110, "mineo-hyoban", 788, "mineo", "mineo評判重複(地方)"),

    # --- ワイモバイル (2本→1本) --- キープ: #22 (WP:269, 8300字) ※#31(評判悪い)は別KWなので残す
    (269, "ymobile-hyoban", 712, "ymobile-review", "ワイモバイル評判重複(レビュー)"),

    # --- povo (2本→1本) --- キープ: #34 (WP:684, 4850字)
    (684, "povo-review", 789, "povo", "povo評判重複(悪い)"),

    # --- 格安SIM料金比較 (2本→1本) --- キープ: #5 (WP:27, 9200字)
    (27, "kakuyasu-sim-ryokin-hikaku-ichiran", 653, "kakuyasu-sim-ryoukin-hikaku", "格安SIM料金比較重複"),

    # --- 1GB最安 (2本→1本) --- キープ: #19 (WP:253, 7600字)
    (253, "kakuyasu-sim-1gb-hikaku", 629, "1gb-ika-kakuyasu-sim-ranking", "1GB最安重複"),

    # --- 10GB最安 (2本→1本) --- キープ: #18 (WP:255, 7800字)
    (255, "kakuyasu-sim-10gb-hikaku", 628, "10gb-kakuyasu-sim-ranking", "10GB最安重複"),

    # --- 乗り換えガイド (3本→1本) --- キープ: #6 (WP:120, 8200字)
    (120, "kakuyasu-sim-norikae-tejun-pillar", 652, "kakuyasu-sim-norikae-guide", "乗り換えガイド重複"),
    (120, "kakuyasu-sim-norikae-tejun-pillar", 790, "sim-mnp", "乗り換えMNP重複"),
]


def get_post_info(wp_id):
    """WordPress記事の現在の情報を取得"""
    try:
        r = requests.get(f"{WP_API}/posts/{wp_id}", auth=AUTH, timeout=30)
        if r.status_code == 200:
            data = r.json()
            return {
                "id": data["id"],
                "title": data["title"]["rendered"],
                "slug": data["slug"],
                "status": data["status"],
                "link": data["link"],
            }
    except Exception as e:
        print(f"  [ERROR] WP ID {wp_id}: {e}")
    return None


def set_draft(wp_id):
    """記事を下書きに変更"""
    r = requests.post(
        f"{WP_API}/posts/{wp_id}",
        auth=AUTH,
        json={"status": "draft"},
        timeout=30,
    )
    return r.status_code == 200


def generate_htaccess_rules(consolidation_map, site_url="https://sim-hikaku.online"):
    """301リダイレクトの.htaccessルールを生成"""
    rules = [
        "# === sim-hikaku.online 重複記事301リダイレクト ===",
        f"# 生成日: {datetime.now().strftime('%Y-%m-%d %H:%M')}",
        "# 重複記事を正規URLにリダイレクト",
        "",
    ]
    for keep_id, keep_slug, from_id, from_slug, reason in consolidation_map:
        rules.append(f"# {reason}")
        rules.append(f"Redirect 301 /{from_slug}/ {site_url}/{keep_slug}/")
        # ハッシュ形式のスラッグもカバー
        if from_slug.startswith("article-"):
            rules.append(f"Redirect 301 /{from_slug} {site_url}/{keep_slug}/")
        rules.append("")
    return "\n".join(rules)


def generate_cocoon_redirects(consolidation_map):
    """Cocoonテーマ用のリダイレクト設定テキスト（管理画面に貼り付け用）"""
    lines = []
    for keep_id, keep_slug, from_id, from_slug, reason in consolidation_map:
        lines.append(f"/{from_slug}/\t/{keep_slug}/\t301\t# {reason}")
    return "\n".join(lines)


def main():
    dry_run = "--dry-run" in sys.argv
    mode = "DRY RUN" if dry_run else "LIVE"

    print(f"=" * 60)
    print(f"sim-hikaku.online 重複記事統合 [{mode}]")
    print(f"対象: {len(CONSOLIDATION_MAP)} 記事を下書き化 + 301リダイレクト")
    print(f"=" * 60)

    results = {"success": [], "failed": [], "skipped": []}

    for keep_id, keep_slug, from_id, from_slug, reason in CONSOLIDATION_MAP:
        print(f"\n--- {reason} ---")

        # リダイレクト元の記事情報を取得
        from_info = get_post_info(from_id)
        if from_info is None:
            print(f"  [SKIP] WP ID {from_id} が見つかりません")
            results["skipped"].append((from_id, from_slug, "記事が見つからない"))
            continue

        if from_info["status"] == "draft":
            print(f"  [SKIP] WP ID {from_id} は既に下書きです")
            results["skipped"].append((from_id, from_slug, "既に下書き"))
            continue

        print(f"  リダイレクト元: [{from_info['status']}] {from_info['title']}")
        print(f"    URL: {from_info['link']}")
        print(f"  リダイレクト先: /{keep_slug}/")

        if dry_run:
            print(f"  [DRY RUN] 下書きに変更予定")
            results["success"].append((from_id, from_slug, reason))
        else:
            if set_draft(from_id):
                print(f"  [OK] 下書きに変更しました")
                results["success"].append((from_id, from_slug, reason))
            else:
                print(f"  [FAIL] 下書き変更に失敗")
                results["failed"].append((from_id, from_slug, reason))

    # .htaccess ルール生成
    htaccess_rules = generate_htaccess_rules(CONSOLIDATION_MAP)
    htaccess_path = SCRIPT_DIR.parent / "config" / "redirect-rules.htaccess"
    htaccess_path.write_text(htaccess_rules, encoding="utf-8")
    print(f"\n[SAVED] .htaccess ルール: {htaccess_path}")

    # Cocoon用リダイレクト設定
    cocoon_rules = generate_cocoon_redirects(CONSOLIDATION_MAP)
    cocoon_path = SCRIPT_DIR.parent / "config" / "cocoon-redirects.txt"
    cocoon_path.write_text(cocoon_rules, encoding="utf-8")
    print(f"[SAVED] Cocoon用リダイレクト: {cocoon_path}")

    # レポート出力
    report = {
        "executed_at": datetime.now().isoformat(),
        "mode": mode,
        "total_targets": len(CONSOLIDATION_MAP),
        "success": len(results["success"]),
        "failed": len(results["failed"]),
        "skipped": len(results["skipped"]),
        "details": {
            "success": [{"wp_id": r[0], "slug": r[1], "reason": r[2]} for r in results["success"]],
            "failed": [{"wp_id": r[0], "slug": r[1], "reason": r[2]} for r in results["failed"]],
            "skipped": [{"wp_id": r[0], "slug": r[1], "reason": r[2]} for r in results["skipped"]],
        },
    }
    report_path = LOGS_DIR / f"duplicate-consolidation-{datetime.now().strftime('%Y%m%d-%H%M')}.json"
    report_path.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"[SAVED] レポート: {report_path}")

    # サマリー
    print(f"\n{'=' * 60}")
    print(f"結果サマリー [{mode}]")
    print(f"  成功: {len(results['success'])} 記事")
    print(f"  失敗: {len(results['failed'])} 記事")
    print(f"  スキップ: {len(results['skipped'])} 記事")
    print(f"{'=' * 60}")

    if not dry_run and results["success"]:
        print(f"\n⚠ 次のステップ:")
        print(f"  1. WordPress管理画面 → Cocoon設定 → リダイレクト")
        print(f"     {cocoon_path} の内容を貼り付け")
        print(f"  2. または .htaccess に {htaccess_path} の内容を追記")
        print(f"  3. article-management.csv を更新")

    return 0 if not results["failed"] else 1


if __name__ == "__main__":
    sys.exit(main())
