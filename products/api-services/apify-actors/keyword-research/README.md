# Keyword Research - Free Google Autocomplete Keyword Expander & Scorer

Discover high-potential long-tail keywords from Google Autocomplete suggestions -- for free. Input seed keywords, get ranked keyword ideas with scoring based on search intent and content targeting potential. The best free alternative to Ahrefs Keywords Explorer, SEMrush Keyword Magic Tool, Ubersuggest, and KWFinder.

## Who Is This For?

- **SEO specialists** -- Find low-competition long-tail keywords for content strategy
- **Content marketers** -- Discover what real users are searching for in Google
- **Bloggers & affiliate marketers** -- Identify question-based keywords for FAQ and how-to articles
- **E-commerce SEO** -- Expand product category keywords into buyer-intent variants
- **Agencies** -- Bulk keyword research for multiple clients in one run

## Features

- **Google Autocomplete Data** -- Real suggestions from Google Suggest reflecting actual user search behavior
- **Automatic Question Expansion** -- Generates question-pattern variants (who, what, when, where, why, how) for each seed keyword
- **Smart Longtail Scoring** -- Keywords scored 0-100 based on word count, character length, question intent, and high-value terms
- **Multi-Language Support** -- Works with any Google Suggest locale (Japanese, English, Spanish, German, French, Portuguese, and 50+ languages)
- **No API Keys Required** -- Uses Google's public Suggest endpoint, no developer account needed
- **Bulk Seed Processing** -- Input dozens of seed keywords, get hundreds of ranked suggestions

## Pricing -- Free to Start

| Tier | Cost | What You Get |
|------|------|-------------|
| **Free trial** | $0 | Apify free tier includes monthly compute credits |
| **Pay per run** | ~$0.01-0.03/run | Typically 10-50 suggestions per seed keyword |
| **vs. Ahrefs** | Saves $99-999/mo | Real autocomplete data, no subscription needed |
| **vs. SEMrush** | Saves $129-499/mo | Same Google Suggest source, smart scoring included |

## How It Compares to Paid Keyword Tools

| Feature | This Actor (FREE) | Ahrefs ($99/mo) | SEMrush ($129/mo) | Ubersuggest ($29/mo) |
|---------|-------------------|-----------------|-------------------|---------------------|
| Google Autocomplete data | Yes | Yes | Yes | Yes |
| Question keyword expansion | Auto-generated | Manual filter | Manual filter | Manual filter |
| Longtail scoring | Built-in (0-100) | Keyword Difficulty | Keyword Difficulty | SEO Difficulty |
| Search volume data | No (autocomplete only) | Yes | Yes | Yes |
| Multi-language | 50+ languages | Yes | Yes | Limited |
| API keys required | None | Yes | Yes | Yes |
| Bulk processing | Unlimited seeds | Plan-limited | Plan-limited | Plan-limited |
| Monthly cost | $0 (pay per run) | $99-999 | $129-499 | $29-99 |

> **When to use this Actor:** You want free, real-time keyword ideas from what people actually type into Google. Combine with free tools like Google Search Console for volume estimation.

## Quick Start (3 Steps)

1. **Click "Try for free"** on this Actor's page in Apify Store
2. **Enter seed keywords** (e.g., `["best CRM software", "email marketing"]`) and set your language
3. **Click "Start"** and download ranked keyword ideas as JSON, CSV, or Excel

## Input

| Field | Type | Default | Description |
|---|---|---|---|
| `keywords` | `string[]` | *required* | Seed keywords to research |
| `language` | `string` | `"ja"` | Google Suggest `hl` locale param (e.g. `ja`, `en`, `es`, `de`, `fr`, `pt`) |
| `topN` | `integer` | `20` | Number of top results to output (1-200) |
| `requestDelaySeconds` | `number` | `1.0` | Delay between HTTP requests (seconds) |
| `maxQuestionPatterns` | `integer` | `4` | Question-suffix variants per seed (max 12) |

### Example Input -- Japanese SEO

```json
{
  "keywords": ["パラグアイ 移住", "副業 おすすめ", "格安SIM 比較"],
  "language": "ja",
  "topN": 20,
  "requestDelaySeconds": 1.0,
  "maxQuestionPatterns": 4
}
```

### Example Input -- English SEO

```json
{
  "keywords": ["best CRM software", "remote work tools", "email marketing"],
  "language": "en",
  "topN": 50,
  "requestDelaySeconds": 1.0,
  "maxQuestionPatterns": 6
}
```

## Output (Apify Dataset)

Each item in the dataset represents one ranked keyword:

```json
{
  "priority": 1,
  "keyword": "パラグアイ 移住 費用",
  "type": "longtail",
  "score": 65.0,
  "source_seed": "パラグアイ 移住",
  "status": "pending"
}
```

| Field | Description |
|---|---|
| `priority` | Rank (1 = highest score) |
| `keyword` | Normalized keyword string |
| `type` | `"longtail"` / `"question"` / `"main"` |
| `score` | Internal score (higher = better longtail/content potential) |
| `source_seed` | Which seed keyword produced this result |
| `status` | Always `"pending"` -- ready for your content pipeline |

## Scoring Logic

| Criteria | Points | Description |
|---------|--------|-------------|
| Longtail (3+ words or 10+ chars) | +30 | Long-tail keywords have less competition |
| Question intent | +20 | Question keywords convert well for informational content |
| Main keyword | +10 | Base score for seed match |
| Word count bonus | +5/word (max +20) | More specific = more targeted |
| Optimal length (8-25 chars) | +10 | Sweet spot for keyword targeting |
| Over 25 chars | -5 | Too long for title optimization |
| High-value terms | +5 | Contains commercial intent words |

## Real-World Use Cases

### 1. Blog Content Calendar
Input 10 seed keywords from your niche, get 200+ ranked keyword ideas, and build a 3-month content calendar of long-tail articles that rank faster than head terms.

### 2. FAQ Page Generator
Use question-type keywords to build comprehensive FAQ sections that capture featured snippets and People Also Ask positions in Google.

### 3. E-commerce Category Expansion
Input product category keywords to discover long-tail buyer-intent variations for product page SEO and PPC campaigns.

### 4. Competitor Keyword Gap Analysis
Research your competitors' main topics to find long-tail variations they might be missing, then create content targeting those gaps.

### 5. Multi-Language SEO
Run the same seeds across `en`, `ja`, `es`, `de`, `fr` to discover how search behavior differs by market before launching international content.

## FAQ

**Q: How does this differ from Ahrefs or SEMrush keyword tools?**
A: This Actor focuses on Google Autocomplete suggestions (what real users actually type) with automatic scoring. It lacks search volume data but is completely free and great for discovering long-tail content ideas. Use it alongside free volume tools like Google Search Console for the best results.

**Q: Can I use this for English keywords?**
A: Yes. Set `language: "en"` in the input. Supports 50+ languages including English, Spanish, German, French, Portuguese, and more.

**Q: How many keywords can I research at once?**
A: No hard limit. Each seed keyword generates 10-50 suggestions. Processing time scales linearly. A typical run with 10 seeds completes in under 2 minutes.

**Q: How fresh is the data?**
A: Google Autocomplete updates in near real-time based on trending searches. Each run fetches live data, so you always get the latest suggestions.

**Q: Can I schedule this to run weekly?**
A: Yes. Use Apify's built-in scheduler to track keyword trends over time. Export results to Google Sheets via Apify integrations for a free keyword tracking dashboard.

## Local Development

```bash
pip install apify
python -m src.main
```

Set `APIFY_IS_AT_HOME=1` and `APIFY_INPUT_KEY` if running locally against a real Apify key-value store, or place an `apify_storage/key_value_stores/default/INPUT.json` file with your input JSON for offline testing.

## Building & Pushing to Apify

```bash
apify push
```
