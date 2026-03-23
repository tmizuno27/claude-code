(() => {
  'use strict';

  // --- Settings ---
  const DEFAULT_SETTINGS = { theme: 'dark', indent: 2, collapsed: false };
  let settings = { ...DEFAULT_SETTINGS };
  let jsonData = null;
  let rawText = '';
  let isFormatted = true;

  // --- Detect JSON page ---
  function detectJSON() {
    const ct = document.contentType;
    if (ct && ct.includes('json')) return document.body.innerText;
    // Check if body contains only a <pre> with JSON
    const pre = document.querySelector('body > pre');
    if (pre && document.body.children.length === 1) {
      const txt = pre.textContent.trim();
      if ((txt.startsWith('{') && txt.endsWith('}')) || (txt.startsWith('[') && txt.endsWith(']'))) {
        return txt;
      }
    }
    return null;
  }

  function init() {
    const text = detectJSON();
    if (!text) return;
    rawText = text;
    try {
      jsonData = JSON.parse(text);
    } catch (e) {
      jsonData = null;
      renderError(e, text);
      notifyBackground(false);
      return;
    }
    chrome.storage.sync.get(DEFAULT_SETTINGS, (s) => {
      settings = { ...DEFAULT_SETTINGS, ...s };
      render();
      notifyBackground(true);
    });
  }

  function notifyBackground(valid) {
    try { chrome.runtime.sendMessage({ type: 'json-detected', valid }); } catch (_) {}
  }

  // --- Render ---
  function render() {
    document.body.innerHTML = '';
    document.body.className = 'jfp-root jfp-' + settings.theme;
    document.title = 'JSON Formatter Pro';

    // Toolbar
    const toolbar = el('div', 'jfp-toolbar');
    toolbar.appendChild(makeBtn('Copy Formatted', () => copyJSON(false)));
    toolbar.appendChild(makeBtn('Copy Minified', () => copyJSON(true)));
    toolbar.appendChild(makeBtn(isFormatted ? 'Raw' : 'Formatted', toggleRaw));
    toolbar.appendChild(makeBtn('Expand All', () => toggleAll(true)));
    toolbar.appendChild(makeBtn('Collapse All', () => toggleAll(false)));
    // Search
    const searchBox = el('input', 'jfp-search');
    searchBox.type = 'text';
    searchBox.placeholder = 'Search... (Ctrl+F)';
    searchBox.addEventListener('input', () => searchJSON(searchBox.value));
    toolbar.appendChild(searchBox);
    document.body.appendChild(toolbar);

    // Content
    const container = el('div', 'jfp-container');
    if (isFormatted) {
      container.appendChild(buildTree(jsonData, '$'));
    } else {
      const pre = el('pre', 'jfp-raw');
      pre.textContent = rawText;
      container.appendChild(pre);
    }
    document.body.appendChild(container);

    // Toast
    const toast = el('div', 'jfp-toast');
    toast.id = 'jfp-toast';
    document.body.appendChild(toast);

    // Keyboard shortcut
    document.addEventListener('keydown', (e) => {
      if ((e.ctrlKey || e.metaKey) && e.key === 'f') {
        e.preventDefault();
        searchBox.focus();
      }
    });
  }

  function renderError(err, text) {
    document.body.innerHTML = '';
    document.body.className = 'jfp-root jfp-dark';
    const wrapper = el('div', 'jfp-container');
    const errDiv = el('div', 'jfp-error');

    const match = err.message.match(/position\s+(\d+)/i);
    let pos = match ? parseInt(match[1]) : -1;

    errDiv.innerHTML = `<h2>JSON Parse Error</h2><p>${escapeHTML(err.message)}</p>`;

    const pre = el('pre', 'jfp-raw jfp-error-source');
    if (pos >= 0) {
      const before = escapeHTML(text.substring(Math.max(0, pos - 80), pos));
      const ch = escapeHTML(text.substring(pos, pos + 1) || ' ');
      const after = escapeHTML(text.substring(pos + 1, pos + 81));
      pre.innerHTML = before + '<span class="jfp-error-char">' + ch + '</span>' + after;
    } else {
      pre.textContent = text.substring(0, 500);
    }
    wrapper.appendChild(errDiv);
    wrapper.appendChild(pre);
    document.body.appendChild(wrapper);
  }

  // --- Tree builder ---
  function buildTree(data, path) {
    if (data === null) return valueSpan('null', 'jfp-null', path);
    if (typeof data === 'boolean') return valueSpan(String(data), 'jfp-bool', path);
    if (typeof data === 'number') return valueSpan(String(data), 'jfp-number', path);
    if (typeof data === 'string') return valueSpan('"' + escapeHTML(data) + '"', 'jfp-string', path);

    const isArr = Array.isArray(data);
    const keys = Object.keys(data);
    const block = el('span', 'jfp-block');

    const toggle = el('span', 'jfp-toggle');
    toggle.textContent = isArr ? '[' : '{';
    toggle.addEventListener('click', () => {
      const content = block.querySelector('.jfp-content');
      const collapsed = content.classList.toggle('jfp-collapsed');
      ellipsis.style.display = collapsed ? 'inline' : 'none';
      closeBracket.style.display = collapsed ? 'inline' : 'none';
    });
    block.appendChild(toggle);

    const ellipsis = el('span', 'jfp-ellipsis');
    ellipsis.textContent = ` ${keys.length} items `;
    ellipsis.style.display = 'none';
    block.appendChild(ellipsis);

    const content = el('div', 'jfp-content');
    keys.forEach((key, i) => {
      const line = el('div', 'jfp-line');
      const childPath = isArr ? `${path}[${key}]` : `${path}.${key}`;

      if (!isArr) {
        const keySpan = el('span', 'jfp-key');
        keySpan.textContent = '"' + key + '"';
        keySpan.setAttribute('data-path', childPath);
        keySpan.addEventListener('mouseenter', showPath);
        keySpan.addEventListener('mouseleave', hidePath);
        line.appendChild(keySpan);
        line.appendChild(document.createTextNode(': '));
      }

      line.appendChild(buildTree(data[key], childPath));
      if (i < keys.length - 1) line.appendChild(document.createTextNode(','));
      content.appendChild(line);
    });
    block.appendChild(content);

    const closeBracket = el('span', 'jfp-bracket');
    closeBracket.textContent = isArr ? ']' : '}';
    block.appendChild(closeBracket);

    return block;
  }

  function valueSpan(text, cls, path) {
    const s = el('span', cls);
    s.textContent = text;
    s.setAttribute('data-path', path);
    s.addEventListener('mouseenter', showPath);
    s.addEventListener('mouseleave', hidePath);
    return s;
  }

  // --- JSON Path tooltip ---
  let tooltip = null;
  function showPath(e) {
    const p = e.target.getAttribute('data-path');
    if (!p) return;
    if (!tooltip) {
      tooltip = el('div', 'jfp-tooltip');
      document.body.appendChild(tooltip);
    }
    tooltip.textContent = p;
    tooltip.style.display = 'block';
    const r = e.target.getBoundingClientRect();
    tooltip.style.left = r.left + 'px';
    tooltip.style.top = (r.top - 28 + window.scrollY) + 'px';
  }
  function hidePath() {
    if (tooltip) tooltip.style.display = 'none';
  }

  // --- Actions ---
  function copyJSON(minify) {
    const indent = minify ? undefined : settings.indent === 'tab' ? '\t' : settings.indent;
    const text = JSON.stringify(jsonData, null, indent);
    navigator.clipboard.writeText(text).then(() => showToast('Copied!'));
  }

  function toggleRaw() {
    isFormatted = !isFormatted;
    render();
  }

  function toggleAll(expand) {
    document.querySelectorAll('.jfp-content').forEach(c => {
      c.classList.toggle('jfp-collapsed', !expand);
    });
    document.querySelectorAll('.jfp-ellipsis').forEach(e => {
      e.style.display = expand ? 'none' : 'inline';
    });
  }

  function searchJSON(query) {
    document.querySelectorAll('.jfp-highlight').forEach(el => el.classList.remove('jfp-highlight'));
    if (!query) return;
    const lower = query.toLowerCase();
    document.querySelectorAll('.jfp-key, .jfp-string, .jfp-number, .jfp-bool, .jfp-null').forEach(el => {
      if (el.textContent.toLowerCase().includes(lower)) {
        el.classList.add('jfp-highlight');
        // Expand parents
        let parent = el.closest('.jfp-content');
        while (parent) {
          parent.classList.remove('jfp-collapsed');
          const prev = parent.previousElementSibling;
          if (prev && prev.classList.contains('jfp-ellipsis')) prev.style.display = 'none';
          parent = parent.parentElement?.closest('.jfp-content');
        }
      }
    });
  }

  function showToast(msg) {
    const t = document.getElementById('jfp-toast');
    if (!t) return;
    t.textContent = msg;
    t.classList.add('jfp-toast-show');
    setTimeout(() => t.classList.remove('jfp-toast-show'), 1500);
  }

  // --- Helpers ---
  function el(tag, cls) { const e = document.createElement(tag); if (cls) e.className = cls; return e; }
  function makeBtn(label, fn) { const b = el('button', 'jfp-btn'); b.textContent = label; b.addEventListener('click', fn); return b; }
  function escapeHTML(s) { return s.replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/"/g, '&quot;'); }

  // Listen for settings changes
  chrome.storage.onChanged.addListener((changes) => {
    for (const key of Object.keys(changes)) {
      settings[key] = changes[key].newValue;
    }
    if (jsonData) render();
  });

  init();
})();
