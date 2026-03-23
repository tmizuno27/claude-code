const fs = require('fs');
const path = require('path');

const DOMAIN = 'https://ai-tool-compare-nu.vercel.app';
const TODAY = new Date().toISOString().split('T')[0];

const toolsPath = path.join(__dirname, '..', 'data', 'tools.json');
const tools = JSON.parse(fs.readFileSync(toolsPath, 'utf-8'));

// Build category map
const categoryMap = {};
for (const tool of tools) {
  if (!categoryMap[tool.category]) categoryMap[tool.category] = [];
  categoryMap[tool.category].push(tool);
}

const urls = [];

function addUrl(loc, priority, changefreq = 'weekly') {
  urls.push(`  <url>\n    <loc>${DOMAIN}${loc}</loc>\n    <lastmod>${TODAY}</lastmod>\n    <changefreq>${changefreq}</changefreq>\n    <priority>${priority}</priority>\n  </url>`);
}

// Home
addUrl('/', '1.0', 'daily');

// Categories
for (const catSlug of Object.keys(categoryMap)) {
  addUrl(`/category/${catSlug}/`, '0.8');
}

// Tool pages
for (const tool of tools) {
  addUrl(`/tool/${tool.slug}/`, '0.7');
}

// Comparison pages (same logic as getComparisonPairs)
for (const catSlug of Object.keys(categoryMap)) {
  const catTools = categoryMap[catSlug];
  for (let i = 0; i < catTools.length; i++) {
    for (let j = i + 1; j < catTools.length; j++) {
      const [a, b] = [catTools[i], catTools[j]].sort((x, y) => x.slug.localeCompare(y.slug));
      addUrl(`/compare/${a.slug}-vs-${b.slug}/`, '0.6');
    }
  }
}

const sitemap = `<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
${urls.join('\n')}
</urlset>
`;

const outDir = path.join(__dirname, 'public');
if (!fs.existsSync(outDir)) fs.mkdirSync(outDir, { recursive: true });

const outPath = path.join(outDir, 'sitemap.xml');
fs.writeFileSync(outPath, sitemap, 'utf-8');

console.log(`Sitemap generated: ${urls.length} URLs`);
console.log(`  Home: 1`);
console.log(`  Categories: ${Object.keys(categoryMap).length}`);
console.log(`  Tools: ${tools.length}`);
console.log(`  Comparisons: ${urls.length - 1 - Object.keys(categoryMap).length - tools.length}`);
console.log(`Output: ${outPath}`);
