const puppeteer = require('puppeteer');
const path = require('path');
const fs = require('fs');

const BASE = __dirname;
const STORE = path.join(BASE, 'store');

// Mock SEO data for realistic results display
const MOCK_DATA = {
  seoScore: {
    score: 85,
    checks: [
      { name: 'Title Tag', pass: true, weight: 15 },
      { name: 'Meta Description', pass: true, weight: 10 },
      { name: 'H1 Tag', pass: true, weight: 10 },
      { name: 'Image Alt Text', pass: false, weight: 5 },
      { name: 'Internal Links', pass: true, weight: 5 },
      { name: 'HTTPS', pass: true, weight: 10 },
      { name: 'Canonical URL', pass: true, weight: 5 },
      { name: 'Open Graph', pass: true, weight: 5 },
      { name: 'Viewport Meta', pass: true, weight: 5 },
      { name: 'Robots Meta', pass: true, weight: 5 },
    ]
  },
  title: { text: 'South American Life & Work Abroad Guide', length: 42, optimal: true },
  metaDescription: { text: 'Practical tips for living abroad in South America. Immigration, cost of living, remote work opportunities and more.', length: 118, optimal: true },
  wordCount: 2450,
  links: { total: 34, internal: 22, external: 12, nofollow: 3 },
  images: { total: 8, withAlt: 6, withoutAlt: 2, images: [{ src: '/img/hero.jpg', hasAlt: false }, { src: '/img/banner.png', hasAlt: false }] },
  headings: { counts: { h1: 1, h2: 5, h3: 8 }, texts: { h1: ['Living in South America'], h2: ['Cost of Living', 'Immigration Process', 'Remote Work', 'Education', 'Healthcare'] } },
  openGraph: { title: 'South American Life Guide', type: 'article', image: 'https://example.com/og.jpg' },
  twitterCard: { card: 'summary_large_image', title: 'South American Life Guide' },
  canonical: 'https://nambei-oyaji.com/guide',
  viewport: { present: true },
  favicon: { present: true },
  language: 'ja',
  robotsMeta: 'index, follow',
  jsonLd: [{ '@type': 'Article' }],
  pageSize: 85000,
};

async function generateScreenshot() {
  const browser = await puppeteer.launch({ headless: 'new', args: ['--no-sandbox'] });
  const page = await browser.newPage();
  await page.setViewport({ width: 1280, height: 800, deviceScaleFactor: 2 });

  const popupCss = fs.readFileSync(path.join(BASE, 'popup.css'), 'utf-8');
  const popupHtmlRaw = fs.readFileSync(path.join(BASE, 'popup.html'), 'utf-8');
  // Extract body content only
  const bodyMatch = popupHtmlRaw.match(/<body[^>]*>([\s\S]*)<\/body>/i);
  const popupBody = bodyMatch ? bodyMatch[1].replace(/<script[^>]*>[\s\S]*?<\/script>/gi, '') : '';
  const popupJs = fs.readFileSync(path.join(BASE, 'popup.js'), 'utf-8');

  const html = `<!DOCTYPE html>
<html><head><meta charset="UTF-8"><style>
* { margin: 0; padding: 0; box-sizing: border-box; }
body {
  width: 1280px; height: 800px;
  background: linear-gradient(135deg, #0a0a12 0%, #1a1025 40%, #0d1520 100%);
  font-family: -apple-system, BlinkMacSystemFont, 'SF Pro Text', 'Segoe UI', system-ui, sans-serif;
  color: #e8e8ed;
  display: flex;
  align-items: center;
  justify-content: center;
  overflow: hidden;
  position: relative;
}
/* Decorative gradient orbs */
.orb1 { position:absolute; width:400px; height:400px; border-radius:50%; background:radial-gradient(circle, rgba(10,132,255,0.15), transparent 70%); top:-100px; left:-100px; }
.orb2 { position:absolute; width:500px; height:500px; border-radius:50%; background:radial-gradient(circle, rgba(94,92,230,0.12), transparent 70%); bottom:-150px; right:-100px; }

.layout {
  display: flex;
  align-items: center;
  gap: 80px;
  padding: 0 80px;
  width: 100%;
}

.text-side {
  flex: 1;
  max-width: 480px;
}

.text-side .logo-row {
  display: flex;
  align-items: center;
  gap: 16px;
  margin-bottom: 24px;
}

.text-side .logo-icon {
  width: 56px; height: 56px;
  background: linear-gradient(135deg, #0a84ff, #5e5ce6);
  border-radius: 14px;
  display: flex; align-items: center; justify-content: center;
  color: #fff; font-size: 28px;
}

.text-side h1 {
  font-size: 48px;
  font-weight: 800;
  letter-spacing: -1.5px;
  line-height: 1.1;
  background: linear-gradient(135deg, #ffffff, #a0a0b0);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
}

.text-side .subtitle {
  font-size: 20px;
  color: #8e8e93;
  margin-top: 16px;
  line-height: 1.5;
}

.text-side .features {
  margin-top: 28px;
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.feature-item {
  display: flex;
  align-items: center;
  gap: 10px;
  font-size: 15px;
  color: #c8c8cd;
}

.feature-dot {
  width: 8px; height: 8px;
  border-radius: 50%;
  background: #0a84ff;
  flex-shrink: 0;
}

.popup-side {
  flex-shrink: 0;
  width: 380px;
}

.popup-frame {
  background: #0d0d0f;
  border-radius: 16px;
  border: 1px solid rgba(255,255,255,0.08);
  box-shadow: 0 20px 60px rgba(0,0,0,0.5), 0 0 0 1px rgba(255,255,255,0.05);
  overflow: hidden;
  max-height: 680px;
  overflow-y: auto;
}

/* Embed popup styles with scoping */
.popup-frame ${popupCss.replace(/body/g, '.popup-inner').replace(/380px/g, '100%').replace(/580px/g, 'none')}

.popup-inner {
  width: 100%;
  font-family: -apple-system, BlinkMacSystemFont, 'SF Pro Text', 'Segoe UI', system-ui, sans-serif;
  background: #0d0d0f;
  color: #e8e8ed;
  font-size: 13px;
  line-height: 1.5;
}
</style></head><body>
<div class="orb1"></div>
<div class="orb2"></div>
<div class="layout">
  <div class="text-side">
    <div class="logo-row">
      <div class="logo-icon">
        <svg width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><circle cx="11" cy="11" r="8"/><path d="m21 21-4.3-4.3"/></svg>
      </div>
    </div>
    <h1>SEO Inspector</h1>
    <p class="subtitle">Instant, comprehensive SEO analysis for any webpage — right from your browser.</p>
    <div class="features">
      <div class="feature-item"><div class="feature-dot"></div>One-click SEO score with detailed breakdown</div>
      <div class="feature-item"><div class="feature-dot"></div>Title, meta, headings & image analysis</div>
      <div class="feature-item"><div class="feature-dot"></div>Open Graph & Twitter Card validation</div>
      <div class="feature-item"><div class="feature-dot"></div>Technical SEO checks (canonical, robots, JSON-LD)</div>
      <div class="feature-item"><div class="feature-dot"></div>Beautiful dark UI with actionable insights</div>
    </div>
  </div>
  <div class="popup-side">
    <div class="popup-frame">
      <div class="popup-inner">
        ${popupBody}
      </div>
    </div>
  </div>
</div>
</body></html>`;

  await page.setContent(html, { waitUntil: 'domcontentloaded' });

  // Inject chrome mock and trigger popup logic
  await page.evaluate((mockData) => {
    const frame = document.querySelector('.popup-inner');
    // Set URL
    const urlText = frame.querySelector('#urlText');
    if (urlText) urlText.textContent = 'https://nambei-oyaji.com';

    // Helper
    const $ = (id) => frame.querySelector('#' + id);

    // Hide analyze button, show results
    const btn = $('analyzeBtn');
    if (btn) btn.style.display = 'none';
    const results = $('results');
    if (results) results.style.display = 'block';

    // Render score
    const score = mockData.seoScore.score;
    const circumference = 326.7;
    const ring = $('scoreRing');
    const num = $('scoreNumber');
    const color = score >= 80 ? '#30d158' : score >= 50 ? '#ff9f0a' : '#ff453a';
    if (ring) {
      ring.style.stroke = color;
      ring.style.strokeDashoffset = circumference - (circumference * score) / 100;
    }
    if (num) {
      num.textContent = score;
      num.style.color = color;
    }

    // Grade
    const grade = $('scoreGrade');
    if (grade) { grade.textContent = 'Good'; grade.style.color = '#30d158'; }

    // Quick stats
    const setText = (id, val) => { const el = $(id); if (el) el.textContent = val; };
    setText('statWords', '2.5K');
    setText('statLinks', '34');
    setText('statImages', '8');
    setText('statHeadings', '14');

    // Checks
    const checks = mockData.seoScore.checks;
    const sorted = [...checks].sort((a, b) => a.pass - b.pass);
    const checksList = $('checksList');
    if (checksList) {
      checksList.innerHTML = sorted.map(c => `
        <div class="check-item">
          <div class="check-icon ${c.pass ? 'pass' : 'fail'}">${c.pass ? '\u2713' : '\u2717'}</div>
          <span class="check-name">${c.name}</span>
          <span class="check-weight">${c.weight}pt</span>
        </div>
      `).join('');
    }

    // Detail cards - just title and meta for visible area
    function makeCard(el, title, badge, cls, body) {
      if (!el) return;
      el.innerHTML = `
        <div class="detail-header">
          <span class="detail-title">${title} <span class="detail-badge ${cls}">${badge}</span></span>
          <span class="detail-arrow">\u25B6</span>
        </div>
        <div class="detail-body" style="display:none">${body}</div>
      `;
    }
    makeCard($('detailTitle'), 'Title Tag', 'Optimal', 'badge-good', '<div class="detail-value">South American Life & Work Abroad Guide</div>');
    makeCard($('detailMeta'), 'Meta Description', 'Optimal', 'badge-good', '<div class="detail-value">Practical tips for living abroad...</div>');
    makeCard($('detailHeadings'), 'Headings', 'Good', 'badge-good', '<p>H1: 1, H2: 5, H3: 8</p>');
    makeCard($('detailImages'), 'Images', '2 Missing Alt', 'badge-warn', '<p>8 images, 6 with alt text</p>');
    makeCard($('detailLinks'), 'Links', '34 total', 'badge-good', '<p>22 internal, 12 external</p>');
    makeCard($('detailSocial'), 'Social Media', 'Complete', 'badge-good', '<p>OG + Twitter Card present</p>');
    makeCard($('detailTechnical'), 'Technical SEO', '7/7', 'badge-good', '<p>All checks passed</p>');
  }, MOCK_DATA);

  await new Promise(r => setTimeout(r, 500));
  await page.screenshot({ path: path.join(STORE, 'screenshot-1280x800.png'), clip: { x: 0, y: 0, width: 1280, height: 800 } });
  console.log('Generated: screenshot-1280x800.png');

  await browser.close();
}

async function generatePromoTile() {
  const browser = await puppeteer.launch({ headless: 'new', args: ['--no-sandbox'] });
  const page = await browser.newPage();
  await page.setViewport({ width: 440, height: 280, deviceScaleFactor: 2 });

  const html = `<!DOCTYPE html>
<html><head><meta charset="UTF-8"><style>
* { margin:0; padding:0; box-sizing:border-box; }
body {
  width: 440px; height: 280px;
  background: linear-gradient(135deg, #0a0a14 0%, #161028 50%, #0d1520 100%);
  font-family: -apple-system, BlinkMacSystemFont, 'SF Pro Text', 'Segoe UI', system-ui, sans-serif;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  position: relative;
  overflow: hidden;
}
.orb { position:absolute; border-radius:50%; }
.orb1 { width:300px; height:300px; background:radial-gradient(circle, rgba(10,132,255,0.15), transparent 70%); top:-120px; right:-80px; }
.orb2 { width:250px; height:250px; background:radial-gradient(circle, rgba(94,92,230,0.12), transparent 70%); bottom:-100px; left:-60px; }

.logo-icon {
  width: 64px; height: 64px;
  background: linear-gradient(135deg, #0a84ff, #5e5ce6);
  border-radius: 16px;
  display: flex; align-items: center; justify-content: center;
  color: #fff;
  margin-bottom: 20px;
  box-shadow: 0 8px 32px rgba(10,132,255,0.3);
}

h1 {
  font-size: 28px;
  font-weight: 800;
  letter-spacing: -0.5px;
  color: #fff;
  margin-bottom: 8px;
}

.subtitle {
  font-size: 16px;
  color: #8e8e93;
  font-weight: 500;
}
</style></head><body>
<div class="orb orb1"></div>
<div class="orb orb2"></div>
<div class="logo-icon">
  <svg width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><circle cx="11" cy="11" r="8"/><path d="m21 21-4.3-4.3"/></svg>
</div>
<h1>SEO Inspector</h1>
<p class="subtitle">Instant SEO Analysis</p>
</body></html>`;

  await page.setContent(html, { waitUntil: 'domcontentloaded' });
  await new Promise(r => setTimeout(r, 300));
  await page.screenshot({ path: path.join(STORE, 'promo-440x280.png'), clip: { x: 0, y: 0, width: 440, height: 280 } });
  console.log('Generated: promo-440x280.png');

  await browser.close();
}

async function generateMarquee() {
  const browser = await puppeteer.launch({ headless: 'new', args: ['--no-sandbox'] });
  const page = await browser.newPage();
  await page.setViewport({ width: 1400, height: 560, deviceScaleFactor: 2 });

  const html = `<!DOCTYPE html>
<html><head><meta charset="UTF-8"><style>
* { margin:0; padding:0; box-sizing:border-box; }
body {
  width: 1400px; height: 560px;
  background: linear-gradient(135deg, #0a0a14 0%, #161028 40%, #0d1520 100%);
  font-family: -apple-system, BlinkMacSystemFont, 'SF Pro Text', 'Segoe UI', system-ui, sans-serif;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 80px;
  padding: 0 100px;
  position: relative;
  overflow: hidden;
}
.orb { position:absolute; border-radius:50%; }
.orb1 { width:500px; height:500px; background:radial-gradient(circle, rgba(10,132,255,0.12), transparent 70%); top:-200px; left:-100px; }
.orb2 { width:400px; height:400px; background:radial-gradient(circle, rgba(94,92,230,0.10), transparent 70%); bottom:-150px; right:-50px; }

.left {
  flex: 1;
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.logo-row {
  display: flex;
  align-items: center;
  gap: 16px;
}

.logo-icon {
  width: 52px; height: 52px;
  background: linear-gradient(135deg, #0a84ff, #5e5ce6);
  border-radius: 13px;
  display: flex; align-items: center; justify-content: center;
  color: #fff;
  box-shadow: 0 6px 24px rgba(10,132,255,0.3);
}

h1 {
  font-size: 52px;
  font-weight: 800;
  letter-spacing: -1.5px;
  background: linear-gradient(135deg, #ffffff, #a0a0b0);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  line-height: 1.1;
}

.subtitle {
  font-size: 22px;
  color: #8e8e93;
  line-height: 1.4;
  max-width: 500px;
}

.badges {
  display: flex;
  gap: 12px;
  margin-top: 4px;
}
.badge {
  padding: 6px 16px;
  border-radius: 20px;
  font-size: 13px;
  font-weight: 600;
}
.badge-blue { background: rgba(10,132,255,0.15); color: #0a84ff; }
.badge-purple { background: rgba(94,92,230,0.15); color: #5e5ce6; }
.badge-green { background: rgba(48,209,88,0.15); color: #30d158; }

.right {
  flex-shrink: 0;
  position: relative;
}

/* Mini mockup of score */
.score-card {
  width: 280px;
  background: #0d0d0f;
  border-radius: 16px;
  border: 1px solid rgba(255,255,255,0.08);
  box-shadow: 0 20px 60px rgba(0,0,0,0.5);
  padding: 30px;
  text-align: center;
}

.score-circle-wrap {
  width: 140px; height: 140px;
  margin: 0 auto 16px;
  position: relative;
}
.score-circle-wrap svg {
  transform: rotate(-90deg);
  width: 140px; height: 140px;
}
.score-bg-ring { fill:none; stroke:#242429; stroke-width:10; }
.score-fg-ring { fill:none; stroke:#30d158; stroke-width:10; stroke-linecap:round;
  stroke-dasharray: 377; stroke-dashoffset: 56.55; }
.score-text {
  position: absolute; top: 50%; left: 50%;
  transform: translate(-50%,-50%);
  text-align: center;
}
.score-num { font-size: 44px; font-weight: 800; color: #30d158; display:block; line-height:1; }
.score-sub { font-size: 13px; color: #8e8e93; }

.mini-stats {
  display: flex; gap: 8px; margin-top: 12px;
}
.mini-stat {
  flex: 1;
  background: #1a1a1f;
  border-radius: 8px;
  padding: 8px 4px;
  text-align: center;
}
.mini-stat-val { font-size: 16px; font-weight:700; color:#e8e8ed; display:block; }
.mini-stat-lbl { font-size: 9px; color:#8e8e93; text-transform:uppercase; letter-spacing:0.5px; }
</style></head><body>
<div class="orb orb1"></div>
<div class="orb orb2"></div>
<div class="left">
  <div class="logo-row">
    <div class="logo-icon">
      <svg width="26" height="26" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><circle cx="11" cy="11" r="8"/><path d="m21 21-4.3-4.3"/></svg>
    </div>
  </div>
  <h1>SEO Inspector</h1>
  <p class="subtitle">Comprehensive SEO analysis for any webpage, instantly accessible from your browser toolbar.</p>
  <div class="badges">
    <div class="badge badge-blue">One-Click Analysis</div>
    <div class="badge badge-purple">10+ SEO Checks</div>
    <div class="badge badge-green">Free</div>
  </div>
</div>
<div class="right">
  <div class="score-card">
    <div class="score-circle-wrap">
      <svg viewBox="0 0 140 140">
        <circle class="score-bg-ring" cx="70" cy="70" r="60"/>
        <circle class="score-fg-ring" cx="70" cy="70" r="60"/>
      </svg>
      <div class="score-text">
        <span class="score-num">85</span>
        <span class="score-sub">/ 100</span>
      </div>
    </div>
    <div style="color:#30d158;font-weight:600;font-size:15px;">Good</div>
    <div class="mini-stats">
      <div class="mini-stat"><span class="mini-stat-val">2.5K</span><span class="mini-stat-lbl">Words</span></div>
      <div class="mini-stat"><span class="mini-stat-val">34</span><span class="mini-stat-lbl">Links</span></div>
      <div class="mini-stat"><span class="mini-stat-val">8</span><span class="mini-stat-lbl">Images</span></div>
      <div class="mini-stat"><span class="mini-stat-val">14</span><span class="mini-stat-lbl">Heads</span></div>
    </div>
  </div>
</div>
</body></html>`;

  await page.setContent(html, { waitUntil: 'domcontentloaded' });
  await new Promise(r => setTimeout(r, 300));
  await page.screenshot({ path: path.join(STORE, 'marquee-1400x560.png'), clip: { x: 0, y: 0, width: 1400, height: 560 } });
  console.log('Generated: marquee-1400x560.png');

  await browser.close();
}

(async () => {
  if (!fs.existsSync(STORE)) fs.mkdirSync(STORE, { recursive: true });
  await generateScreenshot();
  await generatePromoTile();
  await generateMarquee();
  console.log('\nAll store images generated in store/');
})();
