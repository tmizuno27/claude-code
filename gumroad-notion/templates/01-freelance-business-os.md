# 01 — Freelance Business OS

**Template Name (EN):** Freelance Business OS
**Template Name (JP):** フリーランス事業管理OS
**Price:** $19
**Target Audience:** Freelancers, solopreneurs, independent contractors, consultants

---

## Page Structure

```
Freelance Business OS (Top Page)
├── Dashboard (home page with linked views)
├── Clients & Projects
│   ├── Clients DB (linked)
│   └── Projects DB (linked)
├── Tasks & Time
│   ├── Tasks DB (linked)
│   └── Time Log DB (linked)
├── Finances
│   ├── Invoices DB (linked)
│   └── Expenses DB (linked)
├── Proposals & Contracts
│   └── Proposals DB (linked)
└── Resources & Notes
    └── Notes DB (linked)
```

---

## Database Schemas

### DB1: Clients

| Property | Type | Details |
|----------|------|---------|
| Client Name | Title | — |
| Status | Select | `Active`, `Prospect`, `Past`, `Paused` |
| Industry | Select | `Tech`, `Marketing`, `Finance`, `E-commerce`, `Education`, `Healthcare`, `Other` |
| Contact Person | Rich Text | — |
| Email | Email | — |
| Phone | Phone | — |
| Website | URL | — |
| Source | Select | `Referral`, `Upwork`, `Fiverr`, `Cold Outreach`, `Inbound`, `Social Media`, `Other` |
| Monthly Retainer | Number (USD) | — |
| Total Revenue | Rollup | Sum of `Amount` from related Invoices |
| Projects | Relation | → Projects DB |
| Invoices | Relation | → Invoices DB |
| Notes | Rich Text | — |
| Start Date | Date | — |
| Rating | Select | `⭐`, `⭐⭐`, `⭐⭐⭐`, `⭐⭐⭐⭐`, `⭐⭐⭐⭐⭐` |

**Views:**
1. **All Clients** (Table) — default, sorted by Status
2. **By Status** (Board/Kanban) — grouped by Status
3. **Active Only** (Table) — filtered: Status = Active
4. **Revenue Ranking** (Table) — sorted by Total Revenue desc

---

### DB2: Projects

| Property | Type | Details |
|----------|------|---------|
| Project Name | Title | — |
| Client | Relation | → Clients DB |
| Status | Select | `Not Started`, `In Progress`, `On Hold`, `Completed`, `Cancelled` |
| Priority | Select | `🔴 High`, `🟡 Medium`, `🟢 Low` |
| Type | Select | `One-time`, `Retainer`, `Hourly` |
| Start Date | Date | — |
| Deadline | Date | — |
| Budget | Number (USD) | — |
| Hours Estimated | Number | — |
| Hours Actual | Rollup | Sum of `Hours` from related Time Logs |
| Progress | Formula | `round(prop("Hours Actual") / prop("Hours Estimated") * 100)` |
| Tasks | Relation | → Tasks DB |
| Time Logs | Relation | → Time Log DB |
| Invoices | Relation | → Invoices DB |
| Deliverables | Rich Text | — |
| Notes | Rich Text | — |

**Views:**
1. **All Projects** (Table) — default
2. **Kanban** (Board) — grouped by Status
3. **Timeline** (Timeline/Gantt) — by Start Date → Deadline
4. **By Client** (Table) — grouped by Client
5. **Active** (Table) — filtered: Status = In Progress

---

### DB3: Tasks

| Property | Type | Details |
|----------|------|---------|
| Task | Title | — |
| Project | Relation | → Projects DB |
| Status | Select | `To Do`, `In Progress`, `Waiting`, `Done` |
| Priority | Select | `🔴 High`, `🟡 Medium`, `🟢 Low` |
| Due Date | Date | — |
| Assignee | Person | — |
| Estimated Hours | Number | — |
| Tags | Multi-select | `Design`, `Development`, `Writing`, `Research`, `Admin`, `Meeting`, `Review` |
| Notes | Rich Text | — |

**Views:**
1. **All Tasks** (Table) — sorted by Due Date
2. **Kanban** (Board) — grouped by Status
3. **Today** (Table) — filtered: Due Date = Today
4. **This Week** (Table) — filtered: Due Date within this week
5. **By Project** (Table) — grouped by Project

---

### DB4: Time Log

| Property | Type | Details |
|----------|------|---------|
| Description | Title | — |
| Project | Relation | → Projects DB |
| Date | Date | — |
| Hours | Number | decimal, e.g. 1.5 |
| Hourly Rate | Number (USD) | — |
| Earnings | Formula | `prop("Hours") * prop("Hourly Rate")` |
| Billable | Checkbox | — |
| Task | Relation | → Tasks DB |

**Views:**
1. **All Logs** (Table) — sorted by Date desc
2. **This Week** (Table) — filtered: Date within this week
3. **By Project** (Table) — grouped by Project
4. **Billable Only** (Table) — filtered: Billable = true
5. **Calendar** (Calendar) — by Date

---

### DB5: Invoices

| Property | Type | Details |
|----------|------|---------|
| Invoice # | Title | e.g. INV-001 |
| Client | Relation | → Clients DB |
| Project | Relation | → Projects DB |
| Status | Select | `Draft`, `Sent`, `Paid`, `Overdue`, `Cancelled` |
| Issue Date | Date | — |
| Due Date | Date | — |
| Amount | Number (USD) | — |
| Tax | Number (USD) | — |
| Total | Formula | `prop("Amount") + prop("Tax")` |
| Payment Method | Select | `Bank Transfer`, `PayPal`, `Wise`, `Stripe`, `Cash`, `Other` |
| Paid Date | Date | — |
| Notes | Rich Text | — |

**Views:**
1. **All Invoices** (Table) — sorted by Issue Date desc
2. **By Status** (Board) — grouped by Status
3. **Unpaid** (Table) — filtered: Status = Sent or Overdue
4. **Monthly Revenue** (Table) — grouped by month

---

### DB6: Expenses

| Property | Type | Details |
|----------|------|---------|
| Expense | Title | — |
| Category | Select | `Software`, `Hardware`, `Marketing`, `Travel`, `Office`, `Education`, `Tax`, `Other` |
| Amount | Number (USD) | — |
| Date | Date | — |
| Recurring | Checkbox | — |
| Frequency | Select | `Monthly`, `Quarterly`, `Yearly`, `One-time` |
| Receipt | Files & Media | — |
| Notes | Rich Text | — |
| Tax Deductible | Checkbox | — |

**Views:**
1. **All Expenses** (Table) — sorted by Date desc
2. **By Category** (Table) — grouped by Category
3. **Monthly** (Table) — grouped by month
4. **Tax Deductible** (Table) — filtered: Tax Deductible = true

---

### DB7: Proposals

| Property | Type | Details |
|----------|------|---------|
| Proposal Title | Title | — |
| Client | Relation | → Clients DB |
| Status | Select | `Draft`, `Sent`, `Accepted`, `Rejected`, `Expired` |
| Amount | Number (USD) | — |
| Sent Date | Date | — |
| Deadline | Date | — |
| Win Rate | Formula | (calculated at view level) |
| Link | URL | — |
| Notes | Rich Text | — |

**Views:**
1. **All Proposals** (Table)
2. **Pipeline** (Board) — grouped by Status
3. **Active** (Table) — filtered: Status = Draft or Sent

---

### DB8: Notes

| Property | Type | Details |
|----------|------|---------|
| Title | Title | — |
| Category | Select | `Meeting Notes`, `Ideas`, `Resources`, `SOP`, `Templates` |
| Related Client | Relation | → Clients DB |
| Related Project | Relation | → Projects DB |
| Tags | Multi-select | — |
| Created | Created time | — |

**Views:**
1. **All Notes** (Table)
2. **By Category** (Board) — grouped by Category
3. **Recent** (Table) — sorted by Created desc

---

## Dashboard Page Layout

The Dashboard (home page) contains:

1. **Header**: "Welcome back! Here's your business at a glance."
2. **Quick Actions**: Callout block with links to create new Task, Log Time, Create Invoice
3. **Active Projects** — linked view of Projects DB, filtered: Status = In Progress (Table, 5 items)
4. **Today's Tasks** — linked view of Tasks DB, filtered: Due = Today (Table)
5. **Unpaid Invoices** — linked view of Invoices DB, filtered: Status = Sent/Overdue (Table)
6. **This Week's Time** — linked view of Time Log, filtered: this week (Table)
7. **Recent Proposals** — linked view of Proposals, filtered: Status = Sent (Table, 3 items)

---

## Pre-filled Sample Data

- 3 sample clients (Active, Prospect, Past)
- 2 sample projects with tasks
- 5 sample time log entries
- 2 sample invoices (Paid, Sent)
- 3 sample expenses
- 1 sample proposal
- A "Getting Started" note with setup instructions

---

## Setup Instructions for Buyer

1. Click "Duplicate" to add this template to your Notion workspace
2. Delete all sample data (or keep as reference)
3. Customize the Select/Multi-select options to match your business
4. Set your default hourly rate in Time Log entries
5. Start by adding your current clients and active projects
6. Log time daily, send invoices weekly
7. Review the Dashboard daily for a quick overview
