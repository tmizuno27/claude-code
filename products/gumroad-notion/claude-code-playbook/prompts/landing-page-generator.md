# Landing Page Generator Prompt

## Objective
Generate a complete, conversion-optimized landing page in HTML/CSS for a product, service, or lead magnet.

## Required Context / Inputs
- Product/service details
- Target audience
- Desired style (modern, minimal, bold)

## Prompt

```
Build a complete landing page for [PRODUCT/SERVICE].

**Page Details:**
- Product: [NAME AND DESCRIPTION]
- Target audience: [WHO IS THIS FOR]
- Primary CTA: [BUTTON TEXT + URL]
- Style: [modern minimal / bold gradient / corporate clean / dark tech]
- Responsive: yes, mobile-first

**Page Sections:**

1. **Hero Section**:
   - Headline (8-12 words, benefit-focused)
   - Subheadline (15-25 words, elaborates on the headline)
   - CTA button
   - Hero visual placeholder

2. **Problem Section**:
   - 3 pain points the audience faces
   - Each with an icon placeholder and short description

3. **Solution Section**:
   - How your product solves each pain point
   - Feature grid (3-4 features with icons)

4. **Social Proof**:
   - Testimonial cards (3 placeholders)
   - Stats bar ("500+ users", "4.9/5 rating", etc.)

5. **Pricing** (if applicable):
   - Pricing card(s)
   - Feature comparison if multiple tiers

6. **FAQ**:
   - 5-6 accordion-style Q&As

7. **Final CTA**:
   - Urgency-driven headline
   - CTA button
   - Risk reversal (guarantee, free trial mention)

**Technical Requirements:**
- Single HTML file with embedded CSS
- No external dependencies (no frameworks, no CDN)
- Smooth scroll, hover effects, responsive grid
- Performance: should load in under 1 second
- Color scheme: [SPECIFY OR "generate a professional palette"]

**Output:**
- Save to outputs/landing-pages/[product-slug]/index.html
- Start a local server to preview

Product: [YOUR PRODUCT]
```

## Expected Output
- `outputs/landing-pages/[product-slug]/index.html` — complete page
- Local server running for preview

## Tips
- Test on mobile — most traffic is mobile
- The hero section determines 80% of conversions. Spend time on that headline.
- Include a favicon and Open Graph meta tags for sharing
