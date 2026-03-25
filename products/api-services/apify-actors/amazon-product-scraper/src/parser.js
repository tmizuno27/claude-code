/**
 * Extract text content matching a regex pattern from HTML.
 */
function extractText(html, pattern, group = 1) {
  const match = html.match(pattern);
  return match ? match[group].trim() : null;
}

/**
 * Decode HTML entities.
 */
function decodeEntities(str) {
  if (!str) return str;
  return str
    .replace(/&amp;/g, '&')
    .replace(/&lt;/g, '<')
    .replace(/&gt;/g, '>')
    .replace(/&quot;/g, '"')
    .replace(/&#39;/g, "'")
    .replace(/&#x27;/g, "'");
}

/**
 * Extract ASIN from URL or HTML.
 */
function extractAsin(html, url) {
  const urlMatch = url.match(/\/dp\/([A-Z0-9]{10})/i) || url.match(/\/product\/([A-Z0-9]{10})/i);
  if (urlMatch) return urlMatch[1].toUpperCase();

  const htmlMatch = html.match(/"ASIN"\s*:\s*"([A-Z0-9]{10})"/i);
  return htmlMatch ? htmlMatch[1].toUpperCase() : null;
}

/**
 * Parse a single Amazon product page.
 */
export function parseProductPage(html, url) {
  const title = decodeEntities(
    extractText(html, /<span[^>]*id="productTitle"[^>]*>([\s\S]*?)<\/span>/i)
  );

  const priceWhole = extractText(html, /<span class="a-price-whole">([\d,.]+)<\/span>/);
  const priceFraction = extractText(html, /<span class="a-price-fraction">(\d+)<\/span>/);
  const price = priceWhole ? `${priceWhole}${priceFraction ? '.' + priceFraction : ''}` : null;

  const currency = extractText(html, /<span class="a-price-symbol">([^<]+)<\/span>/);

  const ratingText = extractText(html, /<span[^>]*class="a-icon-alt"[^>]*>([0-9.]+) out of/);
  const rating = ratingText ? parseFloat(ratingText) : null;

  const reviewCountText = extractText(html, /<span[^>]*id="acrCustomerReviewText"[^>]*>([\d,]+)/);
  const reviewCount = reviewCountText ? parseInt(reviewCountText.replace(/,/g, ''), 10) : null;

  const availability = extractText(html, /<div[^>]*id="availability"[^>]*>[\s\S]*?<span[^>]*>([\s\S]*?)<\/span>/i);

  const brand = extractText(html, /Visit the\s+<a[^>]*>([^<]+)<\/a>\s+Store/i)
    || extractText(html, /"brand"\s*:\s*"([^"]+)"/i);

  const mainImage = extractText(html, /"hiRes"\s*:\s*"([^"]+)"/);

  const asin = extractAsin(html, url);

  // Feature bullets
  const bulletSection = html.match(/<div[^>]*id="feature-bullets"[^>]*>([\s\S]*?)<\/div>/i);
  const features = [];
  if (bulletSection) {
    const bulletRegex = /<span class="a-list-item">\s*([\s\S]*?)\s*<\/span>/gi;
    let m;
    while ((m = bulletRegex.exec(bulletSection[1])) !== null) {
      const text = m[1].replace(/<[^>]+>/g, '').trim();
      if (text && text.length > 2) features.push(decodeEntities(text));
    }
  }

  // Best Sellers Rank
  const bsrMatch = html.match(/#([\d,]+)\s+in\s+([^<(]+)/);
  const bestSellersRank = bsrMatch
    ? { rank: parseInt(bsrMatch[1].replace(/,/g, ''), 10), category: bsrMatch[2].trim() }
    : null;

  return {
    url,
    asin,
    title,
    brand: brand ? decodeEntities(brand) : null,
    price,
    currency: currency ? decodeEntities(currency) : null,
    rating,
    reviewCount,
    availability: availability ? availability.replace(/<[^>]+>/g, '').trim() : null,
    features,
    bestSellersRank,
    mainImage,
    scrapedAt: new Date().toISOString(),
  };
}

/**
 * Parse Amazon search results page.
 */
export function parseSearchPage(html, marketplace, maxResults) {
  const results = [];
  const itemRegex = /<div[^>]*data-asin="([A-Z0-9]{10})"[^>]*data-component-type="s-search-result"[^>]*>([\s\S]*?)<\/div>\s*<\/div>\s*<\/div>\s*<\/div>/gi;

  let match;
  while ((match = itemRegex.exec(html)) !== null && results.length < maxResults) {
    const asin = match[1];
    const block = match[2];

    const title = decodeEntities(
      extractText(block, /<span[^>]*class="a-text-normal"[^>]*>([\s\S]*?)<\/span>/i)
      || extractText(block, /<h2[^>]*>([\s\S]*?)<\/h2>/i)
    );

    const priceWhole = extractText(block, /<span class="a-price-whole">([\d,.]+)<\/span>/);
    const priceFraction = extractText(block, /<span class="a-price-fraction">(\d+)<\/span>/);
    const price = priceWhole ? `${priceWhole}${priceFraction ? '.' + priceFraction : ''}` : null;

    const ratingText = extractText(block, /<span[^>]*class="a-icon-alt"[^>]*>([0-9.]+) out of/);
    const rating = ratingText ? parseFloat(ratingText) : null;

    const reviewText = extractText(block, /<span[^>]*class="a-size-base[^"]*"[^>]*>([\d,]+)<\/span>/);
    const reviewCount = reviewText ? parseInt(reviewText.replace(/,/g, ''), 10) : null;

    const image = extractText(block, /<img[^>]*class="s-image"[^>]*src="([^"]+)"/i);

    const productUrl = `https://www.amazon.${marketplace}/dp/${asin}`;

    if (title) {
      results.push({
        asin,
        title: title.replace(/<[^>]+>/g, '').trim(),
        price,
        rating,
        reviewCount,
        image,
        url: productUrl,
      });
    }
  }

  return results;
}
