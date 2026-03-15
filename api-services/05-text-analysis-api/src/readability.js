// Syllable counting heuristic for English
function countSyllables(word) {
  word = word.toLowerCase().replace(/[^a-z]/g, '');
  if (word.length <= 2) return 1;

  // Common suffixes that don't add syllables
  word = word.replace(/(?:es|ed)$/, '') || word;

  const vowelGroups = word.match(/[aeiouy]+/g);
  let count = vowelGroups ? vowelGroups.length : 1;

  // Silent e at end
  if (word.endsWith('e') && count > 1) count--;
  // le at end usually is a syllable
  if (word.endsWith('le') && word.length > 2 && !/[aeiouy]/.test(word[word.length - 3])) count++;

  return Math.max(1, count);
}

export function analyzeReadability(text) {
  if (!text || !text.trim()) {
    return {
      flesch_kincaid_grade: 0,
      flesch_reading_ease: 0,
      avg_words_per_sentence: 0,
      avg_syllables_per_word: 0,
      total_syllables: 0,
    };
  }

  const sentences = text.split(/[.!?]+/).filter(s => s.trim().length > 0);
  const words = text.replace(/[^a-zA-Z\s]/g, ' ').split(/\s+/).filter(w => w.length > 0);
  const sentenceCount = Math.max(sentences.length, 1);
  const wordCount = Math.max(words.length, 1);

  let totalSyllables = 0;
  for (const w of words) {
    totalSyllables += countSyllables(w);
  }

  const avgWordsPerSentence = wordCount / sentenceCount;
  const avgSyllablesPerWord = totalSyllables / wordCount;

  // Flesch-Kincaid Grade Level
  const grade = 0.39 * avgWordsPerSentence + 11.8 * avgSyllablesPerWord - 15.59;

  // Flesch Reading Ease
  const ease = 206.835 - 1.015 * avgWordsPerSentence - 84.6 * avgSyllablesPerWord;

  return {
    flesch_kincaid_grade: Math.round(Math.max(0, grade) * 100) / 100,
    flesch_reading_ease: Math.round(Math.max(0, Math.min(100, ease)) * 100) / 100,
    avg_words_per_sentence: Math.round(avgWordsPerSentence * 100) / 100,
    avg_syllables_per_word: Math.round(avgSyllablesPerWord * 100) / 100,
    total_syllables: totalSyllables,
  };
}
