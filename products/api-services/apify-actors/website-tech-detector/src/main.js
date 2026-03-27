import { Actor, log } from 'apify';
import {
  fetchSite,
  detectTechnologies,
  extractMetadata,
  extractSecurityHeaders,
} from './detectors.js';

await Actor.init();

const input = await Actor.getInput();
if (!input?.urls || !Array.isArray(input.urls) || input.urls.length === 0) {
  throw new Error('Input must contain a non-empty "urls" array.');
}

const includeHeaders = input.includeHeaders !== false;
const includeMetadata = input.includeMetadata !== false;
const categoryFilter = Array.isArray(input.categoryFilter) ? input.categoryFilter : [];
const delayMs = Math.min(Math.max(Number(input.delayMs) || 1000, 0), 10000);

log.info(`Scanning ${input.urls.length} URL(s) for technologies...`);

const dataset = await Actor.openDataset();

for (let i = 0; i < input.urls.length; i++) {
  const url = input.urls[i];

  // Validate URL
  try {
    const parsed = new URL(url);
    if (!['http:', 'https:'].includes(parsed.protocol)) {
      await dataset.pushData({ url, success: false, error: 'URL must use http or https' });
      continue;
    }
  } catch {
    await dataset.pushData({ url, success: false, error: 'Invalid URL format' });
    continue;
  }

  try {
    log.info(`[${i + 1}/${input.urls.length}] Scanning: ${url}`);
    const { html, headers, finalUrl } = await fetchSite(url);

    const technologies = detectTechnologies(html, headers, categoryFilter);

    // Group by category
    const byCategory = {};
    for (const tech of technologies) {
      if (!byCategory[tech.category]) {
        byCategory[tech.category] = [];
      }
      byCategory[tech.category].push({ name: tech.name, confidence: tech.confidence });
    }

    const result = {
      url: finalUrl,
      success: true,
      technologiesCount: technologies.length,
      technologies,
      byCategory,
    };

    if (includeMetadata) {
      result.metadata = extractMetadata(html);
    }

    if (includeHeaders) {
      result.securityHeaders = extractSecurityHeaders(headers);
      result.server = headers['server'] || null;
    }

    await dataset.pushData(result);
    log.info(`  Found ${technologies.length} technologies.`);
  } catch (e) {
    log.warning(`Failed to scan ${url}: ${e.message}`);
    await dataset.pushData({ url, success: false, error: e.message });
  }

  // Delay between requests
  if (delayMs > 0 && i < input.urls.length - 1) {
    await new Promise((r) => setTimeout(r, delayMs));
  }
}

log.info('Done. All URLs scanned.');
await Actor.exit();
