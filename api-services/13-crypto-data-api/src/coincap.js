// CoinCap API v2 wrapper (free, no API key required)
const BASE_URL = 'https://api.coincap.io/v2';

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
  const idList = ids.split(',').map(s => s.trim().toLowerCase());
  // CoinCap only provides USD prices; we'll note that in the response
  const currencies = vsCurrencies.split(',').map(s => s.trim().toLowerCase());

  // Fetch all requested assets in one call
  const url = `${BASE_URL}/assets?ids=${idList.join(',')}`;
  const res = await cachedFetch(url, CACHE_TTLS.price);
  const raw = await res.json();

  const data = {};
  for (const asset of (raw.data || [])) {
    const key = asset.id;
    const coinData = {};
    for (const cur of currencies) {
      if (cur === 'usd') {
        coinData.usd = parseFloat(asset.priceUsd) || 0;
        coinData.usd_market_cap = parseFloat(asset.marketCapUsd) || 0;
        coinData.usd_24h_vol = parseFloat(asset.volumeUsd24Hr) || 0;
        coinData.usd_24h_change = parseFloat(asset.changePercent24Hr) || 0;
      } else {
        // CoinCap only provides USD; note limitation
        coinData[cur] = null;
        coinData[`${cur}_note`] = 'CoinCap API only provides USD prices';
      }
    }
    data[key] = coinData;
  }

  // Mark any IDs not found
  for (const id of idList) {
    if (!data[id]) {
      data[id] = { error: `Coin '${id}' not found` };
    }
  }

  return data;
}

async function getCoin(id) {
  const url = `${BASE_URL}/assets/${encodeURIComponent(id.toLowerCase())}`;
  const res = await cachedFetch(url, CACHE_TTLS.coin);
  const raw = await res.json();
  const a = raw.data;

  if (!a) throw new Error(`Coin '${id}' not found`);

  return {
    id: a.id,
    symbol: a.symbol?.toLowerCase(),
    name: a.name,
    image: null,
    description: null,
    market_cap_rank: parseInt(a.rank) || null,
    market_data: {
      current_price: { usd: parseFloat(a.priceUsd) || 0 },
      market_cap: { usd: parseFloat(a.marketCapUsd) || 0 },
      total_volume: { usd: parseFloat(a.volumeUsd24Hr) || 0 },
      high_24h: null,
      low_24h: null,
      price_change_24h: null,
      price_change_percentage_24h: parseFloat(a.changePercent24Hr) || 0,
      price_change_percentage_7d: null,
      price_change_percentage_30d: null,
      ath: null,
      ath_date: null,
      circulating_supply: parseFloat(a.supply) || 0,
      total_supply: null,
      max_supply: parseFloat(a.maxSupply) || null,
    },
    links: {
      homepage: a.explorer,
      blockchain_site: a.explorer ? [a.explorer] : [],
      subreddit: null,
      twitter: null,
    },
    started_at: null,
    last_updated: raw.timestamp,
  };
}

async function searchCoins(query) {
  const url = `${BASE_URL}/assets?search=${encodeURIComponent(query)}&limit=20`;
  const res = await cachedFetch(url, CACHE_TTLS.search);
  const raw = await res.json();

  return {
    coins: (raw.data || []).map(a => ({
      id: a.id,
      name: a.name,
      symbol: a.symbol?.toLowerCase(),
      market_cap_rank: parseInt(a.rank) || null,
    })),
  };
}

async function getTrending() {
  const url = `${BASE_URL}/assets?limit=100`;
  const res = await cachedFetch(url, CACHE_TTLS.trending);
  const raw = await res.json();

  const sorted = (raw.data || [])
    .filter(a => a.changePercent24Hr != null)
    .sort((a, b) => Math.abs(parseFloat(b.changePercent24Hr)) - Math.abs(parseFloat(a.changePercent24Hr)))
    .slice(0, 15);

  return {
    coins: sorted.map(a => ({
      id: a.id,
      name: a.name,
      symbol: a.symbol?.toLowerCase(),
      market_cap_rank: parseInt(a.rank) || null,
      price_usd: parseFloat(a.priceUsd) || 0,
      change_24h: parseFloat(a.changePercent24Hr) || 0,
    })),
  };
}

async function getMarkets(vsCurrency = 'usd', perPage = 100, page = 1) {
  perPage = Math.min(Math.max(1, perPage), 250);
  page = Math.max(1, page);
  const offset = (page - 1) * perPage;
  const url = `${BASE_URL}/assets?limit=${perPage}&offset=${offset}`;
  const res = await cachedFetch(url, CACHE_TTLS.markets);
  const raw = await res.json();

  return {
    coins: (raw.data || []).map(a => ({
      id: a.id,
      symbol: a.symbol?.toLowerCase(),
      name: a.name,
      current_price: parseFloat(a.priceUsd) || 0,
      market_cap: parseFloat(a.marketCapUsd) || 0,
      market_cap_rank: parseInt(a.rank) || null,
      total_volume: parseFloat(a.volumeUsd24Hr) || 0,
      price_change_percentage_24h: parseFloat(a.changePercent24Hr) || 0,
      price_change_percentage_7d: null,
      circulating_supply: parseFloat(a.supply) || 0,
      total_supply: null,
      max_supply: parseFloat(a.maxSupply) || null,
    })),
    pagination: { page, per_page: perPage, vs_currency: vsCurrency },
  };
}

async function getHistory(id, date) {
  // CoinCap history uses interval + start/end timestamps
  const startMs = new Date(`${date}T00:00:00Z`).getTime();
  const endMs = startMs + 86400000; // +1 day
  const coinId = id.toLowerCase();
  const url = `${BASE_URL}/assets/${encodeURIComponent(coinId)}/history?interval=d1&start=${startMs}&end=${endMs}`;
  const res = await cachedFetch(url, CACHE_TTLS.history);
  const raw = await res.json();

  const entry = (raw.data || [])[0];
  return {
    id: coinId,
    date,
    market_data: entry ? {
      price: parseFloat(entry.priceUsd) || 0,
      volume_24h: null,
      market_cap: null,
      timestamp: entry.date,
    } : null,
  };
}

async function getExchanges() {
  const url = `${BASE_URL}/exchanges?limit=50`;
  const res = await cachedFetch(url, CACHE_TTLS.exchanges);
  const raw = await res.json();

  return {
    exchanges: (raw.data || []).map(e => ({
      id: e.exchangeId,
      name: e.name,
      description: null,
      active: e.socket != null,
      website: e.exchangeUrl,
      volume_usd_24h: parseFloat(e.volumeUsd) || 0,
      trading_pairs: parseInt(e.tradingPairs) || 0,
      rank: parseInt(e.rank) || null,
    })),
  };
}

async function getGlobal() {
  // Aggregate from top assets
  const url = `${BASE_URL}/assets?limit=2000`;
  const res = await cachedFetch(url, CACHE_TTLS.global);
  const raw = await res.json();

  const assets = raw.data || [];
  let totalMarketCap = 0;
  let totalVolume = 0;
  let btcMarketCap = 0;

  for (const a of assets) {
    const mc = parseFloat(a.marketCapUsd) || 0;
    const vol = parseFloat(a.volumeUsd24Hr) || 0;
    totalMarketCap += mc;
    totalVolume += vol;
    if (a.id === 'bitcoin') btcMarketCap = mc;
  }

  const btcDominance = totalMarketCap > 0 ? (btcMarketCap / totalMarketCap) * 100 : 0;

  return {
    active_cryptocurrencies: assets.length,
    markets: null,
    total_market_cap_usd: totalMarketCap,
    total_volume_24h_usd: totalVolume,
    bitcoin_dominance: parseFloat(btcDominance.toFixed(2)),
    market_cap_change_24h: null,
    last_updated: raw.timestamp,
  };
}

export { getPrice, getCoin, searchCoins, getTrending, getMarkets, getHistory, getExchanges, getGlobal, CACHE_TTLS };
