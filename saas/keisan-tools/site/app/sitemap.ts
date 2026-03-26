import type { MetadataRoute } from 'next';
import { getAllCalculators, getCategories } from '@/lib/utils/data';

const BASE_URL = 'https://keisan-tools.com';

export default function sitemap(): MetadataRoute.Sitemap {
  const categories = getCategories();
  const calculators = getAllCalculators();

  const staticPages: MetadataRoute.Sitemap = [
    { url: `${BASE_URL}/`, lastModified: new Date(), changeFrequency: 'weekly', priority: 1.0 },
    { url: `${BASE_URL}/about/`, lastModified: new Date(), changeFrequency: 'monthly', priority: 0.3 },
    { url: `${BASE_URL}/privacy/`, lastModified: new Date(), changeFrequency: 'monthly', priority: 0.2 },
    { url: `${BASE_URL}/terms/`, lastModified: new Date(), changeFrequency: 'monthly', priority: 0.2 },
    { url: `${BASE_URL}/contact/`, lastModified: new Date(), changeFrequency: 'monthly', priority: 0.2 },
  ];

  const categoryPages: MetadataRoute.Sitemap = categories.map(cat => ({
    url: `${BASE_URL}/${cat.slug}/`,
    lastModified: new Date(),
    changeFrequency: 'weekly' as const,
    priority: 0.8,
  }));

  const calculatorPages: MetadataRoute.Sitemap = calculators.map(calc => ({
    url: `${BASE_URL}/${calc.category}/${calc.slug}/`,
    lastModified: new Date(),
    changeFrequency: 'monthly' as const,
    priority: calc.popular ? 0.9 : 0.6,
  }));

  return [...staticPages, ...categoryPages, ...calculatorPages];
}
