# Free Text Analysis API - Sentiment, Keywords, Readability, NLP

> **Free tier: 500 requests/month** | Pure JavaScript NLP -- no external AI APIs required

Analyze text for sentiment, extract keywords, calculate readability scores, detect language, and count words/sentences. Runs entirely on Cloudflare Workers with zero external dependencies.

## Getting Started in 30 Seconds

1. Subscribe on [RapidAPI](https://rapidapi.com/miccho27-5OJaGGbBiO/api/text-analysis-api) (free plan available)
2. Copy your API key
3. Analyze your first text:

```bash
curl -X POST "https://text-analysis-api.p.rapidapi.com/analyze" \
  -H "Content-Type: application/json" \
  -H "X-RapidAPI-Key: YOUR_KEY" \
  -H "X-RapidAPI-Host: text-analysis-api.p.rapidapi.com" \
  -d '{"text": "This product is absolutely amazing! Best purchase I ever made."}'
```

## How It Compares

| Feature | This API | MonkeyLearn | Aylien | MeaningCloud |
|---------|----------|-------------|--------|--------------|
| Free tier | 500 req/mo | 300 req/mo | None | 1,000 req/day (limited) |
| Pricing | $5.99/50K | $299/mo | Custom | $79/mo |
| Sentiment analysis | Yes | Yes | Yes | Yes |
| Keyword extraction | Yes | Yes | Yes | Yes |
| Readability score | Yes (Flesch-Kincaid) | No | No | No |
| Language detection | Yes | No | Yes | Yes |
| No external AI costs | Yes (pure JS NLP) | No (ML models) | No | No |
| Edge latency | Sub-50ms (CF Workers) | 200-500ms | 300-800ms | 200-600ms |
| Setup complexity | None (RapidAPI key only) | OAuth + dashboard | OAuth + dashboard | API key + dashboard |

## Why Choose This Text Analysis API?

- **No external AI costs** -- pure JavaScript NLP, no GPT/Claude API calls behind the scenes
- **Multi-feature** -- sentiment analysis, keyword extraction, readability scoring, language detection
- **Fast** -- sub-50ms processing on Cloudflare Workers edge
- **Privacy-friendly** -- text is not sent to any third-party AI service
- **Free tier** -- 500 requests/month at $0

## Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/analyze` | POST | Full analysis (sentiment + keywords + readability + language) |
| `/sentiment` | POST | Sentiment analysis only |
| `/keywords` | POST | Keyword extraction only |
| `/readability` | POST | Readability score only |

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

### Node.js Example

```javascript
const axios = require("axios");

const { data } = await axios.post(
  "https://text-analysis-api.p.rapidapi.com/analyze",
  { text: "Great product, fast shipping!" },
  {
    headers: {
      "X-RapidAPI-Key": "YOUR_KEY",
      "X-RapidAPI-Host": "text-analysis-api.p.rapidapi.com",
    },
  }
);

console.log(`Sentiment: ${data.sentiment}, Keywords: ${data.keywords}`);
```

## FAQ

**Q: Does this API use GPT or any external AI?**
A: No. It uses pure JavaScript NLP algorithms running directly on Cloudflare Workers. Your text never leaves Cloudflare's network.

**Q: What languages are supported for sentiment analysis?**
A: English is the primary language. Language detection works for 50+ languages. Sentiment accuracy is highest for English text.

**Q: Can I analyze long documents?**
A: Yes, but for best results keep text under 10,000 characters per request. For larger documents, split into paragraphs and analyze individually.

**Q: What is the Flesch-Kincaid readability score?**
A: It estimates the US school grade level needed to understand the text. A score of 8.0 means an 8th grader can understand it. Lower scores = easier to read.

## Pricing

| Plan | Price | Requests/mo | Rate Limit |
|------|-------|-------------|------------|
| Basic (FREE) | $0 | 500 | 1 req/sec |
| Pro | $5.99 | 50,000 | 10 req/sec |

## Alternative To

A free alternative to MonkeyLearn, Aylien, and MeaningCloud. No per-analysis pricing, no AI API costs.


## Also From This Publisher

Build powerful workflows by combining APIs:

| API | Why Combine? |
|-----|-------------|
| **AI Text API** | Generate text then analyze its quality |
| **AI Translation API** | Translate then analyze sentiment per language |
| **SEO Analyzer API** | Combine content analysis with technical SEO |
| **News Aggregator API** | Analyze sentiment of news headlines |

> All APIs include a free tier. Subscribe to one, discover the full toolkit on [our RapidAPI profile](https://rapidapi.com/miccho27-5OJaGGbBiO).

## Keywords

`text analysis api`, `sentiment analysis api`, `nlp api`, `keyword extraction`, `readability score`, `text mining`, `content analysis`, `free nlp api`, `language detection`, `flesch kincaid api`
