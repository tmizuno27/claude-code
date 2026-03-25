/**
 * Extract text by regex.
 */
function extractText(html, pattern, group = 1) {
  const match = html.match(pattern);
  return match ? match[group].trim() : null;
}

function decodeEntities(str) {
  if (!str) return str;
  return str
    .replace(/&amp;/g, '&')
    .replace(/&lt;/g, '<')
    .replace(/&gt;/g, '>')
    .replace(/&quot;/g, '"')
    .replace(/&#39;/g, "'");
}

/**
 * Parse Google Maps search results from page HTML.
 * Google Maps is heavily JS-rendered, so we parse embedded JSON data.
 */
export function parseSearchResults(html, maxResults) {
  const results = [];

  // Try to extract from embedded JSON data (window.APP_INITIALIZATION_STATE or similar)
  const jsonPatterns = [
    /window\.APP_INITIALIZATION_STATE\s*=\s*(\[[\s\S]*?\]);/,
    /\["([^"]{1,200})",\s*"([^"]*)",\s*([0-9.]+),\s*(-?[0-9.]+),\s*(-?[0-9.]+)/g,
  ];

  // Fallback: extract from structured data / microdata
  const ldJsonRegex = /<script type="application\/ld\+json">([\s\S]*?)<\/script>/gi;
  let ldMatch;
  while ((ldMatch = ldJsonRegex.exec(html)) !== null && results.length < maxResults) {
    try {
      const data = JSON.parse(ldMatch[1]);
      const items = Array.isArray(data) ? data : [data];
      for (const item of items) {
        if (item['@type'] === 'LocalBusiness' || item['@type'] === 'Restaurant' || item.name) {
          results.push({
            name: item.name || null,
            address: item.address?.streetAddress || item.address || null,
            phone: item.telephone || null,
            rating: item.aggregateRating?.ratingValue
              ? parseFloat(item.aggregateRating.ratingValue)
              : null,
            reviewCount: item.aggregateRating?.reviewCount
              ? parseInt(item.aggregateRating.reviewCount, 10)
              : null,
            category: item['@type'] || null,
            website: item.url || null,
            latitude: item.geo?.latitude || null,
            longitude: item.geo?.longitude || null,
          });
        }
      }
    } catch {
      // Skip invalid JSON
    }
  }

  // Also try to extract from aria-label patterns common in Maps HTML
  const placeRegex = /aria-label="([^"]+)"[^>]*data-value="([^"]*)"/gi;
  let placeMatch;
  while ((placeMatch = placeRegex.exec(html)) !== null && results.length < maxResults) {
    const name = decodeEntities(placeMatch[1]);
    if (name && name.length > 2 && !results.some((r) => r.name === name)) {
      results.push({
        name,
        address: null,
        phone: null,
        rating: null,
        reviewCount: null,
        category: null,
        website: null,
      });
    }
  }

  return results.slice(0, maxResults);
}

/**
 * Parse a Google Maps place detail page.
 */
export function parsePlaceDetails(html) {
  const name = extractText(html, /<meta[^>]*property="og:title"[^>]*content="([^"]+)"/i)
    || extractText(html, /<title>([^<]+)<\/title>/i);

  const description = extractText(html, /<meta[^>]*property="og:description"[^>]*content="([^"]+)"/i);

  // Try structured data
  let structuredData = null;
  const ldMatch = html.match(/<script type="application\/ld\+json">([\s\S]*?)<\/script>/i);
  if (ldMatch) {
    try {
      structuredData = JSON.parse(ldMatch[1]);
    } catch {
      // ignore
    }
  }

  const phone = structuredData?.telephone
    || extractText(html, /data-tooltip="Call[^"]*"[^>]*aria-label="([^"]+)"/i)
    || extractText(html, /"telephone"\s*:\s*"([^"]+)"/);

  const website = structuredData?.url
    || extractText(html, /data-tooltip="Open website"[^>]*href="([^"]+)"/i);

  const address = structuredData?.address?.streetAddress
    || extractText(html, /"streetAddress"\s*:\s*"([^"]+)"/);

  const rating = structuredData?.aggregateRating?.ratingValue
    ? parseFloat(structuredData.aggregateRating.ratingValue)
    : null;

  const reviewCount = structuredData?.aggregateRating?.reviewCount
    ? parseInt(structuredData.aggregateRating.reviewCount, 10)
    : null;

  const lat = extractText(html, /"latitude"\s*:\s*(-?[\d.]+)/);
  const lng = extractText(html, /"longitude"\s*:\s*(-?[\d.]+)/);

  // Opening hours
  const hoursMatch = html.match(/"openingHours"\s*:\s*(\[[^\]]+\])/);
  let openingHours = null;
  if (hoursMatch) {
    try {
      openingHours = JSON.parse(hoursMatch[1]);
    } catch {
      // ignore
    }
  }

  return {
    name: name ? decodeEntities(name) : null,
    description: description ? decodeEntities(description) : null,
    address,
    phone,
    website,
    rating,
    reviewCount,
    latitude: lat ? parseFloat(lat) : null,
    longitude: lng ? parseFloat(lng) : null,
    openingHours,
    scrapedAt: new Date().toISOString(),
  };
}
