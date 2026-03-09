"""
Add <strong> emphasis to key phrases in published WordPress articles.
Targets: important numbers, conclusions, warnings, service names.
Conservative approach: 3-6 per section, short phrases only.
"""

import requests
import re
import json
import base64
import time

WP_API = "https://nambei-oyaji.com/wp-json/wp/v2"
AUTH = base64.b64encode(b"t.mizuno27@gmail.com:WutS MaRq ukGx OcQ8 uhBj Ej0D").decode()
HEADERS = {
    "Authorization": f"Basic {AUTH}",
    "Content-Type": "application/json"
}

ARTICLE_IDS = [1214, 1070, 1069, 1068, 1067, 1066, 1065, 1008]

# Patterns to emphasize - Japanese key phrases with numbers, costs, warnings
# Each pattern: (regex, max_per_section)
EMPHASIS_PATTERNS = [
    # Money amounts: 月XX万円, XX万円, XX円, XX万ドル etc.
    (r'(?<![<>/a-zA-Z])(?:約|月|年間?|毎月|合計|最大|最低|総額)?[\d,\.]+(?:万)?(?:円|ドル|USD|Gs|グアラニー|ガラニー)(?:前後|程度|以上|以下|～|〜)?', None),
    # Percentages
    (r'(?<![<>/a-zA-Z])[\d,\.]+(?:%|パーセント)', None),
    # Time periods with numbers
    (r'(?:約)?[\d,]+(?:年|ヶ月|か月|カ月|週間|日間|日|時間)', None),
    # Specific important phrases that commonly appear in these articles
    (r'永住権(?:取得|の取得)', None),
    (r'ビザ(?:なし|免除|不要)', None),
    (r'治安(?:が[良悪]い|の[良悪]さ)', None),
    (r'(?:最大の)?(?:メリット|デメリット)', None),
    (r'要注意', None),
    (r'(?:絶対|必ず)(?:に)?(?:必要|確認|注意)', None),
    (r'無料', None),
    (r'(?:手数料|送料)(?:無料|ゼロ|なし)', None),
]

def fetch_article(post_id):
    """Fetch article raw content."""
    url = f"{WP_API}/posts/{post_id}?context=edit"
    resp = requests.get(url, headers=HEADERS)
    resp.raise_for_status()
    data = resp.json()
    return data["title"]["raw"], data["content"]["raw"]

def update_article(post_id, content):
    """PUT updated content back."""
    url = f"{WP_API}/posts/{post_id}"
    resp = requests.put(url, headers=HEADERS, json={"content": content})
    resp.raise_for_status()
    return resp.status_code

def is_inside_tag(text, pos):
    """Check if position is inside an HTML tag (between < and >)."""
    # Look backward for < or >
    i = pos - 1
    while i >= 0:
        if text[i] == '>':
            return False
        if text[i] == '<':
            return True
        i -= 1
    return False

def split_into_sections(content):
    """Split content by h2 headings, preserving the split points."""
    # Split on h2 tags but keep them
    parts = re.split(r'(<h2[^>]*>.*?</h2>)', content, flags=re.DOTALL)
    return parts

def is_in_protected_context(content, match_start, match_end):
    """Check if a match is inside a heading, link, strong, th, style, or HTML attribute."""
    # Check various protected contexts by looking at surrounding HTML
    text_before = content[max(0, match_start - 500):match_start]
    text_after = content[match_end:match_end + 500]

    # Inside <style> block
    style_opens = len(re.findall(r'<style', text_before, re.IGNORECASE))
    style_closes = len(re.findall(r'</style', text_before, re.IGNORECASE))
    if style_opens > style_closes:
        return True

    # Inside heading tags
    for tag in ['h1', 'h2', 'h3', 'h4', 'h5', 'h6']:
        opens = len(re.findall(rf'<{tag}[\s>]', text_before, re.IGNORECASE))
        closes = len(re.findall(rf'</{tag}>', text_before, re.IGNORECASE))
        if opens > closes:
            return True

    # Inside <a> tags
    a_opens = len(re.findall(r'<a[\s>]', text_before, re.IGNORECASE))
    a_closes = len(re.findall(r'</a>', text_before, re.IGNORECASE))
    if a_opens > a_closes:
        return True

    # Inside <strong> tags already
    s_opens = len(re.findall(r'<strong', text_before, re.IGNORECASE))
    s_closes = len(re.findall(r'</strong>', text_before, re.IGNORECASE))
    if s_opens > s_closes:
        return True

    # Inside <th> tags
    th_opens = len(re.findall(r'<th[\s>]', text_before, re.IGNORECASE))
    th_closes = len(re.findall(r'</th>', text_before, re.IGNORECASE))
    if th_opens > th_closes:
        return True

    # Inside HTML tag attributes
    if is_inside_tag(content, match_start):
        return True

    # Inside <!-- comments -->
    comment_opens = len(re.findall(r'<!--', text_before))
    comment_closes = len(re.findall(r'-->', text_before))
    if comment_opens > comment_closes:
        return True

    return False

def add_emphasis_to_content(content):
    """Add <strong> tags to key phrases in content."""
    changes = []

    # Collect all candidate matches with their positions
    candidates = []
    for pattern, _ in EMPHASIS_PATTERNS:
        for m in re.finditer(pattern, content):
            text = m.group()
            start = m.start()
            end = m.end()

            # Skip very short matches (1-2 chars) or very long (>30 chars)
            if len(text) < 2 or len(text) > 30:
                continue

            # Skip if just a bare number without context
            if re.match(r'^[\d,\.]+$', text):
                continue

            if not is_in_protected_context(content, start, end):
                candidates.append((start, end, text))

    # Remove overlapping candidates (keep longer ones)
    candidates.sort(key=lambda x: x[0])
    filtered = []
    for c in candidates:
        if filtered and c[0] < filtered[-1][1]:
            # Overlap - keep the longer one
            if len(c[2]) > len(filtered[-1][2]):
                filtered[-1] = c
            continue
        filtered.append(c)

    # Limit per section: find h2 boundaries
    h2_positions = [m.start() for m in re.finditer(r'<h2', content, re.IGNORECASE)]
    h2_positions.append(len(content))  # end sentinel

    # Group candidates by section
    section_counts = {}
    final_candidates = []
    for start, end, text in filtered:
        # Find which section this belongs to
        section_idx = 0
        for i, h2_pos in enumerate(h2_positions):
            if start < h2_pos:
                section_idx = i
                break

        count = section_counts.get(section_idx, 0)
        if count < 5:  # max 5 per section
            section_counts[section_idx] = count + 1
            final_candidates.append((start, end, text))

    # Apply changes in reverse order to preserve positions
    final_candidates.sort(key=lambda x: x[0], reverse=True)

    for start, end, text in final_candidates:
        content = content[:start] + f"<strong>{text}</strong>" + content[end:]
        changes.append(text)

    changes.reverse()
    return content, changes

def main():
    for post_id in ARTICLE_IDS:
        print(f"\n{'='*60}")
        print(f"Processing article ID: {post_id}")
        print(f"{'='*60}")

        try:
            title, content = fetch_article(post_id)
            print(f"Title: {title}")
            print(f"Content length: {len(content)} chars")

            new_content, changes = add_emphasis_to_content(content)

            if not changes:
                print("  No changes needed.")
                continue

            print(f"  Adding {len(changes)} emphasis tags:")
            for i, c in enumerate(changes, 1):
                print(f"    {i}. 「{c}」")

            # Update
            status = update_article(post_id, new_content)
            print(f"  Updated! Status: {status}")

            time.sleep(1)  # Be nice to the server

        except Exception as e:
            print(f"  ERROR: {e}")
            import traceback
            traceback.print_exc()

if __name__ == "__main__":
    main()
