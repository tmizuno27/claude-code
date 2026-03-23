import Link from 'next/link';
import { getTools, getCategoryList, getComparisonPairs } from '@/lib/tools';

export default function HomePage() {
  const tools = getTools();
  const categories = getCategoryList();
  const pairs = getComparisonPairs();
  const topPairs = pairs.slice(0, 10);

  return (
    <>
      <section className="hero">
        <div className="container">
          <h1>Find the Best AI Tool for You</h1>
          <p>
            Detailed side-by-side comparisons of the top AI and SaaS tools.
            Data-driven analysis to help you make the right choice.
          </p>
          <div className="hero-stats">
            <div className="hero-stat">
              <div className="num">{tools.length}</div>
              <div className="label">Tools Analyzed</div>
            </div>
            <div className="hero-stat">
              <div className="num">{pairs.length}</div>
              <div className="label">Comparisons</div>
            </div>
            <div className="hero-stat">
              <div className="num">{categories.length}</div>
              <div className="label">Categories</div>
            </div>
          </div>
        </div>
      </section>

      <section className="section" id="categories">
        <div className="container">
          <h2 className="section-title">Browse by Category</h2>
          <div className="category-grid">
            {categories.map(cat => (
              <Link href={`/category/${cat.slug}/`} key={cat.slug} className="category-card">
                <span className="category-emoji">{cat.emoji}</span>
                <div className="category-info">
                  <h3>{cat.name}</h3>
                  <p>{cat.tools.length} tools</p>
                </div>
              </Link>
            ))}
          </div>
        </div>
      </section>

      <section className="section" id="comparisons">
        <div className="container">
          <h2 className="section-title">Popular Comparisons</h2>
          <div className="comparison-grid">
            {topPairs.map(pair => (
              <Link href={`/compare/${pair.slug}/`} key={pair.slug} className="comparison-link">
                {pair.toolA.name} <span className="vs">vs</span> {pair.toolB.name}
              </Link>
            ))}
          </div>
        </div>
      </section>
    </>
  );
}
