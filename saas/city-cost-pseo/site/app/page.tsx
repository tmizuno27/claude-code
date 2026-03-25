import { cities, getTotalMonthlyCost, getAllRegions, getRegionLabel } from '@/lib/data';

function safetyClass(index: number): string {
  if (index >= 70) return 'safety-high';
  if (index >= 50) return 'safety-mid';
  return 'safety-low';
}

export default function HomePage() {
  const sorted = [...cities].sort((a, b) => getTotalMonthlyCost(a) - getTotalMonthlyCost(b));
  const regions = getAllRegions();

  return (
    <>
      <div className="page-header">
        <h1>Cost of Living Comparison — 50+ Cities Worldwide</h1>
        <p>Find the most affordable cities for living, working remotely, or retiring abroad. All costs in USD/month.</p>
      </div>

      <div className="region-grid">
        {regions.map(r => (
          <a key={r} href={`/region/${r}`} className="card region-card">
            {getRegionLabel(r)}
          </a>
        ))}
      </div>

      <div className="affiliate-box">
        <h3>Moving Abroad?</h3>
        <p>Compare international money transfer services, VPNs, and travel insurance to save money on your move.</p>
      </div>

      <h2 style={{ marginBottom: 20 }}>All Cities (Sorted by Cost)</h2>

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
    </>
  );
}
