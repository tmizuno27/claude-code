# 04 — Life OS / Second Brain

**Template Name (EN):** Life OS — Your Complete Second Brain
**Template Name (JP):** ライフOS — セカンドブレイン
**Price:** $19
**Target Audience:** Productivity enthusiasts, personal development focused individuals, anyone wanting to organize their entire life

---

## Page Structure

```
Life OS (Top Page)
├── Command Center (Dashboard)
├── Areas of Life
│   └── Areas DB (linked)
├── Goals & Habits
│   ├── Goals DB (linked)
│   └── Habits DB (linked)
├── Projects
│   └── Projects DB (linked)
├── Tasks
│   └── Tasks DB (linked)
├── Knowledge Base
│   ├── Notes DB (linked)
│   └── Resources DB (linked)
├── Journal
│   └── Journal DB (linked)
├── Finances
│   └── Finance DB (linked)
└── Health & Wellness
    └── Health DB (linked)
```

---

## Database Schemas

### DB1: Areas of Life

| Property | Type | Details |
|----------|------|---------|
| Area | Title | — |
| Icon | Rich Text | emoji |
| Status | Select | `Thriving`, `Good`, `Needs Attention`, `Struggling` |
| Description | Rich Text | — |
| Goals | Relation | → Goals DB |
| Projects | Relation | → Projects DB |
| Score (1-10) | Number | — |
| Last Reviewed | Date | — |

Pre-filled areas: `Career`, `Health & Fitness`, `Finances`, `Relationships`, `Personal Growth`, `Fun & Recreation`, `Environment`, `Spirituality`

**Views:**
1. **Wheel of Life** (Table) — all areas with scores
2. **By Status** (Board) — grouped by Status
3. **Gallery** (Gallery) — visual cards with icons

---

### DB2: Goals

| Property | Type | Details |
|----------|------|---------|
| Goal | Title | — |
| Area | Relation | → Areas DB |
| Timeframe | Select | `This Week`, `This Month`, `This Quarter`, `This Year`, `Long-term` |
| Status | Select | `Not Started`, `In Progress`, `Achieved`, `Paused`, `Abandoned` |
| Priority | Select | `🔴 Must`, `🟡 Should`, `🟢 Could` |
| Start Date | Date | — |
| Target Date | Date | — |
| Progress | Number (%) | — |
| Progress Bar | Formula | `slice("██████████", 0, floor(prop("Progress") / 10)) + slice("░░░░░░░░░░", 0, 10 - floor(prop("Progress") / 10)) + " " + format(prop("Progress")) + "%"` |
| Key Results | Rich Text | — |
| Projects | Relation | → Projects DB |
| Notes | Rich Text | — |

**Views:**
1. **All Goals** (Table)
2. **By Timeframe** (Board) — grouped by Timeframe
3. **By Area** (Table) — grouped by Area
4. **Active** (Table) — filtered: Status = In Progress
5. **Quarterly Review** (Table) — filtered: Timeframe = This Quarter

---

### DB3: Habits

| Property | Type | Details |
|----------|------|---------|
| Habit | Title | — |
| Area | Relation | → Areas DB |
| Frequency | Select | `Daily`, `Weekdays`, `3x/week`, `Weekly` |
| Time of Day | Select | `Morning`, `Afternoon`, `Evening`, `Anytime` |
| Status | Select | `Active`, `Paused`, `Retired` |
| Streak | Number | — |
| Best Streak | Number | — |
| Mon | Checkbox | — |
| Tue | Checkbox | — |
| Wed | Checkbox | — |
| Thu | Checkbox | — |
| Fri | Checkbox | — |
| Sat | Checkbox | — |
| Sun | Checkbox | — |
| Weekly Score | Formula | `(if(prop("Mon"), 1, 0) + if(prop("Tue"), 1, 0) + if(prop("Wed"), 1, 0) + if(prop("Thu"), 1, 0) + if(prop("Fri"), 1, 0) + if(prop("Sat"), 1, 0) + if(prop("Sun"), 1, 0))` |
| Notes | Rich Text | — |

**Views:**
1. **Daily Tracker** (Table) — filtered: Status = Active, showing checkboxes
2. **All Habits** (Table)
3. **By Area** (Table) — grouped by Area
4. **Streaks** (Table) — sorted by Streak desc

---

### DB4: Projects

| Property | Type | Details |
|----------|------|---------|
| Project | Title | — |
| Area | Relation | → Areas DB |
| Goal | Relation | → Goals DB |
| Status | Select | `Someday`, `Planning`, `Active`, `Completed`, `On Hold`, `Cancelled` |
| Priority | Select | `🔴 High`, `🟡 Medium`, `🟢 Low` |
| Start Date | Date | — |
| Deadline | Date | — |
| Tasks | Relation | → Tasks DB |
| Progress | Rollup | % of Tasks where Status = Done |
| Notes | Rich Text | — |

**Views:**
1. **All Projects** (Table)
2. **Kanban** (Board) — grouped by Status
3. **By Area** (Table) — grouped by Area
4. **Active** (Table) — filtered: Status = Active
5. **Timeline** (Timeline) — by Start Date → Deadline

---

### DB5: Tasks

| Property | Type | Details |
|----------|------|---------|
| Task | Title | — |
| Project | Relation | → Projects DB |
| Status | Select | `Inbox`, `To Do`, `In Progress`, `Waiting`, `Done` |
| Priority | Select | `🔴 Urgent+Important`, `🟠 Important`, `🟡 Urgent`, `🟢 Low` |
| Due Date | Date | — |
| Energy | Select | `🔋 High`, `🔋 Medium`, `🔋 Low` |
| Time Estimate | Select | `5 min`, `15 min`, `30 min`, `1 hr`, `2+ hr` |
| Context | Multi-select | `Home`, `Office`, `Computer`, `Phone`, `Errands`, `Anywhere` |
| Notes | Rich Text | — |

**Views:**
1. **Inbox** (Table) — filtered: Status = Inbox
2. **Today** (Table) — filtered: Due = Today
3. **Kanban** (Board) — grouped by Status
4. **Eisenhower Matrix** (Board) — grouped by Priority
5. **By Project** (Table) — grouped by Project
6. **Quick Wins** (Table) — filtered: Time Estimate = 5 min or 15 min, Energy = Low

---

### DB6: Notes (Knowledge Base)

| Property | Type | Details |
|----------|------|---------|
| Title | Title | — |
| Type | Select | `Note`, `Idea`, `Quote`, `Summary`, `How-to`, `Reference` |
| Area | Relation | → Areas DB |
| Source | Rich Text | — |
| Tags | Multi-select | user customizes |
| Created | Created time | — |
| Last Edited | Last edited time | — |

**Views:**
1. **All Notes** (Table) — sorted by Last Edited desc
2. **By Area** (Table) — grouped by Area
3. **By Type** (Board) — grouped by Type
4. **Search** (Table) — sorted by Title

---

### DB7: Resources

| Property | Type | Details |
|----------|------|---------|
| Resource | Title | — |
| Type | Select | `Book`, `Article`, `Video`, `Podcast`, `Course`, `Tool`, `Website` |
| Status | Select | `To Review`, `In Progress`, `Completed`, `Reference` |
| Area | Relation | → Areas DB |
| URL | URL | — |
| Rating | Select | `⭐⭐⭐⭐⭐`, `⭐⭐⭐⭐`, `⭐⭐⭐`, `⭐⭐`, `⭐` |
| Key Takeaways | Rich Text | — |
| Tags | Multi-select | — |

**Views:**
1. **All Resources** (Table)
2. **By Type** (Board) — grouped by Type
3. **To Review** (Table) — filtered: Status = To Review
4. **Top Rated** (Table) — sorted by Rating desc

---

### DB8: Journal

| Property | Type | Details |
|----------|------|---------|
| Date | Title | — |
| Date Value | Date | — |
| Mood | Select | `😊 Great`, `🙂 Good`, `😐 Okay`, `😔 Low`, `😫 Bad` |
| Energy | Select | `🔋 High`, `🔋 Medium`, `🔋 Low` |
| Gratitude | Rich Text | 3 things |
| Highlights | Rich Text | — |
| Learnings | Rich Text | — |
| Tomorrow's Focus | Rich Text | — |
| Tags | Multi-select | — |

**Views:**
1. **All Entries** (Table) — sorted by Date desc
2. **Calendar** (Calendar) — by Date Value
3. **Mood Tracker** (Table) — showing Date + Mood
4. **This Month** (Table) — filtered: Date within this month

---

### DB9: Finance

| Property | Type | Details |
|----------|------|---------|
| Description | Title | — |
| Type | Select | `Income`, `Expense`, `Investment`, `Savings` |
| Category | Select | `Salary`, `Freelance`, `Food`, `Rent`, `Transport`, `Entertainment`, `Shopping`, `Health`, `Education`, `Subscriptions`, `Other` |
| Amount | Number (USD) | — |
| Date | Date | — |
| Recurring | Checkbox | — |
| Account | Select | `Bank`, `Cash`, `Credit Card`, `PayPal`, `Other` |
| Notes | Rich Text | — |

**Views:**
1. **All Transactions** (Table) — sorted by Date desc
2. **By Category** (Table) — grouped by Category
3. **Monthly** (Table) — grouped by month
4. **Income vs Expense** (Table) — grouped by Type

---

### DB10: Health

| Property | Type | Details |
|----------|------|---------|
| Date | Title | — |
| Date Value | Date | — |
| Sleep Hours | Number | — |
| Sleep Quality | Select | `Great`, `Good`, `Fair`, `Poor` |
| Exercise | Checkbox | — |
| Exercise Type | Rich Text | — |
| Exercise Duration | Number (min) | — |
| Water (glasses) | Number | — |
| Weight | Number | — |
| Mood | Select | `😊 Great`, `🙂 Good`, `😐 Okay`, `😔 Low` |
| Notes | Rich Text | — |

**Views:**
1. **Daily Log** (Table) — sorted by Date desc
2. **Calendar** (Calendar) — by Date Value
3. **This Week** (Table) — filtered: this week
4. **Exercise Days** (Table) — filtered: Exercise = true

---

## Dashboard (Command Center) Layout

1. **Header**: "Welcome to your Life OS" + current date
2. **Wheel of Life** — Areas DB scores (Gallery, compact)
3. **Active Goals** — Goals DB, filtered: Status = In Progress (Table, 5 items)
4. **Today's Tasks** — Tasks DB, filtered: Due = Today (Table)
5. **Habit Tracker** — Habits DB daily view (Table, Active only)
6. **Latest Journal** — Journal DB (Table, 1 entry)
7. **Quick Capture** — Callout with links to add Task, Note, Journal entry
8. **Weekly Review Checklist** — Toggle with review prompts

---

## Pre-filled Sample Data

- 8 Areas of Life with descriptions and scores
- 5 sample goals across areas
- 7 sample habits
- 3 sample projects
- 10 sample tasks
- 5 sample notes
- 3 sample journal entries
- 2 sample resources

---

## Setup Instructions for Buyer

1. Duplicate to your workspace
2. Start with the Areas of Life — rate each area 1-10
3. Set 1-3 goals per area that needs attention
4. Break goals into projects and tasks
5. Set up your daily habits in the Habit Tracker
6. Journal daily (even 2 minutes counts)
7. Do a Weekly Review every Sunday using the checklist
8. Customize all Select/Multi-select options to match your life
