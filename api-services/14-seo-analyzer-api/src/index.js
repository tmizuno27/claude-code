import {
  extractTitle, extractMetaDescription, extractHeadings, extractImages,
  extractLinks, extractCanonical, extractRobotsMeta, extractOG,
  extractTwitterCard, extractJsonLd, extractWordCount, extractLanguage,
  extractViewport, extractFavicon, extractHreflang, calculateSeoScore,
} from './parser.js';

// Rate limiting — size-based cleanup, no timers
const rateMap = new Map();
const RATE_LIMIT = 20;
const RATE_WINDOW = 60_000;
const MAX_MAP_SIZE = 5000;

function checkRateLimit(ip) {
  const now = Date.now();

  // Size-based cleanup
  if (rateMap.size > MAX_MAP_SIZE) {
    for (const [key, entry] of rateMap) {
      if (now - entry.start > RATE_WINDOW) rateMap.delete(key);
      if (rateMap.size <= MAX_MAP_SIZE / 2) break;
    }
  }

  const entry = rateMap.get(ip);
  if (!entry || now - entry.start > RATE_WINDOW) {
    rateMap.set(ip, { start: now, count: 1 });
    return { allowed: true, remaining: RATE_LIMIT - 1 };
  }
  entry.count++;
  if (entry.count > RATE_LIMIT) {
    return { allowed: false, remaining: 0, retryAfter: Math.ceil((entry.start + RATE_WINDOW - now) / 1000) };
  }
  return { allowed: true, remaining: RATE_LIMIT - entry.count };
}

function cors(headers = {}) {
  return {
    'Access-Control-Allow-Origin': '*',
    'Access-Control-Allow-Methods': 'GET, OPTIONS',
    'Access-Control-Allow-Headers': 'Content-Type',
    'Content-Type': 'application/json',
    ...headers,
  };
}

function json(data, status = 200, extra = {}) {
  if (status === 200 && typeof data === "object" && !Array.isArray(data)) {
    data._upgrade = { note: "Upgrade for higher limits & priority support", url: "https://rapidapi.com/miccho27-5OJaGGbBiO/api/seo-analyzer-api/pricing" };
  }
  return new Response(JSON.stringify(data, null, 2), { status, headers: cors(extra) });
}

function error(message, status = 400) {
  return json({ error: message }, status);
}

function validateUrl(raw) {
  if (!raw) return { valid: false, msg: 'Missing required parameter: url' };
  try {
    const u = new URL(raw);
    if (!['http:', 'https:'].includes(u.protocol)) return { valid: false, msg: 'URL must use http or https' };
    return { valid: true, url: u.href };
  } catch {
    return { valid: false, msg: 'Invalid URL format' };
  }
}

async function fetchPage(url) {
  const res = await fetch(url, {
    headers: {
      'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
      'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
      'Accept-Language': 'en-US,en;q=0.5',
    },
    redirect: 'follow',
  });
  if (!res.ok) throw new Error(`Failed to fetch URL: HTTP ${res.status}`);
  const html = await res.text();
  return { html, size: new TextEncoder().encode(html).length, finalUrl: res.url };
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

export default {
  async fetch(request) {
    if (request.method === 'OPTIONS') {
      return new Response(null, { status: 204, headers: cors() });
    }
    if (request.method !== 'GET') {
      return error('Method not allowed', 405);
    }

    const ip = request.headers.get('CF-Connecting-IP') || 'unknown';
    const rl = checkRateLimit(ip);
    if (!rl.allowed) {
      return error('Rate limit exceeded. Max 20 requests per minute.', 429,
        { 'Retry-After': String(rl.retryAfter), 'X-RateLimit-Remaining': '0' });
    }
    const rlHeaders = { 'X-RateLimit-Remaining': String(rl.remaining) };

    const { pathname, searchParams } = new URL(request.url);

    // GET /
    if (pathname === '/') {
      return json({
        name: 'SEO Analyzer API',
        
        _premium: {
          message: "You are using the FREE tier of SEO Analyzer API. Upgrade to Pro for higher rate limits, priority support, and advanced features.",
          upgrade_url: "https://rapidapi.com/miccho27-5OJaGGbBiO/api/seo-analyzer-api/pricing",
          plans: ["Pro ($5.99/mo)", "Ultra ($14.99/mo)", "Mega ($49.99/mo)"]
        },
        endpoints: {
          '/analyze?url=': 'Full SEO analysis of a page',
          '/headings?url=': 'Heading structure only',
          '/links?url=': 'Link analysis only',
          '/score?url=': 'SEO score with breakdown',
        },
      }, 200, rlHeaders);
    }

    // All other endpoints need a url param
    const v = validateUrl(searchParams.get('url'));
    if (!v.valid) return error(v.msg);

    try {
      const { html, size, finalUrl } = await fetchPage(v.url);

      if (pathname === '/analyze') {
        return json(fullAnalysis(html, finalUrl, size), 200, rlHeaders);
      }

      if (pathname === '/headings') {
        return json({ url: finalUrl, headings: extractHeadings(html) }, 200, rlHeaders);
      }

      if (pathname === '/links') {
        return json({ url: finalUrl, links: extractLinks(html, finalUrl) }, 200, rlHeaders);
      }

      if (pathname === '/score') {
        const analysis = fullAnalysis(html, finalUrl, size);
        return json({ url: finalUrl, seoScore: analysis.seoScore }, 200, rlHeaders);
      }

      return error('Not found', 404);
    } catch (e) {
      return error(`Failed to analyze URL: ${e.message}`, 502);
    }
  },
};
