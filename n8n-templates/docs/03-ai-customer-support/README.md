# AI Customer Support Agent

AI-powered support system that reads incoming emails/chats, classifies tickets by category and urgency, auto-replies when confident, and escalates to humans when needed.

## What This Workflow Does

1. **Receives support messages** — Via email (IMAP) or chat widget (webhook)
2. **AI classifies** — Category (billing/technical/account/etc.), urgency, sentiment, and whether human review is needed
3. **Searches knowledge base** — Finds relevant articles to ground the AI response
4. **Generates AI reply** — Personalized, empathetic response based on KB results
5. **Confidence check** — High confidence → auto-send; Low confidence → escalate to Slack
6. **Logs everything** — Full ticket history in Google Sheets

## Prerequisites

- n8n v1.30+
- Email account with IMAP access (or Gmail)
- OpenAI API key
- Google Sheets
- Slack (for escalations)
- Knowledge base API (optional — can use a simple Google Sheet as KB)

## Quick Start

1. Import `workflow.json` into n8n
2. Configure IMAP credentials for your support email
3. Set up OpenAI, Gmail, Google Sheets, and Slack credentials
4. Create a "Support Tickets" sheet with headers: timestamp, customer_email, customer_name, category, urgency, sentiment, summary, auto_replied, source
5. Test with a sample email

## Customization

- **Classification categories**: Edit the "Classify Ticket" node prompt
- **Escalation rules**: Edit the system message (e.g., always escalate refunds over $X)
- **Knowledge base**: Replace the HTTP Request node with your own KB API, or use a Google Sheet lookup
- **Auto-reply tone**: Edit the "Generate AI Reply" system message
- **Add chat widget**: Use the webhook URL in your website's chat widget

## Cost Estimate

| Service | Monthly Cost |
|---|---|
| OpenAI (GPT-4o-mini) | ~$5-15 (depends on volume) |
| Gmail/IMAP | Free |
| Google Sheets | Free |
| Slack | Free |

## License
Personal and commercial use. Redistribution prohibited.
