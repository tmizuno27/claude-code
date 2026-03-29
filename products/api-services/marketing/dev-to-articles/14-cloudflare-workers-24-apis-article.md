---
title: I Built 24 APIs on Cloudflare Workers — Here's What I Learned (And What I'd Do Differently)
tags: cloudflare, api, webdev, javascript
published: false
---

Over the past several months, I built and shipped 24 production APIs on Cloudflare Workers. All are live on RapidAPI. Some get traffic. Some don't. Here's an honest breakdown of the architecture decisions, the surprising wins, the frustrations, and what I'd change if I started over.

## Why Cloudflare Workers?

My constraint: I wanted zero fixed infrastructure costs while I validated whether anyone would actually pay for these APIs.

Workers fit that perfectly:
- **100,000 free requests/day** — enough to test and iterate without paying anything
- **No cold starts** (unlike Lambda) — requests wake in under 5ms
- **Global edge** — 300+ locations, sub-50ms P99 for most endpoints
- **No server to maintain** — deploy with `wrangler deploy`, done

The tradeoff: Workers run in a V8 isolate, not Node.js. No native modules, no filesystem access, CPU time capped at 10ms (50ms on paid plans). If you need to run Puppeteer or ffmpeg, Workers isn't your answer.

## The API Portfolio

Here's the full list across categories:

**Data & Lookup**
- IP Geolocation + VPN Detection
- WHOIS & DNS Lookup
- Crypto Prices (Bitcoin, Ethereum, 10,000+ coins)
- Currency Exchange Rates
- Company Data & Enrichment
- Weather Data

**Content & Media**
- Website Screenshot (Puppeteer via external service)
- QR Code Generator (SVG + PNG)
- Placeholder Image Generator
- Social Video Downloader
- PDF Generator (HTML/Markdown/URL)
- Markdown to HTML Converter

**Text & AI**
- Text Analysis (NLP — sentiment, keywords, readability)
- AI Translation (44 languages)
- AI Text Generator
- Hash & Encoding Utilities
- JSON Formatter & Validator

**SEO & Marketing**
- SEO Analyzer
- Trends Aggregator (Google, Reddit, HN, GitHub)
- News Aggregator (BBC, NYT, TechCrunch, HN, Dev.to)
- URL Shortener
- Link Preview Generator
- Email Validation

**WordPress**
- WP Internal Link Suggester

All are on RapidAPI: [rapidapi.com/user/miccho27-RNuiryMxge](https://rapidapi.com/user/miccho27-RNuiryMxge)

## Architecture Patterns That Worked

### 1. Cache Everything at the Edge

Workers KV has ~50ms read latency globally. For any endpoint where freshness isn't critical (crypto prices, news, geolocation), caching at the edge is the single biggest performance win.

```javascript
// Pattern I use across almost every API
export default {
  async fetch(request, env) {
    const cacheKey = new Request(request.url, request);
    const cache = caches.default;

    // Try cache first
    let response = await cache.match(cacheKey);
    if (response) {
      return new Response(response.body, {
        headers: { ...response.headers, 'X-Cache': 'HIT' }
      });
    }

    // Fetch and cache
    const data = await fetchFromUpstream(request, env);
    const jsonResponse = Response.json(data, {
      headers: {
        'Cache-Control': 'public, max-age=300', // 5 min
        'X-Cache': 'MISS'
      }
    });

    // Cache in background (don't await)
    event.waitUntil(cache.put(cacheKey, jsonResponse.clone()));
    return jsonResponse;
  }
};
```

This alone cut upstream API calls by 70%+ on my trends and crypto endpoints.

### 2. Consistent Error Response Shape

I standardized this across all 24 APIs after spending too much time debugging inconsistent error formats:

```javascript
function errorResponse(status, code, message, details = null) {
  return Response.json(
    {
      success: false,
      error: { code, message, details },
      timestamp: new Date().toISOString()
    },
    {
      status,
      headers: { 'Content-Type': 'application/json' }
    }
  );
}

// Usage
if (!params.get('ip')) {
  return errorResponse(400, 'MISSING_PARAM', 'ip parameter is required');
}
```

### 3. CORS in One Place

Every API needs this. I put it in a shared utility:

```javascript
const CORS_HEADERS = {
  'Access-Control-Allow-Origin': '*',
  'Access-Control-Allow-Methods': 'GET, POST, OPTIONS',
  'Access-Control-Allow-Headers': 'Content-Type, x-rapidapi-key',
};

export function handleOptions() {
  return new Response(null, { status: 204, headers: CORS_HEADERS });
}

export function addCors(response) {
  const newResponse = new Response(response.body, response);
  Object.entries(CORS_HEADERS).forEach(([k, v]) => {
    newResponse.headers.set(k, v);
  });
  return newResponse;
}
```

## What Surprised Me

### The CPU Time Limit Is a Real Constraint

Workers have a 10ms CPU time limit on the free plan. This isn't wall-clock time — it's actual CPU execution time. For most JSON APIs, this isn't an issue. But for:

- Base64 encoding large files (PDF generator)
- Complex regex on long strings
- Parsing huge JSON responses from upstream APIs

I hit the limit and had to either:
1. Move to a paid Workers plan ($5/month, 50ms CPU)
2. Restructure the logic to be more efficient
3. Offload the heavy computation to an external service

For the screenshot and PDF APIs, I ultimately had to use external services because headless browsers simply can't run inside a Worker.

### RapidAPI's Free Tier Is Good for Validation, Not Much Else

RapidAPI gives you:
- Good discoverability — your API shows up in search
- Usage analytics
- Subscription management

What they don't tell you clearly: their free tier marketplace takes a 20% revenue share when you start monetizing. That's fine for most use cases, but know it going in.

Also, their API testing UI is unreliable. Always test with curl or Postman.

### Input Validation Upfront Saves You From Embarrassing Bugs

I was sloppy with validation in my early APIs. Lesson learned: validate immediately and return fast.

```javascript
function validateIp(ip) {
  const ipv4 = /^(\d{1,3}\.){3}\d{1,3}$/;
  const ipv6 = /^[0-9a-fA-F:]{2,39}$/;
  if (!ipv4.test(ip) && !ipv6.test(ip)) {
    return { valid: false, message: `Invalid IP format: ${ip}` };
  }
  const parts = ip.split('.');
  if (parts.some(p => parseInt(p) > 255)) {
    return { valid: false, message: `IP octet out of range: ${ip}` };
  }
  return { valid: true };
}
```

## What I'd Do Differently

**1. Write integration tests from day one.** I have unit tests, but I didn't build a proper test harness that fires real HTTP requests against a staging environment. Regressions from upstream API changes have bitten me more than once.

**2. Build a single admin dashboard earlier.** Managing 24 APIs means checking 24 different RapidAPI pages for usage stats. I eventually built a consolidated dashboard, but I should have done it after API #5, not API #24.

**3. Don't name everything "Free [X] API".** Practical for SEO, terrible for brand building. If I'm ever going to move off RapidAPI and sell direct, I need recognizable product names.

**4. Rate limit more aggressively at the Worker level.** RapidAPI handles subscription limits, but I still get bad actors who try to abuse the free tier. Workers supports rate limiting natively now — I should use it.

## The Numbers (Honest)

- **Total APIs**: 24 live
- **Monthly requests (free tier)**: ~2,000–5,000 combined
- **Paying subscribers**: still in early stage
- **Hosting cost**: $5/month (Workers paid plan for the CPU-heavy ones)

The traffic numbers are modest. Building the APIs was relatively fast; getting consistent traffic is the slow part. This is a long-term SEO + content marketing play, not a "launch and profit" story.

## What's Working

The APIs with the most organic traction:
1. **IP Geolocation** — every developer needs this at some point
2. **Trends Aggregator** — unique combination of sources in one call
3. **Screenshot API** — the "no Puppeteer setup" pitch resonates

The pattern: APIs that solve a specific painful setup problem outperform generic data APIs.

---

If you're considering building on Cloudflare Workers, I'd say go for it — especially for the zero-config global edge deployment. Just go in with realistic expectations about the CPU time limits and plan your caching strategy upfront.

[Browse all 24 APIs →](https://rapidapi.com/user/miccho27-RNuiryMxge)

Happy to answer questions about any of the implementation details in the comments.
