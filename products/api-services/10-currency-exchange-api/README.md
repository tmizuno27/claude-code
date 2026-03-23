# Free Currency Exchange Rate API - Real-Time & Historical FX Rates

> **Free tier: 500 requests/month** | ECB-sourced exchange rates for 30+ currencies with conversion and history

Get real-time and historical currency exchange rates from the European Central Bank (ECB). Convert between 30+ currencies, fetch historical rates back to 1999, and list all supported currency codes. No API key required for the underlying data source.

## Getting Started in 30 Seconds

1. Subscribe on [RapidAPI](https://rapidapi.com/miccho27-5OJaGGbBiO/api/currency-exchange-api) (free plan available)
2. Copy your API key
3. Get your first exchange rate:

```bash
curl -X GET "https://currency-exchange-api.p.rapidapi.com/rates?base=USD" \
  -H "X-RapidAPI-Key: YOUR_KEY" \
  -H "X-RapidAPI-Host: currency-exchange-api.p.rapidapi.com"
```

## How It Compares

| Feature | This API | Fixer.io | ExchangeRate-API | Open Exchange Rates |
|---------|----------|---------|-----------------|-------------------|
| Free tier | 500 req/mo | 100 req/mo | 1,500 req/mo | 1,000 req/mo |
| Pro pricing | $5.99/50K | $10/mo | $9.99/mo | $12/mo |
| Data source | ECB (official) | ECB + others | Central banks | Multiple |
| Currencies | 30+ | 170+ | 160+ | 170+ |
| Historical rates | Yes (back to 1999) | Yes (paid) | Yes (paid) | Yes (paid) |
| Direct conversion | Yes | Yes | Yes | Yes |
| Base currency (free) | Any | EUR only (free) | USD only (free) | USD only (free) |
| No upstream API key | Yes (free Frankfurter) | No | No | No |
| 1-hour edge cache | Yes (CF Workers) | No | No | No |

## Why Choose This Currency Exchange API?

- **Official ECB data** -- exchange rates sourced from the European Central Bank via Frankfurter API
- **Historical rates** -- access exchange rates dating back to January 1999
- **30+ currencies** -- USD, EUR, GBP, JPY, BRL, CNY, INR, and many more
- **Direct conversion** -- convert amounts between any two currencies in a single call
- **1-hour caching** -- fresh rates with fast response times via Cloudflare edge cache
- **Free tier** -- 500 requests/month at $0

## Use Cases

- **E-commerce** -- display product prices in customer's local currency
- **Fintech apps** -- power currency conversion features in banking and payment apps
- **Travel apps** -- real-time exchange rates for travel planning and expense tracking
- **Accounting software** -- historical rates for multi-currency bookkeeping and reconciliation
- **SaaS pricing** -- localize subscription pricing by region
- **Crypto exchanges** -- convert fiat amounts alongside cryptocurrency prices
- **Data analytics** -- normalize revenue data across currencies for reporting

## Quick Start

### Get Latest Rates

```bash
curl -X GET "https://currency-exchange-api.t-mizuno27.workers.dev/rates?base=USD" \
  -H "X-RapidAPI-Key: YOUR_KEY"
```

**Response:**
```json
{
  "base": "USD",
  "date": "2026-03-20",
  "rates": {
    "EUR": 0.9234,
    "GBP": 0.7891,
    "JPY": 149.52,
    "BRL": 5.12,
    "CNY": 7.24
  }
}
```

### Convert Currency

```bash
curl -X GET "https://currency-exchange-api.t-mizuno27.workers.dev/convert?from=USD&to=EUR&amount=100" \
  -H "X-RapidAPI-Key: YOUR_KEY"
```

```json
{
  "from": "USD",
  "to": "EUR",
  "amount": 100,
  "result": 92.34,
  "rate": 0.9234,
  "date": "2026-03-20"
}
```

### Historical Rates

```bash
curl -X GET "https://currency-exchange-api.t-mizuno27.workers.dev/historical?base=USD&date=2025-01-15" \
  -H "X-RapidAPI-Key: YOUR_KEY"
```

### List All Currencies

```bash
curl -X GET "https://currency-exchange-api.t-mizuno27.workers.dev/currencies"
```

### Python Example

```python
import requests

url = "https://currency-exchange-api.p.rapidapi.com/convert"
params = {"from": "USD", "to": "JPY", "amount": 1000}
headers = {
    "X-RapidAPI-Key": "YOUR_KEY",
    "X-RapidAPI-Host": "currency-exchange-api.p.rapidapi.com"
}

response = requests.get(url, headers=headers, params=params)
data = response.json()
print(f"${params['amount']} USD = {data['result']} JPY")
```

### Node.js Example

```javascript
const axios = require("axios");

const { data } = await axios.get(
  "https://currency-exchange-api.p.rapidapi.com/convert",
  {
    params: { from: "USD", to: "EUR", amount: 100 },
    headers: {
      "X-RapidAPI-Key": "YOUR_KEY",
      "X-RapidAPI-Host": "currency-exchange-api.p.rapidapi.com",
    },
  }
);

console.log(`$100 USD = ${data.result} EUR`);
```

## API Reference

### `GET /rates`
| Parameter | Required | Default | Description |
|-----------|----------|---------|-------------|
| `base` | No | USD | Base currency (ISO 4217) |

### `GET /convert`
| Parameter | Required | Description |
|-----------|----------|-------------|
| `from` | Yes | Source currency code |
| `to` | Yes | Target currency code |
| `amount` | Yes | Amount to convert |

### `GET /currencies`
List all supported currencies with full names. No parameters.

### `GET /historical`
| Parameter | Required | Default | Description |
|-----------|----------|---------|-------------|
| `base` | No | USD | Base currency code |
| `date` | Yes | -- | Date in YYYY-MM-DD format (back to 1999-01-04) |

## Supported Currencies

AUD, BGN, BRL, CAD, CHF, CNY, CZK, DKK, EUR, GBP, HKD, HUF, IDR, ILS, INR, ISK, JPY, KRW, MXN, MYR, NOK, NZD, PHP, PLN, RON, SEK, SGD, THB, TRY, USD, ZAR

## Pricing

| Plan | Price | Requests/mo | Rate Limit |
|------|-------|-------------|------------|
| Basic (FREE) | $0 | 500 | 1 req/sec |
| Pro | $5.99 | 50,000 | 10 req/sec |
| Ultra | $14.99 | 500,000 | 50 req/sec |

## Alternative To

A free alternative to Fixer.io, ExchangeRate-API, and Open Exchange Rates. Get ECB-sourced exchange rates with historical data and currency conversion without per-request billing.

## Keywords

`currency exchange api`, `exchange rate api`, `currency converter api`, `fx rates api`, `ecb exchange rates`, `historical exchange rates`, `free currency api`, `currency conversion`, `forex api`, `real-time exchange rates`

## FAQ

**Q: How often are exchange rates updated?**
A: ECB publishes rates once per business day around 16:00 CET. Rates are cached for 1 hour at Cloudflare edge.

**Q: Can I use any base currency on the free tier?**
A: Yes. Unlike Fixer.io (EUR only) and Open Exchange Rates (USD only) on their free tiers, this API supports any base currency on all plans.

**Q: How far back do historical rates go?**
A: Back to January 4, 1999, when the Euro was introduced and ECB started publishing rates.

**Q: Are cryptocurrency rates included?**
A: No. This API focuses on fiat currencies from the ECB. For crypto data, see our Crypto Market Data API.

## Development

```bash
npm install
npm run dev      # Local development
npm run deploy   # Deploy to Cloudflare
```
