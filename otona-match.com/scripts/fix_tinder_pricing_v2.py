"""
Fix Tinder pricing in article ID:531 - v2
Restore overview table, replace pricing table, update all price mentions.
"""

import requests
import json

# Load credentials
with open(r"C:\Users\tmizu\マイドライブ\GitHub\claude-code\otona-match.com\config\secrets.json", "r", encoding="utf-8") as f:
    secrets = json.load(f)

WP_USER = secrets["wordpress"]["username"]
WP_PASS = secrets["wordpress"]["app_password"]
BASE_URL = "https://otona-match.com/?rest_route=/wp/v2/posts/531"

# Use the ORIGINAL content (before v1 broke it)
with open(r"C:\Users\tmizu\マイドライブ\GitHub\claude-code\otona-match.com\outputs\tinder-531-original.html", "r", encoding="utf-8") as f:
    content = f.read()

print(f"Original content loaded: {len(content)} chars")

# === Fix 1: Update "2024年時点" to "2026年3月時点" ===
content = content.replace(
    '2024年時点の日本における主な料金は以下の通りです。',
    '2026年3月時点の日本における主な目安料金は以下の通りです。'
)

# === Fix 2: Replace the old pricing table with updated one ===
OLD_PRICING_TABLE = """<table>
<thead>
<tr>
<th>プラン名</th>
<th>月額（1ヶ月）</th>
<th>月額（6ヶ月）</th>
<th>月額（12ヶ月）</th>
<th>主な機能</th>
</tr>
</thead>
<tbody>
<tr>
<td>Tinder Plus</td>
<td>約2,433円</td>
<td>約1,217円</td>
<td>約975円</td>
<td>無制限スワイプ・パスポート・巻き戻し</td>
</tr>
<tr>
<td>Tinder Gold</td>
<td>約4,350円</td>
<td>約2,600円</td>
<td>約2,167円</td>
<td>Plus全機能＋いいねした人を見る</td>
</tr>
<tr>
<td>Tinder Platinum</td>
<td>約6,500円</td>
<td>約3,483円</td>
<td>約2,983円</td>
<td>Gold全機能＋マッチ前メッセージ送信</td>
</tr>
</tbody>
</table>"""

NEW_PRICING_TABLE = """<div class="information-box" style="background:#fff8e1; border-left:4px solid #ffc107; padding:15px; margin:20px 0; border-radius:4px;">
<p style="margin:0; font-weight:bold;">⚠ Tinderの料金は個人ごとに異なります</p>
<p style="margin:8px 0 0;">Tinderは「パーソナライズド・プライシング」を導入しており、年齢・地域・端末（iOS/Android/Web）・利用状況によって表示される料金が異なります。下記の料金はあくまで目安です。正確な料金はTinderアプリ内でご確認ください。</p>
</div>
<table>
<thead>
<tr>
<th>プラン名</th>
<th>月額（1ヶ月）</th>
<th>月額（6ヶ月）</th>
<th>月額（12ヶ月）</th>
<th>主な機能</th>
</tr>
</thead>
<tbody>
<tr>
<td>Tinder Plus</td>
<td>約1,200円〜</td>
<td>約767円〜</td>
<td>約500円〜</td>
<td>無制限スワイプ・パスポート・巻き戻し</td>
</tr>
<tr>
<td>Tinder Gold</td>
<td>約3,400円〜</td>
<td>約2,100円〜</td>
<td>約1,400円〜</td>
<td>Plus全機能＋いいねした人を見る</td>
</tr>
<tr>
<td>Tinder Platinum</td>
<td>約4,300円〜</td>
<td>約2,633円〜</td>
<td>約1,817円〜</td>
<td>Gold全機能＋マッチ前メッセージ送信</td>
</tr>
</tbody>
</table>"""

if OLD_PRICING_TABLE in content:
    content = content.replace(OLD_PRICING_TABLE, NEW_PRICING_TABLE)
    print("OK: Replaced pricing table")
else:
    print("WARNING: Old pricing table not found exactly. Trying partial match...")
    # Try line-by-line trimmed matching
    old_stripped = OLD_PRICING_TABLE.strip()
    if old_stripped in content:
        content = content.replace(old_stripped, NEW_PRICING_TABLE)
        print("OK: Replaced pricing table (stripped)")
    else:
        print("ERROR: Cannot find pricing table!")

# === Fix 3: Update the note after the table ===
content = content.replace(
    '<p><span class="marker-pink">注意点：Tinderの料金はユーザーの年齢・地域・端末（iOS/Android）によって異なる場合があります。アプリ内で必ず最新の料金を確認してください。</span></p>',
    '<p><span class="marker-pink">※Tinderの料金は年齢・地域・端末により個人ごとに異なります。上記は2026年3月時点のiOS版を基準とした目安料金です。正確な料金はTinderアプリ内でご確認ください。</span></p>'
)
print("OK: Updated pricing note")

# === Fix 4: Update comparison table "無料〜6,500円" ===
content = content.replace('無料〜6,500円', '無料〜約4,300円')
print("OK: Updated comparison table price range")

# === Fix 5: Update "料金比較2024" link text ===
content = content.replace('料金比較2024', '料金比較2026')
print("OK: Updated link text year")

# === Fix 6: Add end-of-article disclaimer ===
DISCLAIMER = (
    '<p style="font-size:0.9em; color:#666; margin-top:30px;">'
    '※本記事のTinder料金情報は2026年3月時点の目安です。Tinderはパーソナライズド・プライシングを'
    '導入しているため、実際の料金はユーザーごとに異なります。最新の正確な料金はTinderアプリ内で'
    'ご確認ください。</p>'
)

# Find the last closing tag area and insert before it
if '※本記事のTinder料金情報は' not in content:
    content = content.rstrip() + '\n' + DISCLAIMER
    print("OK: Added end-of-article disclaimer")

# === Fix 7: Also update other stray price mentions if any ===
# The comparison table row for other apps that mention Tinder prices
content = content.replace('約6,500円', '約4,300円')
content = content.replace('約3,483円', '約2,633円')
content = content.replace('約2,983円', '約1,817円')
content = content.replace('約2,433円', '約1,200円')
content = content.replace('約1,217円', '約767円')
content = content.replace('約4,350円', '約3,400円')
content = content.replace('約2,600円', '約2,100円')
content = content.replace('約2,167円', '約1,400円')
content = content.replace('約975円', '約500円')
print("OK: Cleaned up any remaining old prices")

print(f"\nFinal content: {len(content)} chars")

# === Upload ===
print("\n=== Updating article via REST API ===")
resp = requests.post(
    BASE_URL,
    auth=(WP_USER, WP_PASS),
    json={"content": content},
    headers={"Content-Type": "application/json"}
)

if resp.status_code == 200:
    updated = resp.json()
    print(f"SUCCESS! Modified: {updated['modified']}")
    print(f"Link: {updated['link']}")
else:
    print(f"FAILED: {resp.status_code}")
    print(resp.text[:500])

# Save for reference
with open(r"C:\Users\tmizu\マイドライブ\GitHub\claude-code\otona-match.com\outputs\tinder-531-updated-v2.html", "w", encoding="utf-8") as f:
    f.write(content)
print("Saved to tinder-531-updated-v2.html")
