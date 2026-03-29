import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: {
    default: "GSC Rank Tracker Pro — Google Search Consoleデータを無期限保存",
    template: "%s | GSC Rank Tracker Pro",
  },
  description:
    "Google Search Consoleのデータを自動取得・無期限保存。順位急落アラート・CTR改善提案・複数サイト管理。設定5分で始めるSEOモニタリングツール。",
  keywords: [
    "Google Search Console",
    "GSC",
    "SEOツール",
    "順位追跡",
    "キーワード順位",
    "SEOモニタリング",
  ],
  openGraph: {
    type: "website",
    locale: "ja_JP",
    url: process.env.NEXT_PUBLIC_APP_URL,
    siteName: "GSC Rank Tracker Pro",
  },
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="ja">
      <body>{children}</body>
    </html>
  );
}
