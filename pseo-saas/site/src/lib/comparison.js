import { getFeatureLabel } from './tools';

function hashStr(str) {
  let hash = 0;
  for (let i = 0; i < str.length; i++) {
    hash = ((hash << 5) - hash) + str.charCodeAt(i);
    hash |= 0;
  }
  return Math.abs(hash);
}

function pick(arr, hash) {
  return arr[hash % arr.length];
}

function computeOverallScore(tool) {
  const g2 = tool.g2_rating || 0;
  const cap = tool.capterra_rating || 0;
  return ((g2 + cap) / 2).toFixed(1);
}

function featureCount(tool) {
  if (!tool.features) return 0;
  return Object.values(tool.features).filter(Boolean).length;
}

function pricingValue(tool) {
  const match = (tool.pricing_starts || '').match(/\d+/);
  return match ? parseInt(match[0]) : 0;
}

export function generateComparisonContent(toolA, toolB) {
  const seed = hashStr(toolA.slug + toolB.slug);
  const scoreA = parseFloat(computeOverallScore(toolA));
  const scoreB = parseFloat(computeOverallScore(toolB));
  const featA = featureCount(toolA);
  const featB = featureCount(toolB);
  const priceA = pricingValue(toolA);
  const priceB = pricingValue(toolB);

  const winner = scoreA > scoreB ? toolA : scoreB > scoreA ? toolB : (featA >= featB ? toolA : toolB);
  const loser = winner.slug === toolA.slug ? toolB : toolA;

  const verdictReasons = [];
  if (computeOverallScore(winner) > computeOverallScore(loser)) {
    verdictReasons.push(`higher user ratings (${computeOverallScore(winner)} vs ${computeOverallScore(loser)})`);
  }
  if (featureCount(winner) > featureCount(loser)) {
    verdictReasons.push(`more features (${featureCount(winner)} vs ${featureCount(loser)})`);
  }
  if (pricingValue(winner) < pricingValue(loser) && pricingValue(winner) > 0) {
    verdictReasons.push('more competitive pricing');
  }
  if (winner.free_plan) {
    verdictReasons.push('availability of a free plan');
  }
  if (verdictReasons.length === 0) {
    verdictReasons.push('overall value and user satisfaction');
  }

  const introVariants = [
    `Choosing between ${toolA.name} and ${toolB.name} is a common dilemma for professionals looking for the right solution. Both platforms have carved out significant market positions, but they take notably different approaches to solving similar problems. In this comprehensive comparison, we analyze every aspect that matters — from features and pricing to user experience and support — so you can make an informed decision.`,
    `${toolA.name} and ${toolB.name} are two of the most talked-about solutions in the ${getCategoryName(toolA)} space. Whether you are a small business owner, a growing startup, or an established enterprise, picking the right tool can significantly impact your workflow and results. Let us break down how these two platforms compare across the metrics that matter most.`,
    `The debate between ${toolA.name} and ${toolB.name} comes up frequently in online communities and industry forums. Both tools bring unique strengths to the table, and the best choice depends heavily on your specific needs, budget, and technical requirements. We have put together this detailed analysis to help you cut through the marketing noise and focus on what each platform actually delivers.`,
  ];

  const pricingAnalysis = generatePricingSection(toolA, toolB, priceA, priceB);
  const featureAnalysis = generateFeatureSection(toolA, toolB);
  const useCaseAnalysis = generateUseCaseSection(toolA, toolB, seed);
  const verdict = generateVerdict(winner, loser, verdictReasons, toolA, toolB);
  const faqs = generateFAQs(toolA, toolB, winner, scoreA, scoreB);

  return {
    intro: pick(introVariants, seed),
    pricingAnalysis,
    featureAnalysis,
    useCaseAnalysis,
    verdict,
    faqs,
    winner,
    scoreA,
    scoreB,
    overallA: computeOverallScore(toolA),
    overallB: computeOverallScore(toolB),
  };
}

function getCategoryName(tool) {
  const map = {
    'email-marketing': 'email marketing',
    'ai-writing': 'AI writing',
    'ai-image': 'AI image generation',
    'ai-chatbot': 'AI chatbot',
    'ai-coding': 'AI coding',
    'ai-video': 'AI video',
    'ai-audio': 'AI audio',
    'ai-nocode': 'no-code automation',
    'ai-seo': 'SEO and marketing',
    'ai-translation': 'translation',
    'ai-design': 'AI design',
    'ai-productivity': 'productivity',
  };
  return map[tool.category] || 'software';
}

function generatePricingSection(toolA, toolB, priceA, priceB) {
  let analysis = `When it comes to pricing, `;
  if (priceA === 0 && priceB === 0) {
    analysis += `both ${toolA.name} and ${toolB.name} offer flexible pricing models. `;
  } else if (priceA < priceB) {
    analysis += `${toolA.name} offers a more budget-friendly entry point at ${toolA.pricing_starts}, compared to ${toolB.name}'s starting price of ${toolB.pricing_starts}. `;
  } else if (priceB < priceA) {
    analysis += `${toolB.name} comes in at a lower starting price of ${toolB.pricing_starts}, while ${toolA.name} begins at ${toolA.pricing_starts}. `;
  } else {
    analysis += `both platforms start at similar price points (${toolA.pricing_starts}). `;
  }

  if (toolA.free_plan && toolB.free_plan) {
    analysis += `Both platforms offer free plans, which is great for testing before committing. ${toolA.name}'s free tier and ${toolB.name}'s free tier each have their own limitations, so it is worth evaluating both to see which free offering better matches your initial needs.`;
  } else if (toolA.free_plan) {
    analysis += `${toolA.name} has a notable advantage here with its free plan, allowing you to get started without any financial commitment. ${toolB.name} does not currently offer a free tier, which means you will need to pay from day one.`;
  } else if (toolB.free_plan) {
    analysis += `${toolB.name} stands out by offering a free plan, giving you a risk-free way to explore the platform. ${toolA.name} requires a paid subscription from the start.`;
  } else {
    analysis += `Neither platform offers a free plan, so you will need to budget for at least the starting tier from the beginning. Be sure to take advantage of any trial periods they may offer.`;
  }

  return analysis;
}

function generateFeatureSection(toolA, toolB) {
  const allFeatures = new Set([
    ...Object.keys(toolA.features || {}),
    ...Object.keys(toolB.features || {}),
  ]);

  const onlyA = [];
  const onlyB = [];
  const both = [];

  for (const f of allFeatures) {
    const hasA = toolA.features?.[f];
    const hasB = toolB.features?.[f];
    if (hasA && hasB) both.push(f);
    else if (hasA) onlyA.push(f);
    else if (hasB) onlyB.push(f);
  }

  let text = `Both ${toolA.name} and ${toolB.name} share a solid foundation of core features including ${both.slice(0, 4).map(getFeatureLabel).join(', ')}. `;

  if (onlyA.length > 0) {
    text += `Where ${toolA.name} pulls ahead is with exclusive access to ${onlyA.map(getFeatureLabel).join(' and ')}, which can be a deciding factor for teams that rely on ${onlyA.length > 1 ? 'these capabilities' : 'this capability'}. `;
  }

  if (onlyB.length > 0) {
    text += `On the other hand, ${toolB.name} uniquely offers ${onlyB.map(getFeatureLabel).join(' and ')}, giving it an edge for users who prioritize ${onlyB.length > 1 ? 'these areas' : 'this area'}. `;
  }

  if (onlyA.length === 0 && onlyB.length === 0) {
    text += `Interestingly, both platforms offer nearly identical feature sets. The difference lies more in the implementation quality and depth of each feature rather than feature availability itself. `;
  }

  text += `\n\nLooking at user ratings, ${toolA.name} holds a ${toolA.g2_rating} on G2 and ${toolA.capterra_rating} on Capterra, while ${toolB.name} scores ${toolB.g2_rating} on G2 and ${toolB.capterra_rating} on Capterra. These ratings reflect real user experiences and can indicate differences in usability, support quality, and overall satisfaction.`;

  return text;
}

function generateUseCaseSection(toolA, toolB, seed) {
  const bestForA = (toolA.best_for || []).map(b => b.replace(/-/g, ' ')).join(', ');
  const bestForB = (toolB.best_for || []).map(b => b.replace(/-/g, ' ')).join(', ');

  let text = `The ideal user for each platform differs considerably. `;
  text += `${toolA.name} is best suited for ${bestForA || 'general use'}, `;
  text += `making it a strong choice if you fall into ${toolA.best_for?.length > 1 ? 'any of these categories' : 'this category'}. `;
  text += `${toolB.name}, meanwhile, shines for ${bestForB || 'general use'}, `;
  text += `which means it may be the better pick if your needs align with ${toolB.best_for?.length > 1 ? 'those use cases' : 'that use case'}.\n\n`;

  text += `Founded in ${toolA.founded}, ${toolA.name} describes itself as "${toolA.tagline}." `;
  text += `${toolB.name}, established in ${toolB.founded}, positions itself as "${toolB.tagline}." `;

  const ageDiff = Math.abs((toolA.founded || 2020) - (toolB.founded || 2020));
  if (ageDiff > 5) {
    const older = toolA.founded < toolB.founded ? toolA : toolB;
    const newer = older.slug === toolA.slug ? toolB : toolA;
    text += `With ${ageDiff} years between them, ${older.name} brings the maturity and proven track record of a veteran platform, while ${newer.name} offers the fresh perspective and modern architecture of a newer entrant.`;
  } else {
    text += `Both platforms have been in the market for a similar duration, giving each ample time to refine their offerings and build a loyal user base.`;
  }

  return text;
}

function generateVerdict(winner, loser, reasons, toolA, toolB) {
  return `After analyzing all the data, **${winner.name}** comes out slightly ahead in this comparison, thanks to ${reasons.join(', ')}. However, this does not mean ${loser.name} is a poor choice — far from it. ${loser.name} excels in its own right, particularly for ${(loser.best_for || ['specific use cases']).slice(0, 2).map(b => b.replace(/-/g, ' ')).join(' and ')}.\n\nOur recommendation: if you value ${winner.pros?.[0]?.toLowerCase() || 'overall quality'}, go with ${winner.name}. If ${loser.pros?.[0]?.toLowerCase() || 'specific features'} matters more to you, ${loser.name} is the way to go. Either way, both are solid platforms that have earned their place in the market.`;
}

function generateFAQs(toolA, toolB, winner, scoreA, scoreB) {
  return [
    {
      question: `Is ${toolA.name} better than ${toolB.name}?`,
      answer: `It depends on your needs. ${toolA.name} scores ${scoreA.toFixed(1)} overall while ${toolB.name} scores ${scoreB.toFixed(1)}. ${toolA.name} is best for ${(toolA.best_for || []).slice(0, 2).join(' and ')}, while ${toolB.name} excels for ${(toolB.best_for || []).slice(0, 2).join(' and ')}.`,
    },
    {
      question: `Which is cheaper, ${toolA.name} or ${toolB.name}?`,
      answer: `${toolA.name} starts at ${toolA.pricing_starts || 'contact for pricing'} and ${toolB.name} starts at ${toolB.pricing_starts || 'contact for pricing'}. ${toolA.free_plan ? `${toolA.name} offers a free plan.` : ''} ${toolB.free_plan ? `${toolB.name} offers a free plan.` : ''} Overall value depends on which features you need.`,
    },
    {
      question: `Can I switch from ${toolA.name} to ${toolB.name}?`,
      answer: `Yes, most users can migrate between these platforms. Both ${toolA.name} and ${toolB.name} support data import/export. The migration process typically involves exporting your data from one platform and importing it into the other. Some tools also offer migration assistance to make the transition smoother.`,
    },
    {
      question: `What do users say about ${toolA.name} vs ${toolB.name}?`,
      answer: `On review platforms, ${toolA.name} holds a ${toolA.g2_rating} rating on G2 and ${toolA.capterra_rating} on Capterra. ${toolB.name} has a ${toolB.g2_rating} on G2 and ${toolB.capterra_rating} on Capterra. Users praise ${toolA.name} for ${toolA.pros?.[0]?.toLowerCase() || 'its features'} and ${toolB.name} for ${toolB.pros?.[0]?.toLowerCase() || 'its capabilities'}.`,
    },
    {
      question: `Which should I choose in 2026, ${toolA.name} or ${toolB.name}?`,
      answer: `In 2026, we recommend ${winner.name} for most users based on its overall score and feature set. However, ${toolA.slug === winner.slug ? toolB.name : toolA.name} remains a strong contender, especially if you prioritize ${(toolA.slug === winner.slug ? toolB : toolA).pros?.[0]?.toLowerCase() || 'specific strengths'}. Try both free trials before committing.`,
    },
  ];
}
