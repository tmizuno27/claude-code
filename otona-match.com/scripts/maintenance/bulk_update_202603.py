"""otona-match.com 一括記事修正スクリプト (2026-03)"""
import requests
import json
import time

# 認証
with open(r"C:\Users\tmizu\マイドライブ\GitHub\claude-code\otona-match.com\config\secrets.json") as f:
    sec = json.load(f)
AUTH = (sec["wordpress"]["username"], sec["wordpress"]["app_password"])
BASE = "https://otona-match.com/?rest_route=/wp/v2/posts"

def get_post(pid):
    r = requests.get(f"{BASE}/{pid}", params={"context": "edit"}, auth=AUTH)
    r.raise_for_status()
    return r.json()

def update_post(pid, content):
    r = requests.post(f"{BASE}/{pid}", json={"content": content}, auth=AUTH)
    r.raise_for_status()
    return r.json()

ZEXY_NOTE = '<p style="color: #e74c3c; font-weight: bold;">※ゼクシィ縁結びは2026年3月31日をもってサービス終了しました。</p>'

results = []

# ========== 1. with料金値上げ (3,600→4,160) ==========
with_ids = [9, 11, 13, 14, 133, 155, 156, 163, 191]
for pid in with_ids:
    post = get_post(pid)
    content = post["content"]["raw"]
    new_content = content.replace("3,600円", "4,160円")

    # ID:11 詳細プラン料金
    if pid == 11:
        new_content = new_content.replace("3,000円/月", "3,467円/月")
        new_content = new_content.replace("2,217円/月", "2,560円/月")
        new_content = new_content.replace("1,833円/月", "2,117円/月")

    if new_content != content:
        update_post(pid, new_content)
        results.append(f"[with料金] ID:{pid} 更新完了")
    else:
        results.append(f"[with料金] ID:{pid} 変更なし(既に修正済み?)")
    time.sleep(0.5)

# ========== 2. ゼクシィ縁結びサービス終了注記 ==========
zexy_ids = [13, 17, 133, 150, 152, 155]
for pid in zexy_ids:
    post = get_post(pid)
    content = post["content"]["raw"]

    if "ゼクシィ縁結びは2026年3月31日" in content:
        results.append(f"[ゼクシィ] ID:{pid} 既に注記あり、スキップ")
        time.sleep(0.5)
        continue

    # ゼクシィ縁結びへの言及箇所を探して直後に注記挿入
    # 最初の言及の段落/要素の後に1回だけ挿入
    import re
    # ゼクシィ縁結びを含む最初の</p>や</li>や</td>の後に挿入
    pattern = r'(ゼクシィ縁結び[^<]*(?:</(?:strong|b|a|span)>)*[^<]*</(?:p|li|td|div)>)'
    match = re.search(pattern, content)
    if match:
        insert_pos = match.end()
        new_content = content[:insert_pos] + "\n" + ZEXY_NOTE + content[insert_pos:]
        update_post(pid, new_content)
        results.append(f"[ゼクシィ] ID:{pid} 注記挿入完了")
    else:
        # フォールバック: 単純に「ゼクシィ縁結び」の最初の出現を含むブロックの後
        idx = content.find("ゼクシィ縁結び")
        if idx >= 0:
            # その後の最初の閉じタグを探す
            close_tags = ["</p>", "</li>", "</td>", "</div>", "</tr>"]
            earliest = len(content)
            for tag in close_tags:
                pos = content.find(tag, idx)
                if pos >= 0 and pos < earliest:
                    earliest = pos + len(tag)
            if earliest < len(content):
                new_content = content[:earliest] + "\n" + ZEXY_NOTE + content[earliest:]
                update_post(pid, new_content)
                results.append(f"[ゼクシィ] ID:{pid} 注記挿入完了(フォールバック)")
            else:
                results.append(f"[ゼクシィ] ID:{pid} 挿入位置が見つからず")
        else:
            results.append(f"[ゼクシィ] ID:{pid} ゼクシィ縁結びの言及なし")
    time.sleep(0.5)

# ========== 3. 会員数更新 ==========
# ID:9 - Omiai, タップル, with, marrish
post = get_post(9)
content = post["content"]["raw"]
# Omiai 900万人→1,000万人以上
content = content.replace("Omiai</strong>（900万人）", "Omiai</strong>（1,000万人以上）")
content = content.replace("Omiai（900万人）", "Omiai（1,000万人以上）")
content = content.replace("900万人", "1,000万人以上")  # Omiaiのみの場合に備える（他に900万人がなければ）
# タップル 1,700万人→2,000万人以上
content = content.replace("1,700万人", "2,000万人以上")
# with 800万人→1,000万人以上 (注意: Omiaiと被らないよう)
content = content.replace("800万人", "1,000万人以上")
# marrish 200万人/250万人→400万人以上
content = content.replace("250万人", "400万人以上")
content = content.replace("200万人", "400万人以上")
if content != get_post(9)["content"]["raw"]:
    # 再取得せず保存
    pass
update_post(9, content)
results.append(f"[会員数] ID:9 更新完了")
time.sleep(0.5)

# ID:14 - Omiai, marrish
post = get_post(14)
content = post["content"]["raw"]
content = content.replace("900万人", "1,000万人以上")
content = content.replace("250万人", "400万人以上")
content = content.replace("200万人", "400万人以上")
update_post(14, content)
results.append(f"[会員数] ID:14 更新完了")
time.sleep(0.5)

# ID:151 - marrish
post = get_post(151)
content = post["content"]["raw"]
content = content.replace("250万人", "400万人以上")
content = content.replace("200万人", "400万人以上")
update_post(151, content)
results.append(f"[会員数] ID:151 更新完了")
time.sleep(0.5)

# ID:191 - marrish
post = get_post(191)
content = post["content"]["raw"]
content = content.replace("250万人", "400万人以上")
content = content.replace("200万人", "400万人以上")
update_post(191, content)
results.append(f"[会員数] ID:191 更新完了")
time.sleep(0.5)

# ========== 4. その他 ==========
# ID:143 ユーブライド月額
post = get_post(143)
content = post["content"]["raw"]
content = content.replace("2,400円～", "4,300円（12ヶ月プラン: 2,400円/月）")
update_post(143, content)
results.append(f"[ユーブライド] ID:143 更新完了")
time.sleep(0.5)

# ID:16 PCMAX 600円分→700円分
post = get_post(16)
content = post["content"]["raw"]
content = content.replace("600円分", "700円分")
update_post(16, content)
results.append(f"[PCMAX] ID:16 更新完了")
time.sleep(0.5)

# ID:142 PCMAX 600円分→700円分
post = get_post(142)
content = post["content"]["raw"]
content = content.replace("600円分", "700円分")
update_post(142, content)
results.append(f"[PCMAX] ID:142 更新完了")
time.sleep(0.5)

# ========== 結果出力 ==========
print("\n===== 修正結果 =====")
for r in results:
    print(r)
print(f"\n合計: {len(results)}件処理")
