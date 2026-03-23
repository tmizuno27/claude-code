const API_BASE = 'https://seo-analyzer-api.t-mizuno27.workers.dev';

const $ = (id) => document.getElementById(id);

let currentUrl = '';

// ── Init ──
document.addEventListener('DOMContentLoaded', () => {
  chrome.tabs.query({ active: true, currentWindow: true }, (tabs) => {
    if (tabs[0]?.url) {
      currentUrl = tabs[0].url;
      $('urlText').textContent = currentUrl;
    } else {
      $('urlText').textContent = 'Unable to read URL';
      $('analyzeBtn').disabled = true;
    }
  });

  $('analyzeBtn').addEventListener('click', analyze);
  $('retryBtn').addEventListener('click', analyze);
});

// ── Analyze ──
async function analyze() {
  if (!currentUrl || !currentUrl.startsWith('http')) {
    showError('This page cannot be analyzed. Navigate to a website first.');
    return;
  }

  showLoading();

  try {
    const res = await fetch(`${API_BASE}/analyze?url=${encodeURIComponent(currentUrl)}`);
    if (!res.ok) {
      const err = await res.json().catch(() => ({}));
      throw new Error(err.error || `HTTP ${res.status}`);
    }
    const data = await res.json();
    renderResults(data);
  } catch (e) {
    showError(e.message || 'Failed to analyze. Please try again.');
  }
}

// ── States ──
function showLoading() {
  $('analyzeBtn').style.display = 'none';
  $('errorState').style.display = 'none';
  $('results').style.display = 'none';
  $('loadingState').style.display = 'block';
}

function showError(msg) {
  $('analyzeBtn').style.display = 'none';
  $('loadingState').style.display = 'none';
  $('results').style.display = 'none';
  $('errorState').style.display = 'block';
  $('errorMsg').textContent = msg;
}

function showResults() {
  $('analyzeBtn').style.display = 'none';
  $('loadingState').style.display = 'none';
  $('errorState').style.display = 'none';
  $('results').style.display = 'block';
}

// ── Render Results ──
function renderResults(data) {
  const score = data.seoScore?.score ?? 0;
  const checks = data.seoScore?.checks ?? [];

  // Score animation
  animateScore(score);

  // Grade
  const grade = getGrade(score);
  $('scoreGrade').textContent = grade.text;
  $('scoreGrade').style.color = grade.color;

  // Quick stats
  $('statWords').textContent = formatNum(data.wordCount || 0);
  $('statLinks').textContent = data.links?.total || 0;
  $('statImages').textContent = data.images?.total || 0;
  const totalHeadings = data.headings?.counts
    ? Object.values(data.headings.counts).reduce((a, b) => a + b, 0)
    : 0;
  $('statHeadings').textContent = totalHeadings;

  // Checks list
  renderChecks(checks);

  // Detail cards
  renderTitleDetail(data);
  renderMetaDetail(data);
  renderHeadingsDetail(data);
  renderImagesDetail(data);
  renderLinksDetail(data);
  renderSocialDetail(data);
  renderTechnicalDetail(data);

  showResults();
}

// ── Score Animation ──
function animateScore(score) {
  const circumference = 326.7;
  const ring = $('scoreRing');
  const num = $('scoreNumber');
  const color = score >= 80 ? 'var(--green)' : score >= 50 ? 'var(--orange)' : 'var(--red)';

  ring.style.stroke = color;
  num.style.color = color;

  let current = 0;
  const step = Math.ceil(score / 30);
  const timer = setInterval(() => {
    current = Math.min(current + step, score);
    num.textContent = current;
    const offset = circumference - (circumference * current) / 100;
    ring.style.strokeDashoffset = offset;
    if (current >= score) clearInterval(timer);
  }, 25);
}

function getGrade(score) {
  if (score >= 90) return { text: 'Excellent', color: 'var(--green)' };
  if (score >= 80) return { text: 'Good', color: 'var(--green)' };
  if (score >= 60) return { text: 'Needs Improvement', color: 'var(--orange)' };
  if (score >= 40) return { text: 'Poor', color: 'var(--yellow)' };
  return { text: 'Critical', color: 'var(--red)' };
}

function formatNum(n) {
  return n >= 1000 ? (n / 1000).toFixed(1) + 'K' : n.toString();
}

// ── Checks ──
function renderChecks(checks) {
  const sorted = [...checks].sort((a, b) => a.pass - b.pass);
  $('checksList').innerHTML = sorted.map(c => `
    <div class="check-item">
      <div class="check-icon ${c.pass ? 'pass' : 'fail'}">${c.pass ? '\u2713' : '\u2717'}</div>
      <span class="check-name">${c.name}</span>
      <span class="check-weight">${c.weight}pt</span>
    </div>
  `).join('');
}

// ── Detail Card Helper ──
function makeDetailCard(el, title, badge, badgeClass, bodyHtml) {
  el.innerHTML = `
    <div class="detail-header" onclick="this.parentElement.classList.toggle('open')">
      <span class="detail-title">${title}
        <span class="detail-badge ${badgeClass}">${badge}</span>
      </span>
      <span class="detail-arrow">\u25B6</span>
    </div>
    <div class="detail-body">${bodyHtml}</div>
  `;
}

// ── Title Detail ──
function renderTitleDetail(data) {
  const t = data.title || {};
  const len = t.length || 0;
  const badge = t.optimal ? 'Optimal' : len > 70 ? 'Too Long' : len < 30 ? 'Too Short' : 'OK';
  const cls = t.optimal ? 'badge-good' : 'badge-bad';
  makeDetailCard($('detailTitle'), 'Title Tag', badge, cls, `
    <div class="detail-value">${escHtml(t.text || 'Not found')}</div>
    <div class="detail-meta">
      <span>Length: ${len} chars</span>
      <span>Optimal: 30-60 chars</span>
    </div>
  `);
}

// ── Meta Description ──
function renderMetaDetail(data) {
  const m = data.metaDescription || {};
  const len = m.length || 0;
  const badge = m.optimal ? 'Optimal' : len === 0 ? 'Missing' : len > 160 ? 'Too Long' : 'Too Short';
  const cls = m.optimal ? 'badge-good' : len === 0 ? 'badge-bad' : 'badge-warn';
  makeDetailCard($('detailMeta'), 'Meta Description', badge, cls, `
    <div class="detail-value">${escHtml(m.text || 'Not found')}</div>
    <div class="detail-meta">
      <span>Length: ${len} chars</span>
      <span>Optimal: 120-160 chars</span>
    </div>
  `);
}

// ── Headings ──
function renderHeadingsDetail(data) {
  const h = data.headings || {};
  const counts = h.counts || {};
  const h1Count = counts.h1 || 0;
  const badge = h1Count === 1 ? 'Good' : h1Count === 0 ? 'Missing H1' : 'Multiple H1';
  const cls = h1Count === 1 ? 'badge-good' : 'badge-bad';

  let body = '<div style="margin-bottom:6px">';
  for (let i = 1; i <= 6; i++) {
    const count = counts[`h${i}`] || 0;
    if (count > 0) body += `<span style="margin-right:12px"><strong>H${i}:</strong> ${count}</span>`;
  }
  body += '</div>';

  const texts = h.texts || {};
  for (let i = 1; i <= 3; i++) {
    const items = texts[`h${i}`] || [];
    items.forEach(t => {
      body += `<div class="heading-item"><span class="heading-tag">H${i}</span><span class="heading-text">${escHtml(t)}</span></div>`;
    });
  }

  makeDetailCard($('detailHeadings'), 'Headings', badge, cls, body);
}

// ── Images ──
function renderImagesDetail(data) {
  const img = data.images || {};
  const total = img.total || 0;
  const noAlt = img.withoutAlt || 0;
  const badge = noAlt === 0 ? 'All Good' : `${noAlt} Missing Alt`;
  const cls = noAlt === 0 ? 'badge-good' : 'badge-warn';

  let body = `<p>${total} images found, ${img.withAlt || 0} with alt text</p>`;
  if (noAlt > 0) {
    const issues = (img.images || []).filter(i => !i.hasAlt).slice(0, 5);
    issues.forEach(i => {
      body += `<div class="img-issue">Missing alt: ${escHtml(i.src?.substring(0, 60) || 'unknown')}</div>`;
    });
    if (noAlt > 5) body += `<p style="color:var(--text2)">...and ${noAlt - 5} more</p>`;
  }

  makeDetailCard($('detailImages'), 'Images', badge, cls, body);
}

// ── Links ──
function renderLinksDetail(data) {
  const l = data.links || {};
  const badge = `${l.total || 0} total`;
  makeDetailCard($('detailLinks'), 'Links', badge, 'badge-good', `
    <div class="quick-stats" style="margin:6px 0">
      <div class="stat"><span class="stat-value">${l.internal || 0}</span><span class="stat-label">Internal</span></div>
      <div class="stat"><span class="stat-value">${l.external || 0}</span><span class="stat-label">External</span></div>
      <div class="stat"><span class="stat-value">${l.nofollow || 0}</span><span class="stat-label">Nofollow</span></div>
    </div>
  `);
}

// ── Social ──
function renderSocialDetail(data) {
  const og = data.openGraph || {};
  const tw = data.twitterCard || {};
  const hasOg = Object.keys(og).length > 0;
  const hasTw = Object.keys(tw).length > 0;
  const badge = hasOg && hasTw ? 'Complete' : hasOg || hasTw ? 'Partial' : 'Missing';
  const cls = hasOg && hasTw ? 'badge-good' : hasOg || hasTw ? 'badge-warn' : 'badge-bad';

  let body = '';
  if (hasOg) {
    body += '<p><strong>Open Graph</strong></p>';
    Object.entries(og).forEach(([k, v]) => {
      body += `<div class="detail-meta"><span>${k}</span><span style="color:var(--text)">${escHtml(String(v).substring(0, 50))}</span></div>`;
    });
  } else {
    body += '<p style="color:var(--red)">No Open Graph tags found</p>';
  }
  if (hasTw) {
    body += '<p style="margin-top:8px"><strong>Twitter Card</strong></p>';
    Object.entries(tw).forEach(([k, v]) => {
      body += `<div class="detail-meta"><span>${k}</span><span style="color:var(--text)">${escHtml(String(v).substring(0, 50))}</span></div>`;
    });
  } else {
    body += '<p style="margin-top:8px;color:var(--red)">No Twitter Card tags found</p>';
  }

  makeDetailCard($('detailSocial'), 'Social Media', badge, cls, body);
}

// ── Technical ──
function renderTechnicalDetail(data) {
  const items = [
    { label: 'Canonical', value: data.canonical || 'Not set', ok: !!data.canonical },
    { label: 'Viewport', value: data.viewport?.present ? 'Present' : 'Missing', ok: data.viewport?.present },
    { label: 'Favicon', value: data.favicon?.present ? 'Present' : 'Missing', ok: data.favicon?.present },
    { label: 'Language', value: data.language || 'Not set', ok: !!data.language },
    { label: 'Robots', value: data.robotsMeta || 'Not set', ok: data.robotsMeta !== 'noindex' },
    { label: 'JSON-LD', value: data.jsonLd?.length ? `${data.jsonLd.length} found` : 'None', ok: data.jsonLd?.length > 0 },
    { label: 'Page Size', value: data.pageSize ? `${(data.pageSize / 1024).toFixed(1)} KB` : '-', ok: true },
  ];

  const passCount = items.filter(i => i.ok).length;
  const badge = `${passCount}/${items.length}`;
  const cls = passCount === items.length ? 'badge-good' : passCount >= 5 ? 'badge-warn' : 'badge-bad';

  const body = items.map(i => `
    <div class="detail-meta" style="padding:3px 0">
      <span>${i.label}</span>
      <span style="color:${i.ok ? 'var(--green)' : 'var(--red)'}">${escHtml(String(i.value).substring(0, 60))}</span>
    </div>
  `).join('');

  makeDetailCard($('detailTechnical'), 'Technical SEO', badge, cls, body);
}

function escHtml(str) {
  const div = document.createElement('div');
  div.textContent = str;
  return div.innerHTML;
}
