import type { Metadata } from 'next';
import { Noto_Sans_JP } from 'next/font/google';
import Link from 'next/link';
import Script from 'next/script';
import '@/styles/globals.css';
import '@/styles/home.css';

const GA_MEASUREMENT_ID = 'G-3R1LVHX9VJ';
const ADSENSE_CLIENT_ID = 'ca-pub-7177224921699744';

const notoSansJP = Noto_Sans_JP({
  subsets: ['latin'],
  weight: ['400', '500', '600', '700'],
  variable: '--font-noto-sans-jp',
  display: 'swap',
});

export const metadata: Metadata = {
  title: '計算ツール｜keisan.tools',
  description:
    '無料で使えるオンライン計算ツール。住宅ローン、税金、BMI、日数計算など3,000種類以上。',
  verification: {
    google: 'NbIFsNGN9cGMho1jOTMb0w7V9wLTucQoZQPq_vBUA_0',
  },
  other: {
    'google-adsense-account': ADSENSE_CLIENT_ID,
  },
};

const NAV_CATEGORIES = [
  { slug: 'money', label: 'お金・金融' },
  { slug: 'health', label: '健康' },
  { slug: 'life', label: '生活・日常' },
  { slug: 'business', label: 'ビジネス' },
  { slug: 'math', label: '数学' },
  { slug: 'education', label: '教育' },
];

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="ja" className={notoSansJP.variable}>
      <head>
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
              <span className="site-logo-icon">⚡</span>
              keisan.tools
            </Link>
            <nav className="header-nav">
              {NAV_CATEGORIES.map(cat => (
                <Link key={cat.slug} href={`/${cat.slug}/`}>
                  {cat.label}
                </Link>
              ))}
            </nav>
          </div>
        </header>

        <main>{children}</main>

        <footer className="site-footer">
          <div className="footer-grid">
            <div className="footer-brand">
              <div className="footer-logo">⚡ keisan.tools</div>
              <p className="footer-tagline">あらゆる計算を、もっと簡単に。</p>
            </div>
            <div className="footer-col">
              <h4 className="footer-heading">カテゴリ</h4>
              <ul className="footer-links">
                {NAV_CATEGORIES.map(cat => (
                  <li key={cat.slug}>
                    <Link href={`/${cat.slug}/`}>{cat.label}</Link>
                  </li>
                ))}
              </ul>
            </div>
            <div className="footer-col">
              <h4 className="footer-heading">サイト情報</h4>
              <ul className="footer-links">
                <li><Link href="/about/">サイトについて</Link></li>
                <li><Link href="/privacy/">プライバシーポリシー</Link></li>
                <li><Link href="/terms/">利用規約</Link></li>
                <li><Link href="/contact/">お問い合わせ</Link></li>
              </ul>
            </div>
          </div>
          <div className="footer-bottom">
            <p className="footer-disclaimer">
              ※計算結果は参考値です。正確な金額は専門家にご相談ください。
            </p>
            <p className="footer-copyright">
              &copy; {new Date().getFullYear()} keisan.tools
            </p>
          </div>
        </footer>
      </body>
    </html>
  );
}
