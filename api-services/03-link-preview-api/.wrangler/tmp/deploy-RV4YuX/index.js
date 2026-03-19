var __defProp = Object.defineProperty;
var __name = (target, value) => __defProp(target, "name", { value, configurable: true });

// src/parser.js
function firstMatch(html, patterns) {
  for (const pattern of patterns) {
    const match = html.match(pattern);
    if (match && match[1]) {
      return decodeHtmlEntities(match[1].trim());
    }
  }
  return null;
}
__name(firstMatch, "firstMatch");
function decodeHtmlEntities(str) {
  return str.replace(/&amp;/g, "&").replace(/&lt;/g, "<").replace(/&gt;/g, ">").replace(/&quot;/g, '"').replace(/&#39;/g, "'").replace(/&#x27;/g, "'").replace(/&#x2F;/g, "/");
}
__name(decodeHtmlEntities, "decodeHtmlEntities");
function resolveUrl(relative, base) {
  if (!relative)
    return null;
  try {
    return new URL(relative, base).href;
  } catch {
    return null;
  }
}
__name(resolveUrl, "resolveUrl");
function parseMetadata(html, url) {
  const title = firstMatch(html, [
    /<meta[^>]+property=["']og:title["'][^>]+content=["']([^"']+)["']/i,
    /<meta[^>]+content=["']([^"']+)["'][^>]+property=["']og:title["']/i,
    /<meta[^>]+name=["']twitter:title["'][^>]+content=["']([^"']+)["']/i,
    /<meta[^>]+content=["']([^"']+)["'][^>]+name=["']twitter:title["']/i,
    /<title[^>]*>([^<]+)<\/title>/i
  ]);
  const description = firstMatch(html, [
    /<meta[^>]+property=["']og:description["'][^>]+content=["']([^"']+)["']/i,
    /<meta[^>]+content=["']([^"']+)["'][^>]+property=["']og:description["']/i,
    /<meta[^>]+name=["']description["'][^>]+content=["']([^"']+)["']/i,
    /<meta[^>]+content=["']([^"']+)["'][^>]+name=["']description["']/i
  ]);
  const rawImage = firstMatch(html, [
    /<meta[^>]+property=["']og:image["'][^>]+content=["']([^"']+)["']/i,
    /<meta[^>]+content=["']([^"']+)["'][^>]+property=["']og:image["']/i,
    /<meta[^>]+name=["']twitter:image["'][^>]+content=["']([^"']+)["']/i,
    /<meta[^>]+content=["']([^"']+)["'][^>]+name=["']twitter:image["']/i
  ]);
  const image = resolveUrl(rawImage, url);
  const rawFavicon = firstMatch(html, [
    /<link[^>]+rel=["'](?:shortcut )?icon["'][^>]+href=["']([^"']+)["']/i,
    /<link[^>]+href=["']([^"']+)["'][^>]+rel=["'](?:shortcut )?icon["']/i,
    /<link[^>]+rel=["']apple-touch-icon["'][^>]+href=["']([^"']+)["']/i,
    /<link[^>]+href=["']([^"']+)["'][^>]+rel=["']apple-touch-icon["']/i
  ]);
  const favicon = rawFavicon ? resolveUrl(rawFavicon, url) : resolveUrl("/favicon.ico", url);
  const siteName = firstMatch(html, [
    /<meta[^>]+property=["']og:site_name["'][^>]+content=["']([^"']+)["']/i,
    /<meta[^>]+content=["']([^"']+)["'][^>]+property=["']og:site_name["']/i
  ]);
  const type = firstMatch(html, [
    /<meta[^>]+property=["']og:type["'][^>]+content=["']([^"']+)["']/i,
    /<meta[^>]+content=["']([^"']+)["'][^>]+property=["']og:type["']/i
  ]) || "website";
  const author = firstMatch(html, [
    /<meta[^>]+name=["']author["'][^>]+content=["']([^"']+)["']/i,
    /<meta[^>]+content=["']([^"']+)["'][^>]+name=["']author["']/i,
    /<meta[^>]+property=["']article:author["'][^>]+content=["']([^"']+)["']/i,
    /<meta[^>]+content=["']([^"']+)["'][^>]+property=["']article:author["']/i
  ]);
  const publishedDate = firstMatch(html, [
    /<meta[^>]+property=["']article:published_time["'][^>]+content=["']([^"']+)["']/i,
    /<meta[^>]+content=["']([^"']+)["'][^>]+property=["']article:published_time["']/i,
    /<meta[^>]+name=["']date["'][^>]+content=["']([^"']+)["']/i,
    /<meta[^>]+content=["']([^"']+)["'][^>]+name=["']date["']/i,
    /<time[^>]+datetime=["']([^"']+)["']/i
  ]);
  const language = firstMatch(html, [
    /<html[^>]+lang=["']([^"']+)["']/i,
    /<meta[^>]+property=["']og:locale["'][^>]+content=["']([^"']+)["']/i,
    /<meta[^>]+content=["']([^"']+)["'][^>]+property=["']og:locale["']/i,
    /<meta[^>]+http-equiv=["']content-language["'][^>]+content=["']([^"']+)["']/i
  ]);
  const rawKeywords = firstMatch(html, [
    /<meta[^>]+name=["']keywords["'][^>]+content=["']([^"']+)["']/i,
    /<meta[^>]+content=["']([^"']+)["'][^>]+name=["']keywords["']/i
  ]);
  const keywords = rawKeywords ? rawKeywords.split(",").map((k) => k.trim()).filter(Boolean) : [];
  const twitterCard = firstMatch(html, [
    /<meta[^>]+name=["']twitter:card["'][^>]+content=["']([^"']+)["']/i,
    /<meta[^>]+content=["']([^"']+)["'][^>]+name=["']twitter:card["']/i
  ]);
  const twitterSite = firstMatch(html, [
    /<meta[^>]+name=["']twitter:site["'][^>]+content=["']([^"']+)["']/i,
    /<meta[^>]+content=["']([^"']+)["'][^>]+name=["']twitter:site["']/i
  ]);
  const twitter = twitterCard || twitterSite ? { card: twitterCard || null, site: twitterSite || null } : null;
  const themeColor = firstMatch(html, [
    /<meta[^>]+name=["']theme-color["'][^>]+content=["']([^"']+)["']/i,
    /<meta[^>]+content=["']([^"']+)["'][^>]+name=["']theme-color["']/i
  ]);
  const canonical = firstMatch(html, [
    /<link[^>]+rel=["']canonical["'][^>]+href=["']([^"']+)["']/i,
    /<link[^>]+href=["']([^"']+)["'][^>]+rel=["']canonical["']/i,
    /<meta[^>]+property=["']og:url["'][^>]+content=["']([^"']+)["']/i,
    /<meta[^>]+content=["']([^"']+)["'][^>]+property=["']og:url["']/i
  ]);
  const feeds = [];
  const feedRegex = /<link[^>]+type=["'](application\/(?:rss|atom)\+xml)["'][^>]*>/gi;
  let feedMatch;
  while ((feedMatch = feedRegex.exec(html)) !== null) {
    const tag = feedMatch[0];
    const hrefMatch = tag.match(/href=["']([^"']+)["']/i);
    const titleMatch = tag.match(/title=["']([^"']+)["']/i);
    if (hrefMatch) {
      feeds.push({
        url: resolveUrl(hrefMatch[1], url),
        type: feedMatch[1],
        title: titleMatch ? decodeHtmlEntities(titleMatch[1]) : null
      });
    }
  }
  return {
    title,
    description,
    image,
    favicon,
    siteName,
    type,
    author,
    publishedDate,
    language,
    keywords,
    twitter,
    themeColor,
    canonical,
    feeds
  };
}
__name(parseMetadata, "parseMetadata");

// src/index.js
var CORS_HEADERS = {
  "Access-Control-Allow-Origin": "*",
  "Access-Control-Allow-Methods": "GET, POST, OPTIONS",
  "Access-Control-Allow-Headers": "Content-Type, X-RapidAPI-Proxy-Secret"
};
function jsonResponse(data, status = 200) {
  if (status === 200 && typeof data === "object" && !Array.isArray(data)) {
    data._upgrade = { note: "Upgrade for higher limits & priority support", url: "https://rapidapi.com/miccho27-5OJaGGbBiO/api/link-preview-api/pricing" };
  }
  return new Response(JSON.stringify(data), {
    status,
    headers: { "Content-Type": "application/json", ...CORS_HEADERS }
  });
}
__name(jsonResponse, "jsonResponse");
async function fetchPreview(targetUrl, env) {
  const timeout = parseInt(env.FETCH_TIMEOUT) || 5e3;
  const cacheTtl = parseInt(env.CACHE_TTL) || 3600;
  const cacheKey = new Request(`https://link-preview-cache/${encodeURIComponent(targetUrl)}`);
  const cache = caches.default;
  const cached = await cache.match(cacheKey);
  if (cached) {
    const data = await cached.json();
    data._cached = true;
    return data;
  }
  const start = Date.now();
  const controller = new AbortController();
  const timer = setTimeout(() => controller.abort(), timeout);
  let response;
  try {
    response = await fetch(targetUrl, {
      signal: controller.signal,
      headers: {
        "User-Agent": "LinkPreviewBot/1.0 (compatible; Cloudflare Worker)",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.5"
      },
      redirect: "follow"
    });
  } catch (err) {
    if (err.name === "AbortError") {
      return { url: targetUrl, error: "Timeout: page took longer than 5 seconds to respond" };
    }
    return { url: targetUrl, error: `Fetch failed: ${err.message}` };
  } finally {
    clearTimeout(timer);
  }
  const contentType = response.headers.get("content-type") || "";
  if (!contentType.includes("text/html") && !contentType.includes("application/xhtml+xml")) {
    return {
      url: targetUrl,
      error: `Non-HTML response: ${contentType.split(";")[0].trim()}`
    };
  }
  const html = await response.text();
  const metadata = parseMetadata(html, response.url);
  const responseTime = Date.now() - start;
  const result = {
    url: response.url,
    ...metadata,
    responseTime
  };
  const cacheResponse = new Response(JSON.stringify(result), {
    headers: {
      "Content-Type": "application/json",
      "Cache-Control": `s-maxage=${cacheTtl}`
    }
  });
  await cache.put(cacheKey, cacheResponse);
  return result;
}
__name(fetchPreview, "fetchPreview");
var src_default = {
  async fetch(request, env) {
    if (request.method === "OPTIONS") {
      return new Response(null, { status: 204, headers: CORS_HEADERS });
    }
    const url = new URL(request.url);
    const path = url.pathname;
    if (path === "/" && request.method === "GET") {
      return jsonResponse({
        service: "Link Preview API",
        _premium: {
          message: "You are using the FREE tier of Link Preview API. Upgrade to Pro for higher rate limits, priority support, and advanced features.",
          upgrade_url: "https://rapidapi.com/miccho27-5OJaGGbBiO/api/link-preview-api/pricing",
          plans: ["Pro ($5.99/mo)", "Ultra ($14.99/mo)", "Mega ($49.99/mo)"]
        },
        endpoints: {
          "GET /preview?url=": "Get metadata for a single URL",
          "POST /preview/bulk": 'Get metadata for multiple URLs (JSON body: { "urls": [...] })'
        }
      });
    }
    if (path === "/preview" && request.method === "GET") {
      const targetUrl = url.searchParams.get("url");
      if (!targetUrl) {
        return jsonResponse({ error: "Missing required query parameter: url" }, 400);
      }
      try {
        new URL(targetUrl);
      } catch {
        return jsonResponse({ error: "Invalid URL format" }, 400);
      }
      const result = await fetchPreview(targetUrl, env);
      return jsonResponse(result, result.error ? 502 : 200);
    }
    if (path === "/preview/bulk" && request.method === "POST") {
      let body;
      try {
        body = await request.json();
      } catch {
        return jsonResponse({ error: "Invalid JSON body" }, 400);
      }
      const urls = body.urls;
      if (!Array.isArray(urls) || urls.length === 0) {
        return jsonResponse({ error: 'Body must contain a non-empty "urls" array' }, 400);
      }
      const maxBulk = parseInt(env.MAX_BULK_URLS) || 10;
      if (urls.length > maxBulk) {
        return jsonResponse({ error: `Maximum ${maxBulk} URLs per request` }, 400);
      }
      for (const u of urls) {
        try {
          new URL(u);
        } catch {
          return jsonResponse({ error: `Invalid URL: ${u}` }, 400);
        }
      }
      const results = await Promise.all(urls.map((u) => fetchPreview(u, env)));
      return jsonResponse({ results });
    }
    return jsonResponse({ error: "Not found" }, 404);
  }
};
export {
  src_default as default
};
//# sourceMappingURL=index.js.map
