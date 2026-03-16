# 09 — Book & Learning Tracker

**Template Name (EN):** Book & Learning Tracker
**Template Name (JP):** 読書・学習トラッカー
**Price:** $9
**Target Audience:** Avid readers, lifelong learners, personal development enthusiasts, students

---

## Page Structure

```
Book & Learning Tracker (Top Page)
├── Dashboard
├── Reading List
│   └── Books DB (linked)
├── Courses & Learning
│   └── Courses DB (linked)
├── Notes & Highlights
│   └── Notes DB (linked)
├── Reading Log
│   └── Reading Log DB (linked)
├── Annual Reading Challenge
│   └── Challenge DB (linked)
└── Wishlist
    └── (filtered view of Books DB)
```

---

## Database Schemas

### DB1: Books

| Property | Type | Details |
|----------|------|---------|
| Title | Title | — |
| Author | Rich Text | — |
| Status | Select | `Wishlist`, `To Read`, `Reading`, `Completed`, `DNF (Did Not Finish)`, `Re-reading` |
| Genre | Multi-select | `Fiction`, `Non-fiction`, `Self-help`, `Business`, `Science`, `Biography`, `Fantasy`, `Sci-Fi`, `History`, `Psychology`, `Philosophy`, `Technical` |
| Format | Select | `Physical`, `Kindle`, `Audiobook`, `PDF` |
| Pages | Number | — |
| Current Page | Number | — |
| Progress | Formula | `if(prop("Pages") > 0, round(prop("Current Page") / prop("Pages") * 100), 0)` |
| Progress Bar | Formula | `slice("██████████", 0, floor(prop("Progress") / 10)) + slice("░░░░░░░░░░", 0, 10 - floor(prop("Progress") / 10)) + " " + format(prop("Progress")) + "%"` |
| Rating | Select | `⭐⭐⭐⭐⭐`, `⭐⭐⭐⭐`, `⭐⭐⭐`, `⭐⭐`, `⭐` |
| Start Date | Date | — |
| Finish Date | Date | — |
| Reading Time (days) | Formula | `if(and(not(empty(prop("Start Date"))), not(empty(prop("Finish Date")))), dateBetween(prop("Finish Date"), prop("Start Date"), "days"), 0)` |
| Source/Recommendation | Rich Text | — |
| Notes | Relation | → Notes DB |
| Cover | Files & Media | — |
| Key Takeaway | Rich Text | one-line summary |
| Would Recommend | Checkbox | — |
| Challenge | Relation | → Challenge DB |

**Views:**
1. **All Books** (Table) — default
2. **Currently Reading** (Gallery) — filtered: Status = Reading, show Cover
3. **Bookshelf** (Gallery) — filtered: Status = Completed, show Cover
4. **To Read** (Table) — filtered: Status = To Read
5. **Wishlist** (Table) — filtered: Status = Wishlist
6. **By Genre** (Table) — grouped by Genre
7. **Top Rated** (Table) — filtered: Status = Completed, sorted by Rating desc
8. **By Author** (Table) — grouped by Author

---

### DB2: Courses

| Property | Type | Details |
|----------|------|---------|
| Course Name | Title | — |
| Platform | Select | `Udemy`, `Coursera`, `YouTube`, `Skillshare`, `LinkedIn Learning`, `edX`, `Book`, `Podcast`, `Other` |
| Instructor | Rich Text | — |
| Status | Select | `Wishlist`, `Not Started`, `In Progress`, `Completed`, `Dropped` |
| Category | Select | `Programming`, `Design`, `Business`, `Marketing`, `Data Science`, `Language`, `Personal Development`, `Other` |
| Progress | Number (%) | — |
| Rating | Select | `⭐⭐⭐⭐⭐`, `⭐⭐⭐⭐`, `⭐⭐⭐`, `⭐⭐`, `⭐` |
| URL | URL | — |
| Cost | Number (USD) | — |
| Start Date | Date | — |
| Finish Date | Date | — |
| Certificate | Checkbox | — |
| Notes | Relation | → Notes DB |
| Key Takeaways | Rich Text | — |

**Views:**
1. **All Courses** (Table)
2. **In Progress** (Table) — filtered: Status = In Progress
3. **By Platform** (Table) — grouped by Platform
4. **By Category** (Board) — grouped by Category
5. **Completed** (Table) — filtered: Status = Completed

---

### DB3: Notes & Highlights

| Property | Type | Details |
|----------|------|---------|
| Title | Title | — |
| Source | Select | `Book`, `Course`, `Article`, `Podcast`, `Video`, `Own Thought` |
| Book | Relation | → Books DB |
| Course | Relation | → Courses DB |
| Type | Select | `Highlight`, `Summary`, `Quote`, `Key Concept`, `Action Item`, `Question` |
| Chapter/Section | Rich Text | — |
| Page Number | Number | — |
| Content | Rich Text | (in page body) |
| Tags | Multi-select | user customizes |
| Created | Created time | — |

**Views:**
1. **All Notes** (Table) — sorted by Created desc
2. **By Book** (Table) — grouped by Book
3. **By Course** (Table) — grouped by Course
4. **By Type** (Board) — grouped by Type
5. **Quotes** (Table) — filtered: Type = Quote
6. **Action Items** (Table) — filtered: Type = Action Item

---

### DB4: Reading Log

| Property | Type | Details |
|----------|------|---------|
| Date | Title | — |
| Date Value | Date | — |
| Book | Relation | → Books DB |
| Pages Read | Number | — |
| Minutes | Number | — |
| Notes | Rich Text | — |

**Views:**
1. **All Logs** (Table) — sorted by Date desc
2. **Calendar** (Calendar) — by Date Value
3. **This Month** (Table) — filtered: this month
4. **By Book** (Table) — grouped by Book

---

### DB5: Challenge

| Property | Type | Details |
|----------|------|---------|
| Year | Title | e.g. "2026 Reading Challenge" |
| Goal (books) | Number | — |
| Completed | Rollup | Count of related Books (Status = Completed) |
| Progress | Formula | `if(prop("Goal (books)") > 0, round(prop("Completed") / prop("Goal (books)") * 100), 0)` |
| Progress Bar | Formula | `format(prop("Completed")) + "/" + format(prop("Goal (books)")) + " books"` |
| Books | Relation | → Books DB |
| Status | Select | `Active`, `Completed`, `Past` |

**Views:**
1. **All Challenges** (Table)
2. **Current** (Table) — filtered: Status = Active

---

## Dashboard Page Layout

1. **Header**: "Reading & Learning Hub"
2. **Currently Reading** — Books DB, Gallery (Status = Reading)
3. **Reading Challenge Progress** — Challenge DB, current year (Table, 1)
4. **This Month's Reading Log** — Reading Log, calendar view (this month)
5. **Up Next** — Books DB, filtered: Status = To Read, top 5 (Table)
6. **Courses in Progress** — Courses DB, filtered: In Progress (Table)
7. **Recent Notes** — Notes DB, sorted by Created desc (Table, 5)
8. **Stats** — Callout: Books read this year / Pages this month / Streak

---

## Pre-filled Sample Data

- 8 sample books (2 Reading, 3 Completed, 2 To Read, 1 Wishlist)
- 3 sample courses
- 10 sample notes/highlights
- 7 sample reading log entries
- 1 annual challenge (2026, goal: 24 books)

---

## Setup Instructions for Buyer

1. Duplicate to workspace
2. Set up your Annual Reading Challenge with a goal
3. Add books you're currently reading and update Current Page
4. Import your "To Read" list
5. Log reading sessions daily (even 10 minutes)
6. Take notes and highlights as you read (link to the book)
7. Add courses you want to take or are taking
8. Review Dashboard weekly to stay motivated
