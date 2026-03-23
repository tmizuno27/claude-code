// AFINN-style sentiment lexicon (200+ words)
const LEXICON = {
  // Strong positive (4-5)
  outstanding: 5, excellent: 5, superb: 5, amazing: 5, wonderful: 5,
  fantastic: 5, brilliant: 5, exceptional: 5, magnificent: 5, perfect: 5,
  // Positive (3-4)
  love: 3, great: 3, happy: 3, beautiful: 3, awesome: 4, best: 3,
  good: 3, nice: 3, enjoy: 3, pleasant: 3, delightful: 4, impressive: 4,
  remarkable: 4, terrific: 4, marvelous: 4, fabulous: 4, splendid: 4,
  // Moderate positive (1-2)
  like: 2, fine: 2, glad: 2, pleased: 2, satisfied: 2, helpful: 2,
  useful: 2, interesting: 2, fun: 2, cool: 1, okay: 1, decent: 1,
  agree: 1, accept: 1, adequate: 1, calm: 1, comfortable: 2,
  convenient: 2, creative: 2, eager: 2, easy: 1, effective: 2,
  efficient: 2, elegant: 2, encouraging: 2, exciting: 3, fair: 1,
  faithful: 2, familiar: 1, favorable: 2, fortunate: 2, free: 1,
  friendly: 2, generous: 2, gentle: 2, genuine: 2, graceful: 2,
  grateful: 2, healthy: 2, honest: 2, hopeful: 2, humorous: 2,
  ideal: 2, innovative: 2, inspiring: 3, joyful: 3, kind: 2,
  laughing: 2, lively: 2, logical: 1, loyal: 2, lucky: 2,
  meaningful: 2, neat: 1, noble: 2, optimistic: 2, peaceful: 2,
  polite: 2, popular: 1, positive: 2, powerful: 2, pretty: 1,
  productive: 2, proud: 2, pure: 1, quick: 1, quiet: 1,
  ready: 1, reasonable: 1, relaxed: 2, reliable: 2, remarkable: 3,
  respectful: 2, safe: 1, secure: 2, simple: 1, sincere: 2,
  smart: 2, smooth: 1, stable: 1, strong: 2, successful: 3,
  suitable: 1, super: 3, supportive: 2, sure: 1, sweet: 2,
  talented: 2, thankful: 2, thriving: 3, top: 2, tremendous: 3,
  trustworthy: 2, upbeat: 2, valuable: 2, vibrant: 2, victorious: 3,
  warm: 2, welcome: 2, winning: 3, wise: 2, worthy: 2,
  // Negative (-1 to -2)
  bad: -3, sad: -2, boring: -2, poor: -2, wrong: -2, ugly: -2,
  annoying: -2, difficult: -1, hard: -1, problem: -2, issue: -1,
  fail: -2, failure: -2, miss: -1, lost: -1, lose: -2,
  slow: -1, weak: -2, tired: -2, sick: -2, broken: -2,
  confused: -2, worried: -1, sorry: -1, afraid: -2, anxious: -2,
  awkward: -1, bitter: -2, blame: -2, bored: -2, clumsy: -1,
  cold: -1, complaint: -2, complex: -1, costly: -1, crazy: -1,
  critical: -1, cruel: -3, damage: -2, danger: -2, dark: -1,
  delay: -1, deny: -1, dirty: -2, disappoint: -2, dislike: -2,
  doubt: -1, dull: -2, empty: -1, error: -2, expensive: -1,
  fake: -2, fault: -2, fear: -2, fool: -2, guilty: -2,
  harm: -2, harsh: -2, heavy: -1, helpless: -2, hopeless: -3,
  hostile: -2, hurt: -2, ignorant: -2, illegal: -2, immature: -1,
  impatient: -1, impossible: -2, inferior: -2, insecure: -2, jealous: -2,
  lazy: -2, lonely: -2, messy: -1, mistake: -2, miserable: -3,
  moody: -1, nasty: -3, negative: -2, nervous: -1, noisy: -1,
  // Strong negative (-3 to -5)
  terrible: -4, horrible: -4, awful: -4, hate: -4, worst: -5,
  disgusting: -4, dreadful: -4, atrocious: -5, abysmal: -5, pathetic: -4,
  disaster: -4, catastrophe: -5, destroy: -3, ruin: -3, toxic: -3,
  violent: -3, abuse: -3, murder: -4, kill: -3, death: -3,
  die: -3, dead: -3, agony: -4, anger: -3, angry: -3,
  rage: -4, furious: -4, outrage: -4, scam: -3, fraud: -3,
  steal: -3, lie: -3, cheat: -3, betray: -3, abandon: -3,
  reject: -2, suffer: -3, pain: -3, cry: -2, scream: -2,
  panic: -3, terror: -4, horror: -4, nightmare: -3, hell: -4,
  damn: -2, stupid: -3, idiot: -3, trash: -3, waste: -2,
  useless: -3, worthless: -4, pointless: -2, ridiculous: -2, absurd: -2,
};

// Negation words that flip sentiment
const NEGATIONS = new Set([
  'not', "don't", "doesn't", "didn't", "won't", "wouldn't", "shouldn't",
  "couldn't", "isn't", "aren't", "wasn't", "weren't", 'no', 'never',
  'neither', 'nobody', 'nothing', 'nowhere', 'nor', 'cannot', "can't",
]);

// Intensifiers
const INTENSIFIERS = {
  very: 1.5, really: 1.5, extremely: 2.0, absolutely: 2.0,
  incredibly: 1.8, highly: 1.5, totally: 1.5, completely: 1.5,
  utterly: 2.0, somewhat: 0.5, slightly: 0.5, barely: 0.3,
  hardly: 0.3, quite: 1.2, rather: 0.8, fairly: 0.8,
};

export function analyzeSentiment(text) {
  if (!text || !text.trim()) {
    return { sentiment: 'neutral', score: 0, confidence: 0 };
  }

  const words = text.toLowerCase().replace(/[^a-z'\s-]/g, ' ').split(/\s+/).filter(Boolean);
  let totalScore = 0;
  let scoredWords = 0;
  let negated = false;
  let intensifier = 1.0;

  for (let i = 0; i < words.length; i++) {
    const word = words[i];

    if (NEGATIONS.has(word)) {
      negated = true;
      continue;
    }

    if (INTENSIFIERS[word]) {
      intensifier = INTENSIFIERS[word];
      continue;
    }

    if (LEXICON[word] !== undefined) {
      let score = LEXICON[word] * intensifier;
      if (negated) {
        score *= -0.75;
        negated = false;
      }
      totalScore += score;
      scoredWords++;
    } else {
      negated = false;
    }
    intensifier = 1.0;
  }

  const normalizedScore = scoredWords > 0 ? totalScore / scoredWords : 0;
  const clampedScore = Math.max(-1, Math.min(1, normalizedScore / 5));
  const confidence = Math.min(1, scoredWords / Math.max(1, words.length) * 3);

  let sentiment;
  if (clampedScore > 0.05) sentiment = 'positive';
  else if (clampedScore < -0.05) sentiment = 'negative';
  else sentiment = 'neutral';

  return {
    sentiment,
    score: Math.round(clampedScore * 1000) / 1000,
    confidence: Math.round(confidence * 1000) / 1000,
  };
}
