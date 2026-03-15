# Weather API

Free weather data API powered by [Open-Meteo](https://open-meteo.com/), deployed on Cloudflare Workers. No API key required.

## Endpoints

| Method | Path | Description |
|--------|------|-------------|
| GET | `/` | API info |
| GET | `/current?lat={lat}&lon={lon}` | Current weather |
| GET | `/forecast?lat={lat}&lon={lon}&days={1-16}` | Daily forecast |
| GET | `/hourly?lat={lat}&lon={lon}&hours={1-384}` | Hourly forecast |
| GET | `/geocode?q={city_name}` | City name to coordinates |
| GET | `/history?lat={lat}&lon={lon}&start={YYYY-MM-DD}&end={YYYY-MM-DD}` | Historical data |

## Examples

```bash
# Current weather in Tokyo
curl "https://weather-api.YOUR.workers.dev/current?lat=35.68&lon=139.76"

# 7-day forecast for Asuncion
curl "https://weather-api.YOUR.workers.dev/forecast?lat=-25.26&lon=-57.58&days=7"

# Find coordinates for a city
curl "https://weather-api.YOUR.workers.dev/geocode?q=Tokyo"

# Historical data
curl "https://weather-api.YOUR.workers.dev/history?lat=35.68&lon=139.76&start=2025-01-01&end=2025-01-07"
```

## Features

- WMO weather code to human-readable description mapping
- CORS enabled
- Rate limiting: 30 requests/minute per IP
- Cache: current 5min, forecast 30min, history 24h

## Setup

```bash
npm install
npm run dev      # Local development
npm run deploy   # Deploy to Cloudflare Workers
```
