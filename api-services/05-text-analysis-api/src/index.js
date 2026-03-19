import { analyzeSentiment } from './sentiment.js';
import { extractKeywords } from './keywords.js';
import { analyzeReadability } from './readability.js';
import { detectLanguage } from './language.js';

const CORS_HEADERS = {
  'Access-Control-Allow-Origin': '*',
  'Access-Control-Allow-Methods': 'GET, POST, OPTIONS',
  'Access-Control-Allow-Headers': 'Content-Type, X-RapidAPI-Proxy-Secret, X-RapidAPI-Key',
  'Content-Type': 'application/json',
};

function json(data, status = 200) {
  if (status === 200 && typeof data === "object" && !Array.isArray(data)) {
    data._upgrade = { note: "Upgrade for higher limits & priority support", url: "https://rapidapi.com/miccho27-5OJaGGbBiO/api/text-analysis-api/pricing" };
  }
  return new Response(JSON.stringify(data), { status, headers: CORS_HEADERS });
}

function error(message, status = 400) {
  return json({ error: message }, status);
}

async function parseBody(request) {
  try {
    const body = await request.json();
    if (!body.text || typeof body.text !== 'string' || !body.text.trim()) {
      return { error: 'Missing or empty "text" field in request body' };
    }
    if (body.text.length > 100000) {
      return { error: 'Text exceeds maximum length of 100,000 characters' };
    }
    return { text: body.text };
  } catch {
    return { error: 'Invalid JSON in request body' };
  }
}

// Basic text metrics
function getBasicMetrics(text) {
  const charCount = text.length;
  const charCountNoSpaces = text.replace(/\s/g, '').length;
  const words = text.split(/\s+/).filter(w => w.length > 0);
  const wordCount = words.length;
  const sentences = text.split(/[.!?]+/).filter(s => s.trim().length > 0);
  const sentenceCount = sentences.length;
  const paragraphs = text.split(/\n\s*\n/).filter(p => p.trim().length > 0);
  const paragraphCount = Math.max(paragraphs.length, 1);
  const readingTime = Math.max(0.1, Math.round((wordCount / 238) * 100) / 100);
  const speakingTime = Math.max(0.1, Math.round((wordCount / 150) * 100) / 100);

  return {
    word_count: wordCount,
    character_count: charCount,
    character_count_no_spaces: charCountNoSpaces,
    sentence_count: sentenceCount,
    paragraph_count: paragraphCount,
    reading_time_minutes: readingTime,
    speaking_time_minutes: speakingTime,
  };
}

// TextRank-like extractive summarization
function extractSummarySentences(text, topN = 3) {
  const sentences = text.split(/(?<=[.!?])\s+/).filter(s => s.trim().length > 5);
  if (sentences.length <= topN) return sentences.map(s => s.trim());

  // Build word sets per sentence
  const tokenize = s => s.toLowerCase().replace(/[^a-z0-9\s]/g, '').split(/\s+/).filter(w => w.length > 2);
  const sentenceWords = sentences.map(tokenize);

  // Similarity matrix & score via simplified TextRank
  const scores = new Array(sentences.length).fill(1);
  for (let iter = 0; iter < 10; iter++) {
    const newScores = new Array(sentences.length).fill(0);
    for (let i = 0; i < sentences.length; i++) {
      for (let j = 0; j < sentences.length; j++) {
        if (i === j) continue;
        const common = sentenceWords[i].filter(w => sentenceWords[j].includes(w)).length;
        const denom = Math.log(sentenceWords[i].length + 1) + Math.log(sentenceWords[j].length + 1);
        if (denom > 0) {
          newScores[i] += (common / denom) * scores[j];
        }
      }
    }
    const max = Math.max(...newScores, 0.001);
    for (let i = 0; i < scores.length; i++) scores[i] = newScores[i] / max;
  }

  // Boost earlier sentences slightly
  for (let i = 0; i < scores.length; i++) {
    scores[i] *= (1 + 0.1 * (1 - i / sentences.length));
  }

  return scores
    .map((score, i) => ({ score, i }))
    .sort((a, b) => b.score - a.score)
    .slice(0, topN)
    .sort((a, b) => a.i - b.i) // preserve original order
    .map(x => sentences[x.i].trim());
}

// Route handlers
async function handleAnalyze(request) {
  const parsed = await parseBody(request);
  if (parsed.error) return error(parsed.error);
  const { text } = parsed;

  return json({
    ...getBasicMetrics(text),
    readability: analyzeReadability(text),
    sentiment: analyzeSentiment(text),
    language: detectLanguage(text),
    keywords: extractKeywords(text, 10),
    summary_sentences: extractSummarySentences(text, 3),
  });
}

async function handleSentiment(request) {
  const parsed = await parseBody(request);
  if (parsed.error) return error(parsed.error);
  return json(analyzeSentiment(parsed.text));
}

async function handleKeywords(request) {
  const parsed = await parseBody(request);
  if (parsed.error) return error(parsed.error);
  return json({ keywords: extractKeywords(parsed.text, 10) });
}

async function handleReadability(request) {
  const parsed = await parseBody(request);
  if (parsed.error) return error(parsed.error);
  return json(analyzeReadability(parsed.text));
}

export default {
  async fetch(request, env, ctx) {
    if (request.method === 'OPTIONS') {
      return new Response(null, { status: 204, headers: CORS_HEADERS });
    }

    const url = new URL(request.url);
    const path = url.pathname.replace(/\/+$/, '') || '/';

    if (request.method === 'GET' && (path === '/' || path === '/health')) {
      return json({
        service: 'Text Analysis API',
        
        _premium: {
          message: "You are using the FREE tier of Text Analysis API. Upgrade to Pro for higher rate limits, priority support, and advanced features.",
          upgrade_url: "https://rapidapi.com/miccho27-5OJaGGbBiO/api/text-analysis-api/pricing",
          plans: ["Pro ($5.99/mo)", "Ultra ($14.99/mo)", "Mega ($49.99/mo)"]
        },
        status: 'healthy',
        endpoints: ['POST /analyze', 'POST /sentiment', 'POST /keywords', 'POST /readability'],
      });
    }

    if (request.method !== 'POST') {
      return error('Method not allowed. Use POST.', 405);
    }

    switch (path) {
      case '/analyze': return handleAnalyze(request);
      case '/sentiment': return handleSentiment(request);
      case '/keywords': return handleKeywords(request);
      case '/readability': return handleReadability(request);
      default: return error('Not found', 404);
    }
  },
};
