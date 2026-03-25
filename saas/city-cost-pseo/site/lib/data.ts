import citiesData from '@/data/cities.json';

export interface CityData {
  slug: string;
  name: string;
  country: string;
  region: string;
  currency: string;
  costs: {
    rent1br_center: number;
    rent1br_outside: number;
    meal_inexpensive: number;
    meal_mid: number;
    monthly_pass: number;
    utilities: number;
    internet: number;
    groceries_monthly: number;
  };
  salary_avg_monthly: number;
  safety_index: number;
  description: string;
  tips: string[];
}

export const cities: CityData[] = citiesData as CityData[];

export function getCityBySlug(slug: string): CityData | undefined {
  return cities.find(c => c.slug === slug);
}

export function getCitiesByRegion(region: string): CityData[] {
  return cities.filter(c => c.region === region);
}

export function getAllRegions(): string[] {
  return [...new Set(cities.map(c => c.region))].sort();
}

export function getRegionLabel(region: string): string {
  const labels: Record<string, string> = {
    'asia': 'Asia',
    'southeast-asia': 'Southeast Asia',
    'south-america': 'South America',
    'north-america': 'North America',
    'europe': 'Europe',
    'oceania': 'Oceania',
    'middle-east': 'Middle East',
    'africa': 'Africa',
  };
  return labels[region] ?? region;
}

export function getTotalMonthlyCost(city: CityData): number {
  const { costs } = city;
  return costs.rent1br_center + costs.meal_inexpensive * 30 + costs.monthly_pass +
    costs.utilities + costs.internet + costs.groceries_monthly;
}

export function getAllComparisons(): Array<{ city1: string; city2: string }> {
  const pairs: Array<{ city1: string; city2: string }> = [];
  const popular = cities.slice(0, 20);
  for (let i = 0; i < popular.length; i++) {
    for (let j = i + 1; j < popular.length; j++) {
      pairs.push({ city1: popular[i].slug, city2: popular[j].slug });
    }
  }
  return pairs;
}
