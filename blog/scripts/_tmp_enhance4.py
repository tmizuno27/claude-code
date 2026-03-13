import requests, json, re

creds = json.load(open('c:/Users/tmizu/マイドライブ/GitHub/claude-code/blog/config/secrets.json'))
wp = creds['wordpress']
auth = (wp['username'], wp['app_password'])

YELLOW = 'background:linear-gradient(transparent 60%,#fff3cd 60%)'
PINK = 'background:linear-gradient(transparent 60%,#ffd6e7 60%)'
BLUE = 'background:linear-gradient(transparent 60%,#d6e4ff 60%)'

def add_marker(content, phrase, color):
    """Add marker to <strong>phrase</strong>."""
    escaped = re.escape(phrase)
    pattern = f'<strong>({escaped})</strong>'
    replacement = f'<span style="{color}"><strong>\\1</strong></span>'
    return re.sub(pattern, replacement, content, count=1)

post_ids = [1214, 1070, 1069, 1068, 1067, 1066, 1065, 1008]

for pid in post_ids:
    r = requests.get(f'https://nambei-oyaji.com/wp-json/wp/v2/posts/{pid}?context=edit&_fields=content,title', auth=auth)
    data = r.json()
    content = data['content']['raw']
    title = data.get('title', {}).get('raw', '')[:40]

    # Find all existing <strong> phrases
    strongs = re.findall(r'<strong>([^<]{4,80})</strong>', content)
    # Filter out ones already marked
    already_marked = set(m.group(1) for m in re.finditer(r'<span style="[^"]*linear-gradient[^"]*"><strong>([^<]+)</strong></span>', content))
    available = [s for s in strongs if s not in already_marked]

    # Strategy: mark every 4th-5th strong to get ~5-8 markers per article
    # Pick strategically: longer phrases, numbers, key conclusions
    scored = []
    for s in available:
        score = 0
        # Prefer phrases with numbers
        if re.search(r'[\d,]+', s): score += 3
        # Prefer longer phrases (more meaningful)
        if len(s) > 15: score += 2
        # Prefer conclusions/key words
        keywords = ['おすすめ', '安い', '高い', '注意', '重要', '必ず', 'メリット', 'デメリット',
                     '実際', '結論', 'ポイント', '最大', '最も', '一番', '圧倒的', '驚',
                     '無料', '半額', '簡単', '難し', '危険', '安全', '人気']
        for kw in keywords:
            if kw in s: score += 2
        # Prefer phrases with yen/percentage
        if '円' in s or '%' in s or 'ドル' in s: score += 3
        scored.append((score, s))

    # Sort by score desc, pick top 5-7
    scored.sort(key=lambda x: -x[0])
    to_mark = scored[:7]

    applied = 0
    for i, (score, phrase) in enumerate(to_mark):
        # Alternate colors: yellow for top, blue for medium, pink for warnings
        if '注意' in phrase or '危険' in phrase or '避け' in phrase or '高い' in phrase or '高すぎ' in phrase:
            color = PINK
        elif i % 3 == 0:
            color = YELLOW
        elif i % 3 == 1:
            color = BLUE
        else:
            color = YELLOW

        new_content = add_marker(content, phrase, color)
        if new_content != content:
            content = new_content
            applied += 1

    if applied > 0:
        r2 = requests.post(f'https://nambei-oyaji.com/wp-json/wp/v2/posts/{pid}', auth=auth, json={'content': content})
        total_markers = len(re.findall(r'linear-gradient', content))
        print(f'ID:{pid} +{applied} markers (total: {total_markers}), status: {r2.status_code}')
    else:
        total_markers = len(re.findall(r'linear-gradient', content))
        print(f'ID:{pid} no new markers (total: {total_markers})')

print("\nDone!")
