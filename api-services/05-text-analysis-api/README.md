# Text Analysis / NLP API

Pure JavaScript text analysis API running on Cloudflare Workers. No external AI APIs required.

## Endpoints

### `POST /analyze` - Full analysis
```json
{"text": "Your text here"}
```
Returns: word count, character count, sentence/paragraph count, reading time, speaking time, readability (Flesch-Kincaid), sentiment, language detection, top 10 keywords, and 3 summary sentences.

### `POST /sentiment` - Sentiment only
Returns: sentiment (positive/negative/neutral), score (-1 to 1), confidence (0 to 1).

### `POST /keywords` - Keywords only
Returns: top 10 keywords with frequency and TF-IDF relevance score.

### `POST /readability` - Readability only
Returns: Flesch-Kincaid Grade Level, Flesch Reading Ease, avg words/sentence, avg syllables/word.

### `GET /` or `GET /health` - Health check

## Features

- **Sentiment Analysis**: AFINN-style lexicon (200+ words) with negation handling and intensifiers
- **Language Detection**: Character frequency + common word matching for 10 languages (en, es, fr, de, pt, it, nl, ja, zh, ko)
- **Keyword Extraction**: TF-IDF scoring with 200+ stop words
- **Readability**: Flesch-Kincaid Grade Level and Reading Ease
- **Extractive Summary**: TextRank-inspired sentence ranking
- **Limits**: Max 100,000 characters per request

## Development

```bash
npm install
npm run dev      # Local dev server
npm run deploy   # Deploy to Cloudflare
```

## Base URL

```
https://text-analysis-api.t-mizuno27.workers.dev
```
