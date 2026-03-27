"""
RapidAPI Popularity Booster — 自分のFree tierで定期リクエストを送りPopularityスコアを上げる

RapidAPIのアルゴリズムはAPI Calls（利用数）をPopularityの主要指標としている。
Free tierで自分のAPIに定期的にリクエストを送ることで、ランキング上昇を狙う。

Task Scheduler: 毎日3回（8:00, 14:00, 20:00 PYT）実行推奨
"""

import requests
import time
import random
import json
import os
from datetime import datetime

LOG_PATH = r"c:\Users\tmizu\マイドライブ\GitHub\claude-code\logs\rapidapi-popularity.log"
HEALTHCHECKS_URL = "https://hc-ping.com/YOUR-UUID-HERE"  # TODO: replace

# RapidAPI Key（環境変数から取得）
RAPIDAPI_KEY = os.environ.get("RAPIDAPI_KEY", "")

if not RAPIDAPI_KEY:
    print("ERROR: RAPIDAPI_KEY environment variable not set")
    print("Set it: $env:RAPIDAPI_KEY = 'your-key-here'")
    exit(1)

# 上位5本を集中的に、残りもローテーションで叩く
PRIORITY_APIS = [
    {
        "name": "SEO Analyzer API",
        "host": "seo-analyzer-api.p.rapidapi.com",
        "calls": [
            {"method": "GET", "url": "https://seo-analyzer-api.p.rapidapi.com/score", "params": {"url": "https://github.com"}},
            {"method": "GET", "url": "https://seo-analyzer-api.p.rapidapi.com/analyze", "params": {"url": "https://example.com"}},
            {"method": "GET", "url": "https://seo-analyzer-api.p.rapidapi.com/headings", "params": {"url": "https://wikipedia.org"}},
        ],
    },
    {
        "name": "Email Validation API",
        "host": "email-validation-api.p.rapidapi.com",
        "calls": [
            {"method": "GET", "url": "https://email-validation-api.p.rapidapi.com/validate", "params": {"email": "test@gmail.com"}},
            {"method": "GET", "url": "https://email-validation-api.p.rapidapi.com/validate", "params": {"email": "info@example.com"}},
            {"method": "GET", "url": "https://email-validation-api.p.rapidapi.com/validate", "params": {"email": "fake@mailinator.com"}},
        ],
    },
    {
        "name": "QR Code Generator API",
        "host": "qr-code-generator-api.p.rapidapi.com",
        "calls": [
            {"method": "GET", "url": "https://qr-code-generator-api.p.rapidapi.com/generate", "params": {"text": "https://example.com", "format": "base64"}},
            {"method": "GET", "url": "https://qr-code-generator-api.p.rapidapi.com/generate", "params": {"text": "Hello World", "format": "svg"}},
        ],
    },
    {
        "name": "WHOIS Domain API",
        "host": "whois-domain-api.p.rapidapi.com",
        "calls": [
            {"method": "GET", "url": "https://whois-domain-api.p.rapidapi.com/lookup", "params": {"domain": "google.com"}},
            {"method": "GET", "url": "https://whois-domain-api.p.rapidapi.com/dns", "params": {"domain": "github.com"}},
            {"method": "GET", "url": "https://whois-domain-api.p.rapidapi.com/availability", "params": {"domain": "randomtest12345.com"}},
        ],
    },
    {
        "name": "Website Screenshot API",
        "host": "website-screenshot-api.p.rapidapi.com",
        "calls": [
            {"method": "GET", "url": "https://website-screenshot-api.p.rapidapi.com/screenshot", "params": {"url": "https://example.com", "width": "1280"}},
        ],
    },
]

SECONDARY_APIS = [
    {
        "name": "IP Geolocation API",
        "host": "ip-geolocation-api.p.rapidapi.com",
        "calls": [
            {"method": "GET", "url": "https://ip-geolocation-api.p.rapidapi.com/me"},
        ],
    },
    {
        "name": "Currency Exchange API",
        "host": "currency-exchange-api.p.rapidapi.com",
        "calls": [
            {"method": "GET", "url": "https://currency-exchange-api.p.rapidapi.com/currencies"},
        ],
    },
    {
        "name": "Hash Encoding API",
        "host": "hash-encoding-api.p.rapidapi.com",
        "calls": [
            {"method": "POST", "url": "https://hash-encoding-api.p.rapidapi.com/hash", "json": {"text": "hello", "algorithm": "sha256"}},
        ],
    },
    {
        "name": "JSON Formatter API",
        "host": "json-formatter-api.p.rapidapi.com",
        "calls": [
            {"method": "POST", "url": "https://json-formatter-api.p.rapidapi.com/validate", "json": {"data": '{"test": true}'}},
        ],
    },
    {
        "name": "Text Analysis API",
        "host": "text-analysis-api.p.rapidapi.com",
        "calls": [
            {"method": "POST", "url": "https://text-analysis-api.p.rapidapi.com/sentiment", "json": {"text": "This product is great!"}},
        ],
    },
    {
        "name": "Link Preview API",
        "host": "link-preview-api.p.rapidapi.com",
        "calls": [
            {"method": "GET", "url": "https://link-preview-api.p.rapidapi.com/preview", "params": {"url": "https://github.com"}},
        ],
    },
    {
        "name": "Crypto Data API",
        "host": "crypto-data-api.p.rapidapi.com",
        "calls": [
            {"method": "GET", "url": "https://crypto-data-api.p.rapidapi.com/global"},
        ],
    },
    {
        "name": "News Aggregator API",
        "host": "news-aggregator-api.p.rapidapi.com",
        "calls": [
            {"method": "GET", "url": "https://news-aggregator-api.p.rapidapi.com/hackernews/top"},
        ],
    },
    {
        "name": "Trends API",
        "host": "trends-api.p.rapidapi.com",
        "calls": [
            {"method": "GET", "url": "https://trends-api.p.rapidapi.com/github/trending"},
        ],
    },
]


def make_request(call, host):
    """Execute a single API call via RapidAPI."""
    headers = {
        "X-RapidAPI-Key": RAPIDAPI_KEY,
        "X-RapidAPI-Host": host,
    }
    method = call.get("method", "GET")
    try:
        if method == "POST":
            r = requests.post(
                call["url"],
                headers=headers,
                json=call.get("json"),
                timeout=30,
            )
        else:
            r = requests.get(
                call["url"],
                headers=headers,
                params=call.get("params"),
                timeout=30,
            )
        return r.status_code, round(r.elapsed.total_seconds() * 1000)
    except Exception as e:
        return None, str(e)


def main():
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"=== RapidAPI Popularity Booster: {timestamp} ===\n")

    results = []
    total_calls = 0
    ok_calls = 0

    # Priority APIs: all calls
    for api in PRIORITY_APIS:
        for call in api["calls"]:
            status, ms = make_request(call, api["host"])
            ok = status is not None and status < 400
            if ok:
                ok_calls += 1
            total_calls += 1
            label = f"{status} ({ms}ms)" if status else f"ERR: {ms}"
            print(f"  [{api['name'][:20]:<20s}] {call.get('url','')[:60]:<60s} -> {label}")
            results.append({"api": api["name"], "status": status, "ms": ms})
            # Random delay to look organic
            time.sleep(random.uniform(1.0, 3.0))

    # Secondary APIs: pick 4 random ones per run
    daily_secondary = random.sample(SECONDARY_APIS, min(4, len(SECONDARY_APIS)))
    for api in daily_secondary:
        for call in api["calls"]:
            status, ms = make_request(call, api["host"])
            ok = status is not None and status < 400
            if ok:
                ok_calls += 1
            total_calls += 1
            label = f"{status} ({ms}ms)" if status else f"ERR: {ms}"
            print(f"  [{api['name'][:20]:<20s}] {call.get('url','')[:60]:<60s} -> {label}")
            results.append({"api": api["name"], "status": status, "ms": ms})
            time.sleep(random.uniform(1.0, 3.0))

    summary = f"\n--- {ok_calls}/{total_calls} successful calls ---"
    print(summary)

    # Log
    try:
        os.makedirs(os.path.dirname(LOG_PATH), exist_ok=True)
        with open(LOG_PATH, "a", encoding="utf-8") as f:
            f.write(f"\n[{timestamp}] Popularity Boost: {ok_calls}/{total_calls} OK\n")
            for r in results:
                f.write(f"  {r['api']}: {r['status']} ({r['ms']})\n")
        print(f"Log: {LOG_PATH}")
    except Exception as e:
        print(f"Log error: {e}")


if __name__ == "__main__":
    main()
