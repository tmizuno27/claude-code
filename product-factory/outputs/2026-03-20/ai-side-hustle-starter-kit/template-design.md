# AI Side Hustle Starter Kit — Template Design

## パート1: Notionテンプレート設計（7 DB）

### DB1: AI Prompts（AIプロンプト集）
| プロパティ | タイプ | 説明 |
|-----------|--------|------|
| Prompt Name | Title | プロンプト名 |
| Category | Select | Blog Writing / Social Media / Email / Ad Copy / SEO / Client Comms / Ideation |
| Prompt Text | Text | コピペ用プロンプト本文 |
| AI Tool | Multi-select | ChatGPT / Claude / Gemini / Any |
| Difficulty | Select | Beginner / Intermediate / Advanced |
| Output Type | Select | Long-form / Short-form / List / Template |
| Tips | Text | 使い方のコツ |
| Favorite | Checkbox | お気に入り |

**ビュー:**
- Table: 全プロンプト一覧（Category でソート）
- Board: Category でグループ化（カンバン）
- Gallery: カード表示（プロンプト名+カテゴリ）
- Filtered: Favorites のみ
- Filtered: Beginner のみ（初心者向け）

### DB2: Clients（クライアント管理CRM）
| プロパティ | タイプ | 説明 |
|-----------|--------|------|
| Client Name | Title | クライアント名 |
| Status | Select | Lead / Contacted / Proposal Sent / Active / Completed / Lost |
| Service | Select | Blog Writing / Social Media / Email Marketing / Ad Copy / SEO / Other |
| Contact | Email | メールアドレス |
| Source | Select | LinkedIn / Twitter/X / Upwork / Fiverr / Referral / Cold Outreach |
| Deal Value | Number ($) | 案件金額 |
| Next Action | Text | 次のアクション |
| Follow-up Date | Date | フォローアップ日 |
| Notes | Text | メモ |
| Projects | Relation → Projects | 紐付くプロジェクト |

**ビュー:**
- Board: Status でグループ化（セールスパイプライン）
- Table: 全クライアント一覧
- Calendar: Follow-up Date でカレンダー表示
- Filtered: Active クライアントのみ

### DB3: Projects（プロジェクト管理）
| プロパティ | タイプ | 説明 |
|-----------|--------|------|
| Project Name | Title | プロジェクト名 |
| Client | Relation → Clients | クライアント |
| Service Type | Select | Blog Writing / Social Media / Email Marketing / Ad Copy / SEO / Other |
| Status | Select | Not Started / In Progress / Review / Delivered / Paid |
| Deadline | Date | 納期 |
| Fee | Number ($) | 報酬額 |
| Paid | Checkbox | 入金済み |
| AI Prompts Used | Relation → AI Prompts | 使用したプロンプト |
| Deliverables | Text | 納品物の説明 |
| Income | Relation → Income | 収入レコード |

**ビュー:**
- Board: Status でグループ化
- Table: 全プロジェクト一覧
- Calendar: Deadline でカレンダー表示
- Filtered: Unpaid（Paid = false）のみ

### DB4: Income（収入トラッカー）
| プロパティ | タイプ | 説明 |
|-----------|--------|------|
| Description | Title | 収入の説明 |
| Amount | Number ($) | 金額 |
| Date | Date | 入金日 |
| Source | Select | Freelance / Product Sales / Affiliate / Other |
| Client | Relation → Clients | クライアント |
| Project | Relation → Projects | プロジェクト |
| Payment Method | Select | PayPal / Stripe / Bank Transfer / Crypto / Other |
| Status | Select | Pending / Received / Overdue |

**ビュー:**
- Table: 全収入一覧（Date で降順ソート）
- Board: Source でグループ化
- Calendar: Date でカレンダー表示
- Summary: 月別集計ビュー

### DB5: AI Tools（AIツール比較）
| プロパティ | タイプ | 説明 |
|-----------|--------|------|
| Tool Name | Title | ツール名 |
| Category | Select | Text / Image / Video / Audio / Code / Multi-modal |
| Pricing | Text | 料金体系 |
| Free Tier | Checkbox | 無料プランあり |
| Best For | Multi-select | Blog Writing / Social Media / Email / Ad Copy / SEO / Image Gen / Code |
| URL | URL | サイトURL |
| Rating | Select | 1 / 2 / 3 / 4 / 5 |
| Notes | Text | レビューメモ |

**ビュー:**
- Table: 全ツール一覧
- Board: Category でグループ化
- Gallery: カード表示
- Filtered: Free Tier のみ

### DB6: Weekly Planner（週間プランナー）
| プロパティ | タイプ | 説明 |
|-----------|--------|------|
| Task | Title | タスク名 |
| Day | Select | Monday / Tuesday / Wednesday / Thursday / Friday / Saturday / Sunday |
| Time Block | Select | Morning / Afternoon / Evening |
| Category | Select | Client Work / Prospecting / Content Creation / Admin / Learning |
| Duration | Number (hrs) | 所要時間 |
| Completed | Checkbox | 完了 |
| AI Prompt | Relation → AI Prompts | 使用するプロンプト |

**ビュー:**
- Board: Day でグループ化（週間ボード）
- Table: 全タスク一覧
- Board: Category でグループ化

### DB7: Service Packages（サービスパッケージ）
| プロパティ | タイプ | 説明 |
|-----------|--------|------|
| Package Name | Title | パッケージ名 |
| Service Type | Select | Blog Writing / Social Media / Email Marketing / Ad Copy / SEO / Content Strategy |
| Pricing Model | Select | Per Project / Hourly / Monthly Retainer |
| Price Range | Text | 価格帯（例: $200-500/project） |
| Deliverables | Text | 納品物の詳細 |
| Time Estimate | Text | 所要時間目安 |
| AI Prompts | Relation → AI Prompts | 推奨プロンプト |
| Description | Text | クライアント向け説明文 |

**ビュー:**
- Table: 全パッケージ一覧
- Gallery: カード表示（パッケージ名+価格）

## ダッシュボード構成

```
┌──────────────────────────────────────────┐
│  AI Side Hustle Starter Kit              │
│  "From Zero to First Client with AI"     │
├──────────────────────────────────────────┤
│  Revenue This Month: $____               │
│  Active Clients: __  |  Pipeline: __     │
│  Projects Due This Week: __              │
├─────────────────────┬────────────────────┤
│ Sales Pipeline      │ Income Tracker     │
│ (Clients Board)     │ (Monthly summary)  │
│                     │                    │
├─────────────────────┼────────────────────┤
│ This Week's Plan    │ Quick Access       │
│ (Weekly Planner     │ Prompts            │
│  filtered: current) │ (Favorites view)   │
├─────────────────────┴────────────────────┤
│ Quick Links:                              │
│ [All Prompts] [Clients] [Projects]        │
│ [Income] [AI Tools] [Packages] [Planner]  │
└──────────────────────────────────────────┘
```

## リレーション
- Clients ↔ Projects: クライアントのプロジェクト一覧
- Projects ↔ AI Prompts: プロジェクトで使用したプロンプト
- Projects ↔ Income: プロジェクトの入金記録
- Weekly Planner ↔ AI Prompts: タスクで使うプロンプト
- Service Packages ↔ AI Prompts: パッケージの推奨プロンプト
- Income ↔ Clients: 収入のクライアント紐付け

## サンプルデータ

### Clients（3件）
1. "TechStartup Co." — Status: Active, Service: Blog Writing, Deal Value: $500, Source: LinkedIn
2. "Sarah's Bakery" — Status: Proposal Sent, Service: Social Media, Deal Value: $300, Source: Referral
3. "DigitalNomad Blog" — Status: Lead, Service: SEO, Deal Value: $400, Source: Twitter/X

### Projects（2件）
1. "Monthly Blog Package — TechStartup Co." — Service: Blog Writing, Status: In Progress, Fee: $500, Deadline: Next Friday
2. "Instagram Content Calendar — Sarah's Bakery" — Service: Social Media, Status: Not Started, Fee: $300, Deadline: Next Month

### Income（2件）
1. "Blog Package — March" — $500, Date: March 15, Source: Freelance, Status: Received
2. "Social Media Audit" — $150, Date: March 10, Source: Freelance, Status: Received

### AI Tools（5件）
1. "ChatGPT" — Text, Free Tier: Yes, Best For: Blog Writing / Email / Ad Copy, Rating: 5
2. "Claude" — Text, Free Tier: Yes, Best For: Blog Writing / SEO / Content Strategy, Rating: 5
3. "Midjourney" — Image, Free Tier: No, Best For: Image Gen, Rating: 4
4. "Canva AI" — Image, Free Tier: Yes, Best For: Social Media / Image Gen, Rating: 4
5. "Jasper" — Text, Free Tier: No, Best For: Ad Copy / Email, Rating: 3

### Service Packages（3件）
1. "Blog Content Package" — Blog Writing, Per Project, $300-600/month (4 posts), Time: 8-10 hrs/month
2. "Social Media Manager" — Social Media, Monthly Retainer, $400-800/month, Time: 10-15 hrs/month
3. "Email Sequence Setup" — Email Marketing, Per Project, $200-400, Time: 4-6 hrs

---

## パート2: AIプロンプト50本（カテゴリ別構成）

### Category 1: Blog Writing (10 prompts)
1. **SEO Blog Post Generator** — "Write a 1,500-word blog post about [TOPIC] targeting the keyword [KEYWORD]. Include an engaging introduction with a hook, 5-7 H2 subheadings, practical examples, and a conclusion with a call to action. Tone: conversational but authoritative."
2. **Blog Outline Creator** — "Create a detailed outline for a blog post about [TOPIC]. Include: a compelling title (under 60 chars), meta description (under 155 chars), 6-8 H2 sections with 2-3 bullet points each, and 3 internal linking opportunities."
3. **Listicle Generator** — "Write a listicle titled '[NUMBER] [ADJECTIVE] [THINGS] for [AUDIENCE]'. Each item should have a bold title, 2-3 sentence explanation, and a practical tip. Make it scannable and actionable."
4. **How-To Guide Writer** — "Write a step-by-step how-to guide on [TOPIC] for [AUDIENCE]. Include: prerequisites, 7-10 numbered steps with detailed instructions, common mistakes to avoid, and expected results."
5. **Blog Post Refresher** — "Rewrite this blog post to improve readability and SEO. Keep the core message but: shorten paragraphs to 2-3 sentences, add transition phrases, include the keyword [KEYWORD] 3-5 times naturally, and add a FAQ section. Original: [PASTE TEXT]"
6. **Case Study Writer** — "Write a case study about [SUBJECT] achieving [RESULT]. Structure: Challenge (what problem they faced), Solution (what they did), Results (specific numbers), Key Takeaways (3 lessons). Length: 800-1,000 words."
7. **Product Review Writer** — "Write an honest, detailed review of [PRODUCT] for [AUDIENCE]. Include: overview, key features (pros/cons), pricing comparison, who it's best for, and a verdict. Tone: helpful and unbiased."
8. **Content Repurposer** — "Take this blog post and create: (1) a LinkedIn post (300 words), (2) a Twitter/X thread (5 tweets), (3) an Instagram caption (150 words), (4) a newsletter intro (100 words). Original: [PASTE TEXT]"
9. **Comparison Article Writer** — "Write a comparison article: [PRODUCT A] vs [PRODUCT B] for [USE CASE]. Include: overview of each, feature-by-feature comparison table, pricing, pros/cons, and a recommendation based on user type."
10. **FAQ Section Generator** — "Generate 8 frequently asked questions and detailed answers about [TOPIC]. Each answer should be 50-100 words, factual, and include a natural mention of [KEYWORD]. Format as structured Q&A."

### Category 2: Social Media (10 prompts)
11. **Twitter/X Thread Creator** — "Write a 7-tweet thread about [TOPIC]. Tweet 1: bold hook with a number or contrarian take. Tweets 2-6: one key insight each with a specific example. Tweet 7: summary + CTA. Use line breaks for readability."
12. **LinkedIn Post Generator** — "Write a LinkedIn post about [TOPIC/EXPERIENCE]. Start with a one-line hook. Tell a brief story (what happened, what you learned). End with 3 actionable takeaways and a question to drive comments. 200-300 words."
13. **Instagram Caption Writer** — "Write 5 Instagram captions for a [NICHE] account. Each caption: hook in first line, value in body (3-5 lines), CTA, and 10 relevant hashtags. Tone: authentic and engaging."
14. **Social Media Calendar** — "Create a 7-day social media content calendar for a [BUSINESS TYPE]. For each day include: platform, content type (carousel, reel, story, text post), topic, caption draft, and best posting time."
15. **Viral Hook Generator** — "Generate 20 scroll-stopping hooks for social media posts about [TOPIC]. Mix formats: questions, bold statements, 'How I...' stories, numbered lists, and contrarian takes. Each hook should be under 15 words."
16. **Hashtag Research** — "Generate 30 hashtags for a [NICHE] post about [TOPIC]. Organize into: 10 high-volume (500K+ posts), 10 medium (50K-500K), 10 niche-specific (under 50K). Include estimated reach category."
17. **YouTube Title & Thumbnail Ideas** — "Generate 10 YouTube video title and thumbnail text combinations for a video about [TOPIC]. Each title should use curiosity gaps, numbers, or power words. Include a thumbnail text (4-6 words max) for each."
18. **TikTok/Reel Script** — "Write a 60-second TikTok/Reel script about [TOPIC]. Structure: Hook (first 3 seconds), Problem, Solution (3 tips), CTA. Include on-screen text suggestions and transition notes."
19. **Community Engagement Responses** — "Write 10 thoughtful, value-adding comment responses for posts in [NICHE] communities. Each response should: acknowledge the original post, add a unique insight, and end with a soft authority signal. No self-promotion."
20. **Social Proof Post** — "Write a social media post sharing a client win/testimonial. Structure: 'Just helped [CLIENT TYPE] achieve [RESULT].' Brief backstory. What you did (without giving away the full process). Lesson for the audience. Subtle CTA."

### Category 3: Email Marketing (8 prompts)
21. **Welcome Email Sequence (3-email)** — "Write a 3-email welcome sequence for new subscribers of [BUSINESS]. Email 1: Warm welcome + deliver the lead magnet + what to expect. Email 2 (Day 2): Your story + biggest insight. Email 3 (Day 4): Introduce your paid offer + social proof."
22. **Cold Outreach Email** — "Write a cold outreach email to [TARGET ROLE] at [COMPANY TYPE] offering [SERVICE]. Keep it under 100 words. Personalization placeholder: [SPECIFIC THING ABOUT THEIR BUSINESS]. Clear CTA: book a 15-min call."
23. **Follow-Up Email Series** — "Write 3 follow-up emails for a prospect who hasn't replied. Email 1 (Day 3): Quick check-in + add new value. Email 2 (Day 7): Share a relevant case study. Email 3 (Day 14): Breakup email with a final offer."
24. **Newsletter Template** — "Write a weekly newsletter issue about [TOPIC]. Structure: One-line subject line (curiosity-driven), personal intro (2 sentences), main insight (300 words), 3 curated links with one-line descriptions, CTA."
25. **Sales Page Email** — "Write a sales email for [PRODUCT/SERVICE] priced at [PRICE]. Structure: Subject line (urgency/curiosity), pain point, agitate, introduce solution, 3 bullet benefits, social proof, CTA, P.S. with bonus/deadline."
26. **Client Proposal Email** — "Write a proposal email for [SERVICE] to [CLIENT TYPE]. Include: understanding of their problem (show research), proposed solution (3 phases), timeline, pricing (3 tiers), next steps. Professional but warm tone."
27. **Testimonial Request Email** — "Write an email asking a satisfied client for a testimonial. Be specific about what to include: the problem they had, the result they got, and whether they'd recommend you. Make it easy to respond (provide a template)."
28. **Re-engagement Email** — "Write an email to re-engage inactive subscribers/clients. Subject line with curiosity gap. Acknowledge the silence. Share something valuable and new. Soft CTA. Include an easy unsubscribe note."

### Category 4: Ad Copy & Sales (7 prompts)
29. **Facebook/Instagram Ad Copy** — "Write 3 Facebook ad variations for [PRODUCT/SERVICE]. For each: Primary text (125 words, hook + problem + solution + CTA), Headline (5 words), Description (1 sentence). Target: [AUDIENCE]. Goal: [CLICK/SIGN UP/BUY]."
30. **Google Ads Copy** — "Write 5 Google Search ad variations for the keyword [KEYWORD]. Each ad: 3 headlines (30 chars max each), 2 descriptions (90 chars max each). Include the keyword naturally. Focus on benefits and urgency."
31. **Landing Page Copy** — "Write landing page copy for [PRODUCT/SERVICE]. Include: Hero headline + subheadline, 3 pain points, solution introduction, 6 bullet benefits, 2 testimonial placeholders, pricing section, FAQ (4 questions), final CTA."
32. **Product Description** — "Write a compelling product description for [PRODUCT] sold on [PLATFORM]. Include: one-line hook, key features (5 bullets), ideal customer profile, what's included, and a scarcity/urgency element. 200 words max."
33. **Sales Script (Discovery Call)** — "Write a discovery call script for selling [SERVICE] to [CLIENT TYPE]. Include: rapport building (2 min), situation questions (3), problem questions (3), implication questions (2), present solution, handle 3 common objections, close."
34. **Upsell/Cross-sell Email** — "Write an email to existing clients offering [NEW SERVICE/UPGRADE]. Reference their current results. Introduce the upgrade as a natural next step. Include an exclusive loyalty discount. Deadline: [DATE]."
35. **Pricing Page Copy** — "Write pricing page copy for 3 tiers of [SERVICE]: Basic, Pro, Premium. For each tier: name, price, tagline, 5-8 features with checkmarks, who it's best for, CTA button text. Highlight the Pro tier as 'Most Popular'."

### Category 5: SEO & Content Strategy (8 prompts)
36. **Keyword Cluster Generator** — "Generate a keyword cluster for the topic [MAIN TOPIC]. Include: 1 pillar keyword, 5 cluster keywords, 10 long-tail keywords, estimated search intent for each (informational/transactional/navigational), and suggested content type."
37. **Meta Title & Description Writer** — "Write SEO-optimized meta titles (under 60 chars) and meta descriptions (under 155 chars) for these 5 pages: [LIST PAGES]. Include the primary keyword naturally and a compelling reason to click."
38. **Content Gap Analyzer Prompt** — "I run a [BUSINESS TYPE] website. My top 5 competitors are: [LIST]. Analyze what content topics they likely cover that I'm missing. Suggest 10 content pieces I should create to fill gaps, with target keywords and content type."
39. **Internal Linking Strategy** — "Given these 10 blog posts: [LIST TITLES], suggest an internal linking strategy. For each post, recommend 2-3 posts it should link to and the anchor text to use. Prioritize topical relevance."
40. **Schema Markup Generator** — "Generate JSON-LD schema markup for a [PAGE TYPE: FAQ/How-to/Product/Article] page about [TOPIC]. Include all required and recommended properties. Output as a ready-to-paste script tag."
41. **Content Brief Creator** — "Create a comprehensive content brief for an article about [TOPIC] targeting [KEYWORD]. Include: target word count, search intent, outline (H2s and H3s), 5 competitor URLs to analyze, key points to cover, internal links, and CTA."
42. **Topic Authority Builder** — "I want to become a topical authority on [SUBJECT]. Create a 20-article content plan organized by: 5 pillar posts (2,000+ words), 10 supporting posts (1,000-1,500 words), 5 FAQ/glossary posts (500-800 words). Include target keywords."
43. **Local SEO Optimizer** — "Optimize this business listing for local SEO: [BUSINESS NAME, TYPE, LOCATION]. Generate: Google Business Profile description (750 chars), 5 Google Posts, 10 local keywords to target, and 3 citation-building opportunities."

### Category 6: Client Communication (4 prompts)
44. **Project Kickoff Brief** — "Write a project kickoff document for [PROJECT TYPE] with [CLIENT NAME]. Include: project overview, objectives (3), scope of work, timeline with milestones, deliverables list, communication plan (frequency/channel), and next steps."
45. **Progress Update Email** — "Write a weekly progress update email to a client. Include: what was completed this week (3 items), what's in progress, any blockers or decisions needed, plan for next week, and estimated completion vs. deadline."
46. **Scope Creep Response** — "Write a professional email responding to a client requesting work outside the original scope. Acknowledge the request positively. Explain what's included in the current scope. Offer to add it as a separate project with a quote. Maintain the relationship."
47. **Project Wrap-Up Email** — "Write a project completion email to a client. Include: summary of what was delivered, results/metrics if available, how to access/use deliverables, invitation for feedback, mention of ongoing support options, and a referral ask."

### Category 7: Ideation & Strategy (3 prompts)
48. **Side Hustle Idea Generator** — "Generate 10 AI-powered side hustle ideas for someone with skills in [SKILLS]. For each idea: name, description (2 sentences), target market, revenue model, startup cost, monthly income potential, and which AI tools to use."
49. **Niche Research Prompt** — "Research the [NICHE] market for freelance opportunities. Analyze: market size, typical client budgets, most in-demand services (top 5), common pain points clients have, where to find clients, and 3 ways to differentiate from competitors."
50. **90-Day Side Hustle Plan** — "Create a 90-day action plan to launch a [SERVICE TYPE] side hustle. Break into: Month 1 (Foundation: skills, portfolio, pricing), Month 2 (Launch: first clients, systems), Month 3 (Scale: processes, raise prices). Include weekly milestones."
