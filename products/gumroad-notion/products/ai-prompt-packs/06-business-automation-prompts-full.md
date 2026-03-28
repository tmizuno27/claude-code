# AI Business Automation Mega Prompt Pack — Full Prompts

> 52 prompts organized by business function. Each prompt includes variables [IN_BRACKETS], context instructions, and expected output format.
> Compatible with ChatGPT, Claude, Gemini, Copilot, or any LLM.

---

## CATEGORY 1: EMAIL & COMMUNICATION (10 Prompts)

### Prompt 1: Customer Inquiry Auto-Responder
```
You are a customer support specialist for [BUSINESS_NAME], a [BUSINESS_TYPE].

A customer sent this inquiry:
"""
[PASTE_CUSTOMER_MESSAGE]
"""

Write a professional, warm response that:
1. Acknowledges their specific concern
2. Provides a clear answer or next steps
3. Offers additional help
4. Keeps tone [TONE: friendly/formal/casual]
5. Stays under 150 words

If you cannot fully answer, explain what you need from them to resolve it.
```

### Prompt 2: Follow-Up Email Sequence Generator
```
Create a 5-email follow-up sequence for [CONTEXT: cold lead / post-demo / post-purchase / abandoned cart].

Business: [BUSINESS_NAME]
Product/Service: [PRODUCT]
Target audience: [AUDIENCE]
Goal: [GOAL: close sale / get feedback / upsell / re-engage]

For each email provide:
- Subject line (A/B variants)
- Send timing (days after trigger)
- Body (under 200 words)
- CTA (one clear action)
- Personalization variables

Tone: [TONE]. Make each email progressively more compelling without being pushy.
```

### Prompt 3: Meeting Summary & Action Items Extractor
```
Here are my meeting notes (raw/messy):
"""
[PASTE_MEETING_NOTES]
"""

Extract and format:
1. **Meeting Summary** (3-5 bullet points, max 50 words total)
2. **Key Decisions** (numbered list)
3. **Action Items** (table format: Action | Owner | Deadline | Priority)
4. **Open Questions** (unresolved items needing follow-up)
5. **Next Meeting Agenda** (suggested topics based on open items)

If owner or deadline is unclear, mark as "TBD" and flag it.
```

### Prompt 4: Cold Outreach Personalization
```
I want to reach out to [PROSPECT_NAME] at [COMPANY].

What I know about them:
- Role: [ROLE]
- Company: [COMPANY_DESCRIPTION]
- Recent news/activity: [RECENT_INFO]
- Mutual connections: [CONNECTIONS_IF_ANY]

My offer: [YOUR_PRODUCT_SERVICE]
Value prop: [HOW_IT_HELPS_THEM]

Write 3 versions of a cold email (each under 100 words):
1. Direct approach (lead with value)
2. Curiosity approach (question-based opener)
3. Social proof approach (reference similar companies)

Include subject line for each. No generic phrases like "I hope this finds you well."
```

### Prompt 5: Support Ticket Categorizer & Draft Responder
```
Here are today's support tickets:
"""
[PASTE_TICKETS_OR_LIST]
"""

For each ticket:
1. Assign category: [Bug | Feature Request | Billing | How-To | Account | Other]
2. Assign priority: [P1-Critical | P2-High | P3-Medium | P4-Low]
3. Draft a response (under 100 words)
4. Flag if escalation is needed (and why)
5. Suggest knowledge base article to create if this is a recurring issue

Output as a table for easy copy-paste into our ticketing system.
```

### Prompt 6: Newsletter Content Generator
```
Create a newsletter for [BUSINESS_NAME] targeting [AUDIENCE].

Theme: [THEME_OR_TOPIC]
Frequency: [WEEKLY/BIWEEKLY/MONTHLY]
Tone: [TONE]

Structure:
1. Hook headline (curiosity-driven, under 10 words)
2. Opening paragraph (personal, relatable, under 50 words)
3. Main content section (3 key insights/tips with subheadings)
4. Quick win (one actionable tip readers can use today)
5. CTA (what to do next)
6. P.S. line (teaser for next issue or bonus)

Total length: 400-600 words. Write like a smart friend, not a corporation.
```

### Prompt 7: Client Onboarding Email Sequence
```
Create a 7-day onboarding email sequence for new clients of [BUSINESS_NAME].

Service/Product: [PRODUCT]
Onboarding goal: [GOAL: activate account / complete setup / first success]
Key milestones: [MILESTONE_1], [MILESTONE_2], [MILESTONE_3]

For each email:
- Day number and trigger
- Subject line
- Body (under 150 words)
- One clear action for the client
- Link placeholder for relevant resource

Tone: helpful and encouraging. Celebrate small wins. Address common confusion points proactively.
```

### Prompt 8: Feedback Request Composer
```
Write a feedback request for [CONTEXT: post-project / post-purchase / quarterly review].

Client/Customer: [NAME]
What they bought/used: [PRODUCT_SERVICE]
Relationship length: [DURATION]

Create:
1. Email requesting feedback (warm, specific, under 150 words)
2. 5 targeted questions (not generic "how was your experience")
3. Option for a testimonial quote (with permission language)
4. Follow-up if no response after 5 days

Make the ask feel like a conversation, not a survey. Reference specific work we did together.
```

### Prompt 9: Partnership Proposal Writer
```
Write a partnership proposal for:

My business: [YOUR_BUSINESS] — [WHAT_YOU_DO]
Target partner: [PARTNER_COMPANY] — [WHAT_THEY_DO]
Partnership type: [TYPE: affiliate / co-marketing / integration / referral / white-label]
Mutual benefit: [WHY_IT_WORKS_FOR_BOTH]

Structure:
1. Executive summary (3 sentences)
2. The opportunity (market data, audience overlap)
3. Proposed partnership structure
4. Revenue/benefit split
5. Timeline and next steps
6. Quick FAQ (3 anticipated objections with answers)

Tone: professional but not stiff. Under 500 words total.
```

### Prompt 10: Complaint Resolution Drafter
```
A customer has complained:
"""
[PASTE_COMPLAINT]
"""

Context: [ANY_BACKGROUND_INFO]
Our policy: [RELEVANT_POLICY]
My authority level: [WHAT_I_CAN_OFFER: refund / discount / replacement / escalation]

Write a response that:
1. Acknowledges the frustration without being defensive
2. Takes responsibility where appropriate
3. Offers a specific resolution
4. Explains what we'll do to prevent recurrence
5. Ends on a positive note

Under 200 words. The goal is to turn this person into a loyal customer.
```

---

## CATEGORY 2: CONTENT & MARKETING (12 Prompts)

### Prompt 11: Blog Post Outline from Keyword
```
Create a comprehensive blog post outline for the keyword: "[KEYWORD]"

Target audience: [AUDIENCE]
Search intent: [INFORMATIONAL / COMMERCIAL / TRANSACTIONAL]
Competitor URLs to beat: [URL_1], [URL_2] (optional)
Word count target: [1500 / 2000 / 3000]

Provide:
1. SEO-optimized title (with keyword near the front)
2. Meta description (155 characters)
3. H2/H3 heading structure (with target word count per section)
4. Key points to cover under each heading
5. Internal linking opportunities
6. CTA suggestion
7. Featured snippet opportunity (if any — write the snippet)
```

### Prompt 12: 30-Day Social Media Content Calendar
```
Create a 30-day content calendar for [PLATFORM(S)].

Brand: [BRAND_NAME]
Niche: [NICHE]
Target audience: [AUDIENCE]
Content pillars: [PILLAR_1], [PILLAR_2], [PILLAR_3]
Posting frequency: [X posts per day/week]

For each post:
- Day and time
- Content type (carousel, reel, thread, single image, story)
- Topic/angle
- Hook (first line)
- CTA
- Hashtags (5-10)

Mix: 40% educational, 25% entertaining, 20% promotional, 15% engagement.
Include 2 viral-bait posts and 2 controversial takes (within brand voice).
```

### Prompt 13: Product Description Optimizer
```
Optimize this product description for conversions:
"""
[PASTE_CURRENT_DESCRIPTION]
"""

Product: [PRODUCT_NAME]
Price: [PRICE]
Target buyer: [BUYER_PERSONA]
Platform: [AMAZON / SHOPIFY / GUMROAD / ETSY]

Rewrite with:
1. Benefit-first headline (not feature-first)
2. Problem → Agitation → Solution structure
3. 5 bullet points (benefit + feature format)
4. Social proof placeholder
5. Urgency element (if appropriate)
6. SEO keywords naturally integrated: [KEYWORD_1], [KEYWORD_2]

A/B variant: Write two versions — one emotional, one data-driven.
```

### Prompt 14: SEO Meta Title & Description Generator
```
Generate SEO meta titles and descriptions for these pages:

[LIST_PAGES_WITH_URLS_OR_TOPICS]

For each page:
- Primary keyword: [KEYWORD]
- Page type: [blog / product / landing / category]

Provide:
1. Meta title (under 60 characters, keyword near front)
2. Meta description (under 155 characters, includes CTA)
3. OG title (can be slightly different for social)
4. OG description

Create 2 variants for each (for A/B testing). Include power words: free, proven, guide, best, how to, etc.
```

### Prompt 15: Ad Copy A/B Test Variants
```
Create ad copy variants for [PLATFORM: Google Ads / Facebook / Instagram / LinkedIn].

Product/Service: [PRODUCT]
Target audience: [AUDIENCE]
Campaign goal: [AWARENESS / TRAFFIC / CONVERSIONS]
Budget level: [LOW / MEDIUM / HIGH]
Competitor advantage: [WHAT_MAKES_US_DIFFERENT]

Generate 5 variants:
1. Pain point focus
2. Benefit focus
3. Social proof focus
4. Urgency/scarcity focus
5. Curiosity/question focus

For each: headline (30 chars), description (90 chars), CTA button text.
Include targeting suggestions for each variant.
```

### Prompt 16: Landing Page Copy Framework
```
Write landing page copy for [PRODUCT/SERVICE].

Target: [AUDIENCE]
Price: [PRICE]
Main benefit: [BENEFIT]
Key objection: [OBJECTION]

Sections:
1. Hero: Headline + subheadline + CTA (above the fold)
2. Problem section (3 pain points)
3. Solution section (how we solve it)
4. Features → Benefits (5 items)
5. Social proof (testimonial framework + stats)
6. FAQ (5 questions addressing objections)
7. Final CTA with urgency

Write conversationally. No jargon. Every sentence should make them want to read the next one.
```

### Prompt 17: Case Study Writer from Raw Notes
```
Turn these raw project notes into a polished case study:
"""
[PASTE_RAW_NOTES]
"""

Client: [CLIENT_NAME_OR_ANONYMOUS]
Industry: [INDUSTRY]
Our service: [SERVICE]

Format:
1. Headline (result-driven: "How [Client] achieved [Result] in [Timeframe]")
2. The Challenge (what they struggled with)
3. The Solution (what we did — be specific)
4. The Results (numbers, metrics, before/after)
5. Client quote (write a realistic one they can approve/edit)
6. Key Takeaway (what others can learn)

Under 600 words. Focus on results, not process.
```

### Prompt 18: Testimonial Request & Formatter
```
I need to request testimonials from these clients:
[CLIENT_1]: [PROJECT_DETAILS]
[CLIENT_2]: [PROJECT_DETAILS]

For each:
1. Personalized request email (reference specific work, under 100 words)
2. 3 guided questions to help them write (specific, not generic)
3. Draft a testimonial they can edit/approve (based on project details)
4. Format for: website card, social media post, case study quote

Make the request feel effortless for them — "reply with one sentence" energy.
```

### Prompt 19: Competitor Analysis Summarizer
```
Analyze these competitors for [MY_BUSINESS]:

Competitors:
[COMPETITOR_1_URL]
[COMPETITOR_2_URL]
[COMPETITOR_3_URL]

Analyze (based on their public website/content):
1. Positioning & messaging (what they promise)
2. Pricing strategy
3. Content strategy (blog, social, email)
4. Strengths to learn from
5. Weaknesses to exploit
6. Gaps in the market they're missing

Output as a comparison matrix + strategic recommendations for differentiation.
```

### Prompt 20: Content Repurposing (Blog to Social to Email)
```
Repurpose this blog post into multiple formats:
"""
[PASTE_BLOG_POST_OR_URL]
"""

Create:
1. Twitter/X thread (10 tweets, hook + value + CTA)
2. LinkedIn post (professional angle, under 300 words)
3. Instagram carousel (10 slides, text for each)
4. Email newsletter version (400 words, personal tone)
5. YouTube video script outline (5-7 minutes)
6. Reddit post (value-first, no self-promotion feel)

Each format should feel native to the platform, not like a copy-paste job.
```

### Prompt 21: Hashtag Research & Strategy
```
Research and create a hashtag strategy for [BRAND] on [PLATFORM].

Niche: [NICHE]
Target audience: [AUDIENCE]
Top 3 content topics: [TOPIC_1], [TOPIC_2], [TOPIC_3]

Provide:
1. 10 high-volume hashtags (>100K posts) for reach
2. 10 medium-volume hashtags (10K-100K) for engagement
3. 10 niche hashtags (<10K) for targeted audience
4. 5 branded hashtags to create
5. Hashtag sets for each content pillar (copy-paste ready)
6. Hashtags to AVOID (banned, spammy, irrelevant)
```

### Prompt 22: Brand Voice Consistency Checker
```
Here is our brand voice guide:
"""
[PASTE_BRAND_VOICE_GUIDELINES_OR_DESCRIBE]
"""

Review this content for brand voice consistency:
"""
[PASTE_CONTENT_TO_REVIEW]
"""

Check for:
1. Tone alignment (formal/casual/playful match?)
2. Vocabulary (any off-brand words?)
3. Sentence structure (matches our style?)
4. Values alignment (does it reflect our brand values?)
5. Consistency score (1-10)

Provide specific fixes with before/after examples. Flag any lines that feel "off-brand."
```

---

## CATEGORY 3: OPERATIONS & FINANCE (10 Prompts)

### Prompt 23: Invoice Data Extractor
```
Extract structured data from this invoice:
"""
[PASTE_INVOICE_TEXT_OR_DESCRIBE]
"""

Output as JSON:
{
  "vendor": "",
  "invoice_number": "",
  "date": "",
  "due_date": "",
  "line_items": [{"description": "", "quantity": 0, "unit_price": 0, "total": 0}],
  "subtotal": 0,
  "tax": 0,
  "total": 0,
  "payment_terms": "",
  "notes": ""
}

Flag any missing or ambiguous fields. Suggest expense category for each line item.
```

### Prompt 24: Expense Categorizer
```
Categorize these expenses into accounting categories:
"""
[PASTE_EXPENSE_LIST_OR_BANK_STATEMENT]
"""

Categories: [CUSTOMIZE_OR_USE_DEFAULTS: Software, Marketing, Travel, Office Supplies, Professional Services, Utilities, Equipment, Meals & Entertainment, Insurance, Other]

Output as table: Date | Description | Amount | Category | Tax Deductible? | Notes
Flag any unusual expenses or potential duplicates.
Provide monthly summary by category at the end.
```

### Prompt 25: Project Status Report Generator
```
Generate a project status report from these notes:
"""
[PASTE_RAW_NOTES_OR_UPDATES]
"""

Project: [PROJECT_NAME]
Reporting period: [DATE_RANGE]
Stakeholders: [WHO_READS_THIS]

Format:
1. Executive Summary (3 sentences)
2. Progress vs. Plan (table: Milestone | Status | % Complete | ETA)
3. Achievements this period
4. Blockers & Risks (with mitigation)
5. Next period priorities
6. Resource needs / decisions needed

Traffic light status: [GREEN / YELLOW / RED] with justification.
```

### Prompt 26: SOP Writer
```
Write a Standard Operating Procedure for: [PROCESS_NAME]

Context: [WHO_DOES_THIS_AND_WHY]
Current process: [DESCRIBE_CURRENT_STEPS_ROUGHLY]
Tools used: [TOOL_1], [TOOL_2]
Frequency: [DAILY / WEEKLY / AS_NEEDED]

Format:
1. Purpose & scope
2. Prerequisites (access, tools, permissions)
3. Step-by-step procedure (numbered, with screenshots placeholder notes)
4. Quality checklist (what "done right" looks like)
5. Troubleshooting (top 3 common issues and fixes)
6. Version history table

Write for someone doing this for the first time. No assumed knowledge.
```

### Prompt 27: Meeting Agenda Creator
```
Create a meeting agenda for: [MEETING_TYPE: standup / sprint planning / 1-on-1 / quarterly review / brainstorm]

Attendees: [LIST]
Duration: [MINUTES]
Goal: [WHAT_SUCCESS_LOOKS_LIKE]
Context: [ANY_RELEVANT_BACKGROUND]

Provide:
1. Pre-meeting prep (what attendees should bring/review)
2. Timed agenda (topic | time | owner | goal)
3. Discussion prompts for each topic
4. Decision framework (how to resolve disagreements)
5. Post-meeting: action items template

Total agenda time should equal [MINUTES] minus 5 min buffer.
```

### Prompt 28: Risk Assessment Analyzer
```
Assess risks for: [PROJECT_OR_DECISION]

Context: [BACKGROUND]
Stakeholders: [WHO_IS_AFFECTED]
Timeline: [DEADLINE]
Budget: [BUDGET_IF_RELEVANT]

For each risk identified:
1. Risk description
2. Likelihood: [Low / Medium / High]
3. Impact: [Low / Medium / High]
4. Risk score (Likelihood x Impact)
5. Mitigation strategy
6. Contingency plan (if risk materializes)
7. Owner

Output as a risk register table, sorted by risk score (highest first).
Top 3 risks should have detailed mitigation plans.
```

### Prompt 29: Vendor Comparison Matrix
```
Compare these vendors/tools for [USE_CASE]:

Option A: [VENDOR_A]
Option B: [VENDOR_B]
Option C: [VENDOR_C]

Evaluation criteria:
- Price (weight: [X]%)
- Features (weight: [X]%)
- Ease of use (weight: [X]%)
- Support (weight: [X]%)
- Scalability (weight: [X]%)
- [CUSTOM_CRITERIA] (weight: [X]%)

Output:
1. Comparison matrix (criteria x vendors, scored 1-5)
2. Weighted total score
3. Pros/cons for each
4. Recommendation with reasoning
5. Migration effort estimate if switching from current tool
```

### Prompt 30: KPI Dashboard Narrative Writer
```
Write a narrative summary of these KPIs:
"""
[PASTE_KPI_DATA_OR_DESCRIBE_METRICS]
"""

Period: [THIS_MONTH / THIS_QUARTER]
Audience: [CEO / TEAM / INVESTORS]

Provide:
1. Executive headline (one sentence: are we winning or losing?)
2. Key metrics summary (table: Metric | Actual | Target | % | Trend)
3. What's working (top 3 wins with data)
4. What needs attention (top 3 concerns with data)
5. Recommended actions (specific, actionable, tied to data)
6. Forecast for next period

No fluff. Every sentence backed by a number.
```

### Prompt 31: Process Bottleneck Identifier
```
Analyze this workflow for bottlenecks:
"""
[DESCRIBE_CURRENT_WORKFLOW_STEPS_WITH_TIMES]
"""

For each step:
1. Current time to complete
2. Who does it
3. Dependencies (what must happen before this step)
4. Failure rate (if known)

Identify:
- The #1 bottleneck and why
- 3 quick wins to reduce cycle time
- Automation opportunities (what can AI/software handle?)
- Ideal vs. current flow comparison
- Estimated time savings if optimized

Output as current-state flowchart (text) → recommended future-state flowchart.
```

### Prompt 32: Resource Allocation Optimizer
```
Optimize resource allocation for these projects:

Available resources:
[PERSON_1]: [SKILLS], [HOURS_PER_WEEK]
[PERSON_2]: [SKILLS], [HOURS_PER_WEEK]
[PERSON_3]: [SKILLS], [HOURS_PER_WEEK]

Active projects:
[PROJECT_A]: [REQUIRED_SKILLS], [DEADLINE], [PRIORITY]
[PROJECT_B]: [REQUIRED_SKILLS], [DEADLINE], [PRIORITY]
[PROJECT_C]: [REQUIRED_SKILLS], [DEADLINE], [PRIORITY]

Constraints: [ANY_CONSTRAINTS]

Provide:
1. Allocation matrix (person x project x hours)
2. Conflicts and tradeoffs
3. Risk of burnout assessment
4. Recommendation for what to defer/cut if resources are insufficient
```

---

## CATEGORY 4: SALES & CRM (10 Prompts)

### Prompt 33: Lead Qualification Scorer
```
Score this lead based on our criteria:

Lead info:
"""
[PASTE_LEAD_INFO: name, company, role, company size, industry, source, behavior]
"""

Scoring criteria:
- Budget authority: [WEIGHT]
- Need/pain match: [WEIGHT]
- Timeline: [WEIGHT]
- Company size fit: [WEIGHT]
- Engagement level: [WEIGHT]

Output:
1. Score (0-100)
2. Category: [Hot / Warm / Cold / Disqualified]
3. Key signals (why this score)
4. Recommended next action
5. Personalized talking points for first call
```

### Prompt 34: Proposal Customizer
```
Customize this proposal template for a new prospect:

Template:
"""
[PASTE_PROPOSAL_TEMPLATE]
"""

Prospect details:
- Company: [COMPANY]
- Industry: [INDUSTRY]
- Pain points: [PAIN_1], [PAIN_2]
- Budget range: [BUDGET]
- Decision timeline: [TIMELINE]
- Key stakeholder: [NAME, ROLE]

Customize:
1. Executive summary (specific to their situation)
2. Proposed solution (mapped to their pain points)
3. Pricing (within their budget range)
4. Timeline (aligned with their deadline)
5. Case study (pick most relevant from: [LIST_CASE_STUDIES])
```

### Prompt 35: Objection Handler Script Generator
```
Generate objection handling scripts for selling [PRODUCT/SERVICE].

Common objections:
1. "It's too expensive"
2. "We're already using [COMPETITOR]"
3. "We need to think about it"
4. "I need to talk to my [boss/partner/team]"
5. [CUSTOM_OBJECTION]

For each objection:
- Acknowledge (validate their concern)
- Reframe (shift perspective)
- Evidence (proof point or story)
- Bridge (redirect to value)
- Close attempt (soft close question)

Tone: consultative, not pushy. The goal is to help them make the right decision.
```

### Prompt 36: Win/Loss Analysis Summarizer
```
Analyze these recent deals:

Wins:
[DEAL_1]: [DETAILS]
[DEAL_2]: [DETAILS]

Losses:
[DEAL_3]: [DETAILS]
[DEAL_4]: [DETAILS]

For each deal, analyze:
1. Key decision factors
2. Competitive dynamics
3. Sales process effectiveness
4. Pricing sensitivity

Then provide:
- Pattern analysis (what wins have in common vs losses)
- Top 3 improvement recommendations
- Ideal customer profile refinement
- Competitor strategy adjustments
```

### Prompt 37: Upsell Opportunity Identifier
```
Analyze this customer account for upsell/cross-sell opportunities:

Customer: [CUSTOMER_NAME]
Current products: [CURRENT_PRODUCTS]
Usage data: [USAGE_STATS_IF_AVAILABLE]
Account age: [MONTHS]
NPS/satisfaction: [SCORE_IF_KNOWN]
Industry: [INDUSTRY]

Our full product line: [LIST_ALL_PRODUCTS_PRICES]

Identify:
1. Top 3 upsell opportunities (with reasoning)
2. Timing recommendation (when to approach)
3. Talk track for each opportunity
4. Risk assessment (could this backfire?)
5. Expected revenue uplift
```

### Prompt 38: Sales Call Prep Briefing
```
Prepare a briefing for a sales call with:

Prospect: [NAME] at [COMPANY]
Role: [TITLE]
Meeting type: [DISCOVERY / DEMO / NEGOTIATION / CLOSE]
Previous interactions: [SUMMARY]

Research and prepare:
1. Company overview (size, industry, recent news)
2. Prospect's likely priorities based on role
3. 5 discovery questions (open-ended, insightful)
4. Potential objections and responses
5. Competitive intel (what else they might be evaluating)
6. Ideal next step after this call
7. Small talk topics (recent company news, shared interests)
```

### Prompt 39: Pipeline Forecast Narrator
```
Narrate this sales pipeline for [AUDIENCE: CEO / board / sales team]:

Pipeline data:
"""
[PASTE_PIPELINE_DATA: stage, deal name, amount, probability, close date]
"""

Provide:
1. Pipeline summary (total value, weighted value, expected close this month/quarter)
2. Stage analysis (where deals are getting stuck)
3. Top 5 deals to watch (highest impact)
4. Risk deals (at risk of slipping or losing)
5. Coverage ratio (pipeline vs. quota)
6. Recommended actions to hit target
```

### Prompt 40: Customer Segment Profiler
```
Profile our customer segments based on this data:
"""
[PASTE_CUSTOMER_DATA_OR_DESCRIBE_PATTERNS]
"""

For each segment:
1. Segment name (descriptive)
2. Demographics/firmographics
3. Behavior patterns
4. Average deal size / LTV
5. Acquisition channel
6. Pain points
7. Messaging that resonates
8. Churn risk factors

Recommend: which segment to double down on and which to deprioritize (with data justification).
```

### Prompt 41: Referral Request Composer
```
Write referral requests for these happy customers:
[CUSTOMER_1]: [WHAT_WE_DID_FOR_THEM]
[CUSTOMER_2]: [WHAT_WE_DID_FOR_THEM]

For each:
1. Personalized referral request email (reference specific results, under 100 words)
2. Make it easy: "Do you know anyone who [specific situation]?"
3. Incentive mention (if applicable): [INCENTIVE]
4. LinkedIn message version (shorter, casual)
5. Follow-up if no response (5 days later)

The ask should feel natural, not transactional.
```

### Prompt 42: Churn Risk Early Warning Analyzer
```
Analyze this customer for churn risk:

Customer: [CUSTOMER]
Account details: [PLAN, PRICE, TENURE]
Recent behavior:
"""
[PASTE_USAGE_DATA_OR_BEHAVIOR_SIGNALS]
"""

Industry churn benchmarks: [IF_KNOWN]

Assess:
1. Churn risk score (1-10)
2. Warning signals identified
3. Root cause hypothesis
4. Recommended intervention (specific action)
5. Timeline (how urgent)
6. Retention offer to consider
7. Win-back strategy if they do churn
```

---

## CATEGORY 5: DATA & RESEARCH (10 Prompts)

### Prompt 43: Market Research Summarizer
```
Summarize market research for [INDUSTRY/NICHE]:
"""
[PASTE_RAW_RESEARCH_DATA_OR_MULTIPLE_SOURCES]
"""

Output:
1. Market size and growth rate
2. Key trends (top 5)
3. Major players and market share
4. Customer demographics and behavior
5. Pricing landscape
6. Opportunities (unserved needs)
7. Threats (regulatory, competitive, technological)
8. Recommendation: should we enter/expand/pivot? Why?
```

### Prompt 44: Survey Response Analyzer
```
Analyze these survey responses:
"""
[PASTE_SURVEY_DATA]
"""

Survey goal: [WHAT_WE_WANTED_TO_LEARN]
Respondent count: [N]

Provide:
1. Key findings (top 5, with percentages)
2. Sentiment analysis (positive/neutral/negative breakdown)
3. Surprising insights (anything unexpected)
4. Correlation analysis (any interesting patterns between answers)
5. Quotes worth highlighting (verbatim responses)
6. Actionable recommendations (what to do with this data)
7. Limitations and caveats
```

### Prompt 45: Competitive Pricing Analyzer
```
Analyze pricing in the [INDUSTRY] market:

Our price: [OUR_PRICE]
Our features at that price: [OUR_FEATURES]

Competitors:
[COMPETITOR_1]: [PRICE] — [FEATURES]
[COMPETITOR_2]: [PRICE] — [FEATURES]
[COMPETITOR_3]: [PRICE] — [FEATURES]

Analyze:
1. Price positioning map (premium / mid / budget)
2. Value-per-dollar comparison
3. Feature gap analysis (what do they offer that we don't, and vice versa)
4. Price elasticity estimate
5. Recommended pricing strategy (raise / lower / bundle / tiered)
6. A/B test suggestion for pricing page
```

### Prompt 46: Trend Spotter from News Feeds
```
Analyze these recent articles/news items for trends:
"""
[PASTE_HEADLINES_OR_ARTICLES]
"""

Industry: [INDUSTRY]
Time period: [LAST_WEEK / LAST_MONTH / LAST_QUARTER]

Identify:
1. Top 3 emerging trends (with evidence from the articles)
2. Declining trends (what's fading)
3. Signals vs. noise (which trends have staying power)
4. Implications for [MY_BUSINESS]
5. Action items (how to capitalize on each trend)
6. Predicted timeline (when will each trend peak)
```

### Prompt 47: SWOT Analysis Generator
```
Generate a SWOT analysis for [BUSINESS/PROJECT/PRODUCT].

Context:
- What we do: [DESCRIPTION]
- Market position: [MARKET_POSITION]
- Recent performance: [PERFORMANCE_SUMMARY]
- Competitive landscape: [KEY_COMPETITORS]

Output:
1. Strengths (internal, current advantages) — 5 items
2. Weaknesses (internal, current limitations) — 5 items
3. Opportunities (external, future potential) — 5 items
4. Threats (external, future risks) — 5 items
5. SWOT matrix visualization (text)
6. Strategic implications (SO/WO/ST/WT strategies)
7. Top 3 priority actions
```

### Prompt 48: Customer Feedback Theme Extractor
```
Extract themes from this customer feedback:
"""
[PASTE_FEEDBACK: reviews, support tickets, NPS comments, social mentions]
"""

Output:
1. Theme ranking (most mentioned to least)
2. Sentiment per theme (positive/negative/mixed)
3. Verbatim quotes for each theme (best examples)
4. Urgency assessment (which themes need immediate action)
5. Feature request patterns
6. Competitor mentions and context
7. Recommended product roadmap priorities based on this data
```

### Prompt 49: Industry Report Key Takeaway Extractor
```
Extract key takeaways from this report:
"""
[PASTE_REPORT_TEXT_OR_KEY_SECTIONS]
"""

Report: [REPORT_TITLE]
Published by: [PUBLISHER]
Date: [DATE]

Output:
1. Executive summary (5 bullet points)
2. Key statistics (table: metric | value | implication)
3. Predictions/forecasts
4. How this affects [MY_BUSINESS] specifically
5. Action items based on this report
6. Quotes worth sharing (for social media / internal communication)
```

### Prompt 50: A/B Test Result Analyzer
```
Analyze this A/B test:

Test: [WHAT_WE_TESTED]
Hypothesis: [WHAT_WE_EXPECTED]
Duration: [DAYS]
Sample size: Control [N], Variant [N]

Results:
Control: [METRIC] = [VALUE]
Variant: [METRIC] = [VALUE]

Additional data:
[ANY_SEGMENTED_DATA]

Analyze:
1. Statistical significance (is the result real?)
2. Practical significance (is the difference meaningful?)
3. Confidence interval
4. Segment analysis (did it work better for some groups?)
5. Recommendation: ship / iterate / kill
6. Next test to run based on learnings
```

### Prompt 51: ROI Calculator Narrative
```
Calculate and narrate the ROI for [INVESTMENT/TOOL/HIRE]:

Investment: [COST]
Time period: [MONTHS]
Benefits:
- [BENEFIT_1]: [ESTIMATED_VALUE]
- [BENEFIT_2]: [ESTIMATED_VALUE]
- [BENEFIT_3]: [ESTIMATED_VALUE]

Costs:
- [COST_1]: [AMOUNT]
- [COST_2]: [AMOUNT]

Calculate:
1. Net ROI percentage
2. Payback period
3. Break-even point
4. 12-month projected return
5. Sensitivity analysis (best/worst/likely scenarios)
6. Non-financial benefits
7. Executive summary (one paragraph to justify the investment)
```

### Prompt 52: Data Cleanup & Standardizer
```
Clean and standardize this data:
"""
[PASTE_MESSY_DATA]
"""

Issues to fix:
- Inconsistent formatting (dates, phone numbers, addresses)
- Duplicates
- Missing values
- Typos and misspellings
- Inconsistent capitalization
- Invalid entries

Output:
1. Cleaned data (same format as input but fixed)
2. Change log (what was fixed and why)
3. Data quality score (before vs after)
4. Entries that need human review (ambiguous cases)
```

---

## BONUS: Prompt Chaining Guide

### Chain 1: Lead to Close
```
Prompt 33 (Score Lead) → Prompt 38 (Call Prep) → Prompt 35 (Handle Objections) → Prompt 34 (Customize Proposal) → Prompt 36 (Win/Loss Analysis)
```

### Chain 2: Content Machine
```
Prompt 11 (Blog Outline) → Write the post → Prompt 20 (Repurpose) → Prompt 12 (Calendar) → Prompt 21 (Hashtags)
```

### Chain 3: Customer Success
```
Prompt 42 (Churn Risk) → Prompt 37 (Upsell) → Prompt 8 (Feedback) → Prompt 18 (Testimonial) → Prompt 41 (Referral)
```

### Chain 4: Operations Audit
```
Prompt 31 (Bottleneck) → Prompt 26 (SOP) → Prompt 28 (Risk) → Prompt 30 (KPI Narrative)
```

---

## LLM Comparison Chart

| Task Type | Best LLM | Why |
|-----------|----------|-----|
| Long-form writing | Claude | Superior at nuanced, long-form content |
| Data analysis | ChatGPT (Code Interpreter) | Can run Python, create charts |
| Quick tasks | ChatGPT | Fast responses for simple prompts |
| Code-heavy | Claude or ChatGPT | Both strong; Claude better at complex logic |
| Creative brainstorming | Claude or Gemini | More creative, less formulaic |
| Research synthesis | Claude | 200K context window handles long inputs |
| Structured output (JSON) | ChatGPT | Better at consistent JSON formatting |
| Multilingual | Gemini | Strongest multilingual capabilities |

---

*52 prompts. 5 categories. Unlimited business leverage.*
*Buy once. Use forever. Automate everything.*
