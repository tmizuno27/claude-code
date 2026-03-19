import { fetchWebsiteMetadata, detectTechnologies, rdapLookup } from './enrichment.js';

// --- Rate Limiting (size-based cleanup, no setInterval) ---
const rateLimitMap = new Map();
const RATE_LIMIT = 20;
const RATE_WINDOW_MS = 60_000;
const MAX_MAP_SIZE = 5000;

function checkRateLimit(ip) {
  const now = Date.now();

  // Size-based cleanup
  if (rateLimitMap.size > MAX_MAP_SIZE) {
    for (const [key, entry] of rateLimitMap) {
      if (now - entry.start > RATE_WINDOW_MS) {
        rateLimitMap.delete(key);
      }
    }
  }

  const entry = rateLimitMap.get(ip);
  if (!entry || now - entry.start > RATE_WINDOW_MS) {
    rateLimitMap.set(ip, { start: now, count: 1 });
    return true;
  }
  entry.count++;
  if (entry.count > RATE_LIMIT) return false;
  return true;
}

// --- Caching ---
const cache = new Map();
const CACHE_MAX = 2000;

function getCached(key) {
  const entry = cache.get(key);
  if (!entry) return null;
  if (Date.now() > entry.expires) {
    cache.delete(key);
    return null;
  }
  return entry.data;
}

function setCache(key, data, ttlSeconds) {
  if (cache.size > CACHE_MAX) {
    // Remove oldest entries
    const keys = [...cache.keys()];
    for (let i = 0; i < keys.length / 2; i++) {
      cache.delete(keys[i]);
    }
  }
  cache.set(key, { data, expires: Date.now() + ttlSeconds * 1000 });
}

// --- CORS ---
const CORS_HEADERS = {
  'Access-Control-Allow-Origin': '*',
  'Access-Control-Allow-Methods': 'GET, OPTIONS',
  'Access-Control-Allow-Headers': 'Content-Type',
};

function json(data, status = 200) {
  if (status === 200 && typeof data === "object" && !Array.isArray(data)) {
    data._upgrade = { note: "Upgrade for higher limits & priority support", url: "https://rapidapi.com/miccho27-5OJaGGbBiO/api/company-data-api/pricing" };
  }
  return new Response(JSON.stringify(data, null, 2), {
    status,
    headers: { 'Content-Type': 'application/json', ...CORS_HEADERS },
  });
}

function errorResponse(message, status = 400) {
  return json({ error: message }, status);
}

// --- Handlers ---

function handleInfo() {
  return json({
    name: 'Company Data API',
    
        _premium: {
          message: "You are using the FREE tier of Company Data API. Upgrade to Pro for higher rate limits, priority support, and advanced features.",
          upgrade_url: "https://rapidapi.com/miccho27-5OJaGGbBiO/api/company-data-api/pricing",
          plans: ["Pro ($5.99/mo)", "Ultra ($14.99/mo)", "Mega ($49.99/mo)"]
        },
    description: 'Company/business information from free public sources',
    endpoints: {
      'GET /': 'API information',
      'GET /search?q=<company_name>': 'Search companies via OpenCorporates',
      'GET /company?jurisdiction=<code>&number=<number>': 'Get specific company details',
      'GET /domain?domain=<domain>': 'Get company info by domain (website + RDAP)',
      'GET /enrich?domain=<domain>': 'Full company enrichment (metadata, tech, social, contacts)',
    },
    limits: { rate: '20 requests/minute' },
    source: 'OpenCorporates (free tier), RDAP, web scraping',
  });
}

async function handleSearch(url) {
  const q = url.searchParams.get('q');
  if (!q) return errorResponse('Missing required parameter: q');

  const cacheKey = `search:${q.toLowerCase()}`;
  const cached = getCached(cacheKey);
  if (cached) return json({ ...cached, cached: true });

  // Use Wikidata API to search for companies/organizations
  const apiUrl = `https://www.wikidata.org/w/api.php?action=wbsearchentities&search=${encodeURIComponent(q)}&language=en&limit=10&format=json`;

  try {
    const res = await fetch(apiUrl, { headers: { 'User-Agent': 'CompanyDataAPI/1.0' } });
    if (!res.ok) {
      return errorResponse(`Wikidata API error: ${res.status}`, 502);
    }
    const data = await res.json();
    const companies = (data.search || []).map((item) => ({
      name: item.label,
      description: item.description || null,
      wikidataId: item.id,
      wikidataUrl: item.concepturi,
    }));

    const result = { query: q, count: companies.length, companies };
    setCache(cacheKey, result, 3600);
    return json(result);
  } catch (err) {
    return errorResponse(`Failed to search: ${err.message}`, 502);
  }
}

async function handleCompany(url) {
  const jurisdiction = url.searchParams.get('jurisdiction');
  const number = url.searchParams.get('number');
  if (!jurisdiction) {
    return errorResponse('Missing required parameter: jurisdiction (Wikidata ID, e.g., Q95)');
  }

  const cacheKey = `company:${jurisdiction}`;
  const cached = getCached(cacheKey);
  if (cached) return json({ ...cached, cached: true });

  // Use Wikidata to get entity details
  const wikidataId = jurisdiction; // Reuse jurisdiction param as Wikidata ID (e.g., Q95)
  const apiUrl = `https://www.wikidata.org/w/api.php?action=wbgetentities&ids=${encodeURIComponent(wikidataId)}&languages=en&format=json`;

  try {
    const res = await fetch(apiUrl, { headers: { 'User-Agent': 'CompanyDataAPI/1.0' } });
    if (!res.ok) {
      return errorResponse(`Wikidata API error: ${res.status}`, 502);
    }
    const data = await res.json();
    const entity = data.entities?.[wikidataId];
    if (!entity || entity.missing !== undefined) return errorResponse('Entity not found', 404);

    const labels = entity.labels?.en?.value || null;
    const desc = entity.descriptions?.en?.value || null;
    const claims = entity.claims || {};

    const getClaimValue = (prop) => {
      const c = claims[prop]?.[0]?.mainsnak?.datavalue?.value;
      return c?.time || c?.id || c?.['numeric-id'] || c || null;
    };

    const result = {
      wikidataId,
      name: labels,
      description: desc,
      founded: getClaimValue('P571'),
      headquarters: getClaimValue('P159'),
      website: claims.P856?.[0]?.mainsnak?.datavalue?.value || null,
      industry: getClaimValue('P452'),
      ceo: getClaimValue('P169'),
      employees: getClaimValue('P1128'),
      wikidataUrl: `https://www.wikidata.org/wiki/${wikidataId}`,
    };

    setCache(cacheKey, result, 3600);
    return json(result);
  } catch (err) {
    return errorResponse(`Failed to fetch entity: ${err.message}`, 502);
  }
}

async function handleDomain(url) {
  const domain = url.searchParams.get('domain');
  if (!domain) return errorResponse('Missing required parameter: domain');

  const cacheKey = `domain:${domain.toLowerCase()}`;
  const cached = getCached(cacheKey);
  if (cached) return json({ ...cached, cached: true });

  const targetUrl = `https://${domain}`;

  try {
    const [metadata, rdap] = await Promise.all([
      fetchWebsiteMetadata(targetUrl).catch((e) => ({ error: e.message })),
      rdapLookup(domain).catch((e) => ({ error: e.message })),
    ]);

    const result = {
      domain,
      website: metadata.error
        ? { error: metadata.error }
        : {
            title: metadata.title,
            description: metadata.description,
            socialLinks: metadata.socialLinks,
            emails: metadata.emails,
            phones: metadata.phones,
          },
      rdap,
    };

    setCache(cacheKey, result, 1800);
    return json(result);
  } catch (err) {
    return errorResponse(`Failed to look up domain: ${err.message}`, 502);
  }
}

async function handleEnrich(url) {
  const domain = url.searchParams.get('domain');
  if (!domain) return errorResponse('Missing required parameter: domain');

  const cacheKey = `enrich:${domain.toLowerCase()}`;
  const cached = getCached(cacheKey);
  if (cached) return json({ ...cached, cached: true });

  const targetUrl = `https://${domain}`;

  try {
    const [metadata, rdap] = await Promise.all([
      fetchWebsiteMetadata(targetUrl).catch((e) => ({ error: e.message })),
      rdapLookup(domain).catch((e) => ({ error: e.message })),
    ]);

    let technologies = [];
    if (metadata.html) {
      technologies = detectTechnologies(metadata.html);
    }

    const result = {
      domain,
      metadata: metadata.error
        ? { error: metadata.error }
        : {
            title: metadata.title,
            description: metadata.description,
            ogTags: metadata.ogTags,
          },
      domainInfo: {
        registrar: rdap.registrar || null,
        registrationDate: rdap.registrationDate || null,
        expirationDate: rdap.expirationDate || null,
        domainAge: rdap.registrationDate ? calculateAge(rdap.registrationDate) : null,
        nameservers: rdap.nameservers || null,
      },
      socialLinks: metadata.socialLinks || null,
      technologies,
      contact: {
        emails: metadata.emails || null,
        phones: metadata.phones || null,
      },
    };

    setCache(cacheKey, result, 1800);
    return json(result);
  } catch (err) {
    return errorResponse(`Enrichment failed: ${err.message}`, 502);
  }
}

function calculateAge(dateStr) {
  try {
    const then = new Date(dateStr);
    const now = new Date();
    const years = Math.floor((now - then) / (365.25 * 24 * 60 * 60 * 1000));
    return `${years} years`;
  } catch {
    return null;
  }
}

// --- Router ---
export default {
  async fetch(request) {
    if (request.method === 'OPTIONS') {
      return new Response(null, { status: 204, headers: CORS_HEADERS });
    }

    if (request.method !== 'GET') {
      return errorResponse('Method not allowed', 405);
    }

    const ip = request.headers.get('CF-Connecting-IP') || 'unknown';
    if (!checkRateLimit(ip)) {
      return errorResponse('Rate limit exceeded. Maximum 20 requests per minute.', 429);
    }

    const url = new URL(request.url);
    const path = url.pathname;

    switch (path) {
      case '/':
        return handleInfo();
      case '/search':
        return handleSearch(url);
      case '/company':
        return handleCompany(url);
      case '/domain':
        return handleDomain(url);
      case '/enrich':
        return handleEnrich(url);
      default:
        return errorResponse('Not found', 404);
    }
  },
};
