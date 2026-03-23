/**
 * Internal Link Analysis Engine
 * Ported from nambei-oyaji.com/scripts/content/internal_linker.py
 */

import type { WPPost, LinkSuggestion, OrphanPost, PostLinkStats } from "./types";

// Japanese stop words
const STOP_WORDS = new Set([
  "の", "に", "は", "を", "が", "で", "と", "て", "た", "し",
  "な", "も", "や", "か", "から", "まで", "より", "へ", "ね",
  "よ", "わ", "さ", "れ", "る", "する", "ある", "いる", "なる",
  "こと", "もの", "ため", "それ", "これ", "あの", "その", "この",
  "など", "ずつ", "だけ", "でも", "ほど", "まま", "ながら",
  "について", "として", "による", "において", "における",
  // English stop words
  "the", "a", "an", "is", "are", "was", "were", "be", "been",
  "being", "have", "has", "had", "do", "does", "did", "will",
  "would", "could", "should", "may", "might", "can", "shall",
  "to", "of", "in", "for", "on", "with", "at", "by", "from",
  "as", "into", "through", "during", "before", "after", "and",
  "but", "or", "not", "no", "if", "then", "than", "so", "it",
  "this", "that", "these", "those", "my", "your", "his", "her",
]);

function stripHtml(html: string): string {
  return html.replace(/<[^>]+>/g, " ").trim();
}

function tokenize(text: string): string[] {
  const cleaned = text.replace(/[^\w\u3000-\u9fff\uff00-\uffef]/g, " ");
  return cleaned
    .split(/\s+/)
    .map((t) => t.trim())
    .filter((t) => t.length >= 2 && !STOP_WORDS.has(t.toLowerCase()));
}

function extractNgrams(tokens: string[], n: number): string[] {
  const ngrams: string[] = [];
  for (let i = 0; i <= tokens.length - n; i++) {
    ngrams.push(tokens.slice(i, i + n).join(" "));
  }
  return ngrams;
}

function buildKeywordSet(title: string, contentHtml: string): Set<string> {
  const titleText = stripHtml(title);
  const bodyText = stripHtml(contentHtml);
  const combined = `${titleText} ${bodyText}`;
  const tokens = tokenize(combined);
  const unigrams = new Set(tokens);
  const bigrams = new Set(extractNgrams(tokens, 2));
  return new Set([...unigrams, ...bigrams]);
}

function computeRelevance(a: Set<string>, b: Set<string>): number {
  let count = 0;
  for (const kw of a) {
    if (b.has(kw)) count++;
  }
  return count;
}

function isAlreadyLinked(contentHtml: string, targetUrl: string): boolean {
  return contentHtml.includes(targetUrl);
}

// Build detailed link graph with title references
function buildDetailedLinkGraph(
  posts: { id: number; title: string; url: string; content: string }[]
): Map<number, { incoming: number; outgoing: number; linked_from: string[]; links_to: string[] }> {
  const graph = new Map<number, { incoming: number; outgoing: number; linked_from: string[]; links_to: string[] }>();

  for (const p of posts) {
    graph.set(p.id, { incoming: 0, outgoing: 0, linked_from: [], links_to: [] });
  }

  for (const p of posts) {
    for (const other of posts) {
      if (p.id === other.id) continue;
      if (p.content.includes(other.url)) {
        graph.get(p.id)!.outgoing++;
        graph.get(p.id)!.links_to.push(other.title);
        graph.get(other.id)!.incoming++;
        graph.get(other.id)!.linked_from.push(p.title);
      }
    }
  }

  return graph;
}

export interface AnalysisResult {
  suggestions: LinkSuggestion[];
  orphanPosts: OrphanPost[];
  postStats: PostLinkStats[];
  totalPosts: number;
}

export function analyzeInternalLinks(
  posts: WPPost[],
  topN: number = 3
): AnalysisResult {
  // Build metadata
  const meta = posts.map((post) => ({
    id: post.id,
    title: stripHtml(post.title.rendered),
    url: post.link,
    content: post.content.rendered,
    keywords: buildKeywordSet(post.title.rendered, post.content.rendered),
  }));

  // Compute pairwise relevance
  const relevance = new Map<string, number>();
  for (let i = 0; i < meta.length; i++) {
    for (let j = i + 1; j < meta.length; j++) {
      const score = computeRelevance(meta[i].keywords, meta[j].keywords);
      relevance.set(`${i}-${j}`, score);
    }
  }

  // Generate suggestions
  const suggestions: LinkSuggestion[] = [];

  for (let idx = 0; idx < meta.length; idx++) {
    const post = meta[idx];
    const scored: { score: number; jdx: number }[] = [];

    for (let jdx = 0; jdx < meta.length; jdx++) {
      if (idx === jdx) continue;
      const key =
        idx < jdx ? `${idx}-${jdx}` : `${jdx}-${idx}`;
      const score = relevance.get(key) ?? 0;
      if (score <= 0) continue;

      const linked = isAlreadyLinked(post.content, meta[jdx].url);
      scored.push({ score, jdx });

      if (linked) continue; // still count but don't suggest
    }

    scored.sort((a, b) => b.score - a.score);

    for (const { score, jdx } of scored.slice(0, topN)) {
      const linked = isAlreadyLinked(post.content, meta[jdx].url);
      suggestions.push({
        source_post_id: post.id,
        source_title: post.title,
        source_url: post.url,
        target_post_id: meta[jdx].id,
        target_title: meta[jdx].title,
        target_url: meta[jdx].url,
        relevance_score: score,
        already_linked: linked,
      });
    }
  }

  // Build detailed link graph
  const linkGraph = buildDetailedLinkGraph(meta);
  const orphanPosts: OrphanPost[] = [];
  const postStats: PostLinkStats[] = [];

  for (const [id, counts] of linkGraph) {
    const m = meta.find((p) => p.id === id)!;
    postStats.push({
      post_id: id,
      title: m.title,
      url: m.url,
      incoming_links: counts.incoming,
      outgoing_links: counts.outgoing,
      linked_from: counts.linked_from,
      links_to: counts.links_to,
    });
    if (counts.incoming === 0) {
      orphanPosts.push({
        post_id: id,
        title: m.title,
        url: m.url,
        incoming_links: counts.incoming,
        outgoing_links: counts.outgoing,
      });
    }
  }

  // Sort postStats: orphans first, then by incoming ascending
  postStats.sort((a, b) => a.incoming_links - b.incoming_links);

  return {
    suggestions: suggestions.filter((s) => !s.already_linked),
    orphanPosts,
    postStats,
    totalPosts: posts.length,
  };
}

// Build HTML block for related links (used when applying suggestions)
export function buildRelatedLinksHtml(
  relatedPosts: { title: string; url: string }[]
): string {
  const items = relatedPosts
    .map((p) => `  <li><a href="${p.url}">${p.title}</a></li>`)
    .join("\n");
  return `\n<!-- wp-linker-internal-links -->\n<div class="related-articles">\n<h3>Related Articles</h3>\n<ul>\n${items}\n</ul>\n</div>\n`;
}
