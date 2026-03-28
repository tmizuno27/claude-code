# Free Weather API - Forecast, Current Conditions, Historical Data

> **Free tier: 500 requests/month** | Open-Meteo powered weather data -- no API key for data source

Get current weather, hourly/daily forecasts, and historical weather data for any location. Powered by Open-Meteo (free, open-source) and deployed on Cloudflare Workers.

## Getting Started in 30 Seconds

1. Subscribe on [RapidAPI](https://rapidapi.com/miccho27-5OJaGGbBiO/api/weather-api) (free plan available)
2. Copy your API key
3. Get your first weather forecast:

```bash
curl -X GET "https://weather-api.p.rapidapi.com/current?city=Tokyo" \
  -H "X-RapidAPI-Key: YOUR_KEY" \
  -H "X-RapidAPI-Host: weather-api.p.rapidapi.com"
```

## How It Compares

| Feature | This API | OpenWeatherMap | WeatherAPI | AccuWeather |
|---------|----------|---------------|------------|-------------|
| Free tier | 500 req/mo | 1,000 req/day | 1M req/mo | 50 req/day |
| Pro pricing | $5.99/50K | $40/mo | $8/mo | Custom |
| Current weather | Yes | Yes | Yes | Yes |
| Hourly forecast | Yes (48h) | Yes (48h, paid) | Yes (3d) | Yes (12h) |
| Daily forecast | Yes (7d) | Yes (7d) | Yes (3d free) | Yes (5d) |
| Historical data | Yes | Yes (paid) | Yes (paid) | Yes (paid) |
| Geocoding | Yes (city name) | Yes | Yes | Yes |
| Data source | Open-Meteo (ECMWF, NOAA) | Proprietary | Proprietary | Proprietary |
| No upstream API key | Yes | No | No | No |

## Why Choose This Weather API?

- **Open-Meteo data** -- accurate weather from NOAA, ECMWF, DWD, and other national agencies
- **No upstream API key** -- Open-Meteo is fully free and open-source
- **Current + forecast** -- current conditions, hourly (48h), and daily (7d) forecasts
- **Historical data** -- access past weather data for any date and location
- **Geocoding** -- search by city name or coordinates
- **Free tier** -- 500 requests/month at $0

## Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/current` | GET | Current weather conditions |
| `/forecast` | GET | Daily forecast (up to 7 days) |
| `/hourly` | GET | Hourly forecast (up to 48 hours) |
| `/geocode` | GET | City name to coordinates lookup |
| `/history` | GET | Historical weather data for past dates |

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

### Node.js Example

```javascript
const axios = require("axios");

const { data } = await axios.get(
  "https://weather-api.p.rapidapi.com/forecast",
  {
    params: { city: "London", days: 5 },
    headers: {
      "X-RapidAPI-Key": "YOUR_KEY",
      "X-RapidAPI-Host": "weather-api.p.rapidapi.com",
    },
  }
);

data.daily.forEach(day => {
  console.log(`${day.date}: ${day.temp_max}C / ${day.temp_min}C`);
});
```

## FAQ

**Q: How accurate is the weather data?**
A: Data comes from Open-Meteo, which aggregates from ECMWF, NOAA, DWD, and other national weather agencies. Accuracy is comparable to commercial weather APIs.

**Q: Can I get weather for coordinates instead of city names?**
A: Yes. Use `lat` and `lon` parameters instead of `city` on any endpoint.

**Q: How far back does historical data go?**
A: Historical data is available from 1940 to present via Open-Meteo's ERA5 reanalysis dataset.

**Q: What units are used?**
A: Temperature in Celsius, wind speed in km/h, precipitation in mm. Use the `units` parameter to switch to imperial (Fahrenheit, mph, inches).

## Pricing

| Plan | Price | Requests/mo | Rate Limit |
|------|-------|-------------|------------|
| Basic (FREE) | $0 | 500 | 1 req/sec |
| Pro | $5.99 | 50,000 | 10 req/sec |

## Alternative To

A free alternative to OpenWeatherMap API, WeatherAPI, and AccuWeather. Open-source data with no upstream API key costs.


## Also From This Publisher

Build powerful workflows by combining APIs:

| API | Why Combine? |
|-----|-------------|
| **IP Geolocation API** | Auto-detect user location for weather lookup |
| **AI Text API** | Generate weather-based content or notifications |
| **News Aggregator API** | Combine weather with local news |
| **Currency Exchange API** | Travel planning: weather + currency info |

> All APIs include a free tier. Subscribe to one, discover the full toolkit on [our RapidAPI profile](https://rapidapi.com/miccho27-5OJaGGbBiO).

## Keywords

`weather api`, `weather forecast api`, `free weather api`, `current weather api`, `historical weather`, `open meteo api`, `weather data`, `temperature api`, `forecast api`, `openweathermap alternative`
