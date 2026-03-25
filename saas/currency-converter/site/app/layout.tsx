import type { Metadata } from 'next';
import Link from 'next/link';
import '@/styles/globals.css';

const SITE_NAME = 'CurrencyRate.page';
const SITE_URL = 'https://currencyrate.page';

export const metadata: Metadata = {
  title: {
    default: `Currency Converter - Live Exchange Rates | ${SITE_NAME}`,
    template: `%s | ${SITE_NAME}`,
  },
  description:
    'Free currency converter with live exchange rates. Convert between 30+ world currencies instantly. Updated daily with reliable rates.',
  metadataBase: new URL(SITE_URL),
  openGraph: {
    type: 'website',
    siteName: SITE_NAME,
    locale: 'en_US',
  },
  robots: { index: true, follow: true },
};

const POPULAR_FROM = ['USD', 'EUR', 'GBP', 'JPY'];

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en">
      <head />
      <body>
        <header className="site-header">
          <div className="header-inner">
            <Link href="/" className="site-logo">
              💱 {SITE_NAME}
            </Link>
            <nav className="header-nav">
              {POPULAR_FROM.map(code => (
                <Link key={code} href={`/#${code.toLowerCase()}`}>
                  {code}
                </Link>
              ))}
              <Link href="/about/">About</Link>
            </nav>
          </div>
        </header>

        <main>{children}</main>

        <footer className="site-footer">
          <div className="footer-inner">
            <div className="footer-links">
              <Link href="/">Home</Link>
              <Link href="/about/">About</Link>
              <Link href="/privacy/">Privacy Policy</Link>
              <Link href="/terms/">Terms of Use</Link>
            </div>
            <div style={{ fontSize: '0.75rem', color: 'var(--text-muted)', marginTop: '0.5rem' }}>
              Exchange rates are provided for informational purposes only. Rates may differ from
              actual bank or transfer rates. Always verify with your financial provider.
            </div>
            <div style={{ marginTop: '0.5rem' }}>
              &copy; {new Date().getFullYear()} {SITE_NAME}
            </div>
          </div>
        </footer>
      </body>
    </html>
  );
}
