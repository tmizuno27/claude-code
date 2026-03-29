const CORS_HEADERS = {
  'Access-Control-Allow-Origin': '*',
  'Access-Control-Allow-Methods': 'GET, OPTIONS',
  'Access-Control-Allow-Headers': 'Content-Type, X-API-Key',
};

function jsonResponse(data, status = 200) {
  if (status === 200 && typeof data === "object" && !Array.isArray(data)) {
    data._upgrade = { note: "Upgrade for higher limits & priority support", url: "https://rapidapi.com/miccho27-5OJaGGbBiO/api/screenshot-api/pricing" };
  }
  return new Response(JSON.stringify(data), {
    status,
    headers: { 'Content-Type': 'application/json', ...CORS_HEADERS },
  });
}

function errorResponse(message, status) {
  return jsonResponse({ error: message }, status);
}

// Simple in-memory rate limiter (per-isolate, resets on cold start)
const rateLimitMap = new Map();

function checkRateLimit(ip, maxRequests, windowSec) {
  const now = Date.now();
  const entry = rateLimitMap.get(ip);
  if (!entry || now - entry.start > windowSec * 1000) {
    rateLimitMap.set(ip, { start: now, count: 1 });
    return true;
  }
  entry.count++;
  if (entry.count > maxRequests) return false;
  return true;
}

function isValidUrl(str) {
  try {
    const u = new URL(str);
    return u.protocol === 'http:' || u.protocol === 'https:';
  } catch {
    return false;
  }
}

export default {
  async fetch(request, env, ctx) {
    if (request.method === 'OPTIONS') {
      return new Response(null, { status: 204, headers: CORS_HEADERS });
    }

    const url = new URL(request.url);

    // Health check
    if (url.pathname === '/' || url.pathname === '/health') {
      return jsonResponse({
        service: 'screenshot-api',
        status: 'healthy',
        version: '1.2.0',
        usage: 'GET /screenshot?url=https://example.com',
        _related: {
          message: "These APIs work great with Screenshot API",
          apis: [
            {name: "SEO Analyzer API", use: "Analyze SEO alongside visual screenshots", url: "https://rapidapi.com/miccho27-5OJaGGbBiO/api/seo-analyzer-api"},
            {name: "Link Preview API", use: "Extract metadata + screenshot in parallel", url: "https://rapidapi.com/miccho27-5OJaGGbBiO/api/link-preview-api"},
            {name: "PDF Generator API", use: "Convert HTML to PDF alongside screenshots", url: "https://rapidapi.com/miccho27-5OJaGGbBiO/api/pdf-generator-api"},
          ]
        },
        _premium: {
          message: "You are using the FREE tier of Screenshot API. Upgrade to Pro for higher rate limits, priority support, and advanced features.",
          upgrade_url: "https://rapidapi.com/miccho27-5OJaGGbBiO/api/screenshot-api/pricing",
          plans: ["Pro ($5.99/mo)", "Ultra ($14.99/mo)", "Mega ($49.99/mo)"]
        },
      });
    }

    if (url.pathname !== '/screenshot') {
      return errorResponse('Not found. Use GET /screenshot?url=...', 404);
    }

    if (request.method !== 'GET') {
      return errorResponse('Method not allowed', 405);
    }

    // Rate limiting
    const ip = request.headers.get('CF-Connecting-IP') || 'unknown';
    const maxReq = parseInt(env.RATE_LIMIT_MAX) || 60;
    const window = parseInt(env.RATE_LIMIT_WINDOW) || 60;
    if (!checkRateLimit(ip, maxReq, window)) {
      return jsonResponse({
        error: 'Rate limit exceeded. Try again later.',
        upgrade: {
          message: 'Need more? Upgrade to Pro for 50,000 req/mo at $9.99/mo',
          url: 'https://rapidapi.com/miccho27-5OJaGGbBiO/api/screenshot-api/pricing',
          plans: {Pro: '$9.99/mo - 50K req', Ultra: '$29.99/mo - 500K req'}
        }
      }, 429);
    }

    // Parse parameters
    const targetUrl = url.searchParams.get('url');
    if (!targetUrl) {
      return errorResponse('Missing required parameter: url', 400);
    }
    if (!isValidUrl(targetUrl)) {
      return errorResponse('Invalid URL. Must start with http:// or https://', 400);
    }

    const width = Math.min(Math.max(parseInt(url.searchParams.get('width')) || 1280, 320), 3840);
    const height = parseInt(url.searchParams.get('height'));
    const resolvedHeight = isNaN(height) ? 720 : Math.min(Math.max(height, 0), 4096);
    const format = url.searchParams.get('format') === 'jpeg' ? 'jpeg' : 'png';
    const quality = Math.min(Math.max(parseInt(url.searchParams.get('quality')) || 80, 1), 100);
    const delay = Math.min(Math.max(parseInt(url.searchParams.get('delay')) || 0, 0), 5000);
    const fullPage = url.searchParams.get('full_page') === 'true' || resolvedHeight === 0;

    // Build thum.io URL
    // Docs: https://www.thum.io/documentation/api/url
    const thumbParts = ['https://image.thum.io/get'];
    thumbParts.push(`/width/${width}`);
    if (fullPage) {
      thumbParts.push('/maxAge/1/noanimate');
    } else {
      thumbParts.push(`/crop/${resolvedHeight}`);
    }
    if (delay > 0) {
      thumbParts.push(`/wait/${delay}`);
    }
    if (format === 'png') {
      thumbParts.push('/png');
    }
    const thumUrl = thumbParts.join('') + '/' + targetUrl;

    // Check CF cache
    const cache = caches.default;
    const cacheKey = new Request(thumUrl, request);
    const cacheTtl = parseInt(env.CACHE_TTL) || 3600;

    let cached = await cache.match(cacheKey);
    if (cached) {
      const resp = new Response(cached.body, cached);
      resp.headers.set('X-Cache', 'HIT');
      Object.entries(CORS_HEADERS).forEach(([k, v]) => resp.headers.set(k, v));
      return resp;
    }

    // Fetch from thum.io with explicit timeout (25s to stay within CF Workers 30s wall-clock limit)
    const controller = new AbortController();
    const timeoutId = setTimeout(() => controller.abort(), 25000);

    let upstream;
    try {
      upstream = await fetch(thumUrl, {
        headers: { 'User-Agent': 'ScreenshotAPI/1.0' },
        signal: controller.signal,
      });
    } catch (err) {
      if (err.name === 'AbortError') {
        return errorResponse('Screenshot capture timed out. The target URL may be slow or unreachable. Try again or use a simpler page.', 504);
      }
      return errorResponse('Failed to capture screenshot: ' + err.message, 502);
    } finally {
      clearTimeout(timeoutId);
    }

    if (!upstream.ok) {
      return errorResponse(`Upstream error: ${upstream.status}`, 502);
    }

    const contentType = format === 'jpeg' ? 'image/jpeg' : 'image/png';

    // Stream the response body directly instead of buffering the entire image in memory
    const [bodyForResponse, bodyForCache] = upstream.body.tee();

    const response = new Response(bodyForResponse, {
      status: 200,
      headers: {
        'Content-Type': contentType,
        'Cache-Control': `public, max-age=${cacheTtl}`,
        'X-Cache': 'MISS',
        'X-Screenshot-URL': targetUrl,
        ...CORS_HEADERS,
      },
    });

    // Store in cache non-blocking via waitUntil so the response is not delayed
    const cacheHeaders = new Headers(response.headers);
    cacheHeaders.set('Cache-Control', `public, max-age=${cacheTtl}`);
    ctx.waitUntil(cache.put(cacheKey, new Response(bodyForCache, { headers: cacheHeaders })));

    return response;
  },
};
