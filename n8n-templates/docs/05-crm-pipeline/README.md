# CRM Pipeline Automation

Auto-create HubSpot contacts and deals from form submissions, AI-score leads (hot/warm/cold), route to the right action, and track stale deals.

## What This Workflow Does

1. **New lead intake** — Webhook receives form submissions
2. **HubSpot contact + deal creation** — Automatic upsert
3. **AI lead scoring** — GPT scores 1-100 based on email domain, title, company, message
4. **Smart routing** — Hot → Slack alert, Warm → nurture email, Cold → drip sequence
5. **Payment tracking** — Stripe webhook updates deal to "Closed Won"
6. **Stale deal alerts** — Daily check for stuck deals

## Prerequisites

- n8n v1.30+, HubSpot account, OpenAI API key, Gmail, Slack, Google Sheets

## Quick Start

1. Import → Configure credentials
2. Connect your website form to the webhook URL
3. Set up Stripe webhook for payment events
4. Create "Drip Queue" sheet with headers: email, name, drip_stage, next_send

## Customization

- **Scoring criteria**: Edit the AI prompt in "Score Lead with AI"
- **Routing thresholds**: Adjust the Switch node conditions
- **CRM**: Replace HubSpot nodes with Salesforce/Pipedrive
- **Nurture emails**: Customize the email template in "Send Nurture Email"

## Cost: ~$2-5/month (OpenAI only; HubSpot free CRM)

## License
Personal and commercial use. Redistribution prohibited.
