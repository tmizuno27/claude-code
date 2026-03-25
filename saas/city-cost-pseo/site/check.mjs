import { readFileSync } from 'fs';
const c = JSON.parse(readFileSync('./data/cities.json', 'utf8'));
const slugs = c.map(x => x.slug);
const unique = [...new Set(slugs)];
const dupes = slugs.filter((s, i) => slugs.indexOf(s) !== i);
console.log('Total:', c.length, 'Unique:', unique.length, 'Dupes:', JSON.stringify(dupes));
