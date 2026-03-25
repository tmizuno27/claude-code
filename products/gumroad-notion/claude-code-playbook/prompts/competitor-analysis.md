# Competitor Analysis Prompt

## Objective
Analyze competitors in your niche to identify content gaps, keyword opportunities, product ideas, and strategic advantages.

## Required Context / Inputs
- Your site URL and niche
- 3-5 competitor URLs (or let Claude find them)
- Your current content list (article-management.csv)

## Prompt

```
Perform a competitive analysis for my [NICHE] business.

**My Business:**
- Site: [YOUR URL]
- Niche: [YOUR NICHE]
- Current articles: read outputs/article-management.csv
- Monetization: [affiliate / ads / products / SaaS]

**Competitors to analyze:**
[LIST 3-5 COMPETITOR URLS, or "find the top 5 competitors via web search"]

**Analysis Required:**

1. **Content Gap Analysis**:
   - Web search each competitor's sitemap or main categories
   - List topics they cover that I don't
   - List topics I cover that they don't (my advantage)
   - Identify their most linked/shared content
   - Estimate their content volume and publishing frequency

2. **Keyword Overlap**:
   - Identify keywords where we both compete
   - Identify keywords they rank for that I should target
   - Identify keywords I rank for that they don't (defend these)

3. **Monetization Analysis**:
   - What affiliate programs do they use?
   - What products do they sell?
   - How do they structure their CTAs?
   - What pricing models do they use?
   - Ad placements and density

4. **Strengths & Weaknesses**:
   For each competitor:
   - Domain authority estimate
   - Content quality assessment (depth, originality, freshness)
   - UX and design quality
   - Unique value proposition
   - Biggest weakness I can exploit

5. **Strategic Recommendations**:
   - Top 5 content pieces I should create based on gaps
   - Top 3 keyword clusters to prioritize
   - Monetization tactics to adopt
   - Differentiation strategy (what makes me unique)

**Output:**
- Save to outputs/reports/competitor-analysis-[date].md
- Include comparison table: my_site vs each competitor across key metrics
- Actionable next steps with priority ranking

Niche: [YOUR NICHE]
```

## Expected Output
- `outputs/reports/competitor-analysis-[date].md` — full analysis
- Comparison matrix and prioritized action items

## Example Usage

```
My Business:
- Site: otona-match.com
- Niche: dating app reviews and comparisons (Japanese market)
- Monetization: affiliate (dating app referral programs)
Competitors: find the top 5 via web search
```

## Tips
- Run quarterly — the competitive landscape changes
- Don't just copy competitors; look for what they're all missing
- Focus on exploiting weaknesses rather than competing head-on with strengths
- Use findings to feed your keyword research and content pipeline
