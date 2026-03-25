# Multi-Site Deployer Prompt

## Objective
Apply the same operation (update, fix, optimization) across multiple sites simultaneously, with per-site configuration and consolidated reporting.

## Required Context / Inputs
- List of sites with credentials in their respective `config/` directories
- The operation to perform

## Prompt

```
Execute an operation across all my sites.

**Sites:**
[LIST SITES or "all sites in sites/ directory"]

**Operation:** [Choose one]

A) **Deploy CSS/JS update**: Apply the same theme changes across all sites
B) **Security patch**: Update WordPress plugins or apply security headers
C) **Content sync**: Publish queued articles on all sites
D) **SEO sweep**: Run meta optimization across all sites
E) **Affiliate update**: Insert new affiliate links on all sites
F) **Custom**: [DESCRIBE OPERATION]

**Execution:**
1. Load config for each site from sites/[site]/config/secrets.json
2. Execute the operation on each site
3. Handle per-site errors without stopping other sites
4. Log results per site

**Output:**
- Per-site result log
- Consolidated summary: sites processed, succeeded, failed
- Save to logs/multi-site-[operation]-[date].md

Operation: [A-F]
Details: [SPECIFICS OF THE OPERATION]
```

## Expected Output
- Consolidated log in `logs/multi-site-[operation]-[date].md`
- Console summary

## Tips
- Always test on one site first before deploying to all
- Per-site error handling is critical — one site's failure should not block others
- Use this pattern for any repeating cross-site maintenance
