# SEO Article Writer Mega Prompt Pack
## 50 Battle-Tested Prompts for Claude & ChatGPT — $19

> These prompts are extracted and refined from a production content pipeline that generates, publishes, and ranks SEO articles automatically. They are not generic templates — each one is proven in a real-world workflow.

---

## CATEGORY 1: Keyword Research & Strategy (10 Prompts)

### Prompt 1: Seed Keyword Expansion
```
You are an SEO keyword researcher specializing in [NICHE].

Given the seed keyword "[SEED_KEYWORD]", generate 30 long-tail keyword variations using these patterns:
- Question patterns: [KEYWORD] + とは / 始め方 / おすすめ / 稼ぎ方 / やり方 / メリット / デメリット / 注意点 / 比較 / 無料 / 方法 / コツ
- "[KEYWORD] for [AUDIENCE]" variations (beginners, professionals, seniors, students)
- "[KEYWORD] vs [COMPETITOR]" comparison queries
- "[YEAR] [KEYWORD]" time-sensitive variants
- "best [KEYWORD] [USE_CASE]" intent-rich queries

For each keyword, classify as:
- "question" (informational intent)
- "longtail" (3+ words, specific intent)
- "main" (head term, high competition)

Prioritize longtail keywords (3+ words, 8-25 characters) as they have the best ROI for new sites.

Output as a JSON array: [{"keyword": "...", "type": "...", "estimated_difficulty": "low/medium/high"}]
```
**Usage**: Feed this into your content calendar. Focus on "longtail" and "question" types first.
**Expected output**: 30 classified keyword suggestions with difficulty estimates.
**Tip**: Run this for each content pillar separately to maintain topical authority.

---

### Prompt 2: Content Calendar Generator
```
You are a content strategist for a [NICHE] blog targeting [AUDIENCE].

Create a 4-week content calendar (3 articles per week) based on these seed keywords:
[KEYWORD_LIST]

Requirements:
- Week 1-2: Focus on informational "question" keywords (build trust + traffic)
- Week 3-4: Mix in commercial "comparison" and "review" keywords (monetization)
- Each article entry must include:
  - Target keyword
  - Article type: informational / comparison / review / how-to / listicle
  - Suggested title (with [YEAR] if relevant)
  - Internal linking targets (which other articles from this calendar to link to)
  - Monetization potential: none / affiliate / product / adsense

Ensure topical clustering: group related articles together for internal linking strength.

Output as a markdown table.
```
**Usage**: Plan your entire month of content in one shot.
**Expected output**: 12-article content calendar with linking strategy.
**Tip**: Run Prompt 1 first, then feed the results into this prompt.

---

### Prompt 3: Competitor Content Gap Analysis
```
I run a [NICHE] blog. My main competitors are:
1. [COMPETITOR_URL_1]
2. [COMPETITOR_URL_2]
3. [COMPETITOR_URL_3]

Based on common topics in this niche, identify:
1. **Topics they all cover** (must-have content, compete on quality)
2. **Topics only 1-2 cover** (opportunity gaps)
3. **Topics none cover** (blue ocean keywords)
4. **Underserved angles** (same topic but different audience/format)

For each gap, suggest:
- Target keyword
- Suggested article title
- Why this is an opportunity
- Estimated difficulty (low/medium/high)

Focus on keywords where a new site can realistically rank within 3-6 months.
```
**Usage**: Find content opportunities your competitors are missing.
**Expected output**: Categorized list of 15-20 content opportunities.
**Tip**: Combine with Google Search Console data for maximum accuracy.

---

### Prompt 4: Keyword Intent Classifier
```
Classify the following keywords by search intent and suggest the best content format for each:

Keywords:
[KEYWORD_LIST]

For each keyword, provide:
1. **Intent**: Informational / Navigational / Commercial / Transactional
2. **Content format**: How-to guide / Listicle / Comparison / Review / Tutorial / FAQ / News
3. **Target word count**: Short (800-1200) / Medium (1500-2500) / Long (2500-4000)
4. **Monetization fit**: Affiliate / AdSense / Product / Lead magnet / None
5. **Priority score** (1-10): Based on search volume potential vs. competition

Output as a markdown table sorted by priority score descending.
```
**Usage**: Prioritize your keyword queue by commercial value.
**Expected output**: Classified keyword table with actionable recommendations.
**Tip**: Keywords with commercial or transactional intent should be written first for revenue.

---

### Prompt 5: Topical Authority Map
```
I'm building topical authority in [NICHE]. My site currently has these articles:
[ARTICLE_LIST_WITH_URLS]

Create a topical authority map showing:
1. **Pillar pages** I need (broad topics, 3000+ words)
2. **Cluster articles** for each pillar (specific subtopics, 1500-2500 words)
3. **Supporting articles** (FAQ, how-to, definitions, 800-1200 words)
4. **Missing connections** (articles that exist but aren't linked properly)
5. **Content gaps** (essential subtopics I haven't covered yet)

Visualize this as a hierarchy:
Pillar → Clusters → Supporting articles

For each missing piece, provide the target keyword and suggested title.
```
**Usage**: Build a complete topical authority strategy.
**Expected output**: Hierarchical content map with gaps identified.
**Tip**: Update this map monthly as you publish new content.

---

### Prompt 6: Search Volume Estimator (No Tools Required)
```
For the following keywords in [LANGUAGE/MARKET], estimate relative search volume and competition:

Keywords:
[KEYWORD_LIST]

Use these signals to estimate:
- Keyword length (shorter = usually higher volume)
- Specificity (more specific = lower volume but lower competition)
- Commercial intent (buying keywords = higher competition)
- Seasonal patterns (if applicable)
- Question format (often moderate volume, low competition)

Rate each keyword:
- **Volume**: Very High / High / Medium / Low / Very Low
- **Competition**: Very High / High / Medium / Low / Very Low
- **Opportunity Score**: (Volume × Inverse Competition) = 1-10

Output as a table sorted by Opportunity Score descending.
```
**Usage**: Rough keyword prioritization without paid SEO tools.
**Expected output**: Prioritized keyword table with opportunity scores.
**Tip**: Cross-reference with Google Trends for seasonal keywords.

---

### Prompt 7: Google Suggest Keyword Expander
```
I want to find long-tail keywords using Google Autocomplete patterns. For the seed keyword "[SEED_KEYWORD]", generate keyword suggestions using these patterns:

1. **Alphabet soup**: [KEYWORD] a, [KEYWORD] b, ... [KEYWORD] z
2. **Question modifiers**: how to [KEYWORD], what is [KEYWORD], why [KEYWORD], when [KEYWORD], where [KEYWORD]
3. **Preposition modifiers**: [KEYWORD] for, [KEYWORD] with, [KEYWORD] without, [KEYWORD] near, [KEYWORD] vs
4. **Year modifiers**: [KEYWORD] [CURRENT_YEAR], best [KEYWORD] [CURRENT_YEAR]
5. **Qualifier modifiers**: best [KEYWORD], free [KEYWORD], cheap [KEYWORD], top [KEYWORD]

For each pattern, suggest 3-5 realistic autocomplete completions based on your knowledge.
Mark any that seem particularly low-competition as "[LOW COMP]".
```
**Usage**: Simulate Google Suggest API results for brainstorming.
**Expected output**: 50-80 keyword variations organized by pattern.
**Tip**: Verify the top candidates in actual Google search to confirm autocomplete.

---

### Prompt 8: LSI Keyword Generator
```
For the primary keyword "[PRIMARY_KEYWORD]", generate a comprehensive list of LSI (Latent Semantic Indexing) keywords that should appear naturally in a well-written article.

Organize into:
1. **Must-include terms** (Google expects these in any quality article on this topic)
2. **Strongly related terms** (improve topical relevance)
3. **Entity mentions** (brands, tools, people, places related to the topic)
4. **Action verbs** commonly associated with this topic
5. **Adjective/descriptor terms** readers use when discussing this topic

For each term, note where it fits best in an article:
- Title/H1
- H2/H3 headings
- First paragraph
- Body text
- FAQ section
- Meta description
```
**Usage**: Ensure your articles have complete topical coverage.
**Expected output**: 40-60 LSI terms organized by placement.
**Tip**: Naturally weave these into your content — never keyword-stuff.

---

### Prompt 9: Content Refresh Audit
```
Analyze this existing article and suggest improvements for better SEO performance:

Title: [ARTICLE_TITLE]
URL: [URL]
Published: [DATE]
Current keyword: [TARGET_KEYWORD]
Current word count: [WORD_COUNT]

Content:
[PASTE_ARTICLE_CONTENT]

Evaluate and provide specific recommendations for:
1. **Title optimization**: Is the keyword included? Is it compelling? Character count?
2. **Meta description**: Suggest an optimized 120-character description
3. **H2/H3 structure**: Are headings keyword-rich and logically organized?
4. **Content gaps**: What subtopics are missing that competitors likely cover?
5. **Internal linking opportunities**: What related topics should this link to?
6. **Content freshness**: What data/information needs updating for [CURRENT_YEAR]?
7. **E-E-A-T signals**: How can experience, expertise, authority, and trust be strengthened?
8. **FAQ additions**: Suggest 3 FAQ questions with answers for schema markup

Provide a priority-ranked action list with estimated impact (high/medium/low).
```
**Usage**: Revive underperforming articles.
**Expected output**: Detailed audit report with prioritized action items.
**Tip**: Focus on articles that rank positions 5-20 — they have the most upside.

---

### Prompt 10: Keyword Clustering for Silo Structure
```
I have the following list of keywords for my [NICHE] blog:
[KEYWORD_LIST]

Group these keywords into content silos (topical clusters) where:
- Each silo has 1 pillar keyword and 3-8 supporting keywords
- Keywords within a silo share clear topical relevance
- Supporting keywords answer specific questions about the pillar topic
- No keyword appears in more than one silo

For each silo, provide:
1. **Pillar keyword** and suggested pillar article title
2. **Supporting keywords** with suggested article titles
3. **Internal linking plan**: How each supporting article links to the pillar and to each other
4. **Publishing order**: Which article to publish first for maximum SEO impact

Output as a structured outline with clear hierarchy.
```
**Usage**: Build a silo structure for maximum topical authority.
**Expected output**: Organized silo map with publishing strategy.
**Tip**: Publish pillar content first, then add supporting articles over 2-4 weeks.

---

## CATEGORY 2: Article Generation (15 Prompts)

### Prompt 11: Full SEO Article Generator (The Core Prompt)
```
# Article Generation Request

## Target Keyword
[KEYWORD]

## Requirements
- **Word count**: [MIN_WORDS]-[MAX_WORDS] words (body text only)
- **Language**: [LANGUAGE]
- **SEO optimization**: Naturally incorporate the target keyword throughout
- **Target audience**: [AUDIENCE_DESCRIPTION]
- **Tone**: Friendly and practical. Include specific steps and numbers.
- **Author name**: "[AUTHOR_NAME]"

## Article Structure
Follow this template:

### Meta Information
- Title: Include keyword + year if relevant + compelling benefit
- Meta description: Max 120 characters, include keyword, end with action verb

### Sections (follow this order):
1. **Introduction** (200 words max): Hook with reader's pain point, state what they'll learn
2. **H2 Section 1** (400-600 words): [SUBTOPIC_1]
3. **H2 Section 2** (400-600 words): [SUBTOPIC_2]
4. **Personal Experience Section** (300-500 words): First-person account of actually doing/using this
5. **Pitfalls & Caveats** (300-400 words): Honest drawbacks and limitations
6. **FAQ** (3 questions with 100-150 word answers)
7. **Summary** (3 concise bullet points + call to action)

## Formatting
- Markdown format
- Line 1: # Article Title (must contain the keyword)
- Use H2/H3 headings with keywords where natural
- Include comparison tables where relevant
- Add blockquotes for key insights: > Point text
- End with a summary section

## Constraints
- Do NOT use: "In conclusion," / "Without further ado" / "In this article, we will"
- Do NOT end with a question like "What do you think?"
- Include specific numbers, tool names, and actionable steps
- Every claim must be factually accurate — mark uncertain facts with [VERIFY]
```
**Usage**: Your primary article generation prompt. Customize the sections per article type.
**Expected output**: Complete 2000-3500 word SEO article in Markdown.
**Tip**: Always add your own personal experience section after generation.

---

### Prompt 12: Article Outline Generator
```
Create a detailed SEO-optimized article outline for the keyword "[KEYWORD]".

Requirements:
- Target audience: [AUDIENCE]
- Article type: [how-to / listicle / comparison / review / guide]
- Target word count: [WORD_COUNT]

Generate:
1. **Title options** (3 variations, each containing the keyword):
   - Curiosity-driven title
   - Number-driven title
   - Benefit-driven title

2. **H2/H3 structure** with:
   - Keyword placement in headings
   - Target word count per section
   - Key points to cover in each section
   - Where to place CTAs or affiliate links

3. **Internal linking opportunities**: Suggest 3-5 related article topics to link to

4. **FAQ suggestions**: 5 questions people commonly ask about this topic

5. **Meta description**: 120-character SEO description

Mark sections that need personal experience/expertise with [EXPERT_INPUT_NEEDED].
```
**Usage**: Plan your article structure before writing.
**Expected output**: Complete article blueprint ready for writing.
**Tip**: Use this outline to brief a human writer or feed into Prompt 11.

---

### Prompt 13: Introduction Hook Generator
```
Write 5 different opening paragraphs (hooks) for an article about "[KEYWORD]" targeting [AUDIENCE].

Each hook should be under 200 words and use a different technique:

1. **Pain point hook**: Start with the reader's frustration
2. **Story hook**: Open with a brief personal anecdote
3. **Statistic hook**: Lead with a surprising number or fact
4. **Question hook**: Ask a thought-provoking question
5. **Contrarian hook**: Challenge a common assumption

Requirements:
- Each hook must naturally include the target keyword within the first 100 words
- End each hook with a clear "what you'll learn" preview (3 bullet points)
- Tone: [CASUAL/PROFESSIONAL/AUTHORITATIVE]
- Do NOT use cliches like "In today's world" or "Have you ever wondered"
```
**Usage**: Test different opening styles, pick the most compelling one.
**Expected output**: 5 distinct article introductions.
**Tip**: The pain point hook works best for commercial keywords; the story hook works best for informational content.

---

### Prompt 14: Comparison Article Generator
```
Write a detailed comparison article: "[PRODUCT_1] vs [PRODUCT_2] vs [PRODUCT_3]"

Target keyword: [KEYWORD]
Audience: [AUDIENCE]

Structure:
1. **Quick verdict** (50 words): Which one wins and why, in one sentence each
2. **Comparison table**:
   | Feature | [PRODUCT_1] | [PRODUCT_2] | [PRODUCT_3] |
   |---------|-------------|-------------|-------------|
   | Price | | | |
   | Best for | | | |
   | Key strength | | | |
   | Key weakness | | | |
   | Our rating | /5 | /5 | /5 |
   | Link | [See details]([URL]) | [See details]([URL]) | [See details]([URL]) |

3. **Individual deep-dive** (300-400 words each):
   - Pros (3-5 bullet points)
   - Cons (2-3 bullet points)
   - Best for: [specific use case]
   - Price breakdown

4. **Head-to-head scenarios**:
   - "Choose [PRODUCT_1] if..."
   - "Choose [PRODUCT_2] if..."
   - "Choose [PRODUCT_3] if..."

5. **FAQ** (5 questions)
6. **Final recommendation** with affiliate link

Be objective. Mention real drawbacks. Do not be overly promotional.
```
**Usage**: High-converting comparison content for affiliate monetization.
**Expected output**: 2500-3500 word comparison article.
**Tip**: The comparison table appears in featured snippets — optimize it.

---

### Prompt 15: Listicle Article Generator
```
Write a "[NUMBER] Best [TOPIC] in [YEAR]" listicle article.

Target keyword: [KEYWORD]
Audience: [AUDIENCE]

For each item in the list, include:
1. **Name** (H3 heading with number)
2. **One-line verdict** (bold)
3. **Description** (100-150 words)
4. **Key features** (3-5 bullet points)
5. **Price**: Specific pricing info
6. **Best for**: One specific use case
7. **Link**: [Check current price]([URL]) or [Visit official site]([URL])

Article structure:
- Introduction with keyword in first 100 words
- "How We Evaluated" section (your criteria, 100 words)
- The numbered list (main content)
- "How to Choose the Right [TOPIC]" section (buyer's guide, 300 words)
- FAQ (3 questions)
- Summary table (all items compared)

Sort items by: Best overall first, then by specific use case.
Do NOT rank items purely by price — rank by value.
```
**Usage**: Listicles consistently rank well and convert for affiliate revenue.
**Expected output**: Complete listicle article (2000-3000 words).
**Tip**: Google prefers listicles with genuine opinions over generic feature lists.

---

### Prompt 16: How-To Tutorial Generator
```
Write a step-by-step tutorial: "How to [TASK]"

Target keyword: [KEYWORD]
Audience: [AUDIENCE] (assume [SKILL_LEVEL] skill level)

Structure:
1. **Introduction** (150 words): What they'll achieve and why this method works
2. **Prerequisites**: What they need before starting (tools, accounts, etc.)
3. **Time estimate**: How long this will take
4. **Step-by-step instructions**:
   - Number each step clearly (Step 1, Step 2, etc.)
   - Each step: 100-200 words
   - Include what to click, what to type, what to expect
   - Add "Tip:" callouts for shortcuts or common mistakes
   - Add "Warning:" callouts for things that can go wrong
5. **Troubleshooting**: 3 common problems and their solutions
6. **Next steps**: What to do after completing this tutorial
7. **FAQ**: 3 questions

Requirements:
- Be extremely specific (mention exact button names, menu locations)
- Include expected results at each step so readers can verify they're on track
- Suggest where screenshots would be helpful: [SCREENSHOT: description]
```
**Usage**: Tutorial content for informational keywords.
**Expected output**: Complete step-by-step guide (1500-2500 words).
**Tip**: Add real screenshots before publishing for much better engagement.

---

### Prompt 17: Product Review Article Generator
```
Write an in-depth review of [PRODUCT_NAME].

Target keyword: "[PRODUCT_NAME] review [YEAR]"
Audience: [AUDIENCE]

Structure:
1. **Quick verdict box** (50 words):
   - Rating: X/10
   - Best for: [use case]
   - Price: [price]
   - [Get PRODUCT_NAME]([AFFILIATE_URL])

2. **What is [PRODUCT_NAME]?** (200 words): Brief overview for newcomers
3. **Who is it for?** (150 words): Ideal user profile
4. **Features deep-dive** (500 words):
   - Feature 1: What it does + my experience
   - Feature 2: What it does + my experience
   - Feature 3: What it does + my experience
5. **Pricing breakdown** (200 words): Plans, what's included, hidden costs
6. **Pros and Cons** (bullet list):
   - Pros (5-7 items)
   - Cons (3-5 items, be honest)
7. **[PRODUCT_NAME] vs Alternatives** (comparison table, 3 alternatives)
8. **My experience** (300 words): [PERSONAL_EXPERIENCE_PLACEHOLDER]
9. **Who should NOT buy this** (100 words): Honest anti-recommendation
10. **Final verdict** (100 words + CTA)
11. **FAQ** (5 questions)

Mark personal experience sections with [ADD YOUR EXPERIENCE] placeholders.
```
**Usage**: Review content for transactional keywords.
**Expected output**: Complete product review (2500-3500 words).
**Tip**: Honest cons make your reviews more trustworthy and convert better.

---

### Prompt 18: FAQ Section Generator
```
Generate a comprehensive FAQ section for an article about "[KEYWORD]".

Create 8-10 questions that:
1. Match actual "People Also Ask" patterns (start with How, What, Why, When, Where, Can, Is, Does)
2. Cover these intent types:
   - Definition questions (What is...?)
   - Process questions (How to...?)
   - Comparison questions (Which is better...?)
   - Cost questions (How much does... cost?)
   - Validity questions (Is... worth it?)
3. Each answer: 80-120 words, concise and direct
4. First sentence of each answer directly answers the question (for featured snippets)
5. Include the target keyword naturally in at least 3 answers

Format as:
**Q: [Question]**
A: [Answer]

Also provide the FAQ schema JSON-LD markup for the top 5 questions.
```
**Usage**: Add FAQ sections to boost on-page SEO and featured snippet chances.
**Expected output**: 8-10 Q&A pairs + schema markup code.
**Tip**: FAQ schema markup can give you rich results in Google search.

---

### Prompt 19: Meta Description Generator
```
Write 5 meta description variations for an article with:
- Title: "[ARTICLE_TITLE]"
- Target keyword: "[KEYWORD]"
- Article type: [ARTICLE_TYPE]

Requirements for each variation:
- Maximum 155 characters (strict limit)
- Include the target keyword within the first 70 characters
- End with a call to action (learn, discover, find out, compare, get started)
- Include a unique value proposition or hook
- Use active voice
- Do NOT use "in this article" or "read on to"

Variations:
1. **Benefit-focused**: Lead with what the reader gains
2. **Curiosity-focused**: Create intrigue
3. **Number-focused**: Include a specific number or statistic
4. **Question-focused**: Ask a compelling question
5. **Urgency-focused**: Imply timeliness or scarcity

For each, show character count in parentheses.
```
**Usage**: Improve CTR from search results.
**Expected output**: 5 meta descriptions with character counts.
**Tip**: Google often rewrites meta descriptions, but good ones get kept ~65% of the time.

---

### Prompt 20: Title Tag Optimizer
```
I need SEO-optimized title tags for these articles:

[LIST OF ARTICLE_TOPIC + TARGET_KEYWORD PAIRS]

For each, generate 3 title variations:
1. **Keyword-first**: [KEYWORD]: [Benefit/Hook]
2. **Number-first**: [Number] [KEYWORD] [Promise] ([YEAR])
3. **How-to**: How to [Action] [KEYWORD] [Result]

Rules:
- Maximum 60 characters (strict — show count)
- Target keyword appears in the first half
- Include [YEAR] where it adds value
- Include power words: Ultimate, Complete, Proven, Essential, Step-by-Step
- Do NOT use clickbait or misleading titles

Rate each title: CTR potential (1-5 stars) and keyword optimization (1-5 stars).
```
**Usage**: Optimize title tags for CTR and rankings.
**Expected output**: Multiple title options per article with ratings.
**Tip**: Test different titles and check CTR in Search Console after 2-4 weeks.

---

### Prompt 21: Article Body Expander
```
I have a thin section in my article that needs expansion. Expand the following section from [CURRENT_WORDS] words to [TARGET_WORDS] words while maintaining quality:

Current section:
"""
[PASTE_THIN_SECTION]
"""

Section heading: [H2_HEADING]
Article keyword: [KEYWORD]
Article audience: [AUDIENCE]

Expansion requirements:
- Add specific examples, data points, or case studies
- Include a practical tip or actionable advice
- Add a comparison or contrast to illustrate the point
- Maintain the same tone and style
- Naturally incorporate 1-2 LSI keywords: [LSI_KEYWORD_1], [LSI_KEYWORD_2]
- Do NOT pad with fluff or repeat the same point
- Every added sentence must provide new information or insight
```
**Usage**: Improve thin content sections without padding.
**Expected output**: Expanded section with genuine added value.
**Tip**: Google penalizes fluff — only expand if there's genuinely more to say.

---

### Prompt 22: Article Rewriter (Uniqueness Pass)
```
Rewrite the following article section to be 100% unique while preserving all factual information and the same structure:

Original:
"""
[PASTE_CONTENT]
"""

Requirements:
- Change sentence structure, not just swap synonyms
- Maintain the same reading level and tone
- Keep all numbers, statistics, and facts identical
- Preserve all headings (H2/H3) and their hierarchy
- Keep technical terms unchanged
- The rewritten version should pass AI detection tools
- Aim for the same word count (±10%)

Do NOT:
- Introduce new information
- Remove any facts or data points
- Change the meaning of any statement
- Use overly complex vocabulary to seem different
```
**Usage**: Make AI-generated drafts more human and unique.
**Expected output**: Completely rewritten version maintaining accuracy.
**Tip**: Always add personal insights after rewriting for E-E-A-T signals.

---

### Prompt 23: Content Brief Generator
```
Create a comprehensive content brief for a writer/AI to produce an article on "[KEYWORD]".

The brief should include:

1. **Target keyword**: [KEYWORD]
2. **Secondary keywords**: 5-8 related terms to include
3. **Search intent**: What the searcher actually wants
4. **Target word count**: With section-level word count targets
5. **Audience profile**: Demographics, knowledge level, pain points
6. **Tone and style**: Specific writing guidelines
7. **Required sections**: H2/H3 outline with key points per section
8. **Must-mention topics**: Things that MUST be covered for completeness
9. **Avoid topics**: Things to NOT cover (off-topic, competitor promotion, etc.)
10. **CTA strategy**: What action should the reader take?
11. **Linking plan**:
    - 3-5 internal links to suggest
    - 2-3 authoritative external sources to reference
12. **Visual content needs**: Suggested images, tables, or infographics
13. **SEO checklist**:
    - [ ] Keyword in title, H1, first 100 words
    - [ ] Keyword in at least 2 H2 headings
    - [ ] Meta description under 155 chars
    - [ ] Alt text for all images
    - [ ] FAQ section with schema
```
**Usage**: Create standardized briefs for consistent content quality.
**Expected output**: Complete content brief document.
**Tip**: Save your best briefs as templates for recurring content types.

---

### Prompt 24: Conclusion & CTA Writer
```
Write a compelling conclusion section for an article about "[KEYWORD]".

Article summary (key points covered):
1. [POINT_1]
2. [POINT_2]
3. [POINT_3]

CTA type: [AFFILIATE_LINK / EMAIL_SIGNUP / RELATED_ARTICLE / PRODUCT_PURCHASE]
CTA target: [URL_OR_DESCRIPTION]

Requirements:
- Maximum 200 words
- Summarize the 3 key takeaways in bold
- Do NOT start with "In conclusion" or "To sum up"
- Include a specific, actionable next step
- Create urgency without being pushy
- End with the CTA naturally integrated into the text
- Include the target keyword one final time

Write 3 variations:
1. **Action-oriented**: Focus on what to do next
2. **Emotional**: Connect with the reader's aspirations
3. **Practical**: Summary + resource recommendation
```
**Usage**: End articles with high-converting conclusions.
**Expected output**: 3 conclusion variations with CTAs.
**Tip**: The action-oriented variation typically performs best for affiliate content.

---

### Prompt 25: E-E-A-T Enhancement Prompt
```
I have an article about "[KEYWORD]". Enhance it with E-E-A-T (Experience, Expertise, Authoritativeness, Trustworthiness) signals.

Current article:
"""
[PASTE_ARTICLE]
"""

Add or suggest additions for:

**Experience signals**:
- First-person accounts ("I've been using X for Y months...")
- Specific results and numbers from personal use
- Photos/screenshots placeholders [ADD PHOTO: description]
- Timestamps ("As of [MONTH] [YEAR]...")

**Expertise signals**:
- Technical details that show deep knowledge
- Industry-specific terminology used correctly
- Mention of credentials or relevant background

**Authoritativeness signals**:
- References to official sources (government sites, academic papers)
- Quotes from industry experts
- Data from recognized research organizations

**Trustworthiness signals**:
- Honest disclaimers and limitations
- Affiliate disclosure
- "Last updated" date
- Author bio section

Provide the enhanced version with all additions clearly marked with [ADDED: E-E-A-T].
```
**Usage**: Boost E-E-A-T signals for YMYL and competitive topics.
**Expected output**: Enhanced article with clearly marked additions.
**Tip**: Google's Helpful Content system specifically looks for these signals.

---

## CATEGORY 3: On-Page SEO Optimization (10 Prompts)

### Prompt 26: H2/H3 Heading Structure Optimizer
```
Analyze and optimize the heading structure of this article:

Current headings:
[PASTE_ALL_H2_AND_H3_HEADINGS]

Target keyword: [KEYWORD]

Optimize for:
1. **Keyword inclusion**: Ensure keyword appears in H1 and at least 2 H2s
2. **Logical flow**: Headings should tell the article's story when read alone
3. **Search intent match**: Headings should match what people search for
4. **Featured snippet optimization**: At least one H2 should match a common question
5. **Parallel structure**: Consistent grammatical structure within the same level
6. **Length**: H2s should be 5-10 words, H3s should be 4-8 words

Provide:
- Original heading → Optimized heading (with explanation)
- Any headings to add or remove
- Suggested FAQ headings for schema markup
```
**Usage**: Fix heading structure after article generation.
**Expected output**: Optimized heading hierarchy with rationale.
**Tip**: Headings are the second most important on-page SEO element after title tags.

---

### Prompt 27: Internal Link Suggestion Engine
```
I have a blog with the following published articles:
[LIST: title, URL, target keyword for each article]

For the article "[CURRENT_ARTICLE_TITLE]" (keyword: [KEYWORD]), suggest internal links:

1. **Outbound internal links** (from this article to others):
   - Which articles to link to (max 5)
   - Which anchor text to use (natural, keyword-rich)
   - Where in the article to place each link (specific section/paragraph)
   - Why this link adds value for the reader

2. **Inbound internal links** (from other articles to this one):
   - Which existing articles should link to this new article
   - Suggested anchor text
   - Which paragraph in the source article to add the link

3. **Missing articles** (content you should create to strengthen the internal link network):
   - Topic suggestions that would bridge gaps between existing articles

Prioritize links that:
- Connect topically related articles (same silo/cluster)
- Pass link equity to money pages
- Help readers naturally progress through related content
```
**Usage**: Build a strong internal link structure automatically.
**Expected output**: Complete internal linking plan with specific placements.
**Tip**: Internal links are one of the most underused SEO tactics.

---

### Prompt 28: Image Alt Text Generator
```
Generate SEO-optimized alt text for the following images in my article about "[KEYWORD]":

Images:
1. [DESCRIBE_IMAGE_1]
2. [DESCRIBE_IMAGE_2]
3. [DESCRIBE_IMAGE_3]
4. [DESCRIBE_IMAGE_4]
5. [DESCRIBE_IMAGE_5]

For each image, provide:
- **Alt text** (max 125 characters): Descriptive, includes keyword where natural
- **Title attribute**: Slightly different from alt text
- **Caption** (optional): Engaging caption for below the image
- **File name suggestion**: keyword-descriptive-name.webp

Rules:
- Do NOT start with "Image of" or "Photo of"
- Include the target keyword in at least 2 alt texts
- Be specific about what's shown (colors, actions, numbers)
- Alt text should make sense when read by a screen reader
```
**Usage**: Optimize image SEO across all articles.
**Expected output**: Complete image optimization plan.
**Tip**: Image search drives 20-30% of traffic for visual topics.

---

### Prompt 29: Schema Markup Generator
```
Generate the appropriate schema markup (JSON-LD) for this content:

Content type: [ARTICLE_TYPE: Article / HowTo / FAQ / Product Review / Comparison]
Title: [TITLE]
Author: [AUTHOR_NAME]
Date published: [DATE]
Date modified: [DATE]
Description: [META_DESCRIPTION]
Image URL: [IMAGE_URL]

Content-specific data:
[PROVIDE RELEVANT DATA — e.g., FAQ Q&As, How-to steps, Review rating, etc.]

Generate:
1. **Primary schema** (Article or specific type)
2. **FAQ schema** (if FAQ section exists)
3. **Breadcrumb schema**
4. **Author schema** (Person)

Output as complete, valid JSON-LD code blocks ready to paste into <head>.
Test validity notes: what to check at schema.org validator.
```
**Usage**: Get rich results in Google search.
**Expected output**: Ready-to-use JSON-LD schema markup.
**Tip**: FAQ schema consistently increases CTR by 20-30%.

---

### Prompt 30: URL Slug Optimizer
```
Generate SEO-optimized URL slugs for these article titles:

Titles:
[LIST_OF_TITLES]

For each, provide:
1. **Recommended slug**: lowercase, hyphens, no stop words
2. **Alternative slug**: shorter variant
3. **Slug to avoid**: common mistake

Rules:
- Maximum 5 words / 60 characters
- Include the primary keyword
- Remove stop words (the, a, an, in, on, of, for, to, and, is, it, how)
- Use hyphens (not underscores)
- No dates in URLs (content should be evergreen)
- No special characters or numbers unless essential

Example:
Title: "10 Best Free SEO Tools for Beginners in 2026"
Good: /best-free-seo-tools-beginners
Avoid: /10-best-free-seo-tools-for-beginners-in-2026
```
**Usage**: Optimize URL structure for new articles.
**Expected output**: Optimized slug options for each title.
**Tip**: Shorter URLs correlate with higher rankings (Backlinko study).

---

### Prompt 31: Content Readability Optimizer
```
Analyze and improve the readability of this article section:

"""
[PASTE_CONTENT]
"""

Target reading level: [GRADE_LEVEL, e.g., Grade 8]

Optimize for:
1. **Sentence length**: Break sentences over 25 words into shorter ones
2. **Paragraph length**: Max 3-4 sentences per paragraph
3. **Active voice**: Convert passive constructions to active
4. **Transition words**: Add where flow is choppy (however, additionally, in contrast, etc.)
5. **Jargon**: Simplify or briefly explain technical terms
6. **Scanability**: Add bold/italic emphasis to key phrases
7. **White space**: Suggest where to add line breaks or bullet lists

Provide:
- The improved version
- A before/after readability score estimate
- Top 3 changes that had the most impact
```
**Usage**: Make AI-generated content more readable and engaging.
**Expected output**: Improved content with readability analysis.
**Tip**: Aim for Flesch Reading Ease of 60-70 for general web content.

---

### Prompt 32: Anchor Text Optimizer
```
I need optimized anchor text for these internal and external links in my article about "[KEYWORD]":

Links to optimize:
1. [TARGET_URL_1] — currently: "[CURRENT_ANCHOR_1]"
2. [TARGET_URL_2] — currently: "[CURRENT_ANCHOR_2]"
3. [TARGET_URL_3] — currently: "[CURRENT_ANCHOR_3]"

For each link, provide 3 anchor text options:
1. **Exact match**: Contains the target page's keyword
2. **Partial match**: Related phrase that includes part of the keyword
3. **Natural/contextual**: Reads naturally in the sentence

Rules:
- Never use "click here" or "read more"
- Vary anchor text across the article (don't repeat the same anchor)
- For affiliate links: use branded or descriptive anchors, not "buy now"
- Keep anchor text 2-6 words
- The anchor should give the reader a clear idea of what they'll find

Also suggest the surrounding sentence context for each anchor option.
```
**Usage**: Optimize anchor text distribution across your site.
**Expected output**: Anchor text options with contextual sentences.
**Tip**: Diverse anchor text profiles look more natural to Google.

---

### Prompt 33: Featured Snippet Optimizer
```
I want to win the featured snippet for "[KEYWORD]". The current featured snippet shows:

Type: [PARAGRAPH / LIST / TABLE / VIDEO]
Content: [PASTE_CURRENT_SNIPPET_CONTENT]

My article's current answer to this query:
"""
[PASTE_MY_RELEVANT_SECTION]
"""

Rewrite my section to beat the current snippet:

For **paragraph snippets** (40-60 words):
- Start with a direct, concise answer to the query
- Follow Google's "is" definition pattern: "[KEYWORD] is..."
- Include the exact keyword in the first sentence
- Add one supporting detail

For **list snippets** (5-8 items):
- Create a clear numbered or bulleted list
- Each item: 1-2 sentences, starts with a bold keyword
- Use H2 or H3 for the question heading

For **table snippets** (3-5 rows):
- Create a comparison or data table
- Include clear column headers
- Keep cells concise (2-5 words)

Provide the optimized version in the correct format.
```
**Usage**: Win featured snippets (position 0) in Google.
**Expected output**: Snippet-optimized content block.
**Tip**: Pages in positions 1-5 have the highest chance of winning featured snippets.

---

### Prompt 34: Content Cannibalisation Detector
```
I have multiple articles that might be competing for the same keywords. Analyze these articles and identify cannibalization:

Articles:
1. Title: [TITLE_1], URL: [URL_1], Target KW: [KW_1]
2. Title: [TITLE_2], URL: [URL_2], Target KW: [KW_2]
3. Title: [TITLE_3], URL: [URL_3], Target KW: [KW_3]
[... add more as needed]

For each potential conflict:
1. **Conflicting articles**: Which 2+ articles compete for the same query
2. **Overlap keyword**: The keyword they both target
3. **Recommended action**:
   - Merge: Combine into one comprehensive article
   - Differentiate: Adjust keywords/angles to target different intents
   - Redirect: 301 redirect the weaker article
   - Canonical: Add canonical tag to preferred version
4. **Implementation steps**: Specific changes to make

Also suggest how to restructure the remaining articles' internal linking after fixes.
```
**Usage**: Fix keyword cannibalization issues.
**Expected output**: Cannibalization audit with actionable fixes.
**Tip**: Cannibalization is one of the top reasons good content fails to rank.

---

### Prompt 35: Page Speed Content Optimization
```
Review this article HTML/content for elements that may slow down page speed:

"""
[PASTE_ARTICLE_HTML_OR_MARKDOWN]
"""

Identify and suggest fixes for:
1. **Image optimization**:
   - Images without width/height attributes (causes layout shift)
   - Images that should be lazy-loaded
   - Images that could be WebP format
   - Oversized images (suggest dimensions)

2. **Embed optimization**:
   - YouTube embeds → suggest lite-youtube-embed
   - Social media embeds → suggest screenshots instead
   - Third-party widgets → suggest deferring

3. **Content structure**:
   - Above-the-fold content that needs prioritization
   - Below-the-fold content that can be lazy-loaded
   - Tables that need responsive wrapper

4. **HTML cleanup**:
   - Unnecessary inline styles
   - Empty elements or redundant tags
   - Large HTML blocks that can be simplified

Provide the optimized version with comments explaining each change.
```
**Usage**: Optimize content for Core Web Vitals.
**Expected output**: Optimized HTML with performance annotations.
**Tip**: Page speed is a confirmed ranking factor, especially on mobile.

---

## CATEGORY 4: Content Enhancement (10 Prompts)

### Prompt 36: Affiliate Link Placement Strategist
```
I have an article about "[KEYWORD]" and need to naturally insert affiliate links.

Article structure:
[PASTE_H2/H3_HEADINGS_AND_BRIEF_DESCRIPTION_OF_EACH_SECTION]

Available affiliate links:
1. [PRODUCT_1] — [AFFILIATE_URL_1] — context: [WHEN_TO_USE_1]
2. [PRODUCT_2] — [AFFILIATE_URL_2] — context: [WHEN_TO_USE_2]
3. [PRODUCT_3] — [AFFILIATE_URL_3] — context: [WHEN_TO_USE_3]

Rules:
- Maximum [MAX_LINKS] affiliate links per article
- Minimum 300 words between affiliate links
- First link should appear after the reader has received genuine value (not in the intro)
- Use natural anchor text (product name or descriptive phrase, not "click here")
- Include a disclosure at the top of the article

For each link placement, provide:
1. Which section to place it in
2. The exact sentence with the link embedded
3. Why this placement feels natural to the reader
4. The anchor text to use
```
**Usage**: Monetize content without being spammy.
**Expected output**: Specific link placement plan with context sentences.
**Tip**: Links placed after valuable content convert 3-5x better than early links.

---

### Prompt 37: Social Proof Enhancer
```
I need to add social proof elements to this article about "[KEYWORD]":

"""
[PASTE_ARTICLE_OR_SUMMARY]
"""

Generate and suggest placements for:
1. **Testimonial-style quotes** (3): Realistic quotes from a hypothetical user that illustrate key benefits
   - Mark as [PLACEHOLDER — Replace with real testimonial]
2. **Data points** (5): Statistics that support the article's claims
   - Include source suggestions (where to find the real data)
3. **Case study snippets** (2): Brief before/after scenarios (100 words each)
   - Mark as [PLACEHOLDER — Replace with real case study]
4. **Trust badges text**: Suggest trust elements like "Used by X people" or "Rated X/5"
   - Mark as [VERIFY DATA]
5. **Expert quote suggestions**: What type of expert to quote and what they might say
   - Include instructions for finding real quotes

For each element, specify exactly where in the article it should go.
```
**Usage**: Increase article credibility and conversion rates.
**Expected output**: Social proof elements with placement instructions.
**Tip**: ALWAYS replace placeholders with real data before publishing.

---

### Prompt 38: Call-to-Action Generator
```
Generate 10 different CTAs for an article about "[KEYWORD]" that promotes [PRODUCT/ACTION].

CTA types needed:
1. **Inline text CTA** (within a paragraph): 1-2 sentences
2. **Button CTA**: Short text for a button (max 5 words) + supporting text
3. **Box/banner CTA**: Highlighted section with offer details (50 words)
4. **Exit-intent CTA**: What to show when reader is about to leave
5. **End-of-article CTA**: Closing call to action (100 words)
6. **Soft CTA**: Gentle nudge without being salesy
7. **Urgency CTA**: Time-sensitive or scarcity-based
8. **Value CTA**: Focused on what the reader gets
9. **Social proof CTA**: References others who took action
10. **Question CTA**: Engages the reader with a rhetorical question

For each, provide:
- The CTA text
- Best placement in the article (which section)
- Expected conversion impact (low/medium/high)
```
**Usage**: Test different CTA styles for maximum conversions.
**Expected output**: 10 CTA variations with placement suggestions.
**Tip**: A/B test button text — small changes can improve conversions 20-50%.

---

### Prompt 39: Content Localization Adapter
```
Adapt this article for a different market/locale:

Original article (written for [ORIGINAL_MARKET]):
"""
[PASTE_ARTICLE]
"""

Target market: [TARGET_MARKET]
Target language: [TARGET_LANGUAGE] (or same language, different region)

Adapt:
1. **Currency**: Convert all prices to local currency with current rates
2. **Cultural references**: Replace with locally relevant examples
3. **Products/services**: Substitute with locally available alternatives
4. **Legal/tax info**: Flag any claims that may differ by jurisdiction [VERIFY FOR LOCAL LAWS]
5. **Tone/formality**: Adjust for cultural communication norms
6. **Measurements**: Convert units if needed
7. **Season references**: Adjust for hemisphere differences
8. **Local competitors**: Reference local market leaders
9. **Payment methods**: Mention locally popular payment options
10. **SEO**: Adjust keywords for local search patterns

Mark all changes with [LOCALIZED] and flag items needing verification with [VERIFY].
```
**Usage**: Repurpose content for different markets.
**Expected output**: Localized version with change annotations.
**Tip**: Localized content outperforms translated content by 2-3x in engagement.

---

### Prompt 40: Article Update Prompt (Annual Refresh)
```
This article was published on [ORIGINAL_DATE] and needs an annual update for [CURRENT_YEAR].

Article:
"""
[PASTE_ARTICLE]
"""

Update the following:
1. **Year references**: Change [OLD_YEAR] to [CURRENT_YEAR] throughout
2. **Statistics**: Flag all numbers/stats that need current data [UPDATE NEEDED: original stat]
3. **Pricing**: Flag all prices that may have changed [VERIFY PRICE]
4. **Products/tools**: Note any that have been discontinued, rebranded, or had major updates
5. **Links**: Flag any links that might be broken [CHECK LINK]
6. **New developments**: Suggest 1-2 new sections to add based on recent developments in [TOPIC]
7. **Remove outdated info**: Flag content that is no longer accurate
8. **Competitor check**: Note if any new major competitors have emerged

Provide:
- The updated article with all changes marked in [BRACKETS]
- A changelog summary of all modifications
- Suggested "Last updated: [DATE]" text
```
**Usage**: Keep content fresh and ranking.
**Expected output**: Updated article with change log.
**Tip**: Google rewards freshness — updating articles often recovers lost rankings.

---

### Prompt 41: Engagement Hook Injector
```
This article is informative but dry. Add engagement elements throughout:

"""
[PASTE_ARTICLE]
"""

Add these elements at appropriate points:
1. **Analogies** (3): Complex concepts explained through everyday comparisons
2. **Mini-stories** (2): 2-3 sentence anecdotes that illustrate a point
3. **Rhetorical questions** (4): Questions that make the reader think
4. **Surprising facts** (3): Counterintuitive information that grabs attention
5. **Direct address** (5+): "you" statements that connect with the reader
6. **Sensory language** (3): Descriptions that paint a picture
7. **Humor** (1-2): Lighthearted comments where appropriate
8. **Controversy/opinion** (1): A strong, defensible opinion

Rules:
- Don't change the factual content
- Don't increase word count by more than 15%
- Mark all additions with [ADDED FOR ENGAGEMENT]
- Maintain the article's original tone
```
**Usage**: Make informational content more engaging.
**Expected output**: Enhanced article with engagement elements marked.
**Tip**: Articles with stories and analogies have 40% lower bounce rates.

---

### Prompt 42: Table & Visual Data Creator
```
Create data-rich visual elements for an article about "[KEYWORD]":

Article context:
[BRIEF_DESCRIPTION_OF_ARTICLE_CONTENT]

Generate:

1. **Comparison table** (HTML/Markdown):
   - Compare 3-5 items relevant to the topic
   - Include 5-7 comparison criteria
   - Add emoji ratings or star ratings
   - Highlight the "best pick"

2. **Pros/Cons table**:
   - Format as a two-column table with green/red indicators
   - 5 pros, 4 cons (show honesty)

3. **Step-by-step process table**:
   - Step number | Action | Time needed | Tools required
   - 5-8 steps

4. **Quick facts box** (markdown blockquote):
   - 5-7 key facts about the topic
   - Each fact in one line with emoji bullet

5. **Decision flowchart** (text-based):
   - If [condition] → [recommendation]
   - Help reader choose the right option

6. **Cost breakdown table**:
   - Category | Low end | Mid range | High end
   - Total row

Provide all elements in Markdown format ready to copy-paste.
```
**Usage**: Add visual richness to text-heavy articles.
**Expected output**: 6 visual data elements in Markdown.
**Tip**: Articles with tables are 2x more likely to win featured snippets.

---

### Prompt 43: Content Upgrade Creator
```
I want to create a content upgrade (lead magnet) for this article about "[KEYWORD]":

Article summary:
[BRIEF_SUMMARY]

Target audience: [AUDIENCE]

Suggest and create outlines for 3 content upgrade options:

1. **Checklist** (1-2 pages):
   - Turn the article's advice into an actionable checklist
   - Include checkboxes, categories, and notes fields
   - Provide the complete checklist content

2. **Cheat sheet** (1 page):
   - Condense the most important information onto one page
   - Include tables, formulas, or reference data
   - Provide the complete cheat sheet content

3. **Template/worksheet** (2-3 pages):
   - Create a fill-in-the-blank template related to the topic
   - Include example entries
   - Provide the complete template content

For each:
- Complete content (ready to design)
- CTA text to use in the article
- Where in the article to place the CTA
- Email subject line for the delivery email
```
**Usage**: Build your email list with article-specific lead magnets.
**Expected output**: 3 complete content upgrade outlines.
**Tip**: Content upgrades convert 5-10x better than generic "subscribe" CTAs.

---

### Prompt 44: Storytelling Framework Injector
```
Transform this informational section into a narrative-driven section using storytelling:

Original section:
"""
[PASTE_SECTION]
"""

Apply the following storytelling framework:

**Framework: Problem-Agitation-Solution (PAS)**
1. **Problem**: Describe the reader's current painful situation (2-3 sentences)
2. **Agitation**: Make the problem feel urgent and real (2-3 sentences)
3. **Solution**: Present the answer with your content (main body)

Also provide alternative versions using:
- **Before/After/Bridge**: Show the transformation
- **AIDA**: Attention, Interest, Desire, Action

Requirements:
- Keep all factual information intact
- Use "you" language
- Include specific details (numbers, names, scenarios)
- The story should feel authentic, not manipulative
- Maximum 20% longer than the original
```
**Usage**: Make dry content compelling through storytelling.
**Expected output**: 3 story-driven versions of the same content.
**Tip**: PAS works best for commercial content; Before/After works best for tutorials.

---

### Prompt 45: Tone & Voice Adapter
```
Rewrite this content in a different tone/voice:

Original content:
"""
[PASTE_CONTENT]
"""

Current tone: [FORMAL/CASUAL/ACADEMIC/GENERIC]
Target tone: [CHOOSE ONE]:

a) **Casual expert**: Like a knowledgeable friend explaining over coffee
b) **Authoritative professional**: Corporate but not boring
c) **Enthusiastic blogger**: Energetic, lots of personality
d) **Minimalist**: Short sentences. Clear. No fluff.
e) **Empathetic guide**: Understanding, supportive, encouraging
f) **Data-driven analyst**: Numbers-focused, logical, evidence-based

Requirements:
- Preserve all factual information
- Adjust vocabulary, sentence length, and structure
- Change analogies and examples to match the new tone
- Same word count (±10%)
- Provide the full rewritten version
```
**Usage**: Adapt content for different platforms or audiences.
**Expected output**: Complete rewrite in the target tone.
**Tip**: Match your tone to where your audience spends time online.

---

## CATEGORY 5: Technical & WordPress SEO (5 Prompts)

### Prompt 46: WordPress Gutenberg Block Template
```
Convert this article content into WordPress Gutenberg block markup:

Article content (Markdown):
"""
[PASTE_MARKDOWN_CONTENT]
"""

Convert to WordPress block format including:
1. **Heading blocks** (wp:heading) with proper level attributes
2. **Paragraph blocks** (wp:paragraph)
3. **List blocks** (wp:list) for bullet/numbered lists
4. **Table blocks** (wp:table) for any tables
5. **Quote blocks** (wp:quote) for callouts/tips
6. **Separator blocks** (wp:separator) between major sections
7. **Image blocks** (wp:image) with alt text placeholders
8. **Button blocks** (wp:buttons) for CTAs
9. **Group blocks** for styled sections (tips, warnings)

Add appropriate CSS classes:
- "has-background" for highlighted sections
- "is-style-info" for tip boxes
- "is-style-warning" for caution boxes

Output the complete HTML with WordPress block comments.
```
**Usage**: Prepare articles for WordPress paste-ready format.
**Expected output**: Complete Gutenberg block HTML.
**Tip**: This format preserves styling when pasted into WordPress editor.

---

### Prompt 47: WordPress REST API Article Payload Generator
```
Generate a WordPress REST API payload to create/update a post:

Article details:
- Title: [TITLE]
- Content: [PASTE_HTML_CONTENT]
- Slug: [URL_SLUG]
- Category: [CATEGORY_NAME]
- Tags: [TAG_1, TAG_2, TAG_3]
- Featured image ID: [MEDIA_ID]
- Meta description: [META_DESCRIPTION]
- Focus keyword: [KEYWORD]
- Status: [draft/publish]

Generate:
1. **Create post** cURL command with full payload
2. **Python requests** code to create the post
3. **Update post** variant (using post ID)
4. **Bulk create** variant (for multiple articles)

Include:
- Basic authentication header (username + application password)
- All Rank Math / Yoast SEO meta fields
- Custom fields if needed
- Error handling code
- Response validation

```python
# Generated WordPress API code here
```
```
**Usage**: Automate WordPress publishing via API.
**Expected output**: Ready-to-run API code.
**Tip**: Use Application Passwords (not regular passwords) for WordPress API auth.

---

### Prompt 48: Robots.txt & Sitemap Optimizer
```
Analyze my site structure and generate optimized robots.txt and sitemap configuration:

Site: [SITE_URL]
CMS: [WordPress/Next.js/etc.]
Content types:
- Blog posts: [NUMBER] (URL pattern: /blog/[slug]/)
- Pages: [NUMBER] (URL pattern: /[slug]/)
- Categories: [NUMBER] (URL pattern: /category/[slug]/)
- Tags: [NUMBER]
- Author pages: [NUMBER]
- Media attachments: [NUMBER]

Current issues:
[DESCRIBE_ANY_KNOWN_ISSUES]

Generate:
1. **robots.txt**:
   - Allow important content
   - Block thin/duplicate content
   - Block admin, search results, tag pages if thin
   - Point to sitemap

2. **XML sitemap strategy**:
   - Which content types to include/exclude
   - Priority values for each type
   - Change frequency settings
   - Lastmod strategy

3. **Meta robots suggestions**:
   - Which pages should be noindex, nofollow
   - Canonical URL strategy for similar pages
```
**Usage**: Technical SEO foundation setup.
**Expected output**: Complete robots.txt + sitemap strategy.
**Tip**: Blocking thin content (tags, archives) focuses crawl budget on important pages.

---

### Prompt 49: Core Web Vitals Content Checklist
```
Audit this article for Core Web Vitals impact:

[PASTE_ARTICLE_HTML_OR_URL]

Check and provide recommendations for:

**Largest Contentful Paint (LCP)**:
- [ ] Hero image optimized (WebP, proper dimensions, preloaded)
- [ ] No render-blocking CSS for above-the-fold content
- [ ] Font loading strategy (font-display: swap)
- Suggested fixes:

**First Input Delay (FID) / Interaction to Next Paint (INP)**:
- [ ] No heavy JavaScript in the article
- [ ] Third-party scripts deferred
- [ ] No complex event listeners
- Suggested fixes:

**Cumulative Layout Shift (CLS)**:
- [ ] All images have width/height attributes
- [ ] Ad slots have reserved space
- [ ] No dynamically injected content above the fold
- [ ] Web fonts don't cause layout shift
- Suggested fixes:

Provide:
1. Priority-ranked fix list
2. Estimated impact of each fix
3. Implementation code/instructions for each fix
```
**Usage**: Ensure articles don't harm Core Web Vitals.
**Expected output**: CWV audit with actionable fixes.
**Tip**: CWV is a confirmed ranking factor — sites in "good" range get a small ranking boost.

---

### Prompt 50: Multilingual SEO Adapter
```
I want to create a [TARGET_LANGUAGE] version of this article for international SEO:

Original article ([SOURCE_LANGUAGE]):
"""
[PASTE_ARTICLE]
"""

Target market: [COUNTRY/REGION]

Provide:
1. **Translated + localized version**:
   - Not just translation — adapt examples, references, currency
   - Local keyword research: suggest 3 target keyword alternatives in [TARGET_LANGUAGE]
   - Adjust H2/H3 for local search patterns

2. **Hreflang tags**:
   - For the original page
   - For the new language version
   - x-default tag

3. **URL strategy recommendation**:
   - Subdirectory (/es/article) vs subdomain (es.site.com) vs ccTLD
   - Recommended approach for this site

4. **Local SEO adjustments**:
   - Local link building opportunities
   - Local directory submissions
   - Region-specific schema markup

5. **Content differences**:
   - Topics that need different emphasis for this market
   - Topics to remove (not relevant locally)
   - Topics to add (locally important)
```
**Usage**: Expand content to international markets.
**Expected output**: Localized article + technical SEO implementation guide.
**Tip**: Proper hreflang implementation prevents duplicate content issues across languages.

---

## BONUS: Quick-Reference Prompt Snippets

### Snippet A: Quick Title Formula
```
Write 3 titles for "[KEYWORD]" using these formulas:
1. [Number] + [Keyword] + [Promise] + ([Year])
2. How to [Keyword] + [Outcome] + [Timeframe]
3. [Keyword]: [Complete/Ultimate/Definitive] Guide for [Audience]
Max 60 chars each. Show character count.
```

### Snippet B: Quick Meta Description
```
Write a meta description for "[TITLE]" targeting "[KEYWORD]".
Max 155 chars. Include keyword in first 70 chars. End with action verb. Show char count.
```

### Snippet C: Quick Outline
```
Give me H2/H3 headings for a [WORD_COUNT]-word article about "[KEYWORD]" targeting [AUDIENCE]. Include target word count per section.
```

### Snippet D: Quick FAQ
```
Write 5 FAQ questions and 80-word answers about "[KEYWORD]". Start each answer with a direct response. Format for FAQ schema.
```

### Snippet E: Quick Internal Link Check
```
I'm writing about "[KEYWORD]". My site has these articles: [LIST]. Which 3 should I link to, and with what anchor text?
```

---

## How to Use This Pack Effectively

1. **Start with research**: Use Category 1 prompts to find your keywords and plan content
2. **Generate content**: Use Category 2 prompts to create your article draft
3. **Optimize on-page**: Apply Category 3 prompts to polish SEO elements
4. **Enhance quality**: Use Category 4 prompts to add engagement and depth
5. **Publish**: Use Category 5 prompts for technical implementation

**Pro tips**:
- Customize the [PLACEHOLDER] variables for your specific niche
- Chain prompts together: Research → Outline → Draft → Optimize → Publish
- Save your best-performing prompt configurations as presets
- Always add personal experience before publishing — AI-only content won't rank long-term

---

*50 prompts. Zero fluff. Built from a production content pipeline that generates, publishes, and ranks articles automatically.*
