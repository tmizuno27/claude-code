# Free Crypto Data API - Real-Time Prices, Market Cap, Charts

> **Free tier: 500 requests/month** | Real-time cryptocurrency data with edge caching

Get real-time cryptocurrency prices, market cap, 24h volume, price changes, and historical chart data for 10,000+ coins. Powered by CoinCap API with Cloudflare Workers edge caching for sub-100ms responses.

## Getting Started in 30 Seconds

1. Subscribe on [RapidAPI](https://rapidapi.com/miccho27-5OJaGGbBiO/api/crypto-data-api) (free plan available)
2. Copy your API key
3. Get Bitcoin's price:

```bash
curl -X GET "https://crypto-data-api.p.rapidapi.com/price?ids=bitcoin&vs=usd" \
  -H "X-RapidAPI-Key: YOUR_KEY" \
  -H "X-RapidAPI-Host: crypto-data-api.p.rapidapi.com"
```

## Why Choose This Crypto Data API?

- **10,000+ coins** -- Bitcoin, Ethereum, Solana, and thousands of altcoins
- **8 endpoints** -- prices, coin details, search, trending, markets, history, exchanges, global stats
- **Edge-cached** -- sub-100ms responses via Cloudflare Workers (300+ cities)
- **No rate limit surprises** -- flat-rate plans, no per-request billing
- **No CoinGecko Pro required** -- access comprehensive data through our proxy
- **Free tier** -- 500 requests/month at $0

## How It Compares

| Feature | This API | CoinGecko Pro | CoinMarketCap | CryptoCompare |
|---------|----------|---------------|---------------|---------------|
| Free tier | 500 req/mo | 30 req/min (demo) | 333 req/day | 100K req/mo |
| Price | $0-$9.99 | $129/mo | $79/mo | $49/mo |
| Coins covered | 10,000+ | 10,000+ | 10,000+ | 5,000+ |
| Historical data | Yes | Yes | Paid only | Paid only |
| Edge caching | Yes (CF Workers) | No | No | No |
| Setup complexity | RapidAPI key only | API key + plan | API key + plan | API key + plan |

## Endpoints

### GET /price -- Current Prices

Get prices for one or more coins in any fiat currency.

```bash
# Single coin
curl "https://crypto-data-api.p.rapidapi.com/price?ids=bitcoin&vs=usd" \
  -H "X-RapidAPI-Key: YOUR_KEY" \
  -H "X-RapidAPI-Host: crypto-data-api.p.rapidapi.com"

# Multiple coins
curl "https://crypto-data-api.p.rapidapi.com/price?ids=bitcoin,ethereum,solana&vs=usd" \
  -H "X-RapidAPI-Key: YOUR_KEY" \
  -H "X-RapidAPI-Host: crypto-data-api.p.rapidapi.com"
```

**Response:**
```json
{
  "bitcoin": {
    "price_usd": 67432.15,
    "market_cap": 1324567890123,
    "volume_24h": 28456789012,
    "change_24h": 2.34
  }
}
```

### GET /coin/:id -- Coin Details

Detailed information for a specific coin including description, links, and market data.

```bash
curl "https://crypto-data-api.p.rapidapi.com/coin/ethereum" \
  -H "X-RapidAPI-Key: YOUR_KEY" \
  -H "X-RapidAPI-Host: crypto-data-api.p.rapidapi.com"
```

### GET /search -- Search Coins

Search coins by name or symbol.

```bash
curl "https://crypto-data-api.p.rapidapi.com/search?q=solana" \
  -H "X-RapidAPI-Key: YOUR_KEY" \
  -H "X-RapidAPI-Host: crypto-data-api.p.rapidapi.com"
```

### GET /trending -- Trending Coins

Get currently trending coins based on search activity.

```bash
curl "https://crypto-data-api.p.rapidapi.com/trending" \
  -H "X-RapidAPI-Key: YOUR_KEY" \
  -H "X-RapidAPI-Host: crypto-data-api.p.rapidapi.com"
```

### GET /markets -- Market Listings

Paginated market listings sorted by market cap.

```bash
curl "https://crypto-data-api.p.rapidapi.com/markets?vs=usd&per_page=100&page=1" \
  -H "X-RapidAPI-Key: YOUR_KEY" \
  -H "X-RapidAPI-Host: crypto-data-api.p.rapidapi.com"
```

### GET /history -- Historical Price

Get price on a specific date.

```bash
curl "https://crypto-data-api.p.rapidapi.com/history?id=bitcoin&date=2025-01-01" \
  -H "X-RapidAPI-Key: YOUR_KEY" \
  -H "X-RapidAPI-Host: crypto-data-api.p.rapidapi.com"
```

### GET /exchanges -- Top Exchanges

List top cryptocurrency exchanges.

```bash
curl "https://crypto-data-api.p.rapidapi.com/exchanges" \
  -H "X-RapidAPI-Key: YOUR_KEY" \
  -H "X-RapidAPI-Host: crypto-data-api.p.rapidapi.com"
```

### GET /global -- Global Market Stats

Total market cap, BTC dominance, and other global metrics.

```bash
curl "https://crypto-data-api.p.rapidapi.com/global" \
  -H "X-RapidAPI-Key: YOUR_KEY" \
  -H "X-RapidAPI-Host: crypto-data-api.p.rapidapi.com"
```

## Use Cases

- **Portfolio trackers** -- display real-time crypto prices and portfolio value
- **Trading bots** -- feed price data into automated trading strategies
- **Fintech apps** -- integrate cryptocurrency data alongside traditional finance
- **Price alerts** -- monitor price changes and trigger notifications
- **Analytics dashboards** -- chart historical price and volume data
- **DeFi apps** -- display token prices in decentralized finance interfaces
- **Telegram/Discord bots** -- real-time price commands for community channels
- **Mobile apps** -- lightweight crypto price widget

## Code Examples

### Python -- Portfolio Tracker

```python
import requests

url = "https://crypto-data-api.p.rapidapi.com/price"
params = {"ids": "bitcoin,ethereum,solana", "vs": "usd"}
headers = {
    "X-RapidAPI-Key": "YOUR_KEY",
    "X-RapidAPI-Host": "crypto-data-api.p.rapidapi.com"
}

data = requests.get(url, headers=headers, params=params).json()

portfolio = {"bitcoin": 0.5, "ethereum": 3.0, "solana": 50.0}
total = 0
for coin, amount in portfolio.items():
    price = data[coin]["price_usd"]
    value = price * amount
    total += value
    print(f"{coin}: {amount} x ${price:,.2f} = ${value:,.2f}")
print(f"\nTotal: ${total:,.2f}")
```

### Node.js -- Price Alert Bot

```javascript
const axios = require("axios");

async function checkPrice(coin, threshold) {
  const { data } = await axios.get(
    "https://crypto-data-api.p.rapidapi.com/price",
    {
      params: { ids: coin, vs: "usd" },
      headers: {
        "X-RapidAPI-Key": "YOUR_KEY",
        "X-RapidAPI-Host": "crypto-data-api.p.rapidapi.com",
      },
    }
  );

  const price = data[coin].price_usd;
  const change = data[coin].change_24h;

  if (Math.abs(change) > threshold) {
    console.log(`ALERT: ${coin} moved ${change}% in 24h (now $${price})`);
  }
}

checkPrice("bitcoin", 5); // Alert if BTC moves more than 5%
```

### JavaScript (Fetch) -- Trending Coins Widget

```javascript
const response = await fetch("https://crypto-data-api.p.rapidapi.com/trending", {
  headers: {
    "X-RapidAPI-Key": "YOUR_KEY",
    "X-RapidAPI-Host": "crypto-data-api.p.rapidapi.com"
  }
});

const trending = await response.json();
trending.coins.forEach(coin => {
  console.log(`${coin.name} (${coin.symbol}) - Rank #${coin.market_cap_rank}`);
});
```

## Pricing

| Plan | Price | Requests/mo | Rate Limit | Best For |
|------|-------|-------------|------------|----------|
| Basic (FREE) | $0 | 500 | 1 req/sec | Prototyping, hobby projects |
| Pro | $9.99 | 50,000 | 10 req/sec | Production apps, bots |

## FAQ

**Q: How often is price data updated?**
A: Price data is cached for 60 seconds at the edge. You get near-real-time data with excellent performance.

**Q: What coin IDs should I use?**
A: Use CoinGecko-style IDs (e.g., "bitcoin", "ethereum", "solana"). Use the /search endpoint to find the correct ID.

**Q: Can I get prices in EUR, GBP, JPY?**
A: Yes. Use the `vs` parameter: `/price?ids=bitcoin&vs=eur`

**Q: Is there a WebSocket/streaming option?**
A: Not currently. For real-time streaming, poll the /price endpoint at your desired interval.

## Alternative To

A free, developer-friendly alternative to CoinMarketCap API, CoinGecko Pro, and CryptoCompare. No complex setup, no $50+/month subscription, no credit card required for free tier.


## Also From This Publisher

Build powerful workflows by combining APIs:

| API | Why Combine? |
|-----|-------------|
| **Currency Exchange API** | Combine crypto + fiat rates for full coverage |
| **Trends API** | Track which coins are trending on social media |
| **News Aggregator API** | Get crypto news alongside price data |
| **AI Text API** | Generate market analysis from crypto data |

> All APIs include a free tier. Subscribe to one, discover the full toolkit on [our RapidAPI profile](https://rapidapi.com/miccho27-5OJaGGbBiO).

## Keywords

`crypto api`, `cryptocurrency api`, `bitcoin price api`, `crypto market data`, `coin prices api`, `free crypto api`, `defi api`, `crypto chart api`, `market cap api`, `coingecko alternative`, `coinmarketcap alternative`, `real-time crypto prices`, `crypto trading api`
