# AI Text API

Text generation, summarization, translation, sentiment analysis, and rewriting powered by Cloudflare Workers AI (Llama 3.1 8B Instruct, free tier).

## Endpoints

| Method | Path | Description |
|--------|------|-------------|
| GET | `/` | API info |
| POST | `/generate` | Text generation (prompt, max_tokens, temperature) |
| POST | `/summarize` | Summarize text (text, max_length) |
| POST | `/translate` | Translate text (text, source_lang, target_lang) |
| POST | `/sentiment` | Sentiment analysis (text) |
| POST | `/rewrite` | Rewrite in different tone (text, tone: formal/casual/professional/simple) |

## Limits

- Rate limit: 30 requests/minute per IP
- Max prompt (`/generate`): 1,000 characters
- Max text (`/summarize`, `/translate`, `/sentiment`, `/rewrite`): 5,000 characters

## Setup

```bash
npm install
npx wrangler dev    # local dev
npx wrangler deploy # deploy to Cloudflare
```

Requires a Cloudflare account with Workers AI enabled (free tier).

## Example

```bash
curl -X POST https://ai-text-api.YOUR-SUBDOMAIN.workers.dev/generate \
  -H "Content-Type: application/json" \
  -d '{"prompt": "Write a haiku about coding", "max_tokens": 100}'
```
