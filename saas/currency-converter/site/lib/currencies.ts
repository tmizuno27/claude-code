import currenciesData from '@/data/currencies.json';

export interface Currency {
  code: string;
  name: string;
  symbol: string;
  flag: string;
  country: string;
  region: string;
  description: string;
  funFact: string;
}

export interface ExchangeRates {
  base: string;
  date: string;
  rates: Record<string, number>;
}

let ratesCache: ExchangeRates | null = null;

export function getCurrencies(): readonly Currency[] {
  return currenciesData as Currency[];
}

export function getCurrency(code: string): Currency | undefined {
  return getCurrencies().find(c => c.code === code);
}

export function getCurrencyCodes(): readonly string[] {
  return getCurrencies().map(c => c.code);
}

export function getAllPairs(): readonly { from: string; to: string }[] {
  const codes = getCurrencyCodes();
  const pairs: { from: string; to: string }[] = [];
  for (const from of codes) {
    for (const to of codes) {
      if (from !== to) {
        pairs.push({ from, to });
      }
    }
  }
  return pairs;
}

export function getRates(): ExchangeRates {
  if (ratesCache) return ratesCache;
  try {
    // eslint-disable-next-line @typescript-eslint/no-require-imports
    const data = require('@/data/rates.json');
    ratesCache = data as ExchangeRates;
    return ratesCache;
  } catch {
    // Fallback rates if fetch hasn't run yet
    return {
      base: 'USD',
      date: new Date().toISOString().slice(0, 10),
      rates: { USD: 1, EUR: 0.92, GBP: 0.79, JPY: 150.5, CHF: 0.88, CAD: 1.36, AUD: 1.53, NZD: 1.67, CNY: 7.24, HKD: 7.82, SGD: 1.34, SEK: 10.42, NOK: 10.65, DKK: 6.87, KRW: 1330, INR: 83.1, BRL: 4.97, MXN: 17.15, ZAR: 18.65, TRY: 30.5, RUB: 91.5, PLN: 3.98, THB: 35.2, IDR: 15600, MYR: 4.72, PHP: 55.8, CZK: 22.8, ILS: 3.65, AED: 3.67, SAR: 3.75 },
    };
  }
}

export function convert(amount: number, from: string, to: string): number {
  const rates = getRates();
  const fromRate = from === rates.base ? 1 : rates.rates[from];
  const toRate = to === rates.base ? 1 : rates.rates[to];
  if (!fromRate || !toRate) return 0;
  return (amount / fromRate) * toRate;
}

export function formatRate(rate: number): string {
  if (rate >= 1000) return rate.toFixed(2);
  if (rate >= 100) return rate.toFixed(3);
  if (rate >= 1) return rate.toFixed(4);
  return rate.toFixed(6);
}

export function pairToSlug(from: string, to: string): string {
  return `${from.toLowerCase()}-to-${to.toLowerCase()}`;
}

export function slugToPair(slug: string): { from: string; to: string } | null {
  const match = slug.match(/^([a-z]{3})-to-([a-z]{3})$/);
  if (!match) return null;
  return { from: match[1].toUpperCase(), to: match[2].toUpperCase() };
}

/** Common conversion amounts for display */
export function getCommonAmounts(from: string, to: string): { amount: number; result: number }[] {
  const amounts = [1, 5, 10, 25, 50, 100, 250, 500, 1000, 5000, 10000];
  return amounts.map(amount => ({
    amount,
    result: convert(amount, from, to),
  }));
}
