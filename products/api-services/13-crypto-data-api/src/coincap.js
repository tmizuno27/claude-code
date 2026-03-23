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
    if (response.status === 429) {
      const stale = await cache.match(cacheKey);
      if (stale) return stale;
      throw new Error('Rate limit exceeded. Please try again later.');
    }
    throw new Error(`Upstream API error: ${response.status}`);
  }

  const responseToCache = new Response(response.body, response);
  responseToCache.headers.set('Cache-Control', `public, max-age=${cacheTtl}`);
  await cache.put(cacheKey, responseToCache.clone());

  return responseToCache;
}

// Map common names to CoinPaprika IDs
function toPaprikaId(id) {
  const map = {
    'bitcoin': 'btc-bitcoin',
    'ethereum': 'eth-ethereum',
    'solana': 'sol-solana',
    'cardano': 'ada-cardano',
    'dogecoin': 'doge-dogecoin',
    'ripple': 'xrp-xrp',
    'xrp': 'xrp-xrp',
    'polkadot': 'dot-polkadot',
    'litecoin': 'ltc-litecoin',
    'chainlink': 'link-chainlink',
    'avalanche': 'avax-avalanche',
    'bnb': 'bnb-binance-coin',
    'tron': 'trx-tron',
  };
  return map[id.toLowerCase()] || id.toLowerCase();
}

async function getPrice(ids, vsCurrencies) {
  const idList = ids.split(',').map(s => s.trim().toLowerCase());
  const data = {};

  const fetches = idList.map(async (id) => {
    const paprikaId = toPaprikaId(id);
    const url = `${BASE_URL}/tickers/${paprikaId}`;
    try {
      const res = await cachedFetch(url, CACHE_TTLS.price);
      const raw = await res.json();
      const q = raw.quotes?.USD || {};
      data[id] = {
        usd: q.price || 0,
        usd_market_cap: q.market_cap || 0,
        usd_24h_vol: q.volume_24h || 0,
        usd_24h_change: q.percent_change_24h || 0,
      };
    } catch {
      data[id] = { error: `Coin '${id}' not found` };
    }
  });

  await Promise.all(fetches);
  return data;
}

async function getCoin(id) {
  const paprikaId = toPaprikaId(id);
  const [coinRes, tickerRes] = await Promise.all([
    cachedFetch(`${BASE_URL}/coins/${paprikaId}`, CACHE_TTLS.coin),
    cachedFetch(`${BASE_URL}/tickers/${paprikaId}`, CACHE_TTLS.price),
  ]);
  const coin = await coinRes.json();
  const ticker = await tickerRes.json();
  const q = ticker.quotes?.USD || {};

  return {
    id: coin.id,
    symbol: coin.symbol?.toLowerCase(),
    name: coin.name,
    image: coin.logo,
    description: coin.description,
    market_cap_rank: ticker.rank || null,
    market_data: {
      current_price: { usd: q.price || 0 },
      market_cap: { usd: q.market_cap || 0 },
      total_volume: { usd: q.volume_24h || 0 },
      high_24h: null,
      low_24h: null,
      price_change_24h: q.percent_change_24h || 0,
      price_change_percentage_24h: q.percent_change_24h || 0,
      price_change_percentage_7d: q.percent_change_7d || 0,
      price_change_percentage_30d: q.percent_change_30d || 0,
      ath: q.ath_price || null,
      ath_date: q.ath_date || null,
      circulating_supply: ticker.circulating_supply || 0,
      total_supply: ticker.total_supply || null,
      max_supply: ticker.max_supply || null,
    },
    links: {
      homepage: coin.links?.website?.[0] || null,
      blockchain_site: coin.links?.explorer || [],
      subreddit: coin.links?.reddit?.[0] || null,
      twitter: coin.links?.twitter ? [`https://twitter.com/${coin.links.twitter[0]}`] : null,
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
    coins: (raw.currencies || []).map(c => ({
      id: c.id,
      name: c.name,
      symbol: c.symbol?.toLowerCase(),
      market_cap_rank: c.rank || null,
    })),
  };
}

async function getTrending() {
  const url = `${BASE_URL}/tickers?limit=100`;
  const res = await cachedFetch(url, CACHE_TTLS.trending);
  const raw = await res.json();

  const sorted = (raw || [])
    .filter(t => t.quotes?.USD?.percent_change_24h != null)
    .sort((a, b) => Math.abs(b.quotes.USD.percent_change_24h) - Math.abs(a.quotes.USD.percent_change_24h))
    .slice(0, 15);

  return {
    coins: sorted.map(t => ({
      id: t.id,
      name: t.name,
      symbol: t.symbol?.toLowerCase(),
      market_cap_rank: t.rank || null,
      price_usd: t.quotes.USD.price || 0,
      change_24h: t.quotes.USD.percent_change_24h || 0,
    })),
  };
}

async function getMarkets(vsCurrency = 'usd', perPage = 100, page = 1) {
  perPage = Math.min(Math.max(1, perPage), 250);
  page = Math.max(1, page);
  const url = `${BASE_URL}/tickers?limit=${perPage}&page=${page}`;
  const res = await cachedFetch(url, CACHE_TTLS.markets);
  const raw = await res.json();

  return {
    coins: (raw || []).map(t => ({
      id: t.id,
      symbol: t.symbol?.toLowerCase(),
      name: t.name,
      current_price: t.quotes?.USD?.price || 0,
      market_cap: t.quotes?.USD?.market_cap || 0,
      market_cap_rank: t.rank || null,
      total_volume: t.quotes?.USD?.volume_24h || 0,
      price_change_percentage_24h: t.quotes?.USD?.percent_change_24h || 0,
      price_change_percentage_7d: t.quotes?.USD?.percent_change_7d || 0,
      circulating_supply: t.circulating_supply || 0,
      total_supply: t.total_supply || null,
      max_supply: t.max_supply || null,
    })),
    pagination: { page, per_page: perPage, vs_currency: vsCurrency },
  };
}

async function getHistory(id, date) {
  const paprikaId = toPaprikaId(id);
  const url = `${BASE_URL}/tickers/${paprikaId}/historical?start=${date}T00:00:00Z&end=${date}T23:59:59Z&interval=1d`;
  const res = await cachedFetch(url, CACHE_TTLS.history);
  const raw = await res.json();

  const entry = (raw || [])[0];
  return {
    id,
    date,
    market_data: entry ? {
      price: entry.price || 0,
      volume_24h: entry.volume_24h || 0,
      market_cap: entry.market_cap || 0,
      timestamp: entry.timestamp,
    } : null,
  };
}

async function getExchanges() {
  const url = `${BASE_URL}/exchanges`;
  const res = await cachedFetch(url, CACHE_TTLS.exchanges);
  const raw = await res.json();

  return {
    exchanges: (raw || []).slice(0, 50).map(e => ({
      id: e.id,
      name: e.name,
      description: e.description || null,
      active: e.active,
      website: e.website_status ? e.links?.website?.[0] : null,
      volume_usd_24h: e.quotes?.USD?.reported_volume_24h || 0,
      trading_pairs: e.markets || 0,
      rank: e.adjusted_rank || null,
    })),
  };
}

async function getGlobal() {
  const url = `${BASE_URL}/global`;
  const res = await cachedFetch(url, CACHE_TTLS.global);
  const raw = await res.json();

  return {
    active_cryptocurrencies: raw.cryptocurrencies_number || 0,
    markets: raw.market_cap_change_24h || null,
    total_market_cap_usd: raw.market_cap_usd || 0,
    total_volume_24h_usd: raw.volume_24h_usd || 0,
    bitcoin_dominance: raw.bitcoin_dominance_percentage || 0,
    market_cap_change_24h: raw.market_cap_ath_value || null,
    last_updated: raw.last_updated,
  };
}

export { getPrice, getCoin, searchCoins, getTrending, getMarkets, getHistory, getExchanges, getGlobal, CACHE_TTLS };
