"""
RapidAPI 全24 API テストスイート

Workers直接アクセス（RapidAPI経由ではない）で全エンドポイントの動作確認を行う。
レスポンスのJSON構造、ステータスコード、レスポンスタイムを検証。

Usage: python api-test-suite.py [--verbose]
"""

import requests
import json
import sys
import time
from datetime import datetime

VERBOSE = "--verbose" in sys.argv or "-v" in sys.argv
BASE = "t-mizuno27.workers.dev"
TIMEOUT = 30
PASS_COUNT = 0
FAIL_COUNT = 0
RESULTS = []


def test(api_name, endpoint, method="GET", params=None, json_body=None,
         expect_status=200, expect_keys=None, expect_content_type="application/json"):
    """Run a single test and track results."""
    global PASS_COUNT, FAIL_COUNT
    url = f"https://{endpoint}"
    errors = []

    try:
        start = time.time()
        if method == "POST":
            r = requests.post(url, json=json_body, timeout=TIMEOUT)
        else:
            r = requests.get(url, params=params, timeout=TIMEOUT)
        elapsed_ms = round((time.time() - start) * 1000)

        # Status check
        if r.status_code != expect_status:
            errors.append(f"Status {r.status_code} (expected {expect_status})")

        # Content-Type check
        ct = r.headers.get("Content-Type", "")
        if expect_content_type and expect_content_type not in ct:
            errors.append(f"Content-Type '{ct}' (expected '{expect_content_type}')")

        # Key presence check (JSON only)
        data = None
        if "json" in ct:
            try:
                data = r.json()
                if expect_keys:
                    for key in expect_keys:
                        if key not in data:
                            errors.append(f"Missing key '{key}'")
            except json.JSONDecodeError:
                errors.append("Invalid JSON response")

        # CORS check
        if "Access-Control-Allow-Origin" not in r.headers:
            errors.append("Missing CORS header")

        passed = len(errors) == 0
        if passed:
            PASS_COUNT += 1
        else:
            FAIL_COUNT += 1

        result = {
            "api": api_name,
            "url": url,
            "status": "PASS" if passed else "FAIL",
            "http_status": r.status_code,
            "ms": elapsed_ms,
            "errors": errors,
        }
        RESULTS.append(result)

        icon = "PASS" if passed else "FAIL"
        print(f"  [{icon}] {api_name:<30s} {url:<70s} {r.status_code} ({elapsed_ms}ms)")
        if errors and VERBOSE:
            for e in errors:
                print(f"         -> {e}")
        if data and VERBOSE:
            preview = json.dumps(data, ensure_ascii=False)[:200]
            print(f"         -> {preview}")

    except Exception as e:
        FAIL_COUNT += 1
        RESULTS.append({"api": api_name, "url": url, "status": "FAIL", "errors": [str(e)]})
        print(f"  [FAIL] {api_name:<30s} {url:<70s} ERROR: {e}")


def main():
    print(f"=== RapidAPI Test Suite: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} ===\n")

    # 01 - QR Code API
    test("QR Code - root", f"qr-code-api.{BASE}/", expect_keys=["endpoints"])
    test("QR Code - generate PNG", f"qr-code-api.{BASE}/generate",
         params={"text": "hello", "size": "200"}, expect_content_type="image/png", expect_keys=None)
    test("QR Code - generate SVG", f"qr-code-api.{BASE}/generate",
         params={"text": "hello", "format": "svg"}, expect_content_type="image/svg+xml", expect_keys=None)
    test("QR Code - generate base64", f"qr-code-api.{BASE}/generate",
         params={"text": "hello", "format": "base64"}, expect_keys=["data", "data_uri"])
    test("QR Code - missing text", f"qr-code-api.{BASE}/generate", expect_status=400, expect_keys=["error"])

    # 02 - Email Validation API
    test("Email - root", f"email-validation-api.{BASE}/", expect_keys=["endpoints"])
    test("Email - validate", f"email-validation-api.{BASE}/validate",
         params={"email": "test@gmail.com"}, expect_keys=["valid", "score", "mx_found"])
    test("Email - disposable", f"email-validation-api.{BASE}/validate",
         params={"email": "test@mailinator.com"}, expect_keys=["is_disposable"])
    test("Email - typo", f"email-validation-api.{BASE}/validate",
         params={"email": "user@gmial.com"}, expect_keys=["suggestion"])
    test("Email - missing param", f"email-validation-api.{BASE}/validate", expect_status=400)
    test("Email - bulk", f"email-validation-api.{BASE}/validate/bulk",
         method="POST", json_body={"emails": ["a@gmail.com", "b@yahoo.com"]},
         expect_keys=["count", "results"])

    # 03 - Link Preview API
    test("Link Preview - root", f"link-preview-api.{BASE}/", expect_keys=[])
    test("Link Preview - preview", f"link-preview-api.{BASE}/preview",
         params={"url": "https://example.com"})

    # 04 - Screenshot API
    test("Screenshot - root", f"screenshot-api.{BASE}/", expect_keys=["service"])
    test("Screenshot - capture", f"screenshot-api.{BASE}/screenshot",
         params={"url": "https://example.com"}, expect_content_type="image/")
    test("Screenshot - missing url", f"screenshot-api.{BASE}/screenshot", expect_status=400)

    # 05 - Text Analysis API
    test("Text Analysis - root", f"text-analysis-api.{BASE}/")
    test("Text Analysis - sentiment", f"text-analysis-api.{BASE}/sentiment",
         method="POST", json_body={"text": "This is great!"})

    # 06 - IP Geolocation API
    test("IP Geo - root", f"ip-geolocation-api.{BASE}/")
    test("IP Geo - me", f"ip-geolocation-api.{BASE}/me")

    # 07 - URL Shortener API
    test("URL Shortener - root", f"url-shortener-api.{BASE}/")
    test("URL Shortener - shorten", f"url-shortener-api.{BASE}/shorten",
         method="POST", json_body={"url": "https://example.com"})

    # 08 - JSON Formatter API
    test("JSON Formatter - root", f"json-formatter-api.{BASE}/")
    test("JSON Formatter - validate", f"json-formatter-api.{BASE}/validate",
         method="POST", json_body={"data": '{"a":1}'})

    # 09 - Hash Encoding API
    test("Hash - root", f"hash-encoding-api.{BASE}/")
    test("Hash - sha256", f"hash-encoding-api.{BASE}/hash",
         method="POST", json_body={"text": "hello", "algorithm": "sha256"})

    # 10 - Currency Exchange API
    test("Currency - root", f"currency-exchange-api.{BASE}/")
    test("Currency - currencies", f"currency-exchange-api.{BASE}/currencies")

    # 11 - AI Text API
    test("AI Text - root", f"ai-text-api.{BASE}/")

    # 12 - Social Video API
    test("Social Video - root", f"social-video-api.{BASE}/")
    test("Social Video - platforms", f"social-video-api.{BASE}/platforms")

    # 13 - Crypto Data API
    test("Crypto - root", f"crypto-data-api.{BASE}/")
    test("Crypto - global", f"crypto-data-api.{BASE}/global")

    # 14 - SEO Analyzer API
    test("SEO - root", f"seo-analyzer-api.{BASE}/", expect_keys=["endpoints"])
    test("SEO - analyze", f"seo-analyzer-api.{BASE}/analyze",
         params={"url": "https://example.com"}, expect_keys=["seoScore", "title"])
    test("SEO - score", f"seo-analyzer-api.{BASE}/score",
         params={"url": "https://example.com"}, expect_keys=["seoScore"])
    test("SEO - headings", f"seo-analyzer-api.{BASE}/headings",
         params={"url": "https://example.com"}, expect_keys=["headings"])
    test("SEO - links", f"seo-analyzer-api.{BASE}/links",
         params={"url": "https://example.com"}, expect_keys=["links"])
    test("SEO - missing url", f"seo-analyzer-api.{BASE}/analyze", expect_status=400)

    # 15 - Weather API
    test("Weather - root", f"weather-api.{BASE}/")
    test("Weather - current", f"weather-api.{BASE}/current",
         params={"lat": "35.68", "lon": "139.69"})

    # 16 - WHOIS Domain API
    test("WHOIS - root", f"whois-domain-api.{BASE}/", expect_keys=["endpoints"])
    test("WHOIS - lookup", f"whois-domain-api.{BASE}/lookup",
         params={"domain": "google.com"}, expect_keys=["domain"])
    test("WHOIS - dns", f"whois-domain-api.{BASE}/dns",
         params={"domain": "google.com"}, expect_keys=["domain", "records"])
    test("WHOIS - availability", f"whois-domain-api.{BASE}/availability",
         params={"domain": "randomtest99999999.com"}, expect_keys=["available"])
    test("WHOIS - tld-list", f"whois-domain-api.{BASE}/tld-list", expect_keys=["count", "tlds"])

    # 17 - News Aggregator API
    test("News - root", f"news-aggregator-api.{BASE}/")
    test("News - HN top", f"news-aggregator-api.{BASE}/hackernews/top")

    # 18 - AI Translate API
    test("Translate - root", f"ai-translate-api.{BASE}/")
    test("Translate - languages", f"ai-translate-api.{BASE}/languages")

    # 19 - Trends API
    test("Trends - root", f"trends-api.{BASE}/")
    test("Trends - github", f"trends-api.{BASE}/github/trending")

    # 20 - Company Data API
    test("Company - root", f"company-data-api.{BASE}/")
    test("Company - search", f"company-data-api.{BASE}/search",
         params={"q": "google"})

    # 21-24 - Newer APIs
    for name, sub in [("WP Internal Link", "wp-internal-link-api"),
                       ("PDF Generator", "pdf-generator-api"),
                       ("Placeholder Image", "placeholder-image-api"),
                       ("Markdown Converter", "markdown-converter-api")]:
        test(f"{name} - root", f"{sub}.{BASE}/")
        test(f"{name} - health", f"{sub}.{BASE}/health")

    # Summary
    total = PASS_COUNT + FAIL_COUNT
    print(f"\n{'='*80}")
    print(f"RESULTS: {PASS_COUNT}/{total} PASSED, {FAIL_COUNT} FAILED")
    print(f"{'='*80}")

    if FAIL_COUNT > 0:
        print("\nFailed tests:")
        for r in RESULTS:
            if r["status"] == "FAIL":
                print(f"  - {r['api']}: {', '.join(r['errors'])}")

    # Save report
    report_path = r"c:\Users\tmizu\マイドライブ\GitHub\claude-code\products\api-services\scripts\test-report.json"
    with open(report_path, "w", encoding="utf-8") as f:
        json.dump({
            "timestamp": datetime.now().isoformat(),
            "summary": {"total": total, "passed": PASS_COUNT, "failed": FAIL_COUNT},
            "results": RESULTS,
        }, f, indent=2, ensure_ascii=False)
    print(f"\nReport: {report_path}")

    return 0 if FAIL_COUNT == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
