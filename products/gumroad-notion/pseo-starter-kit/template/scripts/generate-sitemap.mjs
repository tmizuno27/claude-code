/**
 * Sitemap generator for pSEO sites
 * Run after build: node scripts/generate-sitemap.mjs
 *
 * Reads data/items.example.json and generates sitemap.xml in the output directory.
 * Supports sitemap index for sites with 50,000+ URLs.
 */

import { readFileSync, writeFileSync, existsSync } from 'fs';
import { join, dirname } from 'path';
import { fileURLToPath } from 'url';

const __dirname = dirname(fileURLToPath(import.meta.url));
const ROOT = join(__dirname, '..');
const SITE_URL = process.env.SITE_URL || 'https://yourdomain.com';
const MAX_URLS_PER_SITEMAP = 50000;

// Load items
const itemsPath = join(ROOT, 'data', 'items.example.json');
const items = JSON.parse(readFileSync(itemsPath, 'utf-8'));

// Determine output dir
const outDir = existsSync(join(ROOT, 'out')) ? join(ROOT, 'out') : join(ROOT, 'public');

// Build URL list
const urls = [
  { loc: '/', lastmod: new Date().toISOString().split('T')[0], priority: '1.0' },
  ...items.map((item) => ({
    loc: `/${item.slug}/`,
    lastmod: item.updatedAt || new Date().toISOString().split('T')[0],
    priority: '0.8',
  })),
];

function buildSitemap(urlList) {
  const entries = urlList
    .map(
      (u) => `  <url>
    <loc>${SITE_URL}${u.loc}</loc>
    <lastmod>${u.lastmod}</lastmod>
    <priority>${u.priority}</priority>
  </url>`
    )
    .join('\n');

  return `<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
${entries}
</urlset>`;
}

if (urls.length <= MAX_URLS_PER_SITEMAP) {
  writeFileSync(join(outDir, 'sitemap.xml'), buildSitemap(urls), 'utf-8');
  console.log(`Sitemap generated: ${urls.length} URLs → ${outDir}/sitemap.xml`);
} else {
  // Split into multiple sitemaps with an index
  const chunks = [];
  for (let i = 0; i < urls.length; i += MAX_URLS_PER_SITEMAP) {
    chunks.push(urls.slice(i, i + MAX_URLS_PER_SITEMAP));
  }

  const indexEntries = chunks
    .map((_, i) => {
      const filename = `sitemap-${i + 1}.xml`;
      writeFileSync(join(outDir, filename), buildSitemap(chunks[i]), 'utf-8');
      return `  <sitemap>
    <loc>${SITE_URL}/${filename}</loc>
    <lastmod>${new Date().toISOString().split('T')[0]}</lastmod>
  </sitemap>`;
    })
    .join('\n');

  const sitemapIndex = `<?xml version="1.0" encoding="UTF-8"?>
<sitemapindex xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
${indexEntries}
</sitemapindex>`;

  writeFileSync(join(outDir, 'sitemap.xml'), sitemapIndex, 'utf-8');
  console.log(
    `Sitemap index generated: ${urls.length} URLs across ${chunks.length} sitemaps → ${outDir}/`
  );
}
