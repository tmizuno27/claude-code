/**
 * Generate sitemap.xml for the currency converter site
 * Run after build: node scripts/generate-sitemap.mjs
 */
import { readFileSync, writeFileSync } from 'fs';
import { join, dirname } from 'path';
import { fileURLToPath } from 'url';

const __dirname = dirname(fileURLToPath(import.meta.url));
const SITE_URL = 'https://currencyrate.page';

const currencies = JSON.parse(
  readFileSync(join(__dirname, '..', 'data', 'currencies.json'), 'utf-8')
);
const codes = currencies.map(c => c.code);

const staticPages = ['', 'about/', 'privacy/', 'terms/'];

const pairs = [];
for (const from of codes) {
  for (const to of codes) {
    if (from !== to) {
      pairs.push(`${from.toLowerCase()}-to-${to.toLowerCase()}/`);
    }
  }
}

const today = new Date().toISOString().slice(0, 10);

let xml = `<?xml version="1.0" encoding="UTF-8"?>\n`;
xml += `<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n`;

for (const page of staticPages) {
  xml += `  <url>\n    <loc>${SITE_URL}/${page}</loc>\n    <lastmod>${today}</lastmod>\n    <changefreq>daily</changefreq>\n    <priority>${page === '' ? '1.0' : '0.5'}</priority>\n  </url>\n`;
}

for (const pair of pairs) {
  xml += `  <url>\n    <loc>${SITE_URL}/${pair}</loc>\n    <lastmod>${today}</lastmod>\n    <changefreq>daily</changefreq>\n    <priority>0.8</priority>\n  </url>\n`;
}

xml += `</urlset>\n`;

const outPath = join(__dirname, '..', 'public', 'sitemap.xml');
writeFileSync(outPath, xml);
console.log(`Sitemap generated: ${staticPages.length + pairs.length} URLs → public/sitemap.xml`);
