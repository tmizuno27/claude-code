// ── Dictionaries ──

const DICT = {
  lorem: [
    'lorem', 'ipsum', 'dolor', 'sit', 'amet', 'consectetur', 'adipiscing', 'elit',
    'sed', 'do', 'eiusmod', 'tempor', 'incididunt', 'ut', 'labore', 'et', 'dolore',
    'magna', 'aliqua', 'enim', 'ad', 'minim', 'veniam', 'quis', 'nostrud',
    'exercitation', 'ullamco', 'laboris', 'nisi', 'aliquip', 'ex', 'ea', 'commodo',
    'consequat', 'duis', 'aute', 'irure', 'in', 'reprehenderit', 'voluptate',
    'velit', 'esse', 'cillum', 'fugiat', 'nulla', 'pariatur', 'excepteur', 'sint',
    'occaecat', 'cupidatat', 'non', 'proident', 'sunt', 'culpa', 'qui', 'officia',
    'deserunt', 'mollit', 'anim', 'id', 'est', 'laborum', 'pellentesque', 'habitant',
    'morbi', 'tristique', 'senectus', 'netus', 'malesuada', 'fames', 'ac', 'turpis',
    'egestas', 'vestibulum', 'tortor', 'quam', 'feugiat', 'vitae', 'ultricies',
    'augue', 'mauris', 'pharetra', 'nibh', 'venenatis', 'cras', 'justo', 'odio',
    'dapibus', 'facilisis', 'sociis', 'natoque', 'penatibus', 'magnis', 'dis',
    'parturient', 'montes', 'nascetur', 'ridiculus', 'mus', 'donec', 'blandit',
    'cursus', 'leo', 'maecenas', 'accumsan', 'lacus', 'vel', 'porta', 'condimentum'
  ],
  japanese: [
    'あいうえお', 'かきくけこ', 'さしすせそ', 'たちつてと', 'なにぬねの',
    'はひふへほ', 'まみむめも', 'やゆよ', 'らりるれろ', 'わをん',
    'これはダミーテキストです', '文章の体裁を確認するために使用します',
    'ここに本文が入ります', 'サンプルテキスト', 'テスト用の文章',
    '段落のレイアウトを確認', 'フォントサイズの調整', 'デザイン確認用',
    '仮のテキストを挿入', '実際の文章に差し替えてください',
    '見出しのスタイル確認', 'コンテンツ領域のテスト', '行間の調整を行う',
    '余白の確認に使用', 'レスポンシブデザインの検証', 'カラム幅のテスト',
    '文字の折り返し確認', 'テキストエリアの表示確認', '日本語組版のテスト',
    'ウェブページのモックアップ', 'プレースホルダーテキスト', '仮置きの文章',
    'デザインカンプ用', 'ワイヤーフレーム確認', 'プロトタイプ用テキスト'
  ],
  hipster: [
    'artisan', 'craft', 'authentic', 'sustainable', 'organic', 'small-batch',
    'handcrafted', 'curated', 'bespoke', 'vintage', 'retro', 'minimalist',
    'aesthetic', 'vegan', 'gluten-free', 'kombucha', 'avocado', 'toast',
    'cold-brew', 'single-origin', 'pour-over', 'fixie', 'vinyl', 'typewriter',
    'polaroid', 'succulent', 'terrarium', 'macrame', 'sourdough', 'fermented',
    'locally-sourced', 'farm-to-table', 'ethically-made', 'zero-waste',
    'upcycled', 'raw', 'activated', 'charcoal', 'matcha', 'turmeric',
    'plant-based', 'mindful', 'intentional', 'slow-living', 'hygge',
    'wabi-sabi', 'kinfolk', 'wanderlust', 'dreamcatcher', 'boho',
    'artisanal', 'microbrew', 'gastropub', 'speakeasy', 'reclaimed',
    'Edison-bulb', 'exposed-brick', 'industrial-chic', 'mid-century',
    'Scandinavian', 'japandi', 'biophilic', 'terrazzo', 'rattan'
  ]
};

// ── State ──

let state = {
  pattern: 'lorem',
  type: 'paragraphs',
  quantity: 3,
  html: false,
  output: ''
};

// ── Generators ──

function pick(arr) {
  return arr[Math.floor(Math.random() * arr.length)];
}

function generateWords(n, dict) {
  const words = [];
  for (let i = 0; i < n; i++) words.push(pick(dict));
  return words;
}

function capitalize(s) {
  return s.charAt(0).toUpperCase() + s.slice(1);
}

function generateSentence(dict) {
  const len = 6 + Math.floor(Math.random() * 10);
  const words = generateWords(len, dict);
  words[0] = capitalize(words[0]);
  return words.join(' ') + '.';
}

function generateParagraph(dict) {
  const count = 3 + Math.floor(Math.random() * 5);
  const sentences = [];
  for (let i = 0; i < count; i++) sentences.push(generateSentence(dict));
  return sentences.join(' ');
}

function generate() {
  const dict = DICT[state.pattern];
  const n = state.quantity;
  let parts = [];

  switch (state.type) {
    case 'paragraphs':
      for (let i = 0; i < n; i++) parts.push(generateParagraph(dict));
      if (state.html) {
        state.output = parts.map(p => `<p>${p}</p>`).join('\n\n');
      } else {
        state.output = parts.join('\n\n');
      }
      break;

    case 'sentences':
      for (let i = 0; i < n; i++) parts.push(generateSentence(dict));
      state.output = parts.join(' ');
      if (state.html) state.output = `<p>${state.output}</p>`;
      break;

    case 'words':
      state.output = generateWords(n, dict).join(' ');
      if (state.html) state.output = `<span>${state.output}</span>`;
      break;

    case 'list':
      for (let i = 0; i < n; i++) parts.push(generateSentence(dict));
      if (state.html) {
        state.output = '<ul>\n' + parts.map(p => `  <li>${p}</li>`).join('\n') + '\n</ul>';
      } else {
        state.output = parts.map((p, i) => `${i + 1}. ${p}`).join('\n');
      }
      break;
  }

  renderPreview();
}

function renderPreview() {
  const el = document.getElementById('preview');
  if (!state.output) {
    el.innerHTML = '<p class="placeholder">Click "Generate" to create text...</p>';
    return;
  }
  el.textContent = state.output;
}

function showToast(msg) {
  const t = document.getElementById('toast');
  t.textContent = msg;
  t.classList.add('show');
  setTimeout(() => t.classList.remove('show'), 1500);
}

// ── Segmented Control ──

function setupSegmented(groupId, stateKey) {
  const group = document.getElementById(groupId);
  group.addEventListener('click', e => {
    const btn = e.target.closest('.seg-btn');
    if (!btn) return;
    group.querySelectorAll('.seg-btn').forEach(b => b.classList.remove('active'));
    btn.classList.add('active');
    state[stateKey] = btn.dataset.value;
  });
}

// ── Init ──

document.addEventListener('DOMContentLoaded', () => {
  setupSegmented('patternGroup', 'pattern');
  setupSegmented('typeGroup', 'type');

  const slider = document.getElementById('quantity');
  const qVal = document.getElementById('quantityValue');
  slider.addEventListener('input', () => {
    state.quantity = parseInt(slider.value);
    qVal.textContent = slider.value;
  });

  document.getElementById('htmlToggle').addEventListener('change', e => {
    state.html = e.target.checked;
  });

  document.getElementById('generateBtn').addEventListener('click', generate);

  document.getElementById('copyBtn').addEventListener('click', () => {
    if (!state.output) return;
    navigator.clipboard.writeText(state.output).then(() => {
      showToast('Copied!');
    }).catch(() => {
      // Fallback
      const ta = document.createElement('textarea');
      ta.value = state.output;
      document.body.appendChild(ta);
      ta.select();
      document.execCommand('copy');
      document.body.removeChild(ta);
      showToast('Copied!');
    });
  });

  // Generate on load
  generate();
});
