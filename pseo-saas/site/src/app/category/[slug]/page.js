import Link from 'next/link';
import { getCategoryList, getCategoryBySlug, getToolsByCategory, getComparisonPairs } from '@/lib/tools';

export function generateStaticParams() {
  return getCategoryList().map(c => ({ slug: c.slug }));
}

export async function generateMetadata({ params }) {
  const { slug } = await params;
  const cat = getCategoryBySlug(slug);
  if (!cat) return { title: 'Category Not Found' };
  return {
    title: `Best ${cat.name} Tools Compared (2026)`,
    description: `Compare the top ${cat.name.toLowerCase()} tools side-by-side. Features, pricing, and ratings for ${cat.tools.length} tools.`,
  };
}

export default async function CategoryPage({ params }) {
  const { slug } = await params;
  const cat = getCategoryBySlug(slug);
  if (!cat) return <div className="container" style={{ padding: '80px 20px' }}>Category not found.</div>;

  const tools = getToolsByCategory(params.slug);
  const pairs = getComparisonPairs().filter(p => p.category === params.slug);

  return (
    <>
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
