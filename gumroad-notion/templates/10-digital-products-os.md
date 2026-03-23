# 10 — Digital Products OS

**Template Name (EN):** Digital Products OS — Build, Launch & Scale
**Template Name (JP):** デジタルプロダクトOS
**Price:** $19
**Target Audience:** Digital product creators, online business owners, course creators, template sellers, e-book authors

---

## Page Structure

```
Digital Products OS (Top Page)
├── Dashboard
├── Products
│   └── Products DB (linked)
├── Sales & Revenue
│   └── Sales DB (linked)
├── Customers
│   └── Customers DB (linked)
├── Marketing
│   ├── Campaigns DB (linked)
│   └── Funnels DB (linked)
├── Launch Planner
│   └── Launches DB (linked)
├── Platforms
│   └── Platforms DB (linked)
├── Tasks
│   └── Tasks DB (linked)
└── Ideas Lab
    └── Ideas DB (linked)
```

---

## Database Schemas

### DB1: Products

| Property | Type | Details |
|----------|------|---------|
| Product Name | Title | — |
| Type | Select | `Template`, `E-book`, `Course`, `Printable`, `Plugin/Extension`, `SaaS`, `Membership`, `Workshop`, `Preset/Filter`, `Other` |
| Status | Select | `Idea`, `Building`, `Beta`, `Live`, `Retired`, `Paused` |
| Price | Number (USD) | — |
| Cost to Create | Number (USD) | — |
| Platform | Relation | → Platforms DB |
| Launch Date | Date | — |
| URL | URL | — |
| Sales | Relation | → Sales DB |
| Total Units | Rollup | Count of related Sales |
| Total Revenue | Rollup | Sum of Amount from related Sales |
| Profit | Formula | `prop("Total Revenue") - prop("Cost to Create")` |
| ROI | Formula | `if(prop("Cost to Create") > 0, round(prop("Profit") / prop("Cost to Create") * 100), 0)` |
| Rating | Number | average customer rating |
| Reviews Count | Number | — |
| Description | Rich Text | — |
| Thumbnail | Files & Media | — |
| Launches | Relation | → Launches DB |
| Tasks | Relation | → Tasks DB |
| Notes | Rich Text | — |

**Views:**
1. **All Products** (Table)
2. **By Status** (Board) — grouped by Status
3. **Live Products** (Gallery) — filtered: Status = Live, show Thumbnail
4. **Revenue Ranking** (Table) — sorted by Total Revenue desc
5. **By Type** (Table) — grouped by Type
6. **P&L** (Table) — showing Product, Revenue, Cost, Profit, ROI

---

### DB2: Sales

| Property | Type | Details |
|----------|------|---------|
| Sale ID | Title | auto or manual |
| Product | Relation | → Products DB |
| Customer | Relation | → Customers DB |
| Amount | Number (USD) | — |
| Platform Fee | Number (USD) | — |
| Net Revenue | Formula | `prop("Amount") - prop("Platform Fee")` |
| Date | Date | — |
| Platform | Relation | → Platforms DB |
| Coupon Used | Rich Text | — |
| Refunded | Checkbox | — |
| Notes | Rich Text | — |

**Views:**
1. **All Sales** (Table) — sorted by Date desc
2. **By Product** (Table) — grouped by Product
3. **Monthly** (Table) — grouped by month
4. **By Platform** (Table) — grouped by Platform
5. **Refunds** (Table) — filtered: Refunded = true
6. **This Month** (Table) — filtered: Date within this month

---

### DB3: Customers

| Property | Type | Details |
|----------|------|---------|
| Name/Email | Title | — |
| Email | Email | — |
| Source | Select | `Organic`, `Social Media`, `Referral`, `Ads`, `Email List`, `Affiliate`, `Other` |
| First Purchase | Date | — |
| Purchases | Relation | → Sales DB |
| Total Spent | Rollup | Sum of Amount from Sales |
| Purchase Count | Rollup | Count of Sales |
| Customer Type | Formula | `if(prop("Purchase Count") > 2, "🏆 VIP", if(prop("Purchase Count") > 1, "🔄 Repeat", "🆕 New"))` |
| Tags | Multi-select | — |
| Notes | Rich Text | — |
| Testimonial | Rich Text | — |

**Views:**
1. **All Customers** (Table)
2. **VIP** (Table) — filtered: Purchase Count > 2
3. **By Source** (Table) — grouped by Source
4. **Recent** (Table) — sorted by First Purchase desc
5. **Testimonials** (Table) — filtered: Testimonial is not empty

---

### DB4: Campaigns

| Property | Type | Details |
|----------|------|---------|
| Campaign | Title | — |
| Type | Select | `Email`, `Social Media`, `Ads`, `Content Marketing`, `Collaboration`, `Affiliate`, `SEO` |
| Status | Select | `Planning`, `Active`, `Completed`, `Paused` |
| Product | Relation | → Products DB |
| Platform | Rich Text | — |
| Budget | Number (USD) | — |
| Spend | Number (USD) | — |
| Revenue Generated | Number (USD) | — |
| ROAS | Formula | `if(prop("Spend") > 0, round(prop("Revenue Generated") / prop("Spend") * 100) / 100, 0)` |
| Start Date | Date | — |
| End Date | Date | — |
| Clicks | Number | — |
| Conversions | Number | — |
| Conversion Rate | Formula | `if(prop("Clicks") > 0, round(prop("Conversions") / prop("Clicks") * 10000) / 100, 0)` |
| Notes | Rich Text | — |

**Views:**
1. **All Campaigns** (Table)
2. **Active** (Table) — filtered: Status = Active
3. **By Type** (Board) — grouped by Type
4. **Performance** (Table) — sorted by ROAS desc

---

### DB5: Funnels

| Property | Type | Details |
|----------|------|---------|
| Funnel Name | Title | — |
| Product | Relation | → Products DB |
| Status | Select | `Draft`, `Active`, `Optimizing`, `Paused` |
| Type | Select | `Free → Paid`, `Low → High Ticket`, `Webinar`, `Email Sequence`, `Social → Landing Page` |
| Steps | Rich Text | describe each step |
| Landing Page URL | URL | — |
| Opt-in Rate | Number (%) | — |
| Conversion Rate | Number (%) | — |
| Revenue | Number (USD) | — |
| Notes | Rich Text | — |

**Views:**
1. **All Funnels** (Table)
2. **Active** (Table) — filtered: Status = Active
3. **By Type** (Board) — grouped by Type

---

### DB6: Launches

| Property | Type | Details |
|----------|------|---------|
| Launch Name | Title | — |
| Product | Relation | → Products DB |
| Status | Select | `Planning`, `Pre-launch`, `Live`, `Completed` |
| Launch Date | Date | — |
| End Date | Date | — |
| Goal (units) | Number | — |
| Goal (revenue) | Number (USD) | — |
| Actual Units | Number | — |
| Actual Revenue | Number (USD) | — |
| Achievement | Formula | `if(prop("Goal (revenue)") > 0, round(prop("Actual Revenue") / prop("Goal (revenue)") * 100), 0)` |
| Channels | Multi-select | `Email`, `Twitter/X`, `Instagram`, `LinkedIn`, `Product Hunt`, `Reddit`, `Ads`, `Affiliates` |
| Pre-launch Checklist | Rich Text | — |
| Launch Day Checklist | Rich Text | — |
| Post-launch Review | Rich Text | — |
| Notes | Rich Text | — |

**Views:**
1. **All Launches** (Table)
2. **Timeline** (Timeline) — by Launch Date → End Date
3. **Upcoming** (Table) — filtered: Status = Planning or Pre-launch
4. **Results** (Table) — filtered: Status = Completed, showing goals vs actuals

---

### DB7: Platforms

| Property | Type | Details |
|----------|------|---------|
| Platform | Title | — |
| Type | Select | `Marketplace`, `Own Website`, `Course Platform`, `Membership` |
| URL | URL | — |
| Fee Structure | Rich Text | — |
| Fee Percentage | Number (%) | — |
| Products | Relation | → Products DB |
| Sales | Relation | → Sales DB |
| Total Revenue | Rollup | Sum of Amount from Sales |
| Username | Rich Text | — |
| Notes | Rich Text | — |

Pre-filled: `Gumroad`, `Etsy`, `Amazon KDP`, `Udemy`, `Shopify`, `Lemonsqueezy`, `Own Website`

**Views:**
1. **All Platforms** (Table)
2. **By Revenue** (Table) — sorted by Total Revenue desc

---

### DB8: Tasks

| Property | Type | Details |
|----------|------|---------|
| Task | Title | — |
| Product | Relation | → Products DB |
| Launch | Relation | → Launches DB |
| Status | Select | `To Do`, `In Progress`, `Done` |
| Priority | Select | `🔴 High`, `🟡 Medium`, `🟢 Low` |
| Due Date | Date | — |
| Category | Select | `Creation`, `Design`, `Marketing`, `Listing`, `Customer Support`, `Optimization`, `Admin` |
| Notes | Rich Text | — |

**Views:**
1. **All Tasks** (Table)
2. **Kanban** (Board) — grouped by Status
3. **By Product** (Table) — grouped by Product
4. **This Week** (Table) — filtered: Due within this week

---

### DB9: Ideas

| Property | Type | Details |
|----------|------|---------|
| Idea | Title | — |
| Type | Select | `New Product`, `Improvement`, `Bundle`, `Upsell`, `Cross-sell`, `Marketing` |
| Status | Select | `Raw`, `Researching`, `Validated`, `Building`, `Discarded` |
| Market Size | Select | `🔥 Large`, `👍 Medium`, `🤔 Small` |
| Effort | Select | `Low`, `Medium`, `High` |
| Priority Score | Formula | Conceptual: market_size / effort |
| Validation Notes | Rich Text | — |
| Competitor Links | Rich Text | — |
| Notes | Rich Text | — |
| Created | Created time | — |

**Views:**
1. **All Ideas** (Table)
2. **By Status** (Board) — grouped by Status
3. **Top Opportunities** (Table) — sorted by Market Size desc, Effort asc

---

## Dashboard Page Layout

1. **Header**: "Digital Products HQ"
2. **Revenue Overview** — Callout: This Month / Last Month / All Time (manual or linked views)
3. **Live Products** — Products DB, Gallery (Status = Live)
4. **Sales This Month** — Sales DB, this month (Table, 10)
5. **Active Campaigns** — Campaigns DB, filtered: Active (Table)
6. **Upcoming Launches** — Launches DB, filtered: Planning/Pre-launch (Table)
7. **Tasks This Week** — Tasks DB, filtered: this week (Table)
8. **Top Products** — Products DB, sorted by Total Revenue desc (Table, 3)
9. **Quick Add** — links to add Sale, Task, Idea

---

## Pre-filled Sample Data

- 3 sample products (Template - Live, E-book - Building, Course - Idea)
- 10 sample sales
- 5 sample customers
- 2 sample campaigns
- 1 sample funnel
- 1 sample launch (completed with results)
- 7 sample platforms
- 5 tasks, 4 ideas

---

## Setup Instructions for Buyer

1. Duplicate to workspace
2. Add your selling platforms with fee structures
3. Add existing products with details and links
4. Log sales as they come in (or weekly batch)
5. Plan your next launch using the Launch Planner
6. Track marketing campaigns and their ROI
7. Use the Ideas Lab for new product brainstorming
8. Review Dashboard weekly for business overview
