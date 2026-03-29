import { Actor, log } from 'apify';

const FETCH_TIMEOUT_MS = 30_000;
const MAX_RETRIES = 2;
const RETRY_DELAY_MS = 2_000;

await Actor.init();

// --- Input validation ---
const input = await Actor.getInput();

const {
  sitemapUrls = [],
  websiteUrl = null,
  checkHttpStatus = false,
  filterPattern = null,
  maxUrls = 0,
  outputFormat = 'full',
} = input ?? {};

if (!sitemapUrls.length && !websiteUrl) {
  throw new Error('Input must contain either "sitemapUrls" (array) or "websiteUrl" (string) for auto-discovery.');
}

const filterRegex = filterPattern ? new RegExp(filterPattern, 'i') : null;
const dataset = await Actor.openDataset();
let totalExtracted = 0;

// --- HTTP helper ---
async function fetchText(url, method = 'GET') {
  let lastError;
  for (let attempt = 0; attempt <= MAX_RETRIES; attempt++) {
    try {
      const controller = new AbortController();
      const timer = setTimeout(() => controller.abort(), FETCH_TIMEOUT_MS);
      try {
        const res = await fetch(url, {
          method,
          headers: {
            'User-Agent': 'Mozilla/5.0 (compatible; SitemapCrawler/1.0)',
            'Accept': 'application/xml,text/xml,*/*',
          },
          signal: controller.signal,
          redirect: 'follow',
        });
        clearTimeout(timer);
        if (method === 'HEAD') return { ok: res.ok, status: res.status };
        if (!res.ok) throw new Error(`HTTP ${res.status}`);
        return { ok: true, status: res.status, text: await res.text() };
      } finally {
        clearTimeout(timer);
      }
    } catch (e) {
      lastError = e;
      if (attempt < MAX_RETRIES) {
        await new Promise((r) => setTimeout(r, RETRY_DELAY_MS));
      }
    }
  }
  throw lastError;
}

// --- Parse sitemap XML ---
function parseSitemapXml(xml) {
  const isSitemapIndex = xml.includes('<sitemapindex') || xml.includes('<sitemap>');
  const isUrlSet = xml.includes('<urlset');

  if (isSitemapIndex) {
    const locMatches = [...xml.matchAll(/<sitemap>[\s\S]*?<loc>(.*?)<\/loc>[\s\S]*?<\/sitemap>/gi)];
    const sitemaps = locMatches.map((m) => m[1].trim());
    return { type: 'index', sitemaps, urls: [] };
  }

  if (isUrlSet) {
    const urlMatches = [...xml.matchAll(/<url>([\s\S]*?)<\/url>/gi)];
    const urls = urlMatches.map((m) => {
      const block = m[1];
      const loc = (block.match(/<loc>(.*?)<\/loc>/i)?.[1] || '').trim();
      const lastmod = (block.match(/<lastmod>(.*?)<\/lastmod>/i)?.[1] || '').trim();
      const changefreq = (block.match(/<changefreq>(.*?)<\/changefreq>/i)?.[1] || '').trim();
      const priority = (block.match(/<priority>(.*?)<\/priority>/i)?.[1] || '').trim();
      return { loc, lastmod: lastmod || null, changefreq: changefreq || null, priority: priority || null };
    }).filter((u) => u.loc);
    return { type: 'urlset', sitemaps: [], urls };
  }

  // Try to extract any <loc> tags as fallback
  const locs = [...xml.matchAll(/<loc>(.*?)<\/loc>/gi)].map((m) => m[1].trim());
  return { type: 'unknown', sitemaps: [], urls: locs.map((loc) => ({ loc, lastmod: null, changefreq: null, priority: null })) };
}

// --- Auto-discover sitemaps from website URL ---
async function discoverSitemaps(baseUrl) {
  const discovered = new Set();
  const normalized = baseUrl.replace(/\/$/, '');

  // Try /sitemap.xml
  const candidates = [`${normalized}/sitemap.xml`, `${normalized}/sitemap_index.xml`];
  for (const candidate of candidates) {
    try {
      const { ok } = await fetchText(candidate, 'HEAD');
      if (ok) {
        discovered.add(candidate);
        log.info(`  Auto-discovered sitemap: ${candidate}`);
      }
    } catch (_) { /* not found */ }
  }

  // Try robots.txt
  try {
    const { text } = await fetchText(`${normalized}/robots.txt`);
    const sitemapMatches = [...text.matchAll(/^Sitemap:\s*(https?:\/\/\S+)/gim)];
    for (const m of sitemapMatches) {
      discovered.add(m[1].trim());
      log.info(`  Discovered from robots.txt: ${m[1].trim()}`);
    }
  } catch (_) { /* robots.txt not found */ }

  return [...discovered];
}

// --- Recursive sitemap processor ---
async function processSitemap(sitemapUrl, depth = 0) {
  if (maxUrls > 0 && totalExtracted >= maxUrls) return;
  if (depth > 5) {
    log.warning(`Max sitemap nesting depth reached for ${sitemapUrl}`);
    return;
  }

  log.info(`${'  '.repeat(depth)}Fetching sitemap: ${sitemapUrl}`);

  let xml;
  try {
    const result = await fetchText(sitemapUrl);
    xml = result.text;
  } catch (e) {
    log.error(`Failed to fetch sitemap ${sitemapUrl}: ${e.message}`);
    await dataset.pushData({ type: 'error', sitemapUrl, error: e.message });
    return;
  }

  const parsed = parseSitemapXml(xml);

  if (parsed.type === 'index') {
    log.info(`${'  '.repeat(depth)}  Sitemap index found — ${parsed.sitemaps.length} child sitemap(s)`);
    for (const childSitemap of parsed.sitemaps) {
      if (maxUrls > 0 && totalExtracted >= maxUrls) break;
      await processSitemap(childSitemap, depth + 1);
    }
    return;
  }

  // Process URL entries
  let urls = parsed.urls;
  if (filterRegex) {
    urls = urls.filter((u) => filterRegex.test(u.loc));
  }
  if (maxUrls > 0) {
    urls = urls.slice(0, maxUrls - totalExtracted);
  }

  log.info(`${'  '.repeat(depth)}  Found ${parsed.urls.length} URLs${filterRegex ? ` (${urls.length} after filter)` : ''}`);

  for (const urlEntry of urls) {
    let httpStatus = null;
    if (checkHttpStatus) {
      try {
        const result = await fetchText(urlEntry.loc, 'HEAD');
        httpStatus = result.status;
      } catch (e) {
        httpStatus = 0;
      }
    }

    const record = outputFormat === 'urls-only'
      ? { url: urlEntry.loc }
      : {
          url: urlEntry.loc,
          lastmod: urlEntry.lastmod,
          changefreq: urlEntry.changefreq,
          priority: urlEntry.priority ? parseFloat(urlEntry.priority) : null,
          sitemapSource: sitemapUrl,
          httpStatus: checkHttpStatus ? httpStatus : undefined,
        };

    await dataset.pushData(record);
    totalExtracted++;
  }
}

// --- Entry point ---
let urlsToProcess = [...sitemapUrls];

if (urlsToProcess.length === 0 && websiteUrl) {
  log.info(`Auto-discovering sitemaps for: ${websiteUrl}`);
  urlsToProcess = await discoverSitemaps(websiteUrl);
  if (urlsToProcess.length === 0) {
    throw new Error(`No sitemaps found for ${websiteUrl}. Try providing sitemap URLs directly.`);
  }
}

log.info(`Processing ${urlsToProcess.length} sitemap URL(s)...`);
for (const sitemapUrl of urlsToProcess) {
  await processSitemap(sitemapUrl);
}

log.info(`Sitemap Crawler complete. ${totalExtracted} URL(s) extracted.`);
await Actor.exit();
