import type { Metadata } from 'next';

export const metadata: Metadata = {
  title: {
    default: 'YourSiteName — Compare Developer Tools & Frameworks',
    template: '%s | YourSiteName',
  },
  description:
    'Compare popular developer tools, frameworks, and libraries. Detailed side-by-side comparisons to help you choose the right technology.',
  metadataBase: new URL('https://yourdomain.com'),
  openGraph: {
    type: 'website',
    locale: 'en_US',
    siteName: 'YourSiteName',
  },
  robots: {
    index: true,
    follow: true,
  },
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en">
      <body
        style={{
          margin: 0,
          fontFamily:
            '-apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif',
          color: '#1a1a1a',
          backgroundColor: '#fafafa',
        }}
      >
        <header
          style={{
            borderBottom: '1px solid #e5e5e5',
            padding: '16px 24px',
            backgroundColor: '#fff',
          }}
        >
          <a
            href="/"
            style={{
              textDecoration: 'none',
              color: '#1a1a1a',
              fontWeight: 700,
              fontSize: '20px',
            }}
          >
            YourSiteName
          </a>
        </header>

        <main style={{ maxWidth: '900px', margin: '0 auto', padding: '32px 24px' }}>
          {children}
        </main>

        <footer
          style={{
            borderTop: '1px solid #e5e5e5',
            padding: '24px',
            textAlign: 'center',
            color: '#666',
            fontSize: '14px',
          }}
        >
          &copy; {new Date().getFullYear()} YourSiteName. All rights reserved.
        </footer>

        {/* Google AdSense - uncomment after approval */}
        {/* <script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-XXXXXXX" crossOrigin="anonymous"></script> */}
      </body>
    </html>
  );
}
