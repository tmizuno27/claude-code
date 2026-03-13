import requests, json, re

creds = json.load(open('c:/Users/tmizu/マイドライブ/GitHub/claude-code/blog/config/secrets.json'))
wp = creds['wordpress']
auth = (wp['username'], wp['app_password'])

post_ids = [1214, 1070, 1069, 1068, 1067, 1066, 1065, 1008]

# ===== STEP 1: Clean up embedded script/style from all articles =====
print("=== STEP 1: Cleaning embedded script/style ===")
for pid in post_ids:
    r = requests.get(f'https://nambei-oyaji.com/wp-json/wp/v2/posts/{pid}?context=edit&_fields=content,title', auth=auth)
    data = r.json()
    content = data['content']['raw']
    title = data.get('title', {}).get('raw', '')[:40]
    original_len = len(content)

    # Remove <script>...</script> blocks
    content = re.sub(r'<script[\s\S]*?</script>\s*', '', content, flags=re.IGNORECASE)

    # Remove <style>...</style> blocks
    content = re.sub(r'<style[\s\S]*?</style>\s*', '', content, flags=re.IGNORECASE)

    # Remove leftover wpautop artifacts from style removal (e.g. <p>/* CSS comments */...</p>)
    content = re.sub(r'<p>/\*[\s\S]*?\*/</p>\s*', '', content)
    content = re.sub(r'<p>\s*</p>\s*', '', content)  # empty paragraphs

    # Clean leading whitespace
    content = content.lstrip()

    removed = original_len - len(content)
    if removed > 0:
        r2 = requests.post(f'https://nambei-oyaji.com/wp-json/wp/v2/posts/{pid}', auth=auth, json={'content': content})
        print(f'  ID:{pid} cleaned {removed} chars, status: {r2.status_code}')
    else:
        print(f'  ID:{pid} already clean')

# ===== STEP 2: Add bold + color highlights to all articles =====
print("\n=== STEP 2: Adding bold & color highlights ===")

# Color scheme:
# - Key numbers/stats: <strong style="color:#d4380d"> (warm red-orange)
# - Important conclusions: <strong style="background:linear-gradient(transparent 60%,#ffd6e7 60%)"> (pink marker)
# - Emphasis: <strong> (just bold)

def enhance_article(content):
    """Add strategic bold and color highlights to article content."""

    # Skip if already heavily formatted
    strong_count = content.count('<strong')
    if strong_count > 20:
        return content, False

    # Pattern 1: Numbers with units (金額, 割合, 期間) - make them stand out
    # Match patterns like 月XX万円, XX%, XX年, XX円, XX万, XXドル etc.
    # Only wrap if not already in <strong>
    def highlight_number(match):
        full = match.group(0)
        # Don't double-wrap
        if '<strong' in full or '</strong>' in full:
            return full
        return f'<strong>{full}</strong>'

    # Key monetary amounts (月XX万円, XXX万円, XX,XXX円 etc.)
    content = re.sub(
        r'(?<!<strong>)(?<!<strong style="[^"]*">)(月[\d,\.]+万円?〜?[\d,\.]*万?円?|[\d,\.]+万円〜[\d,\.]+万円|約[\d,\.]+万円|[\d,\.]+万円|[\d,]+円〜[\d,]+円|[\d,]+ドル|USD\s*[\d,\.]+)',
        highlight_number, content
    )

    # Percentages
    content = re.sub(
        r'(?<!</strong>)(?<!<strong>)([\d\.]+%〜[\d\.]+%|約[\d\.]+%|[\d\.]+%)',
        highlight_number, content
    )

    # Pattern 2: Important phrases - add background marker highlight
    marker_style = 'background:linear-gradient(transparent 60%,#fff3cd 60%)'

    important_phrases = [
        '実体験', '一次情報', '最大のメリット', '最大のデメリット',
        '絶対に', '要注意', '注意が必要', '必ず',
        'おすすめ', 'おすすめです', '結論から言うと',
        '最も重要', '一番大切', 'ポイント',
    ]

    for phrase in important_phrases:
        # Only highlight if not already in strong/styled tag
        pattern = f'(?<!</strong>)(?<!<strong>)(?<!">){re.escape(phrase)}'
        replacement = f'<span style="{marker_style}"><strong>{phrase}</strong></span>'
        # Only replace first 2 occurrences per phrase to avoid over-highlighting
        content = re.sub(pattern, replacement, content, count=2)

    # Pattern 3: Key takeaway sentences after 結論 or まとめ headings
    # These are already in headings so skip

    return content, True

for pid in post_ids:
    r = requests.get(f'https://nambei-oyaji.com/wp-json/wp/v2/posts/{pid}?context=edit&_fields=content,title', auth=auth)
    data = r.json()
    content = data['content']['raw']
    title = data.get('title', {}).get('raw', '')[:40]

    new_content, changed = enhance_article(content)

    if changed and new_content != content:
        added_strongs = new_content.count('<strong') - content.count('<strong')
        added_spans = new_content.count('<span style=') - content.count('<span style=')
        r2 = requests.post(f'https://nambei-oyaji.com/wp-json/wp/v2/posts/{pid}', auth=auth, json={'content': new_content})
        print(f'  ID:{pid} +{added_strongs} bold, +{added_spans} markers, status: {r2.status_code}')
    else:
        print(f'  ID:{pid} no changes needed')

print("\nDone!")
