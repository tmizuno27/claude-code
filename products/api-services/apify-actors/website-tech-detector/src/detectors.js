/**
 * Technology detection signatures — 80+ technologies across 17 categories.
 * Each entry defines HTML patterns, header patterns, and/or meta patterns.
 */

export const TECHNOLOGY_SIGNATURES = [
  // ── Frameworks ──
  { name: 'React', category: 'framework', patterns: { html: ['react.production.min.js', 'react-dom', '__NEXT_DATA__', '_next/', 'data-reactroot', 'data-reactid'] } },
  { name: 'Next.js', category: 'framework', patterns: { html: ['__NEXT_DATA__', '_next/static', 'next/dist'], headers: ['x-nextjs-cache', 'x-nextjs-matched-path'] } },
  { name: 'Vue.js', category: 'framework', patterns: { html: ['vue.min.js', 'vue.runtime', '__vue__', 'data-v-', 'vue.global'] } },
  { name: 'Nuxt.js', category: 'framework', patterns: { html: ['__NUXT__', '_nuxt/', 'nuxt.config'] } },
  { name: 'Angular', category: 'framework', patterns: { html: ['ng-version', 'angular.min.js', 'ng-app', 'ng-controller', 'angular.io'] } },
  { name: 'Svelte', category: 'framework', patterns: { html: ['svelte', '__svelte'] } },
  { name: 'SvelteKit', category: 'framework', patterns: { html: ['__sveltekit', 'sveltekit'] } },
  { name: 'Remix', category: 'framework', patterns: { html: ['__remixContext', 'remix.run'] } },
  { name: 'Astro', category: 'framework', patterns: { html: ['astro-island', 'astro-slot'], headers: ['x-astro'] } },
  { name: 'Gatsby', category: 'framework', patterns: { html: ['gatsby-', '/static/d/'] } },
  { name: 'Ember.js', category: 'framework', patterns: { html: ['ember.min.js', 'ember-cli', 'data-ember'] } },
  { name: 'Ruby on Rails', category: 'framework', patterns: { html: ['csrf-token', 'data-turbo', 'turbolinks'], headers: ['x-powered-by: phusion passenger'] } },
  { name: 'Django', category: 'framework', patterns: { html: ['csrfmiddlewaretoken', 'django'], headers: ['x-frame-options: deny'] } },
  { name: 'Laravel', category: 'framework', patterns: { html: ['laravel', 'csrf-token'], headers: ['x-powered-by: laravel'] } },
  { name: 'Express', category: 'framework', patterns: { headers: ['x-powered-by: express'] } },
  { name: 'FastAPI', category: 'framework', patterns: { headers: ['x-process-time'] } },

  // ── CMS ──
  { name: 'WordPress', category: 'cms', patterns: { html: ['wp-content/', 'wp-includes/', 'wp-json', '/xmlrpc.php'] } },
  { name: 'Shopify', category: 'cms', patterns: { html: ['cdn.shopify.com', 'Shopify.theme', 'shopify-section'] } },
  { name: 'Wix', category: 'cms', patterns: { html: ['static.wixstatic.com', 'wix.com', '_wixCIDX'] } },
  { name: 'Squarespace', category: 'cms', patterns: { html: ['static1.squarespace.com', 'squarespace-cdn'] } },
  { name: 'Webflow', category: 'cms', patterns: { html: ['assets.website-files.com', 'webflow', 'w-nav'] } },
  { name: 'Ghost', category: 'cms', patterns: { html: ['ghost.org', 'ghost-', 'content/themes'] } },
  { name: 'Drupal', category: 'cms', patterns: { html: ['drupal.js', 'Drupal.settings', '/sites/default/files'] } },
  { name: 'Joomla', category: 'cms', patterns: { html: ['/media/jui/', 'joomla', '/administrator/'] } },
  { name: 'HubSpot CMS', category: 'cms', patterns: { html: ['hs-sites.com', 'hubspot-content'] } },
  { name: 'Contentful', category: 'cms', patterns: { html: ['contentful.com', 'images.ctfassets.net'] } },
  { name: 'Sanity', category: 'cms', patterns: { html: ['sanity.io', 'cdn.sanity.io'] } },
  { name: 'Strapi', category: 'cms', patterns: { html: ['strapi'] } },

  // ── JavaScript Libraries ──
  { name: 'jQuery', category: 'javascript-library', patterns: { html: ['jquery.min.js', 'jquery-', 'jquery/'] } },
  { name: 'Lodash', category: 'javascript-library', patterns: { html: ['lodash.min.js', 'lodash.js'] } },
  { name: 'Axios', category: 'javascript-library', patterns: { html: ['axios.min.js', 'axios/'] } },
  { name: 'Moment.js', category: 'javascript-library', patterns: { html: ['moment.min.js', 'moment-with-locales'] } },
  { name: 'GSAP', category: 'javascript-library', patterns: { html: ['gsap.min.js', 'greensock', 'TweenMax'] } },
  { name: 'Three.js', category: 'javascript-library', patterns: { html: ['three.min.js', 'three.module.js'] } },
  { name: 'Alpine.js', category: 'javascript-library', patterns: { html: ['alpine.min.js', 'x-data', 'x-init'] } },
  { name: 'HTMX', category: 'javascript-library', patterns: { html: ['htmx.min.js', 'htmx.org', 'hx-get', 'hx-post'] } },

  // ── CSS Frameworks ──
  { name: 'Bootstrap', category: 'css-framework', patterns: { html: ['bootstrap.min.css', 'bootstrap.min.js', 'bootstrap/'] } },
  { name: 'Tailwind CSS', category: 'css-framework', patterns: { html: ['tailwindcss', 'tailwind.min.css'] } },
  { name: 'Bulma', category: 'css-framework', patterns: { html: ['bulma.min.css', 'bulma/'] } },
  { name: 'Material UI', category: 'css-framework', patterns: { html: ['MuiButton', 'mui/', '@mui/material'] } },
  { name: 'Chakra UI', category: 'css-framework', patterns: { html: ['chakra-ui', 'css-'] } },
  { name: 'Foundation', category: 'css-framework', patterns: { html: ['foundation.min.css', 'foundation.min.js'] } },

  // ── Analytics ──
  { name: 'Google Analytics', category: 'analytics', patterns: { html: ['google-analytics.com/analytics.js', 'googletagmanager.com/gtag', 'ga.js', "gtag('config"] } },
  { name: 'Google Analytics 4', category: 'analytics', patterns: { html: ['gtag/js?id=G-', 'measurement_id'] } },
  { name: 'Hotjar', category: 'analytics', patterns: { html: ['static.hotjar.com', 'hotjar', 'hj('] } },
  { name: 'Segment', category: 'analytics', patterns: { html: ['cdn.segment.com', 'analytics.js', 'analytics.identify'] } },
  { name: 'Mixpanel', category: 'analytics', patterns: { html: ['mixpanel.com', 'mixpanel.init'] } },
  { name: 'Amplitude', category: 'analytics', patterns: { html: ['cdn.amplitude.com', 'amplitude.getInstance'] } },
  { name: 'Heap', category: 'analytics', patterns: { html: ['heap-', 'heapanalytics.com'] } },
  { name: 'Plausible', category: 'analytics', patterns: { html: ['plausible.io/js'] } },
  { name: 'Fathom', category: 'analytics', patterns: { html: ['cdn.usefathom.com', 'fathom'] } },
  { name: 'PostHog', category: 'analytics', patterns: { html: ['posthog.com', 'posthog.init'] } },
  { name: 'Clarity', category: 'analytics', patterns: { html: ['clarity.ms/tag'] } },
  { name: 'Matomo', category: 'analytics', patterns: { html: ['matomo.js', 'piwik.js'] } },

  // ── Tag Managers ──
  { name: 'Google Tag Manager', category: 'tag-manager', patterns: { html: ['googletagmanager.com/gtm.js', 'GTM-'] } },
  { name: 'Adobe Launch', category: 'tag-manager', patterns: { html: ['assets.adobedtm.com', 'launch-'] } },

  // ── CDN / Hosting ──
  { name: 'Cloudflare', category: 'cdn', patterns: { html: ['cdnjs.cloudflare.com', 'cdn-cgi/'], headers: ['cf-ray', 'cf-cache-status', 'server: cloudflare'] } },
  { name: 'Fastly', category: 'cdn', patterns: { headers: ['x-served-by', 'via: 1.1 varnish', 'x-fastly'] } },
  { name: 'AWS CloudFront', category: 'cdn', patterns: { headers: ['x-amz-cf-id', 'x-amz-cf-pop', 'via: cloudfront'] } },
  { name: 'Akamai', category: 'cdn', patterns: { headers: ['x-akamai-transformed', 'server: akamaighost'] } },
  { name: 'Vercel', category: 'hosting', patterns: { html: ['vercel.app', 'vercel-analytics'], headers: ['x-vercel-id', 'server: vercel'] } },
  { name: 'Netlify', category: 'hosting', patterns: { headers: ['x-nf-request-id', 'server: netlify'] } },
  { name: 'Heroku', category: 'hosting', patterns: { headers: ['via: 1.1 vegur'] } },
  { name: 'Firebase', category: 'hosting', patterns: { html: ['firebaseapp.com', 'firebase.js', 'firebase-app.js'] } },
  { name: 'GitHub Pages', category: 'hosting', patterns: { headers: ['server: github.com'] } },

  // ── Payment ──
  { name: 'Stripe', category: 'payment', patterns: { html: ['js.stripe.com', 'stripe.js', 'Stripe('] } },
  { name: 'PayPal', category: 'payment', patterns: { html: ['paypal.com/sdk', 'paypalobjects.com'] } },
  { name: 'Paddle', category: 'payment', patterns: { html: ['paddle.com', 'Paddle.Setup'] } },
  { name: 'LemonSqueezy', category: 'payment', patterns: { html: ['lemonsqueezy.com', 'lemon-squeezy'] } },

  // ── Marketing / CRM ──
  { name: 'HubSpot', category: 'marketing', patterns: { html: ['js.hs-scripts.com', 'hs-analytics', 'hbspt.forms'] } },
  { name: 'Intercom', category: 'marketing', patterns: { html: ['widget.intercom.io', 'intercomSettings'] } },
  { name: 'Drift', category: 'marketing', patterns: { html: ['js.driftt.com', 'drift.com'] } },
  { name: 'Mailchimp', category: 'marketing', patterns: { html: ['chimpstatic.com', 'list-manage.com', 'mc.us'] } },
  { name: 'ConvertKit', category: 'marketing', patterns: { html: ['convertkit.com', 'ck.page'] } },
  { name: 'ActiveCampaign', category: 'marketing', patterns: { html: ['trackcmp.net', 'activehosted.com'] } },

  // ── Chat / Support ──
  { name: 'Zendesk', category: 'chat', patterns: { html: ['static.zdassets.com', 'zopim', 'zendesk'] } },
  { name: 'Crisp', category: 'chat', patterns: { html: ['client.crisp.chat', 'crisp.im'] } },
  { name: 'Tawk.to', category: 'chat', patterns: { html: ['embed.tawk.to'] } },
  { name: 'LiveChat', category: 'chat', patterns: { html: ['cdn.livechatinc.com'] } },
  { name: 'Freshdesk', category: 'chat', patterns: { html: ['freshdesk.com', 'freshchat.com'] } },

  // ── Advertising ──
  { name: 'Facebook Pixel', category: 'advertising', patterns: { html: ['connect.facebook.net', 'fbq(', 'facebook-jssdk'] } },
  { name: 'Google Ads', category: 'advertising', patterns: { html: ['googleads.g.doubleclick.net', 'pagead2.googlesyndication.com', 'adsbygoogle'] } },
  { name: 'Google AdSense', category: 'advertising', patterns: { html: ['pagead2.googlesyndication.com/pagead/js/adsbygoogle.js', 'adsbygoogle'] } },
  { name: 'Twitter Pixel', category: 'advertising', patterns: { html: ['static.ads-twitter.com', 'twq('] } },
  { name: 'LinkedIn Insight Tag', category: 'advertising', patterns: { html: ['snap.licdn.com', '_linkedin_partner_id'] } },
  { name: 'TikTok Pixel', category: 'advertising', patterns: { html: ['analytics.tiktok.com', 'ttq.load'] } },
  { name: 'Pinterest Tag', category: 'advertising', patterns: { html: ['pintrk', 's.pinimg.com/ct/core.js'] } },

  // ── Fonts ──
  { name: 'Google Fonts', category: 'font', patterns: { html: ['fonts.googleapis.com', 'fonts.gstatic.com'] } },
  { name: 'Adobe Fonts (Typekit)', category: 'font', patterns: { html: ['use.typekit.net', 'p.typekit.net'] } },
  { name: 'Font Awesome', category: 'font', patterns: { html: ['fontawesome', 'font-awesome', 'fa-'] } },

  // ── Video ──
  { name: 'YouTube Embed', category: 'video', patterns: { html: ['youtube.com/embed', 'youtube-nocookie.com'] } },
  { name: 'Vimeo', category: 'video', patterns: { html: ['player.vimeo.com', 'vimeo.com'] } },
  { name: 'Wistia', category: 'video', patterns: { html: ['fast.wistia.com', 'wistia-'] } },

  // ── Security ──
  { name: 'reCAPTCHA', category: 'security', patterns: { html: ['google.com/recaptcha', 'g-recaptcha'] } },
  { name: 'hCaptcha', category: 'security', patterns: { html: ['hcaptcha.com', 'h-captcha'] } },
  { name: 'Cloudflare Turnstile', category: 'security', patterns: { html: ['challenges.cloudflare.com/turnstile'] } },

  // ── Server ──
  { name: 'Nginx', category: 'server', patterns: { headers: ['server: nginx'] } },
  { name: 'Apache', category: 'server', patterns: { headers: ['server: apache'] } },
  { name: 'LiteSpeed', category: 'server', patterns: { headers: ['server: litespeed'] } },
  { name: 'IIS', category: 'server', patterns: { headers: ['server: microsoft-iis'] } },
];

const FETCH_TIMEOUT_MS = 30_000;
const MAX_RETRIES = 2;
const RETRY_DELAY_MS = 2_000;

async function fetchWithRetry(url, options = {}, timeoutMs = FETCH_TIMEOUT_MS) {
  let lastError;
  for (let attempt = 0; attempt <= MAX_RETRIES; attempt++) {
    const controller = new AbortController();
    const timer = setTimeout(() => controller.abort(), timeoutMs);
    try {
      const res = await fetch(url, { ...options, signal: controller.signal });
      clearTimeout(timer);
      return res;
    } catch (e) {
      clearTimeout(timer);
      lastError = e;
      if (attempt < MAX_RETRIES) {
        await new Promise((r) => setTimeout(r, RETRY_DELAY_MS));
      }
    }
  }
  throw lastError;
}

/**
 * Fetch a URL and return html + response headers.
 */
export async function fetchSite(url) {
  const res = await fetchWithRetry(url, {
    headers: {
      'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
      'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
      'Accept-Language': 'en-US,en;q=0.9',
    },
    redirect: 'follow',
  });

  if (!res.ok) throw new Error(`HTTP ${res.status}`);

  const html = await res.text();

  // Normalize headers to lowercase key-value pairs
  const headers = {};
  for (const [key, value] of res.headers.entries()) {
    headers[key.toLowerCase()] = value.toLowerCase();
  }

  return { html, headers, finalUrl: res.url };
}

/**
 * Detect technologies from HTML content and HTTP headers.
 * Returns array of { name, category, confidence }.
 */
export function detectTechnologies(html, headers, categoryFilter = []) {
  const lowerHtml = html.toLowerCase();
  const detected = [];
  const filterSet = categoryFilter.length > 0 ? new Set(categoryFilter) : null;

  for (const tech of TECHNOLOGY_SIGNATURES) {
    if (filterSet && !filterSet.has(tech.category)) continue;

    let matched = false;
    let matchedPatterns = 0;
    let totalPatterns = 0;

    // Check HTML patterns
    const htmlPatterns = tech.patterns.html || [];
    totalPatterns += htmlPatterns.length;
    for (const pattern of htmlPatterns) {
      if (lowerHtml.includes(pattern.toLowerCase())) {
        matched = true;
        matchedPatterns++;
      }
    }

    // Check header patterns
    const headerPatterns = tech.patterns.headers || [];
    totalPatterns += headerPatterns.length;
    for (const pattern of headerPatterns) {
      const [headerKey, ...valueParts] = pattern.split(': ');
      const expectedValue = valueParts.join(': ').toLowerCase();
      const headerValue = headers[headerKey.toLowerCase()] || '';

      if (expectedValue) {
        if (headerValue.includes(expectedValue)) {
          matched = true;
          matchedPatterns++;
        }
      } else {
        if (headerValue) {
          matched = true;
          matchedPatterns++;
        }
      }
    }

    if (matched) {
      // Confidence: how many patterns matched out of total
      const confidence = totalPatterns > 0
        ? Math.round((matchedPatterns / totalPatterns) * 100)
        : 100;

      detected.push({
        name: tech.name,
        category: tech.category,
        confidence: Math.max(confidence, 50), // minimum 50% if at least one pattern matched
      });
    }
  }

  // Sort by confidence desc, then name
  return detected.sort((a, b) => b.confidence - a.confidence || a.name.localeCompare(b.name));
}

/**
 * Extract basic page metadata from HTML.
 */
export function extractMetadata(html) {
  const titleMatch = html.match(/<title[^>]*>([\s\S]*?)<\/title>/i);
  const title = titleMatch ? titleMatch[1].trim() : null;

  const descMatch =
    html.match(/<meta[^>]+name\s*=\s*["']description["'][^>]+content\s*=\s*["']([\s\S]*?)["'][^>]*>/i) ||
    html.match(/<meta[^>]+content\s*=\s*["']([\s\S]*?)["'][^>]+name\s*=\s*["']description["'][^>]*>/i);
  const description = descMatch ? descMatch[1].trim() : null;

  const faviconMatch =
    html.match(/<link[^>]+rel\s*=\s*["'](?:shortcut )?icon["'][^>]+href\s*=\s*["']([\s\S]*?)["'][^>]*>/i) ||
    html.match(/<link[^>]+href\s*=\s*["']([\s\S]*?)["'][^>]+rel\s*=\s*["'](?:shortcut )?icon["'][^>]*>/i);
  const favicon = faviconMatch ? faviconMatch[1].trim() : null;

  const ogImageMatch =
    html.match(/<meta[^>]+property\s*=\s*["']og:image["'][^>]+content\s*=\s*["']([\s\S]*?)["'][^>]*>/i) ||
    html.match(/<meta[^>]+content\s*=\s*["']([\s\S]*?)["'][^>]+property\s*=\s*["']og:image["'][^>]*>/i);
  const ogImage = ogImageMatch ? ogImageMatch[1].trim() : null;

  return { title, description, favicon, ogImage };
}

/**
 * Extract security headers from response.
 */
export function extractSecurityHeaders(headers) {
  const securityHeaders = [
    'strict-transport-security',
    'content-security-policy',
    'x-content-type-options',
    'x-frame-options',
    'x-xss-protection',
    'referrer-policy',
    'permissions-policy',
  ];

  const result = {};
  for (const h of securityHeaders) {
    result[h] = headers[h] || null;
  }
  return result;
}
