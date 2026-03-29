# I Built 10 Chrome Extensions in 2 Months — Here's What Actually Drives Installs

**Subtitle:** Data-backed insights from someone who shipped, not just planned

**Tags:** `#chrome` `#javascript` `#webdev` `#productivity` `#ai`

**Reading time:** ~7 minutes

**Published:** Medium (@miccho27) + Dev.to (@miccho27)

---

I shipped 10 Chrome extensions in 2 months. Some flopped. A few are growing steadily. Here's what I learned about what actually drives installs in the Chrome Web Store — and what the advice you read online gets wrong.

---

## Why Chrome Extensions?

Before the data, let me explain why I targeted this platform.

The Chrome Web Store has over 2.7 billion active Chrome users. That's not a niche market — that's a platform. And unlike the App Store or Google Play, the competition in most specific niches is surprisingly thin.

Here's what made extensions attractive for me specifically:

- **Low barrier to entry**: A working extension can be built in a day. Review takes 1–3 weeks, but that's the only gate
- **No platform fees on installs**: You pay nothing to get your extension installed (unlike 30% app store cuts on IAP)
- **Freemium model is natural**: Free core product, paid upgrades — this works well for tools that have genuine power users
- **Discovery through search**: The Web Store has internal search, similar to the App Store. Good SEO = organic installs
- **Persistent presence**: Unlike a web app, an extension icon sits in the browser toolbar. Daily visibility without a marketing budget

The downside: monetization is harder than app stores. But if you build the right tool for the right audience, the math works.

---

## The 10 Extensions I Built

Here's my full portfolio with current status:

| Extension | Category | Model | Status |
|-----------|----------|-------|--------|
| SEO Meta Inspector | SEO Tools | Free | Published |
| Hash & Encode Tool | Developer Tools | Free | Published |
| Japanese Page Translator | Productivity | Freemium | Under Review |
| Readability Checker | Content Tools | Freemium | Under Review |
| Open Graph Preview | SEO/Social | Free | Under Review |
| CSS Selector Helper | Developer Tools | Free | Under Review |
| Tab Manager Pro | Productivity | Freemium | Under Review |
| WordPress Admin Helper | CMS Tools | Freemium | Under Review |
| Affiliate Link Checker | Blogger Tools | Freemium | Under Review |
| Page Speed Badge | SEO Tools | Free | Under Review |

Two published. Eight in the review queue. The Chrome Web Store reviews in batches — submitting multiple at once is the right strategy (more on this below).

**[Search "SEO Meta Inspector" or "Hash Encode Tool" on the Chrome Web Store to find my published extensions.](https://chrome.google.com/webstore)**

---

## How I Use Claude AI to Build Extensions

Each extension follows the same build process. Here's the exact workflow.

### 1. Manifest generation

Manifest v3 is mandatory for new extensions since 2023. The permission model changed significantly from v2, and many Stack Overflow answers are outdated. Claude stays current:

```
Prompt: "Create a Chrome Extension manifest v3 for a tool that
highlights all links on the current page and shows their
href attributes in a popup sidebar. Include only the minimal
permissions needed. Use action popup and content script.
No background service worker needed."
```

Claude returns a valid `manifest.json` with the exact permissions needed — not a kitchen-sink list that triggers security warnings during review.

### 2. Content script logic

Content scripts are the most error-prone part of extension development. They run in the context of the page but in a sandboxed environment. Common pitfalls:

- Accessing `window` properties that don't exist in the extension context
- Injecting HTML without sanitization (huge security risk — will get rejected)
- Blocking the main thread with synchronous operations
- Conflicts with the page's own JavaScript

My Claude prompt for content scripts always includes these constraints:

```
Generate a content script that:
- Uses MutationObserver for dynamic content (not polling)
- Sanitizes any HTML injection with DOMPurify or textContent only
- Communicates with popup via chrome.runtime.sendMessage only
- Fails silently if required DOM elements aren't present
- Works on both HTTP and HTTPS pages
```

### 3. Popup UI

I use a minimal HTML/CSS template that I've standardized across all my extensions. Claude handles the JavaScript logic; I maintain a consistent visual style:

```html
<!DOCTYPE html>
<html>
<head>
  <meta charset="UTF-8">
  <link rel="stylesheet" href="popup.css">
  <style>
    body { width: 320px; min-height: 200px; font-family: system-ui, sans-serif; }
    .container { padding: 16px; }
    .header { font-size: 14px; font-weight: 600; color: #1a1a1a; margin-bottom: 12px; }
    .result { background: #f5f5f5; border-radius: 8px; padding: 12px; font-size: 13px; }
  </style>
</head>
<body>
  <div class="container">
    <div class="header">Extension Name</div>
    <div id="result" class="result">Loading...</div>
  </div>
  <script src="popup.js"></script>
</body>
</html>
```

Consistent UI across extensions builds a recognizable brand in the Web Store.

---

## What Actually Drives Installs: The Data

After publishing 2 extensions and watching Web Store analytics, here's what I've found.

### Title is everything (accounts for ~70% of CTR)

The Web Store search algorithm weights the extension title heavily. Most developers write titles like product names — which is wrong for discoverability.

**Bad title:** `JSON Formatter`

**Good title:** `JSON Formatter & Validator — Pretty Print, Minify, Tree View`

The good title includes:
- Primary keyword (what users search for)
- Secondary use case (validates, not just formats)
- Specific features (Pretty Print, Minify, Tree View — things users type in search)

Same product. Dramatically different visibility.

### Screenshots convert better than icons

My first extension had a polished icon and a single screenshot showing the popup. Installs: zero for two weeks.

After adding three annotated screenshots showing the extension working on a real webpage — identifying actual DOM elements, showing color-coded output — installs started within three days.

The rule: **don't screenshot your UI in isolation. Show it solving a real problem on a real page.**

For developer tools, showing the output on a GitHub page works well. For SEO tools, show it on a popular blog or news site. Users recognize the context and understand the value immediately.

### Three trust signals that convert

Extensions have a trust problem. Users are (rightfully) cautious about installing code that runs on every page they visit. Generic "free extension!" copy doesn't address this.

My listing copy that works:

```
✅ No account required — works immediately after install
✅ Offline-capable — no data sent to external servers
✅ Open source — review the code on GitHub
```

These three lines directly address the three concerns users have:

1. "Will I have to sign up and give you my email?" — No
2. "Are you tracking my browsing?" — No
3. "How do I know you're not lying?" — Here's the source code

Adding these to my second extension's description visibly improved the install-to-impression ratio.

### Category matters more than you think

The Web Store has specific category pages, and category matters for two reasons:

1. Users browse "Featured" extensions by category
2. The algorithm considers category fit when surfacing extensions in search

If your extension does five things, it still needs one primary category. Pick the category that matches the primary use case, not the broadest possible bucket.

"Developer Tools" works well for extensions that directly help developers. "Productivity" is overcrowded. "SEO Tools" is a real category with real searchers.

---

## The Freemium Split That Works

I tested several models. Here's what I've converged on:

**Free tier** (core functionality — works for 80% of users):
- No account needed
- No usage caps on the main feature
- No watermarks or nag screens

**Pro tier** ($2.99/month or $19.99/year):
- Bulk processing (export results, batch analysis)
- Save and sync settings across devices
- Priority features and advanced options
- Email support

The critical insight: **the free tier must be genuinely useful.** Not crippled-useful. Not "useful if you don't need the main thing" useful. Actually useful.

Users who feel tricked by a bait-and-switch freemium model don't just uninstall — they leave one-star reviews. And in the Web Store, reviews are hard to recover from.

Give the core value for free. Charge for the power-user features. This builds trust and converts naturally.

---

## Build Time: The Real Numbers

Average time per extension with Claude AI assistance:

| Phase | Time |
|-------|------|
| Concept definition and competitive research | 1 hour |
| Initial code generation and review | 2 hours |
| Testing and bug fixes | 2 hours |
| Store assets (screenshots, description, icon) | 2 hours |
| Submission and review prep | 30 minutes |
| **Total** | **~7.5 hours** |

Without AI assistance, I estimate 2–3x longer — mostly in initial code generation and debugging. The hard parts of extension development (permission modeling, Chrome API edge cases, content script sandboxing) are exactly where Claude adds the most time savings.

For reference: 10 extensions × 7.5 hours = 75 hours over 2 months. That's roughly one hour per weekday. Doable alongside other work.

---

## What I'd Do Differently

### 1. Research before building (not after)

I built three extensions before checking the Web Store competition. All three had well-established competitors with thousands of reviews. I still shipped them — but I would have prioritized differently if I'd done the competitive analysis first.

Now I run this check before committing to build:

```
Chrome Web Store search: [main keyword]
→ How many results?
→ What's the rating distribution?
→ When was the last update?
→ Are there user complaints in reviews?
```

Old, poorly-maintained extensions with mediocre ratings are opportunities. New extensions with recent updates and 4.5+ stars are not.

### 2. Build for a specific audience, not a broad category

"Developer tools" as a positioning is too vague. Users don't search for "developer tools" — they search for "JSON formatter" or "HTTP header inspector."

Better positioning: **one specific person, one specific problem.**

"Built for Next.js developers who debug API routes" beats "a tool for web developers." The specific positioning converts better, even if the total addressable audience is smaller.

### 3. Submit multiple extensions simultaneously

The review process is the bottleneck — 1 to 3 weeks per submission. But you can have multiple extensions under review at the same time. If I'd known this from day one, I would have built all 10 first, then submitted them in a batch.

Instead, I submitted sequentially and spent weeks waiting. Batch submission = faster time to market for the full portfolio.

---

## The Privacy Policy Requirement

One practical note: every extension (even free, even ones with zero permissions) needs a published Privacy Policy URL to submit. This tripped me up on my first submission.

My solution: I host all privacy policies on a static Vercel page:

```
https://[your-domain].vercel.app/privacy-policy-[extension-name].html
```

Build a simple template once, update it for each extension, host it for free. Chrome Web Store validation requires the URL to be live before submission is accepted.

---

## What's Next

I'll post updated install numbers and revenue data once more extensions are live and I have a few months of data. The current portfolio is still in early stages — the story will be more interesting with real conversion numbers.

If you're building Chrome extensions and have questions about the workflow, the manifest v3 transition, or the freemium model, drop a comment. Happy to go deeper on any of these.

---

*I build developer tools, APIs, and automation systems from Paraguay. Follow for updates on this extension portfolio and other projects.*

*All published extensions searchable on the Chrome Web Store — search "SEO Meta Inspector" or "Hash Encode Tool".*
