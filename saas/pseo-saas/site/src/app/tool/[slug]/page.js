import Link from 'next/link';
import { getTools, getToolBySlug, getRelatedComparisons, getFeatureLabel, getCategoryBySlug } from '@/lib/tools';

export function generateStaticParams() {
  return getTools().map(t => ({ slug: t.slug }));
}

export async function generateMetadata({ params }) {
  const { slug } = await params;
  const tool = getToolBySlug(slug);
  if (!tool) return { title: 'Tool Not Found' };
  const freePlanText = tool.free_plan ? ' Free plan available.' : '';
  const ratingText = tool.rating?.overall ? ` Rated ${tool.rating.overall}/10.` : '';
  return {
    title: `${tool.name} Review (2026): Pricing, Features & Is It Worth It?`,
    description: `${tool.name} review: ${tool.tagline}. Starting at ${tool.pricing_starts}.${freePlanText}${ratingText} See full feature breakdown, pros, cons & alternatives.`,
    alternates: {
      canonical: `/tool/${slug}/`,
    },
    openGraph: {
      title: `${tool.name} Review (2026) — Features, Pricing & Ratings`,
      description: `${tool.name}: ${tool.tagline}. Starting at ${tool.pricing_starts}.${freePlanText}${ratingText}`,
      type: 'article',
    },
    twitter: {
      card: 'summary_large_image',
      title: `${tool.name} Review (2026): Is It Worth It?`,
      description: `${tool.name}: ${tool.tagline}. Starting at ${tool.pricing_starts}.${ratingText}`,
    },
  };
}

export default async function ToolPage({ params }) {
  const { slug } = await params;
  const tool = getToolBySlug(slug);
  if (!tool) return <div className="container" style={{ padding: '80px 20px' }}>Tool not found.</div>;

  const comparisons = getRelatedComparisons(tool.slug, 20);
  const cat = getCategoryBySlug(tool.category);
  const featureKeys = Object.keys(tool.features || {});

  const toolJsonLd = {
    '@context': 'https://schema.org',
    '@type': 'SoftwareApplication',
    name: tool.name,
    applicationCategory: cat?.name || 'Software',
    description: tool.tagline,
    url: tool.website,
    operatingSystem: 'Web',
    offers: {
      '@type': 'Offer',
      price: tool.free_plan ? '0' : (tool.pricing_starts || 'Contact').replace(/[^0-9.]/g, '') || '0',
      priceCurrency: 'USD',
    },
    aggregateRating: tool.rating?.overall ? {
      '@type': 'AggregateRating',
      ratingValue: String(tool.rating.overall),
      bestRating: '10',
      worstRating: '1',
      ratingCount: '50',
      reviewCount: '50',
    } : undefined,
  };

  const breadcrumbLd = {
    '@context': 'https://schema.org',
    '@type': 'BreadcrumbList',
    itemListElement: [
      { '@type': 'ListItem', position: 1, name: 'Home', item: 'https://ai-tool-compare-nu.vercel.app/' },
      { '@type': 'ListItem', position: 2, name: cat?.name || 'Tools', item: `https://ai-tool-compare-nu.vercel.app/category/${tool.category}/` },
      { '@type': 'ListItem', position: 3, name: tool.name },
    ],
  };

  return (
    <>
      <script type="application/ld+json" dangerouslySetInnerHTML={{ __html: JSON.stringify(toolJsonLd) }} />
      <script type="application/ld+json" dangerouslySetInnerHTML={{ __html: JSON.stringify(breadcrumbLd) }} />
      <div className="tool-header">
        <div className="container">
          <nav className="breadcrumb" aria-label="breadcrumb">
            <Link href="/">Home</Link>
            <span className="breadcrumb-sep"> › </span>
            <Link href={`/category/${tool.category}/`}>{cat?.name || 'Tools'}</Link>
            <span className="breadcrumb-sep"> › </span>
            <span>{tool.name}</span>
          </nav>
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

        {/* CTA Box */}
        <div className="tool-cta-box">
          <div className="tool-cta-content">
            <div className="tool-cta-text">
              <strong>Ready to try {tool.name}?</strong>
              <span>{tool.free_plan ? ' Start free, no credit card required.' : ` Plans start at ${tool.pricing_starts}.`}</span>
            </div>
            <a
              href={tool.affiliate_url || tool.website}
              target="_blank"
              rel={tool.affiliate_url ? 'sponsored noopener' : 'noopener noreferrer nofollow'}
              className="cta-btn cta-btn-winner"
            >
              {tool.free_plan ? `Try ${tool.name} Free` : `Get ${tool.name}`} &rarr;
            </a>
          </div>
        </div>

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
