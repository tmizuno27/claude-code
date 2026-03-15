# Currency Exchange Rate API

Real-time and historical currency exchange rates powered by the European Central Bank (ECB) via the Frankfurter API. Deployed as a Cloudflare Worker.

## Base URL

```
https://currency-exchange-api.t-mizuno27.workers.dev
```

## Endpoints

### GET /rates

Get latest exchange rates for a base currency.

```
GET /rates?base=USD
```

| Parameter | Required | Default | Description |
|-----------|----------|---------|-------------|
| base | No | USD | Base currency code (ISO 4217) |

### GET /convert

Convert an amount between two currencies.

```
GET /convert?from=USD&to=EUR&amount=100
```

| Parameter | Required | Description |
|-----------|----------|-------------|
| from | Yes | Source currency code |
| to | Yes | Target currency code |
| amount | Yes | Amount to convert |

### GET /currencies

List all supported currencies with full names.

```
GET /currencies
```

### GET /historical

Get exchange rates for a specific historical date.

```
GET /historical?base=USD&date=2025-01-15
```

| Parameter | Required | Default | Description |
|-----------|----------|---------|-------------|
| base | No | USD | Base currency code |
| date | Yes | - | Date in YYYY-MM-DD format |

## Supported Currencies

30+ currencies including: AUD, BGN, BRL, CAD, CHF, CNY, CZK, DKK, EUR, GBP, HKD, HUF, IDR, ILS, INR, ISK, JPY, KRW, MXN, MYR, NOK, NZD, PHP, PLN, RON, SEK, SGD, THB, TRY, USD, ZAR.

## Features

- Real-time ECB exchange rates
- Historical rates back to 1999
- 1-hour caching via Cloudflare Cache API
- Rate limiting (60 req/min per IP)
- CORS enabled
- No API key required for the data source

## Development

```bash
npm install
npm run dev      # Local dev server
npm run deploy   # Deploy to Cloudflare
```

## Data Source

[Frankfurter API](https://api.frankfurter.dev) - Free, open-source API for ECB reference rates.
