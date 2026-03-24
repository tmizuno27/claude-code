import type { Metadata } from 'next';
import { Noto_Sans_JP } from 'next/font/google';
import Link from 'next/link';
import '@/styles/globals.css';

const notoSansJP = Noto_Sans_JP({
  subsets: ['latin'],
  weight: ['400', '600', '700'],
  variable: '--font-noto-sans-jp',
  display: 'swap',
});

export const metadata: Metadata = {
  title: '計算ツール｜keisan.tools',
  description:
    '無料で使えるオンライン計算ツール。住宅ローン、税金、BMI、日数計算など3,000種類以上。',
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
      <body>
        <header className="site-header">
          <div className="header-inner">
            <Link href="/" className="site-logo">
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
          <div className="footer-inner">
            <div className="footer-links">
              <Link href="/about/">サイトについて</Link>
              <span>
                ※計算結果は参考値です。正確な金額は専門家にご相談ください。
              </span>
            </div>
            <div>&copy; {new Date().getFullYear()} keisan.tools</div>
          </div>
        </footer>
      </body>
    </html>
  );
}
