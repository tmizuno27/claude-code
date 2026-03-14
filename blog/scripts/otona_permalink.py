import urllib.request, json, base64, ssl
BASE = "https://otona-match.com/?rest_route="
AUTH = base64.b64encode(b"t.mizuno27@gmail.com:Yw4j OgFf wwzT o0mn wXQ9 TjYs").decode()
ctx = ssl.create_default_context()

data = json.dumps({"permalink_structure": "/%postname%/"}).encode("utf-8")
req = urllib.request.Request(BASE + "/wp/v2/settings", data=data, method="POST")
req.add_header("Content-Type", "application/json; charset=utf-8")
req.add_header("Authorization", f"Basic {AUTH}")
try:
    with urllib.request.urlopen(req, context=ctx, timeout=30) as resp:
        r = json.loads(resp.read())
        print(f"Permalink: {r.get('permalink_structure', 'N/A')}")
except Exception as e:
    print(f"Error: {e}")
