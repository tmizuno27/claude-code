#!/usr/bin/env python3
"""Add more <strong> emphasis tags to published WordPress articles."""

import requests
import re
import base64
import sys

WP_API = "https://nambei-oyaji.com/wp-json/wp/v2/posts"
AUTH = base64.b64encode(b"t.mizuno27@gmail.com:WutS MaRq ukGx OcQ8 uhBj Ej0D").decode()
HEADERS = {
    "Authorization": f"Basic {AUTH}",
    "Content-Type": "application/json",
}
ARTICLE_IDS = [1214, 1070, 1069, 1068, 1067, 1066, 1065, 1008]

# Phrases/patterns to bold - organized by category
# Each pattern should match 5-25 chars (max 30)
BOLD_PATTERNS = [
    # Numbers, costs, percentages, time periods
    r'(?:約|およそ|最大|最低|月額?|年間?|合計|総額)?[\d,\.]+(?:万?円|ドル|USD|%|パーセント|ヶ月|年間?|日間?|時間|km|人|件|倍|分の1|歳)',
    r'[\d,]+(?:Gs|グアラニー)',
    r'(?:月額?|年間?)[\d,\.]+(?:万?円|ドル)',

    # Comparisons
    r'日本の[\d/／]+(?:程度|以下)?',
    r'日本より[^\s。、]{2,12}',
    r'日本と比べ[^\s。、]{2,12}',
    r'最(?:安|高|大|小|も[^\s。、]{2,8})',
    r'世界(?:最|トップ|有数)[^\s。、]{2,10}',
    r'(?:圧倒的|断トツ)[にで][^\s。、]{2,10}',

    # Conclusions, recommendations
    r'(?:おすすめ|オススメ)(?:です|の[^\s]{1,6})?',
    r'(?:まず|必ず|絶対に)[^\s。、]{2,15}(?:ましょう|してください|すること|が必要|すべき)',
    r'(?:注意が必要|要注意|要確認)',
    r'(?:最も重要|一番大切|最優先)',

    # Emotional/impactful
    r'花粉ゼロ',
    r'災害がない',
    r'地震[がもは][^\s。、]{2,10}',
    r'治安[はがも][^\s。、]{2,10}',
    r'ビザ[がなは不][^\s。、]{2,10}',
    r'永住権[がをの][^\s。、]{2,10}',
    r'(?:無料|タダ|0円|ゼロ円)',
    r'(?:大幅[にな]|劇的[にな]|格段[にの])[^\s。、]{2,10}',

    # Key concepts
    r'(?:パーマネントビザ|一時滞在ビザ|永住ビザ)',
    r'(?:インターナショナルスクール|現地校|私立校)',
    r'(?:アプリケーションパスワード|二段階認証)',
    r'(?:為替レート|送金手数料|隠れコスト)',
    r'(?:食料自給率|自給自足)',
    r'(?:所得税|法人税|付加価値税|消費税)[がはの][^\s。、]{2,10}',
    r'(?:Wise|Revolut|Western Union|PayPal)',
    r'(?:E-E-A-T|SEO|GA4)',

    # Action items
    r'(?:事前に|あらかじめ|前もって)[^\s。、]{2,15}',
    r'[^\s。、]{2,8}(?:が鍵|がカギ|がポイント|が重要|が大切|が必須)',

    # Important qualifiers
    r'(?:実体験|一次情報|リアルな)',
    r'(?:現地で|実際に)[^\s。、]{2,12}',
    r'(?:意外と|実は|驚くほど)[^\s。、]{2,12}',
]


def is_inside_tag(html, pos, tags=('strong', 'h2', 'h3', 'h4', 'th', 'a', 'style')):
    """Check if position is inside any of the specified tags."""
    for tag in tags:
        # Find all opening/closing tag pairs
        pattern = re.compile(rf'<{tag}[^>]*>(.*?)</{tag}>', re.DOTALL | re.IGNORECASE)
        for m in pattern.finditer(html):
            if m.start() <= pos < m.end():
                return True
    return False


def is_inside_html_tag(html, pos):
    """Check if position is inside an HTML tag itself (between < and >)."""
    # Look backward for < or >
    i = pos - 1
    while i >= 0:
        if html[i] == '>':
            return False
        if html[i] == '<':
            return True
        i -= 1
    return False


def count_strong_in_paragraph(html, para_start, para_end):
    """Count <strong> tags in a paragraph region."""
    segment = html[para_start:para_end]
    return len(re.findall(r'<strong', segment, re.IGNORECASE))


def count_strong_in_section(html, section_start, section_end):
    """Count <strong> tags in a section region."""
    segment = html[section_start:section_end]
    return len(re.findall(r'<strong', segment, re.IGNORECASE))


def get_section_boundaries(html):
    """Get boundaries between h2 headings."""
    h2_positions = [m.start() for m in re.finditer(r'<h2[^>]*>', html, re.IGNORECASE)]
    boundaries = []
    for i, start in enumerate(h2_positions):
        end = h2_positions[i + 1] if i + 1 < len(h2_positions) else len(html)
        boundaries.append((start, end))
    return boundaries


def get_paragraph_boundaries(html):
    """Get paragraph boundaries."""
    boundaries = []
    for m in re.finditer(r'<p[^>]*>(.*?)</p>', html, re.DOTALL | re.IGNORECASE):
        boundaries.append((m.start(), m.end()))
    # Also consider <li> tags
    for m in re.finditer(r'<li[^>]*>(.*?)</li>', html, re.DOTALL | re.IGNORECASE):
        boundaries.append((m.start(), m.end()))
    return boundaries


def add_emphasis(html):
    """Add more <strong> tags to HTML content."""
    # Collect all candidate matches with positions
    candidates = []

    for pattern in BOLD_PATTERNS:
        try:
            for m in re.finditer(pattern, html):
                text = m.group(0)
                start = m.start()
                end = m.end()

                # Skip if too short or too long
                if len(text) < 3 or len(text) > 30:
                    continue

                candidates.append((start, end, text))
        except re.error:
            continue

    # Sort by position (reverse so we can insert without shifting)
    candidates.sort(key=lambda x: x[0])

    # Remove overlapping candidates (keep first)
    filtered = []
    last_end = -1
    for start, end, text in candidates:
        if start >= last_end:
            filtered.append((start, end, text))
            last_end = end

    # Get section and paragraph boundaries
    sections = get_section_boundaries(html)
    paragraphs = get_paragraph_boundaries(html)

    # Track how many <strong> we add per section and per paragraph
    section_added = {}
    para_added = {}

    # For each section, count existing <strong> tags
    section_existing = {}
    for i, (s_start, s_end) in enumerate(sections):
        section_existing[i] = count_strong_in_section(html, s_start, s_end)

    # For each paragraph, count existing <strong> tags
    para_existing = {}
    for i, (p_start, p_end) in enumerate(paragraphs):
        para_existing[i] = count_strong_in_paragraph(html, p_start, p_end)

    # Filter candidates
    accepted = []
    for start, end, text in filtered:
        # Check if inside forbidden tags
        if is_inside_tag(html, start):
            continue
        if is_inside_html_tag(html, start):
            continue

        # Find which section this belongs to
        sec_idx = None
        for i, (s_start, s_end) in enumerate(sections):
            if s_start <= start < s_end:
                sec_idx = i
                break

        # Find which paragraph this belongs to
        para_idx = None
        for i, (p_start, p_end) in enumerate(paragraphs):
            if p_start <= start < p_end:
                para_idx = i
                break

        # Check section limit (aim for 5-8 total, so add up to 8 - existing)
        if sec_idx is not None:
            existing = section_existing.get(sec_idx, 0)
            added = section_added.get(sec_idx, 0)
            if existing + added >= 8:
                continue

        # Check paragraph limit (max 2 total per paragraph)
        if para_idx is not None:
            existing_p = para_existing.get(para_idx, 0)
            added_p = para_added.get(para_idx, 0)
            if existing_p + added_p >= 2:
                continue

        accepted.append((start, end, text))
        if sec_idx is not None:
            section_added[sec_idx] = section_added.get(sec_idx, 0) + 1
        if para_idx is not None:
            para_added[para_idx] = para_added.get(para_idx, 0) + 1

    # Apply in reverse order
    new_html = html
    for start, end, text in reversed(accepted):
        new_html = new_html[:start] + f"<strong>{text}</strong>" + new_html[end:]

    return new_html, len(accepted)


def process_article(article_id):
    """Fetch, add emphasis, and update an article."""
    # Fetch
    resp = requests.get(f"{WP_API}/{article_id}?context=edit", headers=HEADERS)
    if resp.status_code != 200:
        print(f"  ERROR fetching {article_id}: {resp.status_code}")
        return 0

    data = resp.json()
    title = data.get("title", {}).get("raw", "???")
    content = data.get("content", {}).get("raw", "")

    if not content:
        print(f"  Article {article_id} ({title}): empty content, skipping")
        return 0

    # Count existing
    existing_count = len(re.findall(r'<strong', content, re.IGNORECASE))

    # Add emphasis
    new_content, added = add_emphasis(content)

    new_count = len(re.findall(r'<strong', new_content, re.IGNORECASE))

    print(f"  Article {article_id} ({title}): {existing_count} existing, +{added} new = {new_count} total")

    if added == 0:
        print(f"    No new emphasis needed")
        return 0

    # Update
    update_resp = requests.post(
        f"{WP_API}/{article_id}",
        headers=HEADERS,
        json={"content": new_content},
    )

    if update_resp.status_code == 200:
        print(f"    Updated successfully")
    else:
        print(f"    ERROR updating: {update_resp.status_code} - {update_resp.text[:200]}")
        return 0

    return added


def main():
    print("Adding more <strong> emphasis to published articles...\n")

    total_added = 0
    for aid in ARTICLE_IDS:
        added = process_article(aid)
        total_added += added
        print()

    print(f"TOTAL: {total_added} new <strong> tags added across {len(ARTICLE_IDS)} articles")


if __name__ == "__main__":
    main()
