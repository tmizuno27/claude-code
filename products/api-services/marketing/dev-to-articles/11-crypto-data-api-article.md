---
title: Free Crypto API — Real-Time Bitcoin & Ethereum Prices Without CoinMarketCap's $79/Month Plan
tags: api, webdev, javascript, python
published: false
---

CoinMarketCap's free tier gives you 10,000 credits/month — sounds generous until you realize a single `/v1/cryptocurrency/listings/latest` call costs 1 credit per coin returned. Need top 100 coins? That's 100 credits per call, or ~3 calls per hour before you hit the wall.

I built a lightweight alternative on Cloudflare Workers that aggregates CoinGecko's public data with edge caching. Here's what it does and how to use it.

## What You Get (Free Tier: 500 requests/month)

- Real-time prices for Bitcoin, Ethereum, and 10,000+ altcoins
- Market cap, 24h volume, price change percentages
- Trending coins (what's hot right now)
- Historical price data by date
- Exchange listings
- Global market statistics
- Sub-100ms latency via Cloudflare's 300+ edge locations

## Quick Start

### Python — Build a Portfolio Tracker

```python
import requests

API_KEY = "your-rapidapi-key"
BASE_URL = "https://crypto-data-api1.p.rapidapi.com"

headers = {
    "x-rapidapi-key": API_KEY,
    "x-rapidapi-host": "crypto-data-api1.p.rapidapi.com"
}

# Get prices for multiple coins at once
response = requests.get(
    f"{BASE_URL}/price",
    headers=headers,
    params={
        "ids": "bitcoin,ethereum,solana,cardano",
        "vs": "usd"
    }
)

prices = response.json()
print(prices)
# {
#   "bitcoin": {"usd": 67432.50},
#   "ethereum": {"usd": 3521.80},
#   "solana": {"usd": 178.40},
#   "cardano": {"usd": 0.612}
# }

# Calculate portfolio value
portfolio = {
    "bitcoin": 0.5,
    "ethereum": 3.2,
    "solana": 50,
    "cardano": 1000
}

total = sum(
    portfolio[coin] * prices[coin]["usd"]
    for coin in portfolio
    if coin in prices
)
print(f"Portfolio value: ${total:,.2f}")
```

### JavaScript — Real-Time Price Ticker

```javascript
const headers = {
  'x-rapidapi-key': 'your-rapidapi-key',
  'x-rapidapi-host': 'crypto-data-api1.p.rapidapi.com'
};

// Fetch trending coins
async function getTrendingCoins() {
  const res = await fetch(
    'https://crypto-data-api1.p.rapidapi.com/trending',
    { headers }
  );
  const data = await res.json();
  return data.coins?.slice(0, 5) || [];
}

// Get market overview
async function getMarketOverview() {
  const res = await fetch(
    'https://crypto-data-api1.p.rapidapi.com/global',
    { headers }
  );
  return res.json();
}

// Build a simple dashboard
async function updateDashboard() {
  const [trending, global] = await Promise.all([
    getTrendingCoins(),
    getMarketOverview()
  ]);

  console.log('=== Crypto Market Dashboard ===');
  console.log(`Total Market Cap: $${(global.data?.total_market_cap?.usd / 1e12).toFixed(2)}T`);
  console.log(`BTC Dominance: ${global.data?.market_cap_percentage?.btc?.toFixed(1)}%`);
  console.log('\nTrending:');
  trending.forEach(coin => {
    console.log(`  ${coin.item.symbol}: #${coin.item.market_cap_rank}`);
  });
}

updateDashboard();
```

## All Endpoints

| Method | Path | Description |
|--------|------|-------------|
| `GET` | `/price` | Current prices for one or more coins |
| `GET` | `/coin/:id` | Full details (supply, ATH, description) |
| `GET` | `/search` | Search by name or ticker symbol |
| `GET` | `/trending` | Top trending coins right now |
| `GET` | `/markets` | Paginated market listings |
| `GET` | `/history` | Historical price on a specific date |
| `GET` | `/exchanges` | Top exchanges by volume |
| `GET` | `/global` | Total market cap, dominance, stats |

## Practical Use Case: Crypto Alert Bot

```python
import requests
import time

API_KEY = "your-rapidapi-key"
headers = {
    "x-rapidapi-key": API_KEY,
    "x-rapidapi-host": "crypto-data-api1.p.rapidapi.com"
}

ALERT_THRESHOLDS = {
    "bitcoin": {"above": 70000, "below": 60000},
    "ethereum": {"above": 4000, "below": 3000},
}

def check_alerts():
    ids = ",".join(ALERT_THRESHOLDS.keys())
    r = requests.get(
        "https://crypto-data-api1.p.rapidapi.com/price",
        headers=headers,
        params={"ids": ids, "vs": "usd"}
    )
    prices = r.json()

    for coin, thresholds in ALERT_THRESHOLDS.items():
        price = prices.get(coin, {}).get("usd", 0)
        if price > thresholds["above"]:
            print(f"🚀 {coin.upper()} ABOVE ${thresholds['above']:,}: ${price:,.2f}")
        elif price < thresholds["below"]:
            print(f"⚠️  {coin.upper()} BELOW ${thresholds['below']:,}: ${price:,.2f}")
        else:
            print(f"  {coin.upper()}: ${price:,.2f} (normal range)")

# Check every 5 minutes
while True:
    check_alerts()
    time.sleep(300)
```

## Pricing

| Plan | Price | Requests/month | Rate Limit |
|------|-------|----------------|------------|
| Basic (FREE) | $0 | 500 | 1 req/sec |
| Pro | $5.99 | 50,000 | 10 req/sec |
| Ultra | $14.99 | 500,000 | 50 req/sec |

**Available on RapidAPI:** [Crypto Data API](https://rapidapi.com/miccho27-RNuiryMxge/api/crypto-data-api1)

## Why Not Just Use CoinGecko Directly?

You can — but:
- CoinGecko's free API has aggressive rate limits and frequent 429 errors
- No guaranteed uptime SLA on the free tier
- This API adds edge caching, so repeated requests (e.g., price tickers) don't burn your quota

For high-frequency use cases like trading bots or real-time dashboards, the caching layer alone is worth it.

## See All My Free APIs

I've built 24 free APIs on Cloudflare Workers covering crypto, news, SEO, AI translation, URL shortening, and more.

[Browse all 24 APIs on RapidAPI →](https://rapidapi.com/user/miccho27-RNuiryMxge)

---

*Questions or feature requests? Drop a comment below.*
