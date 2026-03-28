import { Inter } from 'next/font/google';
import Script from 'next/script';
import './globals.css';
import Link from 'next/link';

const inter = Inter({ subsets: ['latin'], display: 'swap' });
const GA_ID = 'G-HT51NK0YHE';
const ADSENSE_CLIENT_ID = 'ca-pub-7177224921699744';

export const metadata = {
  title: {
    default: 'AI Tool Compare — Find the Best AI Tool for You',
    template: '%s | AI Tool Compare',
  },
  description: 'Compare AI tools side-by-side. Detailed comparisons of features, pricing, and ratings to help you choose the perfect AI tool.',
  metadataBase: new URL('https://ai-tool-compare-nu.vercel.app'),
  verification: {
    google: 'ugn5HFr2hl7GqdPfPacONozz2ZW10w7gF05sM9C8jJE',
  },
  other: {
    'google-adsense-account': ADSENSE_CLIENT_ID,
  },
  alternates: {
    canonical: '/',
  },
  openGraph: {
    title: 'AI Tool Compare — Find the Best AI Tool for You',
    description: 'Compare AI tools side-by-side. Detailed comparisons of features, pricing, and ratings.',
    siteName: 'AI Tool Compare',
    type: 'website',
    url: 'https://ai-tool-compare-nu.vercel.app',
    locale: 'en_US',
  },
  twitter: {
    card: 'summary_large_image',
    title: 'AI Tool Compare — Find the Best AI Tool for You',
    description: 'Compare AI tools side-by-side with data-driven analysis.',
  },
  keywords: ['AI tools comparison', 'best AI tools', 'ChatGPT vs Claude', 'AI tool reviews', 'compare AI software'],
  robots: { index: true, follow: true },
};

export default function RootLayout({ children }) {
  return (
    <html lang="en" className={inter.className}>
      <head>
        <Script
          async
          src={`https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=${ADSENSE_CLIENT_ID}`}
          crossOrigin="anonymous"
          strategy="afterInteractive"
        />
        <Script src={`https://www.googletagmanager.com/gtag/js?id=${GA_ID}`} strategy="afterInteractive" />
        <Script id="gtag-init" strategy="afterInteractive">{`
          window.dataLayer = window.dataLayer || [];
          function gtag(){dataLayer.push(arguments);}
          gtag('js', new Date());
          gtag('config', '${GA_ID}');
        `}</Script>
      </head>
      <body>
        <header className="site-header">
          <div className="container header-inner">
            <Link href="/" className="logo">
              <span className="logo-icon">⚡</span>
              <span className="logo-text">AI Tool Compare</span>
            </Link>
            <nav className="main-nav">
              <Link href="/">Home</Link>
              <Link href="/#categories">Categories</Link>
              <Link href="/#comparisons">Comparisons</Link>
              <Link href="/about/">About</Link>
            </nav>
          </div>
        </header>
        <main>{children}</main>
        <footer className="site-footer">
          <div className="container">
            <nav className="footer-nav">
              <Link href="/about/">About</Link>
              <Link href="/contact/">Contact</Link>
              <Link href="/privacy/">Privacy Policy</Link>
              <Link href="/terms/">Terms of Service</Link>
              <Link href="/disclaimer/">Affiliate Disclaimer</Link>
            </nav>
            <p>&copy; {new Date().getFullYear()} AI Tool Compare. All rights reserved.</p>
            <p className="footer-sub">Helping you find the right AI tool since 2026.</p>
          </div>
        </footer>
      </body>
    </html>
  );
}
