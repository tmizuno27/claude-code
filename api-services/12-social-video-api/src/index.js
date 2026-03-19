import { detectPlatform, isValidUrl, checkRateLimit, jsonResponse, corsHeaders, SUPPORTED_PLATFORMS } from './utils.js';
import { extract } from './extractors.js';

export default {
  async fetch(request, env) {
    // Handle CORS preflight
    if (request.method === 'OPTIONS') {
      return new Response(null, { status: 204, headers: corsHeaders() });
    }

    if (request.method !== 'GET') {
      return jsonResponse({ error: 'Method not allowed' }, 405);
    }

    // Rate limiting
    const ip = request.headers.get('cf-connecting-ip') || request.headers.get('x-forwarded-for') || 'unknown';
    const maxReqs = parseInt(env.RATE_LIMIT_MAX || '20');
    const windowSec = parseInt(env.RATE_LIMIT_WINDOW_SEC || '60');
    const rateCheck = checkRateLimit(ip, maxReqs, windowSec);

    if (!rateCheck.allowed) {
      return jsonResponse(
        { error: 'Rate limit exceeded', remaining: 0, retry_after_sec: Math.ceil((rateCheck.resetAt - Date.now()) / 1000) },
        429
      );
    }

    const url = new URL(request.url);
    const path = url.pathname;

    // ── Routes ──

    if (path === '/' || path === '') {
      return jsonResponse({
        name: 'Social Video API',
        
        _premium: {
          message: "You are using the FREE tier of Social Video API. Upgrade to Pro for higher rate limits, priority support, and advanced features.",
          upgrade_url: "https://rapidapi.com/miccho27-5OJaGGbBiO/api/social-video-api/pricing",
          plans: ["Pro ($5.99/mo)", "Ultra ($14.99/mo)", "Mega ($49.99/mo)"]
        },
        description: 'Extract video download URLs from social media platforms by parsing public HTML pages.',
        endpoints: {
          'GET /download?url=<video_url>': 'Extract video download URL',
          'GET /info?url=<video_url>': 'Get video metadata without download URL',
          'GET /platforms': 'List supported platforms',
        },
        rate_limit: `${maxReqs} requests per ${windowSec} seconds per IP`,
      });
    }

    if (path === '/platforms') {
      return jsonResponse({ platforms: SUPPORTED_PLATFORMS });
    }

    if (path === '/download' || path === '/info') {
      const targetUrl = url.searchParams.get('url');
      if (!targetUrl) {
        return jsonResponse({ error: 'Missing required parameter: url' }, 400);
      }
      if (!isValidUrl(targetUrl)) {
        return jsonResponse({ error: 'Invalid URL format' }, 400);
      }

      const platform = detectPlatform(targetUrl);
      if (!platform) {
        return jsonResponse(
          { error: 'Unsupported platform', supported: SUPPORTED_PLATFORMS.map((p) => p.id) },
          400
        );
      }

      const result = await extract(platform, targetUrl);

      // For /info endpoint, strip the video_url
      if (path === '/info' && result.success) {
        const { video_url, ...meta } = result;
        return jsonResponse(meta);
      }

      return jsonResponse(result, result.success ? 200 : 422);
    }

    return jsonResponse({ error: 'Not found' }, 404);
  },
};
