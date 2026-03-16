#!/usr/bin/env node
/**
 * Generates sitemap.xml from tools.json data.
 * Run after `next build` — outputs to site/out/sitemap.xml
 */
const fs = require('fs');
const path = require('path');

const DOMAIN = 'https://aitoolvs.com'; // TODO: replace with actual domain
const dataPath = path.join(__dirname, '..', 'data', 'tools.json');
const outPath = path.join(__dirname, '..', 'site', 'out', 'sitemap.xml');

const tools = JSON.parse(fs.readFileSync(dataPath, 'utf-8'));
const categories = [...new Set(tools.map(t => t.category))];

// Generate comparison pairs (same logic as tools.js)
const pairs = [];
for (const cat of categories) {
  const catTools = tools.filter(t => t.category === cat).sort((a, b) => a.slug.localeCompare(b.slug));
  for (let i = 0; i < catTools.length; i++) {
    for (let j = i + 1; j < catTools.length; j++) {
      pairs.push(`${catTools[i].slug}-vs-${catTools[j].slug}`);
    }
  }
}

const today = new Date().toISOString().split('T')[0];

const urls = [
  { loc: '/', priority: '1.0', changefreq: 'weekly' },
  ...categories.map(c => ({ loc: `/category/${c}/`, priority: '0.8', changefreq: 'weekly' })),
  ...tools.map(t => ({ loc: `/tool/${t.slug}/`, priority: '0.7', changefreq: 'monthly' })),
  ...pairs.map(p => ({ loc: `/compare/${p}/`, priority: '0.6', changefreq: 'monthly' })),
];

const xml = `<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
${urls.map(u => `  <url>
    <loc>${DOMAIN}${u.loc}</loc>
    <lastmod>${today}</lastmod>
    <changefreq>${u.changefreq}</changefreq>
    <priority>${u.priority}</priority>
  </url>`).join('\n')}
</urlset>`;

fs.mkdirSync(path.dirname(outPath), { recursive: true });
fs.writeFileSync(outPath, xml);
console.log(`Sitemap generated: ${urls.length} URLs → ${outPath}`);
