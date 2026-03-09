/**
 * TCD-Style Single Article Enhancement v2.0
 * Works WITH existing Cocoon/WordPress template structure.
 * Adds: breadcrumbs, category label, meta info, TOC, SNS share,
 *       author info, related articles, floating buttons, scroll spy.
 */
(function () {
  if (!document.body.classList.contains('single')) return;

  var AUTHOR_NAME = '南米おやじ';
  var AUTHOR_DESC = 'パラグアイ・アスンシオン在住の日本人ブロガー。家族4人で2025年に南米移住。海外移住・海外生活のリアルを、実体験ベースで発信しています。';
  var AUTHOR_URL = 'https://nambei-oyaji.com/profile/';
  var SITE_NAME = '南米おやじの海外生活ラボ';

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

    // ===== 2. Category Label =====
    insertCategoryLabel(content);

    // ===== 3. Meta Info (date + tags) =====
    insertMetaInfo(content);

    // ===== 4. SNS share buttons (top) =====
    var topShare = createShareButtons('tcd-share tcd-share--top');
    var firstP = content.querySelector('p');
    if (firstP) {
      firstP.before(topShare);
    } else {
      content.prepend(topShare);
    }

    // ===== 5. TOC in content =====
    var tocBox = createTOC(content);
    if (tocBox) {
      // Insert after lead text (first 1-3 paragraphs)
      var paragraphs = content.querySelectorAll(':scope > p');
      var insertAfter = paragraphs.length >= 3 ? paragraphs[2] : (paragraphs[0] || null);
      if (insertAfter && insertAfter.nextElementSibling) {
        insertAfter.after(tocBox);
      } else {
        // fallback: before first h2
        var firstH2 = content.querySelector('h2');
        if (firstH2) firstH2.before(tocBox);
        else content.prepend(tocBox);
      }
    }

    // ===== 6. TOC in sidebar =====
    insertSidebarTOC(content);

    // ===== 7. SNS share buttons (bottom) =====
    var bottomShare = createShareButtons('tcd-share tcd-share--bottom');
    content.appendChild(bottomShare);

    // ===== 8. Author info =====
    var authorBox = createAuthorInfo();
    content.appendChild(authorBox);

    // ===== 9. Related articles =====
    insertRelatedArticles(content);

    // ===== 10. Floating elements =====
    createBackToTop();
    createMobileTocButton(content);

    // ===== 11. Scroll spy =====
    activateScrollSpy();

    // ===== 12. Enhance content elements =====
    enhanceContentElements(content);
  });

  // ===== Breadcrumbs =====
  function insertBreadcrumbs() {
    var main = document.querySelector('main, .main, #main, .site-main');
    if (!main) main = document.querySelector('.wp-block-group');
    if (!main) return;

    var catLinks = document.querySelectorAll('a[rel="category tag"], .wp-block-post-terms a, .cat-links a');
    var catName = '', catHref = '/';
    if (catLinks.length > 0) {
      catName = catLinks[0].textContent.trim();
      catHref = catLinks[0].href;
    }

    var titleText = document.title.split('|')[0].split('\u2013')[0].trim();
    var bc = el('nav', 'tcd-breadcrumb');
    bc.setAttribute('aria-label', 'パンくずリスト');
    var html = '<a href="/">ホーム</a>';
    html += ' <span class="tcd-bc-sep">›</span> <a href="/blog/">ブログ</a>';
    if (catName) {
      html += ' <span class="tcd-bc-sep">›</span> <a href="' + catHref + '">' + catName + '</a>';
    }
    html += ' <span class="tcd-bc-sep">›</span> <span class="tcd-bc-current">' + titleText + '</span>';
    bc.innerHTML = html;

    main.prepend(bc);
  }

  // ===== Category Label =====
  function insertCategoryLabel(contentEl) {
    var catLinks = document.querySelectorAll('a[rel="category tag"], .wp-block-post-terms a, .cat-links a');
    if (catLinks.length === 0) return;

    var label = el('a', 'tcd-cat-label');
    label.href = catLinks[0].href;
    label.textContent = catLinks[0].textContent.trim();
    contentEl.prepend(label);
  }

  // ===== Meta Info =====
  function insertMetaInfo(contentEl) {
    var meta = el('div', 'tcd-meta');

    // Date
    var dateEl = document.querySelector('.date, time, .post-date, .entry-date, .wp-block-post-date');
    var dateText = '';
    if (dateEl) {
      var timeEl = dateEl.querySelector('time') || dateEl;
      dateText = timeEl.getAttribute('datetime') || timeEl.textContent.trim();
      // Format as YYYY.MM.DD
      if (dateText) {
        var d = new Date(dateText);
        if (!isNaN(d.getTime())) {
          dateText = d.getFullYear() + '.' +
            String(d.getMonth() + 1).padStart(2, '0') + '.' +
            String(d.getDate()).padStart(2, '0');
        }
      }
    }
    if (dateText) {
      meta.innerHTML += '<span class="tcd-meta-date">' + dateText + '</span>';
    }

    // Tags
    var tagLinks = document.querySelectorAll('.tag-links a, a[rel="tag"], .wp-block-post-terms:not(:first-of-type) a');
    if (tagLinks.length > 0) {
      var tagsHtml = '<span class="tcd-meta-tags">';
      for (var i = 0; i < tagLinks.length && i < 5; i++) {
        tagsHtml += '<a href="' + tagLinks[i].href + '" class="tcd-meta-tag">' + tagLinks[i].textContent.trim() + '</a>';
      }
      tagsHtml += '</span>';
      meta.innerHTML += tagsHtml;
    }

    // Insert after category label or at top
    var catLabel = contentEl.querySelector('.tcd-cat-label');
    if (catLabel) {
      catLabel.after(meta);
    } else {
      contentEl.prepend(meta);
    }
  }

  // ===== TOC (in-content) =====
  function createTOC(contentEl) {
    var headings = contentEl.querySelectorAll('h2, h3, h4');
    if (headings.length < 3) return null;

    var toc = el('div', 'tcd-toc');
    var titleBar = el('div', 'tcd-toc-title');
    titleBar.innerHTML = '<span>目次</span><button class="tcd-toc-toggle" aria-label="目次を開閉">▼</button>';
    toc.appendChild(titleBar);

    var list = el('ol', 'tcd-toc-list');
    var currentH2Sub = null;
    var currentH3Sub = null;

    for (var i = 0; i < headings.length; i++) {
      var h = headings[i];
      if (!h.id) h.id = 'tcd-h-' + i;

      var li = el('li', '', '<a href="#' + h.id + '">' + h.textContent.trim() + '</a>');

      if (h.tagName === 'H2') {
        li.className = 'tcd-toc-h2';
        list.appendChild(li);
        currentH2Sub = null;
        currentH3Sub = null;
      } else if (h.tagName === 'H3') {
        if (!currentH2Sub) {
          currentH2Sub = el('ol', 'tcd-toc-sub');
          list.appendChild(currentH2Sub);
        }
        li.className = 'tcd-toc-h3';
        currentH2Sub.appendChild(li);
        currentH3Sub = null;
      } else if (h.tagName === 'H4') {
        // H4 nesting under H3
        var parentSub = currentH2Sub || list;
        if (!currentH3Sub) {
          currentH3Sub = el('ol', 'tcd-toc-sub');
          parentSub.appendChild(currentH3Sub);
        }
        li.className = 'tcd-toc-h3';
        li.style.paddingLeft = '12px';
        currentH3Sub.appendChild(li);
      }
    }
    toc.appendChild(list);

    titleBar.addEventListener('click', function () {
      toc.classList.toggle('tcd-toc--closed');
      titleBar.querySelector('.tcd-toc-toggle').textContent =
        toc.classList.contains('tcd-toc--closed') ? '▶' : '▼';
    });

    return toc;
  }

  // ===== Sidebar TOC =====
  function insertSidebarTOC(contentEl) {
    var sidebar = document.getElementById('nao-tcd-sidebar') ||
                  document.querySelector('.sidebar, #sidebar, aside');
    if (!sidebar) return;

    var headings = contentEl.querySelectorAll('h2, h3');
    if (headings.length < 3) return;

    var wrap = el('div', 'nao-tcd-widget tcd-sidebar-toc');
    var title = el('h4', 'nao-tcd-widget-title', '目次');
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

    var inner = sidebar.querySelector('.nao-tcd-sidebar-inner') || sidebar;
    inner.prepend(wrap);
  }

  // ===== SNS Share Buttons =====
  function createShareButtons(className) {
    var url = encodeURIComponent(location.href);
    var title = encodeURIComponent(document.title);
    var wrap = el('div', className);
    wrap.innerHTML =
      '<span class="tcd-share-label">シェア</span>' +
      '<div class="tcd-share-buttons">' +
      '<a href="https://twitter.com/intent/tweet?url=' + url + '&text=' + title + '" target="_blank" rel="noopener" class="tcd-share-btn tcd-share-x" aria-label="Xでシェア">X</a>' +
      '<a href="https://www.facebook.com/sharer/sharer.php?u=' + url + '" target="_blank" rel="noopener" class="tcd-share-btn tcd-share-fb" aria-label="Facebookでシェア">Facebook</a>' +
      '<a href="https://b.hatena.ne.jp/entry/' + location.href + '" target="_blank" rel="noopener" class="tcd-share-btn tcd-share-hatena" aria-label="はてブでシェア">はてブ</a>' +
      '<button class="tcd-share-btn tcd-share-copy" aria-label="URLをコピー">コピー</button>' +
      '</div>';

    setTimeout(function () {
      var copyBtn = wrap.querySelector('.tcd-share-copy');
      if (copyBtn) {
        copyBtn.addEventListener('click', function () {
          navigator.clipboard.writeText(location.href).then(function () {
            copyBtn.textContent = 'コピー済み';
            setTimeout(function () { copyBtn.textContent = 'コピー'; }, 2000);
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
      '<div class="tcd-author-avatar"><div class="tcd-author-avatar-fallback">🧑</div></div>' +
      '<div class="tcd-author-text">' +
      '<div class="tcd-author-label">この記事を書いた人</div>' +
      '<div class="tcd-author-name">' + AUTHOR_NAME + '</div>' +
      '<p class="tcd-author-desc">' + AUTHOR_DESC + '</p>' +
      '<a href="' + AUTHOR_URL + '" class="tcd-author-link">プロフィールを見る</a>' +
      '</div></div>';
    return box;
  }

  // ===== Related Articles =====
  function insertRelatedArticles(contentEl) {
    // Try to find existing related posts from Cocoon or WP
    var existingRelated = document.querySelector('.related-entries, .related-list, .wp-block-query');
    if (existingRelated) return; // Already has related articles

    // Create a placeholder section — actual content populated by WP/Cocoon
    var section = el('div', 'tcd-related');
    section.innerHTML = '<h3 class="tcd-related-title">関連記事</h3>' +
      '<div class="tcd-related-grid" id="tcd-related-grid"></div>';

    // Fetch related posts via WP REST API
    var catLinks = document.querySelectorAll('a[rel="category tag"], .cat-links a');
    if (catLinks.length === 0) return;

    var catSlug = catLinks[0].href.split('/').filter(Boolean).pop();
    var currentUrl = location.pathname;

    fetch('/wp-json/wp/v2/posts?per_page=7&_embed&categories_slug=' + catSlug)
      .then(function (r) { return r.ok ? r.json() : []; })
      .then(function (posts) {
        if (!posts || posts.length === 0) return;

        var grid = document.getElementById('tcd-related-grid');
        if (!grid) return;

        var count = 0;
        for (var i = 0; i < posts.length && count < 6; i++) {
          var p = posts[i];
          // Skip current post
          var postPath = new URL(p.link).pathname;
          if (postPath === currentUrl) continue;

          var thumb = '';
          try {
            thumb = p._embedded['wp:featuredmedia'][0].media_details.sizes.medium.source_url;
          } catch (e) { thumb = ''; }

          var dateObj = new Date(p.date);
          var dateStr = dateObj.getFullYear() + '.' +
            String(dateObj.getMonth() + 1).padStart(2, '0') + '.' +
            String(dateObj.getDate()).padStart(2, '0');

          var card = el('a', 'tcd-related-card');
          card.href = p.link;
          card.innerHTML =
            '<div class="tcd-related-card-thumb">' +
            (thumb ? '<img src="' + thumb + '" alt="" loading="lazy">' : '') +
            '</div>' +
            '<div class="tcd-related-card-body">' +
            '<div class="tcd-related-card-title">' + p.title.rendered + '</div>' +
            '<div class="tcd-related-card-date">' + dateStr + '</div>' +
            '</div>';
          grid.appendChild(card);
          count++;
        }

        if (count > 0) {
          contentEl.appendChild(section);
        }
      })
      .catch(function () { /* silently fail */ });
  }

  // ===== Floating Back to Top =====
  function createBackToTop() {
    var btn = el('button', 'tcd-totop');
    btn.innerHTML = '↑';
    btn.setAttribute('aria-label', 'ページ上部に戻る');
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
    overlayInner.innerHTML = '<div class="tcd-mtoc-header"><span>目次</span><button class="tcd-mtoc-close">✕</button></div>';

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
    btn.innerHTML = '☰ 目次';
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

    var ticking = false;
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
      ticking = false;
    }

    window.addEventListener('scroll', function () {
      if (!ticking) {
        requestAnimationFrame(update);
        ticking = true;
      }
    }, { passive: true });
    update();
  }

  // ===== Enhance Content Elements =====
  function enhanceContentElements(contentEl) {
    // Add smooth scroll offset for anchor links
    var style = document.createElement('style');
    style.textContent = 'html { scroll-padding-top: 80px; }';
    document.head.appendChild(style);

    // Add loading="lazy" to all content images
    var imgs = contentEl.querySelectorAll('img:not([loading])');
    for (var i = 0; i < imgs.length; i++) {
      imgs[i].setAttribute('loading', 'lazy');
    }

    // Wrap tables for horizontal scroll on mobile
    var tables = contentEl.querySelectorAll('table');
    for (var j = 0; j < tables.length; j++) {
      if (!tables[j].parentElement.classList.contains('tcd-table-wrap')) {
        var wrapper = el('div', 'tcd-table-wrap');
        wrapper.style.overflowX = 'auto';
        wrapper.style.webkitOverflowScrolling = 'touch';
        tables[j].parentNode.insertBefore(wrapper, tables[j]);
        wrapper.appendChild(tables[j]);
      }
    }
  }

})();
