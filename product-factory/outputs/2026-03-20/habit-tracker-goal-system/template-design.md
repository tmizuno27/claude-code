# Notion Template Design — Habit Tracker & Goal System

## Databases (7)

### 1. Habits DB
| Property | Type | Details |
|----------|------|---------|
| Habit Name | Title | e.g. "Meditate 10 min" |
| Category | Select | Health, Learning, Finance, Mindfulness, Productivity, Social |
| Frequency | Select | Daily, Weekdays, Weekends, Custom |
| Linked Goal | Relation | → Goals DB |
| Current Streak | Formula | Count consecutive completed days |
| Longest Streak | Formula | Max streak ever achieved |
| Status | Select | Active, Paused, Archived |
| Icon | Text | Emoji for visual identification |
| Created | Created time | Auto |

### 2. Daily Check-Ins DB
| Property | Type | Details |
|----------|------|---------|
| Date | Title | Auto-formatted YYYY-MM-DD |
| Habit | Relation | → Habits DB |
| Completed | Checkbox | One-click check-in |
| Notes | Text | Optional context |
| Mood | Select | Great, Good, Okay, Tough, Bad |
| Energy Level | Select | High, Medium, Low |
| Day of Week | Formula | Derived from Date |

### 3. Goals DB (OKR)
| Property | Type | Details |
|----------|------|---------|
| Objective | Title | Big-picture goal statement |
| Time Frame | Select | Q1, Q2, Q3, Q4, Annual, Custom |
| Status | Select | Not Started, In Progress, At Risk, Completed, Dropped |
| Key Results | Relation | → Key Results DB |
| Linked Habits | Relation | → Habits DB |
| Progress | Rollup | Average of Key Results progress % |
| Priority | Select | High, Medium, Low |
| Start Date | Date | |
| Target Date | Date | |
| Notes | Text | Context and motivation |

### 4. Key Results DB
| Property | Type | Details |
|----------|------|---------|
| Key Result | Title | Measurable outcome statement |
| Parent Goal | Relation | → Goals DB |
| Target Value | Number | Numeric target |
| Current Value | Number | Current progress |
| Unit | Text | e.g. "books", "km", "days" |
| Progress % | Formula | (Current / Target) * 100, capped at 100 |
| Status | Formula | Auto: <30% At Risk, 30-70% On Track, >70% Almost There, 100% Done |
| Deadline | Date | |

### 5. Reviews DB
| Property | Type | Details |
|----------|------|---------|
| Title | Title | "Week 12 Review" / "March Review" |
| Type | Select | Weekly, Monthly |
| Period Start | Date | |
| Period End | Date | |
| Wins | Text | What went well |
| Challenges | Text | What was difficult |
| Lessons | Text | Key takeaways |
| Habit Completion Rate | Number | % (manually entered or calculated) |
| Goals Reviewed | Relation | → Goals DB |
| Next Period Focus | Text | Top 3 priorities |
| Rating | Select | 1-5 stars |

### 6. Journal DB
| Property | Type | Details |
|----------|------|---------|
| Date | Title | YYYY-MM-DD |
| Entry | Text | Free-form journaling |
| Mood | Select | Great, Good, Okay, Tough, Bad |
| Gratitude | Text | 3 things grateful for |
| Daily Intention | Text | One focus for the day |
| Evening Reflection | Text | End-of-day thoughts |
| Tags | Multi-select | Personal, Work, Health, Learning, Relationships |

### 7. Rewards DB
| Property | Type | Details |
|----------|------|---------|
| Reward | Title | e.g. "New running shoes" |
| Milestone Type | Select | Streak (7/21/30/60/100), Goal Completed, Custom |
| Linked Goal | Relation | → Goals DB |
| Linked Habit | Relation | → Habits DB |
| Required Streak | Number | Days needed (if streak-based) |
| Earned | Checkbox | Auto or manual |
| Earned Date | Date | |
| Cost | Number | Optional budget tracking |

---

## Views (17)

### Habits DB Views
1. **All Habits — Table** — Full table with all properties, grouped by Category
2. **Active Habits — Board** — Kanban by Category, filtered to Active only
3. **Streak Leaderboard — Table** — Sorted by Current Streak descending, showing streak + longest streak

### Daily Check-Ins DB Views
4. **Today's Check-In — List** — Filtered to today's date, shows habit name + checkbox only (minimal)
5. **Weekly Calendar — Calendar** — Calendar view by Date, dot-colored by Completed status
6. **Completion Heatmap — Table** — Grouped by week, showing completion counts per habit
7. **Check-In History — Table** — Full table sorted by Date descending

### Goals DB Views
8. **Active Goals — Board** — Kanban by Status, filtered to exclude Dropped
9. **Goals Timeline — Timeline** — Timeline view using Start Date → Target Date
10. **All Goals — Table** — Full table with progress rollup

### Key Results DB Views
11. **Key Results — Table** — Grouped by Parent Goal, showing progress bars
12. **At Risk — Table** — Filtered to Progress < 30% and not Done

### Reviews DB Views
13. **Weekly Reviews — Gallery** — Gallery cards showing title, rating, wins
14. **Monthly Reviews — Gallery** — Filtered to Monthly type

### Journal DB Views
15. **Journal — List** — Reverse chronological, showing date + mood + first line
16. **Mood Timeline — Table** — Date + Mood columns for pattern spotting

### Rewards DB Views
17. **Rewards Board — Board** — Kanban: Locked vs Earned, with milestone details

---

## Dashboard Layout

### Top Section — Daily Command Center
| Column 1 (40%) | Column 2 (60%) |
|-----------------|-----------------|
| **Today's Date** (large heading) | **Today's Check-In** (linked view — Today's Check-In) |
| **Current Active Streaks** (callout showing top 3 streaks with fire emoji) | |
| **Daily Intention** (from Journal) | |

### Middle Section — Goals & Progress
| Column 1 (50%) | Column 2 (50%) |
|-----------------|-----------------|
| **Active Goals** (linked view — Active Goals Board) | **Key Results Progress** (linked view — Key Results Table) |

### Bottom Section — Reflection & Rewards
| Column 1 (33%) | Column 2 (33%) | Column 3 (33%) |
|-----------------|-----------------|-----------------|
| **Latest Weekly Review** (linked view) | **Accountability Journal** (linked view — Journal List, last 3 entries) | **Rewards** (linked view — Rewards Board) |

### Sidebar (Toggle Block)
- Quick-Start Guide (step-by-step setup instructions)
- Habit Library (pre-loaded habit suggestions by category)
- FAQ & Tips

---

## Relations Map
```
Goals DB ←→ Key Results DB    (1:many)
Goals DB ←→ Habits DB         (many:many)
Goals DB ←→ Reviews DB        (many:many)
Goals DB ←→ Rewards DB        (1:many)
Habits DB ←→ Daily Check-Ins  (1:many)
Habits DB ←→ Rewards DB       (1:many)
```

---

## Sample Data

### Sample Habits (6)
| Habit | Category | Frequency |
|-------|----------|-----------|
| Meditate 10 minutes | Mindfulness | Daily |
| Read 20 pages | Learning | Daily |
| Exercise 30 minutes | Health | Weekdays |
| Write in journal | Mindfulness | Daily |
| No social media before noon | Productivity | Daily |
| Save $5 to investment fund | Finance | Daily |

### Sample Goal (1 OKR)
**Objective:** Build a consistent morning routine by end of Q1

| Key Result | Target | Unit |
|------------|--------|------|
| Complete morning meditation 80 of 90 days | 80 | days |
| Read 6 books | 6 | books |
| Exercise 60 of 90 days | 60 | days |

### Sample Rewards (3)
| Reward | Milestone |
|--------|-----------|
| Buy a new book | 7-day reading streak |
| Spa day | 30-day meditation streak |
| Weekend trip | Complete Q1 goal |

### Sample Weekly Review (1)
- **Title:** Week 1 Review
- **Wins:** Hit 100% on meditation, finished 1 book
- **Challenges:** Missed 2 exercise days due to rain
- **Lessons:** Need indoor workout backup plan
- **Rating:** 4/5
- **Next Week Focus:** Add bodyweight routine, start journaling daily

### Sample Journal Entry (1)
- **Mood:** Good
- **Gratitude:** Morning sunshine, productive work session, good conversation with a friend
- **Daily Intention:** Stay present during meetings
- **Evening Reflection:** Managed to stay focused most of the day. The no-social-media habit is getting easier.
