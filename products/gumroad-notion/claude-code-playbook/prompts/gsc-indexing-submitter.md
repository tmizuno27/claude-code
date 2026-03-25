# GSC Indexing API Submitter Prompt

## Objective
Submit new or updated pages to Google's Indexing API for faster crawling and indexing.

## Required Context / Inputs
- Google service account with Indexing API access (`config/service-account.json`)
- List of URLs to submit (or auto-detect from recent changes)

## Prompt

```
Submit pages to Google Indexing API for faster indexing.

**Configuration:**
- Service account: config/service-account.json
- Sites: [LIST SITES or "all sites in sites/ directory"]

**Steps:**

1. **Identify pages to submit:**
   Option A: Submit specific URLs: [LIST URLS]
   Option B: Auto-detect — find all pages published or updated in the last [N] days
   Option C: Read from inputs/indexing-queue.csv

2. **Pre-submission checks:**
   - Verify each URL returns 200 status
   - Verify page is not noindexed
   - Verify page is in sitemap.xml
   - Skip pages already submitted in the last 48 hours (check logs)

3. **Submit via Indexing API:**
   - Use URL_UPDATED type for existing pages
   - Use URL_UPDATED type for new pages (Google treats both the same)
   - Respect quota: 200 submissions per day per property
   - Add 1-second delay between submissions

4. **Log results:**
   - Save to logs/indexing-submissions-[date].csv
   - Columns: url, submission_time, status, response_code, error_message
   - Summary: submitted, succeeded, failed, skipped

**Output:**
- logs/indexing-submissions-[date].csv
- Console summary

Mode: [auto-detect / specific-urls / queue-file]
Days lookback (for auto-detect): [N]
```

## Expected Output
- Submission log CSV
- Console summary with success/failure counts

## Tips
- The Indexing API gets pages crawled within hours instead of days
- Quota is 200/day per property — prioritize new and recently updated pages
- Not a guarantee of indexing — the page still needs to meet quality thresholds
- Run daily as part of your SEO automation stack
