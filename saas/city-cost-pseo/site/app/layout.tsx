import type { Metadata } from 'next';
import '@/styles/globals.css';

export const metadata: Metadata = {
  title: {
    default: 'City Living Cost — Compare Cost of Living Worldwide',
    template: '%s | City Living Cost',
  },
  description: 'Compare cost of living across 50+ cities worldwide. Rent, food, transport, and more — all in USD.',
  keywords: ['cost of living', 'city comparison', 'expat', 'digital nomad', 'rent prices', 'living abroad'],
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en">
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
