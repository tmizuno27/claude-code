"""Generate sitemap.xml for pSEO site from out/ directory."""
import os
from pathlib import Path

BASE_URL = "https://ai-tool-compare.vercel.app"
OUT_DIR = Path(r"c:\Users\tmizu\マイドライブ\GitHub\claude-code\pseo-saas\site\out")
TODAY = "2026-03-19"

def get_priority(url_path: str) -> str:
    if url_path == "/":
        return "1.0"
    if url_path.startswith("/category/"):
        return "0.8"
    if url_path.startswith("/tool/"):
        return "0.7"
    if url_path.startswith("/compare/"):
        return "0.5"
    return "0.5"

urls = []
for root, dirs, files in os.walk(OUT_DIR):
    # Skip _next, 404, _not-found
    dirs[:] = [d for d in dirs if d not in ("_next", "404", "_not-found")]
    for f in files:
        if f != "index.html":
            continue
        full = Path(root) / f
        rel = full.parent.relative_to(OUT_DIR)
        url_path = "/" if str(rel) == "." else f"/{rel.as_posix()}/"
        urls.append(url_path)

# Also check for non-index html at root (skip 404.html)
for f in OUT_DIR.glob("*.html"):
    if f.name in ("404.html", "index.html"):
        continue
    url_path = f"/{f.stem}/"
    urls.append(url_path)

urls.sort()

lines = ['<?xml version="1.0" encoding="UTF-8"?>']
lines.append('<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">')
for url_path in urls:
    loc = f"{BASE_URL}{url_path}" if url_path != "/" else BASE_URL + "/"
    pri = get_priority(url_path)
    lines.append(f"""  <url>
    <loc>{loc}</loc>
    <lastmod>{TODAY}</lastmod>
    <changefreq>weekly</changefreq>
    <priority>{pri}</priority>
  </url>""")
lines.append("</urlset>")

sitemap_path = OUT_DIR / "sitemap.xml"
sitemap_path.write_text("\n".join(lines), encoding="utf-8")

# Count by type
cats = {"top": 0, "category": 0, "tool": 0, "compare": 0, "other": 0}
for u in urls:
    if u == "/":
        cats["top"] += 1
    elif u.startswith("/category/"):
        cats["category"] += 1
    elif u.startswith("/tool/"):
        cats["tool"] += 1
    elif u.startswith("/compare/"):
        cats["compare"] += 1
    else:
        cats["other"] += 1

print(f"sitemap.xml generated: {sitemap_path}")
print(f"Total URLs: {len(urls)}")
for k, v in cats.items():
    print(f"  {k}: {v}")
