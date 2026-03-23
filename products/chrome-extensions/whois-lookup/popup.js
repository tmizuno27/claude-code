const API_PRIMARY = 'https://whois-domain-lookup.t-mizuno27.workers.dev';
const API_FALLBACK = 'https://api.api-ninjas.com/v1/whois?domain=';
const DNS_API = 'https://dns.google/resolve';
const MAX_HISTORY = 10;

let currentDomain = '';
let collectedInfo = { whois: null, dns: null, ssl: null };

// --- Init ---
document.addEventListener('DOMContentLoaded', async () => {
  setupTabs();
  document.getElementById('btnCopy').addEventListener('click', copyAll);

  const [tab] = await chrome.tabs.query({ active: true, currentWindow: true });
  if (!tab?.url) return;

  try {
    currentDomain = new URL(tab.url).hostname.replace(/^www\./, '');
  } catch {
    document.getElementById('domainDisplay').textContent = 'Invalid URL';
    return;
  }

  document.getElementById('domainDisplay').textContent = currentDomain;
  addToHistory(currentDomain);

  fetchWhois(currentDomain);
  fetchDNS(currentDomain);
  fetchSSL(currentDomain);
  loadHistory();
});

// --- Tabs ---
function setupTabs() {
  document.querySelectorAll('.tab').forEach(btn => {
    btn.addEventListener('click', () => {
      document.querySelectorAll('.tab').forEach(b => b.classList.remove('active'));
      document.querySelectorAll('.tab-content').forEach(c => c.classList.remove('active'));
      btn.classList.add('active');
      document.getElementById(`tab-${btn.dataset.tab}`).classList.add('active');
    });
  });
}

// --- WHOIS ---
async function fetchWhois(domain) {
  const loading = document.getElementById('whoisLoading');
  const errorEl = document.getElementById('whoisError');
  const dataEl = document.getElementById('whoisData');

  try {
    let data = null;

    // Try primary API
    try {
      const res = await fetch(`${API_PRIMARY}?domain=${domain}`, { signal: AbortSignal.timeout(8000) });
      if (res.ok) {
        const json = await res.json();
        data = normalizeWhois(json, 'primary');
      }
    } catch {}

    // Fallback
    if (!data) {
      try {
        const res = await fetch(`${API_FALLBACK}${domain}`, { signal: AbortSignal.timeout(8000) });
        if (res.ok) {
          const json = await res.json();
          data = normalizeWhois(json, 'fallback');
        }
      } catch {}
    }

    if (!data) throw new Error('Could not fetch WHOIS data');

    collectedInfo.whois = data;
    loading.classList.add('hidden');
    dataEl.classList.remove('hidden');
    renderWhois(data, dataEl);
  } catch (e) {
    loading.classList.add('hidden');
    errorEl.classList.remove('hidden');
    errorEl.textContent = e.message;
  }
}

function normalizeWhois(json, source) {
  if (source === 'primary') {
    // Cloudflare Worker format - adapt as needed
    return {
      domain: json.domain_name || json.domainName || currentDomain,
      registrar: json.registrar || json.registrarName || 'N/A',
      creationDate: json.creation_date || json.createdDate || json.created || null,
      expirationDate: json.expiration_date || json.expiryDate || json.expires || null,
      updatedDate: json.updated_date || json.updatedDate || null,
      nameservers: json.name_servers || json.nameservers || json.nameServers || [],
      status: json.status || json.domain_status || json.domainStatus || [],
      registrant: json.registrant_name || json.registrant || json.registrantName || 'REDACTED',
      registrantOrg: json.registrant_organization || json.registrantOrganization || '',
      registrantCountry: json.registrant_country || json.registrantCountry || '',
    };
  }

  // api-ninjas format
  return {
    domain: json.name || currentDomain,
    registrar: json.registrar || 'N/A',
    creationDate: json.creation_date ? new Date(json.creation_date * 1000).toISOString() : null,
    expirationDate: json.expiration_date ? new Date(json.expiration_date * 1000).toISOString() : null,
    updatedDate: json.updated_date ? new Date(json.updated_date * 1000).toISOString() : null,
    nameservers: json.nameservers || [],
    status: [],
    registrant: 'N/A',
    registrantOrg: '',
    registrantCountry: '',
  };
}

function renderWhois(data, el) {
  const rows = [];

  rows.push(row('Domain', data.domain));
  rows.push(row('Registrar', data.registrar));

  if (data.creationDate) {
    const created = formatDate(data.creationDate);
    const age = calcAge(data.creationDate);
    rows.push(row('Created', `${created} <span class="age-badge">${age}</span>`));
  }

  if (data.expirationDate) {
    const exp = formatDate(data.expirationDate);
    const daysLeft = daysUntil(data.expirationDate);
    let cls = '';
    if (daysLeft < 0) cls = 'danger';
    else if (daysLeft < 30) cls = 'danger';
    else if (daysLeft < 90) cls = 'warn';
    else cls = 'success';
    rows.push(row('Expires', `<span class="${cls}">${exp} (${daysLeft < 0 ? 'EXPIRED' : daysLeft + ' days left'})</span>`));
  }

  if (data.updatedDate) rows.push(row('Updated', formatDate(data.updatedDate)));

  if (data.nameservers.length) {
    const ns = Array.isArray(data.nameservers) ? data.nameservers : [data.nameservers];
    rows.push(row('Nameservers', ns.join('<br>')));
  }

  if (data.status && data.status.length) {
    const st = Array.isArray(data.status) ? data.status : [data.status];
    rows.push(row('Status', st.map(s => s.split(' ')[0]).join('<br>')));
  }

  if (data.registrant && data.registrant !== 'N/A') rows.push(row('Registrant', data.registrant));
  if (data.registrantOrg) rows.push(row('Organization', data.registrantOrg));
  if (data.registrantCountry) rows.push(row('Country', data.registrantCountry));

  el.innerHTML = rows.join('');
}

// --- DNS ---
async function fetchDNS(domain) {
  const loading = document.getElementById('dnsLoading');
  const errorEl = document.getElementById('dnsError');
  const dataEl = document.getElementById('dnsData');

  try {
    const types = ['A', 'AAAA', 'MX', 'NS', 'TXT'];
    const results = {};

    await Promise.all(types.map(async type => {
      try {
        const res = await fetch(`${DNS_API}?name=${domain}&type=${type}`, { signal: AbortSignal.timeout(6000) });
        if (res.ok) {
          const json = await res.json();
          if (json.Answer) {
            results[type] = json.Answer.map(a => a.data);
          }
        }
      } catch {}
    }));

    collectedInfo.dns = results;
    loading.classList.add('hidden');

    if (Object.keys(results).length === 0) {
      errorEl.classList.remove('hidden');
      errorEl.textContent = 'No DNS records found';
      return;
    }

    dataEl.classList.remove('hidden');
    let html = '';
    for (const type of types) {
      if (!results[type]?.length) continue;
      html += `<div class="dns-section"><h3>${type} Records</h3>`;
      results[type].forEach(r => {
        html += `<div class="dns-record">${escapeHtml(r)}</div>`;
      });
      html += '</div>';
    }
    dataEl.innerHTML = html;
  } catch (e) {
    loading.classList.add('hidden');
    errorEl.classList.remove('hidden');
    errorEl.textContent = e.message;
  }
}

// --- SSL ---
async function fetchSSL(domain) {
  const loading = document.getElementById('sslLoading');
  const errorEl = document.getElementById('sslError');
  const dataEl = document.getElementById('sslData');

  try {
    // Use crt.sh for certificate transparency logs
    const res = await fetch(`https://crt.sh/?q=${domain}&output=json`, { signal: AbortSignal.timeout(8000) });

    if (!res.ok) throw new Error('Could not fetch SSL data');

    const certs = await res.json();

    if (!certs.length) throw new Error('No SSL certificates found');

    // Get most recent cert
    const cert = certs.sort((a, b) => new Date(b.not_before) - new Date(a.not_before))[0];

    const sslInfo = {
      issuer: cert.issuer_name || 'N/A',
      commonName: cert.common_name || domain,
      notBefore: cert.not_before,
      notAfter: cert.not_after,
      serialNumber: cert.serial_number || 'N/A',
    };

    collectedInfo.ssl = sslInfo;
    loading.classList.add('hidden');
    dataEl.classList.remove('hidden');

    const rows = [];
    rows.push(row('Common Name', escapeHtml(sslInfo.commonName)));
    rows.push(row('Issuer', escapeHtml(sslInfo.issuer)));
    rows.push(row('Valid From', formatDate(sslInfo.notBefore)));

    if (sslInfo.notAfter) {
      const dLeft = daysUntil(sslInfo.notAfter);
      let cls = dLeft < 30 ? 'danger' : dLeft < 90 ? 'warn' : 'success';
      rows.push(row('Valid Until', `<span class="${cls}">${formatDate(sslInfo.notAfter)} (${dLeft} days)</span>`));
    }

    rows.push(row('Serial', sslInfo.serialNumber));
    dataEl.innerHTML = rows.join('');
  } catch (e) {
    loading.classList.add('hidden');
    errorEl.classList.remove('hidden');
    errorEl.textContent = e.message;
  }
}

// --- History ---
async function addToHistory(domain) {
  const { whoisHistory = [] } = await chrome.storage.local.get('whoisHistory');
  const filtered = whoisHistory.filter(h => h.domain !== domain);
  filtered.unshift({ domain, date: new Date().toISOString() });
  await chrome.storage.local.set({ whoisHistory: filtered.slice(0, MAX_HISTORY) });
}

async function loadHistory() {
  const { whoisHistory = [] } = await chrome.storage.local.get('whoisHistory');
  const list = document.getElementById('historyList');

  if (!whoisHistory.length) {
    list.innerHTML = '<p class="empty-state">No history yet</p>';
    return;
  }

  list.innerHTML = whoisHistory.map(h => `
    <div class="history-item" data-domain="${escapeHtml(h.domain)}">
      <span class="history-domain">${escapeHtml(h.domain)}</span>
      <span class="history-date">${new Date(h.date).toLocaleDateString()}</span>
    </div>
  `).join('');

  list.querySelectorAll('.history-item').forEach(item => {
    item.addEventListener('click', () => {
      const domain = item.dataset.domain;
      currentDomain = domain;
      document.getElementById('domainDisplay').textContent = domain;

      // Reset and reload
      ['whoisData', 'dnsData', 'sslData'].forEach(id => {
        document.getElementById(id).classList.add('hidden');
        document.getElementById(id).innerHTML = '';
      });
      ['whoisError', 'dnsError', 'sslError'].forEach(id => {
        document.getElementById(id).classList.add('hidden');
      });
      ['whoisLoading', 'dnsLoading', 'sslLoading'].forEach(id => {
        document.getElementById(id).classList.remove('hidden');
      });

      // Switch to WHOIS tab
      document.querySelectorAll('.tab')[0].click();

      collectedInfo = { whois: null, dns: null, ssl: null };
      fetchWhois(domain);
      fetchDNS(domain);
      fetchSSL(domain);
    });
  });
}

// --- Copy ---
async function copyAll() {
  const btn = document.getElementById('btnCopy');
  let text = `=== WHOIS Lookup: ${currentDomain} ===\n\n`;

  if (collectedInfo.whois) {
    const w = collectedInfo.whois;
    text += `[WHOIS]\nDomain: ${w.domain}\nRegistrar: ${w.registrar}\n`;
    if (w.creationDate) text += `Created: ${formatDate(w.creationDate)} (${calcAge(w.creationDate)})\n`;
    if (w.expirationDate) text += `Expires: ${formatDate(w.expirationDate)}\n`;
    if (w.nameservers?.length) text += `Nameservers: ${w.nameservers.join(', ')}\n`;
    if (w.status?.length) text += `Status: ${(Array.isArray(w.status) ? w.status : [w.status]).join(', ')}\n`;
    text += '\n';
  }

  if (collectedInfo.dns) {
    text += '[DNS]\n';
    for (const [type, records] of Object.entries(collectedInfo.dns)) {
      if (records?.length) text += `${type}: ${records.join(', ')}\n`;
    }
    text += '\n';
  }

  if (collectedInfo.ssl) {
    const s = collectedInfo.ssl;
    text += `[SSL]\nIssuer: ${s.issuer}\nCommon Name: ${s.commonName}\n`;
    if (s.notBefore) text += `Valid From: ${formatDate(s.notBefore)}\n`;
    if (s.notAfter) text += `Valid Until: ${formatDate(s.notAfter)}\n`;
  }

  await navigator.clipboard.writeText(text);
  btn.textContent = 'Copied!';
  btn.classList.add('copied');
  setTimeout(() => {
    btn.textContent = 'Copy All Info';
    btn.classList.remove('copied');
  }, 1500);
}

// --- Helpers ---
function row(label, value) {
  return `<div class="data-row"><span class="data-label">${label}</span><span class="data-value">${value}</span></div>`;
}

function formatDate(d) {
  try {
    const date = new Date(d);
    if (isNaN(date)) return String(d);
    return date.toLocaleDateString('en-US', { year: 'numeric', month: 'short', day: 'numeric' });
  } catch { return String(d); }
}

function calcAge(d) {
  const created = new Date(d);
  if (isNaN(created)) return '';
  const now = new Date();
  const years = Math.floor((now - created) / (365.25 * 86400000));
  const months = Math.floor(((now - created) % (365.25 * 86400000)) / (30.44 * 86400000));
  if (years > 0) return `${years}y ${months}m`;
  return `${months}m`;
}

function daysUntil(d) {
  const target = new Date(d);
  if (isNaN(target)) return 999;
  return Math.floor((target - new Date()) / 86400000);
}

function escapeHtml(s) {
  const div = document.createElement('div');
  div.textContent = String(s);
  return div.innerHTML;
}
