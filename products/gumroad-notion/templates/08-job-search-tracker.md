# 08 — Job Search Tracker

**Template Name (EN):** Job Search Tracker
**Template Name (JP):** 就職活動トラッカー
**Price:** $9
**Target Audience:** Job seekers, career changers, new graduates, anyone actively looking for work

---

## Page Structure

```
Job Search Tracker (Top Page)
├── Dashboard
├── Applications
│   └── Applications DB (linked)
├── Companies
│   └── Companies DB (linked)
├── Contacts & Networking
│   └── Contacts DB (linked)
├── Interview Prep
│   └── Interviews DB (linked)
├── Skills & Resume
│   └── Skills DB (linked)
└── Resources
    └── Resources DB (linked)
```

---

## Database Schemas

### DB1: Applications

| Property | Type | Details |
|----------|------|---------|
| Position | Title | — |
| Company | Relation | → Companies DB |
| Status | Select | `Bookmarked`, `Applied`, `Phone Screen`, `Interview`, `Technical`, `Final Round`, `Offer`, `Rejected`, `Withdrawn`, `Ghosted` |
| Priority | Select | `🔥 Dream Job`, `👍 Good Fit`, `💼 Backup` |
| Salary Range | Rich Text | e.g. "$80K-100K" |
| Location | Rich Text | — |
| Work Type | Select | `Remote`, `Hybrid`, `On-site` |
| Job Type | Select | `Full-time`, `Part-time`, `Contract`, `Freelance`, `Internship` |
| Applied Date | Date | — |
| Source | Select | `LinkedIn`, `Indeed`, `Company Website`, `Referral`, `Recruiter`, `Job Board`, `Networking`, `Other` |
| Job URL | URL | — |
| Resume Version | Rich Text | — |
| Cover Letter | Checkbox | — |
| Contacts | Relation | → Contacts DB |
| Interviews | Relation | → Interviews DB |
| Next Step | Rich Text | — |
| Next Date | Date | — |
| Notes | Rich Text | — |
| Days Since Applied | Formula | `if(empty(prop("Applied Date")), 0, dateBetween(now(), prop("Applied Date"), "days"))` |
| Excitement (1-5) | Number | — |

**Views:**
1. **Pipeline** (Board) — grouped by Status (primary view)
2. **All Applications** (Table) — sorted by Applied Date desc
3. **Active** (Table) — filtered: Status not in [Rejected, Withdrawn, Ghosted]
4. **Calendar** (Calendar) — by Next Date
5. **By Company** (Table) — grouped by Company
6. **Offers** (Table) — filtered: Status = Offer
7. **Stats** (Table) — for tracking response rates

---

### DB2: Companies

| Property | Type | Details |
|----------|------|---------|
| Company Name | Title | — |
| Industry | Select | `Tech`, `Finance`, `Healthcare`, `Education`, `Marketing`, `Consulting`, `Retail`, `Startup`, `Other` |
| Size | Select | `Startup (1-50)`, `Small (51-200)`, `Medium (201-1000)`, `Large (1000+)`, `Enterprise (10000+)` |
| Website | URL | — |
| Glassdoor Rating | Number | — |
| Culture Notes | Rich Text | — |
| Pros | Rich Text | — |
| Cons | Rich Text | — |
| Applications | Relation | → Applications DB |
| Contacts | Relation | → Contacts DB |
| Salary Range | Rich Text | — |
| Interview Process | Rich Text | — |
| Notes | Rich Text | — |

**Views:**
1. **All Companies** (Table)
2. **By Industry** (Table) — grouped by Industry
3. **Top Rated** (Table) — sorted by Glassdoor Rating desc

---

### DB3: Contacts

| Property | Type | Details |
|----------|------|---------|
| Name | Title | — |
| Company | Relation | → Companies DB |
| Title/Role | Rich Text | — |
| Email | Email | — |
| LinkedIn | URL | — |
| Phone | Phone | — |
| Relationship | Select | `Recruiter`, `Hiring Manager`, `Referral`, `Former Colleague`, `Alumni`, `Networking`, `Other` |
| Last Contact | Date | — |
| Next Follow-up | Date | — |
| Applications | Relation | → Applications DB |
| Notes | Rich Text | — |
| Status | Select | `Active`, `Inactive` |

**Views:**
1. **All Contacts** (Table)
2. **Follow-up Due** (Table) — filtered: Next Follow-up <= Today
3. **By Company** (Table) — grouped by Company
4. **Recruiters** (Table) — filtered: Relationship = Recruiter

---

### DB4: Interviews

| Property | Type | Details |
|----------|------|---------|
| Interview | Title | e.g. "Round 1 - Technical" |
| Application | Relation | → Applications DB |
| Type | Select | `Phone Screen`, `Video Call`, `Technical`, `Behavioral`, `Case Study`, `Panel`, `On-site`, `Final` |
| Date | Date | — |
| Time | Rich Text | — |
| Duration | Rich Text | — |
| Interviewer | Rich Text | — |
| Status | Select | `Scheduled`, `Completed`, `Cancelled`, `Rescheduled` |
| Questions Asked | Rich Text | — |
| My Questions | Rich Text | — |
| Performance | Select | `Crushed it`, `Good`, `Okay`, `Could be better`, `Bombed` |
| Feedback | Rich Text | — |
| Follow-up Sent | Checkbox | — |
| Notes | Rich Text | — |

**Views:**
1. **All Interviews** (Table) — sorted by Date
2. **Upcoming** (Table) — filtered: Date >= Today, Status = Scheduled
3. **Calendar** (Calendar) — by Date
4. **By Application** (Table) — grouped by Application

---

### DB5: Skills

| Property | Type | Details |
|----------|------|---------|
| Skill | Title | — |
| Category | Select | `Technical`, `Soft Skill`, `Tool`, `Language`, `Certification` |
| Level | Select | `Beginner`, `Intermediate`, `Advanced`, `Expert` |
| Priority to Improve | Select | `🔴 High`, `🟡 Medium`, `🟢 Low` |
| In Resume | Checkbox | — |
| Notes | Rich Text | — |

**Views:**
1. **All Skills** (Table)
2. **By Category** (Board) — grouped by Category
3. **Resume Skills** (Table) — filtered: In Resume = true
4. **To Improve** (Table) — sorted by Priority

---

### DB6: Resources

| Property | Type | Details |
|----------|------|---------|
| Resource | Title | — |
| Type | Select | `Job Board`, `Resume Tool`, `Interview Prep`, `Networking`, `Salary Info`, `Course`, `Article` |
| URL | URL | — |
| Notes | Rich Text | — |
| Rating | Select | `⭐⭐⭐⭐⭐`, `⭐⭐⭐⭐`, `⭐⭐⭐` |

**Views:**
1. **All Resources** (Table)
2. **By Type** (Board) — grouped by Type

---

## Dashboard Page Layout

1. **Header**: "Job Search HQ — You've got this!"
2. **Application Pipeline** — Applications DB, Board view (all stages)
3. **Key Stats** — Callout: Total Applied / Interviews / Offers / Response Rate
4. **Upcoming Interviews** — Interviews DB, filtered: upcoming (Table, 5)
5. **Follow-ups Due** — Contacts DB, filtered: Follow-up <= Today (Table)
6. **Recent Applications** — Applications DB, sorted by Applied Date desc (Table, 5)
7. **Weekly Goals** — Callout with checkboxes (manual)
8. **Quick Add** — links to create Application, Contact

---

## Pre-filled Sample Data

- 5 sample applications across pipeline stages
- 3 sample companies with research notes
- 4 sample contacts
- 3 sample interviews
- 10 sample skills
- 5 sample resources (real job boards)

---

## Setup Instructions for Buyer

1. Duplicate to workspace
2. Start by researching and adding target companies
3. Track every application immediately after applying
4. Log all networking contacts with follow-up dates
5. Use Interview Prep section before each interview
6. Update the Pipeline Board daily
7. Review weekly stats every Sunday to adjust strategy
8. Customize Status options if needed for your job market
