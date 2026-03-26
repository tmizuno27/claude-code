import Link from 'next/link';
import { getCategories, getPopularCalculators, getAllCalculators } from '@/lib/utils/data';

export default function HomePage() {
  const categories = getCategories();
  const popularCalcs = getPopularCalculators().slice(0, 6);
  const totalCalcs = getAllCalculators().length;

  return (
    <>
      {/* Hero Section - Apple-style full-width */}
      <section className="home-hero">
        <div className="home-hero-inner">
          <p className="home-hero-eyebrow">無料オンライン計算ツール</p>
          <h1 className="home-hero-title">
            あらゆる計算を、
            <br />
            もっと簡単に。
          </h1>
          <p className="home-hero-subtitle">
            住宅ローン、税金、BMI、日数計算など
            <br />
            暮らしに役立つ{totalCalcs}種類以上の計算ツールを完全無料で提供。
          </p>
          <div className="home-hero-cta">
            <Link href="#categories" className="home-btn-primary">
              カテゴリを見る
            </Link>
            <Link href="#popular" className="home-btn-secondary">
              人気ツール
            </Link>
          </div>
        </div>
      </section>

      {/* Stats - Floating cards */}
      <section className="home-stats">
        <div className="home-stats-inner">
          <div className="home-stat-card">
            <span className="home-stat-number">{totalCalcs}+</span>
            <span className="home-stat-label">計算ツール</span>
          </div>
          <div className="home-stat-card">
            <span className="home-stat-number">{categories.length}</span>
            <span className="home-stat-label">カテゴリ</span>
          </div>
          <div className="home-stat-card">
            <span className="home-stat-number">0円</span>
            <span className="home-stat-label">完全無料</span>
          </div>
        </div>
      </section>

      {/* Popular Calculators */}
      <section id="popular" className="home-section">
        <div className="container">
          <div className="home-section-header">
            <p className="home-section-eyebrow">Popular</p>
            <h2 className="home-section-title">人気の計算ツール</h2>
            <p className="home-section-desc">
              多くのユーザーに利用されている定番ツールをピックアップ。
            </p>
          </div>
          <div className="home-popular-grid">
            {popularCalcs.map((calc, i) => (
              <Link
                key={calc.slug}
                href={`/${calc.category}/${calc.slug}/`}
                className={`home-popular-card ${i === 0 ? 'home-popular-card--featured' : ''}`}
              >
                <div className="home-popular-card-inner">
                  <span className="home-popular-badge">
                    {categories.find(c => c.slug === calc.category)?.icon || '📊'}
                  </span>
                  <h3 className="home-popular-card-title">{calc.title}</h3>
                  <p className="home-popular-card-desc">{calc.description}</p>
                  <span className="home-popular-card-arrow">→</span>
                </div>
              </Link>
            ))}
          </div>
        </div>
      </section>

      {/* Categories */}
      <section id="categories" className="home-section home-section--dark">
        <div className="container">
          <div className="home-section-header">
            <p className="home-section-eyebrow home-section-eyebrow--light">Categories</p>
            <h2 className="home-section-title home-section-title--light">カテゴリ一覧</h2>
            <p className="home-section-desc home-section-desc--light">
              目的に合ったカテゴリから、ぴったりの計算ツールを見つけよう。
            </p>
          </div>
          <div className="home-category-grid">
            {categories.map(cat => (
              <Link
                key={cat.slug}
                href={`/${cat.slug}/`}
                className="home-category-card"
              >
                <div className="home-category-icon">{cat.icon}</div>
                <h3 className="home-category-name">{cat.name}</h3>
                <p className="home-category-desc">{cat.description}</p>
                <span className="home-category-link">
                  詳しく見る →
                </span>
              </Link>
            ))}
          </div>
        </div>
      </section>

      {/* CTA Section */}
      <section className="home-cta-section">
        <div className="home-cta-inner">
          <h2 className="home-cta-title">
            今すぐ計算を始めよう。
          </h2>
          <p className="home-cta-desc">
            登録不要・完全無料。必要な計算ツールがきっと見つかります。
          </p>
          <Link href="#categories" className="home-btn-primary home-btn-primary--large">
            計算ツールを探す
          </Link>
        </div>
      </section>
    </>
  );
}
