# Gumroad出品 手順書

商品1（AI Lead Gen）は作成済み。以下、商品2〜10を順番に出品する。

ZIPファイルの場所: `c:\Users\tmizu\マイドライブ\GitHub\claude-code\n8n-templates\listings\zips\`

エクスプローラーで上記フォルダを開いておくと、アップロード時に楽。

---

# ========== 商品2 ==========

## ステップ1: 新規商品作成画面を開く
Gumroadダッシュボード → 左メニュー「Products」→ 「New Product」ボタン

## ステップ2: Name欄に以下を貼り付け
```
QuickBooks & Stripe Invoice Automation for n8n
```

## ステップ3: 「Digital product」を選択（デフォルトで選択済みのはず）

## ステップ4: Price欄に入力
```
69
```

## ステップ5: 「Next: Customize」ボタンをクリック

## ステップ6: Description欄に以下を貼り付け（ここから↓）
```
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
```

## ステップ7: ファイルアップロード
「Add file」または「Upload」ボタン → `02-invoice-automation.zip` を選択

## ステップ8: 「Publish」ボタンをクリック

## → 商品2 完了！

---

# ========== 商品3 ==========

## ステップ1: 「Products」→ 「New Product」

## ステップ2: Name欄
```
AI Customer Support Agent for n8n
```

## ステップ3: Digital product を選択

## ステップ4: Price
```
99
```

## ステップ5: 「Next: Customize」

## ステップ6: Description
```
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
```

## ステップ7: `03-ai-customer-support.zip` をアップロード

## ステップ8: 「Publish」

## → 商品3 完了！

---

# ========== 商品4 ==========

## ステップ1: 「Products」→ 「New Product」

## ステップ2: Name欄
```
Social Media Content Factory for n8n
```

## ステップ3: Digital product

## ステップ4: Price
```
49
```

## ステップ5: 「Next: Customize」

## ステップ6: Description
```
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
```

## ステップ7: `04-social-media-factory.zip` をアップロード

## ステップ8: 「Publish」

## → 商品4 完了！

---

# ========== 商品5 ==========

## ステップ1: 「Products」→ 「New Product」

## ステップ2: Name欄
```
CRM Pipeline Automation for n8n
```

## ステップ3: Digital product

## ステップ4: Price
```
69
```

## ステップ5: 「Next: Customize」

## ステップ6: Description
```
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
```

## ステップ7: `05-crm-pipeline.zip` をアップロード

## ステップ8: 「Publish」

## → 商品5 完了！

---

# ========== 商品6 ==========

## ステップ1: 「Products」→ 「New Product」

## ステップ2: Name欄
```
Email Classification & Auto-Routing for n8n
```

## ステップ3: Digital product

## ステップ4: Price
```
49
```

## ステップ5: 「Next: Customize」

## ステップ6: Description
```
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
```

## ステップ7: `06-email-classification.zip` をアップロード

## ステップ8: 「Publish」

## → 商品6 完了！

---

# ========== 商品7 ==========

## ステップ1: 「Products」→ 「New Product」

## ステップ2: Name欄
```
PDF & Invoice Data Extraction for n8n
```

## ステップ3: Digital product

## ステップ4: Price
```
79
```

## ステップ5: 「Next: Customize」

## ステップ6: Description
```
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
```

## ステップ7: `07-pdf-data-extraction.zip` をアップロード

## ステップ8: 「Publish」

## → 商品7 完了！

---

# ========== 商品8 ==========

## ステップ1: 「Products」→ 「New Product」

## ステップ2: Name欄
```
Shopify Order Automation for n8n
```

## ステップ3: Digital product

## ステップ4: Price
```
59
```

## ステップ5: 「Next: Customize」

## ステップ6: Description
```
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
```

## ステップ7: `08-shopify-order.zip` をアップロード

## ステップ8: 「Publish」

## → 商品8 完了！

---

# ========== 商品9 ==========

## ステップ1: 「Products」→ 「New Product」

## ステップ2: Name欄
```
AI Blog Content Pipeline for n8n
```

## ステップ3: Digital product

## ステップ4: Price
```
49
```

## ステップ5: 「Next: Customize」

## ステップ6: Description
```
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
```

## ステップ7: `09-ai-blog-pipeline.zip` をアップロード

## ステップ8: 「Publish」

## → 商品9 完了！

---

# ========== 商品10 ==========

## ステップ1: 「Products」→ 「New Product」

## ステップ2: Name欄
```
Zapier-to-n8n Migration Kit (Top 5 Zaps)
```

## ステップ3: Digital product

## ステップ4: Price
```
99
```

## ステップ5: 「Next: Customize」

## ステップ6: Description
```
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
```

## ステップ7: `10-zapier-migration.zip` をアップロード

## ステップ8: 「Publish」

## → 商品10 完了！

---

# ========== 全商品出品完了！ ==========

## 確認
Gumroadダッシュボード → Products で10商品が表示されていればOK。

## 商品1について
最初に作成した「AI Lead Gen & Cold Outreach Automation for n8n」がまだPublishされていない場合：
1. 商品をクリック → Edit
2. Descriptionを貼り付け（下記参照）
3. `01-ai-lead-gen.zip` をアップロード
4. Publish

商品1のDescription:
```
Stop writing cold emails manually. Let AI do the research AND the writing.

This n8n workflow template automates your entire cold outreach pipeline:

Find → Research → Write → Send → Follow Up

What's included:
• Ready-to-import n8n workflow JSON (20+ nodes, fully configured)
• Step-by-step setup guide (README)
• Google Sheets CRM template structure
• Customization guide

How it works:
1. Automatic lead discovery from Apollo.io or Hunter.io — target by job title, industry, and company size
2. AI-powered company research — GPT-4o-mini analyzes each prospect to find pain points and personalization hooks
3. AI-written emails — every email is unique, personalized, and spam-safe (no templates!)
4. Smart sending — auto-send or create Gmail drafts for review
5. CRM logging — every lead and email tracked in Google Sheets
6. Auto follow-up — checks for replies after 3 days and sends a follow-up if no response

Perfect for:
• Freelancers looking for clients
• Agency owners doing outbound
• SaaS founders doing founder-led sales
• Sales teams wanting to automate prospecting

Requirements:
• n8n (self-hosted or cloud)
• Apollo.io or Hunter.io API key (free tiers available)
• OpenAI API key (~$2-5/month)
• Gmail account
```
