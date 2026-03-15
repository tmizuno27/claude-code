"""
Gumroad Auto-Publisher for n8n Templates
Automatically creates and publishes products on Gumroad via API.
"""

import json
import os
import sys
import requests
from pathlib import Path

# Paths
SCRIPT_DIR = Path(__file__).parent
PROJECT_DIR = SCRIPT_DIR.parent
CONFIG_PATH = PROJECT_DIR / "config" / "gumroad-secrets.json"
LISTINGS_DIR = PROJECT_DIR / "listings"
ZIPS_DIR = LISTINGS_DIR / "zips"

GUMROAD_API = "https://api.gumroad.com/v2"

# Template definitions
TEMPLATES = [
    {
        "id": "01-ai-lead-gen",
        "name": "AI Lead Gen & Cold Outreach Automation for n8n",
        "price": 7900,  # cents
        "description": """Stop writing cold emails manually. Let AI do the research AND the writing.

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
• Gmail account""",
        "tags": ["n8n", "lead-generation", "cold-email", "ai", "sales-automation"],
    },
    {
        "id": "02-invoice-automation",
        "name": "QuickBooks & Stripe Invoice Automation for n8n",
        "price": 6900,
        "description": """Auto-sync every Stripe payment to QuickBooks — zero manual bookkeeping.

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

No AI costs — this workflow doesn't use any AI APIs.""",
        "tags": ["n8n", "stripe", "quickbooks", "invoicing", "accounting"],
    },
    {
        "id": "03-ai-customer-support",
        "name": "AI Customer Support Agent for n8n",
        "price": 9900,
        "description": """AI-powered support that reads, classifies, and replies to customer emails automatically.

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
• n8n, Email (IMAP), OpenAI API key (~$5-15/month), Google Sheets, Slack""",
        "tags": ["n8n", "customer-support", "ai-agent", "chatbot", "automation"],
    },
    {
        "id": "04-social-media-factory",
        "name": "Social Media Content Factory for n8n",
        "price": 4900,
        "description": """AI generates a full week of social media posts with images — automatically.

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
• n8n, OpenAI API key (~$10-20/month with images), Google Sheets, Slack (optional)""",
        "tags": ["n8n", "social-media", "content-creation", "ai", "marketing"],
    },
    {
        "id": "05-crm-pipeline",
        "name": "CRM Pipeline Automation for n8n",
        "price": 6900,
        "description": """Auto-create contacts, score leads with AI, and route hot/warm/cold — all in n8n.

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
• n8n, HubSpot (free CRM), OpenAI API key (~$2-5/month), Gmail, Slack""",
        "tags": ["n8n", "crm", "hubspot", "lead-scoring", "sales-pipeline"],
    },
    {
        "id": "06-email-classification",
        "name": "Email Classification & Auto-Routing for n8n",
        "price": 4900,
        "description": """AI classifies every incoming email and routes it automatically.

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
• n8n, Email (IMAP), OpenAI API key (~$2-5/month), Gmail, Slack, Google Sheets""",
        "tags": ["n8n", "email", "classification", "ai", "productivity"],
    },
    {
        "id": "07-pdf-data-extraction",
        "name": "PDF & Invoice Data Extraction for n8n",
        "price": 7900,
        "description": """Email a PDF invoice → AI extracts all data → saves to spreadsheet → creates QuickBooks bill.

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
• n8n, Email (IMAP), OpenAI API key (~$2-5/month), Google Sheets, QuickBooks (optional)""",
        "tags": ["n8n", "pdf", "invoice", "data-extraction", "accounting"],
    },
    {
        "id": "08-shopify-order",
        "name": "Shopify Order Automation for n8n",
        "price": 5900,
        "description": """Automate everything after a Shopify order — logging, emails, alerts, tagging.

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

No AI costs — this workflow doesn't use any AI APIs.""",
        "tags": ["n8n", "shopify", "ecommerce", "orders", "automation"],
    },
    {
        "id": "09-ai-blog-pipeline",
        "name": "AI Blog Content Pipeline for n8n",
        "price": 4900,
        "description": """Pick a topic → AI writes a full SEO article → publishes to WordPress as draft.

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
• n8n, OpenAI API key (~$5-15/month with images), Google Sheets, WordPress""",
        "tags": ["n8n", "blog", "content", "seo", "wordpress", "ai"],
    },
    {
        "id": "10-zapier-migration",
        "name": "Zapier-to-n8n Migration Kit (Top 5 Zaps)",
        "price": 9900,
        "description": """The 5 most popular Zapier automations, rebuilt natively for n8n. Save $49-149/month.

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

No AI costs — these workflows don't use any AI APIs.""",
        "tags": ["n8n", "zapier", "migration", "automation", "integration"],
    },
]


def load_config():
    with open(CONFIG_PATH, "r") as f:
        return json.load(f)


def create_product(access_token, template, zip_path):
    """Create a product on Gumroad via API."""
    url = f"{GUMROAD_API}/products"

    data = {
        "access_token": access_token,
        "name": template["name"],
        "price": template["price"],
        "description": template["description"],
        "customizable_price": "false",
        "require_shipping": "false",
        "tags": ",".join(template["tags"]),
    }

    files = {}
    if zip_path.exists():
        files["file"] = (zip_path.name, open(zip_path, "rb"), "application/zip")

    try:
        response = requests.post(url, data=data, files=files)
        result = response.json()

        if result.get("success"):
            product = result["product"]
            print(f"  ✓ Created: {product['name']}")
            print(f"    URL: {product.get('short_url', 'N/A')}")
            print(f"    Price: ${template['price']/100}")
            return product
        else:
            print(f"  ✗ Failed: {result.get('message', 'Unknown error')}")
            return None
    except Exception as e:
        print(f"  ✗ Error: {e}")
        return None
    finally:
        if files:
            files["file"][1].close()


def publish_product(access_token, product_id):
    """Enable (publish) a product on Gumroad."""
    url = f"{GUMROAD_API}/products/{product_id}/enable"
    response = requests.put(url, data={"access_token": access_token})
    result = response.json()
    if result.get("success"):
        print(f"    → Published!")
    else:
        print(f"    → Publish failed: {result.get('message', '')}")


def list_products(access_token):
    """List all existing products."""
    url = f"{GUMROAD_API}/products"
    response = requests.get(url, params={"access_token": access_token})
    result = response.json()
    if result.get("success"):
        return result.get("products", [])
    return []


def main():
    config = load_config()
    access_token = config["access_token"]

    # Check for --list flag
    if len(sys.argv) > 1 and sys.argv[1] == "--list":
        products = list_products(access_token)
        print(f"\n=== Gumroad Products ({len(products)}) ===\n")
        for p in products:
            status = "Published" if not p.get("unpublished", True) else "Draft"
            print(f"  [{status}] {p['name']} - ${p['price']/100:.0f} - {p.get('short_url', '')}")
        return

    # Check for --publish-all flag
    publish = len(sys.argv) > 1 and sys.argv[1] == "--publish"

    # Get existing products to avoid duplicates
    existing = list_products(access_token)
    existing_names = {p["name"] for p in existing}

    print(f"\n=== Gumroad Auto-Publisher ===\n")
    print(f"Templates to publish: {len(TEMPLATES)}")
    print(f"Already on Gumroad: {len(existing_names)}\n")

    results = []
    for template in TEMPLATES:
        zip_path = ZIPS_DIR / f"{template['id']}.zip"

        if template["name"] in existing_names:
            print(f"  ⊘ Skipped (exists): {template['name']}")
            continue

        if not zip_path.exists():
            print(f"  ⊘ Skipped (no ZIP): {template['id']}")
            continue

        print(f"  Publishing: {template['name']}...")
        product = create_product(access_token, template, zip_path)

        if product and publish:
            publish_product(access_token, product["id"])

        if product:
            results.append(product)

    print(f"\n=== Done ===")
    print(f"Created: {len(results)} products")
    if not publish:
        print(f"Note: Products are in DRAFT. Run with --publish to publish all.")

    # Save results
    if results:
        results_path = PROJECT_DIR / "config" / "gumroad-products.json"
        with open(results_path, "w") as f:
            json.dump(results, f, indent=2)
        print(f"Product data saved to: {results_path}")


if __name__ == "__main__":
    main()
