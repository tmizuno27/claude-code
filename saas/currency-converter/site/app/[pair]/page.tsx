import { notFound } from 'next/navigation';
import Link from 'next/link';
import type { Metadata } from 'next';
import {
  getCurrencies,
  getCurrency,
  getAllPairs,
  convert,
  formatRate,
  getCommonAmounts,
  getRates,
  pairToSlug,
  slugToPair,
} from '@/lib/currencies';

interface Props {
  params: Promise<{ pair: string }>;
}

export async function generateStaticParams() {
  const pairs = getAllPairs();
  return pairs.map(p => ({ pair: pairToSlug(p.from, p.to) }));
}

export async function generateMetadata({ params }: Props): Promise<Metadata> {
  const { pair } = await params;
  const parsed = slugToPair(pair);
  if (!parsed) return {};
  const fromC = getCurrency(parsed.from);
  const toC = getCurrency(parsed.to);
  if (!fromC || !toC) return {};
  const rate = convert(1, parsed.from, parsed.to);
  return {
    title: `1 ${parsed.from} to ${parsed.to} - Convert ${fromC.name}s to ${toC.name}s | Live Rate`,
    description: `Convert ${fromC.name} (${parsed.from}) to ${toC.name} (${parsed.to}). 1 ${parsed.from} = ${formatRate(rate)} ${parsed.to}. Free currency converter with daily updated exchange rates, conversion table, and country information.`,
    openGraph: {
      title: `${parsed.from} to ${parsed.to} Exchange Rate - ${formatRate(rate)}`,
      description: `1 ${fromC.name} = ${formatRate(rate)} ${toC.name}. Live exchange rate with conversion table.`,
    },
  };
}

export default async function PairPage({ params }: Props) {
  const { pair } = await params;
  const parsed = slugToPair(pair);
  if (!parsed) notFound();

  const fromC = getCurrency(parsed.from);
  const toC = getCurrency(parsed.to);
  if (!fromC || !toC) notFound();

  const { from, to } = parsed;
  const rate = convert(1, from, to);
  const reverseRate = convert(1, to, from);
  const amounts = getCommonAmounts(from, to);
  const reverseAmounts = getCommonAmounts(to, from);
  const rates = getRates();
  const allCurrencies = getCurrencies();

  // Related pairs: other conversions from this currency
  const relatedFrom = allCurrencies
    .filter(c => c.code !== from && c.code !== to)
    .slice(0, 8)
    .map(c => ({ from, to: c.code }));

  const relatedTo = allCurrencies
    .filter(c => c.code !== from && c.code !== to)
    .slice(0, 8)
    .map(c => ({ from: to, to: c.code }));

  const jsonLd = {
    '@context': 'https://schema.org',
    '@type': 'ExchangeRateSpecification',
    currency: to,
    currentExchangeRate: {
      '@type': 'UnitPriceSpecification',
      price: rate,
      priceCurrency: to,
      unitCode: from,
    },
  };

  return (
    <div className="container">
      <script
        type="application/ld+json"
        dangerouslySetInnerHTML={{ __html: JSON.stringify(jsonLd) }}
      />

      <nav className="breadcrumb">
        <Link href="/">Home</Link>
        <span>/</span>
        <span>{from} to {to}</span>
      </nav>

      {/* Hero converter box */}
      <div className="converter-box">
        <h1>
          {fromC.flag} {from} to {toC.flag} {to}
        </h1>
        <p>
          Convert {fromC.name} to {toC.name}
        </p>
        <div className="rate-display">
          1 {from} = {formatRate(rate)} {to}
          <span className="rate-small">
            1 {to} = {formatRate(reverseRate)} {from}
          </span>
        </div>
        <div className="rate-date">
          Last updated: {rates.date}
        </div>
        <Link href={`/${pairToSlug(to, from)}/`} className="swap-link">
          ⇄ Swap to {to} → {from}
        </Link>
      </div>

      <div className="ad-slot">Advertisement</div>

      {/* Conversion tables side by side */}
      <div className="info-grid">
        <div className="card">
          <h2 style={{ fontSize: '1.1rem', marginBottom: '0.75rem' }}>
            {from} to {to} Conversion Table
          </h2>
          <table className="conversion-table">
            <thead>
              <tr>
                <th>{fromC.name}</th>
                <th>{toC.name}</th>
              </tr>
            </thead>
            <tbody>
              {amounts.map(row => (
                <tr key={row.amount}>
                  <td className="amount">
                    {fromC.symbol}{row.amount.toLocaleString()}
                  </td>
                  <td className="amount">
                    {toC.symbol}{row.result.toLocaleString(undefined, { minimumFractionDigits: 2, maximumFractionDigits: 2 })}
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>

        <div className="card">
          <h2 style={{ fontSize: '1.1rem', marginBottom: '0.75rem' }}>
            {to} to {from} Conversion Table
          </h2>
          <table className="conversion-table">
            <thead>
              <tr>
                <th>{toC.name}</th>
                <th>{fromC.name}</th>
              </tr>
            </thead>
            <tbody>
              {reverseAmounts.map(row => (
                <tr key={row.amount}>
                  <td className="amount">
                    {toC.symbol}{row.amount.toLocaleString()}
                  </td>
                  <td className="amount">
                    {fromC.symbol}{row.result.toLocaleString(undefined, { minimumFractionDigits: 2, maximumFractionDigits: 2 })}
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>

      <div className="ad-slot">Advertisement</div>

      {/* Currency info cards */}
      <div className="info-grid">
        <div className="info-card">
          <h3>{fromC.flag} {fromC.name} ({from})</h3>
          <p><strong>Country:</strong> {fromC.country}</p>
          <p><strong>Region:</strong> {fromC.region}</p>
          <p><strong>Symbol:</strong> {fromC.symbol}</p>
          <p style={{ marginTop: '0.5rem' }}>{fromC.description}</p>
          <p style={{ marginTop: '0.5rem', fontStyle: 'italic' }}>
            💡 {fromC.funFact}
          </p>
        </div>
        <div className="info-card">
          <h3>{toC.flag} {toC.name} ({to})</h3>
          <p><strong>Country:</strong> {toC.country}</p>
          <p><strong>Region:</strong> {toC.region}</p>
          <p><strong>Symbol:</strong> {toC.symbol}</p>
          <p style={{ marginTop: '0.5rem' }}>{toC.description}</p>
          <p style={{ marginTop: '0.5rem', fontStyle: 'italic' }}>
            💡 {toC.funFact}
          </p>
        </div>
      </div>

      {/* FAQ Section */}
      <section className="faq-section">
        <h2>Frequently Asked Questions</h2>

        <div className="faq-item">
          <h3>How much is 1 {from} in {to}?</h3>
          <p>
            As of {rates.date}, 1 {fromC.name} ({from}) equals {formatRate(rate)}{' '}
            {toC.name} ({to}). Exchange rates fluctuate throughout the day based on
            market conditions.
          </p>
        </div>

        <div className="faq-item">
          <h3>How much is 100 {from} in {to}?</h3>
          <p>
            100 {fromC.name} is equal to approximately{' '}
            {convert(100, from, to).toLocaleString(undefined, { minimumFractionDigits: 2, maximumFractionDigits: 2 })}{' '}
            {toC.name} at current exchange rates.
          </p>
        </div>

        <div className="faq-item">
          <h3>How much is 1,000 {from} in {to}?</h3>
          <p>
            1,000 {fromC.name} converts to about{' '}
            {convert(1000, from, to).toLocaleString(undefined, { minimumFractionDigits: 2, maximumFractionDigits: 2 })}{' '}
            {toC.name}.
          </p>
        </div>

        <div className="faq-item">
          <h3>Where is {from} used?</h3>
          <p>
            The {fromC.name} ({from}) is the official currency of {fromC.country}.
            {' '}{fromC.description}
          </p>
        </div>

        <div className="faq-item">
          <h3>Where is {to} used?</h3>
          <p>
            The {toC.name} ({to}) is the official currency of {toC.country}.
            {' '}{toC.description}
          </p>
        </div>

        <div className="faq-item">
          <h3>How are exchange rates determined?</h3>
          <p>
            Exchange rates between {from} and {to} are determined by supply and demand
            in global foreign exchange markets. Factors include interest rates, inflation,
            trade balances, political stability, and economic performance of both countries.
          </p>
        </div>
      </section>

      <div className="ad-slot">Advertisement</div>

      {/* Related conversions */}
      <section className="related-section">
        <h2>Other {from} Conversions</h2>
        <div className="pairs-grid">
          {relatedFrom.map(p => (
            <Link
              key={`${p.from}-${p.to}`}
              href={`/${pairToSlug(p.from, p.to)}/`}
              className="pair-link"
            >
              {p.from} to {p.to}{' '}
              <span style={{ color: 'var(--primary)' }}>
                {formatRate(convert(1, p.from, p.to))}
              </span>
            </Link>
          ))}
        </div>
      </section>

      <section className="related-section">
        <h2>Other {to} Conversions</h2>
        <div className="pairs-grid">
          {relatedTo.map(p => (
            <Link
              key={`${p.from}-${p.to}`}
              href={`/${pairToSlug(p.from, p.to)}/`}
              className="pair-link"
            >
              {p.from} to {p.to}{' '}
              <span style={{ color: 'var(--primary)' }}>
                {formatRate(convert(1, p.from, p.to))}
              </span>
            </Link>
          ))}
        </div>
      </section>
    </div>
  );
}
