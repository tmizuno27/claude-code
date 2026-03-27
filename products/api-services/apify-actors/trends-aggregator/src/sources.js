// Core trend-fetching logic ported from 19-trends-api/src/index.js
// Cloudflare Workers specifics (cache, rate limiter, Response/CORS) removed.

const FETCH_TIMEOUT_MS = 30_000;
const MAX_RETRIES = 2;
const RETRY_DELAY_MS = 2_000;

async function fetchWithRetry(url, options = {}, timeoutMs = FETCH_TIMEOUT_MS) {
  let lastError;
  for (let attempt = 0; attempt <= MAX_RETRIES; attempt++) {
    const controller = new AbortController();
    const timer = setTimeout(() => controller.abort(), timeoutMs);
    try {
      const res = await fetchWithRetry(url, { ...options, signal: controller.signal });
      clearTimeout(timer);
      return res;
    } catch (e) {
      clearTimeout(timer);
      lastError = e;
      if (attempt < MAX_RETRIES) {
        await new Promise((r) => setTimeout(r, RETRY_DELAY_MS));
      }
    }
  }
  throw lastError;
}

// ── Google Trends Daily ──
export async function googleDaily(geo = 'US', limit = 25) {
  const url = `https://trends.google.com/trending/rss?geo=${encodeURIComponent(geo)}`;
  const res = await fetchWithRetry(url, {
    headers: { 'User-Agent': 'Mozilla/5.0 (compatible; TrendsAggregator/1.0; +https://apify.com/miccho27)' },
  });
  if (!res.ok) throw new Error(`Google Trends returned ${res.status}`);
  const xml = await res.text();

  const items = [];
  const itemRegex = /<item>([\s\S]*?)<\/item>/g;
  let match;
  while ((match = itemRegex.exec(xml)) !== null) {
    const block = match[1];
    const title =
      (block.match(/<title><!\[CDATA\[(.*?)\]\]><\/title>/) ||
        block.match(/<title>(.*?)<\/title>/) ||
        [])[1] || '';
    const traffic =
      (block.match(/<ht:approx_traffic>(.*?)<\/ht:approx_traffic>/) || [])[1] || '';
    const pubDate = (block.match(/<pubDate>(.*?)<\/pubDate>/) || [])[1] || '';
    const link = (block.match(/<link>(.*?)<\/link>/) || [])[1] || '';

    const newsItems = [];
    const newsRegex = /<ht:news_item>([\s\S]*?)<\/ht:news_item>/g;
    let nm;
    while ((nm = newsRegex.exec(block)) !== null) {
      const nb = nm[1];
      const nTitle =
        (nb.match(/<ht:news_item_title><!\[CDATA\[(.*?)\]\]><\/ht:news_item_title>/) ||
          nb.match(/<ht:news_item_title>(.*?)<\/ht:news_item_title>/) ||
          [])[1] || '';
      const nUrl =
        (nb.match(/<ht:news_item_url><!\[CDATA\[(.*?)\]\]><\/ht:news_item_url>/) ||
          nb.match(/<ht:news_item_url>(.*?)<\/ht:news_item_url>/) ||
          [])[1] || '';
      const nSource =
        (nb.match(/<ht:news_item_source>(.*?)<\/ht:news_item_source>/) || [])[1] || '';
      if (nTitle) newsItems.push({ title: nTitle, url: nUrl, source: nSource });
    }

    items.push({ title, traffic, pubDate, link, relatedArticles: newsItems });
    if (items.length >= limit) break;
  }

  return { source: 'google', geo, updated: new Date().toISOString(), count: items.length, items };
}

// ── Hacker News Trending ──
export async function hackerNewsTrending(limit = 25) {
  const res = await fetchWithRetry('https://hacker-news.firebaseio.com/v0/topstories.json');
  if (!res.ok) throw new Error(`HN returned ${res.status}`);
  const ids = await res.json();
  const top = ids.slice(0, limit);

  const stories = await Promise.all(
    top.map(async (id) => {
      const r = await fetchWithRetry(`https://hacker-news.firebaseio.com/v0/item/${id}.json`);
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

  const filtered = stories.filter(Boolean);
  return {
    source: 'hackernews',
    updated: new Date().toISOString(),
    count: filtered.length,
    items: filtered,
  };
}

// ── Reddit Trending ──
export async function redditTrending(limit = 25) {
  const res = await fetchWithRetry(`https://www.reddit.com/r/popular.json?limit=${limit}`, {
    headers: { 'User-Agent': 'Mozilla/5.0 (compatible; TrendsAggregator/1.0; +https://apify.com/miccho27)' },
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

  return { source: 'reddit', updated: new Date().toISOString(), count: items.length, items };
}

// ── GitHub Trending ──
export async function githubTrending(limit = 25) {
  const d = new Date();
  d.setDate(d.getDate() - 7);
  const since = d.toISOString().slice(0, 10);
  const url = `https://api.github.com/search/repositories?q=created:>${since}&sort=stars&order=desc&per_page=${limit}`;
  const res = await fetchWithRetry(url, {
    headers: { 'User-Agent': 'TrendsAggregator/1.0', Accept: 'application/vnd.github.v3+json' },
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

  return { source: 'github', updated: new Date().toISOString(), count: items.length, items };
}

// ── Product Hunt Today ──
export async function productHuntToday(limit = 20) {
  const res = await fetchWithRetry('https://www.producthunt.com/frontend/graphql', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'User-Agent': 'TrendsAggregator/1.0',
    },
    body: JSON.stringify({
      query: `{
        homefeed(first: ${Math.min(limit, 20)}) {
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
    return {
      source: 'producthunt',
      updated: new Date().toISOString(),
      count: 0,
      items: [],
      note: 'Product Hunt scraping unavailable. GraphQL may require auth.',
    };
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
    // parse failure — return empty items
  }

  return { source: 'producthunt', updated: new Date().toISOString(), count: items.length, items };
}
