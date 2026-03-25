# Data Analysis Reporter Prompt

## Objective
Pull data from Google Search Console, GA4, affiliate dashboards, or CSV files and generate an actionable business intelligence report.

## Required Context / Inputs
- Data source (GSC export, GA4 export, CSV files, or API credentials)
- Reporting period
- KPIs you care about

## Prompt

```
Generate a comprehensive analytics report for my business.

**Data Sources:**
- Google Search Console data: [PATH_TO_CSV or "fetch via API using config/secrets.json"]
- GA4 data: [PATH_TO_CSV or "fetch via API"]
- Article management: outputs/article-management.csv
- Affiliate data: [PATH_TO_CSV if available]
- Reporting period: [LAST 7 DAYS / LAST 30 DAYS / CUSTOM DATE RANGE]

**Analysis Required:**

1. **Traffic Overview**:
   - Total sessions, users, pageviews (vs previous period)
   - Traffic by source (organic, direct, social, referral)
   - Top 10 landing pages by traffic
   - Trend direction: growing, stable, or declining

2. **SEO Performance**:
   - Total impressions, clicks, average CTR, average position
   - Top 20 queries by impressions
   - Queries with high impressions but low CTR (title/meta optimization candidates)
   - Queries on page 2 (positions 11-20) — quick win opportunities
   - New queries appearing this period
   - Queries that dropped significantly

3. **Content Performance**:
   - Best performing articles (traffic, engagement, time on page)
   - Worst performing articles (candidates for improvement or deletion)
   - Articles with declining traffic (need refresh)
   - Content gaps (high-traffic queries with no matching article)

4. **Revenue Analysis** (if data available):
   - Total revenue by source (affiliate, ads, products)
   - Revenue per article (top 10)
   - Conversion rates by traffic source
   - Revenue trend vs previous period

5. **Action Items**:
   Generate a prioritized list of 10 specific actions, each with:
   - Action description
   - Expected impact (high/medium/low)
   - Effort required (high/medium/low)
   - Priority score = impact / effort
   - Sort by priority score

**Output:**
- Save full report to outputs/reports/analytics-[date].md
- Save action items to outputs/reports/actions-[date].csv
- Print executive summary (5 bullet points) to console

Reporting period: [DATE RANGE]
Site: [YOUR SITE]
```

## Expected Output
- `outputs/reports/analytics-[date].md` — full report
- `outputs/reports/actions-[date].csv` — prioritized action items
- Console executive summary

## Example Usage

```
Data Sources:
- GSC data: inputs/gsc-export-2026-03.csv
- GA4 data: fetch via API using config/secrets.json
- Reporting period: last 30 days
Site: sim-hikaku.online
```

## Tips
- Schedule this weekly (Sunday evening) so you start Monday with clear priorities
- Compare month-over-month, not just week-over-week, for trend accuracy
- Action items should be specific ("Rewrite meta title for article X to improve CTR") not vague ("Improve SEO")
