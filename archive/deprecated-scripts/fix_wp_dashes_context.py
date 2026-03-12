"""Fix the contextually wrong ： replacements back to proper Japanese punctuation"""
import requests, json, base64, re, sys
sys.stdout.reconfigure(encoding='utf-8')

creds = json.load(open('config/wp-credentials.json', encoding='utf-8'))
auth = base64.b64encode(f"{creds['username']}:{creds['app_password']}".encode()).decode()
headers = {'Authorization': f'Basic {auth}', 'Content-Type': 'application/json'}

# Fix post 1070 - "9万円：みたいなこと" → "9万円、みたいなこと"
fixes = {
    1070: [
        ('9万円</strong>：みたいなことが起きる', '9万円</strong>、みたいなことが起きる'),
    ],
    1069: [
        ('不安……</strong>」：わかる', '不安……</strong>」\n\nわかる'),
        ('に行っている間に集中して片づけて、午後3時に迎えに行く：こういう働き方が',
         'に行っている間に集中して片づけて、午後3時に迎えに行く。こういう働き方が'),
    ],
}

for post_id, replacements in fixes.items():
    r = requests.get(f"{creds['api_base']}/posts/{post_id}", headers=headers,
                     params={'context': 'edit'})
    if r.status_code != 200:
        print(f"Error getting post {post_id}")
        continue
    raw = r.json()['content']['raw']
    title = r.json()['title']['raw']
    new_raw = raw
    changed = 0
    for old, new in replacements:
        if old in new_raw:
            new_raw = new_raw.replace(old, new)
            changed += 1
            print(f"ID:{post_id} ({title})")
            print(f"  '{old[:60]}' -> '{new[:60]}'")

    if changed > 0:
        r2 = requests.post(f"{creds['api_base']}/posts/{post_id}", headers=headers,
                           json={'content': new_raw})
        print(f"  -> {'FIXED' if r2.status_code == 200 else f'ERROR {r2.status_code}'}")

print("\nDone.")
