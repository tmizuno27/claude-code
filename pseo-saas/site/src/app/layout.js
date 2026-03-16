import { Inter } from 'next/font/google';
import './globals.css';
import Link from 'next/link';

const inter = Inter({ subsets: ['latin'], display: 'swap' });

export const metadata = {
  title: {
    default: 'AI Tool Compare — Find the Best AI Tool for You',
    template: '%s | AI Tool Compare',
  },
  description: 'Compare AI tools side-by-side. Detailed comparisons of features, pricing, and ratings to help you choose the perfect AI tool.',
  metadataBase: new URL('https://aitoolcompare.com'),
  openGraph: {
    siteName: 'AI Tool Compare',
    type: 'website',
  },
};

export default function RootLayout({ children }) {
  return (
    <html lang="en" className={inter.className}>
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
            <p>&copy; {new Date().getFullYear()} AI Tool Compare. All rights reserved.</p>
            <p className="footer-sub">Helping you find the right AI tool since 2026.</p>
          </div>
        </footer>
      </body>
    </html>
  );
}
