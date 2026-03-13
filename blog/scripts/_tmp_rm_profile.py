import requests, json, re

creds = json.load(open('c:/Users/tmizu/マイドライブ/GitHub/claude-code/blog/config/secrets.json'))
wp = creds['wordpress']
auth = (wp['username'], wp['app_password'])

post_ids = [1070, 1068, 1067, 1066, 1065]

for pid in post_ids:
    r = requests.get(f'https://nambei-oyaji.com/wp-json/wp/v2/posts/{pid}?context=edit', auth=auth)
    post = r.json()
    content = post['content']['raw']
    title = post['title']['raw'][:40]
    original_len = len(content)

    # Pattern: <hr> or <hr /> then optional span, then <h2>筆者プロフィール</h2> and everything after
    # The h2 id varies but contains プロフィール
    pattern = r'\n?<hr\s*/?\s*>\s*\n?(?:<p><span id="[^"]*"></span></p>\s*\n?)?<h2[^>]*>[^<]*プロフィール[^<]*</h2>.*'
    new_content = re.sub(pattern, '', content, flags=re.DOTALL)

    if len(new_content) < original_len:
        r2 = requests.post(f'https://nambei-oyaji.com/wp-json/wp/v2/posts/{pid}', auth=auth, json={'content': new_content})
        print(f'ID:{pid} - removed {original_len - len(new_content)} chars, status: {r2.status_code}')
    else:
        print(f'ID:{pid} - NO MATCH')
        # Debug: show what's around プロフィール
        idx = content.find('プロフィール')
        if idx > -1:
            print(f'  Context: {repr(content[max(0,idx-100):idx+100])}')
