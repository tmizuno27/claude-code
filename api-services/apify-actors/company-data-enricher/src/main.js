import { Actor, log } from 'apify';
import { enrichDomain, lookupDomain, searchCompanies, getWikidataEntity } from './enricher.js';

await Actor.init();

const input = await Actor.getInput();

const domains = input?.domains ?? [];
const queries = input?.queries ?? [];
const wikidataIds = input?.wikidataIds ?? [];
const mode = input?.mode ?? 'enrich';
const delayMs = input?.delayMs ?? 1000;

const totalItems = domains.length + queries.length + wikidataIds.length;
if (totalItems === 0) {
  throw new Error('Input must contain at least one item in "domains", "queries", or "wikidataIds".');
}

log.info(`Starting Company Data Enricher — ${domains.length} domain(s), ${queries.length} search query(ies), ${wikidataIds.length} Wikidata ID(s). Mode: ${mode}`);

const dataset = await Actor.openDataset();

// --- Process domains ---
for (let i = 0; i < domains.length; i++) {
  const domain = domains[i].trim().replace(/^https?:\/\//, '').replace(/\/.*$/, '');

  if (!domain) {
    await dataset.pushData({ input: domains[i], success: false, error: 'Empty domain after normalization' });
    log.warning(`Skipping empty domain entry at index ${i}`);
    continue;
  }

  log.info(`[${i + 1}/${domains.length}] Enriching domain: ${domain}`);

  try {
    let result;
    if (mode === 'domain') {
      result = await lookupDomain(domain);
    } else {
      result = await enrichDomain(domain);
    }
    await dataset.pushData({ success: true, ...result });
    log.info(`Done: ${domain}`);
  } catch (err) {
    await dataset.pushData({ success: false, type: mode, domain, error: err.message });
    log.error(`Failed to process domain ${domain}: ${err.message}`);
  }

  if (delayMs > 0 && (i < domains.length - 1 || queries.length > 0 || wikidataIds.length > 0)) {
    await new Promise((r) => setTimeout(r, delayMs));
  }
}

// --- Process search queries ---
for (let i = 0; i < queries.length; i++) {
  const query = queries[i].trim();

  if (!query) {
    await dataset.pushData({ input: queries[i], success: false, error: 'Empty query' });
    log.warning(`Skipping empty query at index ${i}`);
    continue;
  }

  log.info(`[${i + 1}/${queries.length}] Searching companies: "${query}"`);

  try {
    const result = await searchCompanies(query);
    await dataset.pushData({ success: true, ...result });
    log.info(`Found ${result.count} result(s) for: ${query}`);
  } catch (err) {
    await dataset.pushData({ success: false, type: 'search', query, error: err.message });
    log.error(`Failed to search "${query}": ${err.message}`);
  }

  if (delayMs > 0 && (i < queries.length - 1 || wikidataIds.length > 0)) {
    await new Promise((r) => setTimeout(r, delayMs));
  }
}

// --- Process Wikidata IDs ---
for (let i = 0; i < wikidataIds.length; i++) {
  const wikidataId = wikidataIds[i].trim();

  if (!wikidataId) {
    await dataset.pushData({ input: wikidataIds[i], success: false, error: 'Empty Wikidata ID' });
    log.warning(`Skipping empty Wikidata ID at index ${i}`);
    continue;
  }

  log.info(`[${i + 1}/${wikidataIds.length}] Fetching Wikidata entity: ${wikidataId}`);

  try {
    const result = await getWikidataEntity(wikidataId);
    await dataset.pushData({ success: true, ...result });
    log.info(`Done: ${wikidataId} — ${result.name ?? 'unknown'}`);
  } catch (err) {
    await dataset.pushData({ success: false, type: 'wikidata', wikidataId, error: err.message });
    log.error(`Failed to fetch ${wikidataId}: ${err.message}`);
  }

  if (delayMs > 0 && i < wikidataIds.length - 1) {
    await new Promise((r) => setTimeout(r, delayMs));
  }
}

log.info(`All done. Processed ${totalItems} item(s).`);

await Actor.exit();
