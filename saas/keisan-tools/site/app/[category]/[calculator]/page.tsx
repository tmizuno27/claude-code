import { notFound } from 'next/navigation';
import Link from 'next/link';
import type { Metadata } from 'next';
import {
  getCategories,
  getAllCalculators,
  getCalculator,
  findCalculatorBySlug,
} from '@/lib/utils/data';
import Breadcrumb from '@/components/ui/Breadcrumb';
import CalculatorClient from '@/components/calculator/CalculatorClient';
import FAQ from '@/components/ui/FAQ';
import AdSlot from '@/components/ads/AdSlot';
import JsonLd from '@/components/seo/JsonLd';

interface Props {
  params: Promise<{ category: string; calculator: string }>;
}

export async function generateStaticParams() {
  const allCalcs = getAllCalculators();
  return allCalcs.map(c => ({
    category: c.category,
    calculator: c.slug,
  }));
}

export async function generateMetadata({ params }: Props): Promise<Metadata> {
  const { category, calculator } = await params;
  const calc = getCalculator(category, calculator);
  if (!calc) return {};
  return {
    title: `${calc.metaTitle || calc.title}｜keisan.tools`,
    description: calc.metaDescription || calc.description,
    alternates: {
      canonical: `/${category}/${calculator}/`,
    },
  };
}

export default async function CalculatorPage({ params }: Props) {
  const { category, calculator } = await params;
  const categories = getCategories();
  const cat = categories.find(c => c.slug === category);
  const calc = getCalculator(category, calculator);

  if (!cat || !calc) notFound();

  // Resolve related calculators
  const relatedCalcs = calc.related
    .map(slug => findCalculatorBySlug(slug))
    .filter(Boolean);

  // Structured data
  const faqJsonLd = calc.faq.length > 0 ? {
    '@context': 'https://schema.org',
    '@type': 'FAQPage',
    mainEntity: calc.faq.map(item => ({
      '@type': 'Question',
      name: item.question,
      acceptedAnswer: {
        '@type': 'Answer',
        text: item.answer,
      },
    })),
  } : null;

  const webAppJsonLd = {
    '@context': 'https://schema.org',
    '@type': 'WebApplication',
    name: calc.title,
    description: calc.description,
    url: `https://keisan-tools.com/${category}/${calculator}/`,
    applicationCategory: 'UtilityApplication',
    operatingSystem: 'All',
    offers: {
      '@type': 'Offer',
      price: '0',
      priceCurrency: 'JPY',
    },
  };

  const breadcrumbJsonLd = {
    '@context': 'https://schema.org',
    '@type': 'BreadcrumbList',
    itemListElement: [
      { '@type': 'ListItem', position: 1, name: 'ホーム', item: 'https://keisan-tools.com/' },
      { '@type': 'ListItem', position: 2, name: cat.name, item: `https://keisan-tools.com/${category}/` },
      { '@type': 'ListItem', position: 3, name: calc.title },
    ],
  };

  return (
    <div className="container">
      <JsonLd data={webAppJsonLd} />
      <JsonLd data={breadcrumbJsonLd} />
      {faqJsonLd && <JsonLd data={faqJsonLd} />}
      <Breadcrumb
        items={[
          { label: cat.name, href: `/${category}/` },
          { label: calc.title },
        ]}
      />

      <div className="calculator-page">
        <div className="calculator-main">
          <CalculatorClient
            title={calc.seo?.h1 || calc.title}
            description={calc.description}
            calculatorFunction={calc.calculatorFunction}
            inputs={calc.inputs}
            outputs={calc.outputs}
          />

          <AdSlot position="after-result" />

          {calc.explanation && (
            <div className="content-section">
              <h2>計算方法の解説</h2>
              <div dangerouslySetInnerHTML={{ __html: calc.explanation }} />
            </div>
          )}

          <FAQ items={calc.faq} />

          {calc.affiliate && (
            <div className="content-section">
              <h2>おすすめ</h2>
              <p>{calc.affiliate.text}</p>
            </div>
          )}
        </div>

        <aside className="calculator-sidebar">
          <AdSlot position="sidebar-top" />

          {relatedCalcs.length > 0 && (
            <div className="content-section">
              <h2>関連する計算ツール</h2>
              <div className="related-list">
                {relatedCalcs.map(rc =>
                  rc ? (
                    <Link
                      key={rc.slug}
                      href={`/${rc.category}/${rc.slug}/`}
                      className="related-link"
                    >
                      {rc.title}
                    </Link>
                  ) : null
                )}
              </div>
            </div>
          )}

          <AdSlot position="sidebar-bottom" />
        </aside>
      </div>
    </div>
  );
}
