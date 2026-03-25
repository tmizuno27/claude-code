# Affiliate Link Auditor Prompt

## Objective
Audit all affiliate links across your site(s) — checking for broken links, expired programs, missing opportunities, and suboptimal placement.

## Required Context / Inputs
- `config/affiliate-links.json` — your affiliate link database
- WordPress REST API credentials
- Published articles list

## Prompt

```
Audit all affiliate links across my site(s).

**Sites to audit:** [LIST SITES or "all sites in sites/ directory"]
**Affiliate config:** config/affiliate-links.json

**Audit Steps:**

1. **Link Inventory**:
   - Fetch all published posts via WordPress REST API
   - Extract every outbound link from every post
   - Classify: internal link, affiliate link, external reference
   - Map: which articles contain which affiliate links

2. **Health Check**:
   - Test each unique affiliate URL (HTTP HEAD request)
   - Flag: 404 errors, redirect chains, timeout, domain expired
   - Check for affiliate links in config that are NOT used in any article

3. **Coverage Analysis**:
   - For each article, check if relevant affiliate links are present
   - Cross-reference article topic with affiliate program categories
   - Identify high-traffic pages with no affiliate links (revenue leaks)
   - Identify pages with too many affiliate links (>5 per article)

4. **Performance Data** (if available):
   - Cross-reference with affiliate dashboard data
   - Identify highest and lowest performing links
   - Suggest replacements for underperforming links

5. **Recommendations**:
   - Broken links to fix immediately
   - New affiliate link insertions (article + link + suggested anchor text)
   - Programs to drop (not relevant or not converting)
   - New programs to apply for (based on content coverage)

**Output:**
- outputs/audits/affiliate-audit-[date].md — full report
- outputs/audits/affiliate-actions-[date].csv — actionable fixes
- Console summary: total links audited, broken, missing opportunities

Sites: [YOUR SITES]
```

## Expected Output
- Full audit report and actionable CSV
- Console summary with severity counts

## Tips
- Run monthly to catch broken links before they cost you commissions
- High-traffic pages without affiliate links are your biggest revenue leaks
- Prioritize fixing broken links (immediate revenue loss) over adding new ones
