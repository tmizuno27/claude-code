# Template Design — Startup Launch Checklist

## Overview
A comprehensive Notion template for first-time founders and indie hackers to go from idea to launch systematically. Covers validation, MVP, launch, and post-launch growth.

## Price: $12

## Databases

### 1. Launch Phases
- **Properties**: Phase Name (Title), Status (Select: Not Started/In Progress/Done), Start Date, Due Date, Progress (Formula: % of completed tasks), Priority (Select: Critical/High/Medium/Low)
- **Views**: Timeline View (Gantt-style), Board View (by Status), Table View (all phases)
- **Default Phases**: Idea Validation, Market Research, MVP Build, Beta Testing, Pre-Launch, Launch Day, Post-Launch

### 2. Tasks
- **Properties**: Task Name (Title), Phase (Relation→Launch Phases), Status (Select: To Do/In Progress/Done/Blocked), Owner (Person), Due Date, Priority, Category (Select: Product/Marketing/Legal/Finance/Tech), Notes (Text), Completed Date
- **Views**: Board by Status, Board by Phase, Calendar, Filtered by Category
- **Pre-populated with 80+ launch tasks across all phases**

### 3. Competitor Analysis
- **Properties**: Company Name (Title), URL, Category (Multi-select), Pricing Model, Strengths (Text), Weaknesses (Text), Threat Level (Select: High/Medium/Low), Notes
- **Views**: Table View, Gallery View with notes

### 4. Budget Tracker
- **Properties**: Item (Title), Category (Select: Development/Marketing/Legal/Design/Tools/Other), Estimated Cost, Actual Cost, Status (Select: Planned/Paid/Cancelled), Date, Notes
- **Views**: Table grouped by Category, Summary with rollups (Total Estimated vs Actual)

### 5. Metrics Dashboard
- **Properties**: Metric Name (Title), Category (Select: Acquisition/Activation/Revenue/Retention/Referral), Current Value, Target Value, Date Updated, Trend (Select: Up/Down/Flat)
- **Views**: Table View, Board by Category

### 6. Launch Day Checklist
- **Properties**: Task (Title), Time Slot (Select: Pre-Launch/Morning/Midday/Evening/Post-Launch), Status (Checkbox), Assigned To, Notes
- **Views**: Table sorted by Time Slot

## Relations & Rollups
- Tasks → Launch Phases (rollup: completion percentage)
- Budget → Launch Phases (rollup: total cost per phase)

## Dashboard Page
- **Header**: Startup name, tagline, launch date countdown (formula)
- **Quick Stats**: Total tasks (done/total), budget (spent/planned), days until launch
- **Active Phase**: Current phase with linked tasks
- **Recent Activity**: Last 5 completed tasks
- **Links to all databases**

## Sample Data
- Example SaaS startup "TaskFlow" — AI-powered project management tool
- 80+ pre-populated tasks across 7 phases
- 5 sample competitors
- Budget items totaling ~$2,000 bootstrapped launch
