# Free Text Analysis API - Sentiment, Keywords, Readability, NLP

> **Free tier: 500 requests/month** | Pure JavaScript NLP -- no external AI APIs required

Analyze text for sentiment, extract keywords, calculate readability scores, detect language, and count words/sentences. Runs entirely on Cloudflare Workers with zero external dependencies.

## Why Choose This Text Analysis API?

- **No external AI costs** -- pure JavaScript NLP, no GPT/Claude API calls behind the scenes
- **Multi-feature** -- sentiment analysis, keyword extraction, readability scoring, language detection
- **Fast** -- sub-50ms processing on Cloudflare Workers edge
- **Privacy-friendly** -- text is not sent to any third-party AI service
- **Free tier** -- 500 requests/month at $0

## Use Cases

- **Content moderation** -- detect negative sentiment in user reviews or comments
- **SEO tools** -- extract keywords and check readability scores before publishing
- **Marketing analytics** -- analyze customer feedback and survey responses at scale
- **Education platforms** -- score text readability (Flesch-Kincaid) for grade-level targeting
- **Chatbots** -- route conversations based on detected sentiment
- **CRM enrichment** -- auto-tag support tickets by topic and sentiment

## Quick Start

```bash
curl -X POST "https://text-analysis-api.t-mizuno27.workers.dev/analyze" \
  -H "Content-Type: application/json" \
  -H "X-RapidAPI-Key: YOUR_KEY" \
  -d '{"text": "This product is absolutely amazing! Best purchase I ever made."}'
```

### Python Example

```python
import requests

url = "https://text-analysis-api.p.rapidapi.com/analyze"
headers = {"X-RapidAPI-Key": "YOUR_KEY", "X-RapidAPI-Host": "text-analysis-api.p.rapidapi.com"}
payload = {"text": "Great product, fast shipping, highly recommended!"}

data = requests.post(url, headers=headers, json=payload).json()
print(f"Sentiment: {data['sentiment']} | Keywords: {data['keywords']}")
```

## Pricing

| Plan | Price | Requests/mo | Rate Limit |
|------|-------|-------------|------------|
| Basic (FREE) | $0 | 500 | 1 req/sec |
| Pro | $5.99 | 50,000 | 10 req/sec |

## Alternative To

A free alternative to MonkeyLearn, Aylien, and MeaningCloud. No per-analysis pricing, no AI API costs.

## Keywords

`text analysis api`, `sentiment analysis api`, `nlp api`, `keyword extraction`, `readability score`, `text mining`, `content analysis`, `free nlp api`, `language detection`, `flesch kincaid api`
