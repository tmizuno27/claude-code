import puppeteer from 'puppeteer';
import path from 'path';
import { fileURLToPath } from 'url';

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const outDir = path.join(__dirname, '..', 'design');

const urls = [
  { url: 'https://nambei-oyaji.com/paraguay-food-culture/', name: 'food' },
  { url: 'https://nambei-oyaji.com/international-money-transfer-comparison/', name: 'transfer' },
  { url: 'https://nambei-oyaji.com/working-after-moving-abroad/', name: 'work' },
];

(async () => {
  const browser = await puppeteer.launch({ headless: true, args: ['--no-sandbox'] });

  for (const { url, name } of urls) {
    const page = await browser.newPage();
    await page.setViewport({ width: 1400, height: 900, deviceScaleFactor: 1 });
    await page.goto(url, { waitUntil: 'networkidle2', timeout: 30000 });
    await new Promise(r => setTimeout(r, 2000));

    // Top
    await page.screenshot({ path: path.join(outDir, `ss-${name}-top.png`), fullPage: false });

    // Scrolled
    await page.evaluate(() => window.scrollTo(0, 4000));
    await new Promise(r => setTimeout(r, 1000));
    await page.screenshot({ path: path.join(outDir, `ss-${name}-mid.png`), fullPage: false });

    console.log(`${name}: done`);
    await page.close();
  }

  await browser.close();
})();
