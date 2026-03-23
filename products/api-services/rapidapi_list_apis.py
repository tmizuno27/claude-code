#!/usr/bin/env python3
"""
RapidAPI Listing Automation Script (APIs 1-24)
================================================
Updates all 24 APIs on RapidAPI using the RapidAPI Platform API.

Usage:
    python rapidapi_list_apis.py --dry-run           # Preview what would be listed
    python rapidapi_list_apis.py                     # Actually update listings
    python rapidapi_list_apis.py --api-num 11        # Update a single API
    python rapidapi_list_apis.py --manual            # Print step-by-step manual instructions

Authentication:
    Set RAPIDAPI_KEY environment variable, or the script will prompt for it.
    The key is your RapidAPI Provider Dashboard API key (not a consumer key).

RapidAPI Provider API docs:
    https://docs.rapidapi.com/docs/creating-updating-apis
    Base URL: https://rapidapi.com/developer/api/
"""

import argparse
import json
import os
import sys
import time
import glob
from pathlib import Path

try:
    import requests
except ImportError:
    print("ERROR: 'requests' library not found. Run: pip install requests")
    sys.exit(1)

# ── Config ────────────────────────────────────────────────────────────────────

BASE_DIR = Path(__file__).parent
APIS_BASE_URL = "https://rapidapi.com/developer/api/"
BASE_DOMAIN = "t-mizuno27.workers.dev"

# RapidAPI Platform API endpoint (GraphQL)
RAPIDAPI_GRAPHQL_URL = "https://graphql.rapidapi.com/"

# Standard pricing tiers (from rapidapi-business.md)
STANDARD_PRICING = [
    {
        "name": "BASIC",
        "price": 0.0,
        "requests_per_month": 100,
        "requests_per_second": 1,
    },
    {
        "name": "PRO",
        "price": 9.99,
        "requests_per_month": 10_000,
        "requests_per_second": 5,
    },
    {
        "name": "ULTRA",
        "price": 24.99,
        "requests_per_month": 50_000,
        "requests_per_second": 10,
    },
    {
        "name": "MEGA",
        "price": 49.99,
        "requests_per_month": 500_000,
        "requests_per_second": 20,
    },
]

# Map API number → subdomain (matches healthcheck.py + rapidapi-stats.json)
API_SUBDOMAINS = {
    1: "qr-code-api",
    2: "email-validation-api",
    3: "link-preview-api",
    4: "screenshot-api",
    5: "text-analysis-api",
    6: "ip-geolocation-api",
    7: "url-shortener-api",
    8: "json-formatter-api",
    9: "hash-encoding-api",
    10: "currency-exchange-api",
    11: "ai-text-api",
    12: "social-video-api",
    13: "crypto-data-api",
    14: "seo-analyzer-api",
    15: "weather-api",
    16: "whois-domain-api",
    17: "news-aggregator-api",
    18: "ai-translate-api",
    19: "trends-api",
    20: "company-data-api",
    21: "wp-internal-link-api",
    22: "pdf-generator-api",
    23: "placeholder-image-api",
    24: "markdown-converter-api",
}


# ── Helpers ───────────────────────────────────────────────────────────────────

def load_api_data(api_num: int) -> dict:
    """Load rapidapi-listing.json and openapi.json for a given API number."""
    pattern = str(BASE_DIR / f"{api_num:02d}-*")
    matches = glob.glob(pattern)
    if not matches:
        raise FileNotFoundError(f"No directory found matching: {pattern}")

    api_dir = Path(matches[0])
    listing_path = api_dir / "rapidapi-listing.json"
    openapi_path = api_dir / "openapi.json"

    if not listing_path.exists():
        raise FileNotFoundError(f"rapidapi-listing.json not found in {api_dir}")

    with open(listing_path, encoding="utf-8") as f:
        listing = json.load(f)

    openapi = {}
    if openapi_path.exists():
        with open(openapi_path, encoding="utf-8") as f:
            openapi = json.load(f)

    return {
        "num": api_num,
        "dir": str(api_dir),
        "listing": listing,
        "openapi": openapi,
        "subdomain": API_SUBDOMAINS.get(api_num, listing.get("slug", "")),
    }


def build_base_url(subdomain: str) -> str:
    return f"https://{subdomain}.{BASE_DOMAIN}"


def build_listing_payload(data: dict) -> dict:
    """Build the payload dict for a RapidAPI listing creation."""
    listing = data["listing"]
    openapi = data["openapi"]
    subdomain = data["subdomain"]
    base_url = build_base_url(subdomain)

    # Merge description from openapi if listing has short one
    description = listing.get("description", "")
    long_description = listing.get("long_description", description)
    if not long_description and openapi:
        long_description = openapi.get("info", {}).get("description", description)

    # Tags (max 5 on RapidAPI)
    tags = listing.get("tags", [])[:5]

    # Category mapping to RapidAPI categories
    category_map = {
        "Text": "Text Analysis",
        "Text_Analysis": "Text Analysis",
        "Video_Images": "Video_Images",
        "Finance": "Finance",
        "Data": "Data",
        "Weather": "Weather",
        "Tools": "Tools",
        "Communication": "Communication",
        "Translation": "Translation",
        "News_Media": "News_Media",
        "Business": "Business",
        "Media": "Media",
        "Social": "Social",
    }
    raw_category = listing.get("category", "Tools")
    category = category_map.get(raw_category, raw_category)

    return {
        "name": listing.get("name", f"API {data['num']}"),
        "description": description,
        "longDescription": long_description,
        "category": category,
        "tags": tags,
        "baseUrl": base_url,
        "websiteUrl": listing.get("website", base_url),
        "termsOfServiceUrl": "",
        "thumbnail": "",
    }


def get_api_key(prompt_if_missing: bool = True) -> str | None:
    """Return the RapidAPI provider key from env, or prompt the user."""
    key = os.environ.get("RAPIDAPI_KEY", "").strip()
    if key:
        return key
    if prompt_if_missing:
        print("\nRAPIDAPI_KEY environment variable not set.")
        print("Find your key at: https://rapidapi.com/developer/dashboard → API Keys")
        print("(This is your PROVIDER key, not a consumer key)\n")
        try:
            key = input("Enter your RapidAPI Provider API key (or press Enter to skip): ").strip()
        except (KeyboardInterrupt, EOFError):
            return None
        return key if key else None
    return None


# ── RapidAPI Platform API calls ───────────────────────────────────────────────

def rapidapi_create_api(payload: dict, api_key: str) -> dict:
    """
    Create a new API listing on RapidAPI via the Platform API.
    Returns {"success": bool, "data": ..., "error": str|None}
    """
    headers = {
        "x-rapidapi-key": api_key,
        "x-rapidapi-host": "rapidapi.com",
        "Content-Type": "application/json",
    }

    # RapidAPI uses a REST endpoint for provider API creation
    url = "https://rapidapi.com/api/provider/hub/api"

    body = {
        "data": {
            "name": payload["name"],
            "description": payload["description"],
            "longDescription": payload.get("longDescription", payload["description"]),
            "category": payload["category"],
            "tags": payload.get("tags", []),
            "thumbnail": payload.get("thumbnail", ""),
            "websiteUrl": payload.get("websiteUrl", ""),
            "termsOfServiceUrl": payload.get("termsOfServiceUrl", ""),
        }
    }

    try:
        resp = requests.post(url, json=body, headers=headers, timeout=30)
        if resp.status_code in (200, 201):
            return {"success": True, "data": resp.json(), "error": None}
        else:
            return {
                "success": False,
                "data": None,
                "error": f"HTTP {resp.status_code}: {resp.text[:300]}",
            }
    except requests.exceptions.Timeout:
        return {"success": False, "data": None, "error": "Request timed out"}
    except Exception as e:
        return {"success": False, "data": None, "error": str(e)}


def rapidapi_upload_openapi(api_id: str, openapi_spec: dict, api_key: str) -> dict:
    """Upload an OpenAPI spec to an existing RapidAPI listing."""
    url = f"https://rapidapi.com/api/provider/hub/api/{api_id}/openapi"
    headers = {
        "x-rapidapi-key": api_key,
        "x-rapidapi-host": "rapidapi.com",
        "Content-Type": "application/json",
    }
    try:
        resp = requests.put(url, json=openapi_spec, headers=headers, timeout=30)
        if resp.status_code in (200, 201, 204):
            return {"success": True, "data": resp.json() if resp.content else {}, "error": None}
        else:
            return {
                "success": False,
                "data": None,
                "error": f"HTTP {resp.status_code}: {resp.text[:300]}",
            }
    except Exception as e:
        return {"success": False, "data": None, "error": str(e)}


# ── Manual instructions ────────────────────────────────────────────────────────

MANUAL_STEPS_TEMPLATE = """
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
API {num:02d}: {name}
Base URL: {base_url}
Category: {category}
Tags: {tags}
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
STEPS:
  1. Go to: https://rapidapi.com/provider/dashboard
  2. Click [+ New API]
  3. Enter API name: {name}
  4. Select category: {category}
  5. Enter base URL: {base_url}
  6. Click [Create API]
  7. In the API editor, go to [Definition] tab
  8. Upload openapi.json from: {openapi_path}
  9. Go to [Pricing] tab and add:
     - BASIC: Free / 100 req/month / 1 req/sec
     - PRO: $9.99/mo / 10,000 req/month / 5 req/sec
     - ULTRA: $24.99/mo / 50,000 req/month / 10 req/sec
     - MEGA: $49.99/mo / 500,000 req/month / 20 req/sec
 10. Go to [Settings] tab:
     - Description: {description}
     - Tags: {tags_csv}
 11. Click [Publish] to make it live

SHORT DESCRIPTION:
{description}

LONG DESCRIPTION:
{long_description}
"""


def print_manual_instructions(apis_data: list[dict]):
    """Print manual step-by-step listing instructions for all APIs."""
    print("\n" + "=" * 60)
    print("MANUAL LISTING INSTRUCTIONS FOR RAPIDAPI APIS 1-24")

    print("=" * 60)
    print("\nPrerequisite: Log in at https://rapidapi.com/provider/dashboard\n")

    for data in apis_data:
        listing = data["listing"]
        payload = build_listing_payload(data)
        openapi_path = str(Path(data["dir"]) / "openapi.json")

        print(MANUAL_STEPS_TEMPLATE.format(
            num=data["num"],
            name=payload["name"],
            base_url=build_base_url(data["subdomain"]),
            category=payload["category"],
            tags=payload["tags"],
            tags_csv=", ".join(payload["tags"]),
            openapi_path=openapi_path,
            description=payload["description"],
            long_description=payload.get("longDescription", payload["description"]),
        ))


# ── Dry run ────────────────────────────────────────────────────────────────────

def dry_run(apis_data: list[dict]):
    """Show what would be submitted to RapidAPI without actually calling the API."""
    print("\n" + "=" * 60)
    print("DRY RUN - APIs that would be listed on RapidAPI")
    print("=" * 60)

    for data in apis_data:
        payload = build_listing_payload(data)
        base_url = build_base_url(data["subdomain"])

        print(f"\n[API {data['num']:02d}] {payload['name']}")
        print(f"  Directory : {data['dir']}")
        print(f"  Base URL  : {base_url}")
        print(f"  Category  : {payload['category']}")
        print(f"  Tags      : {', '.join(payload['tags'])}")
        print(f"  OpenAPI   : {'YES' if data['openapi'] else 'NOT FOUND'}")
        print(f"  Description (short): {payload['description'][:80]}...")
        print(f"  Pricing tiers: {len(STANDARD_PRICING)}")
        for tier in STANDARD_PRICING:
            print(f"    - {tier['name']}: ${tier['price']}/mo | "
                  f"{tier['requests_per_month']:,} req/mo | "
                  f"{tier['requests_per_second']} req/sec")

    print(f"\nTotal: {len(apis_data)} APIs would be listed.")
    print("\nTo execute for real: remove --dry-run flag")
    print("To get manual steps: add --manual flag")


# ── Main listing flow ──────────────────────────────────────────────────────────

def list_api(data: dict, api_key: str, verbose: bool = True) -> bool:
    """Create a single API listing on RapidAPI. Returns True on success."""
    payload = build_listing_payload(data)
    name = payload["name"]
    num = data["num"]

    if verbose:
        print(f"\n[{num:02d}] Creating listing: {name} ... ", end="", flush=True)

    result = rapidapi_create_api(payload, api_key)

    if result["success"]:
        api_id = result["data"].get("id") or result["data"].get("apiId", "")
        if verbose:
            print(f"OK (id={api_id})")

        # Upload OpenAPI spec if available
        if data["openapi"] and api_id:
            if verbose:
                print(f"     Uploading OpenAPI spec ... ", end="", flush=True)
            oa_result = rapidapi_upload_openapi(api_id, data["openapi"], api_key)
            if verbose:
                if oa_result["success"]:
                    print("OK")
                else:
                    print(f"FAILED: {oa_result['error']}")
        return True
    else:
        if verbose:
            print(f"FAILED")
            print(f"     Error: {result['error']}")
        return False


def run_listing(apis_data: list[dict], api_key: str):
    """List all APIs, with rate-limit-aware delays."""
    print(f"\nListing {len(apis_data)} APIs on RapidAPI...")
    print("(Rate limit: 1 request per 2 seconds)\n")

    success_count = 0
    fail_count = 0

    for i, data in enumerate(apis_data):
        ok = list_api(data, api_key)
        if ok:
            success_count += 1
        else:
            fail_count += 1

        # Polite delay between requests
        if i < len(apis_data) - 1:
            time.sleep(2)

    print(f"\n{'=' * 40}")
    print(f"Done: {success_count} succeeded, {fail_count} failed")
    print(f"{'=' * 40}")

    if fail_count > 0:
        print("\nNOTE: For failed APIs, use --manual to get step-by-step instructions.")
    else:
        print("\nAll APIs listed successfully!")
        print("Visit: https://rapidapi.com/provider/dashboard to verify.")


# ── CLI ────────────────────────────────────────────────────────────────────────

def parse_args():
    parser = argparse.ArgumentParser(
        description="Automate RapidAPI listing for APIs 1-24",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python rapidapi_list_apis.py --dry-run           # Preview listings
  python rapidapi_list_apis.py --manual            # Print manual steps
  python rapidapi_list_apis.py                     # Actually update all APIs
  python rapidapi_list_apis.py --api-num 15        # Update only API 15
  RAPIDAPI_KEY=xxx python rapidapi_list_apis.py    # Use key from env
        """,
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Show what would be listed without making API calls",
    )
    parser.add_argument(
        "--manual",
        action="store_true",
        help="Print step-by-step manual listing instructions",
    )
    parser.add_argument(
        "--api-num",
        type=int,
        choices=range(1, 25),
        metavar="N",
        help="Update only a single API (1-24)",
    )
    parser.add_argument(
        "--no-prompt",
        action="store_true",
        help="Do not prompt for API key if not set (exits instead)",
    )
    return parser.parse_args()


def main():
    args = parse_args()

    # Determine which APIs to process
    api_nums = [args.api_num] if args.api_num else list(range(1, 25))

    # Load API data
    apis_data = []
    for num in api_nums:
        try:
            data = load_api_data(num)
            apis_data.append(data)
        except FileNotFoundError as e:
            print(f"WARNING: Skipping API {num}: {e}", file=sys.stderr)

    if not apis_data:
        print("ERROR: No API data found. Check that the api-services/ directories exist.")
        sys.exit(1)

    print(f"Loaded {len(apis_data)} API definitions from: {BASE_DIR}")

    # Dispatch modes
    if args.dry_run:
        dry_run(apis_data)
        return

    if args.manual:
        print_manual_instructions(apis_data)
        return

    # Actual listing: need API key
    api_key = get_api_key(prompt_if_missing=not args.no_prompt)

    if not api_key:
        print("\nNo API key provided. Running in manual mode instead.\n")
        print_manual_instructions(apis_data)
        return

    run_listing(apis_data, api_key)


if __name__ == "__main__":
    main()
