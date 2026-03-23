# 02 — Content Creator Dashboard

**Template Name (EN):** Content Creator Dashboard
**Template Name (JP):** コンテンツクリエイター管理ダッシュボード
**Price:** $15
**Target Audience:** YouTubers, bloggers, podcasters, newsletter writers, TikTokers

---

## Page Structure

```
Content Creator Dashboard (Top Page)
├── Dashboard (overview + linked views)
├── Content Calendar
│   └── Content DB (linked)
├── Ideas Bank
│   └── Ideas DB (linked)
├── Platform Analytics
│   └── Analytics DB (linked)
├── Brand Deals & Sponsorships
│   └── Sponsors DB (linked)
├── Revenue Tracker
│   └── Revenue DB (linked)
└── Equipment & Tools
    └── Equipment DB (linked)
```

---

## Database Schemas

### DB1: Content

| Property | Type | Details |
|----------|------|---------|
| Title | Title | — |
| Platform | Multi-select | `YouTube`, `Blog`, `TikTok`, `Instagram`, `Twitter/X`, `Podcast`, `Newsletter`, `LinkedIn` |
| Status | Select | `Idea`, `Scripting`, `Recording`, `Editing`, `Scheduled`, `Published`, `Repurposed` |
| Content Type | Select | `Video`, `Blog Post`, `Short/Reel`, `Podcast Episode`, `Thread`, `Newsletter`, `Carousel` |
| Category/Niche | Select | (user customizes) `Tutorial`, `Vlog`, `Review`, `Opinion`, `Behind the Scenes`, `Collaboration` |
| Publish Date | Date | — |
| Thumbnail | Files & Media | — |
| Script/Draft | Rich Text | — |
| URL | URL | — |
| Idea Source | Relation | → Ideas DB |
| Sponsor | Relation | → Sponsors DB |
| Revenue | Relation | → Revenue DB |
| Views | Number | — |
| Likes | Number | — |
| Comments | Number | — |
| Engagement Rate | Formula | `if(prop("Views") > 0, round((prop("Likes") + prop("Comments")) / prop("Views") * 10000) / 100, 0)` |
| Notes | Rich Text | — |

**Views:**
1. **Content Calendar** (Calendar) — by Publish Date
2. **Kanban** (Board) — grouped by Status
3. **By Platform** (Table) — grouped by Platform
4. **Published** (Gallery) — filtered: Status = Published, show Thumbnail
5. **Top Performing** (Table) — sorted by Views desc

---

### DB2: Ideas

| Property | Type | Details |
|----------|------|---------|
| Idea | Title | — |
| Status | Select | `Raw Idea`, `Researching`, `Ready to Create`, `Created`, `Discarded` |
| Platform | Multi-select | `YouTube`, `Blog`, `TikTok`, `Instagram`, `Twitter/X`, `Podcast`, `Newsletter` |
| Priority | Select | `🔥 Hot`, `👍 Good`, `💡 Maybe Later` |
| Source | Select | `Audience Request`, `Trending`, `Competitor`, `Personal Experience`, `News`, `AI Generated` |
| Keywords | Rich Text | — |
| Notes | Rich Text | — |
| Content | Relation | → Content DB |
| Created | Created time | — |

**Views:**
1. **All Ideas** (Table) — default
2. **By Status** (Board) — grouped by Status
3. **Hot Ideas** (Table) — filtered: Priority = Hot
4. **By Platform** (Table) — grouped by Platform

---

### DB3: Analytics

| Property | Type | Details |
|----------|------|---------|
| Period | Title | e.g. "2026-W12", "2026-03" |
| Platform | Select | `YouTube`, `Blog`, `TikTok`, `Instagram`, `Twitter/X`, `Podcast`, `Newsletter` |
| Date | Date | — |
| Followers/Subscribers | Number | — |
| New Followers | Number | — |
| Total Views | Number | — |
| Total Engagement | Number | — |
| Top Content | Rich Text | — |
| Notes | Rich Text | — |

**Views:**
1. **All Records** (Table) — sorted by Date desc
2. **By Platform** (Table) — grouped by Platform
3. **Monthly** (Table) — grouped by month

---

### DB4: Sponsors

| Property | Type | Details |
|----------|------|---------|
| Brand Name | Title | — |
| Status | Select | `Lead`, `Negotiating`, `Confirmed`, `Delivered`, `Paid`, `Declined` |
| Contact | Rich Text | — |
| Email | Email | — |
| Deal Type | Select | `Sponsored Post`, `Affiliate`, `Product Review`, `Brand Ambassador`, `Ad Read` |
| Payment | Number (USD) | — |
| Content | Relation | → Content DB |
| Deadline | Date | — |
| Deliverables | Rich Text | — |
| Contract | Files & Media | — |
| Notes | Rich Text | — |

**Views:**
1. **All Deals** (Table)
2. **Pipeline** (Board) — grouped by Status
3. **Active** (Table) — filtered: Status = Negotiating or Confirmed
4. **Revenue** (Table) — sorted by Payment desc

---

### DB5: Revenue

| Property | Type | Details |
|----------|------|---------|
| Description | Title | — |
| Source | Select | `Ad Revenue`, `Sponsorship`, `Affiliate`, `Merch`, `Course/Digital Product`, `Donations/Tips`, `Consulting`, `Other` |
| Platform | Select | `YouTube`, `Blog`, `TikTok`, `Instagram`, `Podcast`, `Newsletter`, `Other` |
| Amount | Number (USD) | — |
| Date | Date | — |
| Content | Relation | → Content DB |
| Sponsor | Relation | → Sponsors DB |
| Recurring | Checkbox | — |
| Notes | Rich Text | — |

**Views:**
1. **All Revenue** (Table) — sorted by Date desc
2. **By Source** (Table) — grouped by Source
3. **Monthly** (Table) — grouped by month
4. **By Platform** (Table) — grouped by Platform

---

### DB6: Equipment

| Property | Type | Details |
|----------|------|---------|
| Item | Title | — |
| Category | Select | `Camera`, `Audio`, `Lighting`, `Computer`, `Software`, `Accessories`, `Other` |
| Cost | Number (USD) | — |
| Purchase Date | Date | — |
| Status | Select | `Active`, `Wishlist`, `Retired` |
| Link | URL | — |
| Notes | Rich Text | — |

**Views:**
1. **All Equipment** (Table)
2. **Wishlist** (Table) — filtered: Status = Wishlist
3. **By Category** (Board) — grouped by Category

---

## Dashboard Page Layout

1. **Header**: "Content Creator HQ" with motivational toggle
2. **This Week's Content** — linked view of Content DB, Calendar view (this week)
3. **Production Pipeline** — linked view of Content DB, Kanban (filtered: Status != Published)
4. **Hot Ideas** — linked view of Ideas DB, filtered: Priority = Hot (Table, 5 items)
5. **Active Sponsorships** — linked view of Sponsors DB, filtered: Status = Confirmed (Table)
6. **Monthly Revenue** — linked view of Revenue DB, this month (Table)
7. **Quick Stats** — Callout with manual KPI updates

---

## Pre-filled Sample Data

- 5 sample content pieces across different platforms and statuses
- 8 sample ideas in various stages
- 2 sample sponsor deals
- 5 sample revenue entries
- 3 sample equipment items

---

## Setup Instructions for Buyer

1. Duplicate template to your workspace
2. Customize Platform and Category options to match your channels
3. Delete sample data
4. Import your existing content ideas into the Ideas Bank
5. Set up your Content Calendar with upcoming planned content
6. Track analytics weekly (manual entry or integrate with tools)
7. Use the Dashboard daily to stay on track
