/**
 * TCD-Style Single Article Enhancement v3.0
 * Faithful reproduction of tcd-theme.com blog article design.
 * Adds: breadcrumbs, category label, meta info, TOC, SNS share (Tweet/Share/Hatena/RSS),
 *       author info with SNS, related articles 2x3, floating buttons, scroll spy.
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
    var content = document.querySelector('.entry-content, .wp-block-post-content');
    if (!content) return;

    // Scroll padding for fixed header
    var scrollStyle = document.createElement('style');
    scrollStyle.textContent = 'html{scroll-padding-top:80px;}';
    document.head.appendChild(scrollStyle);

    // 1. Breadcrumbs
    insertBreadcrumbs();

    // 2. Category label + Meta info
    insertCategoryLabel(content);
    insertMetaInfo(content);

    // 5. TOC
    var tocBox = createTOC(content);
    if (tocBox) {
      var paras = content.querySelectorAll(':scope > p');
      var after = paras.length >= 3 ? paras[2] : (paras[0] || null);
      if (after) { if (after.nextElementSibling) after.after(tocBox); }
      else {
        var h2 = content.querySelector('h2');
        if (h2) h2.before(tocBox);
        else content.prepend(tocBox);
      }
    }

    // 6. Sidebar TOC — insert end-of-article marker BEFORE appending extras
    var articleEndMarker = el('div', '');
    articleEndMarker.id = 'nao-article-end-marker';
    content.appendChild(articleEndMarker);
    try { insertSidebarTOC(content); } catch(e) { console.error('SidebarTOC error:', e); }

    // 8. Author
    content.appendChild(createAuthorInfo());

    // 9. Related articles
    insertRelatedArticles(content);

    // 10. Floating elements
    createBackToTop();
    createMobileTocButton(content);

    // 11. Scroll spy
    activateScrollSpy();

    // 12. Enhance content
    enhanceContent(content);

    // 13. Mobile takeover — rebuild entire page structure on mobile
    if (window.innerWidth <= 768) {
      mobileTakeover();
    }
  });

  /* ===== Breadcrumbs ===== */
  function insertBreadcrumbs() {
    var main = document.querySelector('main, .main, #main, .site-main, .wp-block-group');
    if (!main) return;

    var cats = document.querySelectorAll('a[rel="category tag"], .wp-block-post-terms a, .cat-links a');
    var catName = '', catHref = '/';
    if (cats.length) { catName = cats[0].textContent.trim(); catHref = cats[0].href; }

    var title = document.title.split('|')[0].split('\u2013')[0].trim();
    var bc = el('nav', 'tcd-breadcrumb');
    bc.setAttribute('aria-label', '\u30d1\u30f3\u304f\u305a\u30ea\u30b9\u30c8');
    var h = '<a href="/">\u30db\u30fc\u30e0</a><span class="tcd-bc-sep">&gt;</span>';
    if (catName) h += '<a href="' + catHref + '">' + catName + '</a><span class="tcd-bc-sep">&gt;</span>';
    h += '<span class="tcd-bc-current">' + title + '</span>';
    bc.innerHTML = h;
    main.prepend(bc);
  }

  /* ===== Category Label ===== */
  function insertCategoryLabel(ct) {
    var cats = document.querySelectorAll('a[rel="category tag"], .wp-block-post-terms a, .cat-links a');
    if (!cats.length) return;
    var a = el('a', 'tcd-cat-label');
    a.href = cats[0].href;
    a.textContent = cats[0].textContent.trim();
    ct.prepend(a);
  }

  /* ===== Meta Info ===== */
  function insertMetaInfo(ct) {
    var meta = el('div', 'tcd-meta');
    var dateEl = document.querySelector('.date, time, .post-date, .entry-date, .wp-block-post-date');
    var dateText = '';
    if (dateEl) {
      var t = dateEl.querySelector('time') || dateEl;
      dateText = t.getAttribute('datetime') || t.textContent.trim();
      if (dateText) {
        var d = new Date(dateText);
        if (!isNaN(d.getTime())) {
          dateText = d.getFullYear() + '.' + String(d.getMonth()+1).padStart(2,'0') + '.' + String(d.getDate()).padStart(2,'0');
        }
      }
    }
    if (dateText) meta.innerHTML += '<span class="tcd-meta-date">' + dateText + '</span>';

    var tags = document.querySelectorAll('.tag-links a, a[rel="tag"]');
    if (tags.length) {
      var th = '<span class="tcd-meta-tags">';
      var tagMax = Math.min(tags.length, 5);
      for (var i = 0; i < tagMax; i++) {
        th += '<a href="' + tags[i].href + '" class="tcd-meta-tag">' + tags[i].textContent.trim() + '</a>';
      }
      meta.innerHTML += th + '</span>';
    }

    var catLabel = ct.querySelector('.tcd-cat-label');
    if (catLabel) catLabel.after(meta); else ct.prepend(meta);
  }

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

  /* ===== Sidebar TOC ===== */
  function insertSidebarTOC(ct) {
    var sb = document.querySelector('.nao-tcd-sidebar') || document.getElementById('nao-tcd-sidebar') || document.querySelector('.sidebar, #sidebar, aside');
    if (!sb) return;
    var hs = ct.querySelectorAll('h2, h3');
    if (hs.length < 3) return;

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
    var sbi = sb.querySelector('.nao-tcd-sidebar-inner') || sb;
    sbi.appendChild(w);
    // Make sidebar TOC sticky
    w.style.position = 'sticky';
    w.style.top = '100px';

    // Footer z-index covers sidebar, no JS height needed
  }

  /* ===== Share Buttons — TCD text style (Tweet/Share/Hatena/RSS) ===== */
  function createShareButtons(cls) {
    var url = encodeURIComponent(location.href);
    var title = encodeURIComponent(document.title);
    var w = el('div', cls);
    w.innerHTML =
      '<div class="tcd-share-buttons">' +
      '<a href="https://twitter.com/intent/tweet?url=' + url + '&text=' + title + '" target="_blank" rel="noopener" class="tcd-share-btn tcd-share-x">Tweet</a>' +
      '<a href="https://www.facebook.com/sharer/sharer.php?u=' + url + '" target="_blank" rel="noopener" class="tcd-share-btn tcd-share-fb">Share</a>' +
      '<a href="https://b.hatena.ne.jp/entry/' + location.href + '" target="_blank" rel="noopener" class="tcd-share-btn tcd-share-hatena">Hatena</a>' +
      '<a href="' + SITE_RSS + '" target="_blank" rel="noopener" class="tcd-share-btn tcd-share-rss">RSS</a>' +
      '</div>';
    return w;
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
          '' +
        '</div>' +
      '</div>';
    return box;
  }

  /* ===== Related Articles ===== */
  function insertRelatedArticles(ct) {
    if (document.querySelector('.related-entries, .related-list')) return;

    var section = el('div', 'tcd-related');
    section.innerHTML = '<h3 class="tcd-related-title">\u95a2\u9023\u8a18\u4e8b</h3><div class="tcd-related-grid" id="tcd-related-grid"></div>';

    var cats = document.querySelectorAll('a[rel="category tag"], .cat-links a');
    if (!cats.length) return;

    var catSlug = cats[0].href.split('/').filter(Boolean).pop();
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

  /* ===== Back to Top — TCD square style ===== */
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

  /* ===== Mobile Takeover ===== */
  /* On mobile, hide the entire WP theme DOM and rebuild a clean page. */
  function mobileTakeover() {
    // 1. Grab the data we need from the existing DOM
    var titleEl = document.querySelector('.wp-block-post-title, .entry-title');
    var featImgEl = document.querySelector('.wp-block-post-featured-image img');
    var contentEl = document.querySelector('.wp-block-post-content, .entry-content');
    var headerEl = document.querySelector('header.wp-block-template-part, header');
    var footerEl = document.querySelector('footer.wp-block-template-part, footer');

    if (!contentEl) return;

    var titleHTML = titleEl ? titleEl.innerHTML : '';
    var featImgSrc = featImgEl ? featImgEl.src : '';
    var featImgAlt = featImgEl ? (featImgEl.alt || '') : '';

    // Get category and date from our injected tcd-meta / tcd-cat-label
    var catEl = contentEl.querySelector('.tcd-cat-label');
    var metaEl = contentEl.querySelector('.tcd-meta');
    var catHTML = catEl ? catEl.outerHTML : '';
    var metaHTML = metaEl ? metaEl.outerHTML : '';

    // Remove cat/meta from content before cloning (they'll go in our header area)
    if (catEl) catEl.remove();
    if (metaEl) metaEl.remove();

    // 2. Build the new mobile page
    var page = el('div', 'nao-m-page');

    // Mobile header bar
    var mHeader = el('div', 'nao-m-hdr');
    mHeader.innerHTML = '<a href="/" class="nao-m-hdr-logo">\u5357\u7c73\u304a\u3084\u3058\u306e<br>\u6d77\u5916\u751f\u6d3b\u30e9\u30dc</a>' +
      '<button class="nao-m-hdr-menu" aria-label="\u30e1\u30cb\u30e5\u30fc">\u2630</button>';
    page.appendChild(mHeader);

    // Article wrapper
    var article = el('article', 'nao-m-art');

    // Featured image (full bleed, before title like TCD)
    if (featImgSrc) {
      var imgWrap = el('div', 'nao-m-eyecatch');
      imgWrap.innerHTML = '<img src="' + featImgSrc + '" alt="' + featImgAlt + '" loading="eager">';
      article.appendChild(imgWrap);
    }

    // Category + date
    if (catHTML || metaHTML) {
      var infoBar = el('div', 'nao-m-info');
      infoBar.innerHTML = catHTML + metaHTML;
      article.appendChild(infoBar);
    }

    // Title
    var titleWrap = el('h1', 'nao-m-title');
    titleWrap.innerHTML = titleHTML;
    article.appendChild(titleWrap);

    // Content — MOVE the actual DOM node (preserves event listeners for TOC etc.)
    contentEl.className = 'nao-m-content';
    article.appendChild(contentEl);

    page.appendChild(article);

    // Footer — move to top of page (after header bar)
    if (footerEl) {
      footerEl.className = 'nao-m-footer';
      mHeader.after(footerEl);
    }

    // 3. Hide EVERYTHING in body except our new page + floating elements
    var bodyChildren = document.body.children;
    for (var i = 0; i < bodyChildren.length; i++) {
      var child = bodyChildren[i];
      if (child === page) continue;
      if (child.tagName === 'SCRIPT' || child.tagName === 'STYLE' || child.tagName === 'LINK') continue;
      // Keep floating overlays (mobile TOC, back-to-top)
      if (child.classList.contains('tcd-mtoc-overlay') || child.classList.contains('tcd-mtoc-btn') || child.classList.contains('tcd-totop')) continue;
      child.setAttribute('data-nao-hidden', '1');
      child.style.display = 'none';
    }

    // 4. Insert our page
    document.body.prepend(page);
    document.body.classList.add('nao-mobile-active');

    // 5. Mobile menu toggle
    var menuBtn = page.querySelector('.nao-m-hdr-menu');
    if (menuBtn) {
      menuBtn.addEventListener('click', function() {
        var nav = page.querySelector('.nao-m-nav');
        if (nav) {
          nav.style.display = nav.style.display === 'none' ? 'block' : 'none';
        } else {
          nav = el('nav', 'nao-m-nav');
          nav.innerHTML =
            '<a href="/">\u30db\u30fc\u30e0</a>' +
            '<a href="/category/paraguay/">\u30d1\u30e9\u30b0\u30a2\u30a4\u751f\u6d3b</a>' +
            '<a href="/category/side-business/">\u526f\u696d\u30fb\u7a3c\u304e\u65b9</a>' +
            '<a href="/category/ijuu-junbi/">\u79fb\u4f4f\u6e96\u5099</a>' +
            '<a href="/about/">\u30d7\u30ed\u30d5\u30a3\u30fc\u30eb</a>';
          mHeader.after(nav);
        }
      });
    }
  }

  /* ===== Enhance Content ===== */
  function enhanceContent(ct) {
    // Lazy load images
    var imgs = ct.querySelectorAll('img:not([loading])');
    for (var i = 0; i < imgs.length; i++) imgs[i].setAttribute('loading', 'lazy');

    // Wrap tables for mobile scroll
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
