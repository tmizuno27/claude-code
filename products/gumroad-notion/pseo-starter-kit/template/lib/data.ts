import itemsData from '@/data/items.example.json';

export interface Item {
  slug: string;
  title: string;
  category: string;
  description: string;
  metaDescription: string;
  attributes: Record<string, string | number>;
  relatedSlugs?: string[];
  createdAt: string;
  updatedAt: string;
}

const items: Item[] = itemsData as Item[];

export function getAllItems(): Item[] {
  return items;
}

export function getItemBySlug(slug: string): Item | undefined {
  return items.find((item) => item.slug === slug);
}

export function getItemsByCategory(category: string): Item[] {
  return items.filter((item) => item.category === category);
}

export function getAllCategories(): string[] {
  const categories = new Set(items.map((item) => item.category));
  return Array.from(categories).sort();
}

export function getRelatedItems(item: Item, count: number = 6): Item[] {
  if (item.relatedSlugs && item.relatedSlugs.length > 0) {
    const related = item.relatedSlugs
      .map((slug) => getItemBySlug(slug))
      .filter((i): i is Item => i !== undefined);
    if (related.length >= count) return related.slice(0, count);
  }

  return items
    .filter((i) => i.slug !== item.slug && i.category === item.category)
    .slice(0, count);
}

export function getAllSlugs(): string[] {
  return items.map((item) => item.slug);
}
