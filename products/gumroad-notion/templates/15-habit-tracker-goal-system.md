# Template Design — Habit Tracker & Goal System

## Overview
Build better habits and achieve goals with a comprehensive tracking system. Combines daily habit tracking, streak monitoring, OKR/goal setting, weekly reviews, and progress visualization.

## Price: $9

## Databases

### 1. Habits
- **Properties**: Habit Name (Title), Category (Select: Health/Fitness/Learning/Productivity/Mindfulness/Finance/Social/Creative), Frequency (Select: Daily/Weekdays/3x Week/Weekly), Current Streak (Number), Best Streak (Number), Start Date, Status (Select: Active/Paused/Completed/Dropped), Why (Text — motivation), Cue (Text), Reward (Text), Notes
- **Views**: Table, Board by Category, Active habits filter

### 2. Daily Log
- **Properties**: Date (Title as date), Habit (Relation→Habits), Completed (Checkbox), Notes, Difficulty (Select: Easy/Medium/Hard), Time Spent (Number, minutes)
- **Views**: Calendar, Table grouped by Habit, Weekly summary, Streak view

### 3. Goals (OKRs)
- **Properties**: Goal (Title), Category (Select: Career/Health/Finance/Relationships/Learning/Personal), Timeframe (Select: Q1/Q2/Q3/Q4/Annual/Custom), Start Date, End Date, Progress (Formula: % of completed key results), Status (Select: On Track/At Risk/Behind/Completed), Why It Matters (Text)
- **Views**: Board by Status, Table by Category, Timeline

### 4. Key Results
- **Properties**: Key Result (Title), Goal (Relation→Goals), Target Value (Number), Current Value (Number), Progress (Formula: Current/Target * 100), Unit (Text), Due Date, Status (Select: Not Started/In Progress/Completed/Failed)
- **Views**: Table grouped by Goal, Board by Status

### 5. Weekly Reviews
- **Properties**: Week (Title, e.g., "W12 2026"), Date Range, Wins (Text), Challenges (Text), Habit Completion Rate (Number, %), Goals Progress Summary (Text), Energy Level (Select: High/Medium/Low), Focus Areas Next Week (Text), Gratitude (Text)
- **Views**: Table (reverse chronological), Gallery

### 6. Accountability Journal
- **Properties**: Date (Title), Morning Intention (Text), Evening Reflection (Text), Top 3 Priorities (Text), Completed (Multi-select), Mood (Select: Energized/Good/Neutral/Low/Struggling), Lesson Learned (Text)
- **Views**: Table, Calendar, Gallery

## Dashboard Page
- **Today's Habits**: Checklist of today's habits with completion status
- **Streak Board**: All active habits with current streak counts (visual)
- **Active Goals**: Progress bars for each goal
- **This Week**: Habit completion rate, top priorities
- **Monthly Trend**: Habit completion % over past 30 days
- **Quick Capture**: Button to log today's habits

## Sample Data
- 8 sample habits (exercise, reading, meditation, journaling, etc.)
- 2 weeks of daily log data
- 3 goals with 9 key results
- 2 weekly review entries
- 5 journal entries
