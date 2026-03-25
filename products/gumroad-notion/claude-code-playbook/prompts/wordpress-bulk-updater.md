# WordPress Bulk Updater Prompt

## Objective
Perform bulk updates across all WordPress posts — meta descriptions, titles, affiliate links, formatting, or any repeating change.

## Required Context / Inputs
- WordPress REST API credentials in `config/secrets.json`
- The type of update you want to apply

## Prompt

```
Perform a bulk update across all posts on my WordPress site.

**Site:** [YOUR SITE URL]
**Credentials:** Read from config/secrets.json

**Update Type:** [Choose one or combine]

A) **Meta Title Optimization**:
   - Fetch all posts
   - For each post, analyze the current title
   - If CTR data is available (inputs/gsc-data.csv), prioritize low-CTR posts
   - Generate an improved title that: includes the primary keyword, uses a power word, stays under 60 characters
   - Output a before/after comparison for review

B) **Affiliate Link Insertion**:
   - Read config/affiliate-links.json for available programs
   - Fetch all posts
   - For each post, identify contextually relevant affiliate link opportunities
   - Insert links with appropriate anchor text
   - Never insert more than 3 affiliate links per article
   - Log all insertions

C) **Formatting Standardization**:
   - Ensure all posts have: a meta description, proper H2/H3 structure, alt text on images, at least 2 internal links
   - Fix common issues: orphan paragraphs, missing closing tags, broken HTML
   - Add a table of contents if the article has 4+ H2 headings

D) **Custom Update**: [DESCRIBE YOUR UPDATE]

**Safety:**
- Mode: [dry-run / apply]
- In dry-run mode, generate the changes but don't push them
- In apply mode, push changes and log every modification
- Always create a backup log before applying

**Output:**
- Save change report to outputs/bulk-update-[type]-[date].csv
- Columns: post_id, post_title, change_type, before, after, status
- Console summary: total posts processed, changes made, errors

Mode: [dry-run / apply]
Update type: [A / B / C / D]
```

## Expected Output
- `outputs/bulk-update-[type]-[date].csv` — change log
- Console summary

## Tips
- Always run dry-run first and review before applying
- Process in batches of 10 posts with 1-second delays to respect rate limits
- Keep the backup log — you may need to revert changes
