# AI Translate API

Translation API powered by Cloudflare Workers AI (free tier) using the `@cf/meta/m2m100-1.2b` model.

## Endpoints

| Method | Path | Description |
|--------|------|-------------|
| GET | `/` | API info with supported languages |
| POST | `/translate` | Translate text |
| POST | `/detect` | Detect language (uses Llama 3.1 8B) |
| POST | `/batch` | Batch translate up to 10 texts |
| GET | `/languages` | List supported language codes |

## Usage

### Translate

```bash
curl -X POST https://ai-translate-api.<account>.workers.dev/translate \
  -H "Content-Type: application/json" \
  -d '{"text": "Hello world", "source_lang": "en", "target_lang": "ja"}'
```

### Detect Language

```bash
curl -X POST https://ai-translate-api.<account>.workers.dev/detect \
  -H "Content-Type: application/json" \
  -d '{"text": "Bonjour le monde"}'
```

### Batch Translate

```bash
curl -X POST https://ai-translate-api.<account>.workers.dev/batch \
  -H "Content-Type: application/json" \
  -d '{"texts": ["hello", "world"], "source_lang": "en", "target_lang": "es"}'
```

## Supported Languages (44)

en, es, fr, de, it, pt, nl, pl, ru, zh, ja, ko, ar, hi, tr, vi, th, id, cs, ro, da, fi, hu, no, sv, uk, bg, el, hr, sk, sl, sr, lt, lv, et, mt, ga, cy, af, sw, ha, ig, yo, zu

## Rate Limiting

30 requests per minute per IP.

## Setup

```bash
npm install
npx wrangler dev    # local development
npx wrangler deploy # deploy to Cloudflare
```

Requires a Cloudflare account with Workers AI enabled (free tier).
