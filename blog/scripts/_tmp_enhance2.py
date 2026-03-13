import requests, json, re

creds = json.load(open('c:/Users/tmizu/マイドライブ/GitHub/claude-code/blog/config/secrets.json'))
wp = creds['wordpress']
auth = (wp['username'], wp['app_password'])

# Yellow marker for key conclusions/recommendations
YELLOW = 'background:linear-gradient(transparent 60%,#fff3cd 60%)'
# Pink marker for warnings/important notes
PINK = 'background:linear-gradient(transparent 60%,#ffd6e7 60%)'
# Blue marker for positive highlights
BLUE = 'background:linear-gradient(transparent 60%,#d6e4ff 60%)'

def apply_marker(content, phrase, color=YELLOW, max_count=1):
    """Wrap a phrase with marker highlight. Only if not already styled."""
    escaped = re.escape(phrase)
    # Don't match if already inside a tag or styled span
    pattern = f'(?<!style=")(?<!">)(<strong>){escaped}(</strong>)'
    replacement = f'<span style="{color}">\\1{phrase}\\2</span>'
    new_content = re.sub(pattern, replacement, content, count=max_count)
    if new_content == content:
        # Try without strong tags
        pattern2 = f'(?<!">)(?<!style="){escaped}'
        replacement2 = f'<span style="{color}"><strong>{phrase}</strong></span>'
        new_content = re.sub(pattern2, replacement2, content, count=max_count)
    return new_content

# Per-article highlight rules
# Each entry: (post_id, [(phrase, color), ...])
highlights = {
    1214: [  # パラグアイの食文化
        ('アサードを中心に回っている', YELLOW),
        ('牛肉1kgあたり約500〜800円', YELLOW),
        ('家族4人でお腹いっぱい食べても2,000円程度', BLUE),
        ('週末のアサードは家族の絆を深める大切な時間', BLUE),
        ('テレレは単なる飲み物ではなく、コミュニケーションツール', YELLOW),
    ],
    1070: [  # 海外送金サービス比較
        ('Wiseが最もおすすめ', YELLOW),
        ('実質コストが最も安い', YELLOW),
        ('為替レートの透明性', BLUE),
        ('手数料の安さ', BLUE),
        ('銀行送金は手数料が高すぎる', PINK),
    ],
    1069: [  # 海外移住後の働き方
        ('リモートワーク', YELLOW),
        ('パラグアイの生活費の安さ', BLUE),
        ('月10〜30万円の収入', YELLOW),
        ('時差を味方にする', BLUE),
        ('スキルがなくても始められる', YELLOW),
    ],
    1068: [  # 海外で子育て
        ('英語+スペイン語のバイリンガル教育', YELLOW),
        ('日本の学校では得られない経験', BLUE),
        ('子供の適応力は大人より圧倒的に高い', YELLOW),
        ('学費は日本のインターナショナルスクールの半額以下', BLUE),
    ],
    1067: [  # パラグアイの治安
        ('基本的な防犯対策をしていれば安全に暮らせる', YELLOW),
        ('夜間の一人歩きは避ける', PINK),
        ('貴重品を見せびらかさない', PINK),
        ('住むエリアの選び方が最も重要', YELLOW),
    ],
    1066: [  # パラグアイの生活費
        ('日本の約3分の1', YELLOW),
        ('家族4人', BLUE),
        ('食費が圧倒的に安い', YELLOW),
        ('家賃は立地と物件で大きく変わる', BLUE),
    ],
    1065: [  # パラグアイ移住の費用
        ('永住権の取得が比較的容易', YELLOW),
        ('初期費用', YELLOW),
        ('ビザ', BLUE),
        ('渡航費', BLUE),
        ('思ったより安く移住できる', YELLOW),
    ],
    1008: [  # パラグアイの気候
        ('地震・台風・津波がない', YELLOW),
        ('自然災害がほぼゼロ', YELLOW),
        ('花粉症ゼロ', BLUE),
        ('一年中温暖', BLUE),
    ],
}

for pid, phrases in highlights.items():
    r = requests.get(f'https://nambei-oyaji.com/wp-json/wp/v2/posts/{pid}?context=edit&_fields=content,title', auth=auth)
    data = r.json()
    content = data['content']['raw']
    title = data.get('title', {}).get('raw', '')[:40]

    applied = 0
    for phrase, color in phrases:
        new_content = apply_marker(content, phrase, color)
        if new_content != content:
            content = new_content
            applied += 1

    if applied > 0:
        r2 = requests.post(f'https://nambei-oyaji.com/wp-json/wp/v2/posts/{pid}', auth=auth, json={'content': content})
        print(f'ID:{pid} {title} - {applied} markers added, status: {r2.status_code}')
    else:
        print(f'ID:{pid} {title} - no matches found')

print("\nDone!")
