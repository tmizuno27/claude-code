# Free Crypto Data API - Prices, Market Cap, Charts from CoinGecko

> **Free tier: 500 requests/month** | Real-time cryptocurrency data aggregated from CoinGecko

Get real-time cryptocurrency prices, market cap, 24h volume, price changes, and historical chart data for thousands of coins. Powered by CoinGecko's free API with Cloudflare Workers caching.

## Why Choose This Crypto Data API?

- **CoinGecko data** -- reliable, comprehensive cryptocurrency market data
- **10,000+ coins** -- Bitcoin, Ethereum, Solana, and thousands of altcoins
- **Historical charts** -- price history for 1d, 7d, 30d, 90d, 1y time ranges
- **Market overview** -- global market cap, dominance, trending coins
- **Edge-cached** -- fast responses via Cloudflare Workers caching
- **Free tier** -- 500 requests/month at $0

## Use Cases

- **Portfolio trackers** -- display real-time crypto prices and portfolio value
- **Trading bots** -- feed price data into automated trading strategies
- **Fintech apps** -- integrate cryptocurrency data alongside traditional finance
- **Price alerts** -- monitor price changes and trigger notifications
- **Analytics dashboards** -- chart historical price and volume data
- **DeFi apps** -- display token prices in decentralized finance interfaces

## Quick Start

```bash
curl -X GET "https://crypto-data-api.t-mizuno27.workers.dev/price?coin=bitcoin" \
  -H "X-RapidAPI-Key: YOUR_KEY"
```

### Python Example

```python
import requests

url = "https://crypto-data-api.p.rapidapi.com/price"
params = {"coin": "bitcoin"}
headers = {"X-RapidAPI-Key": "YOUR_KEY", "X-RapidAPI-Host": "crypto-data-api.p.rapidapi.com"}

data = requests.get(url, headers=headers, params=params).json()
print(f"BTC: ${data['price_usd']:,.2f} | 24h: {data['change_24h']}%")
```

## Pricing

| Plan | Price | Requests/mo | Rate Limit |
|------|-------|-------------|------------|
| Basic (FREE) | $0 | 500 | 1 req/sec |
| Pro | $9.99 | 50,000 | 10 req/sec |

## Alternative To

A free alternative to CoinMarketCap API, CoinGecko Pro, and CryptoCompare.

## Keywords

`crypto api`, `cryptocurrency api`, `bitcoin price api`, `crypto market data`, `coin prices api`, `free crypto api`, `defi api`, `crypto chart api`, `market cap api`, `coingecko alternative`
