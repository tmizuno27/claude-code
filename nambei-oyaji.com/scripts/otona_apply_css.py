"""Apply Apple-style CSS to otona-match.com via Cocoon custom CSS widget"""
import urllib.request
import urllib.error
import json
import base64
import ssl

BASE = "https://otona-match.com/?rest_route="
AUTH = base64.b64encode(b"t.mizuno27@gmail.com:Yw4j OgFf wwzT o0mn wXQ9 TjYs").decode()
ctx = ssl.create_default_context()

def wp_post(endpoint, data):
    body = json.dumps(data).encode('utf-8')
    req = urllib.request.Request(BASE + endpoint, data=body, method='POST')
    req.add_header('Content-Type', 'application/json; charset=utf-8')
    req.add_header('Authorization', f'Basic {AUTH}')
    try:
        with urllib.request.urlopen(req, context=ctx, timeout=30) as resp:
            return json.loads(resp.read())
    except urllib.error.HTTPError as e:
        print(f"Error {e.code}: {e.read().decode()[:300]}")
        return None

def wp_get(endpoint):
    req = urllib.request.Request(BASE + endpoint)
    req.add_header('Authorization', f'Basic {AUTH}')
    try:
        with urllib.request.urlopen(req, context=ctx, timeout=30) as resp:
            return json.loads(resp.read())
    except Exception as e:
        print(f"GET Error: {e}")
        return None

# Check existing sidebars/widgets
print("=== Checking sidebars ===")
sidebars = wp_get("/wp/v2/sidebars")
if sidebars:
    for s in sidebars:
        print(f"  {s['id']}: {s.get('name','')}")

# Create custom HTML widget with global CSS
CSS = """<style>
/* ============================================
   大人のマッチングナビ — Apple-Style Design
   ============================================ */
:root {
  --text-primary: #1d1d1f;
  --text-secondary: #86868b;
  --bg-white: #fff;
  --bg-gray: #f5f5f7;
  --link-blue: #0066CC;
  --link-blue-hover: #0077ED;
  --btn-blue: #0071e3;
  --border-light: #d2d2d7;
  --sf-pro: "Meiryo","Hiragino Kaku Gothic ProN","Hiragino Sans",sans-serif;
  --transition: 0.3s ease;
  --card-radius: 18px;
}

/* ===== GLOBAL RESET ===== */
body {
  font-family: var(--sf-pro) !important;
  color: var(--text-primary) !important;
  -webkit-font-smoothing: antialiased !important;
}

/* ===== HEADER — Frosted Glass ===== */
.header, #header, .header-in {
  background: rgba(255,255,255,0.92) !important;
  backdrop-filter: blur(20px) !important;
  -webkit-backdrop-filter: blur(20px) !important;
  border-bottom: 1px solid rgba(0,0,0,0.08) !important;
  position: sticky !important;
  top: 0 !important;
  z-index: 9999 !important;
}
.header-in {
  display: flex !important;
  align-items: center !important;
  justify-content: space-between !important;
  max-width: 1200px !important;
  margin: 0 auto !important;
  padding: 8px 20px !important;
}
.logo-header img, .site-name-text {
  font-size: 18px !important;
  font-weight: 700 !important;
  color: var(--text-primary) !important;
}
#navi .navi-in > ul > li > a {
  color: var(--text-primary) !important;
  font-size: 13px !important;
  font-weight: 500 !important;
  padding: 8px 14px !important;
  transition: color var(--transition) !important;
}
#navi .navi-in > ul > li > a:hover {
  color: var(--link-blue) !important;
}
@media (max-width: 768px) {
  #navi { display: none !important; }
}

/* ===== FOOTER ===== */
#footer, .footer, .footer-bottom {
  background: #1d1d1f !important;
  color: #86868b !important;
}
#footer a, .footer a {
  color: #d2d2d7 !important;
}
.footer-bottom-content {
  max-width: 1200px !important;
  margin: 0 auto !important;
  padding: 20px !important;
  text-align: center !important;
}

/* ===== CONTENT AREA ===== */
#content-in {
  max-width: 1200px !important;
  margin: 0 auto !important;
  padding: 30px 20px !important;
}

/* ===== ARTICLE CARDS (archive/index) ===== */
.entry-card-wrap {
  border: 1px solid var(--border-light) !important;
  border-radius: var(--card-radius) !important;
  overflow: hidden !important;
  transition: transform var(--transition), box-shadow var(--transition) !important;
  background: #fff !important;
  margin-bottom: 20px !important;
}
.entry-card-wrap:hover {
  transform: translateY(-2px) !important;
  box-shadow: 0 8px 30px rgba(0,0,0,0.08) !important;
}
.entry-card-thumb img {
  border-radius: 0 !important;
}
.entry-card-title {
  font-size: 17px !important;
  font-weight: 700 !important;
  line-height: 1.6 !important;
  color: var(--text-primary) !important;
}
.entry-card-snippet {
  color: var(--text-secondary) !important;
  font-size: 13px !important;
  line-height: 1.8 !important;
}

/* ===== SINGLE ARTICLE ===== */
body.single .article {
  max-width: 750px !important;
  margin: 0 auto !important;
}
body.single .entry-title {
  font-size: 28px !important;
  font-weight: 800 !important;
  line-height: 1.5 !important;
  color: var(--text-primary) !important;
  text-align: center !important;
  margin-bottom: 20px !important;
}
body.single .entry-content {
  font-size: 16px !important;
  line-height: 2.4 !important;
  color: var(--text-primary) !important;
}
body.single .entry-content h2 {
  font-size: 24px !important;
  font-weight: 800 !important;
  text-align: center !important;
  margin: 60px 0 30px !important;
  padding: 0 !important;
  border: none !important;
  background: none !important;
  color: var(--text-primary) !important;
}
body.single .entry-content h3 {
  font-size: 20px !important;
  font-weight: 700 !important;
  margin: 40px 0 20px !important;
  padding: 0 0 0 16px !important;
  border-left: 4px solid var(--link-blue) !important;
  border-bottom: none !important;
  background: none !important;
}
body.single .entry-content h4 {
  font-size: 17px !important;
  font-weight: 700 !important;
  margin: 30px 0 15px !important;
}
body.single .entry-content a {
  color: var(--link-blue) !important;
  text-decoration: none !important;
}
body.single .entry-content a:hover {
  text-decoration: underline !important;
}

/* ===== MARKER HIGHLIGHTS ===== */
.marker-yellow { background: linear-gradient(transparent 60%, #fff9c4 60%) !important; }
.marker-pink { background: linear-gradient(transparent 60%, #fce4ec 60%) !important; }
.marker-blue { background: linear-gradient(transparent 60%, #e3f2fd 60%) !important; }

/* ===== SIDEBAR ===== */
#sidebar .widget {
  border: 1px solid var(--border-light) !important;
  border-radius: var(--card-radius) !important;
  padding: 20px !important;
  margin-bottom: 20px !important;
  background: #fff !important;
}
#sidebar .widget-title {
  font-size: 14px !important;
  font-weight: 700 !important;
  color: var(--text-primary) !important;
  margin-bottom: 12px !important;
  padding: 0 !important;
  border: none !important;
  background: none !important;
}

/* ===== BREADCRUMB ===== */
.breadcrumb {
  font-size: 12px !important;
  color: var(--text-secondary) !important;
  max-width: 1200px !important;
  margin: 0 auto !important;
  padding: 10px 20px !important;
}

/* ===== HIDE COCOON DEFAULTS ===== */
.sns-share, .sns-follow { display: none !important; }
body.single .under-entry-content .sns-share { display: none !important; }

/* ===== PAGINATION ===== */
.pagination .page-numbers {
  border-radius: 50% !important;
  width: 40px !important;
  height: 40px !important;
  line-height: 40px !important;
  border: 1px solid var(--border-light) !important;
  color: var(--text-primary) !important;
  transition: all var(--transition) !important;
}
.pagination .page-numbers.current {
  background: var(--link-blue) !important;
  color: #fff !important;
  border-color: var(--link-blue) !important;
}

/* ===== RESPONSIVE ===== */
@media (max-width: 834px) {
  body.single .article { max-width: 100% !important; padding: 0 16px !important; }
  body.single .entry-title { font-size: 22px !important; }
  body.single .entry-content h2 { font-size: 20px !important; }
}
@media (max-width: 600px) {
  body.single .entry-content { font-size: 15px !important; line-height: 2.2 !important; }
}

/* ===== COMPARISON TABLE ===== */
.wp-block-table table {
  border-collapse: collapse !important;
  width: 100% !important;
  border-radius: 12px !important;
  overflow: hidden !important;
}
.wp-block-table th {
  background: var(--bg-gray) !important;
  font-weight: 700 !important;
  padding: 12px 16px !important;
  font-size: 14px !important;
}
.wp-block-table td {
  padding: 12px 16px !important;
  border-bottom: 1px solid var(--border-light) !important;
  font-size: 14px !important;
}

/* ===== COCOON BOX/CALLOUT ===== */
.blank-box, .information-box, .question-box, .alert-box {
  border-radius: 12px !important;
  border-width: 1px !important;
  padding: 20px !important;
}

/* ===== LIST STYLE FIX ===== */
.entry-content ul { list-style: none !important; padding-left: 0 !important; }
.entry-content ul li { position: relative !important; padding-left: 1.5em !important; margin-bottom: 0.5em !important; }
.entry-content ul li::before { content: "•" !important; position: absolute !important; left: 0.3em !important; color: var(--link-blue) !important; font-weight: bold !important; }
.entry-content ol { list-style: decimal !important; padding-left: 1.5em !important; }
.entry-content ol li { margin-bottom: 0.5em !important; }
.entry-content ol li::before { content: none !important; }
</style>

<script>
document.addEventListener('DOMContentLoaded', function() {
  // Rewrite header nav for dating site
  var headerIn = document.querySelector('.header-in');
  if (headerIn) {
    var navi = headerIn.querySelector('#navi .navi-in ul');
    if (navi) {
      navi.innerHTML = '<li><a href="/category/matching-apps/">マッチングアプリ</a></li>'
        + '<li><a href="/category/deaikei/">出会い系サイト</a></li>'
        + '<li><a href="/category/konkatsu/">婚活</a></li>'
        + '<li><a href="/category/renai-technique/">恋愛テクニック</a></li>'
        + '<li><a href="/category/safety/">安全対策</a></li>'
        + '<li><a href="/category/reviews/">体験談</a></li>';
    }
  }
});
</script>"""

print("=== Creating CSS Widget ===")
# Try to create a widget in sidebar
widget_data = {
    "id": "custom_html-2",
    "sidebar": "sidebar-1",
    "instance": {
        "raw": {
            "title": "",
            "content": CSS
        }
    }
}
result = wp_post("/wp/v2/widgets", widget_data)
if result and "id" in result:
    print(f"  Widget created: {result['id']}")
else:
    # Try alternate widget creation
    widget_data2 = {
        "sidebar": "sidebar-1",
        "id_base": "custom_html",
        "instance": {
            "raw": {
                "title": "",
                "content": CSS
            }
        }
    }
    result2 = wp_post("/wp/v2/widgets", widget_data2)
    if result2 and "id" in result2:
        print(f"  Widget created (alt): {result2['id']}")
    else:
        print("  Widget creation failed. Trying page approach...")
        # Create as a page with CSS
        page_data = {
            "title": "Global CSS",
            "content": CSS,
            "status": "draft",
            "slug": "global-css"
        }
        result3 = wp_post("/wp/v2/pages", page_data)
        if result3:
            print(f"  CSS page created as draft (ID:{result3['id']})")

# Set permalink structure
print("\n=== Setting Permalink ===")
options = wp_get("/wp/v2/settings")
if options:
    print(f"  Current title: {options.get('title', 'N/A')}")

# Update site title
print("\n=== Updating Site Settings ===")
settings = wp_post("/wp/v2/settings", {
    "title": "大人のマッチングナビ",
    "description": "30代・40代のための出会い系・マッチングアプリ徹底比較ガイド"
})
if settings:
    print(f"  Title: {settings.get('title', 'N/A')}")
    print(f"  Description: {settings.get('description', 'N/A')}")

print("\nDone!")
