import { Actor, log } from 'apify';
import { detectPlatform, isValidUrl, SUPPORTED_PLATFORMS } from './utils.js';
import { extract } from './extractors.js';

await Actor.init();

const input = await Actor.getInput();
if (!input?.urls || !Array.isArray(input.urls) || input.urls.length === 0) {
  throw new Error('Input must contain a non-empty "urls" array.');
}

const includeMetadata = input.includeMetadata !== false;

log.info(`Processing ${input.urls.length} URL(s)...`);

const dataset = await Actor.openDataset();

for (const url of input.urls) {
  if (!isValidUrl(url)) {
    await dataset.pushData({
      url,
      success: false,
      error: 'Invalid URL format',
    });
    log.warning(`Skipping invalid URL: ${url}`);
    continue;
  }

  const platform = detectPlatform(url);
  if (!platform) {
    await dataset.pushData({
      url,
      success: false,
      error: 'Unsupported platform',
      supported_platforms: SUPPORTED_PLATFORMS.map((p) => p.id),
    });
    log.warning(`Unsupported platform for URL: ${url}`);
    continue;
  }

  log.info(`Extracting from ${platform}: ${url}`);

  const result = await extract(platform, url);

  if (!includeMetadata && result.success) {
    await dataset.pushData({
      url,
      success: true,
      platform: result.platform,
      video_url: result.video_url,
    });
  } else {
    await dataset.pushData({ url, ...result });
  }

  // Small delay between requests to be polite
  if (input.urls.length > 1) {
    await new Promise((r) => setTimeout(r, 1000));
  }
}

log.info('Done. All URLs processed.');

await Actor.exit();
