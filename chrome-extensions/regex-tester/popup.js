(() => {
  const $ = s => document.querySelector(s);
  const regexInput = $('#regex-input');
  const testInput = $('#test-input');
  const highlightArea = $('#highlight-area');
  const matchList = $('#match-list');
  const regexError = $('#regex-error');

  // --- Flags ---
  const flagBtns = document.querySelectorAll('.flag');
  const getFlags = () => Array.from(flagBtns).filter(b => b.classList.contains('active')).map(b => b.dataset.flag).join('');
  flagBtns.forEach(b => b.addEventListener('click', () => { b.classList.toggle('active'); run(); }));

  // --- Presets ---
  const PRESETS = [
    { name: 'Email', pattern: '[a-zA-Z0-9._%+\\-]+@[a-zA-Z0-9.\\-]+\\.[a-zA-Z]{2,}' },
    { name: 'URL', pattern: 'https?:\\/\\/[\\w\\-]+(\\.[\\w\\-]+)+[\\/\\w\\-.~:/?#\\[\\]@!$&\'()*+,;=%]*' },
    { name: 'Phone (JP)', pattern: '0\\d{1,4}[\\-\\s]?\\d{1,4}[\\-\\s]?\\d{3,4}' },
    { name: 'Phone (Intl)', pattern: '\\+?\\d{1,3}[\\-\\s]?\\(?\\d{1,4}\\)?[\\-\\s]?\\d{1,4}[\\-\\s]?\\d{1,9}' },
    { name: 'IPv4', pattern: '(?:25[0-5]|2[0-4]\\d|[01]?\\d\\d?)\\.(?:25[0-5]|2[0-4]\\d|[01]?\\d\\d?)\\.(?:25[0-5]|2[0-4]\\d|[01]?\\d\\d?)\\.(?:25[0-5]|2[0-4]\\d|[01]?\\d\\d?)' },
    { name: 'Date (YYYY-MM-DD)', pattern: '\\d{4}[\\-/](?:0[1-9]|1[0-2])[\\-/](?:0[1-9]|[12]\\d|3[01])' },
    { name: 'Hex Color', pattern: '#(?:[0-9a-fA-F]{3}){1,2}\\b' },
    { name: 'HTML Tag', pattern: '<\\/?[a-zA-Z][a-zA-Z0-9]*[^>]*>' },
  ];

  // --- Panels ---
  const panelPresets = $('#panel-presets');
  const panelFavs = $('#panel-favorites');

  $('#btn-presets').addEventListener('click', () => {
    panelFavs.classList.add('hidden');
    panelPresets.classList.toggle('hidden');
    if (!panelPresets.classList.contains('hidden')) renderPresets();
  });
  $('#btn-favorites').addEventListener('click', () => {
    panelPresets.classList.add('hidden');
    panelFavs.classList.toggle('hidden');
    if (!panelFavs.classList.contains('hidden')) renderFavorites();
  });

  function renderPresets() {
    const list = $('#preset-list');
    list.innerHTML = '';
    PRESETS.forEach(p => {
      const el = document.createElement('div');
      el.className = 'preset-item';
      el.innerHTML = `<span class="preset-name">${p.name}</span><span class="preset-pattern">${escHtml(p.pattern)}</span>`;
      el.addEventListener('click', () => { regexInput.value = p.pattern; panelPresets.classList.add('hidden'); run(); });
      list.appendChild(el);
    });
  }

  // --- Favorites ---
  function loadFavorites(cb) {
    chrome.storage.local.get({ favorites: [] }, d => cb(d.favorites));
  }
  function saveFavorites(favs, cb) {
    chrome.storage.local.set({ favorites: favs }, cb);
  }

  $('#btn-save').addEventListener('click', () => {
    const pattern = regexInput.value.trim();
    if (!pattern) return;
    const flags = getFlags();
    const name = prompt('Name for this regex:', pattern.substring(0, 30));
    if (!name) return;
    loadFavorites(favs => {
      favs.push({ name, pattern, flags });
      saveFavorites(favs, () => {
        panelPresets.classList.add('hidden');
        panelFavs.classList.remove('hidden');
        renderFavorites();
      });
    });
  });

  function renderFavorites() {
    const list = $('#favorite-list');
    list.innerHTML = '';
    loadFavorites(favs => {
      if (!favs.length) { list.innerHTML = '<span class="muted">No saved patterns</span>'; return; }
      favs.forEach((f, i) => {
        const el = document.createElement('div');
        el.className = 'preset-item';
        el.innerHTML = `<span class="preset-name">${escHtml(f.name)}</span><span class="preset-pattern">${escHtml(f.pattern)}</span><button class="delete-btn" data-i="${i}">&times;</button>`;
        el.querySelector('.delete-btn').addEventListener('click', e => {
          e.stopPropagation();
          favs.splice(i, 1);
          saveFavorites(favs, () => renderFavorites());
        });
        el.addEventListener('click', () => {
          regexInput.value = f.pattern;
          // restore flags
          flagBtns.forEach(b => b.classList.remove('active'));
          if (f.flags) f.flags.split('').forEach(c => { const b = document.querySelector(`.flag[data-flag="${c}"]`); if (b) b.classList.add('active'); });
          panelFavs.classList.add('hidden');
          run();
        });
        list.appendChild(el);
      });
    });
  }

  // --- Core ---
  regexInput.addEventListener('input', run);
  testInput.addEventListener('input', run);

  function run() {
    const pattern = regexInput.value;
    const text = testInput.value;
    regexError.textContent = '';
    if (!pattern || !text) {
      highlightArea.textContent = text || '';
      matchList.innerHTML = '<span class="muted">No matches</span>';
      return;
    }

    let re;
    try {
      re = new RegExp(pattern, getFlags());
    } catch (e) {
      regexError.textContent = e.message;
      highlightArea.textContent = text;
      matchList.innerHTML = '<span class="muted">Invalid regex</span>';
      return;
    }

    // Collect matches
    const matches = [];
    if (re.global) {
      let m;
      while ((m = re.exec(text)) !== null) {
        matches.push({ index: m.index, match: m[0], groups: m.slice(1) });
        if (m[0].length === 0) re.lastIndex++;
        if (matches.length > 500) break;
      }
    } else {
      const m = re.exec(text);
      if (m) matches.push({ index: m.index, match: m[0], groups: m.slice(1) });
    }

    // Highlight
    if (!matches.length) {
      highlightArea.textContent = text;
      matchList.innerHTML = '<span class="muted">No matches</span>';
      return;
    }

    let html = '';
    let cursor = 0;
    matches.forEach((m, i) => {
      if (m.index > cursor) html += escHtml(text.slice(cursor, m.index));
      const cls = i % 2 === 0 ? 'hl' : 'hl-alt';
      html += `<span class="${cls}">${escHtml(m.match)}</span>`;
      cursor = m.index + m.match.length;
    });
    if (cursor < text.length) html += escHtml(text.slice(cursor));
    highlightArea.innerHTML = html;

    // Match list
    let listHtml = '';
    matches.forEach((m, i) => {
      listHtml += `<div class="match-item"><span class="match-index">#${i + 1}</span><span class="match-value">${escHtml(m.match)}</span>`;
      if (m.groups.length) {
        m.groups.forEach((g, gi) => {
          listHtml += `<br>&nbsp;&nbsp;<span class="group-label">Group ${gi + 1}:</span> <span class="group-value">${g !== undefined ? escHtml(g) : 'undefined'}</span>`;
        });
      }
      listHtml += '</div>';
    });
    matchList.innerHTML = listHtml;
  }

  function escHtml(s) {
    return s.replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/"/g, '&quot;');
  }
})();
