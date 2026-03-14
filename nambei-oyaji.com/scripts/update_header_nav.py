"""Add お問い合わせ link to header nav widget"""
import requests
import json
import base64
import sys
sys.stdout.reconfigure(encoding='utf-8')

with open('config/wp-credentials.json', encoding='utf-8') as f:
    creds = json.load(f)

auth = base64.b64encode(f"{creds['username']}:{creds['app_password']}".encode()).decode()
headers = {
    'Authorization': f'Basic {auth}',
    'Content-Type': 'application/json'
}

# Get current widget
r = requests.get(f"{creds['api_base']}/widgets/custom_html-2", headers=headers)
w = r.json()
rendered = w['rendered']

# Extract the content between <div class="textwidget custom-html-widget"> and </div></aside>
start_marker = '<div class="textwidget custom-html-widget">'
end_marker = '</div></aside>'
start = rendered.find(start_marker) + len(start_marker)
end = rendered.find(end_marker)
content = rendered[start:end]

# Add お問い合わせ link after プロフィール
old_nav = '<a href="/about/">プロフィール</a></nav>'
new_nav = '<a href="/about/">プロフィール</a><a href="/contact/">お問い合わせ</a></nav>'
content = content.replace(old_nav, new_nav)

# Update widget
update_data = {
    'instance': {
        'raw': {
            'content': content
        }
    }
}

r2 = requests.put(
    f"{creds['api_base']}/widgets/custom_html-2",
    headers=headers,
    json=update_data
)
print(f"Status: {r2.status_code}")
if r2.status_code != 200:
    print(r2.text[:500])
else:
    print("OK: お問い合わせ link added to header nav")
