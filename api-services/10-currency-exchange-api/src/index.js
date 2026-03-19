const CORS_HEADERS = {
  'Access-Control-Allow-Origin': '*',
  'Access-Control-Allow-Methods': 'GET, OPTIONS',
  'Access-Control-Allow-Headers': 'Content-Type, X-RapidAPI-Proxy-Secret',
  'Access-Control-Max-Age': '86400',
};

function jsonResponse(data, status = 200, cacheMaxAge = 3600) {
  if (status === 200 && typeof data === "object" && !Array.isArray(data)) {
    data._upgrade = { note: "Upgrade for higher limits & priority support", url: "https://rapidapi.com/miccho27-5OJaGGbBiO/api/currency-exchange-api/pricing" };
  }
  return new Response(JSON.stringify(data), {
    status,
    headers: {
      'Content-Type': 'application/json',
      'Cache-Control': `public, max-age=${cacheMaxAge}`,
      ...CORS_HEADERS,
    },
  });
}

function errorResponse(message, status = 400) {
  return jsonResponse({ error: message }, status, 0);
}

// Simple in-memory rate limiter (per-isolate, best-effort)
const rateLimitMap = new Map();

function checkRateLimit(ip, limitPerMinute) {
  const now = Date.now();
  const windowStart = now - 60000;
  let record = rateLimitMap.get(ip);
  if (!record || record.windowStart < windowStart) {
    record = { windowStart: now, count: 0 };
  }
  record.count++;
  rateLimitMap.set(ip, record);
  // Cleanup old entries periodically
  if (rateLimitMap.size > 10000) {
    for (const [key, val] of rateLimitMap) {
      if (val.windowStart < windowStart) rateLimitMap.delete(key);
    }
  }
  return record.count <= limitPerMinute;
}

async function fetchWithCache(url, cacheTtl, cacheApi) {
  const cacheKey = new Request(url);
  const cached = await cacheApi.match(cacheKey);
  if (cached) return cached;

  const response = await fetch(url);
  if (!response.ok) {
    throw new Error(`Upstream API error: ${response.status}`);
  }

  const data = await response.json();
  const cachedResponse = jsonResponse(data, 200, cacheTtl);
  // Clone before putting in cache since body can only be read once
  await cacheApi.put(cacheKey, cachedResponse.clone());
  return cachedResponse;
}

// Handlers

async function handleRates(url, env, cacheApi) {
  const base = (url.searchParams.get('base') || 'USD').toUpperCase();
  const cacheTtl = parseInt(env.CACHE_TTL_SECONDS || '3600');
  const apiUrl = `${env.FRANKFURTER_BASE_URL}/latest?base=${base}`;

  try {
    const resp = await fetchWithCache(apiUrl, cacheTtl, cacheApi);
    const data = await resp.json();
    return jsonResponse({
      success: true,
      base: data.base,
      date: data.date,
      rates: data.rates,
    });
  } catch (e) {
    return errorResponse(e.message, 502);
  }
}

async function handleConvert(url, env, cacheApi) {
  const from = (url.searchParams.get('from') || '').toUpperCase();
  const to = (url.searchParams.get('to') || '').toUpperCase();
  const amountStr = url.searchParams.get('amount');

  if (!from || !to) return errorResponse('Missing required parameters: from, to');
  if (!amountStr) return errorResponse('Missing required parameter: amount');

  const amount = parseFloat(amountStr);
  if (isNaN(amount) || amount < 0) return errorResponse('Invalid amount');

  const cacheTtl = parseInt(env.CACHE_TTL_SECONDS || '3600');
  const apiUrl = `${env.FRANKFURTER_BASE_URL}/latest?base=${from}&symbols=${to}`;

  try {
    const resp = await fetchWithCache(apiUrl, cacheTtl, cacheApi);
    const data = await resp.json();
    const rate = data.rates[to];
    if (rate === undefined) return errorResponse(`Unsupported currency: ${to}`, 400);

    return jsonResponse({
      success: true,
      from,
      to,
      amount,
      rate,
      result: Math.round(amount * rate * 10000) / 10000,
      date: data.date,
    });
  } catch (e) {
    return errorResponse(e.message, 502);
  }
}

async function handleCurrencies(env, cacheApi) {
  const cacheTtl = parseInt(env.CACHE_TTL_SECONDS || '3600');
  const apiUrl = `${env.FRANKFURTER_BASE_URL}/currencies`;

  try {
    const resp = await fetchWithCache(apiUrl, cacheTtl, cacheApi);
    const data = await resp.json();
    return jsonResponse({
      success: true,
      currencies: data,
    });
  } catch (e) {
    return errorResponse(e.message, 502);
  }
}

async function handleHistorical(url, env, cacheApi) {
  const base = (url.searchParams.get('base') || 'USD').toUpperCase();
  const date = url.searchParams.get('date');

  if (!date) return errorResponse('Missing required parameter: date');
  if (!/^\d{4}-\d{2}-\d{2}$/.test(date)) return errorResponse('Invalid date format. Use YYYY-MM-DD');

  const cacheTtl = parseInt(env.CACHE_TTL_SECONDS || '3600');
  const apiUrl = `${env.FRANKFURTER_BASE_URL}/${date}?base=${base}`;

  try {
    const resp = await fetchWithCache(apiUrl, cacheTtl, cacheApi);
    const data = await resp.json();
    return jsonResponse({
      success: true,
      base: data.base,
      date: data.date,
      rates: data.rates,
    });
  } catch (e) {
    return errorResponse(e.message, 502);
  }
}

export default {
  async fetch(request, env) {
    if (request.method === 'OPTIONS') {
      return new Response(null, { status: 204, headers: CORS_HEADERS });
    }
    if (request.method !== 'GET') {
      return errorResponse('Method not allowed', 405);
    }

    // Rate limiting
    const ip = request.headers.get('CF-Connecting-IP') || 'unknown';
    const limit = parseInt(env.RATE_LIMIT_PER_MINUTE || '60');
    if (!checkRateLimit(ip, limit)) {
      return errorResponse('Rate limit exceeded. Max 60 requests per minute.', 429);
    }

    const url = new URL(request.url);
    const path = url.pathname.replace(/\/+$/, '') || '/';
    const cacheApi = caches.default;

    switch (path) {
      case '/':
        return jsonResponse({
          name: 'Currency Exchange Rate API',
          
        _premium: {
          message: "You are using the FREE tier of Currency Exchange API. Upgrade to Pro for higher rate limits, priority support, and advanced features.",
          upgrade_url: "https://rapidapi.com/miccho27-5OJaGGbBiO/api/currency-exchange-api/pricing",
          plans: ["Pro ($5.99/mo)", "Ultra ($14.99/mo)", "Mega ($49.99/mo)"]
        },
          endpoints: {
            rates: '/rates?base=USD',
            convert: '/convert?from=USD&to=EUR&amount=100',
            currencies: '/currencies',
            historical: '/historical?base=USD&date=2025-01-15',
          },
        });
      case '/rates':
        return handleRates(url, env, cacheApi);
      case '/convert':
        return handleConvert(url, env, cacheApi);
      case '/currencies':
        return handleCurrencies(env, cacheApi);
      case '/historical':
        return handleHistorical(url, env, cacheApi);
      default:
        return errorResponse('Not found', 404);
    }
  },
};
