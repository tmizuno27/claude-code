import { cities, getCityBySlug, getAllComparisons, getTotalMonthlyCost } from '@/lib/data';
import type { Metadata } from 'next';
import { notFound } from 'next/navigation';

interface Props {
  params: Promise<{ pair: string }>;
}

export async function generateStaticParams() {
  return getAllComparisons().map(({ city1, city2 }) => ({
    pair: `${city1}-vs-${city2}`,
  }));
}

function parsePair(pair: string): [string, string] | null {
  const parts = pair.split('-vs-');
  if (parts.length !== 2) return null;
  return [parts[0], parts[1]];
}

export async function generateMetadata({ params }: Props): Promise<Metadata> {
  const { pair } = await params;
  const parsed = parsePair(pair);
  if (!parsed) return {};
  const [c1, c2] = [getCityBySlug(parsed[0]), getCityBySlug(parsed[1])];
  if (!c1 || !c2) return {};
  return {
    title: `${c1.name} vs ${c2.name} — Cost of Living Comparison`,
    description: `Compare cost of living between ${c1.name} and ${c2.name}. Rent, food, transport, utilities side by side.`,
  };
}

const costLabels: Record<string, string> = {
  rent1br_center: '1BR Apartment (Center)',
  rent1br_outside: '1BR Apartment (Outside)',
  meal_inexpensive: 'Cheap Meal',
  meal_mid: 'Mid-Range Meal',
  monthly_pass: 'Transit Pass',
  utilities: 'Utilities',
  internet: 'Internet',
  groceries_monthly: 'Groceries',
};

export default async function ComparePage({ params }: Props) {
  const { pair } = await params;
  const parsed = parsePair(pair);
  if (!parsed) notFound();

  const city1 = getCityBySlug(parsed[0]);
  const city2 = getCityBySlug(parsed[1]);
  if (!city1 || !city2) notFound();

  const total1 = getTotalMonthlyCost(city1);
  const total2 = getTotalMonthlyCost(city2);
  const costKeys = Object.keys(city1.costs) as Array<keyof typeof city1.costs>;
  const maxVal = Math.max(
    ...costKeys.map(k => Math.max(city1.costs[k], city2.costs[k]))
  );

  const cheaper = total1 < total2 ? city1 : city2;
  const pctDiff = Math.round(Math.abs(total1 - total2) / Math.max(total1, total2) * 100);

  return (
    <>
      <div className="breadcrumb">
        <a href="/">Home</a> &rarr; Compare &rarr; {city1.name} vs {city2.name}
      </div>

      <div className="page-header">
        <h1>{city1.name} vs {city2.name}: Cost of Living</h1>
        <p>
          {cheaper.name} is approximately {pctDiff}% cheaper overall.
          Total estimated monthly costs: {city1.name} ${total1.toLocaleString()} vs {city2.name} ${total2.toLocaleString()}.
        </p>
      </div>

      <div className="compare-legend">
        <div className="legend-item"><div className="legend-dot city1" />{city1.name} (${total1.toLocaleString()}/mo)</div>
        <div className="legend-item"><div className="legend-dot city2" />{city2.name} (${total2.toLocaleString()}/mo)</div>
      </div>

      <div className="bar-chart">
        {costKeys.map(key => {
          const v1 = city1.costs[key];
          const v2 = city2.costs[key];
          const scale = maxVal > 0 ? 100 / maxVal : 1;
          return (
            <div key={key} className="bar-row">
              <div className="bar-label">{costLabels[key] ?? key}</div>
              <div className="bar-track">
                <div className="bar-fill city1" style={{ width: `${Math.max(v1 * scale, 5)}%` }}>${v1}</div>
                <div className="bar-fill city2" style={{ width: `${Math.max(v2 * scale, 5)}%` }}>${v2}</div>
              </div>
            </div>
          );
        })}
      </div>

      <table className="cost-table">
        <thead>
          <tr><th>Category</th><th>{city1.name}</th><th>{city2.name}</th><th>Difference</th></tr>
        </thead>
        <tbody>
          {costKeys.map(key => {
            const v1 = city1.costs[key];
            const v2 = city2.costs[key];
            const diff = v1 - v2;
            return (
              <tr key={key}>
                <td>{costLabels[key] ?? key}</td>
                <td className="cost-value">${v1}</td>
                <td className="cost-value">${v2}</td>
                <td style={{ color: diff > 0 ? 'var(--danger)' : 'var(--accent)', fontWeight: 600 }}>
                  {diff > 0 ? '+' : ''}{diff === 0 ? '-' : `$${diff}`}
                </td>
              </tr>
            );
          })}
          <tr style={{ fontWeight: 700 }}>
            <td>Total Estimated</td>
            <td className="cost-value">${total1.toLocaleString()}</td>
            <td className="cost-value">${total2.toLocaleString()}</td>
            <td style={{ color: total1 > total2 ? 'var(--danger)' : 'var(--accent)' }}>
              ${Math.abs(total1 - total2).toLocaleString()}
            </td>
          </tr>
        </tbody>
      </table>

      <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: 24, marginTop: 32 }}>
        <div>
          <h3>Safety</h3>
          <p>{city1.name}: {city1.safety_index}/100 &mdash; {city2.name}: {city2.safety_index}/100</p>
        </div>
        <div>
          <h3>Average Salary</h3>
          <p>{city1.name}: ${city1.salary_avg_monthly}/mo &mdash; {city2.name}: ${city2.salary_avg_monthly}/mo</p>
        </div>
      </div>

      <div className="affiliate-box">
        <h3>Relocating?</h3>
        <p>Use Wise for the best exchange rates. Protect yourself with international travel insurance.</p>
      </div>
    </>
  );
}
