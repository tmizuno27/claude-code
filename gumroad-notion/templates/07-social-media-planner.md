# 07 — Social Media Planner

**Template Name (EN):** Social Media Planner & Scheduler
**Template Name (JP):** ソーシャルメディアプランナー
**Price:** $14
**Target Audience:** Social media managers, small business owners, content creators, marketing teams

---

## Page Structure

```
Social Media Planner (Top Page)
├── Dashboard
├── Content Calendar
│   └── Posts DB (linked)
├── Platforms
│   └── Platforms DB (linked)
├── Content Pillars
│   └── Pillars DB (linked)
├── Hashtag Library
│   └── Hashtags DB (linked)
├── Analytics
│   └── Analytics DB (linked)
├── Campaign Tracker
│   └── Campaigns DB (linked)
└── Swipe File / Inspiration
    └── Swipe DB (linked)
```

---

## Database Schemas

### DB1: Posts

| Property | Type | Details |
|----------|------|---------|
| Post Title | Title | short descriptor |
| Platform | Multi-select | `Instagram`, `Twitter/X`, `LinkedIn`, `TikTok`, `Facebook`, `Pinterest`, `YouTube`, `Threads` |
| Status | Select | `Idea`, `Drafting`, `Ready`, `Scheduled`, `Published`, `Repurposed` |
| Content Type | Select | `Image`, `Carousel`, `Video`, `Reel/Short`, `Story`, `Text`, `Poll`, `Thread`, `Live` |
| Pillar | Relation | → Pillars DB |
| Campaign | Relation | → Campaigns DB |
| Publish Date | Date | — |
| Time | Select | `6 AM`, `9 AM`, `12 PM`, `3 PM`, `6 PM`, `9 PM` |
| Caption | Rich Text | — |
| Hashtags | Relation | → Hashtags DB |
| Media | Files & Media | — |
| CTA | Select | `Link in Bio`, `Comment`, `Share`, `Save`, `Visit Website`, `DM`, `None` |
| URL | URL | — |
| Likes | Number | — |
| Comments | Number | — |
| Shares | Number | — |
| Saves | Number | — |
| Impressions | Number | — |
| Engagement Rate | Formula | `if(prop("Impressions") > 0, round((prop("Likes") + prop("Comments") + prop("Shares") + prop("Saves")) / prop("Impressions") * 10000) / 100, 0)` |
| Notes | Rich Text | — |

**Views:**
1. **Content Calendar** (Calendar) — by Publish Date (primary view)
2. **Kanban** (Board) — grouped by Status
3. **By Platform** (Table) — grouped by Platform
4. **This Week** (Table) — filtered: Publish Date within this week
5. **Published** (Gallery) — filtered: Status = Published, show Media
6. **Top Performing** (Table) — filtered: Status = Published, sorted by Engagement Rate desc
7. **By Pillar** (Table) — grouped by Pillar

---

### DB2: Platforms

| Property | Type | Details |
|----------|------|---------|
| Platform | Title | — |
| Username/Handle | Rich Text | — |
| URL | URL | — |
| Followers | Number | — |
| Posting Frequency | Select | `Daily`, `2-3x/week`, `Weekly`, `Bi-weekly` |
| Best Times | Rich Text | — |
| Content Types | Multi-select | `Image`, `Video`, `Carousel`, `Text`, `Stories`, `Reels` |
| Goals | Rich Text | — |
| Notes | Rich Text | — |

**Views:**
1. **All Platforms** (Table)
2. **Gallery** (Gallery) — visual cards

---

### DB3: Content Pillars

| Property | Type | Details |
|----------|------|---------|
| Pillar | Title | — |
| Description | Rich Text | — |
| Percentage | Number (%) | target content mix |
| Color | Select | `🔴 Red`, `🔵 Blue`, `🟢 Green`, `🟡 Yellow`, `🟣 Purple` |
| Posts | Relation | → Posts DB |
| Post Count | Rollup | Count of related Posts |
| Example Topics | Rich Text | — |

Pre-filled: `Educational`, `Entertaining`, `Inspirational`, `Promotional`, `Behind the Scenes`

**Views:**
1. **All Pillars** (Table) — showing Pillar, Percentage, Post Count
2. **Gallery** (Gallery)

---

### DB4: Hashtags

| Property | Type | Details |
|----------|------|---------|
| Hashtag Set Name | Title | e.g. "Brand Core" |
| Hashtags | Rich Text | — |
| Platform | Select | `Instagram`, `Twitter/X`, `LinkedIn`, `TikTok`, `Universal` |
| Category | Select | `Brand`, `Niche`, `Trending`, `Community`, `Campaign` |
| Size | Select | `Small (<10K)`, `Medium (10K-500K)`, `Large (500K+)` |
| Posts | Relation | → Posts DB |
| Notes | Rich Text | — |

**Views:**
1. **All Sets** (Table)
2. **By Platform** (Table) — grouped by Platform
3. **By Category** (Board) — grouped by Category

---

### DB5: Analytics

| Property | Type | Details |
|----------|------|---------|
| Period | Title | e.g. "W12 2026" |
| Platform | Select | `Instagram`, `Twitter/X`, `LinkedIn`, `TikTok`, `Facebook`, `Pinterest`, `YouTube` |
| Date | Date | — |
| Followers | Number | — |
| New Followers | Number | — |
| Impressions | Number | — |
| Reach | Number | — |
| Engagement Rate | Number (%) | — |
| Top Post | Rich Text | — |
| Website Clicks | Number | — |
| Notes | Rich Text | — |

**Views:**
1. **All Records** (Table) — sorted by Date desc
2. **By Platform** (Table) — grouped by Platform
3. **Growth Chart** (Table) — sorted by Date, showing Followers

---

### DB6: Campaigns

| Property | Type | Details |
|----------|------|---------|
| Campaign Name | Title | — |
| Status | Select | `Planning`, `Active`, `Completed`, `Paused` |
| Start Date | Date | — |
| End Date | Date | — |
| Goal | Rich Text | — |
| Platforms | Multi-select | `Instagram`, `Twitter/X`, `LinkedIn`, `TikTok`, `Facebook` |
| Posts | Relation | → Posts DB |
| Post Count | Rollup | Count of related Posts |
| Budget | Number (USD) | — |
| Results | Rich Text | — |
| Notes | Rich Text | — |

**Views:**
1. **All Campaigns** (Table)
2. **Active** (Table) — filtered: Status = Active
3. **Timeline** (Timeline) — by Start Date → End Date

---

### DB7: Swipe File

| Property | Type | Details |
|----------|------|---------|
| Title | Title | — |
| Source | Rich Text | — |
| Platform | Select | `Instagram`, `Twitter/X`, `LinkedIn`, `TikTok`, `Other` |
| Type | Select | `Caption`, `Hook`, `Visual`, `Strategy`, `Campaign`, `Ad` |
| Screenshot | Files & Media | — |
| URL | URL | — |
| Why It Works | Rich Text | — |
| Tags | Multi-select | — |
| Created | Created time | — |

**Views:**
1. **All Inspiration** (Gallery) — show Screenshot
2. **By Type** (Board) — grouped by Type
3. **By Platform** (Table) — grouped by Platform

---

## Dashboard Page Layout

1. **Header**: "Social Media HQ"
2. **This Week's Calendar** — Posts DB, Calendar view (this week)
3. **Production Pipeline** — Posts DB, Kanban (Status != Published)
4. **Content Mix** — Pillars DB showing percentages (Table)
5. **Platform Stats** — Platforms DB (Table, compact)
6. **Active Campaigns** — Campaigns DB, filtered: Active (Table)
7. **Top Posts This Month** — Posts DB, sorted by Engagement Rate, this month (Table, 3)
8. **Quick Create** — Callout with link to create new Post

---

## Pre-filled Sample Data

- 10 sample posts across platforms and statuses
- 5 platforms configured
- 5 content pillars with percentages
- 6 hashtag sets
- 2 analytics records
- 1 sample campaign
- 5 swipe file entries

---

## Setup Instructions for Buyer

1. Duplicate to workspace
2. Set up your Platforms with handles and goals
3. Define your Content Pillars and target percentages
4. Build your Hashtag Library (organized by category)
5. Plan your first week of content in the Calendar
6. Use the Kanban to track production status
7. Log analytics weekly
8. Save inspiration to the Swipe File whenever you see great content
