// Common words for top 10 languages
const LANGUAGE_PROFILES = {
  en: { name: 'English', words: new Set(['the', 'is', 'and', 'of', 'to', 'in', 'that', 'it', 'for', 'was', 'on', 'are', 'with', 'as', 'at', 'be', 'this', 'have', 'from', 'not', 'but', 'they', 'which', 'you', 'an', 'can', 'had', 'were', 'all', 'been']) },
  es: { name: 'Spanish', words: new Set(['de', 'la', 'el', 'en', 'y', 'que', 'los', 'del', 'las', 'un', 'por', 'con', 'una', 'su', 'para', 'es', 'al', 'lo', 'como', 'pero', 'sus', 'le', 'ha', 'me', 'si', 'sin', 'sobre', 'este', 'ya', 'entre']) },
  fr: { name: 'French', words: new Set(['le', 'de', 'la', 'les', 'et', 'en', 'un', 'une', 'du', 'est', 'que', 'des', 'il', 'dans', 'pas', 'ne', 'ce', 'qui', 'sur', 'pour', 'par', 'au', 'avec', 'sont', 'mais', 'nous', 'cette', 'ont', 'ses', 'aussi']) },
  de: { name: 'German', words: new Set(['der', 'die', 'und', 'in', 'den', 'von', 'zu', 'das', 'mit', 'sich', 'des', 'auf', 'ist', 'ein', 'eine', 'dem', 'nicht', 'als', 'auch', 'es', 'an', 'aus', 'er', 'hat', 'dass', 'sie', 'nach', 'bei', 'um', 'noch']) },
  pt: { name: 'Portuguese', words: new Set(['de', 'da', 'do', 'que', 'em', 'os', 'as', 'na', 'no', 'um', 'uma', 'com', 'para', 'por', 'mais', 'ao', 'foi', 'dos', 'das', 'se', 'como', 'mas', 'sua', 'seu', 'tem', 'nos', 'nas', 'pelo', 'pela', 'quando']) },
  it: { name: 'Italian', words: new Set(['di', 'che', 'il', 'la', 'in', 'un', 'del', 'per', 'una', 'con', 'non', 'si', 'da', 'le', 'dei', 'al', 'sono', 'ha', 'anche', 'gli', 'lo', 'nel', 'alla', 'della', 'questo', 'suo', 'era', 'nella', 'tutto', 'dal']) },
  nl: { name: 'Dutch', words: new Set(['de', 'het', 'van', 'en', 'een', 'in', 'is', 'dat', 'op', 'te', 'zijn', 'voor', 'met', 'die', 'niet', 'aan', 'er', 'maar', 'om', 'ook', 'als', 'bij', 'nog', 'uit', 'wel', 'kan', 'naar', 'dan', 'wat', 'werd']) },
  ja: { name: 'Japanese', chars: /[\u3040-\u309F\u30A0-\u30FF\u4E00-\u9FFF]/ },
  zh: { name: 'Chinese', chars: /[\u4E00-\u9FFF\u3400-\u4DBF]/ },
  ko: { name: 'Korean', chars: /[\uAC00-\uD7AF\u1100-\u11FF]/ },
};

export function detectLanguage(text) {
  if (!text || !text.trim()) {
    return { language: 'unknown', language_name: 'Unknown', confidence: 0 };
  }

  // Check CJK character-based languages first
  const totalChars = text.replace(/\s/g, '').length || 1;

  for (const lang of ['ja', 'zh', 'ko']) {
    const profile = LANGUAGE_PROFILES[lang];
    const matches = (text.match(profile.chars) || []).length;
    const ratio = matches / totalChars;
    if (ratio > 0.3) {
      // Distinguish Japanese from Chinese: check for kana
      if (lang === 'zh' && /[\u3040-\u309F\u30A0-\u30FF]/.test(text)) {
        return { language: 'ja', language_name: 'Japanese', confidence: Math.round(Math.min(ratio * 1.2, 1) * 1000) / 1000 };
      }
      return { language: lang, language_name: profile.name, confidence: Math.round(Math.min(ratio * 1.2, 1) * 1000) / 1000 };
    }
  }

  // Word-based detection for European languages
  const words = text.toLowerCase().replace(/[^a-z\s]/g, ' ').split(/\s+/).filter(w => w.length > 0);
  if (words.length === 0) {
    return { language: 'unknown', language_name: 'Unknown', confidence: 0 };
  }

  const scores = {};
  for (const [lang, profile] of Object.entries(LANGUAGE_PROFILES)) {
    if (profile.chars) continue; // skip CJK
    let matches = 0;
    for (const w of words) {
      if (profile.words.has(w)) matches++;
    }
    scores[lang] = matches / words.length;
  }

  const sorted = Object.entries(scores).sort((a, b) => b[1] - a[1]);
  if (sorted.length === 0 || sorted[0][1] === 0) {
    return { language: 'unknown', language_name: 'Unknown', confidence: 0 };
  }

  const [lang, score] = sorted[0];
  return {
    language: lang,
    language_name: LANGUAGE_PROFILES[lang].name,
    confidence: Math.round(Math.min(score * 3, 1) * 1000) / 1000,
  };
}
