import { parseMetadata } from './parser.js';

const CORS_HEADERS = {
  'Access-Control-Allow-Origin': '*',
  'Access-Control-Allow-Methods': 'GET, POST, OPTIONS',
  'Access-Control-Allow-Headers': 'Content-Type, X-RapidAPI-Proxy-Secret',
};

function jsonResponse(data, status = 200) {
  if (status === 200 && typeof data === "object" && !Array.isArray(data)) {
    data._upgrade = { note: "Upgrade for higher limits & priority support", url: "https://rapidapi.com/miccho27-5OJaGGbBiO/api/link-preview-api/pricing" };
  }
  return new Response(JSON.stringify(data), {
    status,
    headers: { 'Content-Type': 'application/json', ...CORS_HEADERS },
  });
}

/**
 * Fetch a URL and extract metadata.
 */
async function fetchPreview(targetUrl, env) {
  const timeout = parseInt(env.FETCH_TIMEOUT) || 5000;
  const cacheTtl = parseInt(env.CACHE_TTL) || 3600;
  const cacheKey = new Request(`https://link-preview-cache/${encodeURIComponent(targetUrl)}`);
  const cache = caches.default;

  // Check cache
  const cached = await cache.match(cacheKey);
  if (cached) {
    const data = await cached.json();
    data._cached = true;
    return data;
  }

  const start = Date.now();

  const controller = new AbortController();
  const timer = setTimeout(() => controller.abort(), timeout);

  let response;
  try {
    response = await fetch(targetUrl, {
      signal: controller.signal,
      headers: {
        'User-Agent': 'LinkPreviewBot/1.0 (compatible; Cloudflare Worker)',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
      },
      redirect: 'follow',
    });
  } catch (err) {
    if (err.name === 'AbortError') {
      return { url: targetUrl, error: 'Timeout: page took longer than 5 seconds to respond' };
    }
    return { url: targetUrl, error: `Fetch failed: ${err.message}` };
  } finally {
    clearTimeout(timer);
  }

  const contentType = response.headers.get('content-type') || '';
  if (!contentType.includes('text/html') && !contentType.includes('application/xhtml+xml')) {
    return {
      url: targetUrl,
      error: `Non-HTML response: ${contentType.split(';')[0].trim()}`,
    };
  }

  const html = await response.text();
  const metadata = parseMetadata(html, response.url);
  const responseTime = Date.now() - start;

  const result = {
    url: response.url,
    ...metadata,
    responseTime,
  };

  // Store in cache
  const cacheResponse = new Response(JSON.stringify(result), {
    headers: {
      'Content-Type': 'application/json',
      'Cache-Control': `s-maxage=${cacheTtl}`,
    },
  });
  await cache.put(cacheKey, cacheResponse);

  return result;
}

export default {
  async fetch(request, env) {
    // Handle CORS preflight
    if (request.method === 'OPTIONS') {
      return new Response(null, { status: 204, headers: CORS_HEADERS });
    }

    const url = new URL(request.url);
    const path = url.pathname;

    // GET /
    if (path === '/' && request.method === 'GET') {
      return jsonResponse({
        service: 'Link Preview API',
        
        _premium: {
          message: "You are using the FREE tier of Link Preview API. Upgrade to Pro for higher rate limits, priority support, and advanced features.",
          upgrade_url: "https://rapidapi.com/miccho27-5OJaGGbBiO/api/link-preview-api/pricing",
          plans: ["Pro ($5.99/mo)", "Ultra ($14.99/mo)", "Mega ($49.99/mo)"]
        },
        endpoints: {
          'GET /preview?url=': 'Get metadata for a single URL',
          'POST /preview/bulk': 'Get metadata for multiple URLs (JSON body: { "urls": [...] })',
        },
      });
    }

    // GET /preview?url=...
    if (path === '/preview' && request.method === 'GET') {
      const targetUrl = url.searchParams.get('url');
      if (!targetUrl) {
        return jsonResponse({ error: 'Missing required query parameter: url' }, 400);
      }

      try {
        new URL(targetUrl);
      } catch {
        return jsonResponse({ error: 'Invalid URL format' }, 400);
      }

      const result = await fetchPreview(targetUrl, env);
      return jsonResponse(result, result.error ? 502 : 200);
    }

    // POST /preview/bulk
    if (path === '/preview/bulk' && request.method === 'POST') {
      let body;
      try {
        body = await request.json();
      } catch {
        return jsonResponse({ error: 'Invalid JSON body' }, 400);
      }

      const urls = body.urls;
      if (!Array.isArray(urls) || urls.length === 0) {
        return jsonResponse({ error: 'Body must contain a non-empty "urls" array' }, 400);
      }

      const maxBulk = parseInt(env.MAX_BULK_URLS) || 10;
      if (urls.length > maxBulk) {
        return jsonResponse({ error: `Maximum ${maxBulk} URLs per request` }, 400);
      }

      // Validate all URLs first
      for (const u of urls) {
        try {
          new URL(u);
        } catch {
          return jsonResponse({ error: `Invalid URL: ${u}` }, 400);
        }
      }

      const results = await Promise.all(urls.map(u => fetchPreview(u, env)));
      return jsonResponse({ results });
    }

    return jsonResponse({ error: 'Not found' }, 404);
  },
};
