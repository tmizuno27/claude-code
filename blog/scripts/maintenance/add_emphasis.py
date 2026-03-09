"""
Add <strong> emphasis to key phrases in published WordPress articles.
Targets: important numbers/costs, key conclusions, warnings, service names.
Conservative: 3-5 per section max, short phrases (5-25 chars).
"""

import requests
import re
import base64
import time

WP_API = "https://nambei-oyaji.com/wp-json/wp/v2"
AUTH = base64.b64encode(b"t.mizuno27@gmail.com:agNg 2624 4lL4 QoT9 EOOZ OEZr").decode()
HEADERS = {
    "Authorization": f"Basic {AUTH}",
    "Content-Type": "application/json"
}

ARTICLE_IDS = [1214, 1070, 1069, 1068, 1067, 1066, 1065, 1008]

# Patterns: money with context prefix (月15万円, 約100万円, etc.)
MONEY_PATTERN = r'(?:約|月(?:々|額)?|年間?|毎月|合計|最大|最低|最小|総額|初期費用)?[\d,]+(?:万)?(?:円|ドル|USD)(?:前後|程度|以上|以下|～[\d,]+(?:万)?(?:円|ドル))?'
# Guarani amounts
GUARANI_PATTERN = r'[\d,]+(?:万)?(?:グアラニー|ガラニー|Gs)'
# Percentages with context
PERCENT_PATTERN = r'(?:約)?[\d,\.]+(?:%|パーセント)'
# Time periods - only with context prefix to avoid bare "1年" etc.
TIME_PATTERN = r'(?:約|最短|最長)[\d,]+(?:ヶ月|か月|カ月|年|週間|日間|時間)'
# Important keyword phrases
KEYWORD_PHRASES = [
    r'永住権(?:の)?取得',
    r'ビザ(?:なし|免除|不要)',
    r'要注意',
    r'必ず確認',
    r'手数料(?:無料|ゼロ|なし|0円)',
    r'送金手数料(?:が)?(?:無料|安い|最安)',
    r'為替手数料',
    r'自然災害(?:が)?(?:ない|ゼロ|ほぼない)',
    r'治安(?:が)?(?:良い|悪い|改善)',
    r'(?:最大の)?メリット',
    r'(?:最大の)?デメリット',
]

ALL_PATTERNS = (
    [MONEY_PATTERN, GUARANI_PATTERN, PERCENT_PATTERN, TIME_PATTERN]
    + KEYWORD_PHRASES
)


def fetch_article(post_id):
    url = f"{WP_API}/posts/{post_id}?context=edit"
    resp = requests.get(url, headers=HEADERS)
    resp.raise_for_status()
    data = resp.json()
    return data["title"]["raw"], data["content"]["raw"]


def update_article(post_id, content):
    url = f"{WP_API}/posts/{post_id}"
    resp = requests.post(url, headers=HEADERS, json={"content": content})
    resp.raise_for_status()
    return resp.status_code


def is_inside_tag(text, pos):
    i = pos - 1
    while i >= 0:
        if text[i] == '>':
            return False
        if text[i] == '<':
            return True
        i -= 1
    return False


def is_in_protected_context(content, start, end):
    """Check if match is inside heading, link, strong, th, style, td, caption, or HTML attr."""
    before = content[max(0, start - 2000):start]

    # Style block
    if len(re.findall(r'<style', before, re.I)) > len(re.findall(r'</style', before, re.I)):
        return True

    # Headings
    for t in ['h1','h2','h3','h4','h5','h6']:
        if len(re.findall(rf'<{t}[\s>]', before, re.I)) > len(re.findall(rf'</{t}>', before, re.I)):
            return True

    # Links
    if len(re.findall(r'<a[\s>]', before, re.I)) > len(re.findall(r'</a>', before, re.I)):
        return True

    # Already strong
    if len(re.findall(r'<strong', before, re.I)) > len(re.findall(r'</strong>', before, re.I)):
        return True

    # Table headers
    if len(re.findall(r'<th[\s>]', before, re.I)) > len(re.findall(r'</th>', before, re.I)):
        return True

    # Table cells (td) - skip to avoid messing with table formatting
    if len(re.findall(r'<td[\s>]', before, re.I)) > len(re.findall(r'</td>', before, re.I)):
        return True

    # Inside HTML tag
    if is_inside_tag(content, start):
        return True

    # HTML comments
    if len(re.findall(r'<!--', before)) > len(re.findall(r'-->', before)):
        return True

    # figcaption
    if len(re.findall(r'<figcaption', before, re.I)) > len(re.findall(r'</figcaption', before, re.I)):
        return True

    return False


def add_emphasis(content):
    changes = []
    candidates = []

    for pattern in ALL_PATTERNS:
        for m in re.finditer(pattern, content):
            text = m.group()
            # Skip too short/long
            if len(text) < 3 or len(text) > 25:
                continue
            # Skip bare numbers
            if re.match(r'^[\d,\.]+$', text):
                continue
            # Skip year-only matches like "2026年", "2025年" - not meaningful emphasis
            if re.match(r'^(?:約)?(?:19|20)\d{2}年$', text):
                continue
            # Skip "100%" alone (often just filler)
            if text == '100%':
                continue
            if not is_in_protected_context(content, m.start(), m.end()):
                candidates.append((m.start(), m.end(), text))

    # Deduplicate overlapping, keep longer
    candidates.sort(key=lambda x: x[0])
    filtered = []
    for c in candidates:
        if filtered and c[0] < filtered[-1][1]:
            if len(c[2]) > len(filtered[-1][2]):
                filtered[-1] = c
            continue
        filtered.append(c)

    # Deduplicate same text in same section (only keep first occurrence per section)
    h2_positions = [m.start() for m in re.finditer(r'<h2', content, re.I)]
    h2_positions.append(len(content))

    def get_section(pos):
        for i, h2 in enumerate(h2_positions):
            if pos < h2:
                return i
        return len(h2_positions) - 1

    seen_in_section = {}  # (section, text) -> True
    deduped = []
    for s, e, t in filtered:
        sec = get_section(s)
        key = (sec, t)
        if key in seen_in_section:
            continue
        seen_in_section[key] = True
        deduped.append((s, e, t))

    # Limit: max 4 per section
    section_counts = {}
    final = []
    for s, e, t in deduped:
        sec = get_section(s)
        cnt = section_counts.get(sec, 0)
        if cnt < 4:
            section_counts[sec] = cnt + 1
            final.append((s, e, t))

    # Apply in reverse
    final.sort(key=lambda x: x[0], reverse=True)
    for s, e, t in final:
        content = content[:s] + f"<strong>{t}</strong>" + content[e:]
        changes.append(t)

    changes.reverse()
    return content, changes


def main():
    for post_id in ARTICLE_IDS:
        print(f"\n{'='*60}")
        print(f"Processing article ID: {post_id}")
        print('='*60)

        try:
            title, content = fetch_article(post_id)
            print(f"Title: {title}")
            print(f"Content length: {len(content)} chars")

            new_content, changes = add_emphasis(content)

            if not changes:
                print("  No changes needed.")
                continue

            print(f"  Adding {len(changes)} emphasis tags:")
            for i, c in enumerate(changes, 1):
                print(f"    {i}. [{c}]")

            status = update_article(post_id, new_content)
            print(f"  Updated! Status: {status}")
            time.sleep(1)

        except Exception as e:
            print(f"  ERROR: {e}")
            import traceback
            traceback.print_exc()


if __name__ == "__main__":
    main()
