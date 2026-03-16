import { Actor, log } from 'apify';
import {
  googleDaily,
  hackerNewsTrending,
  redditTrending,
  githubTrending,
  productHuntToday,
} from './sources.js';

await Actor.init();

const input = await Actor.getInput();

const ALL_SOURCES = ['google', 'hackernews', 'reddit', 'github', 'producthunt'];

// Default to all sources if none specified
const sources =
  Array.isArray(input?.sources) && input.sources.length > 0 ? input.sources : ALL_SOURCES;

const googleGeo = input?.googleGeo || 'US';
const limit = Math.min(Math.max(Number(input?.limit) || 25, 1), 50);

log.info(`Fetching trends from sources: ${sources.join(', ')} (limit: ${limit})`);

const dataset = await Actor.openDataset();

const fetchers = {
  google: () => googleDaily(googleGeo, limit),
  hackernews: () => hackerNewsTrending(limit),
  reddit: () => redditTrending(limit),
  github: () => githubTrending(limit),
  producthunt: () => productHuntToday(limit),
};

for (const source of sources) {
  if (!fetchers[source]) {
    log.warning(`Unknown source "${source}", skipping.`);
    continue;
  }

  log.info(`Fetching ${source}...`);
  try {
    const result = await fetchers[source]();
    await dataset.pushData(result);
    log.info(`${source}: fetched ${result.count} items.`);
  } catch (err) {
    log.error(`${source} failed: ${err.message}`);
    await dataset.pushData({
      source,
      updated: new Date().toISOString(),
      count: 0,
      items: [],
      error: err.message,
    });
  }

  // Polite delay between sources
  if (sources.indexOf(source) < sources.length - 1) {
    await new Promise((r) => setTimeout(r, 500));
  }
}

log.info('Done. All sources processed.');

await Actor.exit();
