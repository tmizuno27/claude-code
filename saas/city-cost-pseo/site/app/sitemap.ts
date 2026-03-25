export const dynamic = 'force-static';

import { cities, getAllRegions, getAllComparisons } from '@/lib/data';
import type { MetadataRoute } from 'next';

const BASE = 'https://citylivingcost.com';

export default function sitemap(): MetadataRoute.Sitemap {
  const now = new Date().toISOString();

  const staticPages = [
    { url: BASE, lastModified: now, changeFrequency: 'weekly' as const, priority: 1.0 },
  ];

  const cityPages = cities.map(c => ({
    url: `${BASE}/cities/${c.slug}`,
    lastModified: now,
    changeFrequency: 'monthly' as const,
    priority: 0.8,
  }));

  const regionPages = getAllRegions().map(r => ({
    url: `${BASE}/region/${r}`,
    lastModified: now,
    changeFrequency: 'monthly' as const,
    priority: 0.7,
  }));

  const comparePages = getAllComparisons().map(({ city1, city2 }) => ({
    url: `${BASE}/compare/${city1}-vs-${city2}`,
    lastModified: now,
    changeFrequency: 'monthly' as const,
    priority: 0.6,
  }));

  return [...staticPages, ...cityPages, ...regionPages, ...comparePages];
}
