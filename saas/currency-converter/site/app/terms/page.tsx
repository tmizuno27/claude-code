import type { Metadata } from 'next';
import Link from 'next/link';

export const metadata: Metadata = {
  title: 'Terms of Use',
  description: 'Terms of use for CurrencyRate.page currency converter.',
};

export default function TermsPage() {
  return (
    <div className="container" style={{ maxWidth: 720 }}>
      <nav className="breadcrumb">
        <Link href="/">Home</Link>
        <span>/</span>
        <span>Terms of Use</span>
      </nav>
      <h1 className="section-title">Terms of Use</h1>
      <p style={{ color: 'var(--text-secondary)', lineHeight: 1.8, marginBottom: '1rem' }}>
        Last updated: March 2026
      </p>
      <h2 style={{ fontSize: '1.1rem', margin: '1.5rem 0 0.5rem' }}>Acceptance of Terms</h2>
      <p style={{ color: 'var(--text-secondary)', lineHeight: 1.8 }}>
        By using CurrencyRate.page, you agree to these terms of use.
      </p>
      <h2 style={{ fontSize: '1.1rem', margin: '1.5rem 0 0.5rem' }}>Disclaimer</h2>
      <p style={{ color: 'var(--text-secondary)', lineHeight: 1.8 }}>
        Exchange rates are provided for informational purposes only. We make no guarantees about
        the accuracy or completeness of the rates displayed. Rates may differ from actual bank
        or transfer service rates. Do not rely solely on this site for financial decisions.
      </p>
      <h2 style={{ fontSize: '1.1rem', margin: '1.5rem 0 0.5rem' }}>Limitation of Liability</h2>
      <p style={{ color: 'var(--text-secondary)', lineHeight: 1.8 }}>
        CurrencyRate.page is not liable for any losses or damages arising from the use of
        information on this site.
      </p>
      <h2 style={{ fontSize: '1.1rem', margin: '1.5rem 0 0.5rem' }}>Changes</h2>
      <p style={{ color: 'var(--text-secondary)', lineHeight: 1.8 }}>
        We may update these terms at any time. Continued use of the site constitutes acceptance
        of any changes.
      </p>
    </div>
  );
}
