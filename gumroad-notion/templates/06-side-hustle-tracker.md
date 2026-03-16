# 06 — Side Hustle Tracker

**Template Name (EN):** Side Hustle Tracker
**Template Name (JP):** 副業トラッカー
**Price:** $12
**Target Audience:** People with side hustles, aspiring entrepreneurs, 9-to-5 workers building something on the side

---

## Page Structure

```
Side Hustle Tracker (Top Page)
├── Dashboard
├── Hustles
│   └── Hustles DB (linked)
├── Income & Expenses
│   ├── Income DB (linked)
│   └── Expenses DB (linked)
├── Tasks & Milestones
│   ├── Tasks DB (linked)
│   └── Milestones DB (linked)
├── Time Tracker
│   └── Time DB (linked)
├── Ideas Backlog
│   └── Ideas DB (linked)
└── Resources & Learning
    └── Resources DB (linked)
```

---

## Database Schemas

### DB1: Hustles

| Property | Type | Details |
|----------|------|---------|
| Hustle Name | Title | — |
| Type | Select | `Freelance`, `E-commerce`, `Digital Products`, `Content Creation`, `Consulting`, `Affiliate`, `SaaS`, `Other` |
| Status | Select | `Idea`, `Validating`, `Launching`, `Active`, `Scaling`, `Paused`, `Retired` |
| Started | Date | — |
| Monthly Revenue | Rollup | Sum of Amount from Income (this month) |
| Monthly Expenses | Rollup | Sum of Amount from Expenses (this month) |
| Total Revenue | Rollup | Sum of all Income |
| Total Expenses | Rollup | Sum of all Expenses |
| Net Profit | Formula | `prop("Total Revenue") - prop("Total Expenses")` |
| Hours This Month | Rollup | Sum of Hours from Time DB (this month) |
| Hourly Rate Effective | Formula | `if(prop("Hours This Month") > 0, round(prop("Monthly Revenue") / prop("Hours This Month") * 100) / 100, 0)` |
| Income | Relation | → Income DB |
| Expenses | Relation | → Expenses DB |
| Tasks | Relation | → Tasks DB |
| Milestones | Relation | → Milestones DB |
| Time Logs | Relation | → Time DB |
| Website | URL | — |
| Notes | Rich Text | — |

**Views:**
1. **All Hustles** (Table)
2. **Active** (Table) — filtered: Status = Active or Scaling
3. **By Status** (Board) — grouped by Status
4. **Profitability** (Table) — sorted by Net Profit desc

---

### DB2: Income

| Property | Type | Details |
|----------|------|---------|
| Description | Title | — |
| Hustle | Relation | → Hustles DB |
| Amount | Number (USD) | — |
| Date | Date | — |
| Source | Select | `Client Payment`, `Product Sale`, `Ad Revenue`, `Affiliate`, `Tips`, `Subscription`, `Other` |
| Recurring | Checkbox | — |
| Platform | Select | `Direct`, `Gumroad`, `Etsy`, `Amazon`, `Fiverr`, `Upwork`, `Stripe`, `PayPal`, `Other` |
| Notes | Rich Text | — |

**Views:**
1. **All Income** (Table) — sorted by Date desc
2. **By Hustle** (Table) — grouped by Hustle
3. **Monthly** (Table) — grouped by month
4. **By Source** (Table) — grouped by Source

---

### DB3: Expenses

| Property | Type | Details |
|----------|------|---------|
| Description | Title | — |
| Hustle | Relation | → Hustles DB |
| Amount | Number (USD) | — |
| Date | Date | — |
| Category | Select | `Software/Tools`, `Marketing`, `Inventory`, `Hosting`, `Design`, `Education`, `Legal`, `Tax`, `Other` |
| Recurring | Checkbox | — |
| Tax Deductible | Checkbox | — |
| Receipt | Files & Media | — |
| Notes | Rich Text | — |

**Views:**
1. **All Expenses** (Table) — sorted by Date desc
2. **By Hustle** (Table) — grouped by Hustle
3. **Monthly** (Table) — grouped by month
4. **By Category** (Table) — grouped by Category
5. **Tax Deductible** (Table) — filtered: Tax Deductible = true

---

### DB4: Tasks

| Property | Type | Details |
|----------|------|---------|
| Task | Title | — |
| Hustle | Relation | → Hustles DB |
| Status | Select | `To Do`, `In Progress`, `Waiting`, `Done` |
| Priority | Select | `🔴 High`, `🟡 Medium`, `🟢 Low` |
| Due Date | Date | — |
| Time Estimate | Select | `15 min`, `30 min`, `1 hr`, `2 hr`, `Half day`, `Full day` |
| Milestone | Relation | → Milestones DB |
| Notes | Rich Text | — |

**Views:**
1. **All Tasks** (Table) — sorted by Due Date
2. **Kanban** (Board) — grouped by Status
3. **By Hustle** (Table) — grouped by Hustle
4. **This Week** (Table) — filtered: Due within this week
5. **Quick Wins** (Table) — filtered: Time Estimate = 15 min or 30 min

---

### DB5: Milestones

| Property | Type | Details |
|----------|------|---------|
| Milestone | Title | — |
| Hustle | Relation | → Hustles DB |
| Target Date | Date | — |
| Status | Select | `Upcoming`, `In Progress`, `Achieved`, `Missed` |
| Type | Select | `Revenue`, `Launch`, `Growth`, `Product`, `Other` |
| Target Value | Rich Text | e.g. "$1,000 MRR" |
| Tasks | Relation | → Tasks DB |
| Notes | Rich Text | — |

**Views:**
1. **All Milestones** (Table) — sorted by Target Date
2. **By Hustle** (Table) — grouped by Hustle
3. **Timeline** (Timeline) — by Target Date
4. **Achieved** (Table) — filtered: Status = Achieved

---

### DB6: Time

| Property | Type | Details |
|----------|------|---------|
| Description | Title | — |
| Hustle | Relation | → Hustles DB |
| Date | Date | — |
| Hours | Number | — |
| Type | Select | `Building`, `Marketing`, `Admin`, `Learning`, `Client Work`, `Planning` |
| Notes | Rich Text | — |

**Views:**
1. **All Logs** (Table) — sorted by Date desc
2. **This Week** (Table) — filtered: this week
3. **By Hustle** (Table) — grouped by Hustle
4. **By Type** (Table) — grouped by Type

---

### DB7: Ideas

| Property | Type | Details |
|----------|------|---------|
| Idea | Title | — |
| Type | Select | `New Hustle`, `Feature`, `Marketing`, `Product`, `Improvement` |
| Status | Select | `Raw`, `Researching`, `Validated`, `Building`, `Discarded` |
| Potential Revenue | Select | `$`, `$$`, `$$$`, `$$$$` |
| Effort | Select | `Low`, `Medium`, `High` |
| Score | Formula | Based on revenue/effort |
| Notes | Rich Text | — |
| Created | Created time | — |

**Views:**
1. **All Ideas** (Table)
2. **By Status** (Board) — grouped by Status
3. **Best Opportunities** (Table) — sorted by Potential Revenue desc, Effort asc

---

### DB8: Resources

| Property | Type | Details |
|----------|------|---------|
| Resource | Title | — |
| Type | Select | `Tool`, `Course`, `Book`, `Article`, `Community`, `Template` |
| Category | Select | `Marketing`, `Finance`, `Productivity`, `Technical`, `Legal`, `Mindset` |
| URL | URL | — |
| Cost | Number (USD) | — |
| Rating | Select | `⭐⭐⭐⭐⭐`, `⭐⭐⭐⭐`, `⭐⭐⭐`, `⭐⭐`, `⭐` |
| Notes | Rich Text | — |

**Views:**
1. **All Resources** (Table)
2. **By Type** (Board) — grouped by Type
3. **Free** (Table) — filtered: Cost = 0

---

## Dashboard Page Layout

1. **Header**: "Side Hustle Command Center"
2. **Hustle Overview** — Hustles DB showing Name, Status, Net Profit, Effective Hourly Rate (Table)
3. **This Month's Numbers** — Callout: Total Income / Total Expenses / Net Profit (manual or linked views)
4. **This Week's Tasks** — Tasks DB, filtered: this week, Status != Done (Table)
5. **Active Milestones** — Milestones DB, filtered: Status = In Progress (Table, 3 items)
6. **Time This Week** — Time DB, filtered: this week (Table)
7. **Top Ideas** — Ideas DB, filtered: Status = Validated (Table, 3 items)
8. **Monthly Goal** — Callout with revenue target and progress

---

## Pre-filled Sample Data

- 2 sample hustles (Freelance Writing - Active, Print on Demand - Launching)
- 5 income entries, 4 expense entries
- 6 tasks, 3 milestones
- 4 time log entries
- 5 ideas
- 3 resources

---

## Setup Instructions for Buyer

1. Duplicate to workspace
2. Add your current side hustles with status and details
3. Set up milestones for each hustle (next 3-6 months)
4. Log income and expenses as they occur
5. Track time daily (even 15-minute blocks count)
6. Review Dashboard weekly
7. Do monthly P&L review per hustle
