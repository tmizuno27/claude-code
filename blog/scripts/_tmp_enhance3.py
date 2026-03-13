import requests, json, re

creds = json.load(open('c:/Users/tmizu/マイドライブ/GitHub/claude-code/blog/config/secrets.json'))
wp = creds['wordpress']
auth = (wp['username'], wp['app_password'])

YELLOW = 'background:linear-gradient(transparent 60%,#fff3cd 60%)'
PINK = 'background:linear-gradient(transparent 60%,#ffd6e7 60%)'
BLUE = 'background:linear-gradient(transparent 60%,#d6e4ff 60%)'

def add_marker_to_strong(content, phrase_in_strong, color):
    """Add marker to an existing <strong>phrase</strong>."""
    escaped = re.escape(phrase_in_strong)
    pattern = f'<strong>({escaped})</strong>'
    replacement = f'<span style="{color}"><strong>\\1</strong></span>'
    return re.sub(pattern, replacement, content, count=1)

# Per-article: pick 3-5 most important <strong> phrases to add markers
highlights = {
    1070: [  # 海外送金
        ('実際に使って送金してみた', YELLOW),
        ('為替レート', BLUE),
        ('実質コスト', YELLOW),
        ('銀行送金だけは避けた方がいい', PINK),
        ('手数料の安さ', BLUE),
    ],
    1068: [  # 海外で子育て
        ('実際にやってみた', YELLOW),
        ('実際に経験した子連れ海外移住の準備', YELLOW),
        ('学費は現地校で月3〜4万円程度', BLUE),
        ('月15〜20万円', BLUE),
        ('子連れ海外移住の準備は、6ヶ月前から「住居・学校・ビザ」「保険・保険・予防」「手続き・引越」の3段階で進めるのが安心です。', YELLOW),
    ],
    1067: [  # 治安
        ('治安は「南米の中では比較的安定している」', YELLOW),
        ('日本に比べると確かに危険', PINK),
        ('実際に住んでみた', YELLOW),
        ('場所によってまったく違う', YELLOW),
        ('夜間の外出は車移動が基本', PINK),
        ('スマホは見えない場所で', PINK),
        ('現金は最低限', PINK),
    ],
}

for pid, phrases in highlights.items():
    r = requests.get(f'https://nambei-oyaji.com/wp-json/wp/v2/posts/{pid}?context=edit&_fields=content,title', auth=auth)
    data = r.json()
    content = data['content']['raw']
    title = data.get('title', {}).get('raw', '')[:40]

    applied = 0
    for phrase, color in phrases:
        new_content = add_marker_to_strong(content, phrase, color)
        if new_content != content:
            content = new_content
            applied += 1

    if applied > 0:
        r2 = requests.post(f'https://nambei-oyaji.com/wp-json/wp/v2/posts/{pid}', auth=auth, json={'content': content})
        print(f'ID:{pid} - {applied} markers added, status: {r2.status_code}')
    else:
        print(f'ID:{pid} - no matches (phrases may not match exactly)')

# Now also add markers to remaining articles that got few
# For articles 1214, 1066, 1065, 1008 - add more markers to existing strongs
more_highlights = {
    1214: [  # 食文化
        ('週末のアサードは家族の絆を深める大切な時間', BLUE),
    ],
    1066: [  # 生活費
        ('食費が圧倒的に安い', YELLOW),
    ],
    1065: [  # 移住費用
        ('永住権の取得が比較的容易', YELLOW),
    ],
    1008: [  # 気候
        ('自然災害がほぼゼロ', YELLOW),
        ('花粉症ゼロ', BLUE),
    ],
}

for pid, phrases in more_highlights.items():
    r = requests.get(f'https://nambei-oyaji.com/wp-json/wp/v2/posts/{pid}?context=edit&_fields=content,title', auth=auth)
    data = r.json()
    content = data['content']['raw']

    applied = 0
    for phrase, color in phrases:
        new_content = add_marker_to_strong(content, phrase, color)
        if new_content != content:
            content = new_content
            applied += 1

    if applied > 0:
        r2 = requests.post(f'https://nambei-oyaji.com/wp-json/wp/v2/posts/{pid}', auth=auth, json={'content': content})
        print(f'ID:{pid} - {applied} more markers, status: {r2.status_code}')

print("\nDone!")
