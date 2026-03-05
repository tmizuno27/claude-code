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

block_refs = '\n'.join([f'<!-- wp:block {{"ref":{i}}} /-->' for i in range(932, 955)])

# ============================================================
# Archive CSS (with image support)
# ============================================================
archive_css = '<!-- wp:html -->\n<style>\n'
archive_css += '.nao-archive-hero{background:linear-gradient(180deg,#f5f5f7 0%,#fff 100%)!important;text-align:center!important;}\n'
archive_css += '.nao-archive-hero .wp-block-query-title{font-size:48px!important;font-weight:700!important;line-height:1.08!important;letter-spacing:-.015em!important;color:#1d1d1f!important;}\n'
archive_css += '.nao-archive-hero .wp-block-term-description{font-size:21px!important;line-height:1.38!important;color:#86868b!important;}\n'
archive_css += '.nao-archive-hero .wp-block-term-description p{color:#86868b!important;font-size:21px!important;}\n'
archive_css += '.nao-archive-item{transition:opacity 0.2s ease!important;display:flex!important;gap:24px!important;align-items:flex-start!important;}\n'
archive_css += '.nao-archive-item:hover{opacity:0.7!important;}\n'
archive_css += '.nao-archive-item .wp-block-post-featured-image{flex-shrink:0!important;width:160px!important;border-radius:12px!important;overflow:hidden!important;}\n'
archive_css += '.nao-archive-item .wp-block-post-featured-image img{width:160px!important;height:100px!important;object-fit:cover!important;border-radius:12px!important;}\n'
archive_css += '.nao-archive-item .wp-block-post-title a{text-decoration:none!important;color:#1d1d1f!important;}\n'
archive_css += '.nao-archive-item .wp-block-post-title a:hover{color:#0066CC!important;}\n'
archive_css += '.nao-archive-item .wp-block-post-excerpt{display:-webkit-box!important;-webkit-line-clamp:2!important;-webkit-box-orient:vertical!important;overflow:hidden!important;}\n'
archive_css += '.wp-block-query-pagination{gap:8px!important;margin-top:40px!important;}\n'
archive_css += '.wp-block-query-pagination a,.wp-block-query-pagination span{display:inline-flex!important;align-items:center!important;justify-content:center!important;min-width:40px!important;height:40px!important;border-radius:10px!important;font-size:15px!important;font-weight:500!important;text-decoration:none!important;color:#1d1d1f!important;transition:background 0.2s ease!important;}\n'
archive_css += '.wp-block-query-pagination a:hover{background:#f5f5f7!important;}\n'
archive_css += '.wp-block-query-pagination .current{background:#0071e3!important;color:#fff!important;}\n'
archive_css += '.nao-post-list{list-style:none!important;padding:0!important;}\n'
archive_css += '@media(max-width:768px){\n'
archive_css += '.nao-archive-item{flex-direction:column!important;gap:12px!important;}\n'
archive_css += '.nao-archive-item .wp-block-post-featured-image{width:100%!important;}\n'
archive_css += '.nao-archive-item .wp-block-post-featured-image img{width:100%!important;height:180px!important;}\n'
archive_css += '.nao-archive-hero .wp-block-query-title{font-size:32px!important;}\n'
archive_css += '.nao-archive-hero .wp-block-term-description{font-size:17px!important;}\n'
archive_css += '.nao-archive-item .wp-block-post-title{font-size:20px!important;}\n'
archive_css += '}\n'
archive_css += '</style>\n<!-- /wp:html -->'

# ============================================================
# General page CSS
# ============================================================
general_css = '<!-- wp:html -->\n<style>\n'
general_css += '.wp-block-query-title{font-size:48px!important;font-weight:700!important;line-height:1.08!important;letter-spacing:-.015em!important;color:#1d1d1f!important;}\n'
general_css += '.wp-block-term-description{font-size:21px!important;color:#86868b!important;line-height:1.38!important;}\n'
general_css += '.wp-block-term-description p{color:#86868b!important;font-size:21px!important;}\n'
general_css += '.wp-block-post-template .wp-block-post-title a{color:#1d1d1f!important;text-decoration:none!important;}\n'
general_css += '.wp-block-post-template .wp-block-post-title a:hover{color:#0066CC!important;}\n'
general_css += '.wp-block-post-template .wp-block-post-date{font-size:13px!important;color:#86868b!important;}\n'
general_css += 'body:not(.single) main.wp-block-group{margin-top:0!important;}\n'
general_css += '</style>\n<!-- /wp:html -->'

# ============================================================
# Updated Archive Template with featured image
# ============================================================
archive_template = '<!-- wp:template-part {"slug":"header","theme":"twentytwentyfive"} /-->\n'
archive_template += block_refs + '\n\n'
archive_template += archive_css + '\n'
archive_template += general_css + '\n\n'

archive_template += '''<!-- wp:group {"tagName":"main","style":{"spacing":{"margin":{"top":"0"}}},"layout":{"type":"default"}} -->
<main class="wp-block-group" style="margin-top:0">

<!-- wp:group {"className":"nao-archive-hero","style":{"spacing":{"padding":{"top":"80px","bottom":"60px","left":"22px","right":"22px"}}},"layout":{"type":"constrained","contentSize":"680px"}} -->
<div class="wp-block-group nao-archive-hero" style="padding-top:80px;padding-bottom:60px;padding-left:22px;padding-right:22px">
<!-- wp:query-title {"type":"archive","textAlign":"center","style":{"typography":{"fontSize":"48px","fontWeight":"700"}}} /-->
<!-- wp:term-description {"textAlign":"center"} /-->
</div>
<!-- /wp:group -->

<!-- wp:query {"queryId":1,"query":{"perPage":20,"pages":0,"offset":0,"postType":"post","order":"desc","orderBy":"date","inherit":true},"layout":{"type":"constrained","contentSize":"780px"}} -->
<div class="wp-block-query">
<!-- wp:post-template {"className":"nao-post-list","style":{"spacing":{"blockGap":"0"}}} -->

<!-- wp:group {"className":"nao-archive-item","style":{"spacing":{"padding":{"top":"32px","bottom":"32px"}},"border":{"bottom":{"color":"#e8e8ed","width":"1px"}}},"layout":{"type":"flex","flexWrap":"nowrap","verticalAlignment":"top"}} -->
<div class="wp-block-group nao-archive-item" style="border-bottom-color:#e8e8ed;border-bottom-width:1px;padding-top:32px;padding-bottom:32px">

<!-- wp:post-featured-image {"isLink":true,"width":"160px","height":"100px","style":{"border":{"radius":"12px"}}} /-->

<!-- wp:group {"layout":{"type":"default"},"style":{"layout":{"selfStretch":"fill","flexSize":null}}} -->
<div class="wp-block-group">
<!-- wp:post-title {"isLink":true,"style":{"typography":{"fontSize":"24px","fontWeight":"700","lineHeight":"1.25","letterSpacing":"-0.01em"},"spacing":{"margin":{"bottom":"8px"}}}} /-->
<!-- wp:post-excerpt {"moreText":"","excerptLength":80,"style":{"typography":{"fontSize":"15px","lineHeight":"1.6"},"color":{"text":"#86868b"},"spacing":{"margin":{"bottom":"10px"}}}} /-->
<!-- wp:group {"className":"nao-archive-meta","style":{"spacing":{"blockGap":"16px"}},"layout":{"type":"flex","flexWrap":"nowrap"}} -->
<div class="wp-block-group nao-archive-meta">
<!-- wp:post-terms {"term":"category","style":{"typography":{"fontSize":"13px","fontWeight":"500"},"elements":{"link":{"color":{"text":"#0066CC"}}}}} /-->
<!-- wp:post-date {"style":{"typography":{"fontSize":"13px"},"color":{"text":"#86868b"}}} /-->
</div>
<!-- /wp:group -->
</div>
<!-- /wp:group -->

</div>
<!-- /wp:group -->

<!-- /wp:post-template -->

<!-- wp:query-pagination {"paginationArrow":"arrow","layout":{"type":"flex","justifyContent":"center"}} -->
<!-- wp:query-pagination-previous /-->
<!-- wp:query-pagination-numbers /-->
<!-- wp:query-pagination-next /-->
<!-- /wp:query-pagination -->
</div>
<!-- /wp:query -->

</main>
<!-- /wp:group -->

<!-- wp:template-part {"slug":"footer","theme":"twentytwentyfive"} /-->'''

try:
    api_call('templates/twentytwentyfive//archive', {'content': archive_template}, 'POST')
    print('Updated archive template with featured images')
except Exception as e:
    print(f'Error: {e}')

print('\nDone!')
