# Zapier-to-n8n Migration Kit (Top 5 Zaps)

The 5 most popular Zapier automations, rebuilt natively for n8n. Drop-in replacements that save you $20-100+/month in Zapier fees.

## Included Workflows

| # | Zapier Equivalent | n8n Replacement |
|---|---|---|
| 1 | Gmail → Google Sheets | New email → log to spreadsheet |
| 2 | Typeform → Slack + Gmail | Form submission → notify team + send confirmation |
| 3 | Stripe → QuickBooks | Payment received → create invoice |
| 4 | RSS → Twitter + LinkedIn | New article → post to social media |
| 5 | Webhook → HubSpot | Inbound lead → create CRM contact + notify sales |

## Why Switch from Zapier?

- **No per-task pricing** — n8n charges by workflow, not by step
- **Self-hostable** — your data stays on your servers
- **More powerful** — branching, looping, code nodes, AI nodes built-in
- **Open source** — no vendor lock-in
- **Savings**: Typical Zapier bill for these 5 zaps = $49-149/month → **$0 with self-hosted n8n**

## Prerequisites

- n8n v1.30+
- Credentials for the services you use (Gmail, Sheets, Slack, Stripe, QuickBooks, Twitter, LinkedIn, HubSpot)

## Quick Start

1. Import `workflow.json` into n8n
2. Each "Zap" is an independent sub-workflow — activate only the ones you need
3. Configure credentials for each active sub-workflow
4. Set up webhooks in Stripe/Typeform dashboard where applicable
5. Test each flow individually

## Customization

Each sub-workflow is intentionally simple and mirrors the Zapier equivalent. You can extend any of them:
- Add AI processing (classification, summarization)
- Add conditional logic (branching)
- Chain multiple actions
- Add error handling

## Cost: $0 additional (no AI needed)

## License
Personal and commercial use. Redistribution prohibited.
