"""
Share Templates Helper — Lists all child pages under a parent and outputs
share links and Gumroad product creation instructions.

Usage:
    set NOTION_TOKEN=secret_xxx
    python share_templates.py <parent_page_id>
"""

import requests
import os
import sys
import json
import time

NOTION_TOKEN = os.environ.get("NOTION_TOKEN", "")
BASE_URL = "https://api.notion.com/v1"
HEADERS = {
    "Authorization": f"Bearer {NOTION_TOKEN}",
    "Content-Type": "application/json",
    "Notion-Version": "2022-06-28",
}

# Template metadata for Gumroad listings
TEMPLATE_META = {
    "Freelance Business OS": {
        "price": 19, "tags": ["notion", "freelance", "business", "productivity"],
        "description": "All-in-one Notion workspace for freelancers. Manage clients, projects, tasks, time tracking, invoices, expenses, and proposals.",
    },
    "Content Creator Dashboard": {
        "price": 15, "tags": ["notion", "content-creator", "youtube", "social-media"],
        "description": "Plan, create, publish, and analyze your content across all platforms. Includes ideas bank, sponsor tracking, and revenue dashboard.",
    },
    "Student Study Hub": {
        "price": 9, "tags": ["notion", "student", "study", "education"],
        "description": "Track courses, assignments, study sessions, grades, and notes. Never miss a deadline again.",
    },
    "Life OS": {
        "price": 19, "tags": ["notion", "life-os", "second-brain", "productivity"],
        "description": "Your complete second brain. Organize goals, habits, projects, tasks, journal, finances, and health in one system.",
    },
    "Small Business CRM": {
        "price": 17, "tags": ["notion", "crm", "sales", "business"],
        "description": "Manage contacts, companies, deals pipeline, and activities. Never miss a follow-up.",
    },
    "Side Hustle Tracker": {
        "price": 12, "tags": ["notion", "side-hustle", "income", "entrepreneur"],
        "description": "Track multiple side hustles with income, expenses, P&L, milestones, and time tracking.",
    },
    "Social Media Planner": {
        "price": 14, "tags": ["notion", "social-media", "content-calendar", "marketing"],
        "description": "Plan, schedule, and analyze social media content. Includes hashtag library, analytics, and swipe file.",
    },
    "Job Search Tracker": {
        "price": 9, "tags": ["notion", "job-search", "career", "interview"],
        "description": "Track applications, companies, interviews, networking contacts, and skills. Stay organized during your job search.",
    },
    "Book & Learning Tracker": {
        "price": 9, "tags": ["notion", "reading", "books", "learning"],
        "description": "Track your reading list, courses, notes, highlights, and annual reading challenge.",
    },
    "Digital Products Business OS": {
        "price": 15, "tags": ["notion", "digital-products", "ecommerce", "business"],
        "description": "Manage digital products, sales, marketing campaigns, customer feedback, and product roadmap.",
    },
}


def api_get(endpoint, params=None):
    time.sleep(0.4)
    resp = requests.get(f"{BASE_URL}{endpoint}", headers=HEADERS, params=params)
    resp.raise_for_status()
    return resp.json()


def get_child_pages(parent_id):
    """Get all child blocks that are child_page type."""
    pages = []
    endpoint = f"/blocks/{parent_id}/children"
    has_more = True
    start_cursor = None

    while has_more:
        params = {"page_size": 100}
        if start_cursor:
            params["start_cursor"] = start_cursor
        data = api_get(endpoint, params)
        for block in data.get("results", []):
            if block["type"] == "child_page":
                pages.append({
                    "id": block["id"],
                    "title": block["child_page"]["title"],
                })
        has_more = data.get("has_more", False)
        start_cursor = data.get("next_cursor")

    return pages


def get_page_url(page_id):
    """Get the URL for a page."""
    data = api_get(f"/pages/{page_id}")
    return data.get("url", f"https://notion.so/{page_id.replace('-', '')}")


def find_meta(title):
    """Match a page title to template metadata."""
    for key, meta in TEMPLATE_META.items():
        if key.lower() in title.lower():
            return meta
    return None


def main():
    if len(sys.argv) < 2:
        print("Usage: python share_templates.py <parent_page_id>")
        print("\nThe parent_page_id is the master page containing all 10 templates.")
        print("You can find it in the output of create_all_templates.py")
        sys.exit(1)

    parent_id = sys.argv[1]

    if not NOTION_TOKEN:
        print("ERROR: Set NOTION_TOKEN environment variable first.")
        sys.exit(1)

    print(f"Fetching child pages of: {parent_id}\n")
    pages = get_child_pages(parent_id)

    if not pages:
        print("No child pages found. Make sure the parent_page_id is correct.")
        sys.exit(1)

    print(f"Found {len(pages)} template pages:\n")
    print("=" * 70)

    templates_data = []
    for i, page in enumerate(pages, 1):
        url = get_page_url(page["id"])
        meta = find_meta(page["title"])
        share_url = url  # Notion share URL = page URL (user must enable "Share to web")

        templates_data.append({
            "index": i,
            "title": page["title"],
            "id": page["id"],
            "url": url,
            "meta": meta,
        })

        print(f"\n{i}. {page['title']}")
        print(f"   Page ID:   {page['id']}")
        print(f"   URL:       {url}")
        if meta:
            print(f"   Price:     ${meta['price']}")
            print(f"   Tags:      {', '.join(meta['tags'])}")

    print("\n" + "=" * 70)
    print("\nSHARING INSTRUCTIONS")
    print("=" * 70)
    print("""
For each template above, follow these steps:

1. ENABLE SHARING (Notion)
   - Open each template page URL in Notion
   - Click "Share" button (top right)
   - Enable "Share to web"
   - Toggle ON "Allow duplicate as template"
   - Copy the share link

2. CREATE GUMROAD PRODUCTS
   For each template, create a Gumroad product at https://app.gumroad.com/products/new

   Product settings:
   - Name: [Template Name]
   - Price: [see above]
   - Description: [see below]
   - Content: Paste the Notion share/duplicate link
   - File: None needed (it's a Notion link)
   - Tags: [see above]

3. DELIVERY MESSAGE (set for each product):
   "Thank you for your purchase! Click the link below to duplicate
   this template to your Notion workspace:

   [NOTION_SHARE_LINK]

   Quick start:
   1. Click the link above
   2. Click 'Duplicate' in the top right
   3. The template will be added to your Notion workspace
   4. Delete the sample data and start customizing!

   Need help? Reply to this email."
""")

    # Output JSON for programmatic use
    output_path = os.path.join(os.path.dirname(__file__), "..", "docs", "template_links.json")
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(templates_data, f, indent=2, ensure_ascii=False)
    print(f"\nTemplate data saved to: {os.path.abspath(output_path)}")

    print("\n" + "=" * 70)
    print("GUMROAD PRODUCT DESCRIPTIONS (copy-paste ready)")
    print("=" * 70)
    for t in templates_data:
        meta = t["meta"]
        if not meta:
            continue
        print(f"\n--- {t['title']} (${meta['price']}) ---")
        print(f"\n{meta['description']}")
        print(f"\nWhat's included:")
        print(f"- Fully built Notion template with multiple linked databases")
        print(f"- Pre-filled sample data to see the system in action")
        print(f"- Dashboard page with linked views")
        print(f"- Setup instructions")
        print(f"- Lifetime access (duplicate once, yours forever)")
        print(f"\nTags: {', '.join(meta['tags'])}")


if __name__ == "__main__":
    main()
