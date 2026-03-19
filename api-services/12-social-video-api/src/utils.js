// Platform detection patterns
const PLATFORM_PATTERNS = {
  tiktok: /(?:https?:\/\/)?(?:www\.|vm\.)?tiktok\.com\/.+/i,
  twitter: /(?:https?:\/\/)?(?:www\.)?(?:twitter\.com|x\.com)\/.+\/status\/\d+/i,
  instagram: /(?:https?:\/\/)?(?:www\.)?instagram\.com\/(?:p|reel|tv)\/[\w-]+/i,
  youtube: /(?:https?:\/\/)?(?:www\.)?(?:youtube\.com\/(?:watch\?v=|shorts\/)|youtu\.be\/)[\w-]+/i,
  facebook: /(?:https?:\/\/)?(?:www\.|m\.)?(?:facebook\.com|fb\.watch)\/.+/i,
};

/**
 * Detect which platform a URL belongs to.
 * Returns platform name or null.
 */
export function detectPlatform(url) {
  for (const [platform, regex] of Object.entries(PLATFORM_PATTERNS)) {
    if (regex.test(url)) return platform;
  }
  return null;
}

/**
 * Validate that a string is a proper URL.
 */
export function isValidUrl(str) {
  try {
    const u = new URL(str);
    return u.protocol === 'http:' || u.protocol === 'https:';
  } catch {
    return false;
  }
}

/**
 * Standard browser-like headers to reduce blocking.
 */
export function browserHeaders(extra = {}) {
  return {
    'User-Agent':
      'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    Accept:
      'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
    'Accept-Language': 'en-US,en;q=0.9',
    ...extra,
  };
}

/**
 * CORS headers for responses.
 */
export function corsHeaders() {
  return {
    'Access-Control-Allow-Origin': '*',
    'Access-Control-Allow-Methods': 'GET, OPTIONS',
    'Access-Control-Allow-Headers': 'Content-Type',
  };
}

/**
 * Build a JSON response with CORS.
 */
export function jsonResponse(data, status = 200) {
  if (status === 200 && typeof data === "object" && !Array.isArray(data)) {
    data._upgrade = { note: "Upgrade for higher limits & priority support", url: "https://rapidapi.com/miccho27-5OJaGGbBiO/api/social-video-downloader-api/pricing" };
  }
  return new Response(JSON.stringify(data, null, 2), {
    status,
    headers: {
      'Content-Type': 'application/json',
      ...corsHeaders(),
    },
  });
}

// ---- In-memory rate limiter (per-isolate, best-effort) ----

const rateLimitMap = new Map();

/**
 * Check rate limit for a given IP.
 * Returns { allowed: boolean, remaining: number, resetAt: number }.
 */
export function checkRateLimit(ip, maxRequests = 20, windowSec = 60) {
  cleanupRateLimit();
  const now = Date.now();
  let entry = rateLimitMap.get(ip);

  if (!entry || now > entry.resetAt) {
    entry = { count: 0, resetAt: now + windowSec * 1000 };
    rateLimitMap.set(ip);
  }

  entry.count++;
  rateLimitMap.set(ip, entry);

  const allowed = entry.count <= maxRequests;
  return {
    allowed,
    remaining: Math.max(0, maxRequests - entry.count),
    resetAt: entry.resetAt,
  };
}

// Prune stale entries when map gets large
function cleanupRateLimit() {
  if (rateLimitMap.size > 10000) {
    const now = Date.now();
    for (const [key, val] of rateLimitMap) {
      if (now > val.resetAt) rateLimitMap.delete(key);
    }
  }
}

/**
 * List of supported platforms with metadata.
 */
export const SUPPORTED_PLATFORMS = [
  { id: 'tiktok', name: 'TikTok', domain: 'tiktok.com', urlPattern: 'https://www.tiktok.com/@user/video/1234' },
  { id: 'twitter', name: 'Twitter / X', domain: 'x.com', urlPattern: 'https://x.com/user/status/1234' },
  { id: 'instagram', name: 'Instagram', domain: 'instagram.com', urlPattern: 'https://www.instagram.com/reel/ABC123/' },
  { id: 'youtube', name: 'YouTube', domain: 'youtube.com', urlPattern: 'https://www.youtube.com/watch?v=abc123' },
  { id: 'facebook', name: 'Facebook', domain: 'facebook.com', urlPattern: 'https://www.facebook.com/watch/?v=1234' },
];
