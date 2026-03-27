// Platform detection patterns
const PLATFORM_PATTERNS = {
  tiktok: /(?:https?:\/\/)?(?:www\.|vm\.)?tiktok\.com\/.+/i,
  twitter: /(?:https?:\/\/)?(?:www\.)?(?:twitter\.com|x\.com)\/.+\/status\/\d+/i,
  instagram: /(?:https?:\/\/)?(?:www\.)?instagram\.com\/(?:p|reel|tv)\/[\w-]+/i,
  youtube: /(?:https?:\/\/)?(?:www\.)?(?:youtube\.com\/(?:watch\?v=|shorts\/)|youtu\.be\/)[\w-]+/i,
  facebook: /(?:https?:\/\/)?(?:www\.|m\.)?(?:facebook\.com|fb\.watch)\/.+/i,
};

export function detectPlatform(url) {
  for (const [platform, regex] of Object.entries(PLATFORM_PATTERNS)) {
    if (regex.test(url)) return platform;
  }
  return null;
}

export function isValidUrl(str) {
  try {
    const u = new URL(str);
    return u.protocol === 'http:' || u.protocol === 'https:';
  } catch {
    return false;
  }
}

export const FETCH_TIMEOUT_MS = 30_000;
export const MAX_RETRIES = 2;
export const RETRY_DELAY_MS = 2_000;

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

export async function fetchWithRetry(url, options = {}, { timeoutMs = FETCH_TIMEOUT_MS, retries = MAX_RETRIES, retryDelay = RETRY_DELAY_MS } = {}) {
  let lastError;
  for (let attempt = 0; attempt <= retries; attempt++) {
    const controller = new AbortController();
    const timer = setTimeout(() => controller.abort(), timeoutMs);
    try {
      const res = await fetch(url, { ...options, signal: controller.signal });
      clearTimeout(timer);
      return res;
    } catch (e) {
      clearTimeout(timer);
      lastError = e;
      if (attempt < retries) {
        await new Promise((r) => setTimeout(r, retryDelay));
      }
    }
  }
  throw lastError;
}

export const SUPPORTED_PLATFORMS = [
  { id: 'tiktok', name: 'TikTok', domain: 'tiktok.com' },
  { id: 'twitter', name: 'Twitter / X', domain: 'x.com' },
  { id: 'instagram', name: 'Instagram', domain: 'instagram.com' },
  { id: 'youtube', name: 'YouTube', domain: 'youtube.com' },
  { id: 'facebook', name: 'Facebook', domain: 'facebook.com' },
];
