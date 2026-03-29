import { Actor, log } from 'apify';
import { parse } from 'node-html-parser';

const DEFAULT_DELAY_MS = 3000;
const FETCH_TIMEOUT_MS = 30_000;
const MAX_RETRIES = 2;
const RETRY_DELAY_MS = 5_000;

await Actor.init();

// --- Input validation ---
const input = await Actor.getInput();
if (!input?.keywords || !Array.isArray(input.keywords) || input.keywords.length === 0) {
  throw new Error('Input must contain a non-empty "keywords" array.');
}

const {
  keywords,
  targetUrl = null,
  countryCode = 'us',
  languageCode = 'en',
  numResults = 10,
  includeFeatures = true,
  delayMs = DEFAULT_DELAY_MS,
} = input;

const normalizedTarget = targetUrl ? targetUrl.replace(/^https?:\/\//, '').replace(/\/$/, '').toLowerCase() : null;

const dataset = await Actor.openDataset();

// --- HTTP helper with retry ---
async function fetchWithRetry(url, headers = {}) {
  let lastError;
  for (let attempt = 0; attempt <= MAX_RETRIES; attempt++) {
    try {
      const controller = new AbortController();
      const timer = setTimeout(() => controller.abort(), FETCH_TIMEOUT_MS);
      try {
        const res = await fetch(url, {
          headers: {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': `${languageCode}-${countryCode.toUpperCase()},${languageCode};q=0.9`,
            ...headers,
          },
          signal: controller.signal,
          redirect: 'follow',
        });
        clearTimeout(timer);
        if (!res.ok) throw new Error(`HTTP ${res.status} ${res.statusText}`);
        return res;
      } finally {
        clearTimeout(timer);
      }
    } catch (e) {
      lastError = e;
      if (attempt < MAX_RETRIES) {
        log.warning(`Attempt ${attempt + 1} failed for ${url}: ${e.message}. Retrying in ${RETRY_DELAY_MS}ms...`);
        await new Promise((r) => setTimeout(r, RETRY_DELAY_MS));
      }
    }
  }
  throw lastError;
}

// --- Parse organic SERP results from Google HTML ---
function parseSerpResults(html, keyword, num) {
  const root = parse(html);
  const results = [];

  // Google organic result containers
  const resultDivs = root.querySelectorAll('div.g, div[data-hveid]');

  for (const div of resultDivs) {
    if (results.length >= num) break;

    const linkEl = div.querySelector('a[href^="http"]');
    const titleEl = div.querySelector('h3');
    const snippetEl = div.querySelector('div[data-sncf], div.VwiC3b, span.aCOpRe');

    if (!linkEl || !titleEl) continue;

    const url = linkEl.getAttribute('href');
    const title = titleEl.text.trim();
    const snippet = snippetEl ? snippetEl.text.trim() : '';

    if (!url || !title || url.includes('google.com')) continue;

    results.push({
      position: results.length + 1,
      url,
      title,
      snippet,
      domain: new URL(url).hostname.replace(/^www\./, ''),
    });
  }

  return results;
}

// --- Detect SERP features ---
function detectSerpFeatures(html) {
  const features = [];
  if (html.includes('data-attrid="FeaturedSnippet"') || html.includes('div.xpdopen') || html.includes('"featured_snippet"')) {
    features.push('featured_snippet');
  }
  if (html.includes('People also ask') || html.includes('related_questions')) {
    features.push('people_also_ask');
  }
  if (html.includes('g-section-with-header') || html.includes('"local_results"')) {
    features.push('local_pack');
  }
  if (html.includes('kp-blk') || html.includes('knowledge-panel')) {
    features.push('knowledge_panel');
  }
  if (html.includes('shopping-results') || html.includes('commercial-unit')) {
    features.push('shopping_ads');
  }
  return features;
}

// --- Main loop ---
log.info(`Starting SERP Checker — ${keywords.length} keyword(s), country: ${countryCode}, language: ${languageCode}`);

for (let i = 0; i < keywords.length; i++) {
  const keyword = keywords[i].trim();
  if (!keyword) {
    log.warning(`Skipping empty keyword at index ${i}`);
    continue;
  }

  const num = Math.min(Math.max(Number(numResults) || 10, 10), 100);
  const searchUrl = `https://www.google.com/search?q=${encodeURIComponent(keyword)}&num=${num}&hl=${languageCode}&gl=${countryCode}&pws=0&nfpr=1`;

  log.info(`[${i + 1}/${keywords.length}] Checking: "${keyword}"`);

  let success = false;
  let errorMessage = null;
  let organicResults = [];
  let serpFeatures = [];
  let targetRank = null;

  try {
    const res = await fetchWithRetry(searchUrl);
    const html = await res.text();

    organicResults = parseSerpResults(html, keyword, num);
    serpFeatures = includeFeatures ? detectSerpFeatures(html) : [];

    // Find target URL rank
    if (normalizedTarget) {
      const match = organicResults.find((r) => r.domain.includes(normalizedTarget) || r.url.toLowerCase().includes(normalizedTarget));
      targetRank = match ? match.position : null;
    }

    success = true;
    log.info(`  Found ${organicResults.length} results${targetRank !== null ? `, target at position ${targetRank}` : ''}`);
  } catch (e) {
    errorMessage = e.message;
    log.error(`  Failed to check "${keyword}": ${e.message}`);
  }

  await dataset.pushData({
    keyword,
    success,
    error: errorMessage,
    timestamp: new Date().toISOString(),
    searchUrl,
    countryCode,
    languageCode,
    targetUrl: targetUrl ?? null,
    targetRank,
    totalResults: organicResults.length,
    serpFeatures,
    organicResults,
  });

  // Delay between requests (skip after last keyword)
  if (i < keywords.length - 1) {
    await new Promise((r) => setTimeout(r, Math.max(1000, Number(delayMs) || DEFAULT_DELAY_MS)));
  }
}

log.info(`SERP Checker complete. ${keywords.length} keyword(s) processed.`);
await Actor.exit();
