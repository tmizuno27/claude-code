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
# Block refs string
# ============================================================
block_refs = '\n'.join([f'<!-- wp:block {{"ref":{i}}} /-->' for i in range(932, 955)])

# ============================================================
# New Archive Template - Apple-style category page
# ============================================================
archive_template = '''<!-- wp:template-part {"slug":"header","theme":"twentytwentyfive"} /-->
''' + block_refs + '''

<!-- wp:html -->
<style>
/* Archive page Apple style */
.nao-archive-hero{background:linear-gradient(180deg,#f5f5f7 0%,#fff 100%);padding:80px 22px 60px;text-align:center;}
.nao-archive-hero h1{font-family:var(--sf-pro);font-size:48px;font-weight:700;line-height:1.08;letter-spacing:-.015em;color:#1d1d1f;margin:0 auto 12px;max-width:680px;}
.nao-archive-hero p{font-family:var(--sf-pro);font-size:21px;font-weight:400;line-height:1.38;letter-spacing:.011em;color:#86868b;margin:0 auto;max-width:680px;}
.nao-archive-list{max-width:680px;margin:0 auto;padding:0 22px 80px;}
.nao-archive-item{display:block;padding:32px 0;border-bottom:1px solid #e8e8ed;text-decoration:none;color:inherit;transition:opacity 0.2s ease;}
.nao-archive-item:hover{opacity:0.7;}
.nao-archive-item h2{font-family:var(--sf-pro);font-size:24px;font-weight:700;line-height:1.25;letter-spacing:-.01em;color:#1d1d1f;margin:0 0 8px;}
.nao-archive-item .nao-archive-excerpt{font-family:var(--sf-pro);font-size:15px;line-height:1.6;color:#86868b;margin:0 0 10px;display:-webkit-box;-webkit-line-clamp:2;-webkit-box-orient:vertical;overflow:hidden;}
.nao-archive-item .nao-archive-meta{font-family:var(--sf-pro);font-size:13px;color:#86868b;display:flex;gap:16px;align-items:center;}
.nao-archive-item .nao-archive-meta .nao-cat{color:#0066CC;font-weight:500;}
.nao-archive-item:first-child{padding-top:0;}
.nao-archive-pagination{max-width:680px;margin:0 auto;padding:0 22px 60px;display:flex;justify-content:center;gap:8px;}
.nao-archive-pagination a,.nao-archive-pagination span{display:inline-flex;align-items:center;justify-content:center;min-width:40px;height:40px;border-radius:10px;font-size:15px;font-weight:500;text-decoration:none;color:#1d1d1f;transition:background 0.2s ease;}
.nao-archive-pagination a:hover{background:#f5f5f7;}
.nao-archive-pagination .current{background:#0071e3;color:#fff;border-radius:10px;}
@media(max-width:768px){
.nao-archive-hero{padding:48px 16px 40px;}
.nao-archive-hero h1{font-size:32px;}
.nao-archive-hero p{font-size:17px;}
.nao-archive-list{padding:0 16px 48px;}
.nao-archive-item h2{font-size:20px;}
.nao-archive-item .nao-archive-excerpt{font-size:14px;}
}
</style>
<!-- /wp:html -->

<!-- wp:group {"tagName":"main","style":{"spacing":{"margin":{"top":"0"}}},"layout":{"type":"default"}} -->
<main class="wp-block-group" style="margin-top:0">

<!-- wp:html -->
<div class="nao-archive-hero">
  <h1 id="nao-archive-title"></h1>
  <p id="nao-archive-desc"></p>
</div>
<div class="nao-archive-list" id="nao-archive-list">
</div>
<script>
(function(){
  // Get category info from URL
  var path = window.location.pathname;
  var slug = path.replace(/^\\/category\\//, '').replace(/\\/$/, '');

  var catNames = {
    'paraguay': '\u30d1\u30e9\u30b0\u30a2\u30a4\u751f\u6d3b',
    'side-business': '\u6d77\u5916\u306e\u50cd\u304d\u65b9',
    'ijuu-junbi': '\u79fb\u4f4f\u6e96\u5099',
    'ai': 'AI\u6d3b\u7528',
    'tools': '\u30c4\u30fc\u30eb\u6bd4\u8f03',
    'report': '\u5b9f\u9a13\u30ec\u30dd\u30fc\u30c8'
  };
  var catDescs = {
    'paraguay': '\u30d1\u30e9\u30b0\u30a2\u30a4\u5728\u4f4f\u8005\u304c\u66f8\u304f\u3001\u73fe\u5730\u306e\u30ea\u30a2\u30eb\u306a\u60c5\u5831\u3002',
    'side-business': '\u5357\u7c73\u304b\u3089\u65e5\u672c\u306e\u4ed5\u4e8b\u3092\u30ea\u30e2\u30fc\u30c8\u3067\u3002\u53ce\u5165\u4e8b\u60c5\u3092\u5305\u307f\u96a0\u3055\u305a\u516c\u958b\u3002',
    'ijuu-junbi': '\u79fb\u4f4f\u8cbb\u7528\u3001\u30d3\u30b6\u3001\u6c38\u4f4f\u6a29\u306e\u53d6\u5f97\u3002\u6e96\u5099\u306e\u5168\u5de5\u7a0b\u3092\u89e3\u8aac\u3002'
  };

  var title = catNames[slug] || slug;
  var desc = catDescs[slug] || '';
  document.getElementById('nao-archive-title').textContent = title;
  document.getElementById('nao-archive-desc').textContent = desc;

  // Fetch posts for this category
  fetch('/wp-json/wp/v2/categories?slug=' + slug)
    .then(function(r){ return r.json(); })
    .then(function(cats){
      if(!cats.length) return;
      var catId = cats[0].id;
      // Also update title/desc from API
      if(cats[0].name) document.getElementById('nao-archive-title').textContent = cats[0].name;
      if(cats[0].description) document.getElementById('nao-archive-desc').textContent = cats[0].description;

      return fetch('/wp-json/wp/v2/posts?categories=' + catId + '&per_page=20&_embed&status=publish');
    })
    .then(function(r){ return r.json(); })
    .then(function(posts){
      if(!posts || !posts.length){
        document.getElementById('nao-archive-list').innerHTML = '<p style="text-align:center;color:#86868b;padding:40px 0;">\u8a18\u4e8b\u3092\u6e96\u5099\u4e2d\u3067\u3059\u3002</p>';
        return;
      }
      var html = '';
      posts.forEach(function(p){
        var excerpt = p.excerpt.rendered.replace(/<[^>]+>/g,'').trim();
        if(excerpt.length > 120) excerpt = excerpt.substring(0,120) + '\u2026';
        var date = new Date(p.date);
        var dateStr = date.getFullYear() + '.' + (date.getMonth()+1) + '.' + date.getDate();
        var cat = '';
        var terms = p._embedded && p._embedded['wp:term'] && p._embedded['wp:term'][0];
        if(terms && terms.length) cat = terms[0].name;
        html += '<a href="' + p.link + '" class="nao-archive-item">';
        html += '<h2>' + p.title.rendered + '</h2>';
        if(excerpt) html += '<p class="nao-archive-excerpt">' + excerpt + '</p>';
        html += '<div class="nao-archive-meta">';
        if(cat) html += '<span class="nao-cat">' + cat + '</span>';
        html += '<span>' + dateStr + '</span>';
        html += '</div></a>';
      });
      document.getElementById('nao-archive-list').innerHTML = html;
    })
    .catch(function(e){ console.error(e); });
})();
</script>
<!-- /wp:html -->

</main>
<!-- /wp:group -->

<!-- wp:template-part {"slug":"footer","theme":"twentytwentyfive"} /-->'''

api_call('templates/twentytwentyfive//archive', {'content': archive_template}, 'POST')
print('Updated archive template')

# ============================================================
# Also add Apple-style CSS for other pages (search, 404, general)
# Add to single template's inline CSS blocks
# ============================================================

# Update search template
search_tmpl = api_call('templates/twentytwentyfive//search')
search_content = search_tmpl.get('content', {}).get('raw', '')

search_css = '''<!-- wp:html -->
<style>
.wp-block-search__label{font-family:var(--sf-pro)!important;font-size:48px!important;font-weight:700!important;letter-spacing:-.015em!important;color:#1d1d1f!important;text-align:center!important;display:block!important;margin-bottom:20px!important;}
.wp-block-search__inside-wrapper{max-width:680px!important;margin:0 auto!important;}
.wp-block-search__input{border:1px solid #d2d2d7!important;border-radius:12px!important;padding:14px 18px!important;font-size:17px!important;font-family:var(--sf-pro)!important;transition:border-color 0.3s ease,box-shadow 0.3s ease!important;}
.wp-block-search__input:focus{outline:none!important;border-color:#0071e3!important;box-shadow:0 0 0 3px rgba(0,113,227,0.15)!important;}
.wp-block-search__button{background:#0071e3!important;color:#fff!important;border:none!important;border-radius:12px!important;padding:14px 24px!important;font-size:17px!important;font-weight:600!important;cursor:pointer!important;transition:background 0.3s ease!important;}
.wp-block-search__button:hover{background:#0077ED!important;}
</style>
<!-- /wp:html -->
'''

if 'wp-block-search__label' not in search_content:
    main_marker = '<!-- wp:group {"tagName":"main"'
    if main_marker in search_content:
        parts = search_content.split(main_marker, 1)
        new_search = parts[0] + search_css + main_marker + parts[1]
        api_call('templates/twentytwentyfive//search', {'content': new_search}, 'POST')
        print('Updated search template with Apple CSS')

# Update 404 template
tmpl_404 = api_call('templates/twentytwentyfive//404')
content_404 = tmpl_404.get('content', {}).get('raw', '')

css_404 = '''<!-- wp:html -->
<style>
body.error404 main{text-align:center!important;padding:80px 22px!important;}
body.error404 .wp-block-heading{font-family:var(--sf-pro)!important;font-size:120px!important;font-weight:700!important;color:#d2d2d7!important;letter-spacing:-.03em!important;line-height:1!important;margin-bottom:16px!important;}
body.error404 p{font-family:var(--sf-pro)!important;font-size:21px!important;color:#86868b!important;max-width:480px!important;margin:0 auto 32px!important;}
body.error404 .wp-block-search__label{font-size:17px!important;font-weight:600!important;margin-bottom:12px!important;}
</style>
<!-- /wp:html -->
'''

if 'error404 main' not in content_404:
    main_marker = '<!-- wp:group {"tagName":"main"'
    if main_marker in content_404:
        parts = content_404.split(main_marker, 1)
        new_404 = parts[0] + css_404 + main_marker + parts[1]
        api_call('templates/twentytwentyfive//404', {'content': new_404}, 'POST')
        print('Updated 404 template with Apple CSS')

# ============================================================
# Also add general page typography CSS (for archive, category titles etc)
# This goes into single template CSS but targets all pages
# ============================================================

# Add CSS to single template for archive/category/general page titles
single_tmpl = api_call('templates/twentytwentyfive//single')
single_content = single_tmpl.get('content', {}).get('raw', '')

general_page_css = '''<!-- wp:html -->
<style>
/* General page title styling */
.wp-block-query-title{font-family:var(--sf-pro)!important;font-size:48px!important;font-weight:700!important;line-height:1.08!important;letter-spacing:-.015em!important;color:#1d1d1f!important;max-width:680px!important;margin:0 auto!important;padding:0 22px!important;}
.wp-block-term-description{font-family:var(--sf-pro)!important;font-size:21px!important;color:#86868b!important;max-width:680px!important;margin:8px auto 0!important;padding:0 22px!important;line-height:1.38!important;}
.wp-block-term-description p{color:#86868b!important;font-size:21px!important;}
/* Post list in archive */
.wp-block-post-template .wp-block-post-title{font-family:var(--sf-pro)!important;font-size:24px!important;font-weight:700!important;letter-spacing:-.01em!important;}
.wp-block-post-template .wp-block-post-title a{color:#1d1d1f!important;text-decoration:none!important;}
.wp-block-post-template .wp-block-post-title a:hover{color:#0066CC!important;}
.wp-block-post-template .wp-block-post-date{font-size:13px!important;color:#86868b!important;}
.wp-block-post-template .wp-block-post-date a{color:#86868b!important;text-decoration:none!important;}
/* Pagination */
.wp-block-query-pagination{font-family:var(--sf-pro)!important;gap:8px!important;}
.wp-block-query-pagination a,.wp-block-query-pagination span{font-size:15px!important;color:#1d1d1f!important;text-decoration:none!important;padding:8px 14px!important;border-radius:10px!important;transition:background 0.2s ease!important;}
.wp-block-query-pagination a:hover{background:#f5f5f7!important;}
.wp-block-query-pagination .current{background:#0071e3!important;color:#fff!important;}
/* Main spacing fix for non-single pages */
body:not(.single) main.wp-block-group{margin-top:0!important;}
body:not(.single) main.wp-block-group>.wp-block-group:first-child{padding-top:60px!important;}
</style>
<!-- /wp:html -->
'''

# Insert this CSS into all templates that have block refs
for tmpl_slug in ['single', 'page', 'index', 'home', 'archive', 'search', '404', 'page-no-title']:
    try:
        tmpl = api_call(f'templates/twentytwentyfive//{tmpl_slug}')
        content = tmpl.get('content', {}).get('raw', '')
        if 'wp-block-query-title' in content:
            continue  # Already has the CSS
        main_marker = '<!-- wp:group {"tagName":"main"'
        if main_marker in content:
            parts = content.split(main_marker, 1)
            new_content = parts[0] + general_page_css + main_marker + parts[1]
            api_call(f'templates/twentytwentyfive//{tmpl_slug}', {'content': new_content}, 'POST')
            print(f'Added general page CSS to {tmpl_slug}')
    except Exception as e:
        print(f'Error for {tmpl_slug}: {e}')

print('\nAll done!')
