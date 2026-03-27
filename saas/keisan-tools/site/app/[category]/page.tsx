import { notFound } from 'next/navigation';
import Link from 'next/link';
import type { Metadata } from 'next';
import { getCategories, getCalculatorsByCategory } from '@/lib/utils/data';
import Breadcrumb from '@/components/ui/Breadcrumb';
import JsonLd from '@/components/seo/JsonLd';
import AdSlot from '@/components/ads/AdSlot';

interface Props {
  params: Promise<{ category: string }>;
}

export async function generateStaticParams() {
  const categories = getCategories();
  return categories.map(cat => ({ category: cat.slug }));
}

export async function generateMetadata({ params }: Props): Promise<Metadata> {
  const { category } = await params;
  const categories = getCategories();
  const cat = categories.find(c => c.slug === category);
  if (!cat) return {};
  return {
    title: `${cat.name}の計算ツール｜keisan.tools`,
    description: cat.description,
    alternates: {
      canonical: `/${category}/`,
    },
  };
}

export default async function CategoryPage({ params }: Props) {
  const { category } = await params;
  const categories = getCategories();
  const cat = categories.find(c => c.slug === category);
  if (!cat) notFound();

  const calculators = getCalculatorsByCategory(category);

  // Group by subcategory
  const grouped: Record<string, typeof calculators> = {};
  for (const calc of calculators) {
    const key = calc.subcategory;
    if (!grouped[key]) grouped[key] = [];
    grouped[key].push(calc);
  }

  const breadcrumbJsonLd = {
    '@context': 'https://schema.org',
    '@type': 'BreadcrumbList',
    itemListElement: [
      { '@type': 'ListItem', position: 1, name: 'ホーム', item: 'https://keisan-tools.com/' },
      { '@type': 'ListItem', position: 2, name: cat.name },
    ],
  };

  return (
    <div className="container">
      <JsonLd data={breadcrumbJsonLd} />
      <Breadcrumb items={[{ label: cat.name }]} />

      <h1 className="section-title">
        {cat.icon} {cat.name}
      </h1>
      <p style={{ marginBottom: '2rem', color: 'var(--gray-500)' }}>
        {cat.description}
      </p>

      {cat.subcategories.map(sub => {
        const calcs = grouped[sub.slug];
        if (!calcs || calcs.length === 0) return null;
        return (
          <div key={sub.slug}>
            <h2 className="subcategory-header">{sub.name}</h2>
            <div className="calculator-grid">
              {calcs.map(calc => (
                <Link
                  key={calc.slug}
                  href={`/${category}/${calc.slug}/`}
                  className="calculator-card"
                >
                  <h4>{calc.title}</h4>
                  <p>{calc.description}</p>
                </Link>
              ))}
            </div>
          </div>
        );
      })}

      <AdSlot position="in-article" format="horizontal" />

      {calculators.length === 0 && (
        <p style={{ color: 'var(--gray-400)', textAlign: 'center', padding: '3rem 0' }}>
          このカテゴリの計算ツールは準備中です。
        </p>
      )}
    </div>
  );
}
