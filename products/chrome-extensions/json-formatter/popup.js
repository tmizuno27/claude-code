const themeEl = document.getElementById('theme');
const indentEl = document.getElementById('indent');

chrome.storage.sync.get({ theme: 'dark', indent: 2 }, (s) => {
  themeEl.value = s.theme;
  indentEl.value = String(s.indent);
});

themeEl.addEventListener('change', () => {
  chrome.storage.sync.set({ theme: themeEl.value });
});

indentEl.addEventListener('change', () => {
  const v = indentEl.value;
  chrome.storage.sync.set({ indent: v === 'tab' ? 'tab' : parseInt(v) });
});
