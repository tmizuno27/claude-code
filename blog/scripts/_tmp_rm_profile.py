import requests, json, re

creds = json.load(open('c:/Users/tmizu/マイドライブ/GitHub/claude-code/blog/config/secrets.json'))
wp = creds['wordpress']
auth = (wp['username'], wp['app_password'])

post_ids = [1070, 1069, 1068, 1067, 1066, 1065]

for pid in post_ids:
    r = requests.get(f'https://nambei-oyaji.com/wp-json/wp/v2/posts/{pid}?context=edit', auth=auth)
    post = r.json()
    content = post['content']['raw']
    title = post['title']['raw'][:40]
    original_len = len(content)

    # Find the profile block: <hr /> followed by <p><strong>南米おやじ</strong></p> and everything after
    # Pattern: <hr /> or <hr class="..."/> then profile text until end
    pattern = r'\n?<hr\s*(?:class="[^"]*")?\s*/?\s*>\s*\n?<p><strong>南米おやじ</strong></p>.*'
    new_content = re.sub(pattern, '', content, flags=re.DOTALL)

    if len(new_content) < original_len:
        r2 = requests.post(f'https://nambei-oyaji.com/wp-json/wp/v2/posts/{pid}', auth=auth, json={'content': new_content})
        print(f'ID:{pid} {title} - removed {original_len - len(new_content)} chars, status: {r2.status_code}')
    else:
        print(f'ID:{pid} {title} - NO MATCH, checking alternative pattern...')
        # Alternative: look for <!-- wp:separator --> before profile
        pattern2 = r'\n?<!-- wp:separator.*?-->.*?<!-- /wp:separator -->\s*\n?<!-- wp:paragraph.*?-->\s*\n?<p><strong>南米おやじ</strong></p>.*'
        new_content2 = re.sub(pattern2, '', content, flags=re.DOTALL)
        if len(new_content2) < original_len:
            r3 = requests.post(f'https://nambei-oyaji.com/wp-json/wp/v2/posts/{pid}', auth=auth, json={'content': new_content2})
            print(f'  -> Alt pattern worked! Removed {original_len - len(new_content2)} chars, status: {r3.status_code}')
        else:
            print(f'  -> Still no match. Manual check needed.')
