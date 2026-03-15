import { jsonResponse, errorResponse, handleCors, checkRateLimit, cleanRateLimits } from './utils.js';
import { getPrice, getCoin, searchCoins, getTrending, getMarkets, getHistory, getExchanges, getGlobal, CACHE_TTLS } from './coingecko.js';

export default {
  async fetch(request, env) {
    // CORS preflight
    const corsResponse = handleCors(request);
    if (corsResponse) return corsResponse;

    // Rate limiting
    const ip = request.headers.get('CF-Connecting-IP') || 'unknown';
    if (!checkRateLimit(ip)) {
      return errorResponse('Rate limit exceeded. Max 30 requests per minute.', 429);
    }

    // Periodic cleanup
    cleanRateLimits();

    const url = new URL(request.url);
    const path = url.pathname;
    const params = url.searchParams;

    try {
      // GET /
      if (path === '/' || path === '') {
        return jsonResponse({
          name: 'Crypto Data API',
          version: '1.0.0',
          description: 'Cryptocurrency data aggregated from CoinGecko',
          endpoints: [
            { method: 'GET', path: '/price', params: 'ids (required), vs (default: usd)', description: 'Current prices for multiple coins' },
            { method: 'GET', path: '/coin/:id', description: 'Detailed coin information' },
            { method: 'GET', path: '/search', params: 'q (required)', description: 'Search coins by name or symbol' },
            { method: 'GET', path: '/trending', description: 'Top trending coins' },
            { method: 'GET', path: '/markets', params: 'vs (default: usd), per_page (default: 100), page (default: 1)', description: 'Market listings with pagination' },
            { method: 'GET', path: '/history', params: 'id (required), date (required, YYYY-MM-DD)', description: 'Historical price on a specific date' },
            { method: 'GET', path: '/exchanges', description: 'List top exchanges' },
            { method: 'GET', path: '/global', description: 'Global crypto market stats' },
          ],
          cache_ttls: CACHE_TTLS,
          rate_limit: '30 requests per minute per IP',
          data_source: 'CoinGecko API (free tier)',
        });
      }

      // GET /price
      if (path === '/price') {
        const ids = params.get('ids');
        if (!ids) return errorResponse('Missing required parameter: ids', 400);
        const vs = params.get('vs') || 'usd';
        const data = await getPrice(ids, vs);
        return jsonResponse(data, 200, CACHE_TTLS.price);
      }

      // GET /coin/:id
      if (path.startsWith('/coin/')) {
        const id = path.split('/coin/')[1];
        if (!id) return errorResponse('Missing coin id', 400);
        const data = await getCoin(id);
        return jsonResponse(data, 200, CACHE_TTLS.coin);
      }

      // GET /search
      if (path === '/search') {
        const q = params.get('q');
        if (!q) return errorResponse('Missing required parameter: q', 400);
        const data = await searchCoins(q);
        return jsonResponse(data, 200, CACHE_TTLS.search);
      }

      // GET /trending
      if (path === '/trending') {
        const data = await getTrending();
        return jsonResponse(data, 200, CACHE_TTLS.trending);
      }

      // GET /markets
      if (path === '/markets') {
        const vs = params.get('vs') || 'usd';
        const perPage = parseInt(params.get('per_page') || '100', 10);
        const page = parseInt(params.get('page') || '1', 10);
        const data = await getMarkets(vs, perPage, page);
        return jsonResponse(data, 200, CACHE_TTLS.markets);
      }

      // GET /history
      if (path === '/history') {
        const id = params.get('id');
        const date = params.get('date');
        if (!id || !date) return errorResponse('Missing required parameters: id, date (YYYY-MM-DD)', 400);
        if (!/^\d{4}-\d{2}-\d{2}$/.test(date)) return errorResponse('Invalid date format. Use YYYY-MM-DD', 400);
        const data = await getHistory(id, date);
        return jsonResponse(data, 200, CACHE_TTLS.history);
      }

      // GET /exchanges
      if (path === '/exchanges') {
        const data = await getExchanges();
        return jsonResponse(data, 200, CACHE_TTLS.exchanges);
      }

      // GET /global
      if (path === '/global') {
        const data = await getGlobal();
        return jsonResponse(data, 200, CACHE_TTLS.global);
      }

      return errorResponse('Not found', 404);
    } catch (err) {
      return errorResponse(err.message || 'Internal server error', err.message?.includes('rate limit') ? 429 : 500);
    }
  },
};
