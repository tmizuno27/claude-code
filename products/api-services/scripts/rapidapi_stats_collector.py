#!/usr/bin/env python3
"""RapidAPI Stats Collector

Collects health/status data for all 24 Cloudflare Workers APIs
and writes rapidapi-stats.json.

Since RapidAPI Provider API access is limited, this script:
1. Pings each Cloudflare Worker endpoint to verify it's alive
2. Updates the stats JSON with timestamp and health status
"""

import json
import os
import sys
from datetime import datetime, timezone

import requests

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_DIR = os.path.dirname(SCRIPT_DIR)
STATS_FILE = os.path.join(PROJECT_DIR, "rapidapi-stats.json")
BASE_DOMAIN = "t-mizuno27.workers.dev"
TIMEOUT = 10

API_LIST = [
    {"id": "01", "name": "QR Code API", "subdomain": "qr-code-api"},
    {"id": "02", "name": "Email Validation API", "subdomain": "email-validation-api"},
    {"id": "03", "name": "Link Preview API", "subdomain": "link-preview-api"},
    {"id": "04", "name": "Screenshot API", "subdomain": "screenshot-api"},
    {"id": "05", "name": "Text Analysis API", "subdomain": "text-analysis-api"},
    {"id": "06", "name": "IP Geolocation API", "subdomain": "ip-geolocation-api"},
    {"id": "07", "name": "URL Shortener API", "subdomain": "url-shortener-api"},
    {"id": "08", "name": "JSON Formatter API", "subdomain": "json-formatter-api"},
    {"id": "09", "name": "Hash Encoding API", "subdomain": "hash-encoding-api"},
    {"id": "10", "name": "Currency Exchange API", "subdomain": "currency-exchange-api"},
    {"id": "11", "name": "AI Text API", "subdomain": "ai-text-api"},
    {"id": "12", "name": "Social Video API", "subdomain": "social-video-api"},
    {"id": "13", "name": "Crypto Data API", "subdomain": "crypto-data-api"},
    {"id": "14", "name": "SEO Analyzer API", "subdomain": "seo-analyzer-api"},
    {"id": "15", "name": "Weather API", "subdomain": "weather-api"},
    {"id": "16", "name": "WHOIS Domain API", "subdomain": "whois-domain-api"},
    {"id": "17", "name": "News Aggregator API", "subdomain": "news-aggregator-api"},
    {"id": "18", "name": "AI Translate API", "subdomain": "ai-translate-api"},
    {"id": "19", "name": "Trends API", "subdomain": "trends-api"},
    {"id": "20", "name": "Company Data API", "subdomain": "company-data-api"},
    {"id": "21", "name": "WP Internal Link Optimization API", "subdomain": "wp-internal-link-api"},
    {"id": "22", "name": "PDF Generator API", "subdomain": "pdf-generator-api"},
    {"id": "23", "name": "Placeholder Image API", "subdomain": "placeholder-image-api"},
    {"id": "24", "name": "Markdown Converter API", "subdomain": "markdown-converter-api"},
]


def check_worker_health(subdomain: str) -> str:
    """Ping a Cloudflare Worker and return status."""
    url = f"https://{subdomain}.{BASE_DOMAIN}/"
    try:
        resp = requests.get(url, timeout=TIMEOUT)
        if resp.status_code < 500:
            return "active"
        return "error"
    except requests.RequestException:
        return "unreachable"


def collect_stats() -> dict:
    """Collect stats for all APIs."""
    now = datetime.now(timezone.utc)

    # Load existing stats to preserve any manually-set values
    existing_apis = {}
    if os.path.exists(STATS_FILE):
        try:
            with open(STATS_FILE, "r", encoding="utf-8") as f:
                old_data = json.load(f)
            for api in old_data.get("apis", []):
                existing_apis[api["id"]] = api
        except (json.JSONDecodeError, KeyError):
            pass

    apis = []
    active_count = 0
    for api_def in API_LIST:
        status = check_worker_health(api_def["subdomain"])
        if status == "active":
            active_count += 1

        # Preserve existing subscriber/request/revenue data
        old = existing_apis.get(api_def["id"], {})
        apis.append({
            "id": api_def["id"],
            "name": api_def["name"],
            "subdomain": api_def["subdomain"],
            "rapidapi_listed": old.get("rapidapi_listed", True),
            "subscribers": old.get("subscribers", 0),
            "requests": old.get("requests", 0),
            "api_calls_30d": old.get("api_calls_30d", 0),
            "revenue_30d": old.get("revenue_30d", 0),
            "status": status,
        })

    return {
        "last_updated": now.strftime("%Y-%m-%d"),
        "last_updated_iso": now.isoformat(),
        "total_apis": len(API_LIST),
        "listed_on_rapidapi": len(API_LIST),
        "pending_listing": 0,
        "active_workers": active_count,
        "monthly_revenue": 0,
        "monthly_revenue_usd": 0,
        "total_subscribers": sum(a["subscribers"] for a in apis),
        "total_api_calls": sum(a["api_calls_30d"] for a in apis),
        "total_requests": sum(a["requests"] for a in apis),
        "base_domain": BASE_DOMAIN,
        "collection_method": "worker_healthcheck",
        "apis": apis,
    }


def main():
    try:
        stats = collect_stats()
        with open(STATS_FILE, "w", encoding="utf-8") as f:
            json.dump(stats, f, indent=2, ensure_ascii=False)
        print(f"Stats collected: {stats['active_workers']}/{stats['total_apis']} workers active")
        return 0
    except Exception as e:
        print(f"ERROR: {e}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
