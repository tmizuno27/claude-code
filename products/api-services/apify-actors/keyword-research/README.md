# Keyword Research - Google Autocomplete Keyword Expander & Scorer

Fetches Google Suggest autocomplete suggestions for a list of seed keywords,
expands them with question-pattern variants, scores every candidate
for longtail/question potential, and outputs the top-N results to the Apify
dataset. A free alternative to Ahrefs Keywords Explorer, SEMrush Keyword Magic, and Ubersuggest.

Converted from `nambei-oyaji.com/scripts/content/keyword_research.py`.

---

## Input

| Field | Type | Default | Description |
|---|---|---|---|
| `keywords` | `string[]` | *required* | Seed keywords to research |
| `language` | `string` | `"ja"` | Google Suggest `hl` locale param |
| `topN` | `integer` | `20` | Number of top results to output |
| `requestDelaySeconds` | `number` | `1.0` | Delay between HTTP requests (seconds) |
| `maxQuestionPatterns` | `integer` | `4` | Question-suffix variants per seed (max 12) |

### Example input

```json
{
  "keywords": ["パラグアイ 移住", "副業 おすすめ", "格安SIM 比較"],
  "language": "ja",
  "topN": 20,
  "requestDelaySeconds": 1.0,
  "maxQuestionPatterns": 4
}
```

---

## Output (Apify dataset)

Each item in the dataset represents one ranked keyword:

```json
{
  "priority": 1,
  "keyword": "パラグアイ 移住 費用",
  "type": "longtail",
  "score": 65.0,
  "source_seed": "パラグアイ 移住",
  "status": "pending"
}
```

| Field | Description |
|---|---|
| `priority` | Rank (1 = highest score) |
| `keyword` | Normalised keyword string |
| `type` | `"longtail"` / `"question"` / `"main"` |
| `score` | Internal score (higher = better longtail potential) |
| `source_seed` | Which seed keyword produced this result |
| `status` | Always `"pending"` — consumed downstream by `article_generator` |

---

## Scoring logic

- **Longtail** (3+ words or 10+ chars): base +30
- **Question** (ends with a Japanese informational suffix): base +20
- **Main** keyword: base +10
- Word-count bonus: +5 per word, capped at +20
- Optimal character count (8–25 chars): +10; >25 chars: −5
- High-value term present (`稼ぐ`, `副業`, `おすすめ`, etc.): +5

---

## Why Choose This Actor?

- **Google Suggest data** -- real autocomplete suggestions reflecting actual user search behavior
- **Automatic expansion** -- generates question-pattern variants for each seed keyword
- **Smart scoring** -- longtail keywords scored higher for content targeting potential
- **Multi-language** -- supports any Google Suggest locale (ja, en, es, etc.)
- **No API keys** -- uses public Google Suggest endpoint

## FAQ

**Q: How does this differ from Ahrefs or SEMrush keyword tools?**
A: This Actor focuses on Google autocomplete suggestions (real user queries) with automatic scoring. It lacks search volume data but is free and great for discovering long-tail content ideas.

**Q: Can I use this for English keywords?**
A: Yes. Set `language: "en"` in the input. The question patterns are optimized for Japanese by default but work with any language.

**Q: How many keywords can I research at once?**
A: No hard limit. Each seed keyword generates 10-50 suggestions. Processing time scales linearly.

## Local development

```bash
pip install apify
python -m src.main
```

Set `APIFY_IS_AT_HOME=1` and `APIFY_INPUT_KEY` if running locally against a
real Apify key-value store, or place an `apify_storage/key_value_stores/default/INPUT.json`
file with your input JSON for offline testing.

---

## Building & pushing to Apify

```bash
apify push
```
