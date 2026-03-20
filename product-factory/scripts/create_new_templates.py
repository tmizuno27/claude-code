"""
Notion Template Builder — Creates 8 new Gumroad Notion templates via Notion API.

Products:
  1. Startup Launch Checklist ($12) — 6 DB
  2. Wedding Planning Hub ($17) — 7 DB
  3. Property Investment Tracker ($19) — 8 DB
  4. Travel Planner & Journal ($12) — 8 DB
  5. Habit Tracker & Goal System ($9) — 7 DB
  6. Personal Finance Dashboard ($14) — 8 DB
  7. Airbnb Host Management Hub ($17) — 7 DB
  8. AI Side Hustle Starter Kit ($19) — 7 DB

Usage:
    set NOTION_TOKEN=secret_xxx
    python create_new_templates.py --parent-page-id PAGE_ID [--template "startup"]
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
# TEMPLATE 1: Startup Launch Checklist ($12) — 6 DB
# ============================================================================

def build_startup_launch_checklist(parent: dict) -> dict:
    log.info("=== Startup Launch Checklist ===")
    page = create_page(parent, "Startup Launch Checklist", "🚀", [
        heading1("Startup Launch Checklist"),
        paragraph("From Idea to Launch Day — your complete startup launch roadmap."),
        callout("Delete sample data, customize phases and tasks, and track your launch!", "🚀"),
        divider(),
    ])
    pid = page["id"]

    # --- DB1: Tasks ---
    tasks_db = create_database(pid, "Tasks", "📋", {
        "Task Name": p_title(),
        "Phase": p_select("Idea Validation", "MVP Build", "Pre-Launch", "Launch Day"),
        "Category": p_select("Legal", "Finance", "Marketing", "Product", "Operations"),
        "Status": p_select("Not Started", "In Progress", "Completed", "Blocked"),
        "Priority": p_select("High", "Medium", "Low"),
        "Due Date": p_date(),
        "Notes": p_rt(),
        "Completed": p_checkbox(),
    })
    tasks_id = tasks_db["id"]

    # --- DB2: Milestones ---
    milestones_db = create_database(pid, "Milestones", "🏁", {
        "Milestone Name": p_title(),
        "Phase": p_select("Idea Validation", "MVP Build", "Pre-Launch", "Launch Day"),
        "Target Date": p_date(),
        "Status": p_select("Upcoming", "In Progress", "Completed"),
    })
    milestones_id = milestones_db["id"]

    # Add relations: Tasks <-> Milestones
    _api("patch", f"/databases/{tasks_id}", {"properties": {
        "Milestone": p_relation(milestones_id),
    }})

    # --- DB3: Budget ---
    budget_db = create_database(pid, "Budget", "💰", {
        "Item": p_title(),
        "Category": p_select("Legal", "Software", "Marketing", "Operations", "Other"),
        "Type": p_select("One-time", "Monthly", "Annual"),
        "Amount": p_number("dollar"),
        "Paid": p_checkbox(),
        "Due Date": p_date(),
        "Notes": p_rt(),
    })
    budget_id = budget_db["id"]

    # --- DB4: Resources ---
    resources_db = create_database(pid, "Resources", "📚", {
        "Resource Name": p_title(),
        "Type": p_select("Article", "Tool", "Video", "Template", "Book"),
        "URL": p_url(),
        "Category": p_select("Legal", "Finance", "Marketing", "Product", "Operations"),
        "Rating": p_select("⭐", "⭐⭐", "⭐⭐⭐"),
        "Notes": p_rt(),
    })
    resources_id = resources_db["id"]

    # Add relation: Tasks <-> Resources
    _api("patch", f"/databases/{tasks_id}", {"properties": {
        "Resources": p_relation(resources_id),
    }})

    # --- DB5: Competitors ---
    competitors_db = create_database(pid, "Competitors", "🔍", {
        "Company Name": p_title(),
        "Website": p_url(),
        "Pricing": p_rt(),
        "Key Features": p_mselect("Free Tier", "API", "Mobile App", "Analytics", "Integrations", "AI Features"),
        "Strengths": p_rt(),
        "Weaknesses": p_rt(),
        "Our Differentiator": p_rt(),
    })
    competitors_id = competitors_db["id"]

    # --- DB6: Launch Day Playbook ---
    playbook_db = create_database(pid, "Launch Day Playbook", "🎯", {
        "Action": p_title(),
        "Time": p_rt(),
        "Channel": p_select("Twitter", "Email", "Reddit", "Product Hunt", "LinkedIn", "Other"),
        "Content": p_rt(),
        "Status": p_select("Prepared", "Posted", "Skipped"),
        "Link": p_url(),
    })
    playbook_id = playbook_db["id"]

    # --- Sample Data: Milestones ---
    m1 = add_row(milestones_id, {
        "Milestone Name": title_prop("Idea Validated"),
        "Phase": select_prop("Idea Validation"),
        "Target Date": date_prop(_d(14)),
        "Status": select_prop("Completed"),
    })
    m2 = add_row(milestones_id, {
        "Milestone Name": title_prop("MVP Ready"),
        "Phase": select_prop("MVP Build"),
        "Target Date": date_prop(_d(42)),
        "Status": select_prop("In Progress"),
    })
    m3 = add_row(milestones_id, {
        "Milestone Name": title_prop("Pre-Launch Complete"),
        "Phase": select_prop("Pre-Launch"),
        "Target Date": date_prop(_d(56)),
        "Status": select_prop("Upcoming"),
    })
    m4 = add_row(milestones_id, {
        "Milestone Name": title_prop("Launch Day"),
        "Phase": select_prop("Launch Day"),
        "Target Date": date_prop(_d(70)),
        "Status": select_prop("Upcoming"),
    })

    # --- Sample Data: Tasks ---
    add_row(tasks_id, {
        "Task Name": title_prop("Register business entity"),
        "Phase": select_prop("Idea Validation"),
        "Category": select_prop("Legal"),
        "Status": select_prop("Completed"),
        "Priority": select_prop("High"),
        "Due Date": date_prop(_d(-5)),
        "Completed": checkbox_prop(True),
        "Milestone": relation_prop(m1["id"]),
    })
    add_row(tasks_id, {
        "Task Name": title_prop("Build landing page"),
        "Phase": select_prop("MVP Build"),
        "Category": select_prop("Marketing"),
        "Status": select_prop("In Progress"),
        "Priority": select_prop("High"),
        "Due Date": date_prop(_d(14)),
        "Completed": checkbox_prop(False),
        "Milestone": relation_prop(m2["id"]),
    })
    add_row(tasks_id, {
        "Task Name": title_prop("Set up Stripe payments"),
        "Phase": select_prop("MVP Build"),
        "Category": select_prop("Product"),
        "Status": select_prop("Not Started"),
        "Priority": select_prop("Medium"),
        "Due Date": date_prop(_d(28)),
        "Completed": checkbox_prop(False),
        "Milestone": relation_prop(m2["id"]),
    })
    add_row(tasks_id, {
        "Task Name": title_prop("Create social media accounts"),
        "Phase": select_prop("Pre-Launch"),
        "Category": select_prop("Marketing"),
        "Status": select_prop("Not Started"),
        "Priority": select_prop("Low"),
        "Due Date": date_prop(_d(42)),
        "Completed": checkbox_prop(False),
        "Milestone": relation_prop(m3["id"]),
    })
    add_row(tasks_id, {
        "Task Name": title_prop("Write launch email sequence"),
        "Phase": select_prop("Pre-Launch"),
        "Category": select_prop("Marketing"),
        "Status": select_prop("Not Started"),
        "Priority": select_prop("Medium"),
        "Due Date": date_prop(_d(50)),
        "Completed": checkbox_prop(False),
        "Milestone": relation_prop(m3["id"]),
    })

    # --- Sample Data: Budget ---
    add_row(budget_id, {
        "Item": title_prop("Domain name"),
        "Category": select_prop("Software"),
        "Type": select_prop("One-time"),
        "Amount": num_prop(12),
        "Paid": checkbox_prop(True),
    })
    add_row(budget_id, {
        "Item": title_prop("Hosting (Vercel)"),
        "Category": select_prop("Software"),
        "Type": select_prop("Monthly"),
        "Amount": num_prop(0),
        "Paid": checkbox_prop(True),
    })
    add_row(budget_id, {
        "Item": title_prop("LLC registration"),
        "Category": select_prop("Legal"),
        "Type": select_prop("One-time"),
        "Amount": num_prop(200),
        "Paid": checkbox_prop(True),
    })
    add_row(budget_id, {
        "Item": title_prop("Google Ads test"),
        "Category": select_prop("Marketing"),
        "Type": select_prop("One-time"),
        "Amount": num_prop(100),
        "Paid": checkbox_prop(False),
    })

    # --- Dashboard ---
    append_blocks(pid, [
        heading2("Phase Progress"),
        callout("Idea Validation: Completed | MVP Build: In Progress | Pre-Launch: Upcoming | Launch Day: Upcoming", "📊"),
        divider(),
        heading2("Quick Links"),
        bulleted("Tasks — Track every action item by phase"),
        bulleted("Milestones — Timeline of key deliverables"),
        bulleted("Budget — Track spending by category"),
        bulleted("Resources — Curated tools and references"),
        bulleted("Competitors — Know your market"),
        bulleted("Launch Day Playbook — Hour-by-hour launch plan"),
    ])

    log.info("=== Startup Launch Checklist DONE ===")
    return page


# ============================================================================
# TEMPLATE 2: Wedding Planning Hub ($17) — 7 DB
# ============================================================================

def build_wedding_planning_hub(parent: dict) -> dict:
    log.info("=== Wedding Planning Hub ===")
    page = create_page(parent, "Wedding Planning Hub", "💒", [
        heading1("Wedding Planning Hub"),
        paragraph("[Partner A] & [Partner B] — Wedding Date: [Date]"),
        callout("Your complete wedding command center. Customize names, dates, and start planning!", "💍"),
        divider(),
    ])
    pid = page["id"]

    # --- DB1: Guests ---
    guests_db = create_database(pid, "Guests", "👥", {
        "Guest Name": p_title(),
        "Side": p_select("Bride", "Groom", "Mutual"),
        "Group": p_select("Family", "Friends", "Work", "Partner's Family", "Partner's Friends"),
        "RSVP Status": p_select("Pending", "Confirmed", "Declined", "No Response"),
        "Plus One": p_checkbox(),
        "Plus One Name": p_rt(),
        "Meal Preference": p_select("Standard", "Vegetarian", "Vegan", "Gluten-Free", "Halal", "Kosher", "Other"),
        "Dietary Notes": p_rt(),
        "Email": p_email(),
        "Phone": p_phone(),
        "Address": p_rt(),
        "Invite Sent": p_checkbox(),
        "Thank You Sent": p_checkbox(),
        "Notes": p_rt(),
    })
    guests_id = guests_db["id"]

    # --- DB5: Seating ---
    seating_db = create_database(pid, "Seating", "🪑", {
        "Table Name": p_title(),
        "Capacity": p_number(),
        "Location": p_select("Front", "Middle", "Back", "Outdoor", "Bar Area"),
        "Notes": p_rt(),
    })
    seating_id = seating_db["id"]

    # Add relation: Guests <-> Seating
    _api("patch", f"/databases/{guests_id}", {"properties": {
        "Table": p_relation(seating_id),
    }})
    # Add rollup: Seating Guest Count
    _api("patch", f"/databases/{seating_id}", {"properties": {
        "Guests": p_relation(guests_id),
    }})

    # --- DB3: Vendors ---
    vendors_db = create_database(pid, "Vendors", "🏪", {
        "Vendor Name": p_title(),
        "Category": p_select("Venue", "Catering", "Photography", "Videography", "Florist", "DJ-Band", "Officiant", "Baker", "Hair-Makeup", "Planner", "Rentals", "Other"),
        "Status": p_select("Researching", "Contacted", "Quote Received", "Booked", "Rejected"),
        "Quote": p_number("dollar"),
        "Rating": p_select("★", "★★", "★★★", "★★★★", "★★★★★"),
        "Availability": p_select("Available", "Unavailable", "TBD"),
        "Website": p_url(),
        "Contact Name": p_rt(),
        "Phone": p_phone(),
        "Email": p_email(),
        "Pros": p_rt(),
        "Cons": p_rt(),
        "Notes": p_rt(),
    })
    vendors_id = vendors_db["id"]

    # --- DB2: Budget ---
    budget_db = create_database(pid, "Budget", "💰", {
        "Item": p_title(),
        "Category": p_select("Venue", "Catering", "Photography", "Videography", "Flowers", "Music", "Attire", "Beauty", "Stationery", "Transportation", "Decorations", "Favors", "Rings", "Honeymoon", "Other"),
        "Estimated Cost": p_number("dollar"),
        "Actual Cost": p_number("dollar"),
        "Paid": p_checkbox(),
        "Deposit Paid": p_checkbox(),
        "Due Date": p_date(),
        "Notes": p_rt(),
    })
    budget_id = budget_db["id"]

    # Add relation: Budget <-> Vendors
    _api("patch", f"/databases/{budget_id}", {"properties": {
        "Vendor": p_relation(vendors_id),
    }})

    # --- DB4: Timeline ---
    timeline_db = create_database(pid, "Timeline", "📅", {
        "Task": p_title(),
        "Phase": p_select("12+ Months", "9-11 Months", "6-8 Months", "4-5 Months", "2-3 Months", "1 Month", "2 Weeks", "1 Week", "Day Before", "Wedding Day", "After Wedding"),
        "Category": p_select("Venue", "Catering", "Attire", "Beauty", "Stationery", "Legal", "Music", "Photography", "Decor", "Transportation", "Other"),
        "Status": p_select("Not Started", "In Progress", "Completed", "Skipped"),
        "Priority": p_select("High", "Medium", "Low"),
        "Due Date": p_date(),
        "Notes": p_rt(),
        "Completed": p_checkbox(),
    })
    timeline_id = timeline_db["id"]

    # Add relation: Timeline <-> Vendors
    _api("patch", f"/databases/{timeline_id}", {"properties": {
        "Vendor": p_relation(vendors_id),
    }})

    # --- DB6: Registry ---
    registry_db = create_database(pid, "Registry", "🎁", {
        "Item": p_title(),
        "Registry": p_select("Amazon", "Target", "Zola", "Crate & Barrel", "Custom", "Other"),
        "Price": p_number("dollar"),
        "Status": p_select("Listed", "Purchased", "Received"),
        "Purchased By": p_rt(),
        "Thank You Sent": p_checkbox(),
        "URL": p_url(),
        "Notes": p_rt(),
    })
    registry_id = registry_db["id"]

    # --- DB7: Inspiration ---
    inspiration_db = create_database(pid, "Inspiration", "✨", {
        "Title": p_title(),
        "Category": p_select("Venue", "Flowers", "Dress", "Cake", "Decor", "Color Palette", "Hair", "Table Setting", "Invitation", "Other"),
        "Image URL": p_url(),
        "Source": p_url(),
        "Notes": p_rt(),
        "Favorite": p_checkbox(),
    })
    inspiration_id = inspiration_db["id"]

    # --- Sample Data: Seating ---
    s_head = add_row(seating_id, {
        "Table Name": title_prop("Head Table"),
        "Capacity": num_prop(8),
        "Location": select_prop("Front"),
    })
    s_t1 = add_row(seating_id, {
        "Table Name": title_prop("Table 1"),
        "Capacity": num_prop(10),
        "Location": select_prop("Front"),
    })
    s_t3 = add_row(seating_id, {
        "Table Name": title_prop("Table 3"),
        "Capacity": num_prop(10),
        "Location": select_prop("Middle"),
    })

    # --- Sample Data: Guests ---
    add_row(guests_id, {
        "Guest Name": title_prop("Sarah Johnson"),
        "Side": select_prop("Bride"),
        "Group": select_prop("Family"),
        "RSVP Status": select_prop("Confirmed"),
        "Meal Preference": select_prop("Standard"),
        "Plus One": checkbox_prop(False),
        "Invite Sent": checkbox_prop(True),
        "Table": relation_prop(s_head["id"]),
    })
    add_row(guests_id, {
        "Guest Name": title_prop("Mike & Lisa Chen"),
        "Side": select_prop("Groom"),
        "Group": select_prop("Friends"),
        "RSVP Status": select_prop("Confirmed"),
        "Meal Preference": select_prop("Vegetarian"),
        "Plus One": checkbox_prop(True),
        "Plus One Name": rt_prop("Lisa Chen"),
        "Invite Sent": checkbox_prop(True),
        "Table": relation_prop(s_t3["id"]),
    })
    add_row(guests_id, {
        "Guest Name": title_prop("David Williams"),
        "Side": select_prop("Bride"),
        "Group": select_prop("Work"),
        "RSVP Status": select_prop("Pending"),
        "Plus One": checkbox_prop(False),
        "Invite Sent": checkbox_prop(True),
    })
    add_row(guests_id, {
        "Guest Name": title_prop("Grandma Rose"),
        "Side": select_prop("Bride"),
        "Group": select_prop("Family"),
        "RSVP Status": select_prop("Confirmed"),
        "Meal Preference": select_prop("Gluten-Free"),
        "Plus One": checkbox_prop(False),
        "Invite Sent": checkbox_prop(True),
        "Table": relation_prop(s_t1["id"]),
    })
    add_row(guests_id, {
        "Guest Name": title_prop("Tom & Amy Park"),
        "Side": select_prop("Mutual"),
        "Group": select_prop("Friends"),
        "RSVP Status": select_prop("No Response"),
        "Plus One": checkbox_prop(True),
        "Plus One Name": rt_prop("Amy Park"),
        "Invite Sent": checkbox_prop(True),
    })

    # --- Sample Data: Vendors ---
    add_row(vendors_id, {
        "Vendor Name": title_prop("Rosewood Garden Estate"),
        "Category": select_prop("Venue"),
        "Status": select_prop("Booked"),
        "Quote": num_prop(4800),
        "Rating": select_prop("★★★★★"),
        "Availability": select_prop("Available"),
    })
    add_row(vendors_id, {
        "Vendor Name": title_prop("Capture Moments Photography"),
        "Category": select_prop("Photography"),
        "Status": select_prop("Booked"),
        "Quote": num_prop(2800),
        "Rating": select_prop("★★★★"),
    })
    add_row(vendors_id, {
        "Vendor Name": title_prop("Fresh Blooms Floristry"),
        "Category": select_prop("Florist"),
        "Status": select_prop("Quote Received"),
        "Quote": num_prop(1200),
        "Rating": select_prop("★★★★"),
    })
    add_row(vendors_id, {
        "Vendor Name": title_prop("DJ Smooth"),
        "Category": select_prop("DJ-Band"),
        "Status": select_prop("Researching"),
        "Quote": num_prop(800),
        "Rating": select_prop("★★★"),
    })

    # --- Sample Data: Budget ---
    add_row(budget_id, {
        "Item": title_prop("Venue rental"),
        "Category": select_prop("Venue"),
        "Estimated Cost": num_prop(5000),
        "Actual Cost": num_prop(4800),
        "Paid": checkbox_prop(True),
    })
    add_row(budget_id, {
        "Item": title_prop("Photographer"),
        "Category": select_prop("Photography"),
        "Estimated Cost": num_prop(3000),
        "Actual Cost": num_prop(2800),
        "Deposit Paid": checkbox_prop(True),
        "Paid": checkbox_prop(False),
    })
    add_row(budget_id, {
        "Item": title_prop("Catering (per head)"),
        "Category": select_prop("Catering"),
        "Estimated Cost": num_prop(8000),
        "Actual Cost": num_prop(0),
        "Paid": checkbox_prop(False),
    })
    add_row(budget_id, {
        "Item": title_prop("Wedding dress"),
        "Category": select_prop("Attire"),
        "Estimated Cost": num_prop(2000),
        "Actual Cost": num_prop(1850),
        "Paid": checkbox_prop(True),
    })
    add_row(budget_id, {
        "Item": title_prop("DJ / Band"),
        "Category": select_prop("Music"),
        "Estimated Cost": num_prop(1500),
        "Actual Cost": num_prop(0),
        "Paid": checkbox_prop(False),
        "Deposit Paid": checkbox_prop(False),
    })

    # --- Sample Data: Timeline ---
    add_row(timeline_id, {
        "Task": title_prop("Book venue"),
        "Phase": select_prop("12+ Months"),
        "Category": select_prop("Venue"),
        "Status": select_prop("Completed"),
        "Priority": select_prop("High"),
        "Completed": checkbox_prop(True),
    })
    add_row(timeline_id, {
        "Task": title_prop("Send save-the-dates"),
        "Phase": select_prop("6-8 Months"),
        "Category": select_prop("Stationery"),
        "Status": select_prop("Completed"),
        "Priority": select_prop("High"),
        "Completed": checkbox_prop(True),
    })
    add_row(timeline_id, {
        "Task": title_prop("Final dress fitting"),
        "Phase": select_prop("1 Month"),
        "Category": select_prop("Attire"),
        "Status": select_prop("Not Started"),
        "Priority": select_prop("High"),
        "Due Date": date_prop(_d(30)),
    })
    add_row(timeline_id, {
        "Task": title_prop("Confirm final headcount with caterer"),
        "Phase": select_prop("2 Weeks"),
        "Category": select_prop("Catering"),
        "Status": select_prop("Not Started"),
        "Priority": select_prop("High"),
        "Due Date": date_prop(_d(45)),
    })
    add_row(timeline_id, {
        "Task": title_prop("Send invitations"),
        "Phase": select_prop("4-5 Months"),
        "Category": select_prop("Stationery"),
        "Status": select_prop("In Progress"),
        "Priority": select_prop("High"),
    })

    # --- Dashboard ---
    append_blocks(pid, [
        heading2("RSVP Summary"),
        callout("Confirmed: 3 | Pending: 1 | No Response: 1 | Total Invited: 5", "📨"),
        divider(),
        heading2("Quick Links"),
        bulleted("Guests — RSVP tracking and meal preferences"),
        bulleted("Budget — Estimated vs actual spending"),
        bulleted("Vendors — Compare and book vendors"),
        bulleted("Timeline — Countdown checklist by phase"),
        bulleted("Seating — Table assignments"),
        bulleted("Registry — Gift tracking"),
        bulleted("Inspiration — Collect ideas and mood boards"),
    ])

    log.info("=== Wedding Planning Hub DONE ===")
    return page


# ============================================================================
# TEMPLATE 3: Property Investment Tracker ($19) — 8 DB
# ============================================================================

def build_property_investment_tracker(parent: dict) -> dict:
    log.info("=== Property Investment Tracker ===")
    page = create_page(parent, "Property Investment Tracker", "🏠", [
        heading1("Property Investment Tracker"),
        paragraph("Your Real Estate Command Center — track properties, tenants, mortgages, and ROI."),
        callout("Replace sample data with your portfolio and start tracking cash flow!", "📊"),
        divider(),
    ])
    pid = page["id"]

    # --- DB1: Properties ---
    properties_db = create_database(pid, "Properties", "🏘️", {
        "Property Name": p_title(),
        "Type": p_select("Single Family", "Multi-Family", "Condo", "Apartment", "Commercial", "Short-Term Rental"),
        "Status": p_select("Active", "Vacant", "Under Renovation", "For Sale", "Sold"),
        "Purchase Price": p_number("dollar"),
        "Current Value": p_number("dollar"),
        "Purchase Date": p_date(),
        "Units": p_number(),
        "Square Footage": p_number(),
        "Address": p_rt(),
        "Photo": p_files(),
        "Notes": p_rt(),
    })
    properties_id = properties_db["id"]

    # --- DB2: Transactions ---
    transactions_db = create_database(pid, "Transactions", "💵", {
        "Description": p_title(),
        "Type": p_select("Income", "Expense"),
        "Category": p_select("Rent", "Airbnb Booking", "Security Deposit", "Mortgage Payment", "Insurance", "Property Tax", "Repairs", "Maintenance", "HOA", "Utilities", "Management Fee", "Legal", "Other"),
        "Amount": p_number("dollar"),
        "Date": p_date(),
        "Tax Deductible": p_checkbox(),
        "Tax Category": p_select("Repairs & Maintenance", "Depreciation", "Insurance", "Management", "Taxes", "Utilities", "Interest", "Other"),
        "Receipt": p_files(),
        "Notes": p_rt(),
    })
    transactions_id = transactions_db["id"]

    # --- DB3: Mortgages ---
    mortgages_db = create_database(pid, "Mortgages", "🏦", {
        "Loan Name": p_title(),
        "Lender": p_rt(),
        "Original Amount": p_number("dollar"),
        "Remaining Balance": p_number("dollar"),
        "Interest Rate": p_number("percent"),
        "Term (Years)": p_number(),
        "Start Date": p_date(),
        "Maturity Date": p_date(),
        "Status": p_select("Active", "Paid Off", "Refinanced"),
        "Notes": p_rt(),
    })
    mortgages_id = mortgages_db["id"]

    # --- DB4: Tenants ---
    tenants_db = create_database(pid, "Tenants", "🧑‍🤝‍🧑", {
        "Tenant Name": p_title(),
        "Unit": p_rt(),
        "Email": p_email(),
        "Phone": p_phone(),
        "Lease Start": p_date(),
        "Lease End": p_date(),
        "Monthly Rent": p_number("dollar"),
        "Security Deposit": p_number("dollar"),
        "Status": p_select("Active", "Notice Given", "Moved Out", "Evicted"),
        "Lease Document": p_files(),
        "Notes": p_rt(),
    })
    tenants_id = tenants_db["id"]

    # --- DB5: Maintenance ---
    maintenance_db = create_database(pid, "Maintenance", "🔧", {
        "Request Title": p_title(),
        "Priority": p_select("Emergency", "High", "Medium", "Low"),
        "Status": p_select("Reported", "In Progress", "Waiting for Parts", "Completed"),
        "Reported Date": p_date(),
        "Completed Date": p_date(),
        "Cost": p_number("dollar"),
        "Contractor": p_rt(),
        "Photos": p_files(),
        "Notes": p_rt(),
    })
    maintenance_id = maintenance_db["id"]

    # --- DB6: Documents ---
    documents_db = create_database(pid, "Documents", "📄", {
        "Document Name": p_title(),
        "Type": p_select("Lease", "Insurance Policy", "Inspection Report", "Closing Docs", "Tax Return", "Appraisal", "Other"),
        "File": p_files(),
        "Expiry Date": p_date(),
        "Notes": p_rt(),
    })
    documents_id = documents_db["id"]

    # --- DB7: Vacancies ---
    vacancies_db = create_database(pid, "Vacancies", "🏚️", {
        "Unit": p_title(),
        "Vacant Since": p_date(),
        "Expected Rent": p_number("dollar"),
        "Status": p_select("Listed", "Showing", "Application Received", "Leased"),
        "Listing URL": p_url(),
        "Notes": p_rt(),
    })
    vacancies_id = vacancies_db["id"]

    # --- DB8: Portfolio KPIs ---
    kpis_db = create_database(pid, "Portfolio KPIs", "📈", {
        "Metric Name": p_title(),
        "Period": p_select("Monthly", "Quarterly", "Annual"),
        "Date": p_date(),
        "Total Income": p_number("dollar"),
        "Total Expenses": p_number("dollar"),
        "Notes": p_rt(),
    })
    kpis_id = kpis_db["id"]

    # --- Relations ---
    _api("patch", f"/databases/{properties_id}", {"properties": {
        "Mortgages": p_relation(mortgages_id),
        "Tenants": p_relation(tenants_id),
        "Transactions": p_relation(transactions_id),
        "Maintenance": p_relation(maintenance_id),
        "Documents": p_relation(documents_id),
        "Vacancies": p_relation(vacancies_id),
    }})
    _api("patch", f"/databases/{transactions_id}", {"properties": {
        "Property": p_relation(properties_id),
        "Tenant": p_relation(tenants_id),
    }})
    _api("patch", f"/databases/{mortgages_id}", {"properties": {
        "Property": p_relation(properties_id),
    }})
    _api("patch", f"/databases/{tenants_id}", {"properties": {
        "Property": p_relation(properties_id),
        "Maintenance Requests": p_relation(maintenance_id),
    }})
    _api("patch", f"/databases/{maintenance_id}", {"properties": {
        "Property": p_relation(properties_id),
        "Tenant": p_relation(tenants_id),
        "Expense": p_relation(transactions_id),
    }})
    _api("patch", f"/databases/{documents_id}", {"properties": {
        "Property": p_relation(properties_id),
    }})
    _api("patch", f"/databases/{vacancies_id}", {"properties": {
        "Property": p_relation(properties_id),
    }})
    _api("patch", f"/databases/{kpis_id}", {"properties": {
        "Property": p_relation(properties_id),
    }})

    # --- Sample Data: Properties ---
    prop1 = add_row(properties_id, {
        "Property Name": title_prop("123 Oak Street"),
        "Type": select_prop("Single Family"),
        "Status": select_prop("Active"),
        "Purchase Price": num_prop(280000),
        "Current Value": num_prop(320000),
        "Purchase Date": date_prop("2023-06-15"),
        "Units": num_prop(1),
    })
    prop2 = add_row(properties_id, {
        "Property Name": title_prop("456 Maple Avenue, Unit A-D"),
        "Type": select_prop("Multi-Family"),
        "Status": select_prop("Active"),
        "Purchase Price": num_prop(520000),
        "Current Value": num_prop(610000),
        "Purchase Date": date_prop("2022-03-01"),
        "Units": num_prop(4),
    })
    prop3 = add_row(properties_id, {
        "Property Name": title_prop("789 Beach Blvd #12"),
        "Type": select_prop("Condo"),
        "Status": select_prop("Active"),
        "Purchase Price": num_prop(180000),
        "Current Value": num_prop(195000),
        "Purchase Date": date_prop("2024-01-10"),
        "Units": num_prop(1),
    })
    prop4 = add_row(properties_id, {
        "Property Name": title_prop("Sunset Cottage"),
        "Type": select_prop("Short-Term Rental"),
        "Status": select_prop("Active"),
        "Purchase Price": num_prop(150000),
        "Current Value": num_prop(175000),
        "Units": num_prop(1),
    })
    prop5 = add_row(properties_id, {
        "Property Name": title_prop("1010 Industrial Way"),
        "Type": select_prop("Commercial"),
        "Status": select_prop("Under Renovation"),
        "Purchase Price": num_prop(400000),
        "Current Value": num_prop(400000),
        "Units": num_prop(2),
    })

    # --- Sample Data: Tenants ---
    t1 = add_row(tenants_id, {
        "Tenant Name": title_prop("John Smith"),
        "Property": relation_prop(prop1["id"]),
        "Lease Start": date_prop("2025-06-01"),
        "Lease End": date_prop("2026-05-31"),
        "Monthly Rent": num_prop(1800),
        "Status": select_prop("Active"),
    })
    t2 = add_row(tenants_id, {
        "Tenant Name": title_prop("Maria Garcia"),
        "Property": relation_prop(prop2["id"]),
        "Unit": rt_prop("Unit A"),
        "Lease Start": date_prop("2025-09-01"),
        "Lease End": date_prop("2026-08-31"),
        "Monthly Rent": num_prop(1200),
        "Status": select_prop("Active"),
    })
    t3 = add_row(tenants_id, {
        "Tenant Name": title_prop("David Chen"),
        "Property": relation_prop(prop3["id"]),
        "Lease Start": date_prop("2025-12-01"),
        "Lease End": date_prop("2026-11-30"),
        "Monthly Rent": num_prop(1500),
        "Status": select_prop("Active"),
    })

    # --- Sample Data: Transactions ---
    add_row(transactions_id, {
        "Description": title_prop("March Rent - 123 Oak"),
        "Property": relation_prop(prop1["id"]),
        "Type": select_prop("Income"),
        "Category": select_prop("Rent"),
        "Amount": num_prop(1800),
        "Date": date_prop("2026-03-01"),
    })
    add_row(transactions_id, {
        "Description": title_prop("March Rent - 456 Maple A"),
        "Property": relation_prop(prop2["id"]),
        "Type": select_prop("Income"),
        "Category": select_prop("Rent"),
        "Amount": num_prop(1200),
        "Date": date_prop("2026-03-01"),
    })
    add_row(transactions_id, {
        "Description": title_prop("Plumbing repair - 123 Oak"),
        "Property": relation_prop(prop1["id"]),
        "Type": select_prop("Expense"),
        "Category": select_prop("Repairs"),
        "Amount": num_prop(450),
        "Date": date_prop("2026-03-05"),
        "Tax Deductible": checkbox_prop(True),
        "Tax Category": select_prop("Repairs & Maintenance"),
    })
    add_row(transactions_id, {
        "Description": title_prop("Property Insurance - 789 Beach"),
        "Property": relation_prop(prop3["id"]),
        "Type": select_prop("Expense"),
        "Category": select_prop("Insurance"),
        "Amount": num_prop(120),
        "Date": date_prop("2026-03-10"),
        "Tax Deductible": checkbox_prop(True),
        "Tax Category": select_prop("Insurance"),
    })
    add_row(transactions_id, {
        "Description": title_prop("Mortgage - 123 Oak"),
        "Property": relation_prop(prop1["id"]),
        "Type": select_prop("Expense"),
        "Category": select_prop("Mortgage Payment"),
        "Amount": num_prop(1350),
        "Date": date_prop("2026-03-01"),
    })
    add_row(transactions_id, {
        "Description": title_prop("Airbnb Booking #4821"),
        "Property": relation_prop(prop4["id"]),
        "Type": select_prop("Income"),
        "Category": select_prop("Airbnb Booking"),
        "Amount": num_prop(280),
        "Date": date_prop("2026-03-08"),
    })

    # --- Sample Data: Mortgages ---
    add_row(mortgages_id, {
        "Loan Name": title_prop("123 Oak St - Primary"),
        "Property": relation_prop(prop1["id"]),
        "Lender": rt_prop("First National Bank"),
        "Original Amount": num_prop(224000),
        "Remaining Balance": num_prop(198000),
        "Interest Rate": num_prop(4.5),
        "Term (Years)": num_prop(30),
        "Status": select_prop("Active"),
    })
    add_row(mortgages_id, {
        "Loan Name": title_prop("456 Maple - Primary"),
        "Property": relation_prop(prop2["id"]),
        "Lender": rt_prop("Wells Fargo"),
        "Original Amount": num_prop(416000),
        "Remaining Balance": num_prop(389000),
        "Interest Rate": num_prop(5.2),
        "Term (Years)": num_prop(30),
        "Status": select_prop("Active"),
    })
    add_row(mortgages_id, {
        "Loan Name": title_prop("789 Beach - Primary"),
        "Property": relation_prop(prop3["id"]),
        "Lender": rt_prop("Chase"),
        "Original Amount": num_prop(144000),
        "Remaining Balance": num_prop(131000),
        "Interest Rate": num_prop(3.8),
        "Term (Years)": num_prop(15),
        "Status": select_prop("Active"),
    })

    # --- Sample Data: Maintenance ---
    add_row(maintenance_id, {
        "Request Title": title_prop("Leaking faucet - kitchen"),
        "Property": relation_prop(prop1["id"]),
        "Tenant": relation_prop(t1["id"]),
        "Priority": select_prop("Medium"),
        "Status": select_prop("Completed"),
        "Reported Date": date_prop("2026-02-20"),
        "Completed Date": date_prop("2026-02-25"),
        "Cost": num_prop(450),
    })
    add_row(maintenance_id, {
        "Request Title": title_prop("HVAC not cooling"),
        "Property": relation_prop(prop2["id"]),
        "Priority": select_prop("High"),
        "Status": select_prop("In Progress"),
        "Reported Date": date_prop("2026-03-15"),
    })

    # --- Dashboard ---
    append_blocks(pid, [
        heading2("Portfolio Summary"),
        callout("Total Properties: 5 | Total Value: $1,300,000 | Monthly Cash Flow: Track in Transactions", "📊"),
        divider(),
        heading2("Quick Links"),
        bulleted("Properties — All properties with status and value"),
        bulleted("Transactions — Income and expenses by property"),
        bulleted("Tenants — Lease dates and contact info"),
        bulleted("Maintenance — Open repair requests"),
        bulleted("Documents — Leases, insurance, closing docs"),
        bulleted("Mortgages — Loan details and balances"),
        bulleted("Vacancies — Track lost income from empty units"),
        bulleted("Portfolio KPIs — Monthly/quarterly performance"),
    ])

    log.info("=== Property Investment Tracker DONE ===")
    return page


# ============================================================================
# TEMPLATE 4: Travel Planner & Journal ($12) — 8 DB
# ============================================================================

def build_travel_planner_journal(parent: dict) -> dict:
    log.info("=== Travel Planner & Journal ===")
    page = create_page(parent, "Travel Planner & Journal", "✈️", [
        heading1("Travel Planner & Journal"),
        paragraph("Your travel command center — plan trips, track expenses, and journal memories."),
        callout("Welcome to your travel command center! Add your first trip and start planning.", "🌍"),
        divider(),
    ])
    pid = page["id"]

    # --- DB1: Trips ---
    trips_db = create_database(pid, "Trips", "🗺️", {
        "Trip Name": p_title(),
        "Destination": p_rt(),
        "Status": p_select("Planning", "Booked", "In Progress", "Completed", "Cancelled"),
        "Start Date": p_date(),
        "End Date": p_date(),
        "Travel Companions": p_mselect("Solo"),
        "Trip Type": p_select("Solo", "Couple", "Family", "Group", "Business"),
        "Budget (Target)": p_number("dollar"),
        "Home Currency": p_select("USD", "EUR", "JPY", "GBP", "AUD", "BRL", "PYG"),
        "Notes": p_rt(),
        "Cover Image": p_files(),
    })
    trips_id = trips_db["id"]

    # --- DB2: Itinerary ---
    itinerary_db = create_database(pid, "Itinerary", "📍", {
        "Activity": p_title(),
        "Date": p_date(),
        "Start Time": p_rt(),
        "End Time": p_rt(),
        "Location": p_rt(),
        "Map Link": p_url(),
        "Category": p_select("Sightseeing", "Food", "Transport", "Shopping", "Adventure", "Relaxation", "Culture"),
        "Status": p_select("Planned", "Confirmed", "Done", "Skipped"),
        "Cost Estimate": p_number("dollar"),
        "Notes": p_rt(),
        "Priority": p_select("Must-do", "Nice-to-have", "Optional"),
    })
    itinerary_id = itinerary_db["id"]

    # --- DB3: Packing ---
    packing_db = create_database(pid, "Packing List", "🧳", {
        "Item": p_title(),
        "Category": p_select("Documents", "Clothing", "Toiletries", "Electronics", "Medicine", "Gear", "Misc"),
        "Trip Type Tag": p_mselect("Beach", "City", "Hiking", "Winter", "Business"),
        "Packed": p_checkbox(),
        "Quantity": p_number(),
        "Essential": p_checkbox(),
    })
    packing_id = packing_db["id"]

    # --- DB4: Expenses ---
    expenses_db = create_database(pid, "Expenses", "💸", {
        "Expense": p_title(),
        "Date": p_date(),
        "Category": p_select("Accommodation", "Food", "Transport", "Activities", "Shopping", "Insurance", "Visa", "Other"),
        "Local Amount": p_number(),
        "Local Currency": p_select("USD", "EUR", "JPY", "GBP", "AUD", "THB", "MXN"),
        "Exchange Rate": p_number(),
        "Payment Method": p_select("Cash", "Credit Card", "Debit", "Mobile Pay"),
        "Receipt": p_files(),
        "Notes": p_rt(),
    })
    expenses_id = expenses_db["id"]

    # --- DB5: Accommodation ---
    accommodation_db = create_database(pid, "Accommodation", "🏨", {
        "Name": p_title(),
        "Type": p_select("Hotel", "Hostel", "Airbnb", "Couchsurfing", "Camping", "Other"),
        "Check-in": p_date(),
        "Check-out": p_date(),
        "Price per Night": p_number("dollar"),
        "Currency": p_select("USD", "EUR", "JPY", "GBP"),
        "Location": p_rt(),
        "Map Link": p_url(),
        "Booking Link": p_url(),
        "Rating": p_select("★", "★★", "★★★", "★★★★", "★★★★★"),
        "Amenities": p_mselect("WiFi", "Kitchen", "AC", "Pool", "Laundry", "Parking", "Breakfast"),
        "Status": p_select("Researching", "Booked", "Stayed", "Cancelled"),
        "Notes": p_rt(),
    })
    accommodation_id = accommodation_db["id"]

    # --- DB6: Journal ---
    journal_db = create_database(pid, "Journal", "📔", {
        "Entry Title": p_title(),
        "Date": p_date(),
        "Mood": p_select("Amazing", "Good", "Okay", "Tough", "Terrible"),
        "Highlight": p_rt(),
        "Photos": p_files(),
        "Rating": p_select("★", "★★", "★★★", "★★★★", "★★★★★"),
        "Weather": p_select("Sunny", "Cloudy", "Rainy", "Snowy", "Hot", "Cold"),
        "Body": p_rt(),
    })
    journal_id = journal_db["id"]

    # --- DB7: Bucket List ---
    bucket_db = create_database(pid, "Bucket List", "🌟", {
        "Destination": p_title(),
        "Region": p_select("Asia", "Europe", "Americas", "Africa", "Oceania", "Middle East"),
        "Priority": p_select("Dream", "High", "Medium", "Low"),
        "Best Season": p_mselect("Spring", "Summer", "Fall", "Winter"),
        "Estimated Budget": p_number("dollar"),
        "Trip Duration (days)": p_number(),
        "Status": p_select("Dream", "Researching", "Planned", "Visited"),
        "Why I Want to Go": p_rt(),
        "Cover Image": p_files(),
    })
    bucket_id = bucket_db["id"]

    # --- DB8: Documents ---
    documents_db = create_database(pid, "Documents", "📋", {
        "Document": p_title(),
        "Type": p_select("Passport", "Visa", "Insurance", "Booking Confirmation", "Emergency Contact", "Vaccination", "Other"),
        "Number": p_rt(),
        "Expiry Date": p_date(),
        "File": p_files(),
        "Notes": p_rt(),
    })
    documents_id = documents_db["id"]

    # --- Relations: all DBs -> Trips ---
    _api("patch", f"/databases/{itinerary_id}", {"properties": {"Trip": p_relation(trips_id)}})
    _api("patch", f"/databases/{packing_id}", {"properties": {"Trip": p_relation(trips_id)}})
    _api("patch", f"/databases/{expenses_id}", {"properties": {"Trip": p_relation(trips_id)}})
    _api("patch", f"/databases/{accommodation_id}", {"properties": {"Trip": p_relation(trips_id)}})
    _api("patch", f"/databases/{journal_id}", {"properties": {"Trip": p_relation(trips_id)}})
    _api("patch", f"/databases/{bucket_id}", {"properties": {"Trip Link": p_relation(trips_id)}})
    _api("patch", f"/databases/{documents_id}", {"properties": {"Trip": p_relation(trips_id)}})

    # --- Sample Data: Trip ---
    trip1 = add_row(trips_id, {
        "Trip Name": title_prop("Tokyo & Kyoto Adventure"),
        "Destination": rt_prop("Tokyo & Kyoto, Japan"),
        "Status": select_prop("Planning"),
        "Start Date": date_prop("2026-05-01"),
        "End Date": date_prop("2026-05-10"),
        "Trip Type": select_prop("Solo"),
        "Budget (Target)": num_prop(2500),
        "Home Currency": select_prop("USD"),
    })

    # --- Sample Data: Itinerary ---
    itin_data = [
        ("Arrive Narita, train to Shinjuku", "2026-05-01", "14:00", "17:00", "Transport", "Planned"),
        ("Explore Shinjuku Gyoen", "2026-05-01", "17:30", "19:00", "Sightseeing", "Planned"),
        ("Dinner at Omoide Yokocho", "2026-05-01", "19:30", "21:00", "Food", "Planned"),
        ("Tsukiji Outer Market breakfast", "2026-05-02", "07:00", "08:30", "Food", "Planned"),
        ("TeamLab Borderless", "2026-05-02", "10:00", "12:30", "Culture", "Planned"),
        ("Shibuya crossing & Harajuku", "2026-05-02", "13:00", "17:00", "Sightseeing", "Planned"),
        ("Shinkansen to Kyoto", "2026-05-03", "08:00", "10:15", "Transport", "Planned"),
        ("Fushimi Inari shrine", "2026-05-03", "11:00", "13:00", "Sightseeing", "Planned"),
        ("Nishiki Market lunch", "2026-05-03", "13:30", "15:00", "Food", "Planned"),
    ]
    for act, date, start, end, cat, status in itin_data:
        add_row(itinerary_id, {
            "Activity": title_prop(act),
            "Trip": relation_prop(trip1["id"]),
            "Date": date_prop(date),
            "Start Time": rt_prop(start),
            "End Time": rt_prop(end),
            "Category": select_prop(cat),
            "Status": select_prop(status),
        })

    # --- Sample Data: Packing ---
    packing_items = [
        ("Passport", "Documents", True), ("Sunscreen SPF50", "Toiletries", False),
        ("Swimsuit", "Clothing", False), ("Flip flops", "Clothing", False),
        ("Sunglasses", "Gear", False), ("Beach towel", "Gear", False),
        ("Waterproof phone case", "Electronics", False), ("Charger", "Electronics", True),
        ("First aid kit", "Medicine", True), ("Travel adapter", "Electronics", True),
    ]
    for item, cat, essential in packing_items:
        add_row(packing_id, {
            "Item": title_prop(item),
            "Trip": relation_prop(trip1["id"]),
            "Category": select_prop(cat),
            "Packed": checkbox_prop(False),
            "Quantity": num_prop(1),
            "Essential": checkbox_prop(essential),
        })

    # --- Sample Data: Expenses ---
    exp_data = [
        ("Narita Express", "Transport", 3250, "JPY", 0.0067),
        ("Hotel night 1", "Accommodation", 12000, "JPY", 0.0067),
        ("Ramen dinner", "Food", 1100, "JPY", 0.0067),
        ("Tsukiji sushi", "Food", 3500, "JPY", 0.0067),
        ("TeamLab ticket", "Activities", 3800, "JPY", 0.0067),
    ]
    for desc, cat, amt, cur, rate in exp_data:
        add_row(expenses_id, {
            "Expense": title_prop(desc),
            "Trip": relation_prop(trip1["id"]),
            "Date": date_prop("2026-05-01"),
            "Category": select_prop(cat),
            "Local Amount": num_prop(amt),
            "Local Currency": select_prop(cur),
            "Exchange Rate": num_prop(rate),
            "Payment Method": select_prop("Credit Card"),
        })

    # --- Sample Data: Bucket List ---
    bucket_data = [
        ("Patagonia, Argentina", "Americas", "Dream", 3000, ["Fall"]),
        ("Iceland Ring Road", "Europe", "High", 4000, ["Summer"]),
        ("Bali, Indonesia", "Asia", "Medium", 1500, ["Spring"]),
        ("Morocco", "Africa", "High", 2000, ["Fall"]),
        ("New Zealand", "Oceania", "Dream", 5000, ["Summer"]),
    ]
    for dest, region, priority, budget, seasons in bucket_data:
        add_row(bucket_id, {
            "Destination": title_prop(dest),
            "Region": select_prop(region),
            "Priority": select_prop(priority),
            "Estimated Budget": num_prop(budget),
            "Best Season": mselect_prop(*seasons),
            "Status": select_prop(priority if priority in ("Dream",) else "Researching"),
        })

    # --- Sample Data: Journal ---
    add_row(journal_id, {
        "Entry Title": title_prop("Day 1 — First Steps in Tokyo"),
        "Trip": relation_prop(trip1["id"]),
        "Date": date_prop("2026-05-01"),
        "Mood": select_prop("Amazing"),
        "Highlight": rt_prop("Watching the sunset over Shinjuku from the park while cherry blossoms drifted down"),
        "Rating": select_prop("★★★★★"),
        "Weather": select_prop("Sunny"),
    })

    # --- Dashboard ---
    append_blocks(pid, [
        heading2("Upcoming Trips"),
        paragraph("Your next adventures await! Add trips and plan every detail."),
        divider(),
        heading2("Bucket List"),
        paragraph("Dream destinations to visit someday."),
        divider(),
        heading2("Quick Links"),
        bulleted("Trips — All your trips in one place"),
        bulleted("Itinerary — Day-by-day activity planning"),
        bulleted("Packing List — Never forget essentials"),
        bulleted("Expenses — Track spending in any currency"),
        bulleted("Accommodation — Compare and book stays"),
        bulleted("Journal — Capture memories and highlights"),
        bulleted("Bucket List — Dream destinations"),
        bulleted("Documents — Passports, visas, insurance"),
        divider(),
        toggle("Packing Presets", [
            bulleted("Beach Trip: Swimsuit, sunscreen, sunglasses, flip flops, beach towel, hat, aloe vera, waterproof bag"),
            bulleted("City Trip: Walking shoes, umbrella, day bag, power bank, guidebook, smart casual outfit"),
            bulleted("Hiking Trip: Hiking boots, rain jacket, water bottle, trail snacks, headlamp, first aid kit, trekking poles"),
            bulleted("Winter Trip: Thermal base layers, down jacket, gloves, beanie, hand warmers, waterproof boots, lip balm"),
            bulleted("Business Trip: Suit/blazer, dress shoes, laptop, business cards, portable charger, iron/steamer"),
        ]),
    ])

    log.info("=== Travel Planner & Journal DONE ===")
    return page


# ============================================================================
# TEMPLATE 5: Habit Tracker & Goal System ($9) — 7 DB
# ============================================================================

def build_habit_tracker_goal_system(parent: dict) -> dict:
    log.info("=== Habit Tracker & Goal System ===")
    page = create_page(parent, "Habit Tracker & Goal System", "🎯", [
        heading1("Habit Tracker & Goal System"),
        paragraph("Build better habits, track goals with OKRs, and reflect on your progress."),
        callout("Start by adding your habits, then check in daily. Review weekly to stay on track!", "🔥"),
        divider(),
    ])
    pid = page["id"]

    # --- DB1: Habits ---
    habits_db = create_database(pid, "Habits", "✅", {
        "Habit Name": p_title(),
        "Category": p_select("Health", "Learning", "Finance", "Mindfulness", "Productivity", "Social"),
        "Frequency": p_select("Daily", "Weekdays", "Weekends", "Custom"),
        "Status": p_select("Active", "Paused", "Archived"),
        "Icon": p_rt(),
        "Created": p_created_time(),
    })
    habits_id = habits_db["id"]

    # --- DB2: Daily Check-Ins ---
    checkins_db = create_database(pid, "Daily Check-Ins", "📆", {
        "Date": p_title(),
        "Completed": p_checkbox(),
        "Notes": p_rt(),
        "Mood": p_select("Great", "Good", "Okay", "Tough", "Bad"),
        "Energy Level": p_select("High", "Medium", "Low"),
    })
    checkins_id = checkins_db["id"]

    # Relation: Check-Ins -> Habits
    _api("patch", f"/databases/{checkins_id}", {"properties": {
        "Habit": p_relation(habits_id),
    }})

    # --- DB3: Goals (OKR) ---
    goals_db = create_database(pid, "Goals", "🏆", {
        "Objective": p_title(),
        "Time Frame": p_select("Q1", "Q2", "Q3", "Q4", "Annual", "Custom"),
        "Status": p_select("Not Started", "In Progress", "At Risk", "Completed", "Dropped"),
        "Priority": p_select("High", "Medium", "Low"),
        "Start Date": p_date(),
        "Target Date": p_date(),
        "Notes": p_rt(),
    })
    goals_id = goals_db["id"]

    # Relation: Goals <-> Habits
    _api("patch", f"/databases/{goals_id}", {"properties": {
        "Linked Habits": p_relation(habits_id),
    }})

    # --- DB4: Key Results ---
    kr_db = create_database(pid, "Key Results", "📊", {
        "Key Result": p_title(),
        "Target Value": p_number(),
        "Current Value": p_number(),
        "Unit": p_rt(),
        "Progress %": p_formula('if(prop("Target Value") > 0, min(prop("Current Value") / prop("Target Value") * 100, 100), 0)'),
        "Deadline": p_date(),
    })
    kr_id = kr_db["id"]

    # Relation: Key Results -> Goals
    _api("patch", f"/databases/{kr_id}", {"properties": {
        "Parent Goal": p_relation(goals_id),
    }})

    # --- DB5: Reviews ---
    reviews_db = create_database(pid, "Reviews", "📝", {
        "Title": p_title(),
        "Type": p_select("Weekly", "Monthly"),
        "Period Start": p_date(),
        "Period End": p_date(),
        "Wins": p_rt(),
        "Challenges": p_rt(),
        "Lessons": p_rt(),
        "Habit Completion Rate": p_number("percent"),
        "Next Period Focus": p_rt(),
        "Rating": p_select("★", "★★", "★★★", "★★★★", "★★★★★"),
    })
    reviews_id = reviews_db["id"]

    # Relation: Reviews -> Goals
    _api("patch", f"/databases/{reviews_id}", {"properties": {
        "Goals Reviewed": p_relation(goals_id),
    }})

    # --- DB6: Journal ---
    journal_db = create_database(pid, "Journal", "📓", {
        "Date": p_title(),
        "Entry": p_rt(),
        "Mood": p_select("Great", "Good", "Okay", "Tough", "Bad"),
        "Gratitude": p_rt(),
        "Daily Intention": p_rt(),
        "Evening Reflection": p_rt(),
        "Tags": p_mselect("Personal", "Work", "Health", "Learning", "Relationships"),
    })
    journal_id = journal_db["id"]

    # --- DB7: Rewards ---
    rewards_db = create_database(pid, "Rewards", "🎁", {
        "Reward": p_title(),
        "Milestone Type": p_select("Streak (7)", "Streak (21)", "Streak (30)", "Streak (60)", "Streak (100)", "Goal Completed", "Custom"),
        "Required Streak": p_number(),
        "Earned": p_checkbox(),
        "Earned Date": p_date(),
        "Cost": p_number("dollar"),
    })
    rewards_id = rewards_db["id"]

    # Relations: Rewards -> Goals, Rewards -> Habits
    _api("patch", f"/databases/{rewards_id}", {"properties": {
        "Linked Goal": p_relation(goals_id),
        "Linked Habit": p_relation(habits_id),
    }})

    # --- Sample Data: Habits ---
    h1 = add_row(habits_id, {"Habit Name": title_prop("Meditate 10 minutes"), "Category": select_prop("Mindfulness"), "Frequency": select_prop("Daily"), "Status": select_prop("Active"), "Icon": rt_prop("🧘")})
    h2 = add_row(habits_id, {"Habit Name": title_prop("Read 20 pages"), "Category": select_prop("Learning"), "Frequency": select_prop("Daily"), "Status": select_prop("Active"), "Icon": rt_prop("📖")})
    h3 = add_row(habits_id, {"Habit Name": title_prop("Exercise 30 minutes"), "Category": select_prop("Health"), "Frequency": select_prop("Weekdays"), "Status": select_prop("Active"), "Icon": rt_prop("💪")})
    h4 = add_row(habits_id, {"Habit Name": title_prop("Write in journal"), "Category": select_prop("Mindfulness"), "Frequency": select_prop("Daily"), "Status": select_prop("Active"), "Icon": rt_prop("✍️")})
    h5 = add_row(habits_id, {"Habit Name": title_prop("No social media before noon"), "Category": select_prop("Productivity"), "Frequency": select_prop("Daily"), "Status": select_prop("Active"), "Icon": rt_prop("📵")})
    h6 = add_row(habits_id, {"Habit Name": title_prop("Save $5 to investment fund"), "Category": select_prop("Finance"), "Frequency": select_prop("Daily"), "Status": select_prop("Active"), "Icon": rt_prop("💰")})

    # --- Sample Data: Goal ---
    g1 = add_row(goals_id, {
        "Objective": title_prop("Build a consistent morning routine by end of Q1"),
        "Time Frame": select_prop("Q1"),
        "Status": select_prop("In Progress"),
        "Priority": select_prop("High"),
        "Start Date": date_prop("2026-01-01"),
        "Target Date": date_prop("2026-03-31"),
        "Linked Habits": relation_prop(h1["id"], h2["id"], h3["id"]),
    })

    # --- Sample Data: Key Results ---
    add_row(kr_id, {"Key Result": title_prop("Complete morning meditation 80 of 90 days"), "Parent Goal": relation_prop(g1["id"]), "Target Value": num_prop(80), "Current Value": num_prop(45), "Unit": rt_prop("days"), "Deadline": date_prop("2026-03-31")})
    add_row(kr_id, {"Key Result": title_prop("Read 6 books"), "Parent Goal": relation_prop(g1["id"]), "Target Value": num_prop(6), "Current Value": num_prop(3), "Unit": rt_prop("books"), "Deadline": date_prop("2026-03-31")})
    add_row(kr_id, {"Key Result": title_prop("Exercise 60 of 90 days"), "Parent Goal": relation_prop(g1["id"]), "Target Value": num_prop(60), "Current Value": num_prop(35), "Unit": rt_prop("days"), "Deadline": date_prop("2026-03-31")})

    # --- Sample Data: Rewards ---
    add_row(rewards_id, {"Reward": title_prop("Buy a new book"), "Milestone Type": select_prop("Streak (7)"), "Linked Habit": relation_prop(h2["id"]), "Required Streak": num_prop(7), "Earned": checkbox_prop(True), "Earned Date": date_prop("2026-01-08")})
    add_row(rewards_id, {"Reward": title_prop("Spa day"), "Milestone Type": select_prop("Streak (30)"), "Linked Habit": relation_prop(h1["id"]), "Required Streak": num_prop(30), "Earned": checkbox_prop(False)})
    add_row(rewards_id, {"Reward": title_prop("Weekend trip"), "Milestone Type": select_prop("Goal Completed"), "Linked Goal": relation_prop(g1["id"]), "Earned": checkbox_prop(False)})

    # --- Sample Data: Weekly Review ---
    add_row(reviews_id, {
        "Title": title_prop("Week 1 Review"),
        "Type": select_prop("Weekly"),
        "Period Start": date_prop("2026-01-01"),
        "Period End": date_prop("2026-01-07"),
        "Wins": rt_prop("Hit 100% on meditation, finished 1 book"),
        "Challenges": rt_prop("Missed 2 exercise days due to rain"),
        "Lessons": rt_prop("Need indoor workout backup plan"),
        "Habit Completion Rate": num_prop(85),
        "Rating": select_prop("★★★★"),
        "Next Period Focus": rt_prop("Add bodyweight routine, start journaling daily"),
        "Goals Reviewed": relation_prop(g1["id"]),
    })

    # --- Sample Data: Journal ---
    add_row(journal_id, {
        "Date": title_prop(_d(0)),
        "Mood": select_prop("Good"),
        "Gratitude": rt_prop("Morning sunshine, productive work session, good conversation with a friend"),
        "Daily Intention": rt_prop("Stay present during meetings"),
        "Evening Reflection": rt_prop("Managed to stay focused most of the day. The no-social-media habit is getting easier."),
        "Tags": mselect_prop("Personal", "Work"),
    })

    # --- Dashboard ---
    append_blocks(pid, [
        heading2("Daily Command Center"),
        callout("Check in on your habits daily. Track streaks and build momentum!", "🔥"),
        divider(),
        heading2("Goals & Progress"),
        paragraph("Track your OKRs and key results here."),
        divider(),
        heading2("Reflection & Rewards"),
        paragraph("Review weekly, journal daily, earn rewards for consistency."),
        divider(),
        heading2("Quick Links"),
        bulleted("Habits — All active habits with categories"),
        bulleted("Daily Check-Ins — One-click daily tracking"),
        bulleted("Goals — OKR-style goal setting"),
        bulleted("Key Results — Measurable progress tracking"),
        bulleted("Reviews — Weekly and monthly reflections"),
        bulleted("Journal — Daily gratitude and intentions"),
        bulleted("Rewards — Earn rewards for streaks and milestones"),
        divider(),
        toggle("Quick-Start Guide", [
            numbered("Add 3-5 habits you want to build"),
            numbered("Set one goal with 2-3 key results"),
            numbered("Check in daily on your habits"),
            numbered("Write a brief journal entry each evening"),
            numbered("Review your week every Sunday"),
            numbered("Set rewards to stay motivated"),
        ]),
    ])

    log.info("=== Habit Tracker & Goal System DONE ===")
    return page


# ============================================================================
# TEMPLATE 6: Personal Finance Dashboard ($14) — 8 DB
# ============================================================================

def build_personal_finance_dashboard(parent: dict) -> dict:
    log.info("=== Personal Finance Dashboard ===")
    page = create_page(parent, "Personal Finance Dashboard", "💰", [
        heading1("Personal Finance Dashboard"),
        paragraph("Track income, expenses, subscriptions, savings, and debt in one place."),
        callout("Start by adding your accounts, then log transactions daily. Review monthly!", "📊"),
        divider(),
    ])
    pid = page["id"]

    # --- DB1: Transactions ---
    transactions_db = create_database(pid, "Transactions", "💳", {
        "Name": p_title(),
        "Amount": p_number("dollar"),
        "Type": p_select("Income", "Expense"),
        "Date": p_date(),
        "Payment Method": p_select("Cash", "Debit Card", "Credit Card", "Bank Transfer", "PayPal", "Other"),
        "Recurring": p_checkbox(),
        "Notes": p_rt(),
        "Receipt": p_files(),
    })
    transactions_id = transactions_db["id"]

    # --- DB2: Categories ---
    categories_db = create_database(pid, "Categories", "🏷️", {
        "Name": p_title(),
        "Type": p_select("Income", "Expense"),
        "Icon": p_rt(),
        "Monthly Budget": p_number("dollar"),
    })
    categories_id = categories_db["id"]

    # Relation: Transactions <-> Categories
    _api("patch", f"/databases/{transactions_id}", {"properties": {
        "Category": p_relation(categories_id),
    }})

    # --- DB3: Subscriptions ---
    subscriptions_db = create_database(pid, "Subscriptions", "🔄", {
        "Name": p_title(),
        "Cost": p_number("dollar"),
        "Billing Cycle": p_select("Monthly", "Quarterly", "Annual"),
        "Next Renewal": p_date(),
        "Category": p_select("Streaming", "Software", "Cloud Storage", "Music", "Fitness", "News", "Gaming", "Other"),
        "Status": p_select("Active", "Paused", "Cancelled", "Trial"),
        "Payment Method": p_select("Cash", "Debit Card", "Credit Card", "Bank Transfer", "PayPal", "Other"),
        "Annual Cost": p_formula('if(prop("Billing Cycle") == "Monthly", prop("Cost") * 12, if(prop("Billing Cycle") == "Quarterly", prop("Cost") * 4, prop("Cost")))'),
        "URL": p_url(),
        "Notes": p_rt(),
    })
    subscriptions_id = subscriptions_db["id"]

    # --- DB4: Savings Goals ---
    savings_db = create_database(pid, "Savings Goals", "🎯", {
        "Name": p_title(),
        "Target Amount": p_number("dollar"),
        "Current Amount": p_number("dollar"),
        "Progress": p_formula('if(prop("Target Amount") > 0, round(prop("Current Amount") / prop("Target Amount") * 100), 0)'),
        "Deadline": p_date(),
        "Priority": p_select("High", "Medium", "Low"),
        "Category": p_select("Emergency", "Travel", "Purchase", "Education", "Retirement", "Other"),
        "Monthly Contribution": p_number("dollar"),
        "Notes": p_rt(),
    })
    savings_id = savings_db["id"]

    # --- DB5: Savings Contributions ---
    contributions_db = create_database(pid, "Savings Contributions", "💵", {
        "Name": p_title(),
        "Amount": p_number("dollar"),
        "Date": p_date(),
        "Notes": p_rt(),
    })
    contributions_id = contributions_db["id"]

    # Relation: Contributions -> Savings Goals
    _api("patch", f"/databases/{contributions_id}", {"properties": {
        "Goal": p_relation(savings_id),
    }})

    # --- DB6: Debts ---
    debts_db = create_database(pid, "Debts", "📉", {
        "Name": p_title(),
        "Original Balance": p_number("dollar"),
        "Current Balance": p_number("dollar"),
        "Interest Rate": p_number("percent"),
        "Minimum Payment": p_number("dollar"),
        "Extra Payment": p_number("dollar"),
        "Total Monthly": p_formula('prop("Minimum Payment") + prop("Extra Payment")'),
        "Due Date": p_number(),
        "Type": p_select("Credit Card", "Student Loan", "Car Loan", "Mortgage", "Personal Loan", "Medical", "Other"),
        "Lender": p_rt(),
        "Progress": p_formula('if(prop("Original Balance") > 0, round((1 - prop("Current Balance") / prop("Original Balance")) * 100), 0)'),
    })
    debts_id = debts_db["id"]

    # --- DB7: Accounts ---
    accounts_db = create_database(pid, "Accounts", "🏦", {
        "Name": p_title(),
        "Type": p_select("Checking", "Savings", "Credit Card", "Investment", "Cash", "Digital Wallet", "Other"),
        "Balance": p_number("dollar"),
        "Institution": p_rt(),
        "Currency": p_select("USD", "EUR", "GBP", "JPY", "Other"),
        "Notes": p_rt(),
    })
    accounts_id = accounts_db["id"]

    # Relation: Transactions -> Accounts
    _api("patch", f"/databases/{transactions_id}", {"properties": {
        "Account": p_relation(accounts_id),
    }})

    # --- DB8: Monthly Snapshots ---
    snapshots_db = create_database(pid, "Monthly Snapshots", "📅", {
        "Name": p_title(),
        "Month": p_date(),
        "Total Income": p_number("dollar"),
        "Total Expenses": p_number("dollar"),
        "Net Cash Flow": p_formula('prop("Total Income") - prop("Total Expenses")'),
        "Savings Rate": p_formula('if(prop("Total Income") > 0, round(prop("Net Cash Flow") / prop("Total Income") * 100), 0)'),
        "Total Assets": p_number("dollar"),
        "Total Liabilities": p_number("dollar"),
        "Net Worth": p_formula('prop("Total Assets") - prop("Total Liabilities")'),
        "Notes": p_rt(),
    })
    snapshots_id = snapshots_db["id"]

    # --- Sample Data: Accounts ---
    acc_checking = add_row(accounts_id, {"Name": title_prop("Main Checking"), "Type": select_prop("Checking"), "Balance": num_prop(3240), "Institution": rt_prop("Chase"), "Currency": select_prop("USD")})
    acc_savings = add_row(accounts_id, {"Name": title_prop("Savings"), "Type": select_prop("Savings"), "Balance": num_prop(8500), "Institution": rt_prop("Ally Bank"), "Currency": select_prop("USD")})
    acc_cc = add_row(accounts_id, {"Name": title_prop("Credit Card"), "Type": select_prop("Credit Card"), "Balance": num_prop(-1200), "Institution": rt_prop("Capital One"), "Currency": select_prop("USD")})
    acc_invest = add_row(accounts_id, {"Name": title_prop("Investment"), "Type": select_prop("Investment"), "Balance": num_prop(15000), "Institution": rt_prop("Vanguard"), "Currency": select_prop("USD")})
    acc_cash = add_row(accounts_id, {"Name": title_prop("Cash"), "Type": select_prop("Cash"), "Balance": num_prop(120), "Currency": select_prop("USD")})

    # --- Sample Data: Categories ---
    cat_names_expense = ["Housing", "Food & Groceries", "Transportation", "Utilities", "Entertainment", "Health", "Shopping", "Education", "Personal Care", "Gifts", "Insurance", "Miscellaneous"]
    cat_names_income = ["Salary", "Freelance", "Side Hustle", "Investment Returns", "Refunds", "Other Income"]
    expense_cats = {}
    for c in cat_names_expense:
        r = add_row(categories_id, {"Name": title_prop(c), "Type": select_prop("Expense")})
        expense_cats[c] = r["id"]
    income_cats = {}
    for c in cat_names_income:
        r = add_row(categories_id, {"Name": title_prop(c), "Type": select_prop("Income")})
        income_cats[c] = r["id"]

    # --- Sample Data: Transactions (subset) ---
    add_row(transactions_id, {"Name": title_prop("Monthly Salary"), "Amount": num_prop(4500), "Type": select_prop("Income"), "Date": date_prop("2026-03-01"), "Category": relation_prop(income_cats["Salary"]), "Account": relation_prop(acc_checking["id"]), "Recurring": checkbox_prop(True)})
    add_row(transactions_id, {"Name": title_prop("Rent"), "Amount": num_prop(1200), "Type": select_prop("Expense"), "Date": date_prop("2026-03-01"), "Category": relation_prop(expense_cats["Housing"]), "Account": relation_prop(acc_checking["id"]), "Recurring": checkbox_prop(True)})
    add_row(transactions_id, {"Name": title_prop("Grocery shopping"), "Amount": num_prop(85), "Type": select_prop("Expense"), "Date": date_prop("2026-03-03"), "Category": relation_prop(expense_cats["Food & Groceries"]), "Account": relation_prop(acc_checking["id"])})
    add_row(transactions_id, {"Name": title_prop("Electric bill"), "Amount": num_prop(65), "Type": select_prop("Expense"), "Date": date_prop("2026-03-05"), "Category": relation_prop(expense_cats["Utilities"]), "Account": relation_prop(acc_checking["id"]), "Recurring": checkbox_prop(True)})
    add_row(transactions_id, {"Name": title_prop("Freelance project"), "Amount": num_prop(800), "Type": select_prop("Income"), "Date": date_prop("2026-03-10"), "Category": relation_prop(income_cats["Freelance"]), "Account": relation_prop(acc_checking["id"])})
    add_row(transactions_id, {"Name": title_prop("Dining out"), "Amount": num_prop(45), "Type": select_prop("Expense"), "Date": date_prop("2026-03-08"), "Category": relation_prop(expense_cats["Entertainment"]), "Account": relation_prop(acc_cc["id"])})

    # --- Sample Data: Subscriptions ---
    subs = [
        ("Netflix", 15.49, "Monthly", "Streaming", _d(10)),
        ("Spotify", 10.99, "Monthly", "Music", _d(15)),
        ("Notion", 10, "Monthly", "Software", _d(20)),
        ("iCloud", 2.99, "Monthly", "Cloud Storage", _d(5)),
        ("Gym", 35, "Monthly", "Fitness", _d(1)),
        ("Adobe Creative Cloud", 22.99, "Monthly", "Software", _d(12)),
        ("ChatGPT Plus", 20, "Monthly", "Software", _d(18)),
    ]
    for name, cost, cycle, cat, renewal in subs:
        add_row(subscriptions_id, {
            "Name": title_prop(name),
            "Cost": num_prop(cost),
            "Billing Cycle": select_prop(cycle),
            "Category": select_prop(cat),
            "Status": select_prop("Active"),
            "Next Renewal": date_prop(renewal),
        })

    # --- Sample Data: Savings Goals ---
    add_row(savings_id, {"Name": title_prop("Emergency Fund"), "Target Amount": num_prop(10000), "Current Amount": num_prop(6200), "Priority": select_prop("High"), "Category": select_prop("Emergency"), "Monthly Contribution": num_prop(300), "Deadline": date_prop("2026-12-31")})
    add_row(savings_id, {"Name": title_prop("Vacation Fund"), "Target Amount": num_prop(2500), "Current Amount": num_prop(800), "Priority": select_prop("Medium"), "Category": select_prop("Travel"), "Monthly Contribution": num_prop(150), "Deadline": date_prop("2026-08-01")})
    add_row(savings_id, {"Name": title_prop("New Laptop"), "Target Amount": num_prop(1500), "Current Amount": num_prop(400), "Priority": select_prop("Low"), "Category": select_prop("Purchase"), "Monthly Contribution": num_prop(100), "Deadline": date_prop("2026-10-01")})

    # --- Sample Data: Debts ---
    add_row(debts_id, {"Name": title_prop("Credit Card"), "Original Balance": num_prop(3000), "Current Balance": num_prop(1200), "Interest Rate": num_prop(22.99), "Minimum Payment": num_prop(35), "Extra Payment": num_prop(65), "Type": select_prop("Credit Card"), "Due Date": num_prop(15), "Lender": rt_prop("Capital One")})
    add_row(debts_id, {"Name": title_prop("Student Loan"), "Original Balance": num_prop(25000), "Current Balance": num_prop(18500), "Interest Rate": num_prop(5.5), "Minimum Payment": num_prop(280), "Extra Payment": num_prop(0), "Type": select_prop("Student Loan"), "Due Date": num_prop(1), "Lender": rt_prop("Nelnet")})
    add_row(debts_id, {"Name": title_prop("Car Loan"), "Original Balance": num_prop(15000), "Current Balance": num_prop(8200), "Interest Rate": num_prop(4.9), "Minimum Payment": num_prop(320), "Extra Payment": num_prop(0), "Type": select_prop("Car Loan"), "Due Date": num_prop(20), "Lender": rt_prop("Local Credit Union")})

    # --- Sample Data: Monthly Snapshots ---
    add_row(snapshots_id, {"Name": title_prop("2026-02"), "Month": date_prop("2026-02-01"), "Total Income": num_prop(5100), "Total Expenses": num_prop(3800), "Total Assets": num_prop(26000), "Total Liabilities": num_prop(28500)})
    add_row(snapshots_id, {"Name": title_prop("2026-03"), "Month": date_prop("2026-03-01"), "Total Income": num_prop(5300), "Total Expenses": num_prop(3600), "Total Assets": num_prop(26860), "Total Liabilities": num_prop(27900)})

    # --- Dashboard ---
    append_blocks(pid, [
        heading2("Quick Stats"),
        callout("Track your income, expenses, and net worth at a glance. Log transactions daily for best results.", "📊"),
        divider(),
        heading2("Quick Links"),
        bulleted("Transactions — Log every income and expense"),
        bulleted("Categories — Organize spending and set budgets"),
        bulleted("Subscriptions — Track recurring payments"),
        bulleted("Savings Goals — Visual progress toward goals"),
        bulleted("Debts — Snowball or avalanche payoff tracker"),
        bulleted("Accounts — All bank accounts and balances"),
        bulleted("Monthly Snapshots — Month-end financial summary"),
        divider(),
        toggle("Debt Payoff Strategies", [
            paragraph("Avalanche Method: Pay minimums on all debts, put extra toward the highest interest rate first. Saves the most money."),
            paragraph("Snowball Method: Pay minimums on all debts, put extra toward the smallest balance first. Builds momentum with quick wins."),
        ]),
    ])

    log.info("=== Personal Finance Dashboard DONE ===")
    return page


# ============================================================================
# TEMPLATE 7: Airbnb Host Management Hub ($17) — 7 DB
# ============================================================================

def build_airbnb_host_management_hub(parent: dict) -> dict:
    log.info("=== Airbnb Host Management Hub ===")
    page = create_page(parent, "Airbnb Host Management Hub", "🏡", [
        heading1("Airbnb Host Management Hub"),
        paragraph("Your Short-Term Rental HQ — manage listings, bookings, cleanings, revenue, and guest communication."),
        callout("Add your listings, then track every booking and automate your hosting workflow!", "🔑"),
        divider(),
    ])
    pid = page["id"]

    # --- DB1: Listings ---
    listings_db = create_database(pid, "Listings", "🏘️", {
        "Listing Name": p_title(),
        "Platform": p_mselect("Airbnb", "VRBO", "Booking.com", "Direct"),
        "Status": p_select("Active", "Paused", "Under Maintenance", "Deactivated"),
        "Property Type": p_select("Entire Home", "Private Room", "Shared Room", "Unique Stay"),
        "Location": p_rt(),
        "Bedrooms": p_number(),
        "Bathrooms": p_number(),
        "Max Guests": p_number(),
        "Base Nightly Rate": p_number("dollar"),
        "Cleaning Fee": p_number("dollar"),
        "Listing URL": p_url(),
        "Photo": p_files(),
        "WiFi Password": p_rt(),
        "Check-in Instructions": p_rt(),
        "House Rules": p_rt(),
        "Notes": p_rt(),
    })
    listings_id = listings_db["id"]

    # --- DB2: Bookings ---
    bookings_db = create_database(pid, "Bookings", "📅", {
        "Guest Name": p_title(),
        "Platform": p_select("Airbnb", "VRBO", "Booking.com", "Direct"),
        "Check-in": p_date(),
        "Check-out": p_date(),
        "Guests": p_number(),
        "Nightly Rate": p_number("dollar"),
        "Total Payout": p_number("dollar"),
        "Status": p_select("Confirmed", "Checked In", "Checked Out", "Cancelled", "No-Show"),
        "Communication Stage": p_select("Pre-Arrival", "Welcome Sent", "Mid-Stay", "Checkout Sent", "Review Requested", "Complete"),
        "Guest Email": p_email(),
        "Guest Phone": p_phone(),
        "Special Requests": p_rt(),
        "Rating Given": p_select("5 Stars", "4 Stars", "3 Stars", "2 Stars", "1 Star", "Not Yet"),
        "Review Written": p_checkbox(),
        "Notes": p_rt(),
    })
    bookings_id = bookings_db["id"]

    # --- DB3: Cleanings ---
    cleanings_db = create_database(pid, "Cleanings", "🧹", {
        "Cleaning Task": p_title(),
        "Cleaner": p_select("Cleaner A", "Cleaner B", "Cleaner C", "Self"),
        "Date": p_date(),
        "Time Slot": p_select("Morning (8-11am)", "Afternoon (12-3pm)", "Evening (4-7pm)"),
        "Status": p_select("Scheduled", "In Progress", "Completed", "Issue Reported"),
        "Type": p_select("Turnover", "Deep Clean", "Mid-Stay", "Inspection"),
        "Checklist Completed": p_checkbox(),
        "Cost": p_number("dollar"),
        "Supply Notes": p_rt(),
        "Photos": p_files(),
        "Notes": p_rt(),
    })
    cleanings_id = cleanings_db["id"]

    # --- DB4: Transactions ---
    transactions_db = create_database(pid, "Transactions", "💵", {
        "Description": p_title(),
        "Type": p_select("Income", "Expense"),
        "Category": p_select("Booking Payout", "Cleaning Fee Collected", "Direct Payment", "Cleaning Cost", "Maintenance", "Supplies", "Platform Fee", "Insurance", "Utilities", "Mortgage", "Property Tax", "Furnishing", "Marketing", "Other"),
        "Amount": p_number("dollar"),
        "Date": p_date(),
        "Tax Deductible": p_checkbox(),
        "Receipt": p_files(),
        "Notes": p_rt(),
    })
    transactions_id = transactions_db["id"]

    # --- DB5: Maintenance ---
    maintenance_db = create_database(pid, "Maintenance", "🔧", {
        "Issue Title": p_title(),
        "Reported By": p_select("Guest", "Cleaner", "Self", "Neighbor"),
        "Priority": p_select("Emergency", "High", "Medium", "Low"),
        "Status": p_select("Reported", "Scheduled", "In Progress", "Waiting for Parts", "Completed"),
        "Reported Date": p_date(),
        "Resolved Date": p_date(),
        "Cost": p_number("dollar"),
        "Contractor": p_rt(),
        "Photos": p_files(),
        "Notes": p_rt(),
    })
    maintenance_id = maintenance_db["id"]

    # --- DB6: Supplies ---
    supplies_db = create_database(pid, "Supplies", "📦", {
        "Item Name": p_title(),
        "Category": p_select("Toiletries", "Linens", "Kitchen", "Cleaning Products", "Welcome Kit", "Electronics", "Furniture", "Other"),
        "Current Stock": p_number(),
        "Reorder Threshold": p_number(),
        "Needs Reorder": p_formula('if(prop("Current Stock") <= prop("Reorder Threshold"), "Yes", "No")'),
        "Unit Cost": p_number("dollar"),
        "Supplier": p_rt(),
        "Purchase URL": p_url(),
        "Last Restocked": p_date(),
        "Notes": p_rt(),
    })
    supplies_id = supplies_db["id"]

    # --- DB7: Pricing Calendar ---
    pricing_db = create_database(pid, "Pricing Calendar", "💲", {
        "Period Name": p_title(),
        "Season": p_select("Peak", "High", "Mid", "Low", "Holiday", "Event"),
        "Start Date": p_date(),
        "End Date": p_date(),
        "Nightly Rate": p_number("dollar"),
        "Minimum Stay": p_number(),
        "Competitor Rate": p_number("dollar"),
        "Rate Difference": p_formula('prop("Nightly Rate") - prop("Competitor Rate")'),
        "Occupancy Target": p_number("percent"),
        "Notes": p_rt(),
    })
    pricing_id = pricing_db["id"]

    # --- Relations ---
    _api("patch", f"/databases/{listings_id}", {"properties": {
        "Bookings": p_relation(bookings_id),
        "Cleanings": p_relation(cleanings_id),
        "Transactions": p_relation(transactions_id),
        "Maintenance": p_relation(maintenance_id),
        "Supplies": p_relation(supplies_id),
    }})
    _api("patch", f"/databases/{bookings_id}", {"properties": {
        "Listing": p_relation(listings_id),
        "Cleaning": p_relation(cleanings_id),
    }})
    _api("patch", f"/databases/{cleanings_id}", {"properties": {
        "Listing": p_relation(listings_id),
        "Booking": p_relation(bookings_id),
    }})
    _api("patch", f"/databases/{transactions_id}", {"properties": {
        "Listing": p_relation(listings_id),
        "Booking": p_relation(bookings_id),
    }})
    _api("patch", f"/databases/{maintenance_id}", {"properties": {
        "Listing": p_relation(listings_id),
        "Expense": p_relation(transactions_id),
    }})
    _api("patch", f"/databases/{supplies_id}", {"properties": {
        "Listing": p_relation(listings_id),
    }})
    _api("patch", f"/databases/{pricing_id}", {"properties": {
        "Listing": p_relation(listings_id),
    }})

    # --- Sample Data: Listings ---
    l1 = add_row(listings_id, {"Listing Name": title_prop("Sunny Downtown Loft"), "Platform": mselect_prop("Airbnb", "VRBO"), "Status": select_prop("Active"), "Property Type": select_prop("Entire Home"), "Bedrooms": num_prop(1), "Bathrooms": num_prop(1), "Max Guests": num_prop(4), "Base Nightly Rate": num_prop(120), "Cleaning Fee": num_prop(60)})
    l2 = add_row(listings_id, {"Listing Name": title_prop("Cozy Beach Cottage"), "Platform": mselect_prop("Airbnb"), "Status": select_prop("Active"), "Property Type": select_prop("Entire Home"), "Bedrooms": num_prop(2), "Bathrooms": num_prop(1), "Max Guests": num_prop(6), "Base Nightly Rate": num_prop(180), "Cleaning Fee": num_prop(80)})
    l3 = add_row(listings_id, {"Listing Name": title_prop("Modern Studio near Airport"), "Platform": mselect_prop("Airbnb", "Booking.com"), "Status": select_prop("Active"), "Property Type": select_prop("Entire Home"), "Bedrooms": num_prop(0), "Bathrooms": num_prop(1), "Max Guests": num_prop(2), "Base Nightly Rate": num_prop(75), "Cleaning Fee": num_prop(40)})
    l4 = add_row(listings_id, {"Listing Name": title_prop("Mountain View Cabin"), "Platform": mselect_prop("Airbnb", "Direct"), "Status": select_prop("Paused"), "Property Type": select_prop("Entire Home"), "Bedrooms": num_prop(3), "Bathrooms": num_prop(2), "Max Guests": num_prop(8), "Base Nightly Rate": num_prop(250), "Cleaning Fee": num_prop(120)})

    # --- Sample Data: Bookings ---
    b1 = add_row(bookings_id, {"Guest Name": title_prop("Sarah M."), "Listing": relation_prop(l1["id"]), "Platform": select_prop("Airbnb"), "Check-in": date_prop("2026-03-18"), "Check-out": date_prop("2026-03-21"), "Guests": num_prop(2), "Nightly Rate": num_prop(110), "Total Payout": num_prop(297), "Status": select_prop("Checked Out"), "Communication Stage": select_prop("Review Requested"), "Review Written": checkbox_prop(False)})
    b2 = add_row(bookings_id, {"Guest Name": title_prop("James K."), "Listing": relation_prop(l2["id"]), "Platform": select_prop("Airbnb"), "Check-in": date_prop("2026-03-22"), "Check-out": date_prop("2026-03-27"), "Guests": num_prop(4), "Nightly Rate": num_prop(180), "Total Payout": num_prop(810), "Status": select_prop("Confirmed"), "Communication Stage": select_prop("Pre-Arrival")})
    b3 = add_row(bookings_id, {"Guest Name": title_prop("Emily R."), "Listing": relation_prop(l3["id"]), "Platform": select_prop("Booking.com"), "Check-in": date_prop("2026-03-19"), "Check-out": date_prop("2026-03-20"), "Guests": num_prop(1), "Nightly Rate": num_prop(75), "Total Payout": num_prop(64), "Status": select_prop("Checked Out"), "Communication Stage": select_prop("Complete"), "Review Written": checkbox_prop(True)})
    add_row(bookings_id, {"Guest Name": title_prop("Carlos D."), "Listing": relation_prop(l1["id"]), "Platform": select_prop("Airbnb"), "Check-in": date_prop("2026-03-22"), "Check-out": date_prop("2026-03-25"), "Guests": num_prop(3), "Nightly Rate": num_prop(120), "Total Payout": num_prop(324), "Status": select_prop("Confirmed"), "Communication Stage": select_prop("Pre-Arrival")})
    add_row(bookings_id, {"Guest Name": title_prop("Yuki T."), "Listing": relation_prop(l2["id"]), "Platform": select_prop("Airbnb"), "Check-in": date_prop("2026-03-28"), "Check-out": date_prop("2026-04-02"), "Guests": num_prop(2), "Nightly Rate": num_prop(195), "Total Payout": num_prop(878), "Status": select_prop("Confirmed")})
    add_row(bookings_id, {"Guest Name": title_prop("Mike & Lisa"), "Listing": relation_prop(l4["id"]), "Platform": select_prop("Direct"), "Check-in": date_prop("2026-04-05"), "Check-out": date_prop("2026-04-12"), "Guests": num_prop(6), "Nightly Rate": num_prop(250), "Total Payout": num_prop(1575), "Status": select_prop("Confirmed")})

    # --- Sample Data: Cleanings ---
    add_row(cleanings_id, {"Cleaning Task": title_prop("Turnover - Loft - Mar 21"), "Listing": relation_prop(l1["id"]), "Booking": relation_prop(b1["id"]), "Cleaner": select_prop("Cleaner A"), "Date": date_prop("2026-03-21"), "Type": select_prop("Turnover"), "Status": select_prop("Completed"), "Cost": num_prop(60), "Checklist Completed": checkbox_prop(True)})
    add_row(cleanings_id, {"Cleaning Task": title_prop("Turnover - Studio - Mar 20"), "Listing": relation_prop(l3["id"]), "Booking": relation_prop(b3["id"]), "Cleaner": select_prop("Cleaner B"), "Date": date_prop("2026-03-20"), "Type": select_prop("Turnover"), "Status": select_prop("Completed"), "Cost": num_prop(40), "Checklist Completed": checkbox_prop(True)})
    add_row(cleanings_id, {"Cleaning Task": title_prop("Turnover - Loft - Mar 25"), "Listing": relation_prop(l1["id"]), "Cleaner": select_prop("Cleaner A"), "Date": date_prop("2026-03-25"), "Type": select_prop("Turnover"), "Status": select_prop("Scheduled"), "Cost": num_prop(60)})
    add_row(cleanings_id, {"Cleaning Task": title_prop("Deep Clean - Beach Cottage"), "Listing": relation_prop(l2["id"]), "Cleaner": select_prop("Cleaner A"), "Date": date_prop("2026-03-21"), "Type": select_prop("Deep Clean"), "Status": select_prop("Scheduled"), "Cost": num_prop(120)})

    # --- Sample Data: Transactions ---
    add_row(transactions_id, {"Description": title_prop("Payout - Sarah M."), "Listing": relation_prop(l1["id"]), "Booking": relation_prop(b1["id"]), "Type": select_prop("Income"), "Category": select_prop("Booking Payout"), "Amount": num_prop(297), "Date": date_prop("2026-03-21")})
    add_row(transactions_id, {"Description": title_prop("Payout - Emily R."), "Listing": relation_prop(l3["id"]), "Booking": relation_prop(b3["id"]), "Type": select_prop("Income"), "Category": select_prop("Booking Payout"), "Amount": num_prop(64), "Date": date_prop("2026-03-20")})
    add_row(transactions_id, {"Description": title_prop("Cleaning - Loft Mar 21"), "Listing": relation_prop(l1["id"]), "Type": select_prop("Expense"), "Category": select_prop("Cleaning Cost"), "Amount": num_prop(60), "Date": date_prop("2026-03-21"), "Tax Deductible": checkbox_prop(True)})
    add_row(transactions_id, {"Description": title_prop("Cleaning - Studio Mar 20"), "Listing": relation_prop(l3["id"]), "Type": select_prop("Expense"), "Category": select_prop("Cleaning Cost"), "Amount": num_prop(40), "Date": date_prop("2026-03-20"), "Tax Deductible": checkbox_prop(True)})
    add_row(transactions_id, {"Description": title_prop("New bedding set"), "Listing": relation_prop(l2["id"]), "Type": select_prop("Expense"), "Category": select_prop("Supplies"), "Amount": num_prop(85), "Date": date_prop("2026-03-15"), "Tax Deductible": checkbox_prop(True)})
    add_row(transactions_id, {"Description": title_prop("Lockbox battery replacement"), "Listing": relation_prop(l3["id"]), "Type": select_prop("Expense"), "Category": select_prop("Maintenance"), "Amount": num_prop(12), "Date": date_prop("2026-03-18"), "Tax Deductible": checkbox_prop(True)})
    add_row(transactions_id, {"Description": title_prop("Airbnb service fee"), "Listing": relation_prop(l1["id"]), "Type": select_prop("Expense"), "Category": select_prop("Platform Fee"), "Amount": num_prop(45), "Date": date_prop("2026-03-21")})
    add_row(transactions_id, {"Description": title_prop("Direct booking - cabin deposit"), "Listing": relation_prop(l4["id"]), "Type": select_prop("Income"), "Category": select_prop("Direct Payment"), "Amount": num_prop(500), "Date": date_prop("2026-03-19")})

    # --- Sample Data: Supplies ---
    add_row(supplies_id, {"Item Name": title_prop("Shampoo bottles (travel size)"), "Listing": relation_prop(l1["id"]), "Category": select_prop("Toiletries"), "Current Stock": num_prop(8), "Reorder Threshold": num_prop(5), "Unit Cost": num_prop(2.50)})
    add_row(supplies_id, {"Item Name": title_prop("Bath towel sets"), "Listing": relation_prop(l2["id"]), "Category": select_prop("Linens"), "Current Stock": num_prop(3), "Reorder Threshold": num_prop(4), "Unit Cost": num_prop(15)})
    add_row(supplies_id, {"Item Name": title_prop("Coffee pods (variety)"), "Listing": relation_prop(l3["id"]), "Category": select_prop("Kitchen"), "Current Stock": num_prop(12), "Reorder Threshold": num_prop(10), "Unit Cost": num_prop(0.80)})
    add_row(supplies_id, {"Item Name": title_prop("Toilet paper (12-pack)"), "Listing": relation_prop(l1["id"]), "Category": select_prop("Toiletries"), "Current Stock": num_prop(2), "Reorder Threshold": num_prop(3), "Unit Cost": num_prop(12)})

    # --- Sample Data: Pricing Calendar ---
    add_row(pricing_id, {"Period Name": title_prop("Spring Shoulder Season"), "Listing": relation_prop(l1["id"]), "Season": select_prop("Mid"), "Start Date": date_prop("2026-03-01"), "End Date": date_prop("2026-05-31"), "Nightly Rate": num_prop(110), "Minimum Stay": num_prop(2), "Competitor Rate": num_prop(115)})
    add_row(pricing_id, {"Period Name": title_prop("Summer Peak"), "Listing": relation_prop(l2["id"]), "Season": select_prop("Peak"), "Start Date": date_prop("2026-06-01"), "End Date": date_prop("2026-08-31"), "Nightly Rate": num_prop(250), "Minimum Stay": num_prop(3), "Competitor Rate": num_prop(230)})
    add_row(pricing_id, {"Period Name": title_prop("Airport Hotel Alternative"), "Listing": relation_prop(l3["id"]), "Season": select_prop("Low"), "Start Date": date_prop("2026-01-01"), "End Date": date_prop("2026-12-31"), "Nightly Rate": num_prop(75), "Minimum Stay": num_prop(1), "Competitor Rate": num_prop(80)})
    add_row(pricing_id, {"Period Name": title_prop("Holiday Premium"), "Listing": relation_prop(l4["id"]), "Season": select_prop("Holiday"), "Start Date": date_prop("2026-12-20"), "End Date": date_prop("2027-01-05"), "Nightly Rate": num_prop(350), "Minimum Stay": num_prop(5), "Competitor Rate": num_prop(320)})

    # --- Dashboard with Communication Templates ---
    comm_blocks = [
        heading2("Guest Communication Templates"),
        toggle("Booking Confirmation", [
            paragraph("Hi [Guest Name]! Thanks for booking [Listing Name]. We're excited to host you from [Check-in] to [Check-out]. I'll send detailed check-in instructions 2 days before your arrival. In the meantime, let me know if you have any questions!"),
        ]),
        toggle("Check-in Instructions (2 Days Before)", [
            paragraph("Hi [Guest Name]! Your stay is almost here. Here's everything you need:\n- Address: [Address]\n- Check-in time: [Time]\n- Lockbox/Smart Lock code: [Code]\n- WiFi: [Network] / Password: [Password]\n- Parking: [Instructions]\n- House manual: [Link/location]\nLet me know if you need anything before arrival!"),
        ]),
        toggle("Welcome Message (Check-in Day)", [
            paragraph("Welcome, [Guest Name]! I hope you arrived safely. Everything should be ready for you. A few quick tips:\n- Thermostat is set to [temp] — feel free to adjust\n- Extra towels/blankets are in [location]\n- Trash/recycling goes out on [day]\nEnjoy your stay! I'm just a message away if you need anything."),
        ]),
        toggle("Mid-Stay Check-in", [
            paragraph("Hi [Guest Name]! Just checking in — is everything going well? Do you need anything? Happy to help with local restaurant recommendations or activity suggestions. Enjoy the rest of your stay!"),
        ]),
        toggle("Checkout Reminder", [
            paragraph("Hi [Guest Name]! Just a friendly reminder that checkout is tomorrow at [Time]. Before you go:\n- Please start the dishwasher if you used dishes\n- Leave used towels in the bathtub\n- Lock the door behind you\nThank you for being a wonderful guest! If you enjoyed your stay, I'd truly appreciate a review. Safe travels!"),
        ]),
        toggle("Review Request", [
            paragraph("Hi [Guest Name]! Thanks again for staying at [Listing Name]. I hope you had a great time! If you have a moment, I'd really appreciate a review — it helps future guests and means a lot to me as a host. Thanks and hope to host you again!"),
        ]),
        divider(),
        heading2("Review Response Templates"),
        toggle("5-Star Responses", [
            numbered("Thank you so much, [Guest]! You were an absolute dream guest. The place was spotless when you left. You're welcome back anytime!"),
            numbered("What a kind review, [Guest]! We loved hosting you and hope to see you again on your next visit to [City]."),
            numbered("[Guest], thank you for the wonderful words! Guests like you are what make hosting so rewarding. Our door is always open."),
        ]),
        toggle("4-Star Responses", [
            numbered("Thanks for the great review, [Guest]! We appreciate the feedback and are always looking for ways to improve. Hope to host you again!"),
            numbered("Thank you, [Guest]! We're glad you enjoyed most of your stay. If there's anything we could do better, we'd love to hear."),
        ]),
        toggle("Negative Review Recovery", [
            numbered("Thank you for your feedback, [Guest]. I'm sorry your experience didn't meet expectations. I've [specific action taken] to prevent this in the future."),
            numbered("[Guest], I appreciate you sharing your experience. This isn't the standard we aim for, and I take full responsibility."),
        ]),
        divider(),
        heading2("Quick Links"),
        bulleted("Listings — All properties with rates and status"),
        bulleted("Bookings — Guest calendar and communication tracker"),
        bulleted("Cleanings — Schedule and track turnovers"),
        bulleted("Revenue — Income, expenses, and P&L by property"),
        bulleted("Maintenance — Issue tracking and resolution"),
        bulleted("Supplies — Inventory with reorder alerts"),
        bulleted("Pricing Calendar — Seasonal rate strategy"),
    ]
    append_blocks(pid, comm_blocks)

    log.info("=== Airbnb Host Management Hub DONE ===")
    return page


# ============================================================================
# TEMPLATE 8: AI Side Hustle Starter Kit ($19) — 7 DB
# ============================================================================

def build_ai_side_hustle_starter_kit(parent: dict) -> dict:
    log.info("=== AI Side Hustle Starter Kit ===")
    page = create_page(parent, "AI Side Hustle Starter Kit", "🤖", [
        heading1("AI Side Hustle Starter Kit"),
        paragraph("From Zero to First Client with AI — your complete freelance system with 50 AI prompts."),
        callout("Start with the prompt library, set up your service packages, then land your first client!", "🚀"),
        divider(),
    ])
    pid = page["id"]

    # --- DB1: AI Prompts ---
    prompts_db = create_database(pid, "AI Prompts", "💡", {
        "Prompt Name": p_title(),
        "Category": p_select("Blog Writing", "Social Media", "Email", "Ad Copy", "SEO", "Client Comms", "Ideation"),
        "Prompt Text": p_rt(),
        "AI Tool": p_mselect("ChatGPT", "Claude", "Gemini", "Any"),
        "Difficulty": p_select("Beginner", "Intermediate", "Advanced"),
        "Output Type": p_select("Long-form", "Short-form", "List", "Template"),
        "Tips": p_rt(),
        "Favorite": p_checkbox(),
    })
    prompts_id = prompts_db["id"]

    # --- DB2: Clients ---
    clients_db = create_database(pid, "Clients", "👤", {
        "Client Name": p_title(),
        "Status": p_select("Lead", "Contacted", "Proposal Sent", "Active", "Completed", "Lost"),
        "Service": p_select("Blog Writing", "Social Media", "Email Marketing", "Ad Copy", "SEO", "Other"),
        "Contact": p_email(),
        "Source": p_select("LinkedIn", "Twitter/X", "Upwork", "Fiverr", "Referral", "Cold Outreach"),
        "Deal Value": p_number("dollar"),
        "Next Action": p_rt(),
        "Follow-up Date": p_date(),
        "Notes": p_rt(),
    })
    clients_id = clients_db["id"]

    # --- DB3: Projects ---
    projects_db = create_database(pid, "Projects", "📁", {
        "Project Name": p_title(),
        "Service Type": p_select("Blog Writing", "Social Media", "Email Marketing", "Ad Copy", "SEO", "Other"),
        "Status": p_select("Not Started", "In Progress", "Review", "Delivered", "Paid"),
        "Deadline": p_date(),
        "Fee": p_number("dollar"),
        "Paid": p_checkbox(),
        "Deliverables": p_rt(),
    })
    projects_id = projects_db["id"]

    # --- DB4: Income ---
    income_db = create_database(pid, "Income", "💰", {
        "Description": p_title(),
        "Amount": p_number("dollar"),
        "Date": p_date(),
        "Source": p_select("Freelance", "Product Sales", "Affiliate", "Other"),
        "Payment Method": p_select("PayPal", "Stripe", "Bank Transfer", "Crypto", "Other"),
        "Status": p_select("Pending", "Received", "Overdue"),
    })
    income_id = income_db["id"]

    # --- DB5: AI Tools ---
    tools_db = create_database(pid, "AI Tools", "🛠️", {
        "Tool Name": p_title(),
        "Category": p_select("Text", "Image", "Video", "Audio", "Code", "Multi-modal"),
        "Pricing": p_rt(),
        "Free Tier": p_checkbox(),
        "Best For": p_mselect("Blog Writing", "Social Media", "Email", "Ad Copy", "SEO", "Image Gen", "Code"),
        "URL": p_url(),
        "Rating": p_select("1", "2", "3", "4", "5"),
        "Notes": p_rt(),
    })
    tools_id = tools_db["id"]

    # --- DB6: Weekly Planner ---
    planner_db = create_database(pid, "Weekly Planner", "📆", {
        "Task": p_title(),
        "Day": p_select("Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"),
        "Time Block": p_select("Morning", "Afternoon", "Evening"),
        "Category": p_select("Client Work", "Prospecting", "Content Creation", "Admin", "Learning"),
        "Duration": p_number(),
        "Completed": p_checkbox(),
    })
    planner_id = planner_db["id"]

    # --- DB7: Service Packages ---
    packages_db = create_database(pid, "Service Packages", "📦", {
        "Package Name": p_title(),
        "Service Type": p_select("Blog Writing", "Social Media", "Email Marketing", "Ad Copy", "SEO", "Content Strategy"),
        "Pricing Model": p_select("Per Project", "Hourly", "Monthly Retainer"),
        "Price Range": p_rt(),
        "Deliverables": p_rt(),
        "Time Estimate": p_rt(),
        "Description": p_rt(),
    })
    packages_id = packages_db["id"]

    # --- Relations ---
    _api("patch", f"/databases/{clients_id}", {"properties": {"Projects": p_relation(projects_id)}})
    _api("patch", f"/databases/{projects_id}", {"properties": {
        "Client": p_relation(clients_id),
        "AI Prompts Used": p_relation(prompts_id),
        "Income": p_relation(income_id),
    }})
    _api("patch", f"/databases/{income_id}", {"properties": {
        "Client": p_relation(clients_id),
        "Project": p_relation(projects_id),
    }})
    _api("patch", f"/databases/{planner_id}", {"properties": {"AI Prompt": p_relation(prompts_id)}})
    _api("patch", f"/databases/{packages_id}", {"properties": {"AI Prompts": p_relation(prompts_id)}})

    # --- Sample Data: AI Prompts (10 key prompts from the 50) ---
    prompt_samples = [
        ("SEO Blog Post Generator", "Blog Writing", 'Write a 1,500-word blog post about [TOPIC] targeting the keyword [KEYWORD]. Include an engaging introduction with a hook, 5-7 H2 subheadings, practical examples, and a conclusion with a call to action. Tone: conversational but authoritative.', "Long-form", "Beginner"),
        ("Twitter/X Thread Creator", "Social Media", 'Write a 7-tweet thread about [TOPIC]. Tweet 1: bold hook with a number or contrarian take. Tweets 2-6: one key insight each with a specific example. Tweet 7: summary + CTA. Use line breaks for readability.', "Short-form", "Beginner"),
        ("Cold Outreach Email", "Email", 'Write a cold outreach email to [TARGET ROLE] at [COMPANY TYPE] offering [SERVICE]. Keep it under 100 words. Personalization placeholder: [SPECIFIC THING ABOUT THEIR BUSINESS]. Clear CTA: book a 15-min call.', "Template", "Intermediate"),
        ("Facebook/Instagram Ad Copy", "Ad Copy", 'Write 3 Facebook ad variations for [PRODUCT/SERVICE]. For each: Primary text (125 words, hook + problem + solution + CTA), Headline (5 words), Description (1 sentence). Target: [AUDIENCE]. Goal: [CLICK/SIGN UP/BUY].', "Short-form", "Intermediate"),
        ("Keyword Cluster Generator", "SEO", 'Generate a keyword cluster for the topic [MAIN TOPIC]. Include: 1 pillar keyword, 5 cluster keywords, 10 long-tail keywords, estimated search intent for each, and suggested content type.', "List", "Advanced"),
        ("LinkedIn Post Generator", "Social Media", 'Write a LinkedIn post about [TOPIC/EXPERIENCE]. Start with a one-line hook. Tell a brief story. End with 3 actionable takeaways and a question to drive comments. 200-300 words.', "Short-form", "Beginner"),
        ("Welcome Email Sequence", "Email", 'Write a 3-email welcome sequence for new subscribers of [BUSINESS]. Email 1: Warm welcome + deliver the lead magnet. Email 2 (Day 2): Your story + biggest insight. Email 3 (Day 4): Introduce your paid offer + social proof.', "Long-form", "Intermediate"),
        ("Landing Page Copy", "Ad Copy", 'Write landing page copy for [PRODUCT/SERVICE]. Include: Hero headline + subheadline, 3 pain points, solution introduction, 6 bullet benefits, 2 testimonial placeholders, pricing section, FAQ (4 questions), final CTA.', "Long-form", "Advanced"),
        ("Content Brief Creator", "SEO", 'Create a comprehensive content brief for an article about [TOPIC] targeting [KEYWORD]. Include: target word count, search intent, outline, 5 competitor URLs, key points to cover, internal links, and CTA.', "Template", "Advanced"),
        ("Side Hustle Idea Generator", "Ideation", 'Generate 10 AI-powered side hustle ideas for someone with skills in [SKILLS]. For each: name, description, target market, revenue model, startup cost, monthly income potential, and which AI tools to use.', "List", "Beginner"),
    ]
    prompt_ids = {}
    for name, cat, text, output, diff in prompt_samples:
        r = add_row(prompts_id, {
            "Prompt Name": title_prop(name),
            "Category": select_prop(cat),
            "Prompt Text": rt_prop(text),
            "AI Tool": mselect_prop("ChatGPT", "Claude"),
            "Difficulty": select_prop(diff),
            "Output Type": select_prop(output),
            "Favorite": checkbox_prop(diff == "Beginner"),
        })
        prompt_ids[name] = r["id"]

    # --- Sample Data: Clients ---
    c1 = add_row(clients_id, {"Client Name": title_prop("TechStartup Co."), "Status": select_prop("Active"), "Service": select_prop("Blog Writing"), "Deal Value": num_prop(500), "Source": select_prop("LinkedIn"), "Follow-up Date": date_prop(_d(3))})
    c2 = add_row(clients_id, {"Client Name": title_prop("Sarah's Bakery"), "Status": select_prop("Proposal Sent"), "Service": select_prop("Social Media"), "Deal Value": num_prop(300), "Source": select_prop("Referral"), "Follow-up Date": date_prop(_d(5))})
    c3 = add_row(clients_id, {"Client Name": title_prop("DigitalNomad Blog"), "Status": select_prop("Lead"), "Service": select_prop("SEO"), "Deal Value": num_prop(400), "Source": select_prop("Twitter/X"), "Follow-up Date": date_prop(_d(7))})

    # --- Sample Data: Projects ---
    p1 = add_row(projects_id, {"Project Name": title_prop("Monthly Blog Package - TechStartup Co."), "Client": relation_prop(c1["id"]), "Service Type": select_prop("Blog Writing"), "Status": select_prop("In Progress"), "Fee": num_prop(500), "Deadline": date_prop(_d(7)), "Paid": checkbox_prop(False)})
    p2 = add_row(projects_id, {"Project Name": title_prop("Instagram Content Calendar - Sarah's Bakery"), "Client": relation_prop(c2["id"]), "Service Type": select_prop("Social Media"), "Status": select_prop("Not Started"), "Fee": num_prop(300), "Deadline": date_prop(_d(30)), "Paid": checkbox_prop(False)})

    # --- Sample Data: Income ---
    add_row(income_id, {"Description": title_prop("Blog Package - March"), "Amount": num_prop(500), "Date": date_prop("2026-03-15"), "Source": select_prop("Freelance"), "Status": select_prop("Received"), "Client": relation_prop(c1["id"]), "Project": relation_prop(p1["id"]), "Payment Method": select_prop("PayPal")})
    add_row(income_id, {"Description": title_prop("Social Media Audit"), "Amount": num_prop(150), "Date": date_prop("2026-03-10"), "Source": select_prop("Freelance"), "Status": select_prop("Received"), "Payment Method": select_prop("Stripe")})

    # --- Sample Data: AI Tools ---
    tools_data = [
        ("ChatGPT", "Text", "Free + $20/mo Plus", True, ["Blog Writing", "Email", "Ad Copy"], "https://chat.openai.com", "5"),
        ("Claude", "Text", "Free + $20/mo Pro", True, ["Blog Writing", "SEO", "Code"], "https://claude.ai", "5"),
        ("Midjourney", "Image", "$10/mo Basic", False, ["Image Gen"], "https://midjourney.com", "4"),
        ("Canva AI", "Image", "Free + $13/mo Pro", True, ["Social Media", "Image Gen"], "https://canva.com", "4"),
        ("Jasper", "Text", "$49/mo Creator", False, ["Ad Copy", "Email"], "https://jasper.ai", "3"),
    ]
    for name, cat, pricing, free, best_for, url, rating in tools_data:
        add_row(tools_id, {
            "Tool Name": title_prop(name),
            "Category": select_prop(cat),
            "Pricing": rt_prop(pricing),
            "Free Tier": checkbox_prop(free),
            "Best For": mselect_prop(*best_for),
            "URL": url_prop(url),
            "Rating": select_prop(rating),
        })

    # --- Sample Data: Service Packages ---
    add_row(packages_id, {"Package Name": title_prop("Blog Content Package"), "Service Type": select_prop("Blog Writing"), "Pricing Model": select_prop("Per Project"), "Price Range": rt_prop("$300-600/month (4 posts)"), "Deliverables": rt_prop("4 SEO-optimized blog posts (1,500+ words each), keyword research, meta tags"), "Time Estimate": rt_prop("8-10 hrs/month")})
    add_row(packages_id, {"Package Name": title_prop("Social Media Manager"), "Service Type": select_prop("Social Media"), "Pricing Model": select_prop("Monthly Retainer"), "Price Range": rt_prop("$400-800/month"), "Deliverables": rt_prop("30 posts/month across 2 platforms, content calendar, hashtag strategy, monthly report"), "Time Estimate": rt_prop("10-15 hrs/month")})
    add_row(packages_id, {"Package Name": title_prop("Email Sequence Setup"), "Service Type": select_prop("Email Marketing"), "Pricing Model": select_prop("Per Project"), "Price Range": rt_prop("$200-400"), "Deliverables": rt_prop("5-email welcome sequence, subject lines, A/B variants, setup in client's ESP"), "Time Estimate": rt_prop("4-6 hrs")})

    # --- Dashboard ---
    append_blocks(pid, [
        heading2("Sales Pipeline"),
        paragraph("Track leads from first contact to closed deal."),
        divider(),
        heading2("Income Tracker"),
        paragraph("Log every payment and track monthly revenue."),
        divider(),
        heading2("Quick Links"),
        bulleted("AI Prompts — 50 ready-to-use prompts by category"),
        bulleted("Clients — CRM with sales pipeline"),
        bulleted("Projects — Track deliverables and deadlines"),
        bulleted("Income — Revenue tracking by source"),
        bulleted("AI Tools — Compare and choose the right tools"),
        bulleted("Weekly Planner — Time-block your week"),
        bulleted("Service Packages — Pre-built offerings for clients"),
        divider(),
        toggle("Getting Started Guide", [
            numbered("Browse the AI Prompts library and favorite your top 10"),
            numbered("Set up your Service Packages with your pricing"),
            numbered("Add your first lead to the Clients board"),
            numbered("Use the Weekly Planner to block time for prospecting"),
            numbered("Land your first client and create a Project"),
            numbered("Log income and track your growth!"),
        ]),
    ])

    log.info("=== AI Side Hustle Starter Kit DONE ===")
    return page


# ============================================================================
# MAIN
# ============================================================================

def main():
    parser = argparse.ArgumentParser(description="Create 8 new Notion templates for Gumroad")
    parser.add_argument("--parent-page-id", required=True, help="Parent page ID in Notion")
    parser.add_argument("--template", help="Build only a specific template (partial name match)")
    args = parser.parse_args()

    if not NOTION_TOKEN:
        print("ERROR: Set NOTION_TOKEN environment variable first.")
        sys.exit(1)

    parent = {"type": "page_id", "page_id": args.parent_page_id}

    builders = [
        ("Startup Launch Checklist", build_startup_launch_checklist),
        ("Wedding Planning Hub", build_wedding_planning_hub),
        ("Property Investment Tracker", build_property_investment_tracker),
        ("Travel Planner & Journal", build_travel_planner_journal),
        ("Habit Tracker & Goal System", build_habit_tracker_goal_system),
        ("Personal Finance Dashboard", build_personal_finance_dashboard),
        ("Airbnb Host Management Hub", build_airbnb_host_management_hub),
        ("AI Side Hustle Starter Kit", build_ai_side_hustle_starter_kit),
    ]

    if args.template:
        builders = [(n, b) for n, b in builders if args.template.lower() in n.lower()]
        if not builders:
            print(f"No template matching '{args.template}'. Available:")
            for n, _ in [
                ("Startup Launch Checklist", None),
                ("Wedding Planning Hub", None),
                ("Property Investment Tracker", None),
                ("Travel Planner & Journal", None),
                ("Habit Tracker & Goal System", None),
                ("Personal Finance Dashboard", None),
                ("Airbnb Host Management Hub", None),
                ("AI Side Hustle Starter Kit", None),
            ]:
                print(f"  - {n}")
            sys.exit(1)

    log.info(f"Building {len(builders)} template(s)...")
    for name, builder in builders:
        try:
            builder(parent)
        except Exception as e:
            log.error(f"FAILED: {name} — {e}")
            continue

    log.info("All done!")


if __name__ == "__main__":
    main()
