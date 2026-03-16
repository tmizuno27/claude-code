const API_PRIMARY = 'https://currency-exchange-api.t-mizuno27.workers.dev';
const API_FALLBACK = 'https://api.exchangerate-api.com/v4/latest/';
const CACHE_TTL = 3600000; // 1 hour

// Context menu
chrome.runtime.onInstalled.addListener(() => {
  chrome.contextMenus.create({
    id: 'convertCurrency',
    title: 'Convert "%s" to currency',
    contexts: ['selection']
  });
});

chrome.contextMenus.onClicked.addListener(async (info) => {
  if (info.menuItemId !== 'convertCurrency') return;
  const text = info.selectionText.trim();
  const match = text.match(/[\d,]+\.?\d*/);
  if (!match) return;

  const amount = parseFloat(match[0].replace(/,/g, ''));
  if (isNaN(amount)) return;

  const { settings = {} } = await chrome.storage.local.get('settings');
  const from = settings.defaultFrom || 'USD';
  const to = settings.defaultTo || 'JPY';

  const rate = await getRate(from, to);
  if (!rate) return;

  const result = (amount * rate).toFixed(2);
  // Send notification-style alert via badge
  chrome.action.setBadgeText({ text: '!' });
  chrome.action.setBadgeBackgroundColor({ color: '#10b981' });
  chrome.action.setTitle({ title: `${amount} ${from} = ${result} ${to}` });
  setTimeout(() => chrome.action.setBadgeText({ text: '' }), 5000);
});

async function getRate(from, to) {
  const cacheKey = `rate_${from}`;
  const cached = await chrome.storage.local.get(cacheKey);
  if (cached[cacheKey] && Date.now() - cached[cacheKey].timestamp < CACHE_TTL) {
    return cached[cacheKey].rates[to] || null;
  }

  let rates = null;
  try {
    const res = await fetch(`${API_PRIMARY}?base=${from}`);
    if (res.ok) {
      const data = await res.json();
      rates = data.rates || data;
    }
  } catch (e) { /* fall through */ }

  if (!rates) {
    try {
      const res = await fetch(`${API_FALLBACK}${from}`);
      if (res.ok) {
        const data = await res.json();
        rates = data.rates;
      }
    } catch (e) { /* fail silently */ }
  }

  if (rates) {
    await chrome.storage.local.set({
      [cacheKey]: { rates, timestamp: Date.now() }
    });
    return rates[to] || null;
  }
  return null;
}

// Expose getRate to popup via message
chrome.runtime.onMessage.addListener((msg, sender, sendResponse) => {
  if (msg.type === 'getRate') {
    getRate(msg.from, msg.to).then(rate => sendResponse({ rate }));
    return true;
  }
  if (msg.type === 'getRates') {
    getRate(msg.from, 'USD').then(async () => {
      const cacheKey = `rate_${msg.from}`;
      const cached = await chrome.storage.local.get(cacheKey);
      sendResponse({ rates: cached[cacheKey]?.rates || null });
    });
    return true;
  }
});
