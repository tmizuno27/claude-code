import json, urllib.request, base64, sys
sys.stdout.reconfigure(encoding='utf-8')
creds = base64.b64encode(b't.mizuno27@gmail.com:WutS MaRq ukGx OcQ8 uhBj Ej0D').decode()

def api_call(endpoint, data=None, method='GET'):
    url = 'https://nambei-oyaji.com/wp-json/wp/v2/' + endpoint
    if data:
        payload = json.dumps(data).encode('utf-8')
        req = urllib.request.Request(url, data=payload,
            headers={'Content-Type': 'application/json', 'Authorization': 'Basic ' + creds},
            method=method or 'POST')
    else:
        req = urllib.request.Request(url, headers={'Authorization': 'Basic ' + creds})
    resp = urllib.request.urlopen(req)
    return json.loads(resp.read().decode('utf-8'))

# ============================================================
# Archive page CSS
# ============================================================
archive_css = '<!-- wp:html -->\n<style>\n'
archive_css += '.nao-archive-hero{background:linear-gradient(180deg,#f5f5f7 0%,#fff 100%)!important;text-align:center!important;}\n'
archive_css += '.nao-archive-hero .wp-block-query-title{font-size:48px!important;font-weight:700!important;line-height:1.08!important;letter-spacing:-.015em!important;color:#1d1d1f!important;}\n'
archive_css += '.nao-archive-hero .wp-block-term-description{font-size:21px!important;line-height:1.38!important;letter-spacing:.011em!important;color:#86868b!important;}\n'
archive_css += '.nao-archive-hero .wp-block-term-description p{color:#86868b!important;font-size:21px!important;}\n'
archive_css += '.nao-archive-item{transition:opacity 0.2s ease!important;}\n'
archive_css += '.nao-archive-item:hover{opacity:0.7!important;}\n'
archive_css += '.nao-archive-item .wp-block-post-title a{text-decoration:none!important;}\n'
archive_css += '.nao-archive-item .wp-block-post-title a:hover{color:#0066CC!important;}\n'
archive_css += '.nao-archive-item .wp-block-post-excerpt{display:-webkit-box!important;-webkit-line-clamp:2!important;-webkit-box-orient:vertical!important;overflow:hidden!important;}\n'
archive_css += '.wp-block-query-pagination{gap:8px!important;margin-top:40px!important;}\n'
archive_css += '.wp-block-query-pagination a,.wp-block-query-pagination span{display:inline-flex!important;align-items:center!important;justify-content:center!important;min-width:40px!important;height:40px!important;border-radius:10px!important;font-size:15px!important;font-weight:500!important;text-decoration:none!important;color:#1d1d1f!important;transition:background 0.2s ease!important;}\n'
archive_css += '.wp-block-query-pagination a:hover{background:#f5f5f7!important;}\n'
archive_css += '.wp-block-query-pagination .current{background:#0071e3!important;color:#fff!important;}\n'
archive_css += '.nao-post-list{list-style:none!important;padding:0!important;}\n'
archive_css += '</style>\n<!-- /wp:html -->'

# ============================================================
# Search page CSS
# ============================================================
search_css = '<!-- wp:html -->\n<style>\n'
search_css += '.wp-block-search__label{font-size:48px!important;font-weight:700!important;letter-spacing:-.015em!important;color:#1d1d1f!important;text-align:center!important;display:block!important;margin-bottom:20px!important;}\n'
search_css += '.wp-block-search__inside-wrapper{max-width:680px!important;margin:0 auto!important;}\n'
search_css += '.wp-block-search__input{border:1px solid #d2d2d7!important;border-radius:12px!important;padding:14px 18px!important;font-size:17px!important;transition:border-color 0.3s ease,box-shadow 0.3s ease!important;}\n'
search_css += '.wp-block-search__input:focus{outline:none!important;border-color:#0071e3!important;box-shadow:0 0 0 3px rgba(0,113,227,0.15)!important;}\n'
search_css += '.wp-block-search__button{background:#0071e3!important;color:#fff!important;border:none!important;border-radius:12px!important;padding:14px 24px!important;font-size:17px!important;font-weight:600!important;cursor:pointer!important;transition:background 0.3s ease!important;}\n'
search_css += '.wp-block-search__button:hover{background:#0077ED!important;}\n'
search_css += '</style>\n<!-- /wp:html -->'

# ============================================================
# 404 page CSS
# ============================================================
css_404 = '<!-- wp:html -->\n<style>\n'
css_404 += 'body.error404 main{text-align:center!important;padding:80px 22px!important;}\n'
css_404 += 'body.error404 .wp-block-heading{font-size:120px!important;font-weight:700!important;color:#d2d2d7!important;letter-spacing:-.03em!important;line-height:1!important;margin-bottom:16px!important;}\n'
css_404 += 'body.error404 p{font-size:21px!important;color:#86868b!important;max-width:480px!important;margin:0 auto 32px!important;}\n'
css_404 += 'body.error404 .wp-block-search__label{font-size:17px!important;font-weight:600!important;margin-bottom:12px!important;}\n'
css_404 += '</style>\n<!-- /wp:html -->'

# ============================================================
# General page typography
# ============================================================
general_css = '<!-- wp:html -->\n<style>\n'
general_css += '.wp-block-query-title{font-size:48px!important;font-weight:700!important;line-height:1.08!important;letter-spacing:-.015em!important;color:#1d1d1f!important;}\n'
general_css += '.wp-block-term-description{font-size:21px!important;color:#86868b!important;line-height:1.38!important;}\n'
general_css += '.wp-block-term-description p{color:#86868b!important;font-size:21px!important;}\n'
general_css += '.wp-block-post-template .wp-block-post-title a{color:#1d1d1f!important;text-decoration:none!important;}\n'
general_css += '.wp-block-post-template .wp-block-post-title a:hover{color:#0066CC!important;}\n'
general_css += '.wp-block-post-template .wp-block-post-date{font-size:13px!important;color:#86868b!important;}\n'
general_css += '.wp-block-post-template .wp-block-post-date a{color:#86868b!important;text-decoration:none!important;}\n'
general_css += 'body:not(.single) main.wp-block-group{margin-top:0!important;}\n'
general_css += '@media(max-width:768px){\n'
general_css += '.nao-archive-hero .wp-block-query-title,.wp-block-query-title{font-size:32px!important;}\n'
general_css += '.nao-archive-hero .wp-block-term-description,.wp-block-term-description{font-size:17px!important;}\n'
general_css += '.nao-archive-item .wp-block-post-title{font-size:20px!important;}\n'
general_css += '.wp-block-search__label{font-size:32px!important;}\n'
general_css += 'body.error404 .wp-block-heading{font-size:80px!important;}\n'
general_css += '}\n'
general_css += '</style>\n<!-- /wp:html -->'

# ============================================================
# Update search template
# ============================================================
print('=== Updating search template ===')
try:
    search_tmpl = api_call('templates/twentytwentyfive//search')
    search_content = search_tmpl.get('content', {}).get('raw', '')
    if 'wp-block-search__label' not in search_content:
        main_marker = '<!-- wp:group {"tagName":"main"'
        if main_marker in search_content:
            parts = search_content.split(main_marker, 1)
            new_search = parts[0] + search_css + '\n' + main_marker + parts[1]
            api_call('templates/twentytwentyfive//search', {'content': new_search}, 'POST')
            print('Added search CSS')
        else:
            print('No main marker found')
    else:
        print('Search CSS already present')
except Exception as e:
    print(f'Error: {e}')

# ============================================================
# Update 404 template
# ============================================================
print('\n=== Updating 404 template ===')
try:
    tmpl_404 = api_call('templates/twentytwentyfive//404')
    content_404 = tmpl_404.get('content', {}).get('raw', '')
    if 'error404 main' not in content_404:
        main_marker = '<!-- wp:group {"tagName":"main"'
        if main_marker in content_404:
            parts = content_404.split(main_marker, 1)
            new_404 = parts[0] + css_404 + '\n' + main_marker + parts[1]
            api_call('templates/twentytwentyfive//404', {'content': new_404}, 'POST')
            print('Added 404 CSS')
        else:
            print('No main marker found')
    else:
        print('404 CSS already present')
except Exception as e:
    print(f'Error: {e}')

# ============================================================
# Add general + archive CSS to ALL templates
# ============================================================
print('\n=== Adding general + archive CSS to all templates ===')
for tmpl_slug in ['single', 'page', 'index', 'home', 'archive', 'search', '404', 'page-no-title']:
    try:
        tmpl = api_call(f'templates/twentytwentyfive//{tmpl_slug}')
        content = tmpl.get('content', {}).get('raw', '')
        main_marker = '<!-- wp:group {"tagName":"main"'
        if main_marker not in content:
            print(f'SKIP {tmpl_slug}: no main marker')
            continue

        css_to_add = ''
        if 'nao-archive-hero{' not in content:
            css_to_add += archive_css + '\n'
        if 'wp-block-query-title{font-size' not in content:
            css_to_add += general_css + '\n'

        if css_to_add:
            parts = content.split(main_marker, 1)
            new_content = parts[0] + css_to_add + main_marker + parts[1]
            api_call(f'templates/twentytwentyfive//{tmpl_slug}', {'content': new_content}, 'POST')
            print(f'Updated {tmpl_slug}')
        else:
            print(f'SKIP {tmpl_slug}: CSS already present')
    except Exception as e:
        print(f'Error {tmpl_slug}: {e}')

print('\nAll done!')
