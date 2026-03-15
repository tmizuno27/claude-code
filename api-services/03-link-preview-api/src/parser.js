/**
 * HTML Metadata Parser
 * Extracts Open Graph, Twitter Card, meta tags, and link tags from HTML.
 */

/**
 * Get the first matching value from a list of regex results.
 */
function firstMatch(html, patterns) {
  for (const pattern of patterns) {
    const match = html.match(pattern);
    if (match && match[1]) {
      return decodeHtmlEntities(match[1].trim());
    }
  }
  return null;
}

/**
 * Decode common HTML entities.
 */
function decodeHtmlEntities(str) {
  return str
    .replace(/&amp;/g, '&')
    .replace(/&lt;/g, '<')
    .replace(/&gt;/g, '>')
    .replace(/&quot;/g, '"')
    .replace(/&#39;/g, "'")
    .replace(/&#x27;/g, "'")
    .replace(/&#x2F;/g, '/');
}

/**
 * Resolve a potentially relative URL against a base URL.
 */
function resolveUrl(relative, base) {
  if (!relative) return null;
  try {
    return new URL(relative, base).href;
  } catch {
    return null;
  }
}

/**
 * Extract all metadata from an HTML string.
 * @param {string} html - Raw HTML content
 * @param {string} url - The page URL (for resolving relative URLs)
 * @returns {object} Parsed metadata
 */
export function parseMetadata(html, url) {
  // Title
  const title = firstMatch(html, [
    /<meta[^>]+property=["']og:title["'][^>]+content=["']([^"']+)["']/i,
    /<meta[^>]+content=["']([^"']+)["'][^>]+property=["']og:title["']/i,
    /<meta[^>]+name=["']twitter:title["'][^>]+content=["']([^"']+)["']/i,
    /<meta[^>]+content=["']([^"']+)["'][^>]+name=["']twitter:title["']/i,
    /<title[^>]*>([^<]+)<\/title>/i,
  ]);

  // Description
  const description = firstMatch(html, [
    /<meta[^>]+property=["']og:description["'][^>]+content=["']([^"']+)["']/i,
    /<meta[^>]+content=["']([^"']+)["'][^>]+property=["']og:description["']/i,
    /<meta[^>]+name=["']description["'][^>]+content=["']([^"']+)["']/i,
    /<meta[^>]+content=["']([^"']+)["'][^>]+name=["']description["']/i,
  ]);

  // Image
  const rawImage = firstMatch(html, [
    /<meta[^>]+property=["']og:image["'][^>]+content=["']([^"']+)["']/i,
    /<meta[^>]+content=["']([^"']+)["'][^>]+property=["']og:image["']/i,
    /<meta[^>]+name=["']twitter:image["'][^>]+content=["']([^"']+)["']/i,
    /<meta[^>]+content=["']([^"']+)["'][^>]+name=["']twitter:image["']/i,
  ]);
  const image = resolveUrl(rawImage, url);

  // Favicon
  const rawFavicon = firstMatch(html, [
    /<link[^>]+rel=["'](?:shortcut )?icon["'][^>]+href=["']([^"']+)["']/i,
    /<link[^>]+href=["']([^"']+)["'][^>]+rel=["'](?:shortcut )?icon["']/i,
    /<link[^>]+rel=["']apple-touch-icon["'][^>]+href=["']([^"']+)["']/i,
    /<link[^>]+href=["']([^"']+)["'][^>]+rel=["']apple-touch-icon["']/i,
  ]);
  const favicon = rawFavicon
    ? resolveUrl(rawFavicon, url)
    : resolveUrl('/favicon.ico', url);

  // Site name
  const siteName = firstMatch(html, [
    /<meta[^>]+property=["']og:site_name["'][^>]+content=["']([^"']+)["']/i,
    /<meta[^>]+content=["']([^"']+)["'][^>]+property=["']og:site_name["']/i,
  ]);

  // Type
  const type = firstMatch(html, [
    /<meta[^>]+property=["']og:type["'][^>]+content=["']([^"']+)["']/i,
    /<meta[^>]+content=["']([^"']+)["'][^>]+property=["']og:type["']/i,
  ]) || 'website';

  // Author
  const author = firstMatch(html, [
    /<meta[^>]+name=["']author["'][^>]+content=["']([^"']+)["']/i,
    /<meta[^>]+content=["']([^"']+)["'][^>]+name=["']author["']/i,
    /<meta[^>]+property=["']article:author["'][^>]+content=["']([^"']+)["']/i,
    /<meta[^>]+content=["']([^"']+)["'][^>]+property=["']article:author["']/i,
  ]);

  // Published date
  const publishedDate = firstMatch(html, [
    /<meta[^>]+property=["']article:published_time["'][^>]+content=["']([^"']+)["']/i,
    /<meta[^>]+content=["']([^"']+)["'][^>]+property=["']article:published_time["']/i,
    /<meta[^>]+name=["']date["'][^>]+content=["']([^"']+)["']/i,
    /<meta[^>]+content=["']([^"']+)["'][^>]+name=["']date["']/i,
    /<time[^>]+datetime=["']([^"']+)["']/i,
  ]);

  // Language
  const language = firstMatch(html, [
    /<html[^>]+lang=["']([^"']+)["']/i,
    /<meta[^>]+property=["']og:locale["'][^>]+content=["']([^"']+)["']/i,
    /<meta[^>]+content=["']([^"']+)["'][^>]+property=["']og:locale["']/i,
    /<meta[^>]+http-equiv=["']content-language["'][^>]+content=["']([^"']+)["']/i,
  ]);

  // Keywords
  const rawKeywords = firstMatch(html, [
    /<meta[^>]+name=["']keywords["'][^>]+content=["']([^"']+)["']/i,
    /<meta[^>]+content=["']([^"']+)["'][^>]+name=["']keywords["']/i,
  ]);
  const keywords = rawKeywords
    ? rawKeywords.split(',').map(k => k.trim()).filter(Boolean)
    : [];

  // Twitter card
  const twitterCard = firstMatch(html, [
    /<meta[^>]+name=["']twitter:card["'][^>]+content=["']([^"']+)["']/i,
    /<meta[^>]+content=["']([^"']+)["'][^>]+name=["']twitter:card["']/i,
  ]);
  const twitterSite = firstMatch(html, [
    /<meta[^>]+name=["']twitter:site["'][^>]+content=["']([^"']+)["']/i,
    /<meta[^>]+content=["']([^"']+)["'][^>]+name=["']twitter:site["']/i,
  ]);
  const twitter = (twitterCard || twitterSite)
    ? { card: twitterCard || null, site: twitterSite || null }
    : null;

  // Theme color
  const themeColor = firstMatch(html, [
    /<meta[^>]+name=["']theme-color["'][^>]+content=["']([^"']+)["']/i,
    /<meta[^>]+content=["']([^"']+)["'][^>]+name=["']theme-color["']/i,
  ]);

  // Canonical URL
  const canonical = firstMatch(html, [
    /<link[^>]+rel=["']canonical["'][^>]+href=["']([^"']+)["']/i,
    /<link[^>]+href=["']([^"']+)["'][^>]+rel=["']canonical["']/i,
    /<meta[^>]+property=["']og:url["'][^>]+content=["']([^"']+)["']/i,
    /<meta[^>]+content=["']([^"']+)["'][^>]+property=["']og:url["']/i,
  ]);

  // RSS/Atom feeds
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
        title: titleMatch ? decodeHtmlEntities(titleMatch[1]) : null,
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
    feeds,
  };
}
