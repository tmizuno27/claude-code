# Site Audit Prompt

## Objective
Perform a comprehensive technical and content audit of a website, identifying SEO issues, broken links, performance problems, and content quality gaps.

## Required Context / Inputs
- WordPress REST API credentials in `config/secrets.json`
- Site URL
- Google Search Console data (optional but recommended)

## Prompt

```
Run a full site audit on [YOUR SITE].

**Audit Scope:**
- Site URL: [YOUR SITE URL]
- CMS: [WordPress / Next.js / static]
- Access method: [WordPress REST API via config/secrets.json / sitemap crawl / local files]

**Audit Checklist:**

1. **Technical SEO**:
   - Fetch and analyze robots.txt — any critical pages blocked?
   - Fetch and analyze sitemap.xml — are all published pages included?
   - Check for pages with noindex that should be indexed (and vice versa)
   - Identify pages returning 404 errors
   - Check for redirect chains (301 → 301 → 200)
   - Verify canonical URLs are set correctly
   - Check for duplicate title tags and meta descriptions
   - Verify structured data / schema markup presence

2. **Content Quality**:
   - Fetch all published pages via REST API
   - Flag thin content (under 800 words)
   - Flag pages with no internal links
   - Flag pages with no external links
   - Flag pages with no images
   - Flag pages with missing alt text on images
   - Identify content that is over 12 months old and may need refreshing
   - Check for broken internal links

3. **Performance Indicators**:
   - Identify pages with excessive images (>10)
   - Check for missing lazy loading attributes
   - Flag oversized images (if detectable via API)
   - Identify pages with excessive plugins/scripts (WordPress)

4. **Monetization Check**:
   - Verify affiliate links are present and working
   - Cross-reference with config/affiliate-links.json
   - Identify high-traffic pages missing affiliate links
   - Check for expired or broken affiliate URLs

5. **Output:**
   - Save full audit report to outputs/audits/site-audit-[site]-[date].md
   - Categorize all findings as: CRITICAL / HIGH / MEDIUM / LOW
   - Include specific fix instructions for each finding
   - Summary table: category, finding_count, top_priority_fix
   - Prioritized action plan (top 10 fixes by impact)

Site: [YOUR SITE]
Audit depth: [quick / standard / deep]
```

## Expected Output
- `outputs/audits/site-audit-[site]-[date].md` — complete audit report
- Console summary with severity counts and top 5 immediate actions

## Example Usage

```
Site: sim-hikaku.online
CMS: WordPress
Access method: WordPress REST API via config/secrets.json
Audit depth: standard
```

## Tips
- Run monthly as part of site maintenance
- Address CRITICAL issues immediately (noindex on important pages, broken affiliate links)
- Thin content should be either expanded or consolidated (merged with related articles)
- Track audit scores over time to measure improvement
