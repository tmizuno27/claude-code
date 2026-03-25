---
title: "Free Text Analysis API — Sentiment, Keywords, Readability in One Call (No GPT Costs)"
published: false
description: "Analyze text for sentiment, extract keywords, calculate readability scores, and detect language. Pure JS NLP on Cloudflare Workers — no AI API costs. Python & JavaScript examples."
tags: api, nlp, javascript, python
---

Need sentiment analysis, keyword extraction, or readability scoring in your app? Most NLP APIs either charge per token (OpenAI), require heavy ML infrastructure (spaCy server), or cost $200+/month (MonkeyLearn).

I built a **free Text Analysis API** that runs pure JavaScript NLP on Cloudflare Workers. No external AI calls behind the scenes — which means **predictable costs, fast responses, and no data sent to third-party AI providers**.

## What You Get in One API Call

Send any text and get back:

- **Sentiment analysis** — positive, negative, or neutral with a confidence score
- **Keyword extraction** — top keywords ranked by relevance
- **Readability scores** — Flesch-Kincaid grade level and reading ease
- **Language detection** — ISO 639-1 language code
- **Word and sentence count** — basic text statistics

All from a single `POST /analyze` endpoint.

## Quick Start

```bash
curl -X POST "https://text-analysis-api.p.rapidapi.com/analyze" \
  -H "Content-Type: application/json" \
  -H "X-RapidAPI-Key: YOUR_KEY" \
  -H "X-RapidAPI-Host: text-analysis-api.p.rapidapi.com" \
  -d '{"text": "This product is absolutely amazing! Best purchase I have ever made. The quality exceeded all my expectations."}'
```

**Response:**

```json
{
  "sentiment": {
    "label": "positive",
    "score": 0.92
  },
  "keywords": [
    {"word": "product", "score": 0.85},
    {"word": "purchase", "score": 0.72},
    {"word": "quality", "score": 0.68},
    {"word": "expectations", "score": 0.61}
  ],
  "readability": {
    "flesch_reading_ease": 72.4,
    "flesch_kincaid_grade": 5.2
  },
  "language": "en",
  "statistics": {
    "word_count": 19,
    "sentence_count": 3,
    "avg_word_length": 5.1
  }
}
```

## JavaScript — Real-Time Content Feedback

Show writers their content quality as they type:

```javascript
const API_URL = "https://text-analysis-api.p.rapidapi.com/analyze";
const HEADERS = {
  "Content-Type": "application/json",
  "X-RapidAPI-Key": "YOUR_KEY",
  "X-RapidAPI-Host": "text-analysis-api.p.rapidapi.com",
};

async function analyzeContent(text) {
  const res = await fetch(API_URL, {
    method: "POST",
    headers: HEADERS,
    body: JSON.stringify({ text }),
  });
  return res.json();
}

// Debounced analysis on text input
let timeout;
document.querySelector("#editor").addEventListener("input", (e) => {
  clearTimeout(timeout);
  timeout = setTimeout(async () => {
    const text = e.target.value;
    if (text.length < 50) return; // Skip short text

    const result = await analyzeContent(text);

    // Update UI
    document.querySelector("#word-count").textContent = result.statistics.word_count;
    document.querySelector("#readability").textContent =
      `Grade ${result.readability.flesch_kincaid_grade} — ${getReadabilityLabel(result.readability.flesch_reading_ease)}`;
    document.querySelector("#sentiment").textContent =
      `${result.sentiment.label} (${Math.round(result.sentiment.score * 100)}%)`;
    document.querySelector("#keywords").textContent =
      result.keywords.map((k) => k.word).join(", ");
  }, 1000);
});

function getReadabilityLabel(score) {
  if (score >= 80) return "Easy to read";
  if (score >= 60) return "Standard";
  if (score >= 40) return "Somewhat difficult";
  return "Difficult";
}
```

This gives content writers instant feedback without relying on expensive AI APIs.

## Python — Batch Sentiment Analysis for Product Reviews

```python
import requests
import json

API_URL = "https://text-analysis-api.p.rapidapi.com/analyze"
HEADERS = {
    "Content-Type": "application/json",
    "X-RapidAPI-Key": "YOUR_KEY",
    "X-RapidAPI-Host": "text-analysis-api.p.rapidapi.com",
}

reviews = [
    "Absolutely love this product. Works perfectly out of the box.",
    "Terrible quality. Broke after two days. Waste of money.",
    "It's okay. Does what it says but nothing special.",
    "Fast shipping, great packaging, product exceeded expectations!",
    "Customer support was unhelpful and rude. Will not buy again.",
]


def analyze_text(text: str) -> dict:
    """Analyze a single text for sentiment and keywords."""
    resp = requests.post(
        API_URL,
        headers=HEADERS,
        json={"text": text},
    )
    return resp.json()


# Analyze all reviews
results = []
for review in reviews:
    analysis = analyze_text(review)
    results.append({
        "review": review[:60] + "..." if len(review) > 60 else review,
        "sentiment": analysis["sentiment"]["label"],
        "confidence": analysis["sentiment"]["score"],
        "keywords": [k["word"] for k in analysis["keywords"][:3]],
    })

# Summary
positive = sum(1 for r in results if r["sentiment"] == "positive")
negative = sum(1 for r in results if r["sentiment"] == "negative")
neutral = sum(1 for r in results if r["sentiment"] == "neutral")

print(f"Total: {len(results)} reviews")
print(f"Positive: {positive} | Negative: {negative} | Neutral: {neutral}")
print(f"Satisfaction rate: {positive / len(results) * 100:.0f}%")
print()

for r in results:
    emoji = {"positive": "+", "negative": "-", "neutral": "~"}[r["sentiment"]]
    print(f"  [{emoji}] {r['review']}")
    print(f"      Keywords: {', '.join(r['keywords'])}")
```

## Python — Content Quality Checker for Blog Posts

```python
def check_blog_quality(text: str) -> dict:
    """Check if a blog post meets quality standards."""
    analysis = analyze_text(text)

    issues = []
    stats = analysis["statistics"]
    readability = analysis["readability"]

    if stats["word_count"] < 300:
        issues.append(f"Too short ({stats['word_count']} words, aim for 800+)")
    if readability["flesch_kincaid_grade"] > 12:
        issues.append(f"Too complex (grade {readability['flesch_kincaid_grade']}, aim for 8-10)")
    if readability["flesch_reading_ease"] < 40:
        issues.append(f"Hard to read (score {readability['flesch_reading_ease']}, aim for 60+)")
    if len(analysis["keywords"]) < 3:
        issues.append("Not enough distinct keywords — content may lack focus")

    return {
        "word_count": stats["word_count"],
        "grade_level": readability["flesch_kincaid_grade"],
        "reading_ease": readability["flesch_reading_ease"],
        "top_keywords": [k["word"] for k in analysis["keywords"][:5]],
        "issues": issues,
        "pass": len(issues) == 0,
    }
```

## How It Compares

| Feature | This API | MonkeyLearn | Aylien | MeaningCloud |
|---------|----------|-------------|--------|--------------|
| Free tier | 500 req/mo | 300 req/mo | None | Limited |
| Paid pricing | $5.99/50K | $299/mo | Custom | $79/mo |
| Sentiment | Yes | Yes | Yes | Yes |
| Keywords | Yes | Yes | Yes | Yes |
| Readability | Yes (Flesch-Kincaid) | No | No | No |
| Language detection | Yes | No | Yes | Yes |
| External AI costs | None (pure JS NLP) | ML models | ML models | ML models |
| Latency | <50ms | 200-500ms | 300-800ms | 200-600ms |

The key difference: **no hidden AI API costs**. The NLP runs entirely in JavaScript on Cloudflare Workers. Your text is not forwarded to OpenAI, Google, or any other provider.

## When to Use This vs. GPT/Claude

Use **this API** when you need:
- Consistent, fast, cheap sentiment/keyword/readability analysis
- Privacy-sensitive text processing (no third-party AI)
- High-volume analysis (50K+ texts/month)

Use **GPT/Claude** when you need:
- Nuanced understanding, sarcasm detection, topic classification
- Summarization or text generation
- Context-dependent analysis

They complement each other. Use this API for the quantitative layer, and LLMs for the qualitative layer.

## Try It Free

1. [Text Analysis API on RapidAPI](https://rapidapi.com/miccho27-5OJaGGbBiO/api/text-analysis-api)
2. Free plan: 500 requests/month, no credit card
3. POST your text, get structured NLP results in <50ms

---

*Part of a [collection of 24 free developer APIs](https://rapidapi.com/user/miccho27-5OJaGGbBiO) on Cloudflare Workers.*
