# 05 — Small Business CRM

**Template Name (EN):** Small Business CRM
**Template Name (JP):** スモールビジネスCRM
**Price:** $17
**Target Audience:** Small business owners, startups, solopreneurs managing customer relationships

---

## Page Structure

```
Small Business CRM (Top Page)
├── Dashboard
├── Contacts
│   └── Contacts DB (linked)
├── Companies
│   └── Companies DB (linked)
├── Deals Pipeline
│   └── Deals DB (linked)
├── Activities
│   └── Activities DB (linked)
├── Products & Services
│   └── Products DB (linked)
└── Reports
    └── (linked views with filters)
```

---

## Database Schemas

### DB1: Contacts

| Property | Type | Details |
|----------|------|---------|
| Name | Title | — |
| Company | Relation | → Companies DB |
| Role/Title | Rich Text | — |
| Email | Email | — |
| Phone | Phone | — |
| Type | Select | `Lead`, `Prospect`, `Customer`, `Partner`, `Vendor`, `Other` |
| Status | Select | `Active`, `Inactive`, `Churned` |
| Source | Select | `Website`, `Referral`, `Social Media`, `Cold Outreach`, `Event`, `Ads`, `Other` |
| LinkedIn | URL | — |
| Deals | Relation | → Deals DB |
| Activities | Relation | → Activities DB |
| Tags | Multi-select | user customizes |
| Last Contact | Date | — |
| Next Follow-up | Date | — |
| Lifetime Value | Rollup | Sum of Amount from related Deals (Closed Won only) |
| Notes | Rich Text | — |
| Created | Created time | — |

**Views:**
1. **All Contacts** (Table) — default
2. **By Type** (Board) — grouped by Type
3. **Leads** (Table) — filtered: Type = Lead
4. **Customers** (Table) — filtered: Type = Customer
5. **Follow-up Due** (Table) — filtered: Next Follow-up <= Today, sorted by date
6. **By Company** (Table) — grouped by Company

---

### DB2: Companies

| Property | Type | Details |
|----------|------|---------|
| Company Name | Title | — |
| Industry | Select | `Technology`, `Marketing`, `Finance`, `Retail`, `Healthcare`, `Education`, `Manufacturing`, `Consulting`, `Other` |
| Size | Select | `1-10`, `11-50`, `51-200`, `201-1000`, `1000+` |
| Website | URL | — |
| Address | Rich Text | — |
| Status | Select | `Active`, `Inactive`, `Prospect` |
| Contacts | Relation | → Contacts DB |
| Deals | Relation | → Deals DB |
| Total Revenue | Rollup | Sum of Amount from related Deals (Won) |
| Notes | Rich Text | — |

**Views:**
1. **All Companies** (Table)
2. **By Industry** (Table) — grouped by Industry
3. **Active** (Table) — filtered: Status = Active
4. **Top Revenue** (Table) — sorted by Total Revenue desc

---

### DB3: Deals

| Property | Type | Details |
|----------|------|---------|
| Deal Name | Title | — |
| Contact | Relation | → Contacts DB |
| Company | Relation | → Companies DB |
| Stage | Select | `New Lead`, `Qualified`, `Proposal Sent`, `Negotiation`, `Closed Won`, `Closed Lost` |
| Amount | Number (USD) | — |
| Probability | Number (%) | — |
| Weighted Value | Formula | `prop("Amount") * prop("Probability") / 100` |
| Product | Relation | → Products DB |
| Close Date | Date | — |
| Owner | Person | — |
| Source | Select | `Inbound`, `Outbound`, `Referral`, `Upsell`, `Cross-sell` |
| Lost Reason | Select | `Price`, `Competitor`, `No Budget`, `No Need`, `Timing`, `No Response`, `Other` |
| Activities | Relation | → Activities DB |
| Notes | Rich Text | — |
| Created | Created time | — |
| Days in Pipeline | Formula | `dateBetween(now(), prop("Created"), "days")` |

**Views:**
1. **Pipeline** (Board) — grouped by Stage (primary view)
2. **All Deals** (Table) — sorted by Close Date
3. **Won** (Table) — filtered: Stage = Closed Won
4. **Lost** (Table) — filtered: Stage = Closed Lost
5. **Closing This Month** (Table) — filtered: Close Date within this month
6. **By Owner** (Table) — grouped by Owner
7. **Forecast** (Table) — showing Weighted Value, grouped by month

---

### DB4: Activities

| Property | Type | Details |
|----------|------|---------|
| Activity | Title | — |
| Type | Select | `Call`, `Email`, `Meeting`, `Demo`, `Follow-up`, `Note`, `Task` |
| Contact | Relation | → Contacts DB |
| Deal | Relation | → Deals DB |
| Date | Date | — |
| Status | Select | `Planned`, `Completed`, `Cancelled` |
| Duration (min) | Number | — |
| Outcome | Rich Text | — |
| Next Step | Rich Text | — |
| Notes | Rich Text | — |

**Views:**
1. **All Activities** (Table) — sorted by Date desc
2. **Upcoming** (Table) — filtered: Status = Planned, Date >= Today
3. **By Type** (Board) — grouped by Type
4. **Calendar** (Calendar) — by Date
5. **By Contact** (Table) — grouped by Contact

---

### DB5: Products & Services

| Property | Type | Details |
|----------|------|---------|
| Product/Service | Title | — |
| Category | Select | user customizes |
| Price | Number (USD) | — |
| Type | Select | `One-time`, `Recurring`, `Hourly` |
| Status | Select | `Active`, `Discontinued`, `Coming Soon` |
| Description | Rich Text | — |
| Deals | Relation | → Deals DB |
| Units Sold | Rollup | Count of related Deals (Won) |
| Total Revenue | Rollup | Sum of Amount from related Deals (Won) |

**Views:**
1. **All Products** (Table)
2. **Active** (Table) — filtered: Status = Active
3. **By Revenue** (Table) — sorted by Total Revenue desc

---

## Dashboard Page Layout

1. **Header**: "CRM Dashboard" + date
2. **Pipeline Overview** — Deals DB, Board view (all stages)
3. **Hot Deals** — Deals DB, filtered: Probability >= 70%, Stage != Won/Lost (Table, 5 items)
4. **Today's Activities** — Activities DB, filtered: Date = Today (Table)
5. **Follow-ups Due** — Contacts DB, filtered: Next Follow-up <= Today (Table, 5 items)
6. **Monthly Revenue** — Deals DB, filtered: Stage = Won, Close Date this month (Table)
7. **New Leads This Week** — Contacts DB, filtered: Type = Lead, Created this week (Table)
8. **Quick Add** — Callout with links to add Contact, Deal, Activity

---

## Pre-filled Sample Data

- 6 sample contacts (mix of leads, prospects, customers)
- 3 sample companies
- 5 sample deals across pipeline stages
- 8 sample activities
- 4 sample products/services

---

## Setup Instructions for Buyer

1. Duplicate to your workspace
2. Customize Industry, Source, and other Select options
3. Add your products/services first
4. Import existing contacts (or add manually)
5. Create deals for active opportunities
6. Log every interaction as an Activity
7. Review Pipeline Board daily
8. Set follow-up dates for every contact
