// CoinPaprika API wrapper (free, no API key required)
const BASE_URL = 'https://api.coinpaprika.com/v1';

const CACHE_TTLS = {
  price: 60,
  coin: 300,
  markets: 60,
  search: 300,
  trending: 600,
  history: 3600,
  exchanges: 600,
  global: 600,
};

async function cachedFetch(url, cacheTtl) {
  const cache = caches.default;
  const cacheKey = new Request(url, { method: 'GET' });

  let response = await cache.match(cacheKey);
  if (response) return response;

  response = await fetch(url, {
    headers: { 'Accept': 'application/json' },
  });

  if (!response.ok) {
    const status = response.status;
    if (status === 429) {
      const stale = await cache.match(cacheKey);
      if (stale) return stale;
      throw new Error('Rate limit exceeded. Please try again later.');
    }
    throw new Error(`Upstream API error: ${status}`);
  }

  const responseToCache = new Response(response.body, response);
  responseToCache.headers.set('Cache-Control', `public, max-age=${cacheTtl}`);
  await cache.put(cacheKey, responseToCache.clone());

  return responseToCache;
}

async function getPrice(ids, vsCurrencies) {
  // CoinPaprika uses coin IDs like "btc-bitcoin", "eth-ethereum"
  // We accept both formats and also simple names
  const idList = ids.split(',').map(s => s.trim());
  const currencies = vsCurrencies.split(',').map(s => s.trim().toLowerCase());

  const data = {};
  for (const id of idList) {
    try {
      const coinId = await resolveId(id);
      const url = `${BASE_URL}/tickers/${coinId}`;
      const res = await cachedFetch(url, CACHE_TTLS.price);
      const raw = await res.json();

      const coinData = {};
      for (const cur of currencies) {
        const quote = raw.quotes?.[cur.toUpperCase()];
        if (quote) {
          coinData[cur] = quote.price;
          coinData[`${cur}_market_cap`] = quote.market_cap;
          coinData[`${cur}_24h_vol`] = quote.volume_24h;
          coinData[`${cur}_24h_change`] = quote.percent_change_24h;
        }
      }
      data[raw.symbol?.toLowerCase() || id] = coinData;
    } catch (e) {
      data[id] = { error: e.message };
    }
  }
  return data;
}

// Map common names to CoinPaprika IDs
const ID_MAP = {
  bitcoin: 'btc-bitcoin', btc: 'btc-bitcoin',
  ethereum: 'eth-ethereum', eth: 'eth-ethereum',
  solana: 'sol-solana', sol: 'sol-solana',
  cardano: 'ada-cardano', ada: 'ada-cardano',
  dogecoin: 'doge-dogecoin', doge: 'doge-dogecoin',
  polkadot: 'dot-polkadot', dot: 'dot-polkadot',
  ripple: 'xrp-xrp', xrp: 'xrp-xrp',
  litecoin: 'ltc-litecoin', ltc: 'ltc-litecoin',
  avalanche: 'avax-avalanche', avax: 'avax-avalanche',
  chainlink: 'link-chainlink', link: 'link-chainlink',
  polygon: 'matic-polygon', matic: 'matic-polygon',
  tether: 'usdt-tether', usdt: 'usdt-tether',
  'usd-coin': 'usdc-usd-coin', usdc: 'usdc-usd-coin',
  'binance-coin': 'bnb-binance-coin', bnb: 'bnb-binance-coin',
  tron: 'trx-tron', trx: 'trx-tron',
};

async function resolveId(input) {
  const lower = input.toLowerCase();
  if (ID_MAP[lower]) return ID_MAP[lower];
  // If it looks like a CoinPaprika ID already (has a dash)
  if (lower.includes('-')) return lower;
  // Try to search
  return lower;
}

async function getCoin(id) {
  const coinId = await resolveId(id);
  const [coinRes, tickerRes] = await Promise.all([
    cachedFetch(`${BASE_URL}/coins/${coinId}`, CACHE_TTLS.coin),
    cachedFetch(`${BASE_URL}/tickers/${coinId}`, CACHE_TTLS.price),
  ]);
  const coin = await coinRes.json();
  const ticker = await tickerRes.json();
  const usd = ticker.quotes?.USD || {};

  return {
    id: coin.id,
    symbol: coin.symbol,
    name: coin.name,
    image: coin.logo,
    description: coin.description?.substring(0, 500),
    market_cap_rank: coin.rank,
    market_data: {
      current_price: { usd: usd.price },
      market_cap: { usd: usd.market_cap },
      total_volume: { usd: usd.volume_24h },
      high_24h: null,
      low_24h: null,
      price_change_24h: usd.price,
      price_change_percentage_24h: usd.percent_change_24h,
      price_change_percentage_7d: usd.percent_change_7d,
      price_change_percentage_30d: usd.percent_change_30d,
      ath: { usd: usd.ath_price },
      ath_date: { usd: usd.ath_date },
      circulating_supply: ticker.circulating_supply,
      total_supply: ticker.total_supply,
      max_supply: ticker.max_supply,
    },
    links: {
      homepage: coin.links?.website?.[0],
      blockchain_site: coin.links?.explorer?.slice(0, 3),
      subreddit: coin.links?.reddit?.[0],
      twitter: coin.links?.twitter?.[0],
    },
    started_at: coin.started_at,
    last_updated: ticker.last_updated,
  };
}

async function searchCoins(query) {
  const url = `${BASE_URL}/search?q=${encodeURIComponent(query)}&limit=20`;
  const res = await cachedFetch(url, CACHE_TTLS.search);
  const raw = await res.json();

  return {
    coins: (raw.currencies || []).slice(0, 20).map(c => ({
      id: c.id,
      name: c.name,
      symbol: c.symbol,
      market_cap_rank: c.rank,
    })),
  };
}

async function getTrending() {
  // CoinPaprika doesn't have a trending endpoint, use top movers from tickers
  const url = `${BASE_URL}/tickers?limit=100`;
  const res = await cachedFetch(url, CACHE_TTLS.trending);
  const raw = await res.json();

  // Sort by 24h change to find trending
  const sorted = (raw || [])
    .filter(c => c.quotes?.USD?.percent_change_24h != null)
    .sort((a, b) => Math.abs(b.quotes.USD.percent_change_24h) - Math.abs(a.quotes.USD.percent_change_24h))
    .slice(0, 15);

  return {
    coins: sorted.map(c => ({
      id: c.id,
      name: c.name,
      symbol: c.symbol,
      market_cap_rank: c.rank,
      price_usd: c.quotes.USD.price,
      change_24h: c.quotes.USD.percent_change_24h,
    })),
  };
}

async function getMarkets(vsCurrency = 'usd', perPage = 100, page = 1) {
  perPage = Math.min(Math.max(1, perPage), 250);
  page = Math.max(1, page);
  const url = `${BASE_URL}/tickers?limit=${perPage}&page=${page}`;
  const res = await cachedFetch(url, CACHE_TTLS.markets);
  const raw = await res.json();

  const cur = vsCurrency.toUpperCase();
  return {
    coins: (raw || []).map(c => {
      const q = c.quotes?.[cur] || c.quotes?.USD || {};
      return {
        id: c.id,
        symbol: c.symbol,
        name: c.name,
        current_price: q.price,
        market_cap: q.market_cap,
        market_cap_rank: c.rank,
        total_volume: q.volume_24h,
        price_change_percentage_24h: q.percent_change_24h,
        price_change_percentage_7d: q.percent_change_7d,
        circulating_supply: c.circulating_supply,
        total_supply: c.total_supply,
        max_supply: c.max_supply,
      };
    }),
    pagination: { page, per_page: perPage, vs_currency: vsCurrency },
  };
}

async function getHistory(id, date) {
  const coinId = await resolveId(id);
  // CoinPaprika historical tickers: /tickers/{coin_id}/historical?start=DATE&interval=1d&limit=1
  const url = `${BASE_URL}/tickers/${coinId}/historical?start=${date}&interval=1d&limit=1`;
  const res = await cachedFetch(url, CACHE_TTLS.history);
  const raw = await res.json();

  const entry = raw?.[0];
  return {
    id: coinId,
    date,
    market_data: entry ? {
      price: entry.price,
      volume_24h: entry.volume_24h,
      market_cap: entry.market_cap,
      timestamp: entry.timestamp,
    } : null,
  };
}

async function getExchanges() {
  const url = `${BASE_URL}/exchanges?limit=50`;
  const res = await cachedFetch(url, CACHE_TTLS.exchanges);
  const raw = await res.json();

  return {
    exchanges: (raw || []).slice(0, 50).map(e => ({
      id: e.id,
      name: e.name,
      description: e.description?.substring(0, 200),
      active: e.active,
      website: e.links?.website?.[0],
      adjusted_volume_24h: e.adjusted_volume_24h_share,
      currencies: e.currencies,
      markets: e.markets,
    })),
  };
}

async function getGlobal() {
  const url = `${BASE_URL}/global`;
  const res = await cachedFetch(url, CACHE_TTLS.global);
  const raw = await res.json();

  return {
    active_cryptocurrencies: raw.cryptocurrencies_number,
    markets: raw.market_cap_ath_value,
    total_market_cap_usd: raw.market_cap_usd,
    total_volume_24h_usd: raw.volume_24h_usd,
    bitcoin_dominance: raw.bitcoin_dominance_percentage,
    market_cap_change_24h: raw.market_cap_change_24h,
    last_updated: raw.last_updated,
  };
}

export { getPrice, getCoin, searchCoins, getTrending, getMarkets, getHistory, getExchanges, getGlobal, CACHE_TTLS };
