# RapidAPI リスティング更新用コピペ集（上位5本）

**作成日**: 2026-03-28
**用途**: RapidAPI Provider Dashboard → 各APIの「About」タブに貼り付け

> RapidAPI Platform APIはEnterprise Accessが必要なため、手動更新で対応。
> ダッシュボード: https://provider.rapidapi.com/

---

## 1. QR Code Generator API

### ダッシュボードURL
https://provider.rapidapi.com/hub-listing/api/qr-code-generator-api

### Short Description（1行、API検索結果に表示）

```
Generate QR codes in <50ms from 300+ edge locations. PNG, SVG, Base64. Custom colors & error correction. Free 500 req/mo.
```

### Long Description（About タブ → Description欄）

```
The Fastest Free QR Code API on RapidAPI

Generate QR codes in under 50ms from Cloudflare's 300+ edge locations worldwide. Returns PNG, SVG, or Base64 JSON with full color customization and selectable error correction levels (L/M/Q/H).

WHY DEVELOPERS CHOOSE THIS API:
• Sub-50ms latency (Cloudflare edge network) — 5-10x faster than alternatives
• Base64 JSON output — embed QR codes directly in HTML/email without file I/O
• Custom foreground + background colors for brand consistency
• Google Charts QR API was deprecated — this is the modern replacement
• Flat-rate pricing: Pro $5.99/50K vs QR Code Monkey $14/mo

REAL-WORLD USE CASES:
• E-Commerce: Dynamic checkout QR codes per order (sub-50ms = no checkout delay)
• Restaurants: Branded contactless digital menus with custom colors, SVG for print
• SaaS Invoices: Base64 format embeds directly in HTML invoices and PDFs
• Marketing: Branded campaign QR codes for flyers, posters, business cards
• Mobile Apps: Deep link QR codes (myapp://screen/123) for iOS Universal Links / Android App Links
• CI/CD: Automated QR generation for deployment URLs and staging previews

FORMATS:
• PNG — raster, ideal for web/mobile
• SVG — vector, scales perfectly for print
• Base64 JSON — embeddable data_uri, no file download needed

FREE TIER: 500 requests/month, no credit card required.
```

### Tags（カンマ区切りで入力）

```
qr code, qr code generator, qr code api, free qr api, svg qr code, base64 qr code, custom qr code, branded qr code, cloudflare workers, google charts alternative
```

### Category

```
Tools
```

---

## 2. Email Validation API

### ダッシュボードURL
https://provider.rapidapi.com/hub-listing/api/email-validation-api

### Short Description

```
Validate emails with MX verification, disposable detection (500+ domains), typo correction & bulk validation. Save $390/mo vs ZeroBounce. Free 500/mo.
```

### Long Description

```
Save $390/mo vs ZeroBounce — Validate 50K Emails for $9.99 Flat

Most email validation services charge per email. At 50K emails/month, ZeroBounce costs $400, Hunter.io costs $4,900. This API costs $9.99 flat. At 500K emails, you save $3,970/month.

EVERY VALIDATION INCLUDES (no upsell tiers):
• RFC 5322 format validation with detailed error messages
• MX record verification via DNS-over-HTTPS (Cloudflare 1.1.1.1)
• Disposable email detection against 500+ domains (Mailinator, Guerrilla, 10MinuteMail, etc.)
• Free provider detection (Gmail, Yahoo, Outlook)
• Role-based address detection (admin@, info@, support@, noreply@)
• Typo correction (gmial.com → gmail.com, yaho.com → yahoo.com)
• Confidence score (0-100) for easy filtering

BULK VALIDATION: Validate up to 50 emails per request via POST /validate/bulk.

USE CASES:
• SaaS Sign-Up: Block disposable emails, catch typos before account creation
• Email Marketing: Clean lists before campaigns — protect sender reputation
• E-Commerce Checkout: Catch typos so customers get receipts and tracking
• Lead Generation: Score inbound leads by email quality
• Fraud Prevention: Disposable emails = #1 signal for fake accounts and trial farming

ZERO EMAILS SENT: All validation is DNS-based. No bounce risk.

COST COMPARISON (50K emails/mo):
• This API: $9.99 | ZeroBounce: $400 | Hunter.io: $4,900 | NeverBounce: $400

FREE TIER: 500 validations/month, no credit card required.
```

### Tags

```
email validation, email verification, disposable email detection, mx lookup, email hygiene, bulk email validation, zerobounce alternative, email typo correction, bounce prevention, saas signup validation
```

### Category

```
Email
```

---

## 3. Screenshot API

### ダッシュボードURL
https://provider.rapidapi.com/hub-listing/api/screenshot-api

### Short Description

```
Capture any website as PNG or JPEG. Full-page, custom viewports (320-3840px), render delay for SPAs, 1-hour edge cache. Free 500/mo.
```

### Long Description

```
Free Website Screenshot API — Capture Any Page as PNG or JPEG

Capture screenshots of any website with custom viewport sizes, full-page capture, JPEG quality control, and render delay for JavaScript-heavy pages. Powered by Cloudflare Workers with 1-hour edge caching.

WHY THIS API:
• Full-page capture — scroll and capture the entire page, not just the viewport
• Custom viewports — desktop (1920x1080), tablet (768x1024), mobile (375x812)
• Render delay — wait up to 5 seconds for JavaScript/SPA content to load
• 1-hour Cloudflare edge cache — repeat requests served instantly
• Flat-rate pricing: Pro $9.99/50K vs ScreenshotAPI $19/1K ($0.019/each)

USE CASES:
• OG Image Generation: Auto-generate Open Graph preview images from any URL
• Visual Regression Testing: Compare screenshots across viewports in CI/CD
• SEO Monitoring: Capture competitor pages for visual comparison over time
• Portfolio Builders: Auto-generate thumbnails for website showcase galleries
• Link Preview Services: Show visual previews of shared URLs in chat/social
• PDF Reports: Embed website screenshots in automated reports
• Compliance Archiving: Capture web pages for record-keeping

FORMATS: PNG (crisp) or JPEG with quality control (1-100).
VIEWPORTS: 320-3840px width, covers mobile through 4K.

COST COMPARISON:
• This API: $0 (500/mo free), $9.99 (50K) | ScreenshotAPI: $19/1K | Screenshotlayer: $10/2K

FREE TIER: 500 screenshots/month, no credit card required.
```

### Tags

```
screenshot api, website screenshot, webpage capture, url to image, full page screenshot, website thumbnail, visual regression, og image generator, headless browser, screenshotapi alternative
```

### Category

```
Tools
```

---

## 4. IP Geolocation API

### ダッシュボードURL
https://provider.rapidapi.com/hub-listing/api/ip-geolocation-api

### Short Description

```
IP to location + VPN/proxy/datacenter detection + bulk lookup (20 IPs). 15 data fields. Free VPN detection — ipinfo.io charges $99/mo. Free 500/mo.
```

### Long Description

```
Free IP Geolocation with VPN Detection — ipinfo.io Charges $99/mo for This

Look up any IP address to get country, city, region, timezone, ISP, and VPN/proxy/datacenter detection. Supports single IP lookup, own-IP detection (/me), and bulk lookups (up to 20 IPs per request).

KEY DIFFERENTIATOR — FREE VPN DETECTION:
ipinfo.io charges $99/month for VPN detection. This API includes it on all plans, including free.

15 DATA FIELDS PER LOOKUP:
• ip, country, country_name, region, city
• latitude, longitude, timezone
• isp
• is_vpn, is_proxy, is_datacenter
• currency, languages

3 ENDPOINTS:
• GET /me — Your own IP geolocation (uses Cloudflare request.cf, zero external calls, fastest)
• GET /lookup?ip=8.8.8.8 — Any IPv4/IPv6 address
• POST /lookup/bulk — Up to 20 IPs per request

USE CASES:
• Fraud Detection: Flag VPN/proxy/datacenter IPs in payment flows
• Content Localization: Serve region-specific content, currency, language
• Ad Targeting: Geo-target ads based on visitor location
• Access Control: Geo-fencing for compliance (GDPR, gambling, financial regulations)
• Cybersecurity: Monitor login locations, detect suspicious access patterns
• Analytics Enrichment: Add geographic data to event logs and dashboards

COST COMPARISON:
• This API: $0 (500/mo) / $5.99 (50K) | ipinfo.io: $99/mo (VPN detection) | ipstack: $9.99/mo

24-HOUR EDGE CACHE via Cloudflare Workers.
FREE TIER: 500 requests/month, no credit card required.
```

### Tags

```
ip geolocation, ip lookup, geoip, vpn detection, proxy detection, ip to location, bulk ip lookup, ipinfo alternative, ip address api, fraud detection, datacenter detection
```

### Category

```
Location
```

---

## 5. Currency Exchange API

### ダッシュボードURL
https://provider.rapidapi.com/hub-listing/api/currency-exchange-api

### Short Description

```
ECB-sourced real-time & historical FX rates (back to 1999). 30+ currencies. Direct conversion. Any base currency on free tier. Free 500/mo.
```

### Long Description

```
Free Currency Exchange API — ECB Official Rates, Historical Data Back to 1999

Get real-time and historical currency exchange rates from the European Central Bank (ECB). Convert between 30+ currencies, fetch historical rates back to January 1999, and list all supported currency codes.

KEY ADVANTAGES:
• Official ECB data source — trusted central bank rates
• Historical rates back to 1999 — no other free API offers this depth
• Any base currency on free tier — Fixer.io limits to EUR, Open Exchange Rates limits to USD
• Direct conversion endpoint — single call to convert amounts
• 1-hour Cloudflare edge cache for fast response times

4 ENDPOINTS:
• GET /rates — Latest exchange rates for any base currency
• GET /convert — Convert between any two currencies with amount
• GET /historical — Rates for any date back to 1999-01-04
• GET /currencies — List all 30+ supported currency codes

30+ CURRENCIES: USD, EUR, GBP, JPY, BRL, CNY, INR, CHF, CAD, AUD, KRW, MXN, SGD, HKD, and more.

USE CASES:
• E-Commerce: Display product prices in customer's local currency
• Fintech Apps: Power currency conversion features in banking/payment apps
• Travel Apps: Real-time rates for travel planning and expense tracking
• Accounting Software: Historical rates for multi-currency bookkeeping
• SaaS Pricing: Localize subscription pricing by region
• Data Analytics: Normalize revenue across currencies for reporting

COST COMPARISON:
• This API: $0 (500/mo) / $5.99 (50K) | Fixer.io: $10/mo | ExchangeRate-API: $9.99/mo

FREE TIER: 500 requests/month, no credit card required.
```

### Tags

```
currency exchange, exchange rate, currency converter, fx rates, ecb exchange rates, historical exchange rates, forex api, currency conversion, fixer alternative, real-time rates
```

### Category

```
Finance
```

---

## 更新手順

1. https://provider.rapidapi.com/ にログイン
2. 左メニュー「My APIs」から対象APIをクリック
3. 「Hub Listing」タブ → 「About」セクション
4. 以下を更新:
   - **Short Description**: 1行の概要（検索結果に表示される）
   - **Long Description**: 上記のテキストをそのまま貼り付け
   - **Tags**: カンマ区切りで入力（既存タグを削除してから貼り付け）
   - **Category**: 適切なカテゴリを選択
5. 「Save」をクリック
6. 5本全て完了したら、各APIページをブラウザで開いて表示を確認

**所要時間**: 約15-20分（5本分）
