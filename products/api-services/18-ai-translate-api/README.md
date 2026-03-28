# Free AI Translation API - 100+ Languages via Meta M2M-100

> **Free tier: 500 requests/month** | Neural machine translation powered by Cloudflare Workers AI

Translate text between 100+ languages using Meta's M2M-100 1.2B model running on Cloudflare Workers AI free tier. No Google Translate or DeepL API key needed.

## Getting Started in 30 Seconds

1. Subscribe on [RapidAPI](https://rapidapi.com/miccho27-5OJaGGbBiO/api/ai-translate-api) (free plan available)
2. Copy your API key
3. Translate your first text:

```bash
curl -X POST "https://ai-translate-api.p.rapidapi.com/translate" \
  -H "Content-Type: application/json" \
  -H "X-RapidAPI-Key: YOUR_KEY" \
  -H "X-RapidAPI-Host: ai-translate-api.p.rapidapi.com" \
  -d '{"text": "Hello, how are you?", "source": "en", "target": "es"}'
```

## How It Compares

| Feature | This API | DeepL API | Google Translate | LibreTranslate |
|---------|----------|-----------|-----------------|----------------|
| Free tier | 500 req/mo | 500K chars/mo | $300 credit | Self-hosted |
| Pro pricing | $9.99/50K req | $5.49/1M chars | $20/1M chars | Free (self-host) |
| Languages | 100+ | 31 | 130+ | 30+ |
| Direct translation | Yes (any pair) | Via English pivot | Yes | Via English pivot |
| Batch translation | Yes | Yes | Yes | No |
| Language detection | Yes | Yes | Yes | Yes |
| Neural model | Meta M2M-100 (1.2B) | Proprietary | Proprietary | Argos Translate |
| No upstream API key | Yes (CF Workers AI) | No | No | Self-hosted |

## Why Choose This Translation API?

- **100+ languages** -- powered by Meta's M2M-100 multilingual model
- **No upstream API key** -- runs on Cloudflare Workers AI free tier
- **Direct translation** -- translates between any language pair without pivoting through English
- **Neural quality** -- modern transformer model, not rule-based translation
- **Batch support** -- translate multiple texts in one request
- **Free tier** -- 500 requests/month at $0

## Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/translate` | POST | Translate text between languages |
| `/detect` | POST | Detect language of input text |
| `/batch` | POST | Translate multiple texts at once |
| `/languages` | GET | List all supported languages |

## Use Cases

- **SaaS localization** -- translate UI strings and content dynamically
- **Customer support** -- translate incoming tickets and outgoing responses
- **E-commerce** -- translate product listings for international markets
- **Chat apps** -- real-time message translation between users
- **Content platforms** -- offer auto-translation for user-generated content
- **Education** -- translate study materials and assignments

## Quick Start

```bash
curl -X POST "https://ai-translate-api.t-mizuno27.workers.dev/translate" \
  -H "Content-Type: application/json" \
  -H "X-RapidAPI-Key: YOUR_KEY" \
  -d '{"text": "Hello, how are you?", "source": "en", "target": "es"}'
```

### Python Example

```python
import requests

url = "https://ai-translate-api.p.rapidapi.com/translate"
headers = {"X-RapidAPI-Key": "YOUR_KEY", "X-RapidAPI-Host": "ai-translate-api.p.rapidapi.com"}
payload = {"text": "Good morning", "source": "en", "target": "ja"}

data = requests.post(url, headers=headers, json=payload).json()
print(f"Translation: {data['translated_text']}")
```

### Node.js Example

```javascript
const axios = require("axios");

const { data } = await axios.post(
  "https://ai-translate-api.p.rapidapi.com/batch",
  {
    texts: ["Hello", "How are you?", "Thank you"],
    source: "en",
    target: "fr"
  },
  {
    headers: {
      "X-RapidAPI-Key": "YOUR_KEY",
      "X-RapidAPI-Host": "ai-translate-api.p.rapidapi.com",
    },
  }
);

data.translations.forEach(t => console.log(t.translated_text));
```

## FAQ

**Q: How does the translation quality compare to Google Translate?**
A: For major language pairs (EN-ES, EN-FR, EN-DE, EN-JA), quality is comparable. For less common pairs, Google may have an edge due to more training data.

**Q: Can I translate without specifying the source language?**
A: Yes. Use the `/detect` endpoint first, or omit the `source` field and the API will auto-detect.

**Q: Is there a character limit per request?**
A: Single requests support up to 5,000 characters. For longer texts, split into paragraphs or use the batch endpoint.

**Q: What does "direct translation" mean?**
A: M2M-100 can translate directly between any two supported languages (e.g., Japanese to Spanish) without going through English first, which improves accuracy.

## Pricing

| Plan | Price | Requests/mo | Rate Limit |
|------|-------|-------------|------------|
| Basic (FREE) | $0 | 500 | 1 req/sec |
| Pro | $9.99 | 50,000 | 10 req/sec |

## Alternative To

A free alternative to DeepL API, Google Translate API, and LibreTranslate. Neural translation with 100+ languages and no per-character pricing.


## Also From This Publisher

Build powerful workflows by combining APIs:

| API | Why Combine? |
|-----|-------------|
| **AI Text API** | Generate content then translate to any language |
| **Text Analysis API** | Analyze sentiment in the source language |
| **News Aggregator API** | Translate international news headlines |
| **PDF Generator API** | Generate multilingual PDF documents |

> All APIs include a free tier. Subscribe to one, discover the full toolkit on [our RapidAPI profile](https://rapidapi.com/miccho27-5OJaGGbBiO).

## Keywords

`translation api`, `ai translate api`, `free translation api`, `multilingual api`, `machine translation`, `deepl alternative`, `google translate alternative`, `m2m100 api`, `language translation`, `text translation api`
