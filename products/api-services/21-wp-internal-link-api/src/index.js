// WP Internal Link Optimization API
// Analyzes article content and suggests internal links based on keyword matching

// ---------------------------------------------------------------------------
// Rate limiting
// ---------------------------------------------------------------------------
const rateMap = new Map();
const RATE_LIMIT = 20;
const RATE_WINDOW = 60_000;
const MAX_MAP_SIZE = 5000;

function checkRateLimit(ip) {
  const now = Date.now();
  if (rateMap.size > MAX_MAP_SIZE) {
    for (const [key, entry] of rateMap) {
      if (now - entry.start > RATE_WINDOW) rateMap.delete(key);
      if (rateMap.size <= MAX_MAP_SIZE / 2) break;
    }
  }
  const entry = rateMap.get(ip);
  if (!entry || now - entry.start > RATE_WINDOW) {
    rateMap.set(ip, { start: now, count: 1 });
    return { allowed: true, remaining: RATE_LIMIT - 1 };
  }
  entry.count++;
  if (entry.count > RATE_LIMIT) {
    return { allowed: false, remaining: 0, retryAfter: Math.ceil((entry.start + RATE_WINDOW - now) / 1000) };
  }
  return { allowed: true, remaining: RATE_LIMIT - entry.count };
}

// ---------------------------------------------------------------------------
// Response helpers
// ---------------------------------------------------------------------------
function cors(headers = {}) {
  return {
    'Access-Control-Allow-Origin': '*',
    'Access-Control-Allow-Methods': 'GET, POST, OPTIONS',
    'Access-Control-Allow-Headers': 'Content-Type',
    'Content-Type': 'application/json',
    ...headers,
  };
}

function json(data, status = 200, extra = {}) {
  if (status === 200 && typeof data === 'object' && !Array.isArray(data)) {
    data._upgrade = {
      note: 'Upgrade for higher limits & priority support',
      url: 'https://rapidapi.com/miccho27-5OJaGGbBiO/api/wp-internal-link-api/pricing',
    };
  }
  return new Response(JSON.stringify(data, null, 2), { status, headers: cors(extra) });
}

function error(message, status = 400) {
  return json({ error: message }, status);
}

// ---------------------------------------------------------------------------
// HTML / Text utilities
// ---------------------------------------------------------------------------
const RE_HTML_TAG = /<[^>]+>/g;
const RE_NON_WORD = /[^\w\u3000-\u9fff\uff00-\uffef]/g;

const STOP_WORDS = new Set([
  'the', 'a', 'an', 'is', 'are', 'was', 'were', 'be', 'been', 'being',
  'have', 'has', 'had', 'do', 'does', 'did', 'will', 'would', 'could',
  'should', 'may', 'might', 'shall', 'can', 'need', 'dare', 'ought',
  'used', 'to', 'of', 'in', 'for', 'on', 'with', 'at', 'by', 'from',
  'as', 'into', 'through', 'during', 'before', 'after', 'above', 'below',
  'between', 'out', 'off', 'over', 'under', 'again', 'further', 'then',
  'once', 'here', 'there', 'when', 'where', 'why', 'how', 'all', 'each',
  'every', 'both', 'few', 'more', 'most', 'other', 'some', 'such', 'no',
  'not', 'only', 'own', 'same', 'so', 'than', 'too', 'very', 'just',
  'because', 'but', 'and', 'or', 'if', 'while', 'that', 'this', 'it',
  'its', 'i', 'me', 'my', 'we', 'our', 'you', 'your', 'he', 'him',
  'his', 'she', 'her', 'they', 'them', 'their', 'what', 'which', 'who',
  // Japanese stop words
  'の', 'に', 'は', 'を', 'が', 'で', 'と', 'て', 'た', 'し',
  'な', 'も', 'や', 'か', 'から', 'まで', 'より', 'へ', 'ね',
  'よ', 'わ', 'さ', 'れ', 'る', 'する', 'ある', 'いる', 'なる',
  'こと', 'もの', 'ため', 'それ', 'これ', 'あの', 'その', 'この',
  'など', 'ずつ', 'だけ', 'でも', 'ほど', 'まま', 'ながら',
]);

function stripHtml(html) {
  return (html || '').replace(RE_HTML_TAG, ' ').trim();
}

function tokenize(text) {
  const cleaned = text.replace(RE_NON_WORD, ' ');
  return cleaned.split(/\s+/).filter(t => t.length >= 2 && !STOP_WORDS.has(t.toLowerCase()));
}

function extractNgrams(tokens, n) {
  const ngrams = [];
  for (let i = 0; i <= tokens.length - n; i++) {
    ngrams.push(tokens.slice(i, i + n).join(' '));
  }
  return ngrams;
}

function buildKeywordSet(title, content) {
  const text = `${stripHtml(title)} ${stripHtml(content)}`;
  const tokens = tokenize(text);
  const unigrams = new Set(tokens.map(t => t.toLowerCase()));
  const bigrams = new Set(extractNgrams(tokens, 2).map(t => t.toLowerCase()));
  const trigrams = new Set(extractNgrams(tokens, 3).map(t => t.toLowerCase()));
  return new Set([...unigrams, ...bigrams, ...trigrams]);
}

function computeRelevance(kwA, kwB) {
  let count = 0;
  for (const kw of kwA) {
    if (kwB.has(kw)) count++;
  }
  return count;
}

// ---------------------------------------------------------------------------
// Sitemap parser
// ---------------------------------------------------------------------------
async function fetchSitemap(sitemapUrl) {
  const res = await fetch(sitemapUrl, {
    headers: {
      'User-Agent': 'Mozilla/5.0 (compatible; WPInternalLinkBot/1.0)',
      'Accept': 'application/xml, text/xml, */*',
    },
    redirect: 'follow',
  });
  if (!res.ok) throw new Error(`Failed to fetch sitemap: HTTP ${res.status}`);
  const xml = await res.text();

  // Extract <url> entries with <loc> and optional <title> or derive title from URL
  const urls = [];
  const urlBlocks = xml.match(/<url>([\s\S]*?)<\/url>/gi) || [];
  for (const block of urlBlocks) {
    const locMatch = block.match(/<loc>(.*?)<\/loc>/i);
    if (!locMatch) continue;
    const loc = locMatch[1].trim();
    // Try to find title in various possible tags
    const titleMatch = block.match(/<(?:title|news:title)>(.*?)<\/(?:title|news:title)>/i);
    const title = titleMatch ? titleMatch[1].trim() : deriveTitleFromUrl(loc);
    urls.push({ url: loc, title });
  }
  return urls;
}

function deriveTitleFromUrl(url) {
  try {
    const path = new URL(url).pathname;
    const slug = path.replace(/\/$/, '').split('/').pop() || '';
    return slug.replace(/[-_]/g, ' ').replace(/\b\w/g, c => c.toUpperCase());
  } catch {
    return url;
  }
}

// ---------------------------------------------------------------------------
// Core analysis logic
// ---------------------------------------------------------------------------
function analyzeLinks(articleHtml, articleTitle, existingPages) {
  const articleText = stripHtml(articleHtml);
  const articleKw = buildKeywordSet(articleTitle || '', articleHtml);

  const suggestions = [];

  for (const page of existingPages) {
    const pageKw = buildKeywordSet(page.title || '', page.content || page.title || '');
    const score = computeRelevance(articleKw, pageKw);

    if (score === 0) continue;

    // Find best anchor text: use overlapping keywords, prefer longer phrases
    const overlap = [];
    for (const kw of articleKw) {
      if (pageKw.has(kw) && kw.length > 3) overlap.push(kw);
    }
    // Sort by length descending to prefer longer, more specific phrases
    overlap.sort((a, b) => b.length - a.length);

    // Find position in article text where anchor could be inserted
    let insertPosition = null;
    let bestAnchor = page.title || deriveTitleFromUrl(page.url);

    for (const phrase of overlap.slice(0, 5)) {
      const idx = articleText.toLowerCase().indexOf(phrase.toLowerCase());
      if (idx !== -1) {
        insertPosition = idx;
        bestAnchor = articleText.substring(idx, idx + phrase.length);
        break;
      }
    }

    // Check if link already exists in article
    const alreadyLinked = articleHtml.includes(page.url);

    suggestions.push({
      target_url: page.url,
      target_title: page.title,
      relevance_score: score,
      confidence: Math.min(1.0, score / 20),
      anchor_text: bestAnchor,
      insert_position: insertPosition,
      already_linked: alreadyLinked,
      matching_keywords: overlap.slice(0, 10),
    });
  }

  // Sort by relevance score descending
  suggestions.sort((a, b) => b.relevance_score - a.relevance_score);

  return suggestions;
}

function suggestKeywordLinks(articleText, existingPages) {
  const text = stripHtml(articleText);
  const tokens = tokenize(text);
  const articlePhrases = new Set([
    ...tokens.map(t => t.toLowerCase()),
    ...extractNgrams(tokens, 2).map(t => t.toLowerCase()),
    ...extractNgrams(tokens, 3).map(t => t.toLowerCase()),
  ]);

  const matches = [];

  for (const page of existingPages) {
    const pageTokens = tokenize(`${page.title || ''}`);
    const pageKeywords = [
      ...pageTokens.map(t => t.toLowerCase()),
      ...extractNgrams(pageTokens, 2).map(t => t.toLowerCase()),
      ...extractNgrams(pageTokens, 3).map(t => t.toLowerCase()),
    ];

    for (const kw of pageKeywords) {
      if (kw.length < 3) continue;
      if (articlePhrases.has(kw)) {
        // Find the position in original text
        const idx = text.toLowerCase().indexOf(kw.toLowerCase());
        matches.push({
          keyword: kw,
          target_url: page.url,
          target_title: page.title,
          position_in_text: idx !== -1 ? idx : null,
        });
      }
    }
  }

  // Deduplicate by keyword+url, keep first occurrence
  const seen = new Set();
  const unique = [];
  for (const m of matches) {
    const key = `${m.keyword}|${m.target_url}`;
    if (!seen.has(key)) {
      seen.add(key);
      unique.push(m);
    }
  }

  // Sort by keyword length descending (longer = more specific = better)
  unique.sort((a, b) => b.keyword.length - a.keyword.length);

  return unique;
}

// ---------------------------------------------------------------------------
// Request body parser
// ---------------------------------------------------------------------------
async function parseBody(request) {
  const contentType = request.headers.get('Content-Type') || '';
  if (!contentType.includes('application/json')) {
    throw new Error('Content-Type must be application/json');
  }
  const body = await request.json();
  return body;
}

// ---------------------------------------------------------------------------
// Worker entry point
// ---------------------------------------------------------------------------
export default {
  async fetch(request) {
    // CORS preflight
    if (request.method === 'OPTIONS') {
      return new Response(null, { status: 204, headers: cors() });
    }

    const ip = request.headers.get('CF-Connecting-IP') || 'unknown';
    const rl = checkRateLimit(ip);
    if (!rl.allowed) {
      return error('Rate limit exceeded. Max 20 requests per minute.', 429, {
        'Retry-After': String(rl.retryAfter),
        'X-RateLimit-Remaining': '0',
      });
    }
    const rlHeaders = { 'X-RateLimit-Remaining': String(rl.remaining) };

    const { pathname } = new URL(request.url);

    // GET / — API info
    if (pathname === '/' && request.method === 'GET') {
      return json({
        name: 'WP Internal Link Optimization API',
        version: '1.0.0',
        description: 'Analyze article content and get internal link suggestions for WordPress sites',
        _premium: {
          message: 'You are using the FREE tier. Upgrade to Pro for higher rate limits and priority support.',
          upgrade_url: 'https://rapidapi.com/miccho27-5OJaGGbBiO/api/wp-internal-link-api/pricing',
          plans: ['Free (100 req/mo)', 'Pro $9.99/mo (1,000 req)', 'Ultra $29.99/mo (10,000 req)'],
        },
        endpoints: {
          'POST /analyze': 'Analyze article HTML against sitemap or page list, return link suggestions with positions',
          'POST /suggest': 'Match article text keywords to existing URLs',
          'GET /health': 'Health check',
        },
      }, 200, rlHeaders);
    }

    // GET /health
    if (pathname === '/health' && request.method === 'GET') {
      return json({
        status: 'ok',
        timestamp: new Date().toISOString(),
        version: '1.0.0',
      }, 200, rlHeaders);
    }

    // POST /analyze
    if (pathname === '/analyze' && request.method === 'POST') {
      let body;
      try {
        body = await parseBody(request);
      } catch (e) {
        return error(e.message);
      }

      const { article_html, article_title, sitemap_url, pages } = body;

      if (!article_html) {
        return error('Missing required field: article_html');
      }
      if (!sitemap_url && !pages) {
        return error('Provide either sitemap_url or pages array');
      }

      try {
        let existingPages;

        if (sitemap_url) {
          // Fetch and parse sitemap
          const sitemapPages = await fetchSitemap(sitemap_url);
          if (sitemapPages.length === 0) {
            return error('No URLs found in sitemap', 422);
          }
          existingPages = sitemapPages;
        } else {
          // Validate pages array
          if (!Array.isArray(pages) || pages.length === 0) {
            return error('pages must be a non-empty array of {url, title} objects');
          }
          existingPages = pages.map(p => ({
            url: p.url,
            title: p.title || deriveTitleFromUrl(p.url),
            content: p.content || '',
          }));
        }

        const suggestions = analyzeLinks(article_html, article_title || '', existingPages);

        return json({
          article_title: article_title || null,
          total_pages_analyzed: existingPages.length,
          total_suggestions: suggestions.length,
          suggestions: suggestions.slice(0, 20),
        }, 200, rlHeaders);
      } catch (e) {
        return error(`Analysis failed: ${e.message}`, 502);
      }
    }

    // POST /suggest
    if (pathname === '/suggest' && request.method === 'POST') {
      let body;
      try {
        body = await parseBody(request);
      } catch (e) {
        return error(e.message);
      }

      const { article_text, pages } = body;

      if (!article_text) {
        return error('Missing required field: article_text');
      }
      if (!Array.isArray(pages) || pages.length === 0) {
        return error('pages must be a non-empty array of {url, title} objects');
      }

      try {
        const matches = suggestKeywordLinks(article_text, pages);

        return json({
          total_matches: matches.length,
          keyword_matches: matches.slice(0, 50),
        }, 200, rlHeaders);
      } catch (e) {
        return error(`Suggestion failed: ${e.message}`, 500);
      }
    }

    return error('Not found. Available endpoints: POST /analyze, POST /suggest, GET /health', 404);
  },
};
