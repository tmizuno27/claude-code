import type { Metadata } from 'next';
import Script from 'next/script';
import '@/styles/globals.css';

const GA_MEASUREMENT_ID = 'G-HT51NK0YHE';
const ADSENSE_CLIENT_ID = 'ca-pub-7177224921699744';

export const metadata: Metadata = {
  title: {
    default: 'City Living Cost — Compare Cost of Living Worldwide',
    template: '%s | City Living Cost',
  },
  description: 'Compare cost of living across 50+ cities worldwide. Rent, food, transport, and more — all in USD. Perfect for expats, digital nomads, and remote workers.',
  keywords: ['cost of living', 'city comparison', 'expat', 'digital nomad', 'rent prices', 'living abroad', 'cost of living comparison', 'cheapest cities'],
  metadataBase: new URL('https://citylivingcost.com'),
  openGraph: {
    title: 'City Living Cost — Compare Cost of Living Worldwide',
    description: 'Compare cost of living across 50+ cities. Rent, food, transport — all in USD.',
    siteName: 'City Living Cost',
    type: 'website',
    locale: 'en_US',
  },
  twitter: {
    card: 'summary_large_image',
    title: 'City Living Cost — Compare Cost of Living Worldwide',
    description: 'Compare cost of living across 50+ cities. Perfect for expats and digital nomads.',
  },
  robots: { index: true, follow: true },
  other: {
    'google-adsense-account': ADSENSE_CLIENT_ID,
  },
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en">
      <head>
        <script
          type="application/ld+json"
          dangerouslySetInnerHTML={{
            __html: JSON.stringify({
              '@context': 'https://schema.org',
              '@type': 'WebSite',
              name: 'City Living Cost',
              url: 'https://citylivingcost.com',
              description: 'Compare cost of living across 50+ cities worldwide',
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
          <nav className="nav-container">
            <a href="/" className="logo">City Living Cost</a>
            <div className="nav-links">
              <a href="/">Cities</a>
              <a href="/compare/tokyo-vs-bangkok">Compare</a>
              <a href="/region/asia">Regions</a>
            </div>
          </nav>
        </header>
        <main className="main-content">{children}</main>
        {/* AdSense placeholder */}
        <aside className="ad-placeholder" aria-hidden="true">
          <div className="ad-slot" data-ad="leaderboard">Ad Space</div>
        </aside>
        <footer className="site-footer">
          <div className="footer-content">
            <p>&copy; {new Date().getFullYear()} City Living Cost. All costs in USD. Data for reference only.</p>
            <div className="footer-links">
              <a href="/">Home</a>
              <a href="/region/asia">Asia</a>
              <a href="/region/europe">Europe</a>
              <a href="/region/south-america">South America</a>
            </div>
          </div>
        </footer>
      </body>
    </html>
  );
}
