import json, urllib.request, base64, sys
sys.stdout.reconfigure(encoding='utf-8')
creds = base64.b64encode(b't.mizuno27@gmail.com:WutS MaRq ukGx OcQ8 uhBj Ej0D').decode()

# Get current page template
req = urllib.request.Request(
    'https://nambei-oyaji.com/wp-json/wp/v2/templates/twentytwentyfive//page',
    headers={'Authorization': 'Basic ' + creds}
)
resp = urllib.request.urlopen(req)
data = json.loads(resp.read().decode('utf-8'))
current = data.get('content', {}).get('raw', '')
print("Current page template:")
print(current[:300])

if 'ref":932' in current:
    print("Blocks already referenced")
else:
    # Add block references after header
    block_refs = '\n'.join([f'<!-- wp:block {{"ref":{i}}} /-->' for i in range(932, 955)])

    new_content = current.replace(
        '<!-- wp:template-part {"slug":"header","theme":"twentytwentyfive"} /-->',
        '<!-- wp:template-part {"slug":"header","theme":"twentytwentyfive"} /-->\n' + block_refs
    )

    payload = json.dumps({'content': new_content}).encode('utf-8')
    req = urllib.request.Request(
        'https://nambei-oyaji.com/wp-json/wp/v2/templates/twentytwentyfive//page',
        data=payload,
        headers={'Content-Type': 'application/json', 'Authorization': 'Basic ' + creds},
        method='POST'
    )
    resp = urllib.request.urlopen(req)
    data = json.loads(resp.read().decode('utf-8'))
    print(f'Updated page template: {data.get("modified", "")}')

# Also update index and home templates
for tmpl in ['index', 'home']:
    req = urllib.request.Request(
        f'https://nambei-oyaji.com/wp-json/wp/v2/templates/twentytwentyfive//{tmpl}',
        headers={'Authorization': 'Basic ' + creds}
    )
    try:
        resp = urllib.request.urlopen(req)
        data = json.loads(resp.read().decode('utf-8'))
        current = data.get('content', {}).get('raw', '')
        if 'ref":932' not in current and '<!-- wp:template-part {"slug":"header"' in current:
            block_refs = '\n'.join([f'<!-- wp:block {{"ref":{i}}} /-->' for i in range(932, 955)])
            new_content = current.replace(
                '<!-- wp:template-part {"slug":"header","theme":"twentytwentyfive"} /-->',
                '<!-- wp:template-part {"slug":"header","theme":"twentytwentyfive"} /-->\n' + block_refs
            )
            payload = json.dumps({'content': new_content}).encode('utf-8')
            req2 = urllib.request.Request(
                f'https://nambei-oyaji.com/wp-json/wp/v2/templates/twentytwentyfive//{tmpl}',
                data=payload,
                headers={'Content-Type': 'application/json', 'Authorization': 'Basic ' + creds},
                method='POST'
            )
            resp2 = urllib.request.urlopen(req2)
            data2 = json.loads(resp2.read().decode('utf-8'))
            print(f'Updated {tmpl} template: {data2.get("modified", "")}')
        else:
            print(f'{tmpl} template: already has blocks or no header')
    except Exception as e:
        print(f'{tmpl}: {e}')
