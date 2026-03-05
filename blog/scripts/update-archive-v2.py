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
# Step 1: Archive Template - WordPress native blocks (no JS)
# ============================================================
archive_template = '''<!-- wp:template-part {"slug":"header","theme":"twentytwentyfive"} /-->
''' + block_refs + '''

<!-- wp:group {"tagName":"main","style":{"spacing":{"margin":{"top":"0"}}},"layout":{"type":"default"}} -->
<main class="wp-block-group" style="margin-top:0">

<!-- wp:group {"className":"nao-archive-hero","style":{"spacing":{"padding":{"top":"80px","bottom":"60px","left":"22px","right":"22px"}}},"layout":{"type":"constrained","contentSize":"680px"}} -->
<div class="wp-block-group nao-archive-hero" style="padding-top:80px;padding-bottom:60px;padding-left:22px;padding-right:22px">
<!-- wp:query-title {"type":"archive","textAlign":"center","style":{"typography":{"fontSize":"48px","fontWeight":"700","lineHeight":"1.08","letterSpacing":"-0.015em"},"elements":{"link":{"color":{"text":"#1d1d1f"}}},"color":{"text":"#1d1d1f"}}} /-->
<!-- wp:term-description {"textAlign":"center","style":{"typography":{"fontSize":"21px","lineHeight":"1.38","letterSpacing":"0.011em"},"color":{"text":"#86868b"}}} /-->
</div>
<!-- /wp:group -->

<!-- wp:query {"queryId":1,"query":{"perPage":20,"pages":0,"offset":0,"postType":"post","order":"desc","orderBy":"date","inherit":true},"layout":{"type":"constrained","contentSize":"680px"}} -->
<div class="wp-block-query">
<!-- wp:post-template {"className":"nao-post-list","style":{"spacing":{"blockGap":"0"}}} -->

<!-- wp:group {"className":"nao-archive-item","style":{"spacing":{"padding":{"top":"32px","bottom":"32px"}},"border":{"bottom":{"color":"#e8e8ed","width":"1px"}}},"layout":{"type":"default"}} -->
<div class="wp-block-group nao-archive-item" style="border-bottom-color:#e8e8ed;border-bottom-width:1px;padding-top:32px;padding-bottom:32px">
<!-- wp:post-title {"isLink":true,"style":{"typography":{"fontSize":"24px","fontWeight":"700","lineHeight":"1.25","letterSpacing":"-0.01em"},"elements":{"link":{"color":{"text":"#1d1d1f"},":hover":{"color":{"text":"#0066CC"}}}},"color":{"text":"#1d1d1f"},"spacing":{"margin":{"bottom":"8px"}}}} /-->
<!-- wp:post-excerpt {"moreText":"","excerptLength":80,"style":{"typography":{"fontSize":"15px","lineHeight":"1.6"},"color":{"text":"#86868b"},"spacing":{"margin":{"bottom":"10px"}}}} /-->
<!-- wp:group {"className":"nao-archive-meta","style":{"spacing":{"blockGap":"16px"}},"layout":{"type":"flex","flexWrap":"nowrap"}} -->
<div class="wp-block-group nao-archive-meta">
<!-- wp:post-terms {"term":"category","style":{"typography":{"fontSize":"13px","fontWeight":"500"},"elements":{"link":{"color":{"text":"#0066CC"}}}}} /-->
<!-- wp:post-date {"style":{"typography":{"fontSize":"13px"},"color":{"text":"#86868b"}}} /-->
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
    print('Updated archive template')
except Exception as e:
    print(f'Error updating archive: {e}')

print('\nDone!')
