/**
 * Extract email addresses from HTML content.
 * Filters out common false positives (image files, CSS classes, etc.)
 */
export function extractEmails(html) {
  const emailRegex = /[a-zA-Z0-9._%+\-]+@[a-zA-Z0-9.\-]+\.[a-zA-Z]{2,}/g;
  const matches = html.match(emailRegex) || [];

  const BLACKLIST_DOMAINS = [
    'example.com', 'sentry.io', 'wixpress.com', 'w3.org',
    'schema.org', 'purl.org', 'xmlns.com', 'google.com',
    'wordpress.org', 'gravatar.com',
  ];

  const BLACKLIST_EXTENSIONS = ['.png', '.jpg', '.jpeg', '.gif', '.svg', '.webp', '.css', '.js'];

  const filtered = new Set();
  for (const email of matches) {
    const lower = email.toLowerCase();
    const domain = lower.split('@')[1];

    if (BLACKLIST_DOMAINS.some((d) => domain === d || domain.endsWith('.' + d))) continue;
    if (BLACKLIST_EXTENSIONS.some((ext) => lower.endsWith(ext))) continue;
    if (lower.length > 100) continue;
    if (lower.startsWith('.') || lower.endsWith('.')) continue;

    filtered.add(lower);
  }

  return [...filtered];
}

/**
 * Extract phone numbers from HTML content.
 */
export function extractPhones(html) {
  // Remove HTML tags for cleaner extraction
  const text = html.replace(/<[^>]+>/g, ' ');

  const phonePatterns = [
    /\+?\d{1,3}[-.\s]?\(?\d{1,4}\)?[-.\s]?\d{1,4}[-.\s]?\d{1,9}/g,
    /tel:\s*([+\d\-().\s]{7,20})/gi,
    /href="tel:([^"]+)"/gi,
  ];

  const phones = new Set();

  for (const pattern of phonePatterns) {
    const matches = text.match(pattern) || [];
    for (const match of matches) {
      const cleaned = match
        .replace(/^tel:\s*/i, '')
        .replace(/^href="tel:/i, '')
        .replace(/"$/, '')
        .trim();

      // Must have at least 7 digits
      const digits = cleaned.replace(/\D/g, '');
      if (digits.length >= 7 && digits.length <= 15) {
        phones.add(cleaned);
      }
    }
  }

  return [...phones];
}

/**
 * Extract social media links from HTML.
 */
export function extractSocialLinks(html) {
  const social = {};

  const platforms = [
    { name: 'facebook', pattern: /href="(https?:\/\/(?:www\.)?facebook\.com\/[^"]+)"/gi },
    { name: 'twitter', pattern: /href="(https?:\/\/(?:www\.)?(?:twitter|x)\.com\/[^"]+)"/gi },
    { name: 'linkedin', pattern: /href="(https?:\/\/(?:www\.)?linkedin\.com\/[^"]+)"/gi },
    { name: 'instagram', pattern: /href="(https?:\/\/(?:www\.)?instagram\.com\/[^"]+)"/gi },
    { name: 'youtube', pattern: /href="(https?:\/\/(?:www\.)?youtube\.com\/[^"]+)"/gi },
    { name: 'tiktok', pattern: /href="(https?:\/\/(?:www\.)?tiktok\.com\/[^"]+)"/gi },
    { name: 'github', pattern: /href="(https?:\/\/(?:www\.)?github\.com\/[^"]+)"/gi },
  ];

  for (const { name, pattern } of platforms) {
    const match = pattern.exec(html);
    if (match) {
      social[name] = match[1];
    }
  }

  return social;
}

/**
 * Extract company information from structured data.
 */
export function extractCompanyInfo(html) {
  const info = {};

  // Try JSON-LD
  const ldRegex = /<script type="application\/ld\+json">([\s\S]*?)<\/script>/gi;
  let ldMatch;
  while ((ldMatch = ldRegex.exec(html)) !== null) {
    try {
      const data = JSON.parse(ldMatch[1]);
      const items = Array.isArray(data) ? data : [data];
      for (const item of items) {
        if (item['@type'] === 'Organization' || item['@type'] === 'LocalBusiness') {
          if (item.name) info.name = item.name;
          if (item.description) info.description = item.description;
          if (item.address) info.address = typeof item.address === 'string' ? item.address : item.address.streetAddress;
          if (item.telephone) info.phone = item.telephone;
          if (item.email) info.email = item.email;
          break;
        }
      }
    } catch {
      // ignore
    }
  }

  // Fallback: og:site_name
  if (!info.name) {
    const ogName = html.match(/<meta[^>]*property="og:site_name"[^>]*content="([^"]+)"/i);
    if (ogName) info.name = ogName[1];
  }

  return info;
}
