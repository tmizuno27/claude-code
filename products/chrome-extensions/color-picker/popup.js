// ── Color Conversion Utilities ──

function hexToRgb(hex) {
  hex = hex.replace('#', '');
  if (hex.length === 3) hex = hex.split('').map(c => c + c).join('');
  const n = parseInt(hex, 16);
  return { r: (n >> 16) & 255, g: (n >> 8) & 255, b: n & 255 };
}

function rgbToHex({ r, g, b }) {
  return '#' + [r, g, b].map(v => v.toString(16).padStart(2, '0')).join('');
}

function rgbToHsl({ r, g, b }) {
  r /= 255; g /= 255; b /= 255;
  const max = Math.max(r, g, b), min = Math.min(r, g, b);
  let h, s, l = (max + min) / 2;
  if (max === min) { h = s = 0; }
  else {
    const d = max - min;
    s = l > 0.5 ? d / (2 - max - min) : d / (max + min);
    switch (max) {
      case r: h = ((g - b) / d + (g < b ? 6 : 0)) / 6; break;
      case g: h = ((b - r) / d + 2) / 6; break;
      case b: h = ((r - g) / d + 4) / 6; break;
    }
  }
  return { h: Math.round(h * 360), s: Math.round(s * 100), l: Math.round(l * 100) };
}

function hslToRgb({ h, s, l }) {
  h /= 360; s /= 100; l /= 100;
  let r, g, b;
  if (s === 0) { r = g = b = l; }
  else {
    const hue2rgb = (p, q, t) => {
      if (t < 0) t += 1; if (t > 1) t -= 1;
      if (t < 1/6) return p + (q - p) * 6 * t;
      if (t < 1/2) return q;
      if (t < 2/3) return p + (q - p) * (2/3 - t) * 6;
      return p;
    };
    const q = l < 0.5 ? l * (1 + s) : l + s - l * s;
    const p = 2 * l - q;
    r = hue2rgb(p, q, h + 1/3);
    g = hue2rgb(p, q, h);
    b = hue2rgb(p, q, h - 1/3);
  }
  return { r: Math.round(r * 255), g: Math.round(g * 255), b: Math.round(b * 255) };
}

function rgbToCmyk({ r, g, b }) {
  r /= 255; g /= 255; b /= 255;
  const k = 1 - Math.max(r, g, b);
  if (k === 1) return { c: 0, m: 0, y: 0, k: 100 };
  return {
    c: Math.round((1 - r - k) / (1 - k) * 100),
    m: Math.round((1 - g - k) / (1 - k) * 100),
    y: Math.round((1 - b - k) / (1 - k) * 100),
    k: Math.round(k * 100)
  };
}

// ── Parse any color string ──

function parseColor(str) {
  str = str.trim().toLowerCase();
  // HEX
  const hexMatch = str.match(/^#?([0-9a-f]{3}|[0-9a-f]{6})$/);
  if (hexMatch) return hexToRgb(hexMatch[1]);
  // RGB
  const rgbMatch = str.match(/^rgba?\(\s*(\d+)\s*,\s*(\d+)\s*,\s*(\d+)/);
  if (rgbMatch) return { r: +rgbMatch[1], g: +rgbMatch[2], b: +rgbMatch[3] };
  // HSL
  const hslMatch = str.match(/^hsla?\(\s*(\d+)\s*,\s*(\d+)%?\s*,\s*(\d+)%?/);
  if (hslMatch) return hslToRgb({ h: +hslMatch[1], s: +hslMatch[2], l: +hslMatch[3] });
  return null;
}

// ── Contrast (WCAG) ──

function luminance({ r, g, b }) {
  const [rs, gs, bs] = [r, g, b].map(v => {
    v /= 255;
    return v <= 0.03928 ? v / 12.92 : Math.pow((v + 0.055) / 1.055, 2.4);
  });
  return 0.2126 * rs + 0.7152 * gs + 0.0722 * bs;
}

function contrastRatio(c1, c2) {
  const l1 = luminance(c1), l2 = luminance(c2);
  const lighter = Math.max(l1, l2), darker = Math.min(l1, l2);
  return (lighter + 0.05) / (darker + 0.05);
}

// ── Palette Generation ──

function generatePalette(rgb, type) {
  const hsl = rgbToHsl(rgb);
  let angles;
  switch (type) {
    case 'complementary': angles = [0, 180]; break;
    case 'analogous': angles = [-30, 0, 30]; break;
    case 'triadic': angles = [0, 120, 240]; break;
    case 'split': angles = [0, 150, 210]; break;
    default: angles = [0, 180];
  }
  return angles.map(a => {
    const h = (hsl.h + a + 360) % 360;
    return hslToRgb({ h, s: hsl.s, l: hsl.l });
  });
}

// ── Toast ──

function showToast(msg) {
  const t = document.getElementById('toast');
  t.textContent = msg;
  t.classList.add('show');
  setTimeout(() => t.classList.remove('show'), 1500);
}

// ── Clipboard ──

function copyText(text) {
  navigator.clipboard.writeText(text).then(() => showToast(`Copied: ${text}`));
}

// ── State ──

let currentRgb = null;
let savedColors = [];
let history = [];
let currentPaletteType = 'complementary';

// ── DOM ──

const $ = id => document.getElementById(id);

function formatStrings(rgb) {
  const hex = rgbToHex(rgb);
  const hsl = rgbToHsl(rgb);
  const cmyk = rgbToCmyk(rgb);
  return {
    hex: hex,
    rgb: `rgb(${rgb.r}, ${rgb.g}, ${rgb.b})`,
    hsl: `hsl(${hsl.h}, ${hsl.s}%, ${hsl.l}%)`,
    cmyk: `cmyk(${cmyk.c}%, ${cmyk.m}%, ${cmyk.y}%, ${cmyk.k}%)`
  };
}

function setColor(rgb) {
  currentRgb = rgb;
  const hex = rgbToHex(rgb);
  const f = formatStrings(rgb);

  $('colorPreview').style.background = hex;
  $('hexValue').textContent = f.hex;
  $('rgbValue').textContent = f.rgb;
  $('hslValue').textContent = f.hsl;
  $('cmykValue').textContent = f.cmyk;

  // Add to history
  addToHistory(hex);

  // Update palette
  renderGeneratedPalette();
}

function addToHistory(hex) {
  history = history.filter(c => c !== hex);
  history.unshift(hex);
  if (history.length > 10) history.pop();
  saveData();
  renderHistory();
}

function renderChips(container, colors, options = {}) {
  container.innerHTML = '';
  colors.forEach((hex, i) => {
    const chip = document.createElement('div');
    chip.className = 'chip';
    chip.style.background = hex;
    chip.title = hex;
    chip.addEventListener('click', () => {
      const rgb = hexToRgb(hex);
      setColor(rgb);
      copyText(hex);
    });
    if (options.removable) {
      const rm = document.createElement('button');
      rm.className = 'remove';
      rm.textContent = '\u00d7';
      rm.addEventListener('click', e => {
        e.stopPropagation();
        options.onRemove(i);
      });
      chip.appendChild(rm);
    }
    container.appendChild(chip);
  });
}

function renderSaved() {
  renderChips($('savedPalette'), savedColors, {
    removable: true,
    onRemove: i => { savedColors.splice(i, 1); saveData(); renderSaved(); }
  });
  $('savedCount').textContent = `${savedColors.length}/20`;
}

function renderHistory() {
  renderChips($('historyPalette'), history);
  $('historyCount').textContent = history.length;
}

function renderGeneratedPalette() {
  if (!currentRgb) return;
  const colors = generatePalette(currentRgb, currentPaletteType).map(rgbToHex);
  renderChips($('generatedPalette'), colors);
}

function saveData() {
  chrome.storage.local.set({ savedColors, history });
}

function loadData() {
  chrome.storage.local.get(['savedColors', 'history'], data => {
    savedColors = data.savedColors || [];
    history = data.history || [];
    renderSaved();
    renderHistory();
  });
}

// ── Event Listeners ──

// Pick color
$('pickBtn').addEventListener('click', async () => {
  if (!window.EyeDropper) {
    showToast('EyeDropper API not supported');
    return;
  }
  try {
    const dropper = new EyeDropper();
    const result = await dropper.open();
    setColor(hexToRgb(result.sRGBHex));
  } catch (e) {
    // User cancelled
  }
});

// Convert manual input
$('convertBtn').addEventListener('click', () => {
  const rgb = parseColor($('colorInput').value);
  if (rgb) setColor(rgb);
  else showToast('Invalid color format');
});

$('colorInput').addEventListener('keydown', e => {
  if (e.key === 'Enter') $('convertBtn').click();
});

// Copy buttons
document.querySelectorAll('.format-row').forEach(row => {
  const btn = row.querySelector('.copy-btn');
  const val = row.querySelector('.format-value');
  btn.addEventListener('click', () => {
    if (val.textContent !== '-') {
      copyText(val.textContent);
      btn.classList.add('copied');
      setTimeout(() => btn.classList.remove('copied'), 1000);
    }
  });
  val.addEventListener('click', () => {
    if (val.textContent !== '-') copyText(val.textContent);
  });
});

// Save color
$('saveColorBtn').addEventListener('click', () => {
  if (!currentRgb) { showToast('Pick a color first'); return; }
  const hex = rgbToHex(currentRgb);
  if (savedColors.includes(hex)) { showToast('Already saved'); return; }
  if (savedColors.length >= 20) { showToast('Max 20 colors'); return; }
  savedColors.push(hex);
  saveData();
  renderSaved();
  showToast('Color saved');
});

// Contrast check
function updateContrastChips() {
  const fg = parseColor($('fgInput').value);
  const bg = parseColor($('bgInput').value);
  if (fg) $('fgChip').style.background = rgbToHex(fg);
  if (bg) $('bgChip').style.background = rgbToHex(bg);
}

$('fgInput').addEventListener('input', updateContrastChips);
$('bgInput').addEventListener('input', updateContrastChips);

$('checkContrastBtn').addEventListener('click', () => {
  const fg = parseColor($('fgInput').value);
  const bg = parseColor($('bgInput').value);
  if (!fg || !bg) { showToast('Invalid color'); return; }
  const ratio = contrastRatio(fg, bg);
  const r = ratio.toFixed(2);
  const aaNormal = ratio >= 4.5;
  const aaLarge = ratio >= 3;
  const aaaNormal = ratio >= 7;
  const aaaLarge = ratio >= 4.5;
  $('contrastResult').innerHTML = `
    <div class="ratio">${r}:1</div>
    <div>AA Normal: <span class="${aaNormal ? 'pass' : 'fail'}">${aaNormal ? 'PASS' : 'FAIL'}</span></div>
    <div>AA Large: <span class="${aaLarge ? 'pass' : 'fail'}">${aaLarge ? 'PASS' : 'FAIL'}</span></div>
    <div>AAA Normal: <span class="${aaaNormal ? 'pass' : 'fail'}">${aaaNormal ? 'PASS' : 'FAIL'}</span></div>
    <div>AAA Large: <span class="${aaaLarge ? 'pass' : 'fail'}">${aaaLarge ? 'PASS' : 'FAIL'}</span></div>
  `;
});

// Palette type selection
document.querySelectorAll('.palette-type').forEach(btn => {
  btn.addEventListener('click', () => {
    document.querySelectorAll('.palette-type').forEach(b => b.classList.remove('active'));
    btn.classList.add('active');
    currentPaletteType = btn.dataset.type;
    renderGeneratedPalette();
  });
});

// ── Init ──
loadData();
