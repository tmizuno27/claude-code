# Notion Template Design — Travel Planner & Journal

## Architecture Overview

The template is built around a **Trip Dashboard** page that connects 8 databases via relations. Every database links back to the core Trips DB so all data is scoped per trip.

---

## Databases (8)

### 1. Trips DB
| Property | Type | Details |
|----------|------|---------|
| Trip Name | Title | e.g., "Japan Spring 2026" |
| Destination | Text | City/Country |
| Status | Select | Planning / Booked / In Progress / Completed / Cancelled |
| Start Date | Date | Trip start |
| End Date | Date | Trip end |
| Travel Companions | Multi-select | Names |
| Cover Image | Files | Hero photo |
| Trip Type | Select | Solo / Couple / Family / Group / Business |
| Notes | Text | General notes |
| Budget (Target) | Number | Total budget in home currency |
| Home Currency | Select | USD / EUR / JPY / GBP / AUD / BRL / PYG |

**Formulas:**
- Days Until: `dateBetween(prop("Start Date"), now(), "days")`
- Trip Duration: `dateBetween(prop("End Date"), prop("Start Date"), "days") + 1`
- Total Spent: Rollup from Expenses DB (sum of Home Amount)
- Budget Remaining: Budget (Target) - Total Spent
- Budget Status: If remaining > 0 "On Track" else "Over Budget"

### 2. Itinerary DB
| Property | Type | Details |
|----------|------|---------|
| Activity | Title | e.g., "Visit Fushimi Inari" |
| Trip | Relation | -> Trips DB |
| Date | Date | Day of activity |
| Start Time | Text | "09:00" |
| End Time | Text | "12:00" |
| Location | Text | Address or place name |
| Map Link | URL | Google Maps link |
| Category | Select | Sightseeing / Food / Transport / Shopping / Adventure / Relaxation / Culture |
| Status | Select | Planned / Confirmed / Done / Skipped |
| Cost Estimate | Number | Estimated cost |
| Notes | Text | Details, tips |
| Priority | Select | Must-do / Nice-to-have / Optional |

### 3. Packing DB
| Property | Type | Details |
|----------|------|---------|
| Item | Title | e.g., "Passport" |
| Trip | Relation | -> Trips DB |
| Category | Select | Documents / Clothing / Toiletries / Electronics / Medicine / Gear / Misc |
| Trip Type Tag | Multi-select | Beach / City / Hiking / Winter / Business |
| Packed | Checkbox | ✓ when packed |
| Quantity | Number | Default 1 |
| Essential | Checkbox | Cannot forget |

### 4. Expenses DB
| Property | Type | Details |
|----------|------|---------|
| Expense | Title | e.g., "Lunch at ramen shop" |
| Trip | Relation | -> Trips DB |
| Date | Date | Date of expense |
| Category | Select | Accommodation / Food / Transport / Activities / Shopping / Insurance / Visa / Other |
| Local Amount | Number | Amount in local currency |
| Local Currency | Select | USD / EUR / JPY / etc. |
| Exchange Rate | Number | Rate to home currency |
| Home Amount | Formula | `prop("Local Amount") * prop("Exchange Rate")` |
| Payment Method | Select | Cash / Credit Card / Debit / Mobile Pay |
| Receipt | Files | Photo of receipt |
| Notes | Text | |

### 5. Accommodation DB
| Property | Type | Details |
|----------|------|---------|
| Name | Title | e.g., "Shinjuku Granbell Hotel" |
| Trip | Relation | -> Trips DB |
| Type | Select | Hotel / Hostel / Airbnb / Couchsurfing / Camping / Other |
| Check-in | Date | |
| Check-out | Date | |
| Price per Night | Number | |
| Currency | Select | |
| Total Price | Formula | `dateBetween(prop("Check-out"), prop("Check-in"), "days") * prop("Price per Night")` |
| Location | Text | Address |
| Map Link | URL | |
| Booking Link | URL | |
| Rating | Select | 1-5 stars |
| Amenities | Multi-select | WiFi / Kitchen / AC / Pool / Laundry / Parking / Breakfast |
| Status | Select | Researching / Booked / Stayed / Cancelled |
| Notes | Text | Pros/cons |

### 6. Journal DB
| Property | Type | Details |
|----------|------|---------|
| Entry Title | Title | e.g., "Day 3 — Lost in Kyoto" |
| Trip | Relation | -> Trips DB |
| Date | Date | |
| Mood | Select | Amazing / Good / Okay / Tough / Terrible |
| Highlight | Text | Best moment of the day |
| Photos | Files | Multiple photos |
| Rating | Select | 1-5 stars |
| Weather | Select | Sunny / Cloudy / Rainy / Snowy / Hot / Cold |
| Body | Text | Full journal entry (page content) |

### 7. Bucket List DB
| Property | Type | Details |
|----------|------|---------|
| Destination | Title | e.g., "Patagonia, Argentina" |
| Region | Select | Asia / Europe / Americas / Africa / Oceania / Middle East |
| Priority | Select | Dream / High / Medium / Low |
| Best Season | Multi-select | Spring / Summer / Fall / Winter |
| Estimated Budget | Number | |
| Trip Duration (days) | Number | Ideal length |
| Status | Select | Dream / Researching / Planned / Visited |
| Trip Link | Relation | -> Trips DB (when visited) |
| Why I Want to Go | Text | |
| Cover Image | Files | Inspiration photo |

### 8. Documents DB
| Property | Type | Details |
|----------|------|---------|
| Document | Title | e.g., "Passport" |
| Trip | Relation | -> Trips DB |
| Type | Select | Passport / Visa / Insurance / Booking Confirmation / Emergency Contact / Vaccination / Other |
| Number | Text | Document number |
| Expiry Date | Date | |
| File | Files | Scan/photo |
| Notes | Text | |

---

## Views (22)

### Trip Dashboard (main page, not a DB view)
- Callout block: welcome message + quick stats (inline DB queries)
- Linked view: Trips DB — Gallery, filtered to Status != Completed, sorted by Start Date
- Linked view: Trips DB — Gallery, filtered to Status = Completed (travel history)
- Linked view: Bucket List DB — Gallery, sorted by Priority

### Trips DB Views
1. **All Trips — Table**: Default table, all properties
2. **Upcoming — Gallery**: Filter Status = Planning or Booked, sort by Start Date asc, cover image
3. **Timeline — Timeline**: By Start Date to End Date
4. **By Status — Board**: Group by Status

### Itinerary DB Views
5. **Daily Schedule — Table**: Filter by Trip, sort by Date then Start Time
6. **By Category — Board**: Group by Category
7. **Calendar — Calendar**: By Date
8. **Must-Do List — List**: Filter Priority = Must-do

### Packing DB Views
9. **Checklist — Table**: Filter by Trip, group by Category, show Packed checkbox prominently
10. **Unpacked Only — Table**: Filter Packed = unchecked
11. **By Trip Type — Board**: Group by Trip Type Tag

### Expenses DB Views
12. **All Expenses — Table**: Filter by Trip, sort by Date desc
13. **By Category — Board**: Group by Category, show sum of Home Amount
14. **Daily Spending — Table**: Group by Date, show sum
15. **Calendar — Calendar**: By Date

### Accommodation DB Views
16. **Comparison Table — Table**: All properties visible, sort by Price per Night
17. **By Status — Board**: Group by Status
18. **Map Links — List**: Show Name + Map Link only

### Journal DB Views
19. **Timeline — Gallery**: Sort by Date, show cover photo, mood, highlight
20. **Photo Wall — Gallery**: Large thumbnails, photos as cover

### Bucket List DB Views
21. **Dream Board — Gallery**: Cover images, group by Region
22. **Priority Ranked — Table**: Sort by Priority, show Estimated Budget

---

## Dashboard Page Structure

```
Travel Planner & Journal
├── Header: Cover image (world map), icon (airplane emoji), title
├── Callout: "Welcome to your travel command center!"
├── Toggle: Quick Links
│   ├── Button: + New Trip
│   ├── Button: Packing Templates
│   └── Button: Bucket List
├── Section: UPCOMING TRIPS
│   └── Linked DB: Trips — Gallery (Upcoming)
├── Section: CURRENT TRIP (if any)
│   ├── Linked DB: Itinerary — Daily Schedule (filtered to current trip)
│   ├── Linked DB: Expenses — By Category (filtered to current trip)
│   └── Linked DB: Packing — Checklist (filtered to current trip)
├── Section: BUCKET LIST
│   └── Linked DB: Bucket List — Dream Board
├── Section: TRAVEL HISTORY
│   └── Linked DB: Trips — Gallery (Completed)
├── Divider
└── Section: DOCUMENTS & INFO
    └── Linked DB: Documents — Table
```

---

## Relations Map

```
Trips DB (central)
├── <- Itinerary DB (many-to-one)
├── <- Packing DB (many-to-one)
├── <- Expenses DB (many-to-one)
├── <- Accommodation DB (many-to-one)
├── <- Journal DB (many-to-one)
├── <- Documents DB (many-to-one)
└── <- Bucket List DB (one-to-one, optional, when visited)
```

---

## Sample Data (pre-loaded)

### Sample Trip: "Tokyo & Kyoto Adventure"
- Status: Planning
- Dates: 2026-05-01 to 2026-05-10
- Type: Solo
- Budget: $2,500 USD

### Sample Itinerary (3 days)
| Day | Activity | Time | Category |
|-----|----------|------|----------|
| Day 1 | Arrive Narita, train to Shinjuku | 14:00-17:00 | Transport |
| Day 1 | Explore Shinjuku Gyoen | 17:30-19:00 | Sightseeing |
| Day 1 | Dinner at Omoide Yokocho | 19:30-21:00 | Food |
| Day 2 | Tsukiji Outer Market breakfast | 07:00-08:30 | Food |
| Day 2 | TeamLab Borderless | 10:00-12:30 | Culture |
| Day 2 | Shibuya crossing & Harajuku | 13:00-17:00 | Sightseeing |
| Day 3 | Shinkansen to Kyoto | 08:00-10:15 | Transport |
| Day 3 | Fushimi Inari shrine | 11:00-13:00 | Sightseeing |
| Day 3 | Nishiki Market lunch | 13:30-15:00 | Food |

### Sample Packing (Beach preset)
- Passport, Sunscreen SPF50, Swimsuit, Flip flops, Sunglasses, Beach towel, Waterproof phone case, Charger, First aid kit, Travel adapter

### Sample Expenses (5 entries)
| Expense | Category | Local | Currency | Rate | Home |
|---------|----------|-------|----------|------|------|
| Narita Express | Transport | 3,250 | JPY | 0.0067 | $21.78 |
| Hotel night 1 | Accommodation | 12,000 | JPY | 0.0067 | $80.40 |
| Ramen dinner | Food | 1,100 | JPY | 0.0067 | $7.37 |
| Tsukiji sushi | Food | 3,500 | JPY | 0.0067 | $23.45 |
| TeamLab ticket | Activities | 3,800 | JPY | 0.0067 | $25.46 |

### Sample Bucket List (5 entries)
| Destination | Region | Priority | Best Season | Budget |
|-------------|--------|----------|-------------|--------|
| Patagonia, Argentina | Americas | Dream | Fall | $3,000 |
| Iceland Ring Road | Europe | High | Summer | $4,000 |
| Bali, Indonesia | Asia | Medium | Spring | $1,500 |
| Morocco | Africa | High | Fall | $2,000 |
| New Zealand | Oceania | Dream | Summer | $5,000 |

### Sample Journal Entry
- Title: "Day 1 — First Steps in Tokyo"
- Mood: Amazing
- Highlight: "Watching the sunset over Shinjuku from the park while cherry blossoms drifted down"
- Weather: Sunny
- Rating: 5 stars

---

## Packing Presets (toggle blocks)

Each preset is a toggle block users can expand and duplicate items from:

- **Beach Trip**: Swimsuit, sunscreen, sunglasses, flip flops, beach towel, hat, aloe vera, waterproof bag
- **City Trip**: Walking shoes, umbrella, day bag, power bank, guidebook, smart casual outfit
- **Hiking Trip**: Hiking boots, rain jacket, water bottle, trail snacks, headlamp, first aid kit, trekking poles
- **Winter Trip**: Thermal base layers, down jacket, gloves, beanie, hand warmers, waterproof boots, lip balm
- **Business Trip**: Suit/blazer, dress shoes, laptop, business cards, portable charger, iron/steamer
