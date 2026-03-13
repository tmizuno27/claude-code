import requests, json, re

creds = json.load(open('c:/Users/tmizu/マイドライブ/GitHub/claude-code/blog/config/secrets.json'))
wp = creds['wordpress']
auth = (wp['username'], wp['app_password'])

# ===== WIDGET 1: content-top (custom_html-2) =====
css2 = """<style>
/* Header Override */
.header-container-in.hlt-center-logo{display:block!important}
#header{background:rgba(255,255,255,0.92)!important;backdrop-filter:saturate(180%) blur(20px)!important;-webkit-backdrop-filter:saturate(180%) blur(20px)!important;border-bottom:1px solid rgba(0,0,0,0.08)!important;position:sticky!important;top:0!important;z-index:9999!important;padding:0!important;margin:0!important;min-height:auto!important;height:auto!important}
.header-in.wrap.cf{max-width:1200px!important;margin:0 auto!important;padding:14px 40px!important;display:flex!important;flex-direction:row!important;flex-wrap:nowrap!important;align-items:center!important;justify-content:space-between!important;text-align:left!important}
.header-in .logo-header{margin:0!important;padding:0!important;float:none!important;text-align:left!important;width:auto!important}
.header-in .tagline{display:none!important}
#navi{display:none!important}
.tagline{display:none!important}
.nambei-logo{display:flex!important;align-items:center!important;gap:8px!important;text-decoration:none!important}
.nambei-nav{display:flex!important;gap:32px!important;align-items:center!important;float:none!important;margin:0!important}
.nambei-nav a{color:#1d1d1f!important;text-decoration:none!important;font-size:14px!important;font-weight:400!important;font-family:-apple-system,BlinkMacSystemFont,"Hiragino Kaku Gothic ProN",sans-serif!important;transition:color 0.2s!important}
.nambei-nav a:hover{color:#06c!important}

/* Archive: force 2-column with sidebar */
.archive #content-in{display:flex!important;flex-wrap:nowrap!important;gap:40px!important}
.archive #content-in .main{flex:1!important;min-width:0!important}
.archive #content-in #sidebar{display:block!important;width:336px!important;min-width:336px!important;flex-shrink:0!important}

/* Category page list styles */
.archive .entry-card-snippet{font-family:-apple-system,BlinkMacSystemFont,"Hiragino Kaku Gothic ProN",sans-serif!important;font-size:14px!important;color:#666!important;line-height:1.8!important}
.archive .entry-card-title{font-family:-apple-system,BlinkMacSystemFont,"Hiragino Kaku Gothic ProN",sans-serif!important;font-weight:600!important;color:#1d1d1f!important}
.archive .cat-label{font-size:11px!important;padding:2px 8px!important}
.archive .list-title{font-family:-apple-system,BlinkMacSystemFont,"Hiragino Kaku Gothic ProN",sans-serif!important;font-weight:700!important;color:#1d1d1f!important;font-size:24px!important;border:none!important;padding:0!important;margin:0 0 24px!important}
.archive .list-title .fa{display:none!important}

/* Global sidebar card styling (all pages) */
.nambei-sidebar-section{background:#fff!important;border:1px solid #e5e5e7!important;border-radius:16px!important;padding:24px!important;margin-bottom:20px!important;font-family:-apple-system,BlinkMacSystemFont,"Hiragino Kaku Gothic ProN",sans-serif!important}
.nambei-sidebar-title{font-size:15px!important;font-weight:700!important;color:#1d1d1f!important;margin:0 0 16px!important;padding:0 0 12px!important;border-bottom:1px solid #e5e5e7!important}
.nambei-sidebar-list{list-style:none!important;margin:0!important;padding:0!important}
.nambei-sidebar-list li{padding:8px 0!important;border-bottom:1px solid #f5f5f7!important}
.nambei-sidebar-list li:last-child{border-bottom:none!important}
.nambei-sidebar-list a{color:#1d1d1f!important;text-decoration:none!important;font-size:14px!important;line-height:1.6!important;display:block!important}
.nambei-sidebar-list a:hover{color:#06c!important}
.nambei-author-card{text-align:center!important}
.nambei-author-card img{width:80px!important;height:80px!important;border-radius:50%!important;margin-bottom:12px!important}
.nambei-author-card .name{font-weight:700!important;font-size:16px!important;color:#1d1d1f!important;margin-bottom:8px!important}
.nambei-author-card .desc{font-size:13px!important;color:#86868b!important;line-height:1.6!important}
.nambei-sidebar-search{display:flex!important;gap:0!important;border:1px solid #e5e5e7!important;border-radius:8px!important;overflow:hidden!important}
.nambei-sidebar-search input{flex:1!important;border:none!important;padding:8px 12px!important;font-size:14px!important;outline:none!important;font-family:-apple-system,BlinkMacSystemFont,"Hiragino Kaku Gothic ProN",sans-serif!important}
.nambei-sidebar-search button{border:none!important;background:#1d1d1f!important;color:#fff!important;padding:8px 14px!important;cursor:pointer!important;font-size:14px!important}
.nambei-sidebar-toc{position:sticky!important;top:80px!important}
.nambei-sidebar-toc ol{list-style:none!important;margin:0!important;padding:0!important}
.nambei-sidebar-toc li{padding:6px 0!important;border-bottom:1px solid #f5f5f7!important}
.nambei-sidebar-toc li:last-child{border-bottom:none!important}
.nambei-sidebar-toc a{color:#86868b!important;text-decoration:none!important;font-size:13px!important;line-height:1.5!important;display:block!important;transition:color 0.2s!important}
.nambei-sidebar-toc a:hover,.nambei-sidebar-toc a.nambei-toc-active{color:#1d1d1f!important;font-weight:600!important}
.nambei-sidebar-toc .nambei-toc-h3{padding-left:16px!important}
.nambei-sidebar-toc .nambei-toc-sub{list-style:none!important;margin:0!important;padding:0!important}

@media(max-width:834px){
.archive #content-in{flex-direction:column!important}
.archive #content-in #sidebar{width:100%!important;min-width:auto!important}
}

/* Page title override */
.entry-title,.article h1{font-family:-apple-system,BlinkMacSystemFont,"Hiragino Kaku Gothic ProN","Hiragino Sans",Meiryo,sans-serif!important;font-size:32px!important;font-weight:700!important;color:#1d1d1f!important;border:none!important;background:none!important;padding:0!important}

/* Footer override */
#footer{background:#1d1d1f!important;color:#86868b!important;font-family:-apple-system,BlinkMacSystemFont,"Hiragino Kaku Gothic ProN",sans-serif!important}
#footer a{color:#d2d2d7!important}
.footer-bottom{background:#1d1d1f!important;border-top:1px solid #333!important}
.copyright{color:#86868b!important;font-size:13px!important}
</style>"""

# Build JS for widget 2 (header + archive sidebar)
js2_lines = [
    '<script>',
    'document.addEventListener("DOMContentLoaded",function(){',
    'var h=document.getElementById("header-in");',
    'if(h){',
    'h.innerHTML=\'<a href="https://nambei-oyaji.com/" class="nambei-logo"><img src="https://nambei-oyaji.com/wp-content/uploads/2026/03/logo-black-1.png" style="height:28px;width:auto"><img src="https://nambei-oyaji.com/wp-content/uploads/2026/03/nambei-oyaji-grey.png" style="height:27px;width:auto"></a><nav class="nambei-nav"><a href="https://nambei-oyaji.com/category/paraguay/">\u30d1\u30e9\u30b0\u30a2\u30a4\u751f\u6d3b</a><a href="https://nambei-oyaji.com/category/side-business/">\u6d77\u5916\u304b\u3089\u306e\u7a3c\u304e\u65b9</a><a href="https://nambei-oyaji.com/category/ijuu-junbi/">\u304a\u91d1\u3068\u624b\u7d9a\u304d</a><a href="https://nambei-oyaji.com/about/">\u30d7\u30ed\u30d5\u30a3\u30fc\u30eb</a></nav>\';',
    '}',
    'if(document.body.classList.contains("archive")){',
    'var ci=document.getElementById("content-in");',
    'if(ci){ci.style.cssText="display:flex!important;flex-wrap:nowrap!important;gap:40px!important";}',
    'var mn=ci?ci.querySelector(".main"):null;',
    'if(mn){mn.style.cssText="flex:1!important;min-width:0!important";}',
    'var sb=document.getElementById("sidebar");',
    'if(sb){',
    'sb.style.cssText="display:block!important;width:336px!important;min-width:336px!important;flex-shrink:0!important";',
    'sb.innerHTML=\'<div class="nambei-sidebar-section"><div class="nambei-author-card"><img src="https://nambei-oyaji.com/wp-content/uploads/2026/03/profile.png" alt="\u5357\u7c73\u304a\u3084\u3058"><div class="name">\u5357\u7c73\u304a\u3084\u3058</div><div class="desc">\u30d1\u30e9\u30b0\u30a2\u30a4\u30fb\u30a2\u30b9\u30f3\u30b7\u30aa\u30f3\u5728\u4f4f\u306e\u65e5\u672c\u4eba\u30d6\u30ed\u30ac\u30fc\u3002\u5bb6\u65cf4\u4eba\u30672025\u5e74\u306b\u5357\u7c73\u79fb\u4f4f\u3002\u6d77\u5916\u79fb\u4f4f\u30fb\u6d77\u5916\u751f\u6d3b\u306e\u30ea\u30a2\u30eb\u3092\u3001\u5b9f\u4f53\u9a13\u30d9\u30fc\u30b9\u3067\u767a\u4fe1\u3057\u3066\u3044\u307e\u3059\u3002</div></div></div><div class="nambei-sidebar-section"><div class="nambei-sidebar-title">\u30ab\u30c6\u30b4\u30ea\u30fc</div><ul class="nambei-sidebar-list"><li><a href="/category/paraguay/">\u30d1\u30e9\u30b0\u30a2\u30a4\u751f\u6d3b</a></li><li><a href="/category/side-business/">\u6d77\u5916\u304b\u3089\u306e\u7a3c\u304e\u65b9</a></li><li><a href="/category/ijuu-junbi/">\u304a\u91d1\u3068\u624b\u7d9a\u304d</a></li></ul></div><div class="nambei-sidebar-section"><div class="nambei-sidebar-title">\u65b0\u7740\u8a18\u4e8b</div><ul class="nambei-sidebar-list" id="nambei-popular-posts"></ul></div>\';',
    'fetch("/wp-json/wp/v2/posts?per_page=5&orderby=date&order=desc").then(function(r){return r.json()}).then(function(posts){',
    'var ul=document.getElementById("nambei-popular-posts");',
    'if(ul){posts.forEach(function(p){var li=document.createElement("li");li.innerHTML=\'<a href="\'+p.link+\'">\'+p.title.rendered+\'</a>\';ul.appendChild(li);});}',
    '});',
    '}',
    'var mq=window.matchMedia("(max-width:834px)");',
    'function handleMQ(e){',
    'if(e.matches){',
    'if(ci)ci.style.flexDirection="column";',
    'if(sb){sb.style.width="100%";sb.style.minWidth="auto";}',
    '}else{',
    'if(ci)ci.style.flexDirection="row";',
    'if(sb){sb.style.width="336px";sb.style.minWidth="336px";}',
    '}}',
    'mq.addListener(handleMQ);',
    'handleMQ(mq);',
    '}',
    '});',
    '</script>'
]
js2 = '\n'.join(js2_lines)

content2 = css2 + js2

r = requests.put(
    'https://nambei-oyaji.com/wp-json/wp/v2/widgets/custom_html-2',
    auth=auth,
    json={'id': 'custom_html-2', 'sidebar': 'content-top', 'instance': {'raw': {'content': content2}}}
)
print('Widget 2:', r.status_code)

# ===== WIDGET 2: sidebar (custom_html-3) =====
r = requests.get('https://nambei-oyaji.com/wp-json/wp/v2/widgets/custom_html-3', auth=auth)
old_rendered = r.json().get('rendered', '')

script_match = re.search(r'<script>(.*?)</script>', old_rendered, re.DOTALL)
if not script_match:
    print("ERROR: could not find script in widget 3")
    exit(1)

old_script = script_match.group(1)

# New populateSidebar function
new_populate = """
  /* ===== Populate Cocoon Sidebar (Apple-style cards) ===== */
  function populateSidebar(ct) {
    var sb = document.getElementById('sidebar');
    if (!sb) return;

    sb.innerHTML = '';

    // 1. Author card
    var authorSec = el('div', 'nambei-sidebar-section');
    authorSec.innerHTML = '<div class="nambei-author-card"><img src="https://nambei-oyaji.com/wp-content/uploads/2026/03/profile.png" alt="\\u5357\\u7c73\\u304a\\u3084\\u3058"><div class="name">\\u5357\\u7c73\\u304a\\u3084\\u3058</div><div class="desc">\\u30d1\\u30e9\\u30b0\\u30a2\\u30a4\\u30fb\\u30a2\\u30b9\\u30f3\\u30b7\\u30aa\\u30f3\\u5728\\u4f4f\\u306e\\u65e5\\u672c\\u4eba\\u30d6\\u30ed\\u30ac\\u30fc\\u3002\\u5bb6\\u65cf4\\u4eba\\u30672025\\u5e74\\u306b\\u5357\\u7c73\\u79fb\\u4f4f\\u3002\\u6d77\\u5916\\u79fb\\u4f4f\\u30fb\\u6d77\\u5916\\u751f\\u6d3b\\u306e\\u30ea\\u30a2\\u30eb\\u3092\\u3001\\u5b9f\\u4f53\\u9a13\\u30d9\\u30fc\\u30b9\\u3067\\u767a\\u4fe1\\u3057\\u3066\\u3044\\u307e\\u3059\\u3002</div></div>';
    sb.appendChild(authorSec);

    // 2. Search
    var searchSec = el('div', 'nambei-sidebar-section');
    searchSec.innerHTML = '<div class="nambei-sidebar-title">\\u691c\\u7d22</div><form class="nambei-sidebar-search" action="/" method="get"><input type="text" name="s" placeholder="\\u8a18\\u4e8b\\u3092\\u691c\\u7d22..."><button type="submit">\\ud83d\\udd0d</button></form>';
    sb.appendChild(searchSec);

    // 3. Categories
    var catSec = el('div', 'nambei-sidebar-section');
    catSec.innerHTML = '<div class="nambei-sidebar-title">\\u30ab\\u30c6\\u30b4\\u30ea\\u30fc</div><ul class="nambei-sidebar-list"><li><a href="/category/paraguay/">\\u30d1\\u30e9\\u30b0\\u30a2\\u30a4\\u751f\\u6d3b</a></li><li><a href="/category/side-business/">\\u6d77\\u5916\\u304b\\u3089\\u306e\\u7a3c\\u304e\\u65b9</a></li><li><a href="/category/ijuu-junbi/">\\u304a\\u91d1\\u3068\\u624b\\u7d9a\\u304d</a></li></ul>';
    sb.appendChild(catSec);

    // 4. New posts
    var newSec = el('div', 'nambei-sidebar-section');
    newSec.innerHTML = '<div class="nambei-sidebar-title">\\u65b0\\u7740\\u8a18\\u4e8b</div><ul class="nambei-sidebar-list" id="nambei-sidebar-new"></ul>';
    sb.appendChild(newSec);

    fetch('/wp-json/wp/v2/posts?per_page=5&orderby=date&order=desc')
      .then(function(r) { return r.ok ? r.json() : []; })
      .then(function(posts) {
        var ul = document.getElementById('nambei-sidebar-new');
        if (!ul || !posts.length) return;
        posts.forEach(function(p) {
          var li = document.createElement('li');
          li.innerHTML = '<a href="' + p.link + '">' + p.title.rendered + '</a>';
          ul.appendChild(li);
        });
      }).catch(function(){});

    // 5. TOC (sticky)
    var hs = ct.querySelectorAll('h2, h3');
    if (hs.length >= 3) {
      var tocSec = el('div', 'nambei-sidebar-section nambei-sidebar-toc');
      var tocTitle = el('div', 'nambei-sidebar-title', '\\u76ee\\u6b21');
      tocSec.appendChild(tocTitle);
      var list = el('ol', '');
      var sub = null;

      for (var i = 0; i < hs.length; i++) {
        var h = hs[i];
        if (!h.id) h.id = 'tcd-h-' + i;
        var li = el('li', '', '<a href="#' + h.id + '" data-toc-id="' + h.id + '">' + h.textContent.trim() + '</a>');
        if (h.tagName === 'H2') { list.appendChild(li); sub = null; }
        else {
          if (!sub) { sub = el('ol', 'nambei-toc-sub'); list.appendChild(sub); }
          li.className = 'nambei-toc-h3';
          sub.appendChild(li);
        }
      }
      tocSec.appendChild(list);
      sb.appendChild(tocSec);
    }
  }"""

# Find and replace
old_fn_start = '  /* ===== Populate Cocoon Sidebar ===== */'
old_fn_end = '  /* ===== Author Info ===== */'

idx_start = old_script.find(old_fn_start)
idx_end = old_script.find(old_fn_end)

if idx_start == -1 or idx_end == -1:
    print("ERROR: could not find populateSidebar boundaries")
    print("start:", idx_start, "end:", idx_end)
    exit(1)

new_script = old_script[:idx_start] + new_populate + '\n\n  ' + old_script[idx_end:]

# Update scrollSpy to use new class
new_script = new_script.replace(
    "var links = document.querySelectorAll('.tcd-sidebar-toc-list a[data-toc-id]');",
    "var links = document.querySelectorAll('.nambei-sidebar-toc a[data-toc-id]');"
)
new_script = new_script.replace('tcd-stoc-active', 'nambei-toc-active')

new_content3 = '<script>' + new_script + '</script>'

r = requests.put(
    'https://nambei-oyaji.com/wp-json/wp/v2/widgets/custom_html-3',
    auth=auth,
    json={'id': 'custom_html-3', 'sidebar': 'sidebar', 'instance': {'raw': {'content': new_content3}}}
)
print('Widget 3:', r.status_code)
