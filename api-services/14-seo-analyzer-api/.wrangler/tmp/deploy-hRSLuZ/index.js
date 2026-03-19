var __defProp = Object.defineProperty;
var __name = (target, value) => __defProp(target, "name", { value, configurable: true });

// src/parser.js
function extractTitle(html) {
  const m = html.match(/<title[^>]*>([\s\S]*?)<\/title>/i);
  const text = m ? decodeEntities(m[1].trim()) : null;
  const length = text ? text.length : 0;
  return {
    text,
    length,
    optimal: length >= 30 && length <= 60
  };
}
__name(extractTitle, "extractTitle");
function extractMetaDescription(html) {
  const m = html.match(/<meta[^>]+name\s*=\s*["']description["'][^>]+content\s*=\s*["']([\s\S]*?)["'][^>]*>/i) || html.match(/<meta[^>]+content\s*=\s*["']([\s\S]*?)["'][^>]+name\s*=\s*["']description["'][^>]*>/i);
  const text = m ? decodeEntities(m[1].trim()) : null;
  const length = text ? text.length : 0;
  return {
    text,
    length,
    optimal: length >= 120 && length <= 160
  };
}
__name(extractMetaDescription, "extractMetaDescription");
function extractHeadings(html) {
  const result = { h1: [], h2: [], h3: [], h4: [], h5: [], h6: [] };
  const re = /<(h[1-6])[^>]*>([\s\S]*?)<\/\1>/gi;
  let m;
  while ((m = re.exec(html)) !== null) {
    const tag = m[1].toLowerCase();
    result[tag].push(stripTags(decodeEntities(m[2].trim())));
  }
  return {
    counts: {
      h1: result.h1.length,
      h2: result.h2.length,
      h3: result.h3.length,
      h4: result.h4.length,
      h5: result.h5.length,
      h6: result.h6.length
    },
    texts: result
  };
}
__name(extractHeadings, "extractHeadings");
function extractImages(html) {
  const imgs = [];
  const re = /<img[^>]*>/gi;
  let m;
  while ((m = re.exec(html)) !== null) {
    const altMatch = m[0].match(/alt\s*=\s*["']([\s\S]*?)["']/i);
    const srcMatch = m[0].match(/src\s*=\s*["']([\s\S]*?)["']/i);
    imgs.push({
      src: srcMatch ? srcMatch[1] : null,
      alt: altMatch ? altMatch[1] : null,
      hasAlt: altMatch !== null && altMatch[1].trim().length > 0
    });
  }
  return {
    total: imgs.length,
    withAlt: imgs.filter((i) => i.hasAlt).length,
    withoutAlt: imgs.filter((i) => !i.hasAlt).length,
    images: imgs
  };
}
__name(extractImages, "extractImages");
function extractLinks(html, baseUrl) {
  const links = { internal: 0, external: 0, nofollow: 0, all: [] };
  const re = /<a[^>]*>/gi;
  let baseHost;
  try {
    baseHost = new URL(baseUrl).hostname;
  } catch {
    baseHost = "";
  }
  let m;
  while ((m = re.exec(html)) !== null) {
    const hrefMatch = m[0].match(/href\s*=\s*["']([\s\S]*?)["']/i);
    if (!hrefMatch) continue;
    const href = hrefMatch[1].trim();
    if (href.startsWith("#") || href.startsWith("javascript:") || href.startsWith("mailto:")) continue;
    const relMatch = m[0].match(/rel\s*=\s*["']([\s\S]*?)["']/i);
    const isNofollow = relMatch ? relMatch[1].toLowerCase().includes("nofollow") : false;
    let isExternal = false;
    try {
      const linkUrl = new URL(href, baseUrl);
      isExternal = linkUrl.hostname !== baseHost;
    } catch {
      isExternal = false;
    }
    if (isExternal) links.external++;
    else links.internal++;
    if (isNofollow) links.nofollow++;
    links.all.push({ href, external: isExternal, nofollow: isNofollow });
  }
  return {
    internal: links.internal,
    external: links.external,
    nofollow: links.nofollow,
    total: links.all.length
  };
}
__name(extractLinks, "extractLinks");
function extractCanonical(html) {
  const m = html.match(/<link[^>]+rel\s*=\s*["']canonical["'][^>]+href\s*=\s*["']([\s\S]*?)["'][^>]*>/i) || html.match(/<link[^>]+href\s*=\s*["']([\s\S]*?)["'][^>]+rel\s*=\s*["']canonical["'][^>]*>/i);
  return m ? m[1].trim() : null;
}
__name(extractCanonical, "extractCanonical");
function extractRobotsMeta(html) {
  const m = html.match(/<meta[^>]+name\s*=\s*["']robots["'][^>]+content\s*=\s*["']([\s\S]*?)["'][^>]*>/i) || html.match(/<meta[^>]+content\s*=\s*["']([\s\S]*?)["'][^>]+name\s*=\s*["']robots["'][^>]*>/i);
  return m ? m[1].trim().toLowerCase() : null;
}
__name(extractRobotsMeta, "extractRobotsMeta");
function extractOG(html) {
  const og = {};
  const re = /<meta[^>]+property\s*=\s*["'](og:[^"']+)["'][^>]+content\s*=\s*["']([\s\S]*?)["'][^>]*>/gi;
  const re2 = /<meta[^>]+content\s*=\s*["']([\s\S]*?)["'][^>]+property\s*=\s*["'](og:[^"']+)["'][^>]*>/gi;
  let m;
  while ((m = re.exec(html)) !== null) og[m[1]] = decodeEntities(m[2]);
  while ((m = re2.exec(html)) !== null) og[m[2]] = decodeEntities(m[1]);
  return Object.keys(og).length > 0 ? og : null;
}
__name(extractOG, "extractOG");
function extractTwitterCard(html) {
  const tc = {};
  const re = /<meta[^>]+(?:name|property)\s*=\s*["'](twitter:[^"']+)["'][^>]+content\s*=\s*["']([\s\S]*?)["'][^>]*>/gi;
  const re2 = /<meta[^>]+content\s*=\s*["']([\s\S]*?)["'][^>]+(?:name|property)\s*=\s*["'](twitter:[^"']+)["'][^>]*>/gi;
  let m;
  while ((m = re.exec(html)) !== null) tc[m[1]] = decodeEntities(m[2]);
  while ((m = re2.exec(html)) !== null) tc[m[2]] = decodeEntities(m[1]);
  return Object.keys(tc).length > 0 ? tc : null;
}
__name(extractTwitterCard, "extractTwitterCard");
function extractJsonLd(html) {
  const results = [];
  const re = /<script[^>]+type\s*=\s*["']application\/ld\+json["'][^>]*>([\s\S]*?)<\/script>/gi;
  let m;
  while ((m = re.exec(html)) !== null) {
    try {
      results.push(JSON.parse(m[1].trim()));
    } catch {
    }
  }
  return results.length > 0 ? results : null;
}
__name(extractJsonLd, "extractJsonLd");
function extractWordCount(html) {
  const body = html.replace(/<script[\s\S]*?<\/script>/gi, "").replace(/<style[\s\S]*?<\/style>/gi, "").replace(/<[^>]+>/g, " ").replace(/\s+/g, " ").trim();
  const words = body.split(/\s+/).filter((w) => w.length > 0);
  return words.length;
}
__name(extractWordCount, "extractWordCount");
function extractLanguage(html) {
  const m = html.match(/<html[^>]+lang\s*=\s*["']([^"']+)["']/i);
  return m ? m[1].trim() : null;
}
__name(extractLanguage, "extractLanguage");
function extractViewport(html) {
  const m = html.match(/<meta[^>]+name\s*=\s*["']viewport["'][^>]+content\s*=\s*["']([\s\S]*?)["'][^>]*>/i) || html.match(/<meta[^>]+content\s*=\s*["']([\s\S]*?)["'][^>]+name\s*=\s*["']viewport["'][^>]*>/i);
  return { present: m !== null, content: m ? m[1].trim() : null };
}
__name(extractViewport, "extractViewport");
function extractFavicon(html) {
  const m = html.match(/<link[^>]+rel\s*=\s*["'](?:shortcut )?icon["'][^>]+href\s*=\s*["']([\s\S]*?)["'][^>]*>/i) || html.match(/<link[^>]+href\s*=\s*["']([\s\S]*?)["'][^>]+rel\s*=\s*["'](?:shortcut )?icon["'][^>]*>/i);
  return { present: m !== null, href: m ? m[1].trim() : null };
}
__name(extractFavicon, "extractFavicon");
function extractHreflang(html) {
  const tags = [];
  const re = /<link[^>]+rel\s*=\s*["']alternate["'][^>]+hreflang\s*=\s*["']([^"']+)["'][^>]+href\s*=\s*["']([^"']+)["'][^>]*>/gi;
  let m;
  while ((m = re.exec(html)) !== null) tags.push({ lang: m[1], href: m[2] });
  const re2 = /<link[^>]+hreflang\s*=\s*["']([^"']+)["'][^>]+href\s*=\s*["']([^"']+)["'][^>]*rel\s*=\s*["']alternate["'][^>]*>/gi;
  while ((m = re2.exec(html)) !== null) tags.push({ lang: m[1], href: m[2] });
  return tags.length > 0 ? tags : null;
}
__name(extractHreflang, "extractHreflang");
function calculateSeoScore(data) {
  const checks = [];
  const add = /* @__PURE__ */ __name((name, pass, weight = 1) => checks.push({ name, pass, weight }), "add");
  add("Has title", !!data.title.text, 5);
  add("Title optimal length (30-60)", data.title.optimal, 5);
  add("Title not too long (\u226470)", data.title.length <= 70, 5);
  add("Has meta description", !!data.metaDescription.text, 5);
  add("Description optimal length (120-160)", data.metaDescription.optimal, 5);
  add("Description not empty", data.metaDescription.length > 0, 5);
  add("Has H1", data.headings.counts.h1 > 0, 5);
  add("Single H1", data.headings.counts.h1 === 1, 5);
  add("Has H2 subheadings", data.headings.counts.h2 > 0, 5);
  add("All images have alt text", data.images.total === 0 || data.images.withoutAlt === 0, 5);
  add("Has images", data.images.total > 0, 5);
  add("Has internal links", data.links.internal > 0, 5);
  add("Has canonical URL", !!data.canonical, 5);
  add("Has viewport meta", data.viewport.present, 5);
  add("Has favicon", data.favicon.present, 5);
  add("Has language attribute", !!data.language, 5);
  add("Not blocked by robots", data.robotsMeta !== "noindex", 5);
  add("Has Open Graph tags", !!data.openGraph, 5);
  add("Has Twitter Card tags", !!data.twitterCard, 5);
  add("Has JSON-LD structured data", !!data.jsonLd, 5);
  const maxScore = checks.reduce((s, c) => s + c.weight, 0);
  const earned = checks.reduce((s, c) => s + (c.pass ? c.weight : 0), 0);
  const score = Math.round(earned / maxScore * 100);
  return { score, maxPoints: maxScore, earnedPoints: earned, checks };
}
__name(calculateSeoScore, "calculateSeoScore");
function decodeEntities(str) {
  return str.replace(/&amp;/g, "&").replace(/&lt;/g, "<").replace(/&gt;/g, ">").replace(/&quot;/g, '"').replace(/&#39;/g, "'").replace(/&#x27;/g, "'").replace(/&#(\d+);/g, (_, n) => String.fromCharCode(n));
}
__name(decodeEntities, "decodeEntities");
function stripTags(str) {
  return str.replace(/<[^>]+>/g, "").trim();
}
__name(stripTags, "stripTags");

// src/index.js
var rateMap = /* @__PURE__ */ new Map();
var RATE_LIMIT = 20;
var RATE_WINDOW = 6e4;
var MAX_MAP_SIZE = 5e3;
function checkRateLimit(ip) {
  const now = Date.now();
  if (rateMap.size > MAX_MAP_SIZE) {
    for (const [key, entry2] of rateMap) {
      if (now - entry2.start > RATE_WINDOW) rateMap.delete(key);
      if (rateMap.size <= MAX_MAP_SIZE / 2) break;
    }
  }
  const entry = rateMap.get(ip);
  if (!entry || now - entry.start > RATE_WINDOW) {
    rateMap.set(ip, { start: now, count: 1 });
    return { allowed: true, remaining: RATE_LIMIT - 1 };
  }
  entry.count++;
  if (entry.count > RATE_LIMIT) {
    return { allowed: false, remaining: 0, retryAfter: Math.ceil((entry.start + RATE_WINDOW - now) / 1e3) };
  }
  return { allowed: true, remaining: RATE_LIMIT - entry.count };
}
__name(checkRateLimit, "checkRateLimit");
function cors(headers = {}) {
  return {
    "Access-Control-Allow-Origin": "*",
    "Access-Control-Allow-Methods": "GET, OPTIONS",
    "Access-Control-Allow-Headers": "Content-Type",
    "Content-Type": "application/json",
    ...headers
  };
}
__name(cors, "cors");
function json(data, status = 200, extra = {}) {
  if (status === 200 && typeof data === "object" && !Array.isArray(data)) {
    data._upgrade = { note: "Upgrade for higher limits & priority support", url: "https://rapidapi.com/miccho27-5OJaGGbBiO/api/seo-analyzer-api/pricing" };
  }
  return new Response(JSON.stringify(data, null, 2), { status, headers: cors(extra) });
}
__name(json, "json");
function error(message, status = 400) {
  return json({ error: message }, status);
}
__name(error, "error");
function validateUrl(raw) {
  if (!raw) return { valid: false, msg: "Missing required parameter: url" };
  try {
    const u = new URL(raw);
    if (!["http:", "https:"].includes(u.protocol)) return { valid: false, msg: "URL must use http or https" };
    return { valid: true, url: u.href };
  } catch {
    return { valid: false, msg: "Invalid URL format" };
  }
}
__name(validateUrl, "validateUrl");
async function fetchPage(url) {
  const res = await fetch(url, {
    headers: {
      "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
      "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
      "Accept-Language": "en-US,en;q=0.5"
    },
    redirect: "follow"
  });
  if (!res.ok) throw new Error(`Failed to fetch URL: HTTP ${res.status}`);
  const html = await res.text();
  return { html, size: new TextEncoder().encode(html).length, finalUrl: res.url };
}
__name(fetchPage, "fetchPage");
function fullAnalysis(html, url, size) {
  const title = extractTitle(html);
  const metaDescription = extractMetaDescription(html);
  const headings = extractHeadings(html);
  const images = extractImages(html);
  const links = extractLinks(html, url);
  const canonical = extractCanonical(html);
  const robotsMeta = extractRobotsMeta(html);
  const openGraph = extractOG(html);
  const twitterCard = extractTwitterCard(html);
  const jsonLd = extractJsonLd(html);
  const wordCount = extractWordCount(html);
  const language = extractLanguage(html);
  const viewport = extractViewport(html);
  const favicon = extractFavicon(html);
  const hreflang = extractHreflang(html);
  const data = {
    title,
    metaDescription,
    headings,
    images,
    links,
    canonical,
    robotsMeta,
    openGraph,
    twitterCard,
    jsonLd,
    wordCount,
    language,
    viewport,
    favicon,
    hreflang
  };
  const seoScore = calculateSeoScore(data);
  return { url, pageSize: size, ...data, seoScore };
}
__name(fullAnalysis, "fullAnalysis");
var index_default = {
  async fetch(request) {
    if (request.method === "OPTIONS") {
      return new Response(null, { status: 204, headers: cors() });
    }
    if (request.method !== "GET") {
      return error("Method not allowed", 405);
    }
    const ip = request.headers.get("CF-Connecting-IP") || "unknown";
    const rl = checkRateLimit(ip);
    if (!rl.allowed) {
      return error(
        "Rate limit exceeded. Max 20 requests per minute.",
        429,
        { "Retry-After": String(rl.retryAfter), "X-RateLimit-Remaining": "0" }
      );
    }
    const rlHeaders = { "X-RateLimit-Remaining": String(rl.remaining) };
    const { pathname, searchParams } = new URL(request.url);
    if (pathname === "/") {
      return json({
        name: "SEO Analyzer API",
        _premium: {
          message: "You are using the FREE tier of SEO Analyzer API. Upgrade to Pro for higher rate limits, priority support, and advanced features.",
          upgrade_url: "https://rapidapi.com/miccho27-5OJaGGbBiO/api/seo-analyzer-api/pricing",
          plans: ["Pro ($5.99/mo)", "Ultra ($14.99/mo)", "Mega ($49.99/mo)"]
        },
        endpoints: {
          "/analyze?url=": "Full SEO analysis of a page",
          "/headings?url=": "Heading structure only",
          "/links?url=": "Link analysis only",
          "/score?url=": "SEO score with breakdown"
        }
      }, 200, rlHeaders);
    }
    const v = validateUrl(searchParams.get("url"));
    if (!v.valid) return error(v.msg);
    try {
      const { html, size, finalUrl } = await fetchPage(v.url);
      if (pathname === "/analyze") {
        return json(fullAnalysis(html, finalUrl, size), 200, rlHeaders);
      }
      if (pathname === "/headings") {
        return json({ url: finalUrl, headings: extractHeadings(html) }, 200, rlHeaders);
      }
      if (pathname === "/links") {
        return json({ url: finalUrl, links: extractLinks(html, finalUrl) }, 200, rlHeaders);
      }
      if (pathname === "/score") {
        const analysis = fullAnalysis(html, finalUrl, size);
        return json({ url: finalUrl, seoScore: analysis.seoScore }, 200, rlHeaders);
      }
      return error("Not found", 404);
    } catch (e) {
      return error(`Failed to analyze URL: ${e.message}`, 502);
    }
  }
};
export {
  index_default as default
};
//# sourceMappingURL=index.js.map
