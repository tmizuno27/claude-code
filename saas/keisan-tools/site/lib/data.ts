import fs from "fs";
import path from "path";

// Types
export interface SubCategory {
  slug: string;
  name: string;
}

export interface Category {
  slug: string;
  name: string;
  description: string;
  icon: string;
  subcategories: SubCategory[];
}

export interface InputOption {
  value: string;
  label: string;
}

export interface CalculatorInput {
  id: string;
  label: string;
  type: "number" | "slider" | "select" | "date";
  unit: string | null;
  default: number | string;
  min: number | null;
  max: number | null;
  step: number | null;
  options?: InputOption[];
}

export interface CalculatorOutput {
  id: string;
  label: string;
  format: "currency" | "percent" | "number" | "text";
}

export interface CalculatorChart {
  type: "bar" | "line" | "pie";
  dataKey: string;
}

export interface FAQ {
  q: string;
  a: string;
}

export interface CalculatorAffiliate {
  text: string;
  category: string;
}

export interface CalculatorSEO {
  h1: string;
  metaDescription: string;
}

export interface CalculatorData {
  id: string;
  category: string;
  subcategory: string;
  title: string;
  description: string;
  inputs: CalculatorInput[];
  calculator: string;
  outputs: CalculatorOutput[];
  chart: CalculatorChart | null;
  faq: FAQ[];
  related: string[];
  affiliate: CalculatorAffiliate | null;
  seo: CalculatorSEO;
}

// Module-level cache
const DATA_DIR = path.join(process.cwd(), "data");
let categoriesCache: Category[] | null = null;
let allCalculatorsCache: CalculatorData[] | null = null;

/**
 * Load categories.json
 */
export function loadCategories(): Category[] {
  if (categoriesCache !== null) {
    return categoriesCache;
  }
  const filePath = path.join(DATA_DIR, "categories.json");
  const raw = fs.readFileSync(filePath, "utf-8");
  const categories: Category[] = JSON.parse(raw);
  categoriesCache = categories;
  return categories;
}

/**
 * Load a single calculator JSON by category/subcategory/slug
 */
export function loadCalculator(
  category: string,
  subcategory: string,
  slug: string
): CalculatorData | null {
  const filePath = path.join(
    DATA_DIR,
    "calculators",
    category,
    subcategory,
    `${slug}.json`
  );
  if (!fs.existsSync(filePath)) {
    return null;
  }
  const raw = fs.readFileSync(filePath, "utf-8");
  return JSON.parse(raw) as CalculatorData;
}

/**
 * Scan all calculator JSON files under data/calculators/
 */
export function getAllCalculators(): CalculatorData[] {
  if (allCalculatorsCache !== null) {
    return allCalculatorsCache;
  }

  const calculators: CalculatorData[] = [];
  const calculatorsDir = path.join(DATA_DIR, "calculators");

  if (!fs.existsSync(calculatorsDir)) {
    return calculators;
  }

  const categoryDirs = fs
    .readdirSync(calculatorsDir, { withFileTypes: true })
    .filter((d) => d.isDirectory());

  for (const categoryDir of categoryDirs) {
    const categoryPath = path.join(calculatorsDir, categoryDir.name);
    const subcategoryDirs = fs
      .readdirSync(categoryPath, { withFileTypes: true })
      .filter((d) => d.isDirectory());

    for (const subcategoryDir of subcategoryDirs) {
      const subcategoryPath = path.join(categoryPath, subcategoryDir.name);
      const files = fs
        .readdirSync(subcategoryPath)
        .filter((f) => f.endsWith(".json"));

      for (const file of files) {
        const filePath = path.join(subcategoryPath, file);
        const raw = fs.readFileSync(filePath, "utf-8");
        const data = JSON.parse(raw) as CalculatorData;
        calculators.push(data);
      }
    }
  }

  allCalculatorsCache = calculators;
  return calculators;
}

/**
 * Get calculators filtered by category slug
 */
export function getCalculatorsByCategory(
  categorySlug: string
): CalculatorData[] {
  const all = getAllCalculators();
  return all.filter((c) => c.category === categorySlug);
}

/**
 * Get a single category by slug
 */
export function getCategoryBySlug(slug: string): Category | null {
  const categories = loadCategories();
  return categories.find((c) => c.slug === slug) ?? null;
}
