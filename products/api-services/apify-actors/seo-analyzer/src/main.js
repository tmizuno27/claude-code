import { Actor, log } from 'apify';
import {
  extractTitle, extractMetaDescription, extractHeadings, extractImages,
  extractLinks, extractCanonical, extractRobotsMeta, extractOG,
  extractTwitterCard, extractJsonLd, extractWordCount, extractLanguage,
  extractViewport, extractFavicon, extractHreflang, calculateSeoScore,
} from './parser.js';

const FETCH_TIMEOUT_MS = 30_000;
const MAX_RETRIES = 2;
const RETRY_DELAY_MS = 2_000;

await Actor.init();

const input = await Actor.getInput();
if (!input?.urls || !Array.isArray(input.urls) || input.urls.length === 0) {
  throw new Error('Input must contain a non-empty "urls" array.');
}

const analysisType = input.analysisType || 'full';
const dataset = await Actor.openDataset();

async function fetchWithTimeout(url, options, timeoutMs = FETCH_TIMEOUT_MS) {
  const controller = new AbortController();
  const timer = setTimeout(() => controller.abort(), timeoutMs);
  try {
    const res = await fetch(url, { ...options, signal: controller.signal });
    return res;
  } finally {
    clearTimeout(timer);
  }
}

async function fetchPage(url) {
  let lastError;
  for (let attempt = 0; attempt <= MAX_RETRIES; attempt++) {
    try {
      const res = await fetchWithTimeout(url, {
        headers: {
          'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
          'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
          'Accept-Language': 'en-US,en;q=0.5',
        },
        redirect: 'follow',
      });
      if (!res.ok) throw new Error(`HTTP ${res.status}`);
      const html = await res.text();
      return { html, size: new TextEncoder().encode(html).length, finalUrl: res.url };
    } catch (e) {
      lastError = e;
      if (attempt < MAX_RETRIES) {
        log.warning(`Attempt ${attempt + 1} failed for ${url}: ${e.message}. Retrying...`);
        await new Promise((r) => setTimeout(r, RETRY_DELAY_MS));
      }
    }
  }
  throw lastError;
}

function fullAnalysis(html, url, size) {
  const title = extractTitle(html);
  const metaDescription = extractMetaDescription(html);
  const headings = extractHeadings(html);
  const images = extractImages(html);
  const links = extractLinks(html, url);
  const canonical = extractCanonical(html);
  const robotsMeta = extractRobotsMeta(html);
  const openGraph = extractOG(html);
  const twitterCard = extractTwitterCard(html);
  const jsonLd = extractJsonLd(html);
  const wordCount = extractWordCount(html);
  const language = extractLanguage(html);
  const viewport = extractViewport(html);
  const favicon = extractFavicon(html);
  const hreflang = extractHreflang(html);

  const data = {
    title, metaDescription, headings, images, links, canonical,
    robotsMeta, openGraph, twitterCard, jsonLd, wordCount,
    language, viewport, favicon, hreflang,
  };

  const seoScore = calculateSeoScore(data);
  return { url, pageSize: size, ...data, seoScore };
}

log.info(`Analyzing ${input.urls.length} URL(s) (mode: ${analysisType})...`);

for (const url of input.urls) {
  try {
    const parsed = new URL(url);
    if (!['http:', 'https:'].includes(parsed.protocol)) {
      await dataset.pushData({ url, success: false, error: 'URL must use http or https' });
      continue;
    }
  } catch {
    await dataset.pushData({ url, success: false, error: 'Invalid URL format' });
    continue;
  }

  try {
    log.info(`Analyzing: ${url}`);
    const { html, size, finalUrl } = await fetchPage(url);

    let result;
    switch (analysisType) {
      case 'score': {
        const analysis = fullAnalysis(html, finalUrl, size);
        result = { url: finalUrl, success: true, seoScore: analysis.seoScore };
        break;
      }
      case 'headings':
        result = { url: finalUrl, success: true, headings: extractHeadings(html) };
        break;
      case 'links':
        result = { url: finalUrl, success: true, links: extractLinks(html, finalUrl) };
        break;
      default:
        result = { success: true, ...fullAnalysis(html, finalUrl, size) };
    }

    await dataset.pushData(result);
  } catch (e) {
    log.warning(`Failed to analyze ${url}: ${e.message}`);
    await dataset.pushData({ url, success: false, error: e.message });
  }

  if (input.urls.length > 1) {
    await new Promise((r) => setTimeout(r, 1000));
  }
}

log.info('Done. All URLs analyzed.');
await Actor.exit();
