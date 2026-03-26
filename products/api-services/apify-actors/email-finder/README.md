# Email Finder - Free No-Code B2B Contact Scraper (Alternative to Hunter.io, Snov.io, FindThatLead)

Find email addresses, phone numbers, and social media links from any website -- no API keys, no monthly subscription. Perfect for lead generation, sales prospecting, and business directory enrichment. The best free alternative to Hunter.io, Snov.io, FindThatLead, and Lusha.

## Who Is This For?

- **Sales teams & SDRs** -- Build prospect contact lists from company websites before outreach
- **Growth hackers** -- Scrape contact info at scale for cold email campaigns
- **Recruiters** -- Find hiring manager emails and company social profiles from career pages
- **Market researchers** -- Collect contact data across an industry for analysis
- **Freelancers** -- Find decision-maker emails on prospect websites to pitch services

## Features

- **Email Extraction** -- Finds all email addresses with smart filtering (removes false positives like image@2x, noreply, etc.)
- **Phone Detection** -- Extracts phone numbers from text and `tel:` links
- **Social Media Links** -- Detects Facebook, Twitter/X, LinkedIn, Instagram, YouTube, TikTok, GitHub
- **Company Info** -- Extracts organization data from JSON-LD structured data (name, address, description)
- **Deep Scan** -- Optionally crawls /contact, /about, /team pages for more comprehensive results
- **Anti-Detection** -- Browser-like headers and random delays to avoid blocking
- **Zero Configuration** -- No API keys, no developer accounts, no signup required

## Pricing -- Free to Start

| Tier | Cost | What You Get |
|------|------|-------------|
| **Free trial** | $0 | Apify free tier includes monthly compute credits |
| **Pay per site** | ~$0.01-0.05/website | Only pay for actual Apify compute used |
| **vs. Hunter.io** | Saves $49-399/mo | Same contact discovery from public sources |
| **vs. Snov.io** | Saves $39-199/mo | No credit system, unlimited scans |
| **vs. Lusha** | Saves $39-69/mo | No per-contact pricing |

## Quick Start (3 Steps)

1. **Click "Try for free"** on this Actor's page in Apify Store
2. **Paste website URLs** you want to scan for contact info (see examples below)
3. **Click "Start"** and download results as JSON, CSV, or Excel

## How It Compares to Paid Email Finders

| Feature | This Actor (FREE) | Hunter.io ($49/mo) | Snov.io ($39/mo) | FindThatLead ($49/mo) | Lusha ($39/mo) |
|---------|-------------------|-------------------|------------------|----------------------|----------------|
| Email extraction | Yes | Yes | Yes | Yes | Yes |
| Phone numbers | Yes | No | No | No | Yes |
| Social media links | 7 platforms | No | LinkedIn only | No | LinkedIn only |
| Company info (JSON-LD) | Yes | No | No | No | No |
| Deep scan (/contact, /about) | Yes | No | No | No | No |
| API/automation | Yes (Apify API) | Yes | Yes | Yes | Yes |
| Bulk processing | Unlimited | 25-500 credits/mo | 50-5000 credits/mo | Plan-limited | 5-100 credits/mo |
| Cloud-based | Yes | Yes | Yes | Yes | Browser extension |
| API keys required | None | Yes | Yes | Yes | Yes |
| Monthly cost | $0 (pay per run) | $49-399 | $39-199 | $49-399 | $39-69 |

## Input

| Field | Type | Default | Description |
|-------|------|---------|-------------|
| `urls` | string[] | required | Websites to scan for contact info |
| `scanDepth` | string | `"homepage"` | `"homepage"` (fast) or `"deep"` (also scans /contact, /about, /team pages) |
| `includePhones` | boolean | `true` | Extract phone numbers |
| `includeSocial` | boolean | `true` | Extract social media links |

### Example Input -- Single Website

```json
{
  "urls": [
    "https://example.com"
  ],
  "scanDepth": "deep",
  "includePhones": true,
  "includeSocial": true
}
```

### Example Input -- Bulk Lead Generation

```json
{
  "urls": [
    "https://company-a.com",
    "https://company-b.com",
    "https://company-c.com",
    "https://company-d.com",
    "https://company-e.com"
  ],
  "scanDepth": "deep",
  "includePhones": true,
  "includeSocial": true
}
```

## Output Example

```json
{
  "domain": "example.com",
  "emails": ["info@example.com", "sales@example.com", "support@example.com"],
  "emailCount": 3,
  "phones": ["+1-555-123-4567", "+1-555-987-6543"],
  "socialLinks": {
    "linkedin": "https://www.linkedin.com/company/example",
    "twitter": "https://twitter.com/example",
    "facebook": "https://www.facebook.com/example",
    "instagram": "https://www.instagram.com/example",
    "github": "https://github.com/example"
  },
  "companyInfo": {
    "name": "Example Inc.",
    "description": "Leading provider of example services",
    "address": "123 Main St, San Francisco, CA"
  },
  "pagesScanned": [
    "https://example.com",
    "https://example.com/contact",
    "https://example.com/about"
  ]
}
```

## Output Fields

| Field | Description |
|-------|-------------|
| `domain` | Website domain |
| `emails` | Array of found email addresses |
| `emailCount` | Number of unique emails found |
| `phones` | Array of phone numbers (when `includePhones: true`) |
| `socialLinks` | Object with social media URLs (when `includeSocial: true`) |
| `companyInfo` | Organization name, description, address from JSON-LD structured data |
| `pagesScanned` | URLs that were scanned |

## Real-World Use Cases

### 1. Cold Email Outreach Pipeline

Upload a CSV of prospect websites, run this Actor in bulk, and feed results into your email outreach tool (Instantly, Mailshake, Lemlist) via Apify integrations.

### 2. CRM Enrichment

Enrich your CRM records with missing email, phone, and social data. Schedule weekly runs to keep contact info fresh.

### 3. Competitor Contact Research

Scan competitor websites to identify key contacts, social channels, and company structure from their /about and /team pages.

### 4. Business Directory Building

Scrape hundreds of business websites in a niche to build a contact database. Export to Google Sheets for a free lead database.

### 5. Freelancer Prospect Discovery

Find decision-maker emails on potential client websites. Use deep scan to check /about and /team pages for personal email addresses.

## FAQ

**Q: How does this compare to Hunter.io?**

A: Hunter.io uses a proprietary database of verified emails, so it may find emails not published on the website itself. This Actor extracts only what's publicly visible on the website (HTML, structured data, linked pages). For most B2B prospecting, website-published contacts are sufficient and this approach costs nothing per month.

**Q: Does deep scan slow down the process?**

A: Deep scan adds 2-5 seconds per website since it checks additional pages (/contact, /about, /team). For bulk runs, the extra time is minimal and significantly increases email discovery rates.

**Q: How are false positive emails filtered?**

A: The Actor filters out common non-email patterns (image@2x.png, noreply@, wixpress, sentry, cloudflare addresses, etc.) and validates email format before including in results.

**Q: Can I schedule this to run regularly?**

A: Yes. Use Apify's built-in scheduler to run daily or weekly. Combine with webhooks to push new contacts to your CRM, Google Sheets, or Slack automatically.

**Q: What social platforms are detected?**

A: Facebook, Twitter/X, LinkedIn, Instagram, YouTube, TikTok, and GitHub. Links are extracted from page HTML, footer sections, and structured data.

**Q: Can I export results to CSV or Google Sheets?**

A: Yes. Apify datasets can be exported as JSON, CSV, Excel, or pushed directly to Google Sheets, Slack, email, or any webhook endpoint.
