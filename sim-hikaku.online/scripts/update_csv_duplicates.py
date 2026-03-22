"""重複統合後のCSV更新スクリプト"""
import csv
from pathlib import Path

CSV_PATH = Path(__file__).resolve().parent.parent / "outputs" / "article-management.csv"

# 下書き化したWP IDとリダイレクト先のマッピング
DRAFTED_IDS = {
    445: "→ WP:26 (UQモバイル評判メイン)",
    466: "→ WP:26 (UQモバイル評判メイン)",
    468: "→ WP:26 (UQモバイル評判メイン)",
    687: "→ WP:106 (楽天モバイル評判メイン)",
    442: "→ WP:106 (楽天モバイル評判メイン)",
    394: "→ WP:106 (楽天モバイル評判メイン)",
    392: "→ WP:106 (楽天モバイル評判メイン)",
    391: "→ WP:106 (楽天モバイル評判メイン)",
    665: "→ WP:108 (LINEMO評判メイン)",
    787: "→ WP:108 (LINEMO評判メイン)",
    265: "ahamo評判メイン(キープ)",  # This is keep - skip
    632: "→ WP:265 (ahamo評判メイン)",
    784: "→ WP:265 (ahamo評判メイン)",
    641: "→ WP:267 (IIJmio評判メイン)",
    668: "→ WP:110 (mineo評判メイン)",
    788: "→ WP:110 (mineo評判メイン)",
    712: "→ WP:269 (ワイモバイル評判メイン)",
    789: "→ WP:684 (povo評判メイン)",
    653: "→ WP:27 (格安SIM料金比較メイン)",
    629: "→ WP:253 (1GB最安メイン)",
    628: "→ WP:255 (10GB最安メイン)",
    652: "→ WP:120 (乗り換えガイドメイン)",
    790: "→ WP:120 (乗り換えガイドメイン)",
}

# 265はキープ対象なので除外
DRAFTED_IDS.pop(265)

rows = []
with open(CSV_PATH, encoding="utf-8") as f:
    reader = csv.reader(f)
    header = next(reader)
    rows.append(header)

    for row in reader:
        if not row or not row[0].strip():
            rows.append(row)
            continue

        # WordPress IDカラム（13番目、0-indexed）
        try:
            wp_id = int(row[13].strip()) if len(row) > 13 and row[13].strip() else None
        except (ValueError, IndexError):
            wp_id = None

        if wp_id and wp_id in DRAFTED_IDS:
            # ステータスを変更
            if len(row) > 2:
                row[2] = "下書き(重複統合)"
            # 備考に追記
            if len(row) > 15:
                redirect_note = f"重複統合 {DRAFTED_IDS[wp_id]}"
                if row[15]:
                    row[15] = f"{row[15]} | {redirect_note}"
                else:
                    row[15] = redirect_note
            print(f"  Updated: WP:{wp_id} -> 下書き(重複統合) {DRAFTED_IDS[wp_id]}")

        rows.append(row)

with open(CSV_PATH, "w", encoding="utf-8", newline="") as f:
    writer = csv.writer(f)
    writer.writerows(rows)

print(f"\nCSV updated: {CSV_PATH}")
print(f"Total rows: {len(rows)}")
