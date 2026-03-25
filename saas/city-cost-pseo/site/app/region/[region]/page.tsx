import { cities, getAllRegions, getCitiesByRegion, getRegionLabel, getTotalMonthlyCost } from '@/lib/data';
import type { Metadata } from 'next';
import { notFound } from 'next/navigation';

interface Props {
  params: Promise<{ region: string }>;
}

export async function generateStaticParams() {
  return getAllRegions().map(r => ({ region: r }));
}

export async function generateMetadata({ params }: Props): Promise<Metadata> {
  const { region } = await params;
  const label = getRegionLabel(region);
  return {
    title: `Cost of Living in ${label} — City Comparison`,
    description: `Compare living costs across cities in ${label}. Rent, food, transport and more.`,
  };
}

function safetyClass(index: number): string {
  if (index >= 70) return 'safety-high';
  if (index >= 50) return 'safety-mid';
  return 'safety-low';
}

export default async function RegionPage({ params }: Props) {
  const { region } = await params;
  const regionCities = getCitiesByRegion(region);
  if (regionCities.length === 0) notFound();

  const label = getRegionLabel(region);
  const sorted = [...regionCities].sort((a, b) => getTotalMonthlyCost(a) - getTotalMonthlyCost(b));
  const avgCost = Math.round(sorted.reduce((s, c) => s + getTotalMonthlyCost(c), 0) / sorted.length);
  const allRegions = getAllRegions();

  return (
    <>
      <div className="breadcrumb">
        <a href="/">Home</a> &rarr; {label}
      </div>

      <div className="page-header">
        <h1>Cost of Living in {label}</h1>
        <p>{sorted.length} cities. Average estimated monthly cost: ${avgCost.toLocaleString()}.</p>
      </div>

      <div className="region-grid">
        {allRegions.map(r => (
          <a key={r} href={`/region/${r}`} className={`card region-card${r === region ? ' active' : ''}`}
            style={r === region ? { background: 'var(--primary-light)', borderColor: 'var(--primary)' } : {}}>
            {getRegionLabel(r)}
          </a>
        ))}
      </div>

      <div className="city-grid">
        {sorted.map(city => {
          const total = getTotalMonthlyCost(city);
          return (
            <a key={city.slug} href={`/cities/${city.slug}`} className="card city-card">
              <div className="city-name">{city.name}</div>
              <div className="city-country">{city.country}</div>
              <div className="city-cost">${total.toLocaleString()}</div>
              <div className="city-cost-label">estimated monthly cost</div>
              <span className={`city-safety ${safetyClass(city.safety_index)}`}>
                Safety: {city.safety_index}/100
              </span>
            </a>
          );
        })}
      </div>

      <div className="affiliate-box">
        <h3>Living in {label}?</h3>
        <p>Get the best exchange rates with Wise. Stay secure online with NordVPN.</p>
      </div>
    </>
  );
}
