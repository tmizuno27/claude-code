import Link from 'next/link';
import { getComparisonPairs, getRelatedComparisons, getFeatureLabel } from '@/lib/tools';
import { generateComparisonContent } from '@/lib/comparison';
import AdSlot from '@/components/AdSlot';

export function generateStaticParams() {
  return getComparisonPairs().map(p => ({ slug: p.slug }));
}

export async function generateMetadata({ params }) {
  const { slug } = await params;
  const pair = getComparisonPairs().find(p => p.slug === slug);
  if (!pair) return { title: 'Comparison Not Found' };
  const { toolA, toolB } = pair;
  return {
    title: `${toolA.name} vs ${toolB.name}: Which is Better in 2026?`,
    description: `Detailed comparison of ${toolA.name} and ${toolB.name}. Compare features, pricing, ratings, pros & cons to find the best option for your needs.`,
    alternates: {
      canonical: `/compare/${slug}/`,
    },
    openGraph: {
      title: `${toolA.name} vs ${toolB.name} Comparison`,
      description: `Side-by-side comparison of ${toolA.name} (${toolA.rating?.overall || 0}/10) and ${toolB.name} (${toolB.rating?.overall || 0}/10). Features, pricing, and honest verdict.`,
    },
    twitter: {
      card: 'summary_large_image',
      title: `${toolA.name} vs ${toolB.name}: Which is Better in 2026?`,
      description: `Side-by-side comparison of ${toolA.name} and ${toolB.name}. Features, pricing, and honest verdict.`,
    },
  };
}

export default async function ComparePage({ params }) {
  const { slug } = await params;
  const pair = getComparisonPairs().find(p => p.slug === slug);
  if (!pair) return <div className="container" style={{ padding: '80px 20px' }}>Comparison not found.</div>;

  const { toolA, toolB } = pair;
  const content = generateComparisonContent(toolA, toolB);
  const featureKeys = [...new Set([...Object.keys(toolA.features || {}), ...Object.keys(toolB.features || {})])];
  const relatedA = getRelatedComparisons(toolA.slug, 3);
  const relatedB = getRelatedComparisons(toolB.slug, 3);
  const related = [...relatedA, ...relatedB].filter(r => r.slug !== pair.slug).slice(0, 6);

  const isWinnerA = content.winner.slug === toolA.slug;

  const jsonLd = {
    '@context': 'https://schema.org',
    '@type': 'FAQPage',
    mainEntity: content.faqs.map(faq => ({
      '@type': 'Question',
      name: faq.question,
      acceptedAnswer: {
        '@type': 'Answer',
        text: faq.answer,
      },
    })),
  };

  return (
    <>
      <script
        type="application/ld+json"
        dangerouslySetInnerHTML={{ __html: JSON.stringify(jsonLd) }}
      />
      <div className="compare-header">
        <div className="container">
          <h1>{toolA.name} vs {toolB.name}</h1>
          <p className="subtitle">Comprehensive comparison for 2026 — features, pricing, and verdict</p>
        </div>
      </div>

      <div className="compare-content">
        {/* Score Cards */}
        <div className="score-cards">
          <div className={`score-card${isWinnerA ? ' winner' : ''}`}>
            <h2>{toolA.name}</h2>
            <div className="score">{content.overallA}</div>
            <div className="score-label">Overall Score</div>
            <div className="price-tag">{toolA.pricing_starts || 'Contact'}</div>
            {toolA.free_plan && <span className="badge badge-green" style={{ marginLeft: 8 }}>Free Plan</span>}
            <a
              href={toolA.affiliate_url || toolA.website}
              target="_blank"
              rel={toolA.affiliate_url ? 'sponsored noopener' : 'noopener noreferrer nofollow'}
              className="score-card-cta"
            >
              Try {toolA.name} &rarr;
            </a>
          </div>
          <div className="vs-badge">VS</div>
          <div className={`score-card${!isWinnerA ? ' winner' : ''}`}>
            <h2>{toolB.name}</h2>
            <div className="score">{content.overallB}</div>
            <div className="score-label">Overall Score</div>
            <div className="price-tag">{toolB.pricing_starts || 'Contact'}</div>
            {toolB.free_plan && <span className="badge badge-green" style={{ marginLeft: 8 }}>Free Plan</span>}
            <a
              href={toolB.affiliate_url || toolB.website}
              target="_blank"
              rel={toolB.affiliate_url ? 'sponsored noopener' : 'noopener noreferrer nofollow'}
              className="score-card-cta"
            >
              Try {toolB.name} &rarr;
            </a>
          </div>
        </div>

        {/* Intro */}
        <div className="prose">
          <h2>Overview</h2>
          <p>{content.intro}</p>
        </div>

        {/* Rating Bars */}
        <div className="prose">
          <h2>Ratings Comparison</h2>
        </div>
        <div className="rating-bar-wrap">
          {[
            { label: 'Overall', a: toolA.rating?.overall || 0, b: toolB.rating?.overall || 0 },
            { label: 'Ease of Use', a: toolA.rating?.ease_of_use || 0, b: toolB.rating?.ease_of_use || 0 },
            { label: 'Value', a: toolA.rating?.value || 0, b: toolB.rating?.value || 0 },
          ].map(row => (
            <div className="rating-row" key={row.label}>
              <div className="label">{row.label}</div>
              <div className="rating-bar">
                <div className="fill a" style={{ width: `${(row.a / 10) * 100}%` }} />
              </div>
              <div className="rating-val">{typeof row.a === 'number' ? row.a.toFixed(1) : row.a}</div>
              <div className="rating-bar">
                <div className="fill b" style={{ width: `${(row.b / 10) * 100}%` }} />
              </div>
              <div className="rating-val">{typeof row.b === 'number' ? row.b.toFixed(1) : row.b}</div>
            </div>
          ))}
        </div>

        {/* Feature Table */}
        <div className="prose"><h2>Feature Comparison</h2></div>
        <div className="compare-table-wrap">
          <table className="compare-table">
            <thead>
              <tr>
                <th>Feature</th>
                <th>{toolA.name}</th>
                <th>{toolB.name}</th>
              </tr>
            </thead>
            <tbody>
              {featureKeys.map(key => (
                <tr key={key}>
                  <td>{getFeatureLabel(key)}</td>
                  <td>{toolA.features?.[key] ? <span className="check">Yes</span> : <span className="cross">No</span>}</td>
                  <td>{toolB.features?.[key] ? <span className="check">Yes</span> : <span className="cross">No</span>}</td>
                </tr>
              ))}
              <tr>
                <td>Free Plan</td>
                <td>{toolA.free_plan ? <span className="check">Yes</span> : <span className="cross">No</span>}</td>
                <td>{toolB.free_plan ? <span className="check">Yes</span> : <span className="cross">No</span>}</td>
              </tr>
              <tr>
                <td>Starting Price</td>
                <td>{toolA.pricing_starts}</td>
                <td>{toolB.pricing_starts}</td>
              </tr>
              <tr>
                <td>Founded</td>
                <td>{toolA.founded}</td>
                <td>{toolB.founded}</td>
              </tr>
            </tbody>
          </table>
        </div>

        {/* Feature Analysis */}
        <div className="prose">
          <h2>Feature Analysis</h2>
          <p>{content.featureAnalysis}</p>
        </div>

        {/* Pricing Analysis */}
        <div className="prose">
          <h2>Pricing Breakdown</h2>
          <p>{content.pricingAnalysis}</p>
        </div>

        {/* Pros & Cons */}
        <div className="prose"><h2>Pros &amp; Cons</h2></div>
        <div className="pros-cons">
          <div className="pros-cons-card pros-card">
            <h3>{toolA.name}</h3>
            <ul>
              {(toolA.pros || []).map((p, i) => <li key={i}>{p}</li>)}
            </ul>
            <h3 style={{ marginTop: 16 }}>Cons</h3>
            <ul className="cons-list">
              {(toolA.cons || []).map((c, i) => (
                <li key={i} style={{ color: 'var(--text-secondary)' }}>
                  <span style={{ position: 'absolute', left: 0, color: 'var(--red)', fontWeight: 700 }}>-</span>
                  {c}
                </li>
              ))}
            </ul>
          </div>
          <div className="pros-cons-card pros-card">
            <h3>{toolB.name}</h3>
            <ul>
              {(toolB.pros || []).map((p, i) => <li key={i}>{p}</li>)}
            </ul>
            <h3 style={{ marginTop: 16 }}>Cons</h3>
            <ul className="cons-list">
              {(toolB.cons || []).map((c, i) => (
                <li key={i} style={{ color: 'var(--text-secondary)' }}>
                  <span style={{ position: 'absolute', left: 0, color: 'var(--red)', fontWeight: 700 }}>-</span>
                  {c}
                </li>
              ))}
            </ul>
          </div>
        </div>

        {/* Use Cases */}
        <div className="prose">
          <h2>Who Should Choose Which?</h2>
          <p>{content.useCaseAnalysis}</p>
        </div>

        {/* Verdict */}
        <div className="verdict-box">
          <h2>Our Verdict</h2>
          <p>{content.verdict}</p>
          <div className="verdict-cta">
            <a
              href={content.winner.affiliate_url || content.winner.website}
              target="_blank"
              rel={content.winner.affiliate_url ? 'sponsored noopener' : 'noopener noreferrer nofollow'}
              className="cta-btn cta-btn-winner"
            >
              Try {content.winner.name} — Our Top Pick &rarr;
            </a>
          </div>
        </div>

        {/* CTA Buttons */}
        <div className="cta-buttons">
          <a
            href={toolA.affiliate_url || toolA.website}
            target="_blank"
            rel={toolA.affiliate_url ? 'sponsored noopener' : 'noopener'}
            className="cta-btn cta-btn-a"
          >
            Try {toolA.name} {toolA.free_plan ? '(Free)' : ''} &rarr;
          </a>
          <a
            href={toolB.affiliate_url || toolB.website}
            target="_blank"
            rel={toolB.affiliate_url ? 'sponsored noopener' : 'noopener'}
            className="cta-btn cta-btn-b"
          >
            Try {toolB.name} {toolB.free_plan ? '(Free)' : ''} &rarr;
          </a>
        </div>

        {/* FAQ */}
        <div className="prose"><h2>Frequently Asked Questions</h2></div>
        <div className="faq-list">
          {content.faqs.map((faq, i) => (
            <div className="faq-item" key={i}>
              <div className="faq-q">{faq.question}</div>
              <div className="faq-a">{faq.answer}</div>
            </div>
          ))}
        </div>

        {/* Related Comparisons */}
        {related.length > 0 && (
          <div className="prose">
            <h2>Related Comparisons</h2>
            <div className="related-grid">
              {related.map(r => (
                <Link href={`/compare/${r.slug}/`} key={r.slug} className="comparison-link">
                  {r.toolA.name} <span className="vs">vs</span> {r.toolB.name}
                </Link>
              ))}
            </div>
          </div>
        )}

        {/* Tool Links */}
        <div className="prose" style={{ marginBottom: 60 }}>
          <h2>Learn More</h2>
          <p>
            <Link href={`/tool/${toolA.slug}/`}>{toolA.name} details</Link>
            {' | '}
            <Link href={`/tool/${toolB.slug}/`}>{toolB.name} details</Link>
            {' | '}
            <Link href={`/category/${pair.category}/`}>All {pair.category.replace(/-/g, ' ')} tools</Link>
          </p>
        </div>
      </div>
    </>
  );
}
