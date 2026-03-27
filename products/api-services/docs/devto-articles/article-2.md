---
title: "How to Add SEO Audit to Your CI/CD Pipeline in 5 Minutes"
published: false
description: "Automatically catch SEO regressions on every deploy. Add a lightweight SEO check to GitHub Actions using a free API — no Lighthouse, no Puppeteer, no headless browser."
tags: seo, cicd, github, webdev
cover_image:
---

You test your code. You test your UI. But do you test your SEO?

Most teams discover SEO regressions *after* Google notices — missing meta descriptions, broken heading hierarchies, or accidentally noindexed pages that silently tank organic traffic.

Here's how to add an **automated SEO audit** to your CI/CD pipeline in under 5 minutes, using a single API call.

---

## The Problem

SEO issues are invisible at code review time:

- A developer removes an `<h1>` tag during a refactor → heading hierarchy breaks
- A template change drops the meta description → CTR drops 30%
- Someone adds `<meta name="robots" content="noindex">` for staging and forgets to remove it
- Open Graph tags get deleted → social shares look broken

None of these throw errors. None fail unit tests. They ship silently.

---

## The Solution: SEO Checks as a CI Step

We'll use the **[SEO Analyzer API](https://rapidapi.com/miccho27-5OJaGGbBiO/api/seo-analyzer-api)** — a free API running on Cloudflare Workers that analyzes any URL and returns structured SEO data with a score.

### What You Get

One `GET` request returns:

- **SEO score** (0-100) with category breakdown
- Title and meta description (length validation)
- Heading structure (H1-H6 hierarchy)
- Open Graph and Twitter Card tags
- Image alt text coverage
- Internal vs. external link counts
- Canonical URL and robots directives
- Structured data (JSON-LD) presence

---

## Step 1: Create the SEO Check Script

Create `scripts/seo-check.sh` in your repo:

```bash
#!/bin/bash
# seo-check.sh — Fail CI if SEO score drops below threshold

URL="${1:-https://your-site.com}"
THRESHOLD="${2:-70}"

echo "🔍 Running SEO audit on: $URL"
echo "   Minimum score: $THRESHOLD"
echo ""

# Fetch SEO analysis
RESULT=$(curl -sf "https://seo-analyzer-api.t-mizuno27.workers.dev/score?url=$URL")

if [ $? -ne 0 ]; then
  echo "❌ Failed to reach SEO Analyzer API"
  exit 1
fi

# Extract score
SCORE=$(echo "$RESULT" | jq -r '.seo_score // 0')
TITLE=$(echo "$RESULT" | jq -r '.checks.title.value // "MISSING"')
META=$(echo "$RESULT" | jq -r '.checks.meta_description.value // "MISSING"')
H1=$(echo "$RESULT" | jq -r '.checks.h1.count // 0')

echo "📊 Results:"
echo "   SEO Score:        $SCORE / 100"
echo "   Title:            $TITLE"
echo "   Meta Description: $(echo $META | head -c 60)..."
echo "   H1 Tags:          $H1"
echo ""

# Check thresholds
FAILED=0

if [ "$SCORE" -lt "$THRESHOLD" ]; then
  echo "❌ FAIL: SEO score ($SCORE) is below threshold ($THRESHOLD)"
  FAILED=1
fi

if [ "$H1" -eq 0 ]; then
  echo "❌ FAIL: No H1 tag found"
  FAILED=1
fi

if [ "$H1" -gt 1 ]; then
  echo "⚠️  WARN: Multiple H1 tags found ($H1) — consider using only one"
fi

if [ "$TITLE" = "MISSING" ]; then
  echo "❌ FAIL: Title tag is missing"
  FAILED=1
fi

if [ "$META" = "MISSING" ]; then
  echo "⚠️  WARN: Meta description is missing"
fi

if [ $FAILED -eq 1 ]; then
  echo ""
  echo "💡 Full analysis: https://seo-analyzer-api.t-mizuno27.workers.dev/analyze?url=$URL"
  exit 1
fi

echo ""
echo "✅ SEO check passed (score: $SCORE)"
```

Make it executable:

```bash
chmod +x scripts/seo-check.sh
```

---

## Step 2: Add to GitHub Actions

Add this job to your `.github/workflows/deploy.yml` (or create a new workflow):

```yaml
# .github/workflows/seo-check.yml
name: SEO Audit

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

jobs:
  seo-audit:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Wait for deploy preview
        # If using Vercel/Netlify, wait for the preview URL
        # Replace with your actual preview URL logic
        run: sleep 30

      - name: Run SEO check
        run: |
          chmod +x scripts/seo-check.sh
          # Check your production URL (or preview URL for PRs)
          ./scripts/seo-check.sh "https://your-site.com" 70
```

### For Multiple Pages

Check your most important pages:

```yaml
      - name: Run SEO checks on key pages
        run: |
          chmod +x scripts/seo-check.sh
          SITE="https://your-site.com"

          echo "=== Homepage ==="
          ./scripts/seo-check.sh "$SITE" 80

          echo "=== Pricing ==="
          ./scripts/seo-check.sh "$SITE/pricing" 70

          echo "=== Blog ==="
          ./scripts/seo-check.sh "$SITE/blog" 70
```

---

## Step 3: Advanced — Full Analysis in JSON

For more detailed checks, use the `/analyze` endpoint and parse specific fields:

```bash
#!/bin/bash
# seo-check-detailed.sh — Detailed SEO validation

URL="$1"
RESULT=$(curl -sf "https://seo-analyzer-api.t-mizuno27.workers.dev/analyze?url=$URL")

# Title length check (50-60 chars is optimal)
TITLE_LEN=$(echo "$RESULT" | jq -r '.title | length')
if [ "$TITLE_LEN" -gt 60 ]; then
  echo "⚠️  Title is too long ($TITLE_LEN chars, max 60)"
fi
if [ "$TITLE_LEN" -lt 30 ]; then
  echo "⚠️  Title is too short ($TITLE_LEN chars, min 30)"
fi

# Meta description length (150-160 chars)
META_LEN=$(echo "$RESULT" | jq -r '.meta_description | length')
if [ "$META_LEN" -gt 160 ]; then
  echo "⚠️  Meta description too long ($META_LEN chars)"
fi

# Check for missing alt text on images
MISSING_ALT=$(echo "$RESULT" | jq -r '.images.missing_alt')
if [ "$MISSING_ALT" -gt 0 ]; then
  echo "⚠️  $MISSING_ALT images missing alt text"
fi

# Check Open Graph tags
OG_TITLE=$(echo "$RESULT" | jq -r '.og.title // empty')
if [ -z "$OG_TITLE" ]; then
  echo "❌ Missing og:title — social shares will look broken"
fi

# Check canonical
CANONICAL=$(echo "$RESULT" | jq -r '.canonical // empty')
if [ -z "$CANONICAL" ]; then
  echo "⚠️  No canonical URL set"
fi

echo "✅ Detailed SEO check complete"
```

---

## Step 4: Integrate with Vercel/Netlify Preview URLs

If you use Vercel, grab the preview URL from the deployment and check it before merging:

```yaml
jobs:
  seo-audit:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Get Vercel Preview URL
        id: vercel
        run: |
          # Use Vercel CLI or API to get preview URL
          PREVIEW_URL=$(vercel --token ${{ secrets.VERCEL_TOKEN }} inspect --json | jq -r '.url')
          echo "url=$PREVIEW_URL" >> $GITHUB_OUTPUT

      - name: SEO check on preview
        run: ./scripts/seo-check.sh "${{ steps.vercel.outputs.url }}" 70
```

---

## What This Catches

Real examples of SEO issues this pipeline would have caught:

| Issue | Impact | Detected By |
|-------|--------|-------------|
| Missing `<h1>` after component refactor | Google can't identify page topic | H1 count check |
| Title tag > 60 chars | Truncated in search results | Title length check |
| `noindex` left from staging | Page deindexed entirely | Robots meta check |
| Missing Open Graph image | Blank social preview cards | OG tag check |
| 0 internal links on new page | Orphaned page, poor crawlability | Link count check |
| Missing alt text on hero image | Accessibility + image SEO loss | Image alt check |

---

## Cost: $0

The SEO Analyzer API has a **free tier** with 20 requests per minute. For CI/CD checks running on deploy, this is more than enough.

If you need higher limits (monitoring hundreds of pages), paid plans start at **$5.99/month** on [RapidAPI](https://rapidapi.com/miccho27-5OJaGGbBiO/api/seo-analyzer-api/pricing).

---

## Compared to Alternatives

| Tool | Setup Time | Cold Start | Cost | CI-Friendly |
|------|-----------|------------|------|-------------|
| Lighthouse CI | 30+ min | Puppeteer boot | Free | Needs Chrome |
| Ahrefs API | N/A | None | $99+/mo | Yes |
| Screaming Frog | Manual | Desktop app | $259/yr | No |
| **SEO Analyzer API** | **5 min** | **None** | **Free** | **Yes** |

No headless browser. No Chrome installation in CI. No Puppeteer dependency hell. Just `curl` and `jq`.

---

## TL;DR

1. Create `scripts/seo-check.sh` (copy from above)
2. Add a GitHub Actions step that runs it post-deploy
3. Set your minimum score threshold
4. Never ship an SEO regression again

**[SEO Analyzer API on RapidAPI →](https://rapidapi.com/miccho27-5OJaGGbBiO/api/seo-analyzer-api)**

---

*Questions? Hit me in the comments. If this saved you time, a ❤️ helps others find it.*
