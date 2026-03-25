# Email Finder

Find email addresses, phone numbers, and social media links from any website. Perfect for lead generation and sales prospecting.

## Features

- **Email extraction**: Finds all email addresses with smart filtering (removes false positives)
- **Phone detection**: Extracts phone numbers from text and `tel:` links
- **Social media links**: Detects Facebook, Twitter/X, LinkedIn, Instagram, YouTube, TikTok, GitHub
- **Company info**: Extracts organization data from JSON-LD structured data
- **Deep scan**: Optionally crawls /contact, /about, /team pages for more data
- **Anti-detection**: Browser-like headers and random delays

## Input

```json
{
  "urls": [
    "https://example.com",
    "https://another-company.com"
  ],
  "scanDepth": "deep",
  "includePhones": true,
  "includeSocial": true
}
```

## Parameters

| Field | Type | Default | Description |
|-------|------|---------|-------------|
| urls | string[] | required | Websites to scan |
| scanDepth | string | "homepage" | "homepage" or "deep" (also scans /contact, /about, etc.) |
| includePhones | boolean | true | Extract phone numbers |
| includeSocial | boolean | true | Extract social media links |

## Output

| Field | Description |
|-------|-------------|
| domain | Website domain |
| emails | Array of found email addresses |
| emailCount | Number of unique emails found |
| phones | Array of phone numbers (optional) |
| socialLinks | Object with social media URLs (optional) |
| companyInfo | Organization name, description, address from structured data |
| pagesScanned | URLs that were scanned |

## Use Cases

- B2B lead generation
- Sales prospecting and outreach
- Business directory enrichment
- Competitor contact research
