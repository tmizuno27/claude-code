# 03 — Student Study Hub

**Template Name (EN):** Student Study Hub
**Template Name (JP):** 学生スタディハブ
**Price:** $9
**Target Audience:** College students, high school students, graduate students, self-learners

---

## Page Structure

```
Student Study Hub (Top Page)
├── Dashboard
├── Courses & Classes
│   └── Courses DB (linked)
├── Assignments & Exams
│   └── Assignments DB (linked)
├── Study Sessions
│   └── Study Log DB (linked)
├── Notes Library
│   └── Notes DB (linked)
├── Grade Tracker
│   └── Grades DB (linked)
└── Semester Planner
    └── Semester DB (linked)
```

---

## Database Schemas

### DB1: Courses

| Property | Type | Details |
|----------|------|---------|
| Course Name | Title | — |
| Code | Rich Text | e.g. "CS101" |
| Professor | Rich Text | — |
| Semester | Relation | → Semester DB |
| Status | Select | `Current`, `Completed`, `Dropped`, `Planned` |
| Schedule | Rich Text | e.g. "Mon/Wed 10:00-11:30" |
| Location | Rich Text | — |
| Credits | Number | — |
| Current Grade | Formula | Rollup average from Grades |
| Assignments | Relation | → Assignments DB |
| Notes | Relation | → Notes DB |
| Grades | Relation | → Grades DB |
| Syllabus | Files & Media | — |
| Color | Select | `🔴 Red`, `🔵 Blue`, `🟢 Green`, `🟡 Yellow`, `🟣 Purple`, `🟠 Orange` |

**Views:**
1. **All Courses** (Table)
2. **Current Semester** (Table) — filtered: Status = Current
3. **By Semester** (Table) — grouped by Semester
4. **Gallery** (Gallery) — visual cards

---

### DB2: Assignments

| Property | Type | Details |
|----------|------|---------|
| Assignment | Title | — |
| Course | Relation | → Courses DB |
| Type | Select | `Homework`, `Essay`, `Project`, `Quiz`, `Midterm`, `Final Exam`, `Presentation`, `Lab`, `Reading` |
| Status | Select | `Not Started`, `In Progress`, `Completed`, `Submitted`, `Graded` |
| Priority | Select | `🔴 Urgent`, `🟡 Medium`, `🟢 Low` |
| Due Date | Date | — |
| Weight | Number (%) | — |
| Grade | Number (%) | — |
| Score | Rich Text | e.g. "85/100" |
| Estimated Hours | Number | — |
| Notes | Rich Text | — |
| Files | Files & Media | — |
| Days Until Due | Formula | `dateBetween(prop("Due Date"), now(), "days")` |
| Status Emoji | Formula | `if(prop("Status") == "Completed" or prop("Status") == "Submitted", "✅", if(prop("Days Until Due") < 2, "🚨", if(prop("Days Until Due") < 7, "⚠️", "📝")))` |

**Views:**
1. **All Assignments** (Table) — sorted by Due Date
2. **Kanban** (Board) — grouped by Status
3. **Due This Week** (Table) — filtered: Due Date within this week
4. **By Course** (Table) — grouped by Course
5. **Calendar** (Calendar) — by Due Date
6. **Overdue** (Table) — filtered: Due Date < today AND Status != Completed/Submitted

---

### DB3: Study Log

| Property | Type | Details |
|----------|------|---------|
| Session | Title | e.g. "Chapter 5 Review" |
| Course | Relation | → Courses DB |
| Date | Date | — |
| Duration (hrs) | Number | — |
| Type | Select | `Reading`, `Practice Problems`, `Review`, `Flashcards`, `Group Study`, `Office Hours`, `Lecture Review` |
| Productivity | Select | `⭐⭐⭐⭐⭐`, `⭐⭐⭐⭐`, `⭐⭐⭐`, `⭐⭐`, `⭐` |
| Notes | Rich Text | — |

**Views:**
1. **All Sessions** (Table) — sorted by Date desc
2. **This Week** (Table) — filtered: Date within this week
3. **By Course** (Table) — grouped by Course
4. **Calendar** (Calendar) — by Date
5. **Weekly Summary** (Table) — grouped by week

---

### DB4: Notes

| Property | Type | Details |
|----------|------|---------|
| Title | Title | — |
| Course | Relation | → Courses DB |
| Type | Select | `Lecture Notes`, `Reading Notes`, `Summary`, `Cheat Sheet`, `Formula Sheet`, `Study Guide` |
| Date | Date | — |
| Tags | Multi-select | user customizes |
| Content | Rich Text | (the actual notes go in the page body) |
| Files | Files & Media | — |

**Views:**
1. **All Notes** (Table)
2. **By Course** (Table) — grouped by Course
3. **By Type** (Board) — grouped by Type
4. **Recent** (Table) — sorted by Date desc

---

### DB5: Grades

| Property | Type | Details |
|----------|------|---------|
| Item | Title | — |
| Course | Relation | → Courses DB |
| Type | Select | `Homework`, `Quiz`, `Midterm`, `Final`, `Project`, `Participation`, `Essay` |
| Weight | Number (%) | — |
| Score | Number (%) | — |
| Weighted Score | Formula | `prop("Score") * prop("Weight") / 100` |
| Date | Date | — |
| Notes | Rich Text | — |

**Views:**
1. **All Grades** (Table)
2. **By Course** (Table) — grouped by Course
3. **Grade Summary** (Table) — grouped by Course, showing average

---

### DB6: Semesters

| Property | Type | Details |
|----------|------|---------|
| Semester | Title | e.g. "Fall 2026" |
| Start Date | Date | — |
| End Date | Date | — |
| Status | Select | `Current`, `Completed`, `Upcoming` |
| GPA | Number | — |
| Courses | Relation | → Courses DB |
| Notes | Rich Text | — |

**Views:**
1. **All Semesters** (Table) — sorted by Start Date desc
2. **Current** (Table) — filtered: Status = Current

---

## Dashboard Page Layout

1. **Header**: "Student Study Hub" + current semester
2. **Upcoming Deadlines** — Assignments DB, sorted by Due Date, filtered: Status != Completed (Table, 7 items)
3. **Today's Schedule** — Callout with manual class schedule
4. **Study Streak** — Callout tracking consecutive study days (manual)
5. **This Week's Study Hours** — Study Log, filtered: this week (Table)
6. **Grade Overview** — Grades DB grouped by Course (Table)
7. **Quick Links** — toggle with links to each Course page

---

## Pre-filled Sample Data

- 4 sample courses (CS101, MATH201, ENG102, BIO150)
- 8 sample assignments across courses and statuses
- 5 sample study sessions
- 3 sample notes
- 4 sample grades
- 1 sample semester (Current)

---

## Setup Instructions for Buyer

1. Duplicate to your workspace
2. Update Semester info with your current semester dates
3. Add your courses with schedule and professor info
4. Enter all known assignments and deadlines from syllabi
5. Log study sessions daily to build the habit
6. Enter grades as you receive them
7. Check Dashboard daily for upcoming deadlines
