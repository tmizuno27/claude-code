# How to Submit Workflows to n8n.io/workflows Community

## Overview

The n8n workflow library at [n8n.io/workflows](https://n8n.io/workflows) hosts 8,500+ community-contributed workflow templates. Submitting free templates here is an excellent lead magnet strategy — users discover your free workflow, then follow the link to your full paid version on Gumroad.

## Submission Methods

### Method 1: n8n Creator Hub (Recommended)

1. **Sign up** at [n8n.io](https://n8n.io) — create an account if you don't have one
2. **Access the Creator Hub** — go to your n8n dashboard and look for the Creator section
3. **Create a Creator Profile** — add your name, bio, and links (include your Gumroad store URL)
4. **Submit your template**:
   - Upload or paste the workflow JSON
   - Write a clear title and description
   - Add relevant tags (e.g., "email", "ai", "shopify", "ecommerce")
   - Include setup instructions
   - Add screenshots if possible
5. **Wait for review** — n8n reviews submissions before publishing (typically 1-2 weeks)

### Method 2: n8n Community Forum

1. Go to [community.n8n.io](https://community.n8n.io)
2. Create a post in the **Share** category
3. Paste your workflow JSON (users can one-click import from the forum)
4. This doesn't add it to the official library but gets visibility

### Method 3: n8n Cloud (if using cloud version)

1. Open the workflow in n8n Cloud
2. Click **Share** in the workflow editor
3. Select "Share as Template" to submit to the library

## Best Practices for Lead Magnet Templates

### What to Include in Free Versions
- Core functionality that solves a real problem (3-5 nodes)
- Enough value that users rate it highly and share it
- Clear setup instructions

### What to Withhold for Paid Versions
- Advanced routing/branching logic
- Slack/email notifications
- Error handling
- Multi-platform integrations
- AI-powered features (or give basic AI, upsell advanced)

### Description Template

```
[What it does in one line]

This workflow automatically [action] when [trigger].

## What's included (Free Version)
- [Feature 1]
- [Feature 2]
- [Feature 3]

## Setup
1. [Step 1]
2. [Step 2]
3. [Step 3]

## Want more?
The full version adds [feature list]. Get it here: [Gumroad link]
```

### Tags Strategy
- Use 3-5 relevant tags
- Include the main integration names (e.g., "shopify", "gmail")
- Add category tags (e.g., "ecommerce", "productivity")
- Include "free" as a tag

## Key Links

- n8n Workflow Library: https://n8n.io/workflows
- n8n Community Forum: https://community.n8n.io
- n8n Docs - Templates: https://docs.n8n.io/workflows/templates/
- n8n Creator Profile Info: https://community.n8n.io/t/creator-profile-templates-verification/126583

## Our Free Templates

| Template | Free Version | Full Version (Gumroad) |
|----------|-------------|----------------------|
| Email Classification & Auto-Routing | `workflows/free/email-classifier-free.json` | $49 |
| Shopify Order Automation | `workflows/free/shopify-logger-free.json` | $59 |

## Submission Checklist

- [ ] Workflow JSON is valid and imports cleanly into n8n
- [ ] Description clearly states what the free version does
- [ ] Description includes Gumroad link to full version
- [ ] Credential placeholder IDs are generic (e.g., "YOUR_SPREADSHEET_ID")
- [ ] Tags are relevant and include integration names
- [ ] Tested the workflow end-to-end in n8n
