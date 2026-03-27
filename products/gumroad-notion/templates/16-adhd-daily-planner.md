# Template Design — ADHD Daily Planner & Focus System

## Overview
A Notion template designed specifically for adults with ADHD. Not a generic planner with an ADHD label — every feature addresses a specific ADHD challenge (executive dysfunction, time blindness, dopamine-seeking, hyperfocus crashes, decision paralysis).

## Price: $14

## Core Design Principles
1. **Low friction**: Every action should take <10 seconds. No complex workflows.
2. **Visual-first**: Colors, progress bars, and icons over text walls.
3. **Dopamine-friendly**: Streaks, completion celebrations, and quick wins.
4. **Flexible**: Works for "good brain days" and "bad brain days" differently.
5. **No guilt**: No shame for missed days. System resets daily.

---

## Database Schema

### 1. Brain Dump Inbox
**Purpose**: Capture everything instantly. Sort later (or never — that's OK too).

| Property | Type | Notes |
|----------|------|-------|
| Title | Title | Quick thought/task/idea |
| Type | Select | Task, Idea, Note, Reminder, Random |
| Energy Required | Select | Low, Medium, High |
| Urgency | Select | Now, Today, This Week, Someday, Never |
| Processed | Checkbox | Move to proper location when ready |
| Created | Created time | Auto |

**Views**:
- Gallery: Visual cards grouped by Type
- Unprocessed: Filter where Processed = false

### 2. Daily Focus Board
**Purpose**: Maximum 3 tasks per day. That's it. Three.

| Property | Type | Notes |
|----------|------|-------|
| Task | Title | What to do |
| Day | Date | Today by default |
| Priority | Select | Must Do (1), Should Do (2), Could Do (3) |
| Status | Select | Not Started, In Progress, Done, Moved |
| Energy Level | Select | Low Energy, Medium, High Energy |
| Time Estimate | Select | 5min, 15min, 30min, 1hr, 2hr+ |
| Actual Time | Number | Minutes spent |
| Dopamine Reward | Text | What treat after completing? |
| Notes | Text | Quick notes |

**Views**:
- Today's Board: Kanban by Status, filtered to today
- Calendar: Monthly view
- Done This Week: Celebration view showing completed items

**Rule**: Maximum 3 "Must Do" per day. Template enforces this with a callout warning.

### 3. Energy & Mood Tracker
**Purpose**: Identify patterns. When are you most productive? What drains you?

| Property | Type | Notes |
|----------|------|-------|
| Date | Date | One entry per day |
| Morning Energy | Select | 1-5 (emoji scale) |
| Afternoon Energy | Select | 1-5 |
| Evening Energy | Select | 1-5 |
| Overall Mood | Select | Great, Good, Meh, Low, Rough |
| Sleep Hours | Number | |
| Sleep Quality | Select | Deep, OK, Restless, Insomnia |
| Medication Taken | Checkbox | Optional — only show if user enables |
| Medication Notes | Text | Dosage, timing, effects |
| Exercise | Checkbox | |
| Hyperfocus Episode | Checkbox | Did you hyperfocus today? |
| Hyperfocus Topic | Text | What captured you? |
| Biggest Win | Text | One thing that went well |
| Biggest Challenge | Text | One thing that was hard |

**Views**:
- Weekly Overview: Table grouped by week
- Energy Trends: Board view by Overall Mood
- Sleep Patterns: Table sorted by sleep hours

### 4. Hyperfocus Session Logger
**Purpose**: Track and harness hyperfocus instead of fighting it.

| Property | Type | Notes |
|----------|------|-------|
| Session | Title | What you hyperfocused on |
| Date | Date | |
| Duration | Number | Hours |
| Productive | Select | Yes (aligned with goals), Neutral, No (rabbit hole) |
| Trigger | Text | What started the hyperfocus? |
| Outcome | Text | What did you produce/learn? |
| Could Monetize | Checkbox | Is this a marketable skill/interest? |

**Views**:
- All Sessions: Table
- Productive Only: Filtered view
- By Topic: Group by session title to see patterns

### 5. Habit Tracker (ADHD-Optimized)
**Purpose**: Tiny habits only. No 10-habit lists. Start with 1-3 max.

| Property | Type | Notes |
|----------|------|-------|
| Habit | Title | |
| Category | Select | Health, Work, Self-Care, Social, Creative |
| Frequency | Select | Daily, Weekdays, 3x/week, Weekly |
| Streak | Formula | Auto-calculated |
| Best Streak | Number | Personal record |
| Reward | Text | What's your reward for a 7-day streak? |
| Active | Checkbox | Currently tracking? |

**Linked DB: Daily Check-ins**

| Property | Type | Notes |
|----------|------|-------|
| Date | Date | |
| Habit | Relation | Links to Habits |
| Done | Checkbox | |
| Notes | Text | Optional |

**Views**:
- Today's Habits: Simple checklist
- Streak Board: Gallery showing current streaks with progress bars
- Weekly Grid: Calendar-style habit grid

### 6. Project Parking Lot
**Purpose**: ADHD brains have 100 ideas. This is where they live so they stop cluttering your focus.

| Property | Type | Notes |
|----------|------|-------|
| Project/Idea | Title | |
| Status | Select | Parked, Active (max 2), Done, Abandoned |
| Excitement Level | Select | 1-5 (how much dopamine does this give?) |
| Effort | Select | Small, Medium, Large, Massive |
| Value | Select | Fun Only, Could Be Useful, Money-Making, Life-Changing |
| Next Step | Text | ONE tiny next action |
| Parked Date | Date | When you put it here |

**Rule**: Maximum 2 "Active" projects at any time. Everything else stays parked.

**Views**:
- Active Projects: Filtered to Active only
- Parking Lot: All parked ideas, sorted by Excitement
- Abandoned Graveyard: It's OK to let go

---

## Dashboard Layout

### Command Center (Single Page)

```
[Callout: "Today's Date — You showed up. That counts."]

[3-Column Layout]

Column 1: TODAY'S FOCUS
- Linked DB: Daily Focus Board (Today only, Kanban)
- Max 3 tasks visible
- Big "Add Brain Dump" button

Column 2: ENERGY CHECK
- Linked DB: Energy Tracker (Today's entry)
- Quick mood/energy input
- "How are you feeling?" prompt

Column 3: HABITS
- Linked DB: Today's Habits (Checklist)
- Streak display
- "1 habit done = a win" callout

[Full Width Below]

Row 2: BRAIN DUMP INBOX
- Linked DB: Unprocessed items (Gallery, max 10 shown)
- "Dump it here, sort it never" tagline

Row 3: THIS WEEK'S WINS
- Linked DB: Done tasks this week
- Celebration emoji and count

Row 4: ACTIVE PROJECTS (max 2)
- Linked DB: Project Parking Lot (Active only)
```

---

## Callout Messages (ADHD-Affirming)

Placed throughout the template:

- "3 tasks max. Your brain works better with fewer choices."
- "Didn't finish everything? Normal. Tomorrow is a fresh start."
- "Hyperfocus isn't a bug. It's a superpower — when you aim it."
- "If this template feels overwhelming, use ONLY the Brain Dump and Daily Focus. Add more later."
- "Bad brain day? Lower the bar. 1 task = success."
- "You don't need to be productive every day to be successful."
- "Consistency isn't about never missing. It's about always coming back."

---

## Sample Data

Pre-filled examples that feel authentic:
- Brain Dump: "Call dentist", "Research that thing about mushrooms", "Birthday gift for mom??", "Why do I have 47 browser tabs"
- Daily Focus: 3 realistic tasks with dopamine rewards ("Watch one episode of show", "Fancy coffee", "10 min guilt-free scrolling")
- Habits: "Drink water before coffee", "10 min walk", "Brain dump before bed"
- Hyperfocus: "Reorganized entire music library (4 hours)", "Deep-dived into how bridges are engineered"

---

## Setup Instructions (Included in Template)

1. Duplicate this template (takes 5 seconds)
2. Go to the Dashboard — that's your home base
3. Start with ONLY the Brain Dump and Daily Focus Board
4. Add Energy Tracking after 3 days
5. Add Habits after 1 week (start with ONE habit)
6. Add everything else only when you're ready (or never — that's fine)

**The #1 rule: Don't try to use everything at once. Your ADHD brain will rebel. Start small.**
