import { Actor, log } from 'apify';
import { parseSearchResults, parsePlaceDetails } from './parser.js';

await Actor.init();

const input = await Actor.getInput();
if (!input?.searchQuery && !input?.placeUrls) {
  throw new Error('Input must contain "searchQuery" (string) or "placeUrls" (array).');
}

const maxResults = input.maxResults || 20;
const includeReviews = input.includeReviews || false;
const language = input.language || 'en';
const dataset = await Actor.openDataset();

const HEADERS = {
  'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36',
  'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
  'Accept-Language': `${language},en;q=0.5`,
};

async function fetchPage(url) {
  const res = await fetch(url, { headers: HEADERS, redirect: 'follow' });
  if (!res.ok) throw new Error(`HTTP ${res.status}`);
  return res.text();
}

function delay(ms) {
  return new Promise((r) => setTimeout(r, ms));
}

if (input.searchQuery) {
  const query = encodeURIComponent(input.searchQuery);
  const searchUrl = `https://www.google.com/maps/search/${query}/?hl=${language}`;
  log.info(`Searching Google Maps: "${input.searchQuery}" (max ${maxResults})`);

  try {
    const html = await fetchPage(searchUrl);
    const places = parseSearchResults(html, maxResults);
    log.info(`Found ${places.length} place(s).`);

    for (const place of places) {
      if (includeReviews && place.detailUrl) {
        try {
          await delay(1500 + Math.random() * 1500);
          const detailHtml = await fetchPage(place.detailUrl);
          const details = parsePlaceDetails(detailHtml);
          await dataset.pushData({
            success: true,
            source: 'search',
            query: input.searchQuery,
            ...place,
            ...details,
          });
          continue;
        } catch (e) {
          log.warning(`Could not fetch details for ${place.name}: ${e.message}`);
        }
      }
      await dataset.pushData({
        success: true,
        source: 'search',
        query: input.searchQuery,
        ...place,
      });
    }
  } catch (e) {
    log.error(`Search failed: ${e.message}`);
    await dataset.pushData({ success: false, query: input.searchQuery, error: e.message });
  }
}

if (input.placeUrls) {
  log.info(`Scraping ${input.placeUrls.length} place URL(s)...`);

  for (const url of input.placeUrls) {
    try {
      if (!url.includes('google.com/maps')) {
        await dataset.pushData({ url, success: false, error: 'Not a Google Maps URL' });
        continue;
      }
      log.info(`Scraping: ${url}`);
      const html = await fetchPage(url);
      const details = parsePlaceDetails(html);
      await dataset.pushData({ success: true, url, ...details });
    } catch (e) {
      log.warning(`Failed: ${url} - ${e.message}`);
      await dataset.pushData({ url, success: false, error: e.message });
    }
    await delay(2000 + Math.random() * 2000);
  }
}

log.info('Done.');
await Actor.exit();
