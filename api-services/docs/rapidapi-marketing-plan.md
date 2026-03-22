# RapidAPI Marketing Plan - 24 API Portfolio

Created: 2026-03-22 | Current MRR: $9.99 (1 subscriber on IP Geolocation)

## Goal

Scale from $9.99/mo to $100+/mo within 60 days through external content marketing, cross-promotion, community discovery, and pricing optimization.

---

## 1. Dev.to Article Outlines (Top 5 APIs)

### Article 1: "5 Free APIs Every Web Developer Should Bookmark in 2026"
**Target APIs**: QR Code, Screenshot, Email Validation, IP Geolocation, Currency Exchange

- **Hook**: "Stop paying for basic developer utilities. Here are 5 APIs with generous free tiers that run on Cloudflare Workers with sub-100ms latency."
- **Structure**:
  1. Introduction -- the cost problem with developer APIs
  2. QR Code API -- code example: generate QR codes for a restaurant menu app
  3. Screenshot API -- code example: build a link preview thumbnail generator
  4. Email Validation API -- code example: add sign-up form validation in 5 lines
  5. IP Geolocation API -- code example: geo-target content in a Next.js app
  6. Currency Exchange API -- code example: multi-currency pricing widget
  7. Conclusion -- all 24 APIs listed with links
- **Tags**: `webdev`, `api`, `javascript`, `tutorial`
- **CTA**: Link to RapidAPI listings, mention "24 Free APIs" collection

### Article 2: "How to Build an Email Hygiene Pipeline with a Free API"
**Target API**: Email Validation

- **Hook**: "Your mailing list is probably 20-30% garbage. Here's how to clean it for free."
- **Structure**:
  1. Why email validation matters (bounce rates, sender reputation, deliverability)
  2. The API: features overview (MX lookup, disposable detection, typo fix)
  3. Tutorial: Python script to bulk-validate a CSV of emails
  4. Tutorial: Add real-time validation to a React sign-up form
  5. Scoring strategy: how to use the 0-100 score for segmentation
  6. Cost comparison vs ZeroBounce, Hunter.io, NeverBounce
- **Tags**: `email`, `marketing`, `python`, `api`

### Article 3: "Build a Free SEO Audit Tool with the SEO Analyzer API"
**Target API**: SEO Analyzer

- **Hook**: "Ahrefs charges $99/mo. Here's how to build your own SEO checker for $0."
- **Structure**:
  1. What an SEO audit covers (19 checks explained)
  2. Tutorial: build a CLI tool that audits any URL
  3. Tutorial: batch audit 100 pages with Python
  4. Interpret the score: what 80+ vs 50- means for your site
  5. Compare results with Lighthouse and Ahrefs
- **Tags**: `seo`, `webdev`, `python`, `tutorial`

### Article 4: "Add IP-Based Fraud Detection to Your App in 10 Minutes"
**Target API**: IP Geolocation

- **Hook**: "Your payment form is exposed. Here's a 10-minute fix using IP geolocation + VPN detection."
- **Structure**:
  1. Why IP geolocation matters for fraud prevention
  2. The API: VPN, proxy, datacenter detection
  3. Tutorial: Express.js middleware for fraud scoring
  4. Tutorial: Python Flask decorator for geo-restriction
  5. Real-world patterns: mismatched billing country vs IP country
- **Tags**: `security`, `node`, `webdev`, `api`

### Article 5: "24 Free REST APIs Running on Cloudflare Workers -- Complete Developer Toolkit"
**Target**: All 24 APIs (listicle/collection post)

- **Hook**: "I built 24 utility APIs on Cloudflare Workers. They're all free. Here's the complete catalog."
- **Structure**:
  1. Why I built this (developer pain points, cost of API subscriptions)
  2. Architecture overview (Cloudflare Workers, $0 hosting, edge latency)
  3. Catalog organized by category:
     - **Data Processing**: JSON Formatter, Hash & Encoding, Markdown Converter
     - **Web Utilities**: QR Code, Screenshot, Link Preview, URL Shortener, PDF Generator
     - **Validation**: Email Validation, SEO Analyzer, WHOIS
     - **AI-Powered**: AI Text, AI Translate, Text Analysis
     - **Market Data**: Currency Exchange, Crypto Data, Weather, Trends, News
     - **Business**: IP Geolocation, Company Data, Social Video, Placeholder Image, WP Internal Link
  4. Each API: 1-paragraph description + quick code snippet
  5. How to get started on RapidAPI
- **Tags**: `webdev`, `api`, `cloudflare`, `freetools`
- **This is the highest-priority article** -- it drives traffic to all 24 APIs

---

## 2. Stack Overflow / Reddit / Community Discovery Strategies

### Stack Overflow Strategy

**Do NOT spam links.** Instead, answer questions that naturally relate to API use cases:

- Search for questions about:
  - "generate qr code programmatically"
  - "validate email without sending"
  - "ip geolocation free api"
  - "currency exchange rate api free"
  - "html to pdf api"
  - "website screenshot api"
- Write high-quality answers that solve the problem, mention the API as one option among alternatives
- Include code snippets that work immediately
- Target questions with 1000+ views and no accepted answer

**Target Tags**: `api`, `rest`, `qr-code`, `email-validation`, `geolocation`, `currency`, `screenshot`, `pdf-generation`

### Reddit Strategy

**Subreddits to target** (with appropriate context, not pure self-promotion):

| Subreddit | Approach | API Focus |
|-----------|----------|-----------|
| r/webdev | "Show r/webdev" post -- share the 24 API toolkit | All |
| r/SideProject | Share as a side project story | All |
| r/programming | Technical deep dive on Cloudflare Workers architecture | All |
| r/learnprogramming | Tutorial: "Build X with free APIs" | QR, Email, Screenshot |
| r/SEO | SEO Analyzer API as a free tool | SEO Analyzer |
| r/cryptocurrency | Crypto Data API for portfolio tracking | Crypto Data |
| r/smallbusiness | Free tools for small business (QR, email validation, currency) | QR, Email, Currency |
| r/Entrepreneur | "Free developer tools I built" | All |
| r/cloudflare | Architecture post about 24 Workers | All |

**Reddit Post Templates**:

1. **r/SideProject**: "I built 24 free APIs on Cloudflare Workers ($0 hosting) and put them on RapidAPI. Here's what I learned."
2. **r/webdev**: "Free API toolkit: QR codes, screenshots, email validation, IP geolocation, and 20 more -- all on Cloudflare Workers"
3. **r/cloudflare**: "Running 24 production APIs on Cloudflare Workers free tier -- architecture and lessons"

### Hacker News

- **Show HN**: "Show HN: 24 Free Developer APIs on Cloudflare Workers"
  - Focus on the technical achievement (24 APIs, $0 hosting, sub-100ms latency)
  - Link to a GitHub repo with sample code or the Dev.to listicle article
  - Be ready to answer technical questions in comments

### Product Hunt

- **Launch title**: "Free Developer API Toolkit -- 24 APIs, $0 to Start"
- **Tagline**: "QR codes, screenshots, email validation, IP geolocation, and 20 more free APIs"
- **Schedule for Tuesday-Thursday** for maximum visibility
- **Prepare**: logo, screenshots, GIF demos of 3-4 APIs
- **Maker comment**: explain the Cloudflare Workers architecture and $0 hosting story

### GitHub

- Create a public repository: `free-api-toolkit` or `24-free-apis`
- README with all 24 APIs, code examples in Python/Node.js/cURL
- Each API gets a folder with working examples
- Star the repo from multiple accounts (ethically -- ask friends/community)
- Add to awesome-apis lists

---

## 3. Cross-Promotion Between APIs

### Bundle Strategy

Group APIs into logical bundles and promote them together:

| Bundle Name | APIs | Target Audience |
|-------------|------|-----------------|
| **Web Developer Essentials** | QR Code, Screenshot, Link Preview, JSON Formatter, Placeholder Image | Frontend/fullstack devs |
| **SEO Toolkit** | SEO Analyzer, WHOIS Domain, Link Preview, WP Internal Link | SEO professionals |
| **SaaS Building Blocks** | Email Validation, IP Geolocation, URL Shortener, PDF Generator | SaaS founders |
| **AI Power Pack** | AI Text, AI Translate, Text Analysis | AI/ML developers |
| **Data & Finance** | Currency Exchange, Crypto Data, Company Data, Weather | Fintech developers |
| **Content Creator Kit** | Markdown Converter, Social Video, News Aggregator, Trends | Content/media devs |

### Cross-Promotion Tactics

1. **In-API promotion**: Add a `related_apis` field in every API's info endpoint (`GET /`) that lists 3-4 complementary APIs with RapidAPI links
2. **README cross-links**: Each README's "Related APIs" section links to complementary APIs
3. **Bundle landing page**: Create a simple HTML page at `homepage/api-toolkit.html` listing all 24 APIs organized by bundle
4. **Dev.to series**: Each article naturally mentions 2-3 other APIs in the portfolio

### Self-Usage for Popularity Score

Use your own APIs in your existing projects to generate real traffic:

| Project | API to Integrate |
|---------|-----------------|
| nambei-oyaji.com | SEO Analyzer (auto-audit new articles), QR Code (shareable article QR) |
| otona-match.com | QR Code (app download QR), Screenshot (app preview images) |
| sim-hikaku.online | Currency Exchange (SIM prices in multiple currencies) |
| WP Linker SaaS | WP Internal Link API, SEO Analyzer |
| Task Dashboard | Weather API (local weather widget) |

---

## 4. Pricing Adjustments

### Current Pricing Analysis

Most APIs are priced at $5.99/mo Pro. The IP Geolocation API (the only one with a subscriber) is at $5.99 Pro / $14.99 Ultra.

### Recommended Pricing Tiers

**Tier 1 -- High-demand APIs** (Screenshot, Email Validation, IP Geolocation, AI Text, SEO Analyzer, Currency Exchange):

| Plan | Price | Requests/mo | Rate Limit |
|------|-------|-------------|------------|
| Basic (FREE) | $0 | 1,000 | 2 req/sec |
| Pro | $9.99 | 100,000 | 20 req/sec |
| Ultra | $29.99 | 1,000,000 | 100 req/sec |
| Mega | $99.99 | Unlimited | 500 req/sec |

**Key change**: Double the free tier to 1,000 requests/month. This is the single most impactful change -- more free users means higher Popularity Score, which means better search ranking, which means more paid conversions.

**Tier 2 -- Medium-demand APIs** (QR Code, PDF Generator, Social Video, Crypto Data, AI Translate, Company Data, WHOIS):

| Plan | Price | Requests/mo | Rate Limit |
|------|-------|-------------|------------|
| Basic (FREE) | $0 | 1,000 | 2 req/sec |
| Pro | $5.99 | 50,000 | 10 req/sec |
| Ultra | $14.99 | 500,000 | 50 req/sec |

**Tier 3 -- Utility APIs** (all others):

| Plan | Price | Requests/mo | Rate Limit |
|------|-------|-------------|------------|
| Basic (FREE) | $0 | 1,000 | 2 req/sec |
| Pro | $3.99 | 50,000 | 10 req/sec |

### Pricing Rationale

1. **Double the free tier** (500 -> 1,000): More free subscribers = higher Popularity Score = better search ranking. The marginal cost of free requests on Cloudflare Workers is literally $0.
2. **Add Mega tier** for high-demand APIs: Enterprise users will pay $99.99/mo for unlimited access. Even one Mega subscriber = 10x current revenue.
3. **Lower utility API pricing** to $3.99: These APIs have less competitive advantage; lower price removes friction.

---

## 5. Immediate Action Items (Priority Order)

### Week 1 (Now)
1. [x] Rewrite all 24 READMEs with SEO-optimized content (DONE)
2. [ ] Update free tier from 500 to 1,000 requests/month on all APIs via RapidAPI Studio
3. [ ] Add pricing tiers (Mega for Tier 1 APIs)
4. [ ] Publish Article 5 on Dev.to ("24 Free REST APIs" listicle)
5. [ ] Create GitHub repo `free-api-toolkit` with code examples

### Week 2
6. [ ] Publish Article 1 on Dev.to ("5 Free APIs Every Web Developer Should Bookmark")
7. [ ] Post on r/SideProject and r/webdev
8. [ ] Answer 5 Stack Overflow questions related to our API use cases
9. [ ] Integrate SEO Analyzer API into nambei-oyaji.com (self-usage)
10. [ ] Integrate QR Code API into all 3 blog sites (article share QR)

### Week 3
11. [ ] Publish Article 2 (Email Hygiene Pipeline)
12. [ ] Publish Article 3 (SEO Audit Tool)
13. [ ] Post on Hacker News (Show HN)
14. [ ] Add `related_apis` cross-promotion to all API info endpoints

### Week 4
15. [ ] Publish Article 4 (IP Fraud Detection)
16. [ ] Product Hunt launch
17. [ ] Review RapidAPI Dashboard search gap data and adjust tags/descriptions
18. [ ] Evaluate subscriber growth and adjust strategy

### Ongoing (Weekly)
- Answer 2-3 Stack Overflow questions per week
- Post 1 Dev.to article per week
- Monitor RapidAPI Dashboard metrics (subscribers, requests, search impressions)
- Self-use APIs in own projects to maintain Popularity Score

---

## 6. Revenue Projection

| Scenario | Timeline | MRR | Assumption |
|----------|----------|-----|------------|
| Conservative | 60 days | $50 | 5 Pro subscribers across top APIs |
| Moderate | 60 days | $150 | 10 Pro + 1 Ultra subscriber |
| Optimistic | 60 days | $500 | 20 Pro + 3 Ultra + 1 Mega subscriber |

The key multiplier is the Dev.to listicle article + GitHub repo + Product Hunt launch driving a wave of free subscribers, which boosts Popularity Score, which creates a self-reinforcing discovery loop on RapidAPI marketplace search.

---

## 7. KPIs to Track

| Metric | Current | 30-day Target | 60-day Target |
|--------|---------|---------------|---------------|
| Total Subscribers (free+paid) | 1 | 50 | 200 |
| Paid Subscribers | 1 | 5 | 15 |
| MRR | $9.99 | $50 | $150 |
| Total API Calls (30d) | 0 | 5,000 | 50,000 |
| Dev.to Articles Published | 0 | 3 | 5 |
| GitHub Stars (toolkit repo) | 0 | 50 | 200 |
| Stack Overflow Answers | 0 | 5 | 15 |
