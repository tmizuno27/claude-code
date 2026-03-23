// HTML parsing functions — all regex-based, no dependencies

function extractTitle(html) {
  const m = html.match(/<title[^>]*>([\s\S]*?)<\/title>/i);
  const text = m ? decodeEntities(m[1].trim()) : null;
  const length = text ? text.length : 0;
  return {
    text,
    length,
    optimal: length >= 30 && length <= 60,
  };
}

function extractMetaDescription(html) {
  const m = html.match(/<meta[^>]+name\s*=\s*["']description["'][^>]+content\s*=\s*["']([\s\S]*?)["'][^>]*>/i)
    || html.match(/<meta[^>]+content\s*=\s*["']([\s\S]*?)["'][^>]+name\s*=\s*["']description["'][^>]*>/i);
  const text = m ? decodeEntities(m[1].trim()) : null;
  const length = text ? text.length : 0;
  return {
    text,
    length,
    optimal: length >= 120 && length <= 160,
  };
}

function extractHeadings(html) {
  const result = { h1: [], h2: [], h3: [], h4: [], h5: [], h6: [] };
  const re = /<(h[1-6])[^>]*>([\s\S]*?)<\/\1>/gi;
  let m;
  while ((m = re.exec(html)) !== null) {
    const tag = m[1].toLowerCase();
    result[tag].push(stripTags(decodeEntities(m[2].trim())));
  }
  return {
    counts: {
      h1: result.h1.length, h2: result.h2.length, h3: result.h3.length,
      h4: result.h4.length, h5: result.h5.length, h6: result.h6.length,
    },
    texts: result,
  };
}

function extractImages(html) {
  const imgs = [];
  const re = /<img[^>]*>/gi;
  let m;
  while ((m = re.exec(html)) !== null) {
    const altMatch = m[0].match(/alt\s*=\s*["']([\s\S]*?)["']/i);
    const srcMatch = m[0].match(/src\s*=\s*["']([\s\S]*?)["']/i);
    imgs.push({
      src: srcMatch ? srcMatch[1] : null,
      alt: altMatch ? altMatch[1] : null,
      hasAlt: altMatch !== null && altMatch[1].trim().length > 0,
    });
  }
  return {
    total: imgs.length,
    withAlt: imgs.filter(i => i.hasAlt).length,
    withoutAlt: imgs.filter(i => !i.hasAlt).length,
    images: imgs,
  };
}

function extractLinks(html, baseUrl) {
  const links = { internal: 0, external: 0, nofollow: 0, all: [] };
  const re = /<a[^>]*>/gi;
  let baseHost;
  try { baseHost = new URL(baseUrl).hostname; } catch { baseHost = ''; }
  let m;
  while ((m = re.exec(html)) !== null) {
    const hrefMatch = m[0].match(/href\s*=\s*["']([\s\S]*?)["']/i);
    if (!hrefMatch) continue;
    const href = hrefMatch[1].trim();
    if (href.startsWith('#') || href.startsWith('javascript:') || href.startsWith('mailto:')) continue;
    const relMatch = m[0].match(/rel\s*=\s*["']([\s\S]*?)["']/i);
    const isNofollow = relMatch ? relMatch[1].toLowerCase().includes('nofollow') : false;
    let isExternal = false;
    try {
      const linkUrl = new URL(href, baseUrl);
      isExternal = linkUrl.hostname !== baseHost;
    } catch {
      isExternal = false;
    }
    if (isExternal) links.external++;
    else links.internal++;
    if (isNofollow) links.nofollow++;
    links.all.push({ href, external: isExternal, nofollow: isNofollow });
  }
  return {
    internal: links.internal,
    external: links.external,
    nofollow: links.nofollow,
    total: links.all.length,
  };
}

function extractCanonical(html) {
  const m = html.match(/<link[^>]+rel\s*=\s*["']canonical["'][^>]+href\s*=\s*["']([\s\S]*?)["'][^>]*>/i)
    || html.match(/<link[^>]+href\s*=\s*["']([\s\S]*?)["'][^>]+rel\s*=\s*["']canonical["'][^>]*>/i);
  return m ? m[1].trim() : null;
}

function extractRobotsMeta(html) {
  const m = html.match(/<meta[^>]+name\s*=\s*["']robots["'][^>]+content\s*=\s*["']([\s\S]*?)["'][^>]*>/i)
    || html.match(/<meta[^>]+content\s*=\s*["']([\s\S]*?)["'][^>]+name\s*=\s*["']robots["'][^>]*>/i);
  return m ? m[1].trim().toLowerCase() : null;
}

function extractOG(html) {
  const og = {};
  const re = /<meta[^>]+property\s*=\s*["'](og:[^"']+)["'][^>]+content\s*=\s*["']([\s\S]*?)["'][^>]*>/gi;
  const re2 = /<meta[^>]+content\s*=\s*["']([\s\S]*?)["'][^>]+property\s*=\s*["'](og:[^"']+)["'][^>]*>/gi;
  let m;
  while ((m = re.exec(html)) !== null) og[m[1]] = decodeEntities(m[2]);
  while ((m = re2.exec(html)) !== null) og[m[2]] = decodeEntities(m[1]);
  return Object.keys(og).length > 0 ? og : null;
}

function extractTwitterCard(html) {
  const tc = {};
  const re = /<meta[^>]+(?:name|property)\s*=\s*["'](twitter:[^"']+)["'][^>]+content\s*=\s*["']([\s\S]*?)["'][^>]*>/gi;
  const re2 = /<meta[^>]+content\s*=\s*["']([\s\S]*?)["'][^>]+(?:name|property)\s*=\s*["'](twitter:[^"']+)["'][^>]*>/gi;
  let m;
  while ((m = re.exec(html)) !== null) tc[m[1]] = decodeEntities(m[2]);
  while ((m = re2.exec(html)) !== null) tc[m[2]] = decodeEntities(m[1]);
  return Object.keys(tc).length > 0 ? tc : null;
}

function extractJsonLd(html) {
  const results = [];
  const re = /<script[^>]+type\s*=\s*["']application\/ld\+json["'][^>]*>([\s\S]*?)<\/script>/gi;
  let m;
  while ((m = re.exec(html)) !== null) {
    try { results.push(JSON.parse(m[1].trim())); } catch { /* skip invalid */ }
  }
  return results.length > 0 ? results : null;
}

function extractWordCount(html) {
  const body = html.replace(/<script[\s\S]*?<\/script>/gi, '')
    .replace(/<style[\s\S]*?<\/style>/gi, '')
    .replace(/<[^>]+>/g, ' ')
    .replace(/\s+/g, ' ')
    .trim();
  const words = body.split(/\s+/).filter(w => w.length > 0);
  return words.length;
}

function extractLanguage(html) {
  const m = html.match(/<html[^>]+lang\s*=\s*["']([^"']+)["']/i);
  return m ? m[1].trim() : null;
}

function extractViewport(html) {
  const m = html.match(/<meta[^>]+name\s*=\s*["']viewport["'][^>]+content\s*=\s*["']([\s\S]*?)["'][^>]*>/i)
    || html.match(/<meta[^>]+content\s*=\s*["']([\s\S]*?)["'][^>]+name\s*=\s*["']viewport["'][^>]*>/i);
  return { present: m !== null, content: m ? m[1].trim() : null };
}

function extractFavicon(html) {
  const m = html.match(/<link[^>]+rel\s*=\s*["'](?:shortcut )?icon["'][^>]+href\s*=\s*["']([\s\S]*?)["'][^>]*>/i)
    || html.match(/<link[^>]+href\s*=\s*["']([\s\S]*?)["'][^>]+rel\s*=\s*["'](?:shortcut )?icon["'][^>]*>/i);
  return { present: m !== null, href: m ? m[1].trim() : null };
}

function extractHreflang(html) {
  const tags = [];
  const re = /<link[^>]+rel\s*=\s*["']alternate["'][^>]+hreflang\s*=\s*["']([^"']+)["'][^>]+href\s*=\s*["']([^"']+)["'][^>]*>/gi;
  let m;
  while ((m = re.exec(html)) !== null) tags.push({ lang: m[1], href: m[2] });
  // Also match reversed attribute order
  const re2 = /<link[^>]+hreflang\s*=\s*["']([^"']+)["'][^>]+href\s*=\s*["']([^"']+)["'][^>]*rel\s*=\s*["']alternate["'][^>]*>/gi;
  while ((m = re2.exec(html)) !== null) tags.push({ lang: m[1], href: m[2] });
  return tags.length > 0 ? tags : null;
}

function calculateSeoScore(data) {
  const checks = [];
  const add = (name, pass, weight = 1) => checks.push({ name, pass, weight });

  // Title checks (15 pts)
  add('Has title', !!data.title.text, 5);
  add('Title optimal length (30-60)', data.title.optimal, 5);
  add('Title not too long (≤70)', data.title.length <= 70, 5);

  // Meta description (15 pts)
  add('Has meta description', !!data.metaDescription.text, 5);
  add('Description optimal length (120-160)', data.metaDescription.optimal, 5);
  add('Description not empty', data.metaDescription.length > 0, 5);

  // Headings (15 pts)
  add('Has H1', data.headings.counts.h1 > 0, 5);
  add('Single H1', data.headings.counts.h1 === 1, 5);
  add('Has H2 subheadings', data.headings.counts.h2 > 0, 5);

  // Images (10 pts)
  add('All images have alt text', data.images.total === 0 || data.images.withoutAlt === 0, 5);
  add('Has images', data.images.total > 0, 5);

  // Links (5 pts)
  add('Has internal links', data.links.internal > 0, 5);

  // Technical (25 pts)
  add('Has canonical URL', !!data.canonical, 5);
  add('Has viewport meta', data.viewport.present, 5);
  add('Has favicon', data.favicon.present, 5);
  add('Has language attribute', !!data.language, 5);
  add('Not blocked by robots', data.robotsMeta !== 'noindex', 5);

  // Social (10 pts)
  add('Has Open Graph tags', !!data.openGraph, 5);
  add('Has Twitter Card tags', !!data.twitterCard, 5);

  // Structured data (5 pts)
  add('Has JSON-LD structured data', !!data.jsonLd, 5);

  const maxScore = checks.reduce((s, c) => s + c.weight, 0);
  const earned = checks.reduce((s, c) => s + (c.pass ? c.weight : 0), 0);
  const score = Math.round((earned / maxScore) * 100);

  return { score, maxPoints: maxScore, earnedPoints: earned, checks };
}

// Helpers
function decodeEntities(str) {
  return str.replace(/&amp;/g, '&').replace(/&lt;/g, '<').replace(/&gt;/g, '>')
    .replace(/&quot;/g, '"').replace(/&#39;/g, "'").replace(/&#x27;/g, "'")
    .replace(/&#(\d+);/g, (_, n) => String.fromCharCode(n));
}

function stripTags(str) {
  return str.replace(/<[^>]+>/g, '').trim();
}

export {
  extractTitle, extractMetaDescription, extractHeadings, extractImages,
  extractLinks, extractCanonical, extractRobotsMeta, extractOG,
  extractTwitterCard, extractJsonLd, extractWordCount, extractLanguage,
  extractViewport, extractFavicon, extractHreflang, calculateSeoScore,
};
