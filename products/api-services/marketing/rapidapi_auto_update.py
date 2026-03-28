"""
RapidAPI Provider Dashboard 自動リスティング更新スクリプト

Usage:
    python rapidapi_auto_update.py                  # 通常実行（ブラウザ表示）
    python rapidapi_auto_update.py --headless       # ヘッドレス実行
    python rapidapi_auto_update.py --dry-run        # 保存せず確認のみ
    python rapidapi_auto_update.py --api 1          # 特定APIのみ（1-5）
"""

import argparse
import io
import json
import os
import re
import sys
import time

# Fix Windows console encoding
if sys.platform == "win32":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding="utf-8", errors="replace")
from dataclasses import dataclass, field
from pathlib import Path

from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeout

# --- Constants ---
SCRIPT_DIR = Path(__file__).parent
DATA_FILE = SCRIPT_DIR / "rapidapi-listing-copypaste.md"
SESSION_DIR = SCRIPT_DIR / ".rapidapi-session"
SCREENSHOT_DIR = SCRIPT_DIR / "screenshots"
PROVIDER_URL = "https://provider.rapidapi.com/"


@dataclass(frozen=True)
class ApiListing:
    """Immutable data for one API listing update."""
    name: str
    dashboard_url: str
    short_description: str
    long_description: str
    tags: list[str]
    category: str


def parse_listings(filepath: Path) -> list[ApiListing]:
    """Parse the markdown file to extract API listing data."""
    if not filepath.exists():
        print(f"[ERROR] Data file not found: {filepath}")
        sys.exit(1)

    text = filepath.read_text(encoding="utf-8")
    sections = re.split(r"^## \d+\.\s+", text, flags=re.MULTILINE)[1:]

    listings = []
    for section in sections:
        if section.strip().startswith("更新手順"):
            continue

        name_match = re.match(r"(.+?)(?:\n|$)", section)
        name = name_match.group(1).strip() if name_match else "Unknown"

        url_match = re.search(
            r"### ダッシュボードURL\s*\n(https://provider\.rapidapi\.com/hub-listing/api/[^\s]+)",
            section,
        )
        dashboard_url = url_match.group(1).strip() if url_match else ""

        short_desc = _extract_code_block(section, "Short Description")
        long_desc = _extract_code_block(section, "Long Description")
        tags_raw = _extract_code_block(section, "Tags")
        category = _extract_code_block(section, "Category")

        tag_list = [t.strip() for t in tags_raw.split(",") if t.strip()]

        listings.append(
            ApiListing(
                name=name,
                dashboard_url=dashboard_url,
                short_description=short_desc,
                long_description=long_desc,
                tags=tag_list,
                category=category,
            )
        )

    return listings


def _extract_code_block(text: str, heading: str) -> str:
    """Extract content from a fenced code block under a ### heading."""
    pattern = rf"### {re.escape(heading)}.*?\n```\n(.*?)\n```"
    match = re.search(pattern, text, re.DOTALL)
    return match.group(1).strip() if match else ""


def ensure_login(page, headless: bool) -> bool:
    """Navigate to provider dashboard and ensure logged in.
    Returns True if logged in, False if failed."""
    print("[INFO] Navigating to RapidAPI Provider Dashboard...")
    page.goto(PROVIDER_URL, wait_until="networkidle", timeout=30000)
    time.sleep(2)

    # Check if already logged in by looking for dashboard elements
    if _is_logged_in(page):
        print("[OK] Already logged in (session restored).")
        return True

    if headless:
        print("[ERROR] Not logged in and running in headless mode.")
        print("        Run once without --headless to log in manually.")
        return False

    print("[ACTION] Please log in manually in the browser window.")
    print("         Waiting up to 120 seconds...")

    for _ in range(120):
        time.sleep(1)
        if _is_logged_in(page):
            print("[OK] Login detected!")
            return True

    print("[ERROR] Login timeout (120s). Please try again.")
    return False


def _is_logged_in(page) -> bool:
    """Check if the user is logged in to the provider dashboard."""
    try:
        # Look for common dashboard elements that appear when logged in
        return (
            page.locator("text=My APIs").first.is_visible(timeout=3000)
            or page.locator("[data-testid='sidebar']").first.is_visible(timeout=1000)
            or "provider.rapidapi.com" in page.url
            and page.locator("nav").first.is_visible(timeout=1000)
        )
    except (PlaywrightTimeout, Exception):
        return False


def update_api_listing(page, listing: ApiListing, dry_run: bool) -> bool:
    """Update a single API's listing on the provider dashboard.
    Returns True on success, False on failure."""
    print(f"\n{'=' * 60}")
    print(f"[API] {listing.name}")
    print(f"[URL] {listing.dashboard_url}")
    print(f"{'=' * 60}")

    try:
        # Navigate to the API's hub listing page
        page.goto(listing.dashboard_url, wait_until="networkidle", timeout=30000)
        time.sleep(2)

        # Click "About" tab if present
        about_tab = page.locator("text=About").first
        if about_tab.is_visible(timeout=5000):
            about_tab.click()
            time.sleep(1)

        # --- Short Description ---
        _update_field(
            page,
            field_label="Short Description",
            value=listing.short_description,
            selector='textarea[name="shortDescription"], textarea[placeholder*="short description" i], input[name="shortDescription"]',
            dry_run=dry_run,
        )

        # --- Long Description ---
        _update_field(
            page,
            field_label="Long Description",
            value=listing.long_description,
            selector='textarea[name="longDescription"], textarea[placeholder*="description" i], [data-testid="long-description"] textarea, div[contenteditable="true"]',
            dry_run=dry_run,
            is_long=True,
        )

        # --- Category ---
        _update_category(page, listing.category, dry_run)

        # --- Tags ---
        _update_tags(page, listing.tags, dry_run)

        # --- Save ---
        if not dry_run:
            save_btn = page.locator('button:has-text("Save"), button[type="submit"]:has-text("Save")').first
            if save_btn.is_visible(timeout=5000):
                save_btn.click()
                print("[OK] Save clicked.")
                time.sleep(2)
            else:
                print("[WARN] Save button not found. Changes may not be saved.")
        else:
            print("[DRY-RUN] Skipping Save.")

        # Screenshot
        _take_screenshot(page, listing.name)

        return True

    except PlaywrightTimeout as e:
        print(f"[ERROR] Timeout updating {listing.name}: {e}")
        _take_screenshot(page, f"{listing.name}_ERROR")
        return False
    except Exception as e:
        print(f"[ERROR] Failed to update {listing.name}: {e}")
        _take_screenshot(page, f"{listing.name}_ERROR")
        return False


def _update_field(page, field_label: str, value: str, selector: str, dry_run: bool, is_long: bool = False) -> None:
    """Clear and fill a text field."""
    try:
        el = page.locator(selector).first
        if el.is_visible(timeout=5000):
            if dry_run:
                current = el.input_value() if el.evaluate("el => el.tagName") in ["INPUT", "TEXTAREA"] else el.text_content()
                print(f"[DRY-RUN] {field_label}: would update ({len(value)} chars)")
                return
            el.click()
            el.fill("")
            el.fill(value)
            print(f"[OK] {field_label} updated ({len(value)} chars).")
        else:
            # Try alternative: look for label then sibling input
            label_el = page.locator(f'label:has-text("{field_label}")').first
            if label_el.is_visible(timeout=3000):
                input_el = label_el.locator(".. >> textarea, .. >> input").first
                if input_el.is_visible(timeout=2000):
                    if not dry_run:
                        input_el.click()
                        input_el.fill("")
                        input_el.fill(value)
                        print(f"[OK] {field_label} updated via label ({len(value)} chars).")
                    else:
                        print(f"[DRY-RUN] {field_label}: found via label ({len(value)} chars)")
                    return
            print(f"[WARN] {field_label} field not found with selector: {selector}")
    except Exception as e:
        print(f"[WARN] {field_label} update failed: {e}")


def _update_category(page, category: str, dry_run: bool) -> None:
    """Update the category dropdown."""
    try:
        # Try to find and click category selector
        cat_selectors = [
            f'select[name="category"]',
            f'[data-testid="category-select"]',
            f'div:has-text("Category") >> select',
        ]
        for sel in cat_selectors:
            el = page.locator(sel).first
            if el.is_visible(timeout=2000):
                if dry_run:
                    print(f"[DRY-RUN] Category: would set to '{category}'")
                    return
                el.select_option(label=category)
                print(f"[OK] Category set to '{category}'.")
                return

        # Try clicking a dropdown-style category selector
        cat_label = page.locator('label:has-text("Category"), div:has-text("Category")').first
        if cat_label.is_visible(timeout=2000):
            cat_label.click()
            time.sleep(0.5)
            option = page.locator(f'li:has-text("{category}"), div[role="option"]:has-text("{category}")').first
            if option.is_visible(timeout=3000):
                if not dry_run:
                    option.click()
                    print(f"[OK] Category set to '{category}'.")
                else:
                    print(f"[DRY-RUN] Category: would set to '{category}'")
                return

        print(f"[WARN] Category selector not found.")
    except Exception as e:
        print(f"[WARN] Category update failed: {e}")


def _update_tags(page, tags: list[str], dry_run: bool) -> None:
    """Update tags field."""
    try:
        tag_input_selectors = [
            'input[name="tags"]',
            'input[placeholder*="tag" i]',
            '[data-testid="tags-input"] input',
        ]
        for sel in tag_input_selectors:
            el = page.locator(sel).first
            if el.is_visible(timeout=2000):
                if dry_run:
                    print(f"[DRY-RUN] Tags: would set {len(tags)} tags")
                    return

                # Remove existing tags (click all X buttons)
                remove_btns = page.locator('[data-testid="tag-remove"], .tag-remove, svg[data-icon="times"]')
                count = remove_btns.count()
                for i in range(count):
                    try:
                        remove_btns.first.click()
                        time.sleep(0.2)
                    except Exception:
                        break

                # Add new tags one by one
                for tag in tags:
                    el.fill(tag)
                    el.press("Enter")
                    time.sleep(0.3)

                print(f"[OK] Tags updated ({len(tags)} tags).")
                return

        # Fallback: try comma-separated input
        tag_area = page.locator('textarea[name="tags"]').first
        if tag_area.is_visible(timeout=2000):
            if not dry_run:
                tag_area.fill(", ".join(tags))
                print(f"[OK] Tags updated via textarea ({len(tags)} tags).")
            else:
                print(f"[DRY-RUN] Tags: would set {len(tags)} tags via textarea")
            return

        print("[WARN] Tags input not found.")
    except Exception as e:
        print(f"[WARN] Tags update failed: {e}")


def _take_screenshot(page, name: str) -> None:
    """Save a screenshot for verification."""
    SCREENSHOT_DIR.mkdir(parents=True, exist_ok=True)
    safe_name = re.sub(r"[^\w\-]", "_", name)
    filepath = SCREENSHOT_DIR / f"{safe_name}.png"
    page.screenshot(path=str(filepath), full_page=True)
    print(f"[SCREENSHOT] {filepath}")


def main():
    parser = argparse.ArgumentParser(description="RapidAPI listing auto-updater")
    parser.add_argument("--headless", action="store_true", help="Run browser in headless mode")
    parser.add_argument("--dry-run", action="store_true", help="Preview changes without saving")
    parser.add_argument("--api", type=int, choices=range(1, 6), help="Update specific API only (1-5)")
    args = parser.parse_args()

    # Parse listing data
    listings = parse_listings(DATA_FILE)
    print(f"[INFO] Parsed {len(listings)} API listings from {DATA_FILE.name}")

    if args.api:
        idx = args.api - 1
        if idx < len(listings):
            listings = [listings[idx]]
            print(f"[INFO] Targeting only: {listings[0].name}")
        else:
            print(f"[ERROR] API #{args.api} not found.")
            sys.exit(1)

    for i, listing in enumerate(listings, 1):
        print(f"\n  [{i}] {listing.name}")
        print(f"      URL: {listing.dashboard_url}")
        print(f"      Short: {listing.short_description[:60]}...")
        print(f"      Tags: {len(listing.tags)} tags")
        print(f"      Category: {listing.category}")

    if args.dry_run:
        print("\n[MODE] DRY-RUN — no changes will be saved.")

    # Launch browser
    SESSION_DIR.mkdir(parents=True, exist_ok=True)

    with sync_playwright() as p:
        browser = p.chromium.launch_persistent_context(
            user_data_dir=str(SESSION_DIR),
            headless=args.headless,
            viewport={"width": 1280, "height": 900},
            args=["--disable-blink-features=AutomationControlled"],
        )

        page = browser.pages[0] if browser.pages else browser.new_page()

        # Login
        if not ensure_login(page, args.headless):
            browser.close()
            sys.exit(1)

        # Update each API
        results = {}
        for listing in listings:
            success = update_api_listing(page, listing, args.dry_run)
            results[listing.name] = "OK" if success else "FAILED"

        browser.close()

    # Summary
    print(f"\n{'=' * 60}")
    print("RESULTS SUMMARY")
    print(f"{'=' * 60}")
    for name, status in results.items():
        icon = "+" if status == "OK" else "X"
        print(f"  [{icon}] {name}: {status}")

    failed = sum(1 for s in results.values() if s == "FAILED")
    if failed:
        print(f"\n[WARN] {failed}/{len(results)} API(s) failed.")
        sys.exit(1)
    else:
        print(f"\n[OK] All {len(results)} API(s) {'previewed' if args.dry_run else 'updated'} successfully.")


if __name__ == "__main__":
    main()
