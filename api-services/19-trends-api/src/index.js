// ── Rate Limiter (size-based cleanup, no setInterval) ──
const rateLimitMap = new Map();
const RATE_LIMIT = 20;
const RATE_WINDOW = 60000;
const MAX_RATE_ENTRIES = 5000;

function checkRateLimit(ip) {
  const now = Date.now();
  // Size-based cleanup
  if (rateLimitMap.size > MAX_RATE_ENTRIES) {
    for (const [key, val] of rateLimitMap) {
      if (now - val.start > RATE_WINDOW) rateLimitMap.delete(key);
      if (rateLimitMap.size <= MAX_RATE_ENTRIES / 2) break;
    }
  }
  const entry = rateLimitMap.get(ip);
  if (!entry || now - entry.start > RATE_WINDOW) {
    rateLimitMap.set(ip, { start: now, count: 1 });
    return true;
  }
  entry.count++;
  return entry.count <= RATE_LIMIT;
}

// ── Cache ──
const cache = new Map();

function getCached(key, ttlSeconds) {
  const entry = cache.get(key);
  if (entry && Date.now() - entry.time < ttlSeconds * 1000) return entry.data;
  return null;
}

function setCache(key, data) {
  cache.set(key, { data, time: Date.now() });
}

// ── CORS headers ──
const CORS = {
  'Access-Control-Allow-Origin': '*',
  'Access-Control-Allow-Methods': 'GET, OPTIONS',
  'Access-Control-Allow-Headers': 'Content-Type',
};

function json(data, status = 200) {
  if (status === 200 && typeof data === "object" && !Array.isArray(data)) {
    data._upgrade = { note: "Upgrade for higher limits & priority support", url: "https://rapidapi.com/miccho27-5OJaGGbBiO/api/trends-api/pricing" };
  }
  return new Response(JSON.stringify(data), {
    status,
    headers: { 'Content-Type': 'application/json', ...CORS },
  });
}

// ── Google Trends Daily ──
async function googleDaily(geo = 'US') {
  const cacheKey = `google:${geo}`;
  const cached = getCached(cacheKey, 600);
  if (cached) return cached;

  const url = `https://trends.google.com/trending/rss?geo=${encodeURIComponent(geo)}`;
  const res = await fetch(url, {
    headers: { 'User-Agent': 'Mozilla/5.0 (compatible; TrendsAPI/1.0; +https://rapidapi.com)' },
  });
  if (!res.ok) throw new Error(`Google Trends returned ${res.status}`);
  const xml = await res.text();

  const items = [];
  const itemRegex = /<item>([\s\S]*?)<\/item>/g;
  let match;
  while ((match = itemRegex.exec(xml)) !== null) {
    const block = match[1];
    const title = (block.match(/<title><!\[CDATA\[(.*?)\]\]><\/title>/) ||
                   block.match(/<title>(.*?)<\/title>/) || [])[1] || '';
    const traffic = (block.match(/<ht:approx_traffic>(.*?)<\/ht:approx_traffic>/) || [])[1] || '';
    const pubDate = (block.match(/<pubDate>(.*?)<\/pubDate>/) || [])[1] || '';
    const link = (block.match(/<link>(.*?)<\/link>/) || [])[1] || '';
    // Related news
    const newsItems = [];
    const newsRegex = /<ht:news_item>([\s\S]*?)<\/ht:news_item>/g;
    let nm;
    while ((nm = newsRegex.exec(block)) !== null) {
      const nb = nm[1];
      const nTitle = (nb.match(/<ht:news_item_title><!\[CDATA\[(.*?)\]\]><\/ht:news_item_title>/) ||
                      nb.match(/<ht:news_item_title>(.*?)<\/ht:news_item_title>/) || [])[1] || '';
      const nUrl = (nb.match(/<ht:news_item_url><!\[CDATA\[(.*?)\]\]><\/ht:news_item_url>/) ||
                    nb.match(/<ht:news_item_url>(.*?)<\/ht:news_item_url>/) || [])[1] || '';
      const nSource = (nb.match(/<ht:news_item_source>(.*?)<\/ht:news_item_source>/) || [])[1] || '';
      if (nTitle) newsItems.push({ title: nTitle, url: nUrl, source: nSource });
    }
    items.push({ title, traffic, pubDate, link, relatedArticles: newsItems });
  }

  const data = { geo, updated: new Date().toISOString(), count: items.length, items };
  setCache(cacheKey, data);
  return data;
}

// ── Hacker News Trending ──
async function hackerNewsTrending() {
  const cached = getCached('hn', 300);
  if (cached) return cached;

  const res = await fetch('https://hacker-news.firebaseio.com/v0/topstories.json');
  if (!res.ok) throw new Error(`HN returned ${res.status}`);
  const ids = await res.json();
  const top = ids.slice(0, 25);

  const stories = await Promise.all(
    top.map(async (id) => {
      const r = await fetch(`https://hacker-news.firebaseio.com/v0/item/${id}.json`);
      if (!r.ok) return null;
      const item = await r.json();
      return {
        id: item.id,
        title: item.title,
        url: item.url || `https://news.ycombinator.com/item?id=${item.id}`,
        score: item.score,
        by: item.by,
        comments: item.descendants || 0,
        time: item.time,
      };
    })
  );

  const data = {
    updated: new Date().toISOString(),
    count: stories.filter(Boolean).length,
    items: stories.filter(Boolean),
  };
  setCache('hn', data);
  return data;
}

// ── Reddit Trending ──
async function redditTrending() {
  const cached = getCached('reddit', 600);
  if (cached) return cached;

  const res = await fetch('https://www.reddit.com/r/popular.json?limit=25', {
    headers: { 'User-Agent': 'Mozilla/5.0 (compatible; TrendsAPI/1.0; +https://rapidapi.com)' },
  });
  if (!res.ok) throw new Error(`Reddit returned ${res.status}`);
  const body = await res.json();

  const items = (body.data?.children || []).map((c) => {
    const d = c.data;
    return {
      title: d.title,
      subreddit: d.subreddit_name_prefixed,
      score: d.score,
      comments: d.num_comments,
      url: `https://www.reddit.com${d.permalink}`,
      author: d.author,
      created_utc: d.created_utc,
    };
  });

  const data = { updated: new Date().toISOString(), count: items.length, items };
  setCache('reddit', data);
  return data;
}

// ── GitHub Trending ──
async function githubTrending() {
  const cached = getCached('github', 1800);
  if (cached) return cached;

  const d = new Date();
  d.setDate(d.getDate() - 7);
  const since = d.toISOString().slice(0, 10);
  const url = `https://api.github.com/search/repositories?q=created:>${since}&sort=stars&order=desc&per_page=25`;
  const res = await fetch(url, {
    headers: { 'User-Agent': 'TrendsAPI/1.0', Accept: 'application/vnd.github.v3+json' },
  });
  if (!res.ok) throw new Error(`GitHub returned ${res.status}`);
  const body = await res.json();

  const items = (body.items || []).map((r) => ({
    name: r.full_name,
    description: r.description,
    url: r.html_url,
    stars: r.stargazers_count,
    forks: r.forks_count,
    language: r.language,
    created_at: r.created_at,
  }));

  const data = { updated: new Date().toISOString(), count: items.length, items };
  setCache('github', data);
  return data;
}

// ── Product Hunt Today ──
async function productHuntToday() {
  const cached = getCached('ph', 600);
  if (cached) return cached;

  // Use the unofficial front-page JSON endpoint
  const res = await fetch('https://www.producthunt.com/frontend/graphql', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'User-Agent': 'TrendsAPI/1.0',
    },
    body: JSON.stringify({
      query: `{
        homefeed(first: 20) {
          edges {
            node {
              ... on Post {
                id
                name
                tagline
                votesCount
                website
                url
                topics { edges { node { name } } }
              }
            }
          }
        }
      }`,
    }),
  });

  if (!res.ok) {
    // Fallback: return empty with note
    const data = {
      updated: new Date().toISOString(),
      count: 0,
      items: [],
      note: 'Product Hunt scraping unavailable. GraphQL may require auth.',
    };
    setCache('ph', data);
    return data;
  }

  let items = [];
  try {
    const body = await res.json();
    items = (body.data?.homefeed?.edges || [])
      .map((e) => e.node)
      .filter(Boolean)
      .map((p) => ({
        name: p.name,
        tagline: p.tagline,
        votes: p.votesCount,
        url: p.url ? `https://www.producthunt.com${p.url}` : '',
        website: p.website,
        topics: (p.topics?.edges || []).map((t) => t.node.name),
      }));
  } catch {
    // parse failure
  }

  const data = { updated: new Date().toISOString(), count: items.length, items };
  setCache('ph', data);
  return data;
}

// ── Router ──
export default {
  async fetch(request) {
    if (request.method === 'OPTIONS') {
      return new Response(null, { status: 204, headers: CORS });
    }

    const ip = request.headers.get('cf-connecting-ip') || 'unknown';
    if (!checkRateLimit(ip)) {
      return json({ error: 'Rate limit exceeded. Max 20 requests per minute.' }, 429);
    }

    const url = new URL(request.url);
    const path = url.pathname.replace(/\/+$/, '') || '/';

    try {
      if (path === '/') {
        return json({
          name: 'Trends API',
          
        _premium: {
          message: "You are using the FREE tier of Trends API. Upgrade to Pro for higher rate limits, priority support, and advanced features.",
          upgrade_url: "https://rapidapi.com/miccho27-5OJaGGbBiO/api/trends-api/pricing",
          plans: ["Pro ($5.99/mo)", "Ultra ($14.99/mo)", "Mega ($49.99/mo)"]
        },
          endpoints: [
            'GET /google/daily?geo=US',
            'GET /hackernews/trending',
            'GET /reddit/trending',
            'GET /github/trending',
            'GET /producthunt/today',
          ],
        });
      }

      if (path === '/google/daily') {
        const geo = url.searchParams.get('geo') || 'US';
        return json(await googleDaily(geo));
      }

      if (path === '/hackernews/trending') {
        return json(await hackerNewsTrending());
      }

      if (path === '/reddit/trending') {
        return json(await redditTrending());
      }

      if (path === '/github/trending') {
        return json(await githubTrending());
      }

      if (path === '/producthunt/today') {
        return json(await productHuntToday());
      }

      return json({ error: 'Not found' }, 404);
    } catch (err) {
      return json({ error: err.message || 'Internal error' }, 502);
    }
  },
};
