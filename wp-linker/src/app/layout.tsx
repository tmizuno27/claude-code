import type { Metadata } from "next";
import { Geist } from "next/font/google";
import "./globals.css";

const geistSans = Geist({
  variable: "--font-geist-sans",
  subsets: ["latin"],
});

export const metadata: Metadata = {
  title: "WP Linker — WordPress Internal Link Optimizer",
  description:
    "AI-powered internal linking, orphan post detection, and link coverage analysis for WordPress. No plugin install required — works via REST API.",
  keywords: [
    "WordPress internal links",
    "SEO tool",
    "orphan post detection",
    "internal link optimizer",
    "WordPress REST API",
    "link coverage",
  ],
  openGraph: {
    title: "WP Linker — Fix Your Internal Links, Boost Your SEO",
    description:
      "Analyze your WordPress posts, find orphan content, and apply smart internal link suggestions with one click. No plugin required.",
    type: "website",
    locale: "en_US",
    siteName: "WP Linker",
  },
  twitter: {
    card: "summary_large_image",
    title: "WP Linker — WordPress Internal Link Optimizer",
    description:
      "AI-powered internal linking for WordPress. No plugin install required.",
  },
  robots: {
    index: true,
    follow: true,
  },
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <head>
        <link rel="icon" href="/favicon.svg" type="image/svg+xml" />
      </head>
      <body className={`${geistSans.variable} antialiased`}>{children}</body>
    </html>
  );
}
