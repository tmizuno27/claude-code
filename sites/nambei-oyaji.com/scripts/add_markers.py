"""
全公開記事にカラーマーカー（ハイライト）を追加するスクリプト
- 黄色(#fff3cd): 結論・重要数字
- ピンク(#ffd6e7): 注意・警告
- 青色(#d6e4ff): メリット・ポジティブ
"""
import requests
import json
import base64
import sys

# WordPress credentials
with open('config/wp-credentials.json', encoding='utf-8') as f:
    creds = json.load(f)

auth = base64.b64encode(f"{creds['username']}:{creds['app_password']}".encode()).decode()
headers = {
    'Authorization': f'Basic {auth}',
    'Content-Type': 'application/json'
}

def yellow(text):
    return f'<span style="background:linear-gradient(transparent 60%,#fff3cd 60%)"><strong>{text}</strong></span>'

def pink(text):
    return f'<span style="background:linear-gradient(transparent 60%,#ffd6e7 60%)"><strong>{text}</strong></span>'

def blue(text):
    return f'<span style="background:linear-gradient(transparent 60%,#d6e4ff 60%)"><strong>{text}</strong></span>'

# Define replacements per article
# Format: (old_string, new_string)
# Only target phrases that are NOT already marked

replacements = {
    # ID:1008 気候と天気 - 既に6マーカー、3つ追加
    1008: [
        # 花粉ゼロの感動フレーズ
        ('<span>パラグアイに来てから花粉症の症状がゼロ</span>',
         blue('パラグアイに来てから花粉症の症状がゼロ')),
        # 服装アドバイスの重要ポイント
        ('<span>地震がない、台風がない、花粉がない</span>',
         yellow('地震がない、台風がない、花粉がない')),
        # デメリット3つ目
        ('<strong>3. 紫外線が非常に強い</strong>',
         pink('3. 紫外線が非常に強い')),
    ],

    # ID:1065 移住費用 - 既に5マーカー、5つ追加
    1065: [
        # 日本との比較（コスパ訴求）
        ('日本なら同じ3LDKで敷金2ヶ月＋礼金1ヶ月＋仲介手数料＋前家賃で50〜60万円は飛ぶ。パラグアイは15万円。',
         '日本なら同じ3LDKで敷金2ヶ月＋礼金1ヶ月＋仲介手数料＋前家賃で50〜60万円は飛ぶ。' + yellow('パラグアイは15万円') + '。'),
        # 隠れコスト警告
        ('<strong>実際には書かれていない出費が必ずある</strong>',
         pink('実際には書かれていない出費が必ずある')),
        # VPN推奨
        ('VPNは海外生活の必需品です',
         blue('VPNは海外生活の必需品') + 'です'),
        # 精神的安定の訴求
        ('パラグアイでは<strong>月10万円</strong>で「余裕のある暮らし」ができる',
         'パラグアイでは' + yellow('月10万円で「余裕のある暮らし」ができる')),
        # 最後のCTA
        ('動き出すなら今日がベスト',
         blue('動き出すなら今日がベスト')),
    ],

    # ID:1066 生活費 - 既に7マーカー、3つ追加
    1066: [
        # 生活の質キープの訴求
        ('生活の質をほぼ落とさずに半分以下のコストで暮らせている',
         blue('生活の質をほぼ落とさずに半分以下のコストで暮らせている')),
        # 日本食材の高さ（注意喚起）
        ('醤油1本800〜1,000円、味噌1パック1,500円前後。泣ける',
         pink('醤油1本800〜1,000円、味噌1パック1,500円前後') + '。泣ける'),
        # まとめの結論
        ('家賃と食費だけで<strong>月10万円以上</strong>の節約ができる',
         '家賃と食費だけで' + yellow('月10万円以上の節約ができる')),
    ],

    # ID:1067 治安 - 既に5マーカー、4つ追加
    1067: [
        # 安全対策の鉄則
        ('抵抗しない。これが鉄則。',
         pink('抵抗しない。これが鉄則。')),
        # Global Peace Index
        ('<strong>2025年</strong>のGlobal Peace Indexでは南米4位にランクインしています',
         '<strong>2025年</strong>のGlobal Peace Indexでは' + blue('南米4位にランクイン') + 'しています'),
        # 結論フレーズ
        ('パラグアイは「危険な国」ではなく、「日本とは違うルールの国」',
         yellow('パラグアイは「危険な国」ではなく、「日本とは違うルールの国」')),
        # 医療保険の注意
        ('海外旅行保険またはプライベート病院の会員権は必須です。ここはケチらないでください',
         pink('海外旅行保険またはプライベート病院の会員権は必須') + 'です。ここはケチらないでください'),
    ],

    # ID:1068 子連れ移住 - 既に6マーカー、4つ追加
    1068: [
        # 子どもの適応力
        ('子どもの適応力には本当に驚かされます',
         blue('子どもの適応力には本当に驚かされます')),
        # 準備が大事
        ('大人の一人旅と違って準備の量は倍以上になる',
         pink('大人の一人旅と違って準備の量は倍以上になる')),
        # 子どもの感想（ポジティブ）
        ('今では2人とも「<strong>「日本より楽しい」と言っている</strong>',
         '今では2人とも「' + blue('「日本より楽しい」と言っている') + ''),
        # 結論
        ('後悔はない',
         yellow('後悔はない')),
    ],

    # ID:1069 働き方 - 既に6マーカー、4つ追加
    1069: [
        # 日本語で完結
        ('<strong>日本語のオンラインワークだけで、普通に生活できる</strong>',
         yellow('日本語のオンラインワークだけで、普通に生活できる')),
        # 収入安定度
        ('<strong>収入の安定度は5つの方法の中で断トツ</strong>',
         blue('収入の安定度は5つの方法の中で断トツ')),
        # VPNの重要性
        ('これがないとパラグアイからのリモートワークは正直成り立たない',
         pink('これがないとパラグアイからのリモートワークは正直成り立たない')),
        # 仕事の不安は理由にならない
        ('<strong>「仕事の不安」は移住しない理由にはならない</strong>',
         yellow('「仕事の不安」は移住しない理由にはならない')),
    ],

    # ID:1070 海外送金 - 既に8マーカー、2つ追加
    1070: [
        # 年間節約額
        ('<strong>年間で約6万〜12万円の節約</strong>',
         yellow('年間で約6万〜12万円の節約')),
        # 暗号資産の警告
        ('生活費の送金に暗号資産を使うのは個人的におすすめしない',
         pink('生活費の送金に暗号資産を使うのは個人的におすすめしない')),
    ],

    # ID:1214 食文化 - 既に5マーカー、4つ追加
    1214: [
        # アサード体験の感想
        ('「なんだこれ」と声が出た',
         yellow('「なんだこれ」と声が出た')),
        # 食費の安さ
        ('毎日肉を食べる生活をしても、食費は日本の半分以下に収まる',
         blue('毎日肉を食べる生活をしても、食費は日本の半分以下に収まる')),
        # 水道水の注意
        ('水道水は直接飲まないのが基本',
         pink('水道水は直接飲まないのが基本')),
        # 毎週アサードの結論
        ('毎週末アサードを楽しみながら生活費を日本の半分以下に抑えられる',
         yellow('毎週末アサードを楽しみながら生活費を日本の半分以下に抑えられる')),
    ],
}

def update_article(post_id, article_replacements):
    """記事を取得し、マーカーを追加して更新する"""
    # Get current content
    r = requests.get(f"{creds['api_base']}/posts/{post_id}?context=edit", headers=headers)
    if r.status_code != 200:
        print(f"  ERROR: Failed to fetch post {post_id}: {r.status_code}")
        return False

    post = r.json()
    content = post['content']['raw']
    title = post['title']['raw']

    applied = 0
    for old, new in article_replacements:
        if old in content:
            content = content.replace(old, new, 1)
            applied += 1
        else:
            # Try to find partial match for debugging
            short = old[:40]
            if short in content:
                print(f"  WARN: Full match not found but partial exists: {short}...")
            else:
                print(f"  SKIP: Not found: {old[:50]}...")

    if applied == 0:
        print(f"  No changes needed for {post_id}")
        return True

    # Update the post
    update_data = {'content': content}
    r = requests.post(
        f"{creds['api_base']}/posts/{post_id}",
        headers=headers,
        json=update_data
    )

    if r.status_code == 200:
        print(f"  OK: {applied} markers added to ID:{post_id} ({title[:30]})")
        return True
    else:
        print(f"  ERROR: Failed to update {post_id}: {r.status_code} {r.text[:200]}")
        return False

# Process all articles
print("=== Adding color markers to all published articles ===\n")
success = 0
for post_id, article_reps in replacements.items():
    print(f"Processing ID:{post_id} ({len(article_reps)} replacements)...")
    if update_article(post_id, article_reps):
        success += 1

print(f"\n=== Done: {success}/{len(replacements)} articles updated ===")
