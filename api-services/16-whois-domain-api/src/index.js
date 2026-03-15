// WHOIS Domain API - Cloudflare Worker
// Uses free RDAP protocol for domain lookups and Cloudflare DoH for DNS queries

const CORS_HEADERS = {
  'Access-Control-Allow-Origin': '*',
  'Access-Control-Allow-Methods': 'GET, OPTIONS',
  'Access-Control-Allow-Headers': 'Content-Type',
};

// --- Caching ---
const cache = new Map();
const CACHE_TTL = { rdap: 3600, dns: 300, bootstrap: 86400 };
const CACHE_MAX_SIZE = 500;

function cacheGet(key) {
  const entry = cache.get(key);
  if (!entry) return null;
  if (Date.now() > entry.expires) {
    cache.delete(key);
    return null;
  }
  return entry.value;
}

function cacheSet(key, value, ttlSeconds) {
  // Size-based cleanup: if at limit, delete oldest entries
  if (cache.size >= CACHE_MAX_SIZE) {
    let oldest = null;
    let oldestKey = null;
    for (const [k, v] of cache) {
      if (!oldest || v.created < oldest) {
        oldest = v.created;
        oldestKey = k;
      }
    }
    if (oldestKey) cache.delete(oldestKey);
  }
  cache.set(key, { value, expires: Date.now() + ttlSeconds * 1000, created: Date.now() });
}

// --- Rate Limiting ---
const rateLimits = new Map();
const RATE_LIMIT = 20; // per minute
const RATE_WINDOW = 60000;
const RATE_MAX_ENTRIES = 1000;

function checkRateLimit(ip) {
  const now = Date.now();
  // Size-based cleanup
  if (rateLimits.size > RATE_MAX_ENTRIES) {
    for (const [key, entry] of rateLimits) {
      if (now - entry.windowStart > RATE_WINDOW) {
        rateLimits.delete(key);
      }
    }
  }
  let entry = rateLimits.get(ip);
  if (!entry || now - entry.windowStart > RATE_WINDOW) {
    entry = { count: 1, windowStart: now };
    rateLimits.set(ip, entry);
    return true;
  }
  entry.count++;
  if (entry.count > RATE_LIMIT) return false;
  return true;
}

// --- Helpers ---
function json(data, status = 200) {
  return new Response(JSON.stringify(data, null, 2), {
    status,
    headers: { 'Content-Type': 'application/json', ...CORS_HEADERS },
  });
}

function errorJson(message, status = 400) {
  return json({ error: message }, status);
}

function validateDomain(domain) {
  if (!domain) return false;
  return /^[a-zA-Z0-9][a-zA-Z0-9.-]*\.[a-zA-Z]{2,}$/.test(domain);
}

function getTLD(domain) {
  const parts = domain.split('.');
  return parts[parts.length - 1].toLowerCase();
}

// --- RDAP Bootstrap ---
async function getRdapServer(tld) {
  const cacheKey = `bootstrap`;
  let bootstrap = cacheGet(cacheKey);
  if (!bootstrap) {
    const res = await fetch('https://data.iana.org/rdap/dns.json');
    if (!res.ok) throw new Error('Failed to fetch RDAP bootstrap data');
    bootstrap = await res.json();
    cacheSet(cacheKey, bootstrap, CACHE_TTL.bootstrap);
  }
  for (const entry of bootstrap.services) {
    const tlds = entry[0];
    const urls = entry[1];
    if (tlds.map(t => t.toLowerCase()).includes(tld.toLowerCase())) {
      return urls[0].replace(/\/$/, '');
    }
  }
  return null;
}

// --- RDAP Lookup ---
async function rdapLookup(domain) {
  const cacheKey = `rdap:${domain}`;
  let cached = cacheGet(cacheKey);
  if (cached) return cached;

  const tld = getTLD(domain);
  const server = await getRdapServer(tld);
  if (!server) throw new Error(`No RDAP server found for TLD: .${tld}`);

  const res = await fetch(`${server}/domain/${domain}`, {
    headers: { Accept: 'application/rdap+json' },
  });
  if (res.status === 404) return null;
  if (!res.ok) throw new Error(`RDAP query failed with status ${res.status}`);

  const data = await res.json();
  const result = parseRdapResponse(data, domain);
  cacheSet(cacheKey, result, CACHE_TTL.rdap);
  return result;
}

function parseRdapResponse(data, domain) {
  const result = {
    domain: data.ldhName || domain,
    status: data.status || [],
    events: {},
    registrar: null,
    nameservers: [],
    dnssec: null,
  };

  // Events (registration, expiration, last changed)
  if (data.events) {
    for (const event of data.events) {
      if (event.eventAction === 'registration') result.events.registered = event.eventDate;
      if (event.eventAction === 'expiration') result.events.expires = event.eventDate;
      if (event.eventAction === 'last changed') result.events.lastUpdated = event.eventDate;
    }
  }

  // Registrar from entities
  if (data.entities) {
    for (const entity of data.entities) {
      if (entity.roles && entity.roles.includes('registrar')) {
        result.registrar = {
          name: entity.vcardArray
            ? extractVcardFn(entity.vcardArray)
            : entity.handle || null,
          url: entity.links ? entity.links.find(l => l.rel === 'self')?.href || null : null,
        };
        // Try publicIds for IANA ID
        if (entity.publicIds) {
          result.registrar.ianaId = entity.publicIds.find(p => p.type === 'IANA Registrar ID')?.identifier || null;
        }
        break;
      }
    }
  }

  // Nameservers
  if (data.nameservers) {
    result.nameservers = data.nameservers.map(ns => ns.ldhName).filter(Boolean);
  }

  // DNSSEC
  if (data.secureDNS) {
    result.dnssec = data.secureDNS.delegationSigned ? 'signed' : 'unsigned';
  }

  return result;
}

function extractVcardFn(vcardArray) {
  if (!vcardArray || vcardArray.length < 2) return null;
  const fields = vcardArray[1];
  for (const field of fields) {
    if (field[0] === 'fn') return field[3];
  }
  return null;
}

// --- DNS Lookup via Cloudflare DoH ---
const DNS_TYPES = ['A', 'AAAA', 'MX', 'NS', 'TXT', 'CNAME'];

async function dnsLookup(domain, types = DNS_TYPES) {
  const cacheKey = `dns:${domain}`;
  let cached = cacheGet(cacheKey);
  if (cached) return cached;

  const results = {};
  const fetches = types.map(async (type) => {
    try {
      const res = await fetch(
        `https://cloudflare-dns.com/dns-query?name=${encodeURIComponent(domain)}&type=${type}`,
        { headers: { Accept: 'application/dns-json' } }
      );
      if (!res.ok) return;
      const data = await res.json();
      if (data.Answer) {
        results[type] = data.Answer.map(a => ({
          name: a.name,
          type: a.type,
          ttl: a.TTL,
          data: a.data,
        }));
      }
    } catch (e) {
      // skip failed type
    }
  });
  await Promise.all(fetches);

  cacheSet(cacheKey, results, CACHE_TTL.dns);
  return results;
}

// --- TLD List ---
async function getTldList() {
  const cacheKey = 'tld-list';
  let cached = cacheGet(cacheKey);
  if (cached) return cached;

  const bootstrap = cacheGet('bootstrap') || await (async () => {
    const res = await fetch('https://data.iana.org/rdap/dns.json');
    const data = await res.json();
    cacheSet('bootstrap', data, CACHE_TTL.bootstrap);
    return data;
  })();

  const tlds = new Set();
  for (const entry of bootstrap.services) {
    for (const tld of entry[0]) {
      tlds.add(tld.toLowerCase());
    }
  }
  const result = [...tlds].sort();
  cacheSet(cacheKey, result, CACHE_TTL.bootstrap);
  return result;
}

// --- Router ---
async function handleRequest(request) {
  if (request.method === 'OPTIONS') {
    return new Response(null, { status: 204, headers: CORS_HEADERS });
  }
  if (request.method !== 'GET') {
    return errorJson('Method not allowed', 405);
  }

  const ip = request.headers.get('CF-Connecting-IP') || 'unknown';
  if (!checkRateLimit(ip)) {
    return errorJson('Rate limit exceeded. Max 20 requests per minute.', 429);
  }

  const url = new URL(request.url);
  const path = url.pathname;

  try {
    if (path === '/' || path === '') {
      return json({
        name: 'WHOIS Domain API',
        version: '1.0.0',
        description: 'Domain WHOIS/RDAP lookup and DNS query API',
        endpoints: {
          '/lookup?domain=': 'Full RDAP/WHOIS domain lookup',
          '/dns?domain=': 'DNS records lookup (A, AAAA, MX, NS, TXT, CNAME)',
          '/availability?domain=': 'Check domain availability',
          '/tld-list': 'List supported TLDs with RDAP',
        },
        source: 'RDAP (Registration Data Access Protocol) + Cloudflare DoH',
      });
    }

    if (path === '/lookup') {
      const domain = url.searchParams.get('domain')?.toLowerCase();
      if (!validateDomain(domain)) return errorJson('Invalid or missing domain parameter');
      const result = await rdapLookup(domain);
      if (!result) return errorJson('Domain not found in RDAP', 404);
      return json({ domain: result.domain, status: result.status, registered: result.events.registered || null, expires: result.events.expires || null, lastUpdated: result.events.lastUpdated || null, registrar: result.registrar, nameservers: result.nameservers, dnssec: result.dnssec });
    }

    if (path === '/dns') {
      const domain = url.searchParams.get('domain')?.toLowerCase();
      if (!validateDomain(domain)) return errorJson('Invalid or missing domain parameter');
      const records = await dnsLookup(domain);
      return json({ domain, records });
    }

    if (path === '/availability') {
      const domain = url.searchParams.get('domain')?.toLowerCase();
      if (!validateDomain(domain)) return errorJson('Invalid or missing domain parameter');
      try {
        const result = await rdapLookup(domain);
        if (result) {
          return json({ domain, available: false, status: result.status, registrar: result.registrar?.name || null });
        }
        return json({ domain, available: true, note: 'Domain not found in RDAP. Likely available but verify with a registrar.' });
      } catch (e) {
        return json({ domain, available: 'unknown', note: e.message });
      }
    }

    if (path === '/tld-list') {
      const tlds = await getTldList();
      return json({ count: tlds.length, tlds });
    }

    return errorJson('Not found', 404);
  } catch (e) {
    return errorJson(`Internal error: ${e.message}`, 500);
  }
}

export default {
  fetch: handleRequest,
};
