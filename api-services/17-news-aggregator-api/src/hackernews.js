const HN_BASE = 'https://hacker-news.firebaseio.com/v0';

async function fetchTopStories(limit = 20) {
  const res = await fetch(`${HN_BASE}/topstories.json`);
  if (!res.ok) throw new Error('Failed to fetch HN top stories');
  const ids = await res.json();
  const top = ids.slice(0, limit);
  const items = await Promise.all(
    top.map(async (id) => {
      const r = await fetch(`${HN_BASE}/item/${id}.json`);
      if (!r.ok) return null;
      const item = await r.json();
      return {
        id: item.id,
        title: item.title || '',
        url: item.url || `https://news.ycombinator.com/item?id=${item.id}`,
        score: item.score || 0,
        author: item.by || '',
        time: item.time ? new Date(item.time * 1000).toISOString() : '',
        comments: item.descendants || 0,
      };
    })
  );
  return items.filter(Boolean);
}

async function searchHN(query) {
  const res = await fetch(
    `https://hn.algolia.com/api/v1/search?query=${encodeURIComponent(query)}&hitsPerPage=20`
  );
  if (!res.ok) throw new Error('HN search failed');
  const data = await res.json();
  return (data.hits || []).map((h) => ({
    id: h.objectID,
    title: h.title || '',
    url: h.url || `https://news.ycombinator.com/item?id=${h.objectID}`,
    score: h.points || 0,
    author: h.author || '',
    time: h.created_at || '',
    comments: h.num_comments || 0,
  }));
}

export { fetchTopStories, searchHN };
