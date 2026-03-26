"""
VS Code Marketplace Stats Tracker
Publisher: miccho27

Fetches install counts, ratings, and metadata for all published extensions.
Uses filterType 10 (search text) since filterType 8 (publisher name) returns
empty results for this publisher.

API: POST https://marketplace.visualstudio.com/_apis/public/gallery/extensionquery
"""

import json
import sys
from datetime import datetime, timezone
from pathlib import Path
from urllib.request import Request, urlopen
from urllib.error import URLError, HTTPError

PUBLISHER = "miccho27"
API_URL = "https://marketplace.visualstudio.com/_apis/public/gallery/extensionquery"

# flags=914 includes statistics, versions, and properties
QUERY_PAYLOAD = {
    "filters": [
        {
            "criteria": [
                {"filterType": 10, "value": PUBLISHER}
            ],
            "pageNumber": 1,
            "pageSize": 50,
            "sortBy": 0,
            "sortOrder": 0,
        }
    ],
    "assetTypes": [],
    "flags": 914,
}

HEADERS = {
    "Content-Type": "application/json",
    "Accept": "application/json;api-version=3.0-preview.1",
}

STAT_NAMES = {
    "install": "Installs",
    "averagerating": "Avg Rating",
    "ratingcount": "Rating Count",
    "updateCount": "Updates",
    "weightedRating": "Weighted Rating",
    "downloadCount": "Downloads",
    "trendingdaily": "Trend (Daily)",
    "trendingweekly": "Trend (Weekly)",
    "trendingmonthly": "Trend (Monthly)",
}


def fetch_extensions() -> list[dict]:
    """Fetch all extensions for the publisher from Marketplace API."""
    data = json.dumps(QUERY_PAYLOAD).encode("utf-8")
    req = Request(API_URL, data=data, headers=HEADERS, method="POST")

    try:
        with urlopen(req, timeout=30) as resp:
            body = json.loads(resp.read().decode("utf-8"))
    except HTTPError as e:
        print(f"HTTP Error {e.code}: {e.reason}", file=sys.stderr)
        print(f"Response: {e.read().decode('utf-8', errors='replace')}", file=sys.stderr)
        sys.exit(1)
    except URLError as e:
        print(f"Connection error: {e.reason}", file=sys.stderr)
        sys.exit(1)

    results = body.get("results", [])
    if not results:
        return []

    extensions = results[0].get("extensions", [])
    # Filter to only this publisher's extensions
    return [
        ext for ext in extensions
        if ext.get("publisher", {}).get("publisherName", "").lower() == PUBLISHER.lower()
    ]


def extract_stats(ext: dict) -> dict:
    """Extract key statistics from an extension object."""
    stats_list = ext.get("statistics", [])
    stats = {}
    for s in stats_list:
        name = s.get("statisticName", "")
        value = s.get("value", 0)
        if name in STAT_NAMES:
            stats[name] = value
    return stats


def format_report(extensions: list[dict]) -> str:
    """Format extensions data into a readable report."""
    now = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
    lines = [
        f"VS Code Marketplace Stats - Publisher: {PUBLISHER}",
        f"Generated: {now}",
        f"Total extensions: {len(extensions)}",
        "=" * 70,
        "",
    ]

    total_installs = 0
    total_downloads = 0

    for ext in sorted(extensions, key=lambda e: e.get("extensionName", "")):
        name = ext.get("displayName", ext.get("extensionName", "Unknown"))
        ext_name = ext.get("extensionName", "")
        published = ext.get("publishedDate", "")[:10]
        updated = ext.get("lastUpdated", "")[:10]
        description = ext.get("shortDescription", "N/A")
        version = ""
        versions = ext.get("versions", [])
        if versions:
            version = versions[0].get("version", "")

        stats = extract_stats(ext)
        installs = int(stats.get("install", 0))
        downloads = int(stats.get("downloadCount", 0))
        avg_rating = stats.get("averagerating", 0)
        rating_count = int(stats.get("ratingcount", 0))

        total_installs += installs
        total_downloads += downloads

        lines.append(f"{name} ({ext_name})")
        lines.append(f"  Version: {version} | Published: {published} | Updated: {updated}")
        lines.append(f"  Installs: {installs:,} | Downloads: {downloads:,}")
        if rating_count > 0:
            lines.append(f"  Rating: {avg_rating:.1f}/5 ({rating_count} ratings)")
        else:
            lines.append("  Rating: No ratings yet")
        lines.append(f"  {description}")
        lines.append("")

    lines.append("=" * 70)
    lines.append(f"TOTALS: {total_installs:,} installs | {total_downloads:,} downloads")

    return "\n".join(lines)


def save_json(extensions: list[dict], output_path: Path) -> None:
    """Save raw stats as JSON for programmatic use."""
    records = []
    for ext in extensions:
        stats = extract_stats(ext)
        records.append({
            "extensionName": ext.get("extensionName", ""),
            "displayName": ext.get("displayName", ""),
            "version": ext.get("versions", [{}])[0].get("version", "") if ext.get("versions") else "",
            "publishedDate": ext.get("publishedDate", ""),
            "lastUpdated": ext.get("lastUpdated", ""),
            "installs": int(stats.get("install", 0)),
            "downloads": int(stats.get("downloadCount", 0)),
            "averageRating": stats.get("averagerating", 0),
            "ratingCount": int(stats.get("ratingcount", 0)),
        })

    output = {
        "publisher": PUBLISHER,
        "fetchedAt": datetime.now(timezone.utc).isoformat(),
        "extensionCount": len(records),
        "extensions": sorted(records, key=lambda r: r["extensionName"]),
    }

    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(output, indent=2, ensure_ascii=False), encoding="utf-8")


def main():
    print(f"Fetching extensions for publisher: {PUBLISHER}...")
    extensions = fetch_extensions()

    if not extensions:
        print("No extensions found.", file=sys.stderr)
        sys.exit(1)

    report = format_report(extensions)
    print(report)

    # Save JSON to outputs/
    script_dir = Path(__file__).resolve().parent
    json_path = script_dir.parent / "outputs" / "marketplace_stats.json"
    save_json(extensions, json_path)
    print(f"\nJSON saved to: {json_path}")


if __name__ == "__main__":
    main()
