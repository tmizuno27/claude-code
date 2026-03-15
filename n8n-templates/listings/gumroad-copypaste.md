# Gumroad出品 コピペ用テキスト

各商品ごとに「New Product → Digital product」を選択し、Name/Price/Descriptionを貼り付け → ZIPアップロード → Publish

ZIPファイルの場所: `claude-code/n8n-templates/listings/zips/`

---

## 商品2: QuickBooks & Stripe Invoice Automation for n8n
**Price:** $69
**ZIP:** 02-invoice-automation.zip

**Description:**
Auto-sync every Stripe payment to QuickBooks — zero manual bookkeeping.

This n8n workflow automatically:
1. Listens for Stripe payment events via webhook
2. Extracts invoice data (customer, amount, line items)
3. Finds or creates the customer in QuickBooks
4. Creates a matching QuickBooks invoice
5. Records the payment
6. Logs everything to Google Sheets
7. Sends a Slack notification

What's included:
• Ready-to-import n8n workflow JSON (12 nodes)
• Step-by-step setup guide
• Google Sheets audit trail template

Features:
• Real-time sync (processes within seconds)
• Auto customer creation in QuickBooks
• Deduplication (no duplicate invoices)
• Multi-currency support
• Slack notifications
• Error handling

Requirements:
• n8n (self-hosted or cloud)
• Stripe account
• QuickBooks Online account
• Google Sheets
• Slack (optional)

No AI costs — this workflow doesn't use any AI APIs.

---

## 商品3: AI Customer Support Agent for n8n
**Price:** $99
**ZIP:** 03-ai-customer-support.zip

**Description:**
AI-powered support that reads, classifies, and replies to customer emails automatically.

This n8n workflow:
1. Receives support messages via email (IMAP) or chat widget (webhook)
2. AI classifies by category, urgency, and sentiment
3. Searches your knowledge base for relevant answers
4. Generates a personalized, empathetic AI reply
5. Auto-sends if high confidence, escalates to Slack if not
6. Logs every ticket to Google Sheets

What's included:
• Ready-to-import n8n workflow JSON (14 nodes)
• Setup guide with credential configuration
• Customizable AI prompts for your brand voice

Features:
• Dual input (email + chat widget)
• Smart escalation (refunds >$100, legal threats, low confidence)
• Knowledge base integration
• Sentiment analysis
• Full ticket logging

Requirements:
• n8n, Email (IMAP), OpenAI API key (~$5-15/month), Google Sheets, Slack

---

## 商品4: Social Media Content Factory for n8n
**Price:** $49
**ZIP:** 04-social-media-factory.zip

**Description:**
AI generates a full week of social media posts with images — automatically.

This n8n workflow:
1. Fetches trending topics from Twitter API and industry RSS feeds
2. AI creates 7 platform-specific posts (Twitter, LinkedIn, Instagram)
3. Generates accompanying images via DALL-E 3
4. Saves everything to your Google Sheets content calendar
5. Notifies your team via Slack

What's included:
• Ready-to-import n8n workflow JSON (12 nodes)
• Setup guide
• Content calendar template structure

Features:
• Trending topic integration
• Platform-optimized content (280 chars for Twitter, long-form for LinkedIn)
• Content pillar rotation (educational, promotional, engagement, etc.)
• AI image generation
• Weekly automated scheduling

Requirements:
• n8n, OpenAI API key (~$10-20/month with images), Google Sheets, Slack (optional)

---

## 商品5: CRM Pipeline Automation for n8n
**Price:** $69
**ZIP:** 05-crm-pipeline.zip

**Description:**
Auto-create contacts, score leads with AI, and route hot/warm/cold — all in n8n.

This n8n workflow:
1. Receives new leads via webhook (from your website form)
2. Creates/updates HubSpot contact and deal
3. AI scores the lead 1-100 (based on email domain, title, company, message)
4. Routes automatically: Hot → Slack alert, Warm → nurture email, Cold → drip sequence
5. Tracks Stripe payments and updates deals to "Closed Won"
6. Daily stale deal alerts

What's included:
• Ready-to-import n8n workflow JSON (14 nodes)
• Setup guide
• Lead scoring criteria (customizable)

Features:
• AI lead scoring with reasoning
• 3-tier routing (hot/warm/cold)
• HubSpot CRM integration
• Stripe payment tracking
• Stale deal monitoring

Requirements:
• n8n, HubSpot (free CRM), OpenAI API key (~$2-5/month), Gmail, Slack

---

## 商品6: Email Classification & Auto-Routing for n8n
**Price:** $49
**ZIP:** 06-email-classification.zip

**Description:**
AI classifies every incoming email and routes it automatically.

This n8n workflow:
1. Monitors your inbox via IMAP
2. AI classifies each email: category, priority, sentiment, spam detection
3. Spam → auto-moved to spam folder
4. Urgent → Slack alert
5. Invoices → forwarded to accounting
6. Client emails → labeled
7. Everything logged to Google Sheets

What's included:
• Ready-to-import n8n workflow JSON (12 nodes)
• Setup guide
• Classification categories (customizable)

Features:
• 9 categories (urgent, client, invoice, newsletter, spam, internal, personal, support, sales_inquiry)
• 3 priority levels
• Sentiment analysis
• Auto-suggested actions
• Full audit trail

Requirements:
• n8n, Email (IMAP), OpenAI API key (~$2-5/month), Gmail, Slack, Google Sheets

---

## 商品7: PDF & Invoice Data Extraction for n8n
**Price:** $79
**ZIP:** 07-pdf-data-extraction.zip

**Description:**
Email a PDF invoice → AI extracts all data → saves to spreadsheet → creates QuickBooks bill.

This n8n workflow:
1. Receives PDFs via email attachment or file upload webhook
2. Extracts text from PDF
3. AI extracts structured data: vendor, amounts, line items, dates, tax, currency
4. Validates confidence score
5. High confidence → auto-saves to Google Sheets + creates QuickBooks bill
6. Low confidence → flags for human review via Slack

What's included:
• Ready-to-import n8n workflow JSON (12 nodes)
• Setup guide
• Spreadsheet template structure

Features:
• Dual input (email + API upload)
• 15+ extracted fields (vendor, amounts, dates, line items, tax ID, etc.)
• Confidence scoring with automatic escalation
• QuickBooks bill creation
• Webhook response for API integration

Requirements:
• n8n, Email (IMAP), OpenAI API key (~$2-5/month), Google Sheets, QuickBooks (optional)

---

## 商品8: Shopify Order Automation for n8n
**Price:** $59
**ZIP:** 08-shopify-order.zip

**Description:**
Automate everything after a Shopify order — logging, emails, alerts, tagging.

This n8n workflow:
1. Triggers on every new Shopify order
2. Flags high-value orders (>$500) via Slack for manual review
3. Logs all orders to Google Sheets
4. Sends personalized thank-you email with order summary
5. Checks inventory and alerts on low stock
6. Auto-tags processed orders in Shopify

What's included:
• Ready-to-import n8n workflow JSON (10 nodes)
• Setup guide
• Order tracking spreadsheet template

Features:
• High-value order detection
• Personalized thank-you emails
• Inventory monitoring
• Auto-tagging in Shopify
• Full order history in Sheets

Requirements:
• n8n, Shopify store, Gmail, Google Sheets, Slack

No AI costs — this workflow doesn't use any AI APIs.

---

## 商品9: AI Blog Content Pipeline for n8n
**Price:** $49
**ZIP:** 09-ai-blog-pipeline.zip

**Description:**
Pick a topic → AI writes a full SEO article → publishes to WordPress as draft.

This n8n workflow:
1. Pulls the next pending topic from your Google Sheets queue
2. AI researches and creates an SEO-optimized outline (headings, FAQs, internal links)
3. AI writes a full 2,000-word article in HTML format
4. Generates a professional featured image via DALL-E 3
5. Publishes to WordPress as a draft
6. Updates the topic queue with post ID

What's included:
• Ready-to-import n8n workflow JSON (14 nodes)
• Setup guide
• Topic queue template

Features:
• Topic queue system (just add topics, workflow does the rest)
• SEO-optimized outlines with FAQ schema
• Full HTML articles (not markdown)
• AI featured image generation
• WordPress auto-publishing (as draft)
• Scheduled or on-demand

Requirements:
• n8n, OpenAI API key (~$5-15/month with images), Google Sheets, WordPress

---

## 商品10: Zapier-to-n8n Migration Kit (Top 5 Zaps)
**Price:** $99
**ZIP:** 10-zapier-migration.zip

**Description:**
The 5 most popular Zapier automations, rebuilt natively for n8n. Save $49-149/month.

Included workflows:
1. Gmail → Google Sheets (new email → log to spreadsheet)
2. Typeform → Slack + Gmail (form submission → notify team + send confirmation)
3. Stripe → QuickBooks (payment → create invoice)
4. RSS → Twitter + LinkedIn (new article → post to social media)
5. Webhook → HubSpot + Slack (inbound lead → create CRM contact + notify sales)

Why switch from Zapier?
• No per-task pricing — n8n charges by workflow, not by step
• Self-hostable — your data stays on your servers
• More powerful — branching, looping, code nodes, AI nodes built-in
• Open source — no vendor lock-in

What's included:
• Ready-to-import n8n workflow JSON with all 5 workflows (16 nodes total)
• Setup guide for each workflow
• Migration checklist

Each workflow is independent — activate only the ones you need.

Requirements:
• n8n (self-hosted or cloud)
• Credentials for the services you use (Gmail, Sheets, Slack, Stripe, QuickBooks, Twitter, LinkedIn, HubSpot)

No AI costs — these workflows don't use any AI APIs.
