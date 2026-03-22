# Free Weather API - Forecast, Current Conditions, Historical Data

> **Free tier: 500 requests/month** | Open-Meteo powered weather data -- no API key for data source

Get current weather, hourly/daily forecasts, and historical weather data for any location. Powered by Open-Meteo (free, open-source) and deployed on Cloudflare Workers.

## Why Choose This Weather API?

- **Open-Meteo data** -- accurate weather from NOAA, ECMWF, DWD, and other national agencies
- **No upstream API key** -- Open-Meteo is fully free and open-source
- **Current + forecast** -- current conditions, hourly (48h), and daily (7d) forecasts
- **Historical data** -- access past weather data for any date and location
- **Geocoding** -- search by city name or coordinates
- **Free tier** -- 500 requests/month at $0

## Use Cases

- **Travel apps** -- show weather forecasts for destinations
- **Agriculture** -- historical weather data for crop planning
- **Event planning** -- check weather forecasts for outdoor events
- **IoT dashboards** -- display local weather alongside sensor data
- **Logistics** -- weather-aware route planning and delivery ETAs
- **Energy** -- solar/wind forecast for renewable energy planning

## Quick Start

```bash
curl -X GET "https://weather-api.t-mizuno27.workers.dev/current?city=Tokyo" \
  -H "X-RapidAPI-Key: YOUR_KEY"
```

### Python Example

```python
import requests

url = "https://weather-api.p.rapidapi.com/forecast"
params = {"city": "New York", "days": 7}
headers = {"X-RapidAPI-Key": "YOUR_KEY", "X-RapidAPI-Host": "weather-api.p.rapidapi.com"}

data = requests.get(url, headers=headers, params=params).json()
for day in data["daily"]:
    print(f"{day['date']}: {day['temp_max']}C / {day['temp_min']}C")
```

## Pricing

| Plan | Price | Requests/mo | Rate Limit |
|------|-------|-------------|------------|
| Basic (FREE) | $0 | 500 | 1 req/sec |
| Pro | $5.99 | 50,000 | 10 req/sec |

## Alternative To

A free alternative to OpenWeatherMap API, WeatherAPI, and AccuWeather.

## Keywords

`weather api`, `weather forecast api`, `free weather api`, `current weather api`, `historical weather`, `open meteo api`, `weather data`, `temperature api`, `forecast api`, `openweathermap alternative`
