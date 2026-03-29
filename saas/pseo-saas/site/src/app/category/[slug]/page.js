import Link from 'next/link';
import { getCategoryList, getCategoryBySlug, getToolsByCategory, getComparisonPairs } from '@/lib/tools';

export function generateStaticParams() {
  return getCategoryList().map(c => ({ slug: c.slug }));
}

export async function generateMetadata({ params }) {
  const { slug } = await params;
  const cat = getCategoryBySlug(slug);
  if (!cat) return { title: 'Category Not Found' };
  const toolCount = cat.tools.length;
  const pairCount = getComparisonPairs().filter(p => p.category === slug).length;
  return {
    title: `Best ${cat.name} Tools in 2026 — ${toolCount} Tools Compared`,
    description: `We analyzed ${toolCount} ${cat.name.toLowerCase()} tools across ${pairCount} comparisons. See rankings, pricing, features & expert picks to find the best tool for your needs.`,
    alternates: {
      canonical: `/category/${slug}/`,
    },
    openGraph: {
      title: `Best ${cat.name} Tools (2026): Top ${toolCount} Compared`,
      description: `Compare ${toolCount} ${cat.name.toLowerCase()} tools side-by-side. Features, pricing, and ratings updated for 2026.`,
    },
  };
}

export default async function CategoryPage({ params }) {
  const { slug } = await params;
  const cat = getCategoryBySlug(slug);
  if (!cat) return <div className="container" style={{ padding: '80px 20px' }}>Category not found.</div>;

  const tools = getToolsByCategory(slug);
  const pairs = getComparisonPairs().filter(p => p.category === slug);

  const breadcrumbLd = {
    '@context': 'https://schema.org',
    '@type': 'BreadcrumbList',
    itemListElement: [
      { '@type': 'ListItem', position: 1, name: 'Home', item: 'https://ai-tool-compare-nu.vercel.app/' },
      { '@type': 'ListItem', position: 2, name: cat.name },
    ],
  };

  return (
    <>
      <script type="application/ld+json" dangerouslySetInnerHTML={{ __html: JSON.stringify(breadcrumbLd) }} />
      <div className="cat-header">
        <div className="container">
          <h1>{cat.emoji} {cat.name}</h1>
          <p>{cat.description} — {tools.length} tools, {pairs.length} comparisons</p>
        </div>
      </div>

      <div className="container">
        <div className="section">
          <h2 className="section-title">All {cat.name} Tools</h2>
          <div className="tools-grid">
            {tools.map(tool => (
              <Link href={`/tool/${tool.slug}/`} key={tool.slug} className="tool-card">
                <h3>{tool.name}</h3>
                <p className="tool-tagline">{tool.tagline}</p>
                <div className="tool-card-meta">
                  <span>Rating: {tool.rating?.overall || 0}/10</span>
                  <span>{tool.pricing_starts}</span>
                  {tool.free_plan && <span className="badge badge-green">Free</span>}
                </div>
              </Link>
            ))}
          </div>
        </div>

        <div className="section">
          <h2 className="section-title">All Comparisons</h2>
          <div className="comparison-grid">
            {pairs.map(pair => (
              <Link href={`/compare/${pair.slug}/`} key={pair.slug} className="comparison-link">
                {pair.toolA.name} <span className="vs">vs</span> {pair.toolB.name}
              </Link>
            ))}
          </div>
        </div>
      </div>
    </>
  );
}
