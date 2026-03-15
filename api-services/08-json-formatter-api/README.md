# JSON Formatter & Validator API

All-in-one JSON toolkit on Cloudflare Workers: format, minify, validate, diff, transform, and CSV conversion.

**Base URL:** `https://json-formatter-api.t-mizuno27.workers.dev`

## Endpoints

| Method | Path | Description |
|--------|------|-------------|
| POST | `/format` | Prettify JSON with configurable indent |
| POST | `/minify` | Minify JSON |
| POST | `/validate` | Validate JSON, return errors and stats |
| POST | `/diff` | Deep-compare two JSON objects |
| POST | `/transform` | JMESPath-like query on JSON |
| POST | `/csv-to-json` | Convert CSV string to JSON array |
| POST | `/json-to-csv` | Convert JSON array to CSV string |

## Examples

### Format
```bash
curl -X POST https://json-formatter-api.t-mizuno27.workers.dev/format \
  -H "Content-Type: application/json" \
  -d '{"data": "{\"name\":\"John\",\"age\":30}", "indent": 4}'
```

### Validate
```bash
curl -X POST https://json-formatter-api.t-mizuno27.workers.dev/validate \
  -H "Content-Type: application/json" \
  -d '{"data": "{\"key\": \"value\"}"}'
```

Response: `{"valid": true, "errors": [], "stats": {"keys": 1, "depth": 1, "size_bytes": 16}}`

### Diff
```bash
curl -X POST https://json-formatter-api.t-mizuno27.workers.dev/diff \
  -H "Content-Type: application/json" \
  -d '{"a": {"name": "John", "age": 30}, "b": {"name": "Jane", "age": 30, "city": "NYC"}}'
```

### Transform
```bash
curl -X POST https://json-formatter-api.t-mizuno27.workers.dev/transform \
  -H "Content-Type: application/json" \
  -d '{"data": {"items": [{"name": "A"}, {"name": "B"}]}, "query": "items[*].name"}'
```

### CSV to JSON
```bash
curl -X POST https://json-formatter-api.t-mizuno27.workers.dev/csv-to-json \
  -H "Content-Type: application/json" \
  -d '{"csv": "name,age\nJohn,30\nJane,25", "headers": true}'
```

## Development

```bash
npm install
npm run dev      # Local dev server
npm run deploy   # Deploy to Cloudflare
```
