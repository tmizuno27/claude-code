const WMO_CODES = {
  0: "Clear sky",
  1: "Mainly clear",
  2: "Partly cloudy",
  3: "Overcast",
  45: "Foggy",
  48: "Depositing rime fog",
  51: "Light drizzle",
  53: "Moderate drizzle",
  55: "Dense drizzle",
  56: "Light freezing drizzle",
  57: "Dense freezing drizzle",
  61: "Slight rain",
  63: "Moderate rain",
  65: "Heavy rain",
  66: "Light freezing rain",
  67: "Heavy freezing rain",
  71: "Slight snowfall",
  73: "Moderate snowfall",
  75: "Heavy snowfall",
  77: "Snow grains",
  80: "Slight rain showers",
  81: "Moderate rain showers",
  82: "Violent rain showers",
  85: "Slight snow showers",
  86: "Heavy snow showers",
  95: "Thunderstorm",
  96: "Thunderstorm with slight hail",
  99: "Thunderstorm with heavy hail",
};

const CORS_HEADERS = {
  "Access-Control-Allow-Origin": "*",
  "Access-Control-Allow-Methods": "GET, OPTIONS",
  "Access-Control-Allow-Headers": "Content-Type",
};

const CACHE_TTL = {
  current: 300,
  forecast: 1800,
  hourly: 1800,
  geocode: 86400,
  history: 86400,
};

const RATE_LIMIT_MAX = 30;
const RATE_LIMIT_WINDOW_MS = 60000;
const RATE_LIMIT_MAX_ENTRIES = 5000;

const rateLimitMap = new Map();

function checkRateLimit(ip) {
  const now = Date.now();

  // Size-based cleanup
  if (rateLimitMap.size > RATE_LIMIT_MAX_ENTRIES) {
    const cutoff = now - RATE_LIMIT_WINDOW_MS;
    for (const [key, entry] of rateLimitMap) {
      if (entry.resetAt < cutoff) rateLimitMap.delete(key);
      if (rateLimitMap.size <= RATE_LIMIT_MAX_ENTRIES / 2) break;
    }
  }

  let entry = rateLimitMap.get(ip);
  if (!entry || now > entry.resetAt) {
    entry = { count: 0, resetAt: now + RATE_LIMIT_WINDOW_MS };
    rateLimitMap.set(ip, entry);
  }
  entry.count++;
  if (entry.count > RATE_LIMIT_MAX) {
    return { allowed: false, remaining: 0, resetAt: entry.resetAt };
  }
  return { allowed: true, remaining: RATE_LIMIT_MAX - entry.count, resetAt: entry.resetAt };
}

function jsonResponse(data, status = 200, cacheTtl = 0) {
  const headers = {
    "Content-Type": "application/json",
    ...CORS_HEADERS,
  };
  if (cacheTtl > 0) {
    headers["Cache-Control"] = `public, max-age=${cacheTtl}`;
  }
  return new Response(JSON.stringify(data), { status, headers });
}

function errorResponse(message, status = 400) {
  return jsonResponse({ error: message }, status);
}

function describeWeatherCode(code) {
  return WMO_CODES[code] || "Unknown";
}

function requireCoords(url) {
  const lat = parseFloat(url.searchParams.get("lat"));
  const lon = parseFloat(url.searchParams.get("lon"));
  if (isNaN(lat) || isNaN(lon)) return null;
  if (lat < -90 || lat > 90 || lon < -180 || lon > 180) return null;
  return { lat, lon };
}

async function handleCurrent(url) {
  const coords = requireCoords(url);
  if (!coords) return errorResponse("Valid lat and lon parameters are required");

  const apiUrl = `https://api.open-meteo.com/v1/forecast?latitude=${coords.lat}&longitude=${coords.lon}&current=temperature_2m,relative_humidity_2m,wind_speed_10m,weather_code,is_day&timezone=auto`;
  const res = await fetch(apiUrl);
  if (!res.ok) return errorResponse("Failed to fetch weather data", 502);

  const data = await res.json();
  const c = data.current;

  return jsonResponse({
    latitude: data.latitude,
    longitude: data.longitude,
    timezone: data.timezone,
    current: {
      time: c.time,
      temperature_c: c.temperature_2m,
      relative_humidity_percent: c.relative_humidity_2m,
      wind_speed_kmh: c.wind_speed_10m,
      weather_code: c.weather_code,
      condition: describeWeatherCode(c.weather_code),
      is_day: c.is_day === 1,
    },
  }, 200, CACHE_TTL.current);
}

async function handleForecast(url) {
  const coords = requireCoords(url);
  if (!coords) return errorResponse("Valid lat and lon parameters are required");

  let days = parseInt(url.searchParams.get("days") || "7", 10);
  if (isNaN(days) || days < 1) days = 7;
  if (days > 16) days = 16;

  const apiUrl = `https://api.open-meteo.com/v1/forecast?latitude=${coords.lat}&longitude=${coords.lon}&daily=temperature_2m_max,temperature_2m_min,precipitation_sum,weather_code,wind_speed_10m_max&timezone=auto&forecast_days=${days}`;
  const res = await fetch(apiUrl);
  if (!res.ok) return errorResponse("Failed to fetch forecast data", 502);

  const data = await res.json();
  const d = data.daily;

  const forecast = d.time.map((date, i) => ({
    date,
    temperature_max_c: d.temperature_2m_max[i],
    temperature_min_c: d.temperature_2m_min[i],
    precipitation_mm: d.precipitation_sum[i],
    wind_speed_max_kmh: d.wind_speed_10m_max[i],
    weather_code: d.weather_code[i],
    condition: describeWeatherCode(d.weather_code[i]),
  }));

  return jsonResponse({
    latitude: data.latitude,
    longitude: data.longitude,
    timezone: data.timezone,
    days: forecast.length,
    forecast,
  }, 200, CACHE_TTL.forecast);
}

async function handleHourly(url) {
  const coords = requireCoords(url);
  if (!coords) return errorResponse("Valid lat and lon parameters are required");

  let hours = parseInt(url.searchParams.get("hours") || "24", 10);
  if (isNaN(hours) || hours < 1) hours = 24;
  if (hours > 384) hours = 384;

  const forecastDays = Math.min(Math.ceil(hours / 24), 16);
  const apiUrl = `https://api.open-meteo.com/v1/forecast?latitude=${coords.lat}&longitude=${coords.lon}&hourly=temperature_2m,relative_humidity_2m,precipitation,weather_code,wind_speed_10m&timezone=auto&forecast_days=${forecastDays}`;
  const res = await fetch(apiUrl);
  if (!res.ok) return errorResponse("Failed to fetch hourly data", 502);

  const data = await res.json();
  const h = data.hourly;

  const hourly = h.time.slice(0, hours).map((time, i) => ({
    time,
    temperature_c: h.temperature_2m[i],
    relative_humidity_percent: h.relative_humidity_2m[i],
    precipitation_mm: h.precipitation[i],
    wind_speed_kmh: h.wind_speed_10m[i],
    weather_code: h.weather_code[i],
    condition: describeWeatherCode(h.weather_code[i]),
  }));

  return jsonResponse({
    latitude: data.latitude,
    longitude: data.longitude,
    timezone: data.timezone,
    hours: hourly.length,
    hourly,
  }, 200, CACHE_TTL.hourly);
}

async function handleGeocode(url) {
  const query = url.searchParams.get("q");
  if (!query) return errorResponse("Query parameter q is required");

  const apiUrl = `https://geocoding-api.open-meteo.com/v1/search?name=${encodeURIComponent(query)}&count=5&language=en`;
  const res = await fetch(apiUrl);
  if (!res.ok) return errorResponse("Failed to fetch geocoding data", 502);

  const data = await res.json();
  const results = (data.results || []).map((r) => ({
    name: r.name,
    latitude: r.latitude,
    longitude: r.longitude,
    country: r.country,
    country_code: r.country_code,
    admin1: r.admin1 || null,
    timezone: r.timezone,
    population: r.population || null,
  }));

  return jsonResponse({ query, count: results.length, results }, 200, CACHE_TTL.geocode);
}

async function handleHistory(url) {
  const coords = requireCoords(url);
  if (!coords) return errorResponse("Valid lat and lon parameters are required");

  const start = url.searchParams.get("start");
  const end = url.searchParams.get("end");
  if (!start || !end) return errorResponse("start and end date parameters are required (YYYY-MM-DD)");
  if (!/^\d{4}-\d{2}-\d{2}$/.test(start) || !/^\d{4}-\d{2}-\d{2}$/.test(end)) {
    return errorResponse("Dates must be in YYYY-MM-DD format");
  }

  const apiUrl = `https://archive-api.open-meteo.com/v1/archive?latitude=${coords.lat}&longitude=${coords.lon}&start_date=${start}&end_date=${end}&daily=temperature_2m_max,temperature_2m_min,precipitation_sum&timezone=auto`;
  const res = await fetch(apiUrl);
  if (!res.ok) return errorResponse("Failed to fetch historical data", 502);

  const data = await res.json();
  const d = data.daily;

  const history = d.time.map((date, i) => ({
    date,
    temperature_max_c: d.temperature_2m_max[i],
    temperature_min_c: d.temperature_2m_min[i],
    precipitation_mm: d.precipitation_sum[i],
  }));

  return jsonResponse({
    latitude: data.latitude,
    longitude: data.longitude,
    timezone: data.timezone,
    start_date: start,
    end_date: end,
    days: history.length,
    history,
  }, 200, CACHE_TTL.history);
}

export default {
  async fetch(request) {
    if (request.method === "OPTIONS") {
      return new Response(null, { status: 204, headers: CORS_HEADERS });
    }
    if (request.method !== "GET") {
      return errorResponse("Method not allowed", 405);
    }

    const ip = request.headers.get("CF-Connecting-IP") || "unknown";
    const rl = checkRateLimit(ip);
    if (!rl.allowed) {
      return jsonResponse({ error: "Rate limit exceeded. Max 30 requests per minute." }, 429);
    }

    const url = new URL(request.url);
    const path = url.pathname;

    switch (path) {
      case "/":
        return jsonResponse({
          name: "Weather API",
          version: "1.0.0",
          description: "Free weather data powered by Open-Meteo",
          endpoints: [
            "GET /current?lat={lat}&lon={lon}",
            "GET /forecast?lat={lat}&lon={lon}&days={1-16}",
            "GET /hourly?lat={lat}&lon={lon}&hours={1-384}",
            "GET /geocode?q={city_name}",
            "GET /history?lat={lat}&lon={lon}&start={YYYY-MM-DD}&end={YYYY-MM-DD}",
          ],
        });
      case "/current":
        return handleCurrent(url);
      case "/forecast":
        return handleForecast(url);
      case "/hourly":
        return handleHourly(url);
      case "/geocode":
        return handleGeocode(url);
      case "/history":
        return handleHistory(url);
      default:
        return errorResponse("Not found", 404);
    }
  },
};
