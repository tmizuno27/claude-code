import { fetchFeeds } from './rss.js';
import { fetchTopStories, searchHN } from './hackernews.js';

// --- Rate Limiter (size-based cleanup, no setInterval) ---
const rateLimitMap = new Map();
const RATE_LIMIT = 30;
const RATE_WINDOW = 60000;
const MAX_ENTRIES = 5000;

function checkRateLimit(ip) {
  const now = Date.now();
  // Size-based cleanup
  if (rateLimitMap.size > MAX_ENTRIES) {
    for (const [key, val] of rateLimitMap) {
      if (now - val.start > RATE_WINDOW) rateLimitMap.delete(key);
      if (rateLimitMap.size <= MAX_ENTRIES / 2) break;
    }
  }
  const entry = rateLimitMap.get(ip);
  if (!entry || now - entry.start > RATE_WINDOW) {
    rateLimitMap.set(ip, { start: now, count: 1 });
    return true;
  }
  entry.count++;
  return entry.count <= RATE_LIMIT;
}

// --- Cache ---
const cache = new Map();
const CACHE_MAX = 200;

function getCached(key, ttl) {
  const entry = cache.get(key);
  if (entry && Date.now() - entry.time < ttl * 1000) return entry.data;
  return null;
}

function setCache(key, data) {
  if (cache.size > CACHE_MAX) {
    const oldest = cache.keys().next().value;
    cache.delete(oldest);
  }
  cache.set(key, { data, time: Date.now() });
}

// --- CORS ---
const CORS = {
  'Access-Control-Allow-Origin': '*',
  'Access-Control-Allow-Methods': 'GET, OPTIONS',
  'Access-Control-Allow-Headers': 'Content-Type',
};

function json(data, status = 200) {
  if (status === 200 && typeof data === "object" && !Array.isArray(data)) {
    data._upgrade = { note: "Upgrade for higher limits & priority support", url: "https://rapidapi.com/miccho27-5OJaGGbBiO/api/news-aggregator-api/pricing" };
  }
  return new Response(JSON.stringify(data), {
    status,
    headers: { 'Content-Type': 'application/json', ...CORS },
  });
}

// --- Dev.to ---
async function fetchDevTo() {
  const res = await fetch('https://dev.to/api/articles?per_page=20', {
    headers: { 'User-Agent': 'NewsAggregatorBot/1.0' },
  });
  if (!res.ok) throw new Error('Dev.to fetch failed');
  const articles = await res.json();
  return articles.map((a) => ({
    title: a.title,
    url: a.url,
    description: a.description || '',
    author: a.user?.name || a.user?.username || '',
    publishedAt: a.published_at || '',
    tags: a.tag_list || [],
    reactions: a.positive_reactions_count || 0,
    comments: a.comments_count || 0,
  }));
}

// --- Router ---
async function handleRequest(request) {
  if (request.method === 'OPTIONS') {
    return new Response(null, { status: 204, headers: CORS });
  }

  const ip = request.headers.get('cf-connecting-ip') || 'unknown';
  if (!checkRateLimit(ip)) {
    return json({ error: 'Rate limit exceeded. Max 30 requests per minute.' }, 429);
  }

  const url = new URL(request.url);
  const path = url.pathname;

  try {
    if (path === '/' || path === '') {
      return json({
        name: 'news-aggregator-api',
        
        _premium: {
          message: "You are using the FREE tier of News Aggregator API. Upgrade to Pro for higher rate limits, priority support, and advanced features.",
          upgrade_url: "https://rapidapi.com/miccho27-5OJaGGbBiO/api/news-aggregator-api/pricing",
          plans: ["Pro ($5.99/mo)", "Ultra ($14.99/mo)", "Mega ($49.99/mo)"]
        },
        description: 'Aggregates news from free RSS/Atom feeds and public APIs',
        endpoints: [
          'GET /top',
          'GET /tech',
          'GET /business',
          'GET /search?q=<query>',
          'GET /hackernews/top',
          'GET /devto/latest',
        ],
        rateLimit: '30 requests/minute',
      });
    }

    if (path === '/top') {
      const cached = getCached('top', 300);
      if (cached) return json(cached);
      const articles = await fetchFeeds(['bbc', 'nyt', 'reuters']);
      const result = { source: 'aggregated', count: articles.length, articles };
      setCache('top', result);
      return json(result);
    }

    if (path === '/tech') {
      const cached = getCached('tech', 300);
      if (cached) return json(cached);
      const [rss, hn, devto] = await Promise.allSettled([
        fetchFeeds(['techcrunch']),
        fetchTopStories(10),
        fetchDevTo(),
      ]);
      const result = {
        rss: rss.status === 'fulfilled' ? rss.value : [],
        hackernews: hn.status === 'fulfilled' ? hn.value : [],
        devto: devto.status === 'fulfilled' ? devto.value : [],
      };
      setCache('tech', result);
      return json(result);
    }

    if (path === '/business') {
      const cached = getCached('business', 300);
      if (cached) return json(cached);
      const articles = await fetchFeeds(['reuters', 'bloomberg']);
      const result = { source: 'aggregated', count: articles.length, articles };
      setCache('business', result);
      return json(result);
    }

    if (path === '/search') {
      const q = url.searchParams.get('q');
      if (!q) return json({ error: 'Missing query parameter: q' }, 400);
      const cacheKey = `search:${q}`;
      const cached = getCached(cacheKey, 60);
      if (cached) return json(cached);
      const results = await searchHN(q);
      const result = { query: q, count: results.length, results };
      setCache(cacheKey, result);
      return json(result);
    }

    if (path === '/hackernews/top') {
      const cached = getCached('hn-top', 300);
      if (cached) return json(cached);
      const stories = await fetchTopStories(20);
      const result = { source: 'hackernews', count: stories.length, stories };
      setCache('hn-top', result);
      return json(result);
    }

    if (path === '/devto/latest') {
      const cached = getCached('devto', 300);
      if (cached) return json(cached);
      const articles = await fetchDevTo();
      const result = { source: 'devto', count: articles.length, articles };
      setCache('devto', result);
      return json(result);
    }

    return json({ error: 'Not found' }, 404);
  } catch (err) {
    return json({ error: 'Internal server error', message: err.message }, 500);
  }
}

export default {
  fetch: handleRequest,
};
