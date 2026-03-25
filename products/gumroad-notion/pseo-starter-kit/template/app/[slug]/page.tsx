import type { Metadata } from 'next';
import {
  getAllItems,
  getItemBySlug,
  getRelatedItems,
} from '@/lib/data';
import { ItemCard } from '@/components/ItemCard';

interface PageProps {
  params: Promise<{ slug: string }>;
}

export async function generateStaticParams() {
  const items = getAllItems();
  return items.map((item) => ({
    slug: item.slug,
  }));
}

export async function generateMetadata({ params }: PageProps): Promise<Metadata> {
  const { slug } = await params;
  const item = getItemBySlug(slug);
  if (!item) {
    return { title: 'Not Found' };
  }
  return {
    title: item.title,
    description: item.metaDescription,
    openGraph: {
      title: item.title,
      description: item.metaDescription,
      type: 'article',
    },
    alternates: {
      canonical: `https://yourdomain.com/${item.slug}/`,
    },
  };
}

export default async function ItemPage({ params }: PageProps) {
  const { slug } = await params;
  const item = getItemBySlug(slug);

  if (!item) {
    return <h1>Page not found</h1>;
  }

  const related = getRelatedItems(item, 4);

  // Structured data (JSON-LD)
  const jsonLd = {
    '@context': 'https://schema.org',
    '@type': 'Article',
    headline: item.title,
    description: item.metaDescription,
    datePublished: item.createdAt,
    dateModified: item.updatedAt,
  };

  return (
    <div>
      <script
        type="application/ld+json"
        dangerouslySetInnerHTML={{ __html: JSON.stringify(jsonLd) }}
      />

      {/* Breadcrumb */}
      <nav style={{ fontSize: '14px', color: '#666', marginBottom: '24px' }}>
        <a href="/" style={{ color: '#0066cc', textDecoration: 'none' }}>
          Home
        </a>
        {' > '}
        <span style={{ textTransform: 'capitalize' }}>{item.category}</span>
        {' > '}
        <span>{item.title.split('—')[0].trim()}</span>
      </nav>

      <h1 style={{ fontSize: '28px', lineHeight: 1.3, marginBottom: '16px' }}>
        {item.title}
      </h1>

      <p
        style={{
          fontSize: '16px',
          lineHeight: 1.7,
          color: '#333',
          marginBottom: '32px',
        }}
      >
        {item.description}
      </p>

      {/* Attributes Table */}
      <h2 style={{ fontSize: '20px', marginBottom: '12px' }}>Comparison</h2>
      <table
        style={{
          width: '100%',
          borderCollapse: 'collapse',
          marginBottom: '40px',
        }}
      >
        <tbody>
          {Object.entries(item.attributes).map(([key, value]) => (
            <tr key={key}>
              <td
                style={{
                  padding: '10px 16px',
                  borderBottom: '1px solid #e5e5e5',
                  fontWeight: 600,
                  textTransform: 'capitalize',
                  width: '30%',
                  backgroundColor: '#f9f9f9',
                }}
              >
                {key.replace(/_/g, ' ')}
              </td>
              <td
                style={{
                  padding: '10px 16px',
                  borderBottom: '1px solid #e5e5e5',
                }}
              >
                {String(value)}
              </td>
            </tr>
          ))}
        </tbody>
      </table>

      {/* AdSense Placeholder */}
      {/* <div style={{ margin: '32px 0', textAlign: 'center', padding: '20px', background: '#f5f5f5', color: '#999' }}>Ad Unit</div> */}

      {/* Related Items */}
      {related.length > 0 && (
        <section>
          <h2 style={{ fontSize: '20px', marginBottom: '16px' }}>
            Related Comparisons
          </h2>
          <div
            style={{
              display: 'grid',
              gridTemplateColumns: 'repeat(auto-fill, minmax(250px, 1fr))',
              gap: '12px',
            }}
          >
            {related.map((r) => (
              <ItemCard key={r.slug} item={r} />
            ))}
          </div>
        </section>
      )}

      <p style={{ marginTop: '40px', fontSize: '12px', color: '#999' }}>
        Last updated: {item.updatedAt}
      </p>
    </div>
  );
}
