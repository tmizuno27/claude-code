import Link from 'next/link';
import { getCategories, getPopularCalculators, getAllCalculators } from '@/lib/utils/data';

export default function HomePage() {
  const categories = getCategories();
  const popularCalcs = getPopularCalculators();
  const totalCalcs = getAllCalculators().length;

  return (
    <>
      <section className="hero">
        <h1>あらゆる計算を、もっと簡単に。</h1>
        <p>住宅ローン、税金、BMI、日数計算など、暮らしに役立つ計算ツールを無料で。</p>
      </section>

      <div className="stats-bar">
        <div className="stat-item">
          <div className="stat-number">{totalCalcs}+</div>
          <div className="stat-label">計算ツール</div>
        </div>
        <div className="stat-item">
          <div className="stat-number">{categories.length}</div>
          <div className="stat-label">カテゴリ</div>
        </div>
        <div className="stat-item">
          <div className="stat-number">0円</div>
          <div className="stat-label">完全無料</div>
        </div>
      </div>

      <div className="container">
        <section>
          <h2 className="section-title">人気の計算ツール</h2>
          <div className="calculator-grid">
            {popularCalcs.map(calc => (
              <Link
                key={calc.slug}
                href={`/${calc.category}/${calc.slug}/`}
                className="calculator-card"
              >
                <h4>{calc.title}</h4>
                <p>{calc.description}</p>
              </Link>
            ))}
          </div>
        </section>

        <section style={{ marginTop: '3rem' }}>
          <h2 className="section-title">カテゴリ一覧</h2>
          <div className="category-grid">
            {categories.map(cat => (
              <Link
                key={cat.slug}
                href={`/${cat.slug}/`}
                className="category-card"
              >
                <div className="category-card-icon">{cat.icon}</div>
                <h3>{cat.name}</h3>
                <p>{cat.description}</p>
              </Link>
            ))}
          </div>
        </section>
      </div>
    </>
  );
}
