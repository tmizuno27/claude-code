/**
 * TCD-Style Single Article Enhancement
 * Works WITH existing template structure (sidebar, 2-col grid).
 * Adds: breadcrumbs, TOC, SNS share, author info, floating buttons.
 */
(function () {
  if (!document.body.classList.contains('single')) return;

  var AUTHOR_NAME = '\u5357\u7c73\u304a\u3084\u3058';
  var AUTHOR_DESC = '\u30d1\u30e9\u30b0\u30a2\u30a4\u5728\u4f4f\u306e\u65e5\u672c\u4eba\u30d6\u30ed\u30ac\u30fc\u3002\u6d77\u5916\u79fb\u4f4f\u30fb\u6d77\u5916\u751f\u6d3b\u306e\u30ea\u30a2\u30eb\u3092\u767a\u4fe1\u4e2d\u3002\u30a2\u30b5\u30f3\u30b7\u30aa\u30f3\u304b\u3089\u304a\u5c4a\u3051\u3057\u307e\u3059\u3002';

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

    // ===== 1. Breadcrumbs =====
    insertBreadcrumbs();

    // ===== 2. TOC in content =====
    var tocBox = createTOC(content);
    if (tocBox) {
      // Insert after the first paragraph or at the beginning
      var firstP = content.querySelector('p');
      if (firstP && firstP.nextElementSibling) {
        firstP.after(tocBox);
      } else {
        content.prepend(tocBox);
      }
    }

    // ===== 3. TOC in sidebar =====
    insertSidebarTOC(content);

    // ===== 4. SNS share buttons =====
    var topShare = createShareButtons('tcd-share tcd-share--top');
    content.prepend(topShare);

    var bottomShare = createShareButtons('tcd-share tcd-share--bottom');
    content.appendChild(bottomShare);

    // ===== 5. Author info =====
    var authorBox = createAuthorInfo();
    content.appendChild(authorBox);

    // ===== 6. Floating elements =====
    createBackToTop();
    createMobileTocButton(content);

    // ===== 7. Scroll spy =====
    activateScrollSpy();
  });

  // ===== Breadcrumbs =====
  function insertBreadcrumbs() {
    var main = document.querySelector('main.wp-block-group');
    if (!main) return;

    var catLinks = document.querySelectorAll('a[rel="category tag"], .wp-block-post-terms a');
    var catName = '', catHref = '/';
    if (catLinks.length > 0) {
      catName = catLinks[0].textContent.trim();
      catHref = catLinks[0].href;
    }

    var titleText = document.title.split('|')[0].split('\u2013')[0].trim();
    var bc = el('nav', 'tcd-breadcrumb');
    var html = '<a href="/">\u30db\u30fc\u30e0</a>';
    if (catName) {
      html += ' <span class="tcd-bc-sep">\u203a</span> <a href="' + catHref + '">' + catName + '</a>';
    }
    html += ' <span class="tcd-bc-sep">\u203a</span> <span class="tcd-bc-current">' + titleText + '</span>';
    bc.innerHTML = html;

    main.prepend(bc);
  }

  // ===== TOC (in-content) =====
  function createTOC(contentEl) {
    var headings = contentEl.querySelectorAll('h2, h3');
    if (headings.length < 3) return null;

    var toc = el('div', 'tcd-toc');
    var titleBar = el('div', 'tcd-toc-title');
    titleBar.innerHTML = '<span>\u76ee\u6b21</span><button class="tcd-toc-toggle" aria-label="\u76ee\u6b21\u3092\u958b\u9589">\u25bc</button>';
    toc.appendChild(titleBar);

    var list = el('ol', 'tcd-toc-list');
    var currentSub = null;

    for (var i = 0; i < headings.length; i++) {
      var h = headings[i];
      if (!h.id) h.id = 'tcd-h-' + i;

      var li = el('li', '', '<a href="#' + h.id + '">' + h.textContent.trim() + '</a>');

      if (h.tagName === 'H2') {
        li.className = 'tcd-toc-h2';
        list.appendChild(li);
        currentSub = null;
      } else {
        if (!currentSub) {
          currentSub = el('ol', 'tcd-toc-sub');
          list.appendChild(currentSub);
        }
        li.className = 'tcd-toc-h3';
        currentSub.appendChild(li);
      }
    }
    toc.appendChild(list);

    titleBar.addEventListener('click', function () {
      toc.classList.toggle('tcd-toc--closed');
      titleBar.querySelector('.tcd-toc-toggle').textContent =
        toc.classList.contains('tcd-toc--closed') ? '\u25b6' : '\u25bc';
    });

    return toc;
  }

  // ===== Sidebar TOC =====
  function insertSidebarTOC(contentEl) {
    var sidebar = document.getElementById('nao-tcd-sidebar');
    if (!sidebar) return;

    var headings = contentEl.querySelectorAll('h2, h3');
    if (headings.length < 3) return;

    var wrap = el('div', 'nao-tcd-widget tcd-sidebar-toc');
    var title = el('h4', 'nao-tcd-widget-title', '\u76ee\u6b21');
    wrap.appendChild(title);

    var list = el('ol', 'tcd-sidebar-toc-list');
    var currentSub = null;

    for (var i = 0; i < headings.length; i++) {
      var h = headings[i];
      if (!h.id) h.id = 'tcd-h-' + i;

      var li = el('li', '', '<a href="#' + h.id + '" data-toc-id="' + h.id + '">' + h.textContent.trim() + '</a>');

      if (h.tagName === 'H2') {
        li.className = 'tcd-stoc-h2';
        list.appendChild(li);
        currentSub = null;
      } else {
        if (!currentSub) {
          currentSub = el('ol', 'tcd-stoc-sub');
          list.appendChild(currentSub);
        }
        li.className = 'tcd-stoc-h3';
        currentSub.appendChild(li);
      }
    }
    wrap.appendChild(list);

    // Insert TOC as first widget (after existing widgets)
    var inner = sidebar.querySelector('.nao-tcd-sidebar-inner');
    if (inner) {
      inner.prepend(wrap);
    } else {
      sidebar.prepend(wrap);
    }
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
      '<div class="tcd-author-avatar"><div class="tcd-author-avatar-fallback">\ud83e\uddd1</div></div>' +
      '<div class="tcd-author-text">' +
      '<div class="tcd-author-label">\u3053\u306e\u8a18\u4e8b\u3092\u66f8\u3044\u305f\u4eba</div>' +
      '<div class="tcd-author-name">' + AUTHOR_NAME + '</div>' +
      '<p class="tcd-author-desc">' + AUTHOR_DESC + '</p>' +
      '</div></div>';
    return box;
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

    var overlay = el('div', 'tcd-mtoc-overlay');
    overlay.style.display = 'none';
    var overlayInner = el('div', 'tcd-mtoc-inner');
    overlayInner.innerHTML = '<div class="tcd-mtoc-header"><span>\u76ee\u6b21</span><button class="tcd-mtoc-close">\u2715</button></div>';

    var list = el('ol', 'tcd-mtoc-list');
    for (var i = 0; i < headings.length; i++) {
      var h = headings[i];
      if (!h.id) h.id = 'tcd-h-' + i;
      var li = el('li', h.tagName === 'H3' ? 'tcd-mtoc-h3' : 'tcd-mtoc-h2',
        '<a href="#' + h.id + '">' + h.textContent.trim() + '</a>');
      list.appendChild(li);
    }
    overlayInner.appendChild(list);
    overlay.appendChild(overlayInner);
    document.body.appendChild(overlay);

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

    var items = [];
    for (var i = 0; i < tocLinks.length; i++) {
      var target = document.getElementById(tocLinks[i].getAttribute('data-toc-id'));
      if (target) items.push({ el: target, link: tocLinks[i] });
    }

    function update() {
      var scrollY = window.scrollY + 120;
      var active = null;
      for (var i = 0; i < items.length; i++) {
        if (items[i].el.offsetTop <= scrollY) active = items[i];
      }
      for (var j = 0; j < items.length; j++) {
        items[j].link.classList.remove('tcd-stoc-active');
      }
      if (active) active.link.classList.add('tcd-stoc-active');
    }

    window.addEventListener('scroll', update, { passive: true });
    update();
  }

})();
