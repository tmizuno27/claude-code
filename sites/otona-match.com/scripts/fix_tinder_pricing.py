"""
Fix Tinder pricing in article ID:531 on otona-match.com
- Update to personalized pricing model
- Add notice about price variation
- Update approximate price ranges
"""

import requests
import re
import json

# Load credentials
with open(r"C:\Users\tmizu\マイドライブ\GitHub\claude-code\sites\otona-match.com\config\secrets.json", "r", encoding="utf-8") as f:
    secrets = json.load(f)

WP_USER = secrets["wordpress"]["username"]
WP_PASS = secrets["wordpress"]["app_password"]
BASE_URL = "https://otona-match.com/?rest_route=/wp/v2/posts/531"

# Step 1: Fetch article
print("=== Fetching article ID:531 ===")
resp = requests.get(BASE_URL, auth=(WP_USER, WP_PASS))
resp.raise_for_status()
post = resp.json()
print(f"Title: {post['title']['rendered']}")
content = post["content"]["rendered"]

# Save original for reference
with open(r"C:\Users\tmizu\マイドライブ\GitHub\claude-code\sites\otona-match.com\outputs\tinder-531-original.html", "w", encoding="utf-8") as f:
    f.write(content)
print(f"Original content saved. Length: {len(content)} chars")

# Step 2: Show all pricing mentions for debugging
print("\n=== Pricing mentions found ===")
price_patterns = [
    r'\d{1,2},?\d{3}円',
    r'月額[^<\n]{0,30}円',
    r'料金[^<\n]{0,50}',
]
for pat in price_patterns:
    matches = re.findall(pat, content)
    for m in matches:
        print(f"  Found: {m}")

# Step 3: Apply updates
new_content = content

# Personalized pricing notice to insert after first pricing table or pricing section
PRICING_NOTICE = (
    '<div class="information-box" style="background:#fff8e1; border-left:4px solid #ffc107; '
    'padding:15px; margin:20px 0; border-radius:4px;">'
    '<p style="margin:0; font-weight:bold;">⚠ Tinderの料金は個人ごとに異なります</p>'
    '<p style="margin:8px 0 0;">Tinderは「パーソナライズド・プライシング」を導入しており、'
    '年齢・地域・端末（iOS/Android/Web）・利用状況によって表示される料金が異なります。'
    '下記の料金はあくまで目安です。正確な料金はTinderアプリ内でご確認ください。</p>'
    '</div>'
)

# Updated pricing table HTML (approximate ranges for 2026)
UPDATED_PRICING_TABLE = (
    '<figure class="wp-block-table"><table>'
    '<thead><tr><th>プラン</th><th>1ヶ月</th><th>6ヶ月</th><th>12ヶ月</th></tr></thead>'
    '<tbody>'
    '<tr><td><strong>Tinder Plus</strong></td><td>約1,200円/月〜</td><td>約767円/月〜</td><td>約500円/月〜</td></tr>'
    '<tr><td><strong>Tinder Gold</strong></td><td>約3,400円/月〜</td><td>約2,100円/月〜</td><td>約1,400円/月〜</td></tr>'
    '<tr><td><strong>Tinder Platinum</strong></td><td>約4,300円/月〜</td><td>約2,633円/月〜</td><td>約1,817円/月〜</td></tr>'
    '</tbody></table>'
    '<figcaption>※2026年3月時点の目安料金（iOS版基準）。実際の料金は個人により異なります。</figcaption>'
    '</figure>'
)

# Strategy: Find and replace pricing tables, add notice
# Look for existing table patterns with Tinder pricing
table_pattern = r'<figure class="wp-block-table"><table>.*?Tinder\s*Plus.*?</table></figure>'
table_matches = re.findall(table_pattern, new_content, re.DOTALL | re.IGNORECASE)

if table_matches:
    print(f"\n=== Found {len(table_matches)} pricing table(s) ===")
    for i, m in enumerate(table_matches):
        print(f"  Table {i+1}: {m[:100]}...")
    # Replace the first Tinder pricing table
    new_content = re.sub(table_pattern, UPDATED_PRICING_TABLE, new_content, count=1, flags=re.DOTALL | re.IGNORECASE)
    # Insert notice before the new table
    new_content = new_content.replace(UPDATED_PRICING_TABLE, PRICING_NOTICE + '\n' + UPDATED_PRICING_TABLE, 1)
    print("  -> Replaced pricing table + added notice")
else:
    print("\n=== No standard pricing table found, trying alternative patterns ===")
    # Try other table formats
    alt_table_pattern = r'<table[^>]*>.*?(?:Tinder\s*Plus|ティンダー.*?料金).*?</table>'
    alt_matches = re.findall(alt_table_pattern, new_content, re.DOTALL | re.IGNORECASE)
    if alt_matches:
        print(f"  Found {len(alt_matches)} alt table(s)")
        for i, m in enumerate(alt_matches):
            print(f"  Alt Table {i+1}: {m[:100]}...")
        new_content = re.sub(alt_table_pattern, UPDATED_PRICING_TABLE, new_content, count=1, flags=re.DOTALL | re.IGNORECASE)
        new_content = new_content.replace(UPDATED_PRICING_TABLE, PRICING_NOTICE + '\n' + UPDATED_PRICING_TABLE, 1)
        print("  -> Replaced alt pricing table + added notice")
    else:
        print("  No pricing table found at all. Will insert notice near first pricing mention.")

# Update individual price mentions throughout the article
# Common old prices -> new approximate prices with "約" prefix
price_replacements = [
    # Tinder Plus old prices -> new
    (r'(?:Tinder\s*Plus|ティンダープラス)[^<\n]{0,20}(?:月額|は)?[\s]*(\d{1,2},?\d{3})円',
     None),  # handled by table replacement
    # Specific inline price updates
    (r'(?<!約)1,?180円', '約1,200円〜'),
    (r'(?<!約)1,?480円', '約1,200円〜'),
    (r'(?<!約)2,?200円', '約1,200円〜'),  # old Plus prices
    (r'(?<!約)3,?300円(?!/月〜)', '約3,400円〜'),
    (r'(?<!約)3,?400円(?!/月〜)', '約3,400円〜'),
    (r'(?<!約)3,?700円', '約3,400円〜'),  # old Gold prices
    (r'(?<!約)4,?300円(?!/月〜)', '約4,300円〜'),
    (r'(?<!約)6,?300円', '約4,300円〜'),
    (r'(?<!約)7,?680円', '約4,300円〜'),  # old Platinum prices
]

for pattern, replacement in price_replacements:
    if replacement is None:
        continue
    count = len(re.findall(pattern, new_content))
    if count > 0:
        new_content = re.sub(pattern, replacement, new_content)
        print(f"  Replaced {count}x: {pattern} -> {replacement}")

# If notice wasn't inserted yet (no table found), insert before first h2 mentioning 料金
if PRICING_NOTICE not in new_content:
    # Insert after first mention of 料金 in an h2/h3
    pricing_heading = re.search(r'(<h[23][^>]*>.*?料金.*?</h[23]>)', new_content, re.IGNORECASE)
    if pricing_heading:
        insert_pos = pricing_heading.end()
        new_content = new_content[:insert_pos] + '\n' + PRICING_NOTICE + '\n' + new_content[insert_pos:]
        print("  -> Inserted pricing notice after first 料金 heading")
    else:
        # Last resort: insert after first h2
        first_h2 = re.search(r'(</h2>)', new_content)
        if first_h2:
            insert_pos = first_h2.end()
            new_content = new_content[:insert_pos] + '\n' + PRICING_NOTICE + '\n' + new_content[insert_pos:]
            print("  -> Inserted pricing notice after first h2")

# Also add a general note near any remaining "料金" section
# Add disclaimer at the end of content if not already present
DISCLAIMER = (
    '<p style="font-size:0.9em; color:#666; margin-top:30px;">'
    '※本記事のTinder料金情報は2026年3月時点の目安です。Tinderはパーソナライズド・プライシングを'
    '導入しているため、実際の料金はユーザーごとに異なります。最新の正確な料金はTinderアプリ内で'
    'ご確認ください。</p>'
)

if 'パーソナライズド・プライシング' not in new_content.split(PRICING_NOTICE)[-1][-500:]:
    new_content = new_content.rstrip() + '\n' + DISCLAIMER

# Step 4: Update via REST API
print(f"\n=== Updating article (original: {len(content)} chars -> new: {len(new_content)} chars) ===")

update_resp = requests.post(
    BASE_URL,
    auth=(WP_USER, WP_PASS),
    json={"content": new_content},
    headers={"Content-Type": "application/json"}
)

if update_resp.status_code == 200:
    print("SUCCESS: Article updated!")
    updated = update_resp.json()
    print(f"  Title: {updated['title']['rendered']}")
    print(f"  Modified: {updated['modified']}")
    print(f"  Link: {updated['link']}")
else:
    print(f"FAILED: {update_resp.status_code}")
    print(update_resp.text[:500])

# Save updated content for reference
with open(r"C:\Users\tmizu\マイドライブ\GitHub\claude-code\sites\otona-match.com\outputs\tinder-531-updated.html", "w", encoding="utf-8") as f:
    f.write(new_content)
print("Updated content saved to outputs/tinder-531-updated.html")
