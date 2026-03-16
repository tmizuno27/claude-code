const puppeteer = require('puppeteer');
const path = require('path');

const extensions = [
  {
    name: 'JSON Formatter Pro',
    dir: 'json-formatter',
    accent: '#3b82f6',
    icon: '{ }',
    tagline: 'Beautiful JSON formatting in your browser',
    features: ['Auto-detect & format JSON', 'Syntax highlighting', 'Collapsible tree view', 'JSON path on hover', 'Dark & Light themes', '100% local processing'],
  },
  {
    name: 'Quick Currency Converter',
    dir: 'currency-converter',
    accent: '#10b981',
    icon: '$',
    tagline: 'Real-time currency conversion at your fingertips',
    features: ['160+ currencies', 'Real-time exchange rates', 'One-click swap', 'Favorites & quick rates', 'Right-click conversion', 'Works offline (cached)'],
  },
  {
    name: 'Domain WHOIS Lookup',
    dir: 'whois-lookup',
    accent: '#8b5cf6',
    icon: '\u{1F310}',
    tagline: 'Instant domain intelligence in one click',
    features: ['WHOIS registration data', 'DNS records (A, MX, NS...)', 'SSL certificate info', 'Lookup history', 'One-click copy all', 'Privacy-friendly'],
  },
];

function buildHTML(ext, width, height, type) {
  const featureHTML = ext.features.map(f => `<div style="display:flex;align-items:center;gap:8px;font-size:${type === 'promo' ? 14 : 20}px;color:#ccc;"><span style="color:${ext.accent};">&#10003;</span> ${f}</div>`).join('');

  const iconSize = type === 'promo' ? 50 : type === 'marquee' ? 80 : 70;
  const titleSize = type === 'promo' ? 22 : type === 'marquee' ? 42 : 36;
  const tagSize = type === 'promo' ? 13 : type === 'marquee' ? 20 : 18;

  return `<!DOCTYPE html><html><head><meta charset="utf-8"><style>
    * { margin:0; padding:0; box-sizing:border-box; }
    body { width:${width}px; height:${height}px; background:linear-gradient(135deg, #0f172a 0%, #1e293b 50%, #0f172a 100%); display:flex; align-items:center; justify-content:center; font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,sans-serif; overflow:hidden; }
    .card { display:flex; flex-direction:column; align-items:center; justify-content:center; gap:${type === 'promo' ? 10 : 20}px; text-align:center; padding:${type === 'promo' ? 20 : 40}px; }
    .icon { font-size:${iconSize}px; color:${ext.accent}; text-shadow:0 0 40px ${ext.accent}44; }
    .title { font-size:${titleSize}px; font-weight:700; color:#fff; letter-spacing:-0.5px; }
    .tagline { font-size:${tagSize}px; color:#94a3b8; }
    .features { display:grid; grid-template-columns:1fr 1fr; gap:${type === 'promo' ? 4 : 10}px ${type === 'promo' ? 20 : 40}px; text-align:left; margin-top:${type === 'promo' ? 6 : 16}px; }
    .glow { position:absolute; width:300px; height:300px; border-radius:50%; background:${ext.accent}22; filter:blur(100px); }
    .glow1 { top:-100px; right:-50px; }
    .glow2 { bottom:-100px; left:-50px; }
  </style></head><body>
    <div class="glow glow1"></div>
    <div class="glow glow2"></div>
    <div class="card">
      <div class="icon">${ext.icon}</div>
      <div class="title">${ext.name}</div>
      <div class="tagline">${ext.tagline}</div>
      ${type !== 'promo' || true ? `<div class="features">${featureHTML}</div>` : ''}
    </div>
  </body></html>`;
}

(async () => {
  const browser = await puppeteer.launch({ headless: 'new', args: ['--no-sandbox'] });

  for (const ext of extensions) {
    const storeDir = path.join(__dirname, ext.dir, 'store');
    const sizes = [
      { w: 1280, h: 800, file: 'screenshot-1280x800.png', type: 'screenshot' },
      { w: 440, h: 280, file: 'promo-440x280.png', type: 'promo' },
      { w: 1400, h: 560, file: 'marquee-1400x560.png', type: 'marquee' },
    ];

    for (const { w, h, file, type } of sizes) {
      const page = await browser.newPage();
      await page.setViewport({ width: w, height: h, deviceScaleFactor: 1 });
      const html = buildHTML(ext, w, h, type);
      await page.setContent(html, { waitUntil: 'networkidle0' });
      await page.screenshot({ path: path.join(storeDir, file), type: 'png', omitBackground: false });
      await page.close();
      console.log(`Created: ${ext.dir}/store/${file}`);
    }
  }

  await browser.close();
  console.log('All images generated.');
})();
