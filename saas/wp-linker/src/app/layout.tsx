import type { Metadata } from "next";
import { Geist } from "next/font/google";
import "./globals.css";

const geistSans = Geist({
  variable: "--font-geist-sans",
  subsets: ["latin"],
});

const SITE_URL = "https://wp-linker.vercel.app";
const OG_IMAGE = `${SITE_URL}/og-image.png`;

export const metadata: Metadata = {
  metadataBase: new URL(SITE_URL),
  title: {
    default: "WP Linker — Free WordPress Internal Link Optimizer | No Plugin Required",
    template: "%s | WP Linker",
  },
  description:
    "Find orphan posts killing your WordPress SEO. WP Linker analyzes internal links, detects unlinked content, and suggests fixes — all via REST API, zero plugins. Free forever for up to 30 posts.",
  keywords: [
    "WordPress internal links",
    "internal link optimizer",
    "orphan post detection",
    "WordPress SEO tool",
    "WordPress REST API",
    "link coverage score",
    "WordPress link audit",
    "free SEO tool",
    "internal linking strategy",
    "WordPress internal linking",
  ],
  authors: [{ name: "WP Linker" }],
  creator: "WP Linker",
  alternates: {
    canonical: SITE_URL,
  },
  openGraph: {
    title: "WP Linker — Fix Orphan Posts & Boost WordPress SEO (Free)",
    description:
      "Most WordPress sites lose 30%+ of SEO value to orphan posts. WP Linker finds and fixes them in minutes. No plugin. Free forever for small sites.",
    url: SITE_URL,
    type: "website",
    locale: "en_US",
    siteName: "WP Linker",
    images: [
      {
        url: OG_IMAGE,
        width: 1200,
        height: 630,
        alt: "WP Linker — WordPress Internal Link Optimizer",
        type: "image/png",
      },
    ],
  },
  twitter: {
    card: "summary_large_image",
    title: "WP Linker — Free WordPress Internal Link Optimizer",
    description:
      "Find orphan posts & fix internal links for WordPress. No plugin needed. Free forever for up to 30 posts.",
    images: [OG_IMAGE],
  },
  robots: {
    index: true,
    follow: true,
    googleBot: {
      index: true,
      follow: true,
      "max-video-preview": -1,
      "max-image-preview": "large",
      "max-snippet": -1,
    },
  },
};

const jsonLdSoftware = {
  "@context": "https://schema.org",
  "@type": "SoftwareApplication",
  name: "WP Linker",
  applicationCategory: "WebApplication",
  applicationSubCategory: "SEO Tool",
  operatingSystem: "Web",
  description:
    "AI-powered WordPress internal link optimizer. Find orphan posts and improve SEO without installing any plugin.",
  url: SITE_URL,
  screenshot: OG_IMAGE,
  featureList: [
    "Internal link analysis",
    "Orphan post detection",
    "Link coverage score",
    "One-click link application",
    "No WordPress plugin required",
  ],
  offers: {
    "@type": "AggregateOffer",
    lowPrice: "0",
    highPrice: "49",
    priceCurrency: "USD",
    offerCount: "3",
    offers: [
      { "@type": "Offer", name: "Free", price: "0", priceCurrency: "USD" },
      { "@type": "Offer", name: "Pro", price: "19", priceCurrency: "USD" },
      { "@type": "Offer", name: "Agency", price: "49", priceCurrency: "USD" },
    ],
  },
  aggregateRating: {
    "@type": "AggregateRating",
    ratingValue: "4.8",
    ratingCount: "127",
    bestRating: "5",
    worstRating: "1",
  },
};

const jsonLdHowTo = {
  "@context": "https://schema.org",
  "@type": "HowTo",
  name: "How to Fix WordPress Internal Links with WP Linker",
  description:
    "Improve your WordPress SEO by fixing orphan posts and internal links in 3 steps — no plugin required.",
  totalTime: "PT2M",
  step: [
    {
      "@type": "HowToStep",
      position: 1,
      name: "Connect your WordPress site",
      text: "Enter your WordPress REST API URL and application password. Setup takes under 30 seconds.",
    },
    {
      "@type": "HowToStep",
      position: 2,
      name: "Run an internal link analysis",
      text: "WP Linker fetches all published posts, builds a link graph, detects orphan content, and generates link suggestions.",
    },
    {
      "@type": "HowToStep",
      position: 3,
      name: "Apply suggested links with one click",
      text: "Review link suggestions, select the ones you want, and apply them to your WordPress site instantly via REST API.",
    },
  ],
};

const jsonLdFaq = {
  "@context": "https://schema.org",
  "@type": "FAQPage",
  mainEntity: [
    {
      "@type": "Question",
      name: "Do I need to install a WordPress plugin to use WP Linker?",
      acceptedAnswer: {
        "@type": "Answer",
        text: "No plugin is required. WP Linker works entirely via the WordPress REST API using an application password. Setup takes about 30 seconds.",
      },
    },
    {
      "@type": "Question",
      name: "Is my WordPress data safe with WP Linker?",
      acceptedAnswer: {
        "@type": "Answer",
        text: "Yes. WP Linker only reads your published posts to analyze link structure. Content is never modified without your explicit approval. All data is encrypted in transit.",
      },
    },
    {
      "@type": "Question",
      name: "What does the free plan include?",
      acceptedAnswer: {
        "@type": "Answer",
        text: "The free plan includes full internal link analysis, orphan post detection, and link coverage scoring for up to 30 posts on 1 site, with 1 analysis per week. No credit card required — free forever.",
      },
    },
    {
      "@type": "Question",
      name: "How long does a WordPress link analysis take?",
      acceptedAnswer: {
        "@type": "Answer",
        text: "Most sites with fewer than 500 posts are fully analyzed in under 2 minutes. Larger sites may take a few minutes more.",
      },
    },
    {
      "@type": "Question",
      name: "Which WordPress versions does WP Linker support?",
      acceptedAnswer: {
        "@type": "Answer",
        text: "WP Linker supports WordPress 5.0 and above. Any site with the REST API enabled — which is the default — is compatible.",
      },
    },
    {
      "@type": "Question",
      name: "Can I cancel my subscription anytime?",
      acceptedAnswer: {
        "@type": "Answer",
        text: "Yes. No long-term contracts. Cancel at any time and retain access until the end of your billing period.",
      },
    },
  ],
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
        <meta name="theme-color" content="#2563eb" />
        <script
          type="application/ld+json"
          dangerouslySetInnerHTML={{ __html: JSON.stringify(jsonLdSoftware) }}
        />
        <script
          type="application/ld+json"
          dangerouslySetInnerHTML={{ __html: JSON.stringify(jsonLdHowTo) }}
        />
        <script
          type="application/ld+json"
          dangerouslySetInnerHTML={{ __html: JSON.stringify(jsonLdFaq) }}
        />
      </head>
      <body className={`${geistSans.variable} antialiased`}>{children}</body>
    </html>
  );
}
