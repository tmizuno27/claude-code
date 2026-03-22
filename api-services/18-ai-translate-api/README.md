# Free AI Translation API - 100+ Languages via Meta M2M-100

> **Free tier: 500 requests/month** | Neural machine translation powered by Cloudflare Workers AI

Translate text between 100+ languages using Meta's M2M-100 1.2B model running on Cloudflare Workers AI free tier. No Google Translate or DeepL API key needed.

## Why Choose This Translation API?

- **100+ languages** -- powered by Meta's M2M-100 multilingual model
- **No upstream API key** -- runs on Cloudflare Workers AI free tier
- **Direct translation** -- translates between any language pair without pivoting through English
- **Neural quality** -- modern transformer model, not rule-based translation
- **Free tier** -- 500 requests/month at $0

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

## Pricing

| Plan | Price | Requests/mo | Rate Limit |
|------|-------|-------------|------------|
| Basic (FREE) | $0 | 500 | 1 req/sec |
| Pro | $9.99 | 50,000 | 10 req/sec |

## Alternative To

A free alternative to DeepL API, Google Translate API, and LibreTranslate.

## Keywords

`translation api`, `ai translate api`, `free translation api`, `multilingual api`, `machine translation`, `deepl alternative`, `google translate alternative`, `m2m100 api`, `language translation`, `text translation api`
