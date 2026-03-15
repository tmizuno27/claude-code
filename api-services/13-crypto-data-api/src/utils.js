const CORS_HEADERS = {
  'Access-Control-Allow-Origin': '*',
  'Access-Control-Allow-Methods': 'GET, OPTIONS',
  'Access-Control-Allow-Headers': 'Content-Type',
};

function jsonResponse(data, status = 200, cacheTtl = 60) {
  return new Response(JSON.stringify({ success: true, data }, null, 2), {
    status,
    headers: {
      'Content-Type': 'application/json',
      'Cache-Control': `public, max-age=${cacheTtl}`,
      ...CORS_HEADERS,
    },
  });
}

function errorResponse(message, status = 500) {
  return new Response(JSON.stringify({ success: false, error: message }, null, 2), {
    status,
    headers: {
      'Content-Type': 'application/json',
      ...CORS_HEADERS,
    },
  });
}

function handleCors(request) {
  if (request.method === 'OPTIONS') {
    return new Response(null, { status: 204, headers: CORS_HEADERS });
  }
  return null;
}

// Simple in-memory rate limiter per IP (30 req/min)
const rateLimitMap = new Map();
const RATE_LIMIT = 30;
const RATE_WINDOW = 60000;

function checkRateLimit(ip) {
  const now = Date.now();
  const entry = rateLimitMap.get(ip);

  if (!entry || now - entry.start > RATE_WINDOW) {
    rateLimitMap.set(ip, { start: now, count: 1 });
    return true;
  }

  entry.count++;
  if (entry.count > RATE_LIMIT) {
    return false;
  }
  return true;
}

// Clean up old entries periodically
function cleanRateLimits() {
  const now = Date.now();
  for (const [ip, entry] of rateLimitMap) {
    if (now - entry.start > RATE_WINDOW) {
      rateLimitMap.delete(ip);
    }
  }
}

export { CORS_HEADERS, jsonResponse, errorResponse, handleCors, checkRateLimit, cleanRateLimits };
