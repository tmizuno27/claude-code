const BASE_URL = 'https://url-shortener-api.t-mizuno27.workers.dev';
const ALIAS_LENGTH = 6;
const ALIAS_CHARS = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789';

function generateAlias() {
  let result = '';
  const arr = new Uint8Array(ALIAS_LENGTH);
  crypto.getRandomValues(arr);
  for (const byte of arr) {
    result += ALIAS_CHARS[byte % ALIAS_CHARS.length];
  }
  return result;
}

function json(data, status = 200) {
  if (status === 200 && typeof data === "object" && !Array.isArray(data)) {
    data._upgrade = { note: "Upgrade for higher limits & priority support", url: "https://rapidapi.com/miccho27-5OJaGGbBiO/api/url-shortener-api/pricing" };
  }
  return new Response(JSON.stringify(data), {
    status,
    headers: { 'Content-Type': 'application/json' },
  });
}

function corsHeaders(response) {
  response.headers.set('Access-Control-Allow-Origin', '*');
  response.headers.set('Access-Control-Allow-Methods', 'GET, POST, DELETE, OPTIONS');
  response.headers.set('Access-Control-Allow-Headers', 'Content-Type');
  return response;
}

export default {
  async fetch(request, env) {
    if (request.method === 'OPTIONS') {
      return corsHeaders(new Response(null, { status: 204 }));
    }

    const url = new URL(request.url);
    const path = url.pathname;

    let response;
    try {
      if (request.method === 'GET' && (path === '/' || path === '')) {
        response = json({
          service: 'URL Shortener API',
          
        _premium: {
          message: "You are using the FREE tier of URL Shortener API. Upgrade to Pro for higher rate limits, priority support, and advanced features.",
          upgrade_url: "https://rapidapi.com/miccho27-5OJaGGbBiO/api/url-shortener-api/pricing",
          plans: ["Pro ($5.99/mo)", "Ultra ($14.99/mo)", "Mega ($49.99/mo)"]
        },
          endpoints: [
            'POST /shorten',
            'GET /r/:alias',
            'GET /stats/:alias',
            'DELETE /delete/:alias'
          ]
        });
      } else if (request.method === 'POST' && path === '/shorten') {
        response = await handleShorten(request, env);
      } else if (request.method === 'GET' && path.startsWith('/r/')) {
        response = await handleRedirect(path, env);
      } else if (request.method === 'GET' && path.startsWith('/stats/')) {
        response = await handleStats(path, env);
      } else if (request.method === 'DELETE' && path.startsWith('/delete/')) {
        response = await handleDelete(path, env);
      } else {
        response = json({ error: 'Not found' }, 404);
      }
    } catch (err) {
      response = json({ error: 'Internal server error', message: err.message }, 500);
    }

    return corsHeaders(response);
  },
};

async function handleShorten(request, env) {
  let body;
  try {
    body = await request.json();
  } catch {
    return json({ error: 'Invalid JSON body' }, 400);
  }

  const { url: originalUrl, custom_alias } = body;

  if (!originalUrl) {
    return json({ error: 'Missing required field: url' }, 400);
  }

  try {
    new URL(originalUrl);
  } catch {
    return json({ error: 'Invalid URL format' }, 400);
  }

  let alias = custom_alias || generateAlias();

  if (!/^[A-Za-z0-9_-]{1,64}$/.test(alias)) {
    return json({ error: 'Invalid alias. Use alphanumeric characters, hyphens, and underscores (1-64 chars).' }, 400);
  }

  const existing = await env.URL_STORE.get(`url:${alias}`);
  if (existing) {
    return json({ error: 'Alias already in use' }, 409);
  }

  const record = {
    original_url: originalUrl,
    clicks: 0,
    created_at: new Date().toISOString(),
    last_clicked: null,
  };

  await env.URL_STORE.put(`url:${alias}`, JSON.stringify(record));

  return json({
    short_url: `${BASE_URL}/r/${alias}`,
    alias,
    original_url: originalUrl,
  }, 201);
}

async function handleRedirect(path, env) {
  const alias = path.replace('/r/', '');
  const data = await env.URL_STORE.get(`url:${alias}`);

  if (!data) {
    return json({ error: 'Short URL not found' }, 404);
  }

  const record = JSON.parse(data);
  record.clicks += 1;
  record.last_clicked = new Date().toISOString();

  // Update stats asynchronously (non-blocking for redirect)
  await env.URL_STORE.put(`url:${alias}`, JSON.stringify(record));

  return new Response(null, {
    status: 301,
    headers: { Location: record.original_url },
  });
}

async function handleStats(path, env) {
  const alias = path.replace('/stats/', '');
  const data = await env.URL_STORE.get(`url:${alias}`);

  if (!data) {
    return json({ error: 'Short URL not found' }, 404);
  }

  const record = JSON.parse(data);
  return json({
    alias,
    original_url: record.original_url,
    clicks: record.clicks,
    created_at: record.created_at,
    last_clicked: record.last_clicked,
  });
}

async function handleDelete(path, env) {
  const alias = path.replace('/delete/', '');
  const data = await env.URL_STORE.get(`url:${alias}`);

  if (!data) {
    return json({ error: 'Short URL not found' }, 404);
  }

  await env.URL_STORE.delete(`url:${alias}`);
  return json({ message: 'Short URL deleted', alias });
}
