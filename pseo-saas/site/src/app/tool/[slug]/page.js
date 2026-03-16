import Link from 'next/link';
import { getTools, getToolBySlug, getRelatedComparisons, getFeatureLabel, getCategoryBySlug } from '@/lib/tools';

export function generateStaticParams() {
  return getTools().map(t => ({ slug: t.slug }));
}

export async function generateMetadata({ params }) {
  const { slug } = await params;
  const tool = getToolBySlug(slug);
  if (!tool) return { title: 'Tool Not Found' };
  return {
    title: `${tool.name} Review — Features, Pricing & Ratings (2026)`,
    description: `${tool.name}: ${tool.tagline}. Starting at ${tool.pricing_starts}. See features, pros, cons, and comparisons.`,
  };
}

export default async function ToolPage({ params }) {
  const { slug } = await params;
  const tool = getToolBySlug(slug);
  if (!tool) return <div className="container" style={{ padding: '80px 20px' }}>Tool not found.</div>;

  const comparisons = getRelatedComparisons(tool.slug, 20);
  const cat = getCategoryBySlug(tool.category);
  const featureKeys = Object.keys(tool.features || {});

  return (
    <>
      <div className="tool-header">
        <div className="container">
          <h1>{tool.name}</h1>
          <p className="tagline">{tool.tagline}</p>
          <div className="tool-meta">
            <div className="tool-meta-item">
              <span className="val">{tool.rating?.overall || 0}/10</span>
              <span className="lbl">Overall Rating</span>
            </div>
            <div className="tool-meta-item">
              <span className="val">{tool.rating?.ease_of_use || 0}/10</span>
              <span className="lbl">Ease of Use</span>
            </div>
            <div className="tool-meta-item">
              <span className="val">{tool.pricing_starts}</span>
              <span className="lbl">Starting Price</span>
            </div>
            <div className="tool-meta-item">
              <span className="val">{tool.founded}</span>
              <span className="lbl">Founded</span>
            </div>
            {tool.free_plan && (
              <div className="tool-meta-item">
                <span className="badge badge-green">Free Plan Available</span>
              </div>
            )}
          </div>
        </div>
      </div>

      <div className="tool-content">
        <div className="prose">
          <h2>About {tool.name}</h2>
          <p>
            {tool.name} is a {cat?.name?.toLowerCase() || 'software'} platform founded in {tool.founded}.
            It positions itself as &ldquo;{tool.tagline}&rdquo; and is best suited for{' '}
            {(tool.best_for || []).map(b => b.replace(/-/g, ' ')).join(', ')}.
            Pricing starts at {tool.pricing_starts}{tool.free_plan ? ', and a free plan is available' : ''}.
          </p>
        </div>

        {/* Features */}
        <div className="prose"><h2>Features</h2></div>
        <div className="compare-table-wrap">
          <table className="compare-table">
            <thead>
              <tr><th>Feature</th><th>Available</th></tr>
            </thead>
            <tbody>
              {featureKeys.map(key => (
                <tr key={key}>
                  <td>{getFeatureLabel(key)}</td>
                  <td>{tool.features[key] ? <span className="check">Yes</span> : <span className="cross">No</span>}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>

        {/* Pros & Cons */}
        <div className="prose"><h2>Pros &amp; Cons</h2></div>
        <div className="pros-cons">
          <div className="pros-cons-card pros-card">
            <h3>Pros</h3>
            <ul>
              {(tool.pros || []).map((p, i) => <li key={i}>{p}</li>)}
            </ul>
          </div>
          <div className="pros-cons-card cons-card">
            <h3>Cons</h3>
            <ul>
              {(tool.cons || []).map((c, i) => <li key={i}>{c}</li>)}
            </ul>
          </div>
        </div>

        {/* Comparisons */}
        {comparisons.length > 0 && (
          <div className="section">
            <h2 className="section-title">Compare {tool.name} With Others</h2>
            <div className="comparison-grid">
              {comparisons.map(pair => (
                <Link href={`/compare/${pair.slug}/`} key={pair.slug} className="comparison-link">
                  {pair.toolA.name} <span className="vs">vs</span> {pair.toolB.name}
                </Link>
              ))}
            </div>
          </div>
        )}

        <div className="prose" style={{ marginBottom: 60 }}>
          <p>
            <Link href={`/category/${tool.category}/`}>Back to {cat?.name || 'category'}</Link>
            {' | '}
            <a href={tool.website} target="_blank" rel="noopener noreferrer nofollow">
              Visit {tool.name} website
            </a>
          </p>
        </div>
      </div>
    </>
  );
}
