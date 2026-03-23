const STOP_WORDS = new Set([
  'a', 'an', 'the', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for',
  'of', 'with', 'by', 'from', 'as', 'is', 'was', 'are', 'were', 'be',
  'been', 'being', 'have', 'has', 'had', 'do', 'does', 'did', 'will',
  'would', 'could', 'should', 'may', 'might', 'shall', 'can', 'need',
  'dare', 'ought', 'used', 'it', 'its', 'he', 'she', 'they', 'we',
  'you', 'i', 'me', 'him', 'her', 'us', 'them', 'my', 'your', 'his',
  'our', 'their', 'mine', 'yours', 'hers', 'ours', 'theirs', 'this',
  'that', 'these', 'those', 'what', 'which', 'who', 'whom', 'whose',
  'where', 'when', 'why', 'how', 'all', 'each', 'every', 'both',
  'few', 'more', 'most', 'other', 'some', 'such', 'no', 'nor', 'not',
  'only', 'own', 'same', 'so', 'than', 'too', 'very', 'just', 'because',
  'if', 'then', 'else', 'about', 'up', 'out', 'off', 'over', 'under',
  'again', 'further', 'once', 'here', 'there', 'also', 'into', 'through',
  'during', 'before', 'after', 'above', 'below', 'between', 'while',
  'since', 'until', 'against', 'among', 'within', 'without', 'along',
  'around', 'behind', 'beyond', 'near', 'upon', 'across', 'still',
  'get', 'got', 'make', 'made', 'go', 'going', 'come', 'take', 'took',
  'say', 'said', 'tell', 'told', 'think', 'thought', 'know', 'knew',
  'see', 'saw', 'want', 'give', 'gave', 'find', 'found', 'put',
  'thing', 'things', 'much', 'many', 'well', 'back', 'even', 'way',
  'new', 'now', 'one', 'two', 'first', 'last', 'long', 'great', 'little',
  'right', 'old', 'big', 'high', 'small', 'large', 'next', 'early',
  'young', 'important', 'let', 'like', 'people', 'time', 'year',
  'however', 'although', 'though', 'whether', 'yet', 'already',
  'really', 'almost', 'often', 'always', 'never', 'sometimes',
  'another', 'any', 'anything', 'anyone', 'anywhere', 'something',
  'someone', 'somewhere', 'nothing', 'nobody', 'nowhere',
  'been', 'being', 'having', 'doing', 'am', 'isn', 'aren', 'wasn',
  'weren', 'don', 'doesn', 'didn', 'won', 'wouldn', 'shouldn',
  'couldn', 'hadn', 'hasn', 'haven', 'mustn', 'needn',
]);

function tokenize(text) {
  return text.toLowerCase().replace(/[^a-z0-9\s-]/g, ' ').split(/\s+/)
    .filter(w => w.length > 2 && !STOP_WORDS.has(w) && !/^\d+$/.test(w));
}

export function extractKeywords(text, topN = 10) {
  if (!text || !text.trim()) return [];

  const words = tokenize(text);
  if (words.length === 0) return [];

  // Term frequency
  const tf = {};
  for (const w of words) {
    tf[w] = (tf[w] || 0) + 1;
  }

  // Simulate IDF using sentence-level document frequency
  const sentences = text.split(/[.!?]+/).filter(s => s.trim());
  const df = {};
  for (const sentence of sentences) {
    const sentWords = new Set(tokenize(sentence));
    for (const w of sentWords) {
      df[w] = (df[w] || 0) + 1;
    }
  }

  const totalSentences = Math.max(sentences.length, 1);
  const scores = {};
  for (const word in tf) {
    const idf = Math.log((totalSentences + 1) / ((df[word] || 0) + 1)) + 1;
    scores[word] = (tf[word] / words.length) * idf;
  }

  return Object.entries(scores)
    .sort((a, b) => b[1] - a[1])
    .slice(0, topN)
    .map(([word, score]) => ({
      word,
      frequency: tf[word],
      relevance: Math.round(score * 10000) / 10000,
    }));
}
