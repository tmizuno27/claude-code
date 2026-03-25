# pSEO Site Builder — Template

A production-ready Next.js template for building programmatic SEO sites that generate hundreds or thousands of static pages from structured data.

## Quick Start

```bash
npm install
npm run dev
```

Open http://localhost:3000 to see the example site.

## How to Customize

### 1. Replace the Data

Edit `data/items.example.json` with your own items. Each item needs at minimum:

```json
{
  "slug": "unique-url-slug",
  "title": "Page Title — With Keyword",
  "category": "your-category",
  "description": "200+ character description unique to this item.",
  "metaDescription": "150 character meta description for search results.",
  "attributes": { "key": "value pairs for comparison table" },
  "createdAt": "2026-01-01",
  "updatedAt": "2026-03-01"
}
```

### 2. Customize the Page Template

Edit `app/[slug]/page.tsx` to match your content type. The default template includes:
- Breadcrumb navigation
- Title and description
- Attributes comparison table
- Related items section
- JSON-LD structured data

### 3. Update Site Info

Search and replace these placeholders across all files:
- `YourSiteName` → Your actual site name
- `yourdomain.com` → Your actual domain
- `Your site description` → Your actual description

### 4. Build and Deploy

```bash
npm run build    # Generates static pages + sitemap
npm start        # Preview locally
```

Deploy to Vercel:
1. Push to GitHub
2. Import at vercel.com
3. Done — it auto-detects Next.js

## File Structure

```
app/
  layout.tsx        → Root layout (header, footer, global meta)
  page.tsx          → Homepage (lists all items by category)
  [slug]/page.tsx   → Dynamic item pages (one per data item)
components/
  ItemCard.tsx      → Reusable card for item listings
data/
  items.example.json → YOUR DATA GOES HERE
lib/
  data.ts           → Data loading and filtering utilities
scripts/
  generate-sitemap.mjs → Auto-generates sitemap.xml after build
public/
  robots.txt        → Search engine directives
```

## Adding More Page Types

### Category Pages

Create `app/category/[category]/page.tsx` with its own `generateStaticParams` to build category hub pages.

### Comparison Pages (X vs Y)

Create `app/compare/[pair]/page.tsx` and generate all valid pairs from your dataset.

### Calculator Pages

Create `app/calculate/[params]/page.tsx` with pre-filled parameter combinations.

## SEO Checklist

- [ ] Every page has a unique `<title>` and `<meta description>`
- [ ] JSON-LD structured data on every page
- [ ] Sitemap submitted to Google Search Console
- [ ] Internal links between related pages
- [ ] Canonical URLs set on all pages
- [ ] Robots.txt allows crawling
- [ ] Page load time under 2 seconds

## Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `SITE_URL` | `https://yourdomain.com` | Used in sitemap generation |
