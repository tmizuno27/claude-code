import type { Metadata } from 'next';
import Link from 'next/link';

export const metadata: Metadata = {
  title: 'Privacy Policy',
  description: 'Privacy policy for CurrencyRate.page currency converter.',
};

export default function PrivacyPage() {
  return (
    <div className="container" style={{ maxWidth: 720 }}>
      <nav className="breadcrumb">
        <Link href="/">Home</Link>
        <span>/</span>
        <span>Privacy Policy</span>
      </nav>
      <h1 className="section-title">Privacy Policy</h1>
      <p style={{ color: 'var(--text-secondary)', lineHeight: 1.8, marginBottom: '1rem' }}>
        Last updated: March 2026
      </p>
      <h2 style={{ fontSize: '1.1rem', margin: '1.5rem 0 0.5rem' }}>Information We Collect</h2>
      <p style={{ color: 'var(--text-secondary)', lineHeight: 1.8 }}>
        We do not collect personal information. We use Google Analytics to understand how visitors
        use our site. This may include anonymous data such as pages visited, time on site, and
        referring URLs.
      </p>
      <h2 style={{ fontSize: '1.1rem', margin: '1.5rem 0 0.5rem' }}>Cookies</h2>
      <p style={{ color: 'var(--text-secondary)', lineHeight: 1.8 }}>
        We use cookies from Google Analytics and Google AdSense to provide analytics and display
        relevant advertisements. You can disable cookies in your browser settings.
      </p>
      <h2 style={{ fontSize: '1.1rem', margin: '1.5rem 0 0.5rem' }}>Third-Party Services</h2>
      <p style={{ color: 'var(--text-secondary)', lineHeight: 1.8 }}>
        We use Google Analytics for website analytics and Google AdSense for advertising. These
        services have their own privacy policies.
      </p>
      <h2 style={{ fontSize: '1.1rem', margin: '1.5rem 0 0.5rem' }}>Contact</h2>
      <p style={{ color: 'var(--text-secondary)', lineHeight: 1.8 }}>
        If you have questions about this privacy policy, please contact us through our website.
      </p>
    </div>
  );
}
