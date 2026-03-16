import { getTools, getCategoryList, getComparisonPairs } from '@/lib/tools';

const BASE_URL = 'https://aitoolcompare.com';

export default function sitemap() {
  const tools = getTools();
  const categories = getCategoryList();
  const pairs = getComparisonPairs();
  const now = new Date().toISOString();

  const entries = [
    { url: BASE_URL, lastModified: now, changeFrequency: 'weekly', priority: 1.0 },
  ];

  for (const cat of categories) {
    entries.push({
      url: `${BASE_URL}/category/${cat.slug}/`,
      lastModified: now,
      changeFrequency: 'weekly',
      priority: 0.8,
    });
  }

  for (const tool of tools) {
    entries.push({
      url: `${BASE_URL}/tool/${tool.slug}/`,
      lastModified: now,
      changeFrequency: 'monthly',
      priority: 0.7,
    });
  }

  for (const pair of pairs) {
    entries.push({
      url: `${BASE_URL}/compare/${pair.slug}/`,
      lastModified: now,
      changeFrequency: 'monthly',
      priority: 0.6,
    });
  }

  return entries;
}
