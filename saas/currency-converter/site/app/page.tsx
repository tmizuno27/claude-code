import Link from 'next/link';
import type { Metadata } from 'next';
import { getCurrencies, getRates, convert, formatRate, pairToSlug } from '@/lib/currencies';

export const metadata: Metadata = {
  title: 'Currency Converter - Live Exchange Rates for 30+ Currencies',
  description:
    'Convert between 30+ world currencies with live exchange rates. Free online currency converter updated daily. USD, EUR, GBP, JPY, and more.',
};

const POPULAR_PAIRS = [
  ['USD', 'EUR'], ['USD', 'GBP'], ['USD', 'JPY'], ['EUR', 'GBP'],
  ['EUR', 'JPY'], ['GBP', 'JPY'], ['USD', 'CAD'], ['USD', 'AUD'],
  ['USD', 'CHF'], ['EUR', 'CHF'], ['USD', 'CNY'], ['USD', 'INR'],
  ['GBP', 'EUR'], ['USD', 'MXN'], ['USD', 'BRL'], ['EUR', 'USD'],
];

export default function HomePage() {
  const currencies = getCurrencies();
  const rates = getRates();

  return (
    <div className="container">
      <h1 className="section-title">Currency Converter &amp; Live Exchange Rates</h1>
      <p className="section-subtitle">
        Convert between {currencies.length} world currencies with rates updated daily.
        Select a currency pair below to see the live exchange rate, conversion table, and
        country information.
      </p>

      <div className="ad-slot">Advertisement</div>

      <h2 className="section-title" style={{ fontSize: '1.25rem' }}>
        Popular Currency Pairs
      </h2>
      <div className="pairs-grid">
        {POPULAR_PAIRS.map(([from, to]) => {
          const rate = convert(1, from, to);
          return (
            <Link
              key={`${from}-${to}`}
              href={`/${pairToSlug(from, to)}/`}
              className="pair-link"
            >
              <strong>{from}/{to}</strong>
              <br />
              <span style={{ color: 'var(--primary)', fontWeight: 600 }}>
                {formatRate(rate)}
              </span>
            </Link>
          );
        })}
      </div>

      <div className="ad-slot">Advertisement</div>

      <h2 className="section-title" style={{ fontSize: '1.25rem', marginTop: '2rem' }}>
        All Currencies (vs USD)
      </h2>
      <div className="currency-grid">
        {currencies.map(currency => {
          const rate = currency.code === 'USD' ? 1 : rates.rates[currency.code] || 0;
          return (
            <Link
              key={currency.code}
              href={`/${pairToSlug('USD', currency.code)}/`}
              className="currency-link"
            >
              <span className="flag">{currency.flag}</span>
              <div>
                <div className="code">{currency.code}</div>
                <div className="name">{currency.name}</div>
              </div>
              <div className="rate">
                {currency.code === 'USD' ? '1.0000' : formatRate(rate)}
              </div>
            </Link>
          );
        })}
      </div>

      <div className="ad-slot">Advertisement</div>

      <section style={{ marginTop: '2.5rem' }}>
        <h2 className="section-title" style={{ fontSize: '1.25rem' }}>
          About Our Currency Converter
        </h2>
        <p style={{ color: 'var(--text-secondary)', lineHeight: 1.8 }}>
          Our free online currency converter provides live exchange rates for over{' '}
          {currencies.length} world currencies. Rates are sourced from reliable open
          exchange rate providers and updated daily. Whether you&apos;re traveling abroad,
          sending money internationally, or researching currency markets, our converter
          gives you quick, accurate conversion information along with historical context
          and country details for each currency pair.
        </p>
      </section>
    </div>
  );
}
