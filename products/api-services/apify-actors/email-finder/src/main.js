import { Actor, log } from 'apify';
import { extractEmails, extractPhones, extractSocialLinks, extractCompanyInfo } from './extractor.js';

await Actor.init();

const input = await Actor.getInput();
if (!input?.urls || !Array.isArray(input.urls) || input.urls.length === 0) {
  throw new Error('Input must contain a non-empty "urls" array.');
}

const scanDepth = input.scanDepth || 'homepage';
const includePhones = input.includePhones !== false;
const includeSocial = input.includeSocial !== false;
const dataset = await Actor.openDataset();

const HEADERS = {
  'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36',
  'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
  'Accept-Language': 'en-US,en;q=0.5',
};

const FETCH_TIMEOUT_MS = 30_000;
const MAX_RETRIES = 2;
const RETRY_DELAY_MS = 2_000;

const CONTACT_PATHS = ['/contact', '/contact-us', '/about', '/about-us', '/impressum', '/team'];

async function fetchPage(url) {
  let lastError;
  for (let attempt = 0; attempt <= MAX_RETRIES; attempt++) {
    const controller = new AbortController();
    const timer = setTimeout(() => controller.abort(), FETCH_TIMEOUT_MS);
    try {
      const res = await fetch(url, {
        headers: HEADERS,
        redirect: 'follow',
        signal: controller.signal,
      });
      clearTimeout(timer);
      if (!res.ok) throw new Error(`HTTP ${res.status}`);
      const contentType = res.headers.get('content-type') || '';
      if (!contentType.includes('text/html')) throw new Error('Not HTML');
      return res.text();
    } catch (e) {
      clearTimeout(timer);
      lastError = e;
      if (attempt < MAX_RETRIES) {
        log.warning(`Attempt ${attempt + 1} failed for ${url}: ${e.message}. Retrying...`);
        await new Promise((r) => setTimeout(r, RETRY_DELAY_MS));
      }
    }
  }
  throw lastError;
}

function delay(ms) {
  return new Promise((r) => setTimeout(r, ms));
}

function getBaseUrl(url) {
  const parsed = new URL(url);
  return `${parsed.protocol}//${parsed.host}`;
}

log.info(`Scanning ${input.urls.length} website(s) (depth: ${scanDepth})...`);

for (const url of input.urls) {
  try {
    const parsedUrl = new URL(url);
    if (!['http:', 'https:'].includes(parsedUrl.protocol)) {
      await dataset.pushData({ url, success: false, error: 'URL must use http or https' });
      continue;
    }
  } catch {
    await dataset.pushData({ url, success: false, error: 'Invalid URL' });
    continue;
  }

  log.info(`Scanning: ${url}`);
  const allEmails = new Set();
  const allPhones = new Set();
  const allSocial = {};
  let companyInfo = {};
  const pagesScanned = [];

  try {
    // Scan homepage
    const html = await fetchPage(url);
    pagesScanned.push(url);

    for (const email of extractEmails(html)) allEmails.add(email);
    if (includePhones) {
      for (const phone of extractPhones(html)) allPhones.add(phone);
    }
    if (includeSocial) {
      Object.assign(allSocial, extractSocialLinks(html));
    }
    companyInfo = extractCompanyInfo(html);

    // Scan contact/about pages if depth is 'deep'
    if (scanDepth === 'deep') {
      const baseUrl = getBaseUrl(url);
      for (const path of CONTACT_PATHS) {
        const contactUrl = `${baseUrl}${path}`;
        try {
          await delay(1000 + Math.random() * 1000);
          const contactHtml = await fetchPage(contactUrl);
          pagesScanned.push(contactUrl);

          for (const email of extractEmails(contactHtml)) allEmails.add(email);
          if (includePhones) {
            for (const phone of extractPhones(contactHtml)) allPhones.add(phone);
          }
          if (includeSocial) {
            const social = extractSocialLinks(contactHtml);
            for (const [key, value] of Object.entries(social)) {
              if (!allSocial[key]) allSocial[key] = value;
            }
          }
        } catch {
          // Contact page doesn't exist, skip silently
        }
      }
    }

    const result = {
      success: true,
      url,
      domain: new URL(url).hostname,
      emails: [...allEmails],
      emailCount: allEmails.size,
      ...(includePhones ? { phones: [...allPhones] } : {}),
      ...(includeSocial ? { socialLinks: allSocial } : {}),
      companyInfo,
      pagesScanned,
      scrapedAt: new Date().toISOString(),
    };

    await dataset.pushData(result);
  } catch (e) {
    log.warning(`Failed: ${url} - ${e.message}`);
    await dataset.pushData({ url, success: false, error: e.message });
  }

  await delay(1500 + Math.random() * 1500);
}

log.info('Done.');
await Actor.exit();
