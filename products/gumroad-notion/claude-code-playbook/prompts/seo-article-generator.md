# SEO Article Generator Prompt

## Objective
Generate a complete, SEO-optimized article ready for WordPress publishing. The article should follow E-E-A-T principles, include proper heading structure, internal links, and strategic affiliate link placement.

## Required Context / Inputs
Before running this prompt, ensure you have:
- `config/affiliate-links.json` — your affiliate link database
- `outputs/article-management.csv` — list of existing published articles (for internal linking)
- `templates/article-template.md` — your article structure template (optional but recommended)
- Target keyword decided

## Prompt

```
I need you to generate a complete SEO article. Follow these steps:

1. **Research Phase**:
   - Web search the target keyword: "[YOUR KEYWORD]"
   - Analyze the top 5 ranking pages for structure, word count, and topics covered
   - Identify "People Also Ask" questions related to this keyword
   - Check current facts, statistics, and data points (all numbers must be verified)

2. **Planning Phase**:
   - Create an article outline with H2/H3 structure
   - Plan internal links by reading my existing articles in outputs/article-management.csv
   - Identify 2-3 affiliate link placement opportunities from config/affiliate-links.json

3. **Writing Phase**:
   - Write a 2500-3500 word article targeting "[YOUR KEYWORD]"
   - Include the primary keyword in: title, first paragraph, one H2, meta description
   - Use natural keyword variations throughout (don't keyword-stuff)
   - Include a comparison table if the topic involves multiple options
   - Add a FAQ section with 5-8 questions from "People Also Ask"
   - Write a compelling meta description (150-160 characters)

4. **Optimization Phase**:
   - Insert 3-5 internal links to relevant existing articles
   - Add affiliate links where contextually appropriate
   - Ensure all external claims have a source
   - Verify the article reads naturally (not AI-sounding)

5. **Output**:
   - Save the article as HTML to outputs/articles/[slug].html
   - Save metadata (title, slug, category, meta description, word count) to a JSON sidecar file
   - Update outputs/article-management.csv with the new entry

Target keyword: [YOUR KEYWORD]
Target category: [YOUR CATEGORY]
Target audience: [DESCRIBE YOUR READER]
Tone: [informational / conversational / professional]
```

## Expected Output
- `outputs/articles/[keyword-slug].html` — complete article in HTML
- `outputs/articles/[keyword-slug].json` — metadata file
- Updated `outputs/article-management.csv`

## Example Usage

```
Target keyword: "best budget smartphones 2026"
Target category: tech-reviews
Target audience: cost-conscious consumers researching their next phone purchase
Tone: conversational but authoritative
```

## Tips
- Run this prompt with web search enabled for accurate, current data
- Review the output before publishing — check affiliate links are correct and facts are verified
- For batch generation, create a keyword queue CSV and loop through it
