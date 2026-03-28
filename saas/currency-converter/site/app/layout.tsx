import type { Metadata } from 'next';
import Link from 'next/link';
import Script from 'next/script';
import '@/styles/globals.css';

const SITE_NAME = 'CurrencyRate.page';
const SITE_URL = 'https://currencyrate.page';
const GA_MEASUREMENT_ID = 'G-HT51NK0YHE';
const ADSENSE_CLIENT_ID = 'ca-pub-7177224921699744';

export const metadata: Metadata = {
  title: {
    default: `Currency Converter - Live Exchange Rates | ${SITE_NAME}`,
    template: `%s | ${SITE_NAME}`,
  },
  description:
    'Free currency converter with live exchange rates. Convert between 30+ world currencies instantly. Updated daily with reliable rates.',
  metadataBase: new URL(SITE_URL),
  keywords: ['currency converter', 'exchange rates', 'USD to EUR', 'currency exchange', 'forex rates', 'money converter'],
  openGraph: {
    title: `Currency Converter - Live Exchange Rates | ${SITE_NAME}`,
    description: 'Free currency converter with live exchange rates for 30+ currencies.',
    type: 'website',
    siteName: SITE_NAME,
    locale: 'en_US',
  },
  twitter: {
    card: 'summary',
    title: `Currency Converter | ${SITE_NAME}`,
    description: 'Free currency converter with live exchange rates for 30+ currencies.',
  },
  robots: { index: true, follow: true },
  other: {
    'google-adsense-account': ADSENSE_CLIENT_ID,
  },
};

const POPULAR_FROM = ['USD', 'EUR', 'GBP', 'JPY'];

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en">
      <head>
        <script
          type="application/ld+json"
          dangerouslySetInnerHTML={{
            __html: JSON.stringify({
              '@context': 'https://schema.org',
              '@type': 'WebApplication',
              name: SITE_NAME,
              url: SITE_URL,
              applicationCategory: 'FinanceApplication',
              description: 'Free currency converter with live exchange rates for 30+ currencies.',
              offers: { '@type': 'Offer', price: '0', priceCurrency: 'USD' },
            }),
          }}
        />
        <Script
          async
          src={`https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=${ADSENSE_CLIENT_ID}`}
          crossOrigin="anonymous"
          strategy="afterInteractive"
        />
        <Script
          src={`https://www.googletagmanager.com/gtag/js?id=${GA_MEASUREMENT_ID}`}
          strategy="afterInteractive"
        />
        <Script id="google-analytics" strategy="afterInteractive">
          {`
            window.dataLayer = window.dataLayer || [];
            function gtag(){dataLayer.push(arguments);}
            gtag('js', new Date());
            gtag('config', '${GA_MEASUREMENT_ID}');
          `}
        </Script>
      </head>
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
