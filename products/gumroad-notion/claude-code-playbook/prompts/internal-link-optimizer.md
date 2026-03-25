# Internal Link Optimizer Prompt

## Objective
Analyze all published articles on your site, identify missing internal link opportunities, and generate optimized link insertions with contextual anchor text.

## Required Context / Inputs
- `outputs/article-management.csv` — all published articles with URLs, titles, categories
- WordPress REST API credentials in `config/secrets.json`
- OR: local HTML/Markdown copies of your articles

## Prompt

```
Optimize internal linking across my entire site.

1. **Content Mapping**:
   - Read outputs/article-management.csv to get all published articles
   - For each article, fetch the full content via WordPress REST API (config/secrets.json)
   - Create a topic map: article_id, title, url, primary_topic, related_topics, existing_internal_links

2. **Gap Detection**:
   - For each article, identify other articles it SHOULD link to but doesn't
   - Criteria for a good internal link:
     - Topically relevant (same cluster or complementary topic)
     - Adds value for the reader (not forced)
     - Uses descriptive anchor text (not "click here" or naked URLs)
     - Distributed naturally throughout the article (not all clustered at the end)
   - Flag articles with ZERO internal links (high priority)
   - Flag articles with only 1 internal link (medium priority)

3. **Link Generation**:
   - For each gap, generate:
     - Source article ID and title
     - Target article URL and title
     - Suggested anchor text (3-7 words, descriptive, keyword-relevant)
     - Insertion point (which paragraph, with surrounding context)
   - Aim for 3-5 internal links per article minimum

4. **Implementation**:
   - Generate the updated HTML for each article with new links inserted
   - Push updates via WordPress REST API
   - Log every change: source_article, target_article, anchor_text, position

5. **Output**:
   - Save link map to outputs/internal-link-report.csv
   - Save change log to logs/internal-link-updates.log
   - Print summary: total links added, articles updated, articles still needing attention

Mode: [audit-only / audit-and-apply]
Site: [YOUR SITE]
```

## Expected Output
- `outputs/internal-link-report.csv` — full link map with recommendations
- `logs/internal-link-updates.log` — change log (if apply mode)
- Console summary with statistics

## Example Usage

```
Mode: audit-only
Site: nambei-oyaji.com
```

Run `audit-only` first to review recommendations, then `audit-and-apply` to push changes.

## Tips
- Run after publishing new articles to integrate them into the existing link structure
- Prioritize linking from high-traffic pages to pages you want to rank higher
- Avoid over-linking (more than 8-10 internal links per article looks spammy)
- Use this monthly as part of your SEO maintenance routine
