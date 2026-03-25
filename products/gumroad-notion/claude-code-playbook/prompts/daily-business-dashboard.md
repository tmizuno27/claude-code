# Daily Business Dashboard Prompt

## Objective
Generate a morning briefing that summarizes all business metrics, identifies priority actions, and sets the agenda for the day.

## Required Context / Inputs
- Access to all site analytics (GSC, GA4)
- Task scheduler logs
- Revenue data (affiliate, product sales)

## Prompt

```
Generate my daily business dashboard.

**Data Sources:**
- Site analytics: GSC and GA4 for all sites
- Task logs: logs/ directory (check last 24 hours)
- Article management: outputs/article-management.csv for each site
- Product listings: listings/ directory
- Affiliate config: config/affiliate-links.json

**Dashboard Sections:**

1. **Health Check** (traffic light system):
   - All scheduled tasks: running / failed / stale
   - All sites: up / down / slow
   - API services: responding / errors
   - Git sync: current / behind

2. **Traffic Snapshot** (last 24h vs previous):
   - Total sessions per site
   - Top 3 growing pages
   - Top 3 declining pages
   - New keywords appearing

3. **Revenue Snapshot**:
   - Estimated affiliate earnings (if data available)
   - Product sales (Gumroad, etc.)
   - API usage (RapidAPI)
   - Total estimated daily revenue

4. **Content Pipeline**:
   - Articles in queue
   - Articles published this week
   - Articles scheduled for today

5. **Priority Actions** (top 5):
   - Ranked by revenue impact
   - Each with: action, expected impact, time estimate
   - Mark which ones Claude can auto-execute vs need human action

6. **Alerts**:
   - Anything broken, failing, or significantly declining

**Output:**
- Save to outputs/dashboards/daily-[date].md
- Print executive summary to console
- Flag any CRITICAL issues at the top

Date: [TODAY or auto-detect]
```

## Expected Output
- `outputs/dashboards/daily-[date].md` — full dashboard
- Console executive summary with priority actions

## Tips
- Schedule this to run at 6 AM automatically
- The priority actions should feed directly into your day's work
- Track trends over time, not just daily snapshots
