# Template Design — Property Investment Tracker

## Overview
Notion template for real estate investors to track their property portfolio, rental income, expenses, ROI, and tenant management. Designed for both beginner and experienced investors with 1-50+ properties.

## Price: $19

## Databases

### 1. Properties
- **Properties**: Property Name (Title), Address, Type (Select: Single Family/Multi-Family/Condo/Commercial/Vacant Land), Purchase Date, Purchase Price, Current Value, Equity (Formula: Current Value - Mortgage Balance), Status (Select: Owned/Under Contract/Sold/Prospecting), Mortgage Balance, Monthly Mortgage Payment, Insurance (Monthly), Property Tax (Monthly), HOA (Monthly), Total Monthly Costs (Formula), Notes
- **Views**: Table View, Board by Status, Map-style Gallery, Summary (Portfolio Total Value)

### 2. Rental Income
- **Properties**: Property (Relation→Properties), Tenant (Relation→Tenants), Month (Date), Rent Amount, Received (Checkbox), Received Date, Late (Formula: Received Date > Due Date), Notes
- **Views**: Table grouped by Property, Calendar, Monthly Summary (rollup)

### 3. Expenses
- **Properties**: Property (Relation→Properties), Description (Title), Category (Select: Repair/Maintenance/Capital Improvement/Insurance/Tax/Utilities/Management/Legal/Other), Amount, Date, Tax Deductible (Checkbox), Receipt (Files), Vendor, Notes
- **Views**: Table grouped by Category, Table grouped by Property, Calendar, Tax Deductible filter

### 4. Tenants
- **Properties**: Name (Title), Property (Relation→Properties), Lease Start, Lease End, Monthly Rent, Deposit Amount, Phone, Email, Emergency Contact, Status (Select: Active/Past/Prospective), Notes
- **Views**: Table, Board by Status, Lease Expiration Calendar

### 5. Mortgage Tracker
- **Properties**: Property (Relation→Properties), Lender, Interest Rate, Loan Amount, Term (Years), Monthly Payment (Formula), Remaining Balance, Start Date, Notes
- **Views**: Table, Summary (Total Debt, Average Rate)

### 6. Deal Analyzer
- **Properties**: Property Name (Title), Asking Price, Estimated Rent, Monthly Expenses (Estimate), Cap Rate (Formula), Cash-on-Cash Return (Formula), 1% Rule Pass (Formula: Rent >= 1% of Price), NOI (Formula), Status (Select: Analyzing/Offer Made/Passed), Notes
- **Views**: Table sorted by Cap Rate, Board by Status

## Dashboard Page
- **Portfolio Summary**: Total properties, Total value, Total equity, Total monthly income, Total monthly expenses, Net monthly cash flow
- **Cash Flow**: Monthly income vs expenses
- **ROI Metrics**: Portfolio-wide cap rate, cash-on-cash return
- **Upcoming**: Lease expirations, Upcoming expenses, Late rent alerts
- **Deal Pipeline**: Properties being analyzed

## Sample Data
- 3 sample properties (single family, condo, duplex)
- 6-month income history
- 10 expense entries
- 3 tenants with active leases
- 2 deals in analysis pipeline
