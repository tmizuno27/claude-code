import sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
"""
Gumroad Sales Report
Fetches product list and sales data via Gumroad API.

Usage:
  python gumroad_sales_report.py              # Full report (JSON + summary)
  python gumroad_sales_report.py --summary    # Summary only
  python gumroad_sales_report.py --json       # JSON only (for PDCA pipeline)

API docs: https://app.gumroad.com/api
Access token: https://app.gumroad.com/settings/advanced#application-form
"""

import json
import os
import sys
from datetime import datetime, timezone, timedelta
from copy import deepcopy

import requests

BASE_DIR = os.path.dirname(os.path.dirname(__file__))
SECRETS_PATH = os.path.join(BASE_DIR, "config", "secrets.json")
OUTPUT_DIR = os.path.join(BASE_DIR, "outputs")
os.makedirs(OUTPUT_DIR, exist_ok=True)
REPORT_JSON_PATH = os.path.join(OUTPUT_DIR, "gumroad-sales-report.json")
LOG_DIR = os.path.join(os.path.dirname(os.path.dirname(BASE_DIR)), "logs")
os.makedirs(LOG_DIR, exist_ok=True)
LOG_PATH = os.path.join(LOG_DIR, "gumroad-sales-report.log")

GUMROAD_API_BASE = "https://api.gumroad.com/v2"

# Paraguay Time (UTC-3, no DST)
PYT = timezone(timedelta(hours=-3))


def log(message: str) -> None:
    timestamp = datetime.now(PYT).strftime("%Y-%m-%d %H:%M:%S PYT")
    line = f"[{timestamp}] {message}"
    print(line)
    try:
        with open(LOG_PATH, "a", encoding="utf-8") as f:
            f.write(line + "\n")
    except OSError:
        pass


def load_access_token() -> str | None:
    """Load Gumroad access token from secrets.json."""
    if not os.path.exists(SECRETS_PATH):
        return None
    try:
        with open(SECRETS_PATH, "r", encoding="utf-8") as f:
            data = json.load(f)
        token = data.get("gumroad_access_token", "")
        if not token or token.startswith("YOUR_"):
            return None
        return token
    except (json.JSONDecodeError, OSError):
        return None


def ensure_secrets_file() -> None:
    """Create secrets.json with placeholder if it doesn't exist."""
    if os.path.exists(SECRETS_PATH):
        try:
            with open(SECRETS_PATH, "r", encoding="utf-8") as f:
                data = json.load(f)
            if "gumroad_access_token" not in data:
                updated = deepcopy(data)
                updated["gumroad_access_token"] = "YOUR_GUMROAD_ACCESS_TOKEN"
                with open(SECRETS_PATH, "w", encoding="utf-8") as f:
                    json.dump(updated, f, indent=2, ensure_ascii=False)
                    f.write("\n")
                log("Added gumroad_access_token placeholder to secrets.json")
        except (json.JSONDecodeError, OSError):
            pass
    else:
        os.makedirs(os.path.dirname(SECRETS_PATH), exist_ok=True)
        data = {"gumroad_access_token": "YOUR_GUMROAD_ACCESS_TOKEN"}
        with open(SECRETS_PATH, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
            f.write("\n")
        log("Created secrets.json with gumroad_access_token placeholder")


def api_get(endpoint: str, token: str, params: dict | None = None) -> dict:
    """Make authenticated GET request to Gumroad API."""
    url = f"{GUMROAD_API_BASE}{endpoint}"
    headers = {"Authorization": f"Bearer {token}"}
    resp = requests.get(url, headers=headers, params=params or {}, timeout=30)
    resp.raise_for_status()
    return resp.json()


def fetch_products(token: str) -> list[dict]:
    """Fetch all products."""
    data = api_get("/products", token)
    if not data.get("success"):
        raise RuntimeError(f"Gumroad API error: {data}")
    return data.get("products", [])


def fetch_sales(token: str, after: str | None = None, page: int = 1) -> tuple[list[dict], int]:
    """Fetch sales with pagination. Returns (sales_list, next_page_key)."""
    all_sales: list[dict] = []
    params: dict = {"page": page}
    if after:
        params["after"] = after

    while True:
        data = api_get("/sales", token, params)
        if not data.get("success"):
            raise RuntimeError(f"Gumroad API error: {data}")
        sales = data.get("sales", [])
        all_sales.extend(sales)
        next_page = data.get("next_page_url")
        if not next_page or not sales:
            break
        params["page"] = params.get("page", 1) + 1

    return all_sales, len(all_sales)


def build_report(products: list[dict], sales: list[dict]) -> dict:
    """Build structured report from raw API data."""
    now = datetime.now(PYT).isoformat()

    product_summary = []
    for p in products:
        product_summary.append({
            "id": p.get("id", ""),
            "name": p.get("name", ""),
            "price_cents": p.get("price", 0),
            "sales_count": p.get("sales_count", 0),
            "revenue_cents": p.get("total_revenue", 0),
            "currency": p.get("currency", "usd"),
            "published": p.get("published", False),
            "url": p.get("short_url", ""),
        })

    total_revenue_cents = sum(p["revenue_cents"] for p in product_summary)
    total_sales = sum(p["sales_count"] for p in product_summary)

    # Recent sales (last 30 days)
    thirty_days_ago = datetime.now(timezone.utc) - timedelta(days=30)
    recent_sales = []
    for s in sales:
        created = s.get("created_at", "")
        try:
            dt = datetime.fromisoformat(created.replace("Z", "+00:00"))
            if dt >= thirty_days_ago:
                recent_sales.append({
                    "product": s.get("product_name", ""),
                    "price": s.get("price", 0),
                    "currency": s.get("currency", "usd"),
                    "date": created,
                    "email": s.get("email", "")[:3] + "***",
                })
        except (ValueError, TypeError):
            pass

    report = {
        "generated_at": now,
        "totals": {
            "products": len(product_summary),
            "total_sales": total_sales,
            "total_revenue_cents": total_revenue_cents,
            "total_revenue_display": f"${total_revenue_cents / 100:.2f}",
            "currency": "usd",
        },
        "products": sorted(product_summary, key=lambda x: x["revenue_cents"], reverse=True),
        "recent_sales_30d": recent_sales,
        "recent_sales_count_30d": len(recent_sales),
    }
    return report


def print_summary(report: dict) -> None:
    """Print human-readable summary."""
    totals = report["totals"]
    print("\n" + "=" * 60)
    print("  Gumroad Sales Report")
    print(f"  Generated: {report['generated_at']}")
    print("=" * 60)
    print(f"\n  Total Products: {totals['products']}")
    print(f"  Total Sales:    {totals['total_sales']}")
    print(f"  Total Revenue:  {totals['total_revenue_display']}")
    print(f"\n  {'Product':<35} {'Sales':>6} {'Revenue':>10}")
    print("  " + "-" * 55)
    for p in report["products"]:
        rev = f"${p['revenue_cents'] / 100:.2f}"
        name = p["name"][:33]
        print(f"  {name:<35} {p['sales_count']:>6} {rev:>10}")

    recent = report["recent_sales_30d"]
    if recent:
        print(f"\n  Recent Sales (30 days): {len(recent)}")
        for s in recent[:10]:
            print(f"    - {s['date'][:10]} | {s['product']} | ${s['price'] / 100:.2f}")
    else:
        print("\n  Recent Sales (30 days): 0")
    print("=" * 60 + "\n")


def main() -> None:
    args = set(sys.argv[1:])
    summary_only = "--summary" in args
    json_only = "--json" in args

    ensure_secrets_file()
    token = load_access_token()

    if not token:
        log("ERROR: Gumroad access token not configured")
        print("\n" + "=" * 60)
        print("  Gumroad APIキー未設定")
        print("=" * 60)
        print("\n  以下の手順でアクセストークンを取得してください:\n")
        print("  1. ブラウザで以下にアクセス:")
        print("     https://app.gumroad.com/settings/advanced#application-form\n")
        print("  2. 「Application name」に任意の名前を入力（例: Sales Report）")
        print("  3. 「Create application」をクリック")
        print("  4. 作成されたアプリの「Generate access token」をクリック")
        print("  5. 表示されたアクセストークンをコピー\n")
        print("  6. 以下のファイルを編集:")
        print(f"     {SECRETS_PATH}\n")
        print('     "gumroad_access_token" の値をコピーしたトークンに書き換え\n')
        print("  設定例:")
        print('     "gumroad_access_token": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"')
        print("=" * 60 + "\n")
        sys.exit(1)

    log("Fetching products from Gumroad API...")
    try:
        products = fetch_products(token)
        log(f"Fetched {len(products)} products")
    except Exception as e:
        log(f"ERROR fetching products: {e}")
        print(f"Error: {e}")
        sys.exit(1)

    log("Fetching sales from Gumroad API...")
    try:
        sales, count = fetch_sales(token)
        log(f"Fetched {count} sales")
    except Exception as e:
        log(f"ERROR fetching sales: {e}")
        sales = []

    report = build_report(products, sales)

    # Save JSON
    with open(REPORT_JSON_PATH, "w", encoding="utf-8") as f:
        json.dump(report, f, indent=2, ensure_ascii=False)
        f.write("\n")
    log(f"Report saved to {REPORT_JSON_PATH}")

    if json_only:
        print(json.dumps(report, indent=2, ensure_ascii=False))
    elif summary_only:
        print_summary(report)
    else:
        print_summary(report)
        print(f"  JSON saved: {REPORT_JSON_PATH}\n")


if __name__ == "__main__":
    main()
