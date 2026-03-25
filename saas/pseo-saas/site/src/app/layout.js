import { Inter } from 'next/font/google';
import Script from 'next/script';
import './globals.css';
import Link from 'next/link';

const inter = Inter({ subsets: ['latin'], display: 'swap' });
const GA_ID = 'G-HT51NK0YHE';

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
  openGraph: {
    siteName: 'AI Tool Compare',
    type: 'website',
  },
};

export default function RootLayout({ children }) {
  return (
    <html lang="en" className={inter.className}>
      <head>
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
