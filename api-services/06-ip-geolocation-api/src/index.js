const CORS_HEADERS = {
  'Access-Control-Allow-Origin': '*',
  'Access-Control-Allow-Methods': 'GET, POST, OPTIONS',
  'Access-Control-Allow-Headers': 'Content-Type, X-RapidAPI-Key',
};

function jsonResponse(data, status = 200) {
  return new Response(JSON.stringify(data, null, 2), {
    status,
    headers: { 'Content-Type': 'application/json', ...CORS_HEADERS },
  });
}

function errorResponse(message, status = 400) {
  return jsonResponse({ error: message }, status);
}

function isValidIP(ip) {
  // IPv4
  if (/^(\d{1,3}\.){3}\d{1,3}$/.test(ip)) {
    return ip.split('.').every(n => parseInt(n) >= 0 && parseInt(n) <= 255);
  }
  // IPv6 (simplified check)
  if (/^[0-9a-fA-F:]+$/.test(ip) && ip.includes(':')) {
    return true;
  }
  return false;
}

function formatCfData(ip, cf) {
  return {
    ip,
    country: cf.country || null,
    country_name: cf.country || null,
    region: cf.region || null,
    city: cf.city || null,
    latitude: cf.latitude ? parseFloat(cf.latitude) : null,
    longitude: cf.longitude ? parseFloat(cf.longitude) : null,
    timezone: cf.timezone || null,
    isp: cf.asOrganization || null,
    is_vpn: false,
    is_proxy: false,
    is_datacenter: cf.asOrganization ? /cloud|host|server|data|amazon|google|microsoft|digital ocean|ovh|hetzner/i.test(cf.asOrganization) : false,
    currency: null,
    languages: null,
  };
}

function formatIpApiData(data) {
  return {
    ip: data.query,
    country: data.countryCode || null,
    country_name: data.country || null,
    region: data.regionName || null,
    city: data.city || null,
    latitude: data.lat || null,
    longitude: data.lon || null,
    timezone: data.timezone || null,
    isp: data.isp || null,
    is_vpn: false,
    is_proxy: data.proxy || false,
    is_datacenter: data.hosting || false,
    currency: data.currency || null,
    languages: null,
  };
}

async function lookupIP(ip, env, ctx) {
  const cacheKey = new Request(`https://cache.internal/ip/${ip}`);
  const cache = caches.default;

  // Check cache
  const cached = await cache.match(cacheKey);
  if (cached) {
    const data = await cached.json();
    data._cached = true;
    return data;
  }

  // Fetch from ip-api.com (free tier: 45 req/min)
  const res = await fetch(
    `http://ip-api.com/json/${ip}?fields=status,message,country,countryCode,region,regionName,city,lat,lon,timezone,currency,isp,org,proxy,hosting,query`
  );

  if (!res.ok) {
    throw new Error('Upstream API error');
  }

  const raw = await res.json();
  if (raw.status === 'fail') {
    throw new Error(raw.message || 'Lookup failed');
  }

  const result = formatIpApiData(raw);

  // Cache for 24 hours
  const ttl = parseInt(env.CACHE_TTL) || 86400;
  const cacheResponse = new Response(JSON.stringify(result), {
    headers: { 'Content-Type': 'application/json', 'Cache-Control': `s-maxage=${ttl}` },
  });
  ctx.waitUntil(cache.put(cacheKey, cacheResponse));

  return result;
}

async function handleMe(request) {
  const cf = request.cf || {};
  const ip = request.headers.get('CF-Connecting-IP') || request.headers.get('X-Forwarded-For') || 'unknown';
  const result = formatCfData(ip, cf);
  // Add extra cf fields if available
  result.asn = cf.asn || null;
  result.colo = cf.colo || null;
  return jsonResponse(result);
}

async function handleLookup(request, env, ctx) {
  const url = new URL(request.url);
  const ip = url.searchParams.get('ip');

  if (!ip) {
    return errorResponse('Missing required parameter: ip');
  }
  if (!isValidIP(ip)) {
    return errorResponse('Invalid IP address');
  }

  try {
    const result = await lookupIP(ip, env, ctx);
    return jsonResponse(result);
  } catch (e) {
    return errorResponse(e.message, 502);
  }
}

async function handleBulkLookup(request, env, ctx) {
  let body;
  try {
    body = await request.json();
  } catch {
    return errorResponse('Invalid JSON body');
  }

  const ips = body.ips;
  if (!Array.isArray(ips) || ips.length === 0) {
    return errorResponse('Request body must contain an "ips" array');
  }

  const maxIps = parseInt(env.BULK_MAX_IPS) || 20;
  if (ips.length > maxIps) {
    return errorResponse(`Maximum ${maxIps} IPs per request`);
  }

  const invalid = ips.filter(ip => !isValidIP(ip));
  if (invalid.length > 0) {
    return errorResponse(`Invalid IP addresses: ${invalid.join(', ')}`);
  }

  // Process sequentially to respect ip-api.com rate limits
  const results = [];
  for (const ip of ips) {
    try {
      const result = await lookupIP(ip, env, ctx);
      results.push(result);
    } catch (e) {
      results.push({ ip, error: e.message });
    }
  }

  return jsonResponse({ count: results.length, results });
}

export default {
  async fetch(request, env, ctx) {
    if (request.method === 'OPTIONS') {
      return new Response(null, { status: 204, headers: CORS_HEADERS });
    }

    const url = new URL(request.url);
    const path = url.pathname;

    if (path === '/me' && request.method === 'GET') {
      return handleMe(request);
    }
    if (path === '/lookup' && request.method === 'GET') {
      return handleLookup(request, env, ctx);
    }
    if (path === '/lookup/bulk' && request.method === 'POST') {
      return handleBulkLookup(request, env, ctx);
    }
    if (path === '/' && request.method === 'GET') {
      return jsonResponse({
        name: 'IP Geolocation API',
        
        _premium: {
          message: "You are using the FREE tier of IP Geolocation API. Upgrade to Pro for higher rate limits, priority support, and advanced features.",
          upgrade_url: "https://rapidapi.com/miccho27-5OJaGGbBiO/api/ip-geolocation-api/pricing",
          plans: ["Pro ($5.99/mo)", "Ultra ($14.99/mo)", "Mega ($49.99/mo)"]
        },
        endpoints: ['GET /me', 'GET /lookup?ip=x.x.x.x', 'POST /lookup/bulk'],
        docs: 'https://ip-geolocation-api.t-mizuno27.workers.dev/',
      });
    }

    return errorResponse('Not found', 404);
  },
};
