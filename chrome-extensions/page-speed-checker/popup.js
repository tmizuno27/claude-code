const API = 'https://www.googleapis.com/pagespeedonline/v5/runPagespeed';
const CIRCUMFERENCE = 2 * Math.PI * 28; // r=28

let data = { mobile: null, desktop: null };
let currentStrategy = 'mobile';
let pageUrl = '';

// --- Init ---
document.addEventListener('DOMContentLoaded', () => {
  chrome.tabs.query({ active: true, currentWindow: true }, tabs => {
    pageUrl = tabs[0]?.url || '';
    document.getElementById('url-display').textContent = pageUrl;

    if (!pageUrl || pageUrl.startsWith('chrome://') || pageUrl.startsWith('chrome-extension://')) {
      showError('Cannot analyze this page.');
      return;
    }
    runAnalysis();
  });

  document.getElementById('retry-btn').addEventListener('click', runAnalysis);
  document.getElementById('copy-btn').addEventListener('click', copyResults);
  document.getElementById('share-btn').addEventListener('click', shareResults);

  document.querySelectorAll('.tab').forEach(tab => {
    tab.addEventListener('click', () => {
      document.querySelectorAll('.tab').forEach(t => t.classList.remove('active'));
      tab.classList.add('active');
      currentStrategy = tab.dataset.strategy;
      renderResults();
    });
  });
});

// --- Fetch ---
async function runAnalysis() {
  showLoading();
  data = { mobile: null, desktop: null };
  try {
    document.getElementById('loading-text').textContent = 'Analyzing mobile...';
    data.mobile = await fetchPSI('mobile');
    document.getElementById('loading-text').textContent = 'Analyzing desktop...';
    data.desktop = await fetchPSI('desktop');
    currentStrategy = 'mobile';
    document.querySelectorAll('.tab').forEach(t => t.classList.toggle('active', t.dataset.strategy === 'mobile'));
    renderResults();
    showResults();
  } catch (e) {
    showError(e.message || 'API request failed.');
  }
}

async function fetchPSI(strategy) {
  const url = `${API}?url=${encodeURIComponent(pageUrl)}&strategy=${strategy}&category=performance&category=accessibility&category=best-practices&category=seo`;
  const res = await fetch(url);
  if (!res.ok) throw new Error(`API error ${res.status}`);
  return res.json();
}

// --- Render ---
function renderResults() {
  const d = data[currentStrategy];
  if (!d) return;

  const cats = d.lighthouseResult.categories;
  const categories = [
    { key: 'performance', label: 'Perf' },
    { key: 'accessibility', label: 'A11y' },
    { key: 'best-practices', label: 'Best' },
    { key: 'seo', label: 'SEO' },
  ];

  const grid = document.getElementById('scores-grid');
  grid.innerHTML = categories.map(c => {
    const score = Math.round((cats[c.key]?.score || 0) * 100);
    return scoreCard(score, c.label);
  }).join('');

  renderCWV(d);
  renderOpportunities(d);
}

function scoreCard(score, label) {
  const cls = colorClass(score);
  const offset = CIRCUMFERENCE - (score / 100) * CIRCUMFERENCE;
  return `
    <div class="score-card">
      <div class="score-ring">
        <svg viewBox="0 0 64 64">
          <circle class="bg" cx="32" cy="32" r="28"/>
          <circle class="fg stroke-${cls}" cx="32" cy="32" r="28"
            stroke-dasharray="${CIRCUMFERENCE}"
            stroke-dashoffset="${offset}"/>
        </svg>
        <span class="score-value ${cls}">${score}</span>
      </div>
      <span class="score-label">${label}</span>
    </div>`;
}

function renderCWV(d) {
  const metrics = d.loadingExperience?.metrics || {};
  const audits = d.lighthouseResult?.audits || {};

  const items = [
    { name: 'LCP', value: getMetric(metrics, 'LARGEST_CONTENTFUL_PAINT_MS', audits, 'largest-contentful-paint'), unit: 'ms' },
    { name: 'INP', value: getMetric(metrics, 'INTERACTION_TO_NEXT_PAINT', audits, 'interaction-to-next-paint') || getMetric(metrics, 'FIRST_INPUT_DELAY_MS', audits, 'first-input-delay'), unit: 'ms' },
    { name: 'CLS', value: getMetricCLS(metrics, audits), unit: '' },
  ];

  document.getElementById('cwv').innerHTML = items.map(m => {
    const display = m.value !== null ? m.value : '--';
    const cls = cwvColor(m.name, typeof display === 'number' ? display : null);
    return `
      <div class="cwv-item">
        <div class="metric-name">${m.name}</div>
        <div class="metric-value ${cls}">${display}</div>
        <div class="metric-unit">${m.unit}</div>
      </div>`;
  }).join('');
}

function getMetric(fieldMetrics, fieldKey, audits, auditKey) {
  if (fieldMetrics[fieldKey]?.percentile != null) return fieldMetrics[fieldKey].percentile;
  const a = audits[auditKey];
  if (a?.numericValue != null) return Math.round(a.numericValue);
  return null;
}

function getMetricCLS(fieldMetrics, audits) {
  if (fieldMetrics['CUMULATIVE_LAYOUT_SHIFT_SCORE']?.percentile != null) {
    return (fieldMetrics['CUMULATIVE_LAYOUT_SHIFT_SCORE'].percentile / 100).toFixed(2);
  }
  const a = audits['cumulative-layout-shift'];
  if (a?.numericValue != null) return a.numericValue.toFixed(2);
  return null;
}

function renderOpportunities(d) {
  const audits = d.lighthouseResult?.audits || {};
  const opps = Object.values(audits)
    .filter(a => a.details?.type === 'opportunity' && a.details?.overallSavingsMs > 0)
    .sort((a, b) => b.details.overallSavingsMs - a.details.overallSavingsMs);

  const ul = document.getElementById('opportunities');
  if (!opps.length) {
    ul.innerHTML = '<li>No significant opportunities found.</li>';
    return;
  }
  ul.innerHTML = opps.map(o => {
    const ms = Math.round(o.details.overallSavingsMs);
    const sec = (ms / 1000).toFixed(1);
    return `<li><span>${o.title}</span><span class="savings">-${sec}s</span></li>`;
  }).join('');
}

// --- Helpers ---
function colorClass(score) {
  if (score >= 90) return 'green';
  if (score >= 50) return 'yellow';
  return 'red';
}

function cwvColor(name, val) {
  if (val === null) return '';
  if (name === 'LCP') return val <= 2500 ? 'green' : val <= 4000 ? 'yellow' : 'red';
  if (name === 'INP') return val <= 200 ? 'green' : val <= 500 ? 'yellow' : 'red';
  if (name === 'CLS') return parseFloat(val) <= 0.1 ? 'green' : parseFloat(val) <= 0.25 ? 'yellow' : 'red';
  return '';
}

// --- Copy / Share ---
function buildText() {
  const lines = [`Page Speed: ${pageUrl}\n`];
  ['mobile', 'desktop'].forEach(s => {
    const d = data[s];
    if (!d) return;
    const cats = d.lighthouseResult.categories;
    lines.push(`[${s.toUpperCase()}]`);
    lines.push(`  Perf: ${Math.round((cats.performance?.score||0)*100)} | A11y: ${Math.round((cats.accessibility?.score||0)*100)} | Best: ${Math.round((cats['best-practices']?.score||0)*100)} | SEO: ${Math.round((cats.seo?.score||0)*100)}`);
  });
  return lines.join('\n');
}

function copyResults() {
  navigator.clipboard.writeText(buildText()).then(() => {
    const btn = document.getElementById('copy-btn');
    btn.textContent = 'Copied!';
    setTimeout(() => btn.textContent = 'Copy Results', 1500);
  });
}

function shareResults() {
  if (navigator.share) {
    navigator.share({ title: 'Page Speed Results', text: buildText() }).catch(() => {});
  } else {
    copyResults();
  }
}

// --- Visibility ---
function showLoading() {
  document.getElementById('loading').classList.remove('hidden');
  document.getElementById('results').classList.add('hidden');
  document.getElementById('error').classList.add('hidden');
}

function showResults() {
  document.getElementById('loading').classList.add('hidden');
  document.getElementById('results').classList.remove('hidden');
}

function showError(msg) {
  document.getElementById('loading').classList.add('hidden');
  document.getElementById('results').classList.add('hidden');
  document.getElementById('error').classList.remove('hidden');
  document.getElementById('error-msg').textContent = msg;
}
