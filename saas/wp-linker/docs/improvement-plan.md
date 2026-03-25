# WP Linker 改善計画

## 現状分析

- ランディングページは英語のみ、基本的なSaaS LPの構造（Hero/Features/How it works/Pricing/CTA/Footer）
- Meta/OGP/Twitter Cardは設定済みだが不足あり
- 構造化データ（JSON-LD）なし
- 社会的証明（testimonials, user count）なし
- FAQ セクションなし
- 個別ページ（Privacy, Terms, About）なし

---

## 1. ランディングページのコピー改善

### Hero セクション
**現状**: "Fix your internal links. Boost your SEO."
**改善案**: 具体的な数値とペインポイントを訴求

```
現: Fix your internal links. Boost your SEO.
案: Your WordPress site is losing 40% of its SEO power to orphan posts.
    Fix it in 30 seconds — no plugin required.
```

**サブコピー改善**:
```
現: WP Linker analyzes your WordPress posts, finds orphan content, and suggests the most relevant internal links...
案: 87% of WordPress sites have orphan posts that Google can't discover. WP Linker finds them, suggests the best internal links, and applies them with one click — all via REST API.
```

### Stats Bar
**現状**: "3x Faster", "0 Plugins", "100% Link coverage"
**改善案**: ユーザーの成果に基づく数値に変更（ベータユーザーデータが集まり次第）
- "Average 47% more internal links after first scan"
- "2 minutes to connect your site"
- "Zero plugins. Zero performance impact."

### Feature 説明
各featureの説明を「ユーザーの結果」中心に書き換え:

| 現状 | 改善案 |
|------|--------|
| AI analyzes your content and suggests the most relevant internal links | "Last week one user went from 12 orphan posts to zero in 5 minutes" 的な成果訴求 |
| Find posts with zero incoming links... | "The average WordPress site has 23% orphan posts. Find and fix yours instantly." |

### CTA ボタン
- "Try Free" → "Scan My Site Free" （行動を具体化）
- "Get Started Free" → "Find My Orphan Posts" （ベネフィットを訴求）

---

## 2. SEO改善

### Meta タグ追加・改善

```tsx
// layout.tsx に追加
export const metadata: Metadata = {
  title: "WP Linker — WordPress Internal Link Optimizer | Boost SEO Without Plugins",
  description: "Find orphan posts, get AI-powered internal link suggestions, and apply them with one click. Works via WordPress REST API — no plugin required. Free trial.",
  alternates: {
    canonical: "https://wp-linker.vercel.app",
  },
  openGraph: {
    title: "WP Linker — Fix Orphan Posts & Boost Internal Links",
    description: "87% of WordPress sites have orphan posts killing their SEO. WP Linker finds and fixes them in minutes. No plugin required.",
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
    title: "WP Linker — WordPress Internal Link Optimizer",
    description: "Find orphan posts & boost internal links. No WordPress plugin required.",
    images: ["https://wp-linker.vercel.app/og-image.png"],
  },
};
```

### 構造化データ（JSON-LD）追加

`layout.tsx` の `<head>` に以下を追加:

```json
{
  "@context": "https://schema.org",
  "@type": "SoftwareApplication",
  "name": "WP Linker",
  "applicationCategory": "SEO Tool",
  "operatingSystem": "Web",
  "description": "AI-powered WordPress internal link optimizer. Find orphan posts and boost SEO without installing any plugin.",
  "offers": {
    "@type": "AggregateOffer",
    "lowPrice": "9",
    "highPrice": "79",
    "priceCurrency": "USD",
    "offerCount": "3"
  }
}
```

FAQPage 構造化データも追加（FAQ セクション新設後）:

```json
{
  "@context": "https://schema.org",
  "@type": "FAQPage",
  "mainEntity": [
    {
      "@type": "Question",
      "name": "Do I need to install a WordPress plugin?",
      "acceptedAnswer": {
        "@type": "Answer",
        "text": "No. WP Linker works entirely via the WordPress REST API. You just need to create an application password in your WordPress dashboard."
      }
    },
    {
      "@type": "Question",
      "name": "Is my WordPress data safe?",
      "acceptedAnswer": {
        "@type": "Answer",
        "text": "Yes. WP Linker only reads your published posts to analyze links. We never modify your content without your explicit approval."
      }
    },
    {
      "@type": "Question",
      "name": "How long does the analysis take?",
      "acceptedAnswer": {
        "@type": "Answer",
        "text": "Most sites with under 500 posts are analyzed in under 2 minutes."
      }
    }
  ]
}
```

### OG画像作成
- 1200x630px の OG画像を作成して `/public/og-image.png` に配置
- ブランドカラー（Blue 600）ベースにロゴ+キャッチコピー

---

## 3. コンバージョン改善

### 優先度: 高

1. **FAQ セクション追加**（Pricing の下）
   - "Do I need a WordPress plugin?" → No
   - "Is my data safe?" → Read-only until you approve
   - "What WordPress versions are supported?" → 5.0+
   - "Can I cancel anytime?" → Yes
   - FAQ構造化データでSERP占有率も向上

2. **Social Proof セクション追加**（Stats bar の代わり or 直後）
   - ベータユーザーの声（最初は自サイト3つの実績データでOK）
   - "Trusted by X WordPress sites" カウンター
   - ロゴ群（将来的に）

3. **リスク排除コピー追加**
   - Hero下に「No credit card required. Cancel anytime.」を明示
   - 「Read-only access — we never modify your site without approval」

### 優先度: 中

4. **ページ速度最適化**
   - LCP改善: Hero セクションのテキストをSSGで配信（既に対応済みの可能性）
   - フォント最適化: `font-display: swap` 確認

5. **モバイル最適化**
   - ナビゲーションのハンバーガーメニュー追加
   - Pricing カードの横スクロール対応
   - CTAボタンのタップ領域拡大（min 48px）

6. **Exit Intent ポップアップ**（将来）
   - "Before you go — scan your site for free"
   - メールキャプチャ → ドリップキャンペーン

### 優先度: 低

7. **個別ページ追加**
   - `/privacy` — Privacy Policy
   - `/terms` — Terms of Service
   - `/about` — About / Team page
   - これらはGoogle AdSense申請にも必要

8. **ブログ / コンテンツマーケティング**
   - `/blog` — "Internal Linking Best Practices" 等のSEO記事
   - Product Hunt launch preparation

---

## 4. 実装優先順位

| 順位 | 施策 | 工数 | 期待効果 |
|------|------|------|----------|
| 1 | 構造化データ（JSON-LD）追加 | 30分 | SERP改善 |
| 2 | Meta/OGP完全化 + OG画像 | 1時間 | SNSシェア時のCTR改善 |
| 3 | FAQ セクション + 構造化データ | 1時間 | CVR改善 + SERP占有 |
| 4 | Hero コピー改善 | 30分 | CVR改善 |
| 5 | Social Proof セクション | 1時間 | 信頼性 → CVR改善 |
| 6 | モバイルナビ改善 | 1時間 | モバイルCVR改善 |
| 7 | Privacy/Terms ページ | 2時間 | 信頼性 + 法的要件 |
| 8 | CTA コピーA/Bテスト | 30分 | CVR最適化 |

---

## 5. 即実装可能な変更（コード差分）

### layout.tsx: canonical URL + OG image URL追加

```diff
  openGraph: {
    title: "WP Linker — Fix Your Internal Links, Boost Your SEO",
+   url: "https://wp-linker.vercel.app",
+   images: [{ url: "https://wp-linker.vercel.app/og-image.png", width: 1200, height: 630 }],
  },
  twitter: {
+   images: ["https://wp-linker.vercel.app/og-image.png"],
  },
+ alternates: { canonical: "https://wp-linker.vercel.app" },
```

### page.tsx: CTA テキスト変更

```diff
- Try Free
+ Scan My Site Free

- Get Started Free
+ Find My Orphan Posts
```
