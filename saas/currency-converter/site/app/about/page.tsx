import type { Metadata } from 'next';
import Link from 'next/link';

export const metadata: Metadata = {
  title: 'About - CurrencyRate.page',
  description: 'About our free currency converter. Learn how we provide accurate, daily-updated exchange rates for 30+ world currencies.',
};

export default function AboutPage() {
  return (
    <div className="container" style={{ maxWidth: 720 }}>
      <nav className="breadcrumb">
        <Link href="/">Home</Link>
        <span>/</span>
        <span>About</span>
      </nav>
      <h1 className="section-title">About CurrencyRate.page</h1>
      <p style={{ color: 'var(--text-secondary)', lineHeight: 1.8, marginBottom: '1.5rem' }}>
        CurrencyRate.page is a free online currency converter providing live exchange rates for
        30+ world currencies. Our mission is to make currency conversion simple, fast, and
        accessible to everyone.
      </p>
      <h2 style={{ fontSize: '1.15rem', marginBottom: '0.75rem' }}>How It Works</h2>
      <p style={{ color: 'var(--text-secondary)', lineHeight: 1.8, marginBottom: '1.5rem' }}>
        We source exchange rates from reliable open APIs and update them daily. Each currency
        pair page includes a conversion table, country information, and frequently asked
        questions to help you understand the currencies you are converting between.
      </p>
      <h2 style={{ fontSize: '1.15rem', marginBottom: '0.75rem' }}>Disclaimer</h2>
      <p style={{ color: 'var(--text-secondary)', lineHeight: 1.8 }}>
        Exchange rates shown on this site are for informational purposes only. Actual rates
        may vary depending on your bank, money transfer service, or payment provider. Always
        verify with your financial institution before making transactions.
      </p>
    </div>
  );
}
