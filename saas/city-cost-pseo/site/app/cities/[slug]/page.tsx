import { cities, getCityBySlug, getTotalMonthlyCost } from '@/lib/data';
import type { Metadata } from 'next';
import { notFound } from 'next/navigation';

interface Props {
  params: Promise<{ slug: string }>;
}

export async function generateStaticParams() {
  return cities.map(c => ({ slug: c.slug }));
}

export async function generateMetadata({ params }: Props): Promise<Metadata> {
  const { slug } = await params;
  const city = getCityBySlug(slug);
  if (!city) return {};
  return {
    title: `Cost of Living in ${city.name}, ${city.country}`,
    description: `Monthly living costs in ${city.name}: rent $${city.costs.rent1br_center}, meals from $${city.costs.meal_inexpensive}, utilities $${city.costs.utilities}. Complete breakdown.`,
  };
}

const costLabels: Record<string, string> = {
  rent1br_center: '1BR Apartment (City Center)',
  rent1br_outside: '1BR Apartment (Outside Center)',
  meal_inexpensive: 'Inexpensive Restaurant Meal',
  meal_mid: 'Mid-Range Restaurant (2 people)',
  monthly_pass: 'Monthly Transit Pass',
  utilities: 'Utilities (Electricity, Water, etc.)',
  internet: 'Internet (60 Mbps+)',
  groceries_monthly: 'Groceries (Monthly)',
};

export default async function CityPage({ params }: Props) {
  const { slug } = await params;
  const city = getCityBySlug(slug);
  if (!city) notFound();

  const total = getTotalMonthlyCost(city);
  const costEntries = Object.entries(city.costs) as Array<[string, number]>;
  const maxCost = Math.max(...costEntries.map(([, v]) => v));

  const compareCities = cities
    .filter(c => c.slug !== city.slug)
    .slice(0, 4);

  return (
    <>
      <div className="breadcrumb">
        <a href="/">Home</a> &rarr; <a href={`/region/${city.region}`}>{city.region}</a> &rarr; {city.name}
      </div>

      <div className="page-header">
        <h1>Cost of Living in {city.name}, {city.country}</h1>
        <p>{city.description}</p>
      </div>

      <div className="card" style={{ marginBottom: 24 }}>
        <div style={{ display: 'flex', justifyContent: 'space-between', flexWrap: 'wrap', gap: 16 }}>
          <div>
            <div style={{ fontSize: '0.85rem', color: 'var(--text-secondary)' }}>Estimated Monthly Cost</div>
            <div style={{ fontSize: '2rem', fontWeight: 700, color: 'var(--primary)' }}>${total.toLocaleString()}</div>
          </div>
          <div>
            <div style={{ fontSize: '0.85rem', color: 'var(--text-secondary)' }}>Avg. Monthly Salary</div>
            <div style={{ fontSize: '2rem', fontWeight: 700 }}>${city.salary_avg_monthly.toLocaleString()}</div>
          </div>
          <div>
            <div style={{ fontSize: '0.85rem', color: 'var(--text-secondary)' }}>Safety Index</div>
            <div style={{ fontSize: '2rem', fontWeight: 700 }}>{city.safety_index}/100</div>
          </div>
        </div>
      </div>

      <h2 style={{ marginBottom: 16 }}>Cost Breakdown</h2>
      <div className="bar-chart">
        {costEntries.map(([key, value]) => (
          <div key={key} className="bar-row">
            <div className="bar-label">{costLabels[key] ?? key}</div>
            <div className="bar-track">
              <div
                className="bar-fill city1"
                style={{ width: `${Math.max((value / maxCost) * 100, 8)}%` }}
              >
                ${value}
              </div>
            </div>
          </div>
        ))}
      </div>

      <table className="cost-table">
        <thead>
          <tr><th>Category</th><th>Monthly Cost (USD)</th></tr>
        </thead>
        <tbody>
          {costEntries.map(([key, value]) => (
            <tr key={key}>
              <td>{costLabels[key] ?? key}</td>
              <td className="cost-value">${value.toLocaleString()}</td>
            </tr>
          ))}
        </tbody>
      </table>

      {city.tips.length > 0 && (
        <>
          <h2 style={{ marginTop: 32, marginBottom: 16 }}>Tips for Living in {city.name}</h2>
          <ul className="tips-list">
            {city.tips.map((tip, i) => <li key={i}>{tip}</li>)}
          </ul>
        </>
      )}

      <div className="affiliate-box">
        <h3>Planning to Move to {city.name}?</h3>
        <p>Save on international transfers with Wise. Get a VPN for secure browsing. Compare travel insurance plans.</p>
      </div>

      <h2 style={{ marginTop: 32, marginBottom: 16 }}>Compare {city.name} With Other Cities</h2>
      <div className="city-grid">
        {compareCities.map(c => (
          <a key={c.slug} href={`/compare/${city.slug}-vs-${c.slug}`} className="card city-card">
            <div className="city-name">{city.name} vs {c.name}</div>
            <div className="city-country">{c.country}</div>
            <div className="city-cost">${getTotalMonthlyCost(c).toLocaleString()}/mo</div>
          </a>
        ))}
      </div>
    </>
  );
}
