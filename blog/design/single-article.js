/**
 * TCD-Style Single Article Enhancement
 * Generates: layout wrapper, breadcrumbs, TOC, SNS share,
 * author info, related articles, floating buttons
 */
(function () {
  if (!document.body.classList.contains('single')) return;

  var WP_API = '/wp-json/wp/v2';
  var SITE_URL = location.origin;
  var AUTHOR_NAME = '\u5357\u7c73\u304a\u3084\u3058';
  var AUTHOR_DESC = '\u30d1\u30e9\u30b0\u30a2\u30a4\u5728\u4f4f\u306e\u65e5\u672c\u4eba\u30d6\u30ed\u30ac\u30fc\u3002\u6d77\u5916\u79fb\u4f4f\u30fb\u6d77\u5916\u751f\u6d3b\u306e\u30ea\u30a2\u30eb\u3092\u767a\u4fe1\u4e2d\u3002\u30a2\u30b5\u30f3\u30b7\u30aa\u30f3\u304b\u3089\u304a\u5c4a\u3051\u3057\u307e\u3059\u3002';
  var AUTHOR_AVATAR = '/wp-content/uploads/profile-avatar.webp';

  // Wait for DOM ready
  function ready(fn) {
    if (document.readyState !== 'loading') fn();
    else document.addEventListener('DOMContentLoaded', fn);
  }

  // Utility: create element with class and optional HTML
  function el(tag, cls, html) {
    var e = document.createElement(tag);
    if (cls) e.className = cls;
    if (html) e.innerHTML = html;
    return e;
  }

  ready(function () {
    var content = document.querySelector('.entry-content, .wp-block-post-content');
    if (!content) return;

    var main = content.closest('main') || content.parentElement;

    // ===== 1. Create 2-column layout wrapper =====
    var layoutWrap = el('div', 'tcd-layout');
    var mainCol = el('div', 'tcd-main');
    var sidebar = el('div', 'tcd-sidebar');

    // Find the article title element
    var titleEl = document.querySelector('.wp-block-post-title, .entry-title, h1.wp-block-heading');
    var dateEl = document.querySelector('.wp-block-post-date, .post-date');
    var featuredImg = document.querySelector('.wp-block-post-featured-image, .post-thumbnail');

    // Insert layout wrapper
    var insertPoint = titleEl || content;
    var parent = insertPoint.parentElement;

    // Move title, date, featured image, content into mainCol
    if (titleEl) mainCol.appendChild(titleEl.cloneNode(true));

    // Create article meta (date + category)
    var metaBar = createMetaBar();
    if (metaBar) mainCol.appendChild(metaBar);

    if (dateEl && !metaBar) mainCol.appendChild(dateEl.cloneNode(true));
    if (featuredImg) mainCol.appendChild(featuredImg.cloneNode(true));

    // Create TOC and insert before content
    var tocBox = createTOC(content);
    if (tocBox) mainCol.appendChild(tocBox);

    // Create top share buttons
    var topShare = createShareButtons('tcd-share tcd-share--top');
    mainCol.appendChild(topShare);

    mainCol.appendChild(content.cloneNode(true));

    // Create bottom share buttons
    var bottomShare = createShareButtons('tcd-share tcd-share--bottom');
    mainCol.appendChild(bottomShare);

    // Create author info
    var authorBox = createAuthorInfo();
    mainCol.appendChild(authorBox);

    // Create related articles placeholder
    var relatedSection = el('div', 'tcd-related');
    relatedSection.innerHTML = '<h3 class="tcd-related-title">\u95a2\u9023\u8a18\u4e8b</h3><div class="tcd-related-grid" id="tcd-related-grid"></div>';
    mainCol.appendChild(relatedSection);

    // Sidebar: sticky TOC
    var sidebarToc = createSidebarTOC(content);
    sidebar.appendChild(sidebarToc);

    layoutWrap.appendChild(mainCol);
    layoutWrap.appendChild(sidebar);

    // Create breadcrumbs above layout
    var breadcrumbs = createBreadcrumbs();

    // Remove originals and insert new layout
    if (titleEl) titleEl.style.display = 'none';
    if (dateEl) dateEl.style.display = 'none';
    if (featuredImg) featuredImg.style.display = 'none';
    content.style.display = 'none';

    // Insert breadcrumbs + layout after header
    var headerPart = document.querySelector('header.wp-block-template-part');
    var insertTarget = headerPart ? headerPart.nextElementSibling || headerPart.parentElement : main;

    if (headerPart && headerPart.nextElementSibling) {
      headerPart.nextElementSibling.before(breadcrumbs);
      breadcrumbs.after(layoutWrap);
    } else {
      main.prepend(layoutWrap);
      main.prepend(breadcrumbs);
    }

    // ===== Floating elements =====
    createBackToTop();
    createMobileTocButton(content);

    // Load related articles
    loadRelatedArticles();

    // Activate TOC scroll spy
    activateScrollSpy();
  });

  // ===== Breadcrumbs =====
  function createBreadcrumbs() {
    var wrap = el('nav', 'tcd-breadcrumb');
    var catLinks = document.querySelectorAll('a[rel="category tag"], .cat-links a, .post-categories a');
    var catName = '';
    var catHref = '/';
    if (catLinks.length > 0) {
      catName = catLinks[0].textContent;
      catHref = catLinks[0].href;
    }

    var html = '<a href="/">\u30db\u30fc\u30e0</a>';
    if (catName) {
      html += ' <span class="tcd-bc-sep">\u203a</span> <a href="' + catHref + '">' + catName + '</a>';
    }
    var titleText = document.title.split('|')[0].trim();
    html += ' <span class="tcd-bc-sep">\u203a</span> <span class="tcd-bc-current">' + titleText + '</span>';
    wrap.innerHTML = html;
    return wrap;
  }

  // ===== Article Meta Bar =====
  function createMetaBar() {
    var bar = el('div', 'tcd-meta');
    var dateEl = document.querySelector('.wp-block-post-date time, time.entry-date');
    var catLinks = document.querySelectorAll('a[rel="category tag"], .cat-links a, .post-categories a');

    var html = '';
    if (dateEl) {
      var d = dateEl.getAttribute('datetime') || dateEl.textContent;
      var dateObj = new Date(d);
      var formatted = dateObj.getFullYear() + '.' +
        String(dateObj.getMonth() + 1).padStart(2, '0') + '.' +
        String(dateObj.getDate()).padStart(2, '0');
      html += '<span class="tcd-meta-date">' + formatted + '</span>';
    }
    if (catLinks.length > 0) {
      for (var i = 0; i < catLinks.length; i++) {
        html += '<a href="' + catLinks[i].href + '" class="tcd-meta-cat">' + catLinks[i].textContent + '</a>';
      }
    }
    if (!html) return null;
    bar.innerHTML = html;
    return bar;
  }

  // ===== TOC (in main content) =====
  function createTOC(contentEl) {
    var headings = contentEl.querySelectorAll('h2, h3');
    if (headings.length < 3) return null;

    var toc = el('div', 'tcd-toc');
    var titleBar = el('div', 'tcd-toc-title');
    titleBar.innerHTML = '<span>\u76ee\u6b21</span><button class="tcd-toc-toggle" aria-label="\u76ee\u6b21\u3092\u958b\u9589">\u25bc</button>';
    toc.appendChild(titleBar);

    var list = el('ol', 'tcd-toc-list');
    var currentOl = null;

    for (var i = 0; i < headings.length; i++) {
      var h = headings[i];
      var id = h.id || 'tcd-h-' + i;
      h.id = id;

      var li = el('li', '', '<a href="#' + id + '">' + h.textContent + '</a>');

      if (h.tagName === 'H2') {
        li.className = 'tcd-toc-h2';
        list.appendChild(li);
        currentOl = null;
      } else if (h.tagName === 'H3') {
        if (!currentOl) {
          currentOl = el('ol', 'tcd-toc-sub');
          list.appendChild(currentOl);
        }
        li.className = 'tcd-toc-h3';
        currentOl.appendChild(li);
      }
    }

    toc.appendChild(list);

    // Toggle functionality
    titleBar.addEventListener('click', function () {
      toc.classList.toggle('tcd-toc--closed');
      var btn = titleBar.querySelector('.tcd-toc-toggle');
      btn.textContent = toc.classList.contains('tcd-toc--closed') ? '\u25b6' : '\u25bc';
    });

    return toc;
  }

  // ===== Sidebar TOC (sticky) =====
  function createSidebarTOC(contentEl) {
    var wrap = el('div', 'tcd-sidebar-toc');
    var headings = contentEl.querySelectorAll('h2, h3');
    if (headings.length < 3) {
      wrap.innerHTML = '<p class="tcd-sidebar-empty">\u76ee\u6b21\u306a\u3057</p>';
      return wrap;
    }

    var title = el('div', 'tcd-sidebar-toc-title', '\u76ee\u6b21');
    wrap.appendChild(title);

    var list = el('ol', 'tcd-sidebar-toc-list');
    var currentOl = null;

    for (var i = 0; i < headings.length; i++) {
      var h = headings[i];
      var id = h.id || 'tcd-h-' + i;
      var li = el('li', '', '<a href="#' + id + '" data-toc-id="' + id + '">' + h.textContent + '</a>');

      if (h.tagName === 'H2') {
        li.className = 'tcd-stoc-h2';
        list.appendChild(li);
        currentOl = null;
      } else if (h.tagName === 'H3') {
        if (!currentOl) {
          currentOl = el('ol', 'tcd-stoc-sub');
          list.appendChild(currentOl);
        }
        li.className = 'tcd-stoc-h3';
        currentOl.appendChild(li);
      }
    }

    wrap.appendChild(list);
    return wrap;
  }

  // ===== SNS Share Buttons =====
  function createShareButtons(className) {
    var url = encodeURIComponent(location.href);
    var title = encodeURIComponent(document.title);
    var wrap = el('div', className);
    wrap.innerHTML =
      '<span class="tcd-share-label">\u30b7\u30a7\u30a2</span>' +
      '<div class="tcd-share-buttons">' +
      '<a href="https://twitter.com/intent/tweet?url=' + url + '&text=' + title + '" target="_blank" rel="noopener" class="tcd-share-btn tcd-share-x" aria-label="X\u3067\u30b7\u30a7\u30a2">X</a>' +
      '<a href="https://www.facebook.com/sharer/sharer.php?u=' + url + '" target="_blank" rel="noopener" class="tcd-share-btn tcd-share-fb" aria-label="Facebook\u3067\u30b7\u30a7\u30a2">Facebook</a>' +
      '<a href="https://b.hatena.ne.jp/entry/' + location.href + '" target="_blank" rel="noopener" class="tcd-share-btn tcd-share-hatena" aria-label="\u306f\u3066\u30d6\u3067\u30b7\u30a7\u30a2">\u306f\u3066\u30d6</a>' +
      '<button class="tcd-share-btn tcd-share-copy" aria-label="URL\u3092\u30b3\u30d4\u30fc">\u30b3\u30d4\u30fc</button>' +
      '</div>';

    // Copy button
    setTimeout(function () {
      var copyBtn = wrap.querySelector('.tcd-share-copy');
      if (copyBtn) {
        copyBtn.addEventListener('click', function () {
          navigator.clipboard.writeText(location.href).then(function () {
            copyBtn.textContent = '\u30b3\u30d4\u30fc\u6e08\u307f';
            setTimeout(function () { copyBtn.textContent = '\u30b3\u30d4\u30fc'; }, 2000);
          });
        });
      }
    }, 100);

    return wrap;
  }

  // ===== Author Info =====
  function createAuthorInfo() {
    var box = el('div', 'tcd-author');
    box.innerHTML =
      '<div class="tcd-author-inner">' +
      '<div class="tcd-author-avatar"><img src="' + AUTHOR_AVATAR + '" alt="' + AUTHOR_NAME + '" width="100" height="100" loading="lazy" onerror="this.parentElement.innerHTML=\'<div class=tcd-author-avatar-fallback>\ud83e\uddd1</div>\'"></div>' +
      '<div class="tcd-author-text">' +
      '<div class="tcd-author-label">\u3053\u306e\u8a18\u4e8b\u3092\u66f8\u3044\u305f\u4eba</div>' +
      '<div class="tcd-author-name">' + AUTHOR_NAME + '</div>' +
      '<p class="tcd-author-desc">' + AUTHOR_DESC + '</p>' +
      '</div>' +
      '</div>';
    return box;
  }

  // ===== Related Articles =====
  function loadRelatedArticles() {
    var grid = document.getElementById('tcd-related-grid');
    if (!grid) return;

    // Get current post categories
    var catLinks = document.querySelectorAll('a[rel="category tag"], .cat-links a, .post-categories a');
    var catSlugs = [];
    for (var i = 0; i < catLinks.length; i++) {
      var href = catLinks[i].href;
      var match = href.match(/\/category\/([^\/]+)/);
      if (match) catSlugs.push(match[1]);
    }

    // Fetch posts from same category
    var apiUrl = WP_API + '/posts?per_page=6&_embed&orderby=date&order=desc';
    if (catSlugs.length > 0) {
      // First get category IDs
      fetch(WP_API + '/categories?slug=' + catSlugs.join(','))
        .then(function (r) { return r.json(); })
        .then(function (cats) {
          if (cats.length > 0) {
            var catIds = cats.map(function (c) { return c.id; }).join(',');
            return fetch(apiUrl + '&categories=' + catIds);
          }
          return fetch(apiUrl);
        })
        .then(function (r) { return r.json(); })
        .then(function (posts) { renderRelated(grid, posts); })
        .catch(function () { grid.parentElement.style.display = 'none'; });
    } else {
      fetch(apiUrl)
        .then(function (r) { return r.json(); })
        .then(function (posts) { renderRelated(grid, posts); })
        .catch(function () { grid.parentElement.style.display = 'none'; });
    }
  }

  function renderRelated(grid, posts) {
    // Filter out current post
    var currentUrl = location.pathname;
    var filtered = posts.filter(function (p) {
      return new URL(p.link).pathname !== currentUrl;
    }).slice(0, 6);

    if (filtered.length === 0) {
      grid.parentElement.style.display = 'none';
      return;
    }

    var html = '';
    for (var i = 0; i < filtered.length; i++) {
      var p = filtered[i];
      var thumb = '';
      if (p._embedded && p._embedded['wp:featuredmedia'] && p._embedded['wp:featuredmedia'][0]) {
        var media = p._embedded['wp:featuredmedia'][0];
        var src = (media.media_details && media.media_details.sizes && media.media_details.sizes.medium)
          ? media.media_details.sizes.medium.source_url
          : media.source_url;
        thumb = '<img src="' + src + '" alt="" loading="lazy">';
      } else {
        thumb = '<div class="tcd-related-nothumb">\ud83d\udcdd</div>';
      }

      var date = new Date(p.date);
      var dateStr = date.getFullYear() + '.' +
        String(date.getMonth() + 1).padStart(2, '0') + '.' +
        String(date.getDate()).padStart(2, '0');

      html += '<a href="' + p.link + '" class="tcd-related-card">' +
        '<div class="tcd-related-thumb">' + thumb + '</div>' +
        '<div class="tcd-related-body">' +
        '<h4>' + p.title.rendered + '</h4>' +
        '<span class="tcd-related-date">' + dateStr + '</span>' +
        '</div></a>';
    }
    grid.innerHTML = html;
  }

  // ===== Floating Back to Top =====
  function createBackToTop() {
    var btn = el('button', 'tcd-totop');
    btn.innerHTML = '\u2191';
    btn.setAttribute('aria-label', '\u30da\u30fc\u30b8\u4e0a\u90e8\u306b\u623b\u308b');
    btn.style.display = 'none';
    document.body.appendChild(btn);

    btn.addEventListener('click', function () {
      window.scrollTo({ top: 0, behavior: 'smooth' });
    });

    window.addEventListener('scroll', function () {
      btn.style.display = window.scrollY > 300 ? 'flex' : 'none';
    }, { passive: true });
  }

  // ===== Mobile Floating TOC Button =====
  function createMobileTocButton(contentEl) {
    var headings = contentEl.querySelectorAll('h2, h3');
    if (headings.length < 3) return;

    // Create overlay
    var overlay = el('div', 'tcd-mtoc-overlay');
    overlay.style.display = 'none';
    var overlayInner = el('div', 'tcd-mtoc-inner');
    overlayInner.innerHTML = '<div class="tcd-mtoc-header"><span>\u76ee\u6b21</span><button class="tcd-mtoc-close">\u2715</button></div>';

    var list = el('ol', 'tcd-mtoc-list');
    for (var i = 0; i < headings.length; i++) {
      var h = headings[i];
      var id = h.id || 'tcd-h-' + i;
      var li = el('li', h.tagName === 'H3' ? 'tcd-mtoc-h3' : 'tcd-mtoc-h2',
        '<a href="#' + id + '">' + h.textContent + '</a>');
      list.appendChild(li);
    }
    overlayInner.appendChild(list);
    overlay.appendChild(overlayInner);
    document.body.appendChild(overlay);

    // Create floating button
    var btn = el('button', 'tcd-mtoc-btn');
    btn.innerHTML = '\u2630 \u76ee\u6b21';
    document.body.appendChild(btn);

    btn.addEventListener('click', function () {
      overlay.style.display = 'flex';
      document.body.style.overflow = 'hidden';
    });

    overlay.addEventListener('click', function (e) {
      if (e.target === overlay || e.target.classList.contains('tcd-mtoc-close')) {
        overlay.style.display = 'none';
        document.body.style.overflow = '';
      }
    });

    // Close on link click
    list.addEventListener('click', function (e) {
      if (e.target.tagName === 'A') {
        overlay.style.display = 'none';
        document.body.style.overflow = '';
      }
    });
  }

  // ===== Scroll Spy for Sidebar TOC =====
  function activateScrollSpy() {
    var tocLinks = document.querySelectorAll('.tcd-sidebar-toc-list a[data-toc-id]');
    if (tocLinks.length === 0) return;

    var headingEls = [];
    for (var i = 0; i < tocLinks.length; i++) {
      var target = document.getElementById(tocLinks[i].getAttribute('data-toc-id'));
      if (target) headingEls.push({ el: target, link: tocLinks[i] });
    }

    function updateActive() {
      var scrollY = window.scrollY + 100;
      var active = null;
      for (var i = 0; i < headingEls.length; i++) {
        if (headingEls[i].el.offsetTop <= scrollY) {
          active = headingEls[i];
        }
      }
      for (var j = 0; j < headingEls.length; j++) {
        headingEls[j].link.classList.remove('tcd-stoc-active');
      }
      if (active) active.link.classList.add('tcd-stoc-active');
    }

    window.addEventListener('scroll', updateActive, { passive: true });
    updateActive();
  }

})();
