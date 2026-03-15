# Email Classification & Auto-Routing

AI classifies every incoming email by category, priority, and sentiment — then routes it automatically: spam → trash, urgent → Slack alert, invoices → accounting, clients → labeled.

## What This Workflow Does

1. **Monitors inbox** — IMAP trigger checks for new emails
2. **AI classification** — Category, priority, sentiment, spam detection, suggested action
3. **Spam filtering** — Auto-moves spam to spam folder
4. **Smart routing** — Urgent → Slack, Invoice → forward to accounting, Client → label
5. **Logging** — Full classification history in Google Sheets

## Prerequisites

- n8n v1.30+, Email with IMAP, OpenAI API key, Gmail (for labeling/forwarding), Slack, Google Sheets

## Quick Start

1. Import → Configure IMAP and other credentials
2. Create Gmail labels: "Client", or use existing ones
3. Create "Email Log" sheet with headers: date, from, subject, category, priority, action, summary
4. Set your accounting email in the "Forward to Accounting" node
5. Test with a few sample emails

## Customization

- **Categories**: Edit the classification prompt to add/change categories
- **Routing rules**: Add more outputs to the Switch node
- **Auto-reply**: Add a Gmail send node for certain categories
- **Multiple inboxes**: Duplicate the IMAP trigger for different accounts

## Cost: ~$2-5/month (OpenAI)

## License
Personal and commercial use. Redistribution prohibited.
