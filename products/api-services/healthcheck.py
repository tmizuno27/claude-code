"""
Cloudflare Workers API Health Check Script
Tests 20 APIs: root endpoint + one functional endpoint each.
"""

import requests
import time
from datetime import datetime

TIMEOUT = 30
BASE_DOMAIN = "t-mizuno27.workers.dev"
LOG_PATH = r"c:\Users\tmizu\マイドライブ\GitHub\claude-code\logs\api-healthcheck.log"
HEALTHCHECKS_URL = "https://hc-ping.com/YOUR-UUID-HERE"  # TODO: replace with real UUID

APIS = [
    {"id": "01", "name": "QR Code API", "subdomain": "qr-code-api",
     "test": {"method": "GET", "path": "/generate", "params": {"text": "test", "format": "svg"}}},
    {"id": "02", "name": "Email Validation API", "subdomain": "email-validation-api",
     "test": {"method": "GET", "path": "/validate", "params": {"email": "test@gmail.com"}}},
    {"id": "03", "name": "Link Preview API", "subdomain": "link-preview-api",
     "test": {"method": "GET", "path": "/preview", "params": {"url": "https://example.com"}}},
    {"id": "04", "name": "Screenshot API", "subdomain": "screenshot-api",
     "test": {"method": "GET", "path": "/screenshot", "params": {"url": "https://example.com"}}},
    {"id": "05", "name": "Text Analysis API", "subdomain": "text-analysis-api",
     "test": {"method": "POST", "path": "/sentiment", "json": {"text": "good"}}},
    {"id": "06", "name": "IP Geolocation API", "subdomain": "ip-geolocation-api",
     "test": {"method": "GET", "path": "/me"}},
    {"id": "07", "name": "URL Shortener API", "subdomain": "url-shortener-api",
     "test": {"method": "POST", "path": "/shorten", "json": {"url": "https://example.com"}}},
    {"id": "08", "name": "JSON Formatter API", "subdomain": "json-formatter-api",
     "test": {"method": "POST", "path": "/validate", "json": {"data": '{"a":1}'}}},
    {"id": "09", "name": "Hash Encoding API", "subdomain": "hash-encoding-api",
     "test": {"method": "POST", "path": "/hash", "json": {"text": "hello", "algorithm": "sha256"}}},
    {"id": "10", "name": "Currency Exchange API", "subdomain": "currency-exchange-api",
     "test": {"method": "GET", "path": "/currencies"}},
    {"id": "11", "name": "AI Text API", "subdomain": "ai-text-api",
     "test": {"method": "POST", "path": "/summarize", "json": {"text": "This is a test sentence for summarization."}}},
    {"id": "12", "name": "Social Video API", "subdomain": "social-video-api",
     "test": {"method": "GET", "path": "/platforms"}},
    {"id": "13", "name": "Crypto Data API", "subdomain": "crypto-data-api",
     "test": {"method": "GET", "path": "/global"}},
    {"id": "14", "name": "SEO Analyzer API", "subdomain": "seo-analyzer-api",
     "test": {"method": "GET", "path": "/score", "params": {"url": "https://example.com"}}},
    {"id": "15", "name": "Weather API", "subdomain": "weather-api",
     "test": {"method": "GET", "path": "/current", "params": {"lat": "35.68", "lon": "139.69"}}},
    {"id": "16", "name": "WHOIS Domain API", "subdomain": "whois-domain-api",
     "test": {"method": "GET", "path": "/lookup", "params": {"domain": "google.com"}}},
    {"id": "17", "name": "News Aggregator API", "subdomain": "news-aggregator-api",
     "test": {"method": "GET", "path": "/hackernews/top"}},
    {"id": "18", "name": "AI Translate API", "subdomain": "ai-translate-api",
     "test": {"method": "GET", "path": "/languages"}},
    {"id": "19", "name": "Trends API", "subdomain": "trends-api",
     "test": {"method": "GET", "path": "/github/trending"}},
    {"id": "20", "name": "Company Data API", "subdomain": "company-data-api",
     "test": {"method": "GET", "path": "/search", "params": {"q": "google"}}},
    {"id": "21", "name": "WP Internal Link API", "subdomain": "wp-internal-link-api",
     "test": {"method": "GET", "path": "/health"}},
    {"id": "22", "name": "PDF Generator API", "subdomain": "pdf-generator-api",
     "test": {"method": "GET", "path": "/"}},
    {"id": "23", "name": "Placeholder Image API", "subdomain": "placeholder-image-api",
     "test": {"method": "GET", "path": "/health"}},
    {"id": "24", "name": "Markdown Converter API", "subdomain": "markdown-converter-api",
     "test": {"method": "GET", "path": "/"}},
]


def check_endpoint(url, method="GET", params=None, json_body=None):
    """Hit an endpoint and return (status_code, response_time_ms, error_msg)."""
    try:
        start = time.time()
        if method == "POST":
            r = requests.post(url, json=json_body, timeout=TIMEOUT)
        else:
            r = requests.get(url, params=params, timeout=TIMEOUT)
        elapsed = round((time.time() - start) * 1000)
        return r.status_code, elapsed, None
    except requests.exceptions.Timeout:
        return None, None, "TIMEOUT"
    except requests.exceptions.ConnectionError:
        return None, None, "CONNECTION_ERROR"
    except Exception as e:
        return None, None, str(e)


def main():
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    results = []
    ok_count = 0
    fail_count = 0

    print(f"=== API Health Check: {timestamp} ===\n")

    for api in APIS:
        base_url = f"https://{api['subdomain']}.{BASE_DOMAIN}"

        # 1) Root endpoint
        root_status, root_ms, root_err = check_endpoint(base_url + "/")

        # 2) Functional endpoint
        test = api["test"]
        func_url = base_url + test["path"]
        func_status, func_ms, func_err = check_endpoint(
            func_url,
            method=test.get("method", "GET"),
            params=test.get("params"),
            json_body=test.get("json"),
        )

        root_ok = root_status == 200
        func_ok = func_status is not None and func_status < 500
        all_ok = root_ok and func_ok

        if all_ok:
            ok_count += 1
            status_label = "OK"
        else:
            fail_count += 1
            status_label = "FAIL"

        result = {
            "id": api["id"],
            "name": api["name"],
            "status": status_label,
            "root_status": root_status if root_status else root_err,
            "root_ms": root_ms,
            "func_path": test["path"],
            "func_status": func_status if func_status else func_err,
            "func_ms": func_ms,
        }
        results.append(result)

        # Console output
        root_display = f"{root_status} ({root_ms}ms)" if root_status else root_err
        func_display = f"{func_status} ({func_ms}ms)" if func_status else func_err
        line = f"[{status_label:4s}] {api['id']} {api['name']:<25s} root={root_display:<18s} {test['path']}={func_display}"
        print(line)

        if status_label == "FAIL":
            print(f"  WARNING: {api['name']} has failures!")

    # Summary
    total = ok_count + fail_count
    summary = f"\n--- Summary: {ok_count}/{total} OK, {fail_count} FAILED ---"
    print(summary)

    # Write log (append)
    try:
        with open(LOG_PATH, "a", encoding="utf-8") as f:
            f.write(f"\n{'='*60}\n")
            f.write(f"Health Check: {timestamp}\n")
            f.write(f"Result: {ok_count}/{total} OK, {fail_count} FAILED\n")
            f.write(f"{'-'*60}\n")
            for r in results:
                root_d = f"{r['root_status']} ({r['root_ms']}ms)" if r['root_ms'] else str(r['root_status'])
                func_d = f"{r['func_status']} ({r['func_ms']}ms)" if r['func_ms'] else str(r['func_status'])
                f.write(f"[{r['status']:4s}] {r['id']} {r['name']:<25s} root={root_d:<18s} {r['func_path']}={func_d}\n")
            f.write(f"{'-'*60}\n")
            if fail_count > 0:
                failed = [r for r in results if r['status'] == 'FAIL']
                f.write(f"FAILED APIs: {', '.join(r['name'] for r in failed)}\n")
            f.write(f"{'='*60}\n")
        print(f"\nLog saved to: {LOG_PATH}")
    except Exception as e:
        print(f"\nERROR saving log: {e}")

    # Healthchecks.io ping
    ping_url = HEALTHCHECKS_URL if fail_count == 0 else HEALTHCHECKS_URL + "/fail"
    print(f"Healthchecks.io ping: {ping_url}")
    try:
        requests.get(ping_url, timeout=10)
    except Exception:
        print("WARNING: Failed to ping Healthchecks.io")


if __name__ == "__main__":
    main()
