/**
 * Domain enrichment logic for company-data-api
 */

const TECHNOLOGY_SIGNATURES = [
  { name: 'Google Analytics', patterns: ['google-analytics.com/analytics.js', 'googletagmanager.com/gtag', 'ga.js', 'gtag('] },
  { name: 'Google Tag Manager', patterns: ['googletagmanager.com/gtm.js'] },
  { name: 'Facebook Pixel', patterns: ['connect.facebook.net', 'fbq('] },
  { name: 'Shopify', patterns: ['cdn.shopify.com', 'Shopify.theme'] },
  { name: 'WordPress', patterns: ['wp-content/', 'wp-includes/', 'wp-json'] },
  { name: 'React', patterns: ['react.production.min.js', 'reactDOM', '__NEXT_DATA__', '_next/'] },
  { name: 'Next.js', patterns: ['__NEXT_DATA__', '_next/static'] },
  { name: 'Vue.js', patterns: ['vue.min.js', 'vue.runtime', '__vue__'] },
  { name: 'Nuxt.js', patterns: ['__NUXT__', '_nuxt/'] },
  { name: 'Angular', patterns: ['ng-version', 'angular.min.js'] },
  { name: 'jQuery', patterns: ['jquery.min.js', 'jquery-'] },
  { name: 'Bootstrap', patterns: ['bootstrap.min.css', 'bootstrap.min.js'] },
  { name: 'Tailwind CSS', patterns: ['tailwindcss', 'tailwind.min.css'] },
  { name: 'Cloudflare', patterns: ['cdnjs.cloudflare.com', 'cdn-cgi/'] },
  { name: 'Stripe', patterns: ['js.stripe.com', 'stripe.js'] },
  { name: 'Intercom', patterns: ['widget.intercom.io', 'intercomSettings'] },
  { name: 'Drift', patterns: ['js.driftt.com', 'drift.com'] },
  { name: 'HubSpot', patterns: ['js.hs-scripts.com', 'hs-analytics'] },
  { name: 'Segment', patterns: ['cdn.segment.com', 'analytics.js'] },
  { name: 'Hotjar', patterns: ['static.hotjar.com', 'hotjar'] },
  { name: 'Zendesk', patterns: ['static.zdassets.com', 'zopim'] },
  { name: 'Wix', patterns: ['static.wixstatic.com', 'wix.com'] },
  { name: 'Squarespace', patterns: ['static1.squarespace.com', 'squarespace'] },
  { name: 'Webflow', patterns: ['assets.website-files.com', 'webflow'] },
  { name: 'Vercel', patterns: ['vercel.app', 'vercel-analytics'] },
  { name: 'Gatsby', patterns: ['gatsby-'] },
  { name: 'Svelte', patterns: ['svelte'] },
];

const SOCIAL_PATTERNS = [
  { platform: 'linkedin', regex: /https?:\/\/(www\.)?linkedin\.com\/(?:company|in)\/[^\s"'<>]+/gi },
  { platform: 'twitter', regex: /https?:\/\/(www\.)?(twitter\.com|x\.com)\/[^\s"'<>]+/gi },
  { platform: 'facebook', regex: /https?:\/\/(www\.)?facebook\.com\/[^\s"'<>]+/gi },
  { platform: 'github', regex: /https?:\/\/(www\.)?github\.com\/[^\s"'<>]+/gi },
  { platform: 'instagram', regex: /https?:\/\/(www\.)?instagram\.com\/[^\s"'<>]+/gi },
  { platform: 'youtube', regex: /https?:\/\/(www\.)?youtube\.com\/(channel|c|@)\/[^\s"'<>]+/gi },
];

const EMAIL_REGEX = /[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}/g;
const PHONE_REGEX = /(?:\+?1[-.\s]?)?(?:\(?\d{3}\)?[-.\s]?)?\d{3}[-.\s]?\d{4}/g;

function extractMetaTag(html, name) {
  const patterns = [
    new RegExp(`<meta[^>]+(?:name|property)=["']${name}["'][^>]+content=["']([^"']*)["']`, 'i'),
    new RegExp(`<meta[^>]+content=["']([^"']*)["'][^>]+(?:name|property)=["']${name}["']`, 'i'),
  ];
  for (const p of patterns) {
    const m = html.match(p);
    if (m) return m[1];
  }
  return null;
}

function extractTitle(html) {
  const m = html.match(/<title[^>]*>([^<]*)<\/title>/i);
  return m ? m[1].trim() : null;
}

export async function fetchWebsiteMetadata(url) {
  const response = await fetch(url, {
    headers: { 'User-Agent': 'CompanyDataAPI/1.0' },
    redirect: 'follow',
  });

  if (!response.ok) {
    throw new Error(`Failed to fetch ${url}: ${response.status}`);
  }

  const html = await response.text();
  const title = extractTitle(html);
  const description = extractMetaTag(html, 'description');
  const ogTitle = extractMetaTag(html, 'og:title');
  const ogDescription = extractMetaTag(html, 'og:description');
  const ogImage = extractMetaTag(html, 'og:image');
  const ogType = extractMetaTag(html, 'og:type');
  const ogSiteName = extractMetaTag(html, 'og:site_name');

  // Extract social links
  const socialLinks = {};
  for (const { platform, regex } of SOCIAL_PATTERNS) {
    const matches = html.match(regex);
    if (matches) {
      const unique = [...new Set(matches)];
      socialLinks[platform] = unique.length === 1 ? unique[0] : unique;
    }
  }

  // Extract emails (exclude common false positives)
  const emailMatches = html.match(EMAIL_REGEX) || [];
  const emails = [...new Set(emailMatches)].filter(
    (e) => !e.endsWith('.png') && !e.endsWith('.jpg') && !e.endsWith('.svg')
  );

  // Extract phone numbers
  const phoneMatches = html.match(PHONE_REGEX) || [];
  const phones = [...new Set(phoneMatches)].slice(0, 5);

  return {
    title,
    description,
    ogTags: { title: ogTitle, description: ogDescription, image: ogImage, type: ogType, siteName: ogSiteName },
    socialLinks: Object.keys(socialLinks).length > 0 ? socialLinks : null,
    emails: emails.length > 0 ? emails : null,
    phones: phones.length > 0 ? phones : null,
    html,
  };
}

export function detectTechnologies(html) {
  const detected = [];
  const lowerHtml = html.toLowerCase();
  for (const tech of TECHNOLOGY_SIGNATURES) {
    for (const pattern of tech.patterns) {
      if (lowerHtml.includes(pattern.toLowerCase())) {
        detected.push(tech.name);
        break;
      }
    }
  }
  return detected;
}

export async function rdapLookup(domain) {
  try {
    // Use RDAP bootstrap to find the right server
    const bootstrapRes = await fetch('https://data.iana.org/rdap/dns.json');
    if (!bootstrapRes.ok) throw new Error('RDAP bootstrap failed');
    const bootstrap = await bootstrapRes.json();

    const tld = domain.split('.').pop().toLowerCase();
    let rdapServer = null;

    for (const entry of bootstrap.services) {
      const tlds = entry[0];
      const urls = entry[1];
      if (tlds.includes(tld)) {
        rdapServer = urls[0];
        break;
      }
    }

    if (!rdapServer) {
      return { error: 'No RDAP server found for this TLD' };
    }

    const rdapUrl = `${rdapServer.replace(/\/$/, '')}/domain/${domain}`;
    const res = await fetch(rdapUrl, {
      headers: { Accept: 'application/rdap+json' },
    });

    if (!res.ok) {
      return { error: `RDAP lookup failed: ${res.status}` };
    }

    const data = await res.json();

    // Extract useful fields
    const registrar = data.entities?.find((e) => e.roles?.includes('registrar'));
    const registrarName = registrar?.vcardArray?.[1]?.find((v) => v[0] === 'fn')?.[3] || null;

    const events = data.events || [];
    const registration = events.find((e) => e.eventAction === 'registration');
    const expiration = events.find((e) => e.eventAction === 'expiration');
    const lastChanged = events.find((e) => e.eventAction === 'last changed');

    return {
      domain: data.ldhName || domain,
      status: data.status || null,
      registrar: registrarName,
      registrationDate: registration?.eventDate || null,
      expirationDate: expiration?.eventDate || null,
      lastChanged: lastChanged?.eventDate || null,
      nameservers: data.nameservers?.map((ns) => ns.ldhName) || null,
    };
  } catch (err) {
    return { error: err.message };
  }
}
