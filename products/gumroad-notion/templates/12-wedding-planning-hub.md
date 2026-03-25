# Template Design — Wedding Planning Hub

## Overview
All-in-one wedding planning command center in Notion. Manage every detail from engagement to honeymoon: guest list, budget, vendors, timeline, seating, and more.

## Price: $17

## Databases

### 1. Guest List
- **Properties**: Name (Title), Party Size (Number), RSVP Status (Select: Invited/Confirmed/Declined/Pending), Side (Select: Bride/Groom/Mutual), Meal Choice (Select: Standard/Vegetarian/Vegan/Gluten-Free/Kids), Table Number (Number), Email, Phone, Address (for invitations), Gift Received (Checkbox), Thank You Sent (Checkbox), Notes
- **Views**: Table (all guests), Board by RSVP Status, Filtered by Side, Filtered by Meal Choice
- **Rollups**: Total confirmed, Total declined, Pending count

### 2. Budget Tracker
- **Properties**: Item (Title), Category (Select: Venue/Catering/Photography/Flowers/Music/Attire/Decor/Stationery/Transportation/Honeymoon/Other), Estimated Cost, Actual Cost, Deposit Paid, Balance Due, Vendor (Relation→Vendors), Due Date, Status (Select: Planned/Booked/Paid/Cancelled), Notes
- **Views**: Table grouped by Category, Summary (total budget vs actual), Calendar by Due Date

### 3. Vendors
- **Properties**: Vendor Name (Title), Category (Multi-select), Contact Person, Phone, Email, Website, Price Quote, Booked (Checkbox), Contract Signed (Checkbox), Rating (Select: 1-5 stars), Notes, Meeting Notes (Text)
- **Views**: Table, Board by Category, Filtered (Booked only)

### 4. Timeline & Tasks
- **Properties**: Task (Title), Phase (Select: 12 Months Out/9 Months/6 Months/3 Months/1 Month/1 Week/Day Of/After Wedding), Due Date, Status (Select: To Do/In Progress/Done), Assigned To (Select: Bride/Groom/Planner/Other), Priority, Notes
- **Views**: Timeline, Board by Phase, Board by Status, Calendar
- **Pre-populated with 100+ tasks across all phases**

### 5. Seating Chart
- **Properties**: Table Number (Title), Capacity (Number), Guests (Relation→Guest List), Theme/Name, Notes
- **Views**: Table View, Gallery View

### 6. Inspiration Board
- **Properties**: Item (Title), Category (Select: Venue/Dress/Flowers/Cake/Decor/Color Palette/Music), Image (Files), Source URL, Notes, Favorite (Checkbox)
- **Views**: Gallery by Category, Favorites filter

## Dashboard Page
- **Countdown**: Days until wedding (formula)
- **Quick Stats**: Confirmed guests, Budget remaining, Tasks completed %, Vendors booked
- **RSVP Summary**: Visual breakdown
- **Upcoming Tasks**: Next 5 due tasks
- **Budget Overview**: Spent vs Remaining pie-chart style breakdown

## Sample Data
- 30 sample guests with varied RSVP statuses
- 15 budget items across categories (~$15,000 budget example)
- 5 sample vendors
- 100+ pre-populated tasks across all phases
