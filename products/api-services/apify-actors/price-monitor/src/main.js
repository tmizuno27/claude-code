import { Actor, log } from 'apify';
import { parse } from 'node-html-parser';

const FETCH_TIMEOUT_MS = 30_000;
const MAX_RETRIES = 2;
const RETRY_DELAY_MS = 3_000;
const DEFAULT_DELAY_MS = 2000;

await Actor.init();

// --- Input validation ---
const input = await Actor.getInput();
if (!input?.products || !Array.isArray(input.products) || input.products.length === 0) {
  throw new Error('Input must contain a non-empty "products" array. Each product needs at least a "url" field.');
}

const {
  products,
  currency = '$',
  extractReviews = true,
  checkAvailability = true,
  delayMs = DEFAULT_DELAY_MS,
} = input;

const dataset = await Actor.openDataset();

// --- HTTP helper with retry ---
async function fetchWithRetry(url) {
  let lastError;
  for (let attempt = 0; attempt <= MAX_RETRIES; attempt++) {
    try {
      const controller = new AbortController();
      const timer = setTimeout(() => controller.abort(), FETCH_TIMEOUT_MS);
      try {
        const res = await fetch(url, {
          headers: {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.9',
          },
          signal: controller.signal,
          redirect: 'follow',
        });
        clearTimeout(timer);
        if (!res.ok) throw new Error(`HTTP ${res.status} ${res.statusText}`);
        return { html: await res.text(), finalUrl: res.url };
      } finally {
        clearTimeout(timer);
      }
    } catch (e) {
      lastError = e;
      if (attempt < MAX_RETRIES) {
        log.warning(`Attempt ${attempt + 1} failed for ${url}: ${e.message}. Retrying in ${RETRY_DELAY_MS}ms...`);
        await new Promise((r) => setTimeout(r, RETRY_DELAY_MS));
      }
    }
  }
  throw lastError;
}

// --- Price extraction ---
function extractPrice(html, currencySymbol) {
  const root = parse(html);

  // JSON-LD structured data (most reliable)
  const jsonLdScripts = root.querySelectorAll('script[type="application/ld+json"]');
  for (const script of jsonLdScripts) {
    try {
      const data = JSON.parse(script.text);
      const items = Array.isArray(data) ? data : [data];
      for (const item of items) {
        if (item.offers) {
          const offer = Array.isArray(item.offers) ? item.offers[0] : item.offers;
          if (offer?.price) {
            return {
              price: parseFloat(String(offer.price).replace(/,/g, '')),
              currency: offer.priceCurrency || currencySymbol,
              source: 'json-ld',
            };
          }
        }
        if (item['@type'] === 'Product' && item.offers?.price) {
          return {
            price: parseFloat(String(item.offers.price).replace(/,/g, '')),
            currency: item.offers.priceCurrency || currencySymbol,
            source: 'json-ld',
          };
        }
      }
    } catch (_) { /* skip invalid JSON */ }
  }

  // Meta tags (Open Graph price)
  const ogPrice = root.querySelector('meta[property="product:price:amount"]');
  if (ogPrice) {
    const priceVal = parseFloat(ogPrice.getAttribute('content')?.replace(/,/g, '') || '');
    if (!isNaN(priceVal)) {
      const ogCurrency = root.querySelector('meta[property="product:price:currency"]');
      return { price: priceVal, currency: ogCurrency?.getAttribute('content') || currencySymbol, source: 'og-meta' };
    }
  }

  // Amazon-specific selectors
  const amazonSelectors = [
    'span.a-price-whole',
    '#priceblock_ourprice',
    '#priceblock_dealprice',
    'span.a-offscreen',
    '.a-price .a-offscreen',
  ];
  for (const sel of amazonSelectors) {
    const el = root.querySelector(sel);
    if (el) {
      const text = el.text.replace(/[^\d.,]/g, '').replace(/,/g, '');
      const val = parseFloat(text);
      if (!isNaN(val) && val > 0) {
        return { price: val, currency: currencySymbol, source: 'amazon-selector' };
      }
    }
  }

  // Generic price pattern fallback (looks for currency symbol + number)
  const escapedCurrency = currencySymbol.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
  const priceRegex = new RegExp(`${escapedCurrency}\\s*([\\d,]+\\.?\\d{0,2})`, 'i');
  const match = html.match(priceRegex);
  if (match) {
    const val = parseFloat(match[1].replace(/,/g, ''));
    if (!isNaN(val) && val > 0) {
      return { price: val, currency: currencySymbol, source: 'regex' };
    }
  }

  return { price: null, currency: null, source: null };
}

// --- Review extraction ---
function extractReviewData(html) {
  const root = parse(html);

  // JSON-LD structured data
  const jsonLdScripts = root.querySelectorAll('script[type="application/ld+json"]');
  for (const script of jsonLdScripts) {
    try {
      const data = JSON.parse(script.text);
      const items = Array.isArray(data) ? data : [data];
      for (const item of items) {
        if (item.aggregateRating) {
          return {
            rating: parseFloat(item.aggregateRating.ratingValue) || null,
            reviewCount: parseInt(item.aggregateRating.reviewCount || item.aggregateRating.ratingCount, 10) || null,
          };
        }
      }
    } catch (_) { /* skip */ }
  }

  // Amazon-specific
  const amazonRating = root.querySelector('#acrPopover span.a-icon-alt, .a-icon-star .a-icon-alt');
  const amazonCount = root.querySelector('#acrCustomerReviewText');
  if (amazonRating) {
    const ratingText = amazonRating.text.match(/[\d.]+/);
    const countText = amazonCount?.text.match(/[\d,]+/);
    return {
      rating: ratingText ? parseFloat(ratingText[0]) : null,
      reviewCount: countText ? parseInt(countText[0].replace(/,/g, ''), 10) : null,
    };
  }

  return { rating: null, reviewCount: null };
}

// --- Availability detection ---
function detectAvailability(html) {
  const lowerHtml = html.toLowerCase();
  const outOfStockSignals = [
    'out of stock',
    'currently unavailable',
    'sold out',
    'not available',
    '在庫切れ',
    '品切れ',
    'no disponible',
    'rupture de stock',
    '"availability":"OutOfStock"',
    '"ItemAvailability": "OutOfStock"',
  ];
  const inStockSignals = [
    'add to cart',
    'add to basket',
    'buy now',
    '"availability":"InStock"',
    '"ItemAvailability": "InStock"',
    'カートに入れる',
  ];

  if (outOfStockSignals.some((s) => lowerHtml.includes(s))) return 'out_of_stock';
  if (inStockSignals.some((s) => lowerHtml.includes(s))) return 'in_stock';
  return 'unknown';
}

// --- Extract product title ---
function extractTitle(html) {
  const root = parse(html);

  // JSON-LD
  const jsonLd = root.querySelector('script[type="application/ld+json"]');
  if (jsonLd) {
    try {
      const data = JSON.parse(jsonLd.text);
      if (data.name) return data.name;
    } catch (_) { /* skip */ }
  }

  // OG title
  const og = root.querySelector('meta[property="og:title"]');
  if (og) return og.getAttribute('content')?.trim() || null;

  // Page title
  const title = root.querySelector('title');
  return title?.text?.trim() || null;
}

// --- Main processing loop ---
log.info(`Starting Price Monitor — ${products.length} product(s)`);

for (let i = 0; i < products.length; i++) {
  const product = products[i];
  const productUrl = product.url?.trim();

  if (!productUrl) {
    log.warning(`Skipping product at index ${i}: missing url`);
    continue;
  }

  const productName = product.name || null;
  const targetPrice = product.targetPrice ? parseFloat(product.targetPrice) : null;

  log.info(`[${i + 1}/${products.length}] Checking: ${productName || productUrl}`);

  let success = false;
  let errorMessage = null;
  let priceData = { price: null, currency: null, source: null };
  let reviewData = { rating: null, reviewCount: null };
  let availability = 'unknown';
  let pageTitle = null;
  let priceAlert = false;
  let finalUrl = productUrl;

  try {
    const { html, finalUrl: resolvedUrl } = await fetchWithRetry(productUrl);
    finalUrl = resolvedUrl;

    pageTitle = extractTitle(html);
    priceData = extractPrice(html, currency);
    if (extractReviews) reviewData = extractReviewData(html);
    if (checkAvailability) availability = detectAvailability(html);

    // Alert if price dropped below target
    if (targetPrice !== null && priceData.price !== null && priceData.price <= targetPrice) {
      priceAlert = true;
      log.info(`  PRICE ALERT: ${priceData.currency}${priceData.price} is at or below target ${priceData.currency}${targetPrice}`);
    }

    success = true;
    log.info(`  Price: ${priceData.currency ?? currency}${priceData.price ?? 'N/A'} | Stock: ${availability}`);
  } catch (e) {
    errorMessage = e.message;
    log.error(`  Failed to fetch "${productUrl}": ${e.message}`);
  }

  await dataset.pushData({
    url: productUrl,
    finalUrl,
    name: productName || pageTitle,
    pageTitle,
    success,
    error: errorMessage,
    timestamp: new Date().toISOString(),
    price: priceData.price,
    currency: priceData.currency ?? currency,
    priceSource: priceData.source,
    targetPrice,
    priceAlert,
    availability,
    rating: reviewData.rating,
    reviewCount: reviewData.reviewCount,
  });

  if (i < products.length - 1) {
    await new Promise((r) => setTimeout(r, Math.max(1000, Number(delayMs) || DEFAULT_DELAY_MS)));
  }
}

log.info(`Price Monitor complete. ${products.length} product(s) checked.`);
await Actor.exit();
