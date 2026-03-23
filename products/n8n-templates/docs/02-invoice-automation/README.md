# QuickBooks & Stripe Invoice Automation

Automatically sync every Stripe payment to QuickBooks — create invoices, record payments, and log everything. Zero manual bookkeeping.

## What This Workflow Does

1. **Listens for Stripe events** — Catches `invoice.paid`, `invoice.created`, and other invoice events via webhook
2. **Extracts invoice data** — Pulls customer name, email, amount, currency, and line items
3. **Finds or creates QuickBooks customer** — Matches by email; creates new customer if not found
4. **Creates QuickBooks invoice** — With matching line items, amount, and Stripe reference
5. **Records payment** — Marks the invoice as paid in QuickBooks
6. **Logs to Google Sheets** — Complete sync history for audit trail
7. **Slack notification** — Posts a summary to your #accounting channel

## Features

- **Real-time sync** — Processes within seconds of Stripe payment
- **Auto customer creation** — New Stripe customers are created in QuickBooks automatically
- **Deduplication** — Won't create duplicate invoices (matches by Stripe invoice ID)
- **Audit trail** — Full log in Google Sheets with timestamps
- **Slack alerts** — Know instantly when invoices sync
- **Error handling** — Failed syncs are captured and logged
- **Multi-currency** — Passes through whatever currency Stripe uses

## Prerequisites

- n8n (self-hosted or cloud) v1.30+
- Stripe account with webhook access
- QuickBooks Online account with API access
- Google Sheets (for logging)
- Slack workspace (optional, for notifications)

## Quick Start

### 1. Import the Workflow
Open n8n → Add workflow → Import from file → Select `workflow.json`

### 2. Set Up Credentials

| Credential | Type | Notes |
|---|---|---|
| QuickBooks OAuth2 | OAuth2 | [developer.intuit.com](https://developer.intuit.com) |
| Google Sheets | Google Sheets OAuth2 | Auto-configured via Google OAuth |
| Slack | Slack OAuth2 | Optional — for notifications |

### 3. Configure Stripe Webhook
1. Activate the workflow in n8n to get the webhook URL
2. Go to Stripe Dashboard → Developers → Webhooks → Add endpoint
3. Paste the n8n webhook URL
4. Select events: `invoice.paid`, `invoice.payment_succeeded`

### 4. Update QuickBooks Company ID
Replace `YOUR_COMPANY_ID` in all QuickBooks HTTP Request nodes with your actual QuickBooks company ID.

### 5. Create Logging Sheet
Create a Google Sheets spreadsheet with tab "Invoice Log" and headers:

| stripe_invoice_id | customer | email | amount | currency | qb_invoice_id | qb_payment_id | synced_at | status |
|---|---|---|---|---|---|---|---|---|

### 6. Test
Make a test payment in Stripe (use test mode) and verify the workflow processes correctly.

## Customization

- **Remove Slack**: Delete the "Send Slack Notification" node if you don't use Slack
- **Add email receipt**: Add a Gmail/SendGrid node after logging to send confirmation emails
- **Handle refunds**: Add a second webhook path for `charge.refunded` events
- **Xero instead of QuickBooks**: Replace the QuickBooks API calls with Xero API endpoints

## Cost
- Stripe: Free (webhooks are free)
- QuickBooks: Existing subscription
- OpenAI: Not used (no AI needed for this workflow)
- **Total additional cost: $0**

## License
Personal and commercial use. Redistribution prohibited.
