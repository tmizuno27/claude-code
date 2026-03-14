/**
 * TCD-Style Single Article Enhancement v3.1 (Cocoon Adapted)
 * Works with Cocoon theme DOM: #content > #content-in > #main + #sidebar
 */
(function () {
  if (!document.body.classList.contains('single')) return;

  var AUTHOR_NAME = '\u5357\u7c73\u304a\u3084\u3058';
  var AUTHOR_DESC = '\u30d1\u30e9\u30b0\u30a2\u30a4\u30fb\u30a2\u30b9\u30f3\u30b7\u30aa\u30f3\u5728\u4f4f\u306e\u65e5\u672c\u4eba\u30d6\u30ed\u30ac\u30fc\u3002\u5bb6\u65cf4\u4eba\u30672025\u5e74\u306b\u5357\u7c73\u79fb\u4f4f\u3002\u6d77\u5916\u79fb\u4f4f\u30fb\u6d77\u5916\u751f\u6d3b\u306e\u30ea\u30a2\u30eb\u3092\u3001\u5b9f\u4f53\u9a13\u30d9\u30fc\u30b9\u3067\u767a\u4fe1\u3057\u3066\u3044\u307e\u3059\u3002';
  var AUTHOR_URL = 'https://nambei-oyaji.com/profile/';
  var SITE_RSS = 'https://nambei-oyaji.com/feed/';

  function ready(fn) {
    if (document.readyState !== 'loading') fn();
    else document.addEventListener('DOMContentLoaded', fn);
  }

  function el(tag, cls, html) {
    var e = document.createElement(tag);
    if (cls) e.className = cls;
    if (html) e.innerHTML = html;
    return e;
  }

  ready(function () {
    var content = document.querySelector('.entry-content');
    if (!content) return;

    // Scroll padding for fixed header
    var scrollStyle = document.createElement('style');
    scrollStyle.textContent = 'html{scroll-padding-top:80px;}';
    document.head.appendChild(scrollStyle);

    // 1. TOC in content
    var tocBox = createTOC(content);
    if (tocBox) {
      var paras = content.querySelectorAll(':scope > p');
      var after = paras.length >= 3 ? paras[2] : (paras[0] || null);
      if (after && after.nextElementSibling) after.after(tocBox);
      else {
        var h2 = content.querySelector('h2');
        if (h2) h2.before(tocBox);
        else content.prepend(tocBox);
      }
    }

    // 2. Sidebar TOC + widgets
    try { populateSidebar(content); } catch(e) { console.error('Sidebar error:', e); }

    // 3. Author
    content.appendChild(createAuthorInfo());

    // 4. Related articles
    insertRelatedArticles(content);

    // 5. Floating elements
    createBackToTop();
    createMobileTocButton(content);

    // 6. Scroll spy
    activateScrollSpy();

    // 7. Enhance content
    enhanceContent(content);
  });

  /* ===== TOC ===== */
  function createTOC(ct) {
    var hs = ct.querySelectorAll('h2, h3, h4');
    if (hs.length < 3) return null;

    var toc = el('div', 'tcd-toc');
    var bar = el('div', 'tcd-toc-title');
    bar.innerHTML = '<span>\u76ee\u6b21</span><button class="tcd-toc-toggle" aria-label="\u76ee\u6b21\u3092\u958b\u9589">\u25bc</button>';
    toc.appendChild(bar);

    var list = el('ol', 'tcd-toc-list');
    var sub2 = null, sub3 = null;

    for (var i = 0; i < hs.length; i++) {
      var h = hs[i];
      if (!h.id) h.id = 'tcd-h-' + i;
      var li = el('li', '', '<a href="#' + h.id + '">' + h.textContent.trim() + '</a>');

      if (h.tagName === 'H2') {
        li.className = 'tcd-toc-h2'; list.appendChild(li); sub2 = null; sub3 = null;
      } else if (h.tagName === 'H3') {
        if (!sub2) { sub2 = el('ol', 'tcd-toc-sub'); list.appendChild(sub2); }
        li.className = 'tcd-toc-h3'; sub2.appendChild(li); sub3 = null;
      } else {
        var p = sub2 || list;
        if (!sub3) { sub3 = el('ol', 'tcd-toc-sub'); p.appendChild(sub3); }
        li.className = 'tcd-toc-h3'; li.style.paddingLeft = '12px'; sub3.appendChild(li);
      }
    }
    toc.appendChild(list);

    bar.addEventListener('click', function () {
      toc.classList.toggle('tcd-toc--closed');
      bar.querySelector('.tcd-toc-toggle').textContent = toc.classList.contains('tcd-toc--closed') ? '\u25b6' : '\u25bc';
    });
    return toc;
  }

  /* ===== Populate Cocoon Sidebar ===== */
  function populateSidebar(ct) {
    var sb = document.getElementById('sidebar');
    if (!sb) return;

    // Clear existing content and create wrapper
    sb.innerHTML = '';
    var sbi = el('div', 'nao-tcd-sidebar-inner');
    sb.appendChild(sbi);

    // 1. Search
    var searchW = el('div', 'nao-tcd-widget');
    searchW.innerHTML =
      '<h4 class="nao-tcd-widget-title">\u691c\u7d22</h4>' +
      '<form class="nao-tcd-search" action="/" method="get">' +
        '<input type="text" name="s" class="nao-tcd-search-input" placeholder="\u8a18\u4e8b\u3092\u691c\u7d22...">' +
        '<button type="submit" class="nao-tcd-search-btn">\ud83d\udd0d</button>' +
      '</form>';
    sbi.appendChild(searchW);

    // 2. New posts
    var newW = el('div', 'nao-tcd-widget');
    newW.innerHTML = '<h4 class="nao-tcd-widget-title">\u65b0\u7740\u8a18\u4e8b</h4><ul class="nao-tcd-post-list" id="nao-sidebar-new"></ul>';
    sbi.appendChild(newW);

    fetch('/wp-json/wp/v2/posts?per_page=5&_embed&_fields=id,title,link,date,_embedded')
      .then(function(r) { return r.ok ? r.json() : []; })
      .then(function(posts) {
        var ul = document.getElementById('nao-sidebar-new');
        if (!ul || !posts.length) return;
        posts.forEach(function(p) {
          var catName = '';
          try { catName = p._embedded['wp:term'][0][0].name; } catch(e) {}
          var li = el('li', '');
          li.innerHTML = '<a href="' + p.link + '">' +
            (catName ? '<span class="nao-tcd-post-cat">' + catName + '</span>' : '') +
            '<span class="nao-tcd-post-title">' + p.title.rendered + '</span></a>';
          ul.appendChild(li);
        });
      }).catch(function(){});

    // 3. Categories
    var catW = el('div', 'nao-tcd-widget');
    catW.innerHTML = '<h4 class="nao-tcd-widget-title">\u30ab\u30c6\u30b4\u30ea\u30fc</h4><ul class="nao-tcd-cat-list" id="nao-sidebar-cats"></ul>';
    sbi.appendChild(catW);

    fetch('/wp-json/wp/v2/categories?per_page=20&_fields=id,name,slug,count,link&hide_empty=true')
      .then(function(r) { return r.ok ? r.json() : []; })
      .then(function(cats) {
        var ul = document.getElementById('nao-sidebar-cats');
        if (!ul || !cats.length) return;
        cats.filter(function(c) { return c.slug !== 'uncategorized'; }).forEach(function(c) {
          var li = el('li', '');
          li.innerHTML = '<a href="' + c.link + '"><span class="nao-tcd-cat-name">' + c.name + '</span><span class="nao-tcd-cat-count">(' + c.count + ')</span></a>';
          ul.appendChild(li);
        });
      }).catch(function(){});

    // 4. TOC widget (sticky)
    var hs = ct.querySelectorAll('h2, h3');
    if (hs.length >= 3) {
      var w = el('div', 'nao-tcd-widget tcd-sidebar-toc');
      w.appendChild(el('h4', 'nao-tcd-widget-title', '\u76ee\u6b21'));
      var list = el('ol', 'tcd-sidebar-toc-list');
      var sub = null;

      for (var i = 0; i < hs.length; i++) {
        var h = hs[i];
        if (!h.id) h.id = 'tcd-h-' + i;
        var li = el('li', '', '<a href="#' + h.id + '" data-toc-id="' + h.id + '">' + h.textContent.trim() + '</a>');
        if (h.tagName === 'H2') { li.className = 'tcd-stoc-h2'; list.appendChild(li); sub = null; }
        else { if (!sub) { sub = el('ol', 'tcd-stoc-sub'); list.appendChild(sub); } li.className = 'tcd-stoc-h3'; sub.appendChild(li); }
      }
      w.appendChild(list);
      sbi.appendChild(w);
    }
  }

  /* ===== Author Info ===== */
  function createAuthorInfo() {
    var box = el('div', 'tcd-author');
    box.innerHTML =
      '<div class="tcd-author-inner">' +
        '<div class="nao-author-avatar-wrap"><img src="https://nambei-oyaji.com/wp-content/uploads/2026/03/profile-nambei-oyaji.png" alt="' + AUTHOR_NAME + '" class="nao-author-avatar-img" loading="lazy"></div>' +
        '<div class="tcd-author-text">' +
          '<div class="tcd-author-label">WRITER</div>' +
          '<div class="tcd-author-name">' + AUTHOR_NAME + '</div>' +
          '<p class="tcd-author-desc">' + AUTHOR_DESC + '</p>' +
        '</div>' +
      '</div>';
    return box;
  }

  /* ===== Related Articles ===== */
  function insertRelatedArticles(ct) {
    if (document.querySelector('.related-entries, .related-list')) return;

    var section = el('div', 'tcd-related');
    section.innerHTML = '<h3 class="tcd-related-title">\u95a2\u9023\u8a18\u4e8b</h3><div class="tcd-related-grid" id="tcd-related-grid"></div>';

    var cats = document.querySelectorAll('a[rel="category tag"], .cat-links a, .cat-label');
    if (!cats.length) return;

    var catEl = cats[0];
    var catHref = catEl.href || '';
    var catSlug = catHref.split('/').filter(Boolean).pop();
    var cur = location.pathname;

    fetch('/wp-json/wp/v2/posts?per_page=7&_embed&categories_slug=' + catSlug)
      .then(function (r) { return r.ok ? r.json() : []; })
      .then(function (posts) {
        if (!posts || !posts.length) return;
        var grid = document.getElementById('tcd-related-grid');
        if (!grid) return;

        var n = 0;
        for (var i = 0; i < posts.length; i++) {
          if (n >= 6) break;
          var p = posts[i];
          if (new URL(p.link).pathname === cur) continue;

          var thumb = '';
          try { thumb = p._embedded['wp:featuredmedia'][0].media_details.sizes.medium.source_url; } catch(e) {}

          var dt = new Date(p.date);
          var ds = dt.getFullYear() + '.' + String(dt.getMonth()+1).padStart(2,'0') + '.' + String(dt.getDate()).padStart(2,'0');

          var card = el('a', 'tcd-related-card');
          card.href = p.link;
          card.innerHTML =
            '<div class="tcd-related-card-thumb">' + (thumb ? '<img src="' + thumb + '" alt="" loading="lazy">' : '') + '</div>' +
            '<div class="tcd-related-card-body">' +
              '<div class="tcd-related-card-title">' + p.title.rendered + '</div>' +
              '<div class="tcd-related-card-date">' + ds + '</div>' +
            '</div>';
          grid.appendChild(card);
          n++;
        }
        if (n > 0) ct.appendChild(section);
      })
      .catch(function () {});
  }

  /* ===== Back to Top ===== */
  function createBackToTop() {
    var btn = el('button', 'tcd-totop');
    btn.innerHTML = '\u2191';
    btn.setAttribute('aria-label', '\u30da\u30fc\u30b8\u4e0a\u90e8\u306b\u623b\u308b');
    btn.style.display = 'none';
    document.body.appendChild(btn);
    btn.addEventListener('click', function () { window.scrollTo({ top: 0, behavior: 'smooth' }); });
    window.addEventListener('scroll', function () {
      btn.style.display = window.scrollY > 300 ? 'flex' : 'none';
    }, { passive: true });
  }

  /* ===== Mobile TOC Button ===== */
  function createMobileTocButton(ct) {
    var hs = ct.querySelectorAll('h2, h3');
    if (hs.length < 3) return;

    var ov = el('div', 'tcd-mtoc-overlay');
    ov.style.display = 'none';
    var inner = el('div', 'tcd-mtoc-inner');
    inner.innerHTML = '<div class="tcd-mtoc-header"><span>\u76ee\u6b21</span><button class="tcd-mtoc-close">\u2715</button></div>';

    var list = el('ol', 'tcd-mtoc-list');
    for (var i = 0; i < hs.length; i++) {
      var h = hs[i];
      if (!h.id) h.id = 'tcd-h-' + i;
      list.appendChild(el('li', h.tagName === 'H3' ? 'tcd-mtoc-h3' : 'tcd-mtoc-h2',
        '<a href="#' + h.id + '">' + h.textContent.trim() + '</a>'));
    }
    inner.appendChild(list);
    ov.appendChild(inner);
    document.body.appendChild(ov);

    var btn = el('button', 'tcd-mtoc-btn');
    btn.innerHTML = '\u2630 \u76ee\u6b21';
    document.body.appendChild(btn);

    btn.addEventListener('click', function () { ov.style.display = 'flex'; document.body.style.overflow = 'hidden'; });
    ov.addEventListener('click', function (e) {
      if (e.target === ov || e.target.classList.contains('tcd-mtoc-close')) { ov.style.display = 'none'; document.body.style.overflow = ''; }
    });
    list.addEventListener('click', function (e) {
      if (e.target.tagName === 'A') { ov.style.display = 'none'; document.body.style.overflow = ''; }
    });
  }

  /* ===== Scroll Spy ===== */
  function activateScrollSpy() {
    var links = document.querySelectorAll('.tcd-sidebar-toc-list a[data-toc-id]');
    if (!links.length) return;

    var items = [];
    for (var i = 0; i < links.length; i++) {
      var t = document.getElementById(links[i].getAttribute('data-toc-id'));
      if (t) items.push({ el: t, link: links[i] });
    }

    var ticking = false;
    function update() {
      var sy = window.scrollY + 120;
      var active = null;
      for (var i = 0; i < items.length; i++) { if (items[i].el.offsetTop <= sy) active = items[i]; }
      for (var j = 0; j < items.length; j++) { items[j].link.classList.remove('tcd-stoc-active'); }
      if (active) active.link.classList.add('tcd-stoc-active');
      ticking = false;
    }
    window.addEventListener('scroll', function () {
      if (!ticking) { requestAnimationFrame(update); ticking = true; }
    }, { passive: true });
    update();
  }

  /* ===== Enhance Content ===== */
  function enhanceContent(ct) {
    var imgs = ct.querySelectorAll('img:not([loading])');
    for (var i = 0; i < imgs.length; i++) imgs[i].setAttribute('loading', 'lazy');

    var tables = ct.querySelectorAll('table');
    for (var j = 0; j < tables.length; j++) {
      if (!tables[j].parentElement.classList.contains('tcd-table-wrap')) {
        var w = el('div', 'tcd-table-wrap');
        tables[j].parentNode.insertBefore(w, tables[j]);
        w.appendChild(tables[j]);
      }
    }
  }

})();
