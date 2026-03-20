# Personal Finance Dashboard - Template Design Specification

## Architecture Overview

- **Databases**: 8
- **Views**: 24
- **Dashboard Pages**: 1 main hub + 6 section pages
- **Sample Data**: Pre-populated with 2 months of realistic example data

---

## DATABASE 1: Transactions

The core database. Every income and expense entry lives here.

### Properties
| Property | Type | Details |
|----------|------|---------|
| Name | Title | Transaction description |
| Amount | Number (USD) | Transaction amount |
| Type | Select | `Income`, `Expense` |
| Category | Relation | Links to Categories DB |
| Date | Date | Transaction date |
| Payment Method | Select | `Cash`, `Debit Card`, `Credit Card`, `Bank Transfer`, `PayPal`, `Other` |
| Account | Relation | Links to Accounts DB |
| Recurring | Checkbox | Is this a recurring transaction? |
| Notes | Rich Text | Optional notes |
| Receipt | Files & Media | Attach receipt photo |

### Views (5)
1. **All Transactions** — Table, sorted by date descending. Default view.
2. **This Month** — Table, filtered to current month. Grouped by Type (Income/Expense).
3. **By Category** — Table, grouped by Category relation. Shows spending patterns.
4. **Income Only** — Table, filtered Type = Income. Sorted by date.
5. **Expenses Only** — Table, filtered Type = Expense. Sorted by date descending.

---

## DATABASE 2: Categories

Spending and income categories for organizing transactions.

### Properties
| Property | Type | Details |
|----------|------|---------|
| Name | Title | Category name |
| Type | Select | `Income`, `Expense` |
| Icon | Rich Text | Emoji for visual identification |
| Transactions | Relation | Back-relation to Transactions DB |
| Total | Rollup | Sum of related transaction amounts |
| Transaction Count | Rollup | Count of related transactions |
| Monthly Budget | Number (USD) | Budgeted amount per month |

### Pre-populated Categories
**Expense**: Housing, Food & Groceries, Transportation, Utilities, Entertainment, Health, Shopping, Education, Personal Care, Gifts, Insurance, Miscellaneous
**Income**: Salary, Freelance, Side Hustle, Investment Returns, Refunds, Other Income

### Views (2)
1. **All Categories** — Table, grouped by Type.
2. **Budget Overview** — Table showing Name, Monthly Budget, Total, with formula for remaining.

---

## DATABASE 3: Subscriptions

Track every recurring subscription with renewal awareness.

### Properties
| Property | Type | Details |
|----------|------|---------|
| Name | Title | Service name |
| Cost | Number (USD) | Per-cycle cost |
| Billing Cycle | Select | `Monthly`, `Quarterly`, `Annual` |
| Next Renewal | Date | Next billing date |
| Category | Select | `Streaming`, `Software`, `Cloud Storage`, `Music`, `Fitness`, `News`, `Gaming`, `Other` |
| Status | Select | `Active`, `Paused`, `Cancelled`, `Trial` |
| Payment Method | Select | Same options as Transactions |
| Annual Cost | Formula | Calculates yearly cost based on cycle |
| Days Until Renewal | Formula | `Next Renewal - today()` |
| Renewal Alert | Formula | Shows warning emoji when renewal is within 7 days |
| URL | URL | Link to manage subscription |
| Notes | Rich Text | Cancel instructions, promo codes, etc. |

### Views (4)
1. **Active Subscriptions** — Table, filtered Status = Active, sorted by Next Renewal.
2. **Renewal Calendar** — Calendar view on Next Renewal date.
3. **By Category** — Table, grouped by Category. Shows cost per category.
4. **Cost Summary** — Board view grouped by Billing Cycle, showing total costs.

---

## DATABASE 4: Savings Goals

Visual goal tracking with progress indicators.

### Properties
| Property | Type | Details |
|----------|------|---------|
| Name | Title | Goal name (e.g., "Emergency Fund") |
| Target Amount | Number (USD) | Goal target |
| Current Amount | Number (USD) | Amount saved so far |
| Progress | Formula | `Current Amount / Target Amount` displayed as percent |
| Progress Bar | Formula | Visual bar using filled/empty blocks |
| Status | Formula | Auto-set: `Not Started` / `In Progress` / `Almost There` (>80%) / `Complete` |
| Deadline | Date | Target completion date |
| Priority | Select | `High`, `Medium`, `Low` |
| Category | Select | `Emergency`, `Travel`, `Purchase`, `Education`, `Retirement`, `Other` |
| Monthly Contribution | Number (USD) | Planned monthly savings |
| Months Remaining | Formula | Calculates months needed at current contribution rate |
| Notes | Rich Text | Strategy notes |
| Contributions | Relation | Links to Savings Contributions DB |

### Views (3)
1. **Dashboard View** — Gallery view showing goal name, progress bar, current/target amounts.
2. **All Goals** — Table sorted by Priority then Deadline.
3. **Completed** — Table filtered to Status = Complete.

---

## DATABASE 5: Savings Contributions

Log individual contributions toward savings goals.

### Properties
| Property | Type | Details |
|----------|------|---------|
| Name | Title | Auto: date + goal name |
| Amount | Number (USD) | Contribution amount |
| Date | Date | Contribution date |
| Goal | Relation | Links to Savings Goals DB |
| Notes | Rich Text | Optional |

### Views (2)
1. **Recent Contributions** — Table sorted by date descending.
2. **By Goal** — Table grouped by Goal relation.

---

## DATABASE 6: Debts

Debt tracking with payoff strategy support.

### Properties
| Property | Type | Details |
|----------|------|---------|
| Name | Title | Debt name (e.g., "Student Loan") |
| Original Balance | Number (USD) | Starting balance |
| Current Balance | Number (USD) | Remaining balance |
| Interest Rate | Number (%) | Annual interest rate |
| Minimum Payment | Number (USD) | Monthly minimum |
| Extra Payment | Number (USD) | Additional monthly payment |
| Total Monthly | Formula | Minimum + Extra |
| Due Date | Number | Day of month payment is due |
| Type | Select | `Credit Card`, `Student Loan`, `Car Loan`, `Mortgage`, `Personal Loan`, `Medical`, `Other` |
| Lender | Rich Text | Lender name |
| Paid Off | Formula | True if Current Balance <= 0 |
| Progress | Formula | `1 - (Current Balance / Original Balance)` as percent |
| Progress Bar | Formula | Visual bar |
| Payoff Date | Formula | Estimated payoff date based on total monthly payment and interest |
| Payments | Relation | Links to Debt Payments DB |

### Views (3)
1. **All Debts** — Table sorted by Interest Rate descending (avalanche order).
2. **Snowball Order** — Table sorted by Current Balance ascending.
3. **Payoff Progress** — Gallery view showing progress bars and estimated payoff dates.

---

## DATABASE 7: Accounts

Bank accounts, wallets, and financial accounts.

### Properties
| Property | Type | Details |
|----------|------|---------|
| Name | Title | Account name |
| Type | Select | `Checking`, `Savings`, `Credit Card`, `Investment`, `Cash`, `Digital Wallet`, `Other` |
| Balance | Number (USD) | Current balance |
| Institution | Rich Text | Bank or institution name |
| Currency | Select | `USD`, `EUR`, `GBP`, `JPY`, `Other` |
| Is Asset | Formula | True if Type is not Credit Card (for net worth calc) |
| Transactions | Relation | Back-relation to Transactions DB |
| Notes | Rich Text | Account details |

### Views (2)
1. **All Accounts** — Table grouped by Type.
2. **Net Worth View** — Table showing assets vs liabilities with balance totals.

---

## DATABASE 8: Monthly Snapshots

Month-end financial snapshots for trend tracking.

### Properties
| Property | Type | Details |
|----------|------|---------|
| Name | Title | "YYYY-MM" format |
| Month | Date | First day of month |
| Total Income | Number (USD) | Month's total income |
| Total Expenses | Number (USD) | Month's total expenses |
| Net Cash Flow | Formula | Income - Expenses |
| Savings Rate | Formula | Net Cash Flow / Total Income as percent |
| Total Assets | Number (USD) | Sum of all asset accounts |
| Total Liabilities | Number (USD) | Sum of all debt balances |
| Net Worth | Formula | Assets - Liabilities |
| Notes | Rich Text | Monthly financial notes/reflections |

### Views (3)
1. **Timeline** — Table sorted by Month descending.
2. **Net Worth Trend** — Table showing Month, Net Worth, change from previous month.
3. **Income vs Expenses** — Table showing Month, Income, Expenses, Net Cash Flow.

---

## PAGE STRUCTURE

### Main Dashboard (Hub Page)
Top-level page the user sees on open.

**Layout:**
- **Header**: Title "Personal Finance Dashboard" + current date + motivational callout
- **Quick Stats Row** (linked database inline):
  - This month's income (green)
  - This month's expenses (red)
  - Net cash flow (green/red)
  - Net worth (from latest snapshot)
- **Section: Recent Transactions** — Inline linked DB, "This Month" view, 10 rows
- **Section: Subscriptions Due Soon** — Inline linked DB, filtered to next 14 days
- **Section: Savings Goals** — Inline linked DB, Gallery view with progress bars
- **Section: Debt Overview** — Inline linked DB, Payoff Progress view
- **Section: Monthly Trend** — Inline linked DB, last 6 snapshots

### Sub-Pages
1. **Transactions** — Full Transactions DB with all views + category breakdown
2. **Budget** — Categories DB Budget Overview + budget vs actual comparison
3. **Subscriptions** — Full Subscriptions DB with all views
4. **Savings Goals** — Goals DB + Contributions DB
5. **Debt Payoff** — Debts DB + strategy guide (snowball vs avalanche explanation)
6. **Net Worth** — Accounts DB + Monthly Snapshots + net worth explanation

---

## FORMULAS

### Subscription Annual Cost
```
if(prop("Billing Cycle") == "Monthly", prop("Cost") * 12,
if(prop("Billing Cycle") == "Quarterly", prop("Cost") * 4,
prop("Cost")))
```

### Subscription Renewal Alert
```
if(dateBetween(prop("Next Renewal"), now(), "days") <= 7, "Warning - Renewing Soon", if(dateBetween(prop("Next Renewal"), now(), "days") <= 0, "OVERDUE", ""))
```

### Savings Progress Bar
```
lets(
pct, if(prop("Target Amount") > 0, prop("Current Amount") / prop("Target Amount"), 0),
filled, floor(pct * 10),
empty, 10 - filled,
replaceAll(replaceAll(slice("@@@@@@@@@@", 0, min(filled, 10)), "@", "█") + replaceAll(slice("@@@@@@@@@@", 0, max(empty, 0)), "@", "░"), "", "")
) + " " + format(round(min(pct, 1) * 100)) + "%"
```

### Debt Payoff Progress
```
if(prop("Original Balance") > 0,
format(round((1 - prop("Current Balance") / prop("Original Balance")) * 100)) + "% paid off",
"N/A")
```

### Monthly Snapshot Savings Rate
```
if(prop("Total Income") > 0,
format(round(prop("Net Cash Flow") / prop("Total Income") * 100)) + "%",
"N/A")
```

---

## SAMPLE DATA

Pre-populate with 2 months of realistic data:

**Accounts**: Main Checking ($3,240), Savings ($8,500), Credit Card (-$1,200), Investment ($15,000), Cash ($120)

**Transactions**: ~40 sample entries across both months covering salary, groceries, rent, utilities, dining, subscriptions, freelance income

**Subscriptions**: Netflix ($15.49/mo), Spotify ($10.99/mo), Notion ($10/mo), iCloud ($2.99/mo), Gym ($35/mo), Adobe ($22.99/mo), ChatGPT Plus ($20/mo)

**Savings Goals**: Emergency Fund ($10,000 target, $6,200 current), Vacation ($2,500 target, $800 current), New Laptop ($1,500 target, $400 current)

**Debts**: Credit Card ($1,200, 22.99%), Student Loan ($18,500, 5.5%), Car Loan ($8,200, 4.9%)

**Monthly Snapshots**: 2 months showing income, expenses, and net worth progression
