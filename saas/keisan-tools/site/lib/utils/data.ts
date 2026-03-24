import fs from 'fs';
import path from 'path';

export interface CategoryData {
  slug: string;
  name: string;
  description: string;
  icon: string;
  subcategories: { slug: string; name: string }[];
}

export interface CalculatorInput {
  id: string;
  label: string;
  type: 'number' | 'slider' | 'select' | 'date';
  unit?: string;
  default: number | string;
  min?: number;
  max?: number;
  step?: number;
  hint?: string;
  options?: { value: string; label: string }[];
}

export interface CalculatorOutput {
  id: string;
  label: string;
  format: string;
  primary?: boolean;
}

export interface FAQItem {
  question: string;
  answer: string;
}

export interface CalculatorData {
  slug: string;
  category: string;
  subcategory: string;
  title: string;
  description: string;
  metaTitle?: string;
  metaDescription?: string;
  calculatorFunction: string;
  inputs: CalculatorInput[];
  outputs: CalculatorOutput[];
  explanation?: string;
  faq: FAQItem[];
  related: string[];
  popular?: boolean;
  popularOrder?: number;
  seo?: { h1?: string; metaDescription?: string };
  affiliate?: { text: string; category: string };
}

const DATA_DIR = path.join(process.cwd(), 'data');

export function getCategories(): CategoryData[] {
  const raw = fs.readFileSync(path.join(DATA_DIR, 'categories.json'), 'utf-8');
  return JSON.parse(raw);
}

export function getAllCalculators(): CalculatorData[] {
  const calcDir = path.join(DATA_DIR, 'calculators');
  const results: CalculatorData[] = [];

  if (!fs.existsSync(calcDir)) return results;

  const categories = fs.readdirSync(calcDir);
  for (const cat of categories) {
    const catPath = path.join(calcDir, cat);
    if (!fs.statSync(catPath).isDirectory()) continue;

    const subcats = fs.readdirSync(catPath);
    for (const sub of subcats) {
      const subPath = path.join(catPath, sub);
      if (!fs.statSync(subPath).isDirectory()) continue;

      const files = fs.readdirSync(subPath).filter(f => f.endsWith('.json'));
      for (const file of files) {
        const raw = fs.readFileSync(path.join(subPath, file), 'utf-8');
        const data = JSON.parse(raw);
        results.push(normalizeCalculator(data, cat, sub, file.replace('.json', '')));
      }
    }
  }

  return results;
}

function normalizeCalculator(
  data: Record<string, unknown>,
  category: string,
  subcategory: string,
  fileSlug: string
): CalculatorData {
  // Handle both "slug"/"id" field naming
  const slug = (data.slug || data.id || fileSlug) as string;
  const calcFunction = (data.calculatorFunction || data.calculator || slug) as string;

  // Normalize FAQ format (q/a vs question/answer)
  const rawFaq = (data.faq || []) as Record<string, string>[];
  const faq: FAQItem[] = rawFaq.map(item => ({
    question: item.question || item.q || '',
    answer: item.answer || item.a || '',
  }));

  const seo = data.seo as { h1?: string; metaDescription?: string } | undefined;

  return {
    slug,
    category: (data.category as string) || category,
    subcategory: (data.subcategory as string) || subcategory,
    title: data.title as string,
    description: data.description as string,
    metaTitle: (data.metaTitle as string) || seo?.h1 || undefined,
    metaDescription: (data.metaDescription as string) || seo?.metaDescription || undefined,
    calculatorFunction: calcFunction,
    inputs: data.inputs as CalculatorInput[],
    outputs: data.outputs as CalculatorOutput[],
    explanation: data.explanation as string | undefined,
    faq,
    related: (data.related || []) as string[],
    popular: data.popular as boolean | undefined,
    popularOrder: data.popularOrder as number | undefined,
    seo: seo,
    affiliate: data.affiliate as { text: string; category: string } | undefined,
  };
}

export function getCalculatorsByCategory(categorySlug: string): CalculatorData[] {
  return getAllCalculators().filter(c => c.category === categorySlug);
}

export function getCalculator(categorySlug: string, calcSlug: string): CalculatorData | undefined {
  return getAllCalculators().find(c => c.category === categorySlug && c.slug === calcSlug);
}

export function getPopularCalculators(): CalculatorData[] {
  return getAllCalculators()
    .filter(c => c.popular)
    .sort((a, b) => (a.popularOrder ?? 999) - (b.popularOrder ?? 999));
}

export function findCalculatorBySlug(slug: string): CalculatorData | undefined {
  return getAllCalculators().find(c => c.slug === slug);
}
