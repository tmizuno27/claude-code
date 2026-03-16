import fs from 'fs';
import path from 'path';

const CATEGORY_META = {
  'email-marketing': { name: 'Email Marketing', emoji: '📧', description: 'Email marketing platforms and automation tools' },
  'ai-writing': { name: 'AI Writing', emoji: '✍️', description: 'AI-powered writing and content generation tools' },
  'ai-image': { name: 'AI Image Generation', emoji: '🎨', description: 'AI image generation and editing tools' },
  'ai-chatbot': { name: 'AI Chatbots', emoji: '💬', description: 'AI chatbot and conversational AI platforms' },
  'ai-coding': { name: 'AI Coding', emoji: '💻', description: 'AI-powered coding assistants and IDEs' },
  'ai-video': { name: 'AI Video', emoji: '🎬', description: 'AI video generation and editing tools' },
  'ai-audio': { name: 'AI Audio & Music', emoji: '🎵', description: 'AI voice, audio, and music generation tools' },
  'ai-automation': { name: 'AI Automation', emoji: '⚡', description: 'AI-powered automation and workflow tools' },
  'ai-nocode': { name: 'AI No-Code & Automation', emoji: '⚡', description: 'No-code automation and workflow tools' },
  'ai-customer-service': { name: 'AI Customer Service', emoji: '🎧', description: 'AI-powered customer service and support tools' },
  'ai-seo': { name: 'AI SEO & Marketing', emoji: '📊', description: 'AI-powered SEO and marketing tools' },
  'ai-translation': { name: 'AI Translation', emoji: '🌐', description: 'AI translation and localization tools' },
  'ai-design': { name: 'AI Design', emoji: '🖌️', description: 'AI-powered design and creative tools' },
  'ai-productivity': { name: 'AI Productivity', emoji: '🚀', description: 'AI productivity and workspace tools' },
};

let cachedData = null;

function loadData() {
  if (cachedData) return cachedData;
  const filePath = path.join(process.cwd(), '..', 'data', 'tools.json');
  const raw = fs.readFileSync(filePath, 'utf-8');
  const json = JSON.parse(raw);

  // tools.json is a flat array of tools, each with a "category" field
  const allTools = Array.isArray(json) ? json : [];
  const categoryMap = {};

  for (const tool of allTools) {
    const catSlug = tool.category;
    if (!categoryMap[catSlug]) {
      const meta = CATEGORY_META[catSlug] || { name: catSlug, emoji: '🔧', description: '' };
      categoryMap[catSlug] = {
        slug: catSlug,
        ...meta,
        tools: [],
      };
    }
    categoryMap[catSlug].tools.push(tool.slug);
  }

  cachedData = { allTools, categoryMap };
  return cachedData;
}

export function getTools() {
  return loadData().allTools;
}

export function getCategories() {
  return loadData().categoryMap;
}

export function getCategoryList() {
  const map = getCategories();
  return Object.values(map);
}

export function getToolBySlug(slug) {
  return getTools().find(t => t.slug === slug) || null;
}

export function getToolsByCategory(categorySlug) {
  return getTools().filter(t => t.category === categorySlug);
}

export function getCategoryBySlug(slug) {
  return getCategories()[slug] || null;
}

export function getComparisonSlug(toolA, toolB) {
  const slugs = [toolA.slug, toolB.slug].sort();
  return `${slugs[0]}-vs-${slugs[1]}`;
}

export function getComparisonPairs() {
  const categories = getCategories();
  const pairs = [];

  for (const catSlug of Object.keys(categories)) {
    const tools = getToolsByCategory(catSlug);
    for (let i = 0; i < tools.length; i++) {
      for (let j = i + 1; j < tools.length; j++) {
        const [a, b] = [tools[i], tools[j]].sort((x, y) => x.slug.localeCompare(y.slug));
        pairs.push({
          slug: `${a.slug}-vs-${b.slug}`,
          toolA: a,
          toolB: b,
          category: catSlug,
        });
      }
    }
  }

  return pairs;
}

export function getRelatedComparisons(toolSlug, limit = 6) {
  return getComparisonPairs()
    .filter(p => p.toolA.slug === toolSlug || p.toolB.slug === toolSlug)
    .slice(0, limit);
}

export function getFeatureLabel(key) {
  const labels = {
    email_builder: 'Email Builder',
    automation: 'Automation',
    landing_pages: 'Landing Pages',
    crm: 'CRM',
    analytics: 'Analytics',
    ab_testing: 'A/B Testing',
    segmentation: 'Segmentation',
    templates: 'Templates',
    sms: 'SMS Marketing',
    social_posting: 'Social Posting',
  };
  return labels[key] || key.replace(/_/g, ' ').replace(/\b\w/g, c => c.toUpperCase());
}
