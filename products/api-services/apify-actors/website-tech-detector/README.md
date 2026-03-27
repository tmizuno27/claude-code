# Website Tech Stack Detector - Free BuiltWith & Wappalyzer Alternative

Detect 80+ technologies on any website in seconds -- frameworks, CMS, analytics, CDN, payments, marketing tools, and more. The best free alternative to BuiltWith ($295/mo), Wappalyzer ($250/mo), and SimilarTech. No API keys, no subscription required.

## Who Is This For?

- **Sales & SDR teams** -- Identify prospects using specific technologies (e.g., find all Shopify stores using Stripe) for targeted outreach
- **Competitive analysts** -- Benchmark competitor tech stacks to understand their infrastructure choices
- **Agencies & consultants** -- Audit client websites and recommend technology upgrades
- **Investors & VCs** -- Due diligence on portfolio companies' technology maturity
- **Developers** -- Discover what frameworks and tools successful sites are built with
- **Market researchers** -- Analyze technology adoption trends across industries at scale

## Technologies Detected (80+)

| Category | Technologies |
|----------|-------------|
| **Frameworks** | React, Next.js, Vue.js, Nuxt.js, Angular, Svelte, SvelteKit, Remix, Astro, Gatsby, Ember.js, Ruby on Rails, Django, Laravel, Express, FastAPI |
| **CMS** | WordPress, Shopify, Wix, Squarespace, Webflow, Ghost, Drupal, Joomla, HubSpot CMS, Contentful, Sanity, Strapi |
| **Analytics** | Google Analytics (UA & GA4), Hotjar, Segment, Mixpanel, Amplitude, Heap, Plausible, Fathom, PostHog, Clarity, Matomo |
| **CDN & Hosting** | Cloudflare, Fastly, AWS CloudFront, Akamai, Vercel, Netlify, Heroku, Firebase, GitHub Pages |
| **Payments** | Stripe, PayPal, Paddle, LemonSqueezy |
| **Marketing** | HubSpot, Intercom, Drift, Mailchimp, ConvertKit, ActiveCampaign |
| **Chat & Support** | Zendesk, Crisp, Tawk.to, LiveChat, Freshdesk |
| **Advertising** | Facebook Pixel, Google Ads, Google AdSense, Twitter Pixel, LinkedIn Insight Tag, TikTok Pixel, Pinterest Tag |
| **JavaScript Libraries** | jQuery, Lodash, Axios, Moment.js, GSAP, Three.js, Alpine.js, HTMX |
| **CSS Frameworks** | Bootstrap, Tailwind CSS, Bulma, Material UI, Chakra UI, Foundation |
| **Tag Managers** | Google Tag Manager, Adobe Launch |
| **Fonts** | Google Fonts, Adobe Fonts (Typekit), Font Awesome |
| **Video** | YouTube Embed, Vimeo, Wistia |
| **Security** | reCAPTCHA, hCaptcha, Cloudflare Turnstile |
| **Servers** | Nginx, Apache, LiteSpeed, IIS |

## Pricing -- Free to Start

| Tier | Cost | What You Get |
|------|------|-------------|
| **Free trial** | $0 | Apify free tier includes monthly compute credits |
| **Pay per URL** | ~$0.01-0.05/URL | Full tech stack analysis per URL |
| **vs. BuiltWith** | Saves $295/mo | Same technology detection, no subscription |
| **vs. Wappalyzer** | Saves $250/mo | More technologies detected, bulk processing |
| **vs. SimilarTech** | Saves $199/mo | Real-time scanning, structured JSON output |

## How It Compares to Paid Tech Detection Tools

| Feature | This Actor (FREE) | BuiltWith ($295/mo) | Wappalyzer ($250/mo) | SimilarTech ($199/mo) |
|---------|-------------------|---------------------|---------------------|----------------------|
| Technologies detected | 80+ | 50,000+ | 1,000+ | 10,000+ |
| Real-time scanning | Yes | No (cached) | Yes | No (cached) |
| Confidence scoring | Yes (50-100%) | No | No | No |
| Category filtering | Yes | Limited | Limited | Limited |
| Security headers audit | Yes | No | No | No |
| Bulk URL processing | Unlimited | Plan-limited | Plan-limited | Plan-limited |
| API/automation | Yes (Apify API) | Yes ($795/mo) | Yes ($250/mo) | Yes |
| JSON/CSV/Excel export | Yes | Yes | Yes | Yes |
| Scheduling | Yes (Apify) | No | No | No |
| Monthly cost | $0 (pay per run) | $295-795 | $250 | $199 |

> **When to use this Actor:** You want fast, real-time technology detection for sales prospecting, competitive analysis, or market research without paying hundreds per month for BuiltWith or Wappalyzer subscriptions.

## Quick Start (3 Steps)

1. **Click "Try for free"** on this Actor's page in Apify Store
2. **Paste website URLs** (e.g., `https://stripe.com`, `https://github.com`)
3. **Click "Start"** and get a full tech stack breakdown as JSON, CSV, or Excel

## Input

| Field | Type | Default | Description |
|-------|------|---------|-------------|
| `urls` | string[] | *required* | Website URLs to scan |
| `includeHeaders` | boolean | `true` | Analyze HTTP headers for server/CDN/security info |
| `includeMetadata` | boolean | `true` | Include page title, description, favicon |
| `categoryFilter` | string[] | all | Only return specific categories (e.g., `["framework", "analytics"]`) |
| `delayMs` | integer | `1000` | Delay between requests in ms |

### Example Input -- Full Scan

```json
{
  "urls": ["https://stripe.com", "https://github.com", "https://vercel.com"],
  "includeHeaders": true,
  "includeMetadata": true,
  "delayMs": 1000
}
```

### Example Input -- Frameworks Only

```json
{
  "urls": ["https://stripe.com", "https://github.com"],
  "categoryFilter": ["framework", "css-framework", "javascript-library"],
  "includeHeaders": false,
  "includeMetadata": false
}
```

## Output Example

```json
{
  "url": "https://stripe.com",
  "success": true,
  "technologiesCount": 12,
  "technologies": [
    { "name": "React", "category": "framework", "confidence": 100 },
    { "name": "Next.js", "category": "framework", "confidence": 100 },
    { "name": "Stripe", "category": "payment", "confidence": 100 },
    { "name": "Cloudflare", "category": "cdn", "confidence": 75 },
    { "name": "Google Tag Manager", "category": "tag-manager", "confidence": 100 },
    { "name": "Google Analytics 4", "category": "analytics", "confidence": 100 }
  ],
  "byCategory": {
    "framework": [
      { "name": "React", "confidence": 100 },
      { "name": "Next.js", "confidence": 100 }
    ],
    "payment": [
      { "name": "Stripe", "confidence": 100 }
    ],
    "cdn": [
      { "name": "Cloudflare", "confidence": 75 }
    ]
  },
  "metadata": {
    "title": "Stripe | Financial Infrastructure to Grow Your Revenue",
    "description": "...",
    "favicon": "/favicon.ico",
    "ogImage": "https://stripe.com/img/v3/home/social.png"
  },
  "securityHeaders": {
    "strict-transport-security": "max-age=63072000",
    "content-security-policy": "...",
    "x-content-type-options": "nosniff",
    "x-frame-options": "SAMEORIGIN"
  },
  "server": "cloudflare"
}
```

## Real-World Use Cases

### 1. Sales Prospecting by Tech Stack
"Find me all companies using Shopify + Stripe" -- Bulk-scan prospect URLs to identify which ones use specific technologies, then prioritize outreach based on tech fit.

### 2. Competitive Tech Analysis
Scan your top 20 competitors to understand what frameworks, analytics, and marketing tools they use. Identify technology trends in your industry.

### 3. Technology Migration Planning
Before migrating from WordPress to Next.js, scan 50+ sites that already made the switch to understand common technology companions (CDN, analytics, etc.).

### 4. Agency Website Audits
Quickly audit a prospect's website and identify outdated technologies, missing analytics, and security gaps. Generate a tech audit report for your sales process.

### 5. Market Research at Scale
Scan 1,000+ websites in a vertical to produce technology adoption reports: "What percentage of e-commerce sites use Stripe vs. PayPal?"

### 6. Security Posture Assessment
Check security headers (HSTS, CSP, X-Frame-Options) across your portfolio of sites to identify which ones need security hardening.

## Available Categories

Use these in the `categoryFilter` input to narrow results:

`framework`, `cms`, `analytics`, `cdn`, `payment`, `marketing`, `hosting`, `javascript-library`, `css-framework`, `security`, `font`, `tag-manager`, `advertising`, `chat`, `video`, `database`, `server`

## FAQ

**Q: How many technologies can this detect?**
A: 80+ technologies across 17 categories, with new technologies added regularly. Covers the most popular and business-relevant tools.

**Q: How does confidence scoring work?**
A: Each technology has multiple detection patterns (HTML signatures, HTTP headers). Confidence reflects the percentage of patterns matched: 100% = all patterns found (definite), 50% = minimum one pattern found (likely). Higher confidence = more certain detection.

**Q: Can I scan thousands of URLs?**
A: Yes. Processing scales linearly. Use the `delayMs` parameter to control request pacing. For 1,000+ URLs, consider setting `includeHeaders: false` for faster processing.

**Q: Does this detect server-side technologies?**
A: Partially. Server-side frameworks are detected via HTTP response headers (e.g., `X-Powered-By: Express`) and HTML fingerprints. Pure backend technologies without client-facing signatures are not detectable.

**Q: How does this compare to BuiltWith?**
A: BuiltWith has a larger technology database (50,000+) built over 15+ years with historical data. This Actor detects 80+ of the most business-relevant technologies in real-time, for free. For most sales prospecting and competitive analysis, 80+ technologies covers 95%+ of practical use cases.

**Q: Can I schedule regular scans?**
A: Yes. Use Apify's built-in scheduler to monitor technology changes over time. Track when competitors adopt new tools or switch frameworks.

## Pricing

Pay Per Event -- charged per URL scanned. Typical cost: $0.01-0.05 per URL depending on response time. Free Apify tier available for testing.
