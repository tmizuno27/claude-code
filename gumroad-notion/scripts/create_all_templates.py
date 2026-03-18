"""
Notion Template Builder — Creates 10 Gumroad Notion templates via Notion API.

Each template is a top-level page containing multiple databases with full schemas,
sample data, and a dashboard page with linked views.

Usage:
    set NOTION_TOKEN=secret_xxx
    python create_all_templates.py [--parent-page-id PAGE_ID]

If --parent-page-id is provided, templates are created as children of that page.
Otherwise they are created as top-level workspace pages.
"""

import requests
import json
import os
import sys
import time
import argparse
import logging
from datetime import datetime, timedelta

# ---------------------------------------------------------------------------
# Config
# ---------------------------------------------------------------------------
NOTION_TOKEN = os.environ.get("NOTION_TOKEN", "")
BASE_URL = "https://api.notion.com/v1"
HEADERS = {
    "Authorization": f"Bearer {NOTION_TOKEN}",
    "Content-Type": "application/json",
    "Notion-Version": "2022-06-28",
}

logging.basicConfig(level=logging.INFO, format="%(asctime)s  %(message)s")
log = logging.getLogger(__name__)

# Rate-limit pause (seconds) between API calls
RATE_LIMIT = 0.4

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _api(method: str, endpoint: str, payload: dict | None = None) -> dict:
    """Wrapper around requests with rate limiting and error handling."""
    time.sleep(RATE_LIMIT)
    url = f"{BASE_URL}{endpoint}"
    resp = getattr(requests, method)(url, headers=HEADERS, json=payload)
    if resp.status_code == 429:
        retry_after = float(resp.headers.get("Retry-After", 2))
        log.warning(f"Rate limited. Sleeping {retry_after}s ...")
        time.sleep(retry_after)
        resp = getattr(requests, method)(url, headers=HEADERS, json=payload)
    if resp.status_code >= 400:
        log.error(f"API error {resp.status_code}: {resp.text[:500]}")
        resp.raise_for_status()
    return resp.json()


def rich(text: str) -> list:
    """Create a rich_text array from a plain string."""
    return [{"type": "text", "text": {"content": text}}]


def title_prop(text: str) -> dict:
    return {"title": rich(text)}


def rt_prop(text: str) -> dict:
    return {"rich_text": rich(text)}


def num_prop(val) -> dict:
    return {"number": val}


def select_prop(name: str) -> dict:
    return {"select": {"name": name}}


def mselect_prop(*names: str) -> dict:
    return {"multi_select": [{"name": n} for n in names]}


def date_prop(start: str, end: str | None = None) -> dict:
    d = {"date": {"start": start}}
    if end:
        d["date"]["end"] = end
    return d


def checkbox_prop(val: bool) -> dict:
    return {"checkbox": val}


def url_prop(val: str) -> dict:
    return {"url": val}


def email_prop(val: str) -> dict:
    return {"email": val}


def phone_prop(val: str) -> dict:
    return {"phone_number": val}


def relation_prop(*ids: str) -> dict:
    return {"relation": [{"id": i} for i in ids]}


# ---------------------------------------------------------------------------
# Page / Database creation
# ---------------------------------------------------------------------------

def create_page(parent: dict, title: str, icon: str = "", children: list | None = None) -> dict:
    """Create a Notion page. Returns the full page object."""
    body: dict = {
        "parent": parent,
        "properties": {"title": {"title": rich(title)}},
    }
    if icon:
        body["icon"] = {"type": "emoji", "emoji": icon}
    if children:
        body["children"] = children[:100]  # max 100 blocks per request
    result = _api("post", "/pages", body)
    log.info(f"  Page created: {title} -> {result['id']}")
    return result


def append_blocks(page_id: str, children: list) -> None:
    """Append blocks to an existing page (for >100 blocks)."""
    for i in range(0, len(children), 100):
        _api("patch", f"/blocks/{page_id}/children", {"children": children[i:i+100]})


def create_database(parent_page_id: str, title: str, icon: str,
                    properties: dict) -> dict:
    """Create an inline database inside a page. Returns the DB object."""
    body = {
        "parent": {"type": "page_id", "page_id": parent_page_id},
        "title": rich(title),
        "is_inline": True,
        "properties": properties,
    }
    if icon:
        body["icon"] = {"type": "emoji", "emoji": icon}
    result = _api("post", "/databases", body)
    log.info(f"  DB created: {title} -> {result['id']}")
    return result


def add_row(database_id: str, props: dict) -> dict:
    """Add a row to a database."""
    body = {
        "parent": {"database_id": database_id},
        "properties": props,
    }
    result = _api("post", "/pages", body)
    return result


# ---------------------------------------------------------------------------
# Property schema builders
# ---------------------------------------------------------------------------

def p_title():
    return {"title": {}}

def p_rt():
    return {"rich_text": {}}

def p_number(fmt="number"):
    return {"number": {"format": fmt}}

def p_select(*opts):
    return {"select": {"options": [{"name": o} for o in opts]}}

def p_mselect(*opts):
    return {"multi_select": {"options": [{"name": o} for o in opts]}}

def p_date():
    return {"date": {}}

def p_checkbox():
    return {"checkbox": {}}

def p_url():
    return {"url": {}}

def p_email():
    return {"email": {}}

def p_phone():
    return {"phone_number": {}}

def p_files():
    return {"files": {}}

def p_created_time():
    return {"created_time": {}}

def p_last_edited_time():
    return {"last_edited_time": {}}

def p_formula(expr: str):
    return {"formula": {"expression": expr}}

def p_relation(db_id: str, single=False):
    r: dict = {"relation": {"database_id": db_id, "type": "single_property", "single_property": {}}}
    if not single:
        r["relation"] = {"database_id": db_id, "type": "dual_property", "dual_property": {}}
    return r

def p_relation_single(db_id: str):
    return {"relation": {"database_id": db_id, "type": "single_property", "single_property": {}}}

def p_rollup(relation_prop_name: str, rollup_prop_name: str, function: str):
    return {"rollup": {"relation_property_name": relation_prop_name,
                        "rollup_property_name": rollup_prop_name,
                        "function": function}}

def p_person():
    return {"people": {}}

# ---------------------------------------------------------------------------
# Block builders (for Dashboard / page content)
# ---------------------------------------------------------------------------

def heading1(text: str) -> dict:
    return {"object": "block", "type": "heading_1",
            "heading_1": {"rich_text": rich(text)}}

def heading2(text: str) -> dict:
    return {"object": "block", "type": "heading_2",
            "heading_2": {"rich_text": rich(text)}}

def heading3(text: str) -> dict:
    return {"object": "block", "type": "heading_3",
            "heading_3": {"rich_text": rich(text)}}

def paragraph(text: str) -> dict:
    return {"object": "block", "type": "paragraph",
            "paragraph": {"rich_text": rich(text)}}

def callout(text: str, icon: str = "💡") -> dict:
    return {"object": "block", "type": "callout",
            "callout": {"rich_text": rich(text),
                        "icon": {"type": "emoji", "emoji": icon}}}

def divider() -> dict:
    return {"object": "block", "type": "divider", "divider": {}}

def toggle(text: str, children: list | None = None) -> dict:
    t: dict = {"object": "block", "type": "toggle",
            "toggle": {"rich_text": rich(text)}}
    if children:
        t["toggle"]["children"] = children
    return t

def bulleted(text: str) -> dict:
    return {"object": "block", "type": "bulleted_list_item",
            "bulleted_list_item": {"rich_text": rich(text)}}

def numbered(text: str) -> dict:
    return {"object": "block", "type": "numbered_list_item",
            "numbered_list_item": {"rich_text": rich(text)}}

def table_of_contents() -> dict:
    return {"object": "block", "type": "table_of_contents",
            "table_of_contents": {}}


# ---------------------------------------------------------------------------
# Date helpers
# ---------------------------------------------------------------------------
TODAY = datetime.now().strftime("%Y-%m-%d")
def _d(offset_days: int = 0) -> str:
    return (datetime.now() + timedelta(days=offset_days)).strftime("%Y-%m-%d")


# ============================================================================
# TEMPLATE 1: Freelance Business OS
# ============================================================================

def create_freelance_os(parent: dict) -> dict:
    log.info("=== Template 1: Freelance Business OS ===")
    page = create_page(parent, "Freelance Business OS", "💼", [
        heading1("Freelance Business OS"),
        paragraph("Your all-in-one workspace for managing clients, projects, tasks, time, invoices, and proposals."),
        callout("Quick Start: Delete sample data, add your clients, and start tracking projects!", "🚀"),
        divider(),
    ])
    pid = page["id"]

    # --- DB: Clients ---
    clients_db = create_database(pid, "Clients", "👤", {
        "Client Name": p_title(),
        "Status": p_select("Active", "Prospect", "Past", "Paused"),
        "Industry": p_select("Tech", "Marketing", "Finance", "E-commerce", "Education", "Healthcare", "Other"),
        "Contact Person": p_rt(),
        "Email": p_email(),
        "Phone": p_phone(),
        "Website": p_url(),
        "Source": p_select("Referral", "Upwork", "Fiverr", "Cold Outreach", "Inbound", "Social Media", "Other"),
        "Monthly Retainer": p_number("dollar"),
        "Notes": p_rt(),
        "Start Date": p_date(),
        "Rating": p_select("⭐", "⭐⭐", "⭐⭐⭐", "⭐⭐⭐⭐", "⭐⭐⭐⭐⭐"),
    })
    cid = clients_db["id"]

    # --- DB: Projects ---
    projects_db = create_database(pid, "Projects", "📁", {
        "Project Name": p_title(),
        "Client": p_relation_single(cid),
        "Status": p_select("Not Started", "In Progress", "On Hold", "Completed", "Cancelled"),
        "Priority": p_select("🔴 High", "🟡 Medium", "🟢 Low"),
        "Type": p_select("One-time", "Retainer", "Hourly"),
        "Start Date": p_date(),
        "Deadline": p_date(),
        "Budget": p_number("dollar"),
        "Hours Estimated": p_number(),
        "Deliverables": p_rt(),
        "Notes": p_rt(),
    })
    proj_id = projects_db["id"]

    # --- DB: Tasks ---
    tasks_db = create_database(pid, "Tasks", "✅", {
        "Task": p_title(),
        "Project": p_relation_single(proj_id),
        "Status": p_select("To Do", "In Progress", "Waiting", "Done"),
        "Priority": p_select("🔴 High", "🟡 Medium", "🟢 Low"),
        "Due Date": p_date(),
        "Estimated Hours": p_number(),
        "Tags": p_mselect("Design", "Development", "Writing", "Research", "Admin", "Meeting", "Review"),
        "Notes": p_rt(),
    })

    # --- DB: Time Log ---
    timelog_db = create_database(pid, "Time Log", "⏱️", {
        "Description": p_title(),
        "Project": p_relation_single(proj_id),
        "Date": p_date(),
        "Hours": p_number(),
        "Hourly Rate": p_number("dollar"),
        "Earnings": p_formula('prop("Hours") * prop("Hourly Rate")'),
        "Billable": p_checkbox(),
    })

    # --- DB: Invoices ---
    invoices_db = create_database(pid, "Invoices", "🧾", {
        "Invoice #": p_title(),
        "Client": p_relation_single(cid),
        "Project": p_relation_single(proj_id),
        "Status": p_select("Draft", "Sent", "Paid", "Overdue", "Cancelled"),
        "Issue Date": p_date(),
        "Due Date": p_date(),
        "Amount": p_number("dollar"),
        "Tax": p_number("dollar"),
        "Total": p_formula('prop("Amount") + prop("Tax")'),
        "Payment Method": p_select("Bank Transfer", "PayPal", "Wise", "Stripe", "Cash", "Other"),
        "Paid Date": p_date(),
        "Notes": p_rt(),
    })

    # --- DB: Expenses ---
    expenses_db = create_database(pid, "Expenses", "💸", {
        "Expense": p_title(),
        "Category": p_select("Software", "Hardware", "Marketing", "Travel", "Office", "Education", "Tax", "Other"),
        "Amount": p_number("dollar"),
        "Date": p_date(),
        "Recurring": p_checkbox(),
        "Frequency": p_select("Monthly", "Quarterly", "Yearly", "One-time"),
        "Notes": p_rt(),
        "Tax Deductible": p_checkbox(),
    })

    # --- DB: Proposals ---
    proposals_db = create_database(pid, "Proposals", "📝", {
        "Proposal Title": p_title(),
        "Client": p_relation_single(cid),
        "Status": p_select("Draft", "Sent", "Accepted", "Rejected", "Expired"),
        "Amount": p_number("dollar"),
        "Sent Date": p_date(),
        "Deadline": p_date(),
        "Link": p_url(),
        "Notes": p_rt(),
    })

    # --- DB: Notes ---
    notes_db = create_database(pid, "Notes", "📓", {
        "Title": p_title(),
        "Category": p_select("Meeting Notes", "Ideas", "Resources", "SOP", "Templates"),
        "Related Client": p_relation_single(cid),
        "Related Project": p_relation_single(proj_id),
        "Tags": p_mselect(),
        "Created": p_created_time(),
    })

    # --- Sample Data ---
    log.info("  Adding sample data...")
    c1 = add_row(cid, {"Client Name": title_prop("Acme Corp"), "Status": select_prop("Active"),
                        "Industry": select_prop("Tech"), "Email": email_prop("contact@acme.com"),
                        "Source": select_prop("Referral"), "Monthly Retainer": num_prop(3000),
                        "Start Date": date_prop("2025-06-01"), "Rating": select_prop("⭐⭐⭐⭐⭐")})
    c2 = add_row(cid, {"Client Name": title_prop("Beta Agency"), "Status": select_prop("Prospect"),
                        "Industry": select_prop("Marketing"), "Email": email_prop("hello@beta.io"),
                        "Source": select_prop("Cold Outreach")})
    c3 = add_row(cid, {"Client Name": title_prop("Gamma Ltd"), "Status": select_prop("Past"),
                        "Industry": select_prop("Finance"), "Email": email_prop("info@gamma.com"),
                        "Start Date": date_prop("2024-01-15"), "Rating": select_prop("⭐⭐⭐")})

    p1 = add_row(proj_id, {"Project Name": title_prop("Website Redesign"), "Client": relation_prop(c1["id"]),
                            "Status": select_prop("In Progress"), "Priority": select_prop("🔴 High"),
                            "Type": select_prop("One-time"), "Start Date": date_prop(_d(-30)),
                            "Deadline": date_prop(_d(30)), "Budget": num_prop(8000), "Hours Estimated": num_prop(80)})
    p2 = add_row(proj_id, {"Project Name": title_prop("Monthly SEO Retainer"), "Client": relation_prop(c1["id"]),
                            "Status": select_prop("In Progress"), "Priority": select_prop("🟡 Medium"),
                            "Type": select_prop("Retainer"), "Budget": num_prop(2000)})

    add_row(tasks_db["id"], {"Task": title_prop("Design homepage mockup"), "Project": relation_prop(p1["id"]),
                              "Status": select_prop("In Progress"), "Priority": select_prop("🔴 High"),
                              "Due Date": date_prop(_d(3)), "Estimated Hours": num_prop(8),
                              "Tags": mselect_prop("Design")})
    add_row(tasks_db["id"], {"Task": title_prop("Write blog post about SEO"), "Project": relation_prop(p2["id"]),
                              "Status": select_prop("To Do"), "Priority": select_prop("🟡 Medium"),
                              "Due Date": date_prop(_d(7)), "Tags": mselect_prop("Writing")})
    add_row(tasks_db["id"], {"Task": title_prop("Client call - review mockups"), "Project": relation_prop(p1["id"]),
                              "Status": select_prop("To Do"), "Priority": select_prop("🟡 Medium"),
                              "Due Date": date_prop(_d(5)), "Tags": mselect_prop("Meeting")})

    for i, desc in enumerate(["Homepage wireframe", "Logo revisions", "SEO audit", "Keyword research", "Content outline"]):
        add_row(timelog_db["id"], {"Description": title_prop(desc), "Project": relation_prop(p1["id"] if i < 2 else p2["id"]),
                                    "Date": date_prop(_d(-i-1)), "Hours": num_prop(2.5 if i % 2 == 0 else 1.5),
                                    "Hourly Rate": num_prop(75), "Billable": checkbox_prop(True)})

    add_row(invoices_db["id"], {"Invoice #": title_prop("INV-001"), "Client": relation_prop(c1["id"]),
                                 "Project": relation_prop(p1["id"]), "Status": select_prop("Paid"),
                                 "Issue Date": date_prop(_d(-30)), "Due Date": date_prop(_d(-15)),
                                 "Amount": num_prop(4000), "Tax": num_prop(0),
                                 "Payment Method": select_prop("Wise"), "Paid Date": date_prop(_d(-14))})
    add_row(invoices_db["id"], {"Invoice #": title_prop("INV-002"), "Client": relation_prop(c1["id"]),
                                 "Project": relation_prop(p2["id"]), "Status": select_prop("Sent"),
                                 "Issue Date": date_prop(_d(-5)), "Due Date": date_prop(_d(10)),
                                 "Amount": num_prop(2000), "Tax": num_prop(0)})

    add_row(expenses_db["id"], {"Expense": title_prop("Figma Pro"), "Category": select_prop("Software"),
                                 "Amount": num_prop(15), "Date": date_prop(_d(-10)), "Recurring": checkbox_prop(True),
                                 "Frequency": select_prop("Monthly"), "Tax Deductible": checkbox_prop(True)})
    add_row(expenses_db["id"], {"Expense": title_prop("Ahrefs subscription"), "Category": select_prop("Software"),
                                 "Amount": num_prop(99), "Date": date_prop(_d(-10)), "Recurring": checkbox_prop(True),
                                 "Frequency": select_prop("Monthly"), "Tax Deductible": checkbox_prop(True)})
    add_row(expenses_db["id"], {"Expense": title_prop("Coworking day pass"), "Category": select_prop("Office"),
                                 "Amount": num_prop(25), "Date": date_prop(_d(-3)), "Tax Deductible": checkbox_prop(True)})

    add_row(proposals_db["id"], {"Proposal Title": title_prop("Beta Agency - Social Media Management"),
                                  "Client": relation_prop(c2["id"]), "Status": select_prop("Sent"),
                                  "Amount": num_prop(3500), "Sent Date": date_prop(_d(-3)),
                                  "Deadline": date_prop(_d(7))})

    add_row(notes_db["id"], {"Title": title_prop("Getting Started Guide"), "Category": select_prop("SOP")})

    # Dashboard content
    append_blocks(pid, [
        heading2("Dashboard"),
        callout("Welcome back! Here's your business at a glance.", "👋"),
        paragraph("Use the linked databases above to manage your freelance business. Check your active projects, pending invoices, and upcoming tasks daily."),
        divider(),
        heading3("Setup Instructions"),
        numbered("Delete all sample data (or keep as reference)"),
        numbered("Customize the Select/Multi-select options to match your business"),
        numbered("Set your default hourly rate in Time Log entries"),
        numbered("Start by adding your current clients and active projects"),
        numbered("Log time daily, send invoices weekly"),
        numbered("Review the Dashboard daily for a quick overview"),
    ])

    return page


# ============================================================================
# TEMPLATE 2: Content Creator Dashboard
# ============================================================================

def create_content_creator(parent: dict) -> dict:
    log.info("=== Template 2: Content Creator Dashboard ===")
    page = create_page(parent, "Content Creator Dashboard", "🎬", [
        heading1("Content Creator Dashboard"),
        paragraph("Plan, create, publish, and analyze your content across all platforms."),
        callout("Your content empire starts here!", "🚀"),
        divider(),
    ])
    pid = page["id"]

    content_db = create_database(pid, "Content", "📹", {
        "Title": p_title(),
        "Platform": p_mselect("YouTube", "Blog", "TikTok", "Instagram", "Twitter/X", "Podcast", "Newsletter", "LinkedIn"),
        "Status": p_select("Idea", "Scripting", "Recording", "Editing", "Scheduled", "Published", "Repurposed"),
        "Content Type": p_select("Video", "Blog Post", "Short/Reel", "Podcast Episode", "Thread", "Newsletter", "Carousel"),
        "Category": p_select("Tutorial", "Vlog", "Review", "Opinion", "Behind the Scenes", "Collaboration"),
        "Publish Date": p_date(),
        "Script/Draft": p_rt(),
        "URL": p_url(),
        "Views": p_number(),
        "Likes": p_number(),
        "Comments": p_number(),
        "Engagement Rate": p_formula('if(prop("Views") > 0, round((prop("Likes") + prop("Comments")) / prop("Views") * 10000) / 100, 0)'),
        "Notes": p_rt(),
    })
    cont_id = content_db["id"]

    ideas_db = create_database(pid, "Ideas", "💡", {
        "Idea": p_title(),
        "Status": p_select("Raw Idea", "Researching", "Ready to Create", "Created", "Discarded"),
        "Platform": p_mselect("YouTube", "Blog", "TikTok", "Instagram", "Twitter/X", "Podcast", "Newsletter"),
        "Priority": p_select("🔥 Hot", "👍 Good", "💡 Maybe Later"),
        "Source": p_select("Audience Request", "Trending", "Competitor", "Personal Experience", "News", "AI Generated"),
        "Keywords": p_rt(),
        "Notes": p_rt(),
        "Content": p_relation_single(cont_id),
        "Created": p_created_time(),
    })

    analytics_db = create_database(pid, "Analytics", "📊", {
        "Period": p_title(),
        "Platform": p_select("YouTube", "Blog", "TikTok", "Instagram", "Twitter/X", "Podcast", "Newsletter"),
        "Date": p_date(),
        "Followers/Subscribers": p_number(),
        "New Followers": p_number(),
        "Total Views": p_number(),
        "Total Engagement": p_number(),
        "Top Content": p_rt(),
        "Notes": p_rt(),
    })

    sponsors_db = create_database(pid, "Sponsors", "🤝", {
        "Brand Name": p_title(),
        "Status": p_select("Lead", "Negotiating", "Confirmed", "Delivered", "Paid", "Declined"),
        "Contact": p_rt(),
        "Email": p_email(),
        "Deal Type": p_select("Sponsored Post", "Affiliate", "Product Review", "Brand Ambassador", "Ad Read"),
        "Payment": p_number("dollar"),
        "Content": p_relation_single(cont_id),
        "Deadline": p_date(),
        "Deliverables": p_rt(),
        "Notes": p_rt(),
    })

    revenue_db = create_database(pid, "Revenue", "💰", {
        "Description": p_title(),
        "Source": p_select("Ad Revenue", "Sponsorship", "Affiliate", "Merch", "Course/Digital Product", "Donations/Tips", "Consulting", "Other"),
        "Platform": p_select("YouTube", "Blog", "TikTok", "Instagram", "Podcast", "Newsletter", "Other"),
        "Amount": p_number("dollar"),
        "Date": p_date(),
        "Content": p_relation_single(cont_id),
        "Recurring": p_checkbox(),
        "Notes": p_rt(),
    })

    equipment_db = create_database(pid, "Equipment", "🎥", {
        "Item": p_title(),
        "Category": p_select("Camera", "Audio", "Lighting", "Computer", "Software", "Accessories", "Other"),
        "Cost": p_number("dollar"),
        "Purchase Date": p_date(),
        "Status": p_select("Active", "Wishlist", "Retired"),
        "Link": p_url(),
        "Notes": p_rt(),
    })

    # Sample data
    log.info("  Adding sample data...")
    add_row(cont_id, {"Title": title_prop("10 Tips for New YouTubers"), "Platform": mselect_prop("YouTube"),
                       "Status": select_prop("Published"), "Content Type": select_prop("Video"),
                       "Publish Date": date_prop(_d(-14)), "Views": num_prop(5200), "Likes": num_prop(310), "Comments": num_prop(45)})
    add_row(cont_id, {"Title": title_prop("How I Edit My Videos in 2026"), "Platform": mselect_prop("YouTube", "Blog"),
                       "Status": select_prop("Editing"), "Content Type": select_prop("Video"),
                       "Publish Date": date_prop(_d(3))})
    add_row(cont_id, {"Title": title_prop("Morning Routine Vlog"), "Platform": mselect_prop("TikTok", "Instagram"),
                       "Status": select_prop("Scheduled"), "Content Type": select_prop("Short/Reel"),
                       "Publish Date": date_prop(_d(1))})
    add_row(cont_id, {"Title": title_prop("Camera Gear 2026 Review"), "Platform": mselect_prop("YouTube"),
                       "Status": select_prop("Scripting"), "Content Type": select_prop("Video")})
    add_row(cont_id, {"Title": title_prop("Productivity Newsletter #12"), "Platform": mselect_prop("Newsletter"),
                       "Status": select_prop("Published"), "Content Type": select_prop("Newsletter"),
                       "Publish Date": date_prop(_d(-7)), "Views": num_prop(1200), "Likes": num_prop(89)})

    for i, idea in enumerate(["AI tools for creators", "Studio tour 2026", "Collab with @techguru",
                               "Newsletter monetization tips", "Day in my life", "Top 5 free editing tools",
                               "Why I quit my 9-5", "Creator economy trends"]):
        status = ["Raw Idea", "Researching", "Ready to Create", "Created"][i % 4]
        prio = ["🔥 Hot", "👍 Good", "💡 Maybe Later"][i % 3]
        add_row(ideas_db["id"], {"Idea": title_prop(idea), "Status": select_prop(status), "Priority": select_prop(prio)})

    add_row(sponsors_db["id"], {"Brand Name": title_prop("TechGadget Co"), "Status": select_prop("Confirmed"),
                                 "Payment": num_prop(500), "Deal Type": select_prop("Sponsored Post"),
                                 "Deadline": date_prop(_d(14))})
    add_row(sponsors_db["id"], {"Brand Name": title_prop("CloudApp"), "Status": select_prop("Negotiating"),
                                 "Payment": num_prop(300), "Deal Type": select_prop("Affiliate")})

    for desc, amt, src in [("YouTube AdSense March", 420, "Ad Revenue"), ("Sponsor - TechGadget", 500, "Sponsorship"),
                            ("Affiliate commission", 85, "Affiliate"), ("Newsletter tips", 50, "Donations/Tips"),
                            ("Course sale", 199, "Course/Digital Product")]:
        add_row(revenue_db["id"], {"Description": title_prop(desc), "Amount": num_prop(amt),
                                    "Source": select_prop(src), "Date": date_prop(_d(-5))})

    for item, cat, cost in [("Sony A7IV", "Camera", 2500), ("Rode NT-USB+", "Audio", 169), ("Elgato Key Light", "Lighting", 200)]:
        add_row(equipment_db["id"], {"Item": title_prop(item), "Category": select_prop(cat),
                                      "Cost": num_prop(cost), "Status": select_prop("Active")})

    append_blocks(pid, [
        heading2("Dashboard"),
        callout("Content Creator HQ -- Check your pipeline, track ideas, and grow your audience!", "🎯"),
        divider(),
        heading3("Setup Instructions"),
        numbered("Customize Platform and Category options to match your channels"),
        numbered("Delete sample data"),
        numbered("Import your existing content ideas into the Ideas Bank"),
        numbered("Plan your first week of content in the Calendar"),
        numbered("Track analytics weekly"),
        numbered("Use the Dashboard daily to stay on track"),
    ])
    return page


# ============================================================================
# TEMPLATE 3: Student Study Hub
# ============================================================================

def create_student_hub(parent: dict) -> dict:
    log.info("=== Template 3: Student Study Hub ===")
    page = create_page(parent, "Student Study Hub", "📚", [
        heading1("Student Study Hub"),
        paragraph("Track courses, assignments, study sessions, grades, and notes all in one place."),
        callout("Stay organized, ace your classes!", "🎓"),
        divider(),
    ])
    pid = page["id"]

    semesters_db = create_database(pid, "Semesters", "📅", {
        "Semester": p_title(),
        "Start Date": p_date(),
        "End Date": p_date(),
        "Status": p_select("Current", "Completed", "Upcoming"),
        "GPA": p_number(),
        "Notes": p_rt(),
    })
    sem_id = semesters_db["id"]

    courses_db = create_database(pid, "Courses", "📖", {
        "Course Name": p_title(),
        "Code": p_rt(),
        "Professor": p_rt(),
        "Semester": p_relation_single(sem_id),
        "Status": p_select("Current", "Completed", "Dropped", "Planned"),
        "Schedule": p_rt(),
        "Location": p_rt(),
        "Credits": p_number(),
        "Color": p_select("🔴 Red", "🔵 Blue", "🟢 Green", "🟡 Yellow", "🟣 Purple", "🟠 Orange"),
    })
    course_id = courses_db["id"]

    assignments_db = create_database(pid, "Assignments", "📝", {
        "Assignment": p_title(),
        "Course": p_relation_single(course_id),
        "Type": p_select("Homework", "Essay", "Project", "Quiz", "Midterm", "Final Exam", "Presentation", "Lab", "Reading"),
        "Status": p_select("Not Started", "In Progress", "Completed", "Submitted", "Graded"),
        "Priority": p_select("🔴 Urgent", "🟡 Medium", "🟢 Low"),
        "Due Date": p_date(),
        "Weight": p_number("percent"),
        "Grade": p_number("percent"),
        "Score": p_rt(),
        "Estimated Hours": p_number(),
        "Notes": p_rt(),
        "Days Until Due": p_formula('dateBetween(prop("Due Date"), now(), "days")'),
    })

    studylog_db = create_database(pid, "Study Log", "⏰", {
        "Session": p_title(),
        "Course": p_relation_single(course_id),
        "Date": p_date(),
        "Duration (hrs)": p_number(),
        "Type": p_select("Reading", "Practice Problems", "Review", "Flashcards", "Group Study", "Office Hours", "Lecture Review"),
        "Productivity": p_select("⭐⭐⭐⭐⭐", "⭐⭐⭐⭐", "⭐⭐⭐", "⭐⭐", "⭐"),
        "Notes": p_rt(),
    })

    notes_db = create_database(pid, "Notes", "🗒️", {
        "Title": p_title(),
        "Course": p_relation_single(course_id),
        "Type": p_select("Lecture Notes", "Reading Notes", "Summary", "Cheat Sheet", "Formula Sheet", "Study Guide"),
        "Date": p_date(),
        "Tags": p_mselect(),
        "Content": p_rt(),
    })

    grades_db = create_database(pid, "Grades", "🏆", {
        "Item": p_title(),
        "Course": p_relation_single(course_id),
        "Type": p_select("Homework", "Quiz", "Midterm", "Final", "Project", "Participation", "Essay"),
        "Weight": p_number("percent"),
        "Score": p_number("percent"),
        "Weighted Score": p_formula('prop("Score") * prop("Weight") / 100'),
        "Date": p_date(),
        "Notes": p_rt(),
    })

    # Sample data
    log.info("  Adding sample data...")
    s1 = add_row(sem_id, {"Semester": title_prop("Spring 2026"), "Start Date": date_prop("2026-01-15"),
                           "End Date": date_prop("2026-05-20"), "Status": select_prop("Current")})

    courses = []
    for name, code, prof, color in [("Intro to CS", "CS101", "Dr. Smith", "🔵 Blue"),
                                     ("Calculus II", "MATH201", "Prof. Johnson", "🔴 Red"),
                                     ("English Composition", "ENG102", "Dr. Williams", "🟢 Green"),
                                     ("Biology", "BIO150", "Prof. Chen", "🟡 Yellow")]:
        c = add_row(course_id, {"Course Name": title_prop(name), "Code": rt_prop(code),
                                 "Professor": rt_prop(prof), "Semester": relation_prop(s1["id"]),
                                 "Status": select_prop("Current"), "Credits": num_prop(3),
                                 "Color": select_prop(color)})
        courses.append(c)

    for title, ci, typ, stat, due in [
        ("HW 3 - Arrays", 0, "Homework", "Submitted", _d(-2)),
        ("Essay: Modern Technology", 2, "Essay", "In Progress", _d(5)),
        ("Lab 4 - Cell Division", 3, "Lab", "Not Started", _d(7)),
        ("Quiz 2 - Derivatives", 1, "Quiz", "Completed", _d(-5)),
        ("Midterm Exam", 0, "Midterm", "Not Started", _d(14)),
        ("Group Project Proposal", 2, "Project", "In Progress", _d(10)),
        ("Problem Set 5", 1, "Homework", "Not Started", _d(3)),
        ("Reading Ch. 8-10", 3, "Reading", "Not Started", _d(2)),
    ]:
        add_row(assignments_db["id"], {"Assignment": title_prop(title), "Course": relation_prop(courses[ci]["id"]),
                                        "Type": select_prop(typ), "Status": select_prop(stat),
                                        "Due Date": date_prop(due), "Priority": select_prop("🔴 Urgent" if int(due.split("-")[2]) - int(TODAY.split("-")[2]) < 5 else "🟡 Medium")})

    for sess, ci, hrs in [("Chapter 5 Review", 0, 2), ("Practice integrals", 1, 1.5),
                           ("Essay outline", 2, 1), ("Bio lab prep", 3, 1.5), ("Coding exercises", 0, 2.5)]:
        add_row(studylog_db["id"], {"Session": title_prop(sess), "Course": relation_prop(courses[ci]["id"]),
                                     "Date": date_prop(_d(-1)), "Duration (hrs)": num_prop(hrs),
                                     "Type": select_prop("Review"), "Productivity": select_prop("⭐⭐⭐⭐")})

    for title, ci in [("CS101 Week 5 Lecture", 0), ("Calc Formulas Sheet", 1), ("Essay Draft Notes", 2)]:
        add_row(notes_db["id"], {"Title": title_prop(title), "Course": relation_prop(courses[ci]["id"]),
                                  "Type": select_prop("Lecture Notes"), "Date": date_prop(_d(-3))})

    for item, ci, typ, w, s in [("HW1", 0, "Homework", 5, 92), ("HW2", 0, "Homework", 5, 88),
                                 ("Quiz 1", 1, "Quiz", 10, 78), ("Essay 1", 2, "Essay", 20, 85)]:
        add_row(grades_db["id"], {"Item": title_prop(item), "Course": relation_prop(courses[ci]["id"]),
                                   "Type": select_prop(typ), "Weight": num_prop(w), "Score": num_prop(s),
                                   "Date": date_prop(_d(-10))})

    append_blocks(pid, [
        heading2("Dashboard"),
        callout("Check your upcoming deadlines, study sessions, and grades here.", "📋"),
        divider(),
        heading3("Setup Instructions"),
        numbered("Update Semester info with your current semester dates"),
        numbered("Add your courses with schedule and professor info"),
        numbered("Enter all known assignments and deadlines from syllabi"),
        numbered("Log study sessions daily to build the habit"),
        numbered("Enter grades as you receive them"),
        numbered("Check Dashboard daily for upcoming deadlines"),
    ])
    return page


# ============================================================================
# TEMPLATE 4: Life OS / Second Brain
# ============================================================================

def create_life_os(parent: dict) -> dict:
    log.info("=== Template 4: Life OS — Second Brain ===")
    page = create_page(parent, "Life OS — Your Complete Second Brain", "🧠", [
        heading1("Life OS — Your Complete Second Brain"),
        paragraph("Organize every area of your life: goals, habits, projects, tasks, notes, journal, finances, and health."),
        callout("Start with the Wheel of Life, then build from there!", "🌟"),
        divider(),
    ])
    pid = page["id"]

    areas_db = create_database(pid, "Areas of Life", "🎯", {
        "Area": p_title(),
        "Icon": p_rt(),
        "Status": p_select("Thriving", "Good", "Needs Attention", "Struggling"),
        "Description": p_rt(),
        "Score (1-10)": p_number(),
        "Last Reviewed": p_date(),
    })
    area_id = areas_db["id"]

    goals_db = create_database(pid, "Goals", "🎯", {
        "Goal": p_title(),
        "Area": p_relation_single(area_id),
        "Timeframe": p_select("This Week", "This Month", "This Quarter", "This Year", "Long-term"),
        "Status": p_select("Not Started", "In Progress", "Achieved", "Paused", "Abandoned"),
        "Priority": p_select("🔴 Must", "🟡 Should", "🟢 Could"),
        "Start Date": p_date(),
        "Target Date": p_date(),
        "Progress": p_number("percent"),
        "Key Results": p_rt(),
        "Notes": p_rt(),
    })
    goal_id = goals_db["id"]

    habits_db = create_database(pid, "Habits", "✅", {
        "Habit": p_title(),
        "Area": p_relation_single(area_id),
        "Frequency": p_select("Daily", "Weekdays", "3x/week", "Weekly"),
        "Time of Day": p_select("Morning", "Afternoon", "Evening", "Anytime"),
        "Status": p_select("Active", "Paused", "Retired"),
        "Streak": p_number(),
        "Best Streak": p_number(),
        "Mon": p_checkbox(), "Tue": p_checkbox(), "Wed": p_checkbox(),
        "Thu": p_checkbox(), "Fri": p_checkbox(), "Sat": p_checkbox(), "Sun": p_checkbox(),
        "Notes": p_rt(),
    })

    projects_db = create_database(pid, "Projects", "📂", {
        "Project": p_title(),
        "Area": p_relation_single(area_id),
        "Goal": p_relation_single(goal_id),
        "Status": p_select("Someday", "Planning", "Active", "Completed", "On Hold", "Cancelled"),
        "Priority": p_select("🔴 High", "🟡 Medium", "🟢 Low"),
        "Start Date": p_date(),
        "Deadline": p_date(),
        "Notes": p_rt(),
    })
    proj_id = projects_db["id"]

    tasks_db = create_database(pid, "Tasks", "☑️", {
        "Task": p_title(),
        "Project": p_relation_single(proj_id),
        "Status": p_select("Inbox", "To Do", "In Progress", "Waiting", "Done"),
        "Priority": p_select("🔴 Urgent+Important", "🟠 Important", "🟡 Urgent", "🟢 Low"),
        "Due Date": p_date(),
        "Energy": p_select("🔋 High", "🔋 Medium", "🔋 Low"),
        "Time Estimate": p_select("5 min", "15 min", "30 min", "1 hr", "2+ hr"),
        "Context": p_mselect("Home", "Office", "Computer", "Phone", "Errands", "Anywhere"),
        "Notes": p_rt(),
    })

    notes_db = create_database(pid, "Notes", "📝", {
        "Title": p_title(),
        "Type": p_select("Note", "Idea", "Quote", "Summary", "How-to", "Reference"),
        "Area": p_relation_single(area_id),
        "Source": p_rt(),
        "Tags": p_mselect(),
        "Created": p_created_time(),
        "Last Edited": p_last_edited_time(),
    })

    resources_db = create_database(pid, "Resources", "📚", {
        "Resource": p_title(),
        "Type": p_select("Book", "Article", "Video", "Podcast", "Course", "Tool", "Website"),
        "Status": p_select("To Review", "In Progress", "Completed", "Reference"),
        "Area": p_relation_single(area_id),
        "URL": p_url(),
        "Rating": p_select("⭐⭐⭐⭐⭐", "⭐⭐⭐⭐", "⭐⭐⭐", "⭐⭐", "⭐"),
        "Key Takeaways": p_rt(),
        "Tags": p_mselect(),
    })

    journal_db = create_database(pid, "Journal", "📔", {
        "Date": p_title(),
        "Date Value": p_date(),
        "Mood": p_select("😊 Great", "🙂 Good", "😐 Okay", "😔 Low", "😫 Bad"),
        "Energy": p_select("🔋 High", "🔋 Medium", "🔋 Low"),
        "Gratitude": p_rt(),
        "Highlights": p_rt(),
        "Learnings": p_rt(),
        "Tomorrow's Focus": p_rt(),
        "Tags": p_mselect(),
    })

    finance_db = create_database(pid, "Finance", "💰", {
        "Description": p_title(),
        "Type": p_select("Income", "Expense", "Investment", "Savings"),
        "Category": p_select("Salary", "Freelance", "Food", "Rent", "Transport", "Entertainment", "Shopping", "Health", "Education", "Subscriptions", "Other"),
        "Amount": p_number("dollar"),
        "Date": p_date(),
        "Recurring": p_checkbox(),
        "Account": p_select("Bank", "Cash", "Credit Card", "PayPal", "Other"),
        "Notes": p_rt(),
    })

    health_db = create_database(pid, "Health", "💪", {
        "Date": p_title(),
        "Date Value": p_date(),
        "Sleep Hours": p_number(),
        "Sleep Quality": p_select("Great", "Good", "Fair", "Poor"),
        "Exercise": p_checkbox(),
        "Exercise Type": p_rt(),
        "Exercise Duration": p_number(),
        "Water (glasses)": p_number(),
        "Weight": p_number(),
        "Mood": p_select("😊 Great", "🙂 Good", "😐 Okay", "😔 Low"),
        "Notes": p_rt(),
    })

    # Sample data
    log.info("  Adding sample data...")
    areas = []
    for name, icon, status, score in [
        ("Career", "💼", "Good", 7), ("Health & Fitness", "🏃", "Needs Attention", 5),
        ("Finances", "💰", "Good", 6), ("Relationships", "❤️", "Thriving", 8),
        ("Personal Growth", "📚", "Good", 7), ("Fun & Recreation", "🎮", "Needs Attention", 4),
        ("Environment", "🏠", "Good", 6), ("Spirituality", "🧘", "Needs Attention", 5),
    ]:
        a = add_row(area_id, {"Area": title_prop(name), "Icon": rt_prop(icon),
                               "Status": select_prop(status), "Score (1-10)": num_prop(score),
                               "Last Reviewed": date_prop(TODAY)})
        areas.append(a)

    for goal, ai, tf, prog in [("Get promoted", 0, "This Year", 40), ("Run a half marathon", 1, "This Quarter", 25),
                                ("Save $10,000", 2, "This Year", 60), ("Read 24 books", 4, "This Year", 30),
                                ("Launch side project", 0, "This Quarter", 15)]:
        add_row(goal_id, {"Goal": title_prop(goal), "Area": relation_prop(areas[ai]["id"]),
                           "Timeframe": select_prop(tf), "Status": select_prop("In Progress"),
                           "Priority": select_prop("🔴 Must"), "Progress": num_prop(prog)})

    for habit, ai, freq in [("Morning meditation", 7, "Daily"), ("Exercise", 1, "Weekdays"),
                             ("Read 30 min", 4, "Daily"), ("Journal", 4, "Daily"),
                             ("Drink 8 glasses water", 1, "Daily"), ("Weekly review", 4, "Weekly"),
                             ("No phone before 9am", 5, "Daily")]:
        add_row(habits_db["id"], {"Habit": title_prop(habit), "Area": relation_prop(areas[ai]["id"]),
                                   "Frequency": select_prop(freq), "Status": select_prop("Active"),
                                   "Streak": num_prop(5)})

    for j_date, mood in [(TODAY, "🙂 Good"), (_d(-1), "😊 Great"), (_d(-2), "😐 Okay")]:
        add_row(journal_db["id"], {"Date": title_prop(j_date), "Date Value": date_prop(j_date),
                                    "Mood": select_prop(mood), "Gratitude": rt_prop("Health, family, good weather")})

    add_row(resources_db["id"], {"Resource": title_prop("Atomic Habits"), "Type": select_prop("Book"),
                                  "Status": select_prop("Completed"), "Rating": select_prop("⭐⭐⭐⭐⭐")})
    add_row(resources_db["id"], {"Resource": title_prop("Deep Work"), "Type": select_prop("Book"),
                                  "Status": select_prop("In Progress"), "Rating": select_prop("⭐⭐⭐⭐")})

    append_blocks(pid, [
        heading2("Command Center"),
        callout("Welcome to your Life OS! Start by rating each Area of Life, then set goals.", "🧠"),
        divider(),
        heading3("Weekly Review Checklist"),
        toggle("Click to expand weekly review prompts", [
            bulleted("Review and update Area scores"),
            bulleted("Check goal progress"),
            bulleted("Plan next week's priorities"),
            bulleted("Review habit streaks"),
            bulleted("Celebrate wins!"),
        ]),
        heading3("Setup Instructions"),
        numbered("Rate each Area of Life 1-10"),
        numbered("Set 1-3 goals per area that needs attention"),
        numbered("Break goals into projects and tasks"),
        numbered("Set up your daily habits"),
        numbered("Journal daily (even 2 minutes counts)"),
        numbered("Do a Weekly Review every Sunday"),
    ])
    return page


# ============================================================================
# TEMPLATE 5: Small Business CRM
# ============================================================================

def create_crm(parent: dict) -> dict:
    log.info("=== Template 5: Small Business CRM ===")
    page = create_page(parent, "Small Business CRM", "🏢", [
        heading1("Small Business CRM"),
        paragraph("Manage contacts, companies, deals, and activities to grow your business."),
        callout("Track every customer interaction and never miss a follow-up!", "📞"),
        divider(),
    ])
    pid = page["id"]

    companies_db = create_database(pid, "Companies", "🏭", {
        "Company Name": p_title(),
        "Industry": p_select("Technology", "Marketing", "Finance", "Retail", "Healthcare", "Education", "Manufacturing", "Consulting", "Other"),
        "Size": p_select("1-10", "11-50", "51-200", "201-1000", "1000+"),
        "Website": p_url(),
        "Address": p_rt(),
        "Status": p_select("Active", "Inactive", "Prospect"),
        "Notes": p_rt(),
    })
    comp_id = companies_db["id"]

    contacts_db = create_database(pid, "Contacts", "👥", {
        "Name": p_title(),
        "Company": p_relation_single(comp_id),
        "Role/Title": p_rt(),
        "Email": p_email(),
        "Phone": p_phone(),
        "Type": p_select("Lead", "Prospect", "Customer", "Partner", "Vendor", "Other"),
        "Status": p_select("Active", "Inactive", "Churned"),
        "Source": p_select("Website", "Referral", "Social Media", "Cold Outreach", "Event", "Ads", "Other"),
        "LinkedIn": p_url(),
        "Tags": p_mselect(),
        "Last Contact": p_date(),
        "Next Follow-up": p_date(),
        "Notes": p_rt(),
        "Created": p_created_time(),
    })
    cont_id = contacts_db["id"]

    products_db = create_database(pid, "Products & Services", "📦", {
        "Product/Service": p_title(),
        "Category": p_select("Consulting", "Software", "Training", "Support", "Custom"),
        "Price": p_number("dollar"),
        "Type": p_select("One-time", "Recurring", "Hourly"),
        "Status": p_select("Active", "Discontinued", "Coming Soon"),
        "Description": p_rt(),
    })
    prod_id = products_db["id"]

    deals_db = create_database(pid, "Deals", "💎", {
        "Deal Name": p_title(),
        "Contact": p_relation_single(cont_id),
        "Company": p_relation_single(comp_id),
        "Stage": p_select("New Lead", "Qualified", "Proposal Sent", "Negotiation", "Closed Won", "Closed Lost"),
        "Amount": p_number("dollar"),
        "Probability": p_number("percent"),
        "Weighted Value": p_formula('prop("Amount") * prop("Probability") / 100'),
        "Product": p_relation_single(prod_id),
        "Close Date": p_date(),
        "Source": p_select("Inbound", "Outbound", "Referral", "Upsell", "Cross-sell"),
        "Lost Reason": p_select("Price", "Competitor", "No Budget", "No Need", "Timing", "No Response", "Other"),
        "Notes": p_rt(),
        "Created": p_created_time(),
    })
    deal_id = deals_db["id"]

    activities_db = create_database(pid, "Activities", "📋", {
        "Activity": p_title(),
        "Type": p_select("Call", "Email", "Meeting", "Demo", "Follow-up", "Note", "Task"),
        "Contact": p_relation_single(cont_id),
        "Deal": p_relation_single(deal_id),
        "Date": p_date(),
        "Status": p_select("Planned", "Completed", "Cancelled"),
        "Duration (min)": p_number(),
        "Outcome": p_rt(),
        "Next Step": p_rt(),
        "Notes": p_rt(),
    })

    # Sample data
    log.info("  Adding sample data...")
    co1 = add_row(comp_id, {"Company Name": title_prop("TechStart Inc"), "Industry": select_prop("Technology"),
                              "Size": select_prop("11-50"), "Website": url_prop("https://techstart.io"),
                              "Status": select_prop("Active")})
    co2 = add_row(comp_id, {"Company Name": title_prop("MarketPro Agency"), "Industry": select_prop("Marketing"),
                              "Size": select_prop("1-10"), "Status": select_prop("Active")})
    co3 = add_row(comp_id, {"Company Name": title_prop("FinanceHub"), "Industry": select_prop("Finance"),
                              "Size": select_prop("51-200"), "Status": select_prop("Prospect")})

    contacts = []
    for name, co, typ, email in [("John Smith", co1, "Customer", "john@techstart.io"),
                                   ("Sarah Lee", co1, "Customer", "sarah@techstart.io"),
                                   ("Mike Chen", co2, "Prospect", "mike@marketpro.com"),
                                   ("Lisa Wang", co3, "Lead", "lisa@financehub.com"),
                                   ("Tom Brown", co2, "Customer", "tom@marketpro.com"),
                                   ("Amy Davis", co3, "Lead", "amy@financehub.com")]:
        c = add_row(cont_id, {"Name": title_prop(name), "Company": relation_prop(co["id"]),
                               "Type": select_prop(typ), "Email": email_prop(email),
                               "Status": select_prop("Active"), "Next Follow-up": date_prop(_d(3))})
        contacts.append(c)

    pr1 = add_row(prod_id, {"Product/Service": title_prop("Web Development Package"), "Price": num_prop(5000),
                              "Type": select_prop("One-time"), "Status": select_prop("Active")})
    pr2 = add_row(prod_id, {"Product/Service": title_prop("Monthly SEO Service"), "Price": num_prop(1500),
                              "Type": select_prop("Recurring"), "Status": select_prop("Active")})
    pr3 = add_row(prod_id, {"Product/Service": title_prop("Consulting (hourly)"), "Price": num_prop(150),
                              "Type": select_prop("Hourly"), "Status": select_prop("Active")})
    pr4 = add_row(prod_id, {"Product/Service": title_prop("Training Workshop"), "Price": num_prop(2000),
                              "Type": select_prop("One-time"), "Status": select_prop("Active")})

    for dname, ci, stage, amt, prob in [("TechStart Web Redesign", 0, "Closed Won", 5000, 100),
                                          ("MarketPro SEO", 2, "Proposal Sent", 1500, 50),
                                          ("FinanceHub Consulting", 3, "Qualified", 3000, 30),
                                          ("TechStart Training", 1, "Negotiation", 2000, 70),
                                          ("MarketPro Website", 4, "New Lead", 5000, 10)]:
        add_row(deal_id, {"Deal Name": title_prop(dname), "Contact": relation_prop(contacts[ci]["id"]),
                           "Stage": select_prop(stage), "Amount": num_prop(amt),
                           "Probability": num_prop(prob), "Close Date": date_prop(_d(14))})

    for act, typ, ci, stat in [("Intro call with Lisa", "Call", 3, "Completed"),
                                 ("Send proposal to Mike", "Email", 2, "Completed"),
                                 ("Demo for FinanceHub", "Demo", 3, "Planned"),
                                 ("Follow up on proposal", "Follow-up", 2, "Planned"),
                                 ("Quarterly review", "Meeting", 0, "Planned"),
                                 ("Check in email", "Email", 4, "Completed"),
                                 ("Contract negotiation", "Meeting", 1, "Planned"),
                                 ("Onboarding call", "Call", 0, "Completed")]:
        add_row(activities_db["id"], {"Activity": title_prop(act), "Type": select_prop(typ),
                                       "Contact": relation_prop(contacts[ci]["id"]),
                                       "Date": date_prop(_d(2)), "Status": select_prop(stat)})

    append_blocks(pid, [
        heading2("Dashboard"),
        callout("CRM Dashboard -- Review your pipeline, follow-ups, and activities daily.", "📊"),
        divider(),
        heading3("Setup Instructions"),
        numbered("Customize Industry, Source, and other Select options"),
        numbered("Add your products/services first"),
        numbered("Import existing contacts"),
        numbered("Create deals for active opportunities"),
        numbered("Log every interaction as an Activity"),
        numbered("Review Pipeline Board daily"),
        numbered("Set follow-up dates for every contact"),
    ])
    return page


# ============================================================================
# TEMPLATE 6: Side Hustle Tracker
# ============================================================================

def create_side_hustle(parent: dict) -> dict:
    log.info("=== Template 6: Side Hustle Tracker ===")
    page = create_page(parent, "Side Hustle Tracker", "🚀", [
        heading1("Side Hustle Tracker"),
        paragraph("Track multiple side hustles, income, expenses, tasks, milestones, and time."),
        callout("Build your empire one hustle at a time!", "💪"),
        divider(),
    ])
    pid = page["id"]

    hustles_db = create_database(pid, "Hustles", "💼", {
        "Hustle Name": p_title(),
        "Type": p_select("Freelance", "E-commerce", "Digital Products", "Content Creation", "Consulting", "Affiliate", "SaaS", "Other"),
        "Status": p_select("Idea", "Validating", "Launching", "Active", "Scaling", "Paused", "Retired"),
        "Started": p_date(),
        "Website": p_url(),
        "Notes": p_rt(),
    })
    h_id = hustles_db["id"]

    income_db = create_database(pid, "Income", "💵", {
        "Description": p_title(),
        "Hustle": p_relation_single(h_id),
        "Amount": p_number("dollar"),
        "Date": p_date(),
        "Source": p_select("Client Payment", "Product Sale", "Ad Revenue", "Affiliate", "Tips", "Subscription", "Other"),
        "Recurring": p_checkbox(),
        "Platform": p_select("Direct", "Gumroad", "Etsy", "Amazon", "Fiverr", "Upwork", "Stripe", "PayPal", "Other"),
        "Notes": p_rt(),
    })

    expenses_db = create_database(pid, "Expenses", "💸", {
        "Description": p_title(),
        "Hustle": p_relation_single(h_id),
        "Amount": p_number("dollar"),
        "Date": p_date(),
        "Category": p_select("Software/Tools", "Marketing", "Inventory", "Hosting", "Design", "Education", "Legal", "Tax", "Other"),
        "Recurring": p_checkbox(),
        "Tax Deductible": p_checkbox(),
        "Notes": p_rt(),
    })

    tasks_db = create_database(pid, "Tasks", "✅", {
        "Task": p_title(),
        "Hustle": p_relation_single(h_id),
        "Status": p_select("To Do", "In Progress", "Waiting", "Done"),
        "Priority": p_select("🔴 High", "🟡 Medium", "🟢 Low"),
        "Due Date": p_date(),
        "Time Estimate": p_select("15 min", "30 min", "1 hr", "2 hr", "Half day", "Full day"),
        "Notes": p_rt(),
    })

    milestones_db = create_database(pid, "Milestones", "🏁", {
        "Milestone": p_title(),
        "Hustle": p_relation_single(h_id),
        "Target Date": p_date(),
        "Status": p_select("Upcoming", "In Progress", "Achieved", "Missed"),
        "Type": p_select("Revenue", "Launch", "Growth", "Product", "Other"),
        "Target Value": p_rt(),
        "Notes": p_rt(),
    })

    time_db = create_database(pid, "Time", "⏰", {
        "Description": p_title(),
        "Hustle": p_relation_single(h_id),
        "Date": p_date(),
        "Hours": p_number(),
        "Type": p_select("Building", "Marketing", "Admin", "Learning", "Client Work", "Planning"),
        "Notes": p_rt(),
    })

    ideas_db = create_database(pid, "Ideas", "💡", {
        "Idea": p_title(),
        "Type": p_select("New Hustle", "Feature", "Marketing", "Product", "Improvement"),
        "Status": p_select("Raw", "Researching", "Validated", "Building", "Discarded"),
        "Potential Revenue": p_select("$", "$$", "$$$", "$$$$"),
        "Effort": p_select("Low", "Medium", "High"),
        "Notes": p_rt(),
        "Created": p_created_time(),
    })

    resources_db = create_database(pid, "Resources", "📚", {
        "Resource": p_title(),
        "Type": p_select("Tool", "Course", "Book", "Article", "Community", "Template"),
        "Category": p_select("Marketing", "Finance", "Productivity", "Technical", "Legal", "Mindset"),
        "URL": p_url(),
        "Cost": p_number("dollar"),
        "Rating": p_select("⭐⭐⭐⭐⭐", "⭐⭐⭐⭐", "⭐⭐⭐", "⭐⭐", "⭐"),
        "Notes": p_rt(),
    })

    # Sample data
    log.info("  Adding sample data...")
    h1 = add_row(h_id, {"Hustle Name": title_prop("Freelance Writing"), "Type": select_prop("Freelance"),
                          "Status": select_prop("Active"), "Started": date_prop("2025-03-01"),
                          "Website": url_prop("https://mywriting.com")})
    h2 = add_row(h_id, {"Hustle Name": title_prop("Print on Demand Store"), "Type": select_prop("E-commerce"),
                          "Status": select_prop("Launching"), "Started": date_prop("2026-01-15")})

    for desc, hi, amt, src in [("Blog post for TechCo", h1, 350, "Client Payment"),
                                ("Monthly retainer - Agency", h1, 1200, "Client Payment"),
                                ("Etsy T-shirt sale", h2, 24.99, "Product Sale"),
                                ("Affiliate commission", h1, 85, "Affiliate"),
                                ("Etsy mug sales (5)", h2, 75, "Product Sale")]:
        add_row(income_db["id"], {"Description": title_prop(desc), "Hustle": relation_prop(hi["id"]),
                                   "Amount": num_prop(amt), "Source": select_prop(src), "Date": date_prop(_d(-5))})

    for desc, hi, amt, cat in [("Canva Pro", h2, 13, "Software/Tools"), ("Printful samples", h2, 45, "Inventory"),
                                ("Grammarly", h1, 12, "Software/Tools"), ("Facebook ads", h2, 50, "Marketing")]:
        add_row(expenses_db["id"], {"Description": title_prop(desc), "Hustle": relation_prop(hi["id"]),
                                     "Amount": num_prop(amt), "Category": select_prop(cat), "Date": date_prop(_d(-3))})

    for task, hi, stat, prio in [("Write article for Client X", h1, "In Progress", "🔴 High"),
                                   ("Design 5 new t-shirt mockups", h2, "To Do", "🟡 Medium"),
                                   ("Set up email marketing", h2, "To Do", "🟡 Medium"),
                                   ("Invoice Client Y", h1, "Done", "🔴 High"),
                                   ("Research SEO keywords", h1, "To Do", "🟢 Low"),
                                   ("Optimize Etsy listings", h2, "In Progress", "🔴 High")]:
        add_row(tasks_db["id"], {"Task": title_prop(task), "Hustle": relation_prop(hi["id"]),
                                  "Status": select_prop(stat), "Priority": select_prop(prio),
                                  "Due Date": date_prop(_d(5))})

    for ms, hi, stat, typ in [("First $1000 month", h1, "Achieved", "Revenue"),
                                ("Launch Etsy store", h2, "Achieved", "Launch"),
                                ("100 Etsy sales", h2, "In Progress", "Growth")]:
        add_row(milestones_db["id"], {"Milestone": title_prop(ms), "Hustle": relation_prop(hi["id"]),
                                       "Status": select_prop(stat), "Type": select_prop(typ),
                                       "Target Date": date_prop(_d(30))})

    for desc, hi, hrs, typ in [("Article writing", h1, 3, "Client Work"), ("T-shirt design session", h2, 2, "Building"),
                                ("Etsy SEO research", h2, 1, "Marketing"), ("Client call", h1, 0.5, "Client Work")]:
        add_row(time_db["id"], {"Description": title_prop(desc), "Hustle": relation_prop(hi["id"]),
                                 "Date": date_prop(_d(-1)), "Hours": num_prop(hrs), "Type": select_prop(typ)})

    for idea, typ, rev in [("Start a newsletter", "New Hustle", "$$$"), ("Create writing course", "Product", "$$$$"),
                            ("Add sticker designs", "Product", "$$"), ("YouTube channel", "New Hustle", "$$$"),
                            ("Automate social media", "Improvement", "$")]:
        add_row(ideas_db["id"], {"Idea": title_prop(idea), "Type": select_prop(typ),
                                  "Status": select_prop("Raw"), "Potential Revenue": select_prop(rev)})

    for res, typ, url_val in [("Notion Templates Guide", "Article", "https://example.com"),
                               ("Side Hustle School Podcast", "Community", "https://sidehustleschool.com"),
                               ("Canva", "Tool", "https://canva.com")]:
        add_row(resources_db["id"], {"Resource": title_prop(res), "Type": select_prop(typ), "URL": url_prop(url_val)})

    append_blocks(pid, [
        heading2("Dashboard"),
        callout("Side Hustle Command Center -- Track all your hustles in one place.", "🎯"),
        divider(),
        heading3("Setup Instructions"),
        numbered("Add your current side hustles with status and details"),
        numbered("Set up milestones for each hustle (next 3-6 months)"),
        numbered("Log income and expenses as they occur"),
        numbered("Track time daily (even 15-minute blocks count)"),
        numbered("Review Dashboard weekly"),
        numbered("Do monthly P&L review per hustle"),
    ])
    return page


# ============================================================================
# TEMPLATE 7: Social Media Planner
# ============================================================================

def create_social_media(parent: dict) -> dict:
    log.info("=== Template 7: Social Media Planner ===")
    page = create_page(parent, "Social Media Planner & Scheduler", "📱", [
        heading1("Social Media Planner & Scheduler"),
        paragraph("Plan, schedule, and analyze your social media content across all platforms."),
        callout("Content is king. Consistency is queen!", "👑"),
        divider(),
    ])
    pid = page["id"]

    pillars_db = create_database(pid, "Content Pillars", "🏛️", {
        "Pillar": p_title(),
        "Description": p_rt(),
        "Percentage": p_number("percent"),
        "Color": p_select("🔴 Red", "🔵 Blue", "🟢 Green", "🟡 Yellow", "🟣 Purple"),
        "Example Topics": p_rt(),
    })
    pill_id = pillars_db["id"]

    campaigns_db = create_database(pid, "Campaigns", "📢", {
        "Campaign Name": p_title(),
        "Status": p_select("Planning", "Active", "Completed", "Paused"),
        "Start Date": p_date(),
        "End Date": p_date(),
        "Goal": p_rt(),
        "Platforms": p_mselect("Instagram", "Twitter/X", "LinkedIn", "TikTok", "Facebook"),
        "Budget": p_number("dollar"),
        "Results": p_rt(),
        "Notes": p_rt(),
    })
    camp_id = campaigns_db["id"]

    hashtags_db = create_database(pid, "Hashtag Library", "#️⃣", {
        "Hashtag Set Name": p_title(),
        "Hashtags": p_rt(),
        "Platform": p_select("Instagram", "Twitter/X", "LinkedIn", "TikTok", "Universal"),
        "Category": p_select("Brand", "Niche", "Trending", "Community", "Campaign"),
        "Size": p_select("Small (<10K)", "Medium (10K-500K)", "Large (500K+)"),
        "Notes": p_rt(),
    })
    hash_id = hashtags_db["id"]

    posts_db = create_database(pid, "Posts", "📝", {
        "Post Title": p_title(),
        "Platform": p_mselect("Instagram", "Twitter/X", "LinkedIn", "TikTok", "Facebook", "Pinterest", "YouTube", "Threads"),
        "Status": p_select("Idea", "Drafting", "Ready", "Scheduled", "Published", "Repurposed"),
        "Content Type": p_select("Image", "Carousel", "Video", "Reel/Short", "Story", "Text", "Poll", "Thread", "Live"),
        "Pillar": p_relation_single(pill_id),
        "Campaign": p_relation_single(camp_id),
        "Publish Date": p_date(),
        "Time": p_select("6 AM", "9 AM", "12 PM", "3 PM", "6 PM", "9 PM"),
        "Caption": p_rt(),
        "Hashtags": p_relation_single(hash_id),
        "CTA": p_select("Link in Bio", "Comment", "Share", "Save", "Visit Website", "DM", "None"),
        "URL": p_url(),
        "Likes": p_number(),
        "Comments": p_number(),
        "Shares": p_number(),
        "Saves": p_number(),
        "Impressions": p_number(),
        "Engagement Rate": p_formula('if(prop("Impressions") > 0, round((prop("Likes") + prop("Comments") + prop("Shares") + prop("Saves")) / prop("Impressions") * 10000) / 100, 0)'),
        "Notes": p_rt(),
    })

    platforms_db = create_database(pid, "Platforms", "🌐", {
        "Platform": p_title(),
        "Username/Handle": p_rt(),
        "URL": p_url(),
        "Followers": p_number(),
        "Posting Frequency": p_select("Daily", "2-3x/week", "Weekly", "Bi-weekly"),
        "Best Times": p_rt(),
        "Content Types": p_mselect("Image", "Video", "Carousel", "Text", "Stories", "Reels"),
        "Goals": p_rt(),
        "Notes": p_rt(),
    })

    analytics_db = create_database(pid, "Analytics", "📊", {
        "Period": p_title(),
        "Platform": p_select("Instagram", "Twitter/X", "LinkedIn", "TikTok", "Facebook", "Pinterest", "YouTube"),
        "Date": p_date(),
        "Followers": p_number(),
        "New Followers": p_number(),
        "Impressions": p_number(),
        "Reach": p_number(),
        "Engagement Rate": p_number("percent"),
        "Top Post": p_rt(),
        "Website Clicks": p_number(),
        "Notes": p_rt(),
    })

    swipe_db = create_database(pid, "Swipe File", "💾", {
        "Title": p_title(),
        "Source": p_rt(),
        "Platform": p_select("Instagram", "Twitter/X", "LinkedIn", "TikTok", "Other"),
        "Type": p_select("Caption", "Hook", "Visual", "Strategy", "Campaign", "Ad"),
        "URL": p_url(),
        "Why It Works": p_rt(),
        "Tags": p_mselect(),
        "Created": p_created_time(),
    })

    # Sample data
    log.info("  Adding sample data...")
    pillars = []
    for name, pct, desc in [("Educational", 30, "How-to, tips, tutorials"),
                              ("Entertaining", 25, "Memes, fun facts, relatable"),
                              ("Inspirational", 15, "Quotes, success stories"),
                              ("Promotional", 20, "Product launches, offers"),
                              ("Behind the Scenes", 10, "Process, team, daily life")]:
        p = add_row(pill_id, {"Pillar": title_prop(name), "Percentage": num_prop(pct), "Description": rt_prop(desc)})
        pillars.append(p)

    camp = add_row(camp_id, {"Campaign Name": title_prop("Spring Launch 2026"), "Status": select_prop("Active"),
                              "Start Date": date_prop(_d(-7)), "End Date": date_prop(_d(21)),
                              "Platforms": mselect_prop("Instagram", "Twitter/X")})

    for title, plat, stat, typ, dt in [
        ("5 Productivity Tips", ("Instagram", "LinkedIn"), "Published", "Carousel", _d(-10)),
        ("Behind the scenes: new product", ("Instagram",), "Published", "Reel/Short", _d(-7)),
        ("Thread: My journey so far", ("Twitter/X",), "Published", "Thread", _d(-5)),
        ("New product announcement", ("Instagram", "Twitter/X", "LinkedIn"), "Scheduled", "Image", _d(1)),
        ("Tutorial: Getting started", ("YouTube", "TikTok"), "Drafting", "Video", _d(5)),
        ("Customer testimonial", ("Instagram",), "Idea", "Video", None),
        ("Weekly tips roundup", ("Twitter/X",), "Ready", "Text", _d(2)),
        ("Q&A session", ("Instagram",), "Idea", "Live", None),
        ("Product demo", ("TikTok", "Instagram"), "Drafting", "Reel/Short", _d(7)),
        ("Industry news commentary", ("LinkedIn",), "Ready", "Text", _d(3)),
    ]:
        props = {"Post Title": title_prop(title), "Platform": mselect_prop(*plat),
                 "Status": select_prop(stat), "Content Type": select_prop(typ)}
        if dt:
            props["Publish Date"] = date_prop(dt)
        if stat == "Published":
            props["Likes"] = num_prop(150)
            props["Comments"] = num_prop(22)
            props["Impressions"] = num_prop(3500)
        add_row(posts_db["id"], props)

    for plat, handle, foll in [("Instagram", "@mybrand", 12500), ("Twitter/X", "@mybrand", 8200),
                                ("LinkedIn", "My Brand", 3400), ("TikTok", "@mybrand", 5600),
                                ("YouTube", "My Brand", 2100)]:
        add_row(platforms_db["id"], {"Platform": title_prop(plat), "Username/Handle": rt_prop(handle),
                                      "Followers": num_prop(foll), "Posting Frequency": select_prop("2-3x/week")})

    for hname, tags, cat in [("Brand Core", "#mybrand #brandname #officialpage", "Brand"),
                               ("Niche Keywords", "#productivity #timemanagement #hustle", "Niche"),
                               ("Trending March", "#trending2026 #viral #fyp", "Trending"),
                               ("Community", "#creatoreconomy #buildinpublic #indiemaker", "Community"),
                               ("Spring Campaign", "#springlaunch #newproduct #limitedoffer", "Campaign"),
                               ("LinkedIn Growth", "#linkedintips #networking #career", "Niche")]:
        add_row(hash_id, {"Hashtag Set Name": title_prop(hname), "Hashtags": rt_prop(tags),
                           "Category": select_prop(cat), "Platform": select_prop("Universal")})

    for title, src, typ in [("Great hook example", "competitor post", "Hook"),
                              ("Viral carousel format", "Instagram explore", "Visual"),
                              ("Storytelling thread", "@creator on X", "Caption"),
                              ("Ad copy that converts", "Facebook Ad Library", "Ad"),
                              ("UGC strategy", "marketing blog", "Strategy")]:
        add_row(swipe_db["id"], {"Title": title_prop(title), "Source": rt_prop(src), "Type": select_prop(typ)})

    append_blocks(pid, [
        heading2("Dashboard"),
        callout("Social Media HQ -- Plan, create, publish, analyze.", "📱"),
        divider(),
        heading3("Setup Instructions"),
        numbered("Set up your Platforms with handles and goals"),
        numbered("Define your Content Pillars and target percentages"),
        numbered("Build your Hashtag Library"),
        numbered("Plan your first week of content in the Calendar"),
        numbered("Use the Kanban to track production status"),
        numbered("Log analytics weekly"),
        numbered("Save inspiration to the Swipe File"),
    ])
    return page


# ============================================================================
# TEMPLATE 8: Job Search Tracker
# ============================================================================

def create_job_search(parent: dict) -> dict:
    log.info("=== Template 8: Job Search Tracker ===")
    page = create_page(parent, "Job Search Tracker", "🔍", [
        heading1("Job Search Tracker"),
        paragraph("Track applications, companies, interviews, networking contacts, and skills."),
        callout("You've got this! Stay organized and persistent.", "💪"),
        divider(),
    ])
    pid = page["id"]

    companies_db = create_database(pid, "Companies", "🏢", {
        "Company Name": p_title(),
        "Industry": p_select("Tech", "Finance", "Healthcare", "Education", "Marketing", "Consulting", "Retail", "Startup", "Other"),
        "Size": p_select("Startup (1-50)", "Small (51-200)", "Medium (201-1000)", "Large (1000+)", "Enterprise (10000+)"),
        "Website": p_url(),
        "Glassdoor Rating": p_number(),
        "Culture Notes": p_rt(),
        "Pros": p_rt(),
        "Cons": p_rt(),
        "Salary Range": p_rt(),
        "Interview Process": p_rt(),
        "Notes": p_rt(),
    })
    comp_id = companies_db["id"]

    contacts_db = create_database(pid, "Contacts", "👥", {
        "Name": p_title(),
        "Company": p_relation_single(comp_id),
        "Title/Role": p_rt(),
        "Email": p_email(),
        "LinkedIn": p_url(),
        "Phone": p_phone(),
        "Relationship": p_select("Recruiter", "Hiring Manager", "Referral", "Former Colleague", "Alumni", "Networking", "Other"),
        "Last Contact": p_date(),
        "Next Follow-up": p_date(),
        "Notes": p_rt(),
        "Status": p_select("Active", "Inactive"),
    })
    cont_id = contacts_db["id"]

    apps_db = create_database(pid, "Applications", "📋", {
        "Position": p_title(),
        "Company": p_relation_single(comp_id),
        "Status": p_select("Bookmarked", "Applied", "Phone Screen", "Interview", "Technical", "Final Round", "Offer", "Rejected", "Withdrawn", "Ghosted"),
        "Priority": p_select("🔥 Dream Job", "👍 Good Fit", "💼 Backup"),
        "Salary Range": p_rt(),
        "Location": p_rt(),
        "Work Type": p_select("Remote", "Hybrid", "On-site"),
        "Job Type": p_select("Full-time", "Part-time", "Contract", "Freelance", "Internship"),
        "Applied Date": p_date(),
        "Source": p_select("LinkedIn", "Indeed", "Company Website", "Referral", "Recruiter", "Job Board", "Networking", "Other"),
        "Job URL": p_url(),
        "Resume Version": p_rt(),
        "Cover Letter": p_checkbox(),
        "Contacts": p_relation_single(cont_id),
        "Next Step": p_rt(),
        "Next Date": p_date(),
        "Notes": p_rt(),
        "Days Since Applied": p_formula('if(empty(prop("Applied Date")), 0, dateBetween(now(), prop("Applied Date"), "days"))'),
        "Excitement (1-5)": p_number(),
    })
    app_id = apps_db["id"]

    interviews_db = create_database(pid, "Interviews", "🎤", {
        "Interview": p_title(),
        "Application": p_relation_single(app_id),
        "Type": p_select("Phone Screen", "Video Call", "Technical", "Behavioral", "Case Study", "Panel", "On-site", "Final"),
        "Date": p_date(),
        "Time": p_rt(),
        "Duration": p_rt(),
        "Interviewer": p_rt(),
        "Status": p_select("Scheduled", "Completed", "Cancelled", "Rescheduled"),
        "Questions Asked": p_rt(),
        "My Questions": p_rt(),
        "Performance": p_select("Crushed it", "Good", "Okay", "Could be better", "Bombed"),
        "Feedback": p_rt(),
        "Follow-up Sent": p_checkbox(),
        "Notes": p_rt(),
    })

    skills_db = create_database(pid, "Skills", "🛠️", {
        "Skill": p_title(),
        "Category": p_select("Technical", "Soft Skill", "Tool", "Language", "Certification"),
        "Level": p_select("Beginner", "Intermediate", "Advanced", "Expert"),
        "Priority to Improve": p_select("🔴 High", "🟡 Medium", "🟢 Low"),
        "In Resume": p_checkbox(),
        "Notes": p_rt(),
    })

    resources_db = create_database(pid, "Resources", "📚", {
        "Resource": p_title(),
        "Type": p_select("Job Board", "Resume Tool", "Interview Prep", "Networking", "Salary Info", "Course", "Article"),
        "URL": p_url(),
        "Notes": p_rt(),
        "Rating": p_select("⭐⭐⭐⭐⭐", "⭐⭐⭐⭐", "⭐⭐⭐"),
    })

    # Sample data
    log.info("  Adding sample data...")
    co1 = add_row(comp_id, {"Company Name": title_prop("Google"), "Industry": select_prop("Tech"),
                              "Size": select_prop("Enterprise (10000+)"), "Website": url_prop("https://google.com"),
                              "Glassdoor Rating": num_prop(4.3), "Pros": rt_prop("Great perks, smart colleagues")})
    co2 = add_row(comp_id, {"Company Name": title_prop("Stripe"), "Industry": select_prop("Tech"),
                              "Size": select_prop("Large (1000+)"), "Website": url_prop("https://stripe.com"),
                              "Glassdoor Rating": num_prop(4.2)})
    co3 = add_row(comp_id, {"Company Name": title_prop("Notion"), "Industry": select_prop("Tech"),
                              "Size": select_prop("Medium (201-1000)"), "Website": url_prop("https://notion.so"),
                              "Glassdoor Rating": num_prop(4.5)})

    ct1 = add_row(cont_id, {"Name": title_prop("Jane Recruiter"), "Company": relation_prop(co1["id"]),
                              "Relationship": select_prop("Recruiter"), "Email": email_prop("jane@google.com"),
                              "Status": select_prop("Active"), "Next Follow-up": date_prop(_d(3))})
    ct2 = add_row(cont_id, {"Name": title_prop("Bob Manager"), "Company": relation_prop(co2["id"]),
                              "Relationship": select_prop("Hiring Manager"), "Status": select_prop("Active")})
    ct3 = add_row(cont_id, {"Name": title_prop("Alice Alumni"), "Company": relation_prop(co3["id"]),
                              "Relationship": select_prop("Alumni"), "Status": select_prop("Active")})
    ct4 = add_row(cont_id, {"Name": title_prop("Charlie Referral"), "Relationship": select_prop("Referral"),
                              "Status": select_prop("Active")})

    apps = []
    for pos, co, stat, prio, wt, exc in [
        ("Software Engineer", co1, "Interview", "🔥 Dream Job", "Remote", 5),
        ("Backend Developer", co2, "Applied", "👍 Good Fit", "Hybrid", 4),
        ("Product Manager", co3, "Phone Screen", "🔥 Dream Job", "Remote", 5),
        ("Full Stack Developer", co1, "Rejected", "👍 Good Fit", "On-site", 3),
        ("DevOps Engineer", co2, "Bookmarked", "💼 Backup", "Remote", 3),
    ]:
        a = add_row(app_id, {"Position": title_prop(pos), "Company": relation_prop(co["id"]),
                               "Status": select_prop(stat), "Priority": select_prop(prio),
                               "Work Type": select_prop(wt), "Job Type": select_prop("Full-time"),
                               "Applied Date": date_prop(_d(-10)), "Excitement (1-5)": num_prop(exc)})
        apps.append(a)

    for title, ai, typ, stat in [("Phone Screen - Google", 0, "Phone Screen", "Completed"),
                                   ("Technical Interview - Google", 0, "Technical", "Scheduled"),
                                   ("Intro Call - Notion", 2, "Phone Screen", "Scheduled")]:
        add_row(interviews_db["id"], {"Interview": title_prop(title), "Application": relation_prop(apps[ai]["id"]),
                                       "Type": select_prop(typ), "Date": date_prop(_d(3)),
                                       "Status": select_prop(stat)})

    for skill, cat, lvl, resume in [("Python", "Technical", "Advanced", True), ("JavaScript", "Technical", "Intermediate", True),
                                     ("React", "Technical", "Intermediate", True), ("SQL", "Technical", "Advanced", True),
                                     ("AWS", "Technical", "Intermediate", True), ("Docker", "Tool", "Intermediate", True),
                                     ("Communication", "Soft Skill", "Advanced", False), ("Leadership", "Soft Skill", "Intermediate", False),
                                     ("Spanish", "Language", "Beginner", False), ("PMP", "Certification", "Beginner", False)]:
        add_row(skills_db["id"], {"Skill": title_prop(skill), "Category": select_prop(cat),
                                   "Level": select_prop(lvl), "In Resume": checkbox_prop(resume)})

    for res, typ, url_val in [("LinkedIn Jobs", "Job Board", "https://linkedin.com/jobs"),
                               ("Indeed", "Job Board", "https://indeed.com"),
                               ("Glassdoor", "Salary Info", "https://glassdoor.com"),
                               ("LeetCode", "Interview Prep", "https://leetcode.com"),
                               ("Resumake", "Resume Tool", "https://resumake.io")]:
        add_row(resources_db["id"], {"Resource": title_prop(res), "Type": select_prop(typ), "URL": url_prop(url_val)})

    append_blocks(pid, [
        heading2("Dashboard"),
        callout("Job Search HQ -- You've got this! Track everything and stay persistent.", "🔍"),
        divider(),
        heading3("Setup Instructions"),
        numbered("Research and add target companies"),
        numbered("Track every application immediately after applying"),
        numbered("Log all networking contacts with follow-up dates"),
        numbered("Use Interview Prep section before each interview"),
        numbered("Update the Pipeline Board daily"),
        numbered("Review weekly stats every Sunday to adjust strategy"),
    ])
    return page


# ============================================================================
# TEMPLATE 9: Book & Learning Tracker
# ============================================================================

def create_book_tracker(parent: dict) -> dict:
    log.info("=== Template 9: Book & Learning Tracker ===")
    page = create_page(parent, "Book & Learning Tracker", "📖", [
        heading1("Book & Learning Tracker"),
        paragraph("Track your reading, courses, notes, and learning journey."),
        callout("A reader lives a thousand lives. Track them all here!", "📚"),
        divider(),
    ])
    pid = page["id"]

    challenge_db = create_database(pid, "Reading Challenge", "🏆", {
        "Year": p_title(),
        "Goal": p_number(),
        "Completed": p_number(),
        "Progress": p_formula('if(prop("Goal") > 0, round(prop("Completed") / prop("Goal") * 100), 0)'),
        "Status": p_select("Active", "Completed", "Abandoned"),
        "Notes": p_rt(),
    })
    ch_id = challenge_db["id"]

    books_db = create_database(pid, "Books", "📕", {
        "Title": p_title(),
        "Author": p_rt(),
        "Status": p_select("Wishlist", "To Read", "Reading", "Completed", "DNF (Did Not Finish)", "Re-reading"),
        "Genre": p_mselect("Fiction", "Non-fiction", "Self-help", "Business", "Science", "Biography", "Fantasy", "Sci-Fi", "History", "Psychology", "Philosophy", "Technical"),
        "Format": p_select("Physical", "Kindle", "Audiobook", "PDF"),
        "Pages": p_number(),
        "Current Page": p_number(),
        "Progress": p_formula('if(prop("Pages") > 0, round(prop("Current Page") / prop("Pages") * 100), 0)'),
        "Rating": p_select("⭐⭐⭐⭐⭐", "⭐⭐⭐⭐", "⭐⭐⭐", "⭐⭐", "⭐"),
        "Start Date": p_date(),
        "Finish Date": p_date(),
        "Source/Recommendation": p_rt(),
        "Key Takeaway": p_rt(),
        "Would Recommend": p_checkbox(),
        "Challenge": p_relation_single(ch_id),
    })
    book_id = books_db["id"]

    courses_db = create_database(pid, "Courses", "🎓", {
        "Course Name": p_title(),
        "Platform": p_select("Udemy", "Coursera", "YouTube", "Skillshare", "LinkedIn Learning", "edX", "Book", "Podcast", "Other"),
        "Instructor": p_rt(),
        "Status": p_select("Wishlist", "Not Started", "In Progress", "Completed", "Dropped"),
        "Category": p_select("Programming", "Design", "Business", "Marketing", "Data Science", "Language", "Personal Development", "Other"),
        "Progress": p_number("percent"),
        "Rating": p_select("⭐⭐⭐⭐⭐", "⭐⭐⭐⭐", "⭐⭐⭐", "⭐⭐", "⭐"),
        "URL": p_url(),
        "Cost": p_number("dollar"),
        "Start Date": p_date(),
        "Finish Date": p_date(),
        "Certificate": p_checkbox(),
        "Key Takeaways": p_rt(),
    })
    course_id = courses_db["id"]

    notes_db = create_database(pid, "Notes & Highlights", "📝", {
        "Title": p_title(),
        "Source": p_select("Book", "Course", "Article", "Podcast", "Video", "Own Thought"),
        "Book": p_relation_single(book_id),
        "Course": p_relation_single(course_id),
        "Type": p_select("Highlight", "Summary", "Quote", "Key Concept", "Action Item", "Question"),
        "Chapter/Section": p_rt(),
        "Page Number": p_number(),
        "Content": p_rt(),
        "Tags": p_mselect(),
        "Created": p_created_time(),
    })

    readinglog_db = create_database(pid, "Reading Log", "📅", {
        "Entry": p_title(),
        "Book": p_relation_single(book_id),
        "Date": p_date(),
        "Pages Read": p_number(),
        "Time (min)": p_number(),
        "Notes": p_rt(),
    })

    # Sample data
    log.info("  Adding sample data...")
    ch = add_row(ch_id, {"Year": title_prop("2026"), "Goal": num_prop(24), "Completed": num_prop(7),
                          "Status": select_prop("Active")})

    books = []
    for title, author, stat, genre, pages, cp, rating, rec in [
        ("Atomic Habits", "James Clear", "Completed", "Self-help", 320, 320, "⭐⭐⭐⭐⭐", True),
        ("Deep Work", "Cal Newport", "Reading", "Business", 296, 180, None, False),
        ("Sapiens", "Yuval Noah Harari", "To Read", "History", 443, 0, None, False),
        ("The Pragmatic Programmer", "Andy Hunt", "Completed", "Technical", 352, 352, "⭐⭐⭐⭐", True),
        ("Dune", "Frank Herbert", "Wishlist", "Sci-Fi", 412, 0, None, False),
        ("Thinking, Fast and Slow", "Daniel Kahneman", "Completed", "Psychology", 499, 499, "⭐⭐⭐⭐⭐", True),
    ]:
        props: dict = {"Title": title_prop(title), "Author": rt_prop(author), "Status": select_prop(stat),
                 "Genre": mselect_prop(genre), "Pages": num_prop(pages), "Current Page": num_prop(cp),
                 "Challenge": relation_prop(ch["id"]), "Would Recommend": checkbox_prop(rec)}
        if rating:
            props["Rating"] = select_prop(rating)
        if stat == "Completed":
            props["Start Date"] = date_prop(_d(-60))
            props["Finish Date"] = date_prop(_d(-10))
        elif stat == "Reading":
            props["Start Date"] = date_prop(_d(-14))
        b = add_row(book_id, props)
        books.append(b)

    for cname, plat, stat, cat, prog in [
        ("Python for Data Science", "Udemy", "In Progress", "Programming", 65),
        ("UI/UX Design Fundamentals", "Coursera", "Completed", "Design", 100),
        ("Marketing Strategy", "YouTube", "Not Started", "Marketing", 0),
    ]:
        add_row(course_id, {"Course Name": title_prop(cname), "Platform": select_prop(plat),
                              "Status": select_prop(stat), "Category": select_prop(cat),
                              "Progress": num_prop(prog)})

    for ntitle, bi, typ in [("The 4 Laws of Behavior Change", 0, "Key Concept"),
                              ("Deep Work Protocol", 1, "Summary"),
                              ("System 1 vs System 2", 5, "Key Concept")]:
        add_row(notes_db["id"], {"Title": title_prop(ntitle), "Source": select_prop("Book"),
                                  "Book": relation_prop(books[bi]["id"]), "Type": select_prop(typ)})

    for entry, bi, pages_read in [("Morning reading", 1, 25), ("Evening session", 1, 15), ("Lunch break", 1, 10)]:
        add_row(readinglog_db["id"], {"Entry": title_prop(entry), "Book": relation_prop(books[1]["id"]),
                                       "Date": date_prop(_d(-1)), "Pages Read": num_prop(pages_read),
                                       "Time (min)": num_prop(30)})

    append_blocks(pid, [
        heading2("Dashboard"),
        callout("Track your reading journey and never forget what you learn!", "📖"),
        paragraph(f"2026 Reading Challenge: 7/24 books (29%)"),
        divider(),
        heading3("Setup Instructions"),
        numbered("Set your annual reading goal in Reading Challenge"),
        numbered("Add books you're currently reading"),
        numbered("Import your to-read and wishlist books"),
        numbered("Take notes as you read (highlights, key concepts)"),
        numbered("Log daily reading sessions"),
        numbered("Add courses you're taking or want to take"),
        numbered("Review your notes periodically to retain knowledge"),
    ])
    return page


# ============================================================================
# TEMPLATE 10: Digital Products Business OS
# ============================================================================

def create_digital_products(parent: dict) -> dict:
    log.info("=== Template 10: Digital Products Business OS ===")
    page = create_page(parent, "Digital Products Business OS", "🛍️", [
        heading1("Digital Products Business OS"),
        paragraph("Manage your digital products empire: products, sales, marketing, feedback, and roadmap."),
        callout("Build once, sell forever!", "💎"),
        divider(),
    ])
    pid = page["id"]

    products_db = create_database(pid, "Products", "📦", {
        "Product Name": p_title(),
        "Type": p_select("Template", "Course", "eBook", "Plugin", "SaaS", "Printable", "Preset/Filter", "Other"),
        "Status": p_select("Idea", "Building", "Beta", "Live", "Retired"),
        "Platform": p_mselect("Gumroad", "Etsy", "Shopify", "Own Website", "Creative Market", "Teachable", "Other"),
        "Price": p_number("dollar"),
        "Category": p_select("Productivity", "Design", "Business", "Education", "Creative", "Marketing", "Technical", "Other"),
        "URL": p_url(),
        "Launch Date": p_date(),
        "Description": p_rt(),
        "Notes": p_rt(),
    })
    prod_id = products_db["id"]

    sales_db = create_database(pid, "Sales", "💰", {
        "Transaction": p_title(),
        "Product": p_relation_single(prod_id),
        "Amount": p_number("dollar"),
        "Platform Fee": p_number("dollar"),
        "Net": p_formula('prop("Amount") - prop("Platform Fee")'),
        "Date": p_date(),
        "Platform": p_select("Gumroad", "Etsy", "Shopify", "Own Website", "Creative Market", "Other"),
        "Customer Email": p_rt(),
        "Country": p_rt(),
        "Coupon Used": p_checkbox(),
        "Notes": p_rt(),
    })

    marketing_db = create_database(pid, "Marketing", "📣", {
        "Campaign": p_title(),
        "Product": p_relation_single(prod_id),
        "Channel": p_select("SEO", "Social Media", "Email", "Paid Ads", "Product Hunt", "Reddit", "YouTube", "Partnerships", "Other"),
        "Status": p_select("Planning", "Active", "Completed", "Paused"),
        "Start Date": p_date(),
        "End Date": p_date(),
        "Budget": p_number("dollar"),
        "Leads Generated": p_number(),
        "Sales Generated": p_number(),
        "ROI": p_formula('if(prop("Budget") > 0, round((prop("Sales Generated") - prop("Budget")) / prop("Budget") * 100), 0)'),
        "Notes": p_rt(),
    })

    feedback_db = create_database(pid, "Feedback", "💬", {
        "Feedback": p_title(),
        "Product": p_relation_single(prod_id),
        "Type": p_select("Feature Request", "Bug Report", "Praise", "Complaint", "Question", "Suggestion"),
        "Source": p_select("Email", "Review", "Social Media", "Support Ticket", "Survey"),
        "Priority": p_select("🔴 High", "🟡 Medium", "🟢 Low"),
        "Status": p_select("New", "Reviewing", "Planned", "Implemented", "Won't Fix"),
        "Customer": p_rt(),
        "Date": p_date(),
        "Notes": p_rt(),
    })

    roadmap_db = create_database(pid, "Roadmap", "🗺️", {
        "Feature/Task": p_title(),
        "Product": p_relation_single(prod_id),
        "Status": p_select("Backlog", "Planned", "In Progress", "Testing", "Done"),
        "Priority": p_select("🔴 Critical", "🟡 High", "🟢 Medium", "⚪ Low"),
        "Quarter": p_select("Q1 2026", "Q2 2026", "Q3 2026", "Q4 2026"),
        "Type": p_select("New Feature", "Improvement", "Bug Fix", "Content", "Marketing", "Infrastructure"),
        "Effort": p_select("XS", "S", "M", "L", "XL"),
        "Due Date": p_date(),
        "Notes": p_rt(),
    })

    # Sample data
    log.info("  Adding sample data...")
    pr1 = add_row(prod_id, {"Product Name": title_prop("Notion Freelance OS"), "Type": select_prop("Template"),
                              "Status": select_prop("Live"), "Platform": mselect_prop("Gumroad"),
                              "Price": num_prop(19), "Category": select_prop("Productivity"),
                              "Launch Date": date_prop("2026-01-15")})
    pr2 = add_row(prod_id, {"Product Name": title_prop("Social Media Planner"), "Type": select_prop("Template"),
                              "Status": select_prop("Live"), "Platform": mselect_prop("Gumroad", "Etsy"),
                              "Price": num_prop(14), "Category": select_prop("Marketing"),
                              "Launch Date": date_prop("2026-02-01")})
    pr3 = add_row(prod_id, {"Product Name": title_prop("SEO Checklist eBook"), "Type": select_prop("eBook"),
                              "Status": select_prop("Building"), "Price": num_prop(12),
                              "Category": select_prop("Marketing")})

    for i in range(8):
        p = pr1 if i < 5 else pr2
        amt = 19 if i < 5 else 14
        add_row(sales_db["id"], {"Transaction": title_prop(f"Sale #{i+1}"), "Product": relation_prop(p["id"]),
                                   "Amount": num_prop(amt), "Platform Fee": num_prop(round(amt * 0.1, 2)),
                                   "Date": date_prop(_d(-i*3)), "Platform": select_prop("Gumroad")})

    for camp, pi, ch, stat in [("Twitter launch thread", pr1, "Social Media", "Completed"),
                                 ("Reddit post - r/Notion", pr1, "Reddit", "Completed"),
                                 ("Email blast to list", pr2, "Email", "Active"),
                                 ("SEO blog post", pr2, "SEO", "Planning")]:
        add_row(marketing_db["id"], {"Campaign": title_prop(camp), "Product": relation_prop(pi["id"]),
                                      "Channel": select_prop(ch), "Status": select_prop(stat)})

    for fb, pi, typ, prio in [("Add dark mode", pr1, "Feature Request", "🟡 Medium"),
                                ("Love the dashboard!", pr1, "Praise", "🟢 Low"),
                                ("Calendar view broken on mobile", pr2, "Bug Report", "🔴 High"),
                                ("Add hashtag analytics", pr2, "Feature Request", "🟡 Medium")]:
        add_row(feedback_db["id"], {"Feedback": title_prop(fb), "Product": relation_prop(pi["id"]),
                                     "Type": select_prop(typ), "Priority": select_prop(prio),
                                     "Status": select_prop("New"), "Date": date_prop(_d(-5))})

    for feat, pi, stat, q in [("Dark mode for all templates", pr1, "Planned", "Q2 2026"),
                                ("Mobile optimization", pr2, "In Progress", "Q1 2026"),
                                ("Launch SEO eBook", pr3, "In Progress", "Q1 2026"),
                                ("Create video tutorials", pr1, "Backlog", "Q2 2026"),
                                ("Etsy listing for Freelance OS", pr1, "Planned", "Q1 2026")]:
        add_row(roadmap_db["id"], {"Feature/Task": title_prop(feat), "Product": relation_prop(pi["id"]),
                                    "Status": select_prop(stat), "Quarter": select_prop(q)})

    append_blocks(pid, [
        heading2("Dashboard"),
        callout("Digital Products HQ -- Build, launch, sell, iterate.", "🛍️"),
        divider(),
        heading3("Setup Instructions"),
        numbered("Add your current and planned products"),
        numbered("Connect your sales platforms (manual entry or integrate)"),
        numbered("Plan marketing campaigns for each product"),
        numbered("Collect and organize customer feedback"),
        numbered("Use the Roadmap to plan improvements"),
        numbered("Review sales and feedback weekly"),
    ])
    return page


# ============================================================================
# MAIN
# ============================================================================

TEMPLATE_BUILDERS = [
    ("01 Freelance Business OS ($19)", create_freelance_os),
    ("02 Content Creator Dashboard ($15)", create_content_creator),
    ("03 Student Study Hub ($9)", create_student_hub),
    ("04 Life OS Second Brain ($19)", create_life_os),
    ("05 Small Business CRM ($17)", create_crm),
    ("06 Side Hustle Tracker ($12)", create_side_hustle),
    ("07 Social Media Planner ($14)", create_social_media),
    ("08 Job Search Tracker ($9)", create_job_search),
    ("09 Book & Learning Tracker ($9)", create_book_tracker),
    ("10 Digital Products Business OS ($15)", create_digital_products),
]


def main():
    parser = argparse.ArgumentParser(description="Create 10 Notion templates for Gumroad")
    parser.add_argument("--parent-page-id", help="Parent page ID to nest templates under (optional)")
    parser.add_argument("--only", type=int, help="Create only template N (1-10)")
    parser.add_argument("--dashboard-only", action="store_true",
                        help="Skip page/DB creation; only append dashboard blocks to existing pages (uses docs/template_links.json)")
    args = parser.parse_args()

    if not NOTION_TOKEN:
        print("ERROR: Set NOTION_TOKEN environment variable first.")
        print('  set NOTION_TOKEN=secret_xxx')
        sys.exit(1)

    # --dashboard-only mode: skip creation, just append dashboard blocks to existing pages
    if args.dashboard_only:
        links_path = os.path.join(os.path.dirname(__file__), "..", "docs", "template_links.json")
        if not os.path.exists(links_path):
            print(f"ERROR: {links_path} not found. Run full creation first.")
            sys.exit(1)
        with open(links_path, "r", encoding="utf-8") as f:
            template_links = json.load(f)

        dashboard_blocks = [
            # 1: Freelance Business OS
            [heading2("Dashboard"),
             callout("Welcome back! Here's your business at a glance.", "👋"),
             paragraph("Use the linked databases above to manage your freelance business. Check your active projects, pending invoices, and upcoming tasks daily."),
             divider(),
             heading3("Setup Instructions"),
             numbered("Delete all sample data (or keep as reference)"),
             numbered("Customize the Select/Multi-select options to match your business"),
             numbered("Set your default hourly rate in Time Log entries"),
             numbered("Start by adding your current clients and active projects"),
             numbered("Log time daily, send invoices weekly"),
             numbered("Review the Dashboard daily for a quick overview")],
            # 2: Content Creator Dashboard
            [heading2("Dashboard"),
             callout("Content Creator HQ -- Check your pipeline, track ideas, and grow your audience!", "🎯"),
             divider(),
             heading3("Setup Instructions"),
             numbered("Customize Platform and Category options to match your channels"),
             numbered("Delete sample data"),
             numbered("Import your existing content ideas into the Ideas Bank"),
             numbered("Plan your first week of content in the Calendar"),
             numbered("Track analytics weekly"),
             numbered("Use the Dashboard daily to stay on track")],
            # 3: Student Study Hub
            [heading2("Dashboard"),
             callout("Check your upcoming deadlines, study sessions, and grades here.", "📋"),
             divider(),
             heading3("Setup Instructions"),
             numbered("Update Semester info with your current semester dates"),
             numbered("Add your courses with schedule and professor info"),
             numbered("Enter all known assignments and deadlines from syllabi"),
             numbered("Log study sessions daily to build the habit"),
             numbered("Enter grades as you receive them"),
             numbered("Check Dashboard daily for upcoming deadlines")],
            # 4: Life OS Second Brain
            [heading2("Command Center"),
             callout("Welcome to your Life OS! Start by rating each Area of Life, then set goals.", "🧠"),
             divider(),
             heading3("Weekly Review Checklist"),
             toggle("Click to expand weekly review prompts", [
                 bulleted("Review and update Area scores"),
                 bulleted("Check goal progress"),
                 bulleted("Plan next week's priorities"),
                 bulleted("Review habit streaks"),
                 bulleted("Celebrate wins!"),
             ]),
             heading3("Setup Instructions"),
             numbered("Rate each Area of Life 1-10"),
             numbered("Set 1-3 goals per area that needs attention"),
             numbered("Break goals into projects and tasks")],
            # 5: Small Business CRM
            [heading2("Dashboard"),
             callout("CRM Dashboard -- Review your pipeline, follow-ups, and activities daily.", "📊"),
             divider(),
             heading3("Setup Instructions"),
             numbered("Customize Industry, Source, and other Select options"),
             numbered("Add your products/services first"),
             numbered("Import existing contacts"),
             numbered("Create deals for active opportunities"),
             numbered("Log every interaction as an Activity"),
             numbered("Review Pipeline Board daily"),
             numbered("Set follow-up dates for every contact")],
            # 6: Side Hustle Tracker
            [heading2("Dashboard"),
             callout("Side Hustle Command Center -- Track all your hustles in one place.", "🎯"),
             divider(),
             heading3("Setup Instructions"),
             numbered("Add your current side hustles with status and details"),
             numbered("Set up milestones for each hustle (next 3-6 months)"),
             numbered("Log income and expenses as they occur"),
             numbered("Track time daily (even 15-minute blocks count)"),
             numbered("Review Dashboard weekly"),
             numbered("Do monthly P&L review per hustle")],
            # 7: Social Media Planner
            [heading2("Dashboard"),
             callout("Social Media HQ -- Plan, create, publish, analyze.", "📱"),
             divider(),
             heading3("Setup Instructions"),
             numbered("Set up your Platforms with handles and goals"),
             numbered("Define your Content Pillars and target percentages"),
             numbered("Build your Hashtag Library"),
             numbered("Plan your first week of content in the Calendar"),
             numbered("Use the Kanban to track production status"),
             numbered("Log analytics weekly"),
             numbered("Save inspiration to the Swipe File")],
            # 8: Job Search Tracker
            [heading2("Dashboard"),
             callout("Job Search HQ -- You've got this! Track everything and stay persistent.", "🔍"),
             divider(),
             heading3("Setup Instructions"),
             numbered("Research and add target companies"),
             numbered("Track every application immediately after applying"),
             numbered("Log all networking contacts with follow-up dates"),
             numbered("Use Interview Prep section before each interview"),
             numbered("Update the Pipeline Board daily"),
             numbered("Review weekly stats every Sunday to adjust strategy")],
            # 9: Book & Learning Tracker
            [heading2("Dashboard"),
             callout("Track your reading journey and never forget what you learn!", "📖"),
             paragraph("2026 Reading Challenge: 7/24 books (29%)"),
             divider(),
             heading3("Setup Instructions"),
             numbered("Set your annual reading goal in Reading Challenge"),
             numbered("Add books you're currently reading"),
             numbered("Import your to-read and wishlist books"),
             numbered("Take notes as you read (highlights, key concepts)"),
             numbered("Log daily reading sessions"),
             numbered("Add courses you're taking or want to take"),
             numbered("Review your notes periodically to retain knowledge")],
            # 10: Digital Products Business OS
            [heading2("Dashboard"),
             callout("Digital Products HQ -- Build, launch, sell, iterate.", "🛍️"),
             divider(),
             heading3("Setup Instructions"),
             numbered("Add your current and planned products"),
             numbered("Connect your sales platforms (manual entry or integrate)"),
             numbered("Plan marketing campaigns for each product"),
             numbered("Collect and organize customer feedback"),
             numbered("Use the Roadmap to plan improvements"),
             numbered("Review sales and feedback weekly")],
        ]

        for tpl in template_links:
            idx = tpl["index"] - 1
            if args.only and tpl["index"] != args.only:
                continue
            if idx < 0 or idx >= len(dashboard_blocks):
                continue
            pid = tpl["id"]
            title = tpl["title"]
            try:
                log.info(f"Appending dashboard blocks to: {title} ({pid})")
                append_blocks(pid, dashboard_blocks[idx])
                log.info(f"  OK: {title}")
            except Exception as e:
                log.error(f"  FAILED: {title} -> {e}")

        print("\nDashboard-only mode complete.")
        return

    # Determine parent
    if args.parent_page_id:
        parent = {"type": "page_id", "page_id": args.parent_page_id}
        log.info(f"Creating templates under page: {args.parent_page_id}")
    else:
        # Create a master parent page at workspace level
        # For workspace-level pages, we need a page_id; create under first available page
        log.info("Creating master container page...")
        master = _api("post", "/pages", {
            "parent": {"type": "page_id", "page_id": args.parent_page_id} if args.parent_page_id else {"type": "workspace", "workspace": True},
            "properties": {"title": {"title": rich("Gumroad Notion Templates")}},
            "icon": {"type": "emoji", "emoji": "🎁"},
        })
        parent = {"type": "page_id", "page_id": master["id"]}
        log.info(f"Master page created: {master['id']}")
        log.info(f"URL: {master.get('url', 'N/A')}")

    # Build templates
    results = []
    builders = TEMPLATE_BUILDERS
    if args.only:
        idx = args.only - 1
        if 0 <= idx < len(builders):
            builders = [builders[idx]]
        else:
            print(f"ERROR: --only must be 1-10, got {args.only}")
            sys.exit(1)

    for name, builder in builders:
        try:
            log.info(f"\n{'='*60}")
            log.info(f"Building: {name}")
            log.info(f"{'='*60}")
            page = builder(parent)
            results.append((name, page["id"], page.get("url", "N/A")))
            log.info(f"Done: {name}\n")
        except Exception as e:
            log.error(f"FAILED: {name} -> {e}")
            results.append((name, "FAILED", str(e)))

    # Summary
    print("\n" + "=" * 70)
    print("TEMPLATE CREATION SUMMARY")
    print("=" * 70)
    for name, page_id, url in results:
        status = "FAILED" if page_id == "FAILED" else "OK"
        print(f"  [{status}] {name}")
        if page_id != "FAILED":
            print(f"         ID:  {page_id}")
            print(f"         URL: {url}")
        else:
            print(f"         Error: {url}")
    print("=" * 70)

    if args.parent_page_id:
        print(f"\nParent page ID: {args.parent_page_id}")
    else:
        print(f"\nMaster page ID: {results[0][1] if results else 'N/A'}")
    print(f"Total templates: {len([r for r in results if r[1] != 'FAILED'])}/{len(builders)}")
    print("\nNext step: Run share_templates.py to get share links.")


if __name__ == "__main__":
    main()
