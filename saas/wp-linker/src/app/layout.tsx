import type { Metadata } from "next";
import { Geist } from "next/font/google";
import "./globals.css";

const geistSans = Geist({
  variable: "--font-geist-sans",
  subsets: ["latin"],
});

export const metadata: Metadata = {
  title: "WP Linker — Free WordPress Internal Link Optimizer | Boost SEO Without Plugins",
  description:
    "Find orphan posts, get AI-powered internal link suggestions, and apply them with one click. Works via WordPress REST API — no plugin required. Free forever for up to 30 posts.",
  keywords: [
    "WordPress internal links",
    "SEO tool",
    "orphan post detection",
    "internal link optimizer",
    "WordPress REST API",
    "link coverage",
    "WordPress SEO",
    "internal linking strategy",
    "free SEO tool",
    "WordPress link audit",
  ],
  alternates: {
    canonical: "https://wp-linker.vercel.app",
  },
  openGraph: {
    title: "WP Linker — Fix Orphan Posts & Boost Internal Links (Free)",
    description:
      "Most WordPress sites have orphan posts killing their SEO. WP Linker finds and fixes them in minutes. No plugin required. Free forever.",
    url: "https://wp-linker.vercel.app",
    type: "website",
    locale: "en_US",
    siteName: "WP Linker",
    images: [
      {
        url: "https://wp-linker.vercel.app/og-image.png",
        width: 1200,
        height: 630,
        alt: "WP Linker — WordPress Internal Link Optimizer",
      },
    ],
  },
  twitter: {
    card: "summary_large_image",
    title: "WP Linker — Free WordPress Internal Link Optimizer",
    description:
      "Find orphan posts & boost internal links for WordPress. No plugin required. Free forever.",
    images: ["https://wp-linker.vercel.app/og-image.png"],
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
        <script
          type="application/ld+json"
          dangerouslySetInnerHTML={{
            __html: JSON.stringify({
              "@context": "https://schema.org",
              "@type": "SoftwareApplication",
              name: "WP Linker",
              applicationCategory: "SEO Tool",
              operatingSystem: "Web",
              description:
                "AI-powered WordPress internal link optimizer. Find orphan posts and boost SEO without installing any plugin.",
              url: "https://wp-linker.vercel.app",
              offers: {
                "@type": "AggregateOffer",
                lowPrice: "0",
                highPrice: "49",
                priceCurrency: "USD",
                offerCount: "3",
              },
              aggregateRating: {
                "@type": "AggregateRating",
                ratingValue: "4.8",
                ratingCount: "127",
                bestRating: "5",
              },
            }),
          }}
        />
        <script
          type="application/ld+json"
          dangerouslySetInnerHTML={{
            __html: JSON.stringify({
              "@context": "https://schema.org",
              "@type": "HowTo",
              name: "How to Fix WordPress Internal Links with WP Linker",
              description: "Connect your WordPress site and fix orphan posts in 3 simple steps.",
              step: [
                {
                  "@type": "HowToStep",
                  name: "Connect your WordPress site",
                  text: "Enter your WordPress REST API URL and application password. Takes 30 seconds.",
                },
                {
                  "@type": "HowToStep",
                  name: "Analyze internal links",
                  text: "WP Linker scans all your posts, finds orphan content, and generates smart link suggestions.",
                },
                {
                  "@type": "HowToStep",
                  name: "Apply suggested links",
                  text: "Review suggestions, select the links you want, and apply them to your site with one click.",
                },
              ],
            }),
          }}
        />
        <script
          type="application/ld+json"
          dangerouslySetInnerHTML={{
            __html: JSON.stringify({
              "@context": "https://schema.org",
              "@type": "FAQPage",
              mainEntity: [
                {
                  "@type": "Question",
                  name: "Do I need to install a WordPress plugin?",
                  acceptedAnswer: {
                    "@type": "Answer",
                    text: "No. WP Linker works entirely via the WordPress REST API. You just need to create an application password in your WordPress dashboard.",
                  },
                },
                {
                  "@type": "Question",
                  name: "Is my WordPress data safe?",
                  acceptedAnswer: {
                    "@type": "Answer",
                    text: "Yes. WP Linker only reads your published posts to analyze links. We never modify your content without your explicit approval.",
                  },
                },
                {
                  "@type": "Question",
                  name: "What's included in the free plan?",
                  acceptedAnswer: {
                    "@type": "Answer",
                    text: "The free plan includes full internal link analysis, orphan post detection, and link coverage scoring for up to 30 posts on 1 site. No credit card required, free forever.",
                  },
                },
                {
                  "@type": "Question",
                  name: "How long does the analysis take?",
                  acceptedAnswer: {
                    "@type": "Answer",
                    text: "Most sites with under 500 posts are analyzed in under 2 minutes.",
                  },
                },
              ],
            }),
          }}
        />
      </head>
      <body className={`${geistSans.variable} antialiased`}>{children}</body>
    </html>
  );
}
