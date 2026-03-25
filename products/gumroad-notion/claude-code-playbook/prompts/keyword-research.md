# Keyword Research Prompt

## Objective
Analyze your niche, identify content gaps, and generate a prioritized keyword queue with search intent classification and revenue potential scoring.

## Required Context / Inputs
- `outputs/article-management.csv` — your existing published articles
- Google Search Console data export (optional, improves accuracy)
- Your niche/topic area defined

## Prompt

```
Perform comprehensive keyword research for my [NICHE] website.

1. **Existing Content Audit**:
   - Read outputs/article-management.csv to understand what topics I've already covered
   - Identify topic clusters I've started but haven't fully built out
   - Find orphan topics with no related articles

2. **Gap Analysis**:
   - Web search for top competitors in [NICHE]
   - Identify keywords they rank for that I don't cover
   - Find "People Also Ask" opportunities for my existing topics
   - Look for emerging trends and seasonal keywords

3. **Keyword Clustering**:
   - Group keywords by topic cluster (parent topic + subtopics)
   - Classify each keyword by search intent:
     - Informational (how-to, what-is, guide)
     - Commercial (best, review, comparison, vs)
     - Transactional (buy, discount, coupon, pricing)
     - Navigational (brand + feature)

4. **Prioritization**:
   Score each keyword cluster 1-10 on:
   - Estimated search volume (based on web research)
   - Competition level (how strong are current top results)
   - Affiliate/revenue potential (can I monetize this with my current affiliate programs)
   - Content effort (how much research/expertise needed)
   - Calculate priority = (volume * revenue_potential) / (competition * effort)

5. **Output**:
   - Save to inputs/keyword-queue.csv with columns:
     keyword, cluster, intent, volume_estimate, competition, revenue_potential, effort, priority_score, notes
   - Sort by priority_score descending
   - Include 30-50 keywords minimum

Niche: [YOUR NICHE]
Website URL: [YOUR URL]
Current article count: [NUMBER]
Primary monetization: [adsense / affiliate / products / services]
Affiliate programs available: [list your ASPs or read from config/affiliate-links.json]
```

## Expected Output
- `inputs/keyword-queue.csv` — prioritized keyword list
- Console summary: top 10 keywords with rationale

## Example Usage

```
Niche: budget travel in South America
Website URL: example-travel-blog.com
Current article count: 45
Primary monetization: affiliate (booking.com, travel insurance, SIM cards)
Affiliate programs: read from config/affiliate-links.json
```

## Tips
- Run monthly to keep your content pipeline fresh
- Cross-reference with GSC data if available — keywords you already get impressions for but don't rank well are quick wins
- Focus on commercial intent keywords first if revenue is the priority
