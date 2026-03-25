/**
 * Fetch latest exchange rates from exchangerate-api.com (free, no key needed)
 * Run before build: node scripts/fetch-rates.mjs
 */
import { writeFileSync } from 'fs';
import { join, dirname } from 'path';
import { fileURLToPath } from 'url';

const __dirname = dirname(fileURLToPath(import.meta.url));
const OUTPUT = join(__dirname, '..', 'data', 'rates.json');

const API_URL = 'https://open.er-api.com/v6/latest/USD';

async function fetchRates() {
  console.log('Fetching latest exchange rates...');
  try {
    const res = await fetch(API_URL);
    if (!res.ok) throw new Error(`HTTP ${res.status}`);
    const data = await res.json();

    const output = {
      base: 'USD',
      date: data.time_last_update_utc?.slice(0, 16) || new Date().toISOString().slice(0, 10),
      rates: data.rates,
    };

    writeFileSync(OUTPUT, JSON.stringify(output, null, 2));
    console.log(`Rates saved to data/rates.json (${Object.keys(data.rates).length} currencies, date: ${output.date})`);
  } catch (err) {
    console.error('Failed to fetch rates:', err.message);
    console.log('Build will use fallback rates.');
  }
}

fetchRates();
