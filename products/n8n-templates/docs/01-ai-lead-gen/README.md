# AI Lead Gen & Cold Outreach Automation

Automatically find, research, and contact potential leads with AI-personalized cold emails — then follow up if they don't reply.

## What This Workflow Does

1. **Finds Leads** — Pulls prospects from Apollo.io or Hunter.io based on your target criteria (job titles, industries, company size)
2. **Deduplicates** — Checks against your Google Sheets CRM to avoid contacting the same person twice
3. **AI Research** — Uses GPT-4o-mini to analyze each prospect's company, identify pain points, and find personalization hooks
4. **AI Email Writing** — Generates a unique, personalized cold email for each lead (subject + body)
5. **Sends or Drafts** — Either auto-sends via Gmail or creates drafts for your review
6. **Logs Everything** — Records all outreach in Google Sheets (your lightweight CRM)
7. **Auto Follow-Up** — Waits 3 days, checks for replies, and sends a follow-up if no response

## Features

- **Dual lead source support** — Apollo.io (best for B2B) and Hunter.io (best for domain-based search)
- **AI-powered personalization** — Every email is unique, researched, and relevant
- **Spam-safe** — AI follows strict anti-spam rules (no trigger words, short emails, text-only)
- **Draft mode** — Review emails before sending (recommended for first run)
- **Auto follow-up** — 3-day wait + reply detection + automatic follow-up
- **CRM logging** — Full outreach history in Google Sheets
- **Daily limit** — Configurable cap to protect your sender reputation
- **Schedule or manual trigger** — Runs daily at 9 AM or on-demand

## Prerequisites

- **n8n** (self-hosted or cloud) — v1.30+
- **Apollo.io API key** (free tier: 50 credits/month) or **Hunter.io API key** (free tier: 25 searches/month)
- **OpenAI API key** (GPT-4o-mini costs ~$0.15/1M input tokens)
- **Gmail account** with OAuth2 configured in n8n
- **Google Sheets** — one spreadsheet for CRM tracking

## Quick Start

### 1. Import the Workflow

1. Open n8n
2. Click **"Add workflow"** → **"Import from file"**
3. Select `workflow.json`

### 2. Set Up Credentials

Create these credentials in n8n (Settings → Credentials):

| Credential | Type | Where to Get |
|---|---|---|
| Apollo API Key | HTTP Header Auth | [apollo.io/settings/api](https://app.apollo.io/settings/api) |
| Hunter.io API Key | HTTP Query Auth | [hunter.io/api](https://hunter.io/api) |
| OpenAI Account | OpenAI API | [platform.openai.com/api-keys](https://platform.openai.com/api-keys) |
| Gmail Account | Gmail OAuth2 | n8n auto-configures via Google OAuth |
| Google Sheets | Google Sheets OAuth2 | n8n auto-configures via Google OAuth |

### 3. Configure Your Campaign

Edit the **"Campaign Config"** node and replace the placeholders:

```json
{
  "campaign_name": "Your Campaign Name",
  "target_titles": ["CEO", "CTO", "VP Engineering"],
  "target_industries": ["SaaS", "Technology"],
  "company_size_min": 10,
  "company_size_max": 200,
  "daily_limit": 25,
  "sender_name": "Your Name",
  "sender_company": "Your Company",
  "sender_value_prop": "We help SaaS companies reduce churn by 40%",
  "sender_calendar_link": "https://calendly.com/you/15min"
}
```

### 4. Create Your CRM Sheet

Create a Google Sheets spreadsheet with a tab called **"Contacted Leads"** and these column headers:

| email | first_name | last_name | company | subject | status | sent_at | campaign | follow_up_scheduled | follow_up_sent_at |
|---|---|---|---|---|---|---|---|---|---|

Then update the **Spreadsheet ID** in these nodes:
- "Check Duplicates"
- "Log to CRM Sheet"
- "Update Lead Status"

### 5. Choose Send Mode

In the **"Campaign Config"** node, add:
- `"send_mode": "draft"` — creates Gmail drafts for review (recommended to start)
- `"send_mode": "send"` — auto-sends emails immediately

### 6. Test Run

1. Click **"Execute Workflow"** (uses the Manual Trigger)
2. Check each node's output to verify data flows correctly
3. Review drafts in Gmail
4. When satisfied, toggle to `"send"` mode and activate the schedule

## Customization Guide

### Change Target Audience
Edit the **"Campaign Config"** node — modify `target_titles`, `target_industries`, and company size range.

### Change Email Tone/Style
Edit the **"Generate Cold Email"** node's system message. The AI follows these instructions for every email it writes.

### Change Follow-Up Timing
Edit the **"Wait 3 Days"** node — change the `amount` parameter (e.g., 5 for 5 days).

### Add More Lead Sources
Duplicate the "Search Leads" HTTP Request node, connect it to a new output on the Switch node, and normalize the response data.

### Switch to SendGrid/Mailgun
Replace the Gmail nodes with HTTP Request nodes pointing to SendGrid/Mailgun APIs.

## Cost Estimate

| Service | Free Tier | Paid Estimate (25 leads/day) |
|---|---|---|
| Apollo.io | 50 credits/month | $49/month (Basic) |
| OpenAI (GPT-4o-mini) | — | ~$2-5/month |
| Gmail | 500 emails/day | Free |
| Google Sheets | Unlimited | Free |
| **Total** | — | **~$51-54/month** |

## FAQ

**Q: Will my emails go to spam?**
A: The AI is instructed to avoid spam trigger words and keep emails short and text-only. However, warm up your Gmail account first (send/receive regular emails for 2 weeks before cold outreach).

**Q: Can I use this with Outlook instead of Gmail?**
A: Yes — replace the Gmail nodes with Microsoft Outlook nodes (available in n8n).

**Q: How many emails should I send per day?**
A: Start with 10-15/day for a new email account. After 2-4 weeks, scale to 25-50/day. Never exceed 100/day from a single account.

**Q: Can I use Claude instead of OpenAI?**
A: Yes — replace the OpenAI Chat Model nodes with Anthropic nodes (`@n8n/n8n-nodes-langchain.lmChatAnthropic`).

## Support

If you have questions about setup or customization, email **{{SUPPORT_EMAIL}}**.

## License

This template is for personal and commercial use. Redistribution or resale is prohibited.
