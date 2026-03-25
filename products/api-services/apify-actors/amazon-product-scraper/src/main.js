import { Actor, log } from 'apify';
import { parseProductPage, parseSearchPage } from './parser.js';

await Actor.init();

const input = await Actor.getInput();
const mode = input?.mode || 'product';

if (mode === 'product') {
  if (!input?.urls || !Array.isArray(input.urls) || input.urls.length === 0) {
    throw new Error('Input must contain a non-empty "urls" array for product mode.');
  }
} else if (mode === 'search') {
  if (!input?.keywords || typeof input.keywords !== 'string') {
    throw new Error('Input must contain a "keywords" string for search mode.');
  }
} else {
  throw new Error('Mode must be "product" or "search".');
}

const marketplace = input.marketplace || 'com';
const maxResults = input.maxResults || 20;
const dataset = await Actor.openDataset();

const HEADERS = {
  'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36',
  'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
  'Accept-Language': 'en-US,en;q=0.5',
  'Accept-Encoding': 'gzip, deflate',
};

async function fetchPage(url) {
  const res = await fetch(url, { headers: HEADERS, redirect: 'follow' });
  if (!res.ok) throw new Error(`HTTP ${res.status}`);
  return res.text();
}

function delay(ms) {
  return new Promise((r) => setTimeout(r, ms));
}

if (mode === 'product') {
  log.info(`Scraping ${input.urls.length} product URL(s)...`);

  for (const url of input.urls) {
    try {
      if (!url.includes('amazon.')) {
        await dataset.pushData({ url, success: false, error: 'Not an Amazon URL' });
        continue;
      }
      log.info(`Scraping product: ${url}`);
      const html = await fetchPage(url);
      const product = parseProductPage(html, url);
      await dataset.pushData({ success: true, ...product });
    } catch (e) {
      log.warning(`Failed: ${url} - ${e.message}`);
      await dataset.pushData({ url, success: false, error: e.message });
    }
    await delay(2000 + Math.random() * 2000);
  }
} else {
  const searchUrl = `https://www.amazon.${marketplace}/s?k=${encodeURIComponent(input.keywords)}`;
  log.info(`Searching Amazon for: "${input.keywords}" (max ${maxResults} results)`);

  try {
    const html = await fetchPage(searchUrl);
    const results = parseSearchPage(html, marketplace, maxResults);
    log.info(`Found ${results.length} product(s).`);

    for (const product of results) {
      await dataset.pushData({ success: true, source: 'search', keyword: input.keywords, ...product });
    }
  } catch (e) {
    log.error(`Search failed: ${e.message}`);
    await dataset.pushData({ success: false, keyword: input.keywords, error: e.message });
  }
}

log.info('Done.');
await Actor.exit();
