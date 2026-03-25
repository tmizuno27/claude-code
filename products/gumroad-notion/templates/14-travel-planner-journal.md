# Template Design — Travel Planner & Journal

## Overview
Plan trips from start to finish and document memories along the way. Covers itineraries, packing lists, budgets, bookings, and travel journals with photo galleries.

## Price: $12

## Databases

### 1. Trips
- **Properties**: Trip Name (Title), Destination, Start Date, End Date, Duration (Formula), Status (Select: Planning/Booked/In Progress/Completed/Wishlist), Budget, Actual Spend (Rollup from Expenses), Travel Partners, Cover Image (Files), Rating (Select: 1-5 stars), Notes
- **Views**: Gallery (with cover images), Board by Status, Calendar, Table

### 2. Itinerary
- **Properties**: Activity (Title), Trip (Relation→Trips), Date, Start Time, End Time, Location, Category (Select: Flight/Hotel/Restaurant/Activity/Transport/Meeting/Free Time), Booking Reference, Cost, Confirmed (Checkbox), Notes, Map Link
- **Views**: Table grouped by Date, Calendar, Board by Category

### 3. Packing List
- **Properties**: Item (Title), Trip (Relation→Trips), Category (Select: Clothing/Toiletries/Electronics/Documents/Medicine/Other), Packed (Checkbox), Quantity (Number), Notes
- **Views**: Board by Category, Checklist (sorted by Packed status)
- **Pre-populated with 50+ essential items template**

### 4. Expenses
- **Properties**: Description (Title), Trip (Relation→Trips), Category (Select: Flight/Hotel/Food/Transport/Activity/Shopping/Insurance/Other), Amount, Currency, Amount USD (Formula with exchange rate), Date, Payment Method, Receipt (Files), Notes
- **Views**: Table grouped by Category, Summary (total per category), Calendar

### 5. Travel Journal
- **Properties**: Entry Title (Title), Trip (Relation→Trips), Date, Location, Content (Text — rich text for journal entry), Photos (Files), Mood (Select: Amazing/Great/Good/Okay/Tough), Weather, Highlight of the Day, Notes
- **Views**: Gallery (photo journal), Table by Date, Board by Trip

### 6. Bookings
- **Properties**: Booking Name (Title), Trip (Relation→Trips), Type (Select: Flight/Hotel/Car Rental/Tour/Restaurant/Insurance), Confirmation Number, Check-in Date, Check-out Date, Cost, Status (Select: Confirmed/Pending/Cancelled), Provider, Contact Info, Documents (Files)
- **Views**: Table grouped by Type, Calendar, Board by Status

## Dashboard Page
- **Upcoming Trips**: Next planned trips with countdown
- **Current Trip**: Active itinerary for today
- **Trip Stats**: Countries visited, Total trips, Average trip rating
- **Wishlist**: Dream destinations
- **Recent Memories**: Latest journal entries with photos
- **Packing Status**: Ready/Not ready for upcoming trip

## Sample Data
- 2 sample trips (Tokyo 7-day, Barcelona weekend)
- Full itinerary for Tokyo trip
- Packing list template (50+ items)
- 3 journal entries with placeholder photos
- 5 sample bookings
