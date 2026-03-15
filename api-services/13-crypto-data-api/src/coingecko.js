const BASE_URL = 'https://api.coingecko.com/api/v3';

// Cache TTLs in seconds
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

  // Try cache first
  let response = await cache.match(cacheKey);
  if (response) {
    return response;
  }

  // Fetch from CoinGecko
  response = await fetch(url, {
    headers: { 'Accept': 'application/json' },
  });

  if (!response.ok) {
    const status = response.status;
    if (status === 429) {
      // Rate limited - try cache even if expired
      const stale = await cache.match(cacheKey);
      if (stale) return stale;
      throw new Error('CoinGecko rate limit exceeded. Please try again later.');
    }
    if (status === 503) {
      throw new Error('CoinGecko service temporarily unavailable.');
    }
    throw new Error(`CoinGecko API error: ${status}`);
  }

  // Clone and cache with TTL
  const responseToCache = new Response(response.body, response);
  responseToCache.headers.set('Cache-Control', `public, max-age=${cacheTtl}`);
  await cache.put(cacheKey, responseToCache.clone());

  return responseToCache;
}

async function getPrice(ids, vsCurrencies) {
  const url = `${BASE_URL}/simple/price?ids=${ids}&vs_currencies=${vsCurrencies}&include_24hr_change=true&include_market_cap=true&include_24hr_vol=true`;
  const res = await cachedFetch(url, CACHE_TTLS.price);
  const raw = await res.json();

  // Normalize
  const data = {};
  for (const [coinId, values] of Object.entries(raw)) {
    data[coinId] = {};
    for (const [key, val] of Object.entries(values)) {
      data[coinId][key] = val;
    }
  }
  return data;
}

async function getCoin(id) {
  const url = `${BASE_URL}/coins/${id}?localization=false&tickers=false&community_data=false&developer_data=false`;
  const res = await cachedFetch(url, CACHE_TTLS.coin);
  const raw = await res.json();

  return {
    id: raw.id,
    symbol: raw.symbol,
    name: raw.name,
    image: raw.image?.large,
    description: raw.description?.en?.substring(0, 500),
    market_cap_rank: raw.market_cap_rank,
    market_data: {
      current_price: raw.market_data?.current_price,
      market_cap: raw.market_data?.market_cap,
      total_volume: raw.market_data?.total_volume,
      high_24h: raw.market_data?.high_24h,
      low_24h: raw.market_data?.low_24h,
      price_change_24h: raw.market_data?.price_change_24h,
      price_change_percentage_24h: raw.market_data?.price_change_percentage_24h,
      price_change_percentage_7d: raw.market_data?.price_change_percentage_7d_in_currency,
      price_change_percentage_30d: raw.market_data?.price_change_percentage_30d_in_currency,
      ath: raw.market_data?.ath,
      ath_date: raw.market_data?.ath_date,
      atl: raw.market_data?.atl,
      atl_date: raw.market_data?.atl_date,
      circulating_supply: raw.market_data?.circulating_supply,
      total_supply: raw.market_data?.total_supply,
      max_supply: raw.market_data?.max_supply,
    },
    links: {
      homepage: raw.links?.homepage?.[0],
      blockchain_site: raw.links?.blockchain_site?.filter(Boolean).slice(0, 3),
      subreddit: raw.links?.subreddit_url,
      twitter: raw.links?.twitter_screen_name,
    },
    genesis_date: raw.genesis_date,
    last_updated: raw.last_updated,
  };
}

async function searchCoins(query) {
  const url = `${BASE_URL}/search?query=${encodeURIComponent(query)}`;
  const res = await cachedFetch(url, CACHE_TTLS.search);
  const raw = await res.json();

  return {
    coins: (raw.coins || []).slice(0, 20).map(c => ({
      id: c.id,
      name: c.name,
      symbol: c.symbol,
      market_cap_rank: c.market_cap_rank,
      thumb: c.thumb,
    })),
  };
}

async function getTrending() {
  const url = `${BASE_URL}/search/trending`;
  const res = await cachedFetch(url, CACHE_TTLS.trending);
  const raw = await res.json();

  return {
    coins: (raw.coins || []).map(c => ({
      id: c.item.id,
      name: c.item.name,
      symbol: c.item.symbol,
      market_cap_rank: c.item.market_cap_rank,
      thumb: c.item.thumb,
      score: c.item.score,
      price_btc: c.item.price_btc,
    })),
  };
}

async function getMarkets(vsCurrency = 'usd', perPage = 100, page = 1) {
  perPage = Math.min(Math.max(1, perPage), 250);
  page = Math.max(1, page);
  const url = `${BASE_URL}/coins/markets?vs_currency=${vsCurrency}&order=market_cap_desc&per_page=${perPage}&page=${page}&sparkline=false&price_change_percentage=1h,24h,7d`;
  const res = await cachedFetch(url, CACHE_TTLS.markets);
  const raw = await res.json();

  return {
    coins: (raw || []).map(c => ({
      id: c.id,
      symbol: c.symbol,
      name: c.name,
      image: c.image,
      current_price: c.current_price,
      market_cap: c.market_cap,
      market_cap_rank: c.market_cap_rank,
      total_volume: c.total_volume,
      high_24h: c.high_24h,
      low_24h: c.low_24h,
      price_change_24h: c.price_change_24h,
      price_change_percentage_24h: c.price_change_percentage_24h,
      price_change_percentage_1h: c.price_change_percentage_1h_in_currency,
      price_change_percentage_7d: c.price_change_percentage_7d_in_currency,
      circulating_supply: c.circulating_supply,
      total_supply: c.total_supply,
      ath: c.ath,
      ath_change_percentage: c.ath_change_percentage,
    })),
    pagination: { page, per_page: perPage, vs_currency: vsCurrency },
  };
}

async function getHistory(id, date) {
  // CoinGecko expects dd-mm-yyyy
  const [y, m, d] = date.split('-');
  const formatted = `${d}-${m}-${y}`;
  const url = `${BASE_URL}/coins/${id}/history?date=${formatted}&localization=false`;
  const res = await cachedFetch(url, CACHE_TTLS.history);
  const raw = await res.json();

  return {
    id: raw.id,
    symbol: raw.symbol,
    name: raw.name,
    date,
    market_data: raw.market_data ? {
      current_price: raw.market_data.current_price,
      market_cap: raw.market_data.market_cap,
      total_volume: raw.market_data.total_volume,
    } : null,
  };
}

async function getExchanges() {
  const url = `${BASE_URL}/exchanges?per_page=50`;
  const res = await cachedFetch(url, CACHE_TTLS.exchanges);
  const raw = await res.json();

  return {
    exchanges: (raw || []).map(e => ({
      id: e.id,
      name: e.name,
      country: e.country,
      url: e.url,
      image: e.image,
      trust_score: e.trust_score,
      trust_score_rank: e.trust_score_rank,
      trade_volume_24h_btc: e.trade_volume_24h_btc,
      year_established: e.year_established,
    })),
  };
}

async function getGlobal() {
  const url = `${BASE_URL}/global`;
  const res = await cachedFetch(url, CACHE_TTLS.global);
  const raw = await res.json();
  const d = raw.data || {};

  return {
    active_cryptocurrencies: d.active_cryptocurrencies,
    markets: d.markets,
    total_market_cap: d.total_market_cap,
    total_volume: d.total_volume,
    market_cap_percentage: d.market_cap_percentage,
    market_cap_change_percentage_24h_usd: d.market_cap_change_percentage_24h_usd,
    updated_at: d.updated_at,
  };
}

export { getPrice, getCoin, searchCoins, getTrending, getMarkets, getHistory, getExchanges, getGlobal, CACHE_TTLS };
