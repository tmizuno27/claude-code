# Shopify Order Automation

New Shopify order → log to spreadsheet, send personalized thank-you email, flag high-value orders, check inventory, and auto-tag in Shopify.

## What This Workflow Does

1. **Order trigger** — Fires on every new Shopify order
2. **High-value detection** — Orders over $500 flagged for manual review via Slack
3. **Order logging** — All orders recorded in Google Sheets
4. **Thank-you email** — Personalized confirmation with order summary
5. **Inventory alerts** — Checks stock and alerts on low inventory
6. **Auto-tagging** — Tags processed orders in Shopify

## Prerequisites

- n8n v1.30+, Shopify store, Gmail, Google Sheets, Slack

## Quick Start

1. Import → Configure Shopify, Gmail, Sheets, and Slack credentials
2. Create "Orders" sheet with headers: order_number, date, customer, email, total, currency, items, status, fulfillment
3. Set the high-value threshold in "Fraud Risk Check" (default: $500)
4. Place a test order

## Customization

- **Threshold**: Change the $500 limit for high-value alerts
- **Thank-you email**: Customize the template with your brand voice
- **Fulfillment**: Add shipping label creation nodes (ShipStation, EasyPost)
- **Inventory threshold**: Add a condition to only alert when stock < X

## Cost: $0 additional (no AI needed)

## License
Personal and commercial use. Redistribution prohibited.
