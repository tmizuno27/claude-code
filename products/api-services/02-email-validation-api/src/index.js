import { DISPOSABLE_DOMAINS } from "./disposable-domains.js";
import { FREE_PROVIDERS } from "./free-providers.js";
import { suggestDomain } from "./typo-suggestions.js";

// RFC 5322 compliant email regex (simplified but robust)
const EMAIL_REGEX =
  /^[a-zA-Z0-9.!#$%&'*+/=?^_`{|}~-]+@[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?(?:\.[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?)*$/;

const ROLE_PREFIXES = new Set([
  "abuse", "admin", "administrator", "billing", "compliance",
  "devnull", "dns", "ftp", "help", "hostmaster", "info",
  "inoc", "ispfeedback", "ispsupport", "list", "list-request",
  "mailer-daemon", "mailerdaemon", "marketing", "media",
  "noc", "no-reply", "noreply", "noc", "null", "office",
  "phish", "phishing", "postmaster", "privacy", "registrar",
  "remove", "request", "role", "root", "sales",
  "security", "spam", "support", "sysadmin", "tech",
  "undisclosed-recipients", "unsubscribe", "usenet", "uucp",
  "webmaster", "www", "contact", "enquiries", "enquiry",
  "feedback", "hr", "jobs", "careers", "recruitment",
  "press", "pr", "legal", "accounting", "finance",
  "operations", "ops", "customerservice", "service",
  "newsletter", "subscribe", "all", "everyone", "team",
  "staff", "general", "reception", "orders",
]);

const CORS_HEADERS = {
  "Access-Control-Allow-Origin": "*",
  "Access-Control-Allow-Methods": "GET, POST, OPTIONS",
  "Access-Control-Allow-Headers": "Content-Type, Authorization, X-RapidAPI-Proxy-Secret",
  "Access-Control-Max-Age": "86400",
};

function jsonResponse(data, status = 200) {
  if (status === 200 && typeof data === "object" && !Array.isArray(data)) {
    data._upgrade = { note: "Upgrade for higher limits & priority support", url: "https://rapidapi.com/miccho27-5OJaGGbBiO/api/email-validation-api/pricing" };
  }
  return new Response(JSON.stringify(data), {
    status,
    headers: { "Content-Type": "application/json", ...CORS_HEADERS },
  });
}

// --------------- Validation helpers ---------------

function checkFormat(email) {
  return EMAIL_REGEX.test(email) && email.length <= 254;
}

function extractParts(email) {
  const idx = email.lastIndexOf("@");
  if (idx < 1) return null;
  return { local: email.substring(0, idx).toLowerCase(), domain: email.substring(idx + 1).toLowerCase() };
}

async function lookupMX(domain) {
  try {
    const url = `https://cloudflare-dns.com/dns-query?name=${encodeURIComponent(domain)}&type=MX`;
    const res = await fetch(url, {
      headers: { Accept: "application/dns-json" },
    });
    if (!res.ok) return { found: false, records: [] };
    const data = await res.json();
    const records = (data.Answer || [])
      .filter((r) => r.type === 15)
      .map((r) => {
        const parts = r.data.split(" ");
        return { priority: parseInt(parts[0], 10), exchange: parts[1]?.replace(/\.$/, "") };
      })
      .sort((a, b) => a.priority - b.priority);
    return { found: records.length > 0, records };
  } catch {
    return { found: false, records: [] };
  }
}

function isDisposable(domain) {
  return DISPOSABLE_DOMAINS.has(domain);
}

function isFreeProvider(domain) {
  return FREE_PROVIDERS.has(domain);
}

function isRoleBased(local) {
  return ROLE_PREFIXES.has(local);
}

function computeScore(checks) {
  let score = 0;
  if (checks.format_valid) score += 30;
  else return 0;
  if (checks.mx_found) score += 40;
  if (!checks.is_disposable) score += 15;
  else score -= 20;
  if (!checks.is_role_based) score += 10;
  if (!checks.suggestion) score += 5;
  return Math.max(0, Math.min(100, score));
}

async function validateEmail(email) {
  const normalized = (email || "").trim().toLowerCase();
  const parts = extractParts(normalized);
  const format_valid = checkFormat(normalized) && parts !== null;

  if (!format_valid) {
    return {
      email: normalized,
      valid: false,
      format_valid: false,
      mx_found: false,
      is_disposable: false,
      is_free_provider: false,
      is_role_based: false,
      suggestion: null,
      score: 0,
      checks: {
        format_valid: false,
        mx_found: false,
        is_disposable: false,
        is_free_provider: false,
        is_role_based: false,
        suggestion: null,
      },
    };
  }

  const { local, domain } = parts;

  // Run MX lookup concurrently with sync checks
  const mxPromise = lookupMX(domain);

  const disposable = isDisposable(domain);
  const freeProvider = isFreeProvider(domain);
  const roleBased = isRoleBased(local);
  const suggestion = suggestDomain(domain);

  const mx = await mxPromise;

  const checks = {
    format_valid: true,
    mx_found: mx.found,
    mx_records: mx.records,
    is_disposable: disposable,
    is_free_provider: freeProvider,
    is_role_based: roleBased,
    suggestion: suggestion ? `${local}@${suggestion}` : null,
  };

  const score = computeScore(checks);

  return {
    email: normalized,
    valid: checks.format_valid && checks.mx_found && !checks.is_disposable,
    format_valid: checks.format_valid,
    mx_found: checks.mx_found,
    is_disposable: checks.is_disposable,
    is_free_provider: checks.is_free_provider,
    is_role_based: checks.is_role_based,
    suggestion: checks.suggestion,
    score,
    checks,
  };
}

// --------------- Request handler ---------------

export default {
  async fetch(request, env) {
    const url = new URL(request.url);

    // CORS preflight
    if (request.method === "OPTIONS") {
      return new Response(null, { status: 204, headers: CORS_HEADERS });
    }

    // Health check
    if (url.pathname === "/" || url.pathname === "/health") {
      return jsonResponse({
        status: "ok",
        service: "email-validation-api",
        
        _premium: {
          message: "You are using the FREE tier of Email Validation API. Upgrade to Pro for higher rate limits, priority support, and advanced features.",
          upgrade_url: "https://rapidapi.com/miccho27-5OJaGGbBiO/api/email-validation-api/pricing",
          plans: ["Pro ($5.99/mo)", "Ultra ($14.99/mo)", "Mega ($49.99/mo)"]
        },
        version: '1.2.0',
        endpoints: [
          "GET /validate?email=user@example.com",
          "POST /validate/bulk",
        ],
        _related: {
          message: "These APIs work great with Email Validation",
          apis: [
            {name: "Company Data API", use: "Enrich validated emails with company info", url: "https://rapidapi.com/miccho27-5OJaGGbBiO/api/company-data-api"},
            {name: "IP Geolocation API", use: "Detect user location alongside email validation", url: "https://rapidapi.com/miccho27-5OJaGGbBiO/api/ip-geolocation-api"},
            {name: "Text Analysis API", use: "Analyze email content for spam/sentiment", url: "https://rapidapi.com/miccho27-5OJaGGbBiO/api/text-analysis-api"},
          ]
        },
      });
    }

    // GET /validate?email=...
    if (url.pathname === "/validate" && request.method === "GET") {
      const email = url.searchParams.get("email");
      if (!email) {
        return jsonResponse({ error: "Missing 'email' query parameter" }, 400);
      }
      const result = await validateEmail(email);
      return jsonResponse(result);
    }

    // POST /validate/bulk
    if (url.pathname === "/validate/bulk" && request.method === "POST") {
      let body;
      try {
        body = await request.json();
      } catch {
        return jsonResponse({ error: "Invalid JSON body" }, 400);
      }

      const emails = body.emails || body;
      if (!Array.isArray(emails)) {
        return jsonResponse({ error: "Request body must be { \"emails\": [\"a@b.com\", ...] } or a JSON array of strings" }, 400);
      }

      const maxBulk = parseInt(env.BULK_MAX_EMAILS || "50", 10);
      if (emails.length > maxBulk) {
        return jsonResponse({ error: `Maximum ${maxBulk} emails per request` }, 400);
      }

      const results = await Promise.all(emails.map((e) => validateEmail(String(e))));
      return jsonResponse({
        count: results.length,
        results,
      });
    }

    return jsonResponse({ error: "Not found" }, 404);
  },
};
