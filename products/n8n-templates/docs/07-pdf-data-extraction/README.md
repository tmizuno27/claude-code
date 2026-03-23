# PDF & Invoice Data Extraction

Email a PDF invoice → AI extracts all structured data (vendor, amounts, line items, dates) → saves to spreadsheet → optionally creates a QuickBooks bill.

## What This Workflow Does

1. **Receives PDFs** — Via email attachment or file upload webhook
2. **Extracts text** — Built-in n8n PDF extractor
3. **AI structured extraction** — GPT extracts vendor, amounts, dates, line items, tax, currency
4. **Confidence validation** — High confidence → auto-process; Low → flag for human review
5. **Spreadsheet logging** — All extracted data saved to Google Sheets
6. **QuickBooks integration** — Automatically creates bills (optional)

## Prerequisites

- n8n v1.30+, Email with IMAP, OpenAI API key, Google Sheets, QuickBooks (optional), Slack (optional)

## Quick Start

1. Import → Configure credentials
2. Create "Extracted Invoices" sheet with headers: extracted_at, document_type, vendor, invoice_number, invoice_date, due_date, currency, subtotal, tax, total, confidence, source
3. Forward a test invoice to your email
4. Verify extraction accuracy

## Customization

- **Extraction fields**: Edit the AI prompt to add custom fields
- **Confidence threshold**: Adjust the If node (default: 0.6)
- **Accounting software**: Replace QuickBooks with Xero/FreshBooks API
- **Webhook mode**: Use the upload endpoint for direct file processing via API

## Cost: ~$2-5/month (OpenAI)

## License
Personal and commercial use. Redistribution prohibited.
