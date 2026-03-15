const RSS_FEEDS = {
  bbc: 'https://feeds.bbci.co.uk/news/rss.xml',
  nyt: 'https://rss.nytimes.com/services/xml/rss/nyt/HomePage.xml',
  reuters: 'https://feeds.reuters.com/reuters/topNews',
  techcrunch: 'https://techcrunch.com/feed/',
  bloomberg: 'https://feeds.bloomberg.com/markets/news.rss',
};

function decodeEntities(str) {
  if (!str) return '';
  return str
    .replace(/&amp;/g, '&')
    .replace(/&lt;/g, '<')
    .replace(/&gt;/g, '>')
    .replace(/&quot;/g, '"')
    .replace(/&#39;/g, "'")
    .replace(/&apos;/g, "'")
    .replace(/<!\[CDATA\[([\s\S]*?)\]\]>/g, '$1');
}

function stripHtml(str) {
  if (!str) return '';
  return str.replace(/<[^>]*>/g, '').trim();
}

function extractTag(xml, tag) {
  const re = new RegExp(`<${tag}[^>]*>([\\s\\S]*?)</${tag}>`, 'i');
  const m = xml.match(re);
  return m ? decodeEntities(m[1]).trim() : '';
}

function parseRssItems(xml) {
  const items = [];
  // RSS 2.0 <item>
  const rssItemRe = /<item[\s>]([\s\S]*?)<\/item>/gi;
  let match;
  while ((match = rssItemRe.exec(xml)) !== null) {
    const block = match[1];
    items.push({
      title: stripHtml(extractTag(block, 'title')),
      link: extractTag(block, 'link'),
      description: stripHtml(extractTag(block, 'description')).slice(0, 300),
      pubDate: extractTag(block, 'pubDate'),
      author: extractTag(block, 'author') || extractTag(block, 'dc:creator'),
      category: extractTag(block, 'category'),
    });
  }
  return items;
}

function parseAtomEntries(xml) {
  const entries = [];
  const entryRe = /<entry[\s>]([\s\S]*?)<\/entry>/gi;
  let match;
  while ((match = entryRe.exec(xml)) !== null) {
    const block = match[1];
    const linkMatch = block.match(/<link[^>]*href=["']([^"']*)["'][^>]*\/?>/i);
    entries.push({
      title: stripHtml(extractTag(block, 'title')),
      link: linkMatch ? decodeEntities(linkMatch[1]) : '',
      description: stripHtml(extractTag(block, 'summary') || extractTag(block, 'content')).slice(0, 300),
      pubDate: extractTag(block, 'updated') || extractTag(block, 'published'),
      author: extractTag(block, 'name'),
      category: '',
    });
  }
  return entries;
}

function parseFeed(xml) {
  if (/<feed[\s>]/i.test(xml)) {
    return parseAtomEntries(xml);
  }
  return parseRssItems(xml);
}

async function fetchFeed(url) {
  const res = await fetch(url, {
    headers: { 'User-Agent': 'NewsAggregatorBot/1.0' },
  });
  if (!res.ok) return [];
  const xml = await res.text();
  return parseFeed(xml);
}

async function fetchFeeds(feedKeys) {
  const urls = feedKeys.map((k) => RSS_FEEDS[k]).filter(Boolean);
  const results = await Promise.allSettled(urls.map(fetchFeed));
  const articles = [];
  for (const r of results) {
    if (r.status === 'fulfilled') articles.push(...r.value);
  }
  articles.sort((a, b) => new Date(b.pubDate || 0) - new Date(a.pubDate || 0));
  return articles;
}

export { RSS_FEEDS, parseFeed, fetchFeed, fetchFeeds };
